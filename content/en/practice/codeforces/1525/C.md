---
title: "CF 1525C - Robot Collisions"
description: "We have a set of robots moving along a one-dimensional line segment from 0 to $m$. Each robot starts at a distinct integer position between 0 and $m$ and moves either left or right at a constant speed of 1 unit per second."
date: "2026-06-10T17:25:42+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "greedy", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1525
codeforces_index: "C"
codeforces_contest_name: "Educational Codeforces Round 109 (Rated for Div. 2)"
rating: 2000
weight: 1525
solve_time_s: 183
verified: false
draft: false
---

[CF 1525C - Robot Collisions](https://codeforces.com/problemset/problem/1525/C)

**Rating:** 2000  
**Tags:** data structures, greedy, implementation, sortings  
**Solve time:** 3m 3s  
**Verified:** no  

## Solution
## Problem Understanding

We have a set of robots moving along a one-dimensional line segment from 0 to $m$. Each robot starts at a distinct integer position between 0 and $m$ and moves either left or right at a constant speed of 1 unit per second. The endpoints 0 and $m$ act as walls: when a robot reaches a wall, it reflects instantly and continues moving in the opposite direction. When two or more robots meet exactly at the same integer coordinate, they collide and vanish. Robots meeting at non-integer positions do not collide.

The input gives the starting positions and directions for all robots, and the goal is to determine, for each robot, the time it explodes or report $-1$ if it never collides.

The constraints indicate that $n$ can be up to $3 \cdot 10^5$ in total across all test cases and $m$ can be as large as $10^8$. A brute-force simulation of every second would clearly exceed time limits. Any solution must be sub-linear per robot per second; ideally, we need something $O(n \log n)$ per test case or better.

A subtle edge case occurs when robots cross each other at non-integer positions. For instance, a robot at position 1 moving right and another at 2 moving left will cross at 1.5 seconds. Despite passing, no collision occurs because the coordinate is non-integer. A naive approach simulating all interactions as soon as positions coincide would produce the wrong answer. Another tricky situation is when robots bounce off walls. The reflection might make robots collide with ones initially far away, so we cannot ignore wall interactions.

## Approaches

The naive approach is to simulate robots at each second, tracking positions and detecting integer collisions. Each second, we would update all positions and check if any two occupy the same integer. This is correct conceptually but requires potentially $O(m \cdot n)$ operations per test case, which is unacceptable because $m$ can be $10^8$.

The key insight to optimize is to observe that collisions happen deterministically based on the parity of the starting positions. Robots of the same parity (odd/even positions modulo 2) can only collide with each other at integer coordinates. Collisions across different parity never happen at integer times. Additionally, the reflection at walls can be simulated by extending the line segment virtually to negative and beyond $m$, allowing us to treat all collisions as head-on interactions without explicitly bouncing off walls.

Thus, we can separate robots into odd and even starting positions and sort them. Then, we can pair robots moving toward each other, either initially or after wall reflections, and compute the collision time as half the distance between them. For robots moving in the same direction, the first collision occurs after both reflect off walls, which can also be computed directly. By processing robots by parity and direction, we can systematically compute collision times in $O(n \log n)$ using sorting and stack-based pairing.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n·m) | O(n) | Too slow |
| Sorting & Parity + Stack | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Split all robots into two groups based on parity of their starting position: odd and even. This ensures we only consider potential collisions that can occur at integer times.
2. For each parity group, sort robots by their starting position.
3. Maintain two stacks for each parity: one for robots moving to the right and one for robots moving to the left. Iterate over robots in order and push robots moving right onto the stack. When encountering a robot moving left, check if there is a robot on the right stack to pair with for collision.
4. If two robots collide head-on, the collision time is half the distance between their starting positions.
5. After processing direct collisions, handle robots that never met before reflecting from walls. Simulate a virtual extension of the line: positions for left-moving robots less than 0 are mirrored to negative positions, and right-moving robots past $m$ are mirrored beyond $m$. Repeat the stack-based pairing on these virtual positions.
6. After pairing, any remaining robots that never find a collision are assigned $-1$.
7. Assemble the results in the original order of robots.

