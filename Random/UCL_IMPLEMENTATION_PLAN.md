# UCL IMPLEMENTATION PLAN

## Phased Build Guide for AI-Assisted Development

---

> **How to use this document:**
>
> 1. Work through phases **in order** — each builds on the previous
> 2. Each phase is **self-contained** — copy the entire phase section and give it to your AI assistant
> 3. At the start of each phase, there's a **"Context for AI"** block — paste that to your assistant first
> 4. Don't skip phases. Phase 1 must be 100% working before you start Phase 2
> 5. Each phase has a **"Definition of Done"** checklist — verify every item before moving on

---

## PROJECT OVERVIEW (Read This First)

**What is UCL?** A pip-installable Python library that wraps LLM clients (OpenAI, Anthropic) transparently to add automatic context management, semantic caching, topic tracking, and cost optimization.

**The one-liner:**
```python
from ucl import with_context
from openai import OpenAI

client = with_context(OpenAI())  # That's it. Everything else is automatic.
```

**Tech stack:** Python 3.10+, SQLite (WAL mode), numpy, sqlite-vec (optional), sentence-transformers (optional)

---

## PHASE DEPENDENCY MAP

```
Phase 1: Foundation
    │
    ├──► Phase 2: Providers & Wrapper
    │        │
    │        └──► Phase 4: Scoring & Pipeline ◄── Phase 3: Embeddings
    │                  │
    │                  ├──► Phase 5: Caching & Topics
    │                  │
    │                  └──► Phase 6: API, CLI & Polish
    │
    └──► Phase 3: Embeddings (can start in parallel with Phase 2)
    
Phase 7: Advanced Memory (Future — after v1.0)
```

**Critical path:** 1 → 2 → 4 → 6
**Can be parallelized:** Phase 2 and Phase 3 can be built simultaneously after Phase 1

---

## PROJECT STRUCTURE (Final Target)

```
ucl/
├── pyproject.toml
├── README.md
├── src/
│   └── ucl/
│       ├── __init__.py              # Public API: with_context, UCLConfig
│       ├── config.py                # UCLConfig dataclass
│       ├── engine.py                # ContextEngine (orchestrator)
│       ├── wrapper.py               # WrappedClient, _NamespaceProxy
│       ├── streaming.py             # StreamAccumulator, AsyncStreamAccumulator
│       ├── debug.py                 # UCLDebugLogger, CostTracker
│       ├── providers/
│       │   ├── __init__.py
│       │   ├── base.py              # ProviderAdapter ABC, ProviderRegistry
│       │   ├── openai_adapter.py
│       │   └── anthropic_adapter.py
│       ├── storage/
│       │   ├── __init__.py
│       │   ├── database.py          # Database, ConnectionPool
│       │   ├── schema.py            # SQL schema + migrations
│       │   ├── session_repo.py      # Session CRUD
│       │   ├── node_repo.py         # ContextNode CRUD
│       │   ├── cache_repo.py        # ResponseCache CRUD
│       │   └── topic_repo.py        # TopicBranch CRUD
│       ├── embeddings/
│       │   ├── __init__.py
│       │   ├── base.py              # EmbeddingProvider ABC, EmbeddingResult
│       │   ├── openai_provider.py
│       │   ├── sbert_provider.py
│       │   ├── ollama_provider.py
│       │   ├── engine.py            # EmbeddingEngine
│       │   └── quantizer.py         # BinaryQuantizer
│       ├── context/
│       │   ├── __init__.py
│       │   ├── scorer.py            # ScoringConfig, ScoringEngine
│       │   ├── assembler.py         # ContextAssembler, AssembledContext
│       │   ├── budget.py            # TokenBudgetManager
│       │   └── summarizer.py        # ProgressiveSummarizer
│       ├── pipeline/
│       │   ├── __init__.py
│       │   ├── stages.py            # All PipelineStage implementations
│       │   └── pipeline.py          # MessagePipeline
│       ├── cache/
│       │   ├── __init__.py
│       │   ├── bloom.py             # BloomFilter, ContentDeduplicator
│       │   ├── simhash.py           # SimHasher
│       │   ├── semantic.py          # SemanticCache
│       │   └── fingerprint.py       # ContextFingerprinter
│       ├── topics/
│       │   ├── __init__.py
│       │   ├── detector.py          # TopicDetector
│       │   └── manager.py           # TopicBranchManager
│       ├── code/
│       │   ├── __init__.py
│       │   ├── parser.py            # TreeSitterParser
│       │   └── ranking.py           # PageRank
│       ├── vector/
│       │   ├── __init__.py
│       │   └── index.py             # VectorIndex (HNSW + fallback)
│       ├── export/
│       │   ├── __init__.py
│       │   ├── json_export.py
│       │   └── markdown_export.py
│       └── cli/
│           ├── __init__.py
│           └── main.py              # Click CLI
└── tests/
    ├── __init__.py
    ├── conftest.py                  # Shared fixtures
    ├── test_storage.py
    ├── test_providers.py
    ├── test_wrapper.py
    ├── test_embeddings.py
    ├── test_scorer.py
    ├── test_assembler.py
    ├── test_pipeline.py
    ├── test_cache.py
    ├── test_topics.py
    └── test_e2e.py
```

---
---
---

# PHASE 1: PROJECT FOUNDATION

---

## Context for AI

> **Paste this to your AI assistant when starting Phase 1:**
>
> I'm building a Python library called UCL (Universal Context Layer). It's a pip-installable package that wraps LLM clients (like OpenAI) to add automatic context management.
>
> Right now I need to set up the project foundation:
> 1. Python package with pyproject.toml (using setuptools or hatchling)
> 2. Data models as Python dataclasses
> 3. Configuration dataclass (UCLConfig)
> 4. SQLite storage layer with WAL mode, connection pooling, and a complete schema
> 5. Repository classes for CRUD operations on sessions and context nodes
>
> Tech: Python 3.10+, SQLite with WAL mode, no ORMs (raw SQL), dataclasses, pathlib for paths.
> The library will eventually be imported as `from ucl import with_context`.

---

## 1.1 Goal

Set up the project structure, all core data models, configuration, and the SQLite storage layer. After this phase, you can create sessions, store context nodes, and query them — all persisted to disk.

## 1.2 Files to Create

| File | What It Does |
|------|-------------|
| `pyproject.toml` | Package definition, dependencies, entry points |
| `src/ucl/__init__.py` | Package root — just version for now |
| `src/ucl/config.py` | `UCLConfig` dataclass with all settings |
| `src/ucl/storage/__init__.py` | Storage package |
| `src/ucl/storage/database.py` | `Database` class, `ConnectionPool`, PRAGMA config |
| `src/ucl/storage/schema.py` | Complete SQL schema (all tables + indexes) |
| `src/ucl/storage/session_repo.py` | `SessionRepository` — CRUD for sessions |
| `src/ucl/storage/node_repo.py` | `ContextNodeRepository` — CRUD for context nodes |
| `tests/conftest.py` | Shared pytest fixtures (temp database, etc.) |
| `tests/test_storage.py` | Tests for database, sessions, and nodes |

## 1.3 Detailed Specifications

### pyproject.toml

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "ucl"
version = "0.1.0"
description = "Universal Context Layer for LLM applications"
requires-python = ">=3.10"
dependencies = [
    "numpy>=1.24",
    "lz4>=4.3",
]

[project.optional-dependencies]
openai = ["openai>=1.0", "tiktoken>=0.5"]
anthropic = ["anthropic>=0.18"]
local = ["sentence-transformers>=2.2"]
ollama = []  # uses urllib, no extra deps
all = ["ucl[openai,anthropic,local]"]
dev = ["pytest>=7.0", "pytest-asyncio>=0.21"]

[project.scripts]
ucl = "ucl.cli.main:cli"

