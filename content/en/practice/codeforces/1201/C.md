---
title: "CF 1201C - Maximum Median"
description: "We are given a list of numbers and allowed to repeatedly increase any single element by one. Each such increment has a cost of one operation, and we have a total budget of at most $k$ operations."
date: "2026-06-13T15:12:32+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "greedy", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1201
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 577 (Div. 2)"
rating: 1400
weight: 1201
solve_time_s: 239
verified: true
draft: false
---

[CF 1201C - Maximum Median](https://codeforces.com/problemset/problem/1201/C)

**Rating:** 1400  
**Tags:** binary search, greedy, math, sortings  
**Solve time:** 3m 59s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a list of numbers and allowed to repeatedly increase any single element by one. Each such increment has a cost of one operation, and we have a total budget of at most $k$ operations. The goal is not to maximize the sum or any global statistic, but specifically to maximize the median after the array is sorted.

Since the array size is odd, the median is the element that ends up in position $n/2$ after sorting. The key difficulty is that when we increase some elements, the sorting order may change, so the median is not tied to a fixed index in the original array.

The constraints are large enough that any strategy that simulates operations one by one is impossible. With $n$ up to $2 \cdot 10^5$ and $k$ up to $10^9$, even a single operation loop of length $k$ would clearly exceed time limits. Any viable solution must reduce the problem to either sorting plus linear processing or a logarithmic search over the answer.

A subtle failure mode appears when thinking greedily about increasing the median position directly. If we only increase the current median element, we ignore the fact that other elements to its right may also need to be raised to preserve its median status after sorting. For example, if we only increment the median in isolation, a smaller element to its right could still block it from being the median after sorting.

A second mistake arises if we try to maintain a dynamic sorted structure and repeatedly adjust the median. This becomes too slow due to repeated insertions and deletions, and also obscures the real structure of the problem: only elements at or above the median position matter for the final answer.

## Approaches

A brute-force approach would simulate the process of applying operations in all possible distributions among elements. After each increment, we would resort the array and track the median. Even if we restrict ourselves to only distributing increments among promising elements, the number of possible distributions grows combinatorially with $k$, making this approach infeasible.

The key observation is that once the array is sorted, the median sits at a fixed position, and only the elements from that position onward can influence how large it can become. Any element to the left of the median does not constrain the median value because increasing them only helps the median or leaves it unchanged after re-sorting.

This leads to a greedy structure: we want to raise the median and everything to its right so that the median can be pushed upward as far as possible. If we fix a target value for the median, we can check how many operations are needed to make all elements in the right half at least that value. This naturally leads to a feasibility check.

From here, binary search becomes the natural tool. We search for the maximum median value such that it is possible to raise the median and the suffix of the array to that level within budget $k$. Each check is linear after sorting.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in $k$ | $O(n)$ | Too slow |
| Optimal (binary search + greedy check) | $O(n \log (k + \max a))$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We first sort the array so that the median position becomes fixed. Let $m = n/2$. From this point, the median we control is at index $m$, and only indices $m, m+1, \ldots, n-1$ matter for enforcing a candidate median value.

1. We sort the array because any reasoning about the median requires a stable ordering. Without sorting, we cannot identify which elements constrain the median.
2. We define a function that checks whether a given value $x$ can be achieved as the median. The idea is to force every element from index $m$ onward to be at least $x$, because if all of them are at least $x$, the median is also at least $x$.
3. To compute the cost of achieving this, we iterate from index $m$ to $n-1$ and accumulate the deficit $\max(0, x - a[i])$. This represents the minimum number of increments needed to lift these elements to $x$. The reasoning is that increasing elements left of the median does not help guarantee the median reaches $x$, because they can be pushed out of the median region by larger elements.
4. If the total required cost is within $k$, then the value $x$ is feasible. Otherwise, it is too large.
5. We binary search over $x$. The lower bound is the current median value, and the upper bound can be extended by adding all $k$ operations to the median element in the best case.
6. The final answer is the largest feasible $x$.

### Why it works

The crucial invariant is that in a sorted array, the median is determined entirely by the suffix starting at index $m$. Any strategy that successfully makes all elements in this suffix at least $x$ guarantees the median is also at least $x$, because at least half of the elements will be $\ge x$. Conversely, if the suffix cannot be raised to $x$ within the budget, then any attempt to achieve median $x$ fails since some element in the controlling region would remain below $x$, forcing the median down. This makes the feasibility check both necessary and sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

def can(a, m, k, x):
    cost = 0
    for i in range(m, len(a)):
        if a[i] < x:
            cost += x - a[i]
            if cost > k:
                return False
    return True

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    a.sort()

    m = n // 2

    lo = a[m]
    hi = a[m] + k

    ans = lo
    while lo <= hi:
        mid = (lo + hi) // 2
        if can(a, m, k, mid):
            ans = mid
            lo = mid + 1
        else:
            hi = mid - 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The sorting step is essential because it locks the median position so that all reasoning about feasibility becomes positional rather than value-based. The helper function `can` directly encodes the idea that only the right half contributes to enforcing a candidate median value.

Binary search is safe here because feasibility is monotonic: if a value $x$ is achievable, then any smaller value is also achievable since it requires no more operations.

The upper bound choice $a[m] + k$ reflects the best possible scenario where all operations are concentrated on the median element itself.

## Worked Examples

### Example 1

Input:

```
3 2
1 3 5
```

Sorted array is `[1, 3, 5]`, median index is `1`.

We test feasibility:

| x | cost from suffix [3,5] | feasible |
| --- | --- | --- |
| 3 | 0 | yes |
| 4 | 1 (only 5 already ok, 3 needs +1) | yes |
| 5 | 2 | yes |
| 6 | 3 | no |

The binary search stops at 5.

This shows that both median and right-side elements must be lifted together; increasing only the median is not enough because the suffix constrains feasibility.

### Example 2

Input:

```
5 3
1 2 10 10 10
```

Sorted array is `[1, 2, 10, 10, 10]`, median index is `2`.

| x | cost for [10,10,10] | cost total | feasible |
| --- | --- | --- | --- |
| 10 | 0 | 0 | yes |
| 11 | 3 | 3 | yes |
| 12 | 6 | 6 | no |

Answer is 11.

This demonstrates that once the suffix already contains large values, only partial lifting is needed, and the budget directly controls how far the median can be pushed upward.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log (k + \max a))$ | Sorting takes $O(n \log n)$, each feasibility check is $O(n)$, and binary search runs in logarithmic range over possible median values |
| Space | $O(1)$ extra | Only the array storage is used aside from input |

