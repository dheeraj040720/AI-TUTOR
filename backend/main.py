import os
import requests
import google.generativeai as genai
from pydantic import BaseModel
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from dotenv import load_dotenv
from .supabase_client import supabase

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add compression middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Add security headers middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response

@app.get("/student-progress")
def get_progress():
    response = supabase.table("progress").select("*").execute()
    return response.data

@app.post("/submit-answer")
def submit_answer(payload: dict):
    try:
        # Insert the answer submission into the database
        response = supabase.table("submissions").insert(payload).execute()

        # Update progress
        student_id = payload["student_id"]
        topic = payload["topic"]
        is_correct = payload.get("is_correct", False)

        # Check if progress exists
        existing = supabase.table("progress").select("*").eq("student_id", student_id).eq("topic", topic).execute()
        if existing.data:
            # Update existing
            current = existing.data[0]
            new_attempts = current["attempts"] + 1
            new_correct = current["correct"] + (1 if is_correct else 0)
            supabase.table("progress").update({
                "attempts": new_attempts,
                "correct": new_correct
            }).eq("student_id", student_id).eq("topic", topic).execute()
        else:
            # Insert new
            supabase.table("progress").insert({
                "student_id": student_id,
                "topic": topic,
                "attempts": 1,
                "correct": 1 if is_correct else 0
            }).execute()

        return {"status": "success", "message": "Answer submitted successfully", "data": response.data}
    except Exception as e:
        return {"status": "error", "message": str(e)}



class ChatRequest(BaseModel):
    message: str

class RecommendationRequest(BaseModel):
    progress: list

class QuizRequest(BaseModel):
    subject: str

@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return {"status": "error", "message": "API Key not set."}

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.0-flash")
        
        response = model.generate_content(request.message)
        return {"status": "success", "response": response.text}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Simple in-memory cache to minimize API calls
recommendation_cache = {}

@app.post("/get-recommendation")
def get_recommendation(request: RecommendationRequest):
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return {"status": "error", "message": "Gemini API Key not set."}

        # Create a cache key based on the progress data
        # We sort by topic to ensure consistent keys for the same data
        progress_sorted = sorted(request.progress, key=lambda x: x.get('topic', ''))
        cache_key = str(progress_sorted)

        if cache_key in recommendation_cache:
            print("Returning cached recommendation...")
            return {"status": "success", "recommendation": recommendation_cache[cache_key]}

        # Construct prompt for Gemini
        marks_summary = "\n".join([f"- {item.get('topic', 'Unknown')}: {item.get('accuracy', 0)}%" for item in request.progress])
        
        prompt = f"You are an expert AI Study Tutor. Analyze these student result and provide a 2-3 sentence personalized recommendation. Focus on weak areas (below 60%) and be encouraging.\n\nMarks:\n{marks_summary}\n\nRecommendation:"
        
        print(f"Calling Gemini (gemini-1.5-flash) for recommendation...")
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        try:
            print(f"Calling Gemini (gemini-2.0-flash) for recommendation...")
            model = genai.GenerativeModel("gemini-2.0-flash")
            response = model.generate_content(prompt)
            recommendation = response.text.strip()
        except Exception as api_err:
            error_msg = f"Gemini API Error: {str(api_err)}"
            print(error_msg)
            
            # Retry with gemini-flash-latest which was in the list
            try:
                print("Attempting with gemini-flash-latest fallback...")
                model_2 = genai.GenerativeModel("gemini-flash-latest")
                response = model_2.generate_content(prompt)
                recommendation = response.text.strip()
            except Exception as e2:
                print(f"Final fallback to simple logic: {str(e2)}")
                raise e2 # Let the outer catch handle it

        # Save to cache
        recommendation_cache[cache_key] = recommendation

        return {"status": "success", "recommendation": recommendation}
    except Exception as e:
        print(f"Gemini Error: {str(e)}")
        # Fallback to simple logic if API fails
        weak_topics = [item['topic'] for item in request.progress if item.get('accuracy', 0) < 60]
        if weak_topics:
            fallback = f"Focus on improving your scores in {', '.join(weak_topics)}."
        else:
            fallback = "Great job! Keep maintaining your high scores across all topics."
        return {"status": "success", "recommendation": fallback}

@app.post("/generate-quiz")
async def generate_quiz(request: QuizRequest):
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return {"status": "error", "message": "API Key not set."}

        genai.configure(api_key=api_key)
        
        prompt = f"""
        Generate a 5-question multiple choice quiz about '{request.subject}'.
        Return the result ONLY as a JSON object with this exact structure:
        {{
            "subject": "{request.subject}",
            "questions": [
                {{
                    "id": 1,
                    "question": "The question text?",
                    "options": ["Option A", "Option B", "Option C", "Option D"],
                    "answer": "Option A"
                }}
            ]
        }}
        Ensure the 'answer' is exactly one of the strings in the 'options' array.
        Only return the JSON, no other text or explanation.
        """

        model = genai.GenerativeModel("gemini-1.5-flash")
        
        print(f"Generating quiz for subject: {request.subject}")
        response = model.generate_content(prompt)
        text = response.text
        
        # Robust JSON extraction
        import json
        import re
        
        try:
            # Try to find JSON block
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                content = json_match.group(0)
            else:
                content = text.strip()
                
            quiz_data = json.loads(content)
        except Exception as parse_err:
            print(f"JSON Parsing Error: {parse_err}")
            raise parse_err
        
        print(f"Quiz generated successfully for {request.subject}")
        return {"status": "success", "quiz": quiz_data}
    except Exception as e:
        print(f"Quiz Generation Error: {str(e)}")
        # Expanded fallback quiz with 5 questions
        fallback_quiz = {
            "subject": request.subject,
            "questions": [
                {
                    "id": 1,
                    "question": f"What is one of the most important concepts in {request.subject}?",
                    "options": ["Fundamentals", "Advanced Theory", "History", "Practice"],
                    "answer": "Fundamentals"
                },
                {
                    "id": 2,
                    "question": f"How do experts typically approach {request.subject}?",
                    "options": ["Carefully", "Randomly", "Slowly", "Ignorantly"],
                    "answer": "Carefully"
                },
                {
                    "id": 3,
                    "question": f"Which of these is most likely related to {request.subject}?",
                    "options": ["Learning", "Sleeping", "Eating", "Walking"],
                    "answer": "Learning"
                },
                {
                    "id": 4,
                    "question": f"Mastering {request.subject} requires which of the following?",
                    "options": ["Consistency", "Luck", "Speed", "Silence"],
                    "answer": "Consistency"
                },
                {
                    "id": 5,
                    "question": f"Why is {request.subject} important to study?",
                    "options": ["Builds Knowledge", "Passes Time", "Looks Good", "No Reason"],
                    "answer": "Builds Knowledge"
                }
            ]
        }
        return {"status": "success", "quiz": fallback_quiz}