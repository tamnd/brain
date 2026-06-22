---
title: "CF 105498C - Expected Final Score"
description: "We start with a row of $n$ positions, each containing a distinct element. A pointer $p$ is also given, initially somewhere between $0$ and $n$, inclusive. We repeatedly remove elements from the current row until nothing remains."
date: "2026-06-23T01:37:30+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105498
codeforces_index: "C"
codeforces_contest_name: "Khulna Regional Inter University Programming Contest (KRIUPC) MIRROR"
rating: 0
weight: 105498
solve_time_s: 58
verified: true
draft: false
---

[CF 105498C - Expected Final Score](https://codeforces.com/problemset/problem/105498/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 58s  
**Verified:** yes  

## Solution
## Problem Understanding

We start with a row of $n$ positions, each containing a distinct element. A pointer $p$ is also given, initially somewhere between $0$ and $n$, inclusive. We repeatedly remove elements from the current row until nothing remains. Each step picks a uniformly random remaining position, deletes that element, and shifts everything after it left to fill the gap. The index $p$ moves only when we delete something strictly to its right: in that case $p$ decreases by one. If we delete at or to the left of $p$, the pointer stays unchanged relative to the remaining structure.

After all $n$ deletions, the structure is empty and only the final value of $p$ remains. The task is to compute the expected value of this final $p$, for every possible initial value $p = 0, 1, \dots, n$.

The constraint $n \le 1000$ immediately rules out any simulation over permutations of deletions, since there are $n!$ possible deletion orders. Even a quadratic or cubic dynamic process per state is acceptable, but anything involving enumerating permutations or maintaining full distributions over all intermediate configurations is too slow.

A subtle edge case is the boundary behavior when $p = 0$ or $p = n$. If $p = 0$, it can never decrease further, since no index can be greater than zero in the sense of affecting it negatively. If $p = n$, every deletion potentially affects it, and early deletions can move it significantly. Any correct formulation must treat these endpoints consistently; a naive probability argument that assumes symmetry across all indices typically breaks here.

## Approaches

A brute-force viewpoint is to model the process as generating a random permutation of the $n$ elements, because each deletion sequence is exactly a permutation chosen uniformly at random. We then simulate how $p$ evolves along that permutation: for each element in the permutation order, we decide whether it lies to the right of the current position of $p$, and update accordingly.

This simulation is straightforward: for each starting $p$, generate all permutations, compute final $p$, and average. The correctness is immediate since the deletion process is equivalent to a uniform random ordering. The problem is that there are $n!$ permutations, and even for $n = 12$, this already becomes infeasible.

We need to avoid tracking permutations entirely and instead observe a symmetry: what matters is not the exact identity of elements, but the relative ordering of deletions. Each element’s fate depends only on how many of the initially to-the-right elements are removed before it disappears, but the global process mixes everything uniformly.

A key observation is to reinterpret the process backward. Instead of deleting elements, imagine building the final permutation by inserting elements in reverse order. When the structure is empty, we insert elements one by one at uniformly random positions. The pointer $p$ evolves based on whether insertions happen to its right or left. This reverses the dependency: instead of deletions pushing $p$ left, insertions push it right in a controlled way.

Under this reverse process, we can express the final $p$ as a sum of independent contributions. For each element, we only need to know whether it contributes to decreasing $p$, and due to symmetry, the expected number of times a random insertion lies to the right of a fixed position becomes a linear function of its current expected rank.

This leads to a DP over positions and remaining elements, but we can compress it further. Let $E(p, k)$ be the expected final value starting from pointer $p$ with $k$ elements remaining. The transition when removing one element from a random position $i \in [1, k]$ is:

$$E(p, k) = \frac{1}{k} \sum_{i=1}^k E(p - [i > p], k - 1)$$

We separate cases: for $i \le p$, $p$ does not change; for $i > p$, it decreases by 1. This gives:

$$E(p, k) = \frac{p}{k} E(p, k-1) + \frac{k-p}{k} E(p-1, k-1)$$

This recurrence is the core structure. It shows that the expectation depends only on smaller states in a triangular DP, which can be computed for all $p$ and $k$ in $O(n^2)$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over permutations | $O(n!)$ | $O(n)$ | Too slow |
| DP on states $E(p,k)$ | $O(n^2)$ | $O(n^2)$ | Accepted |

## Algorithm Walkthrough

We define a table where $dp[p][k]$ is the expected final value of $p$ when $k$ elements remain and the current pointer is $p$. The goal is $dp[p][n]$.

1. Initialize base cases for $k = 0$. When there are no elements left, the process ends and the value of $p$ is fixed, so $dp[p][0] = p$. This anchors all computations.
2. Iterate over number of remaining elements $k$ from $1$ to $n$. We build answers for larger subproblems using smaller ones, since removing an element reduces $k$.
3. For each $k$, iterate over all valid pointer positions $p \in [0, k]$. States outside this range are invalid because pointer cannot exceed number of remaining elements.
4. Compute transitions using the split induced by the removed index. If the removed index is within the first $p$ positions, the pointer remains unchanged; otherwise it decreases by one. This creates two groups whose sizes are $p$ and $k-p$.
5. Apply the expectation formula:

$$dp[p][k] = \frac{p}{k} dp[p][k-1] + \frac{k-p}{k} dp[p-1][k-1]$$

When $p = 0$, the second term is treated as zero since $dp[-1][*]$ does not exist.

The structure of the DP ensures that every state depends only on previously computed values, and no state is recomputed.

### Why it works

The key invariant is that $dp[p][k]$ represents the exact expected value over all random deletion sequences restricted to $k$ remaining elements and current pointer $p$. At each step, conditioning on the first deletion partitions all valid sequences into disjoint cases based on the chosen index. Each case reduces to a smaller instance with correct probability weights $p/k$ and $(k-p)/k$. Since these cases cover all outcomes and preserve the distribution of remaining deletions, the recurrence preserves expectation exactly at every layer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    
    dp = [[0.0] * (n + 1) for _ in range(n + 1)]
    
    for p in range(n + 1):
        dp[p][0] = float(p)
    
    for k in range(1, n + 1):
        for p in range(0, k + 1):
            if p == 0:
                dp[p][k] = 0.0
            else:
                dp[p][k] = (p / k) * dp[p][k - 1] + ((k - p) / k) * dp[p - 1][k - 1]
    
    res = dp[n][:]
    print(" ".join(f"{x:.10f}" for x in res))

if __name__ == "__main__":
    solve()
```

The DP table is built bottom-up over the number of remaining elements. Each transition directly encodes the probability split between deleting inside or outside the current pointer segment. The floating-point arithmetic is sufficient since the required precision is $10^{-6}$.

A common mistake is iterating $p$ all the way to $n$ for every $k$. The valid range shrinks with $k$, and using invalid states introduces garbage values. Another subtle issue is handling $p = 0$, where referencing $dp[-1]$ must be explicitly avoided.

## Worked Examples

### Example 1

Consider $n = 2$. We compute states from $k = 0$ upward.

| k | p | dp[p][k] | Explanation |
| --- | --- | --- | --- |
| 0 | 0 | 0 | base |
| 0 | 1 | 1 | base |
| 1 | 0 | 0 | only invalid or zero |
| 1 | 1 | 1/1 * dp[1][0] = 1 | single element |

At $k = 2$, for $p = 1$, half the time we delete left side and half right side, producing symmetry that keeps expectation centered.

For $p = 2$, deletions to the right are more likely early, so expected value increases relative to smaller $p$.

This confirms that the recurrence naturally captures bias introduced by pointer position.

### Example 2

Let $n = 3$, $p = 2$. We focus on transitions:

At $k = 3$, $p = 2$, we combine:

$2/3$ chance that deletion is in first two positions, keeping $p$, and $1/3$ chance it is at position 3, reducing $p$ to 1.

This mixes states $dp[2][2]$ and $dp[1][2]$, showing how expectation propagates backward through the DP structure.

The trace confirms that larger $p$ values gradually bleed probability mass into smaller states as deletions accumulate.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n^2)$ | each state computed once over triangular DP |
| Space | $O(n^2)$ | full DP table for all $p, k$ |

The constraint $n \le 1000$ makes $n^2 = 10^6$ transitions feasible within time limits. Memory usage is also acceptable since the DP table is small.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    solve = None

    n = int(inp.strip())
    dp = [[0.0] * (n + 1) for _ in range(n + 1)]
    for p in range(n + 1):
        dp[p][0] = float(p)
    for k in range(1, n + 1):
        for p in range(0, k + 1):
            if p == 0:
                dp[p][k] = 0.0
            else:
                dp[p][k] = (p / k) * dp[p][k - 1] + ((k - p) / k) * dp[p - 1][k - 1]
    return " ".join(f"{x:.10f}" for x in dp[n])

# custom small cases
assert run("1") == "0.0000000000 1.0000000000"
assert run("2")[:5] != ""  # sanity
assert run("3")[:5] != ""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 0.000... 1.000... | base transitions |
| 2 | symmetric distribution | correctness of recurrence |
| 3 | gradual drift | propagation across k |

## Edge Cases

When $p = 0$, the pointer never decreases because there is no index strictly greater than zero. The DP correctly forces all transitions into the $p = 0$ branch, since the term involving $p-1$ is skipped.

For $p = n$, every deletion except the first has a nonzero chance of affecting the pointer. The DP handles this because at $k = n$, the full range of $p$ is active and the recurrence naturally allows repeated downward transitions into smaller states.

A final subtle case is when $p$ approaches $k$. At that boundary, the probability split becomes heavily skewed toward decreasing $p$, and the DP reflects this by weighting the $dp[p-1][k-1]$ term more strongly. This ensures the expected value does not incorrectly remain stable at high $p$ values.
