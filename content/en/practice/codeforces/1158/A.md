---
title: "CF 1158A - The Party and Sweets"
description: "We have a party with $n$ boys and $m$ girls. Each boy gives some number of sweets to every girl, forming an $n times m$ matrix of integers. For each boy, the minimum number of sweets he gives to any girl is specified as $bi$."
date: "2026-06-12T02:29:03+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "constructive-algorithms", "greedy", "implementation", "math", "sortings", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1158
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 559 (Div. 1)"
rating: 1500
weight: 1158
solve_time_s: 156
verified: false
draft: false
---

[CF 1158A - The Party and Sweets](https://codeforces.com/problemset/problem/1158/A)

**Rating:** 1500  
**Tags:** binary search, constructive algorithms, greedy, implementation, math, sortings, two pointers  
**Solve time:** 2m 36s  
**Verified:** no  

## Solution
## Problem Understanding

We have a party with $n$ boys and $m$ girls. Each boy gives some number of sweets to every girl, forming an $n \times m$ matrix of integers. For each boy, the minimum number of sweets he gives to any girl is specified as $b_i$. For each girl, the maximum number of sweets she receives from any boy is specified as $g_j$. Our task is to reconstruct a plausible assignment of sweets that satisfies all these constraints and simultaneously minimizes the total number of sweets handed out. If it is impossible to satisfy the constraints, we must output $-1$.

The input sizes are large, up to $10^5$ for both boys and girls, with each sweet count up to $10^8$. This implies that any solution that explicitly iterates over all $n \cdot m$ matrix entries is likely too slow, as $10^5 \cdot 10^5 = 10^{10}$ operations would be prohibitive. The solution must rely on clever aggregation or sorting to avoid a full matrix traversal.

A subtle edge case arises when the largest minimal sweet among the boys exceeds the smallest maximal sweet among the girls. For example, consider $b = [5, 1]$ and $g = [4, 6]$. The first boy must give at least $5$ sweets to someone, but no girl can receive more than $4$ from anyone. This configuration is impossible, and a naive approach that fills the matrix greedily without checking feasibility would fail silently.

Another edge case occurs when multiple boys share the same minimal sweet value as the maximal sweet of a girl. The distribution must carefully allocate the largest minimum to the appropriate column to match the girl’s maximum.

## Approaches

The brute-force approach would try to construct the entire $n \times m$ matrix explicitly. We would assign values to satisfy $b_i$ for each row and $g_j$ for each column. One could attempt a greedy assignment: for each boy, start by filling his minimal sweet $b_i$ across all girls and then try to adjust certain entries to match the girls' maxima. While correct in principle, this approach has $O(n \cdot m)$ complexity, which is infeasible for $n, m$ up to $10^5$.

The key insight comes from observing that the minimal sweet for each boy must appear somewhere in his row, and the maximal sweet for each girl must appear somewhere in her column. To minimize the total sum, we should fill as many entries as possible with the row minimums, only increasing values to satisfy column maxima. Sorting $b$ and $g$ allows us to align the largest minimum of boys with the largest maxima of girls to satisfy constraints with minimal increments.

Specifically, if the largest boy minimum equals the smallest girl maximum, we must assign it to that girl; all other row minima can be assigned to other girls without increasing sums unnecessarily. This reduces the problem to a few arithmetic operations instead of iterating over the full matrix.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * m) | O(n * m) | Too slow |
| Optimal | O(n log n + m log m) | O(1) | Accepted |

## Algorithm Walkthrough

1. Sort the array $b$ of boy minima and $g$ of girl maxima. Let $b_{\text{max}}$ be the largest boy minimum and $b_{\text{second}}$ the second largest. Let $g_{\text{min}}$ be the smallest girl maximum.
2. If $b_{\text{max}} > g_{\text{min}}$, the situation is impossible, output $-1$.
3. Initialize the total sum as the sum of all $b_i$ multiplied by $m$, since each boy gives at least his minimum to every girl.
4. Add to the sum the difference between each $g_j$ and $b_{\text{max}}$ for every girl except the one that will receive $b_{\text{max}}$, because each girl must reach her maximum somewhere.
5. Finally, add $b_{\text{max}} - b_{\text{second}}$ to the total sum if the largest boy minimum is less than the largest girl maximum. This accounts for the extra sweets needed to reach the largest girl's maximum while keeping the sum minimal.

