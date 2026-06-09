---
title: "CF 1633C - Kill the Monster"
description: "The problem is a turn-based combat simulation between Monocarp's character and a monster. Each has an initial health and attack."
date: "2026-06-10T04:48:20+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "math"]
categories: ["algorithms"]
codeforces_contest: 1633
codeforces_index: "C"
codeforces_contest_name: "Educational Codeforces Round 122 (Rated for Div. 2)"
rating: 1100
weight: 1633
solve_time_s: 77
verified: true
draft: false
---

[CF 1633C - Kill the Monster](https://codeforces.com/problemset/problem/1633/C)

**Rating:** 1100  
**Tags:** brute force, math  
**Solve time:** 1m 17s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem is a turn-based combat simulation between Monocarp's character and a monster. Each has an initial health and attack. On each turn, the character strikes first, reducing the monster's health by his current attack value, then the monster retaliates, reducing the character's health by the monster's attack. This alternates until one of them reaches zero or negative health. The goal is to determine if Monocarp can guarantee victory by spending up to a certain number of coins to upgrade his character's attack and/or health.

The input specifies the number of test cases. For each test case, we are given the character's health and attack, the monster's health and attack, and the number of coins available along with the benefit per coin for health and attack upgrades. The output is a simple YES or NO indicating if victory is achievable.

The constraints allow very large numbers: character and monster health can be up to $10^{15}$, coins up to $2 \cdot 10^5$, and upgrades as large as $10^{10}$. Since the number of test cases can be $5 \cdot 10^4$, a solution must handle each test case efficiently, in roughly $O(k)$ or better, because naive simulation of each turn would exceed the time limit.

Non-obvious edge cases include situations where the character already wins without upgrades, where all coins should optimally go to attack or health, and where the number of coins is zero. For example, if $h_C = 1$, $d_C = 1$, $h_M = 1$, $d_M = 10$, and $k = 0$, Monocarp cannot survive even one hit, so the correct output is NO. A naive approach that always tries upgrades without considering the current stats could incorrectly report YES.

## Approaches

The brute-force approach is to try all ways to distribute coins between health and attack upgrades. For each distribution, we would simulate the fight by iterating turns until one side dies. This works because each combination of upgrades is valid and the simulation reflects the rules exactly. However, in the worst case, there are $k+1$ distributions to try, and simulating a fight with up to $10^{15}$ health is infeasible. Even calculating the number of turns naively would be too slow. Therefore, brute-force is impractical.

The key insight is that the number of turns each side survives can be computed mathematically without simulating each attack. The character kills the monster in $\lceil h_M / d_C' \rceil$ turns, where $d_C' = d_C + w \cdot x$ and $x$ is the number of coins spent on attack. The monster kills the character in $\lceil h_C' / d_M \rceil$ turns, where $h_C' = h_C + a \cdot (k - x)$ for the coins spent on health. If the character's turn count is less than or equal to the monster's, Monocarp wins. This reduces the problem to checking $k+1$ simple calculations per test case.

We can therefore iterate over all possible splits of coins between attack and health, compute the number of turns to defeat each side using integer arithmetic, and check if there is at least one split that guarantees victory. Since $k$ is at most $2 \cdot 10^5$ and the sum of $k$ over all test cases does not exceed $2 \cdot 10^5$, this approach is efficient.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(k * max(h_M, h_C)) | O(1) | Too slow |
| Optimal Mathematical | O(k) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the initial character and monster stats, and the number of coins and their benefits.
2. Loop over all possible ways to distribute coins between attack and health, from 0 coins to attack up to $k$.
3. For each split, compute the new attack $d_C' = d_C + w \cdot x$ and new health $h_C' = h_C + a \cdot (k - x)$.
4. Compute the number of turns the character needs to defeat the monster as $\text{turns}_C = \lceil h_M / d_C' \rceil$.
5. Compute the number of turns the monster needs to defeat the character as $\text{turns}_M = \lceil h_C' / d_M \rceil$.
6. If $\text{turns}_C \le \text{turns}_M$ for any split, immediately conclude YES for this test case. Otherwise, after checking all splits, conclude NO.
7. Print YES or NO for each test case.

Why it works: By iterating over all feasible distributions of coins and computing survival times mathematically, we guarantee that all optimal upgrades are considered. Since fighting turns are deterministic and strictly decreasing, the comparison of turn counts correctly determines the outcome. The loop over $k+1$ possibilities is sufficient to capture any optimal combination, so no valid winning distribution is missed.

## Python Solution

```python
import sys
input = sys.stdin.readline
import math

t = int(input())
for _ in range(t):
    hC, dC = map(int, input().split())
    hM, dM = map(int, input().split())
    k, w, a = map(int, input().split())
    
    possible = False
    for coins_attack in range(k + 1):
        coins_health = k - coins_attack
        new_attack = dC + coins_attack * w
        new_health = hC + coins_health * a
        
        turns_to_kill_monster = (hM + new_attack - 1) // new_attack
        turns_to_survive = (new_health + dM - 1) // dM
        
        if turns_to_kill_monster <= turns_to_survive:
            possible = True
            break
    
    print("YES" if possible else "NO")
```

The solution first reads the input efficiently using `sys.stdin.readline`. For each test case, it iterates over all coin distributions, computes the resulting attack and health, and calculates the number of turns using ceiling division via integer arithmetic. The loop breaks immediately when a winning distribution is found to avoid unnecessary calculations. Edge cases such as zero coins, zero upgrade values, or already sufficient stats are naturally handled because all distributions, including no upgrades, are tested.

## Worked Examples

Sample input:

```
25 4
9 20
1 1 10
```

| Coins to attack | Coins to health | New attack | New health | Turns to kill monster | Turns to survive | Wins? |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 1 | 4 | 35 | 3 | 2 | No |
| 1 | 0 | 5 | 25 | 2 | 2 | Yes |

Here, spending 1 coin on attack allows the character to kill the monster in 2 turns, surviving 2 turns, so victory is possible.

Another example:

```
25 4
12 20
1 1 10
```

| Coins to attack | Coins to health | New attack | New health | Turns to kill monster | Turns to survive | Wins? |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 1 | 4 | 35 | 3 | 2 | No |
| 1 | 0 | 5 | 25 | 3 | 2 | No |

Here, neither allocation allows killing the monster before dying, so the answer is NO.

These traces demonstrate that the algorithm correctly computes turn counts and evaluates all possible coin allocations.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(k) per test case | We iterate over all possible splits of k coins and compute integer arithmetic operations for each split. Sum of k over all test cases ≤ 2_10^5, so total operations ≤ 2_10^5. |
| Space | O(1) | Only a few integer variables are stored per test case. |

Given the constraints, this solution fits well within the 2-second time limit and 256 MB memory limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    exec(open("solution.py").read())  # assuming solution is in solution.py
    return output.getvalue().strip()

# provided samples
assert run("4\n25 4\n9 20\n1 1 10\n25 4\n12 20\n1 1 10\n100 1\n45 2\n0 4 10\n9 2\n69 2\n4 2 7\n") == \
       "YES\nNO\nYES\nYES", "sample 1"

# custom cases
assert run("1\n1 1\n10 1\n0 1 1\n") == "NO", "minimum coins, cannot survive"
assert run("1\n10 5\n10 5\n10 1 1\n") == "YES", "already winning without upgrades"
assert run("1\n5 5\n20 10\n5 2 5\n") == "YES",
```
