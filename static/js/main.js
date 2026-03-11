/* ═══════════════════════════════════════════════════════════════
   PythonQuest — main.js
   Pure vanilla JS, zero frameworks. Pyodide for real Python.
═══════════════════════════════════════════════════════════════ */

"use strict";

// ── Constants ──────────────────────────────────────────────────────────────
const SAVE_KEY     = "pq_state_v4";
const XP_PER_LEVEL = 200;

// ── Pyodide singleton ──────────────────────────────────────────────────────
let pyodide       = null;
let pyodideReady  = false;
let pyodideError  = false;

(async function bootPyodide() {
  try {
    pyodide = await loadPyodide({
      indexURL: "https://cdn.jsdelivr.net/pyodide/v0.25.0/full/",
    });
    pyodideReady = true;
    el("pyodideStatus").textContent = "✅ Python engine ready!";
    el("pyodideStatus").style.color = "var(--green)";
    el("pyStatus").textContent      = "🐍 Python Ready";
    el("pyStatus").style.color      = "var(--green)";
    setCompilerStatus("READY", "");
    el("btnRun").disabled     = false;
    el("btnRunLive").disabled = false;
  } catch (e) {
    pyodideError = true;
    el("pyodideStatus").textContent = "❌ Python failed to load (offline?)";
    el("pyodideStatus").style.color = "var(--red)";
    el("pyStatus").textContent      = "❌ Python Error";
    el("pyStatus").style.color      = "var(--red)";
    setCompilerStatus("ERROR", "error");
  }
})();

// ── State ──────────────────────────────────────────────────────────────────
let state = {
  currentLesson:     0,
  currentChallenge:  0,
  currentQuizIdx:    0,
  xp:                0,
  streak:            0,
  stars:             0,
  correctQuizzes:    0,
  completedChallenges: new Set(),
  earnedAchievements:  new Set(),
  answeredQuizzes:     new Set(),
  quizResults:         {},   // key → {chosen, correct}
};

// Load saved state
(function loadState() {
  try {
    const raw = localStorage.getItem(SAVE_KEY);
    if (!raw) return;
    const s = JSON.parse(raw);
    state.xp               = s.xp               || 0;
    state.streak           = s.streak            || 0;
    state.stars            = s.stars             || 0;
    state.correctQuizzes   = s.correctQuizzes    || 0;
    state.currentLesson    = s.currentLesson     || 0;
    state.currentChallenge = s.currentChallenge  || 0;
    state.currentQuizIdx   = s.currentQuizIdx    || 0;
    state.completedChallenges = new Set(s.completedChallenges || []);
    state.earnedAchievements  = new Set(s.earnedAchievements  || []);
    state.answeredQuizzes     = new Set(s.answeredQuizzes      || []);
    state.quizResults         = s.quizResults || {};
  } catch (e) { /* fresh start */ }
})();

function saveState() {
  try {
    const s = {
      ...state,
      completedChallenges: [...state.completedChallenges],
      earnedAchievements:  [...state.earnedAchievements],
      answeredQuizzes:     [...state.answeredQuizzes],
    };
    localStorage.setItem(SAVE_KEY, JSON.stringify(s));
  } catch (e) {}
}

// ── DOM helpers ────────────────────────────────────────────────────────────
function el(id)        { return document.getElementById(id); }
function setText(id, t){ const e = el(id); if (e) e.textContent = t; }
function setHTML(id, h){ const e = el(id); if (e) e.innerHTML  = h; }

// ── Screen switching ───────────────────────────────────────────────────────
el("btnStart").addEventListener("click", () => {
  el("titleScreen").classList.remove("active");
  el("gameScreen").classList.add("active");
  loadLesson(state.currentLesson);
  updateHUD();
  updateProgress();
  updateSidebars();
  renderAchievements();
});

// ── HUD ────────────────────────────────────────────────────────────────────
function updateHUD() {
  const level = Math.floor(state.xp / XP_PER_LEVEL) + 1;
  const pct   = ((state.xp % XP_PER_LEVEL) / XP_PER_LEVEL * 100).toFixed(0);
  setText("hudXP",     state.xp.toLocaleString());
  setText("hudLvl",    level);
  setText("hudStreak", state.streak);
  setText("hudDone",   state.completedChallenges.size);
  el("xpBar").style.width = pct + "%";
}

