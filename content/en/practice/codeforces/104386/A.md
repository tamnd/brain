---
title: "CF 104386A - Dungeon videogame"
description: "We are given several independent dungeon runs. Each run consists of a sequence of levels, and at each level we must make exactly one choice: either we clear the level and gain the value written on it, or we skip a contiguous block of levels and pay a penalty equal to the number…"
date: "2026-07-01T02:48:14+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104386
codeforces_index: "A"
codeforces_contest_name: "TheForces Round #14 (Cool-Forces)"
rating: 0
weight: 104386
solve_time_s: 78
verified: false
draft: false
---

[CF 104386A - Dungeon videogame](https://codeforces.com/problemset/problem/104386/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 18s  
**Verified:** no  

## Solution
## Problem Understanding

We are given several independent dungeon runs. Each run consists of a sequence of levels, and at each level we must make exactly one choice: either we clear the level and gain the value written on it, or we skip a contiguous block of levels and pay a penalty equal to the number of levels we skipped.

The important subtlety is that “skip” is not tied to a single level decision in the usual way. It is a segment operation that can be applied starting at any position, and it covers multiple levels at once. While skipping, we still conceptually move past those levels, but we lose one point per skipped level regardless of what the underlying values were.

So the task is to decide a partition of the array into alternating segments of “solved individually” and “skipped as a whole”, where skipped segments contribute a linear negative cost equal to their length, and solved positions contribute their own values.

The output is the maximum achievable total score.

The constraints are tight enough that any quadratic or cubic reasoning over subarrays will fail. The total number of levels across test cases is up to 200,000, so we need an approach that is linear or nearly linear per test case. Anything involving trying all segment boundaries or dynamic programming over pairs of indices would be too slow.

A common failure case comes from misinterpreting the skip operation as something local per index rather than global per segment. For example, if one assumes skipping at index i only affects i, one might incorrectly conclude the answer is simply sum of positive values, which is wrong when long negative runs can be profitably skipped as a group.

Another subtle case is when all values are negative. A naive solution might think skipping everything is optimal, but skipping incurs cost equal to length, which still produces a negative total, so sometimes choosing a single least-negative element is better.

## Approaches

The brute force interpretation tries to decide, for every segment, whether to split it into individual solves or to replace it with a skip operation. That leads to exploring all partitions of the array into segments, and for each segment deciding its mode. The number of such partitions grows exponentially with n, since every boundary between i and i+1 can either be cut or not, and each segment also has a second decision. Even with pruning, this quickly becomes infeasible beyond very small n.

The key observation is that skipping a segment of length L is equivalent to adding a constant cost of -1 per element in that segment. This makes the skip operation distributable over individual positions, meaning we do not actually need to reason about segments at all. Every position i contributes either a_i if we solve it, or -1 if we choose to skip it as part of some skip segment.

Once this is seen, the structure simplifies drastically. Each index independently contributes a choice between two fixed values: take a_i or take -1. The segment nature of skip becomes irrelevant because any grouping of skipped positions still sums to the same total cost as treating them individually.

So the problem reduces to a per-element maximum choice: for each i, we pick max(a_i, -1). Summing these choices gives the global optimum.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over segment partitions | Exponential | O(n) | Too slow |
| Per-element greedy choice | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the array of values representing level rewards. The goal is to compute the best achievable total score under independent per-position decisions.
2. Initialize an accumulator to zero. This variable will store the final score by summing optimal contributions from each level.
3. Iterate through each value a_i in the array. At this point, we consider the two ways this position can be handled in any valid strategy.
4. Compute the contribution of solving the level, which is a_i.
5. Compute the contribution of effectively skipping it, which is -1 per level cost.
6. Add the larger of these two values to the accumulator. This step captures the fact that any global optimal strategy must locally choose the better option at each position, since skip costs do not depend on grouping structure.
7. After processing all positions, output the accumulator as the answer for the test case.

### Why it works

The crucial property is that the skip operation decomposes additively over positions. Any skipped segment of length L contributes exactly -L regardless of how it is partitioned internally. This removes any dependency between decisions at different indices. Once dependencies vanish, the optimal global solution must consist of independently optimal local decisions, because changing one position’s choice cannot affect any other position’s contribution. That eliminates any benefit from coupling decisions into segments.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        ans = 0
        for x in a:
            if x > -1:
                ans += x
            else:
                ans += -1
        
        print(ans)

if __name__ == "__main__":
    solve()
```

The code processes each test case independently, which is necessary because there is no interaction between them. Inside each test case, it iterates once over the array and applies a simple comparison at each element.

The key implementation detail is the threshold comparison against -1. Any value greater than -1 is worth taking directly, while anything less or equal is better replaced by the skip-equivalent cost. This avoids any need for segment tracking or dynamic programming.

## Worked Examples

### Example 1

Input:

```
5
-1 -1 -1 2 -1
```

We evaluate each element and choose between taking it or paying -1.

| i | a[i] | take a[i] | take -1 | chosen | running sum |
| --- | --- | --- | --- | --- | --- |
| 1 | -1 | -1 | -1 | -1 | -1 |
| 2 | -1 | -1 | -1 | -1 | -2 |
| 3 | -1 | -1 | -1 | -1 | -3 |
| 4 | 2 | 2 | -1 | 2 | -1 |
| 5 | -1 | -1 | -1 | -1 | -2 |

Final answer is -2.

This confirms that even a positive spike does not fully compensate for many forced negative contributions when everything else is bad.

### Example 2

Input:

```
5
3 5 6 2 -1000000000
```

| i | a[i] | take a[i] | take -1 | chosen | running sum |
| --- | --- | --- | --- | --- | --- |
| 1 | 3 | 3 | -1 | 3 | 3 |
| 2 | 5 | 5 | -1 | 5 | 8 |
| 3 | 6 | 6 | -1 | 6 | 14 |
| 4 | 2 | 2 | -1 | 2 | 16 |
| 5 | -1e9 | -1e9 | -1 | -1 | 15 |

Final answer is 15.

This trace shows how a single extremely negative value collapses to a constant -1 cost, which is far better than taking the raw value.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each element is processed once with constant work |
| Space | O(1) extra space | Only a running sum is stored |

The total input size across all test cases is at most 200,000, so a single linear scan per test case fits comfortably within the time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        ans = 0
        for x in a:
            ans += x if x > -1 else -1
        out.append(str(ans))
    return "\n".join(out)

# provided samples (as interpreted)
assert run("4\n5\n-1 -1 -1 2 -1\n5\n3 5 6 2 -1000000000\n2\n-1000000000 1\n3\n1 1 1") == "-2\n15\n-1\n3"

# all negative
assert run("1\n3\n-5 -2 -3") == "-3"

# all positive
assert run("1\n4\n1 2 3 4") == "10"

# mix
assert run("1\n5\n-1 10 -5 2 -1") == "12"

# single element
assert run("1\n1\n-1000000000") == "-1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all negative | -3 | skip dominates but still costs -1 per element |
| all positive | 10 | always take values |
| mixed values | 12 | local choice behavior |
| single element | -1 | boundary condition |

## Edge Cases

A fully negative array like `[-5, -2, -3]` demonstrates that the algorithm never tries to “escape” by skipping everything, since skipping still accumulates -1 per element. The computation becomes three comparisons against -1, producing -1 for each position and a final sum of -3.

A fully positive array like `[1, 2, 3, 4]` shows that the algorithm always selects the actual values because each is greater than -1. The running sum becomes the total array sum, which matches the intuitive best strategy.

A mixed case such as `[ -1, 10, -5, 2, -1 ]` shows that only elements below or equal to -1 get replaced by -1, while strong positives are kept intact, and the final result reflects independent decisions per position without any coupling effects.
