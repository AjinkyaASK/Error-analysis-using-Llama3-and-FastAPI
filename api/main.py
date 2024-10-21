import json
import ollama
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class ErrorLogRequest(BaseModel):
    error_log: str
    
LLM = "llama3"
TEMPERATURE = 0.2
PROMPT_MESSAGE = """
                
    Analyse above error log, and tell me 3 things:
    1. What is wrong?
    2. What is the impact on my business?
    3. What are possible steps to fix this?
    
    I want your response as a pure JSON, in following format:
    
    {"cause":["",""],"impact":["",""],"fix":["",""]}
    
    Make sure apart from above JSON, no other text is present in your response.
    """
    
def create_prompt(error_log: str) -> str:
    return f"""
        {error_log}
        
        {PROMPT_MESSAGE}
    """

@app.post("/analyse_error")
async def analyse_error(request: ErrorLogRequest):
    try:
        prompt = create_prompt(request.error_log)
        
        response = ollama.chat(
            model=LLM,
            options={"temperature": TEMPERATURE},
            messages=[{"role": "user", "content": prompt}],
        )
        
        response_text = response.get("message", {}).get("content", "")
        cleaned_response_text = response_text.strip().replace('\\n', ' ').replace('\\"', '"')
    
        try:
            response_json = json.loads(cleaned_response_text)
            if not all(key in response_json for key in ["cause", "impact", "fix"]):
                raise ValueError("Invalid response format")
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Failed to parse response: {cleaned_response_text}")
            raise HTTPException(status_code=500, detail=f"Invalid response format: {str(e)}")
        
        return {"analysis": response_json}
    
    except Exception as e:
        print(f"Error in analysis: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to analyze error log")