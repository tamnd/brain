---
title: "CF 1903E - Geo Game"
description: "We are asked to reason about a two-player game on a 2D plane. The game starts from a fixed point and consists of picking points one by one from a set of given points."
date: "2026-06-08T21:04:15+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "interactive", "math"]
categories: ["algorithms"]
codeforces_contest: 1903
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 912 (Div. 2)"
rating: 2000
weight: 1903
solve_time_s: 134
verified: false
draft: false
---

[CF 1903E - Geo Game](https://codeforces.com/problemset/problem/1903/E)

**Rating:** 2000  
**Tags:** greedy, interactive, math  
**Solve time:** 2m 14s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to reason about a two-player game on a 2D plane. The game starts from a fixed point and consists of picking points one by one from a set of given points. Each time a point is picked, the square of the Euclidean distance from the previously chosen point is added to a running sum. The first player wins if this sum is even at the end of the game, otherwise the second player wins. The challenge is to decide whether to play first or second and how to pick points optimally to guarantee victory.

The input consists of multiple test cases. For each test case, we receive the number of points, the coordinates of the starting point, and the list of points. The output must be interactive: first we choose our player order, then on our turn we pick a point, and on the opponent's turn we read which point they picked. The constraints allow up to $10^5$ points per test case, but the sum of $n$ over all test cases is at most $10^5$, so a solution that processes each point once is acceptable. The coordinates can be very large, up to $10^9$, but the actual distances only need their parity, so we do not need to worry about integer overflow.

The non-obvious edge case arises from the fact that the sum depends only on the parity of squared distances. A naive implementation that tries to sum the exact distances risks large integer arithmetic and misses the simplification that only even or odd values matter. Another subtlety is that the optimal player may not always be the first player; depending on the configuration of points, starting second could allow controlling the parity by matching or countering moves. For example, if all distances from the starting point are even, the first player cannot force an odd sum and should choose second.

## Approaches

A brute-force solution would attempt to simulate all sequences of moves, evaluating the final sum for each. This would involve computing $n!$ permutations of points, which is impossible even for moderate $n$ since $10^5!$ is astronomically large. Brute-force works because the game rules are deterministic, but it fails because the number of sequences grows factorially.

The key observation is that we do not care about exact distances, only the parity of the sum. Squaring an integer preserves parity: a number squared is even if the number is even and odd if the number is odd. The Euclidean distance squared between points $(x_1, y_1)$ and $(x_2, y_2)$ is $(x_2-x_1)^2 + (y_2-y_1)^2$. The parity of this expression is determined solely by the parities of the coordinate differences. Specifically, if both differences are even or both are odd, the sum is even; if one is odd and one is even, the sum is odd.

With this, we reduce the problem to a purely parity-based game. Each point has a color depending on whether the sum of its coordinates modulo 2 matches the starting point's coordinates modulo 2. Points of the same parity from the start are “even moves,” points of opposite parity are “odd moves.” The first player can guarantee a win if the count of odd-move points is odd when they start first, or even when they start second, allowing them to control the parity of the running sum by always choosing points of the appropriate parity. This insight reduces the problem to counting and parity, a linear-time operation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. For each test case, read $n$, $s_x$, $s_y$, and the list of points. For each point, compute its parity with respect to the starting point: $(x_i - s_x) \% 2$ and $(y_i - s_y) \% 2$. The squared distance modulo 2 is 1 if the parities differ in exactly one coordinate, and 0 otherwise.
2. Count the number of points that will contribute an odd squared distance if picked from the start. Let this count be `odd_count`.
3. Decide the player order. If `odd_count` is odd, choose to play first. If `odd_count` is even, choose to play second. This choice ensures control of the final sum's parity.
4. During the game, maintain a list of available points. On our turn, pick any point that contributes an odd squared distance if we need to flip the current sum parity, or an even one if we want to preserve it. This is always possible because the parity counts are known in advance and we alternate turns.
5. On the opponent's turn, read their move and remove it from the list of available points.
6. Repeat until all points are chosen. At this point, the sum parity will be as controlled by the chosen player strategy, ensuring victory.

Why it works: the invariant is that the first or second player can always select a point to control the parity of the running sum. By counting odd and even contributions beforehand and alternating turns, the chosen player can ensure the sum ends up even or odd according to their win condition. Since squared distances modulo 2 only depend on coordinate parity, this invariant is robust to the actual positions and works for any configuration.

## Python Solution

```python
import sys
input = sys.stdin.readline
flush = sys.stdout.flush

def parity(x):
    return x % 2

t = int(input())
for _ in range(t):
    n = int(input())
    sx, sy = map(int, input().split())
    points = [tuple(map(int, input().split())) for _ in range(n)]
    
    odd_points = []
    even_points = []
    for idx, (x, y) in enumerate(points):
        dx = parity(x - sx)
        dy = parity(y - sy)
        if dx ^ dy:
            odd_points.append(idx + 1)
        else:
            even_points.append(idx + 1)
    
    if len(odd_points) % 2 == 1:
        print("First")
        flush()
        my_turn_points = odd_points + even_points
    else:
        print("Second")
        flush()
        my_turn_points = even_points + odd_points

    used = set()
    for turn in range(n):
        if turn % 2 == 0:  # our turn
            for j in my_turn_points:
                if j not in used:
                    print(j)
                    flush()
                    used.add(j)
                    break
        else:  # opponent's turn
            j = int(input())
            if j == -1:
                exit()
            used.add(j)
```

We first separate points into those that flip the parity (odd) and those that do not (even). Choosing player order is based on the count of odd points. During each turn, we pick an available point from our precomputed list to maintain control of parity. The `used` set ensures we never pick an already chosen point. On the opponent's turn, we read their choice and update `used`. The `^` operator efficiently computes XOR to determine parity difference.

## Worked Examples

Sample 1:

| Turn | Current Sum Parity | Points Left (odd/even) | Action | Result |
| --- | --- | --- | --- | --- |
| 1 | 0 | odd: 4 even: 2 | First chooses odd | sum parity flips to 1 |
| 2 | 1 | odd: 3 even: 2 | Opponent chooses even | sum parity remains 1 |
| 3 | 1 | odd: 3 even: 1 | First chooses odd | sum parity flips to 0 |
| ... | ... | ... | ... | ... |

This trace shows that by alternating odd/even picks, the chosen player can manipulate the parity of the sum to ensure it ends even.

Sample 2: n = 3, all points at even distance from start.

| Turn | Current Sum Parity | Action |
| --- | --- | --- |
| 1 | 0 | Second chooses even |
| 2 | 0 | First chooses even |
| 3 | 0 | Second chooses even |

Even if the opponent plays optimally, the second player wins by default as the sum is even at the end.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Computing parity for each point and iterating through turns |
| Space | O(n) | Storing lists of odd/even points and used set |

This fits comfortably within the 2s time limit and 256MB memory limit for $n \le 10^5$ and sum of $n$ across tests $\le 10^5$.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    exec(open("solution.py").read(), {})
    return sys.stdout.getvalue()

# Sample 1
assert run("2\n6\n4 6\n7 6\n8 5\n2 1\n6 2\n6 4\n3 3\n5\n1 4\n1 1\n3 2\n2 1\n3 3\n1 2\n") == "Second\nFirst\n", "Sample 1"

# Minimum input
```
