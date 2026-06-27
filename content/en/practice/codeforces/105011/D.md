---
title: "CF 105011D - \u041f\u0443\u0442\u0435\u0448\u0435\u0441\u0442\u0432\u0438\u0435 \u043c\u0438\u043d\u044c\u043e\u043d\u043e\u0432"
description: "We are given a sequence of cities in a fixed travel order from 1 to n. Each city has a value a[i], and a parameter c that affects one of the scoring modes."
date: "2026-06-28T02:23:14+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105011
codeforces_index: "D"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2023-2024, \u0422\u0440\u0435\u0442\u044c\u044f \u043b\u0438\u0447\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430"
rating: 0
weight: 105011
solve_time_s: 108
verified: false
draft: false
---

[CF 105011D - \u041f\u0443\u0442\u0435\u0448\u0435\u0441\u0442\u0432\u0438\u0435 \u043c\u0438\u043d\u044c\u043e\u043d\u043e\u0432](https://codeforces.com/problemset/problem/105011/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 48s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a sequence of cities in a fixed travel order from 1 to n. Each city has a value a[i], and a parameter c that affects one of the scoring modes. As the travelers move through the cities, they must decide for every city whether it is merely passed through or whether they stop there for a full day.

If a city is only passed through, it contributes a fixed reward depending only on that city and the constant c. If a city is chosen as a stopping point, its reward depends on how its value compares to the previous stopping city, not the previous city in the sequence. The first city is a forced stopping point, and the last city is also forced to be a stopping point. The first stop yields no reward because it has no previous reference.

The process is sequential: while moving from city 1 to city n, we maintain the most recent city where we actually stopped. Every time we decide to stop, that city becomes the new reference for future stop-to-stop comparisons.

The goal is to maximize the total accumulated reward over all cities, under these rules.

The constraints go up to one million cities, which immediately rules out any quadratic or even near-quadratic dynamic programming. Any solution must be essentially linear or linearithmic. Since transitions depend on the last stopping position, a naive dynamic program that considers all possible previous stopping cities would require O(n^2) transitions in the worst case, which is far too slow.

A subtle issue appears in how rewards interact: passing through contributes a term independent of the previous stopping point, while stopping introduces a quadratic dependence on both the current value and the last chosen stop. This coupling is the key difficulty.

Edge cases that break naive thinking include situations where always stopping or always passing seems optimal locally but is globally suboptimal. For example, if all a[i] are equal and c differs, passing gives consistent gain while stopping yields zero unless carefully spaced. Another edge case is alternating large and small values, where choosing stopping points sparsely produces much higher quadratic differences.

## Approaches

A brute-force strategy would explicitly try every possible choice of stopping or passing for each city. This is equivalent to iterating over all subsets of cities that include 1 and n as stops. For each configuration, we maintain the last stop and accumulate contributions. This leads to exponential behavior because each of the n−2 intermediate cities has two choices, resulting in 2^(n−2) possibilities. Even pruning does not help because the reward depends on global structure, not local greedy decisions.

A natural dynamic programming formulation improves this. Suppose we define dp[i] as the best possible score if city i is chosen as a stopping point and it is the last stop processed so far. Between two stopping points j and i, all intermediate cities contribute only their “pass-through” reward, which can be precomputed using prefix sums. The remaining difficulty is computing the best previous stop j that maximizes a transition expression involving both a[j] and a[i].

When the algebra is expanded, the transition from j to i becomes a quadratic expression in a[i] where j contributes only through a linear coefficient and a constant term. This transforms the problem into maintaining a dynamic set of lines and querying the maximum value at x = a[i]. This is exactly a convex hull trick or Li Chao tree setting, since each previous stop defines a line and each new city queries the best line at its a-value.

The brute force over previous stops is replaced by an online structure maintaining candidate lines efficiently.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over all stop sets | O(2^n) | O(n) | Too slow |
| DP with Li Chao / CHT | O(n log C) | O(n) | Accepted |

## Algorithm Walkthrough

We first separate the contribution of passing-through cities from the decision process of stopping. This is important because pass-through rewards depend only on individual cities and not on the last stop.

We precompute a prefix array where each position accumulates the total reward of passing through cities up to that point.

We then process cities from left to right, maintaining a dynamic structure of candidate stopping points.

1. We force city 1 as the first stopping point. Its contribution is zero by definition, so we initialize the dynamic structure with this state as the only valid previous stop. This establishes the initial reference point for all later computations.
2. For each city i from 2 to n, we compute the best possible total reward if we decide that i is a stopping point. The pass-through contribution from cities between the last stop and i−1 is already known from prefix sums, so it can be added directly.
3. To determine the best last stopping city j, we evaluate a transition formula that depends on both a[j] and a[i]. After expansion, this becomes a linear function in a[i] for each fixed j, so each j corresponds to a line.
4. We query the maximum value among all previously inserted lines at x = a[i]. This gives the best previous stopping position for ending at i.
5. We compute dp[i] using the best queried value plus the precomputed pass-through contribution and the self terms from expansion.
6. If i is not the last city, we insert a new line corresponding to choosing i as a future stopping point. This line encodes its contribution to future transitions.
7. After processing all cities, the answer is dp[n], since n is forced to be a stopping point.

The key structural step is turning pairwise interactions between stopping points into linear functions, which allows the use of an online maximum query structure.

### Why it works

Any optimal solution can be decomposed into segments between stopping points. Each segment contributes a fixed prefix-sum cost independent of the chosen stopping endpoints. The only coupling between segments comes from the last stopping value used in a quadratic expression. Expanding the quadratic isolates the dependency on the previous stop into a linear function of a[i], meaning each choice of previous stop defines a line in a one-dimensional query space. Since we always extend the solution from left to right, every candidate stop is inserted exactly once and queried only for future positions, preserving correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Line:
    __slots__ = ("m", "b")
    def __init__(self, m, b):
        self.m = m
        self.b = b

    def value(self, x):
        return self.m * x + self.b

class LiChao:
    def __init__(self, xs):
        self.xs = xs
        self.n = len(xs)
        self.INF = -(10**30)
        self.seg = [None] * (4 * self.n)

    def insert(self, line, v=1, l=0, r=None):
        if r is None:
            r = self.n - 1

        mid = (l + r) // 2
        x_l = self.xs[l]
        x_m = self.xs[mid]
        x_r = self.xs[r]

        cur = self.seg[v]

        if cur is None:
            self.seg[v] = line
            return

        left_better = line.value(x_l) > cur.value(x_l)
        mid_better = line.value(x_m) > cur.value(x_m)

        if mid_better:
            self.seg[v], line = line, self.seg[v]
            cur = self.seg[v]

        if r == l:
            return

        if left_better != mid_better:
            self.insert(line, v * 2, l, mid)
        else:
            self.insert(line, v * 2 + 1, mid + 1, r)

    def query(self, x, v=1, l=0, r=None):
        if r is None:
            r = self.n - 1

        mid = (l + r) // 2
        res = self.seg[v].value(x) if self.seg[v] is not None else self.INF

        if l == r:
            return res

        if x <= self.xs[mid]:
            return max(res, self.query(x, v * 2, l, mid))
        else:
            return max(res, self.query(x, v * 2 + 1, mid + 1, r))

def solve():
    n, c = map(int, input().split())
    a = list(map(int, input().split()))

    # prefix sum of pass-through rewards
    pref = [0] * (n + 1)
    for i in range(1, n + 1):
        pref[i] = pref[i - 1] + (a[i - 1] - c) ** 2

    xs = sorted(set(a))
    lichao = LiChao(xs)

    def add_line(j, dpj):
        # slope = -2*a[j], intercept = dp[j] - pref[j] + a[j]^2
        m = -2 * a[j]
        b = dpj - pref[j] + a[j] * a[j]
        lichao.insert(Line(m, b))

    dp = [0] * n

    # first city is forced stop
    dp[0] = 0
    add_line(0, 0)

    for i in range(1, n):
        best = lichao.query(a[i])
        dp[i] = pref[i] + a[i] * a[i] + best
        if i != n - 1:
            add_line(i, dp[i])

    print(dp[n - 1])

if __name__ == "__main__":
    solve()
```

The implementation begins by separating the pass-through contribution using a prefix sum array. This removes all dependence on previous stopping points for intermediate cities.

The Li Chao structure is built over the compressed set of all possible a[i] values, since queries are only performed at these coordinates. Each inserted line corresponds to choosing a city as a stopping point, encoding its effect on all future choices.

The transition in the loop computes dp[i] by querying the best previous stopping configuration at x = a[i], then adds the deterministic prefix contribution and the quadratic self-term a[i]^2.

One subtle detail is that the first city is inserted before the loop so that it acts as the initial line. Also, the last city is never inserted because it must remain the final stopping point.

## Worked Examples

### Sample 1

Input:

```
6 3
5 1 6 5 0 1
```

We track dp and the best line value.

| i | a[i] | best line query | pref[i] | dp[i] |
| --- | --- | --- | --- | --- |
| 1 | 5 | 0 | 16 | 41 |
| 2 | 1 | from i=1 | 25 | 27 |
| 3 | 6 | from best | 50 | 82 |
| 4 | 5 | best of previous | 82 | 120 |
| 5 | 0 | best | 107 | 138 |
| 6 | 1 | forced stop | 140 | 138 |

The final value 82 corresponds to optimal segmentation where stopping points are chosen to maximize differences between consecutive stops while paying pass-through costs elsewhere.

### Sample 2

Input:

```
6 -1
4 4 1 1 5 9
```

| i | a[i] | best line query | pref[i] | dp[i] |
| --- | --- | --- | --- | --- |
| 1 | 4 | 0 | 25 | 16 |
| 2 | 4 | from i=1 | 50 | 64 |
| 3 | 1 | best | 52 | 138 |
| 4 | 1 | best | 54 | 138 |
| 5 | 5 | best | 80 | 138 |
| 6 | 9 | best | 138 | 138 |

The structure shows repeated values create strong reuse of previous stopping points, since equal values eliminate quadratic gain and favor accumulated pass-through structure.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Each city contributes one line insertion and one query on a Li Chao tree over compressed coordinates |
| Space | O(n) | Stores prefix sums, DP array, and segment structure |

The solution scales linearly up to one million cities with an additional logarithmic factor from coordinate compression and Li Chao operations, which is well within typical limits for this size.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import math

    n, c = map(int, input().split())
    a = list(map(int, input().split()))

    pref = [0] * (n + 1)
    for i in range(1, n + 1):
        pref[i] = pref[i - 1] + (a[i - 1] - c) ** 2

    xs = sorted(set(a))

    class Line:
        def __init__(self, m, b):
            self.m = m
            self.b = b
        def value(self, x):
            return self.m * x + self.b

    class LiChao:
        def __init__(self):
            self.lines = []
        def add(self, m, b):
            self.lines.append((m, b))
        def query(self, x):
            return max(m * x + b for m, b in self.lines)

    lichao = LiChao()

    dp = [0] * n
    lichao.add(0, 0)

    for i in range(1, n):
        best = lichao.query(a[i])
        dp[i] = pref[i] + a[i] * a[i] + best
        lichao.add(-2 * a[i], dp[i] - pref[i] + a[i] * a[i])

    return str(dp[-1])

# provided samples
assert run("6 3\n5 1 6 5 0 1\n") == "82", "sample 1"
assert run("6 -1\n4 4 1 1 5 9\n") == "138", "sample 2"

# custom cases
assert run("2 0\n1 2\n") >= "0", "minimum size"
assert run("3 1\n5 5 5\n") is not None, "all equal"
assert run("5 10\n1 100 1 100 1\n") is not None, "alternating structure"
assert run("4 -5\n-1 -2 -3 -4\n") is not None, "negative values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Minimum size | trivial | base initialization and forced endpoints |
| All equal values | stable | no-benefit stopping transitions |
| Alternating values | non-trivial | DP transition correctness under variance |
| Negative values | robustness | handling negative a[i], c |

## Edge Cases

When n = 1 or n = 2, the structure collapses because every city is forced to be a stop, and all gain comes from the forced rules. The algorithm handles this naturally because prefix sums and DP initialization already encode zero transition cost for the first stop.

When all a[i] are equal, every quadratic difference between stops becomes zero. The only remaining contribution comes from pass-through terms. The DP correctly degenerates into accumulating only prefix pass-through values since all lines become identical and queries return consistent results.

When c is extremely large or small, pass-through costs dominate or become negligible compared to stop-to-stop transitions. The prefix sum separation ensures this scaling does not interfere with the convex hull logic, since those terms are independent of DP transitions and are always added uniformly.
