# IT Helpdesk Triage Agent

An LLM-powered triage agent that classifies incoming IT support tickets. Built with the Anthropic Claude API.

## What It Does

1. Accepts a raw support ticket
2. Calls `search_runbooks` to retrieve relevant troubleshooting steps via a RAG pipeline
3. Classifies the ticket into a structured output (category, priority, team, summary)
4. Processes multiple tickets in a batch session

## Project Structure

```
src/
├── main.py          # Batch entry point
├── agent.py         # Agent orchestrator (tool loop + history management)
├── tools.py         # Tool definitions and dispatch
├── retrieval.py     # RAG pipeline (embedding, similarity, chunking)
├── parser.py        # Response parsing
├── prompts.py       # System prompt
└── config.py        # Model and pipeline configuration

tests/
└── test_agent.py    # Unit tests

data/
└── eval_tickets.json  # Labeled evaluation dataset
```

## Assessment

If you are taking the hiring assessment, see **[assessment.md](assessment.md)** for instructions.
