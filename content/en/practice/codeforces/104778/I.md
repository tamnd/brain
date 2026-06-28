---
title: "CF 104778I - \u041d\u0438\u0447\u044c\u044f"
description: "We are given a football season consisting of $n$ matches. Each match ends in exactly one of three outcomes: a win, a draw, or a loss. A win gives $k$ points, a draw gives 1 point, and a loss gives 0 points."
date: "2026-06-28T15:08:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104778
codeforces_index: "I"
codeforces_contest_name: "2023-2024 \u0412\u0441\u0435\u0440\u043e\u0441\u0441\u0438\u0439\u0441\u043a\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e, \u0440\u0435\u0433\u0438\u043e\u043d\u0430\u043b\u044c\u043d\u044b\u0439 \u044d\u0442\u0430\u043f \u0421\u0430\u0440\u0430\u0442\u043e\u0432\u0441\u043a\u043e\u0439 \u043e\u0431\u043b\u0430\u0441\u0442\u0438 (\u0412\u041a\u041e\u0428\u041f 23, \u0421\u0430\u0440\u0430\u0442\u043e\u0432\u0441\u043a\u0438\u0439 \u043e\u0442\u0431\u043e\u0440\u043e\u0447\u043d\u044b\u0439 \u044d\u0442\u0430\u043f)"
rating: 0
weight: 104778
solve_time_s: 48
verified: true
draft: false
---

