import {test,expect} from '@playwright/test';

test.beforeEach(async({page})=>{
  await page.goto('/?lang=en');
  await page.getByRole('button',{name:/^Pilot & value$/i}).click();
  await expect(page.getByTestId('pilot-value')).toBeVisible();
});

test('report economics retain the negative insurance result and reject invalid assumptions',async({page})=>{
  const amount=(digits:string)=>new RegExp(digits.split('').join('[^0-9]*'));
  await expect(page.getByTestId('annual-benefit')).toContainText(amount('17640'));
  await expect(page.getByTestId('annual-cost')).toContainText(amount('14000'));
  await expect(page.getByTestId('annual-net')).toContainText(amount('3640'));
  await page.getByTestId('economic-scenario').selectOption('industry');
  await expect(page.getByTestId('annual-benefit')).toContainText(amount('21600'));
  await expect(page.getByTestId('annual-net')).toContainText(amount('5600'));
  await page.getByTestId('economic-scenario').selectOption('insurance');
  await expect(page.getByTestId('annual-benefit')).toContainText(amount('20000'));
  await expect(page.getByTestId('annual-cost')).toContainText(amount('25000'));
  await expect(page.getByTestId('annual-net')).toContainText(/-.*5[^0-9]*000/);
  await page.getByTestId('economics-probability').fill('101');
  await expect(page.getByTestId('economics-probability')).toHaveAttribute('aria-invalid','true');
  await expect(page.getByTestId('annual-net')).toHaveCount(0);
  await page.getByRole('button',{name:'Reset report assumptions'}).click();
  await page.getByTestId('economics-years').fill('0');
  await expect(page.getByTestId('annual-net')).toHaveCount(0);
});

test('task comparisons start empty and export only explicit self-reported data',async({page})=>{
  const exportButton=page.getByRole('button',{name:'Export self-reported comparison (JSON)'});
  await expect(page.getByTestId('pilot-baseline')).toHaveValue('');
  await expect(page.getByTestId('pilot-mvp')).toHaveValue('');
  await expect(exportButton).toBeDisabled();
  for(const [field,value] of Object.entries({baseline:'100',mvp:'70',critical:'0',citations:'5',correct:'5'}))await page.getByTestId(`pilot-${field}`).fill(value);
  await expect(page.getByTestId('pilot-result')).toContainText('Self-reported comparison: 30.0%');
  await expect(exportButton).toBeEnabled();
  await page.getByTestId('pilot-correct').fill('6');
  await expect(exportButton).toBeDisabled();
  await page.getByTestId('pilot-correct').fill('5');
  const downloadPromise=page.waitForEvent('download');
  await exportButton.click();
  const download=await downloadPromise;
  expect(download.suggestedFilename()).toBe('navigator-self-reported-task-comparison.json');
  const stream=await download.createReadStream();
  const chunks:Buffer[]=[];
  for await(const chunk of stream!)chunks.push(Buffer.from(chunk));
  const data=JSON.parse(Buffer.concat(chunks).toString());
  expect(data.recordType).toContain('self-reported');
  expect(data.timeReductionPercent).toBeCloseTo(30);
  expect(data.criticalJurisdictionErrors).toBe(0);
  expect(data.limitation).toContain('not proof');
});
