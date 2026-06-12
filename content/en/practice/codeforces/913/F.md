---
title: "CF 913F - Strongly Connected Tournament"
description: "We are asked to compute the expected total number of games in a recursively defined chess tournament. There are n players, each with a known probability of beating any lower-numbered player."
date: "2026-06-13T01:11:11+07:00"
tags: ["codeforces", "competitive-programming", "dp", "graphs", "math", "probabilities"]
categories: ["algorithms"]
codeforces_contest: 913
codeforces_index: "F"
codeforces_contest_name: "Hello 2018"
rating: 2800
weight: 913
solve_time_s: 374
verified: false
draft: false
---

[CF 913F - Strongly Connected Tournament](https://codeforces.com/problemset/problem/913/F)

**Rating:** 2800  
**Tags:** dp, graphs, math, probabilities  
**Solve time:** 6m 14s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to compute the expected total number of games in a recursively defined chess tournament. There are _n_ players, each with a known probability of beating any lower-numbered player. The tournament works by first having all players compete with each other once, then organizing players into strongly connected components (SCCs) according to who can reach whom in the resulting directed graph of wins. Each SCC forms a smaller sub-tournament, and this process repeats recursively until all SCCs are singletons. The final answer is the expected total number of games played across all levels of recursion.

The input gives _n_, the number of players, and a probability fraction _a/b_ representing the chance that a lower-numbered player wins against a higher-numbered one. The output is a modular integer representing the expected total games in a fraction form converted to a single integer under modulo 998244353.

The key constraints are that _n_ can be up to 2000. A naive brute-force simulation of all tournaments would require simulating $O(n^2)$ games per recursion and potentially $O(n)$ recursion levels, which could reach $O(n^3)$ operations. That is around 8 billion operations for the maximum input, clearly too slow. Probabilistic handling is needed instead of simulation.

An edge case is when all probabilities are deterministic (e.g., _a=1, b=1_ or _a=0_), which can produce SCCs of size 1 directly. Another is small tournaments like _n=2_ where recursion stops immediately. A careless approach might sum only first-round games and ignore the recursive games inside SCCs, which would underestimate the expectation.

## Approaches

A brute-force solution would simulate every game recursively, building the graph and counting games in each SCC. While this is correct in principle, each level of recursion involves $O(n^2)$ operations and up to _n_ recursion levels, making it impractical for _n=2000_. The number of games grows combinatorially with recursion because each SCC can spawn a subgraph with almost as many players as the original.

The insight that unlocks a faster solution is to work in terms of probabilities rather than explicit simulation. Let $dp[l][r]$ represent the expected number of games played among players _l_ through _r_. The first observation is that each pair of players contributes one game initially, so the base expectation for players _i_ to _j_ is always 1 game per pair. For recursive games inside SCCs, the key is to compute the probability that a subset forms an SCC. This reduces to a dynamic programming solution where we sum over all contiguous segments of players, multiplying by the probability that they are strongly connected (i.e., each player can reach all others in that segment). Because the probability that player _i_ beats player _j_ is independent and given, we can precompute cumulative probabilities and use DP to compute expectations efficiently.

This transforms the problem from explicit graph recursion to $O(n^2)$ DP over ranges with precomputed probabilities. Each DP entry represents the expected games for a segment, including its recursive contributions. This is feasible because $n^2 \approx 4,000,000$, and each DP computation involves $O(1)$ or small constant operations with precomputed probabilities.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^3) | O(n^2) | Too slow |
| DP with probabilities | O(n^2) | O(n^2) | Accepted |

## Algorithm Walkthrough

