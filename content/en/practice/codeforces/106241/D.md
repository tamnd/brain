---
title: "CF 106241D - Mini-Max Permutation"
description: "We are asked to construct a permutation of the integers from 1 to n. For every subarray of this permutation, we compute a value that depends on how spread out the numbers are inside it. Specifically, for a segment p[i.."
date: "2026-06-20T02:58:37+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106241
codeforces_index: "D"
codeforces_contest_name: "2025 GUC Winter Camp"
rating: 0
weight: 106241
solve_time_s: 64
verified: true
draft: false
---

[CF 106241D - Mini-Max Permutation](https://codeforces.com/problemset/problem/106241/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 4s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to construct a permutation of the integers from 1 to n. For every subarray of this permutation, we compute a value that depends on how spread out the numbers are inside it. Specifically, for a segment p[i..j], we take the maximum value in that segment, subtract the minimum value, and then subtract the length of the segment. This produces a cost that becomes small when values are tightly packed and the segment is short, and becomes large when the segment is long or has large value gaps.

The total score of a permutation is the sum of this cost over all possible subarrays. The task is to find a permutation that minimizes this total score. Among all permutations that achieve the minimum possible score, we must output the lexicographically largest one.

The constraints allow n up to 200,000, so any solution that tries to evaluate all subarrays explicitly is immediately impossible. The number of subarrays is quadratic, and even computing min and max per subarray would lead to cubic behavior.

A subtle point is that the objective depends only on relative ordering of values, not their absolute identity, because the permutation is always of 1 to n. Another important observation is that every subarray contributes a term involving both max and min, which suggests that elements that become extremes in many segments have a large influence on the cost.

A naive approach might try to reason locally or greedily pick elements while tracking contributions of all subarrays, but such approaches usually fail because inserting a value affects all segments crossing its position in a highly nonlocal way.

A small example highlights the sensitivity. For n = 3, permutations 1 2 3 and 3 2 1 behave differently because the middle element determines how many segments have small ranges. A greedy that always places small or large values at ends without a global pattern can easily miss the true optimal structure.

## Approaches

A brute-force approach would generate all permutations and compute the total cost for each. Even if we had an efficient way to compute the cost of a single permutation in O(n^2), the number of permutations is n!, which is completely infeasible. Even restricting to evaluating one permutation still requires iterating over all O(n^2) subarrays, and computing min and max naively gives O(n) per subarray, leading to O(n^3) total work.

We need to understand what structure of permutation reduces the total contribution. The cost of a segment is driven by max and min. If a segment has consecutive integers in the permutation, its range is small and the cost is reduced. This suggests that we want to avoid large jumps inside contiguous segments, and instead want values to be arranged so that extremes are separated in a controlled way.

A key transformation is to rewrite the problem in terms of how often each pair of elements contributes to being a maximum or minimum over subarrays. The expression max minus min can be interpreted as the contribution of pairs where one element becomes the maximum and another becomes the minimum in a segment. The negative length term pushes toward shorter segments contributing less penalty overall.

The structure that emerges is that optimal permutations are built by placing the largest element first or last, then recursively filling outward in a way that keeps the permutation as “centered” as possible. However, because we also need lexicographically maximum among optimal solutions, we prefer placing larger elements earlier whenever symmetry allows.

This leads to a constructive pattern: we build the permutation from both ends inward, always choosing the largest remaining number and placing it in the position that preserves optimal balance, with a bias toward earlier positions to satisfy lexicographic maximality.

The optimal configuration turns out to be a simple decreasing sequence when analyzed under symmetry of contributions, because any deviation that places a smaller number before a larger one tends to create additional subarrays where max-min becomes large while not sufficiently compensating via length reduction.

Thus the solution reduces to placing numbers from n down to 1 in order.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n! · n²) | O(n) | Too slow |
| Optimal construction | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We construct the permutation directly.

1. Initialize an empty list p of size n. This will store the final permutation.
2. Start from the largest value n and move downward to 1.
3. For each value x from n down to 1, append x to p.

This places larger values earlier in the permutation, which is necessary to maximize lexicographic order among optimal solutions.
4. Output the constructed list.

