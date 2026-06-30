# Rationalization Prevention Tables

Use these tables to counter common excuses. When you catch yourself thinking any of these, STOP and follow the process.

---

## TDD Rationalizations

| Excuse | Reality |
|--------|---------|
| "Too simple to test" | Simple code breaks. Test takes 30 seconds. |
| "I'll test after" | Tests passing immediately prove nothing. |
| "Tests after achieve same goals" | Tests-after = "what does this do?" Tests-first = "what should this do?" |
| "Already manually tested" | Ad-hoc ≠ systematic. No record, can't re-run. |
| "Deleting X hours is wasteful" | Sunk cost fallacy. Keeping unverified code is technical debt. |
| "Keep as reference" | You'll adapt it. That's testing after. Delete means delete. |
| "Need to explore first" | Fine. Throw away exploration, start with TDD. |
| "TDD will slow me down" | TDD faster than debugging. Pragmatic = test-first. |
| "Test hard = design unclear" | Listen to test. Hard to test = hard to use. |
| "Manual test faster" | Manual doesn't prove edge cases. You'll re-test every change. |
| "Existing code has no tests" | You're improving it. Add tests for existing code first. |

---

## Debugging Rationalizations

| Excuse | Reality |
|--------|---------|
| "Issue is simple" | Simple issues have root causes too. Process applies. |
| "Emergency, no time" | Systematic debugging is FASTER than guess-and-check thrashing. |
| "Just try this first" | First fix sets the pattern. Do it right from the start. |
| "One more fix attempt" | 3+ failures = architectural problem. Stop and question approach. |
| "I see the problem" | Seeing symptoms ≠ understanding root cause. Trace first. |
| "Pattern says X but I'll adapt" | Partial understanding guarantees bugs. Follow completely. |
| "Add multiple changes, run tests" | Can't isolate what worked. One change at a time. |
| "Skip the test, manually verify" | No record of what was tested. Write automated test. |

---

## Verification Rationalizations

| Excuse | Reality |
|--------|---------|
| "Should work now" | RUN the verification command. |
| "I'm confident" | Confidence ≠ evidence. |
| "Just this once" | No exceptions for verification. |
| "Partial check is enough" | Partial proves nothing. Run full suite. |
| "Linter passed" | Linter ≠ compiler ≠ tests. Different checks. |
| "Agent said success" | Verify independently. Don't trust reports. |
| "I'm tired" | Exhaustion ≠ excuse. Verify anyway. |
| "Different words so rule doesn't apply" | Spirit over letter. If claiming success, verify. |

---

## Vibe Check Rationalizations

| Excuse | Reality |
|--------|---------|
| "User wants it fast" | Fast and wrong wastes more time. Ask first. |
| "It's obvious what they want" | Your assumptions ≠ their requirements. Confirm. |
| "Just this simple function" | Even simple functions have design decisions. |
| "I'll ask after if needed" | Asking after = fixing after. Ask before. |
| "User said 'just code it'" | Log override, ask risk MCQ, proceed minimally. |

---

## How to Use These Tables

1. **Self-Check**: Before skipping a process, scan the relevant table
2. **Quote Reality**: When tempted, read the "Reality" column aloud
3. **Log Override**: If proceeding anyway, log it as SAFETY_OVERRIDE
4. **Teaching Moment**: Use these as MCQ options for user learning
