"""Orchestrator for the IT triage agent."""

from config import client, MODEL, MAX_TOKENS, MAX_HISTORY_MESSAGES
from tools import TOOLS, execute_tool
from prompts import SYSTEM_PROMPT
from parser import parse_triage_response


def _prune_history(history_list):
    """Keep only the most recent messages to prevent context exhaustion."""
    if len(history_list) > MAX_HISTORY_MESSAGES:
        del history_list[:-MAX_HISTORY_MESSAGES]
    return history_list


def triage_ticket(ticket_text, ticket_id, conversation_history):
    """Process a single ticket through the triage loop."""

    conversation_history.append({"role": "user", "content": ticket_text})

    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=SYSTEM_PROMPT,
        tools=TOOLS,
        messages=conversation_history,
    )

    while response.stop_reason == "tool_use":
        tool_block = next(b for b in response.content if b.type == "tool_use")

        tool_result = execute_tool(tool_block.name, tool_block.input)

        conversation_history.append(
            {"role": "assistant", "content": response.content}
        )
        conversation_history.append(
            {
                "role": "user",
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": tool_block.id,
                        "content": tool_result,
                    }
                ],
            }
        )

        _prune_history(conversation_history)

        response = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            system=SYSTEM_PROMPT,
            tools=TOOLS,
            messages=conversation_history,
        )

    raw_response = response.content[0].text
    conversation_history.append({"role": "assistant", "content": response.content})

    _prune_history(conversation_history)

    result = parse_triage_response(raw_response)
    result["ticket_id"] = ticket_id

    return result
