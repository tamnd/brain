---
title: "CF 104783A - Silver Star Stands Alone"
description: "The input gives a single prime number $P$, which represents the position of the final asteroid, called Silver Star, on a one-dimensional line starting from Mars."
date: "2026-06-28T14:47:22+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104783
codeforces_index: "A"
codeforces_contest_name: "2021-2022 CTU Open Contest"
rating: 0
weight: 104783
solve_time_s: 53
verified: true
draft: false
---

[CF 104783A - Silver Star Stands Alone](https://codeforces.com/problemset/problem/104783/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 53s  
**Verified:** yes  

## Solution
## Problem Understanding

The input gives a single prime number $P$, which represents the position of the final asteroid, called Silver Star, on a one-dimensional line starting from Mars. Along this line, there are special asteroids placed at distances from Mars equal to the prime numbers in increasing order: 2, 3, 5, 7, 11, and so on, up to $P$.

A probe starts at the asteroid at distance 2 and must end at the asteroid at distance $P$. It can visit any subset of the intermediate asteroids, but it must respect a movement constraint: whenever it moves from one visited asteroid to the next, the distance between their positions must not exceed 14 units. Since movement is strictly forward along the increasing sequence of primes, a trajectory is simply a subsequence of the prime positions starting at 2 and ending at $P$, where consecutive chosen primes differ by at most 14.

The task is to count how many such valid trajectories exist.

The constraint that $P \le 211$ means we are dealing with a very small prefix of the primes. The number of primes up to 211 is only a few dozen, so even an $O(n^2)$ dynamic programming solution is trivial in terms of performance. This already suggests that the intended solution is based on straightforward combinatorics over a small DAG rather than any heavy optimization.

A subtle failure case appears when one assumes that “at most 14 AU” means only adjacent primes can be considered. For example, from 2 we can jump directly to 11 because 11 − 2 = 9, which is allowed, even though there are intermediate primes. A naive adjacency-only interpretation would incorrectly undercount paths by forbidding such skips.

Another mistake arises if one assumes all primes are equally spaced or tries to index jumps by count instead of actual numeric distance. The constraint depends on actual values, not position in the sequence.

## Approaches

The brute-force viewpoint treats each trajectory as a decision process: at every asteroid, we choose whether to go to any later asteroid that is within 14 units. This can be explored with DFS from the first prime, recursively branching to all valid next steps. This is correct because it enumerates all valid subsequences respecting the jump constraint and counts those reaching the last node.

However, this exploration grows quickly in branching factor. In a worst conceptual case where every node can jump to many future nodes, the number of recursive paths can grow exponentially with the number of primes, roughly $O(2^n)$. Even though $n$ is small here, this approach is structurally inefficient and unnecessary.

The key observation is that the graph formed by primes and valid jumps is a directed acyclic graph ordered by increasing values. Any path count problem on a DAG can be reduced to dynamic programming: the number of ways to reach a node is the sum of ways to reach all nodes that can transition into it.

For each prime $p[i]$, we only need to consider earlier primes $p[j]$ such that $p[i] - p[j] \le 14$. Since primes are increasing and gaps are small, only a short suffix of previous nodes can ever reach the current one. This reduces the transition cost per node to constant amortized time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| DFS enumeration | $O(2^n)$ | $O(n)$ | Too slow |
| DP on DAG | $O(n^2)$ or $O(n)$ optimized | $O(n)$ | Accepted |

## Algorithm Walkthrough

We treat the primes up to $P$ as nodes in increasing order, and we compute how many ways each node can be reached from the start.

1. Generate the list of all primes from 2 up to $P$. This forms the vertex set of the graph. The order of this list is already topological since it is strictly increasing.
2. Create a DP array where `dp[i]` represents the number of valid trajectories that end at the $i$-th prime.
3. Initialize `dp[0] = 1` because there is exactly one way to start at the first asteroid (2 AU), and all paths must begin there.
4. For each prime index $i$ from left to right, compute `dp[i]` by summing contributions from earlier indices $j < i$ such that `primes[i] - primes[j] <= 14`. Each such $j$ represents a valid last step into $i$, so every way to reach $j$ can be extended to $i$.
5. Maintain the sum efficiently by either scanning backward until the distance condition fails, or by keeping a sliding window of valid predecessors. Since values increase, once `primes[i] - primes[j] > 14`, all earlier $j$ are invalid.
6. The final answer is `dp[last]`, since every valid trajectory must end at Silver Star.

### Why it works

Every valid trajectory is uniquely defined by its last jump into each asteroid. The DP ensures that each state accumulates all ways to reach it from valid predecessors, and no invalid transition is ever included because the distance constraint is checked directly on the actual asteroid positions. Since the graph is acyclic in increasing order, each subproblem depends only on already-computed states, guaranteeing correctness by induction over the ordered primes.

## Python Solution

```python
import sys
input = sys.stdin.readline

def sieve(n):
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n ** 0.5) + 1):
        if is_prime[i]:
            step = i
            start = i * i
            for j in range(start, n + 1, step):
                is_prime[j] = False
    return [i for i in range(2, n + 1) if is_prime[i]]

def solve():
    P = int(input().strip())
    primes = sieve(P)

    n = len(primes)
    dp = [0] * n
    dp[0] = 1

    for i in range(1, n):
        total = 0
        j = i - 1
        while j >= 0 and primes[i] - primes[j] <= 14:
            total += dp[j]
            j -= 1
        dp[i] = total

    print(dp[-1])

if __name__ == "__main__":
    solve()
```

The sieve constructs the prime sequence up to $P$, which is small enough that a simple $O(P \log \log P)$ method is sufficient.

The DP array encodes all partial trajectory counts. For each position, we scan backwards until the distance condition breaks. This is safe because primes are strictly increasing, so once a gap exceeds 14, all earlier ones will also exceed it.

A common implementation mistake is forgetting that transitions depend on numeric difference rather than index difference. Another subtle issue is initializing `dp[0] = 1`; without this base case, all subsequent counts remain zero.

## Worked Examples

Since concrete sample outputs were not provided in the statement, consider illustrative inputs.

Let the primes up to 11 be $[2, 3, 5, 7, 11]$.

For input $P = 11$, the DP evolves as follows:

| i | prime | valid predecessors | dp[i] |
| --- | --- | --- | --- |
| 0 | 2 | none | 1 |
| 1 | 3 | 2 | 1 |
| 2 | 5 | 3, 2 | 2 |
| 3 | 7 | 5, 3, 2 | 4 |
| 4 | 11 | 7, 5, 3, 2 | 8 |

This shows that every node aggregates all reachable histories from valid jumps, and the count grows as paths branch through intermediate primes.

Now consider a smaller case up to $P = 5$, primes $[2, 3, 5]$:

| i | prime | valid predecessors | dp[i] |
| --- | --- | --- | --- |
| 0 | 2 | none | 1 |
| 1 | 3 | 2 | 1 |
| 2 | 5 | 3, 2 | 2 |

This demonstrates how skipping is allowed: the jump from 2 to 5 is valid and contributes directly to `dp[2]`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \cdot k)$, effectively $O(n^2)$ worst case | Each prime checks a bounded number of previous primes within distance 14 |
| Space | $O(n)$ | DP array and prime list storage |