// ── Progress bars ──────────────────────────────────────────────────────────
function updateProgress() {
  const total  = TOTAL_CHALLENGES;
  const done   = state.completedChallenges.size;
  const overall = Math.round(done / total * 100);
  setText("overallPct", overall + "%");

  WORLDS_DATA.forEach(w => {
    const wLessons = LESSONS_DATA.filter(l => l.world === w.id);
    const wTotal   = wLessons.reduce((s, l) => s + l.challenges.length, 0);
    const wDone    = wLessons.reduce((s, l) =>
      s + l.challenges.filter(c => state.completedChallenges.has(c.id)).length, 0);
    const p = wTotal ? Math.round(wDone / wTotal * 100) : 0;
    const barEl = el("wbar" + w.id);
    const pctEl = el("wpct" + w.id);
    const progEl = el("wProg" + w.id);
    if (barEl) barEl.style.width = p + "%";
    if (pctEl) pctEl.textContent = p + "%";
    if (progEl) progEl.textContent = wDone + "/" + wTotal;
  });
}

// ── Sidebars ───────────────────────────────────────────────────────────────
function updateSidebars() {
  // Topic list highlights & progress
  document.querySelectorAll(".topic-item").forEach((item, idx) => {
    const lesson = LESSONS_DATA[idx];
    const done   = lesson.challenges.filter(c => state.completedChallenges.has(c.id)).length;
    item.classList.toggle("active", idx === state.currentLesson);
    item.classList.toggle("done",   done === lesson.challenges.length);
    const p = el("tprog" + idx);
    if (p) p.textContent = done + "/" + lesson.challenges.length;
  });

  // World nodes
  document.querySelectorAll(".world-node").forEach(node => {
    const wid    = parseInt(node.dataset.world);
    const wLessons = LESSONS_DATA.filter(l => l.world === wid);
    const wTotal   = wLessons.reduce((s, l) => s + l.challenges.length, 0);
    const wDone    = wLessons.reduce((s, l) =>
      s + l.challenges.filter(c => state.completedChallenges.has(c.id)).length, 0);
    const currentWorld = LESSONS_DATA[state.currentLesson].world;
    node.classList.toggle("current",  currentWorld === wid);
    node.classList.toggle("complete", wDone === wTotal && wTotal > 0);
  });
}

// ── LOAD LESSON ────────────────────────────────────────────────────────────
function loadLesson(idx) {
  state.currentLesson    = idx;
  state.currentChallenge = 0;
  state.currentQuizIdx   = 0;
  saveState();

  const lesson = LESSONS_DATA[idx];

  // Quest Header
  setHTML("questHeader", `
    <div class="quest-icon">${lesson.icon}</div>
    <div>
      <div class="quest-title">${lesson.title}</div>
      <div class="quest-meta">World ${lesson.world} &nbsp;•&nbsp; ${lesson.xp} XP &nbsp;•&nbsp; ${"★".repeat(lesson.stars)}</div>
      <span class="difficulty-badge diff-${lesson.diff}">◆ ${lesson.diff.toUpperCase()}</span>
    </div>
  `);

  // Story
  setHTML("storyBox", lesson.story);

  // Theory
  setHTML("theoryBody", lesson.theory.replace(/\n/g, "<br>"));

  // Examples
  let exHtml = `<div class="examples-section"><div class="examples-label">CODE EXAMPLES</div>`;
  lesson.examples.forEach((ex, i) => {
    exHtml += `
      <div class="example-block">
        <div class="example-block-title">${ex.title}</div>
        <pre>${escHtml(ex.code)}</pre>
      </div>`;
  });
  exHtml += "</div>";
  setHTML("examplesSection", exHtml);

  // Challenge tabs
  renderChallengeTabs(lesson);

  // Load challenge 0
  renderChallenge(lesson, 0);

  // Quiz
  renderQuiz(lesson);

  // Next lesson CTA
  const cta = el("nextLessonCta");
  if (idx < LESSONS_DATA.length - 1) {
    cta.style.display = "block";
    el("btnNextLesson").textContent =
      `⚡ NEXT LESSON: ${LESSONS_DATA[idx + 1].title} ▶`;
  } else {
    cta.style.display = "none";
  }

  updateSidebars();
  updateProgress();
  el("lessonArea").scrollTop = 0;
}

