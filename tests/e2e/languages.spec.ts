import {test,expect} from '@playwright/test';

test.beforeEach(async({context})=>{
 await context.route('**/*',route=>['127.0.0.1','localhost'].includes(new URL(route.request().url()).hostname)?route.continue():route.abort());
});

test('four languages are visible, persist, and keep an acknowledged scenario intact',async({page})=>{
 let evaluations=0;
 page.on('request',request=>{if(new URL(request.url()).pathname==='/api/evaluate')evaluations++;});
 await page.goto('/#scenario');
 await expect(page.locator('.scenario-comparison')).toContainText('9.922');
 const selector=page.getByTestId('language-select');
 await expect(selector).toBeVisible();
 await expect(selector.locator('option')).toHaveText(['English','Italiano','Русский','Български']);
 await page.getByTestId('simulate').click();
 await expect(page.locator('.scenario-comparison')).toContainText('25.922');
 await page.getByRole('button',{name:'Response Navigator',exact:true}).click();
 await page.getByRole('textbox',{name:'Review note'}).fill('Language test: historical evidence checked; legal interpretation still needs domain review.');
 await page.getByRole('button',{name:'Acknowledge this draft context'}).click();
 await expect(page.locator('.review-confirmed')).toBeVisible();
 const countBefore=evaluations;
 const englishTitle=await page.locator('h1').innerText();
 for(const language of ['it','ru','bg','en']){
  await selector.selectOption(language);
  await expect(page.locator('html')).toHaveAttribute('lang',language);
  await expect(page.locator('.review-confirmed')).toBeVisible();
  await expect(page.locator('.export-actions > button').first()).toBeEnabled();
  if(language!=='en'){
   await expect(page.locator('h1')).not.toHaveText(englishTitle);
   await expect(page.locator('.translation-note')).toBeVisible();
  }
  if(language==='ru'||language==='bg')await expect(page.locator('h1')).toContainText(/[А-Яа-я]/);
 }
 expect(evaluations).toBe(countBefore);
 await selector.selectOption('it');
 await page.reload();
 await expect(selector).toHaveValue('it');
 await expect(page.locator('html')).toHaveAttribute('lang','it');
 // Reload creates a fresh review context in the UI; changing only language did not.
 await expect(page.locator('.export-actions > button').first()).toBeDisabled();
});

test('localized dates and numbers, original sources, and mobile language control',async({page})=>{
 await page.goto('/?lang=ru#scenario');
 await expect(page.getByTestId('language-select')).toHaveValue('ru');
 await expect(page.locator('.scenario-comparison')).toContainText('9,922');
 await page.getByTestId('simulate').click();
 await expect(page.locator('.scenario-comparison')).toContainText('25,922');
 await page.getByTestId('language-select').selectOption('en');
 await page.getByRole('button',{name:'Response Navigator',exact:true}).click();
 await page.locator('.procedure-card .source-link').first().click();
 const original=await page.locator('.source-drawer h2').innerText();
 const originalLink=await page.locator('.source-drawer a[target="_blank"]').getAttribute('href');
 await page.keyboard.press('Escape');
 await page.getByTestId('language-select').selectOption('bg');
 await page.locator('.procedure-card .source-link').first().click();
 await expect(page.locator('.source-drawer h2')).toHaveText(original);
 await expect(page.locator('.source-drawer a[target="_blank"]')).toHaveAttribute('href',originalLink!);
 await page.keyboard.press('Escape');
 await page.setViewportSize({width:390,height:844});
 await expect(page.getByTestId('language-select')).toBeVisible();
 for(const language of ['bg','ru','it','en']){
  await page.getByTestId('language-select').selectOption(language);
  await expect(page.getByTestId('language-select')).toBeInViewport();
  expect(await page.evaluate(()=>document.documentElement.scrollWidth)).toBeLessThanOrEqual(390);
 }
 await page.screenshot({path:'test-results/language-switcher-mobile.png',fullPage:true});
});
