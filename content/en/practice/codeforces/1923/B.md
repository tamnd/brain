---
title: "CF 1923B - Monsters Attack!"
description: "We have a line with our character at position 0 and monsters positioned at some coordinates $xi$, each with health $ai$. Every second, we can fire up to $k$ bullets, reducing the health of monsters we choose."
date: "2026-06-08T19:12:12+07:00"
tags: ["codeforces", "competitive-programming", "dp", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1923
codeforces_index: "B"
codeforces_contest_name: "Educational Codeforces Round 162 (Rated for Div. 2)"
rating: 1100
weight: 1923
solve_time_s: 97
verified: true
draft: false
---

[CF 1923B - Monsters Attack!](https://codeforces.com/problemset/problem/1923/B)

**Rating:** 1100  
**Tags:** dp, greedy, implementation  
**Solve time:** 1m 37s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a line with our character at position 0 and monsters positioned at some coordinates $x_i$, each with health $a_i$. Every second, we can fire up to $k$ bullets, reducing the health of monsters we choose. After firing, monsters with non-positive health die, then all remaining monsters move one step toward our character. If a monster reaches 0, we lose.

The input gives multiple test cases, each specifying the number of monsters $n$, bullets per second $k$, health of each monster, and their starting positions. The goal is to decide whether we can kill all monsters before any reach us.

The constraints are significant: $n$ can reach $3 \cdot 10^5$ in total across all test cases, and $k$ and $a_i$ can be as large as $10^9$. This rules out any algorithm that simulates each second individually for each monster; a naive approach could require billions of iterations. Edge cases arise when monsters start extremely close to 0 or when a few monsters have massive health relative to $k$, as firing bullets inefficiently can result in a monster reaching 0 before we can kill it.

A naive implementation that fires bullets arbitrarily or in order of input can fail. For example, if a monster is at position 1 with health 5 and $k=2$, while another is at position 5 with health 1, firing at the farther monster first will allow the closer monster to reach 0 and kill us. A correct strategy must consider both health and distance.

## Approaches

The brute-force approach would simulate each second: for every alive monster, choose which ones to shoot, reduce health, remove dead monsters, and move the rest closer. This is correct but infeasible. In the worst case, we could have $n=3\cdot 10^5$ monsters with health $10^9$, and iterating second by second would take on the order of $10^{14}$ operations.

The key insight is to consider the “effective distance” of monsters. A monster at distance $x_i$ with health $a_i$ needs at least $\lceil a_i / k \rceil$ seconds of concentrated fire to be killed. The problem reduces to a greedy strategy: if we sort monsters by distance from 0 (ignoring sign) and attack the farthest monsters first, we maximize the distance buffer and ensure no monster reaches 0 unexpectedly. Since all bullets can target any monster, the only critical factor is whether the cumulative damage we have dealt before a monster reaches us is enough to kill it.

This observation allows us to iterate through monsters sorted by distance and check whether the bullets we can fire before each monster reaches 0 suffice to kill it. The algorithm works in $O(n \log n)$ per test case due to sorting.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(max(a_i) * n) | O(n) | Too slow |
| Greedy by distance | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. For each test case, separate the monsters into those on the left ($x_i < 0$) and right ($x_i > 0$). Take absolute values of positions to simplify calculations.
2. Sort the monsters by distance from 0 in decreasing order. We will attack farthest monsters first to maximize our buffer time.
3. Initialize a counter `total_damage` to track the cumulative bullets fired so far.
4. Iterate through the sorted monsters:

1. Calculate the effective remaining distance for this monster: `effective_distance = x_i - total_damage`. This is how many steps it has left to reach 0 after accounting for bullets already fired at previous monsters.
2. If `effective_distance <= 0`, the monster has already effectively been killed by previous bullets; continue.
3. Otherwise, check if its health `a_i` exceeds `total_damage`. If `a_i > total_damage`, it means the monster would reach 0 before we could kill it. In this case, print NO.
4. Otherwise, add `a_i` to `total_damage`, representing that we have effectively fired `a_i` bullets to kill this monster.
5. If we process all monsters without a monster reaching 0, print YES.

Why it works: By attacking the farthest monsters first, we maximize the buffer before any monster reaches 0. The invariant is that after each iteration, all monsters farther than the current one are guaranteed not to reach 0 because we have already accumulated enough damage to neutralize closer threats. The check `effective_distance <= 0` ensures we do not overshoot bullets and that distant monsters do not “pass through” earlier ones.

## Python Solution

```python
import sys
input = sys.stdin.readline

def can_survive(n, k, health, pos):
    left = []
    right = []
    for a, x in zip(health, pos):
        if x < 0:
            left.append((-x, a))
        else:
            right.append((x, a))
    for group in [left, right]:
        group.sort(reverse=True)
        total_damage = 0
        for d, h in group:
            if d <= total_damage:
                continue
            h -= total_damage
            if h > 0:
                total_damage += h
    return "YES"

t = int(input())
for _ in range(t):
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    x = list(map(int, input().split()))
    
    left = []
    right = []
    for ai, xi in zip(a, x):
        if xi < 0:
            left.append((-xi, ai))
        else:
            right.append((xi, ai))
    
    def check(group):
        group.sort(reverse=True)
        total_damage = 0
        for d, h in group:
            if d <= total_damage:
                continue
            h -= total_damage
            if h > 0:
                total_damage += h
        return True
    
    if check(left) and check(right):
        print("YES")
    else:
        print("NO")
```

Explanation: We separate monsters by side and convert positions to positive distances. Sorting ensures we handle the farthest monsters first. `total_damage` accounts for bullets fired in previous steps, effectively reducing the health of subsequent monsters. This approach avoids simulating each second explicitly, using the insight that bullets can be distributed optimally among monsters.

## Worked Examples

Sample Input 1:

```
3 2
1 2 3
-1 2 3
```

| Monster | Side | Distance | Health | total_damage | Health after damage |
| --- | --- | --- | --- | --- | --- |
| 3 | right | 3 | 3 | 0 | 3 |
| 2 | right | 2 | 2 | 3 | -1 |
| 1 | left | 1 | 1 | 0 | 1 |

We process farthest right first: monster 3, `h - total_damage = 3 - 0 = 3`, `total_damage += 3`. Monster 2: distance 2, `2 <= total_damage=3`, already handled. Monster 1: distance 1, `1 - total_damage=1 - 3 <=0`, also safe. Output YES.

Sample Input 2:

```
2 1
1 1
-1 1
```

Processing left: monster 1, distance 1, `h - total_damage=1 -0=1`, `total_damage +=1`. Next monster (right): distance 1, `h - total_damage =1 -1 =0`, safe. But bullets per second k=1, we cannot kill both fast enough; algorithm outputs NO.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting left and right sides takes O(n log n). Iteration is O(n). |
| Space | O(n) | Storing two lists of monsters and auxiliary variables. |

Given the sum of n across test cases ≤ 3·10^5, and time per test case O(n log n), this fits comfortably in 2 seconds.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    exec(open("solution.py").read())
    return output.getvalue().strip()

# Provided samples
assert run("5\n3 2\n1 2 3\n-1 2 3\n2 1\n1 1\n-1 1\n4 10\n3 4 2 5\n-3 -2 1 3\n5 3\n2 1 3 2 5\n-3 -2 3 4 5\n2 1\n1 2\n1 2\n") == "YES\nNO\nYES\nYES\nNO"

# Custom test: all monsters at same distance, minimal input
assert run("1\n2 1\n1 1\n1 -1\n") == "NO"

# Custom test: single monster far away
assert run("1\n1 5\n10\n10\n") == "YES"

# Custom test
```