// ── Challenge Tabs ─────────────────────────────────────────────────────────
function renderChallengeTabs(lesson) {
  let html = "";
  lesson.challenges.forEach((ch, i) => {
    const done   = state.completedChallenges.has(ch.id);
    const active = i === state.currentChallenge;
    html += `<div class="ch-tab ${active ? "active" : ""} ${done ? "done" : ""}"
      onclick="switchChallenge(${i})">${done ? "✓" : i + 1} ${ch.title}</div>`;
  });
  setHTML("challengeNav", html);

  // Progress bar
  const done  = lesson.challenges.filter(c => state.completedChallenges.has(c.id)).length;
  const total = lesson.challenges.length;
  const pct   = Math.round(done / total * 100);
  setText("cpText", `${done}/${total} (${pct}%)`);
  el("cpFill").style.width = pct + "%";
}

function switchChallenge(idx) {
  state.currentChallenge = idx;
  saveState();
  const lesson = LESSONS_DATA[state.currentLesson];
  renderChallengeTabs(lesson);
  renderChallenge(lesson, idx);
  el("hintBox").style.display  = "none";
  el("outputBox").style.display = "none";
}

// ── Render Challenge ───────────────────────────────────────────────────────
function renderChallenge(lesson, idx) {
  const ch = lesson.challenges[idx];
  setText("chTitle",    `⚡ CHALLENGE ${idx + 1}`);
  setHTML("chDiff",     `<span class="difficulty-badge diff-${ch.diff}">◆ ${ch.diff.toUpperCase()}</span>`);
  setText("chXp",       `+${ch.xp} XP`);
  setText("chDesc",     ch.desc);
  setText("chExpected", ch.expected);

  el("codeEditor").value = "";
  el("hintBox").textContent = "💡 Hint:\n" + ch.hint;
  el("hintBox").style.display  = "none";
  el("outputBox").style.display = "none";

  // Next / prev button label
  const btnNext = el("btnNextChallenge");
  if (idx < lesson.challenges.length - 1) {
    btnNext.textContent = "NEXT ▶";
    btnNext.style.display = "";
  } else {
    btnNext.textContent = "";
    btnNext.style.display = "none";
  }
}

// ── Run Challenge ──────────────────────────────────────────────────────────
async function runChallenge() {
  const code    = el("codeEditor").value.trim();
  const lesson  = LESSONS_DATA[state.currentLesson];
  const ch      = lesson.challenges[state.currentChallenge];
  const outBox  = el("outputBox");

  if (!code) {
    showOutput("❌ Write some code first!", "output-error");
    return;
  }

  if (!pyodideReady) {
    showOutput("⏳ Python engine is still loading — please wait a moment.", "output-info");
    return;
  }

  el("btnRun").disabled     = true;
  el("btnRun").textContent  = "⚡ Running…";
  showOutput("⚡ Running your code…", "output-info");

  // 1. Actually execute via Pyodide
  const { output, success } = await runPython(code);

  // 2. Ask Flask to validate the code structure
  let passed = false;
  try {
    const res  = await fetch("/api/check_challenge", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ code, lesson_id: lesson.id, challenge_id: ch.id }),
    });
    const data = await res.json();
    passed = data.passed;
  } catch (e) {
    passed = false;
  }

  el("btnRun").disabled    = false;
  el("btnRun").textContent = "▶ RUN & CHECK";

  if (!success) {
    showOutput(`❌ Python Error:\n\n${output}\n\nFix the error and try again.\nIndentation matters in Python!`, "output-error");
    state.streak = 0;
    updateHUD();
    saveState();
    return;
  }

  if (passed) {
    const already = state.completedChallenges.has(ch.id);
    if (!already) {
      state.completedChallenges.add(ch.id);
      state.xp     += ch.xp;
      state.streak += 1;
      state.level   = Math.floor(state.xp / XP_PER_LEVEL) + 1;
      checkAchievements();
      updateHUD();
      updateProgress();
      updateSidebars();
      renderChallengeTabs(lesson);
      saveState();
      notify("✅ CHALLENGE COMPLETE!", `+${ch.xp} XP! Streak: ${state.streak} 🔥`);
    }
    showOutput(
      `✅ CORRECT!\n\n▶ Your output:\n${output}\n\n${already ? "(already completed — no bonus XP)" : "+" + ch.xp + " XP earned! 🎉"}`,
      "output-success"
    );
  } else {
    state.streak = 0;
    updateHUD();
    saveState();
    showOutput(
      `❌ Not quite right yet.\n\n▶ Your output:\n${output}\n\nTips:\n• Check the expected output above\n• Use the 💡 HINT button\n• Make sure required keywords/functions are used\n• Indentation is crucial in Python!`,
      "output-error"
    );
  }
}

