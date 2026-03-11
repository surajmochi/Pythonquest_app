"""
PythonQuest — Master Python
Flask Web Application (Pure Python Backend)
Run: python app.py
Package: pyinstaller --onefile --add-data "templates:templates" --add-data "static:static" app.py
"""

import json
import os
import sys
import threading
import webbrowser
from flask import Flask, render_template, jsonify, request, session

# ── Path resolution (works both dev and PyInstaller bundle) ──────────────────
if getattr(sys, "frozen", False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static"),
)
app.secret_key = "pythonquest-secret-2025"

# ── Lesson Data ──────────────────────────────────────────────────────────────
LESSONS = [
    # ── WORLD 0: FOUNDATIONS ────────────────────────────────────────────────
    {
        "world": 0, "id": "hello", "title": "Hello, Python World!", "icon": "🐍",
        "diff": "beginner", "xp": 50, "stars": 1,
        "story": (
            "You awaken in the Crystal Caverns of Code. A glowing serpent coils "
            "before you: \"To begin your quest, you must first speak — print "
            "something to the world!\""
        ),
        "theory": (
            "<strong>print()</strong> outputs text to the console — every Python "
            "programmer's first spell.\n\n"
            "<h4>BASIC SYNTAX</h4>"
            "<code>print(\"Hello, World!\")</code>\n"
            "<code>print('Single quotes work too')</code>\n"
            "<code>print(42)</code>  ← numbers too!\n\n"
            "<h4>SPECIAL CHARACTERS</h4>"
            "<code>\\n</code> = newline &nbsp; <code>\\t</code> = tab\n"
            "<code>print(\"Line1\\nLine2\")</code>"
        ),
        "examples": [
            {
                "title": "Example 1 — Basic Print",
                "code": 'print("Hello, World!")\nprint(\'Python is awesome!\')\nprint(42)\nprint(3.14)',
            },
            {
                "title": "Example 2 — Multiple Values",
                "code": (
                    'name = "Alice"\nage = 25\n'
                    'print("Name:", name, "Age:", age)\n'
                    'print(f"My name is {name} and I am {age} years old.")'
                ),
            },
        ],
        "challenges": [
            {"id": "h1", "title": "Say Hello", "diff": "beginner", "xp": 10,
             "desc": 'Print "Hello, World!" to the console.',
             "expected": '"Hello, World!"',
             "hint": 'print("Hello, World!")',
             "check_keywords": ["print(", "Hello"]},
            {"id": "h2", "title": "Your Name", "diff": "beginner", "xp": 10,
             "desc": "Print your name using print().",
             "expected": "your name",
             "hint": 'print("Your Name Here")',
             "check_keywords": ["print("]},
            {"id": "h3", "title": "Multiple Lines", "diff": "beginner", "xp": 15,
             "desc": "Print 3 different lines of text using 3 separate print() statements.",
             "expected": "3 lines of text",
             "hint": 'print("Line 1")\nprint("Line 2")\nprint("Line 3")',
             "check_min_prints": 3},
            {"id": "h4", "title": "Print a Number", "diff": "beginner", "xp": 10,
             "desc": "Print the number 42 using print().",
             "expected": "42",
             "hint": "print(42)",
             "check_keywords": ["print(", "42"]},
            {"id": "h5", "title": "Newline Escape", "diff": "intermediate", "xp": 20,
             "desc": r"Print two lines using a single print() statement with \n.",
             "expected": "two lines in one print",
             "hint": r'print("First Line\nSecond Line")',
             "check_keywords": ["\\n"],
             "check_max_prints": 1},
        ],
        "quizzes": [
            {"q": 'What does print("Hello") do?',
             "options": ["Stores Hello in memory", "Outputs Hello to the console", "Creates a variable", "None of the above"],
             "correct": 1},
            {"q": "Which is valid Python syntax?",
             "options": ['print[Hello]', 'Print("Hello")', 'print("Hello")', 'PRINT("Hello")'],
             "correct": 2},
            {"q": r"What character creates a new line inside a string?",
             "options": [r"\t", r"\r", r"\n", r"\b"],
             "correct": 2},
        ],
    },
    {
        "world": 0, "id": "variables", "title": "Variables & Data Types", "icon": "📦",
        "diff": "beginner", "xp": 60, "stars": 1,
        "story": (
            "The Variable Vault appears — shelves of magical containers. "
            "\"Label your containers,\" the Wizard says. \"A name, a value, a purpose.\""
        ),
        "theory": (
            "<strong>Variables</strong> store data. Python is dynamically typed!\n\n"
            "<h4>ASSIGNMENT</h4>"
            "<code>name = \"Alice\"</code>  ← string\n"
            "<code>age = 25</code>  ← integer\n"
            "<code>height = 5.8</code>  ← float\n"
            "<code>is_cool = True</code>  ← boolean\n\n"
            "<h4>DATA TYPES</h4>"
            "<ul>"
            "<li><code>str</code> — text: \"hello\"</li>"
            "<li><code>int</code> — whole numbers: 42</li>"
            "<li><code>float</code> — decimals: 3.14</li>"
            "<li><code>bool</code> — True / False</li>"
            "</ul>\n"
            "<h4>TYPE CONVERSION</h4>"
            "<code>int(\"42\")</code> → 42 &nbsp; "
            "<code>str(42)</code> → \"42\" &nbsp; "
            "<code>float(\"3.14\")</code> → 3.14"
        ),
        "examples": [
            {
                "title": "Example 1 — Variable Assignment",
                "code": (
                    'name = "Python"\nversion = 3\npi = 3.14159\nis_awesome = True\n'
                    "print(name, version, pi, is_awesome)\n"
                    "print(type(name), type(version))"
                ),
            },
            {
                "title": "Example 2 — Type Conversion",
                "code": (
                    'age_str = "25"\nage_int = int(age_str)\nprice = 9.99\n'
                    'price_str = str(price)\nprint(age_int + 5)\n'
                    'print("Price: $" + price_str)'
                ),
            },
        ],
        "challenges": [
            {"id": "v1", "title": "Create Variables", "diff": "beginner", "xp": 10,
             "desc": "Create: name (string), age (int), height (float), is_student (bool). Print all four.",
             "expected": "4 variable values printed",
             "hint": 'name = "Alice"\nage = 20\nheight = 5.6\nis_student = True\nprint(name, age, height, is_student)',
             "check_keywords": ["=", "print("]},
            {"id": "v2", "title": "Type Check", "diff": "beginner", "xp": 15,
             "desc": "Create a string, int, and float variable. Use type() to print each type.",
             "expected": "<class 'str'> <class 'int'> <class 'float'>",
             "hint": 's = "hello"\nn = 42\nf = 3.14\nprint(type(s))\nprint(type(n))\nprint(type(f))',
             "check_keywords": ["type("]},
            {"id": "v3", "title": "Type Conversion", "diff": "intermediate", "xp": 20,
             "desc": 'Convert "100" (string) to int and add 50. Convert 3.99 to int. Print both results.',
             "expected": "150 and 3",
             "hint": 's = "100"\nprint(int(s) + 50)\nprint(int(3.99))',
             "check_keywords": ["int("]},
            {"id": "v4", "title": "Multiple Assignment", "diff": "intermediate", "xp": 20,
             "desc": "Assign a, b, c = 10, 20, 30 on ONE line. Print all three.",
             "expected": "10 20 30",
             "hint": "a, b, c = 10, 20, 30\nprint(a, b, c)",
             "check_keywords": [",", "=", "print("]},
            {"id": "v5", "title": "Swap Variables", "diff": "intermediate", "xp": 25,
             "desc": "Create x=5 and y=10. Swap their values using tuple unpacking. Print before and after.",
             "expected": "before: 5 10  after: 10 5",
             "hint": "x = 5\ny = 10\nprint(x, y)\nx, y = y, x\nprint(x, y)",
             "check_any_keywords": ["y, x", "x, y = y, x"]},
        ],
        "quizzes": [
            {"q": "Which is a valid Python variable name?",
             "options": ["2name", "my-var", "my_var", "class"],
             "correct": 2},
            {"q": "What type is: x = 3.14?",
             "options": ["int", "str", "float", "double"],
             "correct": 2},
            {"q": 'What does int("42") return?',
             "options": ['"42"', "42", "42.0", "Error"],
             "correct": 1},
        ],
    },
    {
        "world": 0, "id": "strings", "title": "Strings — Text Magic", "icon": "✨",
        "diff": "beginner", "xp": 70, "stars": 1,
        "story": (
            "The Enchanted Library holds countless strings. \"Every character matters. "
            "Slice, format, transform — strings are the language of all languages.\""
        ),
        "theory": (
            "<strong>Strings</strong> are immutable sequences of characters.\n\n"
            "<h4>STRING METHODS</h4>"
            "<ul>"
            "<li><code>.upper()</code> / <code>.lower()</code></li>"
            "<li><code>.strip()</code> — remove whitespace</li>"
            "<li><code>.replace(old, new)</code></li>"
            "<li><code>.split(sep)</code> — split into list</li>"
            "<li><code>.join(list)</code></li>"
            "<li><code>.find(sub)</code> — index or -1</li>"
            "<li><code>.startswith()</code> / <code>.endswith()</code></li>"
            "</ul>\n"
            "<h4>F-STRINGS</h4>"
            "<code>f\"Hello {name}, you are {age}!\"</code>\n\n"
            "<h4>SLICING</h4>"
            "<code>s[0:3]</code> — chars 0,1,2 &nbsp; "
            "<code>s[-1]</code> — last &nbsp; "
            "<code>s[::-1]</code> — reverse"
        ),
        "examples": [
            {
                "title": "Example 1 — String Methods",
                "code": (
                    'msg = "  Hello, Python World!  "\n'
                    "print(msg.strip())\n"
                    "print(msg.upper())\n"
                    'print(msg.replace("Python", "Amazing"))\n'
                    "words = msg.strip().split(\", \")\nprint(words)"
                ),
            },
            {
                "title": "Example 2 — F-Strings & Slicing",
                "code": (
                    'name = "Pythonia"\nlevel = 42\n'
                    'print(f"Hero: {name}, Level: {level}")\n'
                    'print(f"Reversed: {name[::-1]}")\n'
                    'print(f"First 3: {name[:3]}")\n'
                    'print(f"Length: {len(name)}")'
                ),
            },
        ],
        "challenges": [
            {"id": "s1", "title": "String Methods", "diff": "beginner", "xp": 10,
             "desc": 'Store "hello world". Print it UPPERCASE and in title case (.title()).',
             "expected": "HELLO WORLD and Hello World",
             "hint": 's = "hello world"\nprint(s.upper())\nprint(s.title())',
             "check_keywords": [".upper()", ".title()"]},
            {"id": "s2", "title": "F-String Format", "diff": "beginner", "xp": 15,
             "desc": 'Create name and age variables. Print using f-string: "My name is X and I am Y years old."',
             "expected": "formatted sentence with name and age",
             "hint": 'name = "Alice"\nage = 20\nprint(f"My name is {name} and I am {age} years old.")',
             "check_keywords": ['f"', "{"]},
            {"id": "s3", "title": "String Slicing", "diff": "intermediate", "xp": 20,
             "desc": 'Store "Python Programming". Print: first 6 chars, reversed string, every other character.',
             "expected": "Python, reversed, alternating",
             "hint": 's = "Python Programming"\nprint(s[:6])\nprint(s[::-1])\nprint(s[::2])',
             "check_keywords": ["[:6]", "[::-1]"]},
            {"id": "s4", "title": "Split & Join", "diff": "intermediate", "xp": 20,
             "desc": 'Split "one,two,three,four" by comma. Join with " - ". Print both.',
             "expected": "list then joined string",
             "hint": 's = "one,two,three,four"\nparts = s.split(",")\nprint(parts)\nprint(" - ".join(parts))',
             "check_keywords": [".split(", ".join("]},
            {"id": "s5", "title": "Password Checker", "diff": "advanced", "xp": 40,
             "desc": "Create a password. Check: length >= 8, contains a digit, contains uppercase. Print all 3 checks.",
             "expected": "Length OK: True\nHas digit: True\nHas upper: True",
             "hint": 'pwd = "Python3Rocks"\nprint("Length OK:", len(pwd) >= 8)\nprint("Has digit:", any(c.isdigit() for c in pwd))\nprint("Has upper:", any(c.isupper() for c in pwd))',
             "check_keywords": ["len(", "isdigit"]},
        ],
        "quizzes": [
            {"q": 'What does "Python"[::-1] return?',
             "options": ["Python", "nohtyP", "Pytho", "Error"],
             "correct": 1},
            {"q": 'What does "  hello  ".strip() return?',
             "options": ['"  hello  "', '"hello"', '"hello  "', '"  hello"'],
             "correct": 1},
            {"q": 'What does "-".join(["a","b","c"]) return?',
             "options": ["a-b-c", '["a","b","c"]', "-a-b-c-", "a b c"],
             "correct": 0},
        ],
    },
    # ── WORLD 1: DATA TYPES ─────────────────────────────────────────────────
    {
        "world": 1, "id": "lists", "title": "Lists — Ordered Collections", "icon": "📋",
        "diff": "beginner", "xp": 90, "stars": 2,
        "story": (
            "You enter the Gallery of Lists — endless shelves, perfectly ordered. "
            "\"Zero-indexed!\" shouts the curator. \"The first item is ALWAYS position zero!\""
        ),
        "theory": (
            "<strong>Lists</strong> store ordered, mutable sequences.\n\n"
            "<h4>CREATING LISTS</h4>"
            "<code>fruits = [\"apple\", \"banana\", \"cherry\"]</code>\n"
            "<code>mixed = [1, \"hello\", True, 3.14]</code>\n\n"
            "<h4>INDEXING</h4>"
            "<code>fruits[0]</code> → \"apple\" &nbsp; "
            "<code>fruits[-1]</code> → \"cherry\" &nbsp; "
            "<code>fruits[1:3]</code> → slice\n\n"
            "<h4>KEY METHODS</h4>"
            "<ul>"
            "<li><code>.append(x)</code> — add to end</li>"
            "<li><code>.insert(i, x)</code> — insert at i</li>"
            "<li><code>.remove(x)</code> — remove first x</li>"
            "<li><code>.pop(i)</code> — remove & return</li>"
            "<li><code>.sort()</code> / <code>.reverse()</code></li>"
            "<li><code>.index(x)</code> / <code>.count(x)</code></li>"
            "</ul>\n"
            "<h4>FUNCTIONS</h4>"
            "<code>len()</code> <code>sum()</code> <code>min()</code> <code>max()</code> <code>sorted()</code>"
        ),
        "examples": [
            {
                "title": "Example 1 — List Operations",
                "code": (
                    'inventory = ["sword", "shield", "potion"]\n'
                    'inventory.append("torch")\n'
                    'inventory.insert(1, "armor")\n'
                    "print(inventory)\n"
                    'inventory.remove("shield")\n'
                    "last = inventory.pop()\n"
                    'print(f"Removed: {last}, Count: {len(inventory)}")'
                ),
            },
            {
                "title": "Example 2 — Comprehensions",
                "code": (
                    "squares = [x**2 for x in range(1, 11)]\n"
                    "print(squares)\n"
                    "evens = [n for n in range(1, 21) if n % 2 == 0]\n"
                    "print(evens)"
                ),
            },
        ],
        "challenges": [
            {"id": "l1", "title": "Shopping List", "diff": "beginner", "xp": 10,
             "desc": "Create a list with 5 grocery items. Print the list and its length.",
             "expected": "5-item list and length",
             "hint": 'groceries = ["milk","eggs","bread","butter","cheese"]\nprint(groceries)\nprint(len(groceries))',
             "check_keywords": ["[", "]", "len("]},
            {"id": "l2", "title": "First and Last", "diff": "beginner", "xp": 10,
             "desc": "Create a list of 5 numbers. Print the first element [0] and last [-1].",
             "expected": "first and last elements",
             "hint": "nums = [10,20,30,40,50]\nprint(nums[0])\nprint(nums[-1])",
             "check_keywords": ["[0]", "[-1]"]},
            {"id": "l3", "title": "Append & Remove", "diff": "beginner", "xp": 15,
             "desc": 'Start with ["cat","dog","bird"]. Append "fish". Remove "bird". Print.',
             "expected": "['cat', 'dog', 'fish']",
             "hint": 'pets = ["cat","dog","bird"]\npets.append("fish")\npets.remove("bird")\nprint(pets)',
             "check_keywords": [".append(", ".remove("]},
            {"id": "l4", "title": "Sort It Out", "diff": "beginner", "xp": 15,
             "desc": "Create [5,2,8,1,9,3]. Sort ascending, print. Sort descending, print.",
             "expected": "[1,2,3,5,8,9] then [9,8,5,3,2,1]",
             "hint": "n = [5,2,8,1,9,3]\nn.sort()\nprint(n)\nn.sort(reverse=True)\nprint(n)",
             "check_keywords": [".sort(", "reverse"]},
            {"id": "l5", "title": "Max Min Sum", "diff": "beginner", "xp": 20,
             "desc": "Create a list of 6 scores. Print the highest, lowest, and average.",
             "expected": "max min average",
             "hint": "scores = [75,88,92,61,79,95]\nprint(max(scores))\nprint(min(scores))\nprint(sum(scores)/len(scores))",
             "check_keywords": ["max(", "min(", "sum("]},
            {"id": "l6", "title": "Comprehension Squares", "diff": "intermediate", "xp": 30,
             "desc": "Use list comprehension to generate squares of odd numbers 1-20. Print.",
             "expected": "[1, 9, 25, 49, 81, 121, 169, 225, 289, 361]",
             "hint": "odds_sq = [x**2 for x in range(1,21) if x%2!=0]\nprint(odds_sq)",
             "check_keywords": ["for", "if", "**2"]},
            {"id": "l7", "title": "Top 3 Scores", "diff": "advanced", "xp": 50,
             "desc": "Given scores = [55,87,92,61,74,98,83,45,77,89]. Print top 3 without modifying original.",
             "expected": "top 3 scores highest to lowest",
             "hint": "scores = [55,87,92,61,74,98,83,45,77,89]\ntop3 = sorted(scores, reverse=True)[:3]\nprint('Top 3:', top3)",
             "check_keywords": ["sorted(", "reverse=True", "[:3]"]},
        ],
        "quizzes": [
            {"q": "What does list.pop() do by default?",
             "options": ["Removes the first element", "Removes and returns the last element", "Adds to the end", "Clears the list"],
             "correct": 1},
            {"q": "What is the output of: [1,2,3] + [4,5]?",
             "options": ["[1,2,3,4,5]", "[[1,2,3],[4,5]]", "[5,7]", "Error"],
             "correct": 0},
            {"q": "How do you access the last element of a list?",
             "options": ["data[last]", "data[-1]", "data[0-1]", "data.last()"],
             "correct": 1},
        ],
    },
    {
        "world": 1, "id": "dicts", "title": "Dictionaries — Key-Value Mastery", "icon": "🐉",
        "diff": "intermediate", "xp": 100, "stars": 2,
        "story": (
            "The Dragon of Dictionaries guards an infinite tome. \"Every treasure has a name,\" "
            "it rumbles. \"Give me the key — I give you the value.\""
        ),
        "theory": (
            "<strong>Dictionaries</strong> store key-value pairs.\n\n"
            "<h4>CREATING</h4>"
            "<code>person = {\"name\": \"Alice\", \"age\": 30}</code>\n\n"
            "<h4>ACCESSING</h4>"
            "<code>person[\"name\"]</code> → \"Alice\" (KeyError if missing!)\n"
            "<code>person.get(\"phone\", \"N/A\")</code> → safe\n\n"
            "<h4>MODIFYING</h4>"
            "<code>person[\"email\"] = \"a@b.com\"</code>\n"
            "<code>del person[\"city\"]</code>\n"
            "<code>person.update({\"age\": 31})</code>\n\n"
            "<h4>KEY METHODS</h4>"
            "<ul>"
            "<li><code>.keys()</code> <code>.values()</code> <code>.items()</code></li>"
            "<li><code>.get(key, default)</code> — safe access</li>"
            "<li><code>.pop(key)</code> — remove & return</li>"
            "</ul>\n"
            "<h4>COMPREHENSIONS</h4>"
            "<code>{k: v*2 for k, v in d.items()}</code>"
        ),
        "examples": [
            {
                "title": "Example 1 — Dict Basics",
                "code": (
                    'hero = {"name": "Pythonia", "level": 5, "hp": 100}\n'
                    'print(hero["name"])\nhero["level"] += 1\nhero["mana"] = 50\n'
                    'del hero["hp"]\nprint(hero)'
                ),
            },
            {
                "title": "Example 2 — Looping & Methods",
                "code": (
                    'grades = {"math":92,"english":85,"science":78}\n'
                    "for subject, grade in grades.items():\n"
                    '    print(f"{subject}: {grade}")\n'
                    "print(\"Average:\", sum(grades.values()) / len(grades))\n"
                    'print(grades.get("art", "Not taken"))'
                ),
            },
        ],
        "challenges": [
            {"id": "d1", "title": "Profile Dict", "diff": "beginner", "xp": 10,
             "desc": "Create a dict with keys: name, age, city, hobby. Print it.",
             "expected": "profile dict",
             "hint": 'profile = {"name":"Alex","age":20,"city":"NY","hobby":"coding"}\nprint(profile)',
             "check_keywords": ["{", ":", "print"]},
            {"id": "d2", "title": "Safe Get", "diff": "beginner", "xp": 15,
             "desc": 'Create a dict. Use .get() for a key that exists and one that doesn\'t (default "Not Found").',
             "expected": "value and Not Found",
             "hint": 'd = {"x":10,"y":20}\nprint(d.get("x"))\nprint(d.get("z","Not Found"))',
             "check_keywords": [".get(", "Not Found"]},
            {"id": "d3", "title": "Loop Items", "diff": "intermediate", "xp": 25,
             "desc": 'Create a dict of 4 country:capital pairs. Loop with .items() printing "Capital of X is Y".',
             "expected": "formatted country-capital pairs",
             "hint": 'caps = {"France":"Paris","Japan":"Tokyo","Brazil":"Brasilia","India":"Delhi"}\nfor country, capital in caps.items():\n    print(f"Capital of {country} is {capital}")',
             "check_keywords": [".items()", "for"]},
            {"id": "d4", "title": "Word Counter", "diff": "intermediate", "xp": 30,
             "desc": 'Count word occurrences in "the cat sat on the mat the cat" using a dict.',
             "expected": "word frequency dict",
             "hint": 'text = "the cat sat on the mat the cat"\ncounts = {}\nfor word in text.split():\n    counts[word] = counts.get(word, 0) + 1\nprint(counts)',
             "check_keywords": [".get(", "for", "split()"]},
            {"id": "d5", "title": "Dict Comprehension", "diff": "advanced", "xp": 40,
             "desc": "Create a dict comprehension: keys 1-10, values are their squares.",
             "expected": "{1: 1, 2: 4, 3: 9, ...}",
             "hint": "squares = {n: n**2 for n in range(1,11)}\nprint(squares)",
             "check_keywords": ["for n in range", "**2"]},
        ],
        "quizzes": [
            {"q": "What is the safest way to access a dict key that might not exist?",
             "options": ["dict[key]", "dict.access(key)", "dict.get(key, default)", "dict.find(key)"],
             "correct": 2},
            {"q": "What does dict.items() return?",
             "options": ["A list of keys", "A list of values", "View of (key, value) pairs", "A sorted dict"],
             "correct": 2},
            {"q": "What happens when you access a missing key with dict[key]?",
             "options": ["Returns None", "Returns False", "Raises KeyError", "Returns empty string"],
             "correct": 2},
        ],
    },
    # ── WORLD 2: CONTROL FLOW ───────────────────────────────────────────────
    {
        "world": 2, "id": "ifelse", "title": "If / Else — Decision Maker", "icon": "⚔️",
        "diff": "beginner", "xp": 80, "stars": 2,
        "story": (
            "The Crossroads of Choices. The ancient If-Stone speaks: \"If your condition is True, "
            "go left. Else go right. Elif there is another way…\""
        ),
        "theory": (
            "<strong>Conditional statements</strong> control program flow.\n\n"
            "<h4>IF-ELIF-ELSE</h4>"
            "<code>if score >= 90: grade = \"A\"\nelif score >= 80: grade = \"B\"\nelse: grade = \"F\"</code>\n\n"
            "<h4>COMPARISON OPERATORS</h4>"
            "<code>==</code> <code>!=</code> <code>&gt;</code> <code>&lt;</code> "
            "<code>&gt;=</code> <code>&lt;=</code>\n\n"
            "<h4>LOGICAL OPERATORS</h4>"
            "<code>and</code> <code>or</code> <code>not</code>\n\n"
            "<h4>TERNARY</h4>"
            "<code>result = \"yes\" if x > 0 else \"no\"</code>"
        ),
        "examples": [
            {
                "title": "Example 1 — Grade Calculator",
                "code": (
                    "score = 85\n"
                    "if score >= 90:\n    grade = \"A\"\n"
                    "elif score >= 80:\n    grade = \"B\"\n"
                    "elif score >= 70:\n    grade = \"C\"\n"
                    "else:\n    grade = \"F\"\n"
                    'print(f"Score: {score}, Grade: {grade}")'
                ),
            },
            {
                "title": "Example 2 — Logical Operators",
                "code": (
                    "age = 25\nhas_id = True\n"
                    "if age >= 18 and has_id:\n    print(\"Access granted!\")\n"
                    "else:\n    print(\"Access denied!\")\n"
                    'x = 0\nprint("zero" if x == 0 else "non-zero")'
                ),
            },
        ],
        "challenges": [
            {"id": "i1", "title": "Positive/Negative", "diff": "beginner", "xp": 10,
             "desc": 'Store a number. Print "Positive", "Negative", or "Zero".',
             "expected": "Positive, Negative, or Zero",
             "hint": "num = -5\nif num > 0:\n    print('Positive')\nelif num < 0:\n    print('Negative')\nelse:\n    print('Zero')",
             "check_keywords": ["if", "else"]},
            {"id": "i2", "title": "Grade Calculator", "diff": "beginner", "xp": 15,
             "desc": "Store a score. Print grade: A(>=90), B(>=80), C(>=70), D(>=60), F(below 60).",
             "expected": "correct grade letter",
             "hint": "score = 85\nif score >= 90: print('A')\nelif score >= 80: print('B')\nelif score >= 70: print('C')\nelif score >= 60: print('D')\nelse: print('F')",
             "check_keywords": ["elif"]},
            {"id": "i3", "title": "Even or Odd", "diff": "beginner", "xp": 15,
             "desc": "Use modulo (%) to check if a number is even or odd. Print result.",
             "expected": "even or odd",
             "hint": "n = 7\nif n % 2 == 0:\n    print(f'{n} is even')\nelse:\n    print(f'{n} is odd')",
             "check_keywords": ["%", "if"]},
            {"id": "i4", "title": "FizzBuzz", "diff": "intermediate", "xp": 30,
             "desc": 'For 1-20: print "Fizz" (÷3), "Buzz" (÷5), "FizzBuzz" (÷both), else number.',
             "expected": "1 2 Fizz 4 Buzz Fizz...",
             "hint": "for n in range(1, 21):\n    if n % 3 == 0 and n % 5 == 0:\n        print('FizzBuzz')\n    elif n % 3 == 0:\n        print('Fizz')\n    elif n % 5 == 0:\n        print('Buzz')\n    else:\n        print(n)",
             "check_keywords": ["Fizz", "Buzz", "for"]},
            {"id": "i5", "title": "Login System", "diff": "advanced", "xp": 40,
             "desc": 'Set username="admin" password="secret123". Check match, print "Login successful" or "Invalid credentials".',
             "expected": "Login successful or Invalid credentials",
             "hint": 'username = "admin"\npassword = "secret123"\nif username == "admin" and password == "secret123":\n    print("Login successful!")\nelse:\n    print("Invalid credentials!")',
             "check_keywords": ["and", "==", "if"]},
        ],
        "quizzes": [
            {"q": "What does elif stand for?",
             "options": ["else if", "else in loop", "extra if", "end if"],
             "correct": 0},
            {"q": 'What is the output of: x=5; print("big" if x>3 else "small")?',
             "options": ["big", "small", "True", "Error"],
             "correct": 0},
            {"q": 'What does "not True" evaluate to?',
             "options": ["True", "False", "None", "Error"],
             "correct": 1},
        ],
    },
    {
        "world": 2, "id": "loops", "title": "Loops — Power of Repetition", "icon": "🔄",
        "diff": "beginner", "xp": 90, "stars": 2,
        "story": (
            "The Infinite Treadmill. \"One step, then another,\" says the Loop Sage. "
            "\"Until the condition fails, or you break free. Repetition is power!\""
        ),
        "theory": (
            "<strong>Loops</strong> repeat code blocks.\n\n"
            "<h4>FOR LOOP</h4>"
            "<code>for i in range(5):\n    print(i)  # 0,1,2,3,4</code>\n\n"
            "<h4>WHILE LOOP</h4>"
            "<code>count = 0\nwhile count &lt; 5:\n    count += 1</code>\n\n"
            "<h4>RANGE</h4>"
            "<code>range(5)</code> → 0-4 &nbsp; "
            "<code>range(1,6)</code> → 1-5 &nbsp; "
            "<code>range(0,10,2)</code> → 0,2,4,6,8\n\n"
            "<h4>CONTROL</h4>"
            "<code>break</code> — exit loop &nbsp; "
            "<code>continue</code> — skip iteration\n\n"
            "<h4>ENUMERATE</h4>"
            "<code>for i, val in enumerate(list):</code>"
        ),
        "examples": [
            {
                "title": "Example 1 — For Loop Patterns",
                "code": (
                    "for i in range(1, 6):\n"
                    "    print(f\"Step {i}: {'*' * i}\")\n"
                    'colors = ["red", "green", "blue"]\n'
                    "for idx, color in enumerate(colors):\n"
                    '    print(f"{idx}: {color}")'
                ),
            },
            {
                "title": "Example 2 — While Loop",
                "code": (
                    "total = 0\ncount = 1\n"
                    "while count <= 10:\n    total += count\n    count += 1\n"
                    'print(f"Sum 1-10: {total}")'
                ),
            },
        ],
        "challenges": [
            {"id": "lo1", "title": "Count to 10", "diff": "beginner", "xp": 10,
             "desc": "Use a for loop to print numbers 1 through 10.",
             "expected": "1 2 3 4 5 6 7 8 9 10",
             "hint": "for i in range(1, 11):\n    print(i)",
             "check_keywords": ["for", "range("]},
            {"id": "lo2", "title": "Sum 1 to 100", "diff": "beginner", "xp": 15,
             "desc": "Use a loop to calculate sum of all numbers from 1 to 100. Print result.",
             "expected": "5050",
             "hint": "total = 0\nfor i in range(1, 101):\n    total += i\nprint(total)",
             "check_any_keywords": ["+=", "sum("]},
            {"id": "lo3", "title": "Multiplication Table", "diff": "intermediate", "xp": 25,
             "desc": "Print the 7 times table (7×1 to 7×10) using a loop.",
             "expected": "7 x 1 = 7 ... 7 x 10 = 70",
             "hint": "for i in range(1, 11):\n    print(f'7 x {i} = {7*i}')",
             "check_keywords": ["for", "range("]},
            {"id": "lo4", "title": "While Countdown", "diff": "intermediate", "xp": 20,
             "desc": 'Use a while loop to count down from 10 to 1, then print "Blast off!"',
             "expected": "10 9 8 ... 1 Blast off!",
             "hint": "n = 10\nwhile n > 0:\n    print(n)\n    n -= 1\nprint('Blast off!')",
             "check_keywords": ["while", "Blast off"]},
            {"id": "lo5", "title": "Enumerate Loop", "diff": "intermediate", "xp": 25,
             "desc": 'Create a list of 5 fruits. Use enumerate() to print "0: apple", "1: banana" etc.',
             "expected": "0: fruit1, 1: fruit2...",
             "hint": 'fruits = ["apple","banana","cherry","mango","grape"]\nfor i, f in enumerate(fruits):\n    print(f"{i}: {f}")',
             "check_keywords": ["enumerate("]},
            {"id": "lo6", "title": "FizzBuzz Loop", "diff": "intermediate", "xp": 35,
             "desc": 'Print FizzBuzz for 1-20: "Fizz" (÷3), "Buzz" (÷5), "FizzBuzz" (÷both).',
             "expected": "1 2 Fizz 4 Buzz Fizz 7...",
             "hint": "for n in range(1,21):\n    if n%3==0 and n%5==0: print('FizzBuzz')\n    elif n%3==0: print('Fizz')\n    elif n%5==0: print('Buzz')\n    else: print(n)",
             "check_keywords": ["FizzBuzz", "for"]},
        ],
        "quizzes": [
            {"q": "What does range(2, 8, 2) produce?",
             "options": ["[2,4,6]", "[2,4,6,8]", "[4,6,8]", "[2,8,2]"],
             "correct": 0},
            {"q": 'What does "break" do in a loop?',
             "options": ["Skips current iteration", "Exits the loop entirely", "Pauses the loop", "Restarts the loop"],
             "correct": 1},
            {"q": "What does enumerate() give you?",
             "options": ["Only values", "Only indices", "Both index and value", "A sorted list"],
             "correct": 2},
        ],
    },
    # ── WORLD 3: FUNCTIONS ──────────────────────────────────────────────────
    {
        "world": 3, "id": "functions", "title": "Functions — Reusable Power", "icon": "⚙️",
        "diff": "intermediate", "xp": 110, "stars": 2,
        "story": (
            "The Function Forge glows with magical energy. \"Write once, call anywhere,\" "
            "the Blacksmith announces. \"A function is a spell — define it and summon it anywhere.\""
        ),
        "theory": (
            "<strong>Functions</strong> are named, reusable code blocks.\n\n"
            "<h4>DEFINING</h4>"
            "<code>def greet(name):\n    return f\"Hello, {name}!\"</code>\n\n"
            "<h4>DEFAULT PARAMETERS</h4>"
            "<code>def greet(name, greeting=\"Hello\"):</code>\n\n"
            "<h4>MULTIPLE RETURNS</h4>"
            "<code>def min_max(lst):\n    return min(lst), max(lst)\nlo, hi = min_max([1,5,3])</code>\n\n"
            "<h4>*ARGS / **KWARGS</h4>"
            "<code>def total(*args): return sum(args)\n"
            "def show(**kwargs):\n    for k,v in kwargs.items(): print(k,v)</code>\n\n"
            "<h4>LAMBDA</h4>"
            "<code>square = lambda x: x**2</code>"
        ),
        "examples": [
            {
                "title": "Example 1 — Basic Functions",
                "code": (
                    'def greet(name, greeting="Hello"):\n'
                    '    return f"{greeting}, {name}!"\n\n'
                    'print(greet("Alice"))\n'
                    'print(greet("Bob", "Hi"))\n\n'
                    "def bmi(weight, height):\n"
                    "    return round(weight / height**2, 2)\n\n"
                    'print(f"BMI: {bmi(70, 1.75)}")'
                ),
            },
            {
                "title": "Example 2 — *args & Lambda",
                "code": (
                    "def total(*args):\n    return sum(args)\n\n"
                    "print(total(1, 2, 3, 4, 5))\n\n"
                    "square = lambda x: x**2\n"
                    "print(list(map(square, [1,2,3,4,5])))"
                ),
            },
        ],
        "challenges": [
            {"id": "fn1", "title": "Square Function", "diff": "beginner", "xp": 15,
             "desc": "Write square(n) that returns n squared. Call it with 5 and print.",
             "expected": "25",
             "hint": "def square(n):\n    return n**2\nprint(square(5))",
             "check_keywords": ["def ", "return"]},
            {"id": "fn2", "title": "Default Parameter", "diff": "beginner", "xp": 20,
             "desc": 'Write greet(name, greeting="Hello") that returns a greeting string. Test both ways.',
             "expected": "Hello Alice! and Hi Bob!",
             "hint": 'def greet(name, greeting="Hello"):\n    return f"{greeting} {name}!"\nprint(greet("Alice"))\nprint(greet("Bob", "Hi"))',
             "check_keywords": ["def ", "=", "return"]},
            {"id": "fn3", "title": "Multiple Returns", "diff": "intermediate", "xp": 25,
             "desc": "Write stats(numbers) returning min, max, average. Unpack and print all three.",
             "expected": "min max average values",
             "hint": "def stats(nums):\n    return min(nums), max(nums), sum(nums)/len(nums)\nlo, hi, avg = stats([10,20,30,40,50])\nprint(lo, hi, avg)",
             "check_keywords": ["def ", "return", ","]},
            {"id": "fn4", "title": "*args Function", "diff": "intermediate", "xp": 30,
             "desc": "Write multiply_all(*args) that returns the product of all arguments. Test it.",
             "expected": "product of all args",
             "hint": "def multiply_all(*args):\n    result = 1\n    for n in args:\n        result *= n\n    return result\nprint(multiply_all(2,3,4,5))",
             "check_keywords": ["*args", "def "]},
            {"id": "fn5", "title": "Recursive Factorial", "diff": "advanced", "xp": 50,
             "desc": "Write recursive factorial(n). Print factorials for 1 through 7.",
             "expected": "1 2 6 24 120 720 5040",
             "hint": "def factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n-1)\nfor i in range(1,8):\n    print(factorial(i))",
             "check_keywords": ["def factorial", "factorial(", "return"]},
        ],
        "quizzes": [
            {"q": "What keyword defines a function?",
             "options": ["function", "define", "def", "func"],
             "correct": 2},
            {"q": "What does *args allow?",
             "options": ["Only keyword args", "Any number of positional args", "Default values", "Nothing"],
             "correct": 1},
            {"q": "What does a function return with no return statement?",
             "options": ["0", '""', "None", "Error"],
             "correct": 2},
        ],
    },
    # ── WORLD 4: OOP ────────────────────────────────────────────────────────
    {
        "world": 4, "id": "oop", "title": "Classes & OOP", "icon": "🏯",
        "diff": "advanced", "xp": 130, "stars": 3,
        "story": (
            "The OOP Citadel rises before you. \"A class is a blueprint, an object is the building,\" "
            "the Architect explains. \"Attributes hold data, methods hold behavior.\""
        ),
        "theory": (
            "<strong>Object-Oriented Programming</strong> organizes code as classes & objects.\n\n"
            "<h4>DEFINING A CLASS</h4>"
            "<code>class Dog:\n    def __init__(self, name, age):\n        self.name = name\n"
            "        self.age = age\n    def bark(self):\n        return f\"{self.name} says Woof!\"</code>\n\n"
            "<h4>CREATING OBJECTS</h4>"
            "<code>my_dog = Dog(\"Rex\", 3)\nprint(my_dog.bark())</code>\n\n"
            "<h4>INHERITANCE</h4>"
            "<code>class GuideDog(Dog):\n    def __init__(self, name, age, owner):\n"
            "        super().__init__(name, age)</code>\n\n"
            "<h4>MAGIC METHODS</h4>"
            "<code>__str__</code> <code>__len__</code> <code>__add__</code> <code>__eq__</code>"
        ),
        "examples": [
            {
                "title": "Example 1 — Basic Class",
                "code": (
                    "class Hero:\n"
                    "    def __init__(self, name, hp=100):\n"
                    "        self.name = name\n        self.hp = hp\n        self.level = 1\n\n"
                    "    def attack(self, target):\n"
                    "        damage = self.level * 10\n"
                    "        target.hp -= damage\n"
                    '        return f"{self.name} deals {damage} damage!"\n\n'
                    "    def __str__(self):\n"
                    '        return f"Hero({self.name}, HP:{self.hp})"\n\n'
                    'hero = Hero("Pythonia")\nenemy = Hero("Goblin", 50)\n'
                    "print(hero.attack(enemy))\nprint(enemy)"
                ),
            },
            {
                "title": "Example 2 — Inheritance",
                "code": (
                    "class Animal:\n    def __init__(self, name):\n        self.name = name\n"
                    "    def speak(self):\n        return '...'\n\n"
                    "class Dog(Animal):\n"
                    '    def speak(self): return f"{self.name} says Woof!"\n\n'
                    "class Cat(Animal):\n"
                    '    def speak(self): return f"{self.name} says Meow!"\n\n'
                    'animals = [Dog("Rex"), Cat("Luna")]\n'
                    "for a in animals:\n    print(a.speak())"
                ),
            },
        ],
        "challenges": [
            {"id": "oo1", "title": "Simple Class", "diff": "intermediate", "xp": 25,
             "desc": "Create a Car class with make, model, year attributes and a describe() method.",
             "expected": "car description printed",
             "hint": 'class Car:\n    def __init__(self, make, model, year):\n        self.make = make\n        self.model = model\n        self.year = year\n    def describe(self):\n        print(f"{self.year} {self.make} {self.model}")\nmy_car = Car("Toyota","Camry",2023)\nmy_car.describe()',
             "check_keywords": ["class ", "def __init__", "self."]},
            {"id": "oo2", "title": "Counter Class", "diff": "intermediate", "xp": 30,
             "desc": "Build Counter class with count=0, increment(), decrement(), reset(). Test all.",
             "expected": "counter operations working",
             "hint": "class Counter:\n    def __init__(self):\n        self.count = 0\n    def increment(self): self.count += 1\n    def decrement(self): self.count -= 1\n    def reset(self): self.count = 0\nc = Counter()\nc.increment()\nc.increment()\nprint(c.count)\nc.reset()\nprint(c.count)",
             "check_keywords": ["class ", "def ", "self.count"]},
            {"id": "oo3", "title": "Inheritance", "diff": "advanced", "xp": 45,
             "desc": "Create Animal base class with speak(). Create Dog and Cat subclasses overriding speak(). Call each.",
             "expected": "Woof! and Meow!",
             "hint": "class Animal:\n    def speak(self): return '...'\nclass Dog(Animal):\n    def speak(self): return 'Woof!'\nclass Cat(Animal):\n    def speak(self): return 'Meow!'\nprint(Dog().speak())\nprint(Cat().speak())",
             "check_keywords": ["class ", "(Animal)", "def speak"]},
            {"id": "oo4", "title": "__str__ Method", "diff": "advanced", "xp": 35,
             "desc": 'Create Person with name, age. Implement __str__ so print(person) shows "Person(name=Alice, age=30)".',
             "expected": "Person(name=..., age=...)",
             "hint": 'class Person:\n    def __init__(self, name, age):\n        self.name = name\n        self.age = age\n    def __str__(self):\n        return f"Person(name={self.name}, age={self.age})"\nprint(Person("Alice", 30))',
             "check_keywords": ["__str__", "return"]},
        ],
        "quizzes": [
            {"q": "What is __init__ in Python?",
             "options": ["A function to end a class", "The class constructor/initializer", "A private variable", "A static method"],
             "correct": 1},
            {"q": 'What does "self" refer to in a method?',
             "options": ["The class itself", "The current instance", "The parent class", "A global variable"],
             "correct": 1},
            {"q": "What magic method makes a class printable?",
             "options": ["__print__", "__display__", "__str__", "__output__"],
             "correct": 2},
        ],
    },
    # ── WORLD 5: FILES ──────────────────────────────────────────────────────
    {
        "world": 5, "id": "files", "title": "File I/O & Data Persistence", "icon": "📁",
        "diff": "intermediate", "xp": 110, "stars": 2,
        "story": (
            "The Archive Dimension. \"Files persist beyond memory,\" the Archivist says. "
            "\"Write to disk. Read from disk. JSON, CSV — the universal tongues.\""
        ),
        "theory": (
            "<strong>File I/O</strong> lets Python read/write data to disk.\n\n"
            "<h4>OPENING FILES</h4>"
            "<code>with open(\"file.txt\", \"r\") as f:\n    content = f.read()</code>\n\n"
            "Modes: <code>\"r\"</code> read &nbsp; <code>\"w\"</code> write &nbsp; "
            "<code>\"a\"</code> append &nbsp; <code>\"rb\"</code> binary\n\n"
            "<h4>READING</h4>"
            "<code>f.read()</code> — entire file\n"
            "<code>f.readlines()</code> — list of lines\n"
            "<code>for line in f:</code> — line by line\n\n"
            "<h4>JSON</h4>"
            "<code>import json\njson.dump(data, f, indent=4)\njson.load(f)</code>\n\n"
            "<h4>CSV</h4>"
            "<code>import csv\ncsv.writer(f).writerow([...])</code>"
        ),
        "examples": [
            {
                "title": "Example 1 — Text Files",
                "code": (
                    'with open("demo.txt", "w") as f:\n'
                    '    f.write("Hello, File World!\\n")\n'
                    '    f.write("Line 2\\n")\n\n'
                    'with open("demo.txt", "r") as f:\n'
                    "    content = f.read()\nprint(content)"
                ),
            },
            {
                "title": "Example 2 — JSON",
                "code": (
                    "import json\n\n"
                    'profile = {"name": "Alice", "level": 5, "skills": ["Python"]}\n'
                    'with open("profile.json", "w") as f:\n'
                    "    json.dump(profile, f, indent=4)\n\n"
                    'with open("profile.json") as f:\n'
                    "    loaded = json.load(f)\nprint(loaded)"
                ),
            },
        ],
        "challenges": [
            {"id": "fi1", "title": "Write and Read", "diff": "beginner", "xp": 15,
             "desc": 'Write 3 lines to "test.txt". Read it back and print.',
             "expected": "3 lines printed",
             "hint": 'with open("test.txt","w") as f:\n    f.write("Line 1\\n")\n    f.write("Line 2\\n")\n    f.write("Line 3\\n")\nwith open("test.txt") as f:\n    print(f.read())',
             "check_keywords": ['open(', '"w"']},
            {"id": "fi2", "title": "JSON Save", "diff": "beginner", "xp": 20,
             "desc": "Create a profile dict. Save to JSON with indent=4. Read and print.",
             "expected": "profile json printed",
             "hint": 'import json\nprofile = {"name":"Alex","age":22,"skills":["Python"]}\nwith open("profile.json","w") as f:\n    json.dump(profile, f, indent=4)\nwith open("profile.json") as f:\n    print(json.load(f))',
             "check_keywords": ["json.dump", "json.load"]},
            {"id": "fi3", "title": "Count Lines", "diff": "intermediate", "xp": 25,
             "desc": "Write a file with 5+ lines. Read with readlines() and print the line count.",
             "expected": "Lines: 5",
             "hint": 'with open("data.txt","w") as f:\n    for i in range(5): f.write(f"Line {i+1}\\n")\nwith open("data.txt") as f:\n    lines = f.readlines()\nprint(f"Lines: {len(lines)}")',
             "check_keywords": ["readlines()", "len("]},
            {"id": "fi4", "title": "Error Handling", "diff": "intermediate", "xp": 25,
             "desc": "Try to open a non-existent file. Catch FileNotFoundError and print a message.",
             "expected": "File not found: ...",
             "hint": "try:\n    with open('ghost.txt') as f:\n        print(f.read())\nexcept FileNotFoundError:\n    print('File not found: ghost.txt')",
             "check_keywords": ["FileNotFoundError", "except"]},
            {"id": "fi5", "title": "CSV Writer", "diff": "advanced", "xp": 40,
             "desc": "Use csv module: write header + 3 rows, read back and print each row.",
             "expected": "csv rows printed",
             "hint": 'import csv\nrows = [["Alice",92,"A"],["Bob",78,"C"],["Carol",85,"B"]]\nwith open("grades.csv","w",newline="") as f:\n    w = csv.writer(f)\n    w.writerow(["name","score","grade"])\n    w.writerows(rows)\nwith open("grades.csv") as f:\n    for row in csv.reader(f): print(row)',
             "check_keywords": ["import csv", "writerow"]},
        ],
        "quizzes": [
            {"q": "Which file mode appends without overwriting?",
             "options": ['"w"', '"r"', '"a"', '"x"'],
             "correct": 2},
            {"q": "What does json.load(f) do?",
             "options": ["Writes JSON to file", "Reads JSON from file object", "Converts dict to string", "Loads a module"],
             "correct": 1},
            {"q": 'What does "with open()" ensure?',
             "options": ["Fast reading", "File is automatically closed", "Error handling", "Binary mode"],
             "correct": 1},
        ],
    },
]

