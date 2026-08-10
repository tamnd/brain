---
title: "CF 102412G - AtCoder Quality Problem"
description: "We have a set (S) with (n) elements, and every subset of (S) must be painted either red or blue. For a subset (T), painting it red costs (RT), while painting it blue costs (BT). The costs may be negative, so the goal is not simply to choose the cheaper color independently."
date: "2026-08-10T14:08:43+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102412
codeforces_index: "G"
codeforces_contest_name: "MEX Foundation Contest (supported by AIM Tech)"
rating: 0
weight: 102412
solve_time_s: 245
verified: true
draft: false
---

[CF 102412G - AtCoder Quality Problem](https://codeforces.com/problemset/problem/102412/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 4m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a set (S) with (n) elements, and every subset of (S) must be painted either red or blue. For a subset (T), painting it red costs (R_T), while painting it blue costs (B_T). The costs may be negative, so the goal is not simply to choose the cheaper color independently.

The coloring has one structural restriction. Whenever two subsets (A) and (B) have the same color, their union (A\cup B) must have that same color as well. In other words, the subsets of each color must be closed under taking unions.

The input represents subsets by bitmasks. Mask (i) represents the subset containing exactly those elements whose corresponding bits are set. The two arrays therefore contain (2^n) costs each. We need the minimum possible sum of the chosen painting costs over all (2^n) subsets.

The bound (n\le20) is the main signal. There are at most (2^{20}=1,048,576) subsets, so an (O(2^n)) or (O(n2^n)) solution is realistic. With a two-second limit, anything such as (O(3^n)) is already too large at (n=20), since (3^{20}=3,486,784,401). The memory limit of (256) MiB also means we should keep only a few arrays of size (2^n), rather than storing a large DP table indexed by several subsets. The official constraints and limits are (n\le20), costs between (-10^9) and (10^9), two seconds, and (256) MiB.

There are several edge cases that are easy to mishandle. First, (n=0) leaves only the empty subset. For example,

```
0
-129363358
227605714
```

has answer `-129363358`, because there is exactly one subset and we simply choose its cheaper color. This sample is included in the original statement.

Negative costs are another source of mistakes. A solution that assumes the costs are nonnegative may try to interpret the problem as a normal minimum-cost coloring, but a negative cost can make a seemingly expensive color globally preferable because the union restriction couples many subsets.

Finally, the empty subset must be treated as an ordinary subset. For (n=1), there are exactly two subsets, the empty set and the singleton. The empty set has no special exemption from the coloring rule. Forgetting to include its cost in the base case produces an answer that is off by exactly one subset cost.

## Approaches

A direct way to think about the problem is to determine a valid coloring for every subset. That means considering (2^{2^n}) possible colorings and checking the union condition. This is already hopeless for very small (n), so we need to exploit the special structure of union closure.

A more useful brute-force dynamic programming approach looks at a fixed set (S). Suppose (S) is red. Among all blue subsets of (S), take their union and call it (V). Because blue subsets are closed under union, (V) is itself blue and is the unique largest blue subset. Every subset that is not contained in (V) must then be red, because otherwise it would be another blue subset whose union with (V) would be larger than (V).

This gives a DP that enumerates (V\subseteq S). For each (S), we could try every possible (V), solve the coloring problem inside (V), and pay for all subsets outside (V) in red. Doing this over every pair (V\subseteq S) takes (O(3^n)) time. At (n=20), that is about (3.49) billion subset relationships, far beyond the limit. The same reasoning applies if (S) is blue. This structural DP is correct, but it examines far too many possibilities. The (O(3^n)) viewpoint is also a useful way to discover the faster recurrence.

The key observation is that we do not actually need to identify the largest opposite-colored subset. Suppose (S) is red. There must exist some element (e\in S) such that every subset (T) satisfying (e\in T\subseteq S) is red. To see why, assume the opposite. Then for every element (e), there is some blue subset containing (e). Taking the union of all those blue subsets gives (S). Since the blue subsets are union-closed, (S) itself would have to be blue, contradicting that (S) is red.

Once such an element (e) is chosen, all subsets containing (e) have their color forced to red. The remaining subsets are exactly the subsets of (S\setminus{e}), and they can be colored optimally as an independent smaller instance. This turns the structural observation into a recurrence over masks.

Let (R(S)) denote the sum of red costs of every subset of (S), and define (B(S)) similarly. If we remove (e) from (S), then (R(S)-R(S\setminus{e})) is precisely the total red cost of all subsets of (S) that contain (e). The same holds for blue.

If (dp[S]) denotes the minimum cost for coloring all subsets of (S), without fixing the color of (S), then

\min_{e\in S}
\left(
dp[S\setminus{e}]
+
\min\left(
R(S)-R(S\setminus{e}),
B(S)-B(S\setminus{e})
\right)
\right).
]

