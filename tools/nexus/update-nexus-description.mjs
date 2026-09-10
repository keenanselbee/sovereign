// Adapted from Grailwright tools/nexus/update-nexus-description.mjs, 2026-09-09.
import fs from "node:fs/promises";
import path from "node:path";
import { createHash } from "node:crypto";
import { pathToFileURL } from "node:url";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);

function parseArgs(argv) {
  const result = {};
  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (!token.startsWith("--")) {
      continue;
    }

    const key = token.slice(2);
    const next = argv[i + 1];
    if (next && !next.startsWith("--")) {
      result[key] = next;
      i += 1;
    } else {
      result[key] = true;
    }
  }

  return result;
}

function normalizeText(value) {
  const text = String(value ?? "")
    .replace(/\r\n/g, "\n")
    .replace(/\r/g, "\n")
    .replace(/\u00a0/g, " ")
    .replace(/\n\[\/code\]/gi, "[/code]")
    .trim();

  let inCodeBlock = false;
  return text.split("\n").map((line) => {
    if (/\[code\]/i.test(line)) {
      inCodeBlock = true;
    }

    const normalizedLine = inCodeBlock ? line.trimStart() : line;
    if (/\[\/code\]/i.test(normalizedLine)) {
      inCodeBlock = false;
    }

    return normalizedLine;
  }).join("\n").trim();
}

function delay(ms) {
  return new Promise((resolve) => {
    setTimeout(resolve, ms);
  });
}

function boundedTimeout(timeoutMs, maximumMs) {
  return Math.max(1000, Math.min(timeoutMs, maximumMs));
}

function summarizeButtons(buttons) {
  return buttons
    .slice(0, 20)
    .map((button) => {
      const label = `${button.text || button.aria || button.title || "(blank)"}`.replace(/\s+/g, " ").trim();
      return `${label}@${Math.round(button.top)},${Math.round(button.left)}${button.disabled ? ":disabled" : ""}`;
    });
}

async function recordProgress(request, page, phase, details = {}) {
  if (!request || !request.repoRoot || !request.packageName) {
    return;
  }

  const progressRoot = path.join(request.repoRoot, ".codex-temp", "nexus-description-progress");
  await ensureDirectory(progressRoot);
  const progressPath = path.join(progressRoot, `${request.packageName}.json`);
  const payload = {
    updatedAt: new Date().toISOString(),
    packageName: request.packageName,
    displayName: request.displayName,
    action: request.action,
    phase,
    currentUrl: page && !page.isClosed() ? page.url() : null,
    ...details
  };
  await writeJson(progressPath, payload);
  console.error(`[nexus-description] ${request.packageName}: ${phase}`);
}

function assertTextEquals(actual, expected, label) {
  const actualNormalized = normalizeText(actual);
  const expectedNormalized = normalizeText(expected);
  if (actualNormalized !== expectedNormalized) {
    throw new Error(`${label} did not match after verification. Expected ${expectedNormalized.length} chars, found ${actualNormalized.length} chars.`);
  }
}

function buildEditUrl(modUrl) {
  const parsed = new URL(modUrl);
  const parts = parsed.pathname.split("/").filter(Boolean);
  const modsIndex = parts.indexOf("mods");
  if (modsIndex < 1 || modsIndex + 1 >= parts.length) {
    throw new Error(`Cannot build Nexus edit URL from ${modUrl}`);
  }

  const game = parts[modsIndex - 1];
  const modId = parts[modsIndex + 1];
  return `${parsed.origin}/games/${game}/mods/${modId}/edit/general`;
}

async function exists(filePath) {
  try {
    await fs.access(filePath);
    return true;
  } catch {
    return false;
  }
}

async function ensureDirectory(directory) {
  await fs.mkdir(directory, { recursive: true });
}

async function readJson(filePath) {
  const text = await fs.readFile(filePath, "utf8");
  return JSON.parse(text.replace(/^\uFEFF/, ""));
}