The constraints allow up to $2 \cdot 10^5$ elements, and the logarithmic factor is at most around 30, making this comfortably fast within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    a.sort()
    m = n // 2

    def can(x):
        cost = 0
        for i in range(m, n):
            if a[i] < x:
                cost += x - a[i]
                if cost > k:
                    return False
        return True

    lo, hi = a[m], a[m] + k
    ans = lo
    while lo <= hi:
        mid = (lo + hi) // 2
        if can(mid):
            ans = mid
            lo = mid + 1
        else:
            hi = mid - 1

    return str(ans)

# samples
assert run("3 2\n1 3 5\n") == "5"

# custom: minimum
assert run("1 10\n5\n") == "15"

# all equal
assert run("5 3\n7 7 7 7 7\n") == "8"

# large skew
assert run("5 5\n1 1 1 1 10\n") == "3"

# no budget
assert run("3 0\n1 2 3\n") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | direct increase | base case behavior |
| all equal | uniform lifting | symmetry handling |
| skewed array | suffix-driven cost | correctness of greedy cost |
| zero budget | no change | boundary constraint |

## Edge Cases

A key edge case is when the median is already the maximum element in the array. In that case, the suffix is very small and increasing only the median position might seem sufficient, but the feasibility check correctly accounts for any elements to the right that still need lifting.

Another case occurs when $k$ is extremely large. The binary search will push the median upward even beyond all existing elements, and the cost is entirely determined by how many elements lie in the suffix, not by their initial distribution.