The first term recursively colors all subsets not containing (e). The second term chooses whether all subsets containing (e) are red or all are blue.

We only need to compute (R(S)) and (B(S)), which is a standard subset-sum, or SOS DP, in (O(n2^n)). The final recurrence also considers each set element once, so the total remains (O(n2^n)). This is the optimal approach used by accepted solutions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over valid structural choices | (O(3^n)) | (O(2^n)) | Too slow |
| Optimal SOS DP + mask DP | (O(n2^n)) | (O(2^n)) | Accepted |

## Algorithm Walkthrough

1. Read the two cost arrays. Mask (s) represents a subset of the original set, so there are (2^n) masks.
2. Transform the red array into (R[s]), the sum of red costs over every submask of (s). Perform the same transformation on the blue array to obtain (B[s]). This is the standard SOS DP, and after it finishes, the difference (R[s]-R[t]) for (t=s\setminus{e}) is exactly the total red cost of subsets of (s) containing (e).
3. Set (dp[0]=\min(R[0],B[0])). The empty set has no elements to remove, so it is the base case. Since it is the only subset when (n=0), this also immediately handles the smallest possible instance.
4. Process every nonempty mask (s) in increasing numerical order. For every set bit (e) of (s), let (t=s\setminus{e}). Because (t<s), its DP value has already been computed.
5. Assume the selected element is (e). Every subset of (s) containing (e) must receive one common color. If that color is red, their total contribution is (R[s]-R[t]). If it is blue, their contribution is (B[s]-B[t]). The smaller of these two values is the best choice for this particular (e).
6. Update

\min\left(
dp[s],
dp[t]+\min(R[s]-R[t],B[s]-B[t])
\right).
]

1. After all masks have been processed, output (dp[2^n-1]), because this mask represents the complete set (S), so all subsets of the original set have been considered.

### Why it works

The invariant is that (dp[S]) is the minimum cost of a valid coloring of every subset of (S). Consider any optimal coloring of a nonempty (S), and suppose (S) is red. The union-closure condition guarantees that some element (e\in S) has the property that every subset containing (e) is red. Removing (e) leaves exactly the subsets of (S\setminus{e}), whose optimal cost is (dp[S\setminus{e}]). All remaining subsets containing (e) are forced to red and contribute (R[S]-R[S\setminus{e}]). The same argument applies when (S) is blue. Thus every optimal coloring is represented by one of our transitions, while every transition produces a valid coloring. Taking the minimum gives exactly (dp[S]).

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve(data=None):
    if data is None:
        n = int(input())
        m = 1 << n
        red = list(map(int, input().split()))
        blue = list(map(int, input().split()))
    else:
        it = iter(map(int, data.split()))
        n = next(it)
        m = 1 << n
        red = [next(it) for _ in range(m)]
        blue = [next(it) for _ in range(m)]

    # SOS DP:
    # red[s] = sum(red[t]) for all t subset of s.
    # blue[s] = sum(blue[t]) for all t subset of s.
    step = 1
    while step < m:
        block = step << 1
        for base in range(0, m, block):
            end = base + step
            for s in range(base, end):
                red[s + step] += red[s]
                blue[s + step] += blue[s]
        step <<= 1

    INF = 10**30
    dp = [INF] * m
    dp[0] = min(red[0], blue[0])

    for s in range(1, m):
        best = INF
        x = s
        while x:
            bit = x & -x
            t = s ^ bit

            add = red[s] - red[t]
            other = blue[s] - blue[t]
            if other < add:
                add = other

            cand = dp[t] + add
            if cand < best:
                best = cand

            x ^= bit

        dp[s] = best

    return str(dp[m - 1])