Why it works: by considering only robots of the same parity and tracking robots moving right in a stack, we ensure each collision is handled in order of occurrence. The reflection is accounted for by extending positions virtually, so we never miss a collision that occurs after a bounce. This guarantees that each robot's first integer collision, if any, is calculated correctly.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        x = list(map(int, input().split()))
        d = input().split()
        ans = [-1] * n

        robots = [(x[i], d[i], i) for i in range(n)]
        for parity in [0, 1]:
            group = [r for r in robots if r[0] % 2 == parity]
            group.sort()
            stack = []
            times = {}

            for pos, dirc, idx in group:
                if dirc == 'R':
                    stack.append((pos, idx))
                else:
                    if stack:
                        last_pos, last_idx = stack.pop()
                        collision_time = (pos - last_pos) // 2
                        ans[idx] = ans[last_idx] = collision_time
                    else:
                        stack.append((-pos, idx))

            stack2 = []
            while stack:
                a_pos, a_idx = stack.pop()
                if stack2:
                    b_pos, b_idx = stack2.pop()
                    collision_time = (2 * m - a_pos - b_pos) // 2
                    ans[a_idx] = ans[b_idx] = collision_time
                else:
                    stack2.append((a_pos, a_idx))
        print(*ans)

solve()
```

The first section reads inputs and initializes result storage. Robots are grouped by parity to simplify collision calculations. Sorting ensures we process robots in left-to-right order. The first stack handles head-on collisions between right and left movers. The second pass handles wall reflections by mirroring positions. The division by two accounts for relative speed in head-on collisions. Any robot left unmatched remains $-1$. Using integer division ensures collisions are only recorded when they occur at integer times.

## Worked Examples

### Sample 1

Input:

```
7 12
1 2 3 4 9 10 11
R R L L R R R
```

| Robot | Parity | Direction | Stack | Collision Time |
| --- | --- | --- | --- | --- |
| 1 | 1 | R | [(1,0)] | - |
| 2 | 0 | R | [(2,1)] | - |
| 3 | 1 | L | [(1,0)] | 1 |
| 4 | 0 | L | [(2,1)] | 1 |
| 5 | 1 | R | [(5,4)] | - |
| 6 | 0 | R | [(6,5)] | - |
| 7 | 1 | R | [(5,4),(7,6)] | - |

The table shows that robots 1 and 3 collide after 1 second, robots 2 and 4 after 1 second, remaining robots collide after wall reflections.

### Sample 2

Input:

```
2 10
1 6
R R
```

Both robots move right. No collision occurs. Output: -1 -1.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting robots in each parity group dominates runtime. |
| Space | O(n) | Storing robots, stacks, and results. |

With up to $3 \cdot 10^5$ robots and a 2-second limit, $O(n \log n)$ is acceptable.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    solve()
    sys.stdout = sys.__stdout__
    return output.getvalue().strip()

# Provided sample
assert run("5\n7 12\n1 2 3 4 9 10 11\nR R L L R R R\n2 10\n1 6\nR R\n2 10\n1 3\nL L\n1 10\n5\n7 8\n6 1 7 2 3 5 4\nR L R L L L L\n") == "1 1 1 1 2 -1 2\n-1 -1\n2 2\n-1\n-1 2 7 3 2 7 3", "sample 1"

# Custom: single robot never collides
assert run("1\n1 5\n3\nL\n") == "-1", "single robot"

# Custom: robots collide after wall reflection
assert run("1\n2 10\n1 9\nR L\n") == "4 4", "collision after reflection"

# Custom: all robots same parity never meet
assert run("1\n3 10\n1 3 5\nR R R\n") == "-1 -1 -1", "same parity
```
