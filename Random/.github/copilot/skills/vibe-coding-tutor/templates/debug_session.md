# Debug Session: {Error Summary}

**Session ID:** {YYYYMMDD_HHMMSS}
**Started:** {YYYY-MM-DD HH:MM:SS}
**Status:** OPEN
**Current Phase:** root_cause
**Fixes Attempted:** 0/3

---

## Error Details

```
{Full error message - copy the complete output}
```

## Stack Trace

```
{Full stack trace if available}
```

---

## Phase 1: Root Cause Investigation

> [!IMPORTANT]
> Complete ALL items before proposing any fix. No fixes without root cause.

- [ ] Read error message completely (don't skim)
- [ ] Reproduce consistently (exact steps)
- [ ] Check recent changes (`git diff`, `git log -5`)
- [ ] Trace data flow (where does bad value originate?)

**Reproduction Steps:**
1. {Exact step to reproduce}
2. {Next step}
3. {Expected vs actual behavior}

**Recent Changes:**
```bash
# Output of git diff or relevant changes
```

**Data Flow Trace:**
- Value originates at: {file:line}
- Passed through: {file:line} → {file:line}
- Error occurs at: {file:line}

**Initial Hypothesis:** {Theory about root cause - be specific}

---

## Phase 2: Pattern Analysis

- [ ] Find a working example of similar code
- [ ] Compare working vs broken
- [ ] List all differences (no matter how small)

**Working Example Found:** {yes/no}
**Location:** {file:line or "N/A"}

**Differences Identified:**
| Working | Broken |
|---------|--------|
| {aspect} | {different aspect} |

---

## Phase 3: Hypothesis Testing

> [!IMPORTANT]
> Test ONE hypothesis at a time. Don't stack changes.

| # | Hypothesis | Test Performed | Result |
|---|------------|----------------|--------|
| 1 | {Specific theory} | {How you tested it} | pending |

**Current Hypothesis:** {The theory you're testing now}

**Minimal Test:** {The smallest change to prove/disprove}

---

## Phase 4: Implementation

> [!IMPORTANT]
> Only proceed here AFTER root cause is identified.

- [ ] Create failing test reproducing the bug
- [ ] Implement SINGLE fix addressing root cause
- [ ] Verify fix (test passes)
- [ ] Verify no regression (all other tests pass)
- [ ] Commit with descriptive message

**Root Cause Identified:** {yes/no}
**Root Cause Description:** {What actually caused the bug}

**Failing Test:**
```{language}
def test_reproduces_bug():
    """This test reproduces the bug."""
    # Test that fails without fix, passes with fix
    pass
```

**Fix Applied:** {Description of the fix}

**Verification:**
```bash
# Output showing test now passes
```

**Tests Passing:** {yes/no - show evidence}

---

## ⚠️ Escalation Check

**Fixes Attempted:** {count}/3

> [!CAUTION]
> If 3+ fixes have failed, STOP.
>
> **Ask yourself:**
> - Is this pattern fundamentally sound?
> - Are we sticking with it through sheer inertia?
> - Should we refactor vs continue fixing symptoms?
>
> **Discuss architecture before attempting more fixes.**

---

## Session Log

| Timestamp | Event | Notes |
|-----------|-------|-------|
| {HH:MM} | Session started | {Initial error} |
| {HH:MM} | {Event} | {Notes} |

---

## Resolution

**Status:** {OPEN / RESOLVED}
**Resolution:** {How it was fixed}
**Time Spent:** {Duration}
**Lessons Learned:** {What to remember for next time}
</Parameter>
<parameter name="Complexity">4
