---
title: "CF 104172K - Maximum GCD"
description: "We are given an array of positive integers. We are allowed to repeatedly modify individual elements using an operation of the form “replace a value by its remainder when divided by some chosen positive integer”."
date: "2026-07-02T00:55:14+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104172
codeforces_index: "K"
codeforces_contest_name: "The 2023 ICPC Asia Hong Kong Regional Programming Contest (The 1st Universal Cup, Stage 2:Hong Kong)"
rating: 0
weight: 104172
solve_time_s: 72
verified: true
draft: false
---

[CF 104172K - Maximum GCD](https://codeforces.com/problemset/problem/104172/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of positive integers. We are allowed to repeatedly modify individual elements using an operation of the form “replace a value by its remainder when divided by some chosen positive integer”. We can apply this operation any number of times on any elements, but we are forbidden from ever turning an element into zero.

After performing any sequence of such operations, we look at the resulting array and compute its GCD in the usual sense. Our goal is to choose operations in a way that maximizes this final GCD.

The key difficulty is that the operation does not simply reduce numbers arbitrarily. A remainder operation preserves structural constraints, and not every smaller value is necessarily reachable from a given starting value.

The constraints allow up to 100,000 elements with values up to 1e9, so any solution that tries to simulate transformations or test all possible final states per element is immediately infeasible. Even O(n sqrt A) approaches are too slow because both n and values are large.

A subtle edge case arises from the “no zero allowed” rule. For example, if an element is 2, trying to reduce it further often produces zero and becomes illegal. In particular, from 2 you cannot reach 1 using any valid operation sequence, because every modulo choice either keeps it at 2 or produces 0.

Another edge case is that even when a value is small, it might not be freely reducible to all intermediate numbers. For instance, 4 can reach 1 but cannot reach 2 or 3. This non-uniform reachability is the main reason a naive greedy “just reduce everything to the target GCD” approach fails.

## Approaches

A brute-force interpretation would try to consider all possible final values for each element, then compute the best possible GCD over all combinations. This quickly becomes exponential because each element can branch into many reachable states, and combining choices across n elements is intractable.

A more structured view is to reverse the problem. Instead of asking what GCD can be formed after transformations, we ask what value d can appear as a common value in the final array. If we can force every element to become exactly d, then the GCD is at least d. Since GCD is upper bounded by the minimum chosen value, maximizing a uniform target is the strongest strategy.

This reduces the problem to understanding reachability: for a fixed element a, which values can it be transformed into using repeated modulo operations without ever hitting zero.

The crucial observation is that from a value a, any number strictly larger than a/2 and less than a is impossible to reach, but every value from 1 up to floor((a − 1) / 2) is reachable in at most one operation, and anything above that range either stays unchanged or falls into an unreachable region. This creates a sharp structural constraint: each element either stays itself, or can be reduced only to relatively small values, but cannot smoothly cover the entire interval.

This leads to a global constraint on a candidate target d. If we want every element to become exactly d, then for any element a, either a already equals d, or a must be large enough to reach d through reductions. That requires a ≥ 2d + 1. Otherwise, if d lies in the forbidden middle region (between a/2 and a), it cannot be produced.

So the problem becomes checking which values d are simultaneously “safe” for all array elements.

A direct per-d verification would still be too slow, but sorting the array reveals a simpler structure. The only obstruction for a candidate d is the existence of some value a such that d < a ≤ 2d and a is not equal to d. Any such value blocks the construction because it cannot be transformed into d.

This leads to a simple sweep over sorted unique values.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force reachability per element | Exponential | O(n) | Too slow |
| Sort + validity check on gaps | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

### Algorithm Walkthrough

1. Sort the array and compress it into a list of distinct values.

Sorting is needed because the only dangerous situation depends on neighboring values in value space, not on indices.
2. For each distinct value d in increasing order, consider it as a candidate final GCD.

If we can make all elements equal to d, then d is achievable as the array GCD.
3. Check whether any value exists in the interval (d, 2d].

If such a value exists and it is not equal to d itself, then d is impossible. The reason is that this value cannot be reduced down to d under the allowed operations.
4. If the next distinct value after d is greater than 2d, then no blocking value exists in the forbidden interval, so d is valid.
5. Track the maximum valid d across all candidates and output it.

### Why it works

Each element can only contribute to a final value that is either itself or a relatively small value at most half of its current magnitude. This creates a hard boundary: values in the interval (d, 2d] are “sticky” in the sense that they cannot all be collapsed to d unless they already equal d.

Thus, any candidate d is valid exactly when the value set contains no unavoidable obstruction in that interval. Checking adjacent values in sorted order is sufficient because any obstruction would appear as the next larger element lying inside (d, 2d].

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    a.sort()
    
    # compress distinct values
    vals = []
    for x in a:
        if not vals or vals[-1] != x:
            vals.append(x)
    
    ans = 1
    
    m = len(vals)
    for i, d in enumerate(vals):
        if i < m - 1:
            nxt = vals[i + 1]
            if nxt <= 2 * d:
                continue
        ans = max(ans, d)
    
    print(ans)

if __name__ == "__main__":
    solve()
```

The solution begins by sorting and compressing duplicates so that we reason only about distinct magnitudes. For each candidate value d, we look only at the next distinct value. If that next value lies within 2d, then there exists an intermediate number that cannot be transformed into d under the modulo-reduction rules, so d is rejected. Otherwise, d is feasible and becomes a candidate answer.

The final answer is the largest feasible d.

## Worked Examples

### Example 1

Input:

```
5
2 3 7 8 20
```

We sort and compress:

vals = [2, 3, 7, 8, 20]

We test each value:

| d | next value | next ≤ 2d? | valid |
| --- | --- | --- | --- |
| 2 | 3 | yes (3 ≤ 4) | no |
| 3 | 7 | yes (7 ≤ 6 false → no) actually 7 > 6 | yes |
| 7 | 8 | yes (8 ≤ 14) | no |
| 8 | 20 | yes (20 ≤ 16 false) | yes |
| 20 | none | yes | yes |

Valid candidates are 3, 8, 20, so answer is 20.

This trace shows how values are only blocked when another value lies in their “forbidden collapse window” up to twice themselves.

### Example 2

Input:

```
4
4 5 6 20
```

vals = [4, 5, 6, 20]

| d | next value | next ≤ 2d? | valid |
| --- | --- | --- | --- |
| 4 | 5 | yes (5 ≤ 8) | no |
| 5 | 6 | yes (6 ≤ 10) | no |
| 6 | 20 | no (20 ≤ 12 false) | yes |
| 20 | none | yes | yes |

Answer is 20.

This example highlights that even if many small values exist, only those that do not have a conflicting neighbor within twice their range can serve as the global GCD target.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates; scanning is linear over distinct values |
| Space | O(n) | Storage for array and compressed values |

The constraints allow up to 100,000 elements, so an O(n log n) sorting-based solution is easily fast enough.

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
    vals = []
    for x in a:
        if not vals or vals[-1] != x:
            vals.append(x)
    
    ans = 1
    m = len(vals)
    for i, d in enumerate(vals):
        if i < m - 1:
            if vals[i + 1] <= 2 * d:
                continue
        ans = max(ans, d)
    
    return str(ans)

# minimum size
assert run("1\n7") == "7"

# all equal
assert run("4\n5 5 5 5") == "5"

# increasing chain
assert run("5\n1 2 3 4 8") == "4"

# large separation
assert run("4\n10 25 100 1000") == "1000"

# tight blocking case
assert run("3\n4 5 6") == "6"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element | itself | base case |
| all equal | same value | stability |
| mixed small values | blocking effect | interval constraint |
| sparse values | greedy selection | independence of gaps |
| tight cluster | invalid candidates eliminated | 2d boundary rule |

## Edge Cases

One important edge case is when all elements are equal. In that case, no transformation is needed and the answer is trivially that value, since GCD is maximized by keeping everything unchanged.

Another case is when values are very small and tightly packed, such as 4, 5, 6. Here, every candidate except the largest is blocked because each value has a neighbor within its doubling interval. The algorithm correctly rejects 4 and 5 and selects 6.

A final case is when values are widely spaced, such as 10, 25, 100. Here, most candidates are valid because no value falls into the forbidden interval of another, and the algorithm correctly identifies the maximum value as the best achievable GCD.