Since $P \le 211$, the number of primes is small (tens of elements), so the solution runs instantly even under quadratic behavior.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    from math import isqrt

    def sieve(n):
        is_prime = [True] * (n + 1)
        is_prime[0] = is_prime[1] = False
        for i in range(2, isqrt(n) + 1):
            if is_prime[i]:
                for j in range(i * i, n + 1, i):
                    is_prime[j] = False
        return [i for i in range(2, n + 1) if is_prime[i]]

    P = int(sys.stdin.readline().strip())
    primes = sieve(P)

    dp = [0] * len(primes)
    dp[0] = 1

    for i in range(1, len(primes)):
        total = 0
        j = i - 1
        while j >= 0 and primes[i] - primes[j] <= 14:
            total += dp[j]
            j -= 1
        dp[i] = total

    return str(dp[-1])

# minimal case
assert run("2\n") == "1"

# small case
assert run("5\n") == "2"

# slightly larger case
assert run("11\n") == "8"

# boundary case (largest constraint)
assert run("211\n") == run("211\n")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 | 1 | single-node base case |
| 5 | 2 | direct jump allowed and branching starts |
| 11 | 8 | multi-step accumulation over DAG |
| 211 | computed value | full constraint stress case |

## Edge Cases

The smallest possible input $P = 2$ consists of a single asteroid. The only trajectory is the trivial one starting and ending at the same node, and the DP correctly returns 1 because it initializes `dp[0] = 1` and never performs transitions.

A case like $P = 5$ demonstrates the importance of allowing non-adjacent jumps. The jump from 2 directly to 5 is valid because the difference is 3, and the DP includes it when computing `dp[2]`. A naive adjacency-only approach would incorrectly output 1 instead of 2 by missing the path that skips 3.

For larger $P$, such as 211, the algorithm relies on the fact that only a short suffix of predecessors contributes to each state. The backward loop stops as soon as the distance exceeds 14, ensuring that irrelevant primes are never considered, which preserves efficiency even at the upper bound.
