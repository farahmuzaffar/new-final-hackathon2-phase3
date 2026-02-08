FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# We'll keep everything under /app
WORKDIR /app

# Install deps needed by:
# - ai-agent (fastapi, uvicorn, openai-agents, openai-agents-mcp)
# - mcp-server (mcp, httpx)
RUN pip install --no-cache-dir \
  fastapi uvicorn httpx python-dotenv \
  mcp openai openai-agents openai-agents-mcp

# Copy code
COPY mcp-server /app/mcp-server
COPY ai-agent /app/ai-agent

# Run from ai-agent folder so "from agent import ..." works
WORKDIR /app/ai-agent
ENV PYTHONPATH=/app/ai-agent:/app

EXPOSE 8001
CMD ["python", "main.py"]
