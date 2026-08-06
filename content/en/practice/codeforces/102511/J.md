---
title: "CF 102511J - Miniature Golf"
description: "Each player has a list of scores, one score for every hole. The value remembered after applying the unknown limit l is not the original score x, but min(x, l). For a fixed l, every player gets a total score by replacing all large hole scores with l."
date: "2026-08-06T19:30:15+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102511
codeforces_index: "J"
codeforces_contest_name: "2019 ICPC World Finals"
rating: 0
weight: 102511
solve_time_s: 78
verified: true
draft: false
---

[CF 102511J - Miniature Golf](https://codeforces.com/problemset/problem/102511/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

Each player has a list of scores, one score for every hole. The value remembered after applying the unknown limit `l` is not the original score `x`, but `min(x, l)`. For a fixed `l`, every player gets a total score by replacing all large hole scores with `l`. A smaller total is better, and the rank of a player is the number of players whose adjusted total is not larger than theirs.

The task is not to find one particular limit. Instead, we may choose the value of `l` that gives each player the best possible position, and we must output that minimum achievable rank.

The number of players is at most 500 and the number of holes is at most 50. A direct simulation over possible limits is impossible because scores can be as large as `10^9`. The useful restriction is the small number of score values per player. A player’s adjusted score only changes when `l` reaches one of the original hole scores, so the total number of interesting points is limited by `p * h`, not by the size of the score values.

The tricky part is that the best limit for one player may be somewhere between two score values. A solution that only checks limits appearing in the input can miss the optimum. Another common mistake is to find the best limit separately against every opponent. The same `l` must improve the player’s position against all opponents simultaneously.

For example:

```
2 1
5
10
```

If we only test the original values, we check `l = 5` and `l = 10`. At `l = 5`, both players have score 5, so the first player has rank 2. At `l = 10`, the scores are 5 and 10, so the first player has rank 1. The answer is 1. This case shows why the limit itself matters, not only the intervals between limits.

Another boundary case is:

```
2 2
100 100
1 1
```

The first player can never beat the second player. For every positive `l`, the second player has total score at most 2 while the first player has total score at least 2 and is never strictly better. The correct ranks are:

```
2 1
```

A careless implementation that assumes every player can eventually become better when `l` grows would fail here.

## Approaches

The straightforward approach is to try every possible value of `l`, calculate all adjusted scores, sort the players, and record the best rank. This is correct because it literally checks every possible game adjustment. However, `l` can be as large as `10^9`, so this cannot work.

A better view is to compare players pairwise. Fix a player `i`. If we know the intervals of `l` where `i` beats another player `j`, then the rank of `i` is best when the number of opponents beaten at the same limit is as large as possible.

For two players, their score difference is a piecewise linear function. The only places where the formula changes are the hole scores of these two players. Between two consecutive such values, every hole is either already capped or still equal to `l`, so the total score is a linear function of `l`. This means we can sweep through the important ranges, determine exactly where player `i` becomes better than player `j`, and store those intervals.

After collecting all intervals against all opponents, the remaining problem is finding the maximum number of intervals covering the same integer value of `l`. This is a standard sweep line problem using start and end events.

The brute force approach works because the score function is simple for a fixed limit, but fails because there are too many possible limits. The observation that the score functions are piecewise linear reduces the infinite search space to a small collection of intervals.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(number of limits * p * h) | O(p) | Too slow |
| Optimal | O(p²h log(ph)) | O(ph) | Accepted |

## Algorithm Walkthrough

1. For each player `i`, assume we want to know the best rank of this player. We will count how many other players `i` can strictly beat for some common value of `l`.
2. For every opponent `j`, construct the intervals of limits where player `i` has a smaller adjusted total score than player `j`.
3. To construct these intervals, collect all hole scores belonging to players `i` and `j`. These values divide the positive integers into ranges where both adjusted scores are linear functions.
4. On each range, compute the linear difference between the two players. Since the difference has the form `a*l+b`, we can find the exact integer part where it is negative. Those integers are the limits where `i` beats `j`.
5. Add the resulting interval to a sweep line structure. A start event increases the number of beaten opponents, and the event after the interval ends decreases it.
6. After processing all opponents, the maximum number of simultaneously active intervals is the maximum number of players beaten by `i`. The best rank is `p - maximum_beaten`.

Why it works:

For any fixed opponent, the comparison between two players changes only at score values or where two linear functions cross. The interval construction finds exactly all limits where the first player is better. The sweep line then checks every possible limit represented by those intervals and finds the maximum number of opponents that can be beaten simultaneously. Since rank is exactly the number of players not beaten plus the player themselves, the computed value is minimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def adjusted_diff_coeff(a, b, x):
    m = 0
    c = 0
    for u, v in zip(a, b):
        if x < u:
            m += 1
        else:
            c += u
        if x < v:
            m -= 1
        else:
            c -= v
    return m, c

def intervals(a, b):
    pts = sorted(set(a + b))
    segs = []

    if pts[0] > 1:
        segs.append((1, pts[0] - 1))
    for x in pts:
        segs.append((x, x))
    for x, y in zip(pts, pts[1:]):
        if x + 1 <= y - 1:
            segs.append((x + 1, y - 1))
    segs.append((pts[-1] + 1, None))

    ans = []

    for l, r in segs:
        m, c = adjusted_diff_coeff(a, b, l)

        if r is None:
            if m == 0:
                if c < 0:
                    ans.append((l, None))
            elif m < 0:
                ans.append((l, None))
            continue

        if l == r:
            if m * l + c < 0:
                ans.append((l, l))
            continue

        if m == 0:
            if c < 0:
                ans.append((l, r))
        elif m > 0:
            # m*x+c < 0
            hi = (-c - 1) // m
            if hi >= l:
                ans.append((l, min(r, hi)))
        else:
            # m*x+c < 0, multiply by -1
            lo = c // (-m) + 1
            if lo <= r:
                ans.append((max(l, lo), r))

    return ans

def solve():
    p, h = map(int, input().split())
    scores = [list(map(int, input().split())) for _ in range(p)]

    res = []

    for i in range(p):
        events = []
        for j in range(p):
            if i == j:
                continue
            for l, r in intervals(scores[i], scores[j]):
                events.append((l, 1))
                if r is not None:
                    events.append((r + 1, -1))

        events.sort()
        cur = 0
        best = 0
        k = 0
        while k < len(events):
            pos = events[k][0]
            while k < len(events) and events[k][0] == pos:
                cur += events[k][1]
                k += 1
            best = max(best, cur)

        res.append(str(p - best))

    print(" ".join(res))

if __name__ == "__main__":
    solve()
```

The main function processes players one at a time because the rank of one player does not affect the intervals of another player. The `intervals` function handles one pair of players and returns all limits where the first player wins the comparison.

The helper `adjusted_diff_coeff` computes the linear representation of the score difference on a fixed segment. A hole contributes either a constant original score or one copy of `l`, so the whole difference can always be written as `m*l+c`.

The interval code separates three cases. A single point checks one exact limit. A finite segment solves a linear inequality. The infinite tail is handled separately because there is no upper endpoint. Python integers avoid overflow even when scores reach `10^9`.

The sweep uses `r + 1` for ending events because intervals contain integer limits. Forgetting this conversion is a common off-by-one mistake.

## Worked Examples

For the first sample:

```
3 3
2 2 2
4 2 1
4 4 1
```

Consider player 1.

| Opponent | Winning limits for player 1 | Maximum beaten so far |
| --- | --- | --- |
| Player 2 | limits where score 1 < score 2 | 1 |
| Player 3 | limits where score 1 < score 3 | 2 |

Player 1 can beat both opponents at the same limit, so the best rank is `3 - 2 = 1`.

For the second sample, the same process gives:

| Player | Maximum opponents beaten | Minimum rank |
| --- | --- | --- |
| 1 | 5 | 1 |
| 2 | 4 | 2 |
| 3 | 1 | 5 |
| 4 | 1 | 5 |
| 5 | 2 | 4 |
| 6 | 3 | 3 |

The trace demonstrates that the chosen limit must be shared between all comparisons. The sweep line finds exactly those common regions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(p²h log(ph)) | Every pair of players creates O(h) events, and each player performs a sweep over all opponent intervals. |
| Space | O(ph) | Only the current player’s events and the score matrix are stored. |

With `p = 500` and `h = 50`, the number of pair comparisons is manageable. The algorithm never depends on the magnitude of the scores, only on how many score changes exist.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    solve()
    out = sys.stdout.getvalue() if hasattr(sys.stdout, "getvalue") else ""
    sys.stdin = old
    return out

# sample 1
assert run("""3 3
2 2 2
4 2 1
4 4 1
""") == "1 2 2\n"

# sample 2
assert run("""6 4
3 1 2 2
4 3 2 2
6 6 3 2
7 3 4 3
3 4 2 4
2 3 3 5
""") == "1 2 5 5 4 3\n"

# minimum size
assert run("""2 1
5
10
""") == "1 2\n"

# all equal
assert run("""3 2
4 4
4 4
4 4
""") == "3 3 3\n"

# always losing
assert run("""2 2
100 100
1 1
""") == "2 1\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Two players, one hole | `1 2` | A useful limit can be between score values. |
| Equal players | `3 3 3` | Ties are counted correctly in ranks. |
| Dominated player | `2 1` | A player cannot become better without a valid interval. |
| Samples | Sample outputs | General correctness. |

## Edge Cases

The first edge case is when the best limit is not one of the original scores. For input:

```
2 1
5
10
```

the interval `(5,10)` changes the comparison, and the algorithm examines it because the score functions are linear between breakpoints.

The second edge case is a player who can never beat another player. For:

```
2 2
100 100
1 1
```

the difference function is never negative. The interval generator produces no winning interval, so the sweep counts zero beaten opponents for the first player and one for the second.

A third case is many identical scores:

```
3 1
7
7
7
```

Every pair comparison is always equal, so no player has a winning interval. The maximum number of beaten opponents is zero and every rank becomes 3, matching the definition that equal scores share the same rank.
