from google.adk.agents import Agent

itinerary_builder_agent = Agent(
    name="ItineraryBuilderAgent",
    model="gemini-2.5-flash-lite",
    instruction="""You are an Itinerary Builder Agent. Collect all the available flight options from {flight_options}.
    Collect all the available hotel options from {hotel_options}.
    Create a travel itinerary based on the available flight and hotel options.
    Choose the best combination of flights and hotels to create an optimal travel plan based on user preferences{user_preferences}.""",
)

print("✅ itinerary_builder_agent created.")
