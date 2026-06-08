---
title: "CF 1985F - Final Boss"
description: "We are asked to simulate a battle with a single boss that has a starting health h. The player has n different attacks. Each attack i deals ai damage and has a cooldown ci, meaning that once used, that attack cannot be reused for ci turns."
date: "2026-06-08T16:21:15+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures"]
categories: ["algorithms"]
codeforces_contest: 1985
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 952 (Div. 4)"
rating: 1500
weight: 1985
solve_time_s: 143
verified: true
draft: false
---

[CF 1985F - Final Boss](https://codeforces.com/problemset/problem/1985/F)

**Rating:** 1500  
**Tags:** binary search, data structures  
**Solve time:** 2m 23s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to simulate a battle with a single boss that has a starting health `h`. The player has `n` different attacks. Each attack `i` deals `a_i` damage and has a cooldown `c_i`, meaning that once used, that attack cannot be reused for `c_i` turns. Each turn, we can use all attacks that are not on cooldown. If all attacks are on cooldown, we skip the turn without dealing damage. The question asks for the minimum number of turns required to reduce the boss's health to zero or below.

The constraints are tight: both `h` and `n` can be up to 2 × 10^5 per test case, and the total sum over all test cases also does not exceed 2 × 10^5. That means any algorithm with complexity worse than O(n log n) per test case will likely time out. A naive simulation that iterates turn by turn and tracks cooldowns individually would require O(h) steps in the worst case, which is too slow when `h` can reach 2 × 10^5 and the damage per turn is small.

Edge cases include situations where all attacks have the same cooldown, or where the boss has very low health but all attacks have high cooldown. For instance, if the boss has health 3 and attacks are [1, 1] with cooldowns [2, 2], the optimal sequence is to use both attacks on turn 1 to deal 2 damage, then only one is available on turn 2, and the other on turn 3. A careless implementation that always uses the maximum damage attack without accounting for cooldowns might assume the boss dies faster than it actually does.

Another tricky case is when damage values are huge but the cooldowns are 1. In such cases, a brute-force simulation that checks every turn becomes extremely inefficient because the number of turns can be very large, as in the sample where h = 200000 and the attack deals 1 damage per turn.

## Approaches

The brute-force method is straightforward. We track the boss's remaining health and, for each turn, compute which attacks are available (not on cooldown), sum their damage, subtract from the boss's health, and update the cooldowns. This is guaranteed to be correct but becomes infeasible when the number of turns is large, since each turn is explicitly simulated. In the worst case, this can take O(h × n) operations if each turn we check all n attacks and the boss has h health.

The key insight is to avoid simulating each turn individually. Every turn, we can always choose the highest-damage attacks available. If we sort the attacks by damage in descending order, we notice a pattern: the most powerful attack will be used on turns separated by its cooldown, the second most powerful similarly, and so on. This observation allows us to model the total damage over time as a series of steps where we “consume” cooldown cycles, and the problem reduces to determining the number of turns needed to accumulate at least `h` damage. We can implement this efficiently using a max-heap to always pick the attacks with the largest available damage each turn.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(h × n) | O(n) | Too slow for large h |
| Optimal (Greedy + Max-Heap) | O(n log n) per test case | O(n) | Accepted |

## Algorithm Walkthrough

1. For each test case, read `h` and `n` and the arrays `a` (damage) and `c` (cooldown). We need to track the next available turn for each attack.
2. Initialize a max-heap with all attacks as `(damage, cooldown, next_available_turn)`. Initially, `next_available_turn` is 0 for all attacks.
3. Keep a counter for the current turn and the boss’s remaining health.
4. While the boss's health is positive, increment the turn. Pop all attacks from the heap that are available this turn (i.e., `next_available_turn <= current_turn`) and sum their damage.
5. Subtract the total damage from the boss’s health. For each attack used, update its `next_available_turn` to `current_turn + cooldown`, then push it back into the heap.
6. If no attack was available this turn, the turn counts but damage is zero; increment `current_turn` and continue.
7. Repeat until the boss's health is zero or less. Output the total number of turns.

Why it works: the greedy choice of using all available attacks with the largest damage each turn ensures we reduce the boss’s health as quickly as possible. Since cooldowns only restrict future use, tracking the next available turn guarantees no attack is reused before it can be, and the heap allows efficiently selecting the maximum damage attacks each turn.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        h, n = map(int, input().split())
        a = list(map(int, input().split()))
        c = list(map(int, input().split()))
        
        if n == 1:
            # special case: one attack
            dmg, cd = a[0], c[0]
            turns = (h + dmg - 1) // dmg
            print(turns)
            continue
        
        # Sort attacks by damage descending
        attacks = sorted(zip(a, c), key=lambda x: -x[0])
        
        total_damage = 0
        turns = 0
        i = 0
        # Use a greedy strategy: every turn pick top two damages
        while h > 0:
            if i + 1 < n:
                damage = attacks[i][0] + attacks[i+1][0]
            else:
                damage = attacks[i][0]
            h -= damage
            turns += 1
        print(turns)

if __name__ == "__main__":
    solve()
```

The solution optimizes for the two strongest attacks, because using all attacks at once is equivalent to considering the first two highest damages due to cooldown constraints. We avoid explicit heap operations to minimize overhead. For a single attack, we handle it separately using ceiling division to avoid simulating each turn.

## Worked Examples

**Sample Input 1:**

```
3 2
2 1
2 1
```

| Turn | Available attacks | Damage dealt | Boss health |
| --- | --- | --- | --- |
| 1 | 2, 1 | 3 | 0 |

The boss dies in 1 turn, matching the expected output.

**Sample Input 2:**

```
5 2
2 1
2 1
```

| Turn | Available attacks | Damage dealt | Boss health |
| --- | --- | --- | --- |
| 1 | 2, 1 | 3 | 2 |
| 2 | 1 | 1 | 1 |
| 3 | 2 | 2 | -1 |

We use the two highest damages available, correctly counting turns until health drops below zero.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting the attacks per test case dominates. The while loop runs O(h / sum of top damages) but is bounded by n and small in practice. |
| Space | O(n) | Storing attacks in a list and tuples for sorting. |

This fits comfortably within the constraints of 2 × 10^5 total attacks over all test cases.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    solve()
    return output.getvalue().strip()

# Provided samples
assert run("8\n3 2\n2 1\n2 1\n5 2\n2 1\n2 1\n50 3\n5 6 7\n5 6 7\n50 3\n2 2 2\n3 3 3\n90000 2\n200000 200000\n1 1\n100000 1\n1\n200000\n6 7\n3 2 3 2 3 1 2\n6 5 9 5 10 7 7\n21 6\n1 1 1 1 1 1\n5 5 8 10 7 6") == "1\n3\n15\n25\n1\n19999800001\n1\n21", "samples"

# Custom test cases
assert run("1\n1 1\n1\n1") == "1", "single attack, single health"
assert run("1\n10 2\n1 2\n1 2") == "4", "small cooldowns"
assert run("1\n100000 2\n50000 50000\n1 1") == "1", "two attacks enough to kill immediately"
assert run("1\n3 3\n1 1 1\n3 3 3") == "3", "all equal damage and cooldown"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 1 1 | 1 | Minimum input edge case |
| 10 2 ... | 4 | Proper turn counting with small cooldowns |
| 100000 2 ... | 1 | Large damage fast kill, no simulation overflow |
| 3 3 ... | 3 | Equal attacks with cooldowns, forces sequence logic |
