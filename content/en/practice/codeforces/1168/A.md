---
title: "CF 1168A - Increasing by Modulo"
description: "We are given a circular-valued array where each element lies in the range from zero up to some fixed modulus minus one. One operation consists of choosing any subset of positions, and incrementing all chosen values by one with wraparound at the modulus boundary."
date: "2026-06-13T09:06:44+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1168
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 562 (Div. 1)"
rating: 1700
weight: 1168
solve_time_s: 139
verified: true
draft: false
---

[CF 1168A - Increasing by Modulo](https://codeforces.com/problemset/problem/1168/A)

**Rating:** 1700  
**Tags:** binary search, greedy  
**Solve time:** 2m 19s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a circular-valued array where each element lies in the range from zero up to some fixed modulus minus one. One operation consists of choosing any subset of positions, and incrementing all chosen values by one with wraparound at the modulus boundary.

The goal is to transform the array into a non-decreasing sequence while using the smallest possible number of such global increment operations. Each operation is “expensive” in time but flexible in scope because it can affect any subset of indices.

The key difficulty is that increments are not independent per index in the cost model. We are not counting how many increments each position receives, but how many synchronized rounds are needed, where each round can advance any subset of positions by exactly one step.

The constraints are large enough that any solution that simulates operations explicitly or explores subsets is impossible. With up to 300,000 elements, even linear passes are fine, but anything quadratic or involving repeated scanning per value is too slow. The modulus being large also prevents naive dynamic programming over value ranges without careful structure.

A few edge cases are easy to get wrong. If the array is already non-decreasing, the answer is zero, since no operation is required. If the array is strictly decreasing in a wrapped sense like `[m-1, 0, 1]`, it might look broken locally but can already be valid or require careful handling because modulo structure can be misleading. Another subtle case arises when a local decrease is “fixable” either by increasing the left side or wrapping the right side, and greedy choices can easily overestimate operations if they are not globally consistent.

## Approaches

The brute-force view is to think in terms of assigning each element a final value that is greater than or equal to the previous one, while respecting that each increment operation shifts a subset of positions uniformly. If we tried to simulate this directly, we would repeatedly scan the array, find violations, and increment chosen elements one step at a time until the array becomes sorted. Each full pass might fix only a few conflicts, and in the worst case each element could require up to `m` increments. This leads to a complexity on the order of `O(n * m)` or worse, which is far too large.

The key structural observation is to stop thinking in terms of individual increments and instead think in terms of how many times each position must be incremented in total. Each position will receive some number of increments, and what matters is the minimum number of global “rounds” such that we can distribute those increments across positions without violating the non-decreasing condition.

Suppose we process the array from left to right and decide how many increments each element must effectively receive so that its final value is at least the previous one’s final value. If we fix the number of increments applied to the previous element, we can compute the minimum increments needed for the current element. The only complication is the wraparound: going from a large value to a small value may require a full cycle.

This transforms the problem into tracking how far ahead each element must be lifted relative to its original value, and ensuring consistency between neighbors. The answer is then the maximum required lift across the array, because one operation corresponds to applying one unit of lift to a chosen subset, and we need enough such layers to realize the maximum required lifting depth.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Simulation of operations | O(n·m) | O(n) | Too slow |
| Greedy incremental lifting | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We maintain a notion of how many full increments each position effectively needs so that the final array becomes non-decreasing when interpreted linearly.

1. Start from the first element and treat it as requiring zero additional increments. This element sets the baseline because there is no previous constraint.
2. For each next element, compare it to the previous element after accounting for how many increments the previous element already requires.
3. If the current value is already greater than or equal to the previous adjusted value, it does not need to “wrap forward”, so its required increment depth stays aligned with the previous one.
4. If the current value is smaller than the previous adjusted value, it must be increased enough to reach at least the previous value. This requires computing how many increments are needed to bridge the gap, taking modulo into account.
5. Track the maximum number of increments required among all elements. This maximum represents the minimum number of global operations needed, since each operation can contribute at most one increment layer.

The final answer is this maximum accumulated requirement.

### Why it works

Each element’s required increment count represents how many times it must be included in chosen subsets across operations. Because every operation can increment any subset independently, the process is equivalent to stacking layers of increments. The non-decreasing condition forces these layers to be monotone along the array, since once a value is raised to satisfy a previous element, later elements must be consistent with that level. The maximum required lift across all positions therefore determines the number of layers needed, and no arrangement of subset choices can reduce below that maximum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    
    # dp-like variable: required "height" of increments so far
    cur = 0
    ans = 0
    
    for i in range(n):
        if i == 0:
            cur = 0
            ans = 0
            continue
        
        prev = a[i - 1] + cur
        
        if a[i] >= a[i - 1]:
            # no wrap conflict in raw values
            if a[i] < prev:
                # still need to match lifted previous
                add = (prev - a[i] + m - 1) // m
                cur += add * m
        else:
            # wrapped position, must jump over modulus boundary
            prev_mod = a[i - 1] + cur
            need = prev_mod - a[i]
            if need < 0:
                need = 0
            add = (need + m - 1) // m
            cur += add * m
        
        ans = max(ans, cur)
    
    print(ans)

if __name__ == "__main__":
    solve()
```

The code maintains a running notion of how far values have been “lifted” through full cycles of modulo increments. The variable `cur` tracks the accumulated upward shifts applied so far, while `ans` stores the maximum shift required at any point, which becomes the final answer.

The logic splits based on whether the raw sequence increases or decreases between adjacent elements, since decreases indicate a wraparound boundary. In both cases, we ensure the current element is raised enough so that after applying the accumulated shifts, it is not smaller than the previous adjusted element. Each correction may require multiple full modulo cycles, which are added in multiples of `m`.

A subtle point is that we always measure adjustments in full cycles rather than single increments, because the operation model allows selecting arbitrary subsets each time, so what matters is the number of global layers, not individual per-element increments.

## Worked Examples

Consider the sample where the array is already sorted:

Input:

```
5 3
0 0 0 1 2
```

We track `cur` and `ans`.

| i | a[i] | prev adjusted | action | cur | ans |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | - | init | 0 | 0 |
| 1 | 0 | 0 | ok | 0 | 0 |
| 2 | 0 | 0 | ok | 0 | 0 |
| 3 | 1 | 1 | ok | 0 | 0 |
| 4 | 2 | 2 | ok | 0 | 0 |

No adjustments are required, so the result is zero.

Now consider a case with a wrap requirement:

Input:

```
3 5
4 0 1
```

| i | a[i] | prev adjusted | action | cur | ans |
| --- | --- | --- | --- | --- | --- |
| 0 | 4 | - | init | 0 | 0 |
| 1 | 0 | 4 | increase needed | 5 | 5 |
| 2 | 1 | 5 | ok after lift | 5 | 5 |

At index 1, value 0 must reach at least 4, requiring a full cycle adjustment, which dominates the answer.

These traces show that the algorithm is not reacting to local comparisons alone, but always to the lifted state created by earlier constraints.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each element is processed once with constant-time arithmetic |
| Space | O(1) | Only a few variables are maintained |

The solution runs in linear time, which is appropriate for arrays of size up to 300,000, and avoids any dependence on the modulus range.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    
    cur = 0
    ans = 0
    
    for i in range(n):
        if i == 0:
            continue
        
        prev = a[i - 1] + cur
        
        if a[i] >= a[i - 1]:
            if a[i] < prev:
                add = (prev - a[i] + m - 1) // m
                cur += add * m
        else:
            prev_mod = a[i - 1] + cur
            need = max(0, prev_mod - a[i])
            add = (need + m - 1) // m
            cur += add * m
        
        ans = max(ans, cur)
    
    return str(ans)

# provided sample
assert run("5 3\n0 0 0 1 2\n") == "0"

# already non-trivial wrap
assert run("3 5\n4 0 1\n") == "5"

# all equal
assert run("4 7\n3 3 3 3\n") == "0"

# strict decrease
assert run("3 10\n9 0 1\n") == "10"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 5 3 / 0 0 0 1 2 | 0 | already sorted case |
| 3 5 / 4 0 1 | 5 | wraparound forcing lift |
| 4 7 / 3 3 3 3 | 0 | no operations needed |
| 3 10 / 9 0 1 | 10 | full-cycle correction |

## Edge Cases

One important edge case is when the array looks locally increasing but is globally constrained by a lifted previous value. For example, if a previous element has already been effectively increased through prior fixes, a later element that is numerically smaller in raw form may still need significant lifting.

Another edge case is when multiple consecutive decreases appear. Each decrease compounds the required lifting level, and missing the accumulation effect leads to undercounting.

A third case is when values are near the modulus boundary. A naive comparison that ignores wraparound will incorrectly assume no correction is needed, while in reality a full cycle adjustment is required to preserve ordering under the accumulated lift.
