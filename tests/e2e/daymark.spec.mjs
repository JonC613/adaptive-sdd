import { expect, test } from "@playwright/test";

async function openFixedDay(page) {
  await page.clock.install({ time: new Date("2026-09-06T12:00:00") });
  await page.goto("/");
}

async function addHabit(page, name) {
  await page.getByLabel("New habit").fill(name);
  await page.getByRole("button", { name: "Add habit" }).click();
}

test("E2E-01 — empty state guides a first-time visitor", async ({ page }) => {
  await openFixedDay(page);
  await expect(page.getByText("Start with one small habit.")).toBeVisible();
  await expect(page.getByLabel("New habit")).toBeVisible();
  await expect(page).toHaveScreenshot("01-empty-state.png", { fullPage: true });
});

test("E2E-02 — a visitor adds habits and records a daily check-in", async ({ page }) => {
  await openFixedDay(page);
  await page.getByLabel("New habit").fill("   ");
  await page.getByRole("button", { name: "Add habit" }).click();
  await expect(page.getByRole("status")).toHaveText("Enter a habit name first.");
  await addHabit(page, "Take a walk");
  await addHabit(page, "Read a page");

  const check = page.getByRole("button", { name: "Mark complete: Take a walk" });
  await check.click();
  await expect(page.getByRole("button", { name: "Undo completion for Take a walk" })).toHaveAttribute("aria-pressed", "true");
  await page.getByRole("button", { name: "Undo completion for Take a walk" }).click();
  await expect(page.getByRole("button", { name: "Mark complete: Take a walk" })).toHaveAttribute("aria-pressed", "false");
  await page.getByRole("button", { name: "Mark complete: Take a walk" }).click();
  await expect(page).toHaveScreenshot("02-daily-check-in.png", { fullPage: true });
});

test("E2E-03 — history renders the selected habit and supports month navigation", async ({ page }) => {
  await openFixedDay(page);
  await addHabit(page, "Read a page");
  await page.getByRole("button", { name: "Mark complete: Read a page" }).click();
  await page.getByRole("button", { name: "View calendar history for Read a page" }).click();

  await expect(page.getByText("History for “Read a page”.")).toBeVisible();
  await expect(page.getByLabel("2026-09-06, complete")).toBeVisible();
  await expect(page).toHaveScreenshot("03-calendar-history.png", { fullPage: true });

  await page.getByRole("button", { name: "Previous month" }).click();
  await expect(page.getByText("August 2026")).toBeVisible();
  await expect(page.getByLabel("2026-09-06, complete")).toHaveCount(0);
  await page.getByRole("button", { name: "Next month" }).click();
  await expect(page.getByText("September 2026")).toBeVisible();
});

test("E2E-04 — rename, removal confirmation, and local reload preserve the expected state", async ({ page }) => {
  await openFixedDay(page);
  await addHabit(page, "Journal");

  page.once("dialog", dialog => dialog.accept("Journal briefly"));
  await page.getByRole("button", { name: "Rename Journal" }).click();
  await expect(page.getByRole("button", { name: "View calendar history for Journal briefly" })).toBeVisible();
  await page.reload();
  await expect(page.getByRole("button", { name: "View calendar history for Journal briefly" })).toBeVisible();

  page.once("dialog", dialog => dialog.dismiss());
  await page.getByRole("button", { name: "Remove Journal briefly" }).click();
  await expect(page.getByRole("button", { name: "View calendar history for Journal briefly" })).toBeVisible();

  page.once("dialog", dialog => dialog.accept());
  await page.getByRole("button", { name: "Remove Journal briefly" }).click();
  await expect(page.getByText("Start with one small habit.")).toBeVisible();
  await expect(page).toHaveScreenshot("04-managed-habits.png", { fullPage: true });
});

test("E2E-05 — core controls remain keyboard reachable", async ({ page }) => {
  await openFixedDay(page);
  await page.getByLabel("New habit").press("Tab");
  await expect(page.getByRole("button", { name: "Add habit" })).toBeFocused();
  await page.getByRole("button", { name: "Add habit" }).press("Shift+Tab");
  await expect(page.getByLabel("New habit")).toBeFocused();
});
