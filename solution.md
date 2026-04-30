## Q1: Retrieval Fix

### Is increasing top_k effective?
No, increasing top_k is not an effective solution because it increases the number of retrieved documents but does not improve the relevance of results, and may introduce more noise.

### Root Cause
The retrieval pipeline relies purely on semantic similarity (embeddings), which does not prioritize exact keyword matches such as specific error codes (e.g., "error code 619"). As a result, generic VPN-related documents are ranked higher than the specific troubleshooting guide for that error.

### Proposed Fix
Introduce a lightweight keyword-aware retrieval step to complement the semantic search. For example, detect patterns like "error code <number>" in the query and boost or filter documents that contain the exact same code before or during ranking.

This can be implemented as a minimal change by:
- Adding a keyword match score to the existing similarity score, or
- Filtering candidate documents to prioritize exact matches before applying vector similarity.

This ensures that highly specific queries retrieve the correct targeted documents without significantly increasing system complexity.

## Q2: Code Review Triage

A. **Real Bug** — Sharing conversation history across tickets can cause context leakage between unrelated requests, leading to incorrect classifications.

B. **Acceptable** — Naive slice deletion is sufficient for this simple use case and does not introduce correctness issues, though it may not be optimal.

C. **Real Bug** — Accessing `response.content[0].text` without checking the content type can lead to runtime errors if the structure changes.

D. **Real Bug** — Lack of retry logic on API calls reduces system reliability and can cause failures in production due to transient errors.

E. **Acceptable** — Using `if` statements for tool dispatch is fine for a small number of tools and keeps the implementation simple.

F. **Partially Acceptable** — Using `params.get()` without validation is not immediately breaking but introduces risk of silent failures and should ideally be replaced with structured validation.