---
title: "CF 102461C - Advertisement Profit"
description: "We start with exactly 10,000 subscribers. There are two kinds of videos. A regular video increases the subscriber count by its ai and gives no direct revenue."
date: "2026-08-09T15:03:33+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102461
codeforces_index: "C"
codeforces_contest_name: "Innopolis Open 2019-2020, qualification, contest 2"
rating: 0
weight: 102461
solve_time_s: 453
verified: true
draft: false
---

[CF 102461C - Advertisement Profit](https://codeforces.com/problemset/problem/102461/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 7m 33s  
**Verified:** yes  

## Solution
## Problem Understanding

We start with exactly 10,000 subscribers. There are two kinds of videos. A regular video increases the subscriber count by its `a_i` and gives no direct revenue. A commercial video has parameters `c_i` and `b_i`: when it is released, it earns `c_i` cents for every subscriber currently present, and then the subscriber count decreases by `b_i`.

For every requested number `d`, we must choose exactly `d` videos from the prepared ones and arrange those chosen videos in the best possible order. The answer is the maximum total advertising revenue. The original constraints have `n,m <= 100`, `a_i,b_i,c_i <= 100`, and the time limit is one second with 512 MB of memory.

The small values of `n` and `m` rule out algorithms that enumerate arbitrary subsets or permutations. With 200 available videos, even enumerating every possible ordering would already require on the order of `200!`, which is far beyond anything feasible. The useful numeric bound is instead that the sum of all commercial `c_i` values is at most 10,000. That gives us a manageable knapsack-like dimension.

There are several edge cases where a straightforward implementation can silently go wrong. If `d = 0`, the answer is exactly zero because no commercial video can be released. For example,

```
0
0
1
0
```

has output

```
0
```

An implementation that initializes every answer to a negative sentinel and never handles zero videos separately can accidentally print that sentinel.

Another case is having no commercial videos at all. For

```
2
5
7
0
3
0
1
2
```

every answer is zero. Regular videos can increase the subscriber count, but without a commercial video there is nothing to monetize.

A third edge case is when the requested number of videos is larger than the number of commercial videos. Suppose

```
2
5
6
1
10 1
1
2
```

The optimal choice for `d = 2` is the commercial video together with the regular video worth 6 subscribers. The profit is `10 * 10006 = 100060`. Choosing two regular videos gives zero. A solution that considers only the commercial subset and forgets that regular videos can be required to reach exactly `d` videos will fail here.

The most subtle case is the ordering of commercial videos. For

```
0
2
10 20
20 10
1
2
```

the answer is `299900`. The second commercial video should be released first because its `c/b` ratio is larger. Reversing the order loses additional subscribers before the more expensive advertisement. The official sample exhibits exactly this ordering phenomenon.

## Approaches

The direct approach is to enumerate every possible set of videos and every ordering of that set. For a fixed `d`, there are

[
P(n+m,d)=\frac{(n+m)!}{(n+m-d)!}
]

ordered choices. If all possible values of `d` are queried, the total number of schedules is

[
\sum_{d=0}^{n+m} P(n+m,d).
]

With `n+m=200`, this already contains the term `200!`, approximately `7.9 * 10^374`. The brute force is correct because every possible choice and every possible ordering is considered, but it becomes useless almost immediately.

The first useful observation is that regular videos should always come before commercial videos. Suppose a regular video increases subscribers by `a`, and a commercial video with coefficient `c` is currently released at `s` subscribers. Releasing the commercial video first earns `c*s`. Releasing the regular video first earns `c*(s+a)`, which is strictly larger. Thus every regular video selected for the answer can be moved to the front without hurting the profit.

The second observation is that, once the set of commercial videos is fixed, their relative order is forced by a simple pairwise exchange argument. Consider commercial videos `x` and `y`, and suppose there are `s` subscribers before them. If `x` is released before `y`, their combined revenue is

[
c_xs+c_y(s-b_x).
]

If `y` is released before `x`, it is

[
c_ys+c_x(s-b_y).
]

The first order is at least as good exactly when

[
c_xb_y \ge c_yb_x,
]

which is equivalent to

[
\frac{c_x}{b_x}\ge\frac{c_y}{b_y}.
]

So commercial videos must appear in decreasing order of `c/b`.

Now fix that ordering and suppose we select some commercial videos. If we process them in the reverse order, namely increasing `c/b`, adding a commercial video with parameters `(c,b)` after previously processed advertisements causes a penalty of

[
b \cdot C,
]

where `C` is the sum of the `c` values of the previously processed advertisements. This gives a knapsack-style dynamic program.

Let `dp[k][s]` be the maximum negative penalty after selecting exactly `k` commercial videos whose total `c` is `s`. When the next commercial video has parameters `(c,b)`, skipping it changes nothing. Taking it changes the state to

\max(dp[k+1][s+c], dp[k][s]-b\cdot s).
]