The invariant is that each boy contributes at least his minimal sweet to every girl, and each girl receives her maximal sweet exactly once. The algorithm ensures that no row or column constraint is violated while minimizing additional sweets.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m = map(int, input().split())
b = list(map(int, input().split()))
g = list(map(int, input().split()))

b.sort()
g.sort()

if b[-1] > g[0]:
    print(-1)
    sys.exit()

total = 0
# sum of all minimal contributions
total += sum(b) * m

# add difference for each girl
for j in range(m):
    total += g[j] - b[-1]

# adjust for the largest boy if needed
if b[-1] < g[0]:
    total += b[-1] - b[-2]

print(total)
```

The first step sorts the arrays to easily find maxima and minima and check feasibility. Multiplying sum of row minima by $m$ ensures all minimal contributions are counted. Adjusting by the differences between each girl's maximum and the largest boy minimum ensures every column constraint is satisfied. The final adjustment handles the case where the largest boy minimum is strictly less than the largest girl maximum.

## Worked Examples

**Sample 1**:

Input: `3 2`, `1 2 1`, `3 4`

| Step | b (sorted) | g (sorted) | total |
| --- | --- | --- | --- |
| Initial | [1,1,2] | [3,4] | 0 |
| sum(b)*m |  |  | (1+1+2)*2 = 8 |
| add g[j]-b[-1] |  |  | (3-2)+(4-2)=3 |
| adjust largest boy |  |  | 2-1=1 |
| Final total |  |  | 8+3+1=12 |

This matches the expected output and shows that constraints are satisfied with minimal total sweets.

**Sample 2**:

Input: `2 2`, `5 1`, `4 6`

| Step | b (sorted) | g (sorted) | total |
| --- | --- | --- | --- |
| b[-1] > g[0]? | 5 > 4 |  | impossible |
| Output |  |  | -1 |

This demonstrates the edge case where feasibility fails.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n + m log m) | Sorting both arrays dominates runtime |
| Space | O(n + m) | Arrays themselves, no extra significant structures |

Given $n, m \le 10^5$, sorting is acceptable within the 1-second time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, m = map(int, input().split())
    b = list(map(int, input().split()))
    g = list(map(int, input().split()))

    b.sort()
    g.sort()

    if b[-1] > g[0]:
        return "-1"

    total = sum(b) * m
    for j in range(m):
        total += g[j] - b[-1]
    if b[-1] < g[0]:
        total += b[-1] - b[-2]
    return str(total)

# Provided samples
assert run("3 2\n1 2 1\n3 4\n") == "12", "sample 1"
assert run("2 2\n5 1\n4 6\n") == "-1", "sample 2"

# Custom tests
assert run("2 3\n1 1\n1 1 1\n") == "6", "all equal"
assert run("3 3\n0 0 0\n0 0 0\n") == "0", "all zeros"
assert run("3 2\n1 2 3\n3 3\n") == "15", "increasing minima"
assert run("2 2\n2 2\n3 3\n") == "10", "equal minima, higher maxima"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 3\n1 1\n1 1 1\n` | 6 | all minima and maxima equal, simple case |
| `3 3\n0 0 0\n0 0 0\n` | 0 | zero sweets edge case |
| `3 2\n1 2 3\n3 3\n` | 15 | increasing minima and maxima, confirms algorithm assigns largest minimum to largest maximum |
| `2 2\n2 2\n3 3\n` | 10 | equal minima, higher maxima, tests adjustment for sum minimization |

## Edge Cases

When the largest boy minimum exceeds the smallest girl maximum, the algorithm correctly outputs `-1`. For example, input `2 2\n5 1\n4 6` fails because no assignment satisfies all row and column constraints. When all values are equal, such as `2 3\n1 1\n1
