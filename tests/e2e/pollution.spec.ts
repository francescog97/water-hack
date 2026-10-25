import {test,expect} from '@playwright/test';

test('pollution exercise persists verification, gated review, named actions, outcome and export',async({page})=>{
 await page.goto('/?lang=en');
 await expect(page.getByRole('heading',{name:'A signal. A verified next step.'})).toBeVisible();
 await expect(page.locator('.nav-measurement')).toContainText('96');
 await expect(page.locator('.nav-main')).toContainText('No actual laboratory analysis exists.');
 const newExercise=page.getByRole('button',{name:'New exercise',exact:true});
 if(await newExercise.count())await newExercise.click();else await page.getByRole('button',{name:'Start incident record',exact:true}).click();
 await expect(newExercise).toBeVisible();
 await page.getByRole('button',{name:'Potential receptors',exact:true}).click();
 await expect(page.locator('.nav-receptor')).toHaveCount(4);
 await expect(page.getByRole('img')).toHaveAccessibleName('Illustrative river reach with unverified downstream receptors');
 await expect(page.locator('.nav-main')).toContainText('Propagation forecast unavailable');
 await page.getByRole('button',{name:'Institutions & legal checks',exact:true}).click();
 await expect(page.locator('.nav-legal-list > div')).toHaveCount(5);
 await expect(page.locator('.nav-main')).toContainText('Legal applicability gate remains closed');
 await page.locator('.nav-source-card').first().click();
 const source=page.getByRole('dialog');
 await expect(source).toContainText('Pending · applicable dates and scope unverified');
 await expect(source.getByRole('link',{name:'Open original source'})).toHaveAttribute('href',/^https:\/\//);
 await page.keyboard.press('Escape');
 await page.getByRole('button',{name:'Action plan & history',exact:true}).click();
 const approve=page.getByRole('button',{name:'Approve demonstration plan'});
 await expect(approve).toBeDisabled();
 const tasks=page.locator('.nav-task');
 // Response execution is unavailable until all required evidence and explicit review exist.
 await tasks.nth(5).getByRole('button',{name:'Update task & evidence'}).click();
 await expect(page.getByRole('dialog').getByLabel('Task status')).toHaveValue('completed');
 await expect(page.getByRole('dialog').getByRole('button',{name:'Save task and evidence'})).toBeDisabled();
 await page.keyboard.press('Escape');
 async function update(index:number,status:string,note:string){
  await tasks.nth(index).getByRole('button',{name:'Update task & evidence'}).click();
  const dialog=page.getByRole('dialog');
  await dialog.getByLabel('Assignee name',{exact:true}).fill('Hackathon reviewer');
  await dialog.getByLabel('Self-declared demonstration role',{exact:true}).fill('Simulated case coordinator');
  await dialog.getByLabel('Task status').selectOption(status);
  if(index===0)await dialog.getByLabel('Optional internal target').fill('2026-10-26T09:00');
  await dialog.getByRole('textbox',{name:status==='rejected'?'Rejection reason':'Evidence note / reason',exact:true}).fill(note);
  await dialog.getByRole('button',{name:'Save task and evidence'}).click();
  await expect(dialog).toHaveCount(0);
 }
 for(let i=0;i<5;i++)await update(i,'completed',`Demo check ${i+1}: source inspected; actual laboratory, legal and jurisdiction validation remain pending.`);
 await page.reload();
 await page.getByRole('button',{name:'Action plan & history',exact:true}).click();
 await expect(page.locator('.nav-workflow-summary')).toContainText('5 / 5');
 await page.getByLabel('Review reasoning').fill('Demonstration plan only. No actual contamination or legal applicability has been verified.');
 await page.getByRole('checkbox').check();
 await approve.click();
 await expect(page.locator('.nav-workflow-summary')).toContainText('Demo approved');
 await update(5,'in_progress','Demo sampling draft assigned; no real sample request sent.');
 await update(5,'completed','Demo sampling draft prepared; actual laboratory evidence is absent.');
 await update(6,'rejected','Recipient competence remains unverified; notification draft rejected for this exercise.');
 await update(7,'completed','Demo follow-up recorded; actual pollution finding remains unconfirmed.');
 await page.getByLabel('Outcome evidence and follow-up').fill('Exercise closed unconfirmed. No real pollution, notification or official authority asserted.');
 await page.getByRole('button',{name:'Close as unconfirmed'}).click();
 await expect(page.locator('.nav-workflow-summary')).toContainText('closed unconfirmed');
 const pending=page.waitForEvent('download');
 await page.getByRole('button',{name:'Export full evidence JSON'}).click();
 const download=await pending, stream=await download.createReadStream(), chunks:Buffer[]=[];
 for await(const chunk of stream!)chunks.push(Buffer.from(chunk));
 const result=JSON.parse(Buffer.concat(chunks).toString());
 expect(result.official_authorization).toBe(false);
 expect(result.dispatch_available).toBe(false);
 expect(result.incident.status).toBe('closed_unconfirmed');
 expect(result.incident.finding_status).toBe('UNCONFIRMED_ANOMALY');
 expect(result.incident.tasks[6].status).toBe('rejected');
 expect(result.incident.tasks[5].assignee_name).toBe('Hackathon reviewer');
 expect(result.incident.tasks[0].internal_target_at).toMatch(/^2026-10-26T/);
 expect(result.incident.timeline.length).toBeGreaterThanOrEqual(12);
 expect(result.incident.scenario.sources.every((s:{verification:string})=>s.verification!=='VERIFIED_APPLICABLE')).toBe(true);
 await page.reload();
 await page.getByRole('button',{name:'Action plan & history',exact:true}).click();
 await expect(page.locator('.nav-workflow-summary')).toContainText('closed unconfirmed');
 await page.screenshot({path:'test-results/pollution-workflow-desktop.png',fullPage:true});
});

test('navigator changes all four languages on mobile and retains the incident',async({page})=>{
 await page.goto('/?lang=en');
 await expect(page.locator('h1')).toHaveText('A signal. A verified next step.');
 const incident=(await page.locator('.nav-record-id').innerText()).split('·')[0].trim();
 await page.setViewportSize({width:390,height:844});
 for(const language of ['it','ru','bg','en']){
  await page.getByTestId('language-select').selectOption(language);
  await expect(page.locator('html')).toHaveAttribute('lang',language);
  if(language!=='en')await expect(page.locator('h1')).not.toHaveText('A signal. A verified next step.');
  await expect(page.locator('.nav-record-id')).toContainText(incident);
  expect(await page.evaluate(()=>document.documentElement.scrollWidth)).toBeLessThanOrEqual(390);
 }
 await page.screenshot({path:'test-results/pollution-mobile.png',fullPage:true});
});

test('Italian nine-slide pitch supports keyboard navigation, notes and mobile',async({page})=>{
 await page.goto('/presentation.html');
 await expect(page.locator('article.active h1')).toContainText('Un segnale');
 await page.getByRole('button',{name:'Note del relatore'}).click();
 await expect(page.locator('article.active aside')).toBeVisible();
 await page.keyboard.press('ArrowRight');
 await expect(page.locator('#counter')).toHaveText('2 / 9');
 await expect(page.locator('article.active')).toContainText('valori inventati');
 await page.goto('/presentation.html#6');
 await expect(page.locator('article.active')).toContainText('−€5.000');
 await page.setViewportSize({width:390,height:844});
 expect(await page.evaluate(()=>document.documentElement.scrollWidth)).toBeLessThanOrEqual(390);
 await page.screenshot({path:'test-results/pitch-slide-six-mobile.png',fullPage:true});
});

test('missing pollution configuration shows an error without invented fallback',async({page})=>{
 await page.route('**/api/incidents/scenario',route=>route.fulfill({status:422,json:{detail:'Demonstration configuration unavailable or malformed; no replacement evidence invented'}}));
 await page.goto('/?lang=en');
 await expect(page.getByRole('alert')).toContainText('no replacement evidence invented');
 await expect(page.getByRole('button',{name:'Start incident record'})).toBeDisabled();
 await expect(page.locator('.nav-measurement')).toHaveCount(0);
});
