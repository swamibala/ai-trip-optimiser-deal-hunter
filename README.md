# AI Trip Optimizer & Deal Hunter

**NOTE:** This is a capstone project submission for the Google AI Agent Intensive course. This multi-agent system demonstrates the use of Google Agent Development Kit (ADK) for building a travel planning assistant with baseline price tracking capabilities.

---

## Problem Statement

Travel planning is complex and time-consuming because it requires extensive research across multiple platforms to find the best flight and hotel combinations. Travelers must manually compare dozens of options, check prices across different dates, and evaluate trade-offs between cost, convenience, and quality. The process becomes even more frustrating when prices fluctuate constantly—a flight that costs $400 today might be $500 tomorrow or $350 next week. Manual price tracking is impractical, forcing travelers to either book immediately (risking overpayment) or delay booking (risking price increases). This creates decision paralysis and often results in suboptimal choices.

Additionally, once a trip is planned, travelers have no systematic way to monitor whether better deals become available. They must manually re-search periodically, which is tedious and often forgotten. This means missing out on potential savings when prices drop after initial planning.

---

## Solution Statement

AI agents can automate the entire travel research process by simultaneously searching multiple sources for flights and hotels, comparing options based on user preferences, and generating comprehensive itineraries with optimal recommendations. By capturing baseline prices during initial planning, the system creates a foundation for future price monitoring workflows that can automatically detect when better deals become available and alert users to potential savings.

The multi-agent architecture allows for parallel execution of searches (improving speed), specialized agents for different tasks (improving quality), and a modular design that can be extended with additional capabilities like activity recommendations, calendar integration, or loyalty program optimization.

---

## Architecture

Core to the AI Trip Optimizer is the `trip_optimizer_deal_hunter_agent`—a sequential multi-agent system built with Google's Agent Development Kit. The system follows a three-stage pipeline: preference collection, parallel search, and itinerary generation with baseline price capture.

### The Root Agent: `trip_optimizer_deal_hunter_agent`

The root agent is constructed using the `SequentialAgent` class from Google ADK. It orchestrates three sub-agents in a specific order, ensuring that each stage completes before the next begins. This sequential flow ensures data dependencies are properly managed—preferences must be collected before searching, and search results must be available before building the itinerary.

### Specialized Sub-Agents

The real power of the system lies in its team of specialized agents, each an expert in its domain:

#### Preference Collector: `preference_collector_agent`

This agent is responsible for extracting travel details from user input. It uses a Pydantic `UserPreferences` model to ensure type-safe data collection, validating that all required fields (source, destination, travel dates) are present. The agent stores preferences in shared state for downstream agents to access.

**Model:** `gemini-2.5-flash-lite` (fast, efficient for structured data extraction)

#### Recommendation System: `recommendation_system`

This is a `ParallelAgent` that coordinates two search agents to run concurrently, significantly reducing total execution time. It demonstrates ADK's ability to execute independent tasks in parallel while maintaining proper state management.

**Sub-agents:**
- **Flight Search Agent** (`flight_search_agent`): Queries SerpAPI's Google Flights engine, converts city names to IATA codes, and returns top 3 flight options ranked by price and convenience.
- **Hotel Search Agent** (`hotel_search_agent`): Queries SerpAPI's Google Hotels engine and returns top 3 hotel options ranked by rating and price.

**Model:** `gemini-2.5-flash-lite` (both search agents)

#### Itinerary Builder: `itinerary_builder_agent`

Once search results are available, this agent analyzes all options using Gemini's reasoning capabilities to select the best flight and hotel combination. It generates a comprehensive, formatted itinerary that includes:
- Recommended flight with full details
- Recommended hotel with amenities and pricing
- Total trip cost estimate
- **Baseline Price Tracking section** with structured price data

This baseline price data is formatted for easy database persistence and future price monitoring workflows.

**Model:** `gemini-2.0-flash` (more powerful model for complex reasoning and generation)

---

## Essential Tools and Utilities

The agents are equipped with custom tools to perform their tasks effectively:

### Flight Search (`search_flight`)

Integrates with SerpAPI's Google Flights engine to fetch real-time flight data. The tool:
- Accepts origin/destination IATA codes, dates, and currency
- Returns structured flight data including price, duration, airline, and amenities
- Implements `_top_n_flights_from_results` helper to rank and filter results
- Handles API errors gracefully

### Hotel Search (`search_hotels`)

Integrates with SerpAPI's Google Hotels engine to fetch real-time hotel data. The tool:
- Accepts location query, check-in/out dates, and currency
- Returns structured hotel data including price, rating, amenities, and location
- Implements `_top_n_hotels_from_results` helper to rank by rating and price
- Handles API errors gracefully

### Data Processing Utilities

