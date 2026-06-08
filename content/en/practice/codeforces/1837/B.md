---
title: "CF 1837B - Comparison String"
description: "We are given a string that encodes local comparisons between neighboring elements of an array. Each character describes whether the next element must be larger or smaller than the current one."
date: "2026-06-09T06:38:41+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1837
codeforces_index: "B"
codeforces_contest_name: "Educational Codeforces Round 149 (Rated for Div. 2)"
rating: 900
weight: 1837
solve_time_s: 81
verified: false
draft: false
---

[CF 1837B - Comparison String](https://codeforces.com/problemset/problem/1837/B)

**Rating:** 900  
**Tags:** greedy  
**Solve time:** 1m 21s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a string that encodes local comparisons between neighboring elements of an array. Each character describes whether the next element must be larger or smaller than the current one. The task is not to construct any valid array, but to construct one that uses as few distinct values as possible while still respecting all these comparisons.

A useful way to think about the problem is that we are trying to assign heights to positions along a line, where each step either forces us to go up or down. We are allowed to reuse values, but only when doing so does not break strict inequality requirements.

The output is the smallest number of distinct integers needed to realize such a “walk” that follows the given sequence of ups and downs.

The constraints are small enough that an O(n²) idea per test case would already pass comfortably, since n is at most 100 and t is at most 500. This strongly suggests that we are not expected to optimize asymptotically beyond a linear or quadratic scan. The real challenge is understanding what structure determines the minimum number of distinct values.

A naive attempt might try to explicitly construct arrays or assign values greedily left to right while reusing numbers whenever possible. This quickly becomes fragile because local reuse decisions can block future reuse in ways that are hard to predict.

A second naive idea is to try all possible assignments with backtracking over a small range of integers. Even with only 100 positions, the branching factor is effectively unbounded, and the constraints on inequalities mean we would be exploring a large combinatorial space of labelings.

A subtler failure case appears when the string alternates, such as “<><><><”. A greedy approach might try to reuse two values repeatedly, but it turns out this forces an oscillation that requires introducing more distinct values than expected if you assign poorly. The correct answer depends on the global structure, not local decisions.

## Approaches

The key observation is that the problem is not really about absolute values, but about the relative ordering constraints. We only care about whether consecutive elements go up or down, which means the actual numbers can be thought of as labels assigned to a path that moves up and down.

The minimum number of distinct values corresponds to the minimum number of “levels” needed to realize the entire sequence consistently. Each time we go up, we need to ensure we can move to a higher unused level if necessary, and each time we go down, we mirror that constraint in the opposite direction.

The important structural insight is that any valid assignment can be shifted and compressed so that values correspond to heights in a walk. The cost is then the number of distinct heights visited. This reduces the problem to analyzing the extremal range of a prefix sum-like construction.

If we interpret “<” as +1 and “>” as -1, and track a running balance, the maximum spread between the highest and lowest value of this running sum determines how many distinct values are required. Intuitively, if the walk ever goes k steps below its starting point and also k steps above in some shifted form, we need k+1 distinct levels to accommodate it.

A more precise way to see this is to consider that each position corresponds to a point on an integer line determined by cumulative movement. The minimal number of distinct values is the number of distinct heights in the optimal compressed representation, which is exactly the range of reachable prefix extrema.

The brute force idea of assigning values explicitly fails because it does not capture that only the relative rank matters. Once we switch to tracking prefix extremas, the solution becomes linear per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force construction | O(2^n) or worse | O(n) | Too slow |
| Optimal prefix extremum tracking | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Convert the comparison string into a sequence of directional steps, treating each character as a movement constraint that will influence a running position.
2. Initialize a running counter at zero, which represents the current “height” in a hypothetical construction.
3. Traverse the string from left to right. When encountering a “<”, increase the counter by 1. When encountering a “>”, decrease the counter by 1. This simulates one valid compressed representation of the array.

The reason this works is that we are not assigning actual values yet, but constructing a relative ordering structure that respects every constraint.
4. While updating the running counter, keep track of both the minimum value reached and the maximum value reached during the traversal.
5. The answer is the size of the range covered by this walk, computed as `max_value - min_value + 1`.

This range represents how many distinct integer labels are required if we compress the construction optimally so that each height corresponds to a unique value.

### Why it works

Any valid array induces a sequence of relative comparisons that can be mapped to a walk on integers by repeatedly assigning adjacent differences consistent with the signs. Compressing that walk by shifting it so the minimum value becomes zero does not change validity but minimizes the number of distinct values. The number of distinct values is exactly the number of integer levels visited, which equals the range between the minimum and maximum prefix displacement. No alternative assignment can reduce this range, because any attempt to reuse values would force a violation of strict ordering in at least one segment of the string.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        s = input().strip()

        cur = 0
        mn = 0
        mx = 0

        for ch in s:
            if ch == '<':
                cur += 1
            else:
                cur -= 1
            mn = min(mn, cur)
            mx = max(mx, cur)

        print(mx - mn + 1)

if __name__ == "__main__":
    solve()
```

The code maintains a single running position and updates it according to each comparison. The minimum and maximum values observed during this traversal define the span of the induced structure. The final answer is computed as the size of this span. The implementation is careful to initialize the counters at zero, since the array starts before any comparisons are applied.

## Worked Examples

### Example 1: `<<>>`

We track the running value and its extrema.

| Step | Char | Current | Min | Max |
| --- | --- | --- | --- | --- |
| 0 | start | 0 | 0 | 0 |
| 1 | < | 1 | 0 | 1 |
| 2 | < | 2 | 0 | 2 |
| 3 | > | 1 | 0 | 2 |
| 4 | > | 0 | 0 | 2 |

Final range is 2 - 0 + 1 = 3.

This trace shows that even though we return to zero at the end, the intermediate peak of 2 forces three distinct levels in any valid construction.

### Example 2: `>>>>`

| Step | Char | Current | Min | Max |
| --- | --- | --- | --- | --- |
| 0 | start | 0 | 0 | 0 |
| 1 | > | -1 | -1 | 0 |
| 2 | > | -2 | -2 | 0 |
| 3 | > | -3 | -3 | 0 |
| 4 | > | -4 | -4 | 0 |

Final range is 0 - (-4) + 1 = 5.

This case shows that a monotone decreasing sequence forces a linear increase in required distinct values, since each step pushes the construction into a new minimum.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each character is processed once while updating running bounds |
| Space | O(1) | Only a few counters are maintained |

The total work across all test cases remains small even at maximum input size because the algorithm performs a single linear scan per case.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(sys.stdin.readline())
    out = []
    for _ in range(t):
        n = int(sys.stdin.readline())
        s = sys.stdin.readline().strip()

        cur = 0
        mn = 0
        mx = 0
        for ch in s:
            if ch == '<':
                cur += 1
            else:
                cur -= 1
            mn = min(mn, cur)
            mx = max(mx, cur)

        out.append(str(mx - mn + 1))

    return "\n".join(out)

# provided samples
assert run("""4
4
<<>>
4
>><<
5
>>>>>
7
<><><><
""") == """3
3
6
2"""

# custom cases
assert run("""1
1
<
""") == "2", "minimum size increasing"

assert run("""1
1
>
""") == "2", "minimum size decreasing"

assert run("""1
6
<><><>
""") == "2", "alternating small range"

assert run("""1
6
<<<<<<
""") == "7", "strict increase chain"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `<` | 2 | minimal increasing case |
| `>` | 2 | minimal decreasing case |
| `<><><>` | 2 | alternating pattern reuse |
| `<<<<<<` | 7 | linear growth of range |

## Edge Cases

A single-character string exposes whether the algorithm correctly handles base initialization. For “<”, the running value becomes 1, so the range is [0,1], giving answer 2. For “>”, the running value becomes -1, so the range is [-1,0], again giving 2. The algorithm naturally handles both without special casing because extrema are initialized at zero.

A fully decreasing string like “>>>>>>” continuously pushes the running value downward. The minimum keeps decreasing while the maximum stays at zero, so the range grows linearly. Each step introduces a new minimum, and the final answer reflects the total depth reached.

An alternating string such as “<><><><” keeps the running value oscillating between two adjacent levels. The minimum and maximum stabilize quickly at 0 and 1, so the result remains 2. This confirms that oscillation does not increase required distinct values beyond two because the walk never expands its range.
