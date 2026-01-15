# Phase 3 – AI Chatbot Architecture Plan

## Overview
This plan describes the Phase 3 architecture for integrating an AI-powered chatbot into the existing Todo application, strictly following Hackathon II Phase 3 requirements.

## Architecture Components
- Chat API Endpoint (POST /chat)
- AI Agent (OpenAI Agents SDK)
- MCP Tools Layer (Official MCP SDK)
- Existing Todo REST API (Phase 2 backend)

## Interaction Flow
1. User sends a natural language message to the /chat endpoint
2. The AI agent interprets intent using OpenAI Agents SDK
3. The agent selects the appropriate MCP tool
4. MCP tool calls the existing Todo REST API
5. Backend performs the operation and returns the result
6. The agent formats a user-friendly response

## Constraints
- The AI agent must always use MCP tools for task operations
- The chatbot must not access the database directly
- No business logic duplication is allowed
- Existing backend APIs remain unchanged
- No Kubernetes, Docker, Kafka, or cloud deployment in Phase 3

## Out of Scope
- Research artifacts
- Data model changes
- New API contracts
- UI implementation
- Memory, embeddings, or vector databases

## Phase Boundary
This plan applies only to Hackathon II Phase 3. Advanced infrastructure and deployment concerns are deferred to later phases.
