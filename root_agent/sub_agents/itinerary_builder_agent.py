from google.adk.agents import Agent

itinerary_builder_agent = Agent(
    name="ItineraryBuilderAgent",
    model="gemini-2.5-flash-lite",
    instruction="""You are an Itinerary Builder Agent. Collect all the available flight options from {flight_options}.
    Collect all the available hotel options from {hotel_options}.
    Collect all the available activity options from {activity_options}.
    Create a travel itinerary based on the available flight, hotel, and activity options.
    You will use the flight search tools to find suitable flight options based on user preferences.""",
)

print("✅ flight_search_agent created.")