if __name__ == "__main__":
    print(solve())
```

The first part stores the two original cost arrays. The SOS transform then changes their meaning from “cost of exactly this subset” to “total cost of all submasks”. The in-place transform is safe because each bit is processed once, and when a bit is added to a mask, the value without that bit has already been finalized for the current stage.

The base case uses `min(red[0], blue[0])`, because after the SOS transform both `red[0]` and `blue[0]` still represent the costs of the empty subset alone.

For each mask, `x & -x` extracts one set bit. Removing that bit gives `t = s ^ bit`. Iterating over the set bits rather than all (n) positions avoids unnecessary checks and visits exactly (\operatorname{popcount}(s)) transitions.

The expression `red[s] - red[t]` is the sum of red costs for exactly those submasks of `s` that contain the removed element. The corresponding blue expression has the same interpretation. Since Python integers have arbitrary precision, the possible total costs, which can reach roughly (2^{20}\cdot10^9), require no special overflow handling.

The numerical order of masks is also sufficient for the DP ordering. Removing a set bit always produces a smaller mask, so `dp[t]` is available before `dp[s]` is evaluated.

## Worked Examples

### Sample 1

The input is

```
2
-5 9 9 -5
10 -8 -6 3
```

After the SOS transformation, the cumulative costs are

| Mask (s) | (R[s]) | (B[s]) |
| --- | --- | --- |
| 0 | -5 | 10 |
| 1 | 4 | 2 |
| 2 | 4 | 4 |
| 3 | 8 | -1 |

The DP proceeds as follows.

| Mask | Removed bit | Previous mask | Added cost | Candidate | (dp) |
| --- | --- | --- | --- | --- | --- |
| 0 |  |  |  |  | -5 |
| 1 | 1 | 0 | (\min(9,-8)=-8) | -13 | -13 |
| 2 | 2 | 0 | (\min(9,-6)=-6) | -11 | -11 |
| 3 | 1 | 2 | (\min(4,-5)=-5) | -16 | -16 |
| 3 | 2 | 1 | (\min(4,-3)=-3) | -16 | -16 |

The final answer is `-16`, matching the sample.

The interesting part is mask `3`. There are two possible choices for the special element. Both lead to the same optimum here, but the recurrence only needs the better transition.

### Sample 2

The input is

```
3
-15 19 19 -5 30 -3 -16 13
29 -6 -14 -7 24 -5 18 11
```

After SOS DP we get

| Mask | (R[mask]) | (B[mask]) |
| --- | --- | --- |
| 0 | -15 | 29 |
| 1 | 4 | 23 |
| 2 | 4 | 15 |
| 3 | 18 | 2 |
| 4 | 15 | 53 |
| 5 | 31 | 42 |
| 6 | 18 | 57 |
| 7 | 42 | 50 |

Now the important DP states are

| Mask | Removed bit | Previous mask | Added cost | Candidate | (dp) |
| --- | --- | --- | --- | --- | --- |
| 0 |  |  |  |  | -15 |
| 1 | 1 | 0 | -6 | -21 | -21 |
| 2 | 2 | 0 | -14 | -29 | -29 |
| 3 | 1 | 2 | -13 | -42 | -42 |
| 3 | 2 | 1 | -21 | -42 | -42 |
| 4 | 4 | 0 | 24 | 9 | 9 |
| 5 | 1 | 4 | -11 | -2 | -2 |
| 5 | 4 | 1 | 19 | -2 | -2 |
| 6 | 2 | 4 | 4 | 13 | -15 |
| 6 | 4 | 2 | 28 | -1 | -15 |
| 7 | 1 | 6 | -7 | -22 | -22 |
| 7 | 2 | 5 | 8 | 6 | -22 |
| 7 | 4 | 3 | 48 | 6 | -22 |

The final value is `-22`, which is the sample answer.

This trace demonstrates why the DP must consider every possible removed element. The best transition into a set need not correspond to any fixed bit position.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n2^n)) | SOS DP performs (n2^{n-1}) additions, and the mask DP examines at most (n) bits per mask |
| Space | (O(2^n)) | Two transformed cost arrays and one DP array contain (2^n) values each |

For (n=20), there are only (1,048,576) subsets. The algorithm performs a linear number of operations per subset, rather than considering pairs of subsets. That is the distinction between roughly tens of millions of operations and the (3.49) billion subset relationships of the brute-force (O(3^n)) approach. The official memory limit is (256) MiB and the time limit is two seconds.

## Test Cases

The following tests use the same `solve` function as the submitted solution. The maximum-size test uses (n=20) with identical costs, which is useful for checking both the subset count and the performance boundary.

```
# Save the submitted solution in solution.py first.
from solution import solve

