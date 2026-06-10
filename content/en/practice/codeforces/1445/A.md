---
title: "CF 1445A - Array Rearrangment"
description: "We are given two lists of numbers of equal length, and we are allowed to reorder only the second list. After rearranging, we pair elements by index and check whether every paired sum stays within a fixed upper bound."
date: "2026-06-11T04:01:04+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1445
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 680 (Div. 2, based on Moscow Team Olympiad)"
rating: 800
weight: 1445
solve_time_s: 95
verified: true
draft: false
---

[CF 1445A - Array Rearrangment](https://codeforces.com/problemset/problem/1445/A)

**Rating:** 800  
**Tags:** greedy, sortings  
**Solve time:** 1m 35s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two lists of numbers of equal length, and we are allowed to reorder only the second list. After rearranging, we pair elements by index and check whether every paired sum stays within a fixed upper bound.

A useful way to think about this is that each value in the first array represents a “cost already committed,” and each value in the second array represents a “complement budget” that we are free to assign to those costs. The goal is to assign these budgets so that no position exceeds the limit.

The constraints are small: each test case has at most 50 elements, and there are at most 100 test cases. This means even algorithms that are quadratic per test case are easily fast enough. Anything cubic or exponential would still be acceptable in theory but unnecessary.

A naive mistake that often appears here is trying to match elements arbitrarily or greedily without sorting both arrays. For example, pairing the largest element in the first array with a random element in the second array can fail even when a valid arrangement exists. Consider `a = [1, 4]`, `b = [2, 5]`, `x = 6`. If we pair greedily as `(4, 5)` first, we immediately break the constraint, even though rearranging `b` as `[5, 2]` makes both pairs valid.

Another subtle failure comes from assuming that if the largest element in `a` can be paired with some element in `b`, then the rest will automatically work. That ignores that using a small `b` too early might block feasibility later.

## Approaches

The brute-force idea is to try every permutation of `b` and check whether pairing works. This is correct because it explores all possible assignments, but it grows as `n!`. Even for `n = 50`, this is completely infeasible since the number of permutations is astronomically large.

The key insight is that we are solving an assignment problem with a monotonic constraint: smaller values in `a` are easier to satisfy, so they should be paired with larger flexibility in `b`, and larger values in `a` require smaller paired values from `b`.

This suggests sorting both arrays and pairing them in a structured way instead of trying all permutations. The correct strategy turns out to be pairing the smallest element in `a` with the largest possible valid element in `b` or equivalently, pairing smallest-to-largest in a consistent reversed manner. Sorting transforms the problem from combinatorial matching into a deterministic greedy check.

The reason this works is that if any valid assignment exists, there is one that preserves order: swapping two assignments that violate order never breaks feasibility and often improves slack distribution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) per test | O(n) | Too slow |
| Optimal (sorting + greedy pairing) | O(n log n) per test | O(n) | Accepted |

## Algorithm Walkthrough

We want to test whether there exists a pairing of elements from `b` such that every pair with `a` stays under `x`.

1. Sort array `a` in non-decreasing order and sort array `b` in non-decreasing order. Sorting is essential because it allows us to reason about structure instead of permutations.
2. Reverse array `b`. After reversing, the largest elements of `b` come first. This prepares us for a greedy pairing strategy where we control which “budget” is assigned to which “cost.”
3. For each index `i` from `0` to `n - 1`, check whether `a[i] + b[n - 1 - i] <= x`. This pairs the smallest element of `a` with the largest element of `b`, the second smallest with the second largest, and so on.

The reasoning behind this pairing is that large values in `b` are “expensive” in terms of wasted slack. Assigning them to small values in `a` prevents them from blocking feasibility for larger values in `a`.

If any pair violates the condition, we immediately conclude that no valid rearrangement exists.

### Why it works

