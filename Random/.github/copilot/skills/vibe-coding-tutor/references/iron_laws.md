# Iron Laws

These rules are NON-NEGOTIABLE. Violating the letter is violating the spirit.

---

## 1. The TDD Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

Write code before test? **Delete it. Start over.**

**No exceptions:**
- Don't keep it as "reference"
- Don't "adapt" it while writing tests
- Don't look at it
- Delete means delete

**Red Flags - STOP and restart with TDD:**
- Code before test
- Test after implementation
- Test passes immediately (not failing first)
- Rationalizing "just this once"
- "I already manually tested it"
- "Tests after achieve the same purpose"

---

## 2. The Debugging Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

If you haven't completed Phase 1 (Root Cause Investigation), you cannot propose fixes.

**The Four Phases:**
1. **Root Cause Investigation** - Read error, reproduce, trace data flow
2. **Pattern Analysis** - Find working example, compare differences
3. **Hypothesis Testing** - Single theory, minimal test
4. **Implementation** - Failing test → fix → verify

**Red Flags - STOP and investigate:**
- "Quick fix for now, investigate later"
- "Just try changing X and see"
- "I don't fully understand but this might work"
- Proposing solutions before tracing data flow
- "One more fix attempt" (when already tried 2+)

**Escalation Rule:** If 3+ fixes have failed, STOP and question the architecture.

---

## 3. The Verification Iron Law

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

If you haven't run the verification command in this message, you cannot claim it passes.

**Never say:**
- "Should work now"
- "Probably passes"
- "I'm confident"
- "Looks correct"

**Always say:**
- "Running tests... [actual output] All 5 tests pass."

**The Gate Function:**
1. IDENTIFY: What command proves this claim?
2. RUN: Execute the FULL command (fresh, complete)
3. READ: Full output, check exit code, count failures
4. VERIFY: Does output confirm the claim?
5. ONLY THEN: Make the claim

---

## 4. The Vibe Check Iron Law

```
NEVER WRITE FINAL CODE BEFORE ASKING AND CONFIRMING DESIGN QUESTIONS
```

This is the original law from V1. Still applies.

**The Vibe Check Protocol requires:**
- `findings.md` has ≥2 resolved design decisions
- `progress.md` has ≥2 answered MCQs
- User has explicitly confirmed the summary

---

## Quick Reference

| Iron Law | Trigger | Consequence |
|:---|:---|:---|
| TDD | About to write code | Write test first, watch it fail |
| Debugging | Test fails | Complete Phase 1 before fixing |
| Verification | About to claim success | Run command, show output |
| Vibe Check | New code request | Ask MCQs, get confirmation |
