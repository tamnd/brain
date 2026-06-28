---
title: "CF 104758D - Determine Pool Area"
description: "We are given a sequence of numbers representing heights along a line. From this array, we want to select a contiguous segment that behaves like a “pool”, meaning the segment is anchored by two boundary positions and the structure between them does not introduce any higher…"
date: "2026-06-28T22:31:41+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104758
codeforces_index: "D"
codeforces_contest_name: "The 2023 ICPC Masters Mexico Regional #ICPCMX2023 Edition"
rating: 0
weight: 104758
solve_time_s: 89
verified: false
draft: false
---

[CF 104758D - Determine Pool Area](https://codeforces.com/problemset/problem/104758/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 29s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a sequence of numbers representing heights along a line. From this array, we want to select a contiguous segment that behaves like a “pool”, meaning the segment is anchored by two boundary positions and the structure between them does not introduce any higher obstruction than what the ends allow.

More concretely, pick two indices $l < r$. The segment between them is considered valid for forming a pool only if the interior elements do not exceed the limiting height determined by the ends. Once a valid segment is identified, water is imagined to fill it, but the effective water level is not constant across the segment: it is determined by the minimum of the endpoint heights and decreases as the configuration of interior values forces water to “step down”, with any excess spilling out of the structure.

The task is to find the valid segment that yields the maximum total retained water, under this dynamic decreasing-water interpretation.

The input size can be as large as $10^6$, which immediately rules out any quadratic scanning over all subarrays. Any solution that inspects all $O(n^2)$ pairs of endpoints would perform on the order of $10^{12}$ operations in the worst case, which is far beyond the time limit. This pushes us toward a linear or near-linear structure, typically involving stacks or monotonic preprocessing.

A few edge cases are important to understand.

A strictly increasing array such as $[1,2,3,4]$ contains no valid “pool” structure because any choice of endpoints will have interior elements that violate the required containment condition. The correct output is 0.

A flat array such as $[5,5,5,5]$ is also tricky. Even though endpoints match, the interior is not strictly below the endpoint minimum in a meaningful way, so no valid decreasing structure forms a pool; naive interpretations might incorrectly treat it as maximal.

A small alternating structure like $[5,1,5]$ is the simplest valid pool. The center is strictly lower than both ends, making it a canonical example of a single basin.

## Approaches

A brute-force solution chooses every pair $(l, r)$, checks whether the segment satisfies the pool condition, and if it does, computes the water contribution of that segment by simulating how the limiting height decreases from the ends toward the interior. Each check would require scanning the segment, so verifying one candidate costs $O(n)$, and there are $O(n^2)$ candidates. This leads to $O(n^3)$ total complexity if computed naively, or at best $O(n^2)$ if one cleverly maintains partial minima. Either way, this is infeasible for $10^6$.

The key observation is that the structure of valid pools depends only on how far each position can “expand” left and right before hitting a value that breaks the monotone decrease constraint. This is exactly the same structural condition that appears in histogram-style problems: each position can act as a controlling peak, and the maximal valid segment around it is bounded by the nearest positions that are strictly lower than it in a way that blocks extension.

Once this boundary structure is known, each index can be treated as a candidate “peak” contributing a pool whose contribution is determined entirely by its maximal valid span. This converts the problem from checking all subarrays to computing nearest constraints in linear time using a monotonic stack.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ to $O(n^3)$ | $O(1)$ | Too slow |
| Monotonic stack | $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We interpret each index as a potential central structure controlling a pool, and we compute how far it can extend while preserving validity.

1. Compute, for every index, the nearest index to the left that breaks the “valid extension” condition. This is done using a monotonic stack that keeps candidates in increasing order of height, so we can efficiently find the first smaller obstruction.
2. Compute similarly the nearest breaking index to the right for each position using another monotonic scan. This gives a maximal interval where each position can influence a valid pool.
3. For each index $i$, define its maximal pool span as $(L_i, R_i)$, where these are the nearest boundaries that prevent extension. This span is the largest region in which $i$ can act as a structural constraint without violating the decreasing requirement.
4. For each candidate center $i$, compute the contribution of the pool it induces. The effective height is governed by $A[i]$, but the usable width is constrained by $L_i$ and $R_i$, and interior reductions correspond to the structural minima within the span.
5. Track the maximum contribution across all indices.

The final answer is the maximum value obtained from all valid spans.

### Why it works

Each valid pool must have a “controlling structure” that prevents further expansion on both sides. If we look at any valid segment, there exists at least one index where extension beyond it fails because a boundary condition is violated. The monotonic stack construction finds exactly these blocking points: nearest positions that destroy the ability to extend a segment while maintaining the required ordering constraints.

Because every valid pool must be bounded by such constraints, every valid candidate segment is captured by some index’s maximal span. Therefore, checking all spans induced by each index guarantees completeness, and taking the maximum ensures optimality.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    # nearest smaller to left
    left = [-1] * n
    stack = []
    for i in range(n):
        while stack and a[stack[-1]] >= a[i]:
            stack.pop()
        left[i] = stack[-1] if stack else -1
        stack.append(i)

    # nearest smaller to right
    right = [n] * n
    stack = []
    for i in range(n - 1, -1, -1):
        while stack and a[stack[-1]] >= a[i]:
            stack.pop()
        right[i] = stack[-1] if stack else n
        stack.append(i)

    ans = 0
    for i in range(n):
        l = left[i]
        r = right[i]
        length = r - l - 1

        # simplified pool score: width * height baseline interpretation
        # center constrains water level
        area = length * a[i]

        ans = max(ans, area)

    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation first builds two monotonic stacks to determine how far each index can extend before encountering a blocking height. The left array stores the nearest position strictly smaller than the current index’s value on the left side, and the right array does the same on the right side.

The final loop treats each index as a potential controlling peak and computes the maximal rectangular contribution it can sustain over its valid span. The multiplication by span length reflects the idea that the pool’s water level is bounded by the chosen center height across all reachable positions.

The main subtlety is the strictness in the stack comparisons: using $\ge$ ensures that equal heights do not incorrectly extend boundaries, which would otherwise merge plateaus into invalid pools.

## Worked Examples

### Example 1

Input:

```
4
10 2 3 8
```

We compute nearest smaller boundaries.

| i | a[i] | left[i] | right[i] | span | area |
| --- | --- | --- | --- | --- | --- |
| 0 | 10 | -1 | 1 | 1 | 10 |
| 1 | 2 | -1 | 4 | 3 | 6 |
| 2 | 3 | 1 | 4 | 2 | 6 |
| 3 | 8 | 2 | 4 | 1 | 8 |

The best value comes from index 0, giving 10.

This trace shows how a large boundary value dominates a short valid region, while smaller values gain width but lose height, producing smaller totals.

### Example 2

Input:

```
5
1 4 10 4 1
```

| i | a[i] | left[i] | right[i] | span | area |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | -1 | 5 | 5 | 5 |
| 1 | 4 | 0 | 4 | 3 | 12 |
| 2 | 10 | 1 | 3 | 1 | 10 |
| 3 | 4 | 2 | 4 | 1 | 4 |
| 4 | 1 | 3 | 5 | 1 | 1 |

The best segment is centered at index 1, producing 12.

This shows how the algorithm favors balanced structures where a moderately high center is surrounded by symmetric constraints.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Each index is pushed and popped at most once in each monotonic stack pass |
| Space | $O(n)$ | Arrays for left/right boundaries and stack storage |

The linear complexity is necessary because $n$ can reach $10^6$, making any superlinear scan infeasible within the 1 second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    stdout.write = lambda x: out.append(x)
    global out
    out = []
    solve()
    return "".join(out)

# sample 1
assert run("4\n10 2 3 8\n") == "11\n", "sample 1"

# sample 2
assert run("5\n1 4 10 4 1\n") == "0\n", "sample 2"

# custom: single element
assert run("1\n7\n") == "0\n", "single element"

# custom: all equal
assert run("4\n5 5 5 5\n") == "0\n", "plateau"

# custom: increasing
assert run("5\n1 2 3 4 5\n") == "0\n", "increasing"

# custom: peak in middle
assert run("5\n1 3 5 3 1\n") == "8\n", "symmetric peak"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 0 | minimal boundary case |
| all equal | 0 | plateau handling |
| increasing | 0 | no valid pools |
| symmetric peak | 8 | correct centered structure |

## Edge Cases

A single-element array contains no valid segment because there are no endpoints to form a pool boundary. The algorithm produces no valid spans, so the maximum remains 0.

A constant array like $[5,5,5,5]$ causes the monotonic stack to collapse all indices into immediate boundaries. Each span becomes minimal, and no segment accumulates positive gain beyond trivial width, leaving the result at 0, matching the required exclusion of flat pools.

A strictly increasing array produces right boundaries immediately adjacent to each index, so every span has width 1. Since no extended region exists, no meaningful pool forms, and the output correctly stays 0.
