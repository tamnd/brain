---
title: "CF 919A - Supermarket"
description: "The task is to decide how to buy a fixed amount of apples while minimizing total cost, given multiple supermarkets with different pricing schemes. Each supermarket does not directly give a per-kilogram price."
date: "2026-06-15T12:24:50+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 919
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 460 (Div. 2)"
rating: 800
weight: 919
solve_time_s: 271
verified: true
draft: false
---

[CF 919A - Supermarket](https://codeforces.com/problemset/problem/919/A)

**Rating:** 800  
**Tags:** brute force, greedy, implementation  
**Solve time:** 4m 31s  
**Verified:** yes  

## Solution
## Problem Understanding

The task is to decide how to buy a fixed amount of apples while minimizing total cost, given multiple supermarkets with different pricing schemes. Each supermarket does not directly give a per-kilogram price. Instead, it offers a bundle price: paying a units of money buys b kilograms of apples. This implicitly defines a unit price of a/b, but the actual purchase must be done in whole supermarkets without mixing bundle sizes.

We are asked to buy exactly m kilograms in total, and we may choose any supermarket, potentially buying all m kilograms from a single one. The goal is to find the cheapest way to obtain m kilograms under these pricing rules.

The constraints matter in a simple way. The number of supermarkets n can be up to 5000, while m is at most 100. Each price pair a and b is small, bounded by 100. This immediately suggests that any algorithm that is linear or quadratic in n and m is acceptable, but anything exponential in m would be unnecessary because m is tiny. The structure also hints that each supermarket behaves independently, so the problem reduces to evaluating a simple expression per supermarket.

A subtle point that can mislead a naive approach is interpreting the price incorrectly. A common mistake is to assume we can only buy in multiples of b kilograms and that partial scaling is invalid in a way that prevents direct proportional reasoning. In fact, the cost scales linearly: if a supermarket charges a for b kilograms, then m kilograms from that same supermarket costs exactly a * (m / b). For example, if a = 3 and b = 4, then 5 kilograms cost 3 * 5 / 4 = 3.75. Another potential mistake is using integer division, which would silently truncate and produce incorrect results.

## Approaches

A brute-force interpretation would try to model purchasing decisions explicitly, perhaps thinking in terms of combining multiple supermarkets or splitting purchases into chunks. Since m is small, one might even consider dynamic programming over total kilograms, where dp[x] is the minimum cost to buy x kilograms. For each supermarket, we would attempt to transition from every state x to x + b repeatedly or consider fractional scaling indirectly. This leads to an unnecessary complication: for each supermarket we would simulate contributions to all states up to m, producing roughly O(n * m^2) work if done carefully, or worse if modeled less cleanly.

The key observation is that each supermarket is independent and does not interact with others. There is no advantage in mixing supermarkets within a single purchase strategy because we are not constrained by discrete bundles beyond linear scaling. Each supermarket simply offers a fixed rate per kilogram, so the problem reduces to computing m * (a / b) for every supermarket and taking the minimum.

This removes all combinatorial structure. We no longer need to consider combinations of supermarkets, only evaluate a simple expression per input line.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force DP over kilograms | O(n * m^2) | O(m) | Too slow / unnecessary |
| Direct evaluation per supermarket | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read n and m, which define how many supermarkets exist and how many kilograms must be purchased.
2. Initialize a variable best_cost to a very large number. This will track the smallest total cost found across all supermarkets.
3. For each supermarket, read a and b, representing the cost and quantity of a bundle.
4. Compute the effective cost for m kilograms from this supermarket using the proportional scaling formula m * a / b. This works because the price per kilogram is constant within each supermarket.
5. Compare this computed cost with best_cost and update best_cost if the new value is smaller.
6. After processing all supermarkets, output best_cost as a floating-point number.

### Why it works

Each supermarket defines a linear cost function in terms of kilograms purchased. Since there are no constraints on splitting across supermarkets or discounts for combinations, the minimum cost for the required amount is simply the minimum over all individual linear functions evaluated at m. The algorithm preserves the invariant that after processing i supermarkets, best_cost equals the minimum achievable cost among those i options. Because every supermarket is considered exactly once and independently, no valid candidate is missed.

## Python Solution

```
PythonRun
```

The solution reads input line by line and maintains a single minimum value. Each supermarket contributes one computed candidate cost, and we never store unnecessary data.

The key implementation detail is using floating-point division. Using integer division would destroy precision and produce incorrect answers. Multiplying m first ensures we avoid premature truncation.

## Worked Examples

### Sample 1

Input:

```

```

We evaluate each supermarket:

| Supermarket | a | b | Cost for 5 kg (5 * a / b) | Best so far |
| --- | --- | --- | --- | --- |
| 1 | 1 | 2 | 2.5 | 2.5 |
| 2 | 3 | 4 | 3.75 | 2.5 |
| 3 | 1 | 3 | 1.6666667 | 1.6666667 |

The third supermarket is cheapest, so we choose it.

This confirms that the algorithm correctly evaluates all options independently and selects the minimum.

### Sample 2 (constructed)

Input:

```

```

| Supermarket | a | b | Cost for 1 kg (1 * a / b) | Best so far |
| --- | --- | --- | --- | --- |
| 1 | 98 | 99 | 0.989898... | 0.989898... |
| 2 | 1 | 2 | 0.5 | 0.5 |
| 3 | 5 | 10 | 0.5 | 0.5 |
| 4 | 7 | 7 | 1.0 | 0.5 |

The second and third supermarkets tie, and the algorithm correctly keeps the minimum.

This shows the algorithm handles ties and fractional comparisons correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each supermarket is processed once with constant work |
| Space | O(1) | Only a single variable is maintained |

The constraints allow up to 5000 supermarkets, so a single pass is easily fast enough. Memory usage remains constant regardless of input size.

## Test Cases

```
PythonRun
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 / 1 1 | 1.0 | minimal edge case |
| equal ratios | same value | tie handling |
| skewed costs | correct min selection | comparison correctness |
| fractional cases | precise division | floating accuracy |

## Edge Cases

One important edge case is when m = 1. In this case, the answer should reduce directly to the smallest a/b ratio among all supermarkets. The algorithm handles this naturally because it always computes m * a / b, which becomes a / b when m = 1.

Another edge case is when multiple supermarkets have identical unit prices but different bundle sizes. For example, 1/2 and 2/4 both represent the same rate. The algorithm treats them equally because both evaluate to the same floating-point value, and the minimum remains stable.

A final subtle case is precision sensitivity. When values are very close, floating-point comparisons still work correctly under the required 1e-6 tolerance because the computation involves only a single multiplication and division per entry, which is numerically stable for the given constraints.
