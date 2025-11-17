from google.adk.agents import Agent
from pydantic import BaseModel, Field

class UserPreferences(BaseModel):
    source: str = Field(description="The travel source location")
    destination: str = Field(description="The travel destination location")
    travel_start_date: str = Field(description="The start date of travel in YYYY-MM-DD format")
    travel_end_date: str = Field(description="The end date of travel in YYYY-MM-DD format")


preference_collector_agent = Agent(
    name="PreferenceCollectorAgent",
    model="gemini-2.5-flash-lite",
    instruction="""You are a Preference Collector Agent. Receive user input about their travel preferences.
    Store user preferences in a structured format for further processing.
    Collect information such as origin, destination, travel start date  and travel end date.
    If any of these information is missing, ask the user for it explicitly.""",
    output_key="user_preferences",
    output_schema=UserPreferences,
)

print("✅ preference_collector_agent created.")
