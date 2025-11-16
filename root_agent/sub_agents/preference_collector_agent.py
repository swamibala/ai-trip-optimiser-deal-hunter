from google.adk.agents import Agent
from pydantic import BaseModel, Field

class UserPreferences(BaseModel):
    source: str = Field(description="The travel source location")
    destination: str = Field(description="The travel destination location")
    travel_dates: str = Field(description="The travel dates")
    budget: float = Field(description="The budget for the trip")
    interests: list = Field(description="List of user interests for the trip")

preference_collector_agent = Agent(
    name="PreferenceCollectorAgent",
    model="gemini-2.5-flash-lite",
    instruction="""You are a Preference Collector Agent. Receive user input about their travel preferences.
    Store user preferences in a structured format for further processing.
    Collect information such as origin, destination, travel dates, budget, and interests.
    Ensure all fields except interests are provided by user.
    If any information is missing, ask the user for it.""",
)

print("✅ preference_collector_agent created.")
