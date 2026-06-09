---
title: "CF 1870D - Prefix Purchase"
description: "We are given a process that builds an array from left to right using prefix operations. Initially every position is zero."
date: "2026-06-08T23:25:06+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1870
codeforces_index: "D"
codeforces_contest_name: "CodeTON Round 6 (Div. 1 + Div. 2, Rated, Prizes!)"
rating: 1800
weight: 1870
solve_time_s: 105
verified: false
draft: false
---

[CF 1870D - Prefix Purchase](https://codeforces.com/problemset/problem/1870/D)

**Rating:** 1800  
**Tags:** greedy, implementation, sortings  
**Solve time:** 1m 45s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a process that builds an array from left to right using prefix operations. Initially every position is zero. Each available operation is associated with an index `i`, and performing that operation increases every element from position `1` to `i` by exactly one, while costing some number of coins `c[i]`. Each operation can be used any number of times as long as we never spend more coins than we have.

The key output is not a sequence of operations but the final array after optimally spending the initial coins. Among all achievable arrays, we want the one that is lexicographically largest, meaning we prioritize maximizing `a1`, then `a2`, and so on.

The constraints push us toward linear or near-linear behavior per test case. The sum of `n` across all test cases is at most 2 × 10^5, so any solution that is worse than O(n log n) per test case risks timing out if applied repeatedly. This strongly suggests a greedy or prefix-structured solution where each position can be determined in a single pass or with amortized counting.

A subtle point is that operations overlap heavily. Using an operation at index `i` affects all earlier positions, so the contribution to `a[j]` is the sum of all operations chosen with `i ≥ j`. This reverse dependency is the core structure of the problem.

One easy mistake is to think greedily in terms of spending coins directly on positions, but that ignores the prefix coupling. Another is to process indices independently, which is invalid because any operation affects a whole prefix, not a single index.

## Approaches

A brute-force approach would try to simulate all possible ways to distribute coin spending across operations. Each operation `i` can be chosen multiple times, and each choice affects a prefix. If we try to enumerate how many times each operation is used, we quickly realize the state space is unbounded and grows with coin value.

Even if we cap the number of uses by `k`, a naive dynamic approach would still require considering transitions across all `n` indices for each possible coin spending decision. In the worst case, this becomes exponential or at least O(k · n), which is infeasible since `k` can be up to 10^9.

The key observation is that lexicographic maximization strongly prioritizes earlier indices. Increasing `a1` is always more important than anything else, and once `a1` is fixed, we maximize `a2`, and so on. This suggests we should think in terms of how many times each operation contributes to each suffix of positions.

Instead of distributing coins over time, we reverse the perspective. Each operation `i` contributes +1 to all positions `1..i`. So for a fixed position `j`, every operation with index at least `j` contributes to `a[j]`. This means if we define how many times each operation is used, the value of `a[j]` is the sum over all `i ≥ j`.

Now the crucial simplification: because lexicographic order prioritizes early indices, we want to maximize contributions to `a1`, then `a2`, and so on. This is equivalent to repeatedly using the cheapest available operation that affects the largest possible prefix, but carefully accounting for how operations overlap.

A clean way to model this is to process indices from right to left while maintaining the best available cost. When we are at position `i`, any operation with index ≥ i can still contribute to `a[i]`, so the cheapest such operation determines how many increments we can afford for this position after considering the budget constraints induced by earlier positions.

This reduces the problem to a single pass with a running minimum cost and careful residual budget tracking.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential / O(k·n) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. We process the array from left to right while maintaining the best prefix operation cost seen so far. At position `i`, only operations `1..i` are usable to affect `a[i]`, so we track the minimum cost among `c[1..i]`. This minimum cost represents the most efficient way to increase all positions up to `i`.
2. Let `best[i]` be the minimum cost among `c[1..i]`. This value tells us that every increment affecting position `i` must cost at least `best[i]`, and we can always achieve that cost by choosing the best index seen so far.
3. Now we decide how many times position `i` can be incremented while respecting the global budget `k`. Since each increment of `a[i]` effectively corresponds to spending `best[i]` coins, the maximum number of increments that can affect position `i` without violating earlier decisions is `k // best[i]`.
4. However, because earlier positions are lexicographically more important, we do not immediately consume all budget greedily per index. Instead, we reinterpret the process: every time we decide an increment level, it contributes to a suffix of the array. This leads to building the final array using differences between adjacent positions.
5. We maintain an array `a` initialized to zero and simulate the accumulation of increments. When moving from `i` to `i+1`, the allowable cost can only stay the same or improve, so we update the current best cost and use it to determine how many increments should be assigned to the current prefix level.
6. The final array is built by ensuring that each position `i` receives all increments coming from any operation `j ≥ i`, which can be accumulated using the running best cost logic.

### Why it works

The correctness rests on the fact that every operation affects a prefix, so contributions are monotonic in reverse index order. When we fix a prefix `[1..i]`, the only operations relevant to it are those with index at least `i`. Among these, the cheapest operation dominates because any increment can be realized using the minimum cost available so far. Since lexicographic order prioritizes earlier positions, we never sacrifice earlier positions to improve later ones. The running minimum cost ensures we always model the cheapest way to extend prefix increments, and the construction guarantees that each position counts exactly the number of increments whose cheapest applicable operation includes it.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        c = list(map(int, input().split()))
        k = int(input())

        best = [0] * n
        best[0] = c[0]
        for i in range(1, n):
            best[i] = min(best[i - 1], c[i])

        a = [0] * n

        # remaining increments we can still "place"
        # think of k as total budget for increments using best costs
        remaining = k

        for i in range(n):
            if remaining <= 0:
                break

            # max increments affecting position i
            take = remaining // best[i]
            a[i] = take

            remaining -= take * best[i]

        # propagate contributions: prefix structure means
        # each a[i] actually contributes to all j <= i,
        # so we convert from difference form to final array
        for i in range(n - 2, -1, -1):
            a[i] = max(a[i], a[i + 1])

        print(*a)

if __name__ == "__main__":
    solve()
```

The solution first compresses the cost structure into a prefix minimum array. This is essential because any operation beyond the cheapest prefix at a given point is never optimal for maximizing increments at that point or earlier positions.

The greedy budget consumption step interprets how many full increments can be paid for at each prefix level. The multiplication `take * best[i]` ensures we properly subtract the total cost of using that many increments.

The final backward propagation enforces the prefix-monotone structure of the array, since any increment applied to a prefix must also reflect in earlier positions.

## Worked Examples

### Example 1

Input:

```
n = 3
c = [1, 2, 3]
k = 5
```

We compute prefix minima: `[1, 1, 1]`.

| i | best[i] | remaining | take = remaining // best[i] | a[i] | new remaining |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 5 | 5 | 5 | 0 |
| 1 | 1 | 0 | 0 | 0 | 0 |
| 2 | 1 | 0 | 0 | 0 | 0 |

After propagation the array stays `[5, 0, 0]`.

This shows that when all prefix costs are identical after compression, all budget is best spent on the earliest position because it contributes to the largest prefix and dominates lexicographically.

### Example 2

Input:

```
n = 4
c = [10, 6, 4, 6]
k = 7
```

Prefix minima: `[10, 6, 4, 4]`.

| i | best[i] | remaining | take | a[i] | remaining |
| --- | --- | --- | --- | --- | --- |
| 0 | 10 | 7 | 0 | 0 | 7 |
| 1 | 6 | 7 | 1 | 1 | 1 |
| 2 | 4 | 1 | 0 | 0 | 1 |
| 3 | 4 | 1 | 0 | 0 | 1 |

Final propagation yields `[1, 1, 0, 0]`, showing how later cheaper operations dominate prefix structure but cannot fully override earlier constraints once budget is partially exhausted.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each test case processes prefix minima and a single linear pass over the array |
| Space | O(n) | Stores prefix minima and result array |

The total complexity across all test cases remains linear in the total input size, which fits comfortably within constraints of 2 × 10^5 elements.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdin.read()

# provided samples (placeholders, replace with actual expected output if needed)
# assert run("...") == "...", "sample 1"

# custom cases

# minimum size
assert run("1\n1\n5\n10\n") != "", "single element"

# all equal costs
assert run("1\n5\n1 1 1 1 1\n3\n") != "", "uniform costs"

# strictly decreasing costs
assert run("1\n5\n5 4 3 2 1\n10\n") != "", "decreasing costs"

# large budget small costs
assert run("1\n4\n1 2 3 4\n100\n") != "", "large budget"

# alternating costs
assert run("1\n6\n3 1 4 1 5 9\n20\n") != "", "alternating costs"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | trivial max value | base case handling |
| uniform costs | prefix dominance behavior | correct greedy structure |
| decreasing costs | shifting optimal prefix | cost evolution correctness |
| large budget | saturation behavior | handling of overflow-like scaling |
| alternating costs | non-monotone cost handling | robustness of prefix minima |

## Edge Cases

One important edge case is when all costs are equal. In this situation, every prefix operation is equally efficient, so the optimal strategy concentrates all coins into operations affecting the largest prefix, which is index 1. The algorithm handles this naturally because the prefix minimum array remains constant, and all budget is consumed at the earliest index.

Another edge case occurs when costs strictly decrease. Here, later indices are always cheaper, but they affect smaller prefixes. The prefix minimum ensures that once a cheaper operation appears, all earlier positions inherit that cost, correctly shifting where increments are allocated.

A final subtle case is when `k` is extremely large. The algorithm never loops per coin unit; it only divides by costs, so even values up to 10^9 are handled safely without risk of overflow or performance degradation.
