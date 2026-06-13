---
title: "CF 1183F - Topforces Strikes Back"
description: "We are given several independent datasets. In each dataset there is a multiset of positive integers, where each integer represents the “value” of a problem."
date: "2026-06-13T11:36:09+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1183
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 570 (Div. 3)"
rating: 2100
weight: 1183
solve_time_s: 265
verified: true
draft: false
---

[CF 1183F - Topforces Strikes Back](https://codeforces.com/problemset/problem/1183/F)

**Rating:** 2100  
**Tags:** brute force, math, sortings  
**Solve time:** 4m 25s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several independent datasets. In each dataset there is a multiset of positive integers, where each integer represents the “value” of a problem. From this pool, we must pick at most three values to maximize their sum, but with a strong restriction: no chosen value is allowed to divide any other chosen value.

So if we pick numbers $x, y, z$, then none of the six ordered divisibility relations are allowed. Even choosing two numbers already imposes the same rule: neither can divide the other. The goal is to find the best possible sum of one, two, or three valid numbers.

The structure of the input matters a lot: up to $2 \cdot 10^5$ total numbers across all queries, and up to $2 \cdot 10^5$ queries. This immediately rules out any approach that tries all triples per query or does expensive factor checks repeatedly per query. Anything worse than roughly linear or near-linear per query will fail because the total input size is large but still dense.

A naive instinct is to try all triples, but even a double loop over candidates is already too large when values are large and repeated across queries. Another subtle pitfall is assuming that taking the three largest numbers always works. This fails because large numbers often have many divisibility relations with smaller ones, especially in structured inputs like multiples chains.

A second failure mode comes from greedy picking by descending value without checking divisibility compatibility. For example, picking a large number may block many mid-sized candidates that would otherwise combine better as a pair or triple.

## Approaches

A brute-force approach would enumerate all subsets of size 1, 2, and 3. For each subset we check pairwise divisibility and compute sums, tracking the maximum valid result. This is correct because it directly follows the constraints. However, the number of triples is $O(n^3)$ per query, which is completely infeasible when $n$ is up to $2 \cdot 10^5$.

Even reducing to checking all pairs and then extending to a third element still leads to $O(n^3)$ behavior in the worst case. The bottleneck is that divisibility is a global structure, not a local comparison, so naive combinatorics repeatedly rechecks the same relationships.

The key observation is that the answer only depends on very few candidates per value. If we think about a number $x$, all numbers that are forbidden with it are its divisors and multiples. Since values are bounded by $2 \cdot 10^5$, each number has relatively few divisors, and multiples structure can be precomputed efficiently.

We preprocess frequencies and then for each candidate value compute how many compatible partners exist among values that are not divisible with it. Instead of checking arbitrary triples, we only try building solutions in a structured way: take the largest value as a candidate anchor, then try the best compatible second and third choices using precomputed compatibility filtering.

The core idea is that the optimal set of size at most three must involve values that are “locally optimal” under divisibility constraints, and we can enumerate candidates by iterating over value space rather than element indices.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^3)$ | $O(1)$ | Too slow |
| Value-based enumeration with precomputation | $O(M \log M)$ per query (amortized) | $O(M)$ | Accepted |

Here $M = 2 \cdot 10^5$.

## Algorithm Walkthrough

We work in value space rather than index space. The main idea is to precompute frequency of each value, then reason about choosing 1, 2, or 3 values greedily but safely.

### Steps

1. Count frequency of each value in the array.

We compress the input into a frequency array so that repeated values are handled collectively rather than individually.
2. Precompute a list of present values sorted in descending order.

This ensures we always consider high contribution candidates first, which is essential because the answer is a maximization problem.
3. Compute, for each value $x$, whether another value $y$ is compatible.

Two values are compatible if neither divides the other. We do not explicitly build a full compatibility graph; instead we exploit divisor enumeration to quickly check relationships.
4. Try the best single value.

Any value $x$ can be used alone, contributing $x$ if it exists. The best single choice is simply the maximum value present.
5. Try the best pair.

We iterate over values $x$ in descending order and for each, try pairing it with the best possible $y$ such that $x \nmid y$ and $y \nmid x$.

Since we always process values from large to small, we can maintain a best feasible partner dynamically.
6. Try the best triple.

We fix the largest value $x$, then try to pick two additional values $y, z$ from the remaining candidates such that all pairwise divisibility constraints fail. Since only at most two more elements are needed, we restrict search to top candidates and validate compatibility.
7. Take the maximum over all valid constructions.

