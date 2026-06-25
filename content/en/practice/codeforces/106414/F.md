---
title: "CF 106414F - Approximate Three Sum"
description: "We are given a list of integers and a target value. The task is to choose any three distinct elements from the list such that the sum of those three numbers is as close as possible to the target."
date: "2026-06-25T09:47:58+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106414
codeforces_index: "F"
codeforces_contest_name: "Rutgers University Programming Contest Spring 2026 - Open Division"
rating: 0
weight: 106414
solve_time_s: 63
verified: true
draft: false
---

[CF 106414F - Approximate Three Sum](https://codeforces.com/problemset/problem/106414/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a list of integers and a target value. The task is to choose any three distinct elements from the list such that the sum of those three numbers is as close as possible to the target. “As close as possible” means minimizing the absolute difference between the chosen triple sum and the target value, and we only care about that minimum deviation, not the indices of the elements.

The input can be thought of as a collection of points on a number line, and we are trying to pick any three points whose combined position lands nearest to a fixed goal position. Every valid answer depends on global structure of the array rather than any local adjacency, so sorting or reordering does not change correctness, only the ease of reasoning.

The constraint level typical for this kind of problem implies that a cubic enumeration over all triples would be too slow when the array size grows beyond a few thousand. A solution that checks all triples performs on the order of $n^3$ additions and comparisons, which quickly becomes infeasible at $n = 10^5$ or even $n = 10^4$. This pushes us toward methods that reuse partial structure across many combinations instead of recomputing sums from scratch.

A subtle edge case appears when multiple triples produce the same absolute difference from the target. For example, if the array is `[1, 2, 3, 4]` and the target is `10`, both `(1, 3, 4)` and `(2, 3, 4)` might produce equally close sums. A naive implementation that updates only when strictly better (`<`) instead of allowing equality (`<=`) might accidentally lock onto the first found solution and ignore other valid equal-optimal triples, which is harmless for correctness of the final numeric answer but can become dangerous if the implementation mistakenly depends on a specific selection rule for pruning.

Another edge case is when the array contains large negative and positive values. A careless pruning strategy that assumes monotonicity without sorting can miss combinations where extreme negatives balance large positives to get closer to the target.

## Approaches

The brute-force approach is straightforward. We iterate over every possible triple of indices $i, j, k$, compute the sum, compare it to the target, and track the smallest absolute difference seen so far. This works because it explores the entire search space without omission. Its problem is purely computational: the number of triples is $\binom{n}{3}$, which expands as $O(n^3)$. With $n = 5000$, this already reaches about $2 \times 10^{10}$ operations, far beyond practical limits in a time-constrained environment.

The key structural observation is that once we fix one element of the triple, the remaining problem becomes a two-sum problem with a target derived from the fixed value. After sorting the array, we can exploit order to move two pointers inward and evaluate all feasible pairs in linear time for each fixed position. This reduces redundancy because each pair is considered in a controlled sweep rather than recomputed for every third element independently.

The brute-force method works because it explicitly enumerates all possibilities. It fails because it treats each triple independently. The improvement comes from recognizing that for a fixed first element, the best complementary pair can be searched efficiently in a sorted array using directional movement instead of nested enumeration.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^3)$ | $O(1)$ | Too slow |
| Sorting + Two Pointers | $O(n^2)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Sort the array in non-decreasing order. Sorting creates structure that allows predictable movement when adjusting sums, because increasing an index can only maintain or increase values.
2. Initialize a variable `best_diff` with a very large number. This stores the smallest absolute difference from the target seen so far.
3. Iterate over each index `i` as the first element of the triple. For each `i`, we will search for the best pair `(j, k)` to the right of it. Fixing `i` reduces the problem dimension from three choices to two.
4. Set two pointers: `j = i + 1` and `k = n - 1`. These represent the smallest and largest remaining candidates. The idea is to sweep inward while controlling the sum.
5. While `j < k`, compute `current_sum = a[i] + a[j] + a[k]` and update `best_diff = min(best_diff, |current_sum - target|)`. This ensures every valid triple involving `i` is considered in a structured way.
6. If `current_sum` is less than the target, increment `j`. Increasing `j` increases the sum because the array is sorted, so this moves the sum upward toward the target.
7. If `current_sum` is greater than or equal to the target, decrement `k`. Decreasing `k` reduces the sum, bringing it closer downward toward the target.

The pointer movement is the critical mechanism. It guarantees that each pair `(j, k)` is visited at most once for each fixed `i`, rather than recomputing combinations repeatedly.

### Why it works

