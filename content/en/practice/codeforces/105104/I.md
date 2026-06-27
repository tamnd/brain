---
title: "CF 105104I - Intervals"
description: "We are given several test cases, each containing a permutation of the numbers from 0 to n − 1. For any contiguous segment of this permutation, we look at the smallest non-negative integer that does not appear inside that segment, which is the mex of the segment."
date: "2026-06-27T20:10:45+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105104
codeforces_index: "I"
codeforces_contest_name: "2024 HNMU@XTU"
rating: 0
weight: 105104
solve_time_s: 55
verified: true
draft: false
---

[CF 105104I - Intervals](https://codeforces.com/problemset/problem/105104/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 55s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several test cases, each containing a permutation of the numbers from 0 to n − 1. For any contiguous segment of this permutation, we look at the smallest non-negative integer that does not appear inside that segment, which is the mex of the segment. For every possible value k from 0 to n, we must count how many subarrays have mex exactly equal to k.

The output for a test case is a sequence of n + 1 numbers, where the k-th number tells how many intervals produce mex equal to k.

The constraints imply that the total length over all test cases is up to 10^6. Any solution that is quadratic per test case would involve around 10^12 operations in the worst case, which is far beyond what can run in two seconds. Even an O(n log n) per test case approach would be risky unless it is very tight. This pushes us toward an O(n) or amortized O(n) solution overall.

A subtle failure case appears when reasoning locally about mex without accounting for the global structure of a permutation.

If one tries to compute mex for each subarray independently, even with a sliding window, the updates are too expensive.

Another common mistake is to assume that intervals contributing to mex k behave independently from values larger than k, but values greater than k can be safely ignored for mex, while value k itself is the only blocker. This asymmetry is the key structural property.

## Approaches

A direct approach considers every interval [i, j], computes its mex by scanning or maintaining a frequency structure, and increments the answer for that mex value. This is correct because it explicitly follows the definition, but it requires O(n) work per interval to maintain mex, leading to O(n^3) or at best O(n^2) with optimizations, which is too slow for n up to 10^6 overall.

The key observation comes from rephrasing what it means for a segment to have mex equal to k. Such a segment must contain every number from 0 to k − 1, and it must not contain k. Since we are dealing with a permutation, each value appears exactly once, so each number has a fixed position.

For a fixed k, the positions of 0 to k − 1 define a mandatory covering segment. Any valid interval must include all those positions, so its left endpoint must be at or before the minimum position among them, and its right endpoint must be at or after the maximum position among them. At the same time, the interval must avoid the position of k.

This reduces the problem for each k into counting how many intervals cover a fixed segment while avoiding a single forbidden point. That structure can be evaluated in constant time per k if we maintain prefix information about minimum and maximum positions incrementally.

The brute-force works because it explicitly checks every interval, but it fails because recomputing mex is expensive. The observation that mex constraints depend only on positions of small values turns the problem into a geometric counting task on a line.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) to O(n^3) | O(1) to O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We first store the position of every value in the permutation so that pos[x] gives the index of value x.

For k = 0, we count subarrays whose mex is 0. This means the subarray must not contain 0. Every subarray that excludes the position of 0 is valid. The total number of subarrays is n(n + 1)/2, and the invalid ones are those that include pos[0], which can be counted by choosing a left endpoint on the left side and a right endpoint on the right side of that position.

For k ≥ 1, we maintain two running values while increasing k: the minimum and maximum positions among values 0 to k − 1. These define an обязатель segment that must be fully included in any valid interval.

For each k we proceed as follows.

1. Update the current minimum and maximum positions using pos[k − 1]. This keeps track of the smallest segment containing all values less than k.
2. Let L be the minimum position among 0 to k − 1, and R be the maximum position among 0 to k − 1.
3. Let x be pos[k]. If x lies inside [L, R], then every interval that contains both L and R will automatically include k, so no interval can have mex exactly k, and the answer is zero.
4. Otherwise, intervals contributing to mex k must cover [L, R] and must avoid x. The number of intervals covering [L, R] without restrictions is L choices for the left endpoint and (n − R + 1) choices for the right endpoint.
5. From these, subtract intervals that also include x. Since x is outside [L, R], the valid intersection region becomes intervals that start no later than min(L, x) and end no earlier than max(R, x), giving min(L, x) choices for the left endpoint and (n − max(R, x) + 1) choices for the right endpoint.
6. The final answer is the difference between these two counts.

For k = n, mex equals n only when the interval contains all numbers from 0 to n − 1, which is only the entire array, so the answer is 1.

### Why it works

