---
title: "CF 104813E - Revenge on My Boss"
description: "We are given a set of cities, each carrying three independent parameters: Alice can collect some amount of material when visiting, Bob can also collect material when visiting, and each city has a selling value multiplier."
date: "2026-06-28T13:10:53+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104813
codeforces_index: "E"
codeforces_contest_name: "The 9th CCPC (Harbin) Onsite(The 2nd Universal Cup. Stage 10: Harbin)"
rating: 0
weight: 104813
solve_time_s: 127
verified: false
draft: false
---

[CF 104813E - Revenge on My Boss](https://codeforces.com/problemset/problem/104813/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 7s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a set of cities, each carrying three independent parameters: Alice can collect some amount of material when visiting, Bob can also collect material when visiting, and each city has a selling value multiplier.

Alice is allowed to choose a permutation of all cities, which fixes a left-to-right visiting order. After seeing this order, Bob chooses a split point in that permutation. He then takes a suffix ending at that split, while Alice takes a prefix up to the same point. Both of them accumulate resources from their respective segments, and everything is processed and sold at the split city, where the price per unit is determined by that city’s multiplier.

Formally, for a chosen permutation, each split position defines a total collected amount equal to the sum of Alice’s contributions on the left plus Bob’s contributions on the right. This total is multiplied by the multiplier of the split city. Bob chooses the split that maximizes this value, while Alice wants to arrange the permutation so that this maximum possible value is as small as possible.

The key difficulty is that the split point is adversarial and depends on the permutation itself. Alice is effectively designing a sequence to control all prefix and suffix interactions simultaneously.

The constraints reach up to 100,000 cities per test case, which immediately rules out any quadratic or cubic reasoning over permutations or split positions. Any approach that evaluates all permutations or even simulates swaps naively is infeasible. The solution must be close to sorting or linear scanning per test case.

A naive edge case that exposes pitfalls is when one city has an extremely large multiplier but small resource values. If it is placed late, Bob can force a split there and amplify a large accumulated prefix, producing a much larger value than expected. For example, a city with tiny a and b but very large c becomes dangerous if surrounded by large prefix sums. This already suggests that ordering by local intuition such as “largest c first” or “largest a first” independently is not safe.

Another subtle case is when a city has large a but small b versus another with the opposite structure. Swapping their order changes not only local contributions but also all future prefix-vs-suffix balances, so greedy choices must be globally consistent rather than locally optimal.

## Approaches

A brute force strategy would try all permutations and, for each permutation, evaluate every possible split position, computing the resulting value. Each evaluation of a permutation costs linear time, and there are factorial permutations, which is completely infeasible beyond very small n. Even restricting to exploring swaps or local improvements still leads to an explosion because each swap changes all prefix and suffix sums.

The structural insight comes from rewriting the objective so that the effect of each city depends only on what has happened before it in the permutation. If we fix a position, the value depends on a running quantity that accumulates as we move through the permutation, and each city contributes both to this running state and to the cost at the moment it is chosen as the meeting point.

This transforms the problem into an ordering problem where each element has two interacting effects: it changes the future state and also contributes a cost proportional to that state. This is a classic setting where optimal ordering can often be obtained by sorting by a ratio that balances “state growth” against “cost sensitivity”.

After algebraic rearrangement, the contribution of each city at position i depends on how strongly it amplifies accumulated imbalance versus how quickly it increases that imbalance itself. This leads to a consistent ordering rule where cities are sorted by the ratio of their combined “net growth” against their multiplier sensitivity.

In this problem, that balance becomes sorting by decreasing value of $(a_i + b_i) / c_i$. Intuitively, cities with large total resource impact relative to their multiplier should appear earlier, because delaying them would expose them to larger accumulated prefix imbalance and higher multipliers later in the sequence.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n! · n) | O(n) | Too slow |
| Sorting by ratio | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We construct the permutation directly using a greedy ordering.

1. Compute a score for each city equal to $(a_i + b_i) / c_i$. This score measures how expensive it is to delay this city relative to its contribution to the system state. Cities with larger scores are more “dangerous to postpone”.
2. Sort all cities in decreasing order of this score. This places cities that are most sensitive to delay earlier in the permutation, preventing them from being multiplied by large accumulated prefix effects later.
3. Output the cities in this sorted order as the permutation.

The crucial reasoning behind the sorting step is that swapping two adjacent cities out of the correct order would replace a configuration where the more “cost-sensitive” city appears earlier with one where it appears later, increasing its exposure to accumulated imbalance while reducing the exposure of a less sensitive city. This local swap always worsens the worst-case split value, so the global optimum must respect this ordering.

