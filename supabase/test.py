import os
from supabase import create_client
import uuid
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_ANON_KEY")

if not url or not key:
    raise ValueError("Missing Supabase credentials in environment variables. Please check your .env file.")

supabase = create_client(url, key)


# Test select
try:
    result = supabase.table("students").select("*").execute()
    print("Select successful:", len(result.data), "rows")
except Exception as e:
    print("Select failed:", e)

# Test insert
data = {
    "id": str(uuid.uuid4()),
    "email": "test@student.com",
    "name": "Dheeraj Student",
    "level": "beginner"
}

try:
    result = supabase.table("students").insert(data).execute()
    print("Inserted:", result.data)
except Exception as e:
    print("Insert failed:", e)


supabase.table("progress").upsert({
    "student_id": str(uuid.uuid4()),
    "topic": "math",
    "attempts": 5,
    "correct": 3
}).execute()