function showOutput(text, cls) {
  const box = el("outputBox");
  box.textContent  = text;
  box.className    = "output-box " + cls;
  box.style.display = "block";
}

// ── Python execution via Pyodide ───────────────────────────────────────────
async function runPython(code) {
  let stdout = "";
  try {
    pyodide.setStdout({ batched: (s) => { stdout += s + "\n"; } });
    pyodide.setStderr({ batched: (s) => { stdout += "ERROR: " + s + "\n"; } });
    await pyodide.runPythonAsync(code);
    return { output: stdout.trim() || "(no output)", success: true };
  } catch (e) {
    const msg   = (e.message || String(e)).split("\n");
    const short = msg.slice(-4).join("\n");
    return { output: short, success: false };
  }
}

// ── Live Compiler ──────────────────────────────────────────────────────────
async function runLive() {
  if (!pyodideReady) {
    setHTML("liveOutput",
      '<span style="color:var(--gold)">⏳ Python engine still loading…</span>');
    return;
  }
  const code = el("liveEditor").value;
  const liveOut = el("liveOutput");
  liveOut.className   = "compiler-output out-running";
  liveOut.textContent = "⚡ Running…";
  setCompilerStatus("RUNNING", "running");
  el("btnRunLive").disabled = true;

  const { output, success } = await runPython(code);

  el("btnRunLive").disabled = false;
  setCompilerStatus("READY", "");
  liveOut.className   = "compiler-output " + (success ? "out-success" : "out-error");
  liveOut.textContent = output;
}

function clearLive() {
  el("liveEditor").value   = "";
  el("liveOutput").className   = "compiler-output out-idle";
  el("liveOutput").textContent = "▶ Click RUN to execute Python code";
}

function setCompilerStatus(label, cls) {
  const s = el("compilerStatus");
  if (!s) return;
  s.textContent = label;
  s.className   = "compiler-status " + cls;
}

// ── Hint toggle ────────────────────────────────────────────────────────────
function toggleHint() {
  const h = el("hintBox");
  h.style.display = h.style.display === "none" ? "block" : "none";
}

// ── Navigation ─────────────────────────────────────────────────────────────
function nextChallenge() {
  const lesson = LESSONS_DATA[state.currentLesson];
  if (state.currentChallenge < lesson.challenges.length - 1)
    switchChallenge(state.currentChallenge + 1);
}

function prevChallenge() {
  if (state.currentChallenge > 0)
    switchChallenge(state.currentChallenge - 1);
}

function nextLesson() {
  if (state.currentLesson < LESSONS_DATA.length - 1) {
    loadLesson(state.currentLesson + 1);
  } else {
    notify("🎉 LEGEND!", "You completed ALL lessons! Python Master achieved!");
  }
}

function jumpToWorld(worldId) {
  const idx = LESSONS_DATA.findIndex(l => l.world === worldId);
  if (idx >= 0) loadLesson(idx);
}

