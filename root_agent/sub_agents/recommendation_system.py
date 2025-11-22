from google.adk.agents import ParallelAgent
from .flight_search_agent import flight_search_agent
from .hotel_search_agent import hotel_search_agent

recommendation_system = ParallelAgent(
    name="RecommendationSystem",
    sub_agents=[flight_search_agent, hotel_search_agent]
    )

print("✅ recommendation_system created.")
