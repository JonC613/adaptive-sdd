(function () {
  "use strict";

  var STORAGE_KEY = "adaptive-sdd.habit-tracker.v1";
  var WEEKDAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];

  function emptyState() { return { version: 1, habits: [], selectedHabitId: null }; }
  function clone(value) { return JSON.parse(JSON.stringify(value)); }
  function localDateKey(date) {
    var year = date.getFullYear();
    var month = String(date.getMonth() + 1).padStart(2, "0");
    var day = String(date.getDate()).padStart(2, "0");
    return year + "-" + month + "-" + day;
  }
  function validHabit(habit) {
    return habit && typeof habit.id === "string" && typeof habit.name === "string" &&
      Array.isArray(habit.completionDates) && habit.name.trim().length > 0;
  }
  function normalizeState(value) {
    if (!value || value.version !== 1 || !Array.isArray(value.habits) || !value.habits.every(validHabit)) return emptyState();
    var state = clone(value);
    state.habits.forEach(function (habit) {
      habit.name = habit.name.trim();
      habit.completionDates = Array.from(new Set(habit.completionDates.filter(function (key) { return /^\d{4}-\d{2}-\d{2}$/.test(key); }))).sort();
    });
    if (!state.habits.some(function (habit) { return habit.id === state.selectedHabitId; })) state.selectedHabitId = state.habits[0] ? state.habits[0].id : null;
    return state;
  }
  function loadState(storage) {
    try {
      var raw = storage.getItem(STORAGE_KEY);
      if (!raw) return { state: emptyState(), recovered: false };
      var normalized = normalizeState(JSON.parse(raw));
      return { state: normalized, recovered: normalized.habits.length === 0 && raw !== JSON.stringify(emptyState()) };
    } catch (_) { return { state: emptyState(), recovered: true }; }
  }
  function saveState(storage, state) { storage.setItem(STORAGE_KEY, JSON.stringify(state)); }
  function makeId() { return "habit-" + Date.now().toString(36) + "-" + Math.random().toString(36).slice(2, 7); }
  function addHabit(state, name, id) {
    var clean = String(name || "").trim();
    if (!clean) return { state: state, error: "Enter a habit name first." };
    var next = clone(state); var habit = { id: id || makeId(), name: clean, completionDates: [] };
    next.habits.push(habit); next.selectedHabitId = habit.id;
    return { state: next, habit: habit };
  }
  function renameHabit(state, id, name) {
    var clean = String(name || "").trim();
    if (!clean) return { state: state, error: "Habit names cannot be blank." };
    var next = clone(state); var habit = next.habits.find(function (item) { return item.id === id; });
    if (!habit) return { state: state, error: "That habit no longer exists." };
    habit.name = clean; return { state: next };
  }
  function removeHabit(state, id) {
    var next = clone(state); next.habits = next.habits.filter(function (habit) { return habit.id !== id; });
    if (next.selectedHabitId === id) next.selectedHabitId = next.habits[0] ? next.habits[0].id : null;
    return next;
  }
  function toggleCompletion(state, id, dateKey) {
    var next = clone(state); var habit = next.habits.find(function (item) { return item.id === id; });
    if (!habit) return state;
    var index = habit.completionDates.indexOf(dateKey);
    if (index >= 0) habit.completionDates.splice(index, 1); else habit.completionDates.push(dateKey);
    habit.completionDates.sort(); return next;
  }
  function dailyItems(state, dateKey) {
    return state.habits.map(function (habit) { return { id: habit.id, name: habit.name, complete: habit.completionDates.includes(dateKey) }; });
  }
  function selectedHabit(state) { return state.habits.find(function (habit) { return habit.id === state.selectedHabitId; }) || null; }
  function shiftMonth(year, month, direction) { var next = new Date(year, month + direction, 1); return { year: next.getFullYear(), month: next.getMonth() }; }
  function calendarDays(year, month, completionDates) {
    var completed = new Set(completionDates || []); var first = new Date(year, month, 1);
    var offset = (first.getDay() + 6) % 7; var total = new Date(year, month + 1, 0).getDate(); var days = [];
    for (var blank = 0; blank < offset; blank += 1) days.push(null);
    for (var day = 1; day <= total; day += 1) {
      var key = localDateKey(new Date(year, month, day)); days.push({ day: day, key: key, complete: completed.has(key) });
    }
    while (days.length % 7) days.push(null); return days;
  }

  var api = { STORAGE_KEY: STORAGE_KEY, emptyState: emptyState, localDateKey: localDateKey, normalizeState: normalizeState, loadState: loadState, saveState: saveState, addHabit: addHabit, renameHabit: renameHabit, removeHabit: removeHabit, toggleCompletion: toggleCompletion, dailyItems: dailyItems, selectedHabit: selectedHabit, shiftMonth: shiftMonth, calendarDays: calendarDays };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  if (typeof document === "undefined") return;

  var elements = {
    form: document.getElementById("add-form"), input: document.getElementById("habit-name"), list: document.getElementById("habit-list"), status: document.getElementById("status"), today: document.getElementById("today-date"), selected: document.getElementById("selected-habit"), month: document.getElementById("month-label"), calendar: document.getElementById("calendar"), previous: document.getElementById("previous-month"), next: document.getElementById("next-month")
  };
  var loaded = loadState(window.localStorage); var state = loaded.state; var now = new Date(); var shownYear = now.getFullYear(); var shownMonth = now.getMonth();
  elements.today.dateTime = localDateKey(now); elements.today.textContent = now.toLocaleDateString(undefined, { weekday: "short", month: "short", day: "numeric" });
  function setStatus(message) { elements.status.textContent = message || ""; }
  function persist() { try { saveState(window.localStorage, state); } catch (_) { setStatus("Changes cannot be saved in this browser."); } }
  function findHabit(id) { return state.habits.find(function (habit) { return habit.id === id; }); }
  function button(text, className, label) { var item = document.createElement("button"); item.type = "button"; item.textContent = text; item.className = className || ""; if (label) item.setAttribute("aria-label", label); return item; }
  function renderList() {
    elements.list.replaceChildren();
    if (!state.habits.length) { var empty = document.createElement("p"); empty.className = "empty-state"; empty.textContent = "Start with one small habit. Add it above, then check in here each day."; elements.list.append(empty); return; }
    var todayKey = localDateKey(new Date());
    dailyItems(state, todayKey).forEach(function (item) {
      var habit = findHabit(item.id); var complete = item.complete; var row = document.createElement("article"); row.className = "habit-row";
      var check = button(complete ? "✓" : "", "check-button" + (complete ? " is-complete" : ""), (complete ? "Undo completion for " : "Mark complete: ") + habit.name);
      check.setAttribute("aria-pressed", String(complete)); check.addEventListener("click", function () { state = toggleCompletion(state, habit.id, todayKey); persist(); setStatus(complete ? "Completion undone for " + habit.name + "." : "Marked " + habit.name + " complete."); render(); });
      var name = button(habit.name, "habit-name", "View calendar history for " + habit.name); name.addEventListener("click", function () { state.selectedHabitId = habit.id; persist(); render(); });
      var actions = document.createElement("div"); actions.className = "row-actions";
      var rename = button("Rename", "", "Rename " + habit.name); rename.addEventListener("click", function () { var nextName = window.prompt("Rename habit", habit.name); if (nextName === null) return; var result = renameHabit(state, habit.id, nextName); state = result.state; if (result.error) setStatus(result.error); else { persist(); setStatus("Renamed habit."); } render(); });
      var remove = button("Remove", "", "Remove " + habit.name); remove.addEventListener("click", function () { if (!window.confirm("Remove “" + habit.name + "” and its saved history?")) return; state = removeHabit(state, habit.id); persist(); setStatus("Habit removed."); render(); });
      actions.append(rename, remove); row.append(check, name, actions); elements.list.append(row);
    });
  }
  function renderCalendar() {
    elements.calendar.replaceChildren(); elements.month.textContent = new Date(shownYear, shownMonth, 1).toLocaleDateString(undefined, { month: "long", year: "numeric" });
    var habit = selectedHabit(state); elements.selected.textContent = habit ? "History for “" + habit.name + "”." : "Choose a habit from the daily list to see its history.";
    WEEKDAYS.forEach(function (day) { var label = document.createElement("div"); label.className = "weekday"; label.textContent = day; elements.calendar.append(label); });
    calendarDays(shownYear, shownMonth, habit ? habit.completionDates : []).forEach(function (entry) { var cell = document.createElement("div"); if (!entry) { cell.className = "day blank"; cell.setAttribute("aria-hidden", "true"); } else { cell.className = "day" + (entry.complete ? " is-complete" : "") + (entry.key === localDateKey(new Date()) ? " is-today" : ""); cell.textContent = entry.day; cell.setAttribute("aria-label", entry.key + (entry.complete ? ", complete" : ", incomplete")); } elements.calendar.append(cell); });
  }
  function render() { renderList(); renderCalendar(); }
  elements.form.addEventListener("submit", function (event) { event.preventDefault(); var result = addHabit(state, elements.input.value); state = result.state; if (result.error) { setStatus(result.error); return; } elements.input.value = ""; persist(); setStatus("Added " + result.habit.name + "."); render(); });
  elements.previous.addEventListener("click", function () { var month = shiftMonth(shownYear, shownMonth, -1); shownYear = month.year; shownMonth = month.month; renderCalendar(); });
  elements.next.addEventListener("click", function () { var month = shiftMonth(shownYear, shownMonth, 1); shownYear = month.year; shownMonth = month.month; renderCalendar(); });
  if (loaded.recovered) setStatus("Saved data could not be read, so Daymark started fresh."); render();
}());
