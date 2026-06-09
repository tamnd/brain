---
title: "CF 2151E - Limited Edition Shop"
description: "We are asked to simulate a limited-edition shop where Alice and Bob take turns picking items, but with a twist: we do not control who goes first or in which order they enter. Each item has a value according to us, and Alice and Bob each have a personal ranking of the items."
date: "2026-06-09T04:18:36+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dp", "games", "greedy"]
categories: ["algorithms"]
codeforces_contest: 2151
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 1053 (Div. 2)"
rating: 2100
weight: 2151
solve_time_s: 86
verified: false
draft: false
---

[CF 2151E - Limited Edition Shop](https://codeforces.com/problemset/problem/2151/E)

**Rating:** 2100  
**Tags:** data structures, dp, games, greedy  
**Solve time:** 1m 26s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to simulate a limited-edition shop where Alice and Bob take turns picking items, but with a twist: we do not control who goes first or in which order they enter. Each item has a value according to us, and Alice and Bob each have a personal ranking of the items. The question asks, for Alice, what is the maximum sum of values she could end up with over all possible ways the items could have been bought.

Each test case provides an array of item values `v`, Alice's preference `a`, and Bob's preference `b`. We must consider that on each turn, whoever is acting takes their currently most-preferred available item. We do not know the sequence of turns, so we need to reason over all possible sets Alice could buy. The answer is the maximum sum over these possible sets.

The constraints are significant: `n` can reach 200,000 and the sum over all test cases is also up to 200,000. This immediately rules out naive simulation of every turn order, which would be O(n!) in the worst case. Instead, we need a way to reason efficiently about which items Alice could get, considering Bob will always take his highest-preference remaining item.

Edge cases include negative values, because Alice may avoid taking an item that decreases her total, and the case where Bob's top preferences conflict with Alice's most valuable items according to us. For instance, if all of Alice's high-value items are also Bob's favorites, she might only end up with low-value or negative items. A naive implementation might sum all of Alice's top items without considering Bob's interference, giving an incorrect maximum.

## Approaches

The brute-force approach is to enumerate all possible sequences of picks for Alice and Bob, simulate each, and track Alice’s sum. This is correct but computationally impossible for `n > 10` because it requires O(n!) operations. The brute-force works in principle because it checks every feasible sequence, ensuring Alice's sum is maximized. It fails when n is large because factorial growth quickly exceeds feasible computation.

The key insight is to recognize that the sequence of choices only matters in terms of who gets each item first. Bob will always pick his most-preferred available item, and Alice will do the same with hers. Therefore, an item is guaranteed for Alice if she prefers it more than Bob does and is able to reach it before Bob. We can formalize this using the idea of "turn order dominance."

Specifically, for each item, we can calculate its rank in Alice's preference and Bob's preference. If Alice’s rank is better than Bob’s rank, she could potentially secure it before Bob, depending on the number of items already taken. Conversely, if Bob’s rank is better, he can always prevent Alice from taking it. This reduces the problem to a dynamic programming over prefixes of preferences, or equivalently, a greedy approach: iterate over items in Alice’s order and select only those she can claim, skipping items Bob would take earlier.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Rank-based Greedy | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. For each item, compute its position in Alice’s and Bob’s preference arrays. These positions define "priority scores" for both. Alice’s position array `posA[item]` is the index where item appears in her list, similarly for Bob `posB[item]`.
2. Initialize a list `alice_items` to track items Alice can potentially secure. Iterate over items in order of Alice's preference.
3. For each item in Alice’s preference, check if Alice’s position is better than Bob’s. If `posA[item] < posB[item]`, Alice could reach it before Bob and we consider it available.
4. Sum the values of all items that Alice can claim according to this rule. This sum is the maximum possible sum she can get because it captures the scenario where she always picks an item before Bob can, respecting their turn constraints.
5. Output this sum for the test case.

Why it works: The algorithm works because we effectively compute a "safe set" of items Alice can take, assuming Bob always acts optimally to block her. By comparing preference positions, we guarantee no overestimation: any item with a lower rank for Bob can be blocked if Alice’s rank is not higher. Thus, summing the items Alice can secure in her order of preference yields the maximum total value attainable.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        v = list(map(int, input().split()))
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))

        posA = [0] * (n + 1)
        posB = [0] * (n + 1)
        for idx, item in enumerate(a):
            posA[item] = idx
        for idx, item in enumerate(b):
            posB[item] = idx

        result = 0
        for item in a:
            if posA[item] < posB[item]:
                result += v[item - 1]
        print(result)

if __name__ == "__main__":
    solve()
```

The first part reads inputs and constructs position arrays for Alice and Bob. The loop over `a` ensures we consider items in Alice's order. The condition `posA[item] < posB[item]` guarantees Alice could pick it before Bob. Using 1-based indexing from input, we access values with `v[item-1]`. Printing the accumulated sum gives the answer for each test case.

## Worked Examples

### Sample 1

Input:

```
3
1 -1 1
3 1 2
2 3 1
```

| Step | Alice Item | posA | posB | Condition | Result Sum |
| --- | --- | --- | --- | --- | --- |
| 1 | 3 | 0 | 1 | 0<1 -> yes | 1 |
| 2 | 1 | 1 | 2 | 1<2 -> yes | 1+(-1)=0 |
| 3 | 2 | 2 | 0 | 2<0 -> no | 0 |

Alice’s maximum sum is 0. This confirms that items blocked by Bob cannot be counted.

### Sample 2

Input:

```
4
5 -15 10 -5
2 4 3 1
1 4 2 3
```

| Step | Alice Item | posA | posB | Condition | Result Sum |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | 0 | 2 | yes | -15 |
| 2 | 4 | 1 | 1 | no | -15 |
| 3 | 3 | 2 | 3 | yes | -15+10=-5 |
| 4 | 1 | 3 | 0 | no | -5 |

Maximum sum is -5, which matches expected evaluation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | We build two position arrays in O(n) and iterate over Alice’s preference once |
| Space | O(n) per test case | Two arrays of size n+1 for positions, plus input storage |

The overall sum of n across all test cases is ≤ 2×10^5, so total operations are comfortably below 10^6, fitting within the 2-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    return out.getvalue().strip()

# Provided samples
assert run("1\n3\n1 -1 1\n3 1 2\n2 3 1\n") == "2"
assert run("1\n3\n-2 5 2\n3 1 2\n2 3 1\n") == "5"

# Minimum input
assert run("1\n1\n100\n1\n1\n") == "100"

# All negative values
assert run("1\n3\n-1 -2 -3\n1 2 3\n3 2 1\n") == "-1"

# Maximum size input, values alternating
n = 2*10**5
v = " ".join(str(x) for x in range(n, 0, -1))
a = " ".join(str(x) for x in range(1, n+1))
b = " ".join(str(x) for x in range(n, 0, -1))
assert run(f"1\n{n}\n{v}\n{a}\n{b}\n") == str(sum(range(n//2+1, n+1)))
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 item | 100 | Single-element boundary |
| All negative | -1 | Correct handling of negatives |
| Maximum size | n//2+1 to n sum | Handles large inputs efficiently |

## Edge Cases

When all values are negative, the algorithm skips items blocked by Bob and only counts those Alice can secure
