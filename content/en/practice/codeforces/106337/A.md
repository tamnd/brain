---
title: "CF 106337A - \u0418\u0442\u043e\u0433\u0438 \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b"
description: "We are given an array of integers representing scores of participants in an olympiad. For every ordered pair of participants $(i, j)$, we compute how much “extra” score $j$ has compared to $i$, but only if $j$ is better."
date: "2026-06-19T08:54:48+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106337
codeforces_index: "A"
codeforces_contest_name: "2025-2026 \u0412\u0441\u0435\u0440\u043e\u0441\u0441\u0438\u0439\u0441\u043a\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432 \u043f\u043e \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0442\u0438\u043a\u0435, \u0440\u0435\u0433\u0438\u043e\u043d\u0430\u043b\u044c\u043d\u044b\u0439 \u044d\u0442\u0430\u043f, 1 \u0442\u0443\u0440"
rating: 0
weight: 106337
solve_time_s: 45
verified: true
draft: false
---

[CF 106337A - \u0418\u0442\u043e\u0433\u0438 \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b](https://codeforces.com/problemset/problem/106337/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 45s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers representing scores of participants in an olympiad. For every ordered pair of participants $(i, j)$, we compute how much “extra” score $j$ has compared to $i$, but only if $j$ is better. Formally, for each pair we take $\max(a_j - a_i, 0)$, and we sum this over all pairs.

Another way to see the task is to fix a participant $i$ and look at everyone else. For every $j$ with a higher score than $i$, participant $i$ contributes zero and participant $j$ contributes the difference $a_j - a_i$. The goal is the total accumulated contribution across all such comparisons.

The input size determines how aggressive the solution must be. A quadratic approach that inspects all pairs directly becomes infeasible once $n$ grows beyond a few thousand, since $n^2$ operations would already exceed typical limits for $n \approx 10^5$. This immediately suggests that the structure of the expression must be simplified so that contributions can be aggregated rather than enumerated pair by pair.

A common failure case for naive reasoning is mishandling ordering or double counting. For example, with input $[1, 3, 2]$, one might incorrectly sum only adjacent differences or forget that both directions of comparison are included but asymmetric due to the max function. The correct answer requires considering all ordered pairs, not just neighboring elements or sorted neighbors.

Another subtle pitfall is assuming symmetry: the expression is directional. For instance, $a_j - a_i$ contributes only when positive, so swapping indices changes whether a pair contributes at all. Any approach that treats pairs as unordered will fail.

## Approaches

The brute-force approach follows the definition directly. For every index $i$, we iterate over all $j$, compute $a_j - a_i$, and add it if it is positive. This is correct because it explicitly checks every ordered pair and applies the formula exactly as defined. However, this requires $n^2$ evaluations, and each evaluation is constant time, so the total work grows quadratically. For large inputs, this becomes too slow.

The key observation is that the expression only depends on the relative ordering of values, not their positions in the original array. For a fixed pair $i, j$, only the values matter: if $a_i \ge a_j$, the contribution is zero; otherwise it is $a_j - a_i$. This allows us to reorganize the computation by grouping equal or ordered values together.

Once values are sorted, every pair $i < j$ contributes exactly $a_j - a_i$, because ordering guarantees $a_j \ge a_i$. This removes the need for the max function entirely, since negativity never appears in sorted order. The problem reduces to summing differences over all increasing pairs, which can be expressed using prefix sums: for each position $i$, we compute how much larger $a_i$ is than all previous elements, and accumulate those contributions efficiently.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(1) | Too slow |
| Sorting + prefix sums | O(n log n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Sort the array in non-decreasing order. This ensures that for any pair $i < j$, we have $a_i \le a_j$, which eliminates the need for conditional checks inside the sum.
2. Maintain a running prefix sum of processed elements. This allows us to compute the total contribution of earlier elements in constant time per position.
3. Iterate through the sorted array. At each index $i$, treat $a[i]$ as the larger element in all pairs $(j, i)$ where $j < i$.
4. Compute the contribution of $a[i]$ as $i \cdot a[i] - \text{prefixSum}$. This expression represents the sum of differences between $a[i]$ and all previous elements, expanded algebraically from $\sum (a[i] - a[j])$.
5. Add this contribution to the final answer.
6. Update the prefix sum by adding $a[i]$, preparing it for the next iteration.

The key idea is that each element is processed as the “right endpoint” of all pairs involving smaller elements, and all such contributions are aggregated in one arithmetic expression.

### Why it works

After sorting, every valid contribution $\max(a_j - a_i, 0)$ becomes simply $a_j - a_i$ when $j > i$, since ordering guarantees non-negativity. Each element $a[i]$ contributes exactly once as the larger side of all pairs with previous elements, and the prefix sum ensures we subtract the total of those smaller elements correctly. This guarantees that every ordered pair is accounted for exactly once, with the correct signed difference.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    a.sort()
    
    res = 0
    pref = 0
    
    for i, x in enumerate(a):
        res += i * x - pref
        pref += x
    
    print(res)

if __name__ == "__main__":
    solve()
```

The solution begins by sorting the array so that comparisons become directional and monotonic. The variable `pref` stores the sum of all elements before the current index. At each step, `i * x` represents the total contribution if all previous elements were equal to zero, and subtracting `pref` corrects this to account for their actual values, producing the sum of differences.

A common mistake is updating `pref` before computing the contribution, which would incorrectly include the current element in its own calculation. The order shown here avoids that issue by first computing the contribution, then updating the prefix sum.

## Worked Examples

### Example 1

Input:

```
3
1 3 2
```

Sorted array: `[1, 2, 3]`

| i | x | pref before | contribution = i*x - pref | pref after | res |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 0 | 1 | 0 |
| 1 | 2 | 1 | 1 | 3 | 1 |
| 2 | 3 | 3 | 3 | 6 | 4 |

Final result is 4.

This trace shows that each element contributes based only on earlier elements, confirming that every pair is counted exactly once as a forward difference.

### Example 2

Input:

```
4
5 5 5 5
```

Sorted array remains `[5, 5, 5, 5]`

| i | x | pref before | contribution | pref after | res |
| --- | --- | --- | --- | --- | --- |
| 0 | 5 | 0 | 0 | 5 | 0 |
| 1 | 5 | 5 | 0 | 10 | 0 |
| 2 | 5 | 10 | 0 | 15 | 0 |
| 3 | 5 | 15 | 0 | 20 | 0 |

This confirms that equal elements produce zero contribution, since no positive differences exist.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates, single linear scan follows |
| Space | O(1) | Aside from input storage, only a few variables are used |

The complexity is well within typical constraints for $n$ up to $10^5$, where sorting and a single pass are efficient enough under standard limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    out = io.StringIO()
    sys.stdout = out
    solve()
    return out.getvalue().strip()

# basic sample-style case
assert run("3\n1 3 2\n") == "4"

# all equal
assert run("5\n7 7 7 7 7\n") == "0"

# strictly increasing
assert run("4\n1 2 3 4\n") == "10"

# strictly decreasing
assert run("4\n4 3 2 1\n") == "10"

# single element
assert run("1\n42\n") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 1 3 2 | 4 | basic mixed ordering |
| 5 7 7 7 7 7 | 0 | equal values |
| 4 1 2 3 4 | 10 | increasing structure |
| 4 4 3 2 1 | 10 | decreasing input symmetry |
| 1 42 | 0 | minimal edge case |

## Edge Cases

For equal values, the sorted array produces zero contribution at every step because `i * x` exactly matches the prefix sum scaled across identical elements. For input `5 7 7 7 7 7`, each iteration yields zero difference since no element is strictly smaller or larger in a way that creates positive differences.

For strictly decreasing input such as `4 3 2 1`, sorting reverses it into `1 2 3 4`, and the algorithm computes all pairwise differences once in the correct direction. At `i = 3`, value `4` contributes `3*4 - (1+2+3) = 12 - 6 = 6`, which corresponds to differences with all previous elements. Each earlier step similarly accumulates all valid pairs, ensuring full coverage without duplication.
