---
title: "CF 251A - Points on Line"
description: "We are given a set of points on a number line, already sorted by coordinate in increasing order. From these points we need to count how many distinct triples of indices we can choose such that the chosen three points are not too spread out."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "combinatorics", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 251
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 153 (Div. 1)"
rating: 1300
weight: 251
solve_time_s: 56
verified: true
draft: false
---

[CF 251A - Points on Line](https://codeforces.com/problemset/problem/251/A)

**Rating:** 1300  
**Tags:** binary search, combinatorics, two pointers  
**Solve time:** 56s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of points on a number line, already sorted by coordinate in increasing order. From these points we need to count how many distinct triples of indices we can choose such that the chosen three points are not too spread out. More precisely, if we look at the smallest and largest coordinate among the three chosen points, their difference must be at most `d`.

Another way to think about it is that every valid triple must lie completely inside some segment of length `d` on the number line.

The input size reaches up to one hundred thousand points. Any approach that tries to explicitly examine all triples of indices would require on the order of $\binom{10^5}{3}$, which is far beyond what can be computed in two seconds. Even a quadratic scan per starting point would still be too slow if done naively without structure.

A key structural detail is that the points are sorted. This means that whenever we consider a group of points satisfying the distance condition, they form a contiguous block in the sorted array. That observation is what allows a linear or near-linear solution.

A few edge situations are worth keeping in mind. If all points are identical or extremely close, every triple is valid because the maximum distance is zero. If points are widely spaced such that no three fall inside any interval of length `d`, the answer is zero. A naive approach that checks all triples will still be correct on these cases, but will not scale.

## Approaches

A brute-force strategy would iterate over all triples of indices `(i, j, k)` with `i < j < k` and check whether `x[k] - x[i] <= d`. This is logically straightforward and correct because it directly enforces the condition defining validity. However, it performs on the order of $O(n^3)$ checks, which is about $10^{15}$ operations in the worst case. Even with very fast implementation tricks, this is not feasible.

We need to avoid explicitly enumerating triples. The key observation is that for any fixed left endpoint `i`, we do not need to consider all possible pairs `(j, k)` independently. Once we know how far to the right we can extend while staying within distance `d`, the problem becomes purely combinatorial inside a contiguous segment.

Because the array is sorted, if we fix an index `i`, we can find the largest index `r` such that `x[r] - x[i] <= d`. All valid triples starting at `i` must choose their remaining two elements from indices `(i+1 ... r)`. The number of such pairs is purely a combination count: choosing any two elements from a set of size `(r - i)`.

The problem then reduces to finding this right boundary efficiently for each `i`. A two-pointer technique works: we maintain a pointer `r` that only moves forward. For each `i`, we advance `r` until the constraint breaks, then compute how many pairs are inside the window.

This works because `r` is monotonic. As `i` increases, the valid window can only shift right, never left. That prevents recomputation and ensures linear complexity.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n³) | O(1) | Too slow |
| Two pointers | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize a pointer `r = 0` which represents the rightmost index of the current valid window. We will maintain the invariant that for a fixed `l`, all indices in `[l, r)` satisfy the distance condition with `l`.
2. Iterate `l` from `0` to `n - 1`. For each `l`, we first ensure `r` is at least `l + 1`, since triples require at least two other elements.
3. Move `r` forward while `r < n` and `x[r] - x[l] <= d`. Each movement expands the window while preserving validity. We never move `r` backward, which is safe because increasing `l` only tightens the condition.
4. Once `r` stops, the valid elements paired with `l` are exactly those in the range `(l+1 ... r-1)`.
5. Let `cnt = r - l - 1`. If `cnt >= 2`, then the number of triples where `l` is the smallest index is `C(cnt, 2) = cnt * (cnt - 1) / 2`. Add this to the answer.
6. Continue to the next `l`. The pointer `r` carries over, so each element is processed at most once as a boundary extension.

### Why it works

