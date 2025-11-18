from google.adk.agents import Agent
from root_agent.tools import search_hotels


hotel_search_agent = Agent(
    name="HotelSearchAgent",
    model="gemini-2.5-flash-lite",
    instruction="""You are a Hotel Search Agent. User has already provided travel preferences in {user_preferences}.
    Do not ask more followup questions to the user. Just use the hotel search tool to find suitable hotel options.
    Store hotel search results in a structured format for further processing""",
    tools=[search_hotels],
    output_key="hotel_options",
)

print("✅ hotel_search_agent created.")
