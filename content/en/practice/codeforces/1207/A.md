---
title: "CF 1207A - There Are Two Types Of Burgers"
description: "We are given a small restaurant model where each query describes available ingredients and selling prices for two kinds of burgers. One burger requires buns plus beef, the other requires buns plus chicken."
date: "2026-06-13T16:19:12+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "greedy", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1207
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 71 (Rated for Div. 2)"
rating: 800
weight: 1207
solve_time_s: 178
verified: true
draft: false
---

[CF 1207A - There Are Two Types Of Burgers](https://codeforces.com/problemset/problem/1207/A)

**Rating:** 800  
**Tags:** brute force, greedy, implementation, math  
**Solve time:** 2m 58s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a small restaurant model where each query describes available ingredients and selling prices for two kinds of burgers. One burger requires buns plus beef, the other requires buns plus chicken. Every burger consumes exactly two buns, and each type consumes its own ingredient.

For each query, we must decide how many hamburgers and how many chicken burgers to produce so that the total number of buns is respected, and the total revenue is maximized. The limiting resources are buns, beef patties, and chicken cutlets, and each query is independent.

The constraints are small: each quantity is at most 100, and there are at most 100 queries. This means any solution up to roughly a few million operations is trivial to fit inside time limits. Even approaches that try all reasonable distributions of burgers are feasible, but there is an even simpler structure that avoids enumeration entirely.

A naive mistake in this problem is to assume we should always prioritize the more expensive burger. That is not always correct if the expensive burger consumes a resource that is more restrictive. For example, if buns are plentiful but beef is scarce while chicken is abundant, prioritizing hamburgers might waste buns that could have been used for more valuable chicken burgers.

Another subtle edge case appears when both burger types have equal price. In that case, any allocation that respects resource constraints is optimal, but a greedy strategy that overcommits to one type might reduce feasibility of the other without improving profit.

## Approaches

A straightforward brute-force approach is to try all possible numbers of hamburgers and chicken burgers. Since each burger consumes two buns, if we fix the number of hamburgers, the remaining buns and ingredients determine how many chicken burgers we can produce. For each choice of hamburger count from zero up to its maximum feasible value, we compute the corresponding chicken burger count and evaluate profit. This is correct because it explores all valid distributions of buns between the two burger types.

The problem is that this still involves iterating over up to 100 choices per query, and then computing constraints inside the loop. While this is already small enough, it is unnecessary because the structure of the problem is simpler: both burgers consume the same shared resource (buns), while the other ingredients are independent constraints. The key observation is that each burger type can be treated as consuming a limited capacity, and the only real coupling is the bun constraint.

The key insight is that buns are the only shared bottleneck. Each burger consumes exactly two buns, so the total number of burgers is bounded by `b // 2`. Once we decide how many burgers of one type to produce, the rest can be assigned to the other type up to its ingredient limits. Since there are only two types, the optimal strategy reduces to trying only two meaningful configurations: prioritize hamburgers first or prioritize chicken burgers first. One of these greedy choices must be optimal because swapping one burger type for another only depends on marginal profit per shared bun, and there are no interactions beyond that.

This reduces the problem to evaluating two greedy allocations and taking the maximum.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(b) per query | O(1) | Accepted |
| Optimal | O(1) per query | O(1) | Accepted |

## Algorithm Walkthrough

We compute the best profit by testing both possible priorities.

1. First compute how many hamburgers we can make if we prioritize them. This is limited by beef and buns, so it is `min(p, b // 2)`. This represents the maximum safe commitment to hamburgers without violating constraints.
2. Subtract the buns used by hamburgers, leaving `b - 2 * hamburgers` buns for chicken burgers.
3. Compute chicken burgers as `min(f, remaining_buns // 2)`. This ensures we do not exceed chicken supply or bun availability.
4. Compute total profit as `hamburgers * h + chicken_burgers * c`.
5. Repeat the same process but reverse priorities: first maximize chicken burgers, then use remaining buns for hamburgers.
6. Take the maximum profit between the two strategies.

The reason we explicitly test both directions is that the greedy decision depends on which burger type gets first access to the shared bun resource.

### Why it works

The only coupling between the two choices is the bun constraint, and both burger types consume buns identically. This means any solution corresponds to splitting `b // 2` burger slots between two types under independent caps `p` and `f`. The profit is linear in the number of burgers of each type, so an optimal solution must lie at an extreme allocation where one type is filled as much as possible first, and the remaining capacity is assigned to the other type. Any intermediate swap can only move units between the two types without changing total buns, and checking both extreme directions guarantees the maximum is captured.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve_one(b, p, f, h, c):
    buns = b // 2

    # case 1: prioritize hamburgers
    ham1 = min(p, buns)
    buns_left1 = buns - ham1
    chick1 = min(f, buns_left1)
    profit1 = ham1 * h + chick1 * c

    # case 2: prioritize chicken burgers
    chick2 = min(f, buns)
    buns_left2 = buns - chick2
    ham2 = min(p, buns_left2)
    profit2 = chick2 * c + ham2 * h

    return max(profit1, profit2)

t = int(input())
for _ in range(t):
    b, p, f = map(int, input().split())
    h, c = map(int, input().split())
    print(solve_one(b, p, f, h, c))
```

The solution first reduces buns into usable burger slots using integer division by 2, since each burger consumes two buns. It then simulates both greedy orderings explicitly. Each ordering carefully respects both ingredient limits and remaining bun capacity.

The only subtle point is ensuring we always recompute remaining buns after choosing one type first. Forgetting this step leads to overcounting and invalid allocations.

## Worked Examples

### Example 1

Input:

```
b = 15, p = 2, f = 3
h = 5, c = 10
```

| Step | Ham priority | Chicken priority |
| --- | --- | --- |
| buns | 7 | 7 |
| first type | 2 ham | 3 chicken |
| remaining buns | 3 | 1 |
| second type | 1 chicken | 1 ham |
| profit | 2_5 + 1_10 = 20 | 3_10 + 1_5 = 35 |

The optimal strategy is chicken-first, which yields 35.

This shows that prioritizing the higher-priced item (chicken) leads to better use of limited buns in this configuration.

### Example 2

Input:

```
b = 7, p = 5, f = 2
h = 10, c = 12
```

| Step | Ham priority | Chicken priority |
| --- | --- | --- |
| buns | 3 | 3 |
| first type | 3 ham | 2 chicken |
| remaining buns | 0 | 1 |
| second type | 0 chicken | 0 ham |
| profit | 30 | 24 |

Here, hamburger-first is optimal because it consumes buns in a way that better aligns with available capacity.

These examples confirm that the correct ordering depends on both price and availability, not just price alone.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each query performs constant-time arithmetic operations |
| Space | O(1) | No auxiliary data structures are used |

The solution easily fits within constraints since even at 100 queries, the total number of operations is negligible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    def solve():
        t = int(input())
        out = []
        for _ in range(t):
            b, p, f = map(int, input().split())
            h, c = map(int, input().split())

            buns = b // 2

            ham1 = min(p, buns)
            chick1 = min(f, buns - ham1)
            profit1 = ham1 * h + chick1 * c

            chick2 = min(f, buns)
            ham2 = min(p, buns - chick2)
            profit2 = chick2 * c + ham2 * h

            out.append(str(max(profit1, profit2)))

        return "\n".join(out)

    return solve()

# provided samples
assert run("""3
15 2 3
5 10
7 5 2
10 12
1 100 100
100 100
""") == """40
34
0"""

# custom cases
assert run("""1
1 10 10
5 7
""") == "0", "minimum buns case"

assert run("""1
100 50 50
1 1
""") == "50", "symmetric low price case"

assert run("""1
10 100 0
10 1
""") == "50", "single type only"

assert run("""1
10 5 5
10 20
""") == "100", "prefer chicken due to price"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 bun case | 0 | impossibility handling |
| symmetric resources | 50 | balanced allocation |
| single type only | 50 | one-sided production |
| price skew | 100 | greedy ordering choice |

## Edge Cases

A minimal bun case like `b = 1` immediately forces the answer to zero because no burger can be formed. The algorithm handles this through `b // 2`, which becomes zero, ensuring both strategies produce zero hamburgers and zero chicken burgers.

A case where one ingredient is zero, for example `p = 0`, forces all production into chicken burgers. In the algorithm, `min(p, buns)` correctly becomes zero, so the first strategy naturally assigns all capacity to chicken without requiring special handling.

When both burger prices are equal, the algorithm still works because both greedy orders produce valid allocations. Since profit is symmetric, either ordering yields the same result, and taking the maximum preserves correctness without needing tie-breaking logic.
