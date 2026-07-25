# Maya Property Bot — Architecture Overview
**Project:** PropBot AI · Chennai Properties  
**Technology:** LangGraph State Machine + Groq LLM (Llama 3.3-70b & Llama 3.1-8b)  
**Database:** MongoDB Atlas  
**Voice:** Deepgram STT · ElevenLabs TTS  

---

## Conversation Flow (9-Stage Architecture)

```
WELCOME → ASK_NAME → ASK_PROPERTY_TYPE → ASK_LOCATION → ASK_BUDGET
        → ASK_BHK_OR_SIZE → ASK_REFINEMENT → PROPERTY_SEARCH → LEAD_COMPLETE
```

---

## Active Nodes (13 in use)

### Core Conversation Flow

| # | Node Name | File | Stage | Purpose |
|---|-----------|------|-------|---------|
| 1 | `welcome` | `welcome_node.py` | WELCOME | Greets the user and sets the tone for the conversation. |
| 2 | `capture_name` | `capture_name_node.py` | ASK_NAME | **Omni-Extractor:** Captures name AND can extract all other preferences (type, location, budget, BHK) in a single shot, skipping redundant questions. |
| 3 | `capture_property_type` | `capture_property_type_node.py` | ASK_PROPERTY_TYPE | Detects the property type: Apartment, Villa, Independent House, or Plot. |
| 4 | `capture_location` | `capture_location_node.py` | ASK_LOCATION | Validates and maps user input to a known Chennai area (OMR, Velachery, Tambaram). Uses LLM fallback for flexible input. |
| 5 | `capture_budget` | `capture_budget_node.py` | ASK_BUDGET | Parses budget in natural language (e.g. "60 lakhs", "1.2 Cr") and converts to integer rupees. |
| 6 | `capture_bhk_or_size` | `capture_bhk_or_size_node.py` | ASK_BHK_OR_SIZE | **Dynamic Node:** Asks for BHK for residential properties OR land sqft for plots. Delivers the "Confidence Hook" message before advancing. |
| 7 | `capture_refinement` | `capture_refinement_node.py` | ASK_REFINEMENT | **Omni-Filter Node:** Extracts all optional preferences in a single LLM pass — Vastu, facing, ready-to-move, gym, pool, parking, security, pet-friendly, etc. |
| 8 | `property_search` | `property_search_node.py` | PROPERTY_SEARCH | Executes the MongoDB query. Has a **multi-tier fallback system** that progressively drops filters (amenities → sqft → budget → location) to always return results. Capped at 3 cards. |
| 9 | `lead_complete` | `lead_complete_node.py` | LEAD_COMPLETE | The post-search hub. Handles: Brochure requests, Price breakdowns, Call-back requests, New searches, and saves Phone/Email to the database. |

### Specialist Nodes (Side Branches)

| # | Node Name | File | Triggered By | Purpose |
|---|-----------|------|--------------|---------|
| 10 | `faq` | `faq_handler.py` | Any question mark or question word | Interrupt node. Uses pattern-matching for instant answers (EMI, stamp duty, areas). Falls back to LLM (Llama 3.3-70b) for all other questions. Resumes the original stage after answering. |
| 11 | `compare` | `comparison_engine.py` | "compare", "vs", "difference" | Generates a markdown comparison table for 2-3 shortlisted properties. |
| 12 | `book_visit` | `booking_agent.py` | "visit", "schedule", "book" | Collects date, time, and phone number for a site visit booking. |
| 13 | `human_handoff` | `lead_capture.py` | "talk to someone", "human" | Captures lead info (name + phone) for a senior consultant callback. |

---

## Intents (12 defined)

Intents are classified by the `route_by_stage()` function in `graph.py` based on the user's message and current stage.

| # | Intent | Triggered When | Action Taken |
|---|--------|----------------|--------------|
| 1 | `GIVE_INFO` | User gives a direct short answer (name, location, budget, yes/no). | State is updated with the extracted value and the flow advances. |
| 2 | `FORCE_SEARCH` | User says "just show me", "go ahead", "search now". | Skips remaining collection stages and jumps directly to `PROPERTY_SEARCH`. |
| 3 | `RESET` | User says "start over", "fresh search", "different area". | Clears all filters and restarts from `ASK_LOCATION`. |
| 4 | `REMOVE_FILTER` | User says "remove gym", "forget the budget". | Uses LLM extractor to identify the filter field and removes it, then re-runs the search. |
| 5 | `FAQ` | User asks a question (detected by "?", "what", "how", "is", "can"). | Routes to `faq` node. Answers the question and resumes from the same stage. |
| 6 | `COMPARE` | User says "compare", "vs", "difference between". | Routes to `compare` node to generate a comparison table. |
| 7 | `BOOK_VISIT` | User says "visit", "schedule", "book a site visit". | Routes to `book_visit` node to collect booking details. |
| 8 | `LEAD_RESPONSE` | User provides their phone number or email address. | Captured and saved to the `leads` collection in MongoDB. |
| 9 | `SMALL_TALK` | Greetings, "thank you", jokes, off-topic chatter. | LLM responds warmly and gently brings the conversation back to property search. |
| 10 | `PROPERTY_DETAIL` | User asks about a specific property card ("tell me more about option 2"). | `lead_complete_node` uses LLM to answer contextually based on the search results. |
| 11 | `HUMAN_HANDOFF` | User says "let me talk to someone", "human please". | Routes to `human_handoff` node to collect contact info. |
| 12 | `NEGOTIATE` | User asks "can I get a discount?", "is the price negotiable?". | `lead_complete_node` responds with a warm, consultant-level answer. |

---

---

## Summary of Cleanup
Legacy nodes and unused service/model files have been removed from the repository to ensure a clean, production-ready codebase for Git deployment. The system now strictly follows the 9-stage architecture defined above.

---

## Key Technical Highlights

| Feature | Implementation |
|---------|---------------|
| **One-Shot Extraction** | `capture_name_node.py` uses a single LLM call to extract name + property type + location + budget + BHK + 12 amenity flags simultaneously. Skips redundant stages. |
| **Dynamic Routing** | `get_next_stage()` in `state.py` calculates the next missing piece of information and jumps directly to it. |
| **Ultimate Fallback Search** | `property_search_node.py` progressively relaxes filters (amenities → sqft → budget → location) to ensure results are always returned. |
| **Lead DB Integration** | `lead_service.py` saves name, phone, email, location, and budget to MongoDB `leads` collection in real-time. |
| **FAQ Interrupt** | `graph.py` intercepts question-like messages at any collection stage, routes to `faq_handler.py`, and resumes the original stage. |
| **Voice STT** | Deepgram Nova-2 with `smart_format`, `interim_results`, and `utterance_end_ms` for accurate real-time transcription. |
| **Voice TTS** | ElevenLabs WebSocket streaming with browser TTS fallback if ElevenLabs is unavailable. |
