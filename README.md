Below is my README:



# Rayeva AI Systems Assignment

A FastAPI solution for the Rayeva Full Stack / AI Intern assignment.

Implemented modules:
1. **AI Auto-Category & Tag Generator**
2. **AI B2B Proposal Generator**

Architected but not fully implemented:
3. AI Impact Reporting Generator
4. AI WhatsApp Support Bot

## Stack
- FastAPI
- SQLAlchemy
- SQLite (easy local/Codespaces demo)
- OpenAI-compatible client (works with Groq/OpenAI-compatible endpoints)
- GitHub Codespaces devcontainer

## Security
- API key is loaded from `.env`
- `.env` is ignored by git
- only `.env.example` is committed
- recommended in Codespaces: store `AI_API_KEY` as a Codespaces secret and paste it into `.env`

## Run in Codespaces
1. Create a new GitHub repo.
2. Upload/push this project.
3. Open the repo in Codespaces.
4. Copy `.env.example` to `.env`.
5. Add your real API key in `.env`.
6. Start the app:
   ```bash
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
7. Open the forwarded port and visit `/docs`.

## Example API Requests

### 1) Auto-Category & Tag Generator
`POST /ai/category-tags`
```json
{
  "product_name": "OceanSafe Steel Bottle",
  "description": "A reusable stainless steel bottle for employees and events.",
  "materials": ["stainless steel"],
  "target_market": "B2B corporate gifting",
  "price": 349
}
```

### 2) B2B Proposal Generator
`POST /ai/proposals`
```json
{
  "buyer_name": "GreenBridge Consulting",
  "buyer_type": "Corporate",
  "budget": 50000,
  "goals": ["employee gifting", "brand visibility"],
  "preferred_categories": ["Drinkware", "Stationery"],
  "sustainability_focus": ["reusable", "plastic reduction"]
}
```

## Architecture

### Implemented module 1: AI Auto-Category & Tag Generator
Flow:
- Accept product input
- Build strict prompt
- Ask model for structured JSON
- Validate with Pydantic
- Store result in `product_analyses`
- Log prompt + response in `prompt_logs`

### Implemented module 2: AI B2B Proposal Generator
Flow:
- Accept buyer profile + budget + goals
- Provide compact product catalog context
- Ask model for structured JSON proposal
- Validate with Pydantic
- Store output in `proposals`
- Log prompt + response in `prompt_logs`

### Planned module 3: AI Impact Reporting Generator
Suggested design:
- Input: final order lines + quantities + source metadata
- Rule layer: known constants for plastic saved / carbon avoided / local sourcing score
- AI layer: turn calculated metrics into a client-friendly impact narrative
- Store both raw metrics and human-readable impact statement with order

Proposed tables:
- `orders`
- `order_items`
- `impact_reports`

### Planned module 4: AI WhatsApp Support Bot
Suggested design:
- Webhook endpoint for incoming WhatsApp messages
- Intent classification layer: order-status / return-policy / refund-escalation
- For order status: fetch real DB order info
- For policy: respond from approved policy knowledge base
- For refund/high-priority: create escalation ticket
- Log all messages, intents, AI outputs, and escalation events

Proposed tables:
- `support_conversations`
- `support_messages`
- `support_escalations`

## Folder Structure
```text
app/
  api/routes.py
  core/config.py
  db/session.py
  models/entities.py
  schemas/
  services/
  utils/catalog.py
  main.py
.devcontainer/devcontainer.json
.env.example
requirements.txt
README.md
```

## Design Choices
- SQLite keeps the demo friction low for evaluator testing.
- OpenAI-compatible client lets you switch providers with config only.
- Service layer separates AI orchestration from HTTP handlers.
- Fallback logic lets the app still demonstrate behavior even if no key is configured.

## Demo Plan (3–5 min)
1. Show repo structure and `.env.example`
2. Show `.gitignore` proving secrets are excluded
3. Launch FastAPI in Codespaces
4. Demo `/docs`
5. Run category generation request
6. Run proposal generation request
7. Show SQLite-stored outputs and prompt logs

## SQLite
1. Open in terminal using:
   ```bash
   sqlite raveya.db
   ```
2. Then inside SQLite:
   ```text
.tables
.mode column
.headers on
SELECT * FROM product_analyses;
SELECT * FROM proposals;
SELECT * FROM prompt_logs;
```