async function writeJson(filePath, value) {
  await fs.writeFile(filePath, `${JSON.stringify(value, null, 2)}\n`, "utf8");
}

async function isVisible(locator) {
  try {
    return await locator.isVisible({ timeout: 1500 });
  } catch {
    return false;
  }
}

async function clickByUpdaterId(page, id) {
  await page.locator(`[data-nexus-updater-id="${id}"]`).click();
}

async function replaceTextareaValue(page, textarea, value) {
  const locator = page.locator(`[data-nexus-updater-id="${textarea.id}"]`);
  await locator.scrollIntoViewIfNeeded();
  await clickByUpdaterId(page, textarea.id);
  await page.keyboard.press("Control+A");
  await page.keyboard.press("Backspace");
  if (value.length > 0) {
    await page.keyboard.insertText(value);
  }

  await locator.evaluate((element) => {
    element.dispatchEvent(new Event("change", { bubbles: true }));
    element.blur();
  });
}

async function clickButtonInfo(page, button) {
  const locator = page.locator(`[data-nexus-button-id="${button.id}"]`);
  await locator.scrollIntoViewIfNeeded();
  await locator.click();
}

async function getVisibleTextareas(page) {
  return await page.evaluate(() => {
    for (const element of document.querySelectorAll("[data-nexus-updater-id]")) {
      element.removeAttribute("data-nexus-updater-id");
    }

    return Array.from(document.querySelectorAll("textarea"))
      .map((element, index) => {
        const style = window.getComputedStyle(element);
        const rect = element.getBoundingClientRect();
        const visible = style.display !== "none"
          && style.visibility !== "hidden"
          && rect.width > 1
          && rect.height > 1;
        const id = `textarea-${index}`;
        if (visible) {
          element.setAttribute("data-nexus-updater-id", id);
        }

        return {
          id,
          visible,
          top: rect.top,
          left: rect.left,
          width: rect.width,
          height: rect.height,
          value: element.value ?? "",
          placeholder: element.getAttribute("placeholder") ?? "",
          ariaLabel: element.getAttribute("aria-label") ?? ""
        };
      })
      .filter((item) => item.visible)
      .sort((a, b) => (a.top - b.top) || (a.left - b.left));
  });
}

async function getButtons(page) {
  return await page.evaluate(() => {
    for (const element of document.querySelectorAll("[data-nexus-button-id]")) {
      element.removeAttribute("data-nexus-button-id");
    }

    return Array.from(document.querySelectorAll("button,a,[role='button']"))
      .map((element, index) => {
        const style = window.getComputedStyle(element);
        const rect = element.getBoundingClientRect();
        const text = (element.innerText || element.textContent || "").trim();
        const aria = element.getAttribute("aria-label") || "";
        const title = element.getAttribute("title") || "";
        const disabled = element.disabled === true || element.getAttribute("aria-disabled") === "true";
        const visible = style.display !== "none"
          && style.visibility !== "hidden"
          && rect.width > 1
          && rect.height > 1;
        const id = `button-${index}`;
        if (visible) {
          element.setAttribute("data-nexus-button-id", id);
        }

        return {
          id,
          visible,
          text,
          aria,
          title,
          disabled,
          top: rect.top,
          left: rect.left,
          width: rect.width,
          height: rect.height
        };
      })
      .filter((item) => item.visible)
      .sort((a, b) => (a.top - b.top) || (a.left - b.left));
  });
}

async function getEditorState(page) {
  const [textareas, buttons, editorCount] = await Promise.all([
    getVisibleTextareas(page),
    getButtons(page),
    page.locator(".ProseMirror, [contenteditable='true']").count()
  ]);

  return {
    textareaCount: textareas.length,
    textareas: textareas.map((textarea) => ({
      top: Math.round(textarea.top),
      left: Math.round(textarea.left),
      width: Math.round(textarea.width),
      height: Math.round(textarea.height),
      valueLength: normalizeText(textarea.value).length,
      placeholder: textarea.placeholder,
      ariaLabel: textarea.ariaLabel
    })),
    editorCount,
    buttons: summarizeButtons(buttons)
  };
}

