# 🐍 PythonQuest — Master Python

A gamified Python learning app built with **pure Python (Flask)** on the backend
and **vanilla HTML/CSS/JS** on the frontend — no React, no Vue, no JS framework.
Real Python code runs in-browser via **Pyodide (WebAssembly)**.

---

## 🗂 Project Structure

```
pythonquest/
├── app.py              ← Flask app + all lesson data (pure Python)
├── run.py              ← Quick dev launcher
├── build.sh            ← PyInstaller packaging script
├── requirements.txt
├── templates/
│   └── index.html      ← Jinja2 template (no React/Vue)
└── static/
    ├── css/style.css   ← Pure CSS (no Tailwind/Bootstrap)
    └── js/main.js      ← Vanilla JS (no React/jQuery)
```

---

## 🚀 Quick Start (Development)

```bash
# 1. Install dependencies
pip install flask

# 2. Run the app
python run.py
# OR
python app.py

# 3. Open browser → http://127.0.0.1:5000
```

The app **opens your browser automatically** when started.

---

## 📦 Package as Standalone Executable

```bash
# 1. Install PyInstaller
pip install pyinstaller

# 2. Build
chmod +x build.sh
./build.sh

# 3. Run the executable
./dist/PythonQuest        # Linux / macOS
dist\PythonQuest.exe      # Windows
```

The resulting binary:
- Is a **single self-contained file** (~15–30 MB)
- Includes Flask, Jinja2, and all templates/static files
- Opens the browser automatically on launch
- Requires **no Python installation** on the target machine

---

## ✨ Features

| Feature | Technology |
|---|---|
| Web server | **Flask** (Python) |
| HTML templating | **Jinja2** (Python) |
| Styling | **Pure CSS** |
| Interactivity | **Vanilla JS** |
| Real Python execution | **Pyodide** (WASM, in-browser) |
| AI quiz explanations | **Claude API** (via Flask proxy) |
| Packaging | **PyInstaller** |

---

## 📚 Content

- **10 Lessons** across 6 Worlds
- **50+ Challenges** with real code execution
- **Quiz system** with AI-powered explanations
- **XP, levels, streaks, achievements**
- **Progress auto-saved** in browser localStorage

### Worlds
| # | World | Topics |
|---|---|---|
| 0 | 🏰 The Foundations | print, variables, strings |
| 1 | 📊 Data Kingdoms | lists, dictionaries |
| 2 | ⚔️ Control Realms | if/else, loops |
| 3 | ⚙️ Function Forge | functions, lambdas |
| 4 | 🏯 OOP Citadel | classes, inheritance |
| 5 | 📁 File Frontier | file I/O, JSON, CSV |

---

## 🔑 Claude API (Optional)

Quiz explanations use the Claude API. The Flask server proxies the request
so no API key is exposed to the browser. To enable:

Set your key as an environment variable before starting:
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
python app.py
```

Or update `app.py` → `api_explain_quiz()` to read from `os.environ`.

Without the key, quizzes still work — explanations just show the correct answer.

---

## 🛠 Extending

All lesson data lives in `app.py` in the `LESSONS` list.
Each lesson is a plain Python dict — add new worlds, challenges, and quizzes there.
The Flask route `/api/check_challenge` validates code using keyword matching.
