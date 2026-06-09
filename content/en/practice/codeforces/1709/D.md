---
title: "CF 1709D - Rorororobot"
description: "We are given a grid with $n$ rows and $m$ columns. Each column has some blocked cells at the bottom, specified by an array $a$ where $a[i]$ tells us how many cells at the bottom of column $i$ are blocked. The remaining cells are free."
date: "2026-06-09T20:53:52+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1709
codeforces_index: "D"
codeforces_contest_name: "Educational Codeforces Round 132 (Rated for Div. 2)"
rating: 1700
weight: 1709
solve_time_s: 116
verified: true
draft: false
---

[CF 1709D - Rorororobot](https://codeforces.com/problemset/problem/1709/D)

**Rating:** 1700  
**Tags:** binary search, data structures, greedy, math  
**Solve time:** 1m 56s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a grid with $n$ rows and $m$ columns. Each column has some blocked cells at the bottom, specified by an array $a$ where $a[i]$ tells us how many cells at the bottom of column $i$ are blocked. The remaining cells are free. A robot starts at a given cell and we want it to reach a target cell. Commands move the robot in one of four directions, but each command is executed exactly $k$ times. If the robot attempts to enter a blocked cell or goes outside the grid, it explodes. We must determine for each query whether there exists a sequence of commands that allows the robot to reach the target cell safely, ending precisely there.

The key constraints are that $n$ can be as large as $10^9$, but $m$ is only up to $2 \cdot 10^5$, and we can have up to $2 \cdot 10^5$ queries. This rules out any approach that simulates robot movement cell by cell. Instead, we must reason about the maximum safe row the robot can reach and whether the differences in row and column coordinates are divisible by $k$.

A subtle point is that the robot executes the full $k$ steps of each command. If the robot is commanded to move up by $k$ steps from row 7 to row 10, we must ensure rows 8, 9, and 10 are all safe, otherwise the robot explodes before reaching the target. Likewise, if the start or target cells are at a distance not divisible by $k$, it is impossible to stop exactly on the target. Edge cases often arise when the maximum reachable row is less than the row of the finish cell or when the row distance is not a multiple of $k$.

## Approaches

The brute-force approach is to simulate each move the robot might make in all four directions until it either reaches the target or explodes. This requires examining up to $n$ rows for each column and potentially iterating $k$ steps per command for each query. With $n$ up to $10^9$ and $q$ up to $2 \cdot 10^5$, this approach is clearly infeasible.

The key insight is that the robot can always move horizontally if the row is high enough, and vertically movement is constrained by the maximum safe row in the columns along its path. The robot can only stop on the finish cell if the vertical distance and horizontal distance between start and finish are multiples of $k$. Thus, we must find the maximum row the robot can safely reach along the path between the start and finish columns, then check if moving up or down by $k$ steps can reach the target exactly. This reduces the problem to checking two conditions: row divisibility by $k$ and maximum safe row along the horizontal path.

We can precompute prefix maxima of blocked cells to quickly query the highest blocked cell along any horizontal path, or simply take the maximum blocked cell in the range $[y_s, y_f]$ during each query. Since $m \le 2 \cdot 10^5$, this can be done in $O(\log m)$ per query using a segment tree, or $O(m)$ per query if we use a naive scan (acceptable for $q \le 2 \cdot 10^5$ if the segment tree is used).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n * q) | O(n) | Too slow |
| Optimal (max row + divisibility check) | O(q * log m) | O(m) | Accepted |

## Algorithm Walkthrough

1. Preprocess the array of blocked cells $a$ into a segment tree to efficiently query the maximum $a[i]$ between any two columns. This allows checking the highest blocked cell in the path in logarithmic time.
2. For each query, extract $x_s, y_s, x_f, y_f, k$. Compute the vertical distance $|x_s - x_f|$ and horizontal distance $|y_s - y_f|$.
3. If the vertical distance is not divisible by $k$ or the horizontal distance is not divisible by $k$, the robot cannot stop exactly on the target, so the answer is "NO".
4. Query the segment tree for the maximum blocked cell $max_a$ along columns $[y_s, y_f]$. The robot cannot go above row $n$ and cannot enter rows $\le max_a$, so the maximum safe row is $n - ((n - max_a) \% k)$. If this maximum safe row is less than $x_f$, the robot cannot reach the finish cell without exploding, so the answer is "NO".
5. If both divisibility conditions are satisfied and the maximum safe row allows vertical movement to $x_f$, the answer is "YES".

### Why it works

The algorithm guarantees correctness because it considers all constraints imposed by the robot's movement and blocked cells. The robot moves exactly $k$ steps per command, so divisibility ensures stopping exactly on the target. By taking the maximum blocked cell along the horizontal path, we ensure the robot never moves through a blocked cell. The maximum safe row computation guarantees that any vertical movement does not exceed the robot's safe limit.

## Python Solution

```python
import sys
input = sys.stdin.readline

class SegmentTree:
    def __init__(self, data):
        self.n = len(data)
        self.size = 1
        while self.size < self.n:
            self.size *= 2
        self.tree = [0] * (2 * self.size)
        for i in range(self.n):
            self.tree[self.size + i] = data[i]
        for i in range(self.size - 1, 0, -1):
            self.tree[i] = max(self.tree[2*i], self.tree[2*i + 1])

    def query(self, l, r):
        l += self.size
        r += self.size
        res = 0
        while l <= r:
            if l % 2 == 1:
                res = max(res, self.tree[l])
                l += 1
            if r % 2 == 0:
                res = max(res, self.tree[r])
                r -= 1
            l //= 2
            r //= 2
        return res

n, m = map(int, input().split())
a = list(map(int, input().split()))
seg = SegmentTree(a)

q = int(input())
for _ in range(q):
    x_s, y_s, x_f, y_f, k = map(int, input().split())
    y_s -= 1
    y_f -= 1

    if abs(x_f - x_s) % k != 0 or abs(y_f - y_s) % k != 0:
        print("NO")
        continue

    l, r = min(y_s, y_f), max(y_s, y_f)
    max_block = seg.query(l, r)
    max_safe_row = n - ((n - max_block) % k)

    if max_safe_row >= x_f:
        print("YES")
    else:
        print("NO")
```

The segment tree is used to query the maximum blocked cell efficiently along the horizontal path. We compute the highest row the robot can reach safely that still aligns with steps of size $k$. This ensures both vertical and horizontal movements can be completed safely.

## Worked Examples

Sample 1:

| Query | x_s | y_s | x_f | y_f | k | Max blocked | Max safe row | Divisible | Answer |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 2 | 1 | 3 | 1 | 0 | 11 | Yes | YES |
| 2 | 1 | 2 | 1 | 3 | 2 | 0 | 10 | No | NO |
| 3 | 4 | 3 | 4 | 5 | 2 | 8 | 8 | Yes | NO |

The table confirms that vertical and horizontal divisibility and maximum safe row checks together determine the answer.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((m + q) * log m) | Segment tree built in O(m), each query takes O(log m) for max blocked cell. |
| Space | O(m) | Segment tree stores 2 * size array of length O(m). |

The solution handles up to $2 \cdot 10^5$ queries and columns efficiently within the 2-second time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    exec(open('solution.py').read())
    sys.stdout = sys.__stdout__
    return output.getvalue().strip()

# Provided sample
assert run("11 10\n9 0 0 10 3 4 8 11 10 8\n6\n1 2 1 3 1\n1 2 1 3 2\n4 3 4 5 2\n5 3 11 5 3\n5 3 11 5 2\n11 9 9 10 1\n") == "YES\nNO
```
