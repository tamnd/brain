---
title: "CF 103150A - Addition Range Queries"
description: "We are given an array of integers, and we repeatedly apply a very specific transformation to it. In one transformation step, every position is updated at the same time so that each element becomes the sum of all the other elements in the array, excluding itself."
date: "2026-07-03T19:53:48+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103150
codeforces_index: "A"
codeforces_contest_name: "EZ Programming Contest #1"
rating: 0
weight: 103150
solve_time_s: 52
verified: true
draft: false
---

[CF 103150A - Addition Range Queries](https://codeforces.com/problemset/problem/103150/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 52s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers, and we repeatedly apply a very specific transformation to it. In one transformation step, every position is updated at the same time so that each element becomes the sum of all the other elements in the array, excluding itself.

After performing this transformation exactly $k$ times, we are asked to compute how spread out the final array values are, measured as the maximum absolute difference between any two elements.

A key way to reinterpret the operation is to focus on the total sum of the array. Let the current sum be $S$. After one operation, each element $a_i$ becomes $S - a_i$. This means every value is being reflected around the current total sum in a very structured way, which suggests that the evolution of the array is highly regular rather than chaotic.

The constraints make this observation critical. The number of operations $k$ can be extremely large, up to $10^9$, so simulating the process step by step is impossible. Even a single pass per operation would already exceed time limits when summed over all test cases. This immediately rules out any approach that depends on explicitly applying the transformation repeatedly.

Another constraint that matters is that the total number of elements across all test cases is up to $2 \cdot 10^5$. This suggests we should aim for an $O(n)$ or $O(n \log n)$ solution per test case, ideally with constant time processing per test after preprocessing.

A subtle edge case appears when $n = 1$. In that case, the operation replaces the only element with the sum of all other elements, which is zero. But since there are no "other elements", the sum is zero and remains zero forever. This means the answer is always zero regardless of $k$. Any solution must explicitly handle this case to avoid unnecessary computation or incorrect transformations.

A second important edge case is when all elements are equal. After one operation, each element becomes $(n-1)x$, so the array remains uniform. The difference between maximum and minimum stays zero, and this remains true for all further operations.

The interesting behavior only appears when values differ, and the key challenge is to understand how the difference between elements evolves under repeated transformations.

## Approaches

A brute force simulation directly applies the transformation $k$ times. Each operation recomputes the total sum and rebuilds the array in $O(n)$, leading to a total complexity of $O(nk)$. With $k$ up to $10^9$, this is completely infeasible.

The key insight is to track how individual elements relate to each other rather than their absolute values. If we expand one operation, each element becomes $S - a_i$, which is equivalent to $(n-1)\cdot \text{mean of array} - (a_i - \text{mean})$ up to linear transformations. More importantly, what matters for the final answer is not the absolute values but the difference between two positions.

Let us consider two elements $a_i$ and $a_j$. After one operation, their difference becomes:

$$(S - a_i) - (S - a_j) = a_j - a_i$$

So the difference flips sign but preserves magnitude.

After two operations, the difference flips again and returns to the original sign. This means the structure of pairwise differences is periodic with period 2. The entire array alternates between two states: the original array, and its transformed version where each value is $S - a_i$.

Thus, the problem reduces to evaluating at most two states depending on whether $k$ is even or odd.

We compute:

- If $k$ is even, the array structure is equivalent to the original.
- If $k$ is odd, each element becomes $S - a_i$, where $S$ is the initial sum.

From there, computing the maximum difference is straightforward: we just take the difference between max and min in the corresponding state.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | $O(nk)$ | $O(n)$ | Too slow |
| Parity Observation (2-state system) | $O(n)$ | $O(1)$ extra | Accepted |

## Algorithm Walkthrough

1. Read the array and compute its total sum $S$, as well as its minimum and maximum values. These three values fully determine both possible states of the system, since the transformation depends only on $S$ and individual elements.
2. If $n = 1$, immediately output 0. With one element, the transformation always produces 0, and there is no variation.
3. If $k$ is even, we know the array remains effectively in its original configuration. The maximum difference is simply $\max(a) - \min(a)$, because no structural change affects relative ordering.
4. If $k$ is odd, each element becomes $S - a_i$. In this transformed array, the maximum element corresponds to $S - \min(a)$, and the minimum corresponds to $S - \max(a)$. This inversion happens because subtracting reverses ordering.
5. Compute the difference in the transformed state:

$$(S - \min(a)) - (S - \max(a)) = \max(a) - \min(a)$$

so the difference remains unchanged numerically.
6. Output this computed difference.

Why it works is rooted in the fact that each operation applies an affine transformation to the array values. While the values themselves shift significantly, all pairwise differences only alternate sign and never change magnitude. Since the problem asks only for the maximum absolute difference, the system collapses to two alternating states, making further iteration irrelevant.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        arr = list(map(int, input().split()))

        if n == 1:
            print(0)
            continue

        total = sum(arr)
        mn = min(arr)
        mx = max(arr)

        if k % 2 == 0:
            print(mx - mn)
        else:
            # transformed array would be S - a[i]
            # min becomes S - mx, max becomes S - mn
            print((total - mn) - (total - mx))

if __name__ == "__main__":
    solve()
```

The implementation follows the observation that we never explicitly construct intermediate arrays. We only track aggregate statistics. The only subtle point is handling the parity of $k$, since it determines whether we evaluate the original array or its transformed version.

The expression `(total - mn) - (total - mx)` is carefully ordered to reflect the correct transformed maximum minus transformed minimum. Expanding it algebraically shows it simplifies back to `mx - mn`, but keeping it in this form makes the logic explicit and avoids mistakes when adapting the idea to variants of the problem.

## Worked Examples

### Example 1

Input:

```
4 1
1 3 5 4
```

We compute:

- total = 13
- min = 1
- max = 5

| Step | State |
| --- | --- |
| Initial array | [1, 3, 5, 4] |
| k = 1 (odd) | transformed array uses S - a[i] |
| S | 13 |
| Transformed array | [12, 10, 8, 9] |

The maximum is 12 and minimum is 8.

So answer is 4.

This confirms that for odd $k$, the transformation flips values around the sum but preserves range width.

### Example 2

Input:

```
5 2
2 2 2 2 2
```

| Step | State |
| --- | --- |
| Initial array | [2, 2, 2, 2, 2] |
| min/max | 2 / 2 |
| k even | original state |

The array remains constant under transformation, so every step preserves equality among elements. The maximum difference remains 0.

This shows that uniform arrays are fixed points of the operation and never evolve.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ per test case | We compute sum, min, max once per array |
| Space | $O(1)$ extra | Only scalar aggregates are stored |

The constraints allow up to $2 \cdot 10^5$ total elements, so a single linear scan per test case is sufficient. No dependence on $k$ appears in the final algorithm, which is essential given that $k$ can be as large as $10^9$.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    out = []

    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))

        if n == 1:
            out.append("0")
            continue

        s = sum(a)
        mn, mx = min(a), max(a)

        if k % 2 == 0:
            out.append(str(mx - mn))
        else:
            out.append(str((s - mn) - (s - mx)))

    return "\n".join(out)

# provided sample
assert run("""3
4 1
1 3 5 4
1 1000
2020
10 100000
1 1 1 1 1 1 1 1 1 1
""") == """4
0
0"""

# all equal
assert run("""1
5 123
7 7 7 7 7
""") == "0"

# single element
assert run("""1
1 999
42
""") == "0"

# even k preserves range
assert run("""1
4 2
1 10 5 7
""") == "9"

# odd k still same range width
assert run("""1
4 1
1 10 5 7
""") == "9"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 0 | base case handling |
| all equal | 0 | fixed point behavior |
| even k | mx-mn | parity correctness |
| odd k | same range | transformation invariance |

## Edge Cases

For $n = 1$, the algorithm immediately outputs zero because there is no pair of elements to form a difference. The transformation degenerates to a constant zero sequence, so no further reasoning is needed.

For arrays where all elements are equal, every transformation produces another uniform array scaled by $n-1$, which preserves zero spread. The computed max-min remains zero, matching the correct answer for both even and odd $k$.

For large $k$, the solution never simulates operations. Instead, it relies entirely on parity, so values like $10^9$ do not affect runtime or correctness.
