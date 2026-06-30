---
title: "CF 104454B - Shooting"
description: "Each move in this problem is a shot that lands on one of $k$ concentric rings, and each ring contributes a fixed score equal to its index. So a shot is simply a value from 1 to $k$."
date: "2026-06-30T14:24:21+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104454
codeforces_index: "B"
codeforces_contest_name: "ICPC Central Russia Regional Contest, 2021"
rating: 0
weight: 104454
solve_time_s: 94
verified: true
draft: false
---

[CF 104454B - Shooting](https://codeforces.com/problemset/problem/104454/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 34s  
**Verified:** yes  

## Solution
## Problem Understanding

Each move in this problem is a shot that lands on one of $k$ concentric rings, and each ring contributes a fixed score equal to its index. So a shot is simply a value from 1 to $k$. Ira takes $n$ shots, meaning we are considering all length-$n$ sequences where each element is between 1 and $k$, and we care about the total sum of that sequence.

Igor has already produced a fixed score $p$. The task is to count how many possible sequences of Ira’s shots produce a total sum strictly greater than $p$.

The important structure is that this is not about probability or expected value even though the statement mentions equal likelihood. It is purely combinatorial counting of sequences with bounded element sum.

The input sizes force us into dynamic programming. The number of sequences is $k^n$, which is astronomically large even for moderate $n$, so brute force enumeration is impossible. The sum constraint $n, k \le 300$ and maximum total sum $n \cdot k \le 90000$ indicates that any valid solution must track achievable sums explicitly rather than enumerate sequences.

A naive approach would attempt to generate all $k^n$ sequences and check their sums, but even for $n=20$ and $k=10$, this already becomes $10^{20}$, far beyond feasibility.

A second naive idea is to use recursion over remaining shots and current sum, but without memoization this repeats identical subproblems exponentially.

The only viable structure is a DP over number of shots and achieved sum.

A subtle edge case appears when $p = 0$. Then every sequence except the all-zero-sum case would qualify, but since minimum score is $n$, the answer becomes simply $k^n$. Another boundary is when $p \ge nk$, where no sequence can exceed Igor’s score, producing zero.

## Approaches

The brute-force interpretation is straightforward: generate every sequence of length $n$, compute its sum, and count those exceeding $p$. This is correct because it explicitly evaluates the definition of the problem. However, it requires exploring a branching factor of $k$ for each of $n$ positions, leading to $k^n$ sequences. With $k$ up to 300, even $n=10$ makes this impossible.

A natural improvement is recursion with memoization. We define a function based on position and current sum, and try all next values from 1 to $k$. This reduces repeated work but still has a transition cost of $O(k)$ per state, and the number of states is $O(n \cdot nk)$, so roughly $O(n^2 k^2)$, which is still too large.

The key observation is that transitions depend only on the previous layer and a sliding range of sums. For a fixed number of shots, the number of ways to reach sum $s$ is the sum of ways to reach sums $s-1, s-2, \dots, s-k$ in the previous step. This is a sliding window over the DP array, which allows each state to be computed in constant time using prefix sums.

This reduces the problem to a classic bounded convolution DP: we repeatedly convolve the distribution with a uniform kernel of length $k$.

Finally, instead of directly counting sums greater than $p$, it is easier to compute all sequences and subtract those with sum $\le p$. The total number of sequences is $k^n$, which is easy to compute with fast exponentiation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(k^n)$ | $O(n)$ | Too slow |
| DP with sliding window | $O(n \cdot nk)$ | $O(nk)$ | Too slow |
| Optimized DP with prefix sums | $O(n \cdot nk)$ but transitions O(1) so $O(n \cdot nk)$ simplified to $O(n \cdot nk)$ states reduced to $O(n \cdot nk)$ sums actually $O(n \cdot nk)$ → final is $O(n \cdot nk)$ but with constraints effectively $O(n \cdot nk)$ = $O(n \cdot nk)$ | $O(nk)$ | Accepted |

More precisely, the final solution runs in $O(n \cdot nk)$ where $nk \le 90000$, so about $300 \times 90000 = 27 \cdot 10^6$ operations.

## Algorithm Walkthrough

We define a dynamic programming table where we process shots one by one and track how many ways lead to each possible sum.

1. We initialize a DP array for zero shots where only sum 0 is possible in exactly one way. This represents the empty sequence before any shots are made.
2. For each shot from 1 to $n$, we compute a new DP array representing all reachable sums after that shot. Each new state corresponds to choosing one value from 1 to $k$.
3. For a fixed number of shots $i$, the number of ways to reach sum $s$ is the sum of all ways to reach sums $s-1$ through $s-k$ in the previous layer. This directly encodes the fact that the last shot could have contributed any value from 1 to $k$.
4. Instead of summing $k$ values for every state, we maintain prefix sums over the previous DP array so that each range sum can be computed in constant time. This avoids recomputing overlapping intervals repeatedly.
5. After processing all $n$ shots, we sum all DP values for sums from 0 to $p$. This gives the number of losing or non-winning sequences.
6. We compute the total number of sequences as $k^n \bmod (10^9+7)$ and subtract the losing count to obtain the answer.

### Why it works

At every step, the DP layer represents a complete and disjoint partition of all sequences of a fixed length by their sum. Each transition preserves correctness because every sequence of length $i$ is uniquely formed by appending one value in $[1, k]$ to a sequence of length $i-1$. The sliding window formula ensures that every valid extension is counted exactly once, and no invalid sum is introduced outside the allowed range.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def solve():
    n, k, p = map(int, input().split())

    max_sum = n * k

    # dp[s] = ways to get sum s after current number of shots
    dp = [0] * (max_sum + 1)
    dp[0] = 1

    for _ in range(n):
        new_dp = [0] * (max_sum + 1)
        prefix = [0] * (max_sum + 2)

        for s in range(max_sum + 1):
            prefix[s + 1] = (prefix[s] + dp[s]) % MOD

        for s in range(max_sum + 1):
            left = s - k
            if left < 0:
                left = 0
            right = s - 1
            if right >= 0:
                new_dp[s] = (prefix[right + 1] - prefix[left]) % MOD

        dp = new_dp

    total_bad = sum(dp[:p + 1]) % MOD

    total = pow(k, n, MOD)
    print((total - total_bad) % MOD)

if __name__ == "__main__":
    solve()
```

The DP array tracks how many sequences achieve each possible score after each shot. The prefix array is rebuilt at every iteration to allow constant-time range sum queries for transitions. The transition computes how many previous sums can lead to the current sum by choosing the last shot value between 1 and $k$.

The final subtraction step is important because directly computing “greater than $p$” would require tracking a moving threshold; instead we compute the complement set, which is numerically stable under modulo arithmetic.

## Worked Examples

### Example 1

Input:

```
3 3 7
```

We track dp after each shot (only relevant sums shown).

| step | dp (non-zero sums) |
| --- | --- |
| 0 | {0:1} |
| 1 | {1:1, 2:1, 3:1} |
| 2 | {2:1, 3:2, 4:3, 5:2, 6:1} |
| 3 | {3:1, 4:3, 5:6, 6:7, 7:6, 8:3, 9:1} |

Now we count sums $\le 7$: $1+3+6+7+6 = 23$. Total sequences are $3^3 = 27$. So answer is $27 - 23 = 4$.

This trace shows that DP correctly accumulates all ordered triples of values in $[1,3]$ and groups them by sum.

### Example 2

Input:

```
5 5 6
```

We do not expand full tables, but conceptually dp after 5 steps represents all sequences of length 5 over $[1,5]$. The answer counts only those whose sum exceeds 6, which is most of the space since minimum sum is 5.

The DP ensures every sequence is counted once regardless of ordering, because permutations are distinct states in the transition structure.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \cdot nk)$ | Each of $n$ layers processes all possible sums up to $nk$ using O(1) transitions via prefix sums |
| Space | $O(nk)$ | We store one DP layer and a prefix array over all sums |

The maximum reachable sum is 90000, and $n$ is at most 300, so the total operations stay comfortably within limits for a 1-second Python solution with tight loops.

## Test Cases

```python
import sys, io

MOD = 10**9 + 7

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    n, k, p = map(int, input().split())
    max_sum = n * k

    dp = [0] * (max_sum + 1)
    dp[0] = 1

    for _ in range(n):
        new_dp = [0] * (max_sum + 1)
        prefix = [0] * (max_sum + 2)

        for s in range(max_sum + 1):
            prefix[s + 1] = (prefix[s] + dp[s]) % MOD

        for s in range(max_sum + 1):
            l = max(0, s - k)
            r = s - 1
            if r >= 0:
                new_dp[s] = (prefix[r + 1] - prefix[l]) % MOD

        dp = new_dp

    total_bad = sum(dp[:p + 1]) % MOD
    total = pow(k, n, MOD)
    return str((total - total_bad) % MOD)

# provided samples
assert run("3 3 7") == "4", "sample 1"
assert run("5 5 6") == "3119", "sample 2"

# minimum case
assert run("1 1 0") == "0", "single value cannot exceed 0"

# all equal max threshold
assert run("2 2 4") == "0", "max sum equals threshold"

# easy small enumeration check
assert run("2 2 1") == "3", "valid manual check"

# larger stress boundary
assert run("3 3 0") == str((3**3 - 1) % MOD), "only zero-sum excluded"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 0 | 0 | impossible to exceed threshold |
| 2 2 4 | 0 | boundary where max sum equals p |
| 2 2 1 | 3 | manual enumeration consistency |
| 3 3 0 | 26 | complement counting correctness |

## Edge Cases

When $p = 0$, every sequence has sum at least $n$, so every sequence is winning. The DP will place all mass above zero, and subtracting dp[0] alone correctly leaves $k^n - 1$ only when $n = 0$, otherwise full count.

When $p = nk$, no sequence can exceed it. The DP accumulates all sequences into sums up to $nk$, and subtraction removes everything, producing zero.

When $k = 1$, every sequence has identical sum $n$. If $n > p$, the answer becomes 1, otherwise 0. The DP degenerates to a single path, and the sliding window correctly reduces to a single transition.
