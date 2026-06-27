"""
inspect_db.py
Utility script to query and inspect MongoDB database collections.
Prints registered users and logged activities.
"""
from dotenv import load_dotenv
import os
import sys

# Ensure root folder is on path
sys.path.insert(0, os.path.dirname(__file__))

from database.connection import db_connection, get_db
from database.crud import find_many

def inspect():
    load_dotenv()
    
    # 1. Connect to DB
    print("🔌 Connecting to Database...")
    db_connection.connect()
    db = get_db()
    
    print("\n==============================================")
    print("📊 DATABASE SUMMARY")
    print("==============================================")
    
    # 2. Get list of collections
    collections = db.list_collection_names()
    print(f"Collections present: {collections}")
    
    # 3. Print Users
    print("\n👥 REGISTERED USERS:")
    users = find_many("users", {})
    if not users:
        print("  No users found.")
    for u in users:
        print(f"  - ID: {u.get('id')} | Name: {u.get('name')} | Email: {u.get('email')} | Role: {u.get('role')} | Active: {u.get('is_active')}")
        
    # 4. Print Profiles
    print("\n👤 PROFILES:")
    profiles = find_many("profiles", {})
    if not profiles:
        print("  No profiles found.")
    for p in profiles:
        print(f"  - User ID: {p.get('user_id')} | Title: {p.get('title')} | Preferred Career: {p.get('preferred_career')} | Skills: {p.get('skills', [])[:5]}...")

    # 5. Print Resumes
    print("\n📄 UPLOADED RESUMES:")
    resumes = find_many("resumes", {})
    if not resumes:
        print("  No resumes found.")
    for r in resumes:
        print(f"  - ID: {r.get('id')} | User ID: {r.get('user_id')} | File: {r.get('original_name')} | Status: {r.get('status')}")

    # 6. Print Recent Activity Logs
    print("\n🛡️ RECENT ACTIVITY LOGS (Last 10):")
    logs = find_many("activity_logs", {}, sort=[("created_at", -1)], limit=10)
    if not logs:
        print("  No activity logs found.")
    for l in logs:
        print(f"  - [{l.get('created_at')}] User ID: {l.get('user_id')} | Action: {l.get('action')} | Type: {l.get('resource_type')} | IP: {l.get('ip_address')}")
        
    print("==============================================\n")

if __name__ == "__main__":
    inspect()
