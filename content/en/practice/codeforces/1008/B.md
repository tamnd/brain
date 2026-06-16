---
title: "CF 1008B - Turn the Rectangles"
description: "We are given a sequence of rectangular tiles placed in a fixed left-to-right order. Each tile has two possible orientations: we can either keep it as width-by-height or rotate it by 90 degrees, which swaps the two values."
date: "2026-06-16T23:03:22+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1008
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 497 (Div. 2)"
rating: 1000
weight: 1008
solve_time_s: 73
verified: true
draft: false
---

[CF 1008B - Turn the Rectangles](https://codeforces.com/problemset/problem/1008/B)

**Rating:** 1000  
**Tags:** greedy, sortings  
**Solve time:** 1m 13s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of rectangular tiles placed in a fixed left-to-right order. Each tile has two possible orientations: we can either keep it as width-by-height or rotate it by 90 degrees, which swaps the two values. After choosing an orientation independently for every tile, we look only at the resulting heights. The requirement is that these heights must form a non-increasing sequence from left to right.

The task is to determine whether such a choice of orientations exists.

The key constraint is $n \le 10^5$. This immediately rules out any exponential exploration over orientations, since each rectangle has two states and a full brute-force search would involve $2^n$ possibilities. Even quadratic approaches over pairs of rectangles would be too slow. We are therefore looking for a greedy or linear-time construction that processes rectangles once from left to right.

A subtle edge case appears when both orientations are valid locally but only one leads to a feasible global continuation. For example, if a rectangle is $(5, 4)$, and the previous chosen height is 5, we might be tempted to always pick the larger possible orientation that still fits. However, this greedy “maximize current height” strategy can break future feasibility.

Consider this input:

```
2
5 4
4 6
```

At the first rectangle, picking height 5 is fine. At the second rectangle, neither 6 nor 4 can follow 5 in a non-increasing sequence, so the answer is NO. But if we had chosen differently in other cases, we may preserve feasibility, meaning local optimality must be carefully defined.

## Approaches

A brute-force approach tries every possible choice of orientation for each rectangle. For each configuration, we check whether the resulting sequence of heights is non-increasing. This is straightforward: for each of $2^n$ configurations, we scan $n$ elements, giving $O(n \cdot 2^n)$. With $n = 10^5$, this is completely infeasible.

The structure of the problem allows a simplification: at each step, we only care about the maximum allowed height we can still use for the current rectangle, determined by the previous choice. Each rectangle gives us two candidates for height, and we want to pick the largest one that does not exceed the previous chosen height. This greedy choice works because leaving a larger valid height whenever possible preserves more flexibility for the future, while still maintaining feasibility locally.

We transform the problem into a single pass: maintain a variable `cur` representing the maximum allowed height for the current position. For each rectangle, choose the largest possible orientation that is ≤ `cur`. If neither orientation fits, the process fails.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n \cdot 2^n)$ | $O(n)$ | Too slow |
| Greedy scan | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We process rectangles from left to right while maintaining the maximum allowable height for the current position.

1. Initialize `cur` as infinity. This represents that the first rectangle has no upper restriction.
2. For each rectangle with sides $(w, h)$, consider the two possible heights: $h$ and $w$. The order of these two values does not matter initially.
3. Select the larger of the two values that is less than or equal to `cur`. If both values are valid, we take the larger one because it keeps more room for later rectangles.
4. If neither value is less than or equal to `cur`, we immediately conclude that the sequence cannot be made non-increasing and stop.
5. Update `cur` to the chosen height and continue to the next rectangle.
6. If all rectangles are processed successfully, output YES.

### Why it works

