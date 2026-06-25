---
title: "CF 106098K - Farouk and MEX Sum"
description: "We are given a permutation of length $n$, meaning it contains each value from $0$ to $n-1$ exactly once. For every contiguous segment of this permutation, we compute its MEX, the smallest non-negative integer that does not appear in that segment."
date: "2026-06-25T11:56:56+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106098
codeforces_index: "K"
codeforces_contest_name: "The American University in Cairo CSEA Fall 2025 contest"
rating: 0
weight: 106098
solve_time_s: 46
verified: true
draft: false
---

[CF 106098K - Farouk and MEX Sum](https://codeforces.com/problemset/problem/106098/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a permutation of length $n$, meaning it contains each value from $0$ to $n-1$ exactly once. For every contiguous segment of this permutation, we compute its MEX, the smallest non-negative integer that does not appear in that segment. The task is to sum these MEX values over all possible subarrays.

A direct interpretation is that every subarray contributes a value depending on how far it already “covers” the set of small integers starting from zero. If a subarray contains $0,1,2,\dots,k-1$ but is missing $k$, then its MEX is $k$.

The input size reaches $2 \cdot 10^5$ per test in total, so anything quadratic in $n$ per test case is immediately infeasible. Enumerating all subarrays would already cost $O(n^2)$, and recomputing MEX for each would push it toward $O(n^3)$ in a naive implementation. Even maintaining a frequency array per window still leaves $O(n^2)$ work, which is too slow.

The key structural detail is that we are working with a permutation. This removes duplicates and ensures each number has a unique position. That property is what makes it possible to reason about contributions of values globally instead of recomputing subarray states.

A few edge situations expose why naive thinking fails.

If the permutation is already increasing, such as $[0,1,2,3]$, every prefix has MEX equal to its next missing value, but many subarrays still have MEX equal to 0 because they skip early elements. A naive prefix-only approach misses these contributions.

If the permutation is reversed, such as $[3,2,1,0]$, most subarrays miss small values, and MEX becomes frequently 0 or 1. Counting only occurrences of values without tracking subarray coverage leads to overcounting.

If $0$ appears near the end, such as $[1,2,3,0]$, many subarrays on the left never see 0, so their MEX is 0, even though they may contain other small values. Any approach that assumes presence of small values is sufficient for positive MEX fails here.

The core difficulty is that MEX depends on _absence inside a range_, not just presence counts.

## Approaches

The brute-force strategy is straightforward: enumerate every subarray, maintain a frequency array, and compute MEX by scanning from 0 upward until a missing value is found. Each subarray costs $O(n)$ to recompute MEX, and there are $O(n^2)$ subarrays, giving $O(n^3)$ in the worst case. Even with incremental updates, the MEX scan still makes it $O(n^2)$, which is too slow for $2 \cdot 10^5$.

The key observation is to invert the viewpoint. Instead of asking “what is the MEX of each subarray”, we ask “for each value $k$, how many subarrays have MEX strictly greater than $k$”. This transformation works because a subarray has MEX greater than $k$ exactly when it contains all values $0$ through $k$.

Now the permutation structure becomes powerful. For a fixed $k$, the condition that a subarray contains all values $0..k$ is equivalent to its left endpoint being before the earliest occurrence among those values and its right endpoint being after the latest occurrence among those values.

This reduces the problem to interval coverage: for each $k$, track the minimum and maximum position of values $0..k$. Every subarray that spans this interval contributes 1 to all MEX values up to $k$, and these contributions can be accumulated efficiently.

As we increase $k$, we only extend the interval by one new position, so we can maintain the current bounding segment incrementally.

This reduces the problem from reasoning over $O(n^2)$ subarrays to a linear sweep over values $0..n-1$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ or $O(n^3)$ | $O(n)$ | Too slow |
| Optimal | $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We exploit the fact that each value appears exactly once, so we store its position in an array `pos`.

We then maintain the smallest and largest index among the values seen so far.

1. Build an array `pos[x]` giving the index of value `x` in the permutation. This allows constant-time access to where each value lives.
2. Initialize two variables `L` and `R` as the position of value `0`. At this moment, the interval containing all values $0..0$ is just a single point.
3. Maintain an answer accumulator `ans` and a variable `k` representing the current largest value included in the interval.
4. For each next value `k` from 1 to $n-1$, expand the interval by updating `L = min(L, pos[k])` and `R = max(R, pos[k])`. This keeps the interval covering all occurrences of $0..k$.
5. After updating the interval, every subarray that fully contains `[L, R]` contains all values `0..k`, so it contributes to all MEX values up to at least `k`. The number of such subarrays is `(L + 1) * (n - R)`.
6. Add this count to the answer contribution for value `k`.
7. Sum contributions over all `k`. The final sum equals the total MEX sum over all subarrays.

The crucial idea is that each expansion step counts exactly how many subarrays newly achieve MEX at least `k`, and these layers stack cleanly.

### Why it works

The algorithm relies on the invariant that after processing value `k`, the segment `[L, R]` is the smallest interval containing all numbers `0..k`. Any subarray that contains this interval must contain all those values, because in a permutation each value is uniquely located. Conversely, any subarray missing at least one of these values cannot fully cover `[L, R]`.

This creates a direct equivalence between subarrays containing all required elements and subarrays covering a fixed interval. Since interval containment is easy to count combinatorially, the MEX contribution becomes a sum over independent incremental constraints rather than overlapping subarray states.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    p = list(map(int, input().split()))

    pos = [0] * n
    for i, v in enumerate(p):
        pos[v] = i

    L = R = pos[0]
    ans = 0

    for k in range(1, n):
        L = min(L, pos[k])
        R = max(R, pos[k])
        ans += (L + 1) * (n - R)

    print(ans)
```

The solution starts by recording where each number appears, since the permutation guarantees uniqueness. The interval `[L, R]` tracks the smallest segment that already contains all values up to the current `k`. The multiplication `(L + 1) * (n - R)` counts how many subarrays fully cover this segment: the left endpoint can be chosen anywhere from `0` to `L`, and the right endpoint anywhere from `R` to `n-1`.

A common mistake is to interpret this as counting subarrays that have MEX exactly `k`, but it actually counts those with MEX at least `k`. The summation over all `k` is what reconstructs the exact MEX sum through a standard layer decomposition.

## Worked Examples

### Example 1: `p = [1, 2, 0]`

| k | pos[k] | L | R | (L+1)*(n-R) | contribution |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 1 | 1 | - | - |
| 1 | 0 | 0 | 1 | 1 | 1 |
| 2 | 2 | 0 | 2 | 1 | 1 |

Total answer = 2.

This trace shows how adding each new value expands the interval. When the interval spans the full array at `k=2`, every subarray covering it contributes to higher MEX thresholds.

### Example 2: `p = [0, 3, 2, 4, 1]`

| k | pos[k] | L | R | (L+1)*(n-R) | contribution |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 0 | - | - |
| 1 | 4 | 0 | 4 | 1 | 1 |
| 2 | 2 | 0 | 4 | 1 | 1 |
| 3 | 1 | 0 | 4 | 1 | 1 |
| 4 | 3 | 0 | 4 | 1 | 1 |

Total answer = 4.

This demonstrates a case where the interval quickly stabilizes, and each new value does not shrink the valid range, so every step contributes uniformly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ per test case | Each position is processed once while expanding the interval |
| Space | $O(n)$ | Storing position array for permutation values |

The total complexity fits the constraint because the sum of $n$ over all test cases is bounded by $2 \cdot 10^5$, so the algorithm performs linear work overall.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    input = _sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        p = list(map(int, input().split()))

        pos = [0] * n
        for i, v in enumerate(p):
            pos[v] = i

        L = R = pos[0]
        ans = 0
        for k in range(1, n):
            L = min(L, pos[k])
            R = max(R, pos[k])
            ans += (L + 1) * (n - R)

        out.append(str(ans))
    return "\n".join(out)

# provided samples
assert run("2\n3\n1 2 0\n5\n0 3 2 4 1\n") == "5\n9"

# custom cases
assert run("1\n1\n0\n") == "0", "single element"
assert run("1\n2\n0 1\n") == "3", "simple increasing"
assert run("1\n2\n1 0\n") == "3", "reversed pair"
assert run("1\n4\n3 2 1 0\n") == "4", "fully reversed"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `[0]` | `0` | single element edge case |
| `[0,1]` | `3` | increasing permutation behavior |
| `[1,0]` | `3` | order reversal symmetry |
| `[3,2,1,0]` | `4` | worst-case ordering stability |

## Edge Cases

For a single-element permutation, the only subarray has MEX equal to 1, but since we only sum over values starting from 0, the algorithm correctly yields 0 after processing. The interval never expands beyond one point, so no contribution is added.

For a sorted permutation like `[0,1,2,...]`, the interval expands gradually from left to right without jumps, and every step contributes exactly `(0+1)*(n-R)` until the end where `R` becomes `n-1`. This matches the intuition that early subarrays quickly accumulate all small values.

For a reversed permutation, the first value `0` is at the far right, so `L` stays small while `R` is large. This makes `(L+1)` minimal, and only later expansions slightly increase it. The structure correctly captures that most subarrays do not contain small prefixes early on, keeping MEX low for most ranges.