function hasFullDescriptionEditorShell(state) {
  const buttonText = state.buttons.join(" ").toLowerCase();
  return buttonText.includes("import description")
    || (buttonText.includes("insert a link") && buttonText.includes("bullet list"))
    || (buttonText.includes("bold") && buttonText.includes("underline") && buttonText.includes("font color"))
    || state.editorCount > 0;
}

async function scrollToFullDescriptionEditor(page, timeoutMs) {
  const fullDescription = page.getByText("Full description", { exact: false });
  const fullDescriptionTimeoutMs = boundedTimeout(timeoutMs, 45000);
  const deadline = Date.now() + fullDescriptionTimeoutMs;
  do {
    if (await isVisible(fullDescription)) {
      await fullDescription.scrollIntoViewIfNeeded();
      return;
    }

    const state = await getEditorState(page);
    if (hasFullDescriptionEditorShell(state)) {
      return;
    }

    await page.evaluate(() => {
      window.scrollBy({
        top: Math.max(600, Math.floor(window.innerHeight * 0.8)),
        behavior: "instant"
      });
    });
    await delay(350);
  } while (Date.now() < deadline);

  const state = await getEditorState(page);
  throw new Error(`Full description editor did not appear within ${fullDescriptionTimeoutMs}ms after opening the General editor. Editor state: ${JSON.stringify(state)}`);
}

async function waitForGeneralEditor(page, timeoutMs) {
  await page.getByText("Short description", { exact: false }).waitFor({
    state: "visible",
    timeout: boundedTimeout(timeoutMs, 45000)
  });

  await scrollToFullDescriptionEditor(page, timeoutMs);
}

async function isLoggedOut(page) {
  if (await isVisible(page.getByText("Log in to Nexus Mods", { exact: true }))) {
    return true;
  }

  if (await isVisible(page.getByText("Email or Username", { exact: true }))) {
    return true;
  }

  const loginButton = page.getByText("Log in", { exact: true });
  return await isVisible(loginButton);
}

function isNexusAuthUrl(page) {
  const url = page.url();
  return url.includes("users.nexusmods.com")
    || url.includes("/auth/sign_in")
    || url.includes("/users/login")
    || url.includes("/login");
}

async function hasLoggedInSignal(page) {
  if (await isVisible(page.getByText("Welcome back,", { exact: false }))) {
    return true;
  }

  if (await isVisible(page.getByText("My content", { exact: true }))) {
    return true;
  }

  return false;
}

async function waitForLogin(page, timeoutMs) {
  const deadline = Date.now() + timeoutMs;
  while (Date.now() < deadline) {
    if (page.isClosed()) {
      throw new Error("The isolated browser window was closed before login was detected. Rerun -LoginOnly and leave the window open until the tool closes it.");
    }

    if (await hasLoggedInSignal(page)) {
      return true;
    }

    try {
      await page.waitForTimeout(1500);
    } catch (error) {
      throw new Error("The isolated browser window was closed before login was detected. Rerun -LoginOnly and leave the window open until the tool closes it.");
    }
  }

  return false;
}

async function requireLoggedIn(page) {
  if (isNexusAuthUrl(page) || await isLoggedOut(page)) {
    throw new Error("Nexus is logged out in the isolated browser profile. Run -LoginOnly and log in there first.");
  }
}

async function openEditor(page, modUrl, timeoutMs) {
  // The target was validated by runRequest. Go straight to its known editor;
  // the public page's Manage menu may not have hydrated yet after navigation.
  await page.goto(buildEditUrl(modUrl), { waitUntil: "domcontentloaded", timeout: timeoutMs });
  await requireLoggedIn(page);
  await waitForGeneralEditor(page, timeoutMs);
}

