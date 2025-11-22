from google.adk.agents import Agent

itinerary_builder_agent = Agent(
    name="itinerary_builder_agent",
    model="gemini-2.0-flash",
    description="Combines all search results into a complete travel itinerary",
    instruction=(
        "You are a travel planner. Create a complete, well-organized itinerary "
        "by combining the search results below.\n"
        "\n"
        "**Available Flights:**\n"
        "{flight_options}\n"  # Reads from state!
        "\n"
        "**Available Hotels:**\n"
        "{hotel_options}\n"  # Reads from state!
        "\n"
        "Create a formatted itinerary that:\n"
        "1. Recommends the BEST option from each category (flights, hotel)\n"
        "2. Includes estimated total cost\n"
        "3. Stores the baseline prices for future price monitoring\n"
        "\n"
        "IMPORTANT: Also extract and store the baseline prices in a structured format:\n"
        "- Best flight price and details\n"
        "- Best hotel price per night and details\n"
        "\n"
        "Format beautifully with clear sections and markdown."
    ),
    output_key="final_itinerary"
)


print("✅ itinerary_builder_agent created.")
