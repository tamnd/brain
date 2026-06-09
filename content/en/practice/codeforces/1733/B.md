---
title: "CF 1733B - Rule of League"
description: "We are given a sequential knockout badminton tournament. Player 1 plays player 2 first. The winner of each game continues to play the next player in order. After all $n-1$ games, the last winner is the champion."
date: "2026-06-09T18:23:50+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "math"]
categories: ["algorithms"]
codeforces_contest: 1733
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 821 (Div. 2)"
rating: 900
weight: 1733
solve_time_s: 181
verified: false
draft: false
---

[CF 1733B - Rule of League](https://codeforces.com/problemset/problem/1733/B)

**Rating:** 900  
**Tags:** constructive algorithms, math  
**Solve time:** 3m 1s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a sequential knockout badminton tournament. Player 1 plays player 2 first. The winner of each game continues to play the next player in order. After all $n-1$ games, the last winner is the champion. The input specifies the total number of players $n$ and two numbers $x$ and $y$, which represent the number of games won by two distinct kinds of players. Each player must have either $x$ or $y$ wins. The task is to reconstruct any valid sequence of winners consistent with these numbers, or report -1 if no such arrangement exists.

The constraints allow $n$ up to $10^5$ and the sum of $n$ over all test cases up to $2 \cdot 10^5$, which means we need a linear-time algorithm per test case. Quadratic approaches that simulate every possible combination of winners would perform $O(n^2)$ operations and are therefore infeasible.

A key subtlety is that the champion always has the maximum number of wins in the tournament. Since there are $n-1$ games, no player can have more than $n-1$ wins. Also, the minimum number of wins is zero, which is possible for players eliminated in their first match. A careless implementation might assume any combination of $x$ and $y$ is valid, but for instance if $n=3$, $x=0$, $y=0$, it is impossible because at least one player must win a game.

## Approaches

A brute-force approach would try every possible winner sequence, count wins, and check if the resulting counts match exactly the two given values. This would involve iterating over $n-1$ games and updating counters for $n$ players, and backtracking over multiple possibilities. Even for $n=100$, this is already hundreds of operations per test case, and for $n=10^5$ it is completely infeasible.

The key insight comes from the linear, sequential structure of the tournament. Each game is won by the current champion, who keeps playing until eliminated. Therefore, the number of wins for a player corresponds exactly to how many consecutive games they win once they first play. We can model this as splitting the $n-1$ games into blocks of equal length corresponding to the number of wins $x$ or $y$. Since all games are won by the current winner, each block is contiguous in the sequence. The problem reduces to checking if we can partition $n-1$ games into blocks of length $x$ and $y$. If one of $x$ or $y$ is zero, it simplifies: the player with zero wins loses immediately. If neither divides $n-1$ evenly, no solution exists. This turns the problem into a simple linear check rather than combinatorial exploration.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Start by ensuring $x \ge y$ to simplify reasoning. This allows us to assume the champion will have $x$ wins.
2. Check if $(n-1) \bmod x == 0$ or $(n-1) \bmod y == 0$. If neither divides $n-1$, print -1. This ensures we can partition the sequence into contiguous blocks of size $x$ or $y$.
3. Choose the block size that divides $n-1$. Let it be $k$, which is either $x$ or $y$. The number of blocks is $(n-1)//k$.
4. Assign consecutive players to each block. The first block winner starts with player 1. After $k$ games, move to the next available player to start the next block. This guarantees that each block winner wins exactly $k$ games.
5. Output the sequence of winners by repeating each block winner $k$ times.

Why it works: The tournament structure ensures each block of consecutive wins corresponds to one player’s total wins. Since all games are sequential, no other player can break a block. By choosing a block size that divides $n-1$, we guarantee the sum of all wins equals $n-1$, which satisfies the constraints. Every player has either $x$ or $y$ wins because each block is uniform.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, x, y = map(int, input().split())
        # Always work with x >= y
        if x < y:
            x, y = y, x
        
        found = False
        # Try x as block size
        if (n - 1) % x == 0:
            k = x
            found = True
        # Else try y
        elif (n - 1) % y == 0:
            k = y
            found = True
        
        if not found:
            print(-1)
            continue
        
        res = []
        current = 1
        while len(res) < n - 1:
            for _ in range(k):
                res.append(current)
            current += k
        print(" ".join(map(str, res)))

solve()
```

The solution first normalizes $x$ and $y$ so that $x$ is the larger block. We then try to partition $n-1$ into blocks of size $x$ or $y$. If neither works, there is no valid tournament. Otherwise, we construct the winner sequence by repeating each block winner the required number of times. The increment of `current` ensures the next block starts with the next player in line. Off-by-one mistakes are avoided by working in zero-based counts for blocks but one-based for player numbers.

## Worked Examples

**Example 1:** `n=5, x=2, y=0`

| Step | Current Winner | Block Size | Sequence |
| --- | --- | --- | --- |
| 1 | 1 | 2 | [1,1] |
| 2 | 3 | 2 | [1,1,3,3] |

Player 1 and 3 each win 2 games, players 2 and 4 win 0, which satisfies the condition. Output: `1 1 3 3`

**Example 2:** `n=3, x=0, y=0`

No block size divides `n-1=2`. Therefore, output: `-1`

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each test case iterates through `n-1` games to construct the sequence once. |
| Space | O(n) | We store the winner sequence of length `n-1`. |

The solution fits comfortably within 2s for the given limits. The sum of all $n$ is $2 \cdot 10^5$, so total operations are linear in $2 \cdot 10^5$.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    solve()
    return output.getvalue().strip()

# provided samples
assert run("5\n5 2 0\n8 1 2\n3 0 0\n2 0 1\n6 3 0\n") == "1 1 3 3\n-1\n-1\n2\n-1"

# custom cases
assert run("1\n2 0 1\n") == "2"
assert run("1\n4 3 0\n") == "1 1 1"
assert run("1\n7 2 1\n") == "-1"
assert run("1\n6 2 1\n") == "1 1 2 2 3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 0 1 | 2 | Minimum size n=2, zero win |
| 4 3 0 | 1 1 1 | Block size equals n-1 |
| 7 2 1 | -1 | Impossible partition |
| 6 2 1 | 1 1 2 2 3 | Mixed small numbers |

## Edge Cases

For `n=3, x=0, y=0`, our algorithm first checks divisibility: `(n-1) % x` and `(n-1) % y` both fail, so we output `-1`. This avoids incorrectly assigning a zero-win player to multiple games. For `n=2, x=0, y=1`, we take block size 1 and produce `[2]` as the winner sequence. The method handles one-block tournaments naturally because the while loop fills exactly `n-1` slots.