[tool.hatch.build.targets.wheel]
packages = ["src/ucl"]
```

### UCLConfig (`src/ucl/config.py`)

A dataclass holding all configuration. Key fields:

| Field | Type | Default | Purpose |
|-------|------|---------|---------|
| `data_dir` | `Path` | `~/.ucl` | Where SQLite DB lives |
| `max_context_tokens` | `int \| None` | `None` (auto) | Token budget |
| `context_reserve_ratio` | `float` | `0.15` | Reserve for response |
| `window_size` | `int` | `10` | Sliding window messages |
| `embedding_provider` | `str` | `'auto'` | `'openai'`, `'local'`, `'ollama'`, `'auto'` |
| `enable_cache` | `bool` | `True` | Enable semantic caching |
| `enable_topics` | `bool` | `True` | Enable topic detection |
| `enable_code_analysis` | `bool` | `True` | Enable tree-sitter code parsing |
| `scoring_preset` | `str` | `'coding'` | `'chat'`, `'coding'`, `'research'`, `'persistent'` |
| `debug` | `bool` | `False` | Verbose logging |
| `track_costs` | `bool` | `True` | Cost tracking |

Include `auto_detect()` classmethod that:
- Sets `data_dir` from env var `UCL_DATA_DIR` or defaults to `~/.ucl`
- Detects if `OPENAI_API_KEY` is set → use OpenAI embeddings
- Detects if Ollama is running on localhost:11434 → use Ollama embeddings
- Falls back to local (sentence-transformers)
- Warns if data_dir is on NFS/network filesystem (SQLite WAL doesn't work on NFS)

### Database & ConnectionPool (`src/ucl/storage/database.py`)

**`Database` class:**
- Takes `db_path: Path` and optional `vector_extension_path`
- `connect()` → creates SQLite connection with these PRAGMAs:
  - `journal_mode = WAL`
  - `synchronous = NORMAL`
  - `mmap_size = 268435456` (256MB)
  - `cache_size = -64000` (64MB)
  - `page_size = 4096`
  - `temp_store = MEMORY`
  - `auto_vacuum = INCREMENTAL`
  - `foreign_keys = ON`
- `close()` → checkpoint WAL then close
- `checkpoint(mode='PASSIVE')` → `PRAGMA wal_checkpoint(...)`
- `vacuum()` → incremental vacuum

**`ConnectionPool` class:**
- Thread-safe via `threading.local()` for per-thread connections
- `_write_lock = threading.Lock()` for serializing writes
- `read()` context manager → yields connection (no lock needed in WAL mode)
- `write()` context manager → acquires write lock, BEGIN IMMEDIATE, yields, COMMIT/ROLLBACK
- `close_all()` → checkpoint and close everything
- Max connections configurable (default 8)

### SQL Schema (`src/ucl/storage/schema.py`)

Store all CREATE TABLE statements as a single string constant `SCHEMA_SQL`. Tables needed:

1. **`sessions`** — Top-level container
   - `id TEXT PRIMARY KEY` (UUID v7)
   - `name, description TEXT`
   - `project_path, project_name TEXT`
   - `default_model, default_provider TEXT NOT NULL`
   - `context_limit INTEGER NOT NULL`
   - Statistics: `total_nodes, total_tokens_in, total_tokens_out, total_cost_usd, cache_hit_count, cache_miss_count`
   - `is_active, is_archived BOOLEAN`
   - `created_at, last_active_at, archived_at INTEGER` (Unix ms)
   - `config_json TEXT`

2. **`context_nodes`** — Individual pieces of context
   - `id TEXT PRIMARY KEY`, `content_hash TEXT NOT NULL`
   - `type TEXT NOT NULL` — CHECK IN ('user_message', 'assistant_message', 'code_file', 'code_snippet', 'code_symbol', 'tool_call', 'tool_result', 'summary', 'system', 'error')
   - `content_raw TEXT`, `content_compressed BLOB`, `compression_algo TEXT`
   - `token_count, char_count INTEGER`
   - `base_importance, computed_importance REAL`
   - `access_count INTEGER`, `is_pinned BOOLEAN`
   - `session_id, parent_id, branch_id TEXT`, `sequence_num, depth INTEGER`
   - `topic_id TEXT`, `storage_tier TEXT DEFAULT 'warm'`
   - `file_path, language TEXT`
   - `created_at, accessed_at, modified_at INTEGER`
   - Many indexes on session, branch, topic, importance, pinned, type, content_hash

3. **`embeddings`** — Vector storage (separate table)
   - `node_id TEXT PRIMARY KEY` → FK to context_nodes
   - `model TEXT`, `dimension INTEGER`
   - `vector_f32 BLOB`, `vector_binary BLOB`
   - `created_at INTEGER`

4. **`topic_branches`** — Topic groupings
   - `id TEXT PRIMARY KEY`, `session_id TEXT`
   - `label, description TEXT`, `summary_short, summary_full TEXT`
   - `centroid_embedding BLOB`
   - `node_count, total_tokens INTEGER`
   - `is_active, is_archived, is_auto_generated BOOLEAN`

5. **`response_cache`** — Cached LLM responses
   - `id TEXT PRIMARY KEY`
   - `query_text, query_hash, query_normalized TEXT`
   - `query_embedding BLOB`
   - `context_hash TEXT`
   - `response_text TEXT`, `response_tokens INTEGER`
   - `model TEXT`, `temperature REAL`
   - `hit_count INTEGER`, `expires_at INTEGER`

6. **`session_files`** — Files tracked per session
7. **`metrics`** — Usage tracking
8. **`code_symbols`** — Code analysis results
9. **`code_edges`** — Dependencies between symbols

Include a function `initialize_schema(conn)` that runs all CREATE TABLE and CREATE INDEX statements.

### ContextNode dataclass

```python
@dataclass
class ContextNode:
    id: str
    content_hash: str
    type: str  # 'user_message', 'assistant_message', etc.
    content_raw: Optional[str]
    content_compressed: Optional[bytes]
    token_count: int
    char_count: int
    base_importance: float
    computed_importance: float
    access_count: int
    is_pinned: bool
    session_id: str
    parent_id: Optional[str]
    sequence_num: int
    topic_id: Optional[str]
    branch_id: str
    is_branch_point: bool
    storage_tier: str  # 'hot', 'warm', 'cold'
    created_at: int
    accessed_at: int
    modified_at: int
    subtype: Optional[str] = None
    file_path: Optional[str] = None
    language: Optional[str] = None
```

### ContextNodeRepository

Key methods:
- `create(content, type, session_id, branch_id, **kwargs) → ContextNode` — hashes content (SHA-256), counts tokens (approximate: `len(content) // 4`), compresses if > 1KB with lz4, generates UUID v7, inserts, updates session stats
- `get(node_id) → Optional[ContextNode]` — fetch by ID, updates accessed_at
- `get_content(node) → str` — decompresses if needed
- `find_by_session(session_id, limit, offset) → List[ContextNode]`
- `find_recent(session_id, limit) → List[ContextNode]` — most recent N, returned in chronological order
- `find_by_topic(topic_id) → List[ContextNode]`
- `update_importance(node_id, score)` and `batch_update_importance(updates)`
- `pin(node_id, reason)` / `unpin(node_id)`
- `exists(content_hash) → bool`
- `move_to_cold(node_ids)` — archives content, clears raw/compressed

### SessionRepository

Key methods:
- `create(model, provider, context_limit, **kwargs) → Session`
- `get(session_id) → Optional[Session]`
- `list_all(include_archived=False) → List[Session]`
- `update_stats(session_id, tokens_in, tokens_out, cost)`
- `archive(session_id)`

### UUID v7 Helper

```python
def generate_uuid7() -> str:
    """Generate time-sortable UUID v7."""
    import time, random
    timestamp_ms = int(time.time() * 1000)
    random_bits = random.getrandbits(74)
    uuid_int = (timestamp_ms << 80) | (0x7 << 76) | random_bits
    return format(uuid_int, '032x')
```

## 1.4 Tests to Write

```python
# tests/test_storage.py

def test_database_creates_file(tmp_path):
    """Database creates .db file and WAL file."""

def test_database_pragma_config(tmp_path):
    """WAL mode and other PRAGMAs are set correctly."""

def test_connection_pool_thread_safety(tmp_path):
    """Multiple threads can read simultaneously."""

def test_connection_pool_write_serialization(tmp_path):
    """Writes are serialized (no concurrent writes)."""

def test_schema_creation(tmp_path):
    """All tables and indexes are created."""

def test_session_crud(tmp_path):
    """Create, read, list, archive sessions."""

def test_context_node_create(tmp_path):
    """Create node, verify content_hash, token_count."""

def test_context_node_compression(tmp_path):
    """Content > 1KB is LZ4 compressed, decompression works."""

def test_context_node_dedup(tmp_path):
    """exists() returns True for duplicate content_hash."""

def test_context_node_find_recent(tmp_path):
    """find_recent returns last N in chronological order."""

def test_context_node_importance_update(tmp_path):
    """batch_update_importance changes computed_importance."""

def test_context_node_pin_unpin(tmp_path):
    """pin() sets is_pinned=True and base_importance=1.0."""
```

## 1.5 Definition of Done

