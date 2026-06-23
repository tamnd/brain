---
title: "CF 105492J - Jumbled Scoreboards"
description: "We receive a sequence of snapshots from a game scoreboard, where each snapshot contains two integers representing the scores of two competing teams at that moment."
date: "2026-06-23T19:44:24+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105492
codeforces_index: "J"
codeforces_contest_name: "2024 Benelux Algorithm Programming Contest (BAPC 24)"
rating: 0
weight: 105492
solve_time_s: 55
verified: true
draft: false
---

[CF 105492J - Jumbled Scoreboards](https://codeforces.com/problemset/problem/105492/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 55s  
**Verified:** yes  

## Solution
## Problem Understanding

We receive a sequence of snapshots from a game scoreboard, where each snapshot contains two integers representing the scores of two competing teams at that moment. These snapshots were sent in the order they arrived, but that order might not reflect the actual chronological order in which the match progressed.

The task is to determine whether the given sequence could represent a valid timeline of a real match. A valid timeline means that from one snapshot to the next, neither team’s score ever decreases. Both scores can stay the same or increase, but never go down in time.

So we are not reconstructing the timeline, and we are not reordering anything. We are simply checking whether the given order already respects the monotonicity constraint on both coordinates simultaneously.

The constraints are small: at most 100 snapshots, and each score is between 0 and 100. This immediately tells us that any solution that is even quadratic is comfortably safe, and a linear scan is more than sufficient. There is no need for sophisticated data structures or search.

The main subtlety in this problem is understanding what “chronological order” means. It is not about sorting by time explicitly or comparing timestamps. The only clue we have is that scores only increase over time. That single rule fully determines validity.

A few edge situations can break naive thinking:

If we only check that total score increases, we can fail. For example, (2, 5) followed by (3, 4) has total 7 followed by 7, so totals do not decrease, but the second team’s score drops from 5 to 4, which is invalid. This would incorrectly be accepted by a careless solution.

If we only check that each snapshot is “greater than or equal” in some partial sense like max or min ordering, we also fail. For example, (1, 10) to (2, 0) has an increasing max but violates monotonicity in both components.

So the correct condition must be checked component-wise between consecutive snapshots.

## Approaches

A brute-force mindset might try to verify consistency by considering all pairs of snapshots and checking whether there exists a consistent ordering that satisfies monotonicity constraints globally. That would resemble building a partial order graph and checking for a valid linear extension. While that is theoretically correct, it is completely unnecessary here because the input order is fixed and we are not allowed to reorder anything.

Instead, we observe that if the sequence is valid in time order, then every adjacent transition must preserve non-decreasing values for both teams. Conversely, if every adjacent pair satisfies this condition, then the entire sequence must be valid because monotonicity is transitive: once no step decreases either coordinate, no earlier snapshot can violate a later one.

This reduces the problem to a single pass check over the array, verifying a simple inequality condition at each step.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (global consistency reasoning) | O(n²) or worse | O(n) | Accepted but unnecessary |
| Optimal (adjacent validation) | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read all snapshots in the given order, storing them as pairs of integers.
2. Iterate from the second snapshot to the last snapshot.
3. For each snapshot at position i, compare it with the previous snapshot at position i−1.
4. If either team’s score decreases from i−1 to i, immediately conclude the sequence is invalid.
5. If the loop finishes without finding any decrease, conclude the sequence is valid.

Each step focuses on adjacency because any violation of monotonicity must first appear at some immediate transition. If a drop happens, it cannot be “hidden” across multiple steps.

### Why it works

The key invariant is that after processing each position i, all snapshots from 0 to i are consistent in the sense that both score sequences are non-decreasing. If at any point we detect a decrease, we break the invariant and correctly reject the sequence.

If no adjacent pair violates monotonicity, then for any indices i < j, repeated application of the non-decreasing property ensures both a[i] ≤ a[j] and b[i] ≤ b[j]. This guarantees the entire sequence is temporally valid.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
prev_a, prev_b = map(int, input().split())

ok = True

for _ in range(n - 1):
    a, b = map(int, input().split())
    if a < prev_a or b < prev_b:
        ok = False
    prev_a, prev_b = a, b

print("yes" if ok else "no")
```

The solution keeps only the previous snapshot while scanning forward, which is enough because validity depends solely on consecutive transitions. The variables `prev_a` and `prev_b` represent the last confirmed valid state in the timeline.

The conditional check `a < prev_a or b < prev_b` directly encodes the rule that neither score is allowed to decrease. Updating the previous values unconditionally ensures we continue checking the full sequence even after detecting a violation, though we could also break early.

## Worked Examples

### Example 1

Input:

```
4
1 0
2 0
4 0
4 1
```

| i | prev | current | valid transition |
| --- | --- | --- | --- |
| 1 | (1,0) | (2,0) | yes |
| 2 | (2,0) | (4,0) | yes |
| 3 | (4,0) | (4,1) | yes |

All transitions preserve non-decreasing scores, so the answer is yes.

This trace shows that once both sequences are monotone step by step, the entire timeline remains consistent.

### Example 2

Input:

```
3
0 0
1 0
0 2
```

| i | prev | current | valid transition |
| --- | --- | --- | --- |
| 1 | (0,0) | (1,0) | yes |
| 2 | (1,0) | (0,2) | no |

At the second transition, the first team’s score drops from 1 to 0, which immediately breaks validity.

This demonstrates that even if one coordinate increases significantly, any decrease in the other coordinate invalidates the whole sequence.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | We process each snapshot exactly once and perform constant-time comparisons |
| Space | O(1) | Only the previous pair of scores is stored |

The constraints allow up to 100 snapshots, but even if this were much larger, the linear scan would remain efficient. The solution is optimal because every input value must be read at least once.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n = int(input())
    prev_a, prev_b = map(int, input().split())

    ok = True

    for _ in range(n - 1):
        a, b = map(int, input().split())
        if a < prev_a or b < prev_b:
            ok = False
        prev_a, prev_b = a, b

    return "yes" if ok else "no"

# provided samples
assert run("4\n1 0\n2 0\n4 0\n4 1\n") == "yes"
assert run("3\n0 0\n1 0\n0 2\n") == "no"

# minimum size
assert run("1\n5 7\n") == "yes"

# monotone increase both
assert run("3\n0 0\n0 1\n2 3\n") == "yes"

# single drop in second coordinate
assert run("3\n0 0\n1 2\n2 1\n") == "no"

# flat sequence
assert run("4\n2 2\n2 2\n2 2\n2 2\n") == "yes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 snapshot | yes | minimum edge case |
| strictly increasing | yes | normal valid progression |
| second coordinate drop | no | detects invalid decrease |
| constant values | yes | equality allowed |

## Edge Cases

A minimal input with a single snapshot always represents a valid timeline because there is no previous state to violate monotonicity. The algorithm reads the first pair and immediately outputs yes without entering the loop.

A flat sequence where all scores remain identical across snapshots is also valid. Each comparison `a < prev_a or b < prev_b` evaluates to false because equality is allowed. The invariant holds trivially at every step.

A subtle failing case is when one coordinate increases significantly while the other decreases slightly. For example, (1, 10) followed by (5, 3) might look like overall progression, but the second coordinate drop invalidates it immediately. The algorithm catches this at the first violating transition and correctly rejects it.
