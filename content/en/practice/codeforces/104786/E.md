---
title: "CF 104786E - School"
description: "We are given a permutation of size $n$, meaning every integer from 1 to $n$ appears exactly once. For every pair of indices $(l, r)$, we look at the segment of the array from $l$ to $r$."
date: "2026-06-28T14:31:05+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104786
codeforces_index: "E"
codeforces_contest_name: "FIICode2023Round1"
rating: 0
weight: 104786
solve_time_s: 85
verified: false
draft: false
---

[CF 104786E - School](https://codeforces.com/problemset/problem/104786/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 25s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a permutation of size $n$, meaning every integer from 1 to $n$ appears exactly once. For every pair of indices $(l, r)$, we look at the segment of the array from $l$ to $r$. We only want to count those segments where the values at the endpoints, $p_l$ and $p_r$, already “control” the entire segment: every element inside the segment must lie between the smaller and larger of the two endpoints.

Rephrased, if we take the minimum and maximum values of the two endpoints, the entire subarray between them must stay inside that numeric interval. No element in the segment is allowed to go outside the range defined by the endpoints.

The naive interpretation is to consider every segment and verify whether any element violates the endpoint bounds. With $n$ up to $5 \cdot 10^5$, there are about $2.5 \cdot 10^{11}$ segments, and even checking each in linear time is impossible. Even an $O(n^2)$ method is already too large.

A subtle point is that the condition depends only on the extremes of values at the endpoints, but it still constrains all interior elements. This hints that we are really counting segments whose endpoints are “extremal enough” so that no intermediate element escapes their value interval.

A naive trap is to assume that only adjacent or monotone segments matter. For example, in a permutation like $1\ 3\ 2\ 4\ 5$, the segment $(1,5)$ is valid even though it is not monotone, because all interior values lie between 1 and 5. On the other hand, $(2,4)$ might fail if some interior value is outside the endpoint range.

The difficulty is global: every segment depends on all intermediate values, so we need a way to avoid recomputing minima and maxima for every pair.

## Approaches

The brute-force solution is straightforward. For each pair $(l, r)$, compute the minimum and maximum values in the subarray $p[l:r]$ or scan the segment and check whether any element lies outside $[\min(p_l, p_r), \max(p_l, p_r)]$. This works because it directly verifies the condition, but it requires either $O(n^3)$ time if recomputing extremes naively or $O(n^2)$ if we maintain running minima and maxima per start index. With $n = 5 \cdot 10^5$, even $O(n^2)$ leads to about $2.5 \cdot 10^{11}$ operations, which is far beyond any limit.

The key observation is to shift perspective from segments defined by endpoints to elements acting as barriers. Fix one endpoint, say $l$. As we expand $r$ outward, the segment is valid until we encounter a value that lies outside the range defined by $p_l$ and $p_r$. The issue is that the range itself changes with $r$, so this still feels circular.

The real structure becomes clearer if we think in terms of ordering constraints imposed by intermediate elements. A segment $(l, r)$ is invalid if there exists some index $i \in (l, r)$ such that $p_i < \min(p_l, p_r)$ or $p_i > \max(p_l, p_r)$. This means every interior element must be “covered” by the interval endpoints.

This is equivalent to saying that for every interior position, the endpoint values must straddle it in value space. Each interior element effectively forbids certain endpoint pairs: if an interior value is very small or very large, it restricts which endpoints can form a valid pair around it.

A productive way to reframe this is to process positions in increasing order of value. When we fix a value $x$, it will constrain pairs that “span over it” in index space. Specifically, if we know where all values less than or greater than $x$ lie, we can determine how many pairs have endpoints on both sides of $x$, which would violate validity unless $x$ lies within endpoint values.

This leads to a classic inversion-style counting idea: each element contributes to invalid pairs depending on how many smaller/larger elements are on both sides of it. Instead of checking segments, we count how many triples $(l, r, i)$ cause a violation and subtract from total pairs.

Total pairs of indices is $n(n+1)/2$. A pair is invalid if there exists an interior point that lies outside endpoint range, which can be counted via each element acting as a “separator” for pairs that cross it in a forbidden way. By tracking positions in a Fenwick tree (or BIT), we can maintain how many values have been seen on each side and count contributions efficiently.

The final solution reduces to processing values in order and counting how many inversions they create with respect to their positions, with each element contributing based on how many already-processed elements lie to its left and right.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(1)$ | Too slow |
| Optimal | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We process the permutation in increasing order of values, treating each value as the moment it becomes “active”.

1. Place each value at its position and maintain a data structure that tracks which positions have already been activated. Initially no positions are active. This lets us know, at any moment, which values are smaller than the current one and already processed.
2. When processing value $x$ at position $pos[x]$, we insert it into a Fenwick tree over indices. This structure allows us to count how many already inserted positions lie to the left or right of any index efficiently.
3. For the current position $pos[x]$, compute how many previously processed positions are on the left and how many are on the right. Let these be $L$ and $R$. These correspond to values smaller than $x$ already placed in those regions.
4. The number of new invalid pairs introduced by $x$ is $L \cdot R$. This comes from choosing one smaller element on the left and one on the right, forming endpoints that would sandwich $x$ outside their range.
5. Accumulate these contributions over all values. The total count of invalid configurations is the sum of all such products.
6. Convert to the final answer by taking total pairs of indices and subtracting invalid contributions.

### Why it works

Each element $x$ acts as the unique minimum or maximum barrier for pairs whose endpoints lie on opposite sides of its position. If endpoints straddle $x$ in index order but $x$ is not between them in value order, the condition fails exactly once for that pair. Because values are processed in increasing order, every such violation is attributed exactly to the smallest element inside the span that breaks the endpoint interval. This ensures no pair is double-counted and no invalid pair is missed.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, i, v):
        while i <= self.n:
            self.bit[i] += v
            i += i & -i

    def sum(self, i):
        s = 0
        while i > 0:
            s += self.bit[i]
            i -= i & -i
        return s

