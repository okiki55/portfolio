#!/usr/bin/env python3
"""Setup script to initialize the Flask project"""
import subprocess
import os

# Change to project root
project_root = "/vercel/share/v0-project"
os.chdir(project_root)

# Initialize uv project if not already done
if not os.path.exists("pyproject.toml"):
    subprocess.run(["uv", "init", "--bare", "."], check=True)

# Add required packages
packages = ["flask", "pillow", "numpy", "werkzeug"]
for package in packages:
    subprocess.run(["uv", "add", package], check=True)

print("Setup complete! Run with: uv run python app.py")
