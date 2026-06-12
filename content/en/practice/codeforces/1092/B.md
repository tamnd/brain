---
title: "CF 1092B - Teams Forming"
description: "We are given an array of integers representing the skill levels of students. The students must be paired into exactly $frac{n}{2}$ disjoint pairs, so every student is used exactly once. A pair is only “valid” if both students in it end up with exactly the same skill level."
date: "2026-06-13T04:29:18+07:00"
tags: ["codeforces", "competitive-programming", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1092
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 527 (Div. 3)"
rating: 800
weight: 1092
solve_time_s: 171
verified: true
draft: false
---

[CF 1092B - Teams Forming](https://codeforces.com/problemset/problem/1092/B)

**Rating:** 800  
**Tags:** sortings  
**Solve time:** 2m 51s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers representing the skill levels of students. The students must be paired into exactly $\frac{n}{2}$ disjoint pairs, so every student is used exactly once. A pair is only “valid” if both students in it end up with exactly the same skill level. Since skills can only be increased (never decreased), we are allowed to increment individual students any number of times, paying one unit cost per increment.

The task is to choose the pairing structure and the increments so that every pair consists of equal values, while minimizing the total number of increments performed across all students.

The key observation from constraints is that $n \le 100$, so even quadratic or cubic reasoning over pairs or sorting is fully safe. We are not worried about asymptotic optimization beyond $O(n^2)$, which suggests we should focus on a greedy or pairing strategy rather than any complex data structure or DP over large states.

A subtle failure case for naive thinking is to try matching equal values first and then greedily fixing leftovers. For example, if values are heavily imbalanced, fixing local matches early can force expensive future adjustments. Another pitfall is pairing without sorting or structure, which can easily miss globally optimal pairings.

For instance, if we take `1 100 2 3`, a naive pairing like `(1,100)` and `(2,3)` looks reasonable structurally, but the cost is huge. A better global pairing is `(1,2)` and `(3,100)` which spreads the large value adjustment more efficiently.

This suggests that ordering matters fundamentally.

## Approaches

The brute-force approach would try all possible ways to pair students, and for each pairing compute the cost of making each pair equal. Since there are $(n-1)!!$ ways to pair $n$ items, this grows extremely fast. Even for $n = 20$, this becomes infeasible. Each pairing would still require computing the cost of equalizing pairs, so even if cost computation is fast, enumeration dominates.

The key insight is to sort the array. Once sorted, the optimal pairing becomes structured: we pair adjacent elements. This works because pairing two close values minimizes the cost of raising the smaller one to match the larger one, and sorting ensures we avoid pairing a small value with a very large one when better local alternatives exist.

After sorting, we only need to consider pairs $(a_0, a_1), (a_2, a_3), \dots$. For each pair, the cost is simply $a_{i+1} - a_i$, since we only increase the smaller element.

This reduces the problem from a combinatorial pairing problem to a linear scan over a sorted array.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Pairing Enumeration | $O(n!)$ | $O(n)$ | Too slow |
| Sort + Greedy Adjacent Pairing | $O(n \log n)$ | $O(1)$ or $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Read all student skill values into an array. The goal is to minimize total increments needed to form equal pairs.
2. Sort the array in non-decreasing order. This step ensures that values that are close numerically become neighbors, which is essential for minimizing adjustment cost.
3. Initialize a variable `answer = 0` to accumulate the total number of increments required.
4. Iterate over the sorted array in steps of two, considering consecutive pairs.
5. For each pair `(a[i], a[i+1])`, compute the cost as `a[i+1] - a[i]`. This represents increasing the smaller value to match the larger one.
6. Add this cost to the running total.
7. Output the final accumulated cost.

### Why it works

After sorting, any optimal solution can be transformed into one where pairing is done between adjacent elements without increasing cost. If two pairs are crossing, such as pairing `(a_i, a_k)` and `(a_j, a_l)` with $i < j < k < l$, swapping them into `(a_i, a_j)` and `(a_k, a_l)` never increases total cost because it reduces large gaps within pairs. Repeatedly applying this argument eliminates all crossings, resulting in adjacent pairing being optimal.

This establishes that greedy adjacent pairing is not just convenient, but structurally optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))

a.sort()

ans = 0
for i in range(0, n, 2):
    ans += a[i+1] - a[i]

print(ans)
```

The solution starts by reading the input and sorting the skill array. Sorting is essential because it creates a structure where optimal pairings become local.

The loop processes the array in chunks of two. Each iteration pairs two adjacent sorted values, which guarantees minimal cost for that pair under the global optimal structure. The difference is added directly because only increments are allowed, so we always raise the smaller value to match the larger one.

There are no boundary issues because $n$ is guaranteed even, so `a[i+1]` is always valid.

## Worked Examples

### Example 1

Input:

```
6
5 10 2 3 14 5
```

Sorted array:

```
2 3 5 5 10 14
```

| i | Pair | Cost | Running total |
| --- | --- | --- | --- |
| 0 | (2,3) | 1 | 1 |
| 2 | (5,5) | 0 | 1 |
| 4 | (10,14) | 4 | 5 |

Output is 5.

This trace shows how sorting ensures local differences correspond to minimal necessary increments.

### Example 2

Input:

```
4
1 100 2 3
```

Sorted array:

```
1 2 3 100
```

| i | Pair | Cost | Running total |
| --- | --- | --- | --- |
| 0 | (1,2) | 1 | 1 |
| 2 | (3,100) | 97 | 98 |

Output is 98.

This example highlights why greedy local pairing works better than arbitrary pairing: the large value is forced to absorb the cost, but pairing it with the closest available element minimizes total overhead.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Sorting dominates, single linear pass afterward |
| Space | $O(1)$ or $O(n)$ | Depends on in-place sort implementation |

The constraints $n \le 100$ make this more than sufficient. Even naive sorting or repeated scanning would pass comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))
    a.sort()

    ans = 0
    for i in range(0, n, 2):
        ans += a[i+1] - a[i]
    return str(ans)

# provided sample
assert run("6\n5 10 2 3 14 5\n") == "5"

# all equal
assert run("4\n7 7 7 7\n") == "0"

# increasing sequence
assert run("4\n1 2 3 4\n") == "2"

# large gap case
assert run("4\n1 100 2 3\n") == "98"

# minimum case
assert run("2\n1 10\n") == "9"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal values | 0 | zero-cost pairing correctness |
| 1 2 3 4 | 2 | adjacent pairing optimality |
| 1 100 2 3 | 98 | handling large imbalance |
| 1 10 | 9 | minimal boundary case |

## Edge Cases

One edge case is when all values are already equal. The algorithm sorts them but every adjacent difference is zero, so the result remains zero. For input `4 / 5 5 5 5`, the sorted array is unchanged and all computed differences vanish.

Another edge case is when values are highly skewed, such as `1 1 1 100`. After sorting, pairs become `(1,1)` and `(1,100)`. The first contributes zero cost, and the second contributes 99, which is unavoidable since only one large value exists.

A final edge case is the smallest possible input `n = 2`. The algorithm simply returns the difference between the two values after sorting, which directly matches the only valid pairing.