- [ ] `pip install -e ".[dev]"` works from project root
- [ ] `from ucl.config import UCLConfig` works — `UCLConfig()` creates valid config
- [ ] `UCLConfig.auto_detect()` returns config with correct embedding_provider
- [ ] Database and ConnectionPool create a SQLite file with WAL mode
- [ ] All 9 tables are created by `initialize_schema()`
- [ ] SessionRepository: create, get, list, archive all work
- [ ] ContextNodeRepository: create, get, find_recent, exists, pin/unpin all work
- [ ] LZ4 compression triggers for content > 1KB and decompression returns original
- [ ] All tests pass with `pytest tests/test_storage.py -v`

---
---
---

# PHASE 2: PROVIDER ABSTRACTION & WRAPPER

---

## Context for AI

> **Paste this to your AI assistant when starting Phase 2:**
>
> I'm building UCL, a Python library that transparently wraps LLM clients. I already have Phase 1 done:
> - Project structure with pyproject.toml
> - UCLConfig dataclass
> - SQLite storage with Database, ConnectionPool
> - Schema with sessions, context_nodes, embeddings, etc.
> - SessionRepository and ContextNodeRepository for CRUD
>
> Now I need Phase 2: the provider abstraction and wrapper layer.
>
> **The key insight:** UCL wraps an existing LLM client using Python's `__getattr__` proxy pattern. When a user calls `client.chat.completions.create(...)`, UCL intercepts that call, processes the messages through its pipeline, then forwards the (possibly modified) request to the real client.
>
> I need:
> 1. ProviderAdapter ABC — normalizes messages between OpenAI and Anthropic formats
> 2. OpenAIAdapter — handles OpenAI's message format + tiktoken token counting
> 3. AnthropicAdapter — handles Anthropic's content_blocks format + calibrated token counting
> 4. ProviderRegistry — auto-detects provider from client object
> 5. WrappedClient — the `__getattr__` proxy that intercepts `.chat.completions.create()`
> 6. _NamespaceProxy — allows `client.chat.completions.create()` dot-access chaining
> 7. StreamAccumulator — collects streaming chunks into a complete response
> 8. SyntheticResponse — creates fake response objects for cache hits
>
> Important guards:
> - Double-wrapping guard: `with_context(with_context(client))` should not double-wrap
> - None client guard: passing None should raise TypeError immediately

---

## 2.1 Goal

Build the transparent wrapper that intercepts LLM API calls. After this phase, `with_context(OpenAI())` returns a wrapped client that correctly proxies all calls and can normalize messages between providers.

## 2.2 Files to Create

| File | What It Does |
|------|-------------|
| `src/ucl/providers/__init__.py` | Package exports |
| `src/ucl/providers/base.py` | `ProviderAdapter` ABC, `ProviderRegistry`, `NormalizedMessage` |
| `src/ucl/providers/openai_adapter.py` | OpenAI message normalization + token counting |
| `src/ucl/providers/anthropic_adapter.py` | Anthropic message normalization + token counting |
| `src/ucl/wrapper.py` | `WrappedClient`, `_NamespaceProxy` |
| `src/ucl/streaming.py` | `StreamAccumulator`, `AsyncStreamAccumulator`, `SyntheticResponse` |
| `tests/test_providers.py` | Adapter tests |
| `tests/test_wrapper.py` | Wrapper + proxy tests |

## 2.3 Detailed Specifications

### NormalizedMessage

```python
@dataclass
class NormalizedMessage:
    role: str            # 'system', 'user', 'assistant', 'tool'
    content: str         # Always a plain string
    name: Optional[str] = None
    tool_calls: Optional[list] = None
    tool_call_id: Optional[str] = None
```

### ProviderAdapter ABC

```python
class ProviderAdapter(ABC):
    @property
    @abstractmethod
    def name(self) -> str: ...
    
    @abstractmethod
    def normalize_messages(self, messages: List[dict]) -> List[NormalizedMessage]: ...
    
    @abstractmethod
    def denormalize_messages(self, messages: List[NormalizedMessage]) -> List[dict]: ...
    
    @abstractmethod
    def count_tokens(self, text: str, model: str) -> int: ...
    
    @abstractmethod
    def get_context_limit(self, model: str) -> int: ...
    
    @abstractmethod
    def extract_response_text(self, response) -> str: ...
    
    @abstractmethod
    def extract_usage(self, response) -> dict: ...  # {prompt_tokens, completion_tokens, total_tokens}
```

### OpenAIAdapter specifics:
- `count_tokens` uses `tiktoken` with fallback to `len(text) // 4`
- `get_context_limit` has a dict mapping model names to limits (gpt-4o → 128000, gpt-4o-mini → 128000, gpt-3.5-turbo → 16385, etc.)
- `extract_response_text` → `response.choices[0].message.content`
- **Validate** response has choices[0].message before extracting

