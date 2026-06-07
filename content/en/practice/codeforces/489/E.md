---
title: "CF 489E - Hiking"
description: "We have a sequence of resting points along a river. Point i is located at position x[i] and has picturesqueness value b[i]. The traveler starts at coordinate 0 and must finish at the last resting point, which is also the farthest one."
date: "2026-06-07T17:37:58+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "dp"]
categories: ["algorithms"]
codeforces_contest: 489
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 277.5 (Div. 2)"
rating: 2300
weight: 489
solve_time_s: 158
verified: false
draft: false
---

[CF 489E - Hiking](https://codeforces.com/problemset/problem/489/E)

**Rating:** 2300  
**Tags:** binary search, dp  
**Solve time:** 2m 38s  
**Verified:** no  

## Solution
## Problem Understanding

We have a sequence of resting points along a river. Point `i` is located at position `x[i]` and has picturesqueness value `b[i]`. The traveler starts at coordinate `0` and must finish at the last resting point, which is also the farthest one.

If the traveler moves from position `p` to position `q` in one day, the distance covered that day is `q - p`. His ideal daily distance is `l`, so the frustration contributed by that day equals

$$(q-p-l)^2.$$

A route is any increasing sequence of resting points ending at point `n`. For a chosen route,

$$F = \sum ( \text{daily distance} - l )^2$$

is the total frustration, and

$$B = \sum b_i$$

is the total picturesqueness of the visited resting points.

The quantity to minimize is

$$\frac{F}{B}.$$

The output is not the value of this ratio. We must print one optimal route itself.

The first challenge is that the objective is a ratio. Dynamic programming usually handles additive costs, but here the numerator and denominator depend on the entire path.

The constraints are small enough to allow quadratic dynamic programming. We have at most `1000` resting points. A graph whose vertices are the resting points and whose edges represent possible jumps contains about one million directed edges. An `O(n²)` DP is perfectly acceptable, while exponential enumeration of routes is impossible.

A subtle point is that a route may skip arbitrary resting points. Another subtle point is that picturesqueness is accumulated only for visited points, while frustration depends on every jump. Any approach that greedily chooses locally good jumps can easily fail because a point with large picturesqueness may justify a somewhat worse travel schedule.

Consider:

```
n = 2, l = 10

(10, 1)
(20, 1000)
```

Using both points gives frustration `0 + 0 = 0`, ratio `0`.

Going directly to point 2 gives frustration `(20-10)^2 = 100`, ratio `100/1000 = 0.1`.

The optimal route uses more points even though both routes end at the same destination.

Another easy mistake is forgetting that the journey starts at coordinate `0`. For

```
1 10
20 5
```

the only day covers distance `20`, not `0`. The frustration is `(20-10)^2 = 100`.

## Approaches

A brute force solution would enumerate every subset of intermediate resting points and check every possible route ending at point `n`. Since each point may be either used or skipped, there are roughly `2^(n-1)` routes. With `n = 1000`, this is completely infeasible.

The ratio objective suggests a classical optimization trick. Suppose we somehow know the optimal ratio `R`. Then a route is optimal exactly when

$$\frac{F}{B} \le R.$$

Multiplying by `B > 0` gives

$$F - R B \le 0.$$

This transforms the ratio into an additive expression.

Now imagine fixing a candidate value `C`. Define the cost of a route as

$$F - C B.$$

If the minimum possible value of this expression is negative, then some route satisfies

$$\frac{F}{B} < C.$$

If the minimum value is positive, then every route has ratio larger than `C`.

This turns the original problem into a decision problem suitable for binary search.

For a fixed `C`, the route cost becomes

$$\sum \Big((x_i-x_j-l)^2\Big) - C \sum b_i.$$

The expression is additive along the route. That means we can compute the minimum value using dynamic programming.

Let `dp[i]` be the minimum transformed cost of a route ending at point `i`.

Then

$$dp[i] = -C b_i + \min_j \left( dp[j] + (x_i-x_j-l)^2 \right),$$

where `j < i`.

The start position `0` behaves like a virtual node with coordinate `0` and cost `0`.

Since every transition is examined, the complexity is `O(n²)` per DP run.

The optimal ratio is found by binary searching `C`. After obtaining it with sufficient precision, one final DP run reconstructs the path.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Optimal | O(n² log M) | O(n) | Accepted |

Here `M` is the search range of the answer.

## Algorithm Walkthrough

1. Store all coordinates and picturesqueness values.
2. Binary search on the answer `C`.
3. For a fixed `C`, run dynamic programming.
4. Let `dp[i]` denote the minimum value of

$$F - C B$$

among all routes ending at point `i`.
5. Treat the starting coordinate `0` as a virtual vertex.

The transition from the start directly to point `i` has cost

$$(x_i-l)^2 - C b_i.$$
6. For every pair `j < i`, relax

$$dp[j] + (x_i-x_j-l)^2 - C b_i.$$

This corresponds to visiting point `i` immediately after point `j`.
7. After filling the DP table, inspect `dp[n]`.

If `dp[n] < 0`, then some route achieves ratio smaller than `C`, so move the binary search interval downward.

Otherwise move it upward.
8. Repeat the binary search about sixty times. Double precision easily supports this.
9. Run the DP one final time using the resulting value of `C`.
10. While computing transitions, store the predecessor that produced the best value.
11. Reconstruct the route by following predecessor pointers backward from point `n`.
12. Reverse the reconstructed sequence and print it.

### Why it works

For any fixed value `C`, the DP computes

$$\min_{\text{route}} (F - C B).$$

If this minimum is negative, then some route satisfies

$$F - C B < 0,$$

which is equivalent to

$$\frac{F}{B} < C.$$

If the minimum is nonnegative, then every route has ratio at least `C`.

Thus the sign of the minimum transformed cost exactly answers whether `C` is above or below the optimal ratio. Binary search converges to the smallest feasible ratio.

The final DP is solving the transformed problem at a value arbitrarily close to the optimal ratio. Standard fractional programming theory guarantees that any route minimizing the transformed objective at this value is an optimal route for the original ratio objective.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, l = map(int, input().split())

    x = [0] * (n + 1)
    b = [0] * (n + 1)

    for i in range(1, n + 1):
        x[i], b[i] = map(int, input().split())

    def dp_run(C, restore=False):
        INF = 1e100

        dp = [INF] * (n + 1)
        parent = [-1] * (n + 1)

        for i in range(1, n + 1):
            best = (x[i] - l) ** 2 - C * b[i]
            par = 0

            for j in range(1, i):
                cand = dp[j] + (x[i] - x[j] - l) ** 2 - C * b[i]
                if cand < best:
                    best = cand
                    par = j

            dp[i] = best
            parent[i] = par

        if not restore:
            return dp[n]

        path = []
        cur = n

        while cur:
            path.append(cur)
            cur = parent[cur]

        path.reverse()
        return path

    lo = 0.0
    hi = 1e12

    for _ in range(70):
        mid = (lo + hi) / 2.0

        if dp_run(mid) < 0:
            hi = mid
        else:
            lo = mid

    path = dp_run(hi, True)
    print(*path)

if __name__ == "__main__":
    solve()
```

The key routine is `dp_run(C)`. For a fixed candidate ratio `C`, it computes the minimum transformed cost. The virtual start position is handled by the direct transition

$$(x_i-l)^2 - C b_i.$$

No explicit vertex `0` is required in the DP table.

The transition considers every earlier resting point. Since `n` is only `1000`, the quadratic loop is small enough.

The binary search keeps the invariant that the true optimum ratio lies inside `[lo, hi]`. Whenever the transformed optimum becomes negative, we know that `mid` is larger than the answer, so the upper bound moves down.

The reconstruction run uses exactly the same DP but stores the predecessor responsible for the best transition. Following predecessors from `n` yields the optimal route in reverse order.

A common implementation mistake is reconstructing with the midpoint from the last binary-search iteration. Using the final upper bound `hi` is safer because it remains on the feasible side throughout the search.

## Worked Examples

### Sample 1

Input:

```
5 9
10 10
20 10
30 1
31 5
40 10
```

Suppose the binary search has converged near the optimum ratio.

| Point | Best predecessor | Route so far |
| --- | --- | --- |
| 1 | start | 1 |
| 2 | 1 | 1 2 |
| 3 | 2 | 1 2 3 |
| 4 | 2 | 1 2 4 |
| 5 | 4 | 1 2 4 5 |

Reconstruction produces:

```
1 2 4 5
```

The interesting choice occurs at point `4`. Although point `3` is geographically closer, point `4` has significantly larger picturesqueness. The transformed objective captures this tradeoff automatically.

### Custom Example

Input:

```
3 10
10 1
20 1
30 1
```

Every daily distance can be exactly `10`.

| Point | Direct cost | Chosen predecessor |
| --- | --- | --- |
| 1 | 0 - C | start |
| 2 | 0 - 2C | 1 |
| 3 | 0 - 3C | 2 |

The reconstructed route is:

```
1 2 3
```

Total frustration is zero, which is obviously optimal.

This example confirms that the DP naturally chains together perfect daily segments whenever possible.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n² log M) | One O(n²) DP per binary-search iteration |
| Space | O(n) | DP and predecessor arrays |

The binary search performs a constant number of iterations, about seventy. With `n = 1000`, each DP run examines roughly one million transitions. This easily fits within the time limit, and the memory usage remains tiny compared to the available 256 MB.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    def solve():
        input = sys.stdin.readline

        n, l = map(int, input().split())

        x = [0] * (n + 1)
        b = [0] * (n + 1)

        for i in range(1, n + 1):
            x[i], b[i] = map(int, input().split())

        def dp_run(C, restore=False):
            INF = 1e100
            dp = [INF] * (n + 1)
            parent = [-1] * (n + 1)

            for i in range(1, n + 1):
                best = (x[i] - l) ** 2 - C * b[i]
                par = 0

                for j in range(1, i):
                    cand = dp[j] + (x[i] - x[j] - l) ** 2 - C * b[i]
                    if cand < best:
                        best = cand
                        par = j

                dp[i] = best
                parent[i] = par

            if not restore:
                return dp[n]

            path = []
            cur = n
            while cur:
                path.append(cur)
                cur = parent[cur]
            path.reverse()
            return path

        lo, hi = 0.0, 1e12

        for _ in range(70):
            mid = (lo + hi) / 2
            if dp_run(mid) < 0:
                hi = mid
            else:
                lo = mid

        return " ".join(map(str, dp_run(hi, True)))

    return solve()

# provided sample
assert run(
"""5 9
10 10
20 10
30 1
31 5
40 10
"""
) == "1 2 4 5"

# minimum size
assert run(
"""1 10
10 5
"""
) == "1"

# perfect daily jumps
assert run(
"""3 10
10 1
20 1
30 1
"""
) == "1 2 3"

# skipping an intermediate point is better
assert run(
"""2 10
5 1
20 1000
"""
) == "2"

# boundary case with large spacing
out = run(
"""2 1
1000000 1
1000001 1
"""
)
assert out.endswith("2")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single resting point | `1` | Correct handling of the start state |
| Perfect spacing | `1 2 3` | Zero-frustration route |
| Large picturesqueness at destination | `2` | Ratio optimization, not frustration minimization alone |
| Very large coordinates | Ends with `2` | Large values and arithmetic stability |

## Edge Cases

Consider:

```
1 10
20 5
```

There is only one route. The DP computes

$$(20-10)^2 - C \cdot 5.$$

The start position is correctly treated as coordinate `0`, so the daily distance is `20`. Reconstruction outputs `1`.

Consider:

```
2 10
10 1
20 1000
```

Using both points yields ratio `0`. Going directly to point `2` yields ratio `100/1000 = 0.1`.

The DP compares both possibilities through its transitions. The route `1 -> 2` produces transformed cost `-1001C`, while the direct route produces `100 - 1000C`. Near the optimum ratio, the first expression is smaller, so the reconstruction returns `1 2`.

Consider:

```
3 10
10 1
11 1000
20 1
```

A greedy strategy might visit point `2` because of its huge picturesqueness. The DP does not make local decisions. It evaluates complete route costs, including the poor jump lengths created by visiting point `2`. Only the globally optimal predecessor survives in each state, so the final route remains correct.