async function ensureSourceMode(page, timeoutMs) {
  await scrollToFullDescriptionEditor(page, timeoutMs);
  let textareas = await getVisibleTextareas(page);
  if (textareas.length >= 2) {
    return textareas;
  }

  const editors = page.locator(".ProseMirror, [contenteditable='true']");
  const editorCount = await editors.count();
  if (editorCount > 0) {
    await editors.nth(editorCount - 1).click();
    await page.keyboard.press("Control+Shift+S");
    await page.waitForTimeout(500);
    textareas = await getVisibleTextareas(page);
    if (textareas.length >= 2) {
      return textareas;
    }
  }

  const buttons = await getButtons(page);
  const sourceButton = buttons
    .filter((button) => {
      const haystack = `${button.text} ${button.aria} ${button.title}`.toLowerCase();
      return haystack.includes("source")
        || button.text === "[]"
        || button.text === "<>"
        || button.text === "</>";
    })
    .sort((a, b) => b.top - a.top)[0];

  if (!sourceButton) {
    const state = await getEditorState(page);
    throw new Error(`Could not find the full-description source toggle or rich-text editor. Editor state: ${JSON.stringify(state)}`);
  }

  await clickButtonInfo(page, sourceButton);

  const sourceModeTimeoutMs = boundedTimeout(timeoutMs, 20000);
  const deadline = Date.now() + sourceModeTimeoutMs;
  do {
    textareas = await getVisibleTextareas(page);
    if (textareas.length >= 2) {
      return textareas;
    }

    await page.waitForTimeout(250);
  } while (Date.now() < deadline);

  const state = await getEditorState(page);
  throw new Error(`Full-description source textarea did not appear within ${sourceModeTimeoutMs}ms after opening source mode. Editor state: ${JSON.stringify(state)}`);
}

async function leaveFullDescriptionSourceMode(page, timeoutMs) {
  const context = page.context();
  const buttons = await getButtons(page);
  const sourceButton = buttons
    .filter((button) => {
      const haystack = `${button.text} ${button.aria} ${button.title}`.toLowerCase();
      return haystack.includes("source")
        || button.text === "[]"
        || button.text === "<>"
        || button.text === "</>";
    })
    .sort((a, b) => b.top - a.top)[0];

  if (!sourceButton) {
    throw new Error("Could not find the full-description source toggle before saving.");
  }

  await clickButtonInfo(page, sourceButton);
  await delay(1500);

  const livePage = page.isClosed()
    ? context.pages().find((candidate) => !candidate.isClosed() && candidate.url().includes("nexusmods.com"))
    : page;
  if (!livePage) {
    throw new Error("Nexus page closed after leaving source mode.");
  }

  livePage.setDefaultTimeout(timeoutMs);
  return livePage;
}

async function readDescriptions(page, timeoutMs) {
  const textareas = await ensureSourceMode(page, timeoutMs);
  if (textareas.length < 2) {
    throw new Error(`Expected at least two visible textareas in the Nexus editor, found ${textareas.length}.`);
  }

  return {
    shortDescription: textareas[0].value,
    fullDescription: textareas[textareas.length - 1].value
  };
}

async function fillDescriptions(page, desiredShort, desiredFull, timeoutMs) {
  let textareas = await ensureSourceMode(page, timeoutMs);
  if (textareas.length < 2) {
    throw new Error(`Expected at least two visible textareas in the Nexus editor, found ${textareas.length}.`);
  }

  if (normalizeText(textareas[0].value) !== normalizeText(desiredShort)) {
    await replaceTextareaValue(page, textareas[0], desiredShort);
  }

  textareas = await ensureSourceMode(page, timeoutMs);
  if (normalizeText(textareas[textareas.length - 1].value) !== normalizeText(desiredFull)) {
    await replaceTextareaValue(page, textareas[textareas.length - 1], desiredFull);
  }

  const afterFill = await readDescriptions(page, timeoutMs);
  assertTextEquals(afterFill.shortDescription, desiredShort, "Short description field");
  assertTextEquals(afterFill.fullDescription, desiredFull, "Full description field");
}

