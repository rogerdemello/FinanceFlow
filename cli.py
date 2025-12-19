"""Simple CLI to run demos and manage local DB for the Personal Finance Assistant.

Usage:
    python cli.py demo
    python cli.py aiml-demo
    python cli.py reset-db
"""
from pathlib import Path
import argparse
import subprocess
import sys

ROOT = Path(__file__).parent
DB = ROOT / "data" / "db.sqlite3"


def run_demo():
    subprocess.check_call([sys.executable, str(ROOT / "run_demo.py")])


def run_aiml_demo():
    subprocess.check_call([sys.executable, str(ROOT / "run_aiml_demo.py")])


def reset_db():
    if DB.exists():
        DB.unlink()
        print(f"Removed {DB}")
    else:
        print("No DB file to remove.")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("command", choices=["demo", "aiml-demo", "reset-db"]) 
    args = p.parse_args()

    if args.command == "demo":
        run_demo()
    elif args.command == "aiml-demo":
        run_aiml_demo()
    elif args.command == "reset-db":
        reset_db()


if __name__ == "__main__":
    main()
