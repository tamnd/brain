---
title: "CF 104505G - Choice hero"
description: "We are given a sequence of levels played in a fixed order. At the start, a hero has some initial power, and at each level there are two monsters available."
date: "2026-06-30T10:58:45+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104505
codeforces_index: "G"
codeforces_contest_name: "2023 USP Try-outs"
rating: 0
weight: 104505
solve_time_s: 59
verified: true
draft: false
---

[CF 104505G - Choice hero](https://codeforces.com/problemset/problem/104505/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 59s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of levels played in a fixed order. At the start, a hero has some initial power, and at each level there are two monsters available. The player must choose exactly one monster per level, and the only constraint is that the chosen monster’s power cannot exceed the hero’s current power.

After defeating a monster, the hero’s power increases by exactly the power of that monster. This creates a feedback loop: choosing a weaker monster early may prevent unlocking stronger choices later, while choosing a stronger available monster might be impossible if the current power is too small.

The task is not to compute the final power or an optimal score, but only to determine feasibility: whether there exists any sequence of choices, one per level, that allows the hero to survive all levels in order.

The constraints allow up to 2000 levels, with values up to 10^6. A naive exponential search over choices would immediately be too large because each level branches into two possibilities, leading to 2^n possible paths, which is far beyond any feasible computation.

A subtle failure case for greedy intuition appears when a locally stronger monster blocks future accessibility. For example, if choosing a large monster early makes a later level impossible because both monsters exceed the remaining power, a greedy “always take the strongest possible” strategy can fail. Conversely, always taking the weakest possible can also fail because it may not increase power enough to unlock future options.

So the difficulty lies in tracking all reachable power states after each level while avoiding exponential blowup.

## Approaches

A brute-force approach treats this as a path search in a layered graph. Each layer corresponds to a level, and each state is a possible hero power. From a state with power x at level i, we can transition to level i+1 by choosing either monster a_i or b_i, provided it is ≤ x, and the new state becomes x + a_i or x + b_i.

This immediately suggests a BFS or DFS over states. The problem is that the number of distinct power values grows quickly. In the worst case, every choice creates a new distinct sum, so after i levels we may have O(2^i) states. At n = 2000, this is completely infeasible.

The key observation is that although the number of sequences is exponential, the structure of reachable power values has a strong monotonic property: for a fixed level, if a certain power is reachable, then all smaller powers are also effectively dominated and unnecessary to track individually. This allows us to compress the state space into just the maximum reachable power after each level, or more precisely, a set of “best representatives” that can be reduced to a single greedy frontier.

At each level, we do not need to track all possible powers. We only care about the maximum achievable power so far, because any state with smaller power cannot unlock anything that the maximum state cannot also unlock at the same level. Since transitions only require checking feasibility (x ≥ a_i or b_i), the process reduces to maintaining one value: the best possible current power after processing each level, assuming we always pick the best feasible option.

The decision at each level becomes simple: among a_i and b_i, we take the largest value that is ≤ current power. If neither is feasible, we fail.

This greedy works because choosing a larger feasible monster never reduces future options compared to choosing a smaller one. Both choices consume one level, but the larger choice strictly increases or preserves the future reachable threshold more strongly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(2^n) | Too slow |
| Greedy simulation | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We process levels in order while maintaining a single variable `power`, representing the maximum possible hero strength we can achieve at the current level.

1. Initialize `power = f`, the starting strength. This represents the best possible state before any decisions are made.
2. For each level i from 1 to n, inspect the two monsters `a_i` and `b_i`.
3. Check which of the two monsters can be defeated, meaning their power is ≤ current `power`.
4. If neither monster is defeatable, immediately conclude that the game cannot be completed.
5. If exactly one monster is defeatable, choose it and add its power to `power`.
6. If both are defeatable, choose the larger one. This maximizes the increase in `power` for the same cost of consuming one level, ensuring no future disadvantage.
7. After processing all levels successfully, output that the game can be completed.

### Why it works

The process relies on the fact that at any level, only the current maximum achievable power matters. If two states exist at the same level, the one with higher power dominates the other because every future constraint is of the form “power must be at least some threshold to proceed.” Since transitions only increase power, a higher current value can never reduce future feasibility. Therefore, maintaining only the maximum reachable power is sufficient, and greedy selection of the largest feasible monster preserves this maximum at every step.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, f = map(int, input().split())
    power = f

    for _ in range(n):
        a, b = map(int, input().split())

        can_a = a <= power
        can_b = b <= power

        if not can_a and not can_b:
            print("N")
            return

        if can_a and can_b:
            chosen = max(a, b)
        else:
            chosen = a if can_a else b

        power += chosen

    print("S")

if __name__ == "__main__":
    solve()
```

The solution keeps a single running value `power` and updates it level by level. The key implementation detail is that we always check feasibility before choosing, ensuring we never add an invalid monster. When both choices are valid, we explicitly take the maximum to maximize future reachability.

The order of checks matters: we must detect the failure case before attempting to pick a monster. Otherwise, invalid additions could incorrectly increase power and mask impossibility.

## Worked Examples

### Sample 1

Input:

```
3 2
1 2
5 3
4 4
```

| Level | power before | a | b | feasible choices | chosen | power after |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 2 | 1 | 2 | both | 2 | 4 |
| 2 | 4 | 5 | 3 | 3 only | 3 | 7 |
| 3 | 7 | 4 | 4 | both | 4 | 11 |

At every step, at least one monster is available. The final level succeeds, so the output is `S`.

### Sample 2

Input:

```
3 2
4 4
1 2
5 3
```

| Level | power before | a | b | feasible choices | chosen | power after |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 2 | 4 | 4 | none | fail | - |

The first level already has both monsters stronger than the hero, so no move is possible and the answer is `N`.

The second example shows an immediate blocking condition, where failure occurs before any state evolution.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each level is processed with constant-time comparisons and arithmetic |
| Space | O(1) | Only a single variable `power` is maintained |

With n up to 2000, linear time is trivially fast under the limits, and memory usage is constant.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from solution import solve  # assume function is imported
    return solve()

# provided samples
assert run("3 2\n1 2\n5 3\n4 4\n") == "S"
assert run("3 2\n4 4\n1 2\n5 3\n") == "N"

# minimum size success
assert run("1 5\n3 4\n") == "S"

# minimum size failure
assert run("1 3\n4 5\n") == "N"

# all equal and always feasible
assert run("4 1\n1 1\n1 1\n1 1\n1 1\n") == "S"

# case where choice matters but greedy still works
assert run("3 3\n2 3\n4 1\n5 2\n") == "S"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single small success | S | base feasibility |
| single impossible | N | immediate failure |
| repeated equal values | S | stability under ties |
| mixed constraints | S | greedy consistency |

## Edge Cases

A critical edge case is when both monsters are exactly equal to the current power. The algorithm must still treat this as valid and allow selection. For example:

Input:

```
2 3
3 3
3 3
```

At level 1, both are feasible, so we pick either 3 and increase power to 6. At level 2, again both are feasible, and we succeed. The greedy rule does not matter because both choices are identical.

Another edge case is immediate deadlock:

Input:

```
1 2
3 3
```

At the only level, both monsters exceed power, so the check correctly triggers failure before any update.

A third subtle case is when one monster is feasible but smaller, and the other is infeasible:

Input:

```
1 5
2 10
```

Only 2 is valid, so we must pick it. Choosing max without checking feasibility would incorrectly select 10 and falsely accept the case. The feasibility check before taking max is essential for correctness.
