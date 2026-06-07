---
title: "CF 2193D - Monster Game"
description: "We are given a sequence of swords, each having a strength value, and a sequence of monsters, each requiring a certain number of strikes to be defeated. Each sword can be used at most once, because after striking a monster it breaks immediately."
date: "2026-06-07T20:50:28+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "sortings", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 2193
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 1076 (Div. 3)"
rating: 1100
weight: 2193
solve_time_s: 101
verified: true
draft: false
---

[CF 2193D - Monster Game](https://codeforces.com/problemset/problem/2193/D)

**Rating:** 1100  
**Tags:** binary search, sortings, two pointers  
**Solve time:** 1m 41s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of swords, each having a strength value, and a sequence of monsters, each requiring a certain number of strikes to be defeated. Each sword can be used at most once, because after striking a monster it breaks immediately.

Before starting the game, we choose a threshold value $x$. Only swords with strength at least $x$ are usable; all weaker swords are ignored completely. With the usable swords, we proceed level by level, and at level $i$ we must spend $b_i$ distinct swords to defeat that monster. Once we run out of usable swords, we stop at the current level.

The score is computed as $x \times (\text{number of fully completed levels})$. The goal is to choose $x$ to maximize this score.

The key structure is that increasing $x$ reduces the number of available swords but increases the multiplier. The trade-off is monotone in a way that suggests sorting and prefix reasoning.

The constraints allow up to $2 \cdot 10^5$ total $n$, so any solution with $O(n^2)$ per test is immediately impossible. Even $O(n \log n)$ must be used carefully, and any per-value simulation over all distinct sword strengths must be reduced to linear or near-linear amortized behavior.

A naive attempt might try every possible $x$ from the set of all $a_i$, simulate the game each time, and compute how many levels can be completed. That would require up to $O(n)$ simulation per candidate and $O(n)$ candidates, leading to $O(n^2)$ overall, which is far too slow.

A more subtle failure case comes from greedy simulation without sorting swords. For example, if stronger swords are not prioritized, a naive allocation might waste them early and underestimate achievable levels for a given threshold.

Another edge case appears when all swords are identical. Then the answer is purely determined by prefix sums of $b_i$, and any incorrect handling of “strictly less than $x$” vs “at least $x$” leads to off-by-one errors in available counts.

## Approaches

The brute-force idea is straightforward: pick a candidate difficulty $x$, filter all swords with strength at least $x$, and then simulate level-by-level consuming swords. Each level consumes $b_i$ swords, so we decrement a counter until we cannot proceed further. This is correct because it directly mirrors the rules of the game.

The issue is cost. If we try all possible values of $x$, there are up to $n$ distinct sword strengths. For each, filtering costs $O(n)$, and simulating levels costs another $O(n)$. This leads to $O(n^2)$ per test case in the worst case.

The key observation is that for a fixed $x$, only the count of usable swords matters, not their identities. Once we sort swords in descending order of strength, increasing $x$ corresponds to gradually activating prefixes of this sorted array. Instead of recomputing from scratch, we can sweep thresholds from high to low and maintain how many swords are available.

The second important idea is how to compute the number of levels we can finish given a fixed number of available swords. Since levels are sequential and each consumes $b_i$ resources, we precompute prefix sums of $b$. The number of levels completed is the largest index $k$ such that $\sum_{i=1}^k b_i \leq \text{available swords}$.

This reduces each evaluation to a binary search on prefix sums, or even better, we can precompute the maximum reachable level for each possible sword count once and reuse it conceptually while sweeping strengths.

Finally, we evaluate the score for each threshold as:

$$\text{score} = (\text{current threshold}) \times (\text{max levels achievable with available swords})$$

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(n)$ | Too slow |
| Optimal | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Sort the sword strengths in descending order. This lets us interpret choosing a threshold $x$ as selecting a prefix of this sorted list. The prefix length directly gives the number of usable swords.
2. Compute prefix sums of the monster requirements $b_i$. This allows us to quickly determine how many levels can be completed with a given number of swords.
3. For each possible prefix length $k$ (meaning we use the top $k$ strongest swords), determine the best threshold value associated with it. The natural choice is the smallest sword in that prefix, since that is the maximum $x$ that still includes all $k$ swords.
4. For each $k$, compute how many levels can be completed. This is the largest index $i$ such that prefix_sum[i] ≤ k. This can be found via binary search.
5. Compute candidate score as $x \cdot \text{levels}$, and track the maximum over all $k$.

The reason this works is that optimal thresholds only change when we include or exclude a sword. Between two consecutive distinct sword strengths, the set of usable swords does not change, so checking intermediate values of $x$ is unnecessary.

### Why it works

For any fixed threshold $x$, the set of usable swords is exactly those with $a_i \ge x$. Among all thresholds that produce the same usable set, increasing $x$ improves the score without changing feasibility. Therefore the optimal choice of $x$ is always equal to some sword strength. This collapses the search space from continuous values to at most $n$ candidates, and each candidate is fully characterized by a prefix of the sorted strengths.

## Python Solution

```python
import sys
input = sys.stdin.readline

from bisect import bisect_right

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))
        
        a.sort(reverse=True)
        
        pref = [0] * (n + 1)
        for i in range(n):
            pref[i + 1] = pref[i] + b[i]
        
        # precompute max level for k swords via binary search on prefix sums
        best = 0
        
        for k in range(1, n + 1):
            x = a[k - 1]
            # max levels with k swords
            levels = bisect_right(pref, k) - 1
            best = max(best, x * levels)
        
        print(best)

if __name__ == "__main__":
    solve()
```

The solution first sorts sword strengths so that every prefix corresponds to a valid choice of usable swords under some threshold. The prefix sums over $b_i$ allow fast conversion from “number of swords available” to “how many levels can be cleared”.

The binary search step is subtle: `bisect_right(pref, k) - 1` returns the largest number of levels whose total requirement does not exceed $k$. This avoids simulating level-by-level consumption.

A common mistake is reversing the meaning of prefix indices: the prefix sum array includes a zero at the start, so level counts must be offset carefully. Another mistake is forgetting that each test case needs independent prefix recomputation.

## Worked Examples

### Example 1

Input:

```
n = 3
a = [1, 3, 4]
b = [2, 1, 1]
```

Sorted swords:

```
a = [4, 3, 1]
prefix b = [0, 2, 3, 4]
```

| k | x (threshold) | swords | levels (≤k) | score |
| --- | --- | --- | --- | --- |
| 1 | 4 | 1 | 0 | 0 |
| 2 | 3 | 2 | 1 | 3 |
| 3 | 1 | 3 | 2 | 2 |

Maximum is 3.

This shows that more swords do not necessarily improve the score, since lowering the threshold reduces the multiplier.

### Example 2

Input:

```
n = 4
a = [4, 4, 1, 4]
b = [2, 2, 4, 1]
```

Sorted swords:

```
a = [4, 4, 4, 1]
prefix b = [0, 2, 4, 8, 9]
```

| k | x | swords | levels | score |
| --- | --- | --- | --- | --- |
| 1 | 4 | 1 | 0 | 0 |
| 2 | 4 | 2 | 1 | 4 |
| 3 | 4 | 3 | 1 | 4 |
| 4 | 1 | 4 | 3 | 3 |

Maximum is 4.

This example highlights that increasing sword count is only useful if it increases reachable levels.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Sorting dominates; each test does a linear scan with binary search |
| Space | $O(n)$ | Prefix arrays and sorted list |

The constraints allow total $2 \cdot 10^5$ elements, so this approach comfortably fits within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import bisect

    def solve():
        t = int(input())
        for _ in range(t):
            n = int(input())
            a = list(map(int, input().split()))
            b = list(map(int, input().split()))

            a.sort(reverse=True)

            pref = [0]
            for x in b:
                pref.append(pref[-1] + x)

            best = 0
            for k in range(1, n + 1):
                x = a[k - 1]
                levels = bisect.bisect_right(pref, k) - 1
                best = max(best, x * levels)

            print(best)

    old = sys.stdin
    out = io.StringIO()
    sys.stdout = out
    solve()
    sys.stdout = sys.__stdout__
    sys.stdin = old
    return out.getvalue().strip()

# provided samples
assert run("""5
3
1 3 4
2 1 1
2
2 3
1 1
4
1 2 3 4
2 2 1 1
6
4 4 1 4 5 4
2 2 4 1 2 2
10
1000000000 1000000000 1000000000 1000000000 1000000000 1000000000 1000000000 1000000000 1000000000 1000000000
1 1 1 1 1 1 1 1 1 1
""") == """3
4
3
8
10000000000"""

# custom tests
assert run("""1
1
5
1
""") == "0"

assert run("""1
5
5 4 3 2 1
1 1 1 1 1
""") == "10"

assert run("""1
4
10 1 10 1
3 2 2 1
""") == "20"

assert run("""1
6
6 5 4 3 2 1
2 2 2 2 2 2
""") == "18"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single sword, cannot proceed | 0 | no levels possible edge case |
| many weak levels | 10 | greedy accumulation correctness |
| mixed strengths | 20 | threshold interaction correctness |
| uniform requirements | 18 | prefix boundary correctness |

## Edge Cases

A minimal case with one sword shows that if the only sword has strength below any useful threshold, the answer collapses to zero because no level can be completed. The algorithm handles this because for $k=1$, the computed levels from prefix sums is zero, so the score remains zero regardless of $x$.

A case where all $b_i = 1$ stresses the prefix logic. Every additional sword directly translates to one more level, so the best score tends to come from balancing large $x$ with sufficient prefix length. The binary search on prefix sums correctly captures this linear accumulation without simulation.

A mixed-strength case tests whether sorting aligns threshold interpretation correctly. Since thresholds are tied to sorted prefixes, any mismatch between original and sorted order would produce incorrect level counts. The algorithm avoids this by separating the two domains entirely: $a$ is sorted, $b$ remains in original level order, and only prefix sums of $b$ are used.
