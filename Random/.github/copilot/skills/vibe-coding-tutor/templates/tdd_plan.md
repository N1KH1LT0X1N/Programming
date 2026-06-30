# {Feature Name} Implementation Plan

> **For Agent:** REQUIRED: Use TDD (Red-Green-Refactor) for each task. Follow the Iron Laws.

**Goal:** {One sentence description}
**Language:** {python/javascript/typescript/go/rust}
**Created:** {YYYY-MM-DD HH:MM:SS}

---

## Decisions Made (from Vibe Check)

| Decision | Choice | Rationale | MCQ# |
|:---|:---|:---|:---|
| {decision_1} | {choice_1} | {rationale_1} | #{mcq_number} |

---

## [ ] Task 1: {Component Name}

**Description:** {What this task accomplishes}
**Test File:** `{tests/test_file.py}`
**Implementation File:** `{src/file.py}`

### Step 1: Write Failing Test

```{language}
def test_basic_case():
    """Test that {behavior description}."""
    result = function_under_test(input_value)
    assert result == expected_value
```

### Step 2: Verify Test Fails

**Run:** `pytest tests/test_file.py::test_basic_case -v`
**Expected:** FAIL with "NameError: name 'function_under_test' is not defined"

> [!IMPORTANT]
> You MUST see this test fail before proceeding. If it passes, the test is wrong.

### Step 3: Write Minimal Implementation

```{language}
def function_under_test(input_value):
    """Minimal implementation to pass the test."""
    return expected_value
```

### Step 4: Verify Test Passes

**Run:** `pytest tests/test_file.py::test_basic_case -v`
**Expected:** PASS (1 passed in X.XXs)

> [!IMPORTANT]
> You MUST see this test pass before proceeding. Show the actual output.

### Step 5: Commit

```bash
git add tests/test_file.py src/file.py
git commit -m "feat: add {feature_name} - basic implementation"
```

---

## 🎓 Teaching Moment (After Task 1)

**Reinforcement MCQ:**

> Why did we write the test before the implementation?
>
> A) It proves the test can actually catch bugs (we saw it fail)
> B) It's faster than writing code first
> C) It's required by the language
> D) Custom answer

**Correct:** A - Seeing the test fail proves it tests the right thing.

---

## [ ] Task 2: {Next Component}

**Description:** {What this task accomplishes}
**Test File:** `{tests/test_file.py}`

### Step 1: Write Failing Test

```{language}
def test_edge_case():
    """Test that {edge case behavior}."""
    # TODO: Write test for edge case
    pass
```

### Step 2: Verify Test Fails

**Run:** `pytest tests/test_file.py::test_edge_case -v`
**Expected:** FAIL

### Step 3: Write Minimal Implementation

```{language}
# TODO: Extend implementation for edge case
```

### Step 4: Verify Test Passes

**Run:** `pytest tests/test_file.py -v`
**Expected:** PASS (2 passed)

### Step 5: Commit

```bash
git add .
git commit -m "feat: add {feature_name} - edge case handling"
```

---

## Final Verification

After all tasks complete:

1. **Run full test suite:**
   ```bash
   pytest -v
   ```
   **Expected:** All tests pass

2. **Verify no warnings:**
   ```bash
   pytest -v --tb=short
   ```
   **Expected:** Clean output, no deprecation warnings

3. **Final commit:**
   ```bash
   git add .
   git commit -m "feat: complete {feature_name} implementation"
   ```

---

## Completion Checklist

- [ ] All tasks marked [x]
- [ ] All tests pass (verified with fresh run)
- [ ] Code committed to git
- [ ] No TODO comments remaining
- [ ] Reinforcement MCQs answered
