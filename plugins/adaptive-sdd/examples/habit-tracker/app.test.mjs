import assert from "node:assert/strict";
import test from "node:test";
import tracker from "./app.js";

function storageWith(value) {
  let stored = value;
  return { getItem: () => stored, setItem: (_key, next) => { stored = next; }, value: () => stored };
}

test("adds valid habits and rejects blank names", () => {
  const added = tracker.addHabit(tracker.emptyState(), "  Take a walk  ", "walk");
  assert.equal(added.habit.name, "Take a walk");
  assert.equal(added.state.habits.length, 1);
  assert.equal(tracker.addHabit(added.state, "   ").error, "Enter a habit name first.");
});

test("renames and removes a habit with its history", () => {
  let state = tracker.addHabit(tracker.emptyState(), "Read", "read").state;
  state = tracker.toggleCompletion(state, "read", "2026-09-06");
  state = tracker.renameHabit(state, "read", "Read a page").state;
  assert.equal(state.habits[0].name, "Read a page");
  assert.equal(tracker.removeHabit(state, "read").habits.length, 0);
});

test("toggles one local date without duplicates or changing others", () => {
  let state = tracker.addHabit(tracker.emptyState(), "Walk", "walk").state;
  state = tracker.toggleCompletion(state, "walk", "2026-09-06");
  state = tracker.toggleCompletion(state, "walk", "2026-09-07");
  state = tracker.toggleCompletion(state, "walk", "2026-09-06");
  assert.deepEqual(state.habits[0].completionDates, ["2026-09-07"]);
  assert.deepEqual(tracker.dailyItems(state, "2026-09-07"), [{ id: "walk", name: "Walk", complete: true }]);
});

test("builds calendar data for selected completions and leap February", () => {
  const state = { version: 1, habits: [{ id: "walk", name: "Walk", completionDates: ["2028-02-29"] }], selectedHabitId: "walk" };
  assert.equal(tracker.selectedHabit(state).name, "Walk");
  const days = tracker.calendarDays(2028, 1, ["2028-02-29"]);
  assert.equal(days.filter(Boolean).length, 29);
  assert.equal(days.find((day) => day && day.key === "2028-02-29").complete, true);
  assert.deepEqual(tracker.shiftMonth(2026, 0, -1), { year: 2025, month: 11 });
  assert.deepEqual(tracker.shiftMonth(2026, 11, 1), { year: 2027, month: 0 });
});

test("restores valid saved state and recovers from malformed data", () => {
  const source = tracker.addHabit(tracker.emptyState(), "Journal", "journal").state;
  const storage = storageWith(null); tracker.saveState(storage, source);
  assert.equal(tracker.loadState(storage).state.habits[0].name, "Journal");
  assert.deepEqual(tracker.loadState(storageWith("not json")).state, tracker.emptyState());
});