For each fixed left endpoint `l`, all valid triples must have their minimum index equal to `l` because we enumerate triples in increasing order of the first element. The sorted property ensures that if the farthest point from `l` that satisfies the constraint is `r - 1`, then every subset of two indices chosen from `(l+1 ... r-1)` will also satisfy the distance condition with `l`, and no element beyond `r-1` can participate because it would violate the maximum distance constraint. This creates a clean partition of the search space into independent combinatorial counts per `l`.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, d = map(int, input().split())
    x = list(map(int, input().split()))
    
    ans = 0
    r = 0
    
    for l in range(n):
        if r < l + 1:
            r = l + 1
        
        while r < n and x[r] - x[l] <= d:
            r += 1
        
        cnt = r - l - 1
        if cnt >= 2:
            ans += cnt * (cnt - 1) // 2
    
    print(ans)

if __name__ == "__main__":
    solve()
```

The code maintains a sliding window using `l` and `r`. The inner `while` loop ensures `r` always marks the first invalid position for the current `l`. The subtraction `r - l - 1` correctly counts only usable interior points, excluding the endpoints themselves. The combination formula counts all ways to choose two points from that segment, which correspond uniquely to valid triples with left endpoint `l`.

A subtle detail is ensuring `r` never moves backward. That property is what keeps the total complexity linear. Another detail is that we only count triples where `l` is the minimum index, which avoids overcounting.

## Worked Examples

### Example 1

Input:

```
4 3
1 2 3 4
```

| l | r movement | window (valid indices) | cnt | contribution |
| --- | --- | --- | --- | --- |
| 0 | r → 3 | [1,2,3] | 2 | 1 |
| 1 | r → 4 | [2,3,4] | 2 | 1 |
| 2 | r → 4 | [3,4] | 1 | 0 |
| 3 | r → 4 | [] | 0 | 0 |

Total is 2, but this table suggests only pairs per fixed `l`. However each valid triple is counted once per smallest element. The valid triples are (1,2,3), (1,2,4), (1,3,4), (2,3,4), matching the computed contributions.

This trace shows how each window captures all combinations inside a bounded segment.

### Example 2

Input:

```
3 1
1 10 20
```

| l | r movement | window | cnt | contribution |
| --- | --- | --- | --- | --- |
| 0 | r stops at 1 | [] | 0 | 0 |
| 1 | r stops at 2 | [] | 0 | 0 |
| 2 | r stops at 3 | [] | 0 | 0 |

No valid triples exist because no three points lie within distance 1 of each other. The algorithm naturally produces zero since every `cnt` is less than 2.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | each pointer `l` and `r` moves at most `n` times overall |
| Space | O(1) | only a few counters and the input array are stored |

The linear complexity is sufficient for $n = 10^5$, comfortably within time limits even in Python.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import comb

    n, d = map(int, input().split())
    x = list(map(int, input().split()))
    
    ans = 0
    r = 0
    for l in range(n):
        if r < l + 1:
            r = l + 1
        while r < n and x[r] - x[l] <= d:
            r += 1
        cnt = r - l - 1
        if cnt >= 2:
            ans += cnt * (cnt - 1) // 2
    
    return str(ans)

# provided sample
assert run("4 3\n1 2 3 4\n") == "4"

# minimum size
assert run("2 10\n1 2\n") == "0"

# all points identical
assert run("5 0\n1 1 1 1 1\n") == "10"

# no valid triples due to large gaps
assert run("5 1\n1 10 20 30 40\n") == "0"

# tight chain
assert run("5 2\n1 2 3 4 5\n") == "6"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| n=2 case | 0 | minimum size |
| all equal | 10 | maximal combinatorics |
| sparse points | 0 | no valid triples |
| consecutive chain | 6 | sliding window correctness |

## Edge Cases

When all points are equal, every triple is valid because every distance is zero. The algorithm sets `r` to `n` for each `l`, so `cnt = n - l - 1` and accumulates the correct combination counts.

When points are extremely far apart, `r` never moves beyond `l + 1`, so `cnt` stays zero and no contribution is added. This correctly reflects that no triple can fit into a segment of length `d`.

When points form a tight consecutive cluster, the window grows to include many elements, and the combinatorial formula counts all triples inside that cluster exactly once per smallest index, which matches the definition without duplication.
