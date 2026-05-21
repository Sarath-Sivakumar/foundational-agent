from fastapi import FastAPI
from pydantic import BaseModel

from dotenv import load_dotenv
import os
import ollama

from tools import (
    get_weather,
    get_current_time,
    calculate
)

# -----------------------------------------
# LOAD ENV
# -----------------------------------------

load_dotenv()

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")

# -----------------------------------------
# FASTAPI
# -----------------------------------------

app = FastAPI()

# -----------------------------------------
# REQUEST MODEL
# -----------------------------------------

class UserRequest(BaseModel):
    message: str

# -----------------------------------------
# TOOL ROUTER
# -----------------------------------------

def decide_tool(user_message: str):

    prompt = f"""
You are an AI routing system.

Available tools:

1. weather
- Use for weather-related questions

2. time
- Use for current time questions

3. calculator
- Use for mathematical calculations

4. none
- Use if no tool is needed

Return ONLY the tool name.

User message:
{user_message}
"""

    response = ollama.chat(
        model=OLLAMA_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    tool_name = response["message"]["content"].strip().lower()

    return tool_name

# -----------------------------------------
# MAIN AGENT ENDPOINT
# -----------------------------------------

@app.post("/chat")
def chat(request: UserRequest):

    user_message = request.message

    # -------------------------------
    # STEP 1 — Decide Tool
    # -------------------------------

    tool = decide_tool(user_message)

    # -------------------------------
    # STEP 2 — Execute Tool
    # -------------------------------

    if tool == "weather":

        city = "Chennai"

        tool_result = get_weather(city)

    elif tool == "time":

        tool_result = get_current_time()

    elif tool == "calculator":

        expression = user_message.replace("calculate", "").strip()

        tool_result = calculate(expression)

    else:

        tool_result = "No suitable tool found."

    # -------------------------------
    # FINAL RESPONSE
    # -------------------------------

    return {
        "user_message": user_message,
        "selected_tool": tool,
        "tool_result": tool_result
    }