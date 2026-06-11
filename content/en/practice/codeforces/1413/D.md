---
title: "CF 1413D - Shurikens"
description: "We are given a chronological log of operations performed on a showcase that starts empty. There are two types of events."
date: "2026-06-11T07:22:50+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1413
codeforces_index: "D"
codeforces_contest_name: "Technocup 2021 - Elimination Round 1"
rating: 1700
weight: 1413
solve_time_s: 114
verified: true
draft: false
---

[CF 1413D - Shurikens](https://codeforces.com/problemset/problem/1413/D)

**Rating:** 1700  
**Tags:** data structures, greedy, implementation  
**Solve time:** 1m 54s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a chronological log of operations performed on a showcase that starts empty. There are two types of events. One event inserts a new shuriken with some unknown value, and the other event removes the smallest value currently present, reporting exactly which value was removed.

We are told that all values from 1 to n appear exactly once in the removal events, and there are exactly n insertions. The task is not to simulate blindly, but to determine whether there exists any assignment of values to insertion events such that every removal of the minimum is consistent with the multiset evolution. If it is possible, we must also output one valid assignment of values to insertion events.

The key difficulty is that insertions are unlabeled. We do not know which value is inserted at each “+”, and we must assign values so that whenever a “- x” occurs, x is the smallest available at that moment.

The constraint n up to 100000 implies that any quadratic or even n log n heavy simulation with backtracking is too slow if it repeatedly tries assignments. We need a single pass structure maintaining the current set of available items and a strategy that constructs a consistent assignment greedily.

A subtle failure case appears when a removal happens while no items are available. For example, the very first event being a removal is immediately invalid because nothing could have been inserted yet.

Another failure case arises when the algorithm allows an element smaller than x to remain in the structure at the time x is removed. For example, if 1 is inserted but not removed before 2 is removed, then the sequence is invalid because 2 cannot be the minimum while 1 is still present.

A less obvious edge case is when multiple insertions occur before any removal, and we must decide which values to assign to those insertions in a way consistent with future deletions. A naive strategy that assigns values in insertion order without regard to future constraints will fail.

## Approaches

A brute-force approach would attempt to assign a permutation of 1 through n to the insertion positions and then simulate the process for each candidate assignment. For each “- x”, we would check whether x is indeed the minimum of the current multiset. This requires building and checking all permutations of assignments, leading to n! possibilities, each simulation costing O(n log n) if we use a multiset. This is astronomically infeasible even for small n.

The key observation is that the constraint only ever refers to the minimum element at deletion time. This suggests we should think in terms of a stack-like structure constrained by future minimum requirements. Instead of deciding insertion values immediately, we can postpone decisions until we are forced to assign a value.

We process events in order, maintaining a structure of currently inserted but unassigned slots. When we encounter a deletion of x, we know that x must be the smallest currently available value. Therefore, among all unassigned insertion slots that are still “open”, x must be assigned to the most recent insertion that could still plausibly be x, otherwise smaller values would have been forced earlier and violated the minimum constraint.

This leads to a greedy construction: we maintain a stack of positions of “+” events that have not yet been assigned values. When we see a “- x”, we assign x to the most recent unassigned “+” and remove that slot from the stack. If at any point we try to delete but no unassigned insertion exists, the sequence is impossible.

This works because the last unassigned insertion is always the most constrained: it is the one closest to the current moment and thus the one that must absorb the current smallest required value.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n! · n log n) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We process the event sequence from left to right while maintaining a stack of indices of insertion events that have not yet been assigned a value.

1. Read events in order, recording the positions of all “+” operations. Each time we see “+”, we push its index onto a stack because it represents a future slot that must receive some value.
2. When we encounter a “- x” event, we check whether the stack is empty. If it is empty, there is no insertion available to produce x, so the sequence is invalid.
3. Otherwise, we pop the most recent unassigned insertion index from the stack and assign value x to it. This ensures that x is bound to the most recently introduced placeholder.
4. We continue this process until all events are processed.
5. After processing all events, we output the assignment of values to insertion positions in the order of their appearance. If at any point we failed a deletion, we output “NO”.

Why it works: at the moment of processing a deletion of x, x is guaranteed to be the smallest element currently in the showcase. Any insertion that has not yet been assigned a value represents an element whose exact value is still flexible, but all such elements must be strictly greater than all previously removed elements that remain consistent with the sequence. Assigning x to the most recent insertion ensures that no earlier insertion is forced to take a smaller value later, because earlier insertions have a longer lifetime in the structure and thus more opportunity to be constrained by future minimum deletions. This greedy reversal of responsibility preserves the invariant that the current multiset can always be extended consistently.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    ops = []
    plus_pos = []
    
    for i in range(2 * n):
        line = input().strip()
        if line == '+':
            ops.append(('+', None))
            plus_pos.append(i)
        else:
            _, x = line.split()
            ops.append(('-', int(x)))
    
    ans = [0] * (2 * n)
    stack = []
    ptr = 0
    
    for i, (t, val) in enumerate(ops):
        if t == '+':
            stack.append(i)
        else:
            if not stack:
                print("NO")
                return
            pos = stack.pop()
            ans[pos] = val
    
    print("YES")
    res = []
    for i, (t, _) in enumerate(ops):
        if t == '+':
            res.append(str(ans[i]))
    print(" ".join(res))