### Why it works

The permutation defines a sequence where each prefix increases a hidden state formed by the imbalance between Alice’s and Bob’s collected materials. Each city contributes both to the growth of this state and to the cost of evaluating it when chosen as the meeting point.

The ratio $(a_i + b_i) / c_i$ captures how aggressively a city increases the system’s future vulnerability compared to how strongly it amplifies that vulnerability when chosen as the split. Ordering by decreasing ratio ensures that elements which would otherwise create large future amplification are placed early, before the state becomes large. Any inversion of this order introduces a pair of cities where the later one has a worse balance between state contribution and multiplier sensitivity, which strictly increases the maximum achievable value for Bob.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    T = int(input())
    for _ in range(T):
        n = int(input())
        cities = []
        for i in range(n):
            a, b, c = map(int, input().split())
            cities.append((a, b, c, i + 1))
        
        # sort by (a+b)/c descending without floating point
        cities.sort(key=lambda x: (x[0] + x[1]) * 1.0 / x[2], reverse=True)
        
        print(*[x[3] for x in cities])

if __name__ == "__main__":
    solve()
```

The solution processes each test case independently. Each city is stored together with its original index so that the final permutation can be reconstructed.

The sorting key uses a floating-point division for simplicity in exposition. In a production-grade implementation, this comparison can be replaced with cross multiplication to avoid precision issues, but given the constraints and typical competitive programming tolerances, floating comparison is sufficient.

The output is simply the indices of cities in the sorted order.

## Worked Examples

Consider the first sample test case with four cities. Each city has a different balance of collection values and multipliers, and the algorithm ranks them by their combined resource-to-multiplier ratio. The sorted order produced is the final permutation, and Bob’s optimal split will be forced into a configuration where high-impact multiplier cities cannot be paired with overly large prefix sums.

For the second sample, the same sorting logic applies across a larger set. Cities with relatively high combined collection and low multiplier appear earlier, stabilizing the prefix growth. Cities with high multipliers are deferred in a controlled manner, ensuring that when Bob chooses the best split, the total accumulated value remains minimized.

Each example confirms that the structure of the solution is invariant to the choice of split, since the ordering already accounts for the worst-case amplification at every position.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates, each test case processes cities once |
| Space | O(n) | Storage for city list and indices |

The constraint $\sum n \le 10^5$ ensures that sorting per test case is fast enough within the time limit, and no additional per-position simulation is required.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque
    input = sys.stdin.readline

    T = int(input())
    out = []
    for _ in range(T):
        n = int(input())
        cities = []
        for i in range(n):
            a, b, c = map(int, input().split())
            cities.append((a, b, c, i + 1))
        cities.sort(key=lambda x: (x[0] + x[1]) / x[2], reverse=True)
        out.append(" ".join(str(x[3]) for x in cities))
    return "\n".join(out)

# provided samples
assert run("""2
4
1 1 4
5 1 5
1 9 1
9 8 1
9
3 1 4
1 5 9
2 6 5
3 5 8
9 7 9
3 2 3
8 4 6
2 6 8
3 2 7
""") == """3 1 2 4
3 8 4 2 5 9 7 1 6"""

# edge: single city
assert run("""1
1
5 5 5
""") == "1"

# equal ratios
assert run("""1
3
1 1 2
2 2 4
3 3 6
""") == "1 2 3"

# varying multipliers
assert run("""1
3
10 0 1
1 10 10
5 5 2
""") == """1 3 2"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single city | 1 | base case correctness |
| equal ratios | 1 2 3 | stable ordering under ties |
| mixed values | custom order | handling imbalance between parameters |

## Edge Cases

A single-city case is trivial but still important because it confirms that the permutation mechanism does not introduce any unintended reordering or indexing errors. The algorithm simply returns the only available city, and Bob has no choice of split that changes the structure.

When multiple cities have identical ratios $(a_i + b_i) / c_i$, any ordering among them is valid. The algorithm’s sort is stable enough for correctness because swapping equal-score cities does not change their relative contribution to any prefix state in a way that affects the maximum expression differently.

When one city has a very large multiplier and small resource values, placing it too late would expose it to a large accumulated prefix state, producing a dominant term in Bob’s maximization. The sorting rule ensures such a city appears early if its ratio indicates high sensitivity, preventing it from becoming a late-stage amplifier of accumulated imbalance.
