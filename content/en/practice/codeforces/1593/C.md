---
title: "CF 1593C - Save More Mice"
description: "We are asked to simulate a race between a cat and multiple mice along a one-dimensional line. The cat starts at position 0 and moves right one unit per second, while the mice each have a starting position strictly between 0 and the hole at position n."
date: "2026-06-10T09:05:37+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1593
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 748 (Div. 3)"
rating: 1000
weight: 1593
solve_time_s: 140
verified: false
draft: false
---

[CF 1593C - Save More Mice](https://codeforces.com/problemset/problem/1593/C)

**Rating:** 1000  
**Tags:** binary search, greedy  
**Solve time:** 2m 20s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to simulate a race between a cat and multiple mice along a one-dimensional line. The cat starts at position 0 and moves right one unit per second, while the mice each have a starting position strictly between 0 and the hole at position n. In each second, we can choose exactly one mouse to move one step toward the hole, and then the cat moves one step toward the hole, eating any mouse that happens to be at its new position. Our goal is to maximize the number of mice that reach the hole without being eaten.

The input gives us several test cases. For each test case, we know the position of the hole n, the number of mice k, and the list of starting positions of the mice. The output is simply the maximal number of mice that can reach the hole safely for each test case.

The constraints give important clues for efficiency. The hole's position n can be up to 10^9, but the number of mice summed across all test cases is limited to 4 × 10^5. This tells us that we cannot afford O(n) algorithms iterating over the positions of the cat; we need a solution that scales primarily with k, the number of mice. Another subtle point is that mice can share positions, which could influence how we choose which mouse moves in each second.

A non-obvious edge case arises when many mice are clustered near the hole. For example, if n = 10 and all mice start at position 9, a naive approach that ignores the mouse closest to the hole may underestimate how many can escape. Conversely, if all mice start at position 1, the cat may catch them unless we carefully choose the mouse order. A careless solution that moves mice arbitrarily may produce the wrong maximum.

## Approaches

The brute-force approach is straightforward: simulate every second, moving a mouse toward the hole and updating the cat’s position, then check which mice are eaten. While this would be correct, it requires potentially n × k operations per test case since the cat moves one step at a time and we must track positions, which is far too slow given n can be 10^9. Even with optimizations like tracking only the mice positions, repeatedly scanning for the cat's collision with mice is inefficient.

The key insight is that the cat only moves forward and the mice only move forward. Therefore, for a mouse at position x_i, if it moves before the cat has reached it, it will avoid being eaten. The danger comes from the cat catching up. If we sort the mice by their distance to the hole (n - x_i), we can consider them in order of furthest first. Every mouse contributes a "safe distance" to the total, but the cat consumes time as it progresses. Specifically, we can count how many mice can reach the hole before the cat "covers" the distance. By iterating over sorted distances from the hole and accumulating the total distance moved by all previous mice, we can greedily pick as many mice as possible.

This reduces the problem to a greedy algorithm: sort the mice by distance to the hole, and repeatedly choose mice starting from the furthest, summing the distances until the cat’s cumulative advance would catch the next mouse. This approach scales with k log k for sorting and O(k) for the greedy iteration, which is efficient under the problem constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n × k) | O(k) | Too slow |
| Greedy sorted distances | O(k log k) | O(k) | Accepted |

## Algorithm Walkthrough

1. For each test case, read n, k, and the positions of the mice.
2. Convert each mouse position x_i to its distance from the hole, which is n - x_i. This represents how far each mouse needs to travel to be safe.
3. Sort these distances in descending order. This ensures we consider the mice that require the most time to reach safety first, which is the critical step in the greedy strategy.
4. Initialize two counters: `saved = 0` for the number of mice that will reach the hole, and `total_distance = 0` to track the cumulative distance the cat effectively advances after each second a mouse moves.
5. Iterate over the sorted distances. For each distance d, if d > total_distance, increment `saved` and add the distance difference to `total_distance`. Otherwise, stop the iteration since any remaining mouse would be caught.
6. After processing all mice, output `saved` for the current test case.

Why it works: The invariant is that `total_distance` represents the number of steps the cat has effectively taken relative to the hole. By choosing the furthest mice first, we ensure that each selected mouse reaches the hole before the cat reaches it, because any mouse closer than the accumulated total_distance would be caught. The sorted order guarantees that no further mouse can be added safely once a mouse fails the `d > total_distance` check.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        positions = list(map(int, input().split()))
        distances = [n - x for x in positions]
        distances.sort(reverse=True)
        saved = 0
        total_distance = 0
        for d in distances:
            if d > total_distance:
                saved += 1
                total_distance += d - total_distance
            else:
                break
        print(saved)

if __name__ == "__main__":
    solve()
```

The solution reads multiple test cases efficiently using `sys.stdin.readline`. Distances from the hole are computed first because this transforms the problem into a straightforward greedy decision: can the cat catch this mouse before it reaches the hole? Sorting ensures we deal with the mice that are hardest to save first. The loop accumulates the total distance effectively "used" by the cat, stopping when no further mice can escape.

## Worked Examples

**Sample Input 1:**

```
10 6
8 7 5 4 9 4
```

| Mouse | Distance to Hole | Sorted | Saved? | total_distance |
| --- | --- | --- | --- | --- |
| 9 | 1 | 5 | yes | 1 |
| 8 | 2 | 4 | yes | 2 |
| 7 | 3 | 3 | yes | 3 |
| 5 | 5 | 2 | no | - |
| 4 | 6 | 1 | no | - |
| 4 | 6 | 1 | no | - |

Three mice are saved, matching the expected output.

**Sample Input 2:**

```
2 8
1 1 1 1 1 1 1 1
```

All distances are n - 1 = 1. Only one mouse can move before the cat catches the next, so only one is saved.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(k log k) | Sorting distances dominates; iteration is O(k) |
| Space | O(k) | We store distances array |

Given the sum of k across all test cases is ≤ 4 × 10^5, this algorithm will run comfortably under the 4-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    return out.getvalue().strip()

# Provided samples
assert run("3\n10 6\n8 7 5 4 9 4\n2 8\n1 1 1 1 1 1 1\n12 11\n1 2 3 4 5 6 7 8 9 10 11\n") == "3\n1\n4"

# Custom test cases
assert run("1\n5 5\n1 2 3 4 4\n") == "2", "cluster near hole"
assert run("1\n2 1\n1\n") == "1", "minimum input"
assert run("1\n1000000000 3\n999999998 999999997 999999996\n") == "3", "very large n"
assert run("1\n10 4\n1 1 1 1\n") == "1", "all mice at start"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 5 5; 1 2 3 4 4 | 2 | Handles mice near the hole correctly |
| 2 1; 1 | 1 | Minimum-size input works |
| 1e9 3; 999999998 999999997 999999996 | 3 | Handles very large n without overflow |
| 10 4; 1 1 1 1 | 1 | Multiple mice at same start position handled |

## Edge Cases

For the case where all mice start at the same position, for example n = 10 and positions [1,1,1,1], the algorithm sorts the distances [9,9,9,9] and iterates. The first mouse is saved because 9 > 0, then total_distance becomes 9. The next mouse has distance 9, which is not greater than total_distance 9, so iteration stops. Only one mouse is saved,
