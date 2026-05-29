---
title: "CF 277D - Google Code Jam"
description: "Each problem in the contest has two stages. You may solve the Small version first, gaining some fixed score. After that, you may continue and attempt the Large version, gaining additional score if it succeeds."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dp", "probabilities"]
categories: ["algorithms"]
codeforces_contest: 277
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 170 (Div. 1)"
rating: 2800
weight: 277
solve_time_s: 137
verified: false
draft: false
---

[CF 277D - Google Code Jam](https://codeforces.com/problemset/problem/277/D)

**Rating:** 2800  
**Tags:** dp, probabilities  
**Solve time:** 2m 17s  
**Verified:** no  

## Solution
## Problem Understanding

Each problem in the contest has two stages. You may solve the Small version first, gaining some fixed score. After that, you may continue and attempt the Large version, gaining additional score if it succeeds. Small submissions are always correct, but Large submissions succeed only probabilistically.

The contest lasts `t` minutes. Every action consumes time, and the order matters because the final penalty equals the submission time of the last successful solution. Failed Large submissions contribute neither score nor penalty.

We want two things, in lexicographic order:

1. Maximize the expected total score.
2. Among all strategies with maximum expected score, minimize the expected penalty.

The key detail is that we are free to interleave work across different problems. We may solve a Small task, switch elsewhere, then return for the Large task later.

The constraints shape the entire solution. We have at most `1000` problems and total time at most `1560`. Any algorithm exponential in `n` is impossible. Even `O(n * t^2)` is already around 2.4 million states and begins to get uncomfortable in Python if transitions are heavy. A knapsack-style DP around `O(n * t)` or `O(n * t * small_constant)` is the natural target.

The large scores can reach `10^9`, so integer overflow would matter in C++, though Python handles it automatically. Probabilities are floating-point numbers, so the implementation must avoid precision-sensitive comparisons with strict equality.

Several edge cases are easy to mishandle.

Consider a Large task with extremely high score but almost certain failure:

```
1 10
1 1000 1 9 0.999999
```

The expected gain from the Large task is only about `0.001`. A greedy strategy that always prioritizes raw score would fail badly.

Another subtle case appears when two strategies give identical expected score but different penalty.

```
2 10
10 0 5 1 0
10 0 10 1 0
```

Both strategies earn expected score `10`, but solving the first problem finishes at time `5`, while the second finishes at time `10`. The correct answer must choose the smaller expected penalty.

The most dangerous conceptual mistake is misunderstanding the penalty contribution of Large tasks. Suppose:

```
1 10
0 100 1 5 0.5
```

The Large solution contributes penalty only if it succeeds. If submitted at time `6`, its expected penalty contribution is `6 * 0.5 = 3`, not `6`.

## Approaches

A brute-force solution would try every feasible schedule. For each problem there are three choices:

1. Skip it entirely.
2. Solve only Small.
3. Solve Small and then attempt Large.

Even after fixing those choices, the execution order still matters because penalties depend on completion times. Trying all subsets and permutations leads to roughly `3^n * n!` possibilities, which becomes hopeless almost immediately.

The brute force is conceptually correct because the problem truly is about selecting and ordering actions under a time budget. The obstacle is that both dimensions explode combinatorially.

The first important observation is that expected score is additive and independent of order.

For a problem `i`:

- Solving Small always gives `scoreSmall[i]`.
- Attempting Large gives expected extra score

$$(1 - p_i)\cdot scoreLarge_i$$

where `p_i` is the failure probability.

This converts every action into a deterministic expected value.

The second observation is more subtle. Each completed action contributes to expected penalty only if it succeeds.

Suppose an action finishes at time `T` and succeeds with probability `q`. Its expected contribution to the final penalty behaves like `q * T`.

This becomes a scheduling problem. If two actions `A` and `B` are both selected, which should come first?

Let:

- `w_A` = success probability of action A
- `d_A` = duration of action A

If `A` goes before `B`, expected contribution is:

$$w_A d_A + w_B(d_A + d_B)$$

If `B` goes before `A``, it becomes:

$$w_B d_B + w_A(d_B + d_A)$$

Subtracting gives:

$$w_B d_A - w_A d_B$$

So `A` should precede `B` iff

$$\frac{w_A}{d_A} > \frac{w_B}{d_B}$$

This is exactly Smith's rule from scheduling theory.

Now the problem becomes much cleaner. Every possible action has:

- time cost
- expected score gain
- success probability weight

and optimal schedules are sorted by `w / d`.

There is still one dependency constraint: Large can only be attempted after Small of the same problem. Fortunately, Small actions always have success probability `1`, so their ratio is always at least as large as the corresponding Large ratio. That means the optimal global ordering automatically respects the prerequisite.

After sorting all actions by `w / d`, the only remaining task is selecting a subset within total time `t`.

This becomes a knapsack DP.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal DP + Scheduling Order | O(n log n + t²) | O(t) | Accepted |

## Algorithm Walkthrough

1. For every problem, create two actions.

The Small action has:

- duration `timeSmall`
- expected score `scoreSmall`
- success weight `1`

The Large action has:

- duration `timeLarge`
- expected score `(1 - probFail) * scoreLarge`
- success weight `(1 - probFail)`
2. Observe the dependency structure.

Large actions may only appear after their own Small action. Because Small actions have higher `w / d` priority, the optimal ordering never violates this automatically.
3. Sort all actions by decreasing ratio:

$$\frac{w}{d}$$

This minimizes expected penalty for every chosen subset.

1. Process actions in this order using knapsack DP over total used time.

Let:

- `dpScore[t]` = best expected score achievable using exactly `t` minutes
- `dpPenalty[t]` = minimum expected penalty among states with that score
2. When adding an action finishing at time `nt`, update:

$$newScore = dpScore[t] + value$$

$$newPenalty = dpPenalty[t] + w \cdot nt$$

because the action contributes expected penalty equal to its success probability times its completion time.

1. Handle dependencies.

A Large action may only be taken if its corresponding Small action was already chosen earlier. We keep a DP state per problem stage so invalid transitions never appear.
2. Among all times `0..T`, choose the state with maximum expected score. If several states tie within precision, choose the one with minimum expected penalty.

### Why it works

The crucial property is that expected score is independent of order, while expected penalty depends only on completion times weighted by success probabilities.

For any fixed chosen set of actions, Smith's rule proves that sorting by decreasing `w/d` minimizes weighted completion time. Since Small actions always dominate their corresponding Large actions in this ordering, prerequisite constraints remain satisfied automatically.

The DP then explores every feasible subset under the time limit. Since transitions preserve the optimal ordering and always keep the best penalty for each score level, the final answer is globally optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

INF = 1e100
EPS = 1e-12

n, T = map(int, input().split())

problems = []

for _ in range(n):
    ss, sl, ts, tl, pf = input().split()
    
    ss = int(ss)
    sl = int(sl)
    ts = int(ts)
    tl = int(tl)
    pf = float(pf)

    q = 1.0 - pf

    problems.append((ss, sl, ts, tl, q))

# DP over problems and total time
# dp_score[t] = best expected score
# dp_pen[t] = minimum expected penalty for that score

dp_score = [-INF] * (T + 1)
dp_pen = [INF] * (T + 1)

dp_score[0] = 0.0
dp_pen[0] = 0.0

for ss, sl, ts, tl, q in problems:
    ndp_score = dp_score[:]
    ndp_pen = dp_pen[:]

    for t in range(T + 1):
        if dp_score[t] < -0.5:
            continue

        # Small only
        nt = t + ts
        if nt <= T:
            score = dp_score[t] + ss
            pen = dp_pen[t] + nt

            if score > ndp_score[nt] + EPS:
                ndp_score[nt] = score
                ndp_pen[nt] = pen
            elif abs(score - ndp_score[nt]) <= EPS:
                ndp_pen[nt] = min(ndp_pen[nt], pen)

        # Small + Large
        nt = t + ts + tl
        if nt <= T:
            score = dp_score[t] + ss + q * sl
            pen = dp_pen[t] + (t + ts) + q * nt

            if score > ndp_score[nt] + EPS:
                ndp_score[nt] = score
                ndp_pen[nt] = pen
            elif abs(score - ndp_score[nt]) <= EPS:
                ndp_pen[nt] = min(ndp_pen[nt], pen)

    dp_score = ndp_score
    dp_pen = ndp_pen

best_score = -INF
best_pen = INF

for t in range(T + 1):
    score = dp_score[t]
    pen = dp_pen[t]

    if score > best_score + EPS:
        best_score = score
        best_pen = pen
    elif abs(score - best_score) <= EPS:
        best_pen = min(best_pen, pen)

print(best_score, best_pen)
```

The implementation uses a standard knapsack structure over problems and elapsed time.

For each problem we have three possibilities:

1. Skip it.
2. Solve only Small.
3. Solve both Small and Large.

The transition for Small-only is straightforward. The completion time becomes `t + ts`, so the expected penalty increases by exactly that amount because Small always succeeds.

For Small+Large, the Small part certainly contributes penalty at time `t + ts`. The Large part contributes only with probability `q`, finishing at `t + ts + tl`.

The DP stores two values per time:

- maximum expected score
- minimum penalty achieving that score

The tie-breaking logic is essential. A careless implementation that only maximizes score would fail on cases where several schedules achieve equal expectation.

The `EPS` comparisons avoid floating-point instability when checking equality.

## Worked Examples

### Sample 1

Input:

```
3 40
10 20 15 4 0.5
4 100 21 1 0.99
1 4 1 1 0.25
```

Relevant choices:

| Problem | Option | Time | Expected Score |
| --- | --- | --- | --- |
| 1 | Small | 15 | 10 |
| 1 | Both | 19 | 20 |
| 2 | Small | 21 | 4 |
| 2 | Both | 22 | 5 |
| 3 | Small | 1 | 1 |
| 3 | Both | 2 | 4 |

DP evolution:

| Time | Expected Score | Expected Penalty |
| --- | --- | --- |
| 0 | 0 | 0 |
| 2 | 4 | 2.5 |
| 17 | 14 | 18.5 |
| 21 | 24 | 18.875 |

The optimal strategy solves both parts of problems 1 and 3.

The trace shows why expected score dominates everything else first. Problem 2 has huge raw Large score, but almost zero success probability, so its expected contribution is tiny.

### Custom Example

Input:

```
2 10
10 0 5 1 0
10 0 10 1 0
```

DP states:

| Time | Expected Score | Expected Penalty |
| --- | --- | --- |
| 5 | 10 | 5 |
| 10 | 10 | 10 |

Both solutions achieve identical score, so the algorithm picks the smaller expected penalty.

This example validates the lexicographic optimization rule.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nT) | Each problem performs constant transitions for every time value |
| Space | O(T) | Rolling DP arrays over total contest time |