Both tools include helper functions that:
- Extract relevant fields from SerpAPI responses
- Rank results using multi-criteria sorting (price, rating, duration)
- Limit results to top N options to reduce token usage
- Structure data for optimal LLM consumption

---

## Workflow

The `trip_optimizer_deal_hunter_agent` follows this workflow:

1. **Collect Preferences**: User provides travel details in natural language (e.g., "Plan a trip to Paris from New York, March 10-15, 2026"). The `preference_collector_agent` extracts structured data.

2. **Parallel Search**: The `recommendation_system` triggers both `flight_search_agent` and `hotel_search_agent` simultaneously, fetching real-time options from SerpAPI.

3. **Build Itinerary**: The `itinerary_builder_agent` receives all search results, analyzes options using Gemini's reasoning, and generates a comprehensive itinerary.

4. **Capture Baseline Prices**: The itinerary includes a structured "Baseline Price Tracking" section with:
   - Best flight price and details
   - Best hotel price per night and total cost
   - Departure/arrival times and dates
   
5. **Output**: User receives a formatted markdown itinerary with recommendations and baseline prices ready for database persistence.

---

## Value Statement

This system demonstrates the power of multi-agent orchestration for real-world applications. By breaking down travel planning into specialized tasks and executing searches in parallel, it reduces planning time from hours to seconds while capturing structured data that enables future automation.

**Key Benefits:**
- **Time Savings**: Automated search across multiple sources
- **Better Decisions**: AI-powered analysis of trade-offs
- **Future-Ready**: Baseline prices enable price monitoring workflows
- **Scalable**: Modular architecture allows easy extension

**Future Enhancements:**
If I had more time, I would add:
- **Price Monitoring Workflow**: Separate agent system to re-search periodically and compare with baseline prices
- **Database Persistence**: Store baseline prices in PostgreSQL for long-term tracking
- **Notification System**: Alert users via email/SMS when prices drop
- **Activity Recommendations**: Integrate additional search agents for tours and activities
- **Calendar Integration**: Export itineraries to Google Calendar

---

## Installation

This project was built against **Python 3.12**.

It is suggested you create a virtual environment using your preferred tooling (e.g., `uv`).

### Setup

```bash
# Create virtual environment
uv venv --python 3.12
source .venv/bin/activate

# Install dependencies
uv sync
```

### Configure API Keys

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_gemini_api_key_here
SERPAPI_API_KEY=your_serpapi_key_here
```

Get your API keys:
- [Gemini API Key](https://aistudio.google.com/app/api-keys)
- [SerpAPI Key](https://serpapi.com)

---

## Running the Agent

### ADK Web Mode

From the command line in the working directory:

```bash
adk web
```

Then navigate to `http://localhost:8000` and try:

```
Plan a trip to Paris from New York, March 10-15, 2026
```

---

## Project Structure

```
ai-trip-optimiser-deal-hunter/
├── root_agent/              # Main Python package
│   ├── agent.py            # Defines the main agent and orchestrates sub-agents
│   ├── tools.py            # Custom tools for SerpAPI integration
│   ├── __init__.py         # Package exports
│   └── sub_agents/         # Individual sub-agents
│       ├── preference_collector_agent.py  # Collects travel preferences
│       ├── flight_search_agent.py         # Searches for flights
│       ├── hotel_search_agent.py          # Searches for hotels
│       ├── recommendation_system.py       # Parallel search coordinator
│       └── itinerary_builder_agent.py     # Generates itinerary with baseline prices
├── pyproject.toml          # Project dependencies
├── .env                    # API keys (not in repo)
└── README.md              # This file
```

---

## ADK Concepts Demonstrated

This project showcases several key Google ADK capabilities:

1. **Multi-Agent System**: 5 coordinated agents working together
2. **Sequential Workflow**: `SequentialAgent` for ordered execution
3. **Parallel Execution**: `ParallelAgent` for concurrent searches
4. **Tool Integration**: Custom tools for external API calls
5. **State Management**: Shared state across agents via output keys
6. **Structured Outputs**: Pydantic schemas for type-safe data
7. **Model Selection**: Strategic use of different Gemini models (2.5 Flash Lite for speed, 2.0 Flash for reasoning)
8. **Error Handling**: Graceful handling of API failures

---

## Conclusion

The AI Trip Optimizer demonstrates how multi-agent systems, built with Google's Agent Development Kit, can tackle complex real-world problems. By breaking down travel planning into specialized tasks and executing them efficiently, it creates a workflow that is both fast and intelligent.

The baseline price capture feature lays the foundation for a "living itinerary" concept—where travel plans adapt over time as prices change. This modular architecture makes it easy to extend the system with additional capabilities, making it a robust foundation for future enhancements.

**Submission Track:** Track A — Concierge Agents

**Course:** Google AI Agent Intensive

**Author:** Swaminathan Balakrishnan