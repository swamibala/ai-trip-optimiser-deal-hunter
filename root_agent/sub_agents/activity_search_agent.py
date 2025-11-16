from google.adk.agents import Agent
from google.adk.tools import google_search

activity_search_agent = Agent(
    name="ActivitySearchAgent",
    model="gemini-2.5-flash-lite",
    instruction="""You are an Activity Search Agent. Read user input about their travel preferences from {user_preferences}.
    Based on the input, search for suitable activities and experiences that match their interests.
    Provide a list of recommended activities with brief descriptions.""",
    tools=[google_search],
    output_key="activity_options",
)

print("✅ activity_search_agent created.")