def run(inp: str) -> str:
    return solve(inp).strip()

# Provided sample 1
assert run(
    """2
-5 9 9 -5
10 -8 -6 3
"""
) == "-16", "sample 1"

# Provided sample 2
assert run(
    """3
-15 19 19 -5 30 -3 -16 13
29 -6 -14 -7 24 -5 18 11
"""
) == "-22", "sample 2"

# Provided sample 3, minimum-size instance
assert run(
    """0
-129363358
227605714
"""
) == "-129363358", "empty ground set"

# Custom: n = 1, negative costs
assert run(
    """1
-5 -10
0 -1
"""
) == "-15", "negative costs"

# Custom: all costs equal
assert run(
    """2
5 5 5 5
7 7 7 7
"""
) == "20", "all-equal costs"

# Custom: n = 20, maximum number of subsets.
# Every subset costs 0 in red and 1 in blue, so painting everything red is optimal.
n = 20
cnt = 1 << n
maximum_input = (
    str(n) + "\n" +
    ("0 " * (cnt - 1)) + "0\n" +
    ("1 " * (cnt - 1)) + "1\n"
)
assert run(maximum_input) == "0", "maximum-size instance"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0`, one red and one blue cost | `-129363358` | Empty ground set and base case |
| `1`, mixed negative costs | `-15` | Negative values and singleton boundary |
| `2`, every red cost `5`, every blue cost `7` | `20` | Equal costs within each color and unrestricted all-red coloring |
| `20`, all red costs `0`, all blue costs `1` | `0` | Maximum number of subsets and (2^n) indexing boundary |

## Edge Cases

For (n=0), the mask space contains only mask `0`. The SOS transform has nothing to do, and the DP initializes `dp[0]` to the cheaper of the two costs. For the concrete input

```
0
-129363358
227605714
```

the algorithm computes `dp[0] = min(-129363358, 227605714)`, giving `-129363358`. This is exactly the required behavior for the single empty subset.

For negative costs, consider

```
1
-5 -10
0 -1
```

The empty subset is cheapest in red, at `-5`, and the singleton is also cheapest in red, at `-10`, so the answer is `-15`. The DP starts with `dp[0] = -5`. For mask `1`, removing its only bit leaves mask `0`; the red increment is `-10`, while the blue increment is `-1`. The minimum increment is `-10`, producing `dp[1] = -15`. No assumption about cost positivity appears anywhere in the recurrence.

For all equal costs, consider

```
2
5 5 5 5
7 7 7 7
```

Every one of the four subsets costs `5` in red and `7` in blue. Coloring every subset red is valid because the red family is the entire power set and is trivially union-closed. The answer is consequently `4*5 = 20`. The recurrence finds the same result because every transition chooses the red increment of `5` per newly forced subset rather than the blue increment of `7`.

The maximum-size boundary is (n=20), where mask `2^20-1 = 1,048,575` is the largest valid index. A common implementation error is accidentally allocating `2^n-1` entries or using an inclusive loop that accesses index `2^n`. The solution allocates exactly `1 << n` entries and processes masks from `1` through `m-1`, so the largest mask is handled exactly once without an out-of-bounds access.

The main logical edge case is a set whose optimal coloring contains both colors. The recurrence does not assume that an entire set is monochromatic. Instead, it only relies on the existence of one element whose entire containing half of the subset lattice has the same color as the full set. Once that element is fixed, the remaining half is recursively optimized. This is precisely what makes the union-closure condition useful without having to enumerate complete colorings.
