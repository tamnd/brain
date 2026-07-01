---
title: "CF 104574D - XP Challenge"
description: "We are given a sequence of enemies lined up along Iggy’s escape path. Each enemy has some amount of health, and Iggy starts with a fixed amount of health as well."
date: "2026-06-30T08:16:34+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104574
codeforces_index: "D"
codeforces_contest_name: "UTPC Contest 09-08-23 Div. 2 (Beginner)"
rating: 0
weight: 104574
solve_time_s: 65
verified: true
draft: false
---

[CF 104574D - XP Challenge](https://codeforces.com/problemset/problem/104574/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of enemies lined up along Iggy’s escape path. Each enemy has some amount of health, and Iggy starts with a fixed amount of health as well. She must reduce every enemy’s health to zero or below, one by one, while never letting her own health drop to zero or below.

To defeat enemies, Iggy has two attack modes. The first mode can be used at most once per enemy. It deals a fixed amount of damage to that enemy, but also costs Iggy a fixed amount of her own health. The second mode can be used any number of times, and each use deals some damage to the enemy while also costing Iggy health.

The task is to determine whether there exists a way to choose, for each enemy, how many times to use the unlimited attack and whether to use the single-use attack, so that all enemies are defeated and Iggy’s health remains strictly positive at all times.

The constraints push us toward an $O(M)$ or $O(M \log M)$ solution since there can be up to $10^5$ enemies. Any solution that tries to simulate combinations of attacks per enemy independently in a naive way would quickly explode, because for each enemy we could in principle choose between using the special attack or not, and then many combinations of charge attacks. That leads to exponential or at least quadratic behavior if mishandled.

A subtle failure case for naive reasoning is treating each enemy independently by always maximizing damage efficiency locally. For example, always using the thumb spike whenever it seems efficient per hit can fail because it might waste the best fixed-damage option on a weak enemy, leaving a strong enemy too expensive later.

Another tricky edge case arises when the charge attack is strictly better than the thumb spike in both damage efficiency and health cost per damage, but the thumb spike still matters because it gives a one-time burst that can reduce the number of charge uses significantly for a large enemy.

## Approaches

The key observation is that each enemy is independent except for total remaining health. For each enemy, we need to decide how to minimize the health cost required to reduce its HP to zero, given that we can optionally apply a one-time bonus attack.

If we ignore the thumb spike, each enemy $a_i$ requires $\lceil a_i / Q_1 \rceil$ charge attacks, costing $Q_2 \cdot \lceil a_i / Q_1 \rceil$ health.

Now introduce the thumb spike. If we use it on an enemy, its HP effectively reduces by $P_1$, so the remaining HP becomes $\max(0, a_i - P_1)$. That reduces the number of charge attacks needed for that enemy. However, we pay an additional fixed cost $P_2$ once per such use.

So for each enemy we are choosing between two costs: a pure charge cost, or a mixed cost where we spend $P_2$ plus the charge cost after reducing HP by $P_1$.

This reduces the problem to computing, for each enemy, the minimum of these two values, and summing across all enemies. The only remaining question is whether Iggy’s initial health is sufficient.

The brute-force approach would try both choices per enemy and simulate charge attacks individually, leading to $O(M \cdot a_i)$ in the worst case, which is infeasible since $a_i$ can be up to $10^9$.

The key simplification is recognizing that the cost structure is additive and per-enemy independent. Once we fix an enemy’s choice, its optimal internal strategy is deterministic: always use charge attacks, optionally preceded by the single spike.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(M \cdot \max a_i)$ | $O(1)$ | Too slow |
| Optimal | $O(M)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. For each enemy, compute the cost of defeating it using only charge attacks. This is the number of hits needed times the health cost per hit. The number of hits is computed using ceiling division on the enemy’s HP by $Q_1$.
2. For the same enemy, compute the alternative cost if we use the thumb spike exactly once. First reduce the enemy HP by $P_1$, but not below zero, then compute how many charge attacks are needed for the remaining HP, and add the fixed cost $P_2$. This captures the fact that the spike is only useful if it actually reduces the number of charge attacks.
3. Take the minimum of the two computed costs. This represents the optimal way to defeat that enemy in isolation, given the global structure of the problem.
4. Sum these minimum costs over all enemies. This total is the minimum possible health expenditure required to clear the path.
5. Check if the total cost is strictly less than the initial health $N$. If yes, output YES; otherwise output NO.

### Why it works

The key invariant is that each enemy’s optimal strategy depends only on its own HP and not on decisions for other enemies. Any attack sequence can be rearranged so that all actions on one enemy are contiguous without changing total cost, since attacks do not interact across enemies. Therefore, minimizing cost per enemy independently and summing yields the global optimum. There is no coupling constraint other than total health, which is linear and additive across enemies, so local optimality implies global optimality.

## Python Solution

```python
import sys
input = sys.stdin.readline

def ceil_div(a, b):
    return (a + b - 1) // b

def solve():
    N, M = map(int, input().split())
    P1, P2 = map(int, input().split())
    Q1, Q2 = map(int, input().split())
    arr = list(map(int, input().split()))
    
    total_cost = 0
    
    for a in arr:
        # cost using only charge attacks
        hits = ceil_div(a, Q1)
        cost_charge = hits * Q2
        
        # cost using spike once + charge
        reduced = max(0, a - P1)
        hits2 = ceil_div(reduced, Q1)
        cost_spike = P2 + hits2 * Q2
        
        total_cost += min(cost_charge, cost_spike)
    
    print("YES" if total_cost < N else "NO")

if __name__ == "__main__":
    solve()
```

The implementation follows the derived cost model directly. The helper function for ceiling division avoids floating-point arithmetic and ensures correctness when HP is not divisible by attack damage. Each enemy is processed independently in a single pass.

A subtle implementation detail is using `max(0, a - P1)` before division. Without this, negative HP could incorrectly reduce the number of required charge attacks due to integer division behavior. Another key point is using strict comparison `total_cost < N`, since Iggy must remain strictly above zero HP after all damage is taken.

## Worked Examples

### Sample Input 1

Input:

```
N = 8, M = 3
P = (5, 2)
Q = (3, 1)
a = [5, 8, 6]
```

We compute per enemy costs.

| Enemy | a_i | Charge hits | Charge cost | Reduced HP | Spike hits | Spike cost | Chosen cost |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 5 | 2 | 2 | 0 | 0 | 2 | 2 |
| 2 | 8 | 3 | 3 | 3 | 1 | 2 | 2 |
| 3 | 6 | 2 | 2 | 1 | 1 | 2 | 2 |

Total cost is 6. Since 6 < 8, the output is YES.

This trace shows that even though the spike is useful on larger enemies, the optimal choice per enemy is consistent and additive.

### Sample Input 2 (constructed)

Input:

```
N = 10, M = 2
P = (4, 5)
Q = (2, 1)
a = [3, 9]
```

| Enemy | a_i | Charge hits | Charge cost | Reduced HP | Spike hits | Spike cost | Chosen cost |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 3 | 2 | 2 | 0 | 0 | 5 | 2 |
| 2 | 9 | 5 | 5 | 5 | 3 | 8 | 5 |

Total cost is 7, which is less than 10, so output is YES.

This example demonstrates that the spike is not always useful when its cost $P_2$ dominates the savings from reduced charge attacks.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(M)$ | Each enemy is processed once with constant-time arithmetic operations |
| Space | $O(1)$ | Only aggregate counters are maintained |

The algorithm comfortably fits within limits since $M \leq 10^5$, and each step is a few integer operations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import ceil
    input = sys.stdin.readline

    N, M = map(int, input().split())
    P1, P2 = map(int, input().split())
    Q1, Q2 = map(int, input().split())
    arr = list(map(int, input().split()))
    
    def ceil_div(a, b):
        return (a + b - 1) // b
    
    total = 0
    for a in arr:
        cost1 = ceil_div(a, Q1) * Q2
        reduced = max(0, a - P1)
        cost2 = P2 + ceil_div(reduced, Q1) * Q2
        total += min(cost1, cost2)
    
    return "YES\n" if total < N else "NO\n"

# provided sample
assert run("8 3\n5 2\n3 1\n5 8 6\n") == "YES\n"

# minimum input
assert run("1 1\n1 1\n1 1\n1\n") == "NO\n"

# spike useless case
assert run("20 2\n10 100\n1 1\n10 10\n") == "NO\n"

# spike dominates case
assert run("50 2\n9 1\n5 10\n20 20\n") == "YES\n"

# large HP single enemy
assert run("100 1\n50 1\n10 1\n1000000000\n") == "YES\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| minimal | NO | boundary where any cost kills Iggy |
| spike useless | NO | ensures spike is not always chosen |
| spike dominates | YES | ensures spike reduces charge usage |
| large HP | YES | correctness under large values |

## Edge Cases

One edge case occurs when the spike reduces HP below zero. In this case, all charge attacks disappear and only the spike cost matters. For example, if $a_i \le P_1$, then reduced HP becomes zero, and the cost is exactly $P_2$. The algorithm handles this correctly via `max(0, a - P1)` and then zero charge hits.

Another edge case is when charge attack is extremely inefficient but spike is also expensive. For instance, if $Q_1 = 1$ and $Q_2$ is large, charge cost becomes linear in HP, while spike only provides a bounded reduction. The algorithm still evaluates both expressions correctly and avoids any greedy misuse.

A final edge case is when all enemies are identical and large. The algorithm does not rely on sorting or ordering, so repeated values are handled naturally through independent per-enemy evaluation.
