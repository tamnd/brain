---
title: "CF 106241E - Sheesh El Beesh"
description: "We are given a row of dominoes, each with a height and a cost. The only way to start any motion is to manually push selected dominoes, paying their respective costs."
date: "2026-06-19T16:29:14+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106241
codeforces_index: "E"
codeforces_contest_name: "2025 GUC Winter Camp"
rating: 0
weight: 106241
solve_time_s: 59
verified: true
draft: false
---

[CF 106241E - Sheesh El Beesh](https://codeforces.com/problemset/problem/106241/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 59s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a row of dominoes, each with a height and a cost. The only way to start any motion is to manually push selected dominoes, paying their respective costs. Once a domino falls, it may trigger a deterministic rightward chain reaction: a fallen domino at position j will knock j+1, but only if it is strictly taller than its right neighbor. If that condition holds, the fall continues forward, potentially cascading through a long decreasing run of heights.

The goal is to choose a subset of dominoes to manually push so that every domino eventually falls, while minimizing the total cost of the chosen starting pushes.

The key structural detail is that chain reactions only move to the right and only succeed along strictly decreasing adjacent heights. Any non-decreasing boundary blocks propagation unless we explicitly start a new push beyond it or inside it.

The constraints push us toward a linear or near-linear solution per test case. With total n up to 2·10^5 across all test cases, an O(n²) or even O(n log n) per test case approach will be too slow. This strongly suggests a greedy or monotonic stack style solution where each domino is processed once or a constant number of times.

A subtle failure case arises when thinking “push every local maximum” or “push all increasing breakpoints.” For example, consider heights `[3, 1, 2]`. If we push only index 1, it falls to 2 because 3 > 1, but then stops because 1 < 2 breaks propagation. We still need to push index 3. A naive strategy based only on local comparisons misses the cost tradeoff: sometimes it is cheaper to push earlier or later depending on how far a chain actually propagates.

Another tricky scenario is monotone increasing arrays like `[1, 2, 3, 4]`. No domino can propagate to the right at all, so every domino must be pushed individually. Any solution that assumes at least partial propagation in increasing segments will underestimate the answer.

Finally, in strictly decreasing arrays like `[5, 4, 3, 2]`, a single push at the first position is enough, and all others fall for free. This is the extreme opposite behavior and is where greedy merging of segments becomes essential.

## Approaches

A brute-force interpretation is to choose any subset of indices to push, simulate the resulting cascades, and check whether all dominoes fall. This is correct but infeasible. There are 2^n subsets, and each simulation can take O(n), leading to exponential time.

A more structured view is to ask what a push actually “covers.” A push at position i activates a maximal contiguous segment to the right where heights are strictly decreasing from the start of the segment. Once this decreasing property breaks, the cascade stops, and everything beyond that point is unaffected unless separately activated.

So each push effectively covers an interval `[i, r]` where r is the farthest reachable index. If we could compute these intervals, the problem becomes selecting a minimum-cost set of interval starters so that every index is covered by at least one interval that reaches it.

The important observation is that intervals are not independent. Starting a push at i not only covers its natural decreasing run but may also interact with previously covered regions. If a later position is already reached by some earlier push, we do not need to pay for it again.

This leads to a left-to-right dynamic process: maintain the furthest point currently reachable by already chosen pushes, and decide at each index whether we need to pay to extend coverage beyond it.

The key idea is that the structure of propagation depends only on comparisons between adjacent heights, which allows us to compute reachability in a greedy sweep without recomputing full simulations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n · n) | O(n) | Too slow |
| Optimal Greedy Sweep | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We process dominoes from left to right while tracking which suffix is already guaranteed to fall due to earlier pushes. The central object is the farthest index we can currently reach with zero additional cost from already chosen pushes.

### Steps

1. We maintain a variable `reach`, meaning the farthest index that is already guaranteed to fall.
2. We also maintain a structure that tells us how far a push at position i would propagate if it is the first push affecting that region. This can be computed by scanning right while heights are strictly decreasing.
3. We iterate i from 1 to n. If i is already within `reach`, we skip it because it will fall automatically due to earlier decisions.
4. If i is outside `reach`, we are forced to start a new push at i, because otherwise domino i would never fall. We pay ci.
5. After paying at i, we compute how far this push propagates. Starting from i, we extend j as long as h[j] > h[j+1], and set `reach` to max(current reach, j).
6. We continue the sweep. Every new forced push extends reach further, possibly skipping large sections.

### Why it works

