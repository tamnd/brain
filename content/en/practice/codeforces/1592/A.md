---
title: "CF 1592A - Gamer Hemose"
description: "We are asked to determine how quickly an Agent in a game can defeat an enemy with a given health using a set of weapons, each with a fixed damage. The Agent can attack multiple times, but cannot use the same weapon twice in a row."
date: "2026-06-10T09:15:07+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "greedy", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1592
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 746 (Div. 2)"
rating: 800
weight: 1592
solve_time_s: 98
verified: true
draft: false
---

[CF 1592A - Gamer Hemose](https://codeforces.com/problemset/problem/1592/A)

**Rating:** 800  
**Tags:** binary search, greedy, math, sortings  
**Solve time:** 1m 38s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to determine how quickly an Agent in a game can defeat an enemy with a given health using a set of weapons, each with a fixed damage. The Agent can attack multiple times, but cannot use the same weapon twice in a row. The input provides several independent test cases. Each test case specifies the number of weapons, the enemy's initial health, and the damage values of each weapon. The output for each test case is the minimum number of attacks needed to reduce the enemy’s health to zero or below.

The constraints tell us that there are up to 100,000 test cases, but each test case has at most 1,000 weapons, and the sum of all weapons across all test cases is at most 200,000. Health and damage values can be very large, up to one billion. This rules out any solution that simulates each attack one by one for large health values because that would require billions of operations. Instead, we need a strategy that computes the answer mathematically using the properties of the weapons’ damages.

A non-obvious edge case arises when a single weapon’s damage is greater than or equal to the enemy’s health. In this case, only one attack is required, even if there is another weapon with higher damage. A careless implementation that always assumes alternating weapons will overcount the number of moves. Another edge case occurs when the two strongest weapons together cannot exactly divide the enemy’s health. Here, the remaining health after repeating the strongest pair may require one additional attack with the strongest weapon.

## Approaches

A naive approach is to simulate the attack process. We could repeatedly select the strongest available weapon that is not the same as the previous weapon and subtract its damage from the enemy’s health. This would be correct but extremely slow because for large health values (up to 10^9), the loop could iterate billions of times, making it infeasible.

The key insight comes from realizing that only the two weapons with the highest damage values matter. Let the strongest weapon have damage `max1` and the second strongest `max2`. If the Agent attacks optimally, he will alternate between these two weapons to maximize damage. In two moves, the total damage is `max1 + max2`. For large health values, we can calculate how many full two-move cycles are needed using integer division, then handle the remaining health with one or two extra moves. This reduces the problem to a simple calculation using the two largest values, rather than simulating each attack.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(H / min_damage) | O(1) | Too slow |
| Optimal | O(n log n) for sorting per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the number of weapons `n` and the enemy health `H`. Read the damage values of the weapons into an array.
2. Find the two largest damage values from the array. Sorting is convenient and simple: sort in descending order and take the first two values. Let `max1` be the largest and `max2` be the second largest.
3. Check if the strongest weapon alone is enough to kill the enemy. If `max1 >= H`, the answer is 1 because a single attack suffices.
4. Otherwise, calculate the number of full two-move cycles needed. Each cycle does `max1 + max2` damage. Use integer division: `full_cycles = H // (max1 + max2)`.
5. Compute the remaining health after these full cycles: `remaining = H - full_cycles * (max1 + max2)`.
6. Determine the extra moves needed to finish the enemy. If `remaining` is 0, no extra moves are needed. If `remaining <= max1`, one more attack with the strongest weapon is sufficient. Otherwise, two more attacks (strongest then second strongest) are needed.
7. Sum the moves from full cycles (each cycle is 2 moves) and the extra moves to get the minimum number of moves for the test case.

Why it works: Alternating the two strongest weapons guarantees maximum damage per pair of moves, which is always at least as high as any other choice of weapon sequence. By handling the remainder separately, we account for any leftover health that cannot be covered by full cycles. This approach guarantees that we never overcount or undercount moves.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, H = map(int, input().split())
    weapons = list(map(int, input().split()))
    weapons.sort(reverse=True)
    max1, max2 = weapons[0], weapons[1]

    if max1 >= H:
        print(1)
        continue

    full_cycles = H // (max1 + max2)
    remaining = H - full_cycles * (max1 + max2)

    moves = full_cycles * 2
    if remaining == 0:
        print(moves)
    elif remaining <= max1:
        print(moves + 1)
    else:
        print(moves + 2)
```

The solution reads input quickly using `sys.stdin.readline`. Sorting the weapon damages gives us the two strongest values. We handle the single-attack case first because it is a common early exit. Full cycles and the remainder calculation allow us to avoid simulating each move individually, which would be prohibitively slow for large health values. Checking the remainder ensures correct handling of edge cases where only one additional attack is needed after full cycles.

## Worked Examples

### Example 1

Input: `2 4`, Weapons: `[3, 7]`, Health `H=4`

| Step | max1 | max2 | H | full_cycles | remaining | moves |
| --- | --- | --- | --- | --- | --- | --- |
| Initial | 7 | 3 | 4 | - | - | - |
| Check single attack | 7 >= 4 | - | - | - | - | 1 |

The strongest weapon kills the enemy immediately. Output is 1.

### Example 2

Input: `2 6`, Weapons: `[4, 2]`, Health `H=6`

| Step | max1 | max2 | H | full_cycles | remaining | moves |
| --- | --- | --- | --- | --- | --- | --- |
| Initial | 4 | 2 | 6 | - | - | - |
| Single attack check | 4 < 6 | - | - | - | - | - |
| Full cycles | 6 // (4+2)=1 | remaining = 6-6=0 | moves = 2 | - | 2 |  |

No remaining health, total moves is 2.

These traces show that the logic handles single-attack wins, exact full-cycle kills, and the remainder correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t * n log n) | Sorting the weapons in each test case dominates. Each test case has n ≤ 1000, and sum of n over all test cases ≤ 2×10^5, so total sorting is feasible. |
| Space | O(n) | We store the weapon array for each test case. No additional large structures are needed. |

Given the constraints, this algorithm runs well under 1 second for the maximum input size.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    # insert solution code
    t = int(input())
    for _ in range(t):
        n, H = map(int, input().split())
        weapons = list(map(int, input().split()))
        weapons.sort(reverse=True)
        max1, max2 = weapons[0], weapons[1]

        if max1 >= H:
            print(1)
            continue

        full_cycles = H // (max1 + max2)
        remaining = H - full_cycles * (max1 + max2)

        moves = full_cycles * 2
        if remaining == 0:
            print(moves)
        elif remaining <= max1:
            print(moves + 1)
        else:
            print(moves + 2)
    return output.getvalue().strip()

# provided samples
assert run("3\n2 4\n3 7\n2 6\n4 2\n3 11\n2 1 7\n") == "1\n2\n3", "sample cases"

# custom test cases
assert run("1\n2 10\n5 5\n") == "2", "equal weapons, exact double cycle"
assert run("1\n3 15\n10 5 3\n") == "2", "strongest alone does not suffice, remainder handled"
assert run("1\n2 1\n100 50\n") == "1", "health smaller than any weapon"
assert run("1\n4 17\n6 5 4 3\n") == "3", "remainder requires extra moves"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 10, weapons 5 5 | 2 | Alternating equal weapons in full cycle |
| 3 15, weapons 10 5 3 | 2 | Handling remainder after full cycle |
| 2 1, weapons 100 50 | 1 | Single-attack edge case |
| 4 17, weapons 6 5 4 3 | 3 | Correct handling of remainder > max1 |

## Edge Cases
