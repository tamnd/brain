---
title: "CF 104452D - Professor R's. Median"
description: "We are given a list of integers and we need to select a single element according to a rule that depends on the smallest and largest values in the list."
date: "2026-06-30T14:42:10+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104452
codeforces_index: "D"
codeforces_contest_name: "ICPC Central Russia Regional Contest - 2020"
rating: 0
weight: 104452
solve_time_s: 91
verified: true
draft: false
---

[CF 104452D - Professor R's. Median](https://codeforces.com/problemset/problem/104452/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 31s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a list of integers and we need to select a single element according to a rule that depends on the smallest and largest values in the list.

Instead of sorting the whole array and taking a classical median, we first compute a reference value, which is the arithmetic mean of the minimum and maximum element. Then we look for the element in the array that is closest to this reference value. Distance is measured in the usual absolute difference sense. If multiple elements are equally close, we choose the smallest value among them.

So the task is not about positional ordering in a sorted array, but about proximity to the midpoint of the extreme values.

The input size goes up to 100,000 elements with values up to roughly 2·10^9 in magnitude. This immediately rules out solutions that recompute anything expensive per candidate or try all pairs. Anything quadratic, such as comparing every element to every other element or sorting inside nested loops, would be too slow. A linear scan after simple preprocessing is the only viable direction.

A few edge cases matter here.

If all elements are equal, the minimum and maximum coincide, so the reference value is exactly that number. Every element is equally close, so the answer must be that same value. Any solution that mishandles floating-point midpoint computation or ties can still break this case.

If the array contains values symmetrically placed around the midpoint, for example [1, 3] or [1, 2, 3], multiple elements may tie in distance. The tie-breaking rule forces us to pick the smallest of those candidates, so we must explicitly track ties, not just keep any closest value.

Finally, because values can be large, computing mid = (min + max) / 2 as a floating-point number can introduce precision issues if done carelessly. However, we do not need floating point at all if we compare distances algebraically.

## Approaches

A direct interpretation suggests computing the minimum and maximum of the array, then checking every element to see how close it is to their midpoint. The brute-force idea is straightforward: compute min and max, compute the midpoint, then iterate over all elements and track the one with minimal absolute difference to that midpoint.

This already gives an O(n) solution, so there is no need for sorting or nested comparisons. The only subtlety is how we compare distances without introducing floating-point errors and how we handle ties consistently.

The key observation is that the midpoint is fixed once min and max are known, so the problem reduces to a single pass selection problem: choose the element minimizing |a[i] - (min + max)/2|. Since comparisons against a constant threshold can be rewritten without division, we can avoid floats entirely by comparing 2 * a[i] against (min + max). This keeps everything in integers and preserves exact ordering.

The brute-force mental model works because we only need global extrema and one pass over the array. It fails only if implemented with naive floating-point midpoint computation or if tie-breaking is not explicitly handled.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (min/max + scan) | O(n) | O(1) | Accepted |
| Optimal (same with integer-safe comparisons) | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read all numbers and compute both the minimum value and maximum value in the array. This establishes the reference interval endpoints that define the target midpoint.
2. Compute the sum of these endpoints, which represents twice the midpoint. We avoid division because we only need comparisons, not the actual midpoint value.
3. Initialize a variable to store the best candidate and another to store the best distance seen so far. The best distance starts as infinity.
4. Iterate through every element in the array. For each element, compute its absolute distance from the midpoint in a scaled integer form, comparing |2 * a[i] - (min + max)|. This measures the same ordering as distance to the true midpoint.
5. If this distance is smaller than the best distance so far, update both the best distance and the best candidate value.
6. If the distance is equal to the best distance, update the candidate only if the current value is smaller. This enforces the tie-breaking rule.
7. After processing all elements, output the stored candidate.

### Why it works

The midpoint derived from the global minimum and maximum is a fixed constant independent of the array structure. Every element is evaluated purely by its distance to this constant, so the problem reduces to selecting a global argmin over a deterministic function. The transformation to doubled values preserves ordering because multiplication by 2 is monotonic and does not affect comparisons. The tie-breaking rule is explicitly enforced during the scan, ensuring deterministic selection among equal-distance candidates.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    mn = min(a)
    mx = max(a)
    target_sum = mn + mx

    best_val = None
    best_dist = None

    for x in a:
        dist = abs(2 * x - target_sum)
        if best_dist is None or dist < best_dist or (dist == best_dist and x < best_val):
            best_dist = dist
            best_val = x

    print(best_val)

if __name__ == "__main__":
    solve()
```

The solution begins by extracting the global extrema, which define the reference midpoint implicitly. Instead of computing the midpoint directly, it works with the doubled expression to keep all arithmetic integral and exact. The loop maintains a running best candidate, updating it only when a strictly better distance is found or when a tie is broken by a smaller value.

A common implementation mistake is computing `(mn + mx) / 2` using floating-point arithmetic and then comparing distances using floats. That can introduce rounding errors when values are large. Another subtle mistake is failing to enforce the tie-breaking rule strictly, which leads to incorrect outputs when multiple values are equidistant.

## Worked Examples

### Example 1

Input:

```
5
1 1 1 1 1
```

Here mn = 1 and mx = 1, so the reference midpoint is 1.

| Step | x | 2x | mn+mx | dist | best_val | best_dist |
| --- | --- | --- | --- | --- | --- | --- |
| init | - | - | 2 | - | - | inf |
| 1 | 1 | 2 | 2 | 0 | 1 | 0 |
| 2 | 1 | 2 | 2 | 0 | 1 | 0 |
| ... | 1 | 2 | 2 | 0 | 1 | 0 |

Every element is identical, so all distances are zero. The tie-breaking rule always keeps the smallest value, which is still 1. This confirms correctness in the degenerate case where min equals max.

### Example 2

Input:

```
3
1 2 3
```

Here mn = 1, mx = 3, so midpoint is 2.

| Step | x | 2x | mn+mx | dist | best_val | best_dist |
| --- | --- | --- | --- | --- | --- | --- |
| init | - | - | 4 | - | - | inf |
| 1 | 1 | 2 | 4 | 2 | 1 | 2 |
| 2 | 2 | 4 | 4 | 0 | 2 | 0 |
| 3 | 3 | 6 | 4 | 2 | 2 | 0 |

The element 2 is exactly the midpoint, so it becomes the best candidate immediately. This demonstrates that exact matches dominate all others regardless of tie-breaking.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | one pass to compute min/max and one pass to select best element |
| Space | O(1) | only a few variables are maintained regardless of input size |

The constraints allow up to 100,000 elements, so a linear scan is comfortably within limits. The solution performs only constant work per element and avoids sorting or repeated passes beyond linear time.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))

    mn = min(a)
    mx = max(a)
    target_sum = mn + mx

    best_val = None
    best_dist = None

    for x in a:
        dist = abs(2 * x - target_sum)
        if best_dist is None or dist < best_dist or (dist == best_dist and x < best_val):
            best_dist = dist
            best_val = x

    return str(best_val)

# provided samples
assert run("5\n1 1 1 1 1\n") == "1"
assert run("3\n1 2 3\n") == "2"

# custom cases
assert run("1\n10\n") == "10", "single element"
assert run("2\n1 100\n") == "1", "tie both equal distance choose smaller"
assert run("4\n5 1 9 3\n") == "5", "midpoint selection"
assert run("6\n2 2 2 2 2 2\n") == "2", "all equal"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 10 | minimal size handling |
| 1 100 | 1 | tie-breaking correctness |
| 5 1 9 3 | 5 | general midpoint behavior |
| all equal | 2 | degenerate uniform array |

## Edge Cases

When all values are identical, min equals max and the target midpoint collapses to that same value. The algorithm sets `target_sum = 2 * x`, so every element produces distance zero. Because the tie-breaking rule prefers smaller values and all values are equal, the first encountered element remains valid and the final answer is that repeated value.

When there are two elements equally distant from the midpoint, such as `[1, 3]`, both yield distance 2 from midpoint 2. The algorithm compares first 1, then 3. After processing 1, best_val becomes 1. When processing 3, distance ties but 3 is not smaller than 1, so it is ignored. The output remains 1, matching the required rule.