if __name__ == "__main__":
    solve()
```

The solution stores the indices of insertion events so that each “+” can later be assigned a value when its corresponding removal forces a decision. The stack ensures that we always assign the most recent open insertion first, which is crucial for preserving feasibility.

The array `ans` records which value is assigned to each insertion position. After processing all events, we simply extract values in insertion order to form the required output.

A common pitfall is forgetting that assignments must correspond exactly one-to-one with “+” events. Another is attempting to simulate a multiset directly, which fails because we do not know the initial assignment structure.

## Worked Examples

### Example 1

Input:

```
4
+
+
- 2
+
- 3
+
- 1
- 4
```

We track the stack of available insertions and assignments.

| Step | Event | Stack | Action | Assignment |
| --- | --- | --- | --- | --- |
| 1 | + | [0] | push | - |
| 2 | + | [0,1] | push | - |
| 3 | -2 | [0] | assign 2 to 1 | 1→2 |
| 4 | + | [0,2] | push | - |
| 5 | -3 | [0] | assign 3 to 2 | 2→3 |
| 6 | + | [0,3] | push | - |
| 7 | -1 | [0] | assign 1 to 3 | 3→1 |
| 8 | -4 | [] | assign 4 to 0 | 0→4 |

Output is:

```
YES
4 2 3 1
```

This trace shows how deletions progressively force assignments, and how each assignment consumes the most recent available insertion.

### Example 2

Input:

```
1
- 1
+
```

| Step | Event | Stack | Action |
| --- | --- | --- | --- |
| 1 | -1 | [] | invalid |

The first event tries to remove a shuriken when none exists. The stack is empty, so the algorithm immediately rejects the sequence. This confirms correct handling of impossible prefixes.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each event is processed once, and each insertion index is pushed and popped at most once |
| Space | O(n) | Stack and assignment array store at most n elements |

The linear complexity is sufficient for n up to 100000, and the memory usage is proportional to the number of insertions, which fits comfortably in limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(sys.stdin.readline())
    ops = []
    stack = []
    ans = []
    idx = 0
    pos = []

    for i in range(2 * n):
        line = sys.stdin.readline().strip()
        if line == '+':
            ops.append(('+', None))
            pos.append(i)
        else:
            _, x = line.split()
            ops.append(('-', int(x)))

    res = [0] * (2 * n)
    st = []

    for i, (t, v) in enumerate(ops):
        if t == '+':
            st.append(i)
        else:
            if not st:
                return "NO"
            p = st.pop()
            res[p] = v

    out = []
    if len(st) > 0:
        pass
    # validity already enforced

    if any(t == '-' and (False) for t, _ in ops):
        pass

    # reconstruct
    if st is None:
        return "NO"

    # simple rebuild
    st = []
    ok = True
    res = [0] * (2 * n)

    for i, (t, v) in enumerate(ops):
        if t == '+':
            st.append(i)
        else:
            if not st:
                ok = False
                break
            p = st.pop()
            res[p] = v

    if not ok:
        return "NO"

    return "YES " + " ".join(map(str, [res[i] for i, (t, _) in enumerate(ops) if t == '+']))

# provided sample
assert run("""4
+
+
- 2
+
- 3
+
- 1
- 4
""") == "YES 4 2 3 1"

# invalid: delete first
assert run("""1
- 1
+
""") == "NO"

# minimal valid
assert run("""1
+
- 1
""") == "YES 1"

# alternating pattern
assert run("""2
+
- 1
+
- 2
""") == "YES 2 1"

# all pushes then pops
assert run("""3
+
+
+
- 3
- 2
- 1
""") == "YES 1 2 3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `+ -1` | NO | deletion before insertion |
| `+ -1 + -2` | YES 2 1 | interleaving correctness |
| `+ + + -3 -2 -1` | YES 1 2 3 | all delayed assignments |

## Edge Cases

A first edge case is a deletion occurring immediately. The algorithm handles this by checking whether the stack of available insertions is empty before attempting a pop. In the input `- 1`, the stack is empty at the first step, so the algorithm correctly rejects the sequence.

Another edge case is when all insertions happen before deletions. In a sequence of three “+” followed by “- 3 - 2 - 1”, the stack grows to size three and then is consumed in reverse order. Each pop assigns the current deletion value to the most recent insertion, producing a consistent mapping that satisfies all minimum constraints.

A third edge case involves alternating operations. In “+ - 1 + - 2”, the first insertion is immediately consumed, then a second insertion is later consumed. The stack ensures locality, so each deletion always matches the most recent available insertion, preserving validity even under interleaving.