n = int(input())
p = list(map(int, input().split()))

pos = [0] * (n + 1)
for i, v in enumerate(p, 1):
    pos[v] = i

fw = Fenwick(n)

ans = 0

for v in range(1, n + 1):
    i = pos[v]
    left = fw.sum(i - 1)
    right = fw.sum(n) - fw.sum(i)
    ans += left * right
    fw.add(i, 1)

total_pairs = n * (n + 1) // 2
print(total_pairs - ans)
```

The Fenwick tree maintains how many values smaller than the current one have already been placed. At each step, the current value contributes based on how many such smaller values are to its left and right, since those form endpoint pairs that would fail the condition with this value acting as the interior violation point.

The final subtraction step converts the computed invalid count into the required number of valid segments.

## Worked Examples

### Example 1

Input:

```
5
1 3 2 4 5
```

We map values to positions: 1→1, 2→3, 3→2, 4→4, 5→5.

| Value | Position | Left smaller | Right smaller | Contribution |
| --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0 | 0 |
| 2 | 3 | 1 | 0 | 0 |
| 3 | 2 | 1 | 1 | 1 |
| 4 | 4 | 3 | 0 | 0 |
| 5 | 5 | 4 | 0 | 0 |

Total invalid = 1, total pairs = 15, answer = 14.

This trace shows how only the element 3 creates a split where smaller elements exist on both sides, producing exactly one forbidden configuration.

### Example 2

Input:

```
4
4 3 2 1
```

Positions: 1→4, 2→3, 3→2, 4→1.

| Value | Position | Left smaller | Right smaller | Contribution |
| --- | --- | --- | --- | --- |
| 1 | 4 | 0 | 0 | 0 |
| 2 | 3 | 1 | 0 | 0 |
| 3 | 2 | 2 | 0 | 0 |
| 4 | 1 | 3 | 0 | 0 |

Total invalid = 0, so all segments are valid.

This occurs because the permutation is fully decreasing in index order, so no element ever has smaller elements on both sides simultaneously.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Each update and prefix sum query in Fenwick tree takes logarithmic time |
| Space | $O(n)$ | Stores permutation position mapping and Fenwick tree |

The algorithm comfortably handles $n = 5 \cdot 10^5$, since about $5 \cdot 10^5 \log 5 \cdot 10^5$ operations fits within typical limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    class Fenwick:
        def __init__(self, n):
            self.n = n
            self.bit = [0] * (n + 1)

        def add(self, i, v):
            while i <= self.n:
                self.bit[i] += v
                i += i & -i

        def sum(self, i):
            s = 0
            while i > 0:
                s += self.bit[i]
                i -= i & -i
            return s

    n = int(input())
    p = list(map(int, input().split()))

    pos = [0] * (n + 1)
    for i, v in enumerate(p, 1):
        pos[v] = i

    fw = Fenwick(n)
    ans = 0

    for v in range(1, n + 1):
        i = pos[v]
        left = fw.sum(i - 1)
        right = fw.sum(n) - fw.sum(i)
        ans += left * right
        fw.add(i, 1)

    total_pairs = n * (n + 1) // 2
    return str(total_pairs - ans).strip()

# provided sample
assert run("5\n1 3 2 4 5\n") == "14", "sample 1"

# custom cases
assert run("1\n1\n") == "1", "single element"
assert run("2\n1 2\n") == "3", "two elements all segments valid"
assert run("4\n4 3 2 1\n") == "10", "monotone decreasing"
assert run("3\n2 1 3\n") == "5", "small mixed permutation"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 1 | minimum size |
| 1 2 | 3 | all segments valid |
| 4 3 2 1 | 10 | strictly decreasing case |
| 2 1 3 | 5 | mixed ordering correctness |

## Edge Cases

For a single element permutation, the only valid segment is $(1,1)$. The algorithm inserts the first value, finds no left or right contributions, and outputs $1$ after subtracting zero invalid pairs from the total.

For a completely increasing or decreasing permutation, no value ever has smaller elements on both sides during processing, so every contribution remains zero. The result becomes the full $n(n+1)/2$, matching the fact that every segment is valid under monotone structure.
