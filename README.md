# Rayeva AI Systems Assignment

A FastAPI-based solution for the Rayeva Full Stack / AI Intern assignment.

## Implemented Modules
1. **AI Auto-Category & Tag Generator**
2. **AI B2B Proposal Generator**

## Architected but Not Fully Implemented
3. **AI Impact Reporting Generator**
4. **AI WhatsApp Support Bot**

---

## Stack
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- OpenAI-compatible AI client
- GitHub Codespaces

---

## Security and Configuration
- Secrets are **not hardcoded** in the codebase.
- `.env` is ignored by git.
- Only `.env.example` is committed.
- In GitHub Codespaces, the recommended setup is to store the real API key as a **Codespaces secret** and let the app read it from the environment.
- `.env` can be used only for local development defaults.

### Example `.env.example`
```env
APP_NAME=Rayeva AI Systems Assignment
APP_ENV=development
DEBUG=true
DATABASE_URL=sqlite:///./rayeva.db

AI_PROVIDER=openai_compatible
AI_MODEL=llama-3.3-70b-versatile
AI_API_KEY=your_api_key_here
AI_BASE_URL=https://api.groq.com/openai/v1