### AnthropicAdapter specifics:
- `normalize_messages`: Anthropic uses `content` as a list of blocks `[{"type": "text", "text": "..."}]` — flatten to plain string
- `normalize_messages`: Anthropic puts system prompt in a separate `system` parameter, not in messages — handle this
- `count_tokens`: Use `anthropic.Client().count_tokens()` if available, else use calibrated fallback: `int(len(text) / 3.5)` (Anthropic's tokenizer averages ~3.5 chars/token)
- `get_context_limit`: claude-3-5-sonnet → 200000, claude-3-opus → 200000, etc.

### ProviderRegistry

```python
class ProviderRegistry:
    """Auto-detect provider from client object."""
    
    def detect(self, client: Any) -> ProviderAdapter:
        module = type(client).__module__
        if 'openai' in module:
            return OpenAIAdapter()
        elif 'anthropic' in module:
            return AnthropicAdapter()
        else:
            raise ValueError(f"Unsupported provider: {module}")
```

### WrappedClient

The magic proxy that makes `client.chat.completions.create(...)` work:

```python
class WrappedClient:
    _UCL_WRAPPED = True  # Marker for double-wrap detection
    
    def __init__(self, client, engine):
        if client is None:
            raise TypeError("Cannot wrap None — pass a valid LLM client")
        if getattr(client, '_UCL_WRAPPED', False):
            # Already wrapped — return as-is (set self to the existing wrapper)
            self.__dict__ = client.__dict__
            return
        
        self._client = client
        self._engine = engine
        self._adapter = ProviderRegistry().detect(client)
    
    def __getattr__(self, name):
        if name == 'ucl':
            return self._engine.api  # UCL-specific API
        # Return a namespace proxy that chains until .create() is called
        attr = getattr(self._client, name)
        if hasattr(attr, '__call__'):
            return attr  # Direct method — not the chat.completions path
        return _NamespaceProxy(attr, self._engine, self._adapter, self._client)
```

### _NamespaceProxy

```python
class _NamespaceProxy:
    """Proxy for namespace traversal (client.chat.completions)."""
    
    def __init__(self, obj, engine, adapter, client):
        self._obj = obj
        self._engine = engine
        self._adapter = adapter
        self._client = client
    
    def __getattr__(self, name):
        attr = getattr(self._obj, name)
        
        if name == 'create':
            # This is the interception point!
            return self._make_intercepted_create(attr)
        
        if hasattr(attr, '__call__'):
            return attr
        return _NamespaceProxy(attr, self._engine, self._adapter, self._client)
    
    def _make_intercepted_create(self, original_create):
        def intercepted_create(*args, **kwargs):
            # 1. Pre-process: run messages through pipeline
            # 2. Call original
            # 3. Post-process: store response, update stats
            return self._engine.handle_request(original_create, args, kwargs, self._adapter)
        return intercepted_create
```

**Note:** The `engine.handle_request` method won't exist yet. For now, make it a pass-through that just calls `original_create(*args, **kwargs)` and returns the result. We'll wire in the pipeline in Phase 4.

### StreamAccumulator

For streaming responses (`stream=True`), collects chunks:

```python
class StreamAccumulator:
    """Wraps a streaming response, collects content, then runs post-processing."""
    
    def __init__(self, stream, on_complete):
        self._stream = stream
        self._on_complete = on_complete  # callback(full_text, full_response)
        self._chunks = []
        self._full_text = ""
    
    def __iter__(self):
        for chunk in self._stream:
            self._chunks.append(chunk)
            delta = chunk.choices[0].delta if chunk.choices else None
            if delta and delta.content:
                self._full_text += delta.content
            yield chunk
        # Stream complete — run post-processing
        self._on_complete(self._full_text, self._chunks)
```

### SyntheticResponse

For cache hits, create a fake response that looks like a real OpenAI response:

```python
class SyntheticResponse:
    """Fake response object for cache hits."""
    
    def __init__(self, text, model, cached_tokens):
        self.id = f"ucl-cache-{generate_uuid7()}"
        self.choices = [SyntheticChoice(text)]
        self.model = model
        self.usage = SyntheticUsage(0, cached_tokens, cached_tokens)
        self.created = int(time.time())
```

## 2.4 Tests to Write

```python
# tests/test_providers.py

def test_openai_adapter_normalize():
    """OpenAI messages normalize to NormalizedMessage correctly."""

def test_openai_adapter_denormalize():
    """NormalizedMessages convert back to OpenAI format."""

def test_anthropic_adapter_content_blocks():
    """Anthropic content blocks flatten to plain text."""

def test_anthropic_adapter_system_prompt():
    """Anthropic system prompt is handled correctly."""

def test_provider_registry_detects_openai():
    """Registry identifies OpenAI client."""

def test_provider_registry_unknown_raises():
    """Unknown provider raises ValueError."""

# tests/test_wrapper.py

def test_double_wrap_guard():
    """Wrapping an already-wrapped client doesn't double-wrap."""

def test_none_client_raises():
    """Passing None raises TypeError."""

def test_namespace_proxy_chains():
    """client.chat.completions.create is reachable via proxy."""

def test_stream_accumulator_collects():
    """StreamAccumulator yields all chunks and collects full text."""

def test_synthetic_response_shape():
    """SyntheticResponse has .choices[0].message.content."""
```

## 2.5 Definition of Done

- [ ] `ProviderAdapter` ABC is defined with all abstract methods
- [ ] `OpenAIAdapter` normalizes/denormalizes messages correctly
- [ ] `AnthropicAdapter` handles content blocks and system prompts
- [ ] `ProviderRegistry.detect()` correctly identifies OpenAI and Anthropic clients
- [ ] `WrappedClient` proxies `client.chat.completions.create()` calls through to the real client
- [ ] Double-wrap guard works: `with_context(with_context(client))` doesn't crash
- [ ] None guard works: `with_context(None)` raises `TypeError`
- [ ] `StreamAccumulator` collects full text from streaming chunks
- [ ] `SyntheticResponse` has `.choices[0].message.content` that returns the text
- [ ] All tests pass: `pytest tests/test_providers.py tests/test_wrapper.py -v`

---
---
---

# PHASE 3: EMBEDDING SYSTEM

---

## Context for AI

> **Paste this to your AI assistant when starting Phase 3:**
>
> I'm building UCL, a Python library for LLM context management. I have:
> - Phase 1: SQLite storage layer with CRUD for sessions and context nodes
> - Phase 2: Provider adapters (OpenAI, Anthropic) and a WrappedClient proxy
>
> Now I need Phase 3: the embedding system. This generates vector embeddings for text so we can do semantic similarity search later.
>
> I need:
> 1. EmbeddingProvider ABC — common interface for all embedding providers
> 2. EmbeddingResult dataclass — holds the embedding vector + metadata
> 3. OpenAIEmbeddingProvider — uses OpenAI's text-embedding-3-small (1536 dim)
> 4. SentenceBERTProvider — uses all-MiniLM-L6-v2 locally (384 dim)
> 5. OllamaEmbeddingProvider — uses nomic-embed-text via localhost Ollama (768 dim)
> 6. EmbeddingEngine — main interface with caching and batch support
> 7. BinaryQuantizer — compresses float32 embeddings to 1-bit (32x smaller)
> 8. VectorIndex — similarity search using sqlite-vec (HNSW) with brute-force fallback
>
> All embeddings are numpy float32 arrays. The engine caches embeddings in a dict to avoid re-computing.

---

## 3.1 Goal

Build the embedding generation and vector search system. After this phase, you can embed text, store vectors, and find similar content by cosine similarity.

## 3.2 Files to Create

| File | What It Does |
|------|-------------|
| `src/ucl/embeddings/__init__.py` | Package exports |
| `src/ucl/embeddings/base.py` | `EmbeddingProvider` ABC, `EmbeddingResult` dataclass |
| `src/ucl/embeddings/openai_provider.py` | OpenAI text-embedding-3-small |
| `src/ucl/embeddings/sbert_provider.py` | Local Sentence-BERT |
| `src/ucl/embeddings/ollama_provider.py` | Ollama via HTTP |
| `src/ucl/embeddings/engine.py` | `EmbeddingEngine` with cache + batch |
| `src/ucl/embeddings/quantizer.py` | `BinaryQuantizer` |
| `src/ucl/vector/__init__.py` | Package |
| `src/ucl/vector/index.py` | `VectorIndex` (HNSW + fallback) |
| `tests/test_embeddings.py` | Tests |

## 3.3 Detailed Specifications

### EmbeddingResult

```python
@dataclass
class EmbeddingResult:
    embedding: np.ndarray  # float32 array
    model: str
    dimension: int
    tokens_used: int
    
    def to_binary(self) -> bytes:
        """Binary quantize (1 bit per dim)."""
        return np.packbits(self.embedding > 0).tobytes()
    
    def truncate(self, target_dim: int) -> 'EmbeddingResult':
        """Matryoshka truncation — just slice the first N dims."""
        if target_dim >= self.dimension:
            return self
        return EmbeddingResult(
            embedding=self.embedding[:target_dim],
            model=self.model,
            dimension=target_dim,
            tokens_used=self.tokens_used,
        )
```

### EmbeddingProvider ABC

Properties: `name`, `default_model`, `dimension`, `max_tokens`, `supports_batch`, `supports_matryoshka`
Methods: `embed(text) → EmbeddingResult`, `embed_batch(texts) → List[EmbeddingResult]`

### Provider implementations:

**OpenAIEmbeddingProvider:**
- Uses `openai.OpenAI().embeddings.create(model="text-embedding-3-small", input=text)`
- Supports batch (pass list to `input`)
- Supports Matryoshka (text-embedding-3 models)

**SentenceBERTProvider:**
- Uses `sentence_transformers.SentenceTransformer('all-MiniLM-L6-v2')`
- Call `self._model.encode(text, convert_to_numpy=True)`
- 384 dimensions, 512 max tokens

**OllamaEmbeddingProvider:**
- Uses `urllib.request` to POST to `http://localhost:11434/api/embeddings`
- Payload: `{"model": "nomic-embed-text", "prompt": text}`
- Lazy connection verification (check once, then skip)
- Does NOT support batch (loop and call individually)

### EmbeddingEngine

```python
class EmbeddingEngine:
    def __init__(self, provider, cache_size=10000, target_dimension=None):
        self.provider = provider
        self._cache = {}  # key=md5(text) → EmbeddingResult
        self._cache_size = cache_size
        self.target_dimension = target_dimension
    
    def embed(self, text) -> EmbeddingResult:
        key = md5(text)
        if key in self._cache:
            return self._cache[key]
        result = self.provider.embed(text)
        if self.target_dimension and self.provider.supports_matryoshka:
            result = result.truncate(self.target_dimension)
        self._cache_result(key, result)
        return result
    
    def embed_batch(self, texts) -> List[EmbeddingResult]:
        # Check cache for each, only embed uncached ones
        ...
```

### VectorIndex

```python
class VectorIndex:
    def __init__(self, db, dimension=768):
        # Try to create sqlite-vec virtual table
        # If fails, create fallback regular table
    
    def add(self, node_id, embedding): ...
    def add_batch(self, items): ...
    def search(self, embedding, limit=10) -> List[Tuple[str, float]]: ...
    def remove(self, node_id): ...
```

The search method returns `[(node_id, similarity_score), ...]` sorted by similarity descending.

**Brute-force fallback:** Load all vectors, compute cosine similarity with numpy, sort.

### BinaryQuantizer

```python
class BinaryQuantizer:
    @staticmethod
    def quantize(embedding: np.ndarray) -> bytes:
        return np.packbits(embedding > 0).tobytes()
    
    @staticmethod
    def dequantize(binary: bytes, dimension: int) -> np.ndarray:
        bits = np.unpackbits(np.frombuffer(binary, dtype=np.uint8))
        return bits[:dimension].astype(np.float32) * 2 - 1
    
    @staticmethod
    def hamming_distance(a: bytes, b: bytes) -> int: ...
    
    @staticmethod
    def binary_similarity(a: bytes, b: bytes, dimension: int) -> float: ...
```

## 3.4 Tests to Write

```python
def test_embedding_result_truncate():
    """Matryoshka truncation reduces dimension correctly."""

def test_embedding_result_to_binary():
    """Binary quantization produces correct size (dim/8 bytes)."""

def test_embedding_engine_caches():
    """Same text returns cached result (no second provider call)."""

def test_embedding_engine_batch_partial_cache():
    """Batch with some cached items only embeds uncached ones."""

def test_vector_index_add_and_search():
    """Add vectors, search returns most similar."""

def test_vector_index_brute_force_fallback():
    """Fallback search works when sqlite-vec is not available."""

def test_binary_quantizer_roundtrip():
    """Quantize then dequantize preserves sign of each dimension."""

def test_binary_quantizer_similarity():
    """Identical vectors have similarity 1.0."""

# Skip OpenAI provider test if no API key (use pytest.mark.skipif)
def test_sbert_provider_embed():
    """SentenceBERT returns 384-dim vector."""
```

## 3.5 Definition of Done

- [ ] `EmbeddingProvider` ABC is defined with `embed()` and `embed_batch()`
- [ ] At least one provider works locally (SentenceBERT or mock)
- [ ] `EmbeddingEngine` caches results and avoids duplicate computation
- [ ] `VectorIndex` can add embeddings and search by cosine similarity
- [ ] Brute-force fallback works when sqlite-vec is not installed
- [ ] `BinaryQuantizer` produces 32x smaller representations
- [ ] All tests pass: `pytest tests/test_embeddings.py -v`

---
---
---

# PHASE 4: SCORING, CONTEXT ASSEMBLY & PIPELINE

---

## Context for AI

> **Paste this to your AI assistant when starting Phase 4:**
>
> I'm building UCL, a Python library for LLM context management. I have:
> - Phase 1: SQLite storage (Database, ConnectionPool, SessionRepo, NodeRepo, schema)
> - Phase 2: Provider adapters (OpenAI, Anthropic) + WrappedClient proxy
> - Phase 3: Embedding system (EmbeddingEngine, VectorIndex, BinaryQuantizer)
>
> Now I need Phase 4: the brain of UCL — scoring, context assembly, and the message processing pipeline.
>
> **How context assembly works:**
> Given a token budget (e.g., 32,000) and a user query:
> 1. **Mandatory context** (10%): system prompt + pinned items
> 2. **Sliding window** (20%): last N messages (configurable, default 10)
> 3. **Semantic retrieval** (60%): embed the query, search VectorIndex for similar past context, rank by `similarity × importance_decay`, fill until budget exhausted
> 4. **Reserve** (10%): kept empty for LLM response
>
> **Importance scoring** uses exponential time-decay:
> `score = 0.4 × base_importance + 0.4 × exp(-λt) + 0.2 × log(access_count+1)/5`
> where λ = ln(2) / half_life_hours. Default half_life = 168 hours (7 days).
>
> **The pipeline** is a chain of stages that process messages before they go to the LLM:
> Normalize → Deduplicate → CacheCheck → ContextRetrieval → Assemble
>
> I also need:
> - BloomFilter for fast deduplication (with secondary hash verification)
> - ContentDeduplicator that uses the BloomFilter
> - ProgressiveSummarizer that compresses evicted window messages into a summary
> - TokenBudgetManager that allocates budget across phases

---

## 4.1 Goal

Build the scoring engine, context assembler, and message processing pipeline. After this phase, given messages and a token budget, UCL can assemble optimal context by combining recent messages, semantically relevant past context, and importance-ranked items.

## 4.2 Files to Create

| File | What It Does |
|------|-------------|
| `src/ucl/context/__init__.py` | Package |
| `src/ucl/context/scorer.py` | `ScoringConfig`, `ScoringEngine` |
| `src/ucl/context/assembler.py` | `ContextAssembler`, `AssembledContext`, `AssemblyConfig` |
| `src/ucl/context/budget.py` | `TokenBudgetManager` |
| `src/ucl/context/summarizer.py` | `ProgressiveSummarizer`, `EvictionSummary` |
| `src/ucl/pipeline/__init__.py` | Package |
| `src/ucl/pipeline/stages.py` | `PipelineStage` ABC + all stage implementations |
| `src/ucl/pipeline/pipeline.py` | `MessagePipeline` |
| `src/ucl/cache/__init__.py` | Package |
| `src/ucl/cache/bloom.py` | `BloomFilter`, `ContentDeduplicator` |
| `tests/test_scorer.py` | Scoring tests |
| `tests/test_assembler.py` | Assembly tests |
| `tests/test_pipeline.py` | Pipeline tests |

## 4.3 Detailed Specifications

### ScoringConfig

```python
@dataclass
class ScoringConfig:
    base_weight: float = 0.4
    recency_weight: float = 0.4
    frequency_weight: float = 0.2
    half_life_hours: float = 168.0  # 7 days
    max_frequency_boost: float = 5.0
    pinned_score: float = 1.0
    
    @classmethod
    def chat_preset(cls): return cls(half_life_hours=24.0)
    
    @classmethod
    def coding_preset(cls): return cls(half_life_hours=168.0, base_weight=0.5, recency_weight=0.3, frequency_weight=0.2)
    
    @classmethod
    def research_preset(cls): return cls(half_life_hours=720.0, base_weight=0.3, recency_weight=0.3, frequency_weight=0.4)
    
    @classmethod
    def persistent_preset(cls): return cls(half_life_hours=87600.0, recency_weight=0.1, base_weight=0.5, frequency_weight=0.4)
```

### ScoringEngine

- `compute_importance(node, now_ms) → float` — combines base, recency (exponential decay), frequency (log scaling), returns clamped 0-1
- `rank_nodes(nodes, now_ms) → List[(node, score)]` — sorted descending
- `batch_update_scores(nodes) → List[(node_id, new_score)]` — only returns changed scores (delta > 0.01)

### ContextAssembler

Takes: `session_id, query, total_budget, system_prompt`
Returns: `AssembledContext` with lists of pinned, window, and retrieved nodes.

4 phases:
1. Mandatory: system prompt + pinned items
2. Sliding window: last N messages, evicted ones go to summarizer
3. Progressive summarization: compress evicted window nodes into summary
4. Semantic retrieval: embed query → VectorIndex.search → score by importance × similarity → fill budget

### BloomFilter

```python
class BloomFilter:
    def __init__(self, expected_items=100000, false_positive_rate=0.01):
        # Calculate optimal size: m = -n * ln(p) / (ln(2)^2)
        # Calculate optimal hash count: k = (m/n) * ln(2)
    
    def add(self, item: str): ...
    def contains(self, item: str) -> bool: ...
```

Uses `mmh3` (MurmurHash3) for hashing. **Install dependency**: add `mmh3>=4.0` to pyproject.toml.

### ContentDeduplicator

Two-stage dedup:
1. Bloom filter (fast, may have false positives)
2. Exact hash set verification (confirms Bloom positives)

```python
class ContentDeduplicator:
    def is_duplicate(self, content: str) -> bool:
        hash = sha256(normalize(content))
        if not self.bloom.contains(hash):
            return False  # Definitely not duplicate
        return hash in self._hash_store  # Confirm with exact set
    
    def add(self, content: str): ...
    def check_and_add(self, content: str) -> bool: ...  # True if new
```

### Pipeline Stages

Each stage: `process(ctx: PipelineContext) → PipelineContext`

**PipelineContext** dataclass holds:
- `original_messages`, `normalized_messages`
- `token_budget`, `query_embedding`
- `cache_hit`, `cached_response`
- `retrieved_context`

**NormalizeStage:** Convert raw messages to `NormalizedMessage`. Guards: skip empty messages, truncate messages > 100KB.

**DeduplicateStage:** Check content against BloomFilter + HashStore. Drop exact duplicates.

**CacheCheckStage:** Tiered lookup (L1 hash → L2 simhash → L3 semantic). Only compute embedding on L3 miss. If cache hit, set `ctx.cache_hit = True`.

**ContextRetrievalStage:** If no cache hit, use `ctx.query_embedding` to search VectorIndex. Score candidates with ScoringEngine. Fill budget.

**AssembleStage:** Build final message array: system → retrieved context → recent conversation.

**MessagePipeline:** Chain stages, short-circuit on cache hit.

## 4.4 Tests to Write

```python
# tests/test_scorer.py
def test_pinned_always_max_score(): ...
def test_recency_decays_over_time(): ...
def test_half_life_at_168_hours(): ...
def test_frequency_scales_logarithmically(): ...

# tests/test_assembler.py
def test_mandatory_context_always_included(): ...
def test_sliding_window_takes_recent_n(): ...
def test_semantic_retrieval_fills_budget(): ...
def test_never_exceeds_budget(): ...

# tests/test_pipeline.py
def test_normalize_stage_filters_empty(): ...
def test_dedup_stage_drops_duplicates(): ...
def test_pipeline_short_circuits_on_cache_hit(): ...
def test_full_pipeline_produces_messages(): ...

# tests/test_bloom.py (or within test_pipeline.py)
def test_bloom_no_false_negatives(): ...
def test_content_deduplicator_two_stage(): ...
```

## 4.5 Definition of Done

- [ ] `ScoringEngine.compute_importance()` returns correct decay curve (test at 0h, 24h, 168h, 720h)
- [ ] All 4 presets (chat, coding, research, persistent) are correct
- [ ] `ContextAssembler.assemble()` returns an `AssembledContext` that never exceeds budget
- [ ] Sliding window includes last N messages
- [ ] Semantic retrieval finds relevant past context
- [ ] `BloomFilter` has zero false negatives
- [ ] `ContentDeduplicator` catches duplicates and handles false positives
- [ ] Pipeline stages chain correctly: Normalize → Deduplicate → CacheCheck → Retrieve → Assemble
- [ ] Pipeline short-circuits on cache hit
- [ ] All tests pass

---
---
---

# PHASE 5: CACHING & TOPIC SYSTEM

---

## Context for AI

> **Paste this to your AI assistant when starting Phase 5:**
>
> I'm building UCL, a Python library for LLM context management. I have:
> - Phase 1: SQLite storage layer
> - Phase 2: Provider adapters + WrappedClient proxy
> - Phase 3: Embedding system (EmbeddingEngine, VectorIndex)
> - Phase 4: Scoring engine, context assembler, message pipeline, BloomFilter
>
> Now I need Phase 5: the caching system and topic detection.
>
> **Semantic Cache (3-tier):**
> - L1: Exact hash match (SHA-256 of normalized query) — O(1), no embedding needed
> - L2: Fuzzy hash match via SimHash (catches typos/whitespace diffs) — O(1), no embedding needed
> - L3: Semantic similarity via embeddings (cosine ≥ 0.95) — O(log n), only for temperature ≤ 0.01
>
> Short-circuits on first hit (L1 → L2 → L3).
>
> **SimHash:** A locality-sensitive hash where similar text produces similar hash values. Uses character 3-grams as shingles. Hamming distance ≤ 3 = likely same query.
>
> **Topic Detection:** Automatically groups messages into topics based on:
> - Explicit transition phrases ("now let's", "moving on to", "switching to")
> - Semantic shift detection (cosine similarity < 0.6 with previous message)
> - Centroid-based classification (compare message embedding to existing topic centroids)
>
> Topic management allows users to keep/discard/merge topics to control context.

---

## 5.1 Goal

Build the semantic caching system (saves money by returning cached responses) and the topic detection/management system (organizes context into browseable topics).

## 5.2 Files to Create

| File | What It Does |
|------|-------------|
| `src/ucl/cache/simhash.py` | `SimHasher` — locality-sensitive 64-bit hash |
| `src/ucl/cache/semantic.py` | `SemanticCache` — 3-tier cache (L1/L2/L3) |
| `src/ucl/cache/fingerprint.py` | `ContextFingerprinter` — hash context state |
| `src/ucl/storage/cache_repo.py` | `ResponseCacheRepository` — DB CRUD for cache |
| `src/ucl/topics/__init__.py` | Package |
| `src/ucl/topics/detector.py` | `TopicDetector`, `TopicConfig`, `TopicAssignment` |
| `src/ucl/topics/manager.py` | `TopicBranchManager`, operations |
| `src/ucl/storage/topic_repo.py` | `TopicRepository` — CRUD for topic_branches |
| `tests/test_cache.py` | Cache tests |
| `tests/test_topics.py` | Topic tests |

## 5.3 Detailed Specifications

### SimHasher

```python
class SimHasher:
    BIT_WIDTH = 64
    
    def compute(self, text: str) -> int:
        """Returns a 64-bit integer fingerprint."""
        # 1. Normalize (lowercase, strip)
        # 2. Tokenize into character 3-grams
        # 3. Hash each 3-gram to 64-bit int (md5, take first 8 bytes)
        # 4. For each bit position: if hash bit=1 add 1, else subtract 1
        # 5. Final fingerprint: bit=1 if sum>0
    
    def distance(self, hash_a: int, hash_b: int) -> int:
        """Hamming distance = number of differing bits."""
        return bin(hash_a ^ hash_b).count('1')
```

### SemanticCache

```python
class SemanticCache:
    DETERMINISTIC_TEMPERATURE_THRESHOLD = 0.01
    
    def get(self, query, context_hash, model, temperature) -> Optional[CachedResponse]:
        # L1: Exact hash match
        query_hash = sha256(query.lower().strip())
        exact = self.cache_repo.find_exact(query_hash, model)
        if exact and not exact.is_expired():
            return exact
        
        # L2: SimHash fuzzy match
        query_simhash = self._simhash.compute(query)
        fuzzy = self.cache_repo.find_by_simhash(query_simhash, model, max_distance=3)
        if fuzzy and not fuzzy.is_expired():
            return fuzzy
        
        # L3: Semantic (only if temperature ≤ 0.01)
        if temperature > self.DETERMINISTIC_TEMPERATURE_THRESHOLD:
            return None
        query_embedding = self.embedder.embed(query).embedding
        similar = self.vector_index.search(query_embedding, limit=5)
        for node_id, similarity in similar:
            if similarity >= 0.95:
                cached = self.cache_repo.get_by_id(node_id)
                if cached and cached.model == model and not cached.is_expired():
                    return cached
        return None
    
    def put(self, query, response, context_hash, model, temperature, response_tokens):
        # Store with all lookup keys (hash, simhash, embedding)
```

### TopicDetector

```python
class TopicDetector:
    def detect_topic(self, content, session_id, previous_content=None, previous_topic_id=None) -> TopicAssignment:
        # 1. Check for explicit transition phrases (regex list)
        # 2. Embed content
        # 3. Check semantic shift from previous (cosine < 0.6)
        # 4. Find best matching existing topic (centroid similarity)
        # 5. Decision:
        #    - Strong match (≥0.7) → assign to existing topic
        #    - Transition/shift detected + no decent match → create new topic
        #    - No signals → continue previous topic
```

Transition phrase regexes:
```python
[r"^now let'?s", r"^moving on to", r"^next[,:]", r"^switching to",
 r"^let'?s focus on", r"^regarding", r"^about the", r"^for the",
 r"^can we work on", r"^i want to", r"^let'?s implement", r"^time to"]
```

### TopicBranchManager

Methods:
- `list_topics(session_id) → List[TopicSummary]`
- `keep_topics(session_id, topic_ids) → ContinuationResult` — archive all others
- `discard_topics(session_id, topic_ids) → ContinuationResult`
- `fork_from_topic(session_id, topic_id) → TopicBranch`
- `merge_topics(session_id, source_id, target_id) → TopicBranch`

## 5.4 Tests to Write

```python
# tests/test_cache.py
def test_simhash_similar_text_close_distance(): ...
def test_simhash_different_text_far_distance(): ...
def test_cache_l1_exact_hit(): ...
def test_cache_l2_fuzzy_hit(): ...
def test_cache_l3_semantic_skipped_high_temperature(): ...
def test_cache_expiry(): ...
def test_cache_put_and_get_roundtrip(): ...

# tests/test_topics.py
def test_transition_phrase_detected(): ...
def test_semantic_shift_detected(): ...
def test_topic_matches_existing_centroid(): ...
def test_new_topic_created_on_shift(): ...
def test_keep_topics_archives_others(): ...
def test_merge_topics(): ...
```

## 5.5 Definition of Done

- [ ] `SimHasher` produces similar hashes for similar text (Hamming distance ≤ 3)
- [ ] `SimHasher` produces distant hashes for different text (Hamming distance > 10)
- [ ] `SemanticCache.get()` returns L1 hit for exact query match
- [ ] `SemanticCache.get()` returns L2 hit for minor query variation
- [ ] `SemanticCache.get()` returns None for high temperature (> 0.01)
- [ ] `SemanticCache.put()` stores and `get()` retrieves correctly
- [ ] Expired cache entries are not returned
- [ ] `TopicDetector` catches explicit transition phrases
- [ ] `TopicDetector` detects semantic shifts (cosine < 0.6)
- [ ] `TopicBranchManager.keep_topics()` archives unselected topics
- [ ] All tests pass

---
---
---

# PHASE 6: PUBLIC API, ENGINE & CLI

---

## Context for AI

> **Paste this to your AI assistant when starting Phase 6:**
>
> I'm building UCL, a Python library for LLM context management. I have all the core pieces:
> - Storage layer (SQLite, sessions, nodes)
> - Provider adapters (OpenAI, Anthropic) + WrappedClient proxy
> - Embedding system (providers, engine, vector index)
> - Scoring engine + context assembler + message pipeline
> - Semantic cache (3-tier) + topic detection/management
>
> Now I need Phase 6: wire everything together and build the public API.
>
> **The ContextEngine** is the central orchestrator that:
> - Initializes all components (database, embeddings, cache, topics, pipeline)
> - Handles the `handle_request()` method called by WrappedClient
> - Manages the full lifecycle: intercept → pipeline → LLM call → store → return
>
> **Public API:**
> - `with_context(client, config=None, session=None)` — one-line wrapper
> - `client.ucl.session` — session management (list topics, keep/discard, stats)
> - `client.ucl.context` — direct context operations (add, search, add_file)
> - `client.ucl.cost_report()` — cost savings report
>
> **CLI** (using Click):
> - `ucl sessions` — list all sessions
> - `ucl topics <session_id>` — list topics
> - `ucl search <session_id> <query>` — search context
> - `ucl export <session_id> <output> --format json|md` — export session
> - `ucl stats` — global statistics
>
> **Debug/Observability:**
> - `UCLDebugLogger` — stores last N debug log entries when `debug=True`
> - `CostTracker` — tracks token usage and calculates cost savings from caching
>
> **BackgroundExecutor** — thread-based workers for:
> - Batch embedding generation (every 5 items or 1 second)
> - Topic detection (every 10 messages)
> - WAL checkpointing (every 5 minutes)

---

## 6.1 Goal

Wire all components together into the `ContextEngine` orchestrator, build the public API (`with_context()`), CLI, and debug tools. After this phase, UCL is a working library that can be pip-installed and used.

## 6.2 Files to Create

| File | What It Does |
|------|-------------|
| `src/ucl/engine.py` | `ContextEngine` — the orchestrator |
| `src/ucl/__init__.py` | Public API: `with_context`, `UCLConfig`, version |
| `src/ucl/debug.py` | `UCLDebugLogger`, `CostTracker` |
| `src/ucl/background.py` | `BackgroundExecutor` — worker threads |
| `src/ucl/cli/main.py` | Click CLI commands |
| `src/ucl/export/json_export.py` | JSON exporter |
| `src/ucl/export/markdown_export.py` | Markdown exporter |
| `tests/test_e2e.py` | End-to-end integration tests |

## 6.3 Detailed Specifications

### ContextEngine

```python
class ContextEngine:
    """Central orchestrator — connects all components."""
    
    def __init__(self, config: UCLConfig, session_id: Optional[str] = None):
        # Initialize storage
        self.db = Database(config.data_dir / 'ucl.db')
        self.pool = ConnectionPool(config.data_dir / 'ucl.db')
        initialize_schema(self.db.connect())
        
        # Initialize repos
        self.session_repo = SessionRepository(self.db)
        self.node_repo = ContextNodeRepository(self.db, ...)
        self.cache_repo = ResponseCacheRepository(self.db)
        self.topic_repo = TopicRepository(self.db)
        
        # Initialize or resume session
        if session_id:
            self.session = self.session_repo.get(session_id)
        else:
            self.session = self.session_repo.create(...)
        
        # Initialize embedding engine (based on config)
        self.embedder = self._create_embedding_engine(config)
        
        # Initialize vector index
        self.vector_index = VectorIndex(self.db, dimension=self.embedder.provider.dimension)
        
        # Initialize components
        self.scorer = ScoringEngine(ScoringConfig.from_preset(config.scoring_preset))
        self.assembler = ContextAssembler(...)
        self.cache = SemanticCache(...)
        self.topic_detector = TopicDetector(...)
        self.topic_manager = TopicBranchManager(...)
        
        # Build pipeline
        self.pipeline = MessagePipeline([
            NormalizeStage(),
            DeduplicateStage(ContentDeduplicator()),
            CacheCheckStage(self.cache, self.embedder),
            ContextRetrievalStage(self.vector_index, self.scorer, config),
            AssembleStage(),
        ])
        
        # Debug/cost
        self.debug_logger = UCLDebugLogger(enabled=config.debug)
        self.cost_tracker = CostTracker()
        
        # Background workers
        self.background = BackgroundExecutor()
        self.background.start()
    
    def handle_request(self, original_create, args, kwargs, adapter):
        """Called by WrappedClient when .create() is intercepted."""
        messages = kwargs.get('messages', [])
        model = kwargs.get('model', 'unknown')
        stream = kwargs.get('stream', False)
        temperature = kwargs.get('temperature', 1.0)
        
        # Get token budget
        context_limit = adapter.get_context_limit(model)
        budget = int(context_limit * (1 - self.config.context_reserve_ratio))
        
        # Run pipeline
        processed_messages, ctx = self.pipeline.process(messages, budget)
        
        # Cache hit?
        if ctx.cache_hit:
            self.debug_logger.log("cache_hit", query=messages[-1].get('content', ''))
            self.cost_tracker.record_cache_hit(ctx.cached_response.response_tokens, model)
            return SyntheticResponse(ctx.cached_response.response_text, model, ctx.cached_response.response_tokens)
        
        # Replace messages with processed ones
        kwargs['messages'] = processed_messages
        
        # Call original LLM
        if stream:
            response = original_create(*args, **kwargs)
            return StreamAccumulator(response, lambda text, chunks: self._post_process(text, messages, model, temperature))
        else:
            response = original_create(*args, **kwargs)
            response_text = adapter.extract_response_text(response)
            usage = adapter.extract_usage(response)
            self._post_process(response_text, messages, model, temperature, usage)
            return response
    
    def _post_process(self, response_text, original_messages, model, temperature, usage=None):
        """Store response, update cache, detect topic."""
        # Store user message + assistant response as context nodes
        user_content = original_messages[-1].get('content', '') if original_messages else ''
        self.node_repo.create(content=user_content, type='user_message', session_id=self.session.id, branch_id=self.current_branch)
        self.node_repo.create(content=response_text, type='assistant_message', session_id=self.session.id, branch_id=self.current_branch)
        
        # Queue background embedding
        self.background.queue_embedding(...)
        
        # Cache the response
        if self.config.enable_cache:
            self.cache.put(query=user_content, response=response_text, ...)
        
        # Topic detection
        if self.config.enable_topics:
            self.background.queue_topic_detection(self.session.id)
        
        # Cost tracking
        if usage:
            self.cost_tracker.record_request(model, usage.get('prompt_tokens', 0), usage.get('completion_tokens', 0))
```

### Public `__init__.py`

```python
from ucl.config import UCLConfig
from ucl.wrapper import WrappedClient
from ucl.engine import ContextEngine

__version__ = "0.1.0"

def with_context(client, config=None, session=None):
    config = config or UCLConfig.auto_detect()
    engine = ContextEngine(config, session_id=session)
    return WrappedClient(client, engine)
```

### UCLDebugLogger

```python
class UCLDebugLogger:
    def __init__(self, enabled=False, max_entries=1000):
        self._enabled = enabled
        self._entries = []
        self._max = max_entries
    
    def log(self, event, **data):
        if not self._enabled:
            return
        self._entries.append({"time": time.time(), "event": event, **data})
        if len(self._entries) > self._max:
            self._entries.pop(0)
    
    @property
    def entries(self):
        return list(self._entries)
```

### CostTracker

```python
class CostTracker:
    # Pricing per 1M tokens (approx, as of 2024)
    PRICING = {
        'gpt-4o': {'input': 2.50, 'output': 10.00},
        'gpt-4o-mini': {'input': 0.15, 'output': 0.60},
        'claude-3-5-sonnet': {'input': 3.00, 'output': 15.00},
    }
    
    def __init__(self):
        self.total_tokens_in = 0
        self.total_tokens_out = 0
        self.tokens_saved_by_cache = 0
        self.requests = 0
        self.cache_hits = 0
    
    def record_request(self, model, tokens_in, tokens_out): ...
    def record_cache_hit(self, tokens_saved, model): ...
    def cost_report(self) -> str: ...
```

### CLI (Click)

```python
import click

@click.group()
@click.option('--data-dir', default='~/.ucl')
@click.pass_context
def cli(ctx, data_dir):
    """Universal Context Layer CLI."""
    ctx.obj = {'data_dir': Path(data_dir).expanduser()}

@cli.command()
def sessions(ctx): ...

@cli.command()
def topics(ctx, session_id): ...

@cli.command()
def search(ctx, session_id, query): ...

@cli.command()
def export(ctx, session_id, output, format): ...

@cli.command()
def stats(ctx): ...
```

Add `click>=8.0` to pyproject.toml dependencies.

## 6.4 Tests to Write

```python
# tests/test_e2e.py

def test_with_context_creates_wrapped_client():
    """with_context(MockClient()) returns a working wrapper."""

def test_full_roundtrip_no_llm():
    """Messages go through pipeline, get stored, no actual LLM call (mocked)."""

def test_cache_hit_returns_synthetic():
    """Second identical call returns SyntheticResponse."""

def test_cost_tracker_records():
    """CostTracker accumulates token counts."""

def test_debug_logger_when_enabled():
    """Events are logged when debug=True."""

def test_debug_logger_silent_when_disabled():
    """No entries when debug=False."""
```

## 6.5 Definition of Done

- [ ] `from ucl import with_context, UCLConfig` works
- [ ] `with_context(mock_openai_client)` returns a working wrapper
- [ ] Full request lifecycle works: intercept → pipeline → (mock) LLM call → store → return
- [ ] Cache hit on second identical call returns `SyntheticResponse`
- [ ] `CostTracker` reports tokens used and saved
- [ ] `UCLDebugLogger` captures events when `debug=True`
- [ ] CLI: `ucl sessions` lists stored sessions
- [ ] CLI: `ucl stats` shows global stats
- [ ] JSON and Markdown export work
- [ ] All tests pass

---
---
---

# PHASE 7: ADVANCED FEATURES (FUTURE)

---

## Context for AI

> **Paste this to your AI assistant when starting Phase 7:**
>
> I'm building UCL, a Python library for LLM context management. The core library is complete (Phases 1-6). Now I want to add advanced memory features for a v2.0 release.
>
> These are optional enhancements that build on the existing foundation:
> 1. **Code Understanding** — Parse Python files with tree-sitter, extract symbols (functions, classes), build dependency graph, rank by PageRank
> 2. **Knowledge Graph** — Extract entities and relationships from conversation, store in SQLite, enable multi-hop queries
> 3. **Fact Extraction** — Extract atomic facts from conversation ("User prefers dark mode"), deduplicate, supersede outdated facts
> 4. **Memory Consolidation** — Cluster similar old memories, summarize clusters into consolidated memories
> 5. **Cross-Session Memory** — Share relevant context between sessions (user-level, project-level)
> 6. **MCP Server** — Expose UCL as a Model Context Protocol server
>
> All of these are independent features that can be implemented in any order.

---

## 7.1 Feature: Code Understanding

**Files:** `src/ucl/code/parser.py`, `src/ucl/code/ranking.py`

**What it does:**
- Uses `tree-sitter` + `tree-sitter-python` to parse Python files
- Extracts functions, classes, methods with signatures and docstrings
- Builds a dependency graph (calls, imports, inherits edges)
- Runs PageRank on the graph to find the most "important" symbols
- Important symbols get higher priority in context assembly

**Dependencies:** `tree-sitter>=0.21`, `tree-sitter-python>=0.21`

**Key classes:** `TreeSitterParser`, `DependencyExtractor`, `PageRank`, `CodeAnalyzer`

## 7.2 Feature: Knowledge Graph

**Files:** `src/ucl/memory/knowledge_graph.py`, `src/ucl/memory/entity_extractor.py`

**What it does:**
- Extracts entities (Person, Code, Library, Concept) and relationships from messages
- Uses LLM for extraction (structured JSON output)
- Stores in SQLite tables (`kg_entities`, `kg_relationships`)
- Enables multi-hop graph traversal queries

## 7.3 Feature: Fact Extraction

**Files:** `src/ucl/memory/facts.py`

**What it does:**
- Extracts atomic facts from conversation ("User prefers Python 3.11")
- Deduplicates against existing facts (LLM-based check)
- Facts can supersede/invalidate older ones
- Facts have optional expiry (`valid_until`)

## 7.4 Feature: Memory Consolidation

**Files:** `src/ucl/memory/consolidator.py`

**What it does:**
- Finds clusters of similar cold-tier memories (cosine > 0.85)
- Summarizes each cluster into a single consolidated memory
- Reduces storage and improves retrieval quality

## 7.5 Feature: Cross-Session Memory

**Files:** `src/ucl/memory/cross_session.py`

**What it does:**
- Promote important memories to shared scope (user/project/global)
- Inject relevant shared memories into new sessions
- Enables persistent user preferences across all conversations

## 7.6 Feature: MCP Server

**Files:** `src/ucl/mcp/server.py`

**What it does:**
- Exposes UCL as a Model Context Protocol server
- Tools: `ucl_search`, `ucl_list_topics`, `ucl_keep_topics`, `ucl_add_files`, `ucl_get_stats`
- Resources: `ucl://session/current`, `ucl://context/assembled`, `ucl://topics/summary`

---
---
---

# APPENDIX A: DEVELOPMENT TIPS

## Working with AI Assistants

When asking your AI assistant for help with a specific piece:

1. **Always provide file context:** "Here is my current `scorer.py`: [paste file]. I need to add the `research_preset` classmethod."

2. **Reference the phase doc:** "According to Phase 4, the ScoringEngine should compute importance as `0.4 × base + 0.4 × exp(-λt) + 0.2 × log(access+1)/5`. Can you implement this?"

3. **Ask for tests first:** "Write pytest tests for `BloomFilter.contains()` — it should have zero false negatives."

4. **Break down big files:** If a file has many classes, ask for one class at a time. "Implement just the `NormalizeStage` class first."

5. **Verify incrementally:** Run tests after each file. Don't write 5 files then test.

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| SQLite "database is locked" | Use ConnectionPool with write lock. WAL mode allows concurrent reads. |
| Embeddings are slow | Use EmbeddingEngine cache. Batch embeddings. Don't embed on the hot path. |
| Token count is inaccurate | Use tiktoken for OpenAI. For Anthropic, use `len(text) / 3.5`. |
| Tests need API keys | Mock the providers. Only test real API calls in integration tests with `@pytest.mark.skipif`. |
| `__getattr__` infinite recursion | In WrappedClient, store all internal state in `self.__dict__` directly, not via setattr. |
| Bloom filter false positives | Always verify with secondary hash store (ContentDeduplicator pattern). |
| numpy not installed | Add to pyproject.toml dependencies. |

## Dependency Install Order

```bash
# Core (Phase 1)
pip install -e ".[dev]"

# Phase 2 (if testing with real providers)
pip install -e ".[openai,anthropic]"

# Phase 3 (local embeddings)
pip install -e ".[local]"

# Phase 5 (bloom filter hashing)
pip install mmh3

# Phase 6 (CLI)
pip install click

# Phase 7 (code analysis)
pip install tree-sitter tree-sitter-python
```

## Quick Test Commands

```bash
# Run all tests
pytest tests/ -v

# Run specific phase
pytest tests/test_storage.py -v          # Phase 1
pytest tests/test_providers.py tests/test_wrapper.py -v  # Phase 2
pytest tests/test_embeddings.py -v       # Phase 3
pytest tests/test_scorer.py tests/test_assembler.py tests/test_pipeline.py -v  # Phase 4
pytest tests/test_cache.py tests/test_topics.py -v       # Phase 5
pytest tests/test_e2e.py -v              # Phase 6

# Run with coverage
pytest tests/ --cov=ucl --cov-report=term-missing
```

---

# APPENDIX B: KEY ALGORITHMS REFERENCE

## Exponential Decay

```
decay(t) = exp(-λ × t)
λ = ln(2) / half_life_hours
```

| Half-life | 1h later | 24h later | 7d later | 30d later |
|-----------|----------|-----------|----------|-----------|
| 24h (chat) | 0.97 | 0.50 | 0.008 | ~0 |
| 168h (coding) | 0.996 | 0.90 | 0.50 | 0.08 |
| 720h (research) | 0.999 | 0.98 | 0.86 | 0.50 |

## Cosine Similarity

```python
similarity = dot(a, b) / (norm(a) * norm(b))
# Range: -1 to 1. For normalized embeddings: 0 to 1.
```

## SimHash Hamming Distance

```python
distance = bin(hash_a ^ hash_b).count('1')
# 0 = identical, 1-3 = very similar, 10+ = different
```

## LZ4 Compression

```python
import lz4.frame
compressed = lz4.frame.compress(text.encode())
decompressed = lz4.frame.decompress(compressed).decode()
```

## UUID v7 (Time-Sortable)

```python
timestamp_ms = int(time.time() * 1000)
random_bits = random.getrandbits(74)
uuid_int = (timestamp_ms << 80) | (0x7 << 76) | random_bits
uuid_str = format(uuid_int, '032x')
```

---

*End of UCL Implementation Plan*
*Document Version: 1.0.0*
*Covers: 6 implementation phases + 1 future phase*
*Estimated timeline: 12-16 weeks at part-time pace*
