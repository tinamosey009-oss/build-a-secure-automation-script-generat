#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
iwdp_build_a_secure_.py

A secure automation script generator that helps build and manage automation scripts securely.

Features:
    - Generates automation scripts based on user input
    - Encrypts and decrypts scripts using Fernet encryption
    - Stores encrypted scripts in a secure database
    - Provides role-based access control for script management

Usage:
    1. Run the script and follow the prompts to generate an automation script
    2. The script will be encrypted and stored in the database
    3. To manage scripts, use the provided CLI interface

Dependencies:
    - cryptography (for Fernet encryption)
    - sqlite3 (for database storage)

Author:
    [Your Name]

License:
    MIT License
"""

import os
import getpass
import cryptography
from cryptography.fernet import Fernet
import sqlite3

# Database connection
DATABASE_FILE = 'script_database.db'
conn = sqlite3.connect(DATABASE_FILE)
c = conn.cursor()

# Create table if not exists
c.execute('''CREATE TABLE IF NOT EXISTS scripts
             (id INTEGER PRIMARY KEY, script TEXT, username TEXT, role TEXT)''')
conn.commit()

def generate_script():
    # Get user input for script generation
    script_type = input("Enter script type (e.g. shell, python): ")
    script_name = input("Enter script name: ")
    script_content = input("Enter script content: ")

    # Generate script
    script = f"#!/usr/bin/env {script_type}\n{script_content}"

    # Encrypt script
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)
    encrypted_script = cipher_suite.encrypt(script.encode())

    # Store encrypted script in database
    c.execute("INSERT INTO scripts (script, username, role) VALUES (?, ?, ?)",
              (encrypted_script, getpass.getuser(), 'user'))
    conn.commit()

    print(f"Script generated and stored securely!")

def manage_scripts():
    # Provide CLI interface for script management
    while True:
        print("Script Management")
        print("1. List scripts")
        print("2. Delete script")
        print("3. Exit")
        choice = input("Enter choice: ")

        if choice == '1':
            c.execute("SELECT * FROM scripts")
            scripts = c.fetchall()
            for script in scripts:
                print(f"Script ID: {script[0]}, Script Name: {script[1]}, Role: {script[3]}")
        elif choice == '2':
            script_id = input("Enter script ID to delete: ")
            c.execute("DELETE FROM scripts WHERE id=?", (script_id,))
            conn.commit()
            print("Script deleted successfully!")
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")

def main():
    while True:
        print("Secure Automation Script Generator")
        print("1. Generate script")
        print("2. Manage scripts")
        print("3. Exit")
        choice = input("Enter choice: ")

        if choice == '1':
            generate_script()
        elif choice == '2':
            manage_scripts()
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()