async function clickSave(page, timeoutMs) {
  const saveTimeoutMs = boundedTimeout(timeoutMs, 30000);
  const deadline = Date.now() + saveTimeoutMs;
  do {
    const buttons = await getButtons(page);
    const saveButton = buttons
      .filter((button) => button.text === "Save" && !button.disabled)
      .sort((a, b) => b.top - a.top)[0];

    if (saveButton) {
      await delay(500);
      await clickButtonInfo(page, saveButton);
      await page.waitForLoadState("networkidle", { timeout: Math.min(timeoutMs, 15000) }).catch(() => {});
      await page.waitForTimeout(2500);
      return;
    }

    await delay(500);
  } while (Date.now() < deadline);

  const buttons = await getButtons(page);
  throw new Error(`Could not find an enabled Save button within ${saveTimeoutMs}ms after editing. Buttons: ${JSON.stringify(summarizeButtons(buttons))}`);
}

async function hasUnsavedModal(page) {
  return await isVisible(page.getByText("Unsaved changes", { exact: true }));
}

async function verifySaved(page, modUrl, expectedShort, expectedFull, timeoutMs) {
  const editUrl = buildEditUrl(modUrl);
  for (let attempt = 1; attempt <= 3; attempt += 1) {
    try {
      await page.goto(editUrl, { waitUntil: "domcontentloaded", timeout: timeoutMs });
      break;
    } catch (error) {
      const navigationWasAborted = String(error?.message || error).includes("net::ERR_ABORTED");
      if (!navigationWasAborted || attempt === 3) {
        throw error;
      }

      await delay(1000);
    }
  }

  await page.waitForLoadState("domcontentloaded", { timeout: timeoutMs });
  if (await hasUnsavedModal(page)) {
    throw new Error("Nexus showed the Unsaved changes prompt during verification. The save likely did not complete.");
  }

  const afterReload = await readDescriptions(page, timeoutMs);
  assertTextEquals(afterReload.shortDescription, expectedShort, "Saved short description");
  assertTextEquals(afterReload.fullDescription, expectedFull, "Saved full description");
  return afterReload;
}

async function createBackup(request, previous, desired, action) {
  const modBackupRoot = path.join(request.backupRoot, request.packageName);
  await ensureDirectory(modBackupRoot);
  const safeTimestamp = new Date().toISOString().replace(/[:.]/g, "-");
  const backupPath = path.join(modBackupRoot, `${safeTimestamp}-${action}.json`);
  const backup = {
    createdAt: new Date().toISOString(),
    action,
    packageName: request.packageName,
    displayName: request.displayName,
    nexusUrl: request.nexusUrl,
    previous,
    desired,
    restoreCommand: `tools/Update-NexusDescription.ps1 -BackupPath "${backupPath}" -Save`
  };
  await writeJson(backupPath, backup);
  return backupPath;
}

async function emitResult(request, payload) {
  if (request.resultPath) {
    await writeJson(request.resultPath, payload);
  }
  const summary = { status: payload.status };
  for (const [key, value] of Object.entries(payload)) {
    if (/(Length|Changed)$/.test(key) || /Path$/.test(key)) {
      summary[key] = value;
    }
  }
  console.log(JSON.stringify(summary, null, 2));
}

function getDesiredFromBackup(backup) {
  if (!backup.previous) {
    throw new Error("Backup JSON does not contain a previous description payload.");
  }

  return {
    shortDescription: backup.previous.shortDescription ?? "",
    fullDescription: backup.previous.fullDescription ?? ""
  };
}

