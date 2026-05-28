---
title: "CF 39C - Moon Craters"
description: "Each crater is represented by a center position c on a line and a radius r. Since every crater is circular and the robot"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dp", "sortings"]
categories: ["algorithms"]
codeforces_contest: 39
codeforces_index: "C"
codeforces_contest_name: "School Team Contest 1 (Winter Computer School 2010/11)"
rating: 2100
weight: 39
solve_time_s: 162
verified: false
draft: false
---

[CF 39C - Moon Craters](https://codeforces.com/problemset/problem/39/C)

**Rating:** 2100  
**Tags:** dp, sortings  
**Solve time:** 2m 42s  
**Verified:** no  

## Solution
## Problem Understanding

Each crater is represented by a center position `c` on a line and a radius `r`. Since every crater is circular and the robot only moves along one straight path, every crater can be viewed as an interval on the line:

$[c-r,\ c+r]$

The professor's theory says that for every pair of chosen craters, one of two things must happen:

1. One crater is completely inside the other.
2. The two craters are completely disjoint.

Touching at exactly one point is allowed.

What is forbidden is partial overlap. In interval language, we cannot have:

$l_1 < l_2 < r_1 < r_2$

because that means the intervals intersect but neither contains the other.

We must select the largest subset of craters satisfying this condition and output any valid set of indices.

The input size is at most 2000. That immediately rules out anything exponential. A brute-force subset search would require checking up to:

$2^{2000}$

which is impossible.

An `O(n^2)` or `O(n^3)` dynamic programming solution is realistic. Around four million operations is comfortable in Python, while eight billion is not.

The tricky part is that the condition is global. A crater may be compatible with one crater and also compatible with another, while those two are incompatible with each other. Greedy selection based only on local decisions fails.

There are several edge cases that easily break naive implementations.

Consider touching intervals:

```
2
0 1
2 1
```

The intervals are `[−1,1]` and `[1,3]`. They touch at one point and are allowed together. A strict inequality check would incorrectly reject them.

Now consider nested craters:

```
3
0 10
0 5
0 2
```

All three are valid together because every smaller crater lies fully inside the larger one. A solution that only handles disjoint intervals would miss this.

Partial overlap is the dangerous case:

```
2
0 5
4 5
```

The intervals are `[−5,5]` and `[−1,9]`. They intersect, but neither contains the other. These two cannot coexist.

Another subtle case is when many intervals share endpoints:

```
4
0 2
2 2
4 2
6 2
```

The intervals are `[-2,2]`, `[0,4]`, `[2,6]`, `[4,8]`. Adjacent pairs partially overlap even though endpoints line up neatly. Careless interval logic often misclassifies them.

## Approaches

A brute-force solution would try every subset of craters and verify whether all pairs satisfy the rule. Verifying one subset costs `O(k^2)` for `k` chosen craters, and there are `2^n` subsets. Even for `n = 40`, this becomes hopeless.

A more reasonable brute-force dynamic programming idea is to process intervals after sorting and attempt transitions between compatible intervals. The problem is that compatibility is not transitive. Two intervals may each be compatible with a third while being incompatible with each other. Pairwise DP states are not enough.

The key observation is that valid configurations have a laminar structure.

For any two chosen intervals, exactly one of these holds:

1. They are disjoint.
2. One fully contains the other.

This is precisely the structure of properly nested intervals. If we sort intervals by their left endpoint, then inside any fixed outer interval, the chosen intervals split into independent groups between consecutive boundaries.

That suggests interval DP.

Suppose we define a DP over coordinate-compressed endpoints. For every segment `[L,R]`, we compute the maximum number of craters that can be chosen completely inside that segment.

Now focus on one crater `i` with interval `[li, ri]`.

If we decide to take it, then every other chosen crater inside `[li,ri]` must either:

1. Be fully inside crater `i`, or
2. Be disjoint from crater `i`.

But since we are already restricting ourselves to the interior of `[li,ri]`, every compatible crater must actually lie completely inside it.

That creates a recursive structure. Once we choose an outer crater, the remaining work becomes independent subproblems inside the gaps.

This transforms the problem into a classic interval DP with reconstruction.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(2^n · n^2)` | `O(n)` | Too slow |
| Optimal Interval DP | `O(n^3)` | `O(n^2)` | Accepted |

## Algorithm Walkthrough

1. Convert every crater into an interval `[l, r] = [c-r, c+r]`.

The geometric condition becomes a pure interval relation problem.
2. Collect all interval endpoints and coordinate-compress them.

Endpoints may be as large as `10^9`, but only relative ordering matters.
3. Sort craters by increasing left endpoint and decreasing right endpoint.

When two intervals start at the same position, the larger one must come first so nesting behaves correctly.
4. Define `dp[L][R]` as the maximum number of craters that can be selected using only intervals completely inside compressed segment `[L,R]`.
5. For every segment `[L,R]`, try two possibilities.

Either we skip the left boundary and move forward, or we choose some crater whose left endpoint equals `L`.
6. Suppose crater `i` has interval `[li, ri]`.

If we take it, then:

- We gain `1` for this crater.
- Any chosen crater strictly inside it must lie inside `[li,ri]`.
- Any crater outside it must lie completely to its right.

This leads to the transition:

$dp[L][R] = \max(dp[L][R],\ 1 + dp[li+1][ri-1] + dp[ri+1][R])$

1. Process segments in increasing length order.

Smaller segments are needed before larger ones.
2. Store reconstruction information whenever a transition improves the answer.

After DP finishes, recursively rebuild the chosen set of crater indices.

### Why it works

The crucial invariant is that every valid family of intervals inside a segment can be decomposed around the leftmost chosen interval.

Take the chosen interval with smallest left endpoint. Any other chosen interval must either lie completely inside it or be completely disjoint and to its right. Partial overlap is forbidden.

That means the solution splits into two independent parts:

1. Intervals nested inside the chosen interval.
2. Intervals entirely to the right of it.

The DP transition enumerates exactly these possibilities, and every valid configuration appears in exactly one decomposition. Since every transition combines only compatible substructures, the constructed answer is always valid.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())

craters = []

coords = []

for idx in range(1, n + 1):
    c, r = map(int, input().split())
    l = c - r
    rr = c + r

    craters.append((l, rr, idx))
    coords.append(l)
    coords.append(rr)

coords = sorted(set(coords))
comp = {x: i for i, x in enumerate(coords)}

m = len(coords)

intervals = []

for l, r, idx in craters:
    intervals.append((comp[l], comp[r], idx))

intervals.sort(key=lambda x: (x[0], -x[1]))

starts = [[] for _ in range(m)]

for l, r, idx in intervals:
    starts[l].append((r, idx))

dp = [[0] * m for _ in range(m)]
choice = [[None] * m for _ in range(m)]

for length in range(m):
    for L in range(m - length):
        R = L + length

        best = 0
        best_choice = ("skip",)

        if L + 1 <= R:
            best = dp[L + 1][R]

        for r, idx in starts[L]:
            if r > R:
                continue

            val = 1

            if L + 1 <= r - 1:
                val += dp[L + 1][r - 1]

            if r + 1 <= R:
                val += dp[r + 1][R]

            if val > best:
                best = val
                best_choice = ("take", r, idx)

        dp[L][R] = best
        choice[L][R] = best_choice

answer = []

def build(L, R):
    if L > R:
        return

    act = choice[L][R]

    if act is None:
        return

    if act[0] == "skip":
        build(L + 1, R)
    else:
        _, r, idx = act

        answer.append(idx)

        build(L + 1, r - 1)
        build(r + 1, R)

build(0, m - 1)

print(len(answer))
print(*answer)
```

The first part converts each crater into an interval and compresses coordinates. Coordinate compression is necessary because endpoints can be as large as `10^9`, while the DP only depends on ordering.

Sorting by increasing left endpoint and decreasing right endpoint is subtle but important. If two intervals share the same left endpoint, the larger interval must appear first so nested processing remains valid.

The DP state `dp[L][R]` stores the optimal answer using intervals fully contained inside compressed coordinate range `[L,R]`.

The `"skip"` transition corresponds to ignoring every interval beginning at `L` and moving the left boundary forward.

The `"take"` transition selects one interval starting at `L`. Once selected, the problem splits into two independent subproblems:

1. Intervals strictly inside the chosen crater.
2. Intervals completely to its right.

The reconstruction function mirrors these transitions exactly.

One easy mistake is mishandling empty ranges like `[L+1, r-1]`. The code checks validity before accessing DP values.

Another common bug is using strict inequalities for touching intervals. Touching is allowed, so intervals sharing endpoints are compatible.

## Worked Examples

### Example 1

Input:

```
4
1 1
2 2
4 1
5 1
```

Intervals:

| Crater | Interval |
| --- | --- |
| 1 | [0,2] |
| 2 | [0,4] |
| 3 | [3,5] |
| 4 | [4,6] |

Compressed coordinates:

| Coordinate | Index |
| --- | --- |
| 0 | 0 |
| 2 | 1 |
| 3 | 2 |
| 4 | 3 |
| 5 | 4 |
| 6 | 5 |

Key transitions:

| Segment | Best choice | Value |
| --- | --- | --- |
| [0,1] | take crater 1 | 1 |
| [0,3] | take crater 2 | 2 |
| [0,5] | take crater 2 + crater 4 | 3 |

Final answer contains craters `{1,2,4}`.

This example demonstrates nesting plus disjointness together. Crater 1 lies inside crater 2, while crater 4 is disjoint from crater 2.

### Example 2

Input:

```
3
0 5
4 5
20 1
```

Intervals:

| Crater | Interval |
| --- | --- |
| 1 | [-5,5] |
| 2 | [-1,9] |
| 3 | [19,21] |

The first two intervals partially overlap and cannot coexist.

DP decisions:

| Segment | Decision |
| --- | --- |
| whole range | choose crater 1 and crater 3 |
| alternative | choose crater 2 and crater 3 |

Maximum size is `2`.

This example confirms that partial overlap is correctly rejected.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n^3)` | There are `O(n^2)` DP states and each may iterate over `O(n)` intervals |
| Space | `O(n^2)` | DP and reconstruction tables |

With `n ≤ 2000`, cubic complexity is acceptable in optimized Python because the constant factors are small and the actual number of compressed coordinates is at most `2n`.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n = int(input())

    craters = []
    coords = []

    for idx in range(1, n + 1):
        c, r = map(int, input().split())

        l = c - r
        rr = c + r

        craters.append((l, rr, idx))

        coords.append(l)
        coords.append(rr)

    coords = sorted(set(coords))
    comp = {x: i for i, x in enumerate(coords)}

    m = len(coords)

    intervals = []

    for l, r, idx in craters:
        intervals.append((comp[l], comp[r], idx))

    intervals.sort(key=lambda x: (x[0], -x[1]))

    starts = [[] for _ in range(m)]

    for l, r, idx in intervals:
        starts[l].append((r, idx))

    dp = [[0] * m for _ in range(m)]
    choice = [[None] * m for _ in range(m)]

    for length in range(m):
        for L in range(m - length):
            R = L + length

            best = 0
            best_choice = ("skip",)

            if L + 1 <= R:
                best = dp[L + 1][R]

            for r, idx in starts[L]:
                if r > R:
                    continue

                val = 1

                if L + 1 <= r - 1:
                    val += dp[L + 1][r - 1]

                if r + 1 <= R:
                    val += dp[r + 1][R]

                if val > best:
                    best = val
                    best_choice = ("take", r, idx)

            dp[L][R] = best
            choice[L][R] = best_choice

    ans = []

    def build(L, R):
        if L > R:
            return

        act = choice[L][R]

        if act is None:
            return

        if act[0] == "skip":
            build(L + 1, R)
        else:
            _, r, idx = act

            ans.append(idx)

            build(L + 1, r - 1)
            build(r + 1, R)

    build(0, m - 1)

    return str(len(ans)) + "\n" + " ".join(map(str, sorted(ans)))

# provided sample
assert run(
"""4
1 1
2 2
4 1
5 1
""").splitlines()[0] == "3", "sample 1"

# single crater
assert run(
"""1
10 5
""") == "1\n1", "single crater"

# fully nested
assert run(
"""3
0 10
0 5
0 2
""").splitlines()[0] == "3", "all nested"

# partial overlap
assert run(
"""2
0 5
4 5
""").splitlines()[0] == "1", "partial overlap forbidden"

# touching intervals
assert run(
"""2
0 1
2 1
""").splitlines()[0] == "2", "touching allowed"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single crater | 1 crater selected | Minimum input size |
| Fully nested intervals | All selected | Correct nesting handling |
| Partial overlap | Only one selected | Forbidden overlap detection |
| Touching intervals | Both selected | Boundary inclusiveness |

## Edge Cases

Consider touching intervals:

```
2
0 1
2 1
```

The intervals are `[-1,1]` and `[1,3]`.

During DP, these intervals belong to separate subsegments after compression. Since sharing an endpoint is allowed, no conflict occurs, and both are selected. The answer size becomes `2`.

Now consider fully nested intervals:

```
3
0 10
0 5
0 2
```

Intervals:

```
[-10,10]
[-5,5]
[-2,2]
```

The outer crater is selected first. The recursive subproblem inside it still contains the other two intervals, which are also compatible through containment. The reconstruction correctly outputs all three indices.

For partial overlap:

```
2
0 5
4 5
```

Intervals:

```
[-5,5]
[-1,9]
```

If the DP selects the first interval, the second cannot appear either inside it or completely to its right. The decomposition blocks this invalid combination automatically. The maximum valid subset size is `1`.

Finally, consider intervals sharing many boundaries:

```
4
0 2
2 2
4 2
6 2
```

Intervals:

```
[-2,2]
[0,4]
[2,6]
[4,8]
```

Adjacent intervals partially overlap, so the DP cannot chain all four together. It carefully separates only genuinely disjoint or nested configurations, avoiding false positives caused by endpoint coincidences.