// ── QUIZ ───────────────────────────────────────────────────────────────────
function renderQuiz(lesson) {
  const quizzes = lesson.quizzes || [];
  const container = el("quizSection");
  if (!quizzes.length) { container.innerHTML = ""; return; }

  const idx = state.currentQuizIdx;
  if (idx >= quizzes.length) {
    container.innerHTML = `
      <div class="quiz-title">🧩 KNOWLEDGE CHECK</div>
      <div class="quiz-all-done">🏁 ALL QUIZ QUESTIONS COMPLETE FOR THIS LESSON!</div>`;
    return;
  }

  const q       = quizzes[idx];
  const qKey    = `${lesson.id}_q${idx}`;
  const answered = state.answeredQuizzes.has(qKey);
  const result   = state.quizResults[qKey];

  let optsHtml = "";
  q.options.forEach((opt, i) => {
    let cls   = "quiz-opt" + (answered ? " answered" : "");
    let badge = "";
    if (answered) {
      if (i === q.correct) { cls += " correct"; badge = `<span class="opt-badge badge-correct">✓ CORRECT</span>`; }
      else if (result && i === result.chosen) { cls += " wrong"; badge = `<span class="opt-badge badge-wrong">✗ YOUR ANSWER</span>`; }
    }
    const click = answered ? "" : `onclick="answerQuiz(${i})"`;
    optsHtml += `
      <div class="${cls}" ${click}>
        <span class="opt-key">${String.fromCharCode(65 + i)}</span>
        <span style="flex:1">${escHtml(opt)}</span>
        ${badge}
      </div>`;
  });

  let explHtml = "";
  if (answered) {
    const isCorrect = result && result.correct;
    explHtml = `
      <div class="explanation-box ${isCorrect ? "expl-correct" : "expl-wrong"}" id="explBox">
        <div class="expl-header">${isCorrect ? "🎯 GREAT JOB! +30 XP" : "📖 EXPLANATION"}</div>
        <div class="expl-body" id="explBody">
          <span style="color:var(--dim);animation:pulse 1.2s infinite">● ● ● Generating explanation…</span>
        </div>
      </div>`;
  }

  const navBtn = answered && idx < quizzes.length - 1
    ? `<button class="quiz-nav-btn" onclick="nextQuiz()">NEXT QUESTION ▶</button>` : "";

  container.innerHTML = `
    <div class="quiz-title">🧩 KNOWLEDGE CHECK (${idx + 1}/${quizzes.length})</div>
    <div class="quiz-question">${escHtml(q.q)}</div>
    <div class="quiz-options">${optsHtml}</div>
    ${explHtml}
    ${navBtn}`;

  if (answered) {
    fetchExplanation(q, result ? result.chosen : q.correct, lesson.title, result && result.correct);
  }
}

async function answerQuiz(chosenIdx) {
  const lesson  = LESSONS_DATA[state.currentLesson];
  const quizzes = lesson.quizzes || [];
  const idx     = state.currentQuizIdx;
  const q       = quizzes[idx];
  const qKey    = `${lesson.id}_q${idx}`;

  if (state.answeredQuizzes.has(qKey)) return;

  const isCorrect = chosenIdx === q.correct;
  state.answeredQuizzes.add(qKey);
  state.quizResults[qKey] = { chosen: chosenIdx, correct: isCorrect };

  if (isCorrect) {
    state.xp += 30;
    state.correctQuizzes++;
    checkAchievements();
    updateHUD();
    notify("🧩 QUIZ CORRECT!", "+30 XP! Keep it up!");
  } else {
    state.streak = 0;
    updateHUD();
    notify("📖 WRONG ANSWER", "Read the explanation to learn why!");
  }
  saveState();
  renderQuiz(lesson);
}

function nextQuiz() {
  state.currentQuizIdx++;
  saveState();
  renderQuiz(LESSONS_DATA[state.currentLesson]);
}

// ── Explanation (Claude API via Flask proxy) ───────────────────────────────
const explCache = {};

