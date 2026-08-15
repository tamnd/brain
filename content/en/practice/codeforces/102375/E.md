---
title: "CF 102375E - \u0414\u0443\u043c\u0441\u043a\u0438\u0439 \u0440\u0435\u0433\u043b\u0430\u043c\u0435\u043d\u0442"
description: "We are given a chronological log of a parliamentary session. Every Add x event means that party x introduces a new bill. The newly introduced bill immediately becomes the one being discussed, so the bill that was being discussed before it is suspended."
date: "2026-08-15T17:54:05+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102375
codeforces_index: "E"
codeforces_contest_name: "\u041a\u0432\u0430\u043b\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u043e\u043d\u043d\u044b\u0439 \u0440\u0430\u0443\u043d\u0434 \u0427\u0435\u043c\u043f\u0438\u043e\u043d\u0430\u0442\u0430 \u0421\u0435\u0432\u0435\u0440\u043e-\u0417\u0430\u043f\u0430\u0434\u0430 \u0420\u043e\u0441\u0441\u0438\u0438 \u0438 \u041c\u043e\u0441\u043a\u0432\u044b ICPC 2019"
rating: 0
weight: 102375
solve_time_s: 145
verified: false
draft: false
---

[CF 102375E - \u0414\u0443\u043c\u0441\u043a\u0438\u0439 \u0440\u0435\u0433\u043b\u0430\u043c\u0435\u043d\u0442](https://codeforces.com/problemset/problem/102375/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 25s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a chronological log of a parliamentary session. Every `Add x` event means that party `x` introduces a new bill. The newly introduced bill immediately becomes the one being discussed, so the bill that was being discussed before it is suspended. Every `Vote x` event means that the currently discussed bill is voted on, and the recorded party must be the party that introduced that bill. After the vote, discussion returns to the bill that had been suspended underneath it.

This is exactly a stack discipline. An `Add` places a new bill on top of all unfinished bills. A `Vote` must remove the bill currently on top. The party written in the event must agree with that top bill. When the log ends, there must be no unfinished bills, so the stack must be empty.

The input contains at most 1000 events. That is small enough that even a quadratic algorithm would finish easily, but the structure of the problem gives us a linear solution with only a stack. There is no need for graph algorithms, dynamic programming, or any search over possible orders. In fact, the event order completely determines the stack state.

The first edge case is a vote before any bill has been introduced. For example,

```
1
Vote z
```

must produce `No`. There is no current bill to vote on, so a careless implementation that only checks whether some earlier event used `z` could accept an impossible session.

The second edge case is a vote for a suspended bill instead of the current one. For example,

```
4
Add a
Add b
Vote a
Vote b
```

produces `No`. After `Add b`, bill `b` is being discussed and bill `a` is suspended. The next vote must be for `b`, not `a`. An implementation that merely checks whether `a` is among the unfinished bills would incorrectly accept the sequence.

The third edge case is repeated use of the same party. For example,

```
6
Add a
Add a
Vote a
Vote a
Add b
Vote b
```

produces `Yes`. The two `a` bills are different bills even though they have the same party label. A stack handles this naturally because each `Add a` creates another separate stack entry.

The final edge case is an unfinished bill at the end. For example,

```
1
Add a
```

produces `No`. The bill was introduced but never voted on, so the session cannot finish legally.

## Approaches

A direct brute-force simulation can repeatedly reconstruct the set of unfinished bills before every vote. Starting from the beginning of the log, we process all earlier `Add` and `Vote` events and rebuild the current stack, then inspect its top for the current vote. This is correct because the stack after any prefix is completely determined by that prefix.

The problem with this version is repeated work. If there are (K) events and we rebuild the stack for every event, the first event may require one operation, the second two, and so on. In the worst case this takes about

[
1 + 2 + \dots + K = O(K^2)
]

operations, which is unnecessary.

The key observation is that the state after a prefix does not need to be reconstructed. We only need the state produced by the immediately preceding event. An `Add x` pushes `x`, and a `Vote x` checks the current top and then pops it. The stack itself is exactly the mathematical model of the parliamentary rule.

The brute-force works because every prefix can be simulated from the event history, but fails by recomputing the same history many times. The observation that each event changes the stack in only one local way lets us maintain the state incrementally in one pass.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(K²) | O(K) | Accepted for K ≤ 1000, but unnecessarily slow |
| Optimal | O(K) | O(K) | Accepted |

## Algorithm Walkthrough

1. Create an empty stack. It represents all bills that have been introduced but have not yet received their final vote, with the currently discussed bill at the top.
2. Read the events from left to right. The order cannot be rearranged because it is the chronological record of the session.
3. For an `Add x` event, push `x` onto the stack. The new bill immediately interrupts the previous discussion, so it must become the new top.
4. For a `Vote x` event, first check whether the stack is empty. If it is empty, there is no bill currently under discussion, so the log is impossible.
5. If the stack is not empty, compare its top element with `x`. If they differ, the event is impossible because only the currently discussed bill can be voted on. Return `No`.
6. If the top equals `x`, pop it. That bill has now finished, and the bill underneath it, if one exists, becomes the active discussion again.
7. After all events have been processed, check whether the stack is empty. An empty stack means every introduced bill received its vote. A nonempty stack means at least one bill was left unfinished, so return `No`.

### Why it works

The invariant is that after processing any valid prefix, the stack contains exactly the unfinished bills in their interruption order, with the currently discussed bill at the top. An `Add` preserves this invariant by putting the newly active bill on top. A valid `Vote` preserves it by removing exactly the active bill and exposing the previously suspended one. If a vote refers to anything other than the top, no valid session could have produced that event. If the stack is nonempty at the end, some discussion is unfinished. Thus the algorithm accepts exactly the valid event sequences.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    k = int(input())
    stack = []

    for _ in range(k):
        event, party = input().split()

        if event == "Add":
            stack.append(party)
        else:
            if not stack or stack[-1] != party:
                print("No")
                return
            stack.pop()

    print("Yes" if not stack else "No")

if __name__ == "__main__":
    solve()
```

The `stack` list stores party letters for all unfinished bills. Each occurrence of `Add` creates a new stack entry, even if the party letter is already present, because two bills introduced by the same party are still separate bills.

For `Vote`, the emptiness check must happen before accessing `stack[-1]`. Otherwise a vote as the first event would cause an invalid indexing operation instead of producing `No`.

The comparison with `stack[-1]` happens before the `pop`. If the labels differ, we immediately reject the whole log because removing any lower element would violate the interruption rule.

At the end, checking `not stack` handles the requirement that every discussion must eventually finish. Python integers do not appear in the algorithm, so there are no overflow concerns. Every event is processed exactly once.

## Worked Examples

### Sample 1

The input is:

```
4
Add a
Add b
Vote a
Vote b
```

The state changes are:

| Event | Stack before | Action | Stack after |
| --- | --- | --- | --- |
| `Add a` | `[]` | push `a` | `[a]` |
| `Add b` | `[a]` | push `b` | `[a, b]` |
| `Vote a` | `[a, b]` | top is `b`, mismatch | reject |
| `Vote b` | not reached | not reached | not reached |

After `Add b`, bill `b` is the active bill. The vote for `a` attempts to finish a suspended bill while the newer bill is still being discussed, so the sequence is impossible.

The algorithm rejects immediately and prints `No`.

### Sample 2

The input is:

```
8
Add z
Vote z
Add x
Add y
Add x
Vote x
Vote y
Vote x
```

The trace is:

| Event | Stack before | Action | Stack after |
| --- | --- | --- | --- |
| `Add z` | `[]` | push `z` | `[z]` |
| `Vote z` | `[z]` | pop `z` | `[]` |
| `Add x` | `[]` | push `x` | `[x]` |
| `Add y` | `[x]` | push `y` | `[x, y]` |
| `Add x` | `[x, y]` | push `x` | `[x, y, x]` |
| `Vote x` | `[x, y, x]` | pop `x` | `[x, y]` |
| `Vote y` | `[x, y]` | pop `y` | `[x]` |
| `Vote x` | `[x]` | pop `x` | `[]` |

Every vote matches the current top, and the stack is empty at the end. The repeated `x` labels cause no ambiguity because each `Add x` contributes its own stack entry.

The algorithm prints `Yes`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(K) | Each event performs a constant amount of stack work |
| Space | O(K) | In the worst case all K events can be `Add` events before any vote |

With (K \le 1000), the linear algorithm is comfortably within the limits. Even the quadratic reconstruction approach would be small enough for this particular bound, but the stack simulation is simpler, faster, and directly expresses the rule being checked.

## Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline
    k = int(input())
    stack = []

    for _ in range(k):
        event, party = input().split()

        if event == "Add":
            stack.append(party)
        else:
            if not stack or stack[-1] != party:
                print("No")
                return
            stack.pop()

    print("Yes" if not stack else "No")

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    result = sys.stdout.getvalue().strip()

    sys.stdin = old_stdin
    sys.stdout = old_stdout

    return result

# Provided samples
assert run("""4
Add a
Add b
Vote a
Vote b
""") == "No", "sample 1"

assert run("""8
Add z
Vote z
Add x
Add y
Add x
Vote x
Vote y
Vote x
""") == "Yes", "sample 2"

assert run("""1
Vote z
""") == "No", "sample 3"

# Minimum-size input
assert run("""1
Add a
""") == "No", "unfinished single bill"

# A single complete bill
assert run("""2
Add z
Vote z
""") == "Yes", "single completed bill"

# All events use the same party
assert run("""6
Add a
Add a
Add a
Vote a
Vote a
Vote a
""") == "Yes", "nested bills from one party"

# Wrong nesting order
assert run("""6
Add a
Add b
Add c
Vote b
Vote c
Vote a
""") == "No", "vote must match the top"

# Maximum-size valid input
assert run("1000\n" + "\n".join(["Add a"] * 500 + ["Vote a"] * 500) + "\n") == "Yes", \
    "maximum-size valid sequence"

# Maximum-size invalid input
assert run("1000\n" + "\n".join(["Add a"] * 500 + ["Vote b"] + ["Vote a"] * 499) + "\n") == "No", \
    "maximum-size invalid sequence"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / Add a` | `No` | Minimum size and unfinished final stack |
| `2 / Add z, Vote z` | `Yes` | Smallest possible valid session |
| Three `Add a` followed by three `Vote a` | `Yes` | Multiple distinct bills with the same party |
| `Add a, Add b, Add c, Vote b, ...` | `No` | A suspended bill cannot be voted before the active one |
| 500 adds followed by 500 matching votes | `Yes` | Maximum input size and deep stack |
| 500 `a` adds followed by `Vote b` | `No` | Maximum input size and immediate mismatch detection |

## Edge Cases

### Vote before any Add

For

```
1
Vote z
```

the stack starts empty. The event is a `Vote`, so the algorithm checks the stack before looking at its top. Since there is no current bill, it prints `No` immediately. This avoids both accepting an impossible event and attempting to access an empty stack.

### Voting for a suspended bill

For

```
4
Add a
Add b
Vote a
Vote b
```

the stack becomes `[a, b]` after the second event. The next event asks to vote for `a`, but `stack[-1]` is `b`. The algorithm rejects the log without popping anything. This captures the central nesting rule: a newer bill must finish before the interrupted bill can resume.

### Repeated party labels

For

```
6
Add a
Add a
Vote a
Vote a
Add b
Vote b
```

the stack evolves as `[a]`, `[a, a]`, `[a]`, `[]`, `[b]`, `[]`. The two `a` entries are treated as separate bills even though their labels are identical. The algorithm never tries to identify a bill globally, because only the top position matters.

### Unfinished discussion at the end

For

```
3
Add a
Add b
Vote b
```

the final stack is `[a]`. The vote for `b` was valid because `b` was the active bill, but the older `a` discussion remains suspended and unfinished. The final emptiness check consequently prints `No`.

### Empty stack after every completed bill

For

```
6
Add a
Vote a
Add b
Vote b
Add c
Vote c
```

the stack returns to empty after every pair. Each new bill starts a fresh discussion, and there are never any suspended bills. The algorithm accepts because every vote matches the top and the final stack is empty.

### Same party can introduce nested bills

For

```
4
Add x
Add x
Vote x
Vote x
```

both votes are valid. The first `Vote x` removes the inner bill, revealing the older `x` bill, and the second vote removes that one. A solution that stores only a set of active parties would lose this distinction, while a stack naturally preserves the number and nesting order of unfinished bills.