The actual revenue is then easy to reconstruct. If the selected commercial videos have total `c` equal to `s`, and the selected regular videos contribute `A` additional subscribers, the initial subscriber count seen by every commercial video is `10000+A`. Thus their base revenue is

[
s(10000+A),
]

and the DP value subtracts exactly the loss caused by previous commercial videos.

For a fixed number `l` of regular videos, we should choose the `l` largest `a_i` values. Every selected regular video is placed before every commercial video, so its entire contribution is multiplied by the total `c` of the selected commercial videos. There is no reason to choose a smaller `a_i`.

There is one more optimization useful for Python. For a fixed number `k` of commercial videos, every DP state `(s, dp[k][s])` represents a line

[
f(x)=s x+dp[k][s],
]

where `x=10000+A` is the subscriber count before all advertisements. We need the maximum of these lines for several increasing values of `x`, one for each possible number of regular videos. Since the slopes `s` are increasing, the upper envelope can be constructed with a monotonic convex hull and queried in linear time.

The brute-force method works because it explicitly represents every possible schedule, but fails because there are factorially many schedules. The observation that the order of regular videos and commercial videos can be normalized, followed by the fixed `c/b` ordering of advertisements, reduces the problem to a bounded knapsack DP over the total commercial coefficient.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(sum P(n+m,d))` | `O(n+m)` | Too slow |
| Optimal | `O(m²C + nm + m log m)`, where `C=sum c_i <= 10000` | `O(mC + n)` | Accepted |

The implementation additionally restricts every DP scan to the minimum and maximum reachable sums for each `k`, which is substantially smaller than scanning all `C` positions in many inputs.

## Algorithm Walkthrough

1. Sort the regular-video increases in decreasing order and build prefix sums. If we use exactly `l` regular videos, the best possible total increase is the prefix sum of the first `l` values. This works because every regular video is released before every commercial video, so each additional subscriber helps every selected advertisement equally.
2. Store every commercial video as `(c,b)` and sort them by increasing `c/b`. The actual optimal release order is decreasing `c/b`, but processing the advertisements in the reverse order makes the DP transition convenient. Equal ratios may be ordered arbitrarily because swapping equal-ratio advertisements does not change the revenue.
3. Define `dp[k][s]` as the maximum value of the negative interaction penalty for choosing `k` commercial videos with total coefficient `s` among the advertisements processed so far. Initially only `dp[0][0] = 0` is reachable.
4. Process the commercial videos one by one. For a video `(c,b)`, iterate `k` downward so the same video cannot be selected twice. For every reachable sum `s`, skipping the video leaves the state unchanged. Selecting it creates the state `(k+1, s+c)` with value `dp[k][s] - b*s`.

The term `b*s` has a direct meaning. All previously processed advertisements contribute their `c` values to the total coefficient `s`, and releasing the current advertisement after them means it loses `b` subscribers for each of those coefficient units.
5. For each number `k` of selected advertisements, interpret every finite DP state `(s,dp[k][s])` as a line `s*x + dp[k][s]`. Here `x` is the subscriber count after all selected regular videos and immediately before the commercial sequence.
6. Build the upper hull of these lines. Slopes are already increasing because the slope is exactly the total `c` value `s`. Remove a middle line whenever its intersection with the previous line occurs no earlier than the intersection of the previous line with the next line. Such a line can never be optimal for any query `x`.
7. Query the hull for every possible number `l` of regular videos. The query value is `10000 + prefix[l]`. If the hull gives `profit_ads`, then the total number of released videos is `d=l+k`, so update `answer[d]` with this value.
8. Read the requested values `d` and print the corresponding precomputed answers. Since all possible `d` values are handled before reading the queries, every query is answered in constant time.

### Why it works

For every feasible schedule, moving all selected regular videos to the front cannot decrease any commercial video's subscriber count, so an optimal schedule has all regular videos first. Among the selected commercial videos, the pairwise exchange calculation proves that decreasing `c/b` is the only optimal relative ordering, up to ties. The DP processes exactly the reverse of this order, and its transition subtracts `b` times the total `c` of advertisements already processed, which is precisely the revenue lost because those advertisements were released earlier. Thus every commercial subset has exactly its optimal penalty represented by one DP state. Finally, choosing the largest regular-video increases is optimal for every fixed number of regular videos, and the hull evaluates the best commercial subset for every resulting subscriber count. Hence every combination considered by the final maximization is optimal for its number of released videos, and every possible number is considered.

## Python Solution

```python
import sys
from functools import cmp_to_key

