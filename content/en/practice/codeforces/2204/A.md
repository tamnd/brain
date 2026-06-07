---
title: "CF 2204A - Passing the Ball"
description: "We are given a line of students arranged from left to right, and a ball that moves deterministically according to fixed rules."
date: "2026-06-07T19:56:42+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation"]
categories: ["algorithms"]
codeforces_contest: 2204
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 188 (Rated for Div. 2)"
rating: 800
weight: 2204
solve_time_s: 185
verified: true
draft: false
---

[CF 2204A - Passing the Ball](https://codeforces.com/problemset/problem/2204/A)

**Rating:** 800  
**Tags:** brute force, implementation  
**Solve time:** 3m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a line of students arranged from left to right, and a ball that moves deterministically according to fixed rules. Each student has a direction, either left or right, meaning that whenever the ball reaches that student, it is immediately passed to the adjacent student in that direction. The endpoints are forced: the first student always passes right, and the last student always passes left.

The process starts with student 1 holding the ball. Then the ball is passed exactly $n$ times. During these passes, the ball may revisit the same student multiple times, but we only care about which distinct students ever hold the ball at least once.

So the problem reduces to simulating a deterministic walk on a line graph where each node has exactly one outgoing edge to a neighbor, and we count how many distinct nodes are visited during a fixed number of steps starting from node 1.

The constraints are small enough that a direct simulation is completely safe. With $t \le 10^4$ and $n \le 50$, even $O(n^2)$ per test case leads to at most $2.5 \cdot 10^7$ steps, which is comfortably within limits in Python.

There are no tricky hidden edge cases in terms of invalid moves because movement is always defined. The only subtle point is that the number of steps is exactly $n$, not until stabilization or until exit from bounds. That matters because the path may oscillate and revisit nodes multiple times.

A naive mistake would be to assume the walk forms a monotone segment or that it always moves right first and then left once. For example, in `RLRL`, the ball bounces between 1 and 2 indefinitely. A mistaken greedy interpretation might incorrectly assume the walk expands continuously, but it does not.

Another potential mistake is forgetting to count the starting node (student 1), since the problem explicitly says they receive the ball first before any passes occur.

## Approaches

The process described is already fully deterministic, so the most straightforward approach is to simulate it step by step. We maintain the current position of the ball, and after each pass we update the position according to the direction stored in the current student. We also keep a boolean array or a set marking which students have already received the ball.

After performing exactly $n$ transitions, we count how many students were marked visited.

This works because each state transition is $O(1)$, and we only do $n$ transitions per test case, so the total complexity is linear in $n$.

A brute-force simulation is already optimal here. There is no need for cycle detection or graph compression because $n$ is at most 50, so even repeated recomputation across many test cases remains trivial.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | $O(n^2)$ total over all tests | $O(n)$ | Accepted |
| Optimal Simulation (same idea) | $O(n^2)$ total over all tests | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Start with the ball at position 1 and mark student 1 as visited. This reflects the initial condition before any moves happen.
2. Repeat exactly $n$ times: look at the current student’s direction and move the ball either left or right. Each move corresponds to following the unique outgoing edge from the current node.
3. After each move, mark the new position as visited. This ensures we capture all nodes that ever receive the ball, not just the endpoints of segments.
4. After completing all moves, count how many students were marked visited and output that number.

### Why it works

At any moment, the ball’s position is fully determined by the previous position and the fixed direction at that node, meaning the process is a deterministic walk on a directed graph where each node has outdegree exactly 1. Because we explicitly simulate every transition, we replicate the exact trajectory of this walk for exactly $n$ steps. Every student counted is precisely one that the trajectory enters at least once, and no student is missed because every visit is processed immediately when it occurs.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        n = int(input().strip())
        s = input().strip()

        # 0-indexed positions
        pos = 0
        visited = [False] * n
        visited[pos] = True

        for _ in range(n):
            if s[pos] == 'R':
                pos += 1
            else:
                pos -= 1
            visited[pos] = True

        out.append(str(sum(visited)))

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The implementation directly mirrors the simulation described in the algorithm. The array `visited` tracks whether each student has received the ball. We initialize position 0 because student 1 starts with the ball. Each iteration updates the position according to the current character in the string.

A subtle point is that movement is always safe: the problem guarantees the first character is `R` and the last is `L`, so we never go out of bounds.

## Worked Examples

### Example 1

Input:

```
n = 4
s = RLRL
```

We track the process step by step.

| Step | Position | Move | Visited set |
| --- | --- | --- | --- |
| Start | 1 | - | {1} |
| 1 | 2 | R | {1, 2} |
| 2 | 1 | L | {1, 2} |
| 3 | 2 | R | {1, 2} |
| 4 | 1 | L | {1, 2} |

The walk oscillates between 1 and 2. After 4 moves, only these two students have been visited.

Output is 2.

### Example 2

Input:

```
n = 6
s = RRRRRL
```

| Step | Position | Move | Visited set |
| --- | --- | --- | --- |
| Start | 1 | - | {1} |
| 1 | 2 | R | {1,2} |
| 2 | 3 | R | {1,2,3} |
| 3 | 4 | R | {1,2,3,4} |
| 4 | 5 | R | {1,2,3,4,5} |
| 5 | 6 | R | {1,2,3,4,5,6} |
| 6 | 5 | L | {1,2,3,4,5,6} |

We see a clean sweep to the right, then a single step back. All students are visited.

Output is 6.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(t \cdot n)$ | Each test simulates exactly $n$ moves, each in constant time |
| Space | $O(n)$ | We store a visited array of size $n$ |

With $n \le 50$ and $t \le 10^4$, the total number of operations is at most $5 \cdot 10^5$, which is easily fast enough.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    solve()
    return ""  # output printed directly; for real tests capture stdout

# provided samples (conceptual placeholders since stdout capture is omitted)
# assert run("3\n4\nRLRL\n6\nRRRRRL\n9\nRRLRRRRRL\n") == "2\n6\n3"

# custom cases
# n = 2, immediate bounce
# R L forces 1 -> 2 -> 1
# assert run("1\n2\nRL\n") == "2"

# n = 3, monotone right then left
# assert run("1\n3\nRRL\n") == "3"

# n = 5, alternating pattern
# assert run("1\n5\nRLRLR\n") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| RL | 2 | immediate oscillation |
| RRL | 3 | expansion then partial return |
| RLRLR | 2 | repeated bouncing pattern |

## Edge Cases

A key edge case is the pure oscillation behavior. For input like `RLRL`, the walk never spreads beyond the first two nodes. The simulation starts at node 1, moves to 2, then immediately returns to 1, and repeats. Because we explicitly mark visits at each step, both nodes 1 and 2 are counted, and no incorrect expansion occurs.

Another case is full monotone movement such as `RRRRRL`. Here the ball moves right until it reaches the end, visiting every node, and then steps back once. The simulation ensures node 6 is also counted before returning, since we mark after every move rather than only endpoints.

A final subtle case is minimal input like `n = 2`. The process still performs exactly two moves starting from node 1. The simulation handles this naturally: first move reaches node 2, second move returns to node 1, resulting in both nodes being visited.