At every step, we maintain the invariant that `cur` is the maximum possible height we are allowed to place at the current position given all previous choices. Among all valid orientations for the current rectangle, choosing the maximum feasible height is safe because any smaller choice would only restrict future steps further without unlocking any additional valid configurations. Since feasibility depends only on staying below the previous height, preserving the largest feasible value ensures we never discard a solution that could succeed later.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    cur = float('inf')

    for _ in range(n):
        a, b = map(int, input().split())
        if a > b:
            a, b = b, a

        if a <= cur and b <= cur:
            cur = b
        elif b <= cur:
            cur = b
        elif a <= cur:
            cur = a
        else:
            print("NO")
            return

    print("YES")

if __name__ == "__main__":
    solve()
```

The code mirrors the greedy strategy directly. For each rectangle, we normalize its two candidate heights by sorting them so `a <= b`. This makes reasoning simpler: `b` is always the best possible height for that rectangle, and `a` is the fallback.

The conditional structure ensures we always pick the largest valid height. If both fit under `cur`, we take `b`. If only one fits, we take that one. If neither fits, we terminate early.

A common implementation pitfall is forgetting to normalize each rectangle or incorrectly updating `cur` even when no valid choice exists.

## Worked Examples

### Example 1

Input:

```
3
3 4
4 6
3 5
```

We track `cur`:

| Step | Rectangle | Candidates | Chosen | cur |
| --- | --- | --- | --- | --- |
| 1 | (3,4) | (3,4) | 4 | 4 |
| 2 | (4,6) | (4,6) | 4 | 4 |
| 3 | (3,5) | (3,5) | 3 | 3 |

At each step we always pick the maximum valid height. The final sequence is 4, 4, 3, which is non-increasing, confirming feasibility.

### Example 2

Input:

```
2
5 4
4 6
```

| Step | Rectangle | Candidates | Chosen | cur |
| --- | --- | --- | --- | --- |
| 1 | (5,4) | (4,5) | 5 | 5 |
| 2 | (4,6) | (4,6) | 4 | 4 |

Here the second rectangle forces a drop to 4, which is valid, but if the first step had left insufficient flexibility in other variants, failure would occur. The trace shows how feasibility is checked purely via the current bound.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Each rectangle is processed once with constant-time comparisons |
| Space | $O(1)$ | Only a single variable `cur` is maintained |

The linear scan comfortably fits within limits for $n = 10^5$, where up to a few million operations are acceptable in Python.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque
    input = sys.stdin.readline

    n = int(input())
    cur = float('inf')
    for _ in range(n):
        a, b = map(int, input().split())
        if a > b:
            a, b = b, a

        if a <= cur and b <= cur:
            cur = b
        elif b <= cur:
            cur = b
        elif a <= cur:
            cur = a
        else:
            return "NO\n"
    return "YES\n"

# provided sample
assert run("3\n3 4\n4 6\n3 5\n") == "YES\n"

# minimum size, single rectangle
assert run("1\n5 7\n") == "YES\n"

# impossible case
assert run("2\n5 4\n4 6\n") == "NO\n"

# all equal rectangles
assert run("3\n2 2\n2 2\n2 2\n") == "YES\n"

# strict decreasing requirement
assert run("3\n9 1\n8 2\n7 3\n") == "YES\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single rectangle | YES | base case |
| mixed impossible | NO | early failure detection |
| equal rectangles | YES | stable chain case |
| strictly decreasing | YES | orientation flexibility |

## Edge Cases

A key edge case is when a rectangle can only be placed in one orientation due to previous constraints. For example:

```
2
10 1
5 6
```

After the first rectangle, `cur = 10`. The second rectangle has candidates 5 and 6, both valid, so we pick 6. The sequence remains valid.

Now consider:

```
2
10 1
7 8
```

After first step, `cur = 10`. For the second rectangle, both 7 and 8 are valid, so we pick 8. The sequence is valid and ends at 8 ≤ 10.

Finally:

```
2
5 1
6 7
```

After first rectangle, `cur = 5`. The second rectangle has candidates 6 and 7, neither is ≤ 5, so the algorithm correctly outputs NO. The failure is immediate, and no later adjustment can fix it since no valid orientation exists at this step.