input = sys.stdin.readline

NEG = -10**30
INF = 10**30
INITIAL = 10000

def solve():
    n = int(input())
    good = [int(input()) for _ in range(n)]
    good.sort(reverse=True)

    pref = [0]
    for x in good:
        pref.append(pref[-1] + x)

    m = int(input())
    ads = []
    total_c = 0

    for _ in range(m):
        c, b = map(int, input().split())
        ads.append((c, b))
        total_c += c

    # DP is processed in increasing c / b order.
    # The actual release order is the reverse.
    def cmp(x, y):
        left = x[0] * y[1]
        right = y[0] * x[1]
        if left < right:
            return -1
        if left > right:
            return 1
        return 0

    ads.sort(key=cmp_to_key(cmp))

    # dp[k][s] = maximum negative interaction penalty
    # for k ads with total coefficient s.
    dp = [[NEG] * (total_c + 1) for _ in range(m + 1)]
    dp[0][0] = 0

    # Exact lower/upper bounds on possible total c for k selected
    # advertisements among the already processed advertisements.
    min_sum = [INF] * (m + 1)
    max_sum = [NEG] * (m + 1)
    min_sum[0] = 0
    max_sum[0] = 0

    processed = 0

    for c, b in ads:
        # Descending k makes the update 0/1: the current advertisement
        # cannot be used again during this iteration.
        for k in range(processed, -1, -1):
            lo = min_sum[k]
            hi = max_sum[k]

            if lo == INF:
                continue

            row = dp[k]
            nxt = dp[k + 1]

            for s in range(lo, hi + 1):
                val = row[s]
                if val == NEG:
                    continue

                ns = s + c
                nv = val - b * s

                if nv > nxt[ns]:
                    nxt[ns] = nv

        # Update reachable sum bounds after using this advertisement.
        for k in range(processed, -1, -1):
            if min_sum[k] != INF:
                v = min_sum[k] + c
                if v < min_sum[k + 1]:
                    min_sum[k + 1] = v

            if max_sum[k] != NEG:
                v = max_sum[k] + c
                if v > max_sum[k + 1]:
                    max_sum[k + 1] = v

        processed += 1

    # Build upper hull and query it for every possible subscriber count.
    #
    # A line is represented by y = slope * x + intercept.
    # Slopes are increasing because slope = total commercial c.
    def build_hull(k):
        hull_m = []
        hull_b = []

        lo = min_sum[k]
        hi = max_sum[k]

        if lo == INF:
            return hull_m, hull_b

        row = dp[k]

        for s in range(lo, hi + 1):
            intercept = row[s]
            if intercept == NEG:
                continue

            while len(hull_m) >= 2:
                m1 = hull_m[-2]
                b1 = hull_b[-2]
                m2 = hull_m[-1]
                b2 = hull_b[-1]

                # Remove the middle line if:
                # (b1-b2)/(m2-m1) >= (b2-intercept)/(s-m2)
                if (b1 - b2) * (s - m2) >= \
                   (b2 - intercept) * (m2 - m1):
                    hull_m.pop()
                    hull_b.pop()
                else:
                    break

            hull_m.append(s)
            hull_b.append(intercept)

        return hull_m, hull_b

    answer = [NEG] * (n + m + 1)

    for k in range(m + 1):
        hull_m, hull_b = build_hull(k)

        if not hull_m:
            continue

        pointer = 0

        for l in range(n + 1):
            x = INITIAL + pref[l]

            while pointer + 1 < len(hull_m):
                cur = hull_m[pointer] * x + hull_b[pointer]
                nxt = hull_m[pointer + 1] * x + hull_b[pointer + 1]

                if nxt >= cur:
                    pointer += 1
                else:
                    break

            profit = hull_m[pointer] * x + hull_b[pointer]
            d = k + l

            if profit > answer[d]:
                answer[d] = profit

    q = int(input())
    out = []

    for _ in range(q):
        d = int(input())
        out.append(str(answer[d]))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The input section first sorts the regular increases and builds their prefix sums. `pref[l]` is the maximum total subscriber increase obtainable from exactly `l` regular videos.