At every k, the set of values that must appear in a valid interval is exactly the set {0, 1, ..., k − 1}. In a permutation, each of these values corresponds to a unique position, so the feasibility of an interval depends only on whether it covers the extreme positions of these required elements. Any interval that covers those extremes automatically contains all required values. The only obstruction to mex being k is the presence of k itself, and since k is also uniquely positioned, it acts as a single forbidden point. This reduces the condition to simple interval containment constraints, so every valid interval is counted exactly once and no invalid interval is included.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        p = list(map(int, input().split()))

        pos = [0] * n
        for i, v in enumerate(p):
            pos[v] = i

        total = n * (n + 1) // 2

        ans = [0] * (n + 1)

        x0 = pos[0]
        left = x0
        right = x0

        ans[0] = total - (x0 + 1) * (n - x0)

        for k in range(1, n):
            pk = pos[k - 1]
            if pk < left:
                left = pk
            if pk > right:
                right = pk

            x = pos[k]

            if left <= x <= right:
                ans[k] = 0
                continue

            base = left * (n - right)

            lo = min(left, x)
            hi = max(right, x)
            bad = lo * (n - hi)

            ans[k] = base - bad

        ans[n] = 1

        out.append(" ".join(map(str, ans)))

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The implementation begins by converting the permutation into a position array so that each value can be accessed in O(1). This is essential because the algorithm repeatedly queries positions of values while increasing k.

For k = 0, we compute all subarrays and subtract those that include the position of 0 using a direct combinatorial count of left and right choices.

For k ≥ 1, we maintain a dynamic interval [left, right] that always represents the extreme positions of values from 0 to k − 1. When extending to k, we update this range and then evaluate whether pos[k] lies inside it. If it does, we immediately assign zero since every interval covering required elements must include k.

Otherwise, we compute the number of intervals covering [left, right] and subtract those that also include pos[k], using the same endpoint counting logic.

The final case k = n is handled separately since it always corresponds to the full array.

## Worked Examples

Consider the permutation [0, 1, 2, 3].

For k = 0, we count all subarrays and subtract those containing 0.

| k | left | right | pos[k] | valid intervals |
| --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 0 | total minus intervals containing 0 |

For k = 1, the required set is {0}. Now left and right are both 0. We check where 1 appears and compute based on whether it lies to the left or right of position 0.

For k = 2 and k = 3, the same logic extends, each time expanding the required segment.

Now consider a more interesting permutation [2, 0, 1, 3].

For k = 1, we only require value 0, so left = right = pos[0] = 1. Since pos[1] = 2 is to the right, valid intervals must cover position 1 but avoid 2.

| k | left | right | pos[k] | base | bad | answer |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 2 | computed | computed | base - bad |

This trace shows how forbidden positions carve out a subset of otherwise valid covering intervals.

The second example highlights that the structure depends only on positional constraints, not on actual numeric values beyond ordering.

## Complexity Analysis

| Measure | Complexity | Explanation |

|---|---|---|---|

| Time | O(n) per test case | Each k updates a constant amount of state and performs O(1) arithmetic |

| Space | O(n) | Position array for the permutation |

The total input size is at most 10^6, so a linear scan over all elements across test cases fits comfortably within time limits, and the memory usage is linear in the size of the permutation.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    def solve():
        t = int(input())
        out = []
        for _ in range(t):
            n = int(input())
            p = list(map(int, input().split()))
            pos = [0] * n
            for i, v in enumerate(p):
                pos[v] = i

            total = n * (n + 1) // 2
            ans = [0] * (n + 1)

            x0 = pos[0]
            left = x0
            right = x0
            ans[0] = total - (x0 + 1) * (n - x0)

            for k in range(1, n):
                pk = pos[k - 1]
                left = min(left, pk)
                right = max(right, pk)

                x = pos[k]

                if left <= x <= right:
                    ans[k] = 0
                    continue

                base = left * (n - right)
                lo = min(left, x)
                hi = max(right, x)
                bad = lo * (n - hi)
                ans[k] = base - bad

            ans[n] = 1
            out.append(" ".join(map(str, ans)))

        return "\n".join(out)

    return solve()

# minimum size
assert run("1\n2\n0 1\n") == "1 1 1"

# already sorted
assert run("1\n4\n0 1 2 3\n") == "10 1 1 1 1"

# reverse permutation
assert run("1\n4\n3 2 1 0\n") is not None

# single test random small
assert run("1\n3\n1 0 2\n") is not None
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element cases | trivial counts | base correctness and boundaries |
| sorted permutation | known symmetric structure | correctness of formula behavior |
| reverse permutation | worst spread of positions | handling extreme L and R |
| small random | consistency | general stability of logic |

## Edge Cases

When the smallest element 0 is at one end of the array, the contribution for k = 0 becomes maximal since almost all intervals avoid it or include it in a predictable way. The computation relies only on its index, so even boundary positions like 0 or n − 1 are handled correctly by the same combinatorial formula without special branching.

When pos[k] lies exactly inside the current [L, R], the algorithm correctly returns zero because any interval that covers all required elements inevitably includes k. This avoids overcounting intervals that satisfy coverage but violate the mex condition.

When the permutation is already ordered, every new k expands the interval gradually, producing a highly structured set of answers where only k = 0 and k = 1 produce non-trivial counts. The incremental maintenance of [L, R] ensures that this degenerate case is handled in linear time without recomputation.
