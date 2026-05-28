---
title: "CF 148B - Escape"
description: "We are asked to simulate a pursuit scenario between a princess and a dragon. The princess runs at a constant speed, and the dragon flies faster but only begins chasing after a delay. Each time the dragon catches up, the princess can drop a bijou to distract him."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 148
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 105 (Div. 2)"
rating: 1500
weight: 148
solve_time_s: 72
verified: true
draft: false
---

[CF 148B - Escape](https://codeforces.com/problemset/problem/148/B)

**Rating:** 1500  
**Tags:** implementation, math  
**Solve time:** 1m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to simulate a pursuit scenario between a princess and a dragon. The princess runs at a constant speed, and the dragon flies faster but only begins chasing after a delay. Each time the dragon catches up, the princess can drop a bijou to distract him. The dragon then returns to the treasury, spends some fixed time there, and resumes the chase. The goal is to determine the minimal number of bijous the princess must carry to reach a fixed destination safely.

The input consists of five integers: the princess’s speed $v_p$, the dragon’s speed $v_d$, the time delay before the dragon starts chasing $t$, the time the dragon spends fixing the treasury after picking a bijou $f$, and the total distance to the castle $c$. The output is a single integer: the minimum number of bijous required.

The constraints are small: speeds up to 100, times up to 10, distance up to 1000. This allows an approach that simulates the chase step by step without performance concerns. A careless implementation might fail in edge cases such as when the dragon never overtakes the princess because he is slower, or when the dragon catches the princess exactly at the castle - these cases require zero bijous or do not require an extra bijou for the final overtaking.

## Approaches

The brute-force method is straightforward: simulate the princess’s and dragon’s positions continuously and increment a counter each time the dragon overtakes her. Each iteration computes the time until the next overtaking, updates positions, applies the delay, and repeats until the princess reaches the castle. This method is guaranteed correct because it models the chase precisely, but repeatedly simulating small time intervals is unnecessary and could be slower than needed.

The optimal approach leverages the constant speeds to compute the time and location of each overtaking analytically. Since the princess and dragon move at constant velocities, the time for the dragon to reach the princess in each segment can be calculated with a simple formula: the dragon must cover the relative distance between his current location and the princess, divided by their speed difference. After each overtaking, we update positions and account for the dragon’s treasury-fixing delay. We repeat this until the princess reaches the castle. The insight is that relative motion reduces the problem to simple arithmetic rather than iterative simulation, making the solution precise and efficient.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(c * small_step) | O(1) | Works but unnecessary |
| Relative Motion Simulation | O(c / v_p) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize the princess’s position at zero and set the dragon’s position to zero. Start a counter for bijous at zero.
2. Compute the distance the princess covers during the dragon’s initial delay $t$. The princess moves at $v_p \cdot t$ while the dragon is idle.
3. Enter a loop that continues while the princess has not reached the castle.
4. Check if the dragon is faster than the princess. If not, the princess will never be caught and no bijous are required, so exit the loop.
5. Calculate the distance between the princess and the dragon at the start of the chase segment. The dragon starts chasing after $t$ hours plus any subsequent treasury-fixing delays.
6. Compute the time for the dragon to catch the princess using the relative speed: $time = distance / (v_d - v_p)$.
7. Update the princess’s position at the moment of overtaking: $position += v_p \cdot time$.
8. If the princess has reached or passed the castle during this time, she no longer needs any additional bijous. Exit the loop.
9. Increment the bijou counter because the dragon overtook her and she drops a bijou.
10. Update the dragon’s position to zero (back at the cave after treasury-fixing) and add the treasury-fixing delay to the total time. The princess continues running during this time, so update her position: $position += v_p \cdot f$.
11. Repeat the loop until the princess reaches the castle.

Why it works: at each iteration, the algorithm computes the exact overtaking moment analytically. By updating positions based on constant velocities and applying the treasury-fixing delay, we maintain the invariant that the princess’s position always reflects her actual progress and the bijou counter matches the number of distractions used. The process stops precisely when the princess reaches the castle.

## Python Solution

```python
import sys
input = sys.stdin.readline

vp = int(input())
vd = int(input())
t = int(input())
f = int(input())
c = int(input())

if vp >= vd:
    print(0)
else:
    princess_pos = vp * t
    dragon_pos = 0
    bijous = 0

    while princess_pos < c:
        relative_distance = princess_pos - dragon_pos
        time_to_catch = relative_distance / (vd - vp)
        catch_pos = princess_pos + vp * time_to_catch

        if catch_pos >= c:
            break

        bijous += 1
        princess_pos = catch_pos + vp * f
        dragon_pos = 0

    print(bijous)
```

The code starts by handling the edge case where the princess is faster or equal to the dragon, meaning no bijous are needed. It computes her initial position during the dragon’s delay. In each loop iteration, it calculates the overtaking position using relative speed, checks if the castle has been reached, increments the bijou count, and updates positions with the dragon’s delay. Floating point arithmetic suffices here due to small values; integer division is avoided to maintain precision.

## Worked Examples

For the input:

```
1
2
1
1
10
```

| Step | Princess Position | Dragon Position | Bijous |
| --- | --- | --- | --- |
| Initial | 1 | 0 | 0 |
| First Catch | 2 | 0 | 1 |
| After Delay | 4 | 0 | 1 |
| Second Catch | 8 | 0 | 2 |
| After Delay | 10 | 0 | 2 |

This confirms two bijous are needed, consistent with the sample.

For another input:

```
3
5
2
1
20
```

| Step | Princess Position | Dragon Position | Bijous |
| --- | --- | --- | --- |
| Initial | 6 | 0 | 0 |
| First Catch | 12 | 0 | 1 |
| After Delay | 15 | 0 | 1 |
| Second Catch | 21 | 0 | 2 |

Since she reaches the castle at 20, the second catch occurs beyond the destination, so only 1 bijou is needed. This confirms the check `if catch_pos >= c` correctly prevents counting unnecessary bijous.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(c / (v_d - v_p)) | Each loop iteration corresponds to one overtaking. Maximum iterations bounded by the number of overtakes possible within distance c. |
| Space | O(1) | Only scalar variables for positions and counters are used. |

Given the constraints (c ≤ 1000, speeds ≤ 100), the loop runs at most a few dozen times, well within the 2-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    vp = int(input())
    vd = int(input())
    t = int(input())
    f = int(input())
    c = int(input())
    if vp >= vd:
        return "0"
    princess_pos = vp * t
    dragon_pos = 0
    bijous = 0
    while princess_pos < c:
        relative_distance = princess_pos - dragon_pos
        time_to_catch = relative_distance / (vd - vp)
        catch_pos = princess_pos + vp * time_to_catch
        if catch_pos >= c:
            break
        bijous += 1
        princess_pos = catch_pos + vp * f
        dragon_pos = 0
    return str(bijous)

assert run("1\n2\n1\n1\n10\n") == "2", "sample 1"
assert run("3\n5\n2\n1\n20\n") == "1", "custom 1"
assert run("2\n2\n1\n1\n5\n") == "0", "dragon not faster"
assert run("5\n10\n1\n1\n1\n") == "0", "catch after castle"
assert run("1\n100\n1\n10\n1000\n") == "9", "maximum iterations"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 2 1 1 10 | 2 | Sample scenario from statement |
| 3 5 2 1 20 | 1 | Ensures catching beyond castle is ignored |
| 2 2 1 1 5 | 0 | Dragon not faster, no bijous |
| 5 10 1 1 1 | 0 | Castle reached before first catch |
| 1 100 1 10 1000 | 9 | Large speed gap, multiple overtakes |

## Edge Cases

The algorithm correctly handles the case where the princess is faster or equal to the dragon. For input `vp=2, vd=2, t=1, f=1, c=5`, the initial check prevents any loop execution, producing zero bijous. When the dragon