After sorting both arrays, consider any valid assignment between them. If there exists a crossing assignment where a larger element in `a` is paired with a larger element in `b` while a smaller element in `a` is paired with a smaller element in `b`, swapping these two pairs does not worsen any constraint and often improves feasibility. Repeatedly applying such swaps transforms any valid solution into one that matches opposite ends of the sorted arrays. This establishes that checking the reverse pairing is sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        line = input().strip()
        while line == "":
            line = input().strip()
        n, x = map(int, line.split())
        
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))
        
        a.sort()
        b.sort(reverse=True)
        
        ok = True
        for i in range(n):
            if a[i] + b[i] > x:
                ok = False
                break
        
        print("Yes" if ok else "No")

if __name__ == "__main__":
    solve()
```

The solution starts by reading each test case carefully, including handling blank lines that separate cases. Sorting `a` in ascending order and `b` in descending order establishes the greedy structure.

The core loop checks the only pairing we need to verify. The moment a violation appears, we can stop early because no rearrangement of remaining elements can fix a failed constraint at a fixed index pairing.

A subtle implementation detail is reversing `b` rather than sorting both in the same direction and indexing from opposite ends. Both are equivalent, but reversing makes the pairing logic more explicit.

## Worked Examples

### Example 1

Input:

```
n = 3, x = 4
a = [1, 2, 3]
b = [1, 1, 2]
```

| Step | a[i] | b[i] | sum | valid |
| --- | --- | --- | --- | --- |
| 0 | 1 | 2 | 3 | yes |
| 1 | 2 | 1 | 3 | yes |
| 2 | 3 | 1 | 4 | yes |

All pairs satisfy the constraint, so the answer is Yes.

This demonstrates how the largest value in `b` is reserved for the smallest value in `a`, preserving feasibility for the harder constraints later.

### Example 2

Input:

```
n = 2, x = 6
a = [1, 4]
b = [2, 5]
```

After sorting and reversing `b`:

`a = [1, 4]`, `b = [5, 2]`

| Step | a[i] | b[i] | sum | valid |
| --- | --- | --- | --- | --- |
| 0 | 1 | 5 | 6 | yes |
| 1 | 4 | 2 | 6 | yes |

This shows that the correct solution is not about preserving original order but about matching extremes.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t · n log n) | sorting dominates each test case |
| Space | O(n) | storing arrays for each test |

Given that `n ≤ 50` and `t ≤ 100`, the total work is extremely small even with Python overhead. Sorting is effectively constant-time in practice at this scale.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdin.read()

# We redefine solver for testing
def solve_input(inp):
    import sys
    from io import StringIO
    sys.stdin = StringIO(inp)

    def solve():
        t = int(input())
        out = []
        for _ in range(t):
            line = input().strip()
            while line == "":
                line = input().strip()
            n, x = map(int, line.split())
            a = list(map(int, input().split()))
            b = list(map(int, input().split()))
            a.sort()
            b.sort(reverse=True)
            ok = all(a[i] + b[i] <= x for i in range(n))
            out.append("Yes" if ok else "No")
        return "\n".join(out)

    return solve()

# provided samples
assert solve_input("""4
3 4
1 2 3
1 1 2

2 6
1 4
2 5

4 4
1 2 3 4
1 2 3 4

1 5
5
5
""") == """Yes
Yes
No
No"""

# custom cases
assert solve_input("""1
1 10
5
4
""") == "Yes"

assert solve_input("""1
1 5
5
5
""") == "No"

assert solve_input("""1
3 10
3 3 3
3 3 3
""") == "Yes"

assert solve_input("""1
3 5
1 2 3
3 3 3
""") == "No"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single pair feasible | Yes | minimal case |
| single pair tight fail | No | boundary equality |
| identical arrays valid | Yes | symmetric case |
| impossible distribution | No | greedy detection |

## Edge Cases

A minimal edge case is when `n = 1`. The algorithm reduces to a single comparison, and sorting has no effect. The pairing directly checks whether the only possible sum fits within `x`.

A tight boundary case occurs when `a[i] + b[j]` equals exactly `x` for all pairs. The algorithm accepts this because it only rejects strict violations, and this confirms correctness under equality constraints.

A failure-prone scenario is when both arrays contain repeated large values. For example, `a = [4, 4, 4]`, `b = [3, 3, 3]`, `x = 6`. The greedy pairing checks `4 + 3 = 7`, immediately rejecting, which matches the impossibility of any rearrangement since all pairings are identical up to permutation.