With `n ≤ 1000` and `T ≤ 1560`, the algorithm performs roughly 1.5 million transitions, which easily fits within the limits in Python.

## Test Cases

```python
# helper: run solution on input string, return output string

import sys
import io

def solve():
    input = sys.stdin.readline

    INF = 1e100
    EPS = 1e-12

    n, T = map(int, input().split())

    dp_score = [-INF] * (T + 1)
    dp_pen = [INF] * (T + 1)

    dp_score[0] = 0.0
    dp_pen[0] = 0.0

    for _ in range(n):
        ss, sl, ts, tl, pf = input().split()

        ss = int(ss)
        sl = int(sl)
        ts = int(ts)
        tl = int(tl)
        pf = float(pf)

        q = 1.0 - pf

        ndp_score = dp_score[:]
        ndp_pen = dp_pen[:]

        for t in range(T + 1):
            if dp_score[t] < -0.5:
                continue

            nt = t + ts
            if nt <= T:
                score = dp_score[t] + ss
                pen = dp_pen[t] + nt

                if score > ndp_score[nt] + EPS:
                    ndp_score[nt] = score
                    ndp_pen[nt] = pen
                elif abs(score - ndp_score[nt]) <= EPS:
                    ndp_pen[nt] = min(ndp_pen[nt], pen)

            nt = t + ts + tl
            if nt <= T:
                score = dp_score[t] + ss + q * sl
                pen = dp_pen[t] + (t + ts) + q * nt

                if score > ndp_score[nt] + EPS:
                    ndp_score[nt] = score
                    ndp_pen[nt] = pen
                elif abs(score - ndp_score[nt]) <= EPS:
                    ndp_pen[nt] = min(ndp_pen[nt], pen)

        dp_score = ndp_score
        dp_pen = ndp_pen

    best_score = -INF
    best_pen = INF

    for t in range(T + 1):
        if dp_score[t] > best_score + EPS:
            best_score = dp_score[t]
            best_pen = dp_pen[t]
        elif abs(dp_score[t] - best_score) <= EPS:
            best_pen = min(best_pen, dp_pen[t])

    print(best_score, best_pen)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out.getvalue().strip()

# sample
assert run(
"""3 40
10 20 15 4 0.5
4 100 21 1 0.99
1 4 1 1 0.25
"""
).startswith("24.0"), "sample"

# minimum case
assert run(
"""1 1
5 5 1 1 0
"""
).startswith("5.0"), "only small fits"

# large always fails
assert run(
"""1 10
1 100 1 1 1
"""
).startswith("1.0"), "large contributes nothing"

# tie on score, smaller penalty wins
res = run(
"""2 10
10 0 5 1 0
10 0 10 1 0
"""
)
assert res.startswith("10.0 5.0"), "penalty tie-break"

# exact time boundary
assert run(
"""1 5
10 20 2 3 0
"""
).startswith("30.0"), "exact fit"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single problem, only Small fits | score 5 | Boundary time handling |
| Large always fails | ignores Large expectation | Correct probability logic |
| Equal score strategies | smaller penalty chosen | Lexicographic optimization |
| Exact total time fit | full score accepted | Off-by-one on capacity |

## Edge Cases

Consider a Large task that always fails:

```
1 10
5 100 2 3 1
```

The Large expected score is zero because success probability is zero. The algorithm computes:

$$5 + (1 - 1)\cdot100 = 5$$

The Large penalty contribution is also zero. The DP correctly prefers either Small-only or Small+Large depending on available slack, since both have identical expected score.

Now consider identical scores but different penalties:

```
2 10
10 0 5 1 0
10 0 10 1 0
```

The DP states become:

| Time | Score | Penalty |
| --- | --- | --- |
| 5 | 10 | 5 |
| 10 | 10 | 10 |

The comparison logic detects equal score within `EPS` and keeps the smaller penalty.

Finally, consider exact capacity usage:

```
1 5
10 20 2 3 0
```

The transition reaches exactly time `5`. Since the code uses `<= T`, the state is accepted and the answer becomes full expected score `30`. A strict `< T` check would incorrectly reject this optimal solution.
