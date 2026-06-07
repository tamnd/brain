---
title: "CF 487A - Fight the Monster"
description: "We are given the initial combat statistics of two characters, Master Yang and a monster. Each character has hit points, attack, and defense. Combat proceeds in discrete seconds."
date: "2026-06-07T17:31:28+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "implementation"]
categories: ["algorithms"]
codeforces_contest: 487
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 278 (Div. 1)"
rating: 1800
weight: 487
solve_time_s: 126
verified: true
draft: false
---

[CF 487A - Fight the Monster](https://codeforces.com/problemset/problem/487/A)

**Rating:** 1800  
**Tags:** binary search, brute force, implementation  
**Solve time:** 2m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given the initial combat statistics of two characters, Master Yang and a monster. Each character has hit points, attack, and defense.

Combat proceeds in discrete seconds. During each second, Yang deals

$$\max(0,\ ATK_Y - DEF_M)$$

damage to the monster, while the monster simultaneously deals

$$\max(0,\ ATK_M - DEF_Y)$$

damage to Yang.

Yang wins only if the monster's HP becomes non-positive while Yang still has strictly positive HP at that same moment.

Before the battle starts, Yang may increase any of his three attributes by paying bitcoins. HP, ATK, and DEF each have their own per-unit cost. We must find the minimum total amount of money needed so that Yang can guarantee victory.

The constraints are very small. Every input value is at most 100. Since purchased attributes can also stay in a relatively small range, a brute force search over possible attack and defense upgrades is feasible. The challenge is not computational complexity but correctly modeling the battle and handling all corner cases.

A subtle point is that Yang must actually be able to damage the monster. If

$$ATK_Y \le DEF_M$$

then the monster never loses HP, regardless of how much health Yang buys.

Consider:

```
1 1 1
1 5 5
1 1 1
```

Yang's attack is 1 and the monster's defense is 5. Buying HP alone can never help. Any solution that only checks survivability without ensuring positive damage would incorrectly think enough HP guarantees victory.

Another easy mistake is forgetting that Yang must remain alive after the killing turn. Suppose Yang kills the monster in 5 turns and also receives lethal damage during those same 5 turns. Since damage is simultaneous, Yang needs strictly positive HP at the end.

Example:

```
5 10 0
50 10 0
1 1 1
```

Yang deals 10 damage per turn and needs exactly 5 turns. The monster also deals 10 damage per turn, so Yang loses all 50 HP after 5 turns. This is not a win because Yang's HP is not strictly positive.

The correct requirement is

$$HP_Y > (\text{turns needed}) \times (\text{damage received per turn})$$

not greater than or equal.

A third corner case occurs when Yang's defense is already high enough that the monster deals zero damage. Then any positive HP is sufficient once Yang can eventually kill the monster.

Example:

```
1 2 100
100 2 1
5 5 5
```

The monster cannot hurt Yang at all. We only need enough attack to eventually defeat the monster.

## Approaches

A direct brute force approach is to try every possible amount of HP, attack, and defense that Yang could buy, simulate the battle, and keep the cheapest winning configuration.

This is correct because every possible upgrade combination is examined. The problem is deciding how large the search space must be. If we blindly iterate HP, ATK, and DEF over a large range, the number of states grows cubically.

The key observation is that HP behaves differently from attack and defense.

Suppose we decide the final attack and defense values. Then the battle outcome is completely determined except for HP. Among all HP values, there is a unique minimum HP required to survive. Buying more HP than that is never beneficial because it only increases cost.

This means we do not need to enumerate HP at all.

Instead, we enumerate final attack and defense values. For each pair we compute:

1. Damage Yang deals each turn.
2. Damage Yang receives each turn.
3. Number of turns needed to kill the monster.
4. Minimum HP required to survive those turns.

Once the required HP is known, the cost of that configuration is computed directly.

Since all initial values are at most 100, checking attack and defense values up to a few hundred easily covers every optimal solution. The accepted solutions traditionally iterate both dimensions up to 200.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over HP, ATK, DEF | O(K³) | O(1) | Unnecessarily large |
| Enumerate ATK and DEF, compute HP directly | O(K²) | O(1) | Accepted |

Here $K$ is the chosen upper bound for attack and defense exploration, typically around 200.

## Algorithm Walkthrough

1. Read Yang's and the monster's statistics, along with the three upgrade costs.
2. Enumerate every possible final attack value from the current attack up to a safe upper bound such as 200.
3. Enumerate every possible final defense value from the current defense up to the same upper bound.
4. Compute Yang's damage per turn.

$$dmg_Y = ATK - DEF_M$$

If this value is not positive, skip the configuration because the monster can never be killed.
5. Compute the number of turns required to defeat the monster.

$$turns = \left\lceil \frac{HP_M}{dmg_Y} \right\rceil$$
6. Compute the monster's damage per turn.

$$dmg_M = \max(0,\ ATK_M - DEF)$$
7. Determine the minimum HP Yang must have.

Yang receives damage for exactly `turns` rounds and must remain strictly alive afterward.

$$HP_{required} = turns \times dmg_M + 1$$

If Yang already has at least this much HP, no HP purchase is needed. Otherwise buy the difference.
8. Compute the total cost of all upgrades:

$$(\text{extra HP}) \cdot h
+
(\text{extra ATK}) \cdot a
+
(\text{extra DEF}) \cdot d$$
9. Keep the minimum cost among all valid configurations.
10. Output the minimum cost found.

### Why it works

For any chosen final attack and defense values, there is a smallest HP value that allows victory. Any larger HP only increases cost and never improves the result. Thus every optimal solution is represented by exactly one state in our search.

The algorithm examines every possible final attack and defense that could be part of an optimal answer. For each pair, it computes the minimum HP needed to survive until the monster dies. The resulting cost is the cheapest possible cost for that attack-defense pair.

Since every feasible optimal configuration appears somewhere in the enumeration and we take the minimum cost over all of them, the final answer is optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    hy, ay, dy = map(int, input().split())
    hm, am, dm = map(int, input().split())
    h_cost, a_cost, d_cost = map(int, input().split())

    INF = 10**18
    ans = INF

    for atk in range(ay, 201):
        damage_to_monster = atk - dm
        if damage_to_monster <= 0:
            continue

        turns = (hm + damage_to_monster - 1) // damage_to_monster

        for defense in range(dy, 201):
            damage_to_yang = max(0, am - defense)

            required_hp = turns * damage_to_yang + 1
            extra_hp = max(0, required_hp - hy)

            cost = (
                extra_hp * h_cost
                + (atk - ay) * a_cost
                + (defense - dy) * d_cost
            )

            ans = min(ans, cost)

    print(ans)

solve()
```

The outer loops enumerate all candidate final attack and defense values. For each attack value we immediately discard cases where Yang cannot damage the monster.

The ceiling division

```
(hm + damage_to_monster - 1) // damage_to_monster
```

computes the exact number of combat rounds required to kill the monster.

The survival condition is the most delicate part. Yang must have strictly positive HP after the final simultaneous damage application. If he receives `turns * damage_to_yang` total damage, then the smallest winning HP is one greater than that amount. Using `>=` here would produce incorrect answers in cases where Yang reaches exactly zero HP.

The chosen upper bound of 200 is sufficient. All initial statistics are at most 100. Raising attack or defense beyond 200 can never be useful because attack already exceeds every possible monster defense by at least 100, and defense already neutralizes every possible monster attack.

## Worked Examples

### Sample 1

Input:

```
1 2 1
1 100 1
1 100 100
```

The cheapest strategy is to buy HP only.

| atk | def | dmg_Y | turns | dmg_M | required_hp | extra_hp | cost |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | 1 | 1 | 1 | 99 | 100 | 99 | 99 |
| 3 | 1 | 2 | 1 | 99 | 100 | 99 | 199 |
| 2 | 2 | 1 | 1 | 98 | 99 | 98 | 9899 |

The minimum cost is 99.

This trace shows why attack and defense upgrades are unattractive when their prices are extremely high. Buying health alone already creates a winning configuration.

### Sample 2

Consider:

```
100 100 100
1 1 1
1 1 1
```

Yang is already overwhelmingly stronger.

| atk | def | dmg_Y | turns | dmg_M | required_hp | extra_hp | cost |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 100 | 100 | 99 | 1 | 0 | 1 | 0 | 0 |

The answer is 0.

This example demonstrates that the algorithm naturally handles situations where no purchases are needed.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(200²) | Enumerate all attack-defense pairs |
| Space | O(1) | Only a few variables are stored |

The search examines at most 40,000 configurations. Each configuration requires only constant time arithmetic. This is far below the limits and runs comfortably within one second.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    def input():
        return sys.stdin.readline()

    hy, ay, dy = map(int, input().split())
    hm, am, dm = map(int, input().split())
    h_cost, a_cost, d_cost = map(int, input().split())

    ans = 10**18

    for atk in range(ay, 201):
        dmg_y = atk - dm
        if dmg_y <= 0:
            continue

        turns = (hm + dmg_y - 1) // dmg_y

        for defense in range(dy, 201):
            dmg_m = max(0, am - defense)

            req_hp = turns * dmg_m + 1
            extra_hp = max(0, req_hp - hy)

            cost = (
                extra_hp * h_cost
                + (atk - ay) * a_cost
                + (defense - dy) * d_cost
            )

            ans = min(ans, cost)

    return str(ans)

# provided sample
assert run(
"""1 2 1
1 100 1
1 100 100
"""
) == "99"

# already winning
assert run(
"""100 100 100
1 1 1
1 1 1
"""
) == "0"

# need one attack upgrade to deal damage
assert run(
"""1 1 1
1 1 1
10 1 10
"""
) == "1"

# all values equal
assert run(
"""10 10 10
10 10 10
1 1 1
"""
) == "1"

# defense can completely negate damage
assert run(
"""1 2 1
100 100 1
10 10 1
"""
) == "99"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Yang already stronger than monster | 0 | No upgrades needed |
| Attack equals monster defense | 1 | Positive damage is required |
| All values equal | 1 | Correct handling of simultaneous damage |
| Cheap defense upgrades | 99 | Reducing incoming damage may be optimal |

## Edge Cases

### Yang cannot damage the monster

Input:

```
1 1 1
10 5 5
1 1 1
```

With attack 1 and monster defense 5, Yang deals zero damage. The algorithm skips every configuration whose final attack still satisfies `atk <= 5`. The first valid state is `atk = 6`, which deals one damage per turn. This prevents incorrectly treating infinite battles as wins.

### Yang reaches exactly zero HP

Input:

```
50 10 0
50 10 0
1 1 1
```

Yang deals 10 damage and kills the monster in 5 turns. He also receives 10 damage each turn.

The algorithm computes:

| Variable | Value |
| --- | --- |
| turns | 5 |
| dmg_M | 10 |
| required_hp | 51 |

Since `5 * 10 = 50`, having exactly 50 HP is insufficient. The extra `+1` enforces the requirement that Yang remains strictly alive after the final round.

### Monster deals zero damage

Input:

```
1 2 100
100 2 1
5 5 5
```

For defense 100:

| Variable | Value |
| --- | --- |
| dmg_M | 0 |
| required_hp | 1 |
| extra_hp | 0 |

The algorithm correctly recognizes that no HP upgrade is needed. Only the ability to eventually kill the monster matters.
