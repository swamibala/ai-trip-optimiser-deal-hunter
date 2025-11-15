# AI Living Trip Optimizer & Deal Hunter

### A self-updating, price-aware concierge agent that continuously optimizes your flights, hotels, and itinerary.

---

## 1. Overview

Travel planning is complex and dynamic. Prices for flights and hotels fluctuate constantly, making static itineraries outdated as soon as they are created.

**AI Living Trip Optimizer & Deal Hunter** solves this problem by introducing a **living itinerary**: a travel plan that continuously adapts as prices change, optimizing recommendations for flights, hotels, and activities while notifying the user when better deals are available.

This project leverages **Google ADK** for multi-agent orchestration, session memory, loop agents, and tool integrations, while using **Google Gemini models** for LLM reasoning, itinerary generation, and ranking.

---

## 2. Problem Statement

* Travelers spend hours manually checking flight, hotel, and activity options.
* Static itineraries do not adjust when prices drop.
* Existing tools often fail to integrate real-time search, reasoning, and personalization.

A **dynamic, personal travel assistant** is needed that:

* Builds a complete itinerary
* Monitors price fluctuations
* Updates recommendations continuously
* Provides notifications for cost-saving opportunities

---

## 3. Solution Summary

The system consists of multiple agents working together:

* **Preference Collector Agent:** gathers traveler information (origin, destination, dates, budget, style).
* **Flight Search Agent:** fetches real-time flight options using Google Flight Search / SERP.
* **Hotel Search Agent:** fetches hotel prices and ratings via SERP API.
* **Activity Search Agent:** discovers top local activities using Google Search.
* **Ranking & Optimization Agent:** uses Gemini to reason and rank options based on traveler priorities.
* **Itinerary Builder Agent:** Gemini generates a multi-day itinerary with morning, afternoon, evening activities.
* **Price Monitor Loop Agent:** periodically checks for price drops and triggers notifications.
* **Notification Agent:** alerts the user when better options are available.

The itinerary is **living**, meaning it persists in memory, updates with new information, and adapts automatically when prices change.

---

## 4. Unique Capabilities

* **Living Itinerary:** continuously updated and adaptive; not static.
* **Loop Agent with Long-Running Operations:** monitors flight and hotel prices over time.
* **Memory-Driven Personalization:** stores preferences and baseline prices for dynamic reasoning.
* **Gemini-Powered Reasoning:** generates and ranks itineraries, summarizes activities, and justifies recommendations.
* **Multi-Agent Architecture:** parallel search agents + sequential reasoning + loop notifications.
* **Observability:** logs price changes, agent calls, and decisions for evaluation.

---

## 5. System Architecture

**Agents & Flow:**

1. **Preference Collector Agent** → collects travel preferences and stores in memory.
2. **Flight / Hotel / Activity Agents** → run in parallel, fetch live data.
3. **Ranking & Optimization Agent** → Gemini generates ranking of best options.
4. **Itinerary Builder Agent** → Gemini generates structured itinerary.
5. **Price Monitor Loop Agent** → periodically re-runs search and compares prices.
6. **Notification Agent** → informs the user about deals and updates itinerary if necessary.

*Memory and session services maintain state between iterations.*

---

## 6. ADK Concepts Demonstrated

* **Multi-Agent System:** coordinated pipeline of 7+ agents
* **Parallel Agents:** flights, hotels, activities
* **Sequential Agents:** search → rank → build → monitor → notify
* **Loop Agent / Long-Running Operations:** Price Monitor checks periodically
* **Tools:** Google Search, SERP API
* **Memory & Session:** stores preferences and baseline prices
* **Context Engineering:** compacts search results for Gemini reasoning
* **Observability:** logs and metrics for evaluation
* **A2A Protocol:** monitor agent triggers notifications

---

## 7. Demo Flow

**Step 1:** User initiates a trip

```text
"Plan a trip to Bangkok from Mar 10–15, budget $1200, style: food + culture."
```

**Step 2:** Preference Collector stores the input; agents fetch options:

* Flights
* Hotels
* Activities

**Step 3:** Ranking & Optimization Agent uses Gemini to select best options.

**Step 4:** Itinerary Builder generates a detailed 5-day itinerary.

**Step 5:** Price Monitor Loop Agent stores baseline prices.

**Step 6:** Simulate a hotel price drop:

* Hotel price drops from $112 → $96.
* Notification Agent alerts:

```text
"Hotel Bangkok Central dropped from $112 → $96. Recommend booking now."
```

**Step 7:** User accepts changes → itinerary re-optimized automatically.

---

## 8. Results (Example)

| Component              | Initial Price | New Price | Notes                                           |
| ---------------------- | ------------- | --------- | ----------------------------------------------- |
| Flight: Example Air    | $680          | $680      | No change                                       |
| Hotel: Bangkok Central | $112/night    | $96/night | Price drop triggered notification               |
| Activities             | —             | —         | Activities listed as Gemini-generated itinerary |
| Total Trip Cost        | $1,150        | $1,134    | Savings applied automatically                   |

* The itinerary is **dynamic and adaptive**
* All price changes logged and evaluated
* Agents coordinate seamlessly to maintain traveler preferences

---

## 9. Limitations

* SERP API rate limits
* No direct booking functionality
* Price monitoring requires active trigger or periodic notebook execution
* Activities depend on search accuracy

---

## 10. Future Work

* Integrate Google Calendar for itinerary export
* Loyalty reward optimization for flights & hotels
* Group travel support
* Visual timeline of itinerary with maps
* Continuous agent learning for improved ranking and activity selection

---

## 11. Attachments

* **GitHub Repository** (public) containing:

  * Notebook (`.ipynb`) with all agents and demo flow
  * Memory and price monitoring setup
  * Placeholder SERP API / Gemini calls
* **Kaggle Notebook** (optional demo version)

---

**Submission Track:** Track A — Concierge Agents

This notebook demonstrates a **fully agentic, living, dynamic itinerary system** using **Google ADK + Gemini**, with no OpenAI dependencies.