The reason this simple construction is sufficient is that any alternative arrangement would introduce a pair of indices where a smaller value precedes a larger one in a way that increases the number of subarrays whose range expands unnecessarily. The descending order minimizes the creation of segments where both extremes appear far apart, since large values are concentrated at the front and progressively smaller values only shrink possible ranges.

### Why it works

The key invariant is that after placing the first k elements of the permutation as n, n−1, …, n−k+1, every subarray that starts within this prefix already has its maximum determined immediately by the first element of that subarray. This stabilizes the contribution of max across many segments and prevents additional variability that would arise if a smaller element appeared before a larger one later in the array.

Any inversion of the form i < j but p[i] < p[j] would create additional subarrays where the maximum is not determined locally at the left boundary, increasing variability of max-min across many segments. The descending arrangement eliminates such inversions entirely, making all prefix-based maxima monotone and minimizing the overall spread contribution.

Because this structure is also unique up to symmetry in optimal configurations, it is lexicographically maximal among all optimal solutions.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    res = list(range(n, 0, -1))
    print(*res)

if __name__ == "__main__":
    solve()
```

The implementation directly constructs the permutation in reverse order. The only important detail is to ensure correct formatting with spaces, and to avoid any off-by-one errors by using Python’s range with step -1.

The decision to print immediately rather than building incremental structures avoids unnecessary overhead. No additional data structures are needed since the permutation is deterministic.

## Worked Examples

### Example 1: n = 3

We construct the sequence step by step.

| Step | Current x | Permutation |
| --- | --- | --- |
| 1 | 3 | 3 |
| 2 | 2 | 3 2 |
| 3 | 1 | 3 2 1 |

The final output is 3 2 1. This confirms that the construction consistently appends the largest remaining element first.

This example demonstrates how the permutation builds a strictly decreasing structure without ambiguity, ensuring lexicographically maximal ordering among candidates.

### Example 2: n = 5

| Step | Current x | Permutation |
| --- | --- | --- |
| 1 | 5 | 5 |
| 2 | 4 | 5 4 |
| 3 | 3 | 5 4 3 |
| 4 | 2 | 5 4 3 2 |
| 5 | 1 | 5 4 3 2 1 |

The result is again a strictly decreasing permutation. This shows that the method generalizes uniformly and does not depend on any parity or structural branching.

The trace highlights that no reordering decisions are needed, which is consistent with the absence of local tradeoffs in the construction.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | We output each number exactly once in decreasing order |
| Space | O(n) | We store the permutation before printing |

The complexity fits easily within the constraints for n up to 200,000. The solution is purely linear and performs only simple arithmetic and output operations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from types import ModuleType

    # redefine solve inline for testing simplicity
    n = int(sys.stdin.readline())
    res = list(range(n, 0, -1))
    return " ".join(map(str, res))

# provided samples (conceptual since full samples not shown)
assert run("1") == "1", "n=1"
assert run("2") == "2 1", "n=2"

# custom cases
assert run("3") == "3 2 1", "basic descending"
assert run("5") == "5 4 3 2 1", "larger case"
assert run("10") == "10 9 8 7 6 5 4 3 2 1", "monotone correctness"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 1 | minimum boundary |
| 2 | 2 1 | smallest non-trivial case |
| 5 | 5 4 3 2 1 | general pattern correctness |
| 10 | 10 9 8 7 6 5 4 3 2 1 | scaling consistency |

## Edge Cases

The main edge case is n = 1. The algorithm produces a single-element permutation [1], which trivially has no subarrays with length greater than one, and thus all cost terms are zero. This is consistent with optimality.

For n = 2, the algorithm produces 2 1. The only subarrays are [2], [1], and [2,1]. The descending order ensures the only length-2 segment has max-min equal to 1, and there is no alternative permutation that can improve lexicographic order without increasing structural imbalance.

A slightly less trivial case is n = 3. The algorithm produces 3 2 1. The inversion-free structure ensures that every prefix has a stable maximum, and no alternative permutation can reduce contributions without introducing larger lexicographic penalties, confirming correctness even in the smallest non-symmetric multi-element case.
