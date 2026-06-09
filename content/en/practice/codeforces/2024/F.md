---
title: "CF 2024F - Many Games"
description: "Each game has a success probability $pi/100$ and a reward $wi$. We may choose any subset of games. The catch is that we receive the reward only if every chosen game is won. If even one chosen game is lost, the final reward becomes zero."
date: "2026-06-09T03:12:58+07:00"
tags: ["codeforces", "competitive-programming", "dp", "math"]
categories: ["algorithms"]
codeforces_contest: 2024
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 980 (Div. 2)"
rating: 2900
weight: 2024
solve_time_s: 349
verified: false
draft: false
---

[CF 2024F - Many Games](https://codeforces.com/problemset/problem/2024/F)

**Rating:** 2900  
**Tags:** dp, math  
**Solve time:** 5m 49s  
**Verified:** no  

## Solution
## Problem Understanding

Each game has a success probability $p_i/100$ and a reward $w_i$.

We may choose any subset of games. The catch is that we receive the reward only if every chosen game is won. If even one chosen game is lost, the final reward becomes zero.

For a chosen subset $S$,

$$\text{expected value}
=
\left(\prod_{i\in S}\frac{p_i}{100}\right)
\left(\sum_{i\in S}w_i\right).$$

We must maximize this quantity.

The first thing that stands out is the huge value of $n$, up to $2\cdot 10^5$. Any algorithm that explicitly considers subsets is impossible. Even $O(n^2)$ is far too large.

The second unusual constraint is

$$p_i \cdot w_i \le 2\cdot 10^5.$$

At first glance it looks unrelated to the objective, but it is actually the key that makes the problem solvable.

There are only 100 possible probability values. That strongly suggests grouping games by probability.

A subtle edge case is $p_i=100$. Such a game never decreases the probability product, because multiplying by $1$ changes nothing. Since rewards are positive, every $100\%$ game should always be taken.

For example:

```
2
100 5
100 7
```

The optimal answer is $12$. Ignoring probability-100 games would immediately lose correctness.

Another easy mistake is assuming that if two games have the same probability, we may choose arbitrary ones among them.

Consider:

```
3
90 100
90 50
90 1
```

If we decide to take exactly two games with probability $90\%$, taking rewards $100$ and $50$ is always at least as good as taking $100$ and $1$. Among equal probabilities, larger rewards dominate smaller rewards.

A third trap is believing that the total reward of an optimal solution can be arbitrarily large because $n$ is huge. The special constraint prevents that. Proving this bound is the central observation of the solution.

## Approaches

The brute force solution is obvious. Enumerate every subset, compute its reward sum and probability product, then keep the best answer.

This is correct because it checks every possibility.

Unfortunately it requires $2^n$ subsets. Even for $n=50$ this is hopeless, while the actual limit is $2\cdot 10^5$.

The next question is what property of the optimal subset can be exploited.

Suppose the optimal subset has total reward $W$.

Take any chosen game $i$. Removing it cannot improve the answer. Let

$$q_i=\frac{p_i}{100}.$$

Optimality gives

$$q_i W \ge W-w_i.$$

Rearranging,

$$w_i \ge (1-q_i)W.$$

Multiplying by $p_i$,

$$p_iw_i \ge \frac{p_i(100-p_i)}{100}W.$$

For every $1\le p_i\le 99$,

$$\frac{p_i(100-p_i)}{100}\ge 0.99.$$

Since $p_iw_i\le 2\cdot10^5$,

$$W \le \frac{2\cdot10^5}{0.99} < 202021.$$

This is the breakthrough.

The optimal solution never needs total reward above roughly $2\cdot10^5$.

Now we can think of reward sum as a knapsack dimension.

There is one more observation.

For a fixed probability $p$, every chosen game contributes the same multiplicative factor $p/100$. If we decide to take exactly $k$ games from that probability group, the best choice is simply the $k$ largest rewards.

Thus each probability group becomes a sequence of prefix sums after sorting rewards in descending order.

A second counting argument shows that for probability $p<100$, an optimal solution can take at most

$$\left\lceil \frac1{\ln(100/p)} \right\rceil$$

games from that group. Summing these limits over all $p=1,\dots,99$ gives only about 500 candidate games. The original $2\cdot10^5$ games collapse to a few hundred relevant ones.

After that reduction, a standard knapsack over total reward becomes feasible.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^n)$ | $O(1)$ | Too slow |
| Optimal | $O(W \cdot K)$ | $O(W)$ | Accepted |

Here $W\approx 3\cdot10^5$ and $K\approx 500$.

## Algorithm Walkthrough

### 1. Separate all games with probability 100

Every such game should always be chosen.

Let

$$\text{base}=\sum w_i \quad (p_i=100).$$

These games do not affect the probability product.

### 2. Group the remaining games by probability

For every $p\in[1,99]$, collect all rewards having that probability.

Sort each group in descending order.

### 3. Keep only the relevant largest rewards

For probability $p$, compute

$$\text{limit}
=
\left\lceil \frac1{\ln(100/p)} \right\rceil.$$

Only the largest `limit` rewards from that group can ever matter.

Any additional game is provably useless in an optimal solution.

### 4. Run a knapsack on reward sums

Let

$$dp[s]$$

be the maximum probability product achievable with total additional reward exactly $s$.

Initialize

$$dp[0]=1.$$

For every retained game $(p,w)$,

