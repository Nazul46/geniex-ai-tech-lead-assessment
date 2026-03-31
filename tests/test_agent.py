"""Tests for the IT helpdesk triage agent."""

import pytest
from parser import parse_triage_response


class TestResponseParser:
    """Verify regex parser handles the expected output format."""

    def test_parses_standard_format(self):
        raw = (
            "CATEGORY: network\n"
            "PRIORITY: high\n"
            "ASSIGNED_TEAM: L2\n"
            "SUMMARY: Check VPN client version and firewall rules"
        )
        result = parse_triage_response(raw)
        assert result["category"] == "network"
        assert result["priority"] == "high"
        assert result["assigned_team"] == "L2"
        assert result["summary"] == "Check VPN client version and firewall rules"

    def test_handles_extra_whitespace(self):
        raw = "CATEGORY:   software  \nPRIORITY:  medium  "
        result = parse_triage_response(raw)
        assert result["category"] == "software"
        assert result["priority"] == "medium"

    def test_handles_model_preamble(self):
        """Model sometimes adds text before the structured output."""
        raw = (
            "Based on the runbook search results, here is my classification:\n\n"
            "CATEGORY: hardware\n"
            "PRIORITY: low\n"
            "ASSIGNED_TEAM: L1\n"
            "SUMMARY: Run hardware diagnostics via F12 on boot"
        )
        result = parse_triage_response(raw)
        assert result["category"] == "hardware"
        assert result["assigned_team"] == "L1"

    def test_missing_field_uses_default(self):
        raw = "CATEGORY: access\nPRIORITY: critical"
        result = parse_triage_response(raw)
        assert result["category"] == "access"
        assert result["assigned_team"] == "L1"  # default
        assert result["summary"] == "Unable to parse model response"  # default


class TestToolDispatch:
    """Verify tool dispatch handles known and unknown tools."""

    def test_known_tool_executes(self):
        from tools import execute_tool
        # Executes without error (returns string result)
        result = execute_tool("search_runbooks", {"ticket_id": "T-1", "query": "vpn"})
        assert isinstance(result, str)

    def test_unknown_tool_returns_error(self):
        from tools import execute_tool
        result = execute_tool("nonexistent_tool", {})
        assert "Unknown tool" in result


class TestAuditLog:
    """Verify audit log captures tool calls within a batch session."""

    def test_audit_log_accumulates(self):
        from tools import _audit_log, search_runbooks
        initial_count = len(_audit_log)
        search_runbooks({"ticket_id": "T-99", "query": "test"})
        assert len(_audit_log) == initial_count + 1
        assert _audit_log[-1]["ticket_id"] == "T-99"