export async function runRequest(request) {
  if (!['review', 'save', 'login', 'revert-review', 'revert-save'].includes(request.action)) throw new Error('Unsupported action');
  if (request.nexusUrl !== 'https://www.nexusmods.com/games/eldenring/mods/201') throw new Error('Unexpected Nexus target');
  if (request.action !== "login" && (!request.resultPath || typeof request.resultPath !== "string")) {
    throw new Error("Non-login Nexus description requests require a resultPath.");
  }
  const timeoutMs = Math.max(30, Number(request.timeoutSeconds || 180)) * 1000;
  const toolRoot = process.env.NEXUS_DESCRIPTION_TOOL_ROOT;
  if (!toolRoot) {
    throw new Error("NEXUS_DESCRIPTION_TOOL_ROOT is not set.");
  }

  const playwrightPackage = path.join(toolRoot, "node_modules", "playwright");
  if (!(await exists(path.join(playwrightPackage, "package.json")))) {
    throw new Error(`Playwright package is not installed at ${playwrightPackage}`);
  }

  const { chromium } = require(playwrightPackage);
  await ensureDirectory(request.profileRoot);
  await ensureDirectory(request.backupRoot);

  if (request.browser !== "Chrome") {
    throw new Error("Only Chrome is supported for Nexus description updates.");
  }

  if (!Number.isInteger(request.remoteDebuggingPort) || request.remoteDebuggingPort < 1 || request.remoteDebuggingPort > 65535) {
    throw new Error('A dedicated Chrome debugging port is required');
  }
  const browser = await chromium.connectOverCDP(`http://127.0.0.1:${request.remoteDebuggingPort}`, { timeout: timeoutMs });
  const context = browser.contexts()[0];
  if (!context) throw new Error('Dedicated Chrome did not expose its profile context');
  let page = context.pages()[0] || await context.newPage();

  page.setDefaultTimeout(timeoutMs);
  page.on("dialog", async (dialog) => {
    await dialog.dismiss();
  });

  try {
    await recordProgress(request, page, "started");
    if (request.action === "login") {
      await recordProgress(request, page, "opening-login-page");
      await page.goto("https://www.nexusmods.com/", { waitUntil: "domcontentloaded", timeout: timeoutMs });
      await recordProgress(request, page, "waiting-for-login");
      const loggedIn = await waitForLogin(page, timeoutMs);
      if (!loggedIn) {
        throw new Error("Timed out waiting for Nexus login in the isolated browser profile.");
      }

      await recordProgress(request, page, "logged-in");
      await emitResult(request, {
        status: "logged-in",
        profileRoot: request.profileRoot,
        currentUrl: page.url()
      });
      return;
    }

    await recordProgress(request, page, "opening-editor");
    await openEditor(page, request.nexusUrl, timeoutMs);
    await recordProgress(request, page, "reading-current-descriptions");
    const previous = await readDescriptions(page, timeoutMs);
    await recordProgress(request, page, "read-current-descriptions", {
      currentShortLength: normalizeText(previous.shortDescription).length,
      currentFullLength: normalizeText(previous.fullDescription).length
    });

    let desired = {
      shortDescription: request.desiredShortDescription,
      fullDescription: request.desiredFullDescription
    };

    if (request.action === "revert-save" || request.action === "revert-review") {
      const restoreBackup = await readJson(request.restoreBackupPath);
      if (restoreBackup.nexusUrl !== request.nexusUrl || restoreBackup.packageName !== request.packageName) {
        throw new Error('Backup belongs to a different Nexus page');
      }
      desired = getDesiredFromBackup(restoreBackup);
    }

    const backupPath = await createBackup(request, previous, desired, request.action);
    await recordProgress(request, page, "backup-created", { backupPath });
    const shortDescriptionChanged = normalizeText(previous.shortDescription) !== normalizeText(desired.shortDescription);
    const fullDescriptionChanged = normalizeText(previous.fullDescription) !== normalizeText(desired.fullDescription);

    if (request.action === "review" || request.action === "revert-review") {
      await recordProgress(request, page, "reviewed", {
        backupPath,
        shortDescriptionChanged,
        fullDescriptionChanged
      });
      await emitResult(request, {
        status: "reviewed",
        action: request.action,
        nexusUrl: request.nexusUrl,
        backupPath,
        restoreBackupPath: request.restoreBackupPath || null,
        currentShortLength: normalizeText(previous.shortDescription).length,
        currentFullLength: normalizeText(previous.fullDescription).length,
        desiredShortLength: normalizeText(desired.shortDescription).length,
        desiredFullLength: normalizeText(desired.fullDescription).length,
        shortDescriptionChanged,
        fullDescriptionChanged,
        observedShortDescription: previous.shortDescription,
        observedFullDescription: previous.fullDescription
      });
      return;
    }

    if (!shortDescriptionChanged && !fullDescriptionChanged && !request.forceSave) {
      await recordProgress(request, page, "already-current", { backupPath });
      await emitResult(request, {
        status: "already-current",
        action: request.action,
        nexusUrl: request.nexusUrl,
        backupPath,
        restoreBackupPath: request.restoreBackupPath || null,
        shortLength: normalizeText(previous.shortDescription).length,
        fullLength: normalizeText(previous.fullDescription).length,
        observedShortDescription: previous.shortDescription,
        observedFullDescription: previous.fullDescription
      });
      return;
    }

    await recordProgress(request, page, "filling-descriptions", {
      desiredShortLength: normalizeText(desired.shortDescription).length,
      desiredFullLength: normalizeText(desired.fullDescription).length
    });
    await assertSourceHashes(request);
    await fillDescriptions(page, desired.shortDescription, desired.fullDescription, timeoutMs);
    await recordProgress(request, page, "leaving-source-mode");
    page = await leaveFullDescriptionSourceMode(page, timeoutMs);
    await recordProgress(request, page, "saving");
    await assertSourceHashes(request);
    await clickSave(page, timeoutMs);
    await recordProgress(request, page, "verifying-save");
    const verified = await verifySaved(page, request.nexusUrl, desired.shortDescription, desired.fullDescription, timeoutMs);
    await recordProgress(request, page, "saved-and-verified", {
      backupPath,
      shortLength: normalizeText(verified.shortDescription).length,
      fullLength: normalizeText(verified.fullDescription).length
    });

    await emitResult(request, {
      status: "saved-and-verified",
      action: request.action,
      nexusUrl: request.nexusUrl,
      backupPath,
      restoreBackupPath: request.restoreBackupPath || null,
      shortLength: normalizeText(verified.shortDescription).length,
      fullLength: normalizeText(verified.fullDescription).length,
      observedShortDescription: verified.shortDescription,
      observedFullDescription: verified.fullDescription
    });
  } catch (error) {
    await recordProgress(request, page, "failed", {
      error: error && error.message ? error.message : String(error)
    }).catch(() => {});
    throw error;
  } finally {
    if (browser.isConnected()) {
      const session = await browser.newBrowserCDPSession();
      await session.send('Browser.close').catch(() => {});
      await browser.close().catch(() => {});
    }
  }
}

export async function assertSourceHashes(request) {
  for (const [file, expected] of Object.entries(request.sourceHashes || {})) {
    const actual = createHash('sha256').update(await fs.readFile(file)).digest('hex');
    if (actual !== expected) throw new Error('Local source changed during review; rerun before saving');
  }
}

export { normalizeText, buildEditUrl, readDescriptions, fillDescriptions, clickSave, verifySaved, getDesiredFromBackup };
if (process.argv[1] && import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href) {
  const args = parseArgs(process.argv.slice(2));
  readJson(args.request).then(runRequest).catch(error => {
    console.error(error.message);
    process.exitCode = 1;
  });
}
