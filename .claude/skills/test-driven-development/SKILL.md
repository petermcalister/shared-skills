---
name: test-driven-development
description: >
  Use when implementing any feature, bugfix, or behavior change — before writing
  implementation code. Trigger on: "add a feature", "fix this bug", "implement",
  "build this function", "refactor", "add retry logic", "handle errors", or any
  request to write production code. Also trigger when the user describes desired
  behavior that implies new code ("it should retry 3 times", "validate the email",
  "parse the CSV and output JSON"). The key signal is: code needs to be written,
  and tests should come first.
version: 0.1.0
---

# Test-Driven Development (TDD)

Write the test first. Watch it fail. Write minimal code to pass.

**Core principle:** If you didn't watch the test fail, you don't know if it tests
the right thing. A test that passes immediately proves nothing — it might test the
wrong behavior, test the implementation instead of the requirement, or miss edge
cases entirely.

## When to Use

**Always:** new features, bug fixes, refactoring, behavior changes.

**Exceptions (ask the user):** throwaway prototypes, generated code, configuration.

## The Cycle

```
RED → write one failing test
  ↓
Verify it fails for the right reason (feature missing, not typo)
  ↓
GREEN → write simplest code to pass
  ↓
Verify all tests pass, output clean
  ↓
REFACTOR → clean up while staying green
  ↓
Repeat for next behavior
```

### RED — Write Failing Test

One minimal test showing what should happen. Clear name, real behavior, one thing.

```typescript
// Good: clear name, tests real behavior
test('retries failed operations 3 times', async () => {
  let attempts = 0;
  const operation = () => {
    attempts++;
    if (attempts < 3) throw new Error('fail');
    return 'success';
  };
  const result = await retryOperation(operation);
  expect(result).toBe('success');
  expect(attempts).toBe(3);
});

// Bad: vague name, tests mock not code
test('retry works', async () => {
  const mock = jest.fn().mockRejectedValueOnce(new Error()).mockResolvedValueOnce('ok');
  await retryOperation(mock);
  expect(mock).toHaveBeenCalledTimes(2);
});
```

Run the test. Confirm it **fails** (not errors) for the expected reason.

### GREEN — Minimal Code

Write the simplest code that makes the test pass. Don't add features, options, or
abstractions beyond what the test requires — that's over-engineering. The test defines
the scope.

Run the test. Confirm it passes. Confirm other tests still pass.

### REFACTOR — Clean Up

Only after green: remove duplication, improve names, extract helpers. Keep tests
green throughout. Don't add new behavior during refactor.

---

## Why Test-First Matters

Tests written after code pass immediately, which proves nothing — you never saw them
catch the bug. Tests-after answer "what does this code do?" Tests-first answer "what
should this code do?" That distinction matters because tests-after are biased by your
implementation; you test what you built, not what's required.

Test-first also forces edge case discovery. When you write the test before the code,
you think about boundaries, errors, and empty inputs upfront. Tests-after only verify
the cases you remembered.

---

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Too simple to test" | Simple code breaks. Test takes 30 seconds. |
| "I'll test after" | Tests passing immediately prove nothing. |
| "Tests after achieve same goals" | Tests-after = "what does this do?" Tests-first = "what should this do?" |
| "Already manually tested" | Ad-hoc, no record, can't re-run, easy to miss cases. |
| "Deleting X hours is wasteful" | Sunk cost. Keeping unverified code is the real waste. |
| "Keep as reference" | You'll adapt it. That's testing after. Delete means delete. |
| "Need to explore first" | Fine. Throw away exploration, then start with TDD. |
| "Test hard = design problem" | Listen to the test. Hard to test = hard to use. |
| "TDD slows me down" | TDD is faster than debugging. Short-term pain, long-term speed. |

---

## Red Flags — Stop and Restart

If you notice any of these, you've left the TDD cycle:

- Writing code before a test exists
- A test passing immediately on first run
- Can't explain why a test failed
- Rationalizing "just this once"
- Saying "I'll add tests later"
- Thinking "this is different because..."

---

## Example: Bug Fix

**Bug:** Empty email accepted by form.

**RED:**
```typescript
test('rejects empty email', async () => {
  const result = await submitForm({ email: '' });
  expect(result.error).toBe('Email required');
});
```

Run: `FAIL — expected 'Email required', got undefined`. Good — fails because the
validation is missing, not because of a typo.

**GREEN:**
```typescript
function submitForm(data: FormData) {
  if (!data.email?.trim()) return { error: 'Email required' };
  // ...existing logic
}
```

Run: `PASS`. All other tests still pass.

**REFACTOR:** Extract validation if multiple fields need similar checks.

---

## Good Tests

| Quality | Good | Bad |
|---------|------|-----|
| **Minimal** | Tests one thing | `test('validates email and domain and whitespace')` |
| **Clear** | Name describes behavior | `test('test1')` |
| **Real** | Tests actual code | Tests mock behavior |

---

## When Stuck

| Problem | Solution |
|---------|----------|
| Don't know how to test | Write the API you wish existed. Assertion first. |
| Test too complicated | Design too complicated. Simplify the interface. |
| Must mock everything | Code too coupled. Use dependency injection. |
| Test setup huge | Extract helpers. Still complex? Simplify design. |

---

## Testing Anti-Patterns

When adding mocks or test utilities, read `testing-anti-patterns.md` for common
pitfalls: testing mock behavior instead of real behavior, adding test-only methods
to production classes, mocking without understanding dependencies.

---

## Checklist

Before marking work complete:

- [ ] Every new function/method has a test
- [ ] Watched each test fail before implementing
- [ ] Each test failed for the expected reason
- [ ] Wrote minimal code to pass each test
- [ ] All tests pass, output clean
- [ ] Tests use real code (mocks only if unavoidable)
- [ ] Edge cases and error paths covered
