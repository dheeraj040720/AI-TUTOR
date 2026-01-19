from backend.supabase_client import supabase

def test_connection():
    print("Testing Supabase Connection...")
    email = "dheerajdg9ds@gmail.com"
    
    try:
        # Try to fetch the specific user
        print(f"Querying for {email}...")
        response = supabase.table("students").select("*").eq("email", email).execute()
        
        print(f"Status: {len(response.data)} rows found")
        print(f"Data: {response.data}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_connection()
