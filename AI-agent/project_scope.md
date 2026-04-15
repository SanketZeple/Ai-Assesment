# Project Scope: AI Document Summarizer

## Overview
AI-powered web application that generates structured summaries from user-provided documents using an LLM.

---

## Tech Stack
Backend: FastAPI  
Frontend: React  
Database: PostgreSQL  
AI: LLM API  

---

## Project Structure
- Root (parent folder)
  - backend/ (FastAPI service)
  - frontend/ (React app)

---

## Application Flow
1. User uploads file or enters text
2. Backend receives and validates input
3. System builds structured prompt
4. LLM generates summary
5. Response is validated
6. Fallback used if invalid/error
7. Result stored in DB
8. Summary displayed on UI

---

## Core Capabilities
- Document/Text summarization
- Structured output (summary, key points, action items)
- Error handling + fallback response
- Logging of requests and responses