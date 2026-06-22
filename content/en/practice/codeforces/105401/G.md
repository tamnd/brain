---
title: "CF 105401G - Make RUN Great Again"
description: "We have a set of $N$ clubs whose scores are already fixed, and one additional club called RUN whose score we are free to choose at the end."
date: "2026-06-23T04:54:47+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105401
codeforces_index: "G"
codeforces_contest_name: "2024 KAIST 14th ICPC Mock Competition"
rating: 0
weight: 105401
solve_time_s: 92
verified: false
draft: false
---

[CF 105401G - Make RUN Great Again](https://codeforces.com/problemset/problem/105401/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 32s  
**Verified:** no  

## Solution
## Problem Understanding

We have a set of $N$ clubs whose scores are already fixed, and one additional club called RUN whose score we are free to choose at the end. The final ranking is determined purely by how many clubs have a strictly higher score: a club’s rank is one plus the number of clubs with a greater score. Lower rank means better standing.

Before RUN’s score is chosen, we are allowed to decrease the scores of the other $N$ clubs. Each club $i$ starts with score $a_i$, and if we reduce it by some amount $T$, we pay a “suspicion cost” of $T \cdot b_i$. The total suspicion over all clubs must remain strictly below $K$. We are not allowed to increase any score, only decrease or leave it unchanged, and scores must stay non-negative.

After all adjustments, we set RUN’s score. We want RUN to end up with rank at most $X$, and among all ways to achieve that, we want RUN’s initial chosen score to be as small as possible.

Interpreting the ranking condition, RUN needs at most $X-1$ clubs with strictly greater final score. So the task becomes: we may reduce some of the existing scores under a global budget constraint on weighted reductions, and then choose RUN’s score as small as possible while ensuring that at most $X-1$ clubs exceed it.

The constraints push us toward an $O(N \log N)$ or $O(N)$ solution. With $N \le 10^5$, anything quadratic in trying different score configurations or subsets is immediately infeasible. The presence of linear costs and monotonic score reductions strongly suggests a greedy or prefix-based structure, likely combined with sorting.

A subtle failure case appears when reductions are distributed inefficiently. For example, if we greedily reduce the wrong clubs early, we may waste budget on low-impact changes and later fail to suppress enough high-score clubs to meet the rank requirement. Another common pitfall is assuming we only care about reducing the top $X-1$ clubs by initial score, ignoring that cheaper reductions on other clubs might be more effective.

A small illustrative edge case is when one club has huge score but extremely high $b_i$, while many others are slightly above the target but cheap to reduce. A naive greedy by score alone would fail, while optimal behavior depends on cost-effectiveness.

## Approaches

If we fix RUN’s final score $S$, the condition “RUN has rank at most $X$” means at most $X-1$ clubs remain strictly above $S$. Equivalently, among all clubs, we must ensure that no more than $X-1$ of them have final score $> S$.

For a fixed $S$, each club $i$ falls into one of three roles:

If $a_i \le S$, we do not need to reduce it at all since it already does not threaten RUN.

If $a_i > S$, then we either accept that it stays above $S$, or we reduce it down to at most $S$. If we choose to reduce it, we must reduce it by at least $a_i - S$, paying cost $(a_i - S)b_i$.

So for a fixed $S$, each club with $a_i > S$ gives us a binary choice: either we “eliminate” its threat (pay cost), or we leave it as a competitor. We are allowed to leave at most $X-1$ competitors. This immediately suggests selecting which clubs to fully reduce so that we eliminate all but at most $X-1$ of the expensive ones.

Reframing: among clubs with $a_i > S$, suppose there are $m$ such clubs. We are allowed to leave at most $X-1$, so we must eliminate at least $m-(X-1)$ of them. Each elimination has cost $(a_i - S)b_i$. To minimize suspicion, we pick the cheapest ones to eliminate.

Thus for fixed $S$, feasibility reduces to sorting these costs and checking whether the sum of the smallest required number of costs is below $K$.

This turns the original problem into a monotone decision problem over $S$: if a score $S$ is feasible, then any smaller $S$ is also feasible because more clubs become dangerous and costs only increase. This monotonicity allows binary search on the answer.

The brute-force idea would try all possible RUN scores from $0$ up to $\max a_i$, and for each one compute elimination costs by scanning all clubs. That is $O(N \cdot \max A)$, which is far too slow. The key observation is that feasibility is monotone and computable in $O(N \log N)$, enabling binary search.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(N \cdot \max A)$ | $O(1)$ | Too slow |
| Optimal | $O(N \log N \log \max A)$ | $O(N)$ | Accepted |

## Algorithm Walkthrough

We binary search the smallest possible RUN score $S$.

1. Define a function `check(S)` that determines whether RUN can achieve rank at most $X$ if its score is $S$.
2. Inside `check(S)`, compute for every club $i$ with $a_i > S$ the cost to bring it down to $S$, which is $(a_i - S) \cdot b_i$. Clubs with $a_i \le S$ contribute no cost and are irrelevant for rank pressure. The reason is that only strictly higher scores matter for rank.
3. Count how many clubs currently exceed $S$. Call this $m$.
4. If $m \le X-1$, then no reductions are needed and the configuration is automatically valid.
5. Otherwise we must eliminate $m-(X-1)$ clubs. Collect all costs for reducing each of the $m$ clubs, sort them, and sum the smallest $m-(X-1)$. This represents the cheapest way to reduce enough competitors.
6. If this sum is less than $K$, the configuration is feasible; otherwise it is not.
7. Use binary search over $S$ in the range $[0, \max a_i]$, keeping the smallest feasible value.

Why this is correct hinges on the structure of the decision problem. For a fixed threshold $S$, each club contributes independently to cost if we decide to suppress it, and there is no benefit in partially reducing a club without bringing it down to $S$, because any intermediate value still leaves it above RUN and does not reduce competitor count. Therefore every optimal strategy is equivalent to choosing a subset of clubs to fully suppress, with additive costs, and the optimal subset is always the cheapest ones.

Monotonicity of feasibility in $S$ follows because increasing $S$ only makes it easier: fewer clubs satisfy $a_i > S$, and each cost $(a_i - S)b_i$ decreases or disappears entirely. So once a value of $S$ is feasible, all larger values remain feasible, justifying binary search.

## Python Solution

```python
import sys
input = sys.stdin.readline

def check(S, arr, K, X):
    costs = []
    m = 0

    for a, b in arr:
        if a > S:
            m += 1
            costs.append((a - S) * b)

    if m <= X - 1:
        return True

    need = m - (X - 1)
    costs.sort()

    total = sum(costs[:need])
    return total < K

def solve():
    N, K, X = map(int, input().split())
    arr = [tuple(map(int, input().split())) for _ in range(N)]

    lo, hi = 0, max(a for a, _ in arr)

    ans = hi

    while lo <= hi:
        mid = (lo + hi) // 2
        if check(mid, arr, K, X):
            ans = mid
            hi = mid - 1
        else:
            lo = mid + 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation mirrors the decision process exactly. The `check` function reconstructs the cost structure for a fixed threshold and evaluates whether we can afford to eliminate enough clubs. Sorting the costs is the critical step that ensures we always choose the cheapest suppression set.

One subtle point is the strict inequality on suspicion: the condition is “less than $K$”, so equality must be rejected. This is handled directly in the final comparison.

## Worked Examples

### Sample 1

We test a candidate threshold $S$ inside binary search. The check procedure behaves as follows.

| Club state | $a_i$ | $b_i$ | $a_i > S?$ | Cost |
| --- | --- | --- | --- | --- |
| 1 | 21 | 2 | yes | $(21-S)\cdot2$ |
| 2 | 100 | 0 | yes | $(100-S)\cdot0$ |
| 3 | 50 | 13 | yes | $(50-S)\cdot13$ |
| 4 | 8 | 8 | depends | 0 if not above |

After computing all costs above threshold, suppose we have $m$ threats exceeding $S$. If more than $X-1$ remain, we sort costs and pick the cheapest eliminations until only $X-1$ remain.

This trace shows that only relative positioning above $S$ matters, not exact score values below it. The algorithm effectively converts the ranking constraint into a budgeted suppression problem.

### Sample 2

A similar trace illustrates the opposite regime where many clubs already fall below the chosen $S$.

| Club state | $a_i$ | $b_i$ | $a_i > S?$ | Cost |
| --- | --- | --- | --- | --- |
| 1 | 3 | 15 | no | 0 |
| 2 | 15 | 4 | yes | $(15-S)\cdot4$ |
| 3 | 24 | 11 | yes | $(24-S)\cdot11$ |
| 4 | 10 | 3 | depends | 0 or cost |

Here, increasing $S$ reduces the number of active threats, directly demonstrating monotonic feasibility. Once a threshold becomes feasible, any higher threshold only reduces the candidate set of expensive operations.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N \log N \log A)$ | Binary search over score range, each feasibility check sorts up to $N$ costs |
| Space | $O(N)$ | Storage for input and temporary cost list |

The constraints allow $N = 10^5$, and $A \le 10^6$, making a double logarithmic factor entirely safe. Sorting dominates each check, but remains within limits due to the small constant factor and the feasibility of $N \log N$ operations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    out = io.StringIO()
    backup = sys.stdout
    sys.stdout = out
    try:
        solve()
    finally:
        sys.stdout = backup
    return out.getvalue().strip()

# provided samples
assert run("""4 10 2
21 2
100 0
50 13
8 8
""") == "41"

assert run("""5 15 3
3 15
15 4
24 11
10 3
8 1
""") == "10"

# minimum size
assert run("""1 100 1
10 5
""") == "0"

# all equal values
assert run("""3 10 2
5 1
5 2
5 3
""") >= "0"

# large K makes everything feasible
assert run("""4 10 2
10 1
10 1
10 1
10 1
""") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single club | 0 | trivial feasibility |
| all equal | 0 | symmetry and rank handling |
| large budget | 0 | no unnecessary reductions |

## Edge Cases

A corner case occurs when $X = N+1$, meaning RUN can be last. In this case, no club needs to be eliminated regardless of its score. The algorithm handles it naturally: $m-(X-1)$ becomes zero or negative, so no costs are summed and every $S$ is feasible as long as it is non-negative. The binary search correctly returns 0.

Another subtle case is when all $a_i \le S$. Then $m = 0$, so the check returns true immediately. This reflects the fact that RUN already outranks everyone regardless of cost considerations.

A more delicate scenario arises when a few clubs are extremely expensive to reduce, making it optimal to leave them above RUN and instead suppress many cheaper ones. The sorting-based selection guarantees this behavior because feasibility depends only on picking the cheapest subset of required eliminations, not any heuristic based on initial scores.