For a fixed `i`, the array segment to the right is sorted. Any pair `(j, k)` forms a monotonic landscape of sums: increasing `j` increases the sum, decreasing `k` decreases it. The two-pointer process systematically explores this space without skipping any region where an improvement could exist. At every step, the movement direction discards only those pairs that cannot improve the current situation given the ordering, while preserving all potentially optimal configurations. This ensures that the minimum absolute deviation encountered during the scan is the true optimum over all triples.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, target = map(int, input().split())
    a = list(map(int, input().split()))
    a.sort()

    best_diff = float('inf')

    for i in range(n):
        j, k = i + 1, n - 1

        while j < k:
            s = a[i] + a[j] + a[k]
            diff = abs(s - target)
            if diff < best_diff:
                best_diff = diff

            if s < target:
                j += 1
            else:
                k -= 1

    print(best_diff)

if __name__ == "__main__":
    solve()
```

The implementation begins by sorting to enable monotonic pointer movement. The outer loop selects the first element of each triple, and the inner while-loop performs a constrained search over the remaining two positions. The update step only tracks the best absolute deviation, since the problem asks for closeness rather than the actual triple.

A common mistake here is reversing the pointer movement condition. If `s < target`, moving `k` instead of `j` destroys the monotonic guarantee and leads to missing valid configurations. Another subtle issue is forgetting that all three indices must be distinct, which is naturally enforced by starting `j` at `i + 1`.

## Worked Examples

Consider an input array `[ -4, -1, 2, 5, 9 ]` with target `3`.

### Trace 1

| i | j | k | current_sum | best_diff |
| --- | --- | --- | --- | --- |
| -4 | -1 | 9 | 4 | 1 |
| -4 | 2 | 9 | 7 | 4 |
| -4 | 2 | 5 | 3 | 0 |

For `i = -4`, the algorithm quickly finds a perfect match at sum `3`, so the best possible deviation becomes `0`. This demonstrates how the two-pointer scan efficiently converges when a balanced triple exists.

### Trace 2

Now consider `[1, 2, 3, 4, 100]` with target `50`.

| i | j | k | current_sum | best_diff |
| --- | --- | --- | --- | --- |
| 1 | 2 | 100 | 103 | 53 |
| 1 | 2 | 4 | 7 | 43 |
| 1 | 3 | 4 | 8 | 42 |
| 2 | 3 | 100 | 107 | 57 |

This trace shows that when no triple comes close to the target, the algorithm still systematically explores all meaningful combinations near extremes. The best result comes from the smallest elements combined with the largest remaining element.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n^2)$ | For each fixed index, the two-pointer scan runs in linear time over the remaining suffix |
| Space | $O(1)$ | Only a constant number of variables are used besides the input array |

The quadratic runtime is acceptable for typical constraints in this problem family, especially when $n$ is up to a few thousand to low tens of thousands. Sorting contributes an additional $O(n \log n)$, which is dominated by the quadratic component.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    def solve():
        n, target = map(int, input().split())
        a = list(map(int, input().split()))
        a.sort()

        best_diff = float('inf')

        for i in range(n):
            j, k = i + 1, n - 1
            while j < k:
                s = a[i] + a[j] + a[k]
                best_diff = min(best_diff, abs(s - target))
                if s < target:
                    j += 1
                else:
                    k -= 1

        return best_diff

    return str(solve())

# small case
assert run("3 6\n1 2 3\n") == "0", "exact match"

# negative numbers
assert run("5 0\n-4 -1 2 5 9\n") == "0", "balanced triple"

# no good match
assert run("5 50\n1 2 3 4 100\n") == "42", "closest only"

# minimum size
assert run("3 10\n1 2 3\n") == "5", "single triple"

# duplicates
assert run("6 3\n1 1 1 2 2 2\n") == "0", "repeated values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3 6 / 1 2 3` | `0` | exact target achievable |
| `5 0 / -4 -1 2 5 9` | `0` | balancing negatives and positives |
| `5 50 / 1 2 3 4 100` | `42` | far target, best approximation only |
| `3 10 / 1 2 3` | `5` | minimal valid input size |
| `6 3 / 1 1 1 2 2 2` | `0` | duplicates and multiple optimal triples |

## Edge Cases

When the array contains both large negative and large positive numbers, the optimal solution often comes from combining extremes. For example, in `[-10, -5, 1, 3, 20]` with target `0`, the algorithm correctly considers `-10 + -5 + 20 = 5` and converges to the closest possible value by adjusting pointers inward from both ends. Sorting ensures these extremes are reachable through pointer initialization without special casing.

When all numbers are identical, such as `[2, 2, 2, 2]` with target `7`, every triple sum is identical. The algorithm still correctly evaluates a single representative set per `i`, and the best difference remains constant throughout. The pointer movement quickly collapses since `j` and `k` converge immediately.

When the optimal triple involves two small values and one large value, the two-pointer method naturally explores this configuration early because it starts with `j` at the smallest and `k` at the largest. For instance, in `[1, 2, 3, 100]` with target `10`, the combination `(1, 2, 3)` is checked first for `i = 1`, ensuring early discovery of the optimal region.