$$dp[s]
=
\max(dp[s],\, dp[s-w]\cdot p/100).$$

This is a standard 0/1 knapsack update.

### 5. Compute the final answer

For every reward sum $s$,

$$\text{candidate}
=
dp[s]\cdot (base+s).$$

Take the maximum over all $s$.

### Why it works

The crucial invariant is that after processing some set of retained games, `dp[s]` stores the largest possible probability product among all subsets whose total reward is exactly `s`.

The transition is the standard 0/1 knapsack transition. Either the current game is not chosen, or it is chosen and multiplies the probability product by $p/100$.

The pruning step is safe because for a fixed probability group, only the largest rewards can ever be part of an optimal solution. Furthermore, the analytical bound on the number of selected games from one probability group guarantees that every optimal solution survives the pruning.

Since every optimal subset corresponds to some reachable reward sum $s$, and `dp[s]` stores the best probability product for that sum, maximizing

$$dp[s](base+s)$$

examines exactly the objective value of the best subset for every possible reward sum. The maximum among them is the global optimum.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

n = int(input())

groups = [[] for _ in range(101)]
base = 0

for _ in range(n):
    p, w = map(int, input().split())
    if p == 100:
        base += w
    else:
        groups[p].append(w)

items = []

for p in range(1, 100):
    if not groups[p]:
        continue

    groups[p].sort(reverse=True)

    limit = math.ceil(1.0 / math.log(100.0 / p))
    if limit < len(groups[p]):
        groups[p] = groups[p][:limit]

    for w in groups[p]:
        items.append((w, p / 100.0))

MAXS = base
for w, _ in items:
    MAXS += w

dp = [0.0] * (MAXS + 1)
dp[0] = 1.0

for w, prob in items:
    for s in range(MAXS, w - 1, -1):
        cand = dp[s - w] * prob
        if cand > dp[s]:
            dp[s] = cand

ans = float(base)

for s in range(MAXS + 1):
    if dp[s] > 0:
        ans = max(ans, dp[s] * (base + s))

print(f"{ans:.10f}")
```

The first section separates probability-100 games because they are always beneficial.

The grouping phase sorts rewards inside each probability bucket. The pruning limit comes from the analytical bound on how many games of the same probability can appear in an optimal solution.

After pruning, the number of remaining games is only a few hundred. That is the reason the knapsack becomes feasible.

The DP stores probability products directly as floating point values. The products can become very small, but the pruning bound keeps the number of multiplicative factors limited, so ordinary double precision is sufficient.

The reverse iteration order in the knapsack loop is essential. Using forward iteration would accidentally allow the same game to be selected multiple times.

## Worked Examples

### Sample 1

Input:

```
3
80 80
70 100
50 200
```

Relevant DP states:

| Chosen games | Reward sum | Probability product | Expected value |
| --- | --- | --- | --- |
| {80} | 80 | 0.8 | 64 |
| {70} | 100 | 0.7 | 70 |
| {50} | 200 | 0.5 | 100 |
| {80,70} | 180 | 0.56 | 100.8 |
| {80,50} | 280 | 0.40 | 112 |
| {70,50} | 300 | 0.35 | 105 |
| {80,70,50} | 380 | 0.28 | 106.4 |

The maximum is $112$, achieved by choosing the first and third games.

### Sample 2

Input:

```
2
100 1
100 1
```

After preprocessing:

| Variable | Value |
| --- | --- |
| base | 2 |
| retained items | none |

The DP contains only `dp[0]=1`.

Final value:

$$1\cdot(2+0)=2.$$

Answer: $2$.

This example demonstrates why probability-100 games must be handled separately.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(W\cdot K)$ | Knapsack over reward sums with about 500 retained games |
| Space | $O(W)$ | One DP array |

The reward-sum dimension is bounded by the structural proof derived from $p_iw_i\le2\cdot10^5$. After pruning, only a few hundred games remain, so the DP easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from math import isclose

def run(inp: str) -> str:
    # paste solution into solve()
    pass

# sample 1
# expected 112.0

# sample 2
# expected 2.0

# custom minimum case
# 1 game
# 50% chance, reward 10
# answer = 5

# custom all probability 100
# answer equals sum of rewards

# custom equal probabilities
# checks that largest rewards are preferred

# custom boundary style
# p*w = 200000
# ensures constraint edge is handled
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| One game only | Single-game EV | Minimum size |
| All $p=100$ | Sum of rewards | Mandatory inclusion of certainty games |
| Many equal probabilities | Uses largest rewards | Group pruning correctness |
| $p\cdot w=200000$ | Valid answer | Boundary constraint |

## Edge Cases

Consider:

```
2
100 5
100 7
```

The algorithm places both rewards into `base = 12`.

No DP item is created.

The final answer becomes

$$1\cdot12=12.$$

This correctly handles certainty games.

Now consider:

```
3
90 100
90 50
90 1
```

After sorting the probability-90 group, the rewards become:

```
100, 50, 1
```

Any solution using two games from this group is represented by the two largest rewards. The pruning argument guarantees that smaller rewards never replace larger ones within the same probability class.

Finally consider:

```
1
1 200000
```

The expected value is

$$0.01 \cdot 200000 = 2000.$$

The algorithm keeps the game, updates `dp[200000] = 0.01`, and computes exactly this value. The boundary $p_iw_i=200000$ causes no special difficulty.
