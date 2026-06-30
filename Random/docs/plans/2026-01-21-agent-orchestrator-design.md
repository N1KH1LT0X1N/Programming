# Agent Orchestrator Design Document

**Date:** 2026-01-21
**Topic:** Local Agent Orchestrator & Background Service

## 1. High-Level Architecture

The system follows a **Client-Server** architecture designed to run locally on the user's machine. This separates the long-running agent processes from the user interface, ensuring responsiveness and background execution capabilities.

### Components

1.  **The Server ("The Brain")**
    *   **Technology:** Python with FastAPI.
    *   **Responsibility:** Central hub for request processing, agent orchestration, and state management.
    *   **Execution Model:** Runs as a background daemon/service.
    *   **Persistence:** SQLite database for task history, results, and future "memory" features.

2.  **The Interface Layer**
    *   **CLI Tool:** A `typer`-based command-line interface for sending commands (e.g., `agent run "research LLMs"`).
    *   **System Tray / Hotkey Listener:** A lightweight Python script (using `pystray` and `keyboard`) residing in the system tray.
        *   **Function:** Listens for a global hotkey, captures input (or clipboard), and forwards requests to the Server via API.

## 2. Agent Logic & Orchestration

The system uses **LangGraph** to manage complex, multi-step agent behaviors, supported by standard `asyncio` for concurrent execution.

### Orchestration Engine
*   **Workflow Management:** LangGraph defines the logic flows, enabling cyclic behaviors essential for research tasks (Search -> Analyze -> Refine -> Summarize).
*   **Concurrency:** Python `asyncio` handles background tasks, avoiding the overhead of heavy message queues like Celery/Redis for this version.

### The "Main Agent" (Router)
*   Acts as the single entry point for all user requests.
*   **Function:** Analyzes the user's intent and routes the task to a specialized sub-graph.
    *   *Research Intent* -> Routes to **ResearchGraph**.
    *   *Writing Intent* -> Routes to **WriterGraph**.

### Tools & Capabilities
*   **Web Search:** Integration with search providers (e.g., Tavily, DuckDuckGo).
*   **Content Retrieval:** Lightweight scraper/browser tool to fetch web pages and PDFs.
*   **File System Access:** Capability to save final reports and summaries to the local disk.

### Notifications
*   The system uses native desktop notifications (toasts) to alert the user when a background task is complete.

## 3. Data Persistence & API Structure

### Data Model (SQLite)
Structured to support current needs and future "Supermemory" features.
*   **Tasks:** Stores prompt, execution status, and final results.
*   **Artifacts:** References to generated files or visited resources.
*   **UserPreferences:** (Future) Stores learned user patterns and context.

### API Endpoints (FastAPI)
*   `POST /agent/submit`: Accepts a new prompt and returns a Task ID.
*   `GET /agent/status/{task_id}`: Polling endpoint for progress updates.
*   `GET /agent/history`: Retrieves past task history.
*   `POST /agent/stop/{task_id}`: Terminates a running task.

### Deployment & Setup
*   **Dependency Management:** `poetry` or `pip` (requirements.txt).
*   **Configuration:** `.env` file for secure API key management.
*   **Startup:** A unified script (`start.sh`/`start.bat`) to launch both the API server and the System Tray listener.
