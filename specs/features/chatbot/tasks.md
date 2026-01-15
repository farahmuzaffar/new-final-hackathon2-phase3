# Phase 3 – AI-Powered Todo Chatbot (Hackathon II)

This task list implements **Hackathon II – Phase III** exactly as defined in the official
specification. Scope is intentionally limited to Phase III only.

Tech Stack:
- FastAPI (Backend)
- OpenAI Agents SDK (AI Logic)
- Official MCP SDK (Tooling)
- SQLModel + Neon PostgreSQL (Persistence)
- Better Auth JWT (Authentication)

---

## Task 1: Chat API Endpoint (Stateless)
- Implement POST `/api/{user_id}/chat`
- Accept:
  - message (string)
  - optional conversation_id
- Verify JWT and authenticated user
- Do NOT store server-side state in memory

---

## Task 2: Conversation Persistence
- Create database models:
  - Conversation (id, user_id, timestamps)
  - Message (id, conversation_id, role, content, timestamp)
- Fetch conversation history from DB on every request
- Store user and assistant messages in DB

---

## Task 3: AI Agent Setup (OpenAI Agents SDK)
- Initialize AI agent using OpenAI Agents SDK
- Configure system behavior according to chatbot-agent spec
- Agent must:
  - Interpret natural language
  - Decide which MCP tool to call
  - Never access DB directly

---

## Task 4: MCP Server & Tools (Official MCP SDK)
- Build MCP server exposing Todo operations as tools:
  - add_task
  - list_tasks
  - update_task
  - complete_task
  - delete_task
- MCP tools must:
  - Be stateless
  - Call existing Phase-II Todo REST APIs
  - Enforce user ownership via JWT

---

## Task 5: Agent → MCP → Todo API Flow
- Run agent with:
  - conversation history
  - new user message
- Allow agent to invoke one or more MCP tools
- Capture tool calls made by the agent
- Return assistant response + tool call summary

---

## Task 6: Conversational CRUD Coverage
- Ensure chatbot supports **all Basic Level features**:
  - Add task
  - List tasks
  - Update task
  - Delete task
  - Mark task complete
- Natural language examples must work (as per spec)

---

## Task 7: Error Handling & Confirmation
- Handle:
  - Task not found
  - Invalid task ID
  - Empty task list
- Always confirm successful actions in natural language
- Fail gracefully with user-friendly messages

---

## Task 8: Phase 3 Validation
- Confirm:
  - Stateless server behavior
  - Conversation resumes after restart
  - Agent uses MCP tools ONLY
  - Phase-II APIs remain unchanged
- Prepare for Phase IV (Kubernetes) without implementing it