WORLDS = [
    {"id": 0, "name": "The Foundations",  "icon": "🏰"},
    {"id": 1, "name": "Data Kingdoms",    "icon": "📊"},
    {"id": 2, "name": "Control Realms",   "icon": "⚔️"},
    {"id": 3, "name": "Function Forge",   "icon": "⚙️"},
    {"id": 4, "name": "OOP Citadel",      "icon": "🏯"},
    {"id": 5, "name": "File Frontier",    "icon": "📁"},
]

ACHIEVEMENTS = [
    {"id": "first_code",  "icon": "🌟", "name": "First Blood",      "desc": "Complete your first challenge"},
    {"id": "streak5",     "icon": "🔥", "name": "On Fire",           "desc": "5-challenge streak"},
    {"id": "streak10",    "icon": "💥", "name": "Unstoppable",       "desc": "10-challenge streak"},
    {"id": "quiz10",      "icon": "🧠", "name": "Quiz Wizard",       "desc": "10 quiz questions correct"},
    {"id": "halfway",     "icon": "⚡", "name": "Halfway Hero",      "desc": "Complete half all challenges"},
    {"id": "oop_done",    "icon": "🏯", "name": "OOP Master",        "desc": "All OOP challenges done"},
    {"id": "files_done",  "icon": "📁", "name": "File Whisperer",    "desc": "All File I/O challenges done"},
    {"id": "master",      "icon": "🏆", "name": "Python Legend",     "desc": "Complete every challenge"},
]