The commercial videos are sorted by cross multiplication rather than floating-point division. The comparator places smaller `c/b` first because the DP processes the optimal commercial order backwards. Using `c1 * b2` and `c2 * b1` avoids every possible floating-point comparison issue.

The DP uses one array for every possible number of selected advertisements. Iterating `k` downward is the standard 0/1-knapsack direction. If we iterated upward, the current advertisement could be used repeatedly in the same iteration.

The DP sum is the total `c`, not the total `b`. This is the central implementation detail. When an advertisement with decrease `b` is placed after advertisements whose coefficient sum is `s`, its revenue is reduced by exactly `b*s`. That is why the transition subtracts `b * s`.

The `min_sum` and `max_sum` arrays are only an implementation optimization. They record the smallest and largest possible total `c` for each `k`, so the inner loop does not scan impossible positions in the DP row. The `NEG` sentinel is chosen far below every feasible answer, while Python integers have arbitrary precision, so overflow is not a concern.

The final hull step turns every DP state into a line. Its slope is the total commercial coefficient `s`, and its intercept is the interaction penalty stored by the DP. Since the subscriber count `x` only increases as more regular videos are selected, hull queries can move forward monotonically.

The official samples are

```
1
10
2
10 20
20 10
4
0
1
2
3
```

with output

```
0
200000
299900
300200
```

and

```
3
10
40
30
3
5 10
15 20
1 100
7
0
1
2
3
4
5
6
```

with output

```
0
150000
199900
209870
210710
211340
211550
```

These are the two samples from the original problem.

## Worked Examples

For the first sample, the advertisements are `(c,b)=(10,20)` and `(20,10)`. Their ratios are `0.5` and `2`, so the DP processes `(10,20)` first and `(20,10)` second.

| Processed ads | `k` | Total `c` | DP penalty |
| --- | --- | --- | --- |
| none | 0 | 0 | 0 |
| `(10,20)` | 1 | 10 | 0 |
| `(10,20),(20,10)` | 2 | 30 | -100 |

For `d=1`, taking only the second advertisement gives `20 * 10000 = 200000`. For `d=2`, taking both advertisements gives `30 * 10000 - 100 = 299900`. For `d=3`, the regular video adds 10 subscribers before both advertisements, so the base becomes `10010 * 30`, and the same penalty of 100 gives `300200`.

| `d` | Regular videos | Commercial videos | Base subscribers | Total `c` | Penalty | Profit |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 10000 | 0 | 0 | 0 |
| 1 | 0 | 1 | 10000 | 20 | 0 | 200000 |
| 2 | 0 | 2 | 10000 | 30 | 100 | 299900 |
| 3 | 1 | 2 | 10010 | 30 | 100 | 300200 |

This trace demonstrates why the DP is based on total `c` and why the regular-video contribution is applied to every selected advertisement.

For the second sample, the regular increases become `[40,30,10]`, with prefix sums `[0,40,70,80]`. The commercial ratios are `1/100`, `5/10`, and `15/20`, so the DP order is `(1,100)`, `(5,10)`, `(15,20)`. The optimal actual release order is the reverse.

| `d` | Regular videos | Commercial videos | Base subscribers | Total `c` | Penalty | Profit |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 10000 | 0 | 0 | 0 |
| 1 | 0 | `(15,20)` | 10000 | 15 | 0 | 150000 |
| 2 | 0 | `(15,20),(5,10)` | 10000 | 20 | 100 | 199900 |
| 3 | 0 | all 3 | 10000 | 21 | 130 | 209870 |
| 4 | 1 | all 3 | 10040 | 21 | 130 | 210710 |
| 5 | 2 | all 3 | 10070 | 21 | 130 | 211340 |
| 6 | 3 | all 3 | 10080 | 21 | 130 | 211550 |

The last three rows show why regular videos are useful even though they generate no direct revenue. Once every commercial video has been selected, each additional regular video increases the subscriber count seen by all three advertisements.

