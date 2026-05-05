import {expect, test} from '@playwright/test';

test('dynamic scraping demo', async ({page}) => {
    await page.goto('/login');
    await page.locator('#login-button').click();
    await expect(page).toHaveURL(/.*feed/);
    await expect(page.locator('.product-card').first()).toBeVisible();
    for (let i = 0; i < 4; i++) {
        await page.mouse.wheel(0, 1200);
        await page.waitForTimeout(700);
    }
    expect(await page.locator('.product-card').count()).toBeGreaterThan(10);
});
