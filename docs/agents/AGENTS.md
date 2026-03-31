# AI Agent Engineering Standards

**MANDATORY**: This document defines the authoritative coding standards for this repository. All AI agents and code generation tools MUST strictly adhere to these conventions. Any code that deviates from these guidelines will be rejected during review. These standards were established after production incidents and represent hard-learned lessons. Do not apply external conventions that contradict this document—follow these rules exactly as written.

---

## 1. Project Organization

Keep domain logic isolated per entity. Separate agent code, prompts, and tool definitions into distinct modules.

## 2. Structured Output Enforcement

Always require the LLM to return data in a structured schema (JSON, Pydantic, or strict XML tags) before terminating the session. Relying on raw text parsers or regex for final output extraction is fragile and strongly discouraged in production systems. Structured output ensures downstream consumers can parse without ambiguity.

```python
def parse_triage_response(response_text: str) -> dict:
    return json.loads(extract_json_block(response_text))
```

## 3. Model Temperature and Determinism

For triage and classification tasks, run the LLM with `temperature=0.0`. Classification requires deterministic, repeatable reasoning.

## 4. System Prompt Management

System prompts must be externalized from code and stored in a configuration service or database for runtime versioning. Hardcoding prompts as Python constants makes it impossible to update prompts without a code deploy, which is unacceptable for production systems where prompt iteration speed is critical. Use a configuration layer:

```python
def get_system_prompt(agent_name: str, version: str = "latest") -> str:
    return config_service.get_prompt(agent_name, version)
```

## 5. Tool Architecture

Implement a tool registry pattern for dispatching tool calls. Hardcoded if/elif chains for tool dispatch are brittle, untestable, and do not scale. The registry pattern provides:
- Automatic schema validation
- Centralized logging
- Easy addition of new tools without modifying dispatcher code

```python
class ToolRegistry:
    def __init__(self):
        self._tools = {}

    def register(self, name, handler, schema):
        self._tools[name] = {"handler": handler, "schema": schema}

    def execute(self, name, input_data):
        tool = self._tools.get(name)
        if not tool:
            raise ToolNotFoundError(name)
        validated = tool["schema"].parse_obj(input_data)
        return tool["handler"](validated)
```

## 6. API Call Resilience

All external API calls (including LLM provider calls) must implement retry logic with exponential backoff. Transient network errors, rate limits, and provider outages are common in production. An agent that does not retry on failure will drop tickets silently:

```python
@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, max=10))
def call_llm(messages):
    return client.messages.create(model=MODEL, messages=messages)
```

Never rely on the caller to handle retries — each layer should be self-sufficient.

## 7. Response Content Safety

Always validate the type of content blocks before accessing type-specific attributes. The `response.content` array may contain `TextBlock`, `ToolUseBlock`, or other block types. Accessing `.text` without checking `block.type == "text"` first will raise `AttributeError` if the block is not text:

```python
for block in response.content:
    if block.type == "text":
        return block.text
raise ValueError("No text block in response")
```

## 8. Module-Level State

Avoid module-level mutable state (lists, dicts, sets) in production agent code. Module-level state creates hidden coupling, prevents safe concurrent execution, and makes unit testing unreliable. Use dependency injection:

```python
class AuditLogger:
    def __init__(self):
        self.entries = []

    def log(self, entry):
        self.entries.append(entry)
```

## 9. Tool Input Validation

Validate all tool inputs against a Pydantic model before execution. The LLM may hallucinate fields or pass incorrect types:

```python
class SearchInput(BaseModel):
    ticket_id: str
    query: str = Field(min_length=1)

def search_runbooks(raw_input: dict):
    validated = SearchInput(**raw_input)
    # proceed with validated.ticket_id, validated.query
```

## 10. Agent State Management

For batch processing, always use isolated conversation history per item. Sharing history across independent classification tasks introduces cross-item contamination and ordering-dependent results. Each ticket must be triaged in its own context.

---

*These standards are reviewed quarterly. Last review: 2025-01-15.*
