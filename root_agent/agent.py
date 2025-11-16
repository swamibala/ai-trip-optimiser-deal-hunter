from google.adk.agents import SequentialAgent

from .sub_agents import (
    preference_collector_agent
)

trip_optimizer_deal_hunter_agent = SequentialAgent(
    name="TripOptimizerDealHunterAgent",
    sub_agents=[preference_collector_agent])

print("✅ root_agent created.")

root_agent = trip_optimizer_deal_hunter_agent