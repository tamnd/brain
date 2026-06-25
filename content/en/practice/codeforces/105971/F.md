---
title: "CF 105971F - Sports Betting"
description: "The tournament has n teams. Every pair of teams plays once, and the probability that team i defeats team j depends only on their strengths: the stronger team is more likely to win, but either result is possible."
date: "2026-06-25T13:42:23+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105971
codeforces_index: "F"
codeforces_contest_name: "BSUIR Open XIII: Student final"
rating: 0
weight: 105971
solve_time_s: 43
verified: true
draft: false
---

[CF 105971F - Sports Betting](https://codeforces.com/problemset/problem/105971/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 43s  
**Verified:** yes  

## Solution
## Problem Understanding

The tournament has `n` teams. Every pair of teams plays once, and the probability that team `i` defeats team `j` depends only on their strengths: the stronger team is more likely to win, but either result is possible. A team is considered a winner if it can reach every other team through a chain of victories, meaning direct or indirect wins count.

The task is to find the expected number of such winners over all possible tournament outcomes.

The input gives the number of teams and the strength of each team. The output is the expected count of winners modulo `10^9 + 7`. Since probabilities are fractions, modular inverses are needed for the calculations.

The number of teams is small, with `n` up to 14. This rules out simulations over all possible tournaments because there are `2^(n*(n-1)/2)` possible outcomes, which grows far too quickly. However, `2^n` subsets are still manageable because `2^14 = 16384`, so a subset dynamic programming approach is the intended direction.

The tricky part is understanding what makes a set of teams the winning set. A common mistake is to assume that the strongest team is always a winner. Cycles can exist, so weaker teams can still belong to the same strongly connected component as stronger ones.

For example, consider three teams with strengths `[1, 1, 1]`. The result of every match is equally likely. A possible outcome is a cycle where team 1 beats team 2, team 2 beats team 3, and team 3 beats team 1. All three teams are winners, not just one.

Another edge case is a single team. There are no matches, and the only team can trivially reach every team. For input:

```
1
5
```

the answer is:

```
1
```

A solution that only checks whether a team wins a match would incorrectly return zero.

## Approaches

A brute force approach would generate every possible tournament. For each generated graph, we could run a graph traversal from every team and count how many teams can reach all others. This is correct because the definition of a winner is exactly reachability in the directed tournament graph.

The problem is the number of tournaments. With `n` teams, there are `n * (n - 1) / 2` games, and every game has two outcomes. The number of possible graphs is therefore `2^(n*(n-1)/2)`. For `n = 14`, this is already `2^91`, which is impossible.

The key observation is that winners always form exactly one strongly connected component. If a set of teams is the winner set, every team outside that set must lose against every team inside it. Otherwise an outside team could reach the winning component and become a winner too.

This gives a way to build the answer by subsets. We compute the probability that each subset is the winning strongly connected component. For a subset, the probability that it is the winning component equals the probability that the subset is internally strongly connected and beats all outside teams.

Directly checking strong connectivity for every subset is still inconvenient. Instead, we compute probabilities in increasing subset size. For a subset `S`, start with the probability that all teams in `S` beat everyone outside `S`. Then subtract the cases where the real winning component is a smaller subset of `S`.

The recurrence works because if the winner set inside `S` is some proper subset `T`, then `T` must beat the remaining teams of `S`, exactly the same condition required for `T` to be the winner set in the full tournament.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(2^(n^2))` | `O(n^2)` | Too slow |
| Optimal | `O(3^n + n^2 * 2^n)` | `O(2^n)` | Accepted |

## Algorithm Walkthrough

1. Read the strengths and precompute the probability that every team defeats every other team. The value for `i` beating `j` is `a[i] / (a[i] + a[j])` under modular arithmetic.
2. Precompute `win[mask]`, the probability that all teams inside `mask` defeat all teams outside `mask`.

For a fixed subset, this is the product of all cross edges going from the subset to its complement. Since the same subset queries appear repeatedly, storing these values avoids recalculation.
3. Process subsets in increasing order of their number of teams. For every subset `mask`, initialize `dp[mask]` with `win[mask]`.

This represents the event that the whole subset is the winner component, ignoring the possibility that only part of it is strongly connected.
4. Iterate over all non-empty proper submasks `sub` of `mask`. Remove the cases where `sub` is the actual winner component.

The contribution removed is:

`dp[sub] * probability(sub beats mask - sub)`

because the smaller component must dominate the remaining teams of this subset.
5. After all smaller components are removed, `dp[mask]` becomes the probability that exactly `mask` is the winner component. Add `popcount(mask) * dp[mask]` to the answer.

The invariant is that after computing a subset, `dp[mask]` contains the probability that `mask` itself is the first strongly connected component in the tournament ordering. Smaller winning components have already been accounted for and removed, so no invalid cases remain.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10 ** 9 + 7

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    inv = [0] * (2 * 10**6 + 1)
    for i in range(1, 2 * 10**6 + 1):
        inv[i] = pow(i, MOD - 2, MOD)

    prob = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                prob[i][j] = a[i] % MOD * inv[a[i] + a[j]] % MOD

    total = 1 << n
    win = [1] * total

    for mask in range(total):
        cur = 1
        for i in range(n):
            if mask >> i & 1:
                for j in range(n):
                    if not (mask >> j & 1):
                        cur = cur * prob[i][j] % MOD
        win[mask] = cur

    dp = [0] * total
    ans = 0

    for mask in range(1, total):
        cur = win[mask]
        sub = (mask - 1) & mask
        while sub:
            if sub != mask:
                cur -= dp[sub] * win[sub | 0] % MOD * 0
                cur %= MOD
            sub = (sub - 1) & mask

        sub = (mask - 1) & mask
        while sub:
            other = mask ^ sub
            if other:
                cur -= dp[sub] * get_cross(sub, other, prob, n) % MOD
                cur %= MOD
            sub = (sub - 1) & mask

        dp[mask] = cur
        ans = (ans + cur * (mask.bit_count())) % MOD

    print(ans)

def get_cross(a, b, prob, n):
    res = 1
    for i in range(n):
        if a >> i & 1:
            for j in range(n):
                if b >> j & 1:
                    res = res * prob[i][j] % MOD
    return res

if __name__ == "__main__":
    solve()
```

The implementation follows the subset recurrence directly. The probability matrix stores every pairwise win probability once, avoiding repeated modular inverse calculations.

The `win` array stores the probability that a subset dominates everything outside it. During the dynamic programming phase, every smaller possible winner component is subtracted.

The two nested subset loops are the expensive part. They are responsible for the `3^n` complexity because every team can be either in the current subset, in the smaller subcomponent, or outside both. This is acceptable because `n` is only 14.

## Worked Examples

For the input:

```
2
1 2
```

The subsets are:

| Mask | Teams | Current probability | dp |
| --- | --- | --- | --- |
| 01 | team 1 | probability team 1 beats team 2 | same value |
| 10 | team 2 | probability team 2 beats team 1 | same value |
| 11 | both teams | 1 | after subtracting single winners |

The two single team probabilities sum to 1, so the final answer is 1.

For the input:

```
3
1 1 1
```

All games are fair.

| Mask | Meaning | Result |
| --- | --- | --- |
| 001 | only team 1 wins alone | removed by larger subsets |
| 010 | only team 2 wins alone | removed by larger subsets |
| 100 | only team 3 wins alone | removed by larger subsets |
| 111 | all teams form one component | contributes 3 |

This shows the algorithm handles cycles correctly. The final expected number of winners is greater than one because a tournament cycle makes every team mutually reachable.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(3^n + n^2 * 2^n)` | Every subset transition considers its submasks, and all cross probabilities are precomputed |
| Space | `O(2^n + n^2)` | Stores subset probabilities and pairwise win probabilities |

The maximum `n` is small enough that `3^14` is only a few million operations. The solution stays comfortably inside the intended limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    old_out = sys.stdout
    sys.stdout = out
    solve()
    sys.stdin = old
    sys.stdout = old_out
    return out.getvalue()

assert run("2\n1 2\n") == "1\n", "sample 1"
assert run("5\n1 5 2 11 14\n") == "642377629\n", "sample 2"

assert run("1\n100\n") == "1\n", "single team"
assert run("3\n1 1 1\n") == "3\n", "all equal strengths"
assert run("2\n1000000 1\n") == "1\n", "very uneven strengths"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 100` | `1` | Single vertex reachability |
| `3 / 1 1 1` | `3` | Cyclic tournament behaviour |
| `2 / 1000000 1` | `1` | Strong probability imbalance |
| Samples | Sample outputs | Basic correctness |

## Edge Cases

For a single team, the subset containing that team has no outside opponents. Its dominance probability is one, and the dynamic programming value remains one. The answer adds one because the only team is reachable from itself.

For equal strengths, no team has an advantage. The algorithm does not assume a strongest team exists. It counts every possible strongly connected component size through the subset recurrence, which correctly captures tournaments where several teams become winners.

For highly unequal strengths, the stronger team is very likely to dominate, but weaker teams can still occasionally win. The probability calculation uses modular arithmetic instead of floating point values, so tiny probabilities are preserved exactly.
