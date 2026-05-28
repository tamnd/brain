---
title: "CF 139B - Wallpaper"
description: "We are asked to compute the minimum cost to paper all walls in an apartment where each room is a rectangular prism. For each room, the length, width, and height are given. The perimeter of a room determines how many strips of wallpaper are needed."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 139
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 99 (Div. 2)"
rating: 1600
weight: 139
solve_time_s: 87
verified: true
draft: false
---

[CF 139B - Wallpaper](https://codeforces.com/problemset/problem/139/B)

**Rating:** 1600  
**Tags:** implementation, math  
**Solve time:** 1m 27s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to compute the minimum cost to paper all walls in an apartment where each room is a rectangular prism. For each room, the length, width, and height are given. The perimeter of a room determines how many strips of wallpaper are needed. Each type of wallpaper comes in rolls of fixed width and length, and the roll cannot be rotated. Strips are cut vertically along the roll, and each room must be papered with a single type of wallpaper. Partial rolls are allowed, but rolls cannot be shared across rooms. Our goal is to pick, for each room, the wallpaper type and the number of rolls that minimize total cost.

The constraints are modest: the number of rooms and types of wallpaper is at most 500. Dimensions and prices are capped at 500. This allows algorithms with up to roughly $O(n \cdot m)$ complexity. Because all input numbers are small integers, there are no concerns with floating point precision, but careful integer arithmetic is needed to avoid off-by-one errors when computing the number of strips per roll.

An edge case to watch is when a roll width is larger than the room perimeter, so a single roll suffices. Another case is when the roll length allows only a small number of strips, requiring multiple rolls. For example, a room with perimeter 6 meters and height 5 meters, using a roll 4 meters long and 2 meters wide, needs careful computation to ensure we buy two rolls instead of mistakenly one.

## Approaches

The brute-force approach is straightforward: for each room, iterate through each wallpaper type and compute the number of rolls required to cover the room fully. Multiply the number of rolls by the price to get the cost for that combination. Then pick the cheapest wallpaper type for the room. Sum these minimal costs across all rooms. This works because each room is independent; however, we must carefully compute the number of strips per roll and how many rolls are needed. With $n \le 500$ rooms and $m \le 500$ wallpaper types, this approach results in at most $500 \cdot 500 = 250,000$ operations, which is acceptable for a 2-second time limit.

The key observation that simplifies computation is that the number of strips a roll can provide is the integer division of the roll length by the room height, and the number of strips needed is the integer division of the room perimeter by the roll width, rounded up. With these two integer divisions, we can compute the minimal number of rolls needed for any wallpaper type-room combination. No dynamic programming or graph algorithms are necessary because rooms do not interact.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * m) | O(1) | Accepted |
| Optimal | O(n * m) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read input values: number of rooms, room dimensions, number of wallpaper types, and roll specifications with prices.
2. Initialize a variable `total_cost` to zero.
3. For each room, compute the perimeter as `2 * (length + width)` and store the height.
4. Initialize `min_cost` for the current room to infinity.
5. For each wallpaper type, determine how many vertical strips a single roll provides by integer-dividing the roll length by the room height.
6. Determine the total number of strips needed for the room by dividing the perimeter by the roll width and rounding up.
7. Compute the number of rolls needed as the ceiling of `required_strips / strips_per_roll`.
8. Multiply the number of rolls by the price of the wallpaper type to get the total cost for this wallpaper type.
9. Update `min_cost` if this cost is lower than the current `min_cost`.
10. After considering all wallpaper types for the room, add `min_cost` to `total_cost`.
11. Print `total_cost`.

The correctness relies on two facts: each room is covered by exactly one wallpaper type, and strips cannot be shared across rolls or rooms. Computing the number of strips and rolls with integer arithmetic ensures we do not underestimate the rolls needed. Considering all wallpaper types guarantees the minimum cost is found for each room independently, so summing across rooms gives the global minimum.

## Python Solution