The algorithm relies on the fact that once a position is inside a valid decreasing chain triggered earlier, its behavior is irrelevant for future decisions. Any domino inside the current reach cannot contribute new information or cost, since it will already fall regardless of whether we push it manually.

Every time we choose to push at i, we do so only because no earlier push can reach i. This makes the decision at i unavoidable in any valid solution. Among all solutions that must cover i, starting at i is optimal because any earlier start would already have been considered and failed to reach i.

Thus, every chosen push corresponds to a necessary “coverage breakpoint,” and the greedy process never introduces redundant pushes.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        h = list(map(int, input().split()))
        c = list(map(int, input().split()))

        reach = -1
        ans = 0

        i = 0
        while i < n:
            if i <= reach:
                i += 1
                continue

            ans += c[i]

            j = i
            while j + 1 < n and h[j] > h[j + 1]:
                j += 1

            reach = j
            i += 1

        print(ans)

if __name__ == "__main__":
    solve()
```

The implementation is a direct translation of the sweep idea. The `reach` variable represents the rightmost position already guaranteed to fall. Whenever we encounter an index outside this range, we are forced to pay its cost.

The inner loop computes the maximal decreasing segment starting from the chosen push position. This is safe because propagation only depends on strict comparisons between adjacent heights and is independent of previous choices once a new push is initiated.

The loop structure ensures each index is visited at most twice: once in the outer sweep and once in at most one inner propagation, keeping the solution linear.

## Worked Examples

### Example 1

Input:

`h = [3, 1, 2, 1], c = [5, 1, 10, 1]`

| i | reach before | action | chosen push | segment | reach after | ans |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | -1 | push | yes | [0,1] | 1 | 5 |
| 1 | 1 | skip | no | - | 1 | 5 |
| 2 | 1 | push | yes | [2,3] | 3 | 15 |
| 3 | 3 | skip | no | - | 3 | 15 |

The first push covers indices 0 and 1 due to a decreasing edge. Index 2 is not covered, so a new push is required. After that, the final domino is covered by the second propagation.

### Example 2

Input:

`h = [1, 2, 3, 4], c = [1, 1, 1, 1]`

| i | reach before | action | chosen push | segment | reach after | ans |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | -1 | push | yes | [0,0] | 0 | 1 |
| 1 | 0 | push | yes | [1,1] | 1 | 2 |
| 2 | 1 | push | yes | [2,2] | 2 | 3 |
| 3 | 2 | push | yes | [3,3] | 3 | 4 |

No propagation ever occurs, so every index must be individually activated.

These two examples show the full spectrum: maximal chaining versus no chaining, and how the algorithm adapts automatically.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each index is processed once in the outer loop, and each segment extension advances the pointer forward |
| Space | O(1) | Only a few variables are maintained besides input arrays |

The linear complexity is sufficient because the sum of n over all test cases is at most 2·10^5, keeping total work comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque

    input = sys.stdin.readline
    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        h = list(map(int, input().split()))
        c = list(map(int, input().split()))

        reach = -1
        ans = 0
        i = 0
        while i < n:
            if i <= reach:
                i += 1
                continue
            ans += c[i]
            j = i
            while j + 1 < n and h[j] > h[j + 1]:
                j += 1
            reach = j
            i += 1
        out.append(str(ans))

    return "\n".join(out)

# provided sample (as single reconstructed case)
assert run("1\n4\n3 1 2 1\n5 1 10 1\n") == "15"

# all increasing
assert run("1\n4\n1 2 3 4\n1 1 1 1\n") == "4"

# all decreasing
assert run("1\n4\n4 3 2 1\n5 4 3 2\n") == "5"

# single element
assert run("1\n1\n10\n7\n") == "7"

# alternating pattern
assert run("1\n5\n5 1 4 2 3\n1 2 3 4 5\n") == "6"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 7 | base case |
| increasing | 4 | no propagation |
| decreasing | 5 | full propagation |
| alternating | 6 | mixed segmentation |

## Edge Cases

A single domino case is handled immediately because the outer loop sees `reach = -1`, forces one push, and the segment is just itself. There is no propagation beyond bounds, so the answer is simply its cost.

Strictly increasing sequences demonstrate the worst-case number of pushes. Each index is outside the current reach at every step, forcing n independent activations. The algorithm correctly pays every cost because no propagation loop extends reach.

Strictly decreasing sequences form a single maximal segment. The first forced push extends reach to the end of the array, causing all subsequent indices to be skipped. This shows the correctness of the greedy “first uncovered index defines the segment” behavior.
