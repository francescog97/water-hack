import {test,expect} from '@playwright/test';

test.beforeEach(async({context})=>{
 // Prove offline runtime: public links may be inspected, but the app cannot fetch remote services.
 await context.route('**/*',route=>{const url=new URL(route.request().url());return ['127.0.0.1','localhost'].includes(url.hostname)?route.continue():route.abort();});
});

test('historical evidence → synthetic escalation → source review → draft export',async({page})=>{
 const errors:string[]=[];page.on('pageerror',error=>errors.push(error.message));
 await page.goto('/');
 await expect(page.getByRole('heading',{name:'Crisis Monitor',exact:true})).toBeVisible();
 await expect(page.locator('.signal-number')).toContainText('9.922');
 await expect(page.locator('.signal-panel .badge')).toContainText('WARNING');
 await expect(page.getByText('DEMONSTRATION · NOT FOR OPERATIONAL USE',{exact:true})).toBeVisible();
 await page.getByRole('button',{name:'Dataset sources',exact:true}).click();
 await expect(page.getByRole('dialog',{name:'Dataset provenance'})).toContainText('146 observations; 27 missing calendar days');
 await expect(page.getByRole('dialog',{name:'Dataset provenance'})).toContainText('CSV row');
 await page.getByRole('button',{name:'Close dataset provenance'}).click();
 await page.getByRole('button',{name:'Scenario Lab',exact:true}).click();
 await page.getByTestId('simulate').click();
 await expect(page.locator('.scenario-comparison')).toContainText('25.922');
 await expect(page.locator('.scenario-comparison')).toContainText('DANGER');
 await expect(page.locator('.simulation-result')).toContainText('Day +2');
 await expect(page.locator('.recharts-line path').first()).toHaveAttribute('stroke-dasharray','7 5');
 await page.getByRole('button',{name:'Response Navigator',exact:true}).click();
 await expect(page.locator('.response-summary')).toContainText('DANGER');
 await expect(page.getByRole('button',{name:'Download draft briefing',exact:true})).toBeDisabled();
 await expect(page.locator('.procedure-card')).toHaveCount(4);
 await page.locator('.procedure-card .source-link').first().click();
 const drawer=page.getByRole('dialog',{name:'Source evidence'});
 await expect(drawer).toContainText('interpretation unreviewed');
 await expect(drawer.getByRole('link',{name:'Open original source'})).toHaveAttribute('href',/^https:\/\/(civil-protection-humanitarian-aid.ec.europa.eu|www.me.government.bg|www.moew.government.bg)/);
 await page.getByRole('button',{name:'Close evidence',exact:true}).click();
 await page.getByRole('button',{name:'Coverage Matrix',exact:true}).click();
 await page.getByRole('button',{name:'DANGER Deadlines: unmapped',exact:true}).click();
 await expect(page.getByRole('dialog',{name:'Coverage evidence'})).toContainText('does not imply a gap in Bulgarian law');
 await page.getByRole('button',{name:'Close coverage evidence'}).click();
 await page.getByRole('button',{name:'Legal Package & Evidence',exact:true}).click();
 await page.getByRole('combobox',{name:'Rule package'}).selectOption('alternate-demo');
 await page.getByRole('button',{name:'Scenario Lab',exact:true}).click();
 await expect(page.locator('.scenario-comparison')).toContainText('25.922');
 await expect(page.locator('.scenario-comparison .badge').last()).toContainText('WARNING');
 await page.getByRole('button',{name:'Legal Package & Evidence',exact:true}).click();
 await page.getByRole('combobox',{name:'Legal package'}).selectOption('bulgaria-source-only');
 await page.getByRole('button',{name:'Response Navigator',exact:true}).click();
 await expect(page.getByRole('heading',{name:'No procedural mappings loaded'})).toBeVisible();
 await page.getByRole('button',{name:'Legal Package & Evidence',exact:true}).click();
 await page.getByRole('combobox',{name:'Legal package'}).selectOption('bulgaria-flood');
 await page.getByRole('button',{name:'Response Navigator',exact:true}).click();
 await expect(page.locator('.procedure-card')).toHaveCount(4);
 await page.getByRole('textbox',{name:'Review note'}).fill('I checked the historical source. Jurisdiction and current legal interpretation still require expert review.');
 await page.getByRole('button',{name:'Acknowledge this draft context'}).click();
 await expect(page.locator('.review-confirmed')).toBeVisible();
 const downloadPromise=page.waitForEvent('download');
 await page.getByRole('button',{name:'Download draft briefing',exact:true}).click();
 const download=await downloadPromise;
 expect(download.suggestedFilename()).toMatch(/^crisis2action-DRAFT-2025-09-25\.md$/);
 await download.saveAs('test-results/demo-briefing.md');
 await page.getByRole('button',{name:'Preview',exact:true}).click();
 await expect(page.getByRole('dialog',{name:'Draft briefing preview'})).toContainText('UNAPPROVED DRAFT');
 await expect(page.getByRole('dialog',{name:'Draft briefing preview'})).toContainText('https://');
 await page.getByRole('button',{name:'Close briefing preview'}).click();
 await page.getByRole('combobox',{name:'Station',exact:true}).selectOption('iskar-orehovitsa');
 await expect(page.getByRole('button',{name:'Download draft briefing',exact:true})).toBeDisabled();
 expect(errors).toEqual([]);
});

