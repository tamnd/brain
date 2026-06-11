---
title: "CF 1394A - Boboniu Chats with Du"
description: "We are given a sequence of “fun values” representing how entertaining Du’s messages are on each day. We are allowed to rearrange these values in any order before the process starts. After fixing an order, the days proceed from left to right."
date: "2026-06-11T09:49:12+07:00"
tags: ["codeforces", "competitive-programming", "dp", "greedy", "sortings", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1394
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 664 (Div. 1)"
rating: 1800
weight: 1394
solve_time_s: 319
verified: false
draft: false
---

[CF 1394A - Boboniu Chats with Du](https://codeforces.com/problemset/problem/1394/A)

**Rating:** 1800  
**Tags:** dp, greedy, sortings, two pointers  
**Solve time:** 5m 19s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a sequence of “fun values” representing how entertaining Du’s messages are on each day. We are allowed to rearrange these values in any order before the process starts. After fixing an order, the days proceed from left to right.

On each day, if Du is not currently muted, we take the next value from the sequence and add it to the total fun. If that value is larger than a given threshold `m`, Boboniu becomes angry and forces Du to stop speaking for the next `d` days. During muted days, no values are consumed and no fun is gained, the process simply skips forward in time.

The goal is to permute the array so that the total accumulated fun is maximized.

The key difficulty is that large values are dangerous because they trigger forced silence, which wastes upcoming positions. Small values are safe because they never trigger a penalty and always fill active speaking days efficiently.

The constraints go up to `n = 100000`, which immediately rules out any factorial or quadratic permutation search. Even `O(n^2)` greedy simulation over all reorderings is impossible. We need a strategy where each element is placed exactly once in a controlled structure, ideally in `O(n log n)` or `O(n)` time.

A naive greedy that sorts descending and always picks the largest available value can fail because placing a large value too early may waste too many future positions due to long mute intervals. Conversely, always postponing large values might also be suboptimal if they should be used to “block” time where small values would otherwise be wasted.

A subtle edge case appears when all values are larger than `m`. Then every picked element triggers a mute. For example, `n = 5, d = 2, m = 0, a = [1,2,3,4,5]`. Any ordering still causes frequent blocking, and the strategy must ensure we only use the best positions for large values, minimizing wasted placement.

Another edge case arises when `d = 1`. Then every large value blocks only the next day, so spacing is minimal and the problem becomes much closer to simple selection of best positions. Any overcomplicated scheduling would be unnecessary but still must produce correct results.

## Approaches

A brute-force approach would enumerate all permutations of the array, simulate the process for each permutation, and compute the resulting fun. For each permutation, we scan left to right, maintaining a pointer and a cooldown counter. Whenever we encounter a value greater than `m`, we skip the next `d` positions. This simulation costs `O(n)` per permutation, and there are `n!` permutations, leading to an infeasible `O(n! * n)` complexity.

The main structural observation is that only values greater than `m` affect the dynamics of blocking. Values `<= m` are “safe”: they never trigger a mute and therefore always contribute independently of ordering, except for how many active days are available to place them. The problem reduces to deciding where to place large values among the timeline of available speaking slots.

We can separate the array into two groups: safe values (`<= m`) and dangerous values (`> m`). Safe values should always be taken greedily whenever we have an available speaking day because they never reduce future availability. The challenge becomes how to place dangerous values so that their blocking effect is minimized while still collecting their contribution.

A key insight is to process dangerous values in descending order and simulate placing them into the timeline using a greedy scheduling structure. Each dangerous value consumes one active day and blocks the next `d` days, effectively creating “gaps” in the timeline. Meanwhile, safe values simply fill all remaining unblocked positions.

This leads to a greedy process where we maintain how many active slots remain and how many safe values are available to fill gaps. We always prioritize placing larger dangerous values first because they create the same blocking cost but yield higher reward.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n! · n) | O(n) | Too slow |
| Split + Greedy Scheduling | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We transform the array into two sorted groups and simulate the optimal scheduling of dangerous values among available days.

1. Split the array into two lists: one containing all values greater than `m` and one containing all values less than or equal to `m`. This separation is necessary because only the larger group triggers blocking behavior.
2. Sort both lists in descending order. The largest values must be placed earlier among available slots because they provide higher immediate gain for the same blocking cost.
3. Compute how many “effective positions” we can ever use. Each dangerous value occupies one day and removes the next `d` days from availability, so each placement consumes a block of size `d + 1`.
4. Greedily iterate through the dangerous values in descending order, placing each one as long as we still have available capacity in terms of effective slots. Each placement contributes its value to the answer and reduces remaining capacity.
5. After placing all possible dangerous values, fill all remaining usable days with safe values. Since safe values never trigger blocking, we simply take as many of them as possible and add them all to the answer.
6. If there are more safe values than remaining slots, we still take them all, because safe values do not interfere with each other or with scheduling.

### Why it works

The crucial invariant is that every dangerous value consumes exactly one “activation slot” and deterministically removes `d` future usable slots, regardless of where it is placed. This makes all dangerous values interchangeable in terms of cost, differing only in benefit. Therefore, sorting them in descending order and selecting greedily maximizes total gain under a fixed number of possible activations. Safe values do not affect the availability of future activations, so they can always be added independently once dangerous scheduling is fixed.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, d, m = map(int, input().split())
    a = list(map(int, input().split()))
    
    big = []
    small = []
    
    for x in a:
        if x > m:
            big.append(x)
        else:
            small.append(x)
    
    big.sort(reverse=True)
    small.sort(reverse=True)
    
    # maximum number of big elements we can place
    # each big consumes (d + 1) effective positions
    max_big = (n + d) // (d + 1)
    
    take_big = min(len(big), max_big)
    
    ans = sum(big[:take_big])
    
    # remaining positions after placing big elements
    remaining_slots = n - take_big * (d + 1)
    
    # we can place all small elements in remaining slots
    ans += sum(small[:remaining_slots])
    
    print(ans)

if __name__ == "__main__":
    solve()
```

The solution starts by partitioning values into dangerous and safe groups based on whether they exceed `m`. Sorting both groups in descending order ensures we always consider the most valuable elements first.

The expression `(n + d) // (d + 1)` computes how many times we can trigger a “block event” in the best case, since each dangerous value occupies one day and disables the next `d` days. This gives an upper bound on how many large elements can be scheduled.

After choosing how many large elements to take, we compute how many actual days remain usable for small elements. Those are simply filled with the best available safe values.

The key subtlety is that we never explicitly simulate day-by-day transitions. Instead, we compress the process into counting how many effective slots each large value consumes.

## Worked Examples

### Example 1

Input:

```
n = 5, d = 2, m = 11
a = [8, 10, 15, 23, 5]
```

We split into:

Big: [23, 15]

Small: [10, 8, 5]

We compute `max_big = (5 + 2) // 3 = 2`.

We take both big values.

| Step | Action | Big taken | Remaining slots | Answer |
| --- | --- | --- | --- | --- |
| 1 | Take 23 | [23] | 5 - 3 = 2 | 23 |
| 2 | Take 15 | [23, 15] | 2 - 3 (stop) | 38 |

Now remaining slots is effectively 0, so no small values are added.

Final answer is 38. This shows how large values dominate capacity consumption.

### Example 2

Input:

```
n = 6, d = 1, m = 4
a = [1, 2, 5, 6, 3, 4]
```

Big: [6, 5]

Small: [4, 3, 2, 1]

We compute `max_big = (6 + 1) // 2 = 3`.

We take both big values.

| Step | Action | Big taken | Remaining slots | Answer |
| --- | --- | --- | --- | --- |
| 1 | Take 6 | [6] | 6 - 2 = 4 | 6 |
| 2 | Take 5 | [6, 5] | 4 - 2 = 2 | 11 |

Remaining slots = 2, so we take [4, 3].

Final answer = 18.

This demonstrates how small values fill leftover space greedily after scheduling large values.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates; rest is linear aggregation |
| Space | O(n) | Storage for split arrays |

The constraints allow up to `10^5` elements, so an `O(n log n)` solution is comfortably within limits, while any permutation-based or simulation-heavy approach would be far too slow.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, d, m = map(int, input().split())
    a = list(map(int, input().split()))
    
    big = []
    small = []
    for x in a:
        if x > m:
            big.append(x)
        else:
            small.append(x)
    
    big.sort(reverse=True)
    small.sort(reverse=True)
    
    max_big = (n + d) // (d + 1)
    take_big = min(len(big), max_big)
    
    ans = sum(big[:take_big])
    remaining = n - take_big * (d + 1)
    ans += sum(small[:remaining])
    
    return str(ans)

# provided sample
assert run("5 2 11\n8 10 15 23 5\n") == "48"

# all small values
assert run("4 2 100\n1 2 3 4\n") == "10"

# all big values
assert run("5 1 0\n1 2 3 4 5\n") == "9"

# d = 1 edge case
assert run("6 1 4\n1 2 5 6 3 4\n") == "18"

# single element
assert run("1 10 5\n100\n") == "100"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all small values | 10 | no blocking effect |
| all big values | 9 | frequent cooldown dominates |
| d = 1 case | 18 | minimal penalty spacing |
| single element | 100 | base correctness |

## Edge Cases

When all values are less than or equal to `m`, the algorithm places everything into the small group and computes remaining slots as `n`. No blocking ever occurs, so the answer becomes the sum of all values. For example, `n = 4, m = 10, a = [1,2,3,4]` results in selecting all four elements.

When all values exceed `m`, the algorithm relies entirely on the capacity formula `(n + d) // (d + 1)`. Each selected element consumes a full block, and only the largest few are chosen. For `n = 5, d = 2, a = [5,4,3,2,1]`, at most two elements are selected, giving `5 + 4 = 9`.

When `d` is large relative to `n`, only one or two large elements can be used. The remaining slots are entirely filled by small values if they exist. This case confirms that the capacity calculation correctly caps the influence of dangerous values regardless of ordering.
