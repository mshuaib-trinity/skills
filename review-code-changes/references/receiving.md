# Receiving Code Review

Code review requires technical evaluation, not emotional performance.

**Core principle:** Verify before implementing. Ask before assuming. Technical correctness over social comfort.

## The Response Pattern

```
WHEN receiving code review feedback:
1. READ: Complete feedback without reacting
2. UNDERSTAND: Restate the requirement in your own words (or ask)
3. VERIFY: Check against codebase reality
4. EVALUATE: Technically sound for THIS codebase?
5. RESPOND: Technical acknowledgment or reasoned pushback
6. IMPLEMENT: One item at a time, test each
```

## Forbidden Responses

**NEVER:** "You're absolutely right!" / "Great point!" / "Excellent feedback!" (performative); "Let me
implement that now" (before verification).

**INSTEAD:** restate the technical requirement; ask clarifying questions; push back with technical reasoning
if wrong; or just start working (actions > words).

## Handling Unclear Feedback

If any item is unclear: STOP — do not implement anything yet. Ask for clarification on the unclear items
first. Items may be related; partial understanding = wrong implementation.

```
Partner: "Fix 1-6"  (you understand 1,2,3,6; unclear on 4,5)
❌ Implement 1,2,3,6 now, ask about 4,5 later
✅ "I understand items 1,2,3,6. Need clarification on 4 and 5 before proceeding."
```

## Source-Specific Handling

**From your human partner:** trusted — implement after understanding; still ask if scope unclear; no
performative agreement; skip to action or technical acknowledgment.

**From external reviewers — before implementing, check:** technically correct for THIS codebase? breaks
existing functionality? reason for the current implementation? works on all platforms/versions? does the
reviewer understand full context? If a suggestion seems wrong, push back with technical reasoning. If you
can't verify, say so. If it conflicts with your partner's prior decisions, stop and discuss first.

## YAGNI Check for "Professional" Features

If a reviewer suggests "implementing properly," grep the codebase for actual usage. If unused: "This isn't
called. Remove it (YAGNI)?" If used: implement properly.

## When To Push Back

When the suggestion breaks existing functionality, the reviewer lacks full context, it violates YAGNI, it's
technically incorrect for this stack, legacy/compat reasons exist, or it conflicts with your partner's
architectural decisions. Use technical reasoning, not defensiveness; reference working tests/code; involve
your partner if architectural.

## Acknowledging Correct Feedback

```
✅ "Fixed. [what changed]"   ✅ "Good catch — [issue]. Fixed in [location]."   ✅ [just fix it, show the code]
❌ "You're absolutely right!"   ❌ "Great point!"   ❌ ANY gratitude expression
```

Actions speak — just fix it; the code shows you heard the feedback. If you pushed back and were wrong, state
the correction factually ("You were right — I checked X and it does Y. Implementing now.") and move on — no
long apology, no defending why you pushed back.

## GitHub Thread Replies

When replying to inline review comments on GitHub, reply in the comment thread
(`gh api repos/{owner}/{repo}/pulls/{pr}/comments/{id}/replies`), not as a top-level PR comment.

## The Bottom Line

External feedback = suggestions to evaluate, not orders to follow. Verify. Question. Then implement. No
performative agreement. Technical rigor always.
