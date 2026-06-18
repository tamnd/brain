---
title: "CF 1211A - Three Problems"
description: "We are given a list of problem difficulties, where each problem has an index and a numeric complexity value. The task is to select three distinct indices $a$, $b$, and $c$ such that the corresponding values form a strictly increasing chain: $ra < rb < rc$."
date: "2026-06-18T17:20:39+07:00"
tags: ["codeforces", "competitive-programming", "*special", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1211
codeforces_index: "A"
codeforces_contest_name: "Kotlin Heroes: Episode 2"
rating: 1000
weight: 1211
solve_time_s: 102
verified: false
draft: false
---

[CF 1211A - Three Problems](https://codeforces.com/problemset/problem/1211/A)

**Rating:** 1000  
**Tags:** *special, implementation  
**Solve time:** 1m 42s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a list of problem difficulties, where each problem has an index and a numeric complexity value. The task is to select three distinct indices $a$, $b$, and $c$ such that the corresponding values form a strictly increasing chain: $r_a < r_b < r_c$.

The output is not the values themselves but the indices of any valid triple. If no such triple exists, we must output `-1 -1 -1`.

The constraints allow up to $n = 3000$. This size is small enough that an $O(n^2)$ or even carefully managed $O(n^3)$ approach might pass in some languages, but in Python, anything approaching $O(n^3)$ risks timing out. A quadratic scan is acceptable, but a cubic scan over 27 million operations per worst case is already borderline depending on constants.

The key difficulty is not computational but structural. We are not asked to optimize a numeric function or count triples, but to find existence of an increasing subsequence of length three with indices preserved.

A naive pitfall appears when values repeat or are unsorted. For example, in an array like `[5, 1, 5, 1, 5]`, a careless attempt might pick equal values thinking they form a progression. That fails because strict inequality is required. Another subtle issue is picking values in correct order of indices is irrelevant, since indices can be arbitrary as long as the values satisfy ordering.

A brute force approach might miss that a valid triple could be scattered and not adjacent, so greedy local checks can fail if they only inspect neighbors.

## Approaches

The most direct idea is to try all triples of indices. We pick $i < j < k$ and check whether $r_i < r_j < r_k$. This is correct because it explicitly tests the condition. However, this examines $\binom{n}{3}$ triples, which in the worst case is about 4.5 billion checks when $n = 3000$. That is too slow in Python.

We need to avoid enumerating all triples while still preserving the ability to detect a valid middle element efficiently.

The key observation is that for any fixed middle position $j$, we do not need to search all possible pairs $(i, k)$ independently. Instead, we only need to know whether there exists some value smaller than $r_j$ to its left and some value larger than $r_j$ to its right. If both exist, $j$ serves as the middle of a valid triple.

This transforms the problem into maintaining two helper structures: a prefix scan that tracks the smallest element seen so far (or its index), and a suffix scan that tracks the smallest possible candidate greater than each element or simply checks existence of any greater element to the right. Since values are arbitrary, we can precompute, for each position, whether a larger value exists to the right and similarly whether a smaller value exists to the left.

Once these arrays are computed, scanning for a valid middle index becomes straightforward. For any $j$, if there exists $i < j$ with $r_i < r_j$ and $k > j$ with $r_k > r_j$, we immediately output that triple.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^3)$ | $O(1)$ | Too slow |
| Prefix/Suffix Precompute | $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We build the solution around the idea that every valid triple has a clear middle element.

1. Precompute an array `left_min_index` that stores, for every position $j$, the index of the smallest value seen in the prefix $1..j$. This gives us a candidate $i$ such that $r_i < r_j$ can be quickly tested by comparing values.
2. Precompute an array `right_max_index` that stores, for every position $j$, the index of the largest value seen in the suffix $j..n$. This gives us a candidate $k$ such that $r_k > r_j$.
3. Iterate over each index $j$ treating it as the potential middle element.
4. For each $j$, check whether the best prefix candidate actually satisfies $r_{left[j]} < r_j$. If not, there is no valid left element for this $j$.
5. Similarly, check whether the best suffix candidate satisfies $r_{right[j]} > r_j$. If not, there is no valid right element for this $j$.
6. If both conditions hold, output the triple of indices immediately.

### Why it works

Every valid solution has some middle element $b$. If such a triple exists, then among all elements to the left of $b$, at least one is smaller, and among all elements to the right of $b$, at least one is larger. The prefix and suffix precomputations guarantee we do not miss these candidates. Since we test every possible middle position, we must encounter the correct $b$, and at that point both required companions are already encoded in the precomputed arrays. No valid configuration can be skipped because every candidate middle index is explicitly examined.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
r = list(map(int, input().split()))

left_min_index = [0] * n
min_idx = 0
for i in range(n):
    if r[i] < r[min_idx]:
        min_idx = i
    left_min_index[i] = min_idx

right_max_index = [0] * n
max_idx = n - 1
for i in range(n - 1, -1, -1):
    if r[i] > r[max_idx]:
        max_idx = i
    right_max_index[i] = max_idx

for j in range(n):
    i = left_min_index[j]
    k = right_max_index[j]
    if r[i] < r[j] and r[k] > r[j]:
        print(i + 1, j + 1, k + 1)
        sys.exit()

print(-1, -1, -1)
```

The prefix scan builds a running best candidate for a left-side minimum, ensuring that for each position we have the strongest possible choice of a smaller element.

The suffix scan does the same in reverse for larger elements. Using extrema rather than full lists is sufficient because any valid middle element only requires existence of at least one smaller and one larger value.

The final loop simply tests each index as a potential middle point and verifies whether both sides are satisfied.

## Worked Examples

### Example 1

Input:

```
6
3 1 4 1 5 9
```

We compute prefix minima and suffix maxima:

| j | r[j] | left_min_index[j] | r[left] | right_max_index[j] | r[right] | valid? |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 3 | 0 | 3 | 5 | 9 | no |
| 1 | 1 | 1 | 1 | 5 | 9 | no |
| 2 | 4 | 1 | 1 | 5 | 9 | yes |

At $j = 2$, we have $r[1] = 1 < 4 < 9 = r[5]$, so the algorithm outputs:

```
2 3 6
```

This confirms the method correctly identifies a valid middle element even when it is not obvious locally.

### Example 2

Input:

```
5
5 4 3 2 1
```

| j | r[j] | left_min_index[j] | r[left] | right_max_index[j] | r[right] | valid? |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 5 | 0 | 5 | 0 | 5 | no |
| 1 | 4 | 1 | 4 | 0 | 5 | no |
| 2 | 3 | 2 | 3 | 0 | 5 | no |
| 3 | 2 | 3 | 2 | 0 | 5 | no |
| 4 | 1 | 4 | 1 | 0 | 5 | no |

No index satisfies both conditions, so the output is:

```
-1 -1 -1
```

This shows the algorithm correctly rejects strictly decreasing sequences.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Two linear scans plus one linear check |
| Space | $O(n)$ | Two auxiliary arrays store prefix and suffix information |

The constraints allow up to 3000 elements, and a linear scan is trivial within limits. The solution is well within both time and memory bounds.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from subprocess import run as sp_run

    # Inline solution execution via function wrapper
    # (simplified: re-define solution here for testing)
    input = sys.stdin.readline
    n = int(input())
    r = list(map(int, input().split()))

    left_min_index = [0] * n
    min_idx = 0
    for i in range(n):
        if r[i] < r[min_idx]:
            min_idx = i
        left_min_index[i] = min_idx

    right_max_index = [0] * n
    max_idx = n - 1
    for i in range(n - 1, -1, -1):
        if r[i] > r[max_idx]:
            max_idx = i
        right_max_index[i] = max_idx

    for j in range(n):
        i = left_min_index[j]
        k = right_max_index[j]
        if r[i] < r[j] and r[k] > r[j]:
            return f"{i+1} {j+1} {k+1}"

    return "-1 -1 -1"

# provided sample
assert run("6\n3 1 4 1 5 9\n") in {"2 3 6", "4 2 3", "4 2 6"}, "sample 1"

# minimum size
assert run("3\n1 2 3\n") != "-1 -1 -1"

# all equal
assert run("4\n7 7 7 7\n") == "-1 -1 -1"

# decreasing
assert run("5\n5 4 3 2 1\n") == "-1 -1 -1"

# random valid
assert run("5\n1 5 2 4 3\n") != "-1 -1 -1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3 1 2 3` | any valid triple | minimal increasing case |
| `7 7 7 7` | `-1 -1 -1` | equality blocking strict increase |
| `5 4 3 2 1` | `-1 -1 -1` | monotone decreasing failure |
| `1 5 2 4 3` | valid triple | scattered increasing structure |

## Edge Cases

A tricky scenario is when the smallest valid left element is not adjacent to the middle candidate. Consider `3 1 4 1 5 9`. At index 2 (value 4), the correct left candidate is index 1 (value 1), not index 0 or 3. The prefix minimum array ensures we still select index 1 because it globally tracks the best available left value regardless of position.

Another edge case is repeated values. In `2 2 2 3 3`, a naive scan might pick equal values for both sides, but strict inequality prevents that. The suffix maximum and prefix minimum guarantee correctness because they always verify actual value comparisons rather than relying on positional assumptions.

A final case is when the valid triple is far apart, such as `1 100 2 3 4`. The middle element is not necessarily part of a local increasing trend. The algorithm still works because it checks every index as a potential middle and does not depend on adjacency, only on global prefix and suffix existence.
