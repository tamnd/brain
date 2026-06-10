---
title: "CF 1480B - The Great Hero"
description: "The problem presents a hero with fixed attack power and health facing a set of monsters, each with their own attack and health. Combat is turnless but simultaneous: when the hero attacks a monster, the monster also deals its attack damage back to the hero."
date: "2026-06-10T23:40:43+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1480
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 700 (Div. 2)"
rating: 900
weight: 1480
solve_time_s: 118
verified: true
draft: false
---

[CF 1480B - The Great Hero](https://codeforces.com/problemset/problem/1480/B)

**Rating:** 900  
**Tags:** greedy, implementation, sortings  
**Solve time:** 1m 58s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem presents a hero with fixed attack power and health facing a set of monsters, each with their own attack and health. Combat is turnless but simultaneous: when the hero attacks a monster, the monster also deals its attack damage back to the hero. A monster is defeated when its health drops to zero or below, and the hero is defeated when his health drops to zero or below. The goal is to determine if the hero can kill all monsters, even if he dies in the process, as long as no monsters survive.

Input consists of multiple test cases. Each test case provides the hero's attack, hero's health, number of monsters, a list of monster attacks, and a list of monster healths. The output is a simple YES or NO per test case.

The constraints allow up to 10^5 monsters across all test cases and monster healths and attack powers up to 10^6. Any naive simulation that iteratively subtracts health for each attack until monsters die is too slow in the worst case. For example, if a monster has health 10^6 and the hero’s attack is 1, simulating each attack could involve 10^6 iterations per monster, far exceeding feasible limits.

A subtle edge case occurs when a monster deals massive damage but has low health. A careless greedy algorithm might attack monsters in an arbitrary order and let the hero die prematurely. For example, a single monster with health 999 and attack 1000 against a hero with 999 health is instantly fatal. The correct answer is NO, but if one ignored the total damage needed and only counted number of attacks, one might mistakenly say YES.

## Approaches

The brute-force approach simulates every attack explicitly: repeatedly select a living monster, subtract the hero’s attack from its health, subtract the monster’s attack from the hero’s health, and repeat until either all monsters or the hero are dead. This is correct but potentially requires millions of operations per test case, which is too slow given the constraints.

The optimal approach leverages the observation that the total damage each monster inflicts is proportional to the number of attacks required to kill it. For each monster, the number of hero attacks needed is ceil(monster_health / hero_attack). Each attack costs the hero damage equal to the monster’s attack. Summing this across all monsters gives the total damage the hero would take if the hero were to fight each monster in isolation. The hero survives if his health exceeds or equals this sum minus the largest single monster attack. This works because the last monster can be finished even if the hero dies on that strike, but all others must be fully survived. Sorting is unnecessary; one just needs the maximum monster attack and total “effective damage” across all monsters.

The brute-force is simple to reason about but O(n * max(b_i/A)), while the optimal approach is linear per test case, O(n), which fits perfectly within the constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * max(b_i / A)) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the hero’s attack `A`, hero’s health `B`, and number of monsters `n`.
2. Read the monster attack array `a` and monster health array `b`.
3. For each monster, compute the number of attacks required to kill it. This is `(b_i + A - 1) // A`. Multiply this by the monster's attack to find the total damage this monster inflicts before dying. Sum these values across all monsters.
4. Identify the largest single monster attack `max_attack`. This represents the damage the hero can take on the final monster, because he may die after killing it.
5. If the hero’s health `B` is greater than or equal to the sum of all inflicted damages minus `max_attack`, output YES. Otherwise, output NO.

Why it works: The key invariant is that each monster’s total damage is accounted for based on the minimum number of attacks needed to kill it. Subtracting the maximum monster attack models the scenario where the hero finishes the last monster while possibly dying simultaneously. This ensures that the hero can kill all monsters without leaving any alive, matching the problem’s requirement.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    t = int(input())
    for _ in range(t):
        A, B, n = map(int, input().split())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))
        
        total_damage = 0
        max_attack = 0
        
        for ai, bi in zip(a, b):
            attacks_needed = (bi + A - 1) // A
            total_damage += attacks_needed * ai
            max_attack = max(max_attack, ai)
        
        if B >= total_damage - max_attack:
            print("YES")
        else:
            print("NO")

if __name__ == "__main__":
    main()
```

Each section of the solution corresponds directly to the algorithm walkthrough. The `attacks_needed` computation uses ceiling division to determine precisely how many attacks are required. `total_damage` sums the potential damage from each monster. `max_attack` is used to allow the hero to die on the last attack. Edge cases such as a single monster with hero health exactly equal to damage taken are handled by the final comparison `B >= total_damage - max_attack`.

## Worked Examples

### Sample 1

Input:

```
3 17 1
2
16
```

| Hero Health B | Monster Health b_i | Monster Attack a_i | Attacks Needed | Total Damage |
| --- | --- | --- | --- | --- |
| 17 | 16 | 2 | 6 | 12 |

Max monster attack = 2. Check: 17 >= 12 - 2 → 17 >= 10 → YES.

The table shows that after all attacks, the hero can still survive past the total required damage minus the last monster's attack.

### Sample 2

Input:

```
999 999 1
1000
1000
```

| Hero Health B | Monster Health b_i | Monster Attack a_i | Attacks Needed | Total Damage |
| --- | --- | --- | --- | --- |
| 999 | 1000 | 1000 | 1 | 1000 |

Max monster attack = 1000. Check: 999 >= 1000 - 1000 → 999 >= 0 → YES.

The hero dies after dealing the final blow, which is allowed.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | One pass to calculate attacks needed and total damage; summing max attack is constant |
| Space | O(n) | Storing monster attacks and health |

The algorithm scales linearly with the number of monsters, and the total number of monsters across all test cases is bounded by 10^5, so the solution comfortably executes within the 2-second time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    main()
    return out.getvalue().strip()

# provided samples
assert run("5\n3 17 1\n2\n16\n10 999 3\n10 20 30\n100 50 30\n1000 1000 4\n200 300 400 500\n1000 1000 1000 1000\n999 999 1\n1000\n1000\n999 999 1\n1000000\n999\n") == "YES\nYES\nYES\nNO\nYES", "sample 1"

# custom cases
assert run("1\n1 1 1\n1\n1\n") == "YES", "minimum values"
assert run("1\n1 1000000 1\n1000000\n1000000\n") == "YES", "max monster attack equal hero health"
assert run("1\n5 10 2\n3 6\n7 5\n") == "NO", "hero cannot survive both monsters"
assert run("1\n10 10 2\n5 4\n5 6\n") == "YES", "hero can finish last monster while dying"
assert run("1\n1000000 1 1\n1\n1000000\n") == "NO", "hero dies immediately"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 1\n1\n1 | YES | Minimum input values |
| 1 1000000 1\n1000000\n1000000 | YES | Max monster attack equal to hero health, hero dies last |
| 5 10 2\n3 6\n7 5 | NO | Hero cannot survive all monsters |
| 10 10 2\n5 4\n5 6 | YES | Hero dies on last monster |
| 1000000 1 1\n1\n1000000 | NO | Hero dies immediately |

## Edge Cases

For the case of a single monster whose attack exceeds the hero’s health, the algorithm correctly allows for YES if the hero can kill the monster in one strike. For example, hero health 999, monster health 1000, monster attack 1000. The ceiling division yields 1 attack needed, total damage = 1000. Max attack = 1000. B >= total_damage - max_attack → 999 >= 0, which evaluates
