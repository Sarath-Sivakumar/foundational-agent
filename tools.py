from datetime import datetime


# -----------------------------------------
# WEATHER TOOL
# -----------------------------------------

def get_weather(city: str):

    # Mock weather data for now
    return f"The weather in {city} is sunny with 32°C."


# -----------------------------------------
# TIME TOOL
# -----------------------------------------

def get_current_time():

    now = datetime.now()

    return now.strftime("%I:%M %p")


# -----------------------------------------
# CALCULATOR TOOL
# -----------------------------------------

def calculate(expression: str):

    try:
        result = eval(expression)
        return f"The result is {result}"

    except Exception:
        return "Invalid mathematical expression."