test('missing, stale and unavailable data never generate a forecast or safe classification',async({page})=>{
 await page.goto('/#scenario');
 await expect(page.locator('.scenario-comparison')).toContainText('9.922');
 await page.getByRole('button',{name:'Show a real missing day'}).click();
 await expect(page.locator('.scenario-grid')).toContainText('UNKNOWN · evidence is insufficient');
 await expect(page.locator('.scenario-comparison')).toContainText('Unavailable');
 await page.getByRole('textbox',{name:'Historical date'}).fill('2025-09-25');
 await expect(page.locator('.scenario-comparison')).toContainText('25.922');
 await page.getByRole('switch',{name:'Simulate stale input'}).check();
 await expect(page.locator('.scenario-grid')).toContainText('UNKNOWN · evidence is insufficient');
 await expect(page.locator('.scenario-grid')).toContainText('Stale-input failure injection');
 await page.getByRole('switch',{name:'Simulate stale input'}).uncheck();
 await page.getByRole('switch',{name:'Simulate input unavailable'}).check();
 await expect(page.locator('.scenario-grid')).toContainText('UNKNOWN · evidence is insufficient');
 await page.getByRole('switch',{name:'Simulate input unavailable'}).uncheck();
 await page.getByRole('slider',{name:'Daily increase'}).fill('10');
 await expect(page.locator('.scenario-comparison')).toContainText('29.922');
 await page.getByRole('slider',{name:'Scenario horizon'}).fill('3');
 await expect(page.locator('.scenario-comparison')).toContainText('39.922');
 await page.getByRole('button',{name:'Response Navigator',exact:true}).click();
 await page.getByRole('combobox',{name:'Competent local jurisdiction confirmed'}).selectOption('true');
 await expect(page.locator('.procedure-card').first()).toContainText('Reported met');
 await expect(page.locator('.response-state')).toContainText('Not determined');
 await expect(page.locator('.deadline-line').first()).toContainText('No verified deadline');
});

test('guided tour, screenshots, mobile layout and source protection',async({page,request})=>{
 await page.goto('/');
 await expect(page.locator('.signal-number')).toContainText('9.922');
 await page.screenshot({path:'test-results/overview-desktop.png',fullPage:true});
 await page.getByRole('button',{name:'Start guided demo',exact:true}).click();
 await expect(page.getByRole('region',{name:'Guided demonstration'})).toContainText('1 / 6');
 await page.getByRole('button',{name:'Next',exact:true}).click();
 await expect(page.locator('.scenario-comparison')).toContainText('25.922');
 await page.getByRole('button',{name:'Close guided demo'}).click();
 await page.screenshot({path:'test-results/scenario-desktop.png',fullPage:true});
 await page.getByRole('button',{name:'Coverage Matrix',exact:true}).click();
 await page.screenshot({path:'test-results/coverage-desktop.png',fullPage:true});
 await page.setViewportSize({width:390,height:844});
 await page.getByRole('button',{name:'Crisis Monitor',exact:true}).click();
 await expect(page.locator('.signal-number')).toBeVisible();
 expect(await page.evaluate(()=>document.documentElement.scrollWidth)).toBeLessThanOrEqual(390);
 await page.screenshot({path:'test-results/overview-mobile.png',fullPage:true});
 for(const path of ['/Dataset/portata_iskar_novi_iskar_2025.csv','/runtime/reviews.sqlite3','/Crisis2Action_CODEX_PLAN.md','/t1.png']){
  expect((await request.get(path)).status()).toBe(404);
 }
});

test('complete guided tour and JSON export preserve review semantics',async({page})=>{
 await page.goto('/');
 await expect(page.locator('.signal-number')).toContainText('9.922');
 await page.getByRole('button',{name:'Start guided demo',exact:true}).click();
 for(let step=1;step<6;step++){
  await expect(page.getByRole('region',{name:'Guided demonstration'})).toContainText(`${step} / 6`);
  await page.getByRole('button',{name:'Next',exact:true}).click();
 }
 await expect(page.getByRole('region',{name:'Guided demonstration'})).toContainText('6 / 6');
 await page.getByRole('button',{name:'Finish',exact:true}).click();
 await expect(page.getByRole('region',{name:'Guided demonstration'})).toHaveCount(0);
 await page.getByRole('textbox',{name:'Review note'}).fill('Tour checked; all interpretation and jurisdiction questions remain pending.');
 await page.getByRole('button',{name:'Acknowledge this draft context'}).click();
 await expect(page.locator('.review-confirmed')).toBeVisible();
 const downloaded=page.waitForEvent('download');
 await page.getByRole('button',{name:'JSON evidence',exact:true}).click();
 const file=await downloaded;
 await file.saveAs('test-results/demo-evidence.json');
 expect(file.suggestedFilename()).toMatch(/\.json$/);
 await page.getByRole('button',{name:'Legal Package & Evidence',exact:true}).click();
 await page.getByText('Inspect actual rule JSON',{exact:true}).click();
 await expect(page.locator('.config-details[open] pre')).toContainText('DEMO_CONFIG');
 await page.getByRole('button',{name:'Coverage Matrix',exact:true}).click();
 await page.getByRole('button',{name:'Swap legal package',exact:true}).click();
 await expect(page.getByRole('button',{name:'WARNING Procedures: unmapped',exact:true})).toBeVisible();
});