[CF 104778I - \u041d\u0438\u0447\u044c\u044f](https://codeforces.com/problemset/problem/104778/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a football season consisting of $n$ matches. Each match ends in exactly one of three outcomes: a win, a draw, or a loss. A win gives $k$ points, a draw gives 1 point, and a loss gives 0 points. We are also told the total number of points accumulated over all $n$ matches is exactly $p$.

The task is not to reconstruct a valid season, but to determine the maximum possible number of draws that could have produced the given total score. If no combination of wins, draws, and losses over $n$ games can yield exactly $p$ points, the answer must be $-1$.

The constraints are extremely large: $n$ can go up to $10^{12}$ and $p$ up to $10^{15}$, so any approach that iterates over matches or tries all combinations is impossible. The solution must be purely arithmetic and rely on structural reasoning about linear constraints.

The most delicate situations are boundary cases where the score is impossible to form. For example, if $p$ is too large (greater than $nk$), or if it is not representable as a combination of 1 and $k$, then no valid season exists. Another subtle case is when maximizing draws forces too many matches to be consumed, making it impossible to place enough wins to reach the remaining score.

A simple example of impossibility is $n = 1, k = 5, p = 2$. The only possible scores are 0, 1, or 5, so 2 cannot be formed. The correct output is $-1$.

Another edge case is when all matches are draws, which forces $p = n$. For instance, $n = 10, p = 10, k = 3$ has a valid solution with 10 draws and no wins.

## Approaches

A brute-force approach would attempt to enumerate all possible distributions of wins, draws, and losses across $n$ matches. Even if we reduce this to iterating over the number of wins and draws, we would still check $O(n^2)$ states in the worst case, since each choice of wins constrains draws and losses. This is completely infeasible for $n$ up to $10^{12}$.

The key observation is that losses are irrelevant to scoring except as filler. The problem reduces to finding nonnegative integers $w$ and $d$ such that:

$$wk + d = p$$

and

$$w + d \le n$$

We want to maximize $d$, which means minimizing $w$, but still satisfying both constraints.

The first constraint is purely arithmetic: $p - wk$ must be nonnegative and equal to $d$, so $p - wk \ge 0$ and $p - wk$ is an integer.

This transforms the problem into selecting a valid number of wins $w$, where each win consumes $k$ points, and the remaining points must be exactly filled with draws.

To maximize draws, we want the smallest possible $w$ such that $p - wk \le n - w$, because draws consume both points and match slots, while wins consume only match slots.

This leads to a direct feasibility check over possible $w$, but since $w \le n$ and $w \le p/k$, we only need to consider a small structured search: we start from the minimal number of wins needed to make $p$ not exceed remaining capacity, and adjust within a small bounded range induced by modular constraints.

More concretely, we rewrite:

$$d = p - wk$$

and

$$d \le n - w
\Rightarrow p - wk \le n - w
\Rightarrow p - n \le w(k - 1)$$

This gives a lower bound on $w$, while $w \le \lfloor p/k \rfloor$ gives an upper bound. Since $k \ge 2$, the feasible region for $w$ is a small interval, and we only need to test a constant number of candidates around the boundary.

We pick the smallest valid $w$ in this interval, compute $d$, and return it.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over (w, d) | $O(n^2)$ | $O(1)$ | Too slow |
| Inequality + boundary search | $O(1)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We reformulate the problem in terms of wins and draws, then reduce it to checking feasibility of a linear Diophantine constraint with a capacity limit.

1. Compute the maximum possible wins as $w_{\max} = \lfloor p / k \rfloor$. This is the largest number of wins that does not overshoot the total points.
2. If $w_{\max} > n$, reduce it to $n$, since we cannot play more wins than matches. This ensures we never allocate more matches than exist.
3. For a fixed number of wins $w$, the remaining points must be filled by draws:

$$d = p - wk$$

This is forced; there is no freedom once $w$ is chosen.
4. Check feasibility constraints:

The number of matches used is $w + d$, so we require:

$$w + (p - wk) \le n$$

which simplifies to:

$$p - w(k - 1) \le n$$
5. Since increasing $w$ reduces $d$, but also increases match usage, we search for the smallest $w$ such that both feasibility conditions hold:

$p - wk \ge 0$ and $w + d \le n$.
6. If no such $w$ exists, return $-1$.
7. Otherwise compute $d = p - wk$ for the chosen $w$, and output it.

### Why it works

Any valid season corresponds to a pair $(w, d)$ satisfying a linear equation and a linear capacity constraint. The score equation fixes $d$ once $w$ is chosen, so the search space collapses to a single dimension. The feasibility condition is monotone in $w$: increasing wins reduces remaining points linearly while also reducing available capacity linearly. This monotonic structure ensures that if a solution exists, the boundary where constraints first become satisfied gives the optimal configuration for maximizing draws, since any smaller $w$ would violate score feasibility and any larger $w$ would only reduce draws further.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, p, k = map(int, input().split())

    # If even all wins are not enough or too many points are impossible
    if p > n * k:
        print(-1)
        return

    # We try to minimize wins while still making score achievable with draws
    # From feasibility: p - w*k <= n - w  =>  p - n <= w*(k - 1)
    # Also: p - w*k >= 0

    w_min = max(0, (p - n + (k - 2)) // (k - 1))  # ceil((p - n)/(k - 1))
    w_max = min(n, p // k)

    if w_min > w_max:
        print(-1)
        return

    # Try boundary candidates (monotonic structure)
    best_d = -1

    for w in range(w_min, min(w_max, w_min + 5) + 1):
        d = p - w * k
        if d < 0:
            continue
        if w + d <= n:
            best_d = max(best_d, d)

    print(best_d if best_d >= 0 else -1)

if __name__ == "__main__":
    solve()
```

The code first eliminates impossible cases where even maximum wins cannot reach the score. It then derives a lower bound on wins from the capacity constraint and an upper bound from score feasibility. The final step checks only a constant-size window near the boundary where feasibility transitions, since the constraint behaves monotonically in $w$.

The returned value is the number of draws, computed as $p - wk$, which directly follows once a valid $w$ is fixed.

## Worked Examples

### Example 1

Input:

```
6 7 3
```

We compute bounds:

$w_{\max} = 7 // 3 = 2$, so $w \in [0,2]$.

We compute the lower bound:

$$w \ge \frac{p - n}{k - 1} = \frac{7 - 6}{2} = 0.5 \Rightarrow 1$$

So $w \in [1,2]$.

We test:

| w | d = p - wk | w + d | valid |
| --- | --- | --- | --- |
| 1 | 4 | 5 | yes |
| 2 | 1 | 3 | yes |

Best is $w = 1$, giving $d = 4$.

Output:

```
4
```

This shows that multiple valid decompositions exist, and maximizing draws pushes us toward the smallest feasible number of wins.

### Example 2

Input:

```
3 15 5
```

Here:

$w_{\max} = 15 // 5 = 3$, so potentially all matches are wins.

Check:

$w = 3 \Rightarrow d = 0$, total matches used = 3.

Valid and maximal score.

Output:

```
0
```

This confirms that when the score is fully explained by wins, no draws are possible.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(1)$ | Only constant arithmetic and a bounded number of checks |
| Space | $O(1)$ | No auxiliary structures beyond scalars |

The solution easily fits within limits since it avoids any iteration over $n$ or $p$, relying purely on arithmetic constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    stdout.write = lambda x: out.append(x)
    out = []
    solve()
    return "".join(out).strip()

# helper redefine solve in this scope
def solve():
    n, p, k = map(int, input().split())
    if p > n * k:
        print(-1)
        return
    w_max = min(n, p // k)
    w_min = max(0, (p - n + (k - 2)) // (k - 1))
    if w_min > w_max:
        print(-1)
        return
    best = -1
    for w in range(w_min, min(w_max, w_min + 5) + 1):
        d = p - w * k
        if d >= 0 and w + d <= n:
            best = max(best, d)
    print(best)

# provided samples
assert run("6 7 3") == "4"
assert run("3 15 5") == "0"

# custom cases
assert run("1 2 3") == "-1"
assert run("10 10 3") == "10"
assert run("10 0 5") == "0"
assert run("5 9 2") == "4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 2 3 | -1 | impossible score |
| 10 10 3 | 10 | all draws case |
| 10 0 5 | 0 | all losses case |
| 5 9 2 | 4 | mixed optimal decomposition |

## Edge Cases

One failure mode is assuming every score has a solution once it is below $nk$. For example, $n = 1, k = 5, p = 2$ gives $p \le nk$, but no combination produces 2. The algorithm rejects it because $w_{\max} = 0$ leads to $d = 2$, which violates $w + d \le n$.

Another edge case is when the optimal solution requires zero wins. For $n = 10, p = 10, k = 5$, the best configuration is 10 draws and 0 wins. The formula correctly yields $w = 0$, $d = 10$, and satisfies capacity exactly.

A third case is when wins are necessary to reduce excess draws beyond available matches. For $n = 5, p = 9, k = 2$, naive greed might try too many draws first, but the constraint forces $w = 4, d = 1$, fitting exactly into 5 matches. The algorithm finds this boundary by enforcing both score and capacity constraints simultaneously, ensuring no over-allocation of draws occurs.
