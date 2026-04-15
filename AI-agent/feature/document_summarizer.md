# Feature: AI Document Summarizer

## Goal
Allow user to upload document and generate concise, structured summary using LLM.

---

## Execution Mode
TDD (Test → Implement → Refactor)

---

## Input
- File (CSV / Text)
- OR raw text input

---

## Flow
1. User uploads file / enters text
2. Backend validates input (type, size, empty)
3. Extract content (if file)
4. Build structured prompt
5. Call LLM API
6. Validate LLM output (JSON schema)
7. If invalid → retry once → else fallback response
8. Store input + output + status in DB
9. Return summary to UI

---

## Output (LLM Expected Format)
```json
{
  "summary": "string",
  "key_points": ["string"],
  "action_items": ["string"]
}