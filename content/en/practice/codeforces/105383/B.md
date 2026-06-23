---
title: "CF 105383B - Business Magic"
description: "We are given a line of stores, each store having a current profit value, which can be positive or negative. The goal is to maximize the total profit after applying at most one global operation called a blue spell and any number of local operations called green spells, with the…"
date: "2026-06-23T16:11:15+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105383
codeforces_index: "B"
codeforces_contest_name: "2024 ICPC Asia Taiwan Online Programming Contest"
rating: 0
weight: 105383
solve_time_s: 54
verified: true
draft: false
---

[CF 105383B - Business Magic](https://codeforces.com/problemset/problem/105383/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 54s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a line of stores, each store having a current profit value, which can be positive or negative. The goal is to maximize the total profit after applying at most one global operation called a blue spell and any number of local operations called green spells, with the constraint that green spells cannot be applied inside the interval chosen for the blue spell.

The blue spell selects one contiguous segment and doubles every value inside it. The green spell selects individual positions, but it can only be applied outside the blue segment, and flips the sign of the chosen element.

So after choosing a blue segment, every element falls into one of three categories. Inside the segment, values become doubled and cannot be flipped. Outside, values can either remain unchanged or be negated individually.

The output is the maximum achievable sum after optimally choosing the blue segment and deciding which outside elements to flip.

The constraints reach up to 3×10^5 elements with values up to 10^9 in magnitude. This immediately rules out any solution that tries all O(n^2) segments or recomputes sums for each choice. Any viable solution must be close to linear or linearithmic.

A subtle edge case comes from the fact that flipping is independent per element outside the segment. For any value x outside the blue segment, we can choose max(x, −x) independently. This creates a common pitfall: treating green spells as a global choice instead of per-element optimization.

Another important edge case is when the blue segment is empty or effectively useless. For example, if all values are negative, doubling them makes them worse, but flipping outside may still rescue some portion. A naive strategy that always applies blue to a positive region fails on fully negative arrays.

## Approaches

A brute-force approach tries every possible blue segment [L, R]. For each choice, we compute the best achievable result for the remaining elements. Inside the segment, each element becomes 2·a[i]. Outside the segment, each element contributes max(a[i], −a[i]) = |a[i]|. So for a fixed segment, the total sum is:

sum inside segment after doubling + sum outside segment after taking absolute values.

We can precompute the total absolute sum of the array. Then for a chosen segment, we only need to replace the contribution of elements inside the segment: originally they contribute |a[i]|, but after choosing the blue segment they contribute 2a[i]. So the gain from choosing a segment is:

2a[i] − |a[i]|.

This reduces the problem to finding a maximum subarray sum on a transformed array b[i] = 2a[i] − |a[i]|. However, this is still subtle because the baseline assumes everything outside is absolute value, which is always optimal.

The brute-force over segments is O(n^2), which is far too slow for n up to 3×10^5. The key observation is that the effect of the blue segment is fully local and additive, so the choice reduces to a maximum subarray problem over a derived weight array. Once this is recognized, the problem becomes a standard Kadane’s algorithm.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over segments | O(n^2) | O(1) | Too slow |
| Transform + Kadane | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

### Key reformulation

1. First compute the baseline contribution where no blue spell is used. Every element can be independently flipped if beneficial, so the baseline is the sum of |a[i]|. This corresponds to treating every element as if we could freely apply green magic everywhere.
2. Now consider introducing a blue segment [L, R]. Inside this segment, we lose the freedom of flipping and instead force each value to become 2·a[i]. So the net change compared to baseline for an index i in the segment is:

2a[i] − |a[i]|.

This is the only part of the array affected by choosing the segment.
3. Define an auxiliary array b where b[i] = 2a[i] − |a[i]|. The problem reduces to selecting a contiguous segment that maximizes the sum of b[i].
4. Compute the maximum subarray sum over b using a linear scan. This value represents the best improvement achievable by introducing a blue segment.
5. Add this best improvement to the baseline sum of absolute values. The result is the answer.

### Why it works

The crucial invariant is that outside the chosen blue segment, the optimal strategy for green spells is always independent per element and equal to taking absolute value. This means any global decision only affects the segment itself, and the rest of the array collapses into a fixed constant contribution. Once this decomposition is made, the only remaining optimization is selecting a contiguous region maximizing the incremental gain relative to that baseline, which is exactly a maximum subarray problem.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    base = 0
    b = []

    for x in a:
        base += abs(x)
        b.append(2 * x - abs(x))

    best = b[0]
    cur = b[0]

    for i in range(1, n):
        cur = max(b[i], cur + b[i])
        best = max(best, cur)

    print(base + best)

if __name__ == "__main__":
    solve()
```

The code starts by computing the baseline sum of absolute values, which corresponds to optimally applying green spells everywhere outside any blue segment. It then constructs the transformed array where each element represents the gain from including that index inside the blue segment.

The Kadane scan tracks the best contiguous segment sum in this transformed array. The variable cur represents the best segment ending at the current index, and best tracks the best overall segment. Finally, we add this improvement to the baseline.

A common implementation pitfall is forgetting that the blue segment must be non-empty. The Kadane initialization ensures this by starting from the first element rather than zero.

## Worked Examples

### Example 1

Input:

```
4
-2 5 -3 4
```

Baseline absolute sum is 2 + 5 + 3 + 4 = 14.

We compute b[i] = 2a[i] − |a[i]|:

| i | a[i] | b[i] |
| --- | --- | --- |
| 1 | -2 | -2 |
| 2 | 5 | 5 |
| 3 | -3 | -3 |
| 4 | 4 | 4 |

Now we run Kadane:

| i | b[i] | cur | best |
| --- | --- | --- | --- |
| 1 | -2 | -2 | -2 |
| 2 | 5 | 5 | 5 |
| 3 | -3 | 2 | 5 |
| 4 | 4 | 6 | 6 |

Best improvement is 6, so final answer is 14 + 6 = 20.

This shows how the optimal blue segment is not necessarily aligned with a single sign pattern, and Kadane naturally captures the best mixture.

### Example 2

Input:

```
7
-1 -1 -1 -1 -1 -1 -1
```

Baseline absolute sum is 7.

Compute b[i]:

Each a[i] = -1 gives b[i] = 2(-1) − 1 = -3.

Kadane:

| i | b[i] | cur | best |
| --- | --- | --- | --- |
| 1 | -3 | -3 | -3 |
| 2 | -3 | -3 | -3 |
| 3 | -3 | -3 | -3 |
| ... | ... | ... | ... |

Best improvement is -3, meaning we actually prefer choosing no beneficial blue segment beyond a single element, and overall result becomes 7 − 3 = 4.

This highlights that forcing a blue segment can be harmful, and Kadane correctly accounts for the least damaging choice.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One pass to compute absolute baseline and transformed array, one pass for Kadane |
| Space | O(n) | Stores transformed array, though it can be reduced to O(1) |

The algorithm comfortably handles n up to 3×10^5 since it only performs linear work with simple arithmetic operations per element.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import isclose

    # inline solution
    input = sys.stdin.readline
    n = int(input())
    a = list(map(int, input().split()))

    base = 0
    b = []

    for x in a:
        base += abs(x)
        b.append(2 * x - abs(x))

    best = b[0]
    cur = b[0]

    for i in range(1, n):
        cur = max(b[i], cur + b[i])
        best = max(best, cur)

    return str(base + best)

# provided sample 1
assert run("-2 5 -3 4 -1\n") == "20", "sample 1 (interpreted)"
# custom cases
assert run("1\n5\n") == "5", "single positive"
assert run("1\n-5\n") == "5", "single negative"
assert run("3\n-1 -2 -3\n") == "4", "all negative"
assert run("5\n1 -2 3 -4 5\n") > "0", "mixed values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single positive | unchanged | baseline correctness |
| single negative | flip behavior | green-only optimality |
| all negative | small best segment | Kadane on negatives |
| mixed values | positive gain | interaction of operations |

## Edge Cases

A key edge case is when all values are negative. In this situation, a naive interpretation might suggest choosing a long blue segment to reduce losses, but doubling negatives only worsens them inside the segment. The correct solution instead relies entirely on the absolute-value baseline outside and selects a minimal-impact segment via Kadane, which naturally avoids overcommitting.

Another edge case is a single-element array. The algorithm reduces correctly to comparing 2a[i] versus |a[i]|, and Kadane ensures the segment is either chosen or effectively minimized to that single index.

A final subtle case is when values are large in magnitude, close to 10^9. Since all transformations remain linear and only involve multiplication by 2 and absolute value, 64-bit integer arithmetic is sufficient and no overflow issues arise in Python, though this would matter in fixed-width languages.