```python
import sys
import math
input = sys.stdin.readline

n = int(input())
rooms = []
for _ in range(n):
    l, w, h = map(int, input().split())
    rooms.append((l, w, h))

m = int(input())
wallpapers = []
for _ in range(m):
    roll_length, roll_width, price = map(int, input().split())
    wallpapers.append((roll_length, roll_width, price))

total_cost = 0

for length, width, height in rooms:
    perimeter = 2 * (length + width)
    min_cost = float('inf')
    for roll_length, roll_width, price in wallpapers:
        strips_per_roll = roll_length // height
        if strips_per_roll == 0:
            continue
        strips_needed = (perimeter + roll_width - 1) // roll_width
        rolls_needed = (strips_needed + strips_per_roll - 1) // strips_per_roll
        cost = rolls_needed * price
        min_cost = min(min_cost, cost)
    total_cost += min_cost

print(total_cost)
```

The code reads all rooms and wallpapers first to avoid interleaving input processing with computation. Integer division ensures we correctly compute strips per roll and rolls needed. The addition of `roll_width - 1` and `strips_per_roll - 1` before integer division simulates the ceiling operation, which avoids floating point arithmetic and guarantees correctness.

## Worked Examples

### Example 1

Input:

```
1
5 5 3
3
10 1 100
15 2 320
3 19 500
```

| Room | Perimeter | Wallpaper | Strips/Roll | Strips Needed | Rolls | Cost | Min Cost |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 5x5x3 | 20 | 10x1,100 | 3 | 20 | 7 | 700 | 640 |
|  |  | 15x2,320 | 5 | 10 | 2 | 640 | 640 |
|  |  | 3x19,500 | 1 | 20 | 2 | 1000 | 640 |

The algorithm correctly chooses the second wallpaper type with total cost 640.

### Example 2

Input:

```
2
3 4 2
6 5 3
2
10 2 200
6 1 100
```

| Room | Perimeter | Wallpaper | Strips/Roll | Strips Needed | Rolls | Cost | Min Cost |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 3x4x2 | 14 | 10x2,200 | 5 | 7 | 2 | 400 | 400 |
|  |  | 6x1,100 | 3 | 14 | 5 | 500 | 400 |
| 6x5x3 | 22 | 10x2,200 | 3 | 11 | 4 | 800 | 800 |
|  |  | 6x1,100 | 2 | 22 | 11 | 1100 | 800 |

Total cost = 400 + 800 = 1200.

This demonstrates that the algorithm correctly computes strips per roll and rolls needed for multiple rooms.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n * m) | For each of n rooms, we examine m wallpaper types, computing a few integer divisions per iteration. |
| Space | O(n + m) | We store room dimensions and wallpaper specifications. |

With $n, m \le 500$, the total number of operations is at most 250,000, which easily fits in the 2-second time limit and 256 MB memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    rooms = [tuple(map(int, input().split())) for _ in range(n)]
    m = int(input())
    wallpapers = [tuple(map(int, input().split())) for _ in range(m)]
    
    total_cost = 0
    for length, width, height in rooms:
        perimeter = 2 * (length + width)
        min_cost = float('inf')
        for roll_length, roll_width, price in wallpapers:
            strips_per_roll = roll_length // height
            if strips_per_roll == 0:
                continue
            strips_needed = (perimeter + roll_width - 1) // roll_width
            rolls_needed = (strips_needed + strips_per_roll - 1) // strips_per_roll
            cost = rolls_needed * price
            min_cost = min(min_cost, cost)
        total_cost += min_cost
    return str(total_cost)

# provided sample
assert run("1\n5 5 3\n3\n10 1 100\n15 2 320\n3 19 500\n") == "640", "sample 1"

# minimum input
assert run("1\n1 1 1\n1\n1 1 1\n") == "1", "minimum input"

# equal dimensions and prices
assert run("2\n2 2 2\n2 2 2\n2\n4 1 2\n4 2 3\n") ==
```