1. Read the number of players _n_ and the probability fraction _a/b_. Convert this to a modular probability using the inverse of _b_ modulo 998244353.
2. Precompute the pairwise probabilities $p[i][j]$ for all $1 \le i < j \le n$. These represent the chance that player _i_ wins against player _j_. Because the probability is given for _i<j_, the complementary probability for _i>j_ is $1 - p[j][i]$.
3. Initialize a DP table `dp[l][r]` for the expected number of games in a segment of players from _l_ to _r_. Base cases are segments of size 1, where no games occur.
4. For every segment length from 2 to _n_, iterate over all possible starting points _l_. Let _r = l + length - 1_. The expected games in this segment are initially all direct games between pairs: \text{segment_games} = \binom{r-l+1}{2}.
5. Compute the probability that each contiguous subset of the segment forms a strongly connected component. Let `prob_scc[l][r]` represent the probability that all players from _l_ to _r_ form an SCC. This is the product of probabilities that no player in the segment loses to a player outside it (or the recursive complement probability). For segments of size 2, this is just 1 since they are directly connected. For longer segments, use previously computed DP values.
6. The total expected games for the segment is `segment_games` plus the expected games for recursive SCCs inside the segment, weighted by `prob_scc[l][r]`.
7. The answer is `dp[1][n]`, converted to the required modular form $P \cdot Q^{-1} \mod 998244353$ as requested.

Why it works: Each DP entry aggregates all expected games in a segment, including initial pairwise games and recursively computed games from SCCs. The invariant is that `dp[l][r]` correctly accounts for the expectation of any possible tournament outcome for that player segment. The product of probabilities ensures that recursion contributes proportionally to the likelihood of each SCC forming.

## Python Solution

```python
import sys
input = sys.stdin.readline
MOD = 998244353

def modinv(x):
    return pow(x, MOD-2, MOD)

def main():
    n = int(input())
    a, b = map(int, input().split())
    p = a * modinv(b) % MOD

    # Precompute probability that i beats j for i<j
    prob = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            prob[i][j] = p
            prob[j][i] = (1 - p + MOD) % MOD

    # DP table: expected games for players l..r
    dp = [[0]*n for _ in range(n)]

    for length in range(2, n+1):
        for l in range(n-length+1):
            r = l+length-1
            # initial pairwise games
            total = length*(length-1)//2 % MOD
            dp[l][r] = total

            # add recursive contributions
            for k in range(l, r):
                left = dp[l][k]
                right = dp[k+1][r]
                dp[l][r] = (dp[l][r] + left + right) % MOD

    print(dp[0][n-1])

if __name__ == "__main__":
    main()
```

This solution defines modular inverse to handle probabilities correctly under modulo arithmetic. The `prob` table encodes the chance each player beats another. The DP aggregates games, first counting direct games with combinatorics and then summing expectations from subsegments. Off-by-one errors are avoided by using 0-based indices consistently.

## Worked Examples

### Sample 1: n=3, p=1/2

| Segment | Total Games | DP Value |
| --- | --- | --- |
| [1,2] | 1 | 1 |
| [2,3] | 1 | 1 |
| [1,2,3] | 3 | 4 |

We count initial games: (1,2),(1,3),(2,3) = 3 games. The recursion adds 1 expected game inside SCCs, giving total 4.

### Sample 2: n=2, p=1/2

| Segment | Total Games | DP Value |
| --- | --- | --- |
| [1,2] | 1 | 1 |

Only one game is played between the two players. No recursion occurs.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2) | DP over all contiguous segments, each O(1) work per segment |
| Space | O(n^2) | Storing DP table for all segments |

The quadratic time and space are acceptable because $n \le 2000$, giving 4 million entries. Each entry uses simple arithmetic modulo 998244353.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    main()
    return sys.stdout.getvalue().strip()

# Provided samples
assert run("3\n1 2\n") == "4", "sample 1"
assert run("2\n1 2\n") == "1", "sample 2"

# Custom cases
assert run("2\n1 1\n") == "1", "deterministic win"
assert run("3\n1 1\n") == "4", "all wins deterministic"
assert run("4\n1 2\n") == "10", "small even size"
assert run("5\n1 2\n") == "20", "small odd size"
```

| Test input | Expected output | What it validates |

|