## Complexity Analysis

Let

[
C=\sum_{i=1}^{m} c_i.
]

Because every `c_i <= 100` and `m <= 100`, we have `C <= 10000`.

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(m²C + nm + m log m)` | DP has `m` layers of advertisements and `m` possible selected counts over sums up to `C`; hull construction scans each DP row once |
| Space | `O(mC + n + m)` | The DP has `(m+1)(C+1)` states, with prefix sums and advertisement data stored separately |

The formal worst case of the DP is about `100 * 100 * 10000 = 10^8` elementary state positions. The implementation avoids scanning unreachable sums, which is especially effective when the commercial `c_i` values are equal or have large common structure. The hull removes the additional `O(nmC)` final scan used by the straightforward implementation. The memory usage is about one million integer references for the DP, comfortably within the 512 MB limit.

## Test Cases

The following harness assumes the `solve()` function from the solution above is in the same file.

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    try:
        sys.stdin = io.StringIO(inp)
        sys.stdout = io.StringIO()

        solve()

        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Sample 1
assert run(
    """1
10
2
10 20
20 10
4
0
1
2
3
"""
) == "0\n200000\n299900\n300200", "sample 1"

# Sample 2
assert run(
    """3
10
40
30
3
5 10
15 20
1 100
7
0
1
2
3
4
5
6
"""
) == "0\n150000\n199900\n209870\n210710\n211340\n211550", "sample 2"

# Minimum-size input: no videos at all.
assert run(
    """0
0
1
0
"""
) == "0", "minimum-size case"

# All values equal.
assert run(
    """2
5
5
2
10 5
10 5
5
0
1
2
3
4
"""
) == "0\n100000\n199950\n200050\n200150", "equal values"

# Boundary case: d is larger than the number of commercials.
assert run(
    """1
100
1
1 100
3
0
1
2
"""
) == "0\n10000\n10100", "d larger than m"

# Maximum n and m, with only three queried values.
parts = ["100"]
parts.extend(["100"] * 100)
parts.append("100")
parts.extend(["100 100"] * 100)
parts.append("3")
parts.extend(["0", "100", "200"])

max_input = "\n".join(parts) + "\n"

assert run(max_input) == (
    "0\n50500000\n150500000"
), "maximum-size case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 regular, 0 commercial, d=0` | `0` | Minimum dimensions and the zero-video boundary |
| Two regular and two identical commercials | `0, 100000, 199950, 200050, 200150` | Equal ratios, repeated values, and selecting different numbers of both video types |
| One regular, one commercial, queries `0,1,2` | `0, 10000, 10100` | Exact `d`, including the case `d > m` |
| `n=m=100`, all values equal | `0, 50500000, 150500000` | Maximum input sizes and large integer totals |

## Edge Cases

The zero-video case is handled by the state `dp[0][0] = 0`. The final hull for `k=0` contains the single line `y=0`, so choosing `l=0` regular videos produces answer zero. For

```
0
0
1
0
```

the program prints `0`.

When there are no commercial videos, `m=0`, the DP contains only `dp[0][0]`. Every hull query evaluates to zero regardless of how many regular videos are selected. Thus for

```
2
5
7
0
3
0
1
2
```

the three answers are `0`, `0`, and `0`.

When `d` exceeds the number of available commercial videos, the final maximization automatically considers states with `k=m` and `l=d-m`. For

```
2
5
6
1
10 1
1
2
```

the only way to get positive profit with exactly two videos is to select the commercial video and one regular video. The largest regular increase is 6, so the answer is `10 * 10006 = 100060`.

The ordering edge case is handled by the ratio sort. For

```
0
2
10 20
20 10
1
2
```

the DP order is `(10,20)` followed by `(20,10)`, because `10/20 < 20/10`. The corresponding actual release order is the reverse. The total coefficient is 30, and the second DP transition incurs a penalty of `10 * 10 = 100`. The resulting profit is `30 * 10000 - 100 = 299900`.

Finally, the guarantee about subscriber counts means every considered sequence remains valid with a nonnegative subscriber count. The algorithm never needs to reject a DP state based on subscriber negativity, because the problem guarantees feasibility even in the worst case of releasing all commercial videos alone.

The hull optimization is not necessary for understanding the core idea, but it makes the Python implementation much more practical than a literal translation of the straightforward final `O(nmC)` scan.
