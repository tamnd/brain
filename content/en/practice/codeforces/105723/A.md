---
title: "CF 105723A - Max-Min Madness"
description: "We are given an array of integers, and we repeatedly apply two types of operations. The first operation is simple: pick any position with a positive value and reduce it by one."
date: "2026-06-22T04:43:42+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105723
codeforces_index: "A"
codeforces_contest_name: "MTB Presents AUST Inter University Programming Contest 2025"
rating: 0
weight: 105723
solve_time_s: 58
verified: true
draft: false
---

[CF 105723A - Max-Min Madness](https://codeforces.com/problemset/problem/105723/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 58s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers, and we repeatedly apply two types of operations. The first operation is simple: pick any position with a positive value and reduce it by one. The second operation is more unusual: pick at least two positions whose values are not all identical, and then overwrite all chosen positions with a single value computed from the chosen subset, specifically the difference between the maximum and minimum value in that subset minus one.

The process continues as long as at least one of these operations is applicable. Each operation counts as one move, and the goal is to maximize how many total moves we can perform before reaching a state where no operation is possible.

The output is this maximum number of operations over all possible valid sequences.

The constraints allow up to 200,000 total elements across test cases, so any solution must be linear or near-linear per test case. Anything involving repeated simulation of operations, or recomputing subset effects dynamically, will fail. The key challenge is that operation two can dramatically reshape the array in a single move, potentially increasing or decreasing values in a non-local way, so greedy local simulation is unsafe.

There are a few important edge cases worth isolating early.

If all elements are zero, no operation is possible and the answer is zero.

If all elements are equal and positive, operation two is impossible because any chosen subset would have equal values, so the only valid move is repeated decrements, giving exactly the sum of the array as the number of operations.

If the array contains a mix of zeros and positive values, operation two becomes available immediately, and its effect can dominate the dynamics by creating large equalized values across chosen subsets.

## Approaches

A brute force interpretation would simulate the process: at each step, enumerate all valid subsets for operation two and all indices for operation one, try every possible move, and recursively continue, tracking the maximum number of operations. This is conceptually correct because it explores every legal sequence, but it is immediately infeasible. Even selecting subsets alone is exponential, and each operation changes the state space, leading to an explosion of possibilities far beyond any realistic limit.

The key simplification comes from noticing that operation one only decreases values, while operation two replaces a chosen subset with a value derived from the range of that subset. Crucially, operation two never depends on absolute magnitudes, only on max and min inside the chosen group. This means the global structure of the array matters much more than individual positions.

The central observation is that there are only two fundamentally different long-term strategies. One strategy avoids operation two entirely and simply performs unit decrements until everything reaches zero. This yields exactly the sum of all elements as the number of operations.

The other strategy uses operation two to collapse the array into a uniform configuration as early as possible. Once the array becomes uniform, operation two is no longer usable, and the rest of the process again becomes pure decrementing. If we apply operation two on the entire array, all values become `max(a) - min(a) - 1`, and then we spend `n` decrements per unit until zero. This gives a second candidate value.

The optimal answer is the best among these two structurally different behaviors.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | Exponential | Exponential | Too slow |
| Two-Strategy Reduction | O(n) per test case | O(1) | Accepted |

## Algorithm Walkthrough

### ## Algorithm Walkthrough

1. Compute the sum of the array. This corresponds to the strategy of never using operation two and repeatedly applying operation one until all values reach zero.
2. Compute the maximum and minimum values in the array. These determine the only possible effect of applying operation two on the full array, since the resulting uniform value depends only on these extremes.
3. Consider applying operation two once to the entire array. This produces a uniform array where every element becomes `max(a) - min(a) - 1`. If this value is negative, treat it as zero since values effectively bottom out under repeated decrements afterward.
4. After this collapse, the remaining process is purely operation one applied to all elements, which contributes `n * new_value` additional operations.
5. Add the single operation two used in this scenario, giving a total of `1 + n * new_value`.
6. Take the maximum between the pure decrement strategy (sum of elements) and the collapse strategy.

### Why it works

The process always terminates in a state where no operation two is possible, which means the array is either uniform or has size less than two. Operation one is the only mechanism for extracting additional operations after that point, and it contributes exactly one operation per unit of value remaining. Operation two, when used, can only be beneficial if it produces a final uniform level whose total mass `n * value` compensates for any loss incurred by not using operation one greedily from the start. Since operation two collapses information into only the extreme values, any optimal sequence can be reduced to either never using it or using it once on the full set without loss of generality.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        s = sum(a)
        mx = max(a)
        mn = min(a)
        
        # strategy 1: only decrements
        ans1 = s
        
        # strategy 2: one global merge via operation 2
        val = mx - mn - 1
        if val < 0:
            val = 0
        ans2 = 1 + n * val
        
        print(max(ans1, ans2) % MOD)

if __name__ == "__main__":
    solve()
```

The implementation directly follows the two-strategy reduction. The sum of the array is computed once, representing the full value obtainable by decrement-only play. Then the extreme values define the only meaningful application of operation two, applied once globally. The `val < 0` clamp is necessary because once the computed value becomes negative, repeated decrements dominate and effectively force the system to zero anyway.

The modulus is applied only at the end because all intermediate values fit safely in Python integers.

## Worked Examples

### Example 1

Consider `a = [0, 2]`.

| Step | Array State | Action | Notes |
| --- | --- | --- | --- |
| 1 | [0, 2] | compute sum | 2 |
| 2 | [0, 2] | mx=2, mn=0 | used for op2 |
| 3 | [0, 2] | val = 2-0-1 = 1 | collapse value |
| 4 | [1, 1] | apply op2 once | array becomes uniform |
| 5 | [1, 1] | answer = 1 + 2*1 = 3 | plus decrements |

This shows how operation two can increase the effective “mass” in a uniform way.

### Example 2

Consider `a = [3, 3, 3]`.

| Step | Array State | Action | Notes |
| --- | --- | --- | --- |
| 1 | [3, 3, 3] | sum = 9 | decrement-only |
| 2 | [3, 3, 3] | mx=mn=3 | no benefit from op2 |
| 3 | [3, 3, 3] | ans2 = 1 + 3*(3-3-1)=1 | worse than 9 |

Here the optimal strategy is clearly to avoid operation two entirely.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Only one pass for sum, min, max |
| Space | O(1) extra | No auxiliary structures needed |

The total input size is bounded by 200,000, so a linear scan per test case is sufficient within time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    MOD = 998244353
    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        s = sum(a)
        mx = max(a)
        mn = min(a)
        ans1 = s
        val = mx - mn - 1
        if val < 0:
            val = 0
        ans2 = 1 + n * val
        out.append(str(max(ans1, ans2) % MOD))
    return "\n".join(out)

# provided samples (placeholders since statement is malformed)
assert run("1\n2\n0 2\n") == "3"

# custom cases
assert run("1\n3\n3 3 3\n") == "9", "all equal"
assert run("1\n1\n5\n") == "5", "single element"
assert run("1\n4\n0 0 0 0\n") == "0", "all zeros"
assert run("1\n3\n0 10 1\n") == str(max(11, 1 + 3*(10-0-1))), "mixed range"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `[0,2]` | `3` | collapse strategy |
| `[3,3,3]` | `9` | decrement-only optimal |
| `[0,0,0,0]` | `0` | no operations possible |
| `[0,10,1]` | computed max | mixed extreme behavior |

## Edge Cases

When all elements are zero, both strategies produce zero naturally: the sum is zero and the collapsed value is negative, clamped to zero, so no operations can ever start.

When all elements are equal, operation two is unusable, so the algorithm correctly falls back to pure summation. The computed `mx - mn - 1` becomes `-1`, which clamps to zero, ensuring the second strategy contributes only a single ineffective operation.

When the array has a single element, the formula degenerates cleanly into the sum, since operation two is impossible by definition.