# ── Helper: challenge check ──────────────────────────────────────────────────
def check_challenge(code: str, challenge: dict) -> bool:
    kws      = challenge.get("check_keywords", [])
    any_kws  = challenge.get("check_any_keywords", [])
    min_p    = challenge.get("check_min_prints")
    max_p    = challenge.get("check_max_prints")

    if kws and not all(k in code for k in kws):
        return False
    if any_kws and not any(k in code for k in any_kws):
        return False
    if min_p is not None and code.count("print(") < min_p:
        return False
    if max_p is not None and code.count("print(") > max_p:
        return False
    return True


# ── Routes ───────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    total_challenges = sum(len(l["challenges"]) for l in LESSONS)
    return render_template(
        "index.html",
        lessons=LESSONS,
        worlds=WORLDS,
        achievements=ACHIEVEMENTS,
        total_challenges=total_challenges,
        lessons_json=json.dumps(LESSONS),
        worlds_json=json.dumps(WORLDS),
        achievements_json=json.dumps(ACHIEVEMENTS),
    )


@app.route("/api/check_challenge", methods=["POST"])
def api_check_challenge():
    data        = request.get_json()
    code        = data.get("code", "")
    lesson_id   = data.get("lesson_id")
    challenge_id = data.get("challenge_id")

    lesson    = next((l for l in LESSONS if l["id"] == lesson_id), None)
    if not lesson:
        return jsonify({"ok": False, "error": "Lesson not found"}), 404

    challenge = next((c for c in lesson["challenges"] if c["id"] == challenge_id), None)
    if not challenge:
        return jsonify({"ok": False, "error": "Challenge not found"}), 404

    passed = check_challenge(code, challenge)
    return jsonify({"ok": True, "passed": passed, "xp": challenge["xp"]})


@app.route("/api/lessons")
def api_lessons():
    return jsonify(LESSONS)


@app.route("/api/explain_quiz", methods=["POST"])
def api_explain_quiz():
    """Proxy to Claude API — keeps API key server-side."""
    import urllib.request
    data = request.get_json()
    payload = json.dumps({
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 400,
        "messages": [{"role": "user", "content": data.get("prompt", "")}],
    }).encode()
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            result = json.loads(resp.read())
        return jsonify({"text": result["content"][0]["text"]})
    except Exception as e:
        return jsonify({"text": "", "error": str(e)}), 200


# ── Launcher ─────────────────────────────────────────────────────────────────
def open_browser():
    import time
    time.sleep(1.2)
    webbrowser.open("http://127.0.0.1:5000")


if __name__ == "__main__":
    print("=" * 55)
    print("  🐍 PythonQuest — Starting server…")
    print("  🌐 Opening http://127.0.0.1:5000")
    print("  Press Ctrl+C to quit.")
    print("=" * 55)
    threading.Thread(target=open_browser, daemon=True).start()
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)
