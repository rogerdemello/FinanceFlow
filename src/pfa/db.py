"""Simple SQLite persistence helpers for Personal Finance Assistant."""
from __future__ import annotations
import sqlite3
from typing import Optional
import os


def init_db(db_path: str) -> None:
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        date TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS debts (
        name TEXT PRIMARY KEY,
        balance REAL,
        interest REAL,
        minimum REAL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS savings_goals (
        name TEXT PRIMARY KEY,
        amount REAL,
        target_date TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id TEXT PRIMARY KEY,
        display_name TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS budget (
        id INTEGER PRIMARY KEY,
        income REAL,
        expenses_total REAL,
        recommended_savings REAL,
        updated_at TEXT
    )
    ''')

    conn.commit()
    conn.close()


def get_conn(db_path: str) -> sqlite3.Connection:
    return sqlite3.connect(db_path)


__all__ = ["init_db", "get_conn"]