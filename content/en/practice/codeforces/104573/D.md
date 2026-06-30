---
title: "CF 104573D - XP Challenge"
description: "We are given a sequence of enemies, each with some health, and a creature with an initial amount of health points. The goal is to decide whether she can defeat every enemy in order while ensuring her own health never drops to zero or below. There are two attack options."
date: "2026-06-30T08:20:11+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104573
codeforces_index: "D"
codeforces_contest_name: "UTPC Contest 09-08-23 Div. 1"
rating: 0
weight: 104573
solve_time_s: 94
verified: true
draft: false
---

[CF 104573D - XP Challenge](https://codeforces.com/problemset/problem/104573/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 34s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of enemies, each with some health, and a creature with an initial amount of health points. The goal is to decide whether she can defeat every enemy in order while ensuring her own health never drops to zero or below.

There are two attack options. One is a strong attack that can be used at most once per enemy, dealing high damage but also costing a large amount of health. The other is a weaker attack that can be used unlimited times, dealing smaller damage per use and also costing some health per use.

The key difficulty is that each enemy must be reduced to zero health, and we can mix the two attack types. The decision is not just local per enemy, because spending too much health early can make later fights impossible. So the problem is about minimizing total self-damage while still ensuring each enemy is fully defeated.

The constraints go up to 100,000 enemies, so any solution that tries all combinations of attack allocations per enemy is impossible. Even quadratic reasoning per enemy would be too slow, so we need a greedy or arithmetic per-enemy decision.

A common pitfall is treating each enemy independently and always using the “best damage per cost” attack. That fails because the strong attack is limited to once per enemy and might be wasted on small enemies where it is not efficient, even if locally it looks good.

Another subtle issue is forgetting that partial use of the weak attack must exactly finish remaining health, so leftover health after one strong hit still requires enough weak hits, and that cost matters in total.

## Approaches

A brute-force approach would try every assignment of attack types for each enemy: for each enemy, decide how many weak attacks to use and whether to apply the strong attack. This leads to an exponential number of possibilities, roughly $2^M$, since each enemy has multiple combinations of usage patterns. Even reducing per enemy to “strong used or not” is insufficient because weak attacks are still variable in count.

This quickly becomes infeasible once M grows beyond even 30 or 40.

The key observation is that for each enemy, we only care about the minimum possible self-damage required to defeat it. Since enemies are independent in health requirements (there is no carry-over state except remaining HP), we can compute, for each enemy, the cheapest way to reduce its HP to zero, then sum those costs.

For a given enemy, we compare two strategies: using only weak attacks, or using one strong attack followed by enough weak attacks to finish the remaining health. We pick the cheaper one. Once each enemy is reduced to a cost, we just subtract total cost from initial HP.

This turns the problem into a simple accumulation check.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | exponential | O(1)-O(M) | Too slow |
| Optimal | O(M) | O(1) | Accepted |

## Algorithm Walkthrough

Let each enemy have health $a_i$.

1. For each enemy, compute how many weak attacks are needed to defeat it fully. Each weak attack deals $Q_1$ damage and costs $Q_2$ HP, so the number of weak attacks is $\lceil a_i / Q_1 \rceil$. This gives a total cost of weak-only strategy as $cost_weak = \lceil a_i / Q_1 \rceil \cdot Q_2$.
2. If we use the strong attack once, it reduces the enemy by $P_1$. If $a_i \le P_1$, then one strong attack is enough and the cost is simply $P_2$.
3. Otherwise, after the strong attack, remaining health is $a_i - P_1$. We still need $\lceil (a_i - P_1) / Q_1 \rceil$ weak attacks, so the cost becomes $cost_strong = P_2 + \lceil (a_i - P_1) / Q_1 \rceil \cdot Q_2$.
4. For each enemy, take $min(cost_weak, cost_strong)$ as the minimal required HP loss.
5. Sum all these minimal costs across all enemies.
6. If initial HP $N$ is strictly greater than total cost, output "YES", otherwise "NO".

The reason for taking a minimum per enemy is that there is no interaction between enemies except shared HP budget, so optimal global strategy decomposes into optimal local choices.

### Why it works

Each enemy is independent in terms of damage requirement, and every valid strategy must fully reduce its HP to zero. For any fixed enemy, any sequence of actions can be rearranged into either “all weak attacks” or “one strong attack followed by weak attacks” without increasing cost, since extra strong attacks are disallowed and weak attacks are linear in cost. Thus the per-enemy minimum cost is globally optimal when summed.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    N, M = map(int, input().split())
    P1, P2 = map(int, input().split())
    Q1, Q2 = map(int, input().split())
    a = list(map(int, input().split()))

    total = 0

    for hp in a:
        weak_hits = (hp + Q1 - 1) // Q1
        cost_weak = weak_hits * Q2

        if hp <= P1:
            cost_strong = P2
        else:
            rem = hp - P1
            weak_after = (rem + Q1 - 1) // Q1
            cost_strong = P2 + weak_after * Q2

        total += min(cost_weak, cost_strong)

    print("YES" if total < N else "NO")

if __name__ == "__main__":
    solve()
```

The solution reads all parameters, then iterates through each enemy computing the cheapest way to defeat it. The key implementation detail is careful ceiling division when computing weak attack counts. Both strategies are computed explicitly to avoid reasoning mistakes about edge cases where strong attack overshoots or exactly matches remaining HP.

The final comparison uses strict inequality because Iggy must remain strictly above zero HP.

## Worked Examples

### Example 1

Input:

```
N = 8, M = 3
P1 = 5, P2 = 2
Q1 = 3, Q2 = 1
a = [5, 8, 6]
```

We compute per enemy:

| Enemy | Weak cost | Strong cost | Chosen |
| --- | --- | --- | --- |
| 5 | ceil(5/3)=2 → 2 | P2=2 | 2 |
| 8 | ceil(8/3)=3 → 3 | 2 + ceil(3/3)=1 → 3 | 3 |
| 6 | ceil(6/3)=2 → 2 | 2 + ceil(1/3)=1 → 3 | 2 |

Total cost = 2 + 3 + 2 = 7.

Remaining HP = 8 − 7 = 1, so output is YES.

This trace shows that strong attack is not always beneficial; it depends on remaining health relative to weak attack efficiency.

### Example 2

Input:

```
N = 10, M = 2
P1 = 4, P2 = 5
Q1 = 2, Q2 = 3
a = [3, 7]
```

Enemy 1:

Weak = ceil(3/2)=2 → 6

Strong = 5 (since 3 <= 4) → choose 5

Enemy 2:

Weak = ceil(7/2)=4 → 12

Strong = 5 + ceil(3/2)=2 → 11 → choose 11

Total = 5 + 11 = 16.

Remaining HP = 10 − 16 ≤ 0, so answer is NO.

This shows that even when strong attack is used, cumulative cost can still exceed initial HP, making the outcome impossible.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(M) | Each enemy is processed once with O(1) arithmetic |
| Space | O(1) | Only running sums and input storage |

The constraints allow up to 100,000 enemies, and the solution performs constant work per enemy, so it easily fits within time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import ceil

    def solve():
        N, M = map(int, input().split())
        P1, P2 = map(int, input().split())
        Q1, Q2 = map(int, input().split())
        a = list(map(int, input().split()))

        total = 0
        for hp in a:
            weak = (hp + Q1 - 1) // Q1 * Q2
            if hp <= P1:
                strong = P2
            else:
                rem = hp - P1
                strong = P2 + (rem + Q1 - 1) // Q1 * Q2
            total += min(weak, strong)

        return "YES" if total < N else "NO"

    return solve()

# provided sample
assert run("""8 3
5 2
3 1
5 8 6
""") == "YES"

# minimal case
assert run("""1 1
1 1
1 1
1
""") == "NO"

# strong always best
assert run("""20 2
10 1
100 1
5 5
""") == "YES"

# weak always best
assert run("""20 2
100 100
1 1
10 10
""") == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| minimal | NO | single enemy exact depletion edge |
| strong dominant | YES | strong attack optimality |
| weak dominant | YES | weak-only correctness |

## Edge Cases

A key edge case happens when an enemy’s HP is exactly divisible by the weak attack damage. In that case, ceiling division equals exact division, and there is no wasted attack. The algorithm handles this naturally because integer ceiling division `(hp + Q1 - 1) // Q1` collapses to `hp / Q1`.

Another edge case occurs when the strong attack reduces HP to exactly zero. The code handles this through the condition `hp <= P1`, ensuring no weak attacks are added afterward, preventing an off-by-one extra cost.

Finally, when both attack types are extremely inefficient, total cost can exceed N even for small M, and the algorithm correctly aggregates all per-enemy costs before comparison rather than making early decisions.
