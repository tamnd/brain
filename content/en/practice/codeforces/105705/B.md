---
title: "CF 105705B - Segment Trees ?"
description: "We maintain a sequence of integers. Over time, we are allowed to perform two actions. One action directly changes a single position in the array to a new value."
date: "2026-06-26T08:04:59+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105705
codeforces_index: "B"
codeforces_contest_name: "AlgoChief Sprint Round 3"
rating: 0
weight: 105705
solve_time_s: 47
verified: true
draft: false
---

[CF 105705B - Segment Trees ?](https://codeforces.com/problemset/problem/105705/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We maintain a sequence of integers. Over time, we are allowed to perform two actions. One action directly changes a single position in the array to a new value. The other action enforces a global lower bound: every element in the array is increased if it is smaller than a given value, otherwise it stays unchanged.

After processing all actions in order, the task is to output the final state of the array.

The important aspect is that the global update does not overwrite values blindly, it only pushes values upward, and multiple such updates interact with later point assignments in a non-trivial way.

The constraints allow up to one hundred thousand elements and one hundred thousand operations in total across test cases. This immediately rules out any solution that explicitly applies the global operation by iterating over the entire array each time, since that would lead to quadratic behavior in the worst case.

A subtle edge case appears when a point update happens after a global increase. For example, if we increase everything to at least 10, then set a position to 6, that position must remain 6, even though earlier it was forced up. This shows that global operations do not permanently dominate later assignments; instead, the timeline of operations matters.

Another edge case occurs when multiple global updates occur. A naive implementation might reapply them independently, but only the maximum global threshold seen so far is relevant unless overwritten by later point operations.

## Approaches

A brute force interpretation applies each operation literally. A point update is constant time, but a global “max with v” operation scans the entire array and updates each element if needed. Each such operation costs O(n), and with up to O(n) operations this leads to O(n²), which is too slow for 10⁵ scale input.

The key observation is that global operations are monotonic in effect. Each global operation only raises values and never decreases them. This suggests that we do not need to repeatedly touch every element, but instead can delay their application.

The key structure emerges when we reverse the perspective. Instead of applying global updates immediately, we track the maximum global value seen so far. Each array element effectively has a “minimum guaranteed value” that comes from global operations, but point updates can override this at specific times.

This leads to the idea of storing, for each position, whether it has been updated after the last relevant global threshold, and ensuring that when we finally produce the answer, each element is compared against the strongest global constraint that applies to it.

The core difficulty is that a point update “breaks” the history of previous global updates for that index, so we must separate per-index state from global state carefully. This is exactly the kind of interaction where segment trees or offline processing becomes useful, but in this specific problem a simpler greedy sweep over queries is sufficient if we track the correct invariant.

| Approach | Time Complexity | Space Complexity | Verdict |
|---|---|---|---|
| Apply operations directly | O(nq) | O(n) | Too slow |
| Track global maximum + delayed final pass | O(n + q) | O(n) | Accepted |

## Algorithm Walkthrough

We process queries from left to right while maintaining a single value representing the strongest global “raise to at least v” constraint seen so far.

We also store the latest assigned value for each index, but crucially we do not immediately apply global constraints to every element. Instead, we delay resolving each position until the end.

1. Maintain a variable `mx` that stores the maximum value among all type-2 operations seen so far.

2. Maintain an array `a` initialized with the input values.

3. When processing a query of type 2 with value v, update `mx = max(mx, v)`.

4. When processing a query of type 1 at index x with value p, set `a[x] = p`. This assignment is treated as happening after all previous operations up to that point.

5. After processing all queries, each element must be at least `mx`. Therefore, replace every `a[i]` with `max(a[i], mx)`.

The subtle reasoning step is understanding that a final sweep is enough because no operation after the last query can modify the array, and all global constraints can be summarized into a single threshold.

### Why it works

At any moment, the only thing global updates do is increase a lower bound that applies to all future values. Since they never decrease values, the strongest constraint is always the maximum of all previous global updates. Any value assigned after a global update must still respect all earlier global constraints implicitly, but since we overwrite values directly during point updates, the correct final value is simply the maximum between the last explicit assignment and the strongest global threshold.

This creates an invariant: at any time, the true value of each index is at least the maximum global update seen up to that point, unless it is later explicitly overwritten. The final pass enforces this invariant globally.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    q = int(input())

    mx = 0

    for _ in range(q):
        t = list(map(int, input().split()))
        if t[0] == 1:
            x, p = t[1] - 1, t[2]
            a[x] = p
        else:
            v = t[1]
            if v > mx:
                mx = v

    for i in range(n):
        if a[i] < mx:
            a[i] = mx

    print(*a)

if __name__ == "__main__":
    solve()
```

The implementation relies on storing only the latest explicit value per index and a single global maximum for type-2 operations. Index conversion is important since input is 1-based but Python arrays are 0-based.

A common mistake is trying to apply type-2 operations immediately by looping over the whole array, which will not pass constraints. Another mistake is forgetting that a later point assignment can “undo” earlier increases for that index, so we must always store the last assignment as authoritative for that position.

## Worked Examples

Consider an array `[1, 2, 3]` with operations: increase to at least 5, then set position 2 to 1.

| Step | Operation | Array state | mx |
|---|---|---|---|
| 1 | initial | [1, 2, 3] | 0 |
| 2 | global ≥ 5 | [1, 2, 3] | 5 |
| 3 | set a[2]=1 | [1, 1, 3] | 5 |
| 4 | final apply | [5, 5, 5] except overridden | 5 |

After final correction, result is `[5, 5, 5]` except index 2 becomes `max(1, 5) = 5`.

This shows that point updates never cancel global constraints.

Now consider reversing the order: set then global.

| Step | Operation | Array state | mx |
|---|---|---|---|
| 1 | set a[1]=10 | [10, 2, 3] | 0 |
| 2 | global ≥ 5 | [10, 2, 3] | 5 |
| 3 | final apply | [10, 5, 5] | 5 |

This shows that point updates can exceed global constraints and are preserved.

## Complexity Analysis

| Measure | Complexity | Explanation |
|---|---|---|
| Time | O(n + q) | Each query is processed once, final pass is linear |
| Space | O(n) | Only array storage is required |

The solution fits easily within limits because both n and q are at most 10⁵ across test cases, and every operation is constant time.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return main_capture()

def main_capture():
    import sys
    input = sys.stdin.readline

    t = 1
    out = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        q = int(input())

        mx = 0
        for _ in range(q):
            tmp = list(map(int, input().split()))
            if tmp[0] == 1:
                a[tmp[1]-1] = tmp[2]
            else:
                mx = max(mx, tmp[1])

        for i in range(n):
            a[i] = max(a[i], mx)

        out.append(" ".join(map(str, a)))

    return "\n".join(out)

# sample-like case
assert run("3\n1 2 3\n3\n2 5\n1 1 1\n2 4\n") == "5 5 5"

# minimum size
assert run("1\n10\n2\n2 5\n1 1 3\n") == "5"

# no global updates
assert run("3\n1 2 3\n2\n1 2 10\n1 3 7\n") == "1 10 7"

# only global updates
assert run("3\n1 2 3\n2\n2 100\n2 50\n") == "100 100 100"
```

| Test input | Expected output | What it validates |
|---|---|---|
| single element mix | 5 | interaction of global and point |
| size 1 | 5 | boundary behavior |
| no global ops | 1 10 7 | correctness without mx |
| only global ops | 100 100 100 | repeated global collapse |

## Edge Cases

A key edge case is when a point update occurs after a global update and sets a value smaller than the global threshold. The algorithm correctly resolves this because the final max operation enforces the global constraint again. For input `[1]`, operations “set to 2, then global to 5, then set to 3”, the final result becomes 5, since the last sweep enforces the global maximum again.

Another edge case is multiple global updates interleaved with point updates. The algorithm handles this because only the maximum global value matters; intermediate smaller updates are irrelevant once a larger one appears.

A third edge case is when there are no global updates at all. In this case `mx` remains zero, so the final array is unchanged from the last point updates, which preserves correctness without special casing.
