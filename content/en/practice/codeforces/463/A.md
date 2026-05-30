---
title: "CF 463A - Caisa and Sugar"
description: "We are given a fixed amount of money expressed in dollars, and a list of sugar options in a supermarket. Each option has a price written as dollars and cents."
date: "2026-05-30T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation"]
categories: ["algorithms"]
codeforces_contest: 463
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 264 (Div. 2)"
rating: 1200
weight: 463
solve_time_s: 60
verified: true
draft: false
---

[CF 463A - Caisa and Sugar](https://codeforces.com/problemset/problem/463/A)

**Rating:** 1200  
**Tags:** brute force, implementation  
**Solve time:** 1m  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a fixed amount of money expressed in dollars, and a list of sugar options in a supermarket. Each option has a price written as dollars and cents. Caisa can choose exactly one type of sugar, pay for it using his available money, and receive change if he has more money than required. The unusual detail is that the store returns part of the change in sweets instead of cents, and the number of sweets he receives is exactly equal to the number of cents in his change, capped implicitly by the fact that cents are always normalized so that at most 99 cents remain after converting 100 cents into a dollar.

The task is to choose a single sugar type that Caisa can afford and maximize the number of sweets he gets back in change. If no sugar type is affordable, the answer is -1.

The input size is small: at most 100 options. This immediately rules out any concern about performance; even a double loop over all items is trivial. A linear scan over the list is sufficient.

A subtle edge case appears when all items are too expensive in total. For example, if Caisa has 5 dollars and every sugar costs at least 6 dollars, then no purchase is possible and the answer must be -1. Another case is when multiple items are affordable but one has a lower price while another yields more cents in change; the optimal choice is not the cheapest item but the one maximizing the remainder in cents after subtraction.

A concrete example that can confuse a naive approach is choosing the minimum cost item instead of maximizing change. Suppose Caisa has 10 dollars. One item costs 9 dollars 70 cents and another costs 7 dollars 0 cents. The first yields only 30 cents change, while the second yields 300 cents change, which corresponds to 3 dollars and 0 cents, so 0 sweets. Without carefully computing the remainder in cents, it is easy to compare incorrectly.

## Approaches

A brute-force solution naturally follows from the constraints. We iterate over each sugar type, check if Caisa can afford it, compute the change in cents, and track the maximum remainder. Since there are at most 100 items, this is at most 100 arithmetic checks, which is negligible.

The key observation is that the problem is entirely local to each item. There is no interaction between choices, no combinatorial structure, and no need to optimize across multiple selections. Each sugar type independently produces a candidate value: how many cents remain after subtracting its price from the available money.

We convert everything into cents to avoid floating point reasoning. If Caisa has s dollars, that becomes 100s cents. Each item costs 100xᵢ + yᵢ cents. If the cost exceeds available money, we skip it. Otherwise, we compute the remainder and update the best answer.

The brute-force approach is already optimal because the input size is constant-bounded and small.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(1) | Accepted |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Convert the available money into cents by computing 100 * s. This ensures all comparisons happen in a single unit system, removing any ambiguity between dollars and cents.
2. Initialize a variable best to -1. This will store the maximum cents in change among all affordable options.
3. For each sugar type, convert its price into cents using 100 * xᵢ + yᵢ. This gives a comparable quantity in the same unit as the budget.
4. If the price exceeds the available money, skip this option since it cannot be purchased.
5. Otherwise compute the change as (budget - price). Extract the cents part using modulo 100, since sweets correspond to cents in the remaining change after normalization.
6. Update best if this value is larger than the current best.
7. After processing all items, output best. If no valid item was found, best remains -1.

### Why it works

Each sugar type produces exactly one independent candidate value, which is the number of cents left after purchase. Since Caisa buys exactly one item, the problem reduces to selecting the maximum value among a finite set of independent evaluations. Converting everything into cents preserves ordering and ensures no loss of precision. The algorithm maintains the invariant that best is always the maximum cents-in-change seen among all affordable items processed so far, so the final value is globally optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    n, s = map(int, input().split())
    budget = s * 100

    best = -1

    for _ in range(n):
        x, y = map(int, input().split())
        cost = x * 100 + y

        if cost <= budget:
            change = budget - cost
            sweets = change % 100
            if sweets > best:
                best = sweets

    print(best)

if __name__ == "__main__":
    main()
```

The solution first normalizes the budget into cents so that comparisons are consistent. Each item is also converted into cents before any arithmetic is done, avoiding mixed-unit mistakes.

The key implementation detail is using modulo 100 on the remaining change. Since sweets correspond to cents in the leftover amount after full-dollar normalization, only the remainder after dividing by 100 matters. Tracking only that value avoids unnecessary computation.

Edge handling is implicit: if no item satisfies cost <= budget, best never updates from -1.

## Worked Examples

### Example 1

Input:

```
5 10
3 90
12 0
9 70
5 50
7 0
```

We track budget = 1000 cents.

| Item | Cost (cents) | Affordable | Change (cents) | Sweets | Best |
| --- | --- | --- | --- | --- | --- |
| 3 90 | 390 | yes | 610 | 10 | 10 |
| 12 0 | 1200 | no | - | - | 10 |
| 9 70 | 970 | yes | 30 | 30 | 30 |
| 5 50 | 550 | yes | 450 | 50 | 50 |
| 7 0 | 700 | yes | 300 | 0 | 50 |

Final answer is 50.

This trace shows how the maximum does not correspond to the cheapest item but to the best remainder modulo 100.

### Example 2

Input:

```
3 2
3 0
2 50
5 99
```

Budget = 200 cents.

| Item | Cost | Affordable | Change | Sweets | Best |
| --- | --- | --- | --- | --- | --- |
| 3 0 | 300 | no | - | - | -1 |
| 2 50 | 250 | no | - | - | -1 |
| 5 99 | 599 | no | - | - | -1 |

Final answer is -1.

This confirms the handling of the “no valid purchase” case.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each sugar type is processed once with constant-time arithmetic |
| Space | O(1) | Only a few integer variables are used |

The input constraints cap n at 100, so even linear scanning is effectively instantaneous. Memory usage is constant regardless of input size.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, s = map(int, input().split())
    budget = s * 100

    best = -1

    for _ in range(n):
        x, y = map(int, input().split())
        cost = x * 100 + y
        if cost <= budget:
            best = max(best, (budget - cost) % 100)

    return str(best)

# provided sample
assert run("5 10\n3 90\n12 0\n9 70\n5 50\n7 0\n") == "50"

# minimum case, no affordable item
assert run("1 1\n2 0\n") == "-1"

# exact budget match, zero change
assert run("2 5\n5 0\n3 0\n") == "0"

# multiple options, best is not cheapest
assert run("3 10\n9 99\n9 50\n8 0\n") == "50"

# all affordable, check modulo behavior
assert run("3 10\n1 10\n1 20\n1 30\n") == "90"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| no affordable item | -1 | correct handling of impossibility |
| exact match | 0 | zero-change case |
| mixed prices | 50 | selection by max remainder, not cost |
| all affordable | 90 | correct modulo extraction |

## Edge Cases

One edge case is when all items are too expensive. In that situation, the loop never updates the initial value -1, and the output remains -1. For example, with budget 100 cents and an item costing 200 cents, the check fails and no change computation is performed, correctly preserving the sentinel.

Another case is when multiple items are affordable but produce identical remainders. For instance, two items may both leave 30 cents. The algorithm handles this naturally because it only tracks the maximum value, and equal values do not change the result.

A final case is when the change is a multiple of 100 cents. In that case the modulo operation yields 0, which correctly represents zero sweets.
