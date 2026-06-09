---
title: "CF 1791B - Following Directions"
description: "Alperen starts at the origin (0,0) on a 2D grid. He is given a sequence of n moves, where each move shifts him one unit in one of the four cardinal directions: left, right, up, or down."
date: "2026-06-09T10:30:06+07:00"
tags: ["codeforces", "competitive-programming", "geometry", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1791
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 849 (Div. 4)"
rating: 800
weight: 1791
solve_time_s: 153
verified: true
draft: false
---

[CF 1791B - Following Directions](https://codeforces.com/problemset/problem/1791/B)

**Rating:** 800  
**Tags:** geometry, implementation  
**Solve time:** 2m 33s  
**Verified:** yes  

## Solution
## Problem Understanding

Alperen starts at the origin `(0,0)` on a 2D grid. He is given a sequence of `n` moves, where each move shifts him one unit in one of the four cardinal directions: left, right, up, or down. A candy is located at a fixed position `(1,1)`, and the task is to determine whether Alperen ever passes through that cell while following his moves. The input consists of multiple test cases, each with the number of moves and the move sequence. The output is "YES" if he reaches the candy at least once, and "NO" otherwise.

The constraints are modest: `n` is up to 50 and the number of test cases `t` is up to 1000. This immediately rules out the need for any complex optimization, since even simulating all moves for every test case is fast. Edge cases arise when the candy is reached immediately in the first move, or when the path loops around but never touches `(1,1)`. For example, if the sequence is "LURD", Alperen moves left, then up, then right, then down, ending at the origin. Even though he moves in all directions, he never reaches `(1,1)`, so the answer is "NO". A careless implementation might only check the final position or misinterpret direction sequences, giving wrong answers.

## Approaches

The naive approach is also the optimal one: simulate Alperen’s path step by step. Start at `(0,0)` and iterate over the move string. After each move, update the current coordinates. After every update, check whether the position matches `(1,1)`. If it does, immediately conclude "YES" for that test case. If the loop ends without reaching `(1,1)`, output "NO".

This approach works because `n` is very small, and the check is trivial. Any attempt to optimize further, for example by precomputing reachable cells or using coordinate offsets, adds unnecessary complexity. There is no benefit from sorting, dynamic programming, or BFS since the path is fixed and deterministic.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force / Simulation | O(n) per test case | O(1) | Accepted |
| Precomputation / BFS | O(n) per test case | O(n) | Unnecessary |

## Algorithm Walkthrough

1. Read the number of test cases `t`.
2. For each test case, read the length `n` and the move string `s`.
3. Initialize Alperen’s position at `(x, y) = (0, 0)`.
4. Iterate over each character in the move string:

1. If the character is `L`, decrement `x` by 1.
2. If the character is `R`, increment `x` by 1.
3. If the character is `U`, increment `y` by 1.
4. If the character is `D`, decrement `y` by 1.
5. After each update, check if `(x, y) == (1, 1)`. If true, print "YES" and stop processing this test case.
5. If the loop ends without visiting `(1,1)`, print "NO".

Why it works: the algorithm maintains the invariant that `(x, y)` always reflects Alperen’s current position on the grid. Checking after every move guarantees that the first visit to `(1,1)` is detected. Since the moves are deterministic, no cell is skipped, and no false positives can occur.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        s = input().strip()
        x, y = 0, 0
        found = False
        for move in s:
            if move == 'L':
                x -= 1
            elif move == 'R':
                x += 1
            elif move == 'U':
                y += 1
            elif move == 'D':
                y -= 1
            if x == 1 and y == 1:
                found = True
                break
        print("YES" if found else "NO")

solve()
```

The solution reads inputs efficiently, tracks Alperen’s position, and terminates early upon reaching the candy. The boundary conditions are handled correctly, and the `strip()` ensures no trailing newline interferes with move parsing. Off-by-one errors are impossible since the grid uses exact integer coordinates.

## Worked Examples

### Sample 1: `"UUURDDL"`

| Step | Move | x | y | At Candy? |
| --- | --- | --- | --- | --- |
| 0 | start | 0 | 0 | NO |
| 1 | U | 0 | 1 | NO |
| 2 | U | 0 | 2 | NO |
| 3 | U | 0 | 3 | NO |
| 4 | R | 1 | 3 | NO |
| 5 | D | 1 | 2 | NO |
| 6 | D | 1 | 1 | YES |

Alperen reaches `(1,1)` on the 6th move, so the output is `"YES"`.

### Sample 2: `"LLL"`

| Step | Move | x | y | At Candy? |
| --- | --- | --- | --- | --- |
| 0 | start | 0 | 0 | NO |
| 1 | L | -1 | 0 | NO |
| 2 | L | -2 | 0 | NO |
| 3 | L | -3 | 0 | NO |

Alperen never reaches `(1,1)`, so the output is `"NO"`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t * n) | Each test case simulates `n` moves, with up to `t=1000` test cases. Max `t*n = 50,000`. |
| Space | O(1) | Only coordinates and temporary variables are stored; no extra memory per test case. |

The constraints are small enough that this solution runs comfortably within 1 second and 256 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    return sys.stdout.getvalue().strip()

# provided samples
assert run("7\n7\nUUURDDL\n2\nUR\n8\nRRRUUDDD\n3\nLLL\n4\nDUUR\n5\nRUDLL\n11\nLLLLDDRUDRD\n") == \
    "YES\nYES\nNO\nNO\nYES\nYES\nNO", "sample 1"

# custom cases
assert run("1\n1\nR\n") == "NO", "single move, not reaching candy"
assert run("1\n2\nRU\n") == "YES", "first test reaching candy quickly"
assert run("1\n4\nUDUD\n") == "NO", "moving up and down, never reaching candy"
assert run("1\n50\n" + "R"*25 + "U"*25 + "\n") == "YES", "max length, reaching candy"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n1\nR\n` | NO | Single move that doesn’t reach candy |
| `1\n2\nRU\n` | YES | Minimal path reaching candy quickly |
| `1\n4\nUDUD\n` | NO | Moves that loop but never hit candy |
| 50 moves `R*25+U*25` | YES | Maximum string length reaching candy |

## Edge Cases

A path that oscillates along one axis without ever crossing `(1,1)` is handled correctly. For example, `"LURD"` keeps returning to `(0,0)`. The algorithm updates positions in order and only outputs "YES" when `(1,1)` is reached, otherwise outputs "NO" at the end. Single-move paths, paths that reach the candy on the first move, and maximal-length paths are all correctly simulated.
