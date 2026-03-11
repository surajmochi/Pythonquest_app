#!/usr/bin/env python3
"""
PythonQuest — Quick Launcher
Run this to start the app in development mode.
  python run.py
"""
import subprocess, sys, os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
subprocess.run([sys.executable, "app.py"])