async function fetchExplanation(q, chosenIdx, lessonTitle, isCorrect) {
  const cacheKey = `${q.q}_${chosenIdx}`;
  if (explCache[cacheKey]) {
    injectExplanation(explCache[cacheKey]);
    return;
  }

  const correct = q.options[q.correct];
  const chosen  = q.options[chosenIdx];

  const prompt = isCorrect
    ? `You are a Python tutor. A student answered CORRECTLY.\nQuestion: "${q.q}"\nCorrect answer: "${correct}"\nTopic: ${lessonTitle}\nWrite 2-3 SHORT encouraging sentences explaining WHY "${correct}" is correct. Use backtick code snippets inline. No markdown headers — just clean prose.`
    : `You are a Python tutor. A student answered INCORRECTLY.\nQuestion: "${q.q}"\nOptions: ${q.options.map((o, i) => String.fromCharCode(65+i)+") "+o).join(" | ")}\nChosen (WRONG): "${chosen}"\nCorrect: "${correct}"\nTopic: ${lessonTitle}\nRespond ONLY with valid JSON (no markdown, no backticks):\n{"why_wrong":"2 sentences why chosen is wrong","why_correct":"2 sentences why correct is right with example"}`;

  try {
    const res  = await fetch("/api/explain_quiz", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt }),
    });
    const data = await res.json();
    const text = data.text || "";
    const fmt  = s => s.replace(/`([^`]+)`/g, "<code>$1</code>");

    let html = "";
    if (isCorrect) {
      html = `<div>${fmt(text)}</div>`;
    } else {
      try {
        const parsed = JSON.parse(text.trim());
        html = `
          <div style="border-bottom:1px solid var(--border);padding-bottom:.7rem;margin-bottom:.7rem">
            <div class="expl-sub-label label-wrong">❌ WHY "${escHtml(chosen)}" IS WRONG</div>
            <div>${fmt(parsed.why_wrong || "")}</div>
          </div>
          <div>
            <div class="expl-sub-label label-correct">✅ WHY "${escHtml(correct)}" IS CORRECT</div>
            <div>${fmt(parsed.why_correct || "")}</div>
          </div>`;
      } catch {
        html = `<div>The correct answer is: <strong>${escHtml(correct)}</strong></div>`;
      }
    }
    explCache[cacheKey] = html;
    injectExplanation(html);
  } catch (e) {
    injectExplanation(`<div style="color:var(--dim)">Explanation unavailable. Correct answer: <strong>${escHtml(q.options[q.correct])}</strong></div>`);
  }
}

function injectExplanation(html) {
  const box = el("explBody");
  if (box) {
    box.innerHTML = html;
    box.style.animation = "fadeIn .4s ease";
  }
}

// ── Achievements ───────────────────────────────────────────────────────────
function checkAchievements() {
  const done    = state.completedChallenges;
  const toEarn  = [];
  const ea      = state.earnedAchievements;

  if (done.size >= 1           && !ea.has("first_code")) toEarn.push("first_code");
  if (state.streak >= 5        && !ea.has("streak5"))    toEarn.push("streak5");
  if (state.streak >= 10       && !ea.has("streak10"))   toEarn.push("streak10");
  if (state.correctQuizzes >= 10 && !ea.has("quiz10"))   toEarn.push("quiz10");
  if (done.size >= Math.floor(TOTAL_CHALLENGES / 2) && !ea.has("halfway")) toEarn.push("halfway");

  const oopLessons  = LESSONS_DATA.filter(l => l.world === 4);
  const oopChs      = oopLessons.flatMap(l => l.challenges);
  if (oopChs.length && oopChs.every(c => done.has(c.id)) && !ea.has("oop_done")) toEarn.push("oop_done");

  const fileLessons = LESSONS_DATA.filter(l => l.world === 5);
  const fileChs     = fileLessons.flatMap(l => l.challenges);
  if (fileChs.length && fileChs.every(c => done.has(c.id)) && !ea.has("files_done")) toEarn.push("files_done");

  if (done.size >= TOTAL_CHALLENGES && !ea.has("master")) toEarn.push("master");

  toEarn.forEach(id => {
    ea.add(id);
    const a = ACHIEVEMENTS_DATA.find(x => x.id === id);
    if (a) notify("🏅 ACHIEVEMENT!", `${a.icon} ${a.name}: ${a.desc}`);
  });

  if (toEarn.length) renderAchievements();
}

function renderAchievements() {
  document.querySelectorAll(".achievement").forEach(el => {
    const id = el.id.replace("ach-", "");
    el.classList.toggle("earned", state.earnedAchievements.has(id));
    el.classList.toggle("locked", !state.earnedAchievements.has(id));
  });
}

// ── Notification ───────────────────────────────────────────────────────────
let notifTimer = null;
function notify(title, body) {
  setText("notifTitle", title);
  setText("notifBody",  body);
  const n = el("notif");
  n.classList.add("show");
  n.classList.remove("hide");
  clearTimeout(notifTimer);
  notifTimer = setTimeout(() => {
    n.classList.remove("show");
    n.classList.add("hide");
  }, 4500);
}

// ── Utilities ──────────────────────────────────────────────────────────────
function escHtml(s) {
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

// ── Initial UI state ───────────────────────────────────────────────────────
// Buttons disabled until Pyodide loads
el("btnRun").disabled     = true;
el("btnRunLive").disabled = true;
setCompilerStatus("LOADING…", "loading");
