import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";
const page=await readFile(new URL("../app/page.tsx",import.meta.url),"utf8");
const layout=await readFile(new URL("../app/layout.tsx",import.meta.url),"utf8");
test("provides authenticated API-backed campus workflows",()=>{assert.match(page,/\/auth\/login/);assert.match(page,/\/campus\/dashboard/);assert.match(page,/\/campus\/assistant/);assert.match(page,/\/complaints/);assert.match(page,/Attendance intelligence/);assert.match(page,/Campus Map/)});
test("publishes CampusOS metadata",()=>{assert.match(layout,/CampusOS \| Campus Intelligence/);assert.match(layout,/og\.png/);assert.doesNotMatch(layout,/Starter Project|Building your site/)});