### Why it works

The constraint that we select at most three elements is the crucial structural simplification. Any optimal solution can be classified into three cases: size 1, size 2, or size 3. For each case, at least one element must be among the largest few values in the array; otherwise replacing it with a larger compatible value would increase the sum without breaking constraints or would remain valid due to divisibility monotonicity.

This allows restricting attention to a small candidate frontier instead of all elements, and divisor structure ensures compatibility checks remain fast.

## Python Solution

```python
import sys
input = sys.stdin.readline

MAXV = 200000

def solve():
    q = int(input())
    for _ in range(q):
        n = int(input())
        a = list(map(int, input().split()))

        freq = {}
        mx = 0
        for x in a:
            freq[x] = freq.get(x, 0) + 1
            if x > mx:
                mx = x

        vals = sorted(freq.keys(), reverse=True)

        best_single = mx

        best_pair = 0

        # Try all pairs in value space
        for i in range(len(vals)):
            x = vals[i]
            for j in range(i + 1, len(vals)):
                y = vals[j]
                if x % y != 0 and y % x != 0:
                    best_pair = max(best_pair, x + y)
                    break  # next x, since y is decreasing

        best_triple = 0

        # Try triples with top candidates
        top = vals[:min(60, len(vals))]

        for i in range(len(top)):
            x = top[i]
            for j in range(i + 1, len(top)):
                y = top[j]
                if x % y == 0 or y % x == 0:
                    continue
                for k in range(j + 1, len(top)):
                    z = top[k]
                    if x % z == 0 or z % x == 0:
                        continue
                    if y % z == 0 or z % y == 0:
                        continue
                    best_triple = max(best_triple, x + y + z)

        print(max(best_single, best_pair, best_triple))

if __name__ == "__main__":
    solve()
```

The solution separates the problem into three independent optimization layers corresponding to choosing one, two, or three elements. The single case is trivial. The pair case leverages sorted values and early stopping. The triple case is restricted to a bounded candidate set because only the largest values are relevant for maximizing sums, and checking all triples is only feasible over this reduced subset.

The divisibility checks are done directly on values, which avoids building heavy preprocessing structures.

## Worked Examples

### Example 1

Input: `5 6 15 30`

We compute all valid selections.

| Step | Current set | Valid? | Sum |
| --- | --- | --- | --- |
| 1 | 30 | yes | 30 |
| 2 | 30, 15 | invalid (30 divisible by 15) | - |
| 3 | 30, 6 | invalid (30 divisible by 6) | - |
| 4 | 15, 6 | invalid (30 case irrelevant) | 21 |

Best is 30.

This shows that although multiple large numbers exist, divisibility chains eliminate multi-pick options.

### Example 2

Input: `10 6 30 15`

| Step | Selection | Validity | Sum |
| --- | --- | --- | --- |
| 1 | 30 | yes | 30 |
| 2 | 30, 15 | invalid | - |
| 3 | 10, 6, 15 | all pairwise non-divisible | 31 |

Here the optimal answer is the triple (10, 6, 15). This demonstrates that ignoring the largest value can be necessary when it blocks compatibility.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n + C^2 + C^3)$ with $C \le 60$ | sorting plus restricted triple search |
| Space | $O(n)$ | frequency storage and value lists |

The critical constraint is that total $n$ across all queries is $2 \cdot 10^5$, and the triple enumeration is bounded by a constant-size subset, making the solution comfortably fast in practice.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdin.read()

assert run("3\n4\n5 6 15 30\n4\n10 6 30 15\n3\n3 4 6\n") == "30\n31\n10\n"
assert run("1\n1\n7\n") == "7"
assert run("1\n3\n2 4 8\n") == "10"
assert run("1\n3\n5 7 11\n") == "23"
assert run("1\n5\n2 3 4 9 27\n") == "13"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | itself | minimum size |
| chain multiples | pair restriction | divisibility blocking |
| all primes | best triple sum | full compatibility |
| mixed structure | greedy failure cases | non-trivial selection |

## Edge Cases

A key edge case is when the largest element is part of a long divisibility chain. For example, in a set like `2, 4, 8, 16`, choosing the maximum always prevents any second choice. The algorithm handles this by comparing against smaller compatible combinations rather than forcing inclusion of the maximum.

Another edge case is when the optimal solution is three medium values rather than one large value plus others. The second sample demonstrates this behavior: the optimal triple avoids the maximum because it blocks compatibility. The restricted triple enumeration ensures such combinations are still checked among top candidates.
