"""
SQLite database setup for PackWise AI.

Keeps the schema intentionally simple and explainable:
- foods: catalog of food commodities with typical sensitivity defaults
- materials: catalog of packaging materials with barrier/cost/sustainability properties
- material_properties: free-text application notes & advantages/limitations for each material
- recommendations: a log of past recommendation runs (input + output), used for report generation
"""
import sqlite3
import os
import json

DB_PATH = os.path.join(os.path.dirname(__file__), "packwise.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(reset: bool = False):
    """Create tables and seed prototype data. If reset=True, wipes existing data first."""
    if reset and os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = get_connection()
    cur = conn.cursor()

    cur.executescript(
        """
        CREATE TABLE IF NOT EXISTS foods (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            default_moisture_sensitivity INTEGER NOT NULL,
            default_oxygen_sensitivity INTEGER NOT NULL,
            default_light_sensitivity INTEGER NOT NULL,
            default_fat_content INTEGER NOT NULL,
            notes TEXT
        );

        CREATE TABLE IF NOT EXISTS materials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            short_code TEXT NOT NULL,
            material_form TEXT NOT NULL DEFAULT 'flexible_film', -- 'flexible_film' or 'rigid_container'
            oxygen_barrier INTEGER NOT NULL,      -- 1 (poor) - 5 (excellent)
            moisture_barrier INTEGER NOT NULL,    -- 1 - 5
            light_barrier INTEGER NOT NULL,       -- 1 - 5
            grease_resistance INTEGER NOT NULL,   -- 1 - 5
            mechanical_strength INTEGER NOT NULL, -- 1 - 5
            heat_resistance INTEGER NOT NULL,     -- 1 - 5
            cost_level INTEGER NOT NULL,          -- 1 (cheap) - 5 (expensive)
            sustainability_level INTEGER NOT NULL,-- 1 (low) - 5 (high)
            recyclable INTEGER NOT NULL DEFAULT 0,
            compostable INTEGER NOT NULL DEFAULT 0,
            data_status TEXT NOT NULL DEFAULT 'prototype' -- 'prototype' or 'validated'
        );

        CREATE TABLE IF NOT EXISTS material_properties (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            material_id INTEGER NOT NULL REFERENCES materials(id),
            example_applications TEXT NOT NULL,  -- comma separated examples
            advantages TEXT NOT NULL,            -- JSON list
            limitations TEXT NOT NULL            -- JSON list
        );

        CREATE TABLE IF NOT EXISTS recommendations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            food_id INTEGER REFERENCES foods(id),
            input_params TEXT NOT NULL,   -- JSON of the request payload
            result_json TEXT NOT NULL,    -- JSON of the 3 ranked results
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        );
        """
    )
    conn.commit()

    cur.execute("SELECT COUNT(*) FROM foods")
    if cur.fetchone()[0] == 0:
        _seed(conn)

    conn.close()


def _seed(conn):
    from .seed_data import FOODS, MATERIALS

    cur = conn.cursor()

    for f in FOODS:
        cur.execute(
            """INSERT INTO foods
               (name, category, default_moisture_sensitivity, default_oxygen_sensitivity,
                default_light_sensitivity, default_fat_content, notes)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                f["name"], f["category"], f["moisture"], f["oxygen"],
                f["light"], f["fat"], f.get("notes", ""),
            ),
        )

    for m in MATERIALS:
        cur.execute(
            """INSERT INTO materials
               (name, short_code, material_form, oxygen_barrier, moisture_barrier, light_barrier,
                grease_resistance, mechanical_strength, heat_resistance, cost_level,
                sustainability_level, recyclable, compostable, data_status)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                m["name"], m["short_code"], m["material_form"], m["oxygen_barrier"], m["moisture_barrier"],
                m["light_barrier"], m["grease_resistance"], m["mechanical_strength"],
                m["heat_resistance"], m["cost_level"], m["sustainability_level"],
                int(m["recyclable"]), int(m["compostable"]), m.get("data_status", "prototype"),
            ),
        )
        material_id = cur.lastrowid
        cur.execute(
            """INSERT INTO material_properties
               (material_id, example_applications, advantages, limitations)
               VALUES (?, ?, ?, ?)""",
            (
                material_id, m["example_applications"],
                json.dumps(m["advantages"]), json.dumps(m["limitations"]),
            ),
        )

    conn.commit()
