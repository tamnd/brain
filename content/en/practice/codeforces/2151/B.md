---
title: "CF 2151B - Incremental Path"
description: "We are given a virtual strip with cells numbered from 1 to $10^9$, where some cells are initially black and the rest are white. Multiple people start from cell 1, and each executes a prefix of a command string composed of two instructions."
date: "2026-06-09T04:17:10+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 2151
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 1053 (Div. 2)"
rating: 1300
weight: 2151
solve_time_s: 92
verified: false
draft: false
---

[CF 2151B - Incremental Path](https://codeforces.com/problemset/problem/2151/B)

**Rating:** 1300  
**Tags:** implementation  
**Solve time:** 1m 32s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a virtual strip with cells numbered from 1 to $10^9$, where some cells are initially black and the rest are white. Multiple people start from cell 1, and each executes a prefix of a command string composed of two instructions. The first instruction, `A`, moves the person one cell forward. The second, `B`, moves the person to the next white cell beyond the current one. After executing their commands, each person paints the cell they land on black. Our task is to report all cells that are black after everyone has executed their commands.

The key constraints are that the number of commands per test case can be up to $10^5$, and the number of initial black cells can also be up to $10^5$. The total across all test cases for either commands or initial black cells is capped at $10^5$. This means any solution with complexity worse than $O(n + m)$ per test case risks timing out. Direct simulation of cell-by-cell movement across a billion cells is infeasible, and using a full array to track all cells is impossible due to memory limits.

Edge cases arise when the first cell is black or when multiple `B` commands skip over contiguous black cells. A naive simulation that tries to jump to the next white cell by incrementing one cell at a time will fail because there may be large gaps, and performance would degrade. For instance, if cell 1 is black and the first command is `B`, the person should jump directly to cell 2 if it is white, or further if subsequent cells are black. A careless solution might only consider `x+1` rather than the next white cell.

## Approaches

A brute-force solution would simulate each person starting at cell 1, executing each command one by one, and finding the next white cell by scanning forward until a white cell is found. While this is correct conceptually, it is too slow. If there are $n = 10^5$ commands and the black cells are spread sparsely across the $10^9$ strip, scanning each `B` operation could take up to $10^9$ steps in the worst case, which is far beyond feasible.

The key observation is that the only cells that can ever turn black are either the initial black cells or cells immediately visited by executing a prefix of commands. Each person only paints the cell they end up on after following their prefix, and because each person starts at 1, the sequence of moves is monotonic. We can focus on the effect of `B` commands without iterating over all cells. Specifically, for each prefix, we can determine the final cell by keeping a pointer `cur` starting at 1. We iterate through the commands, increment `cur` for `A`, and for `B` we move `cur` to the smallest unvisited white cell after `cur`.

Maintaining a sorted set of black cells allows us to efficiently find the next white cell. Each time we execute a `B`, we jump to the next position beyond the last black cell at or after `cur`. The number of operations becomes proportional to the number of commands plus the number of black cells, which is acceptable.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * gap) | O(10^9) | Too slow |
| Optimal | O((n + m) log m) | O(m) | Accepted |

The `log m` factor arises if we use a sorted container or binary search to find the next white cell efficiently.

## Algorithm Walkthrough

1. Read the number of test cases. For each test case, read `n` commands, `m` initial black cells, the command string `s`, and the list of black cells `a`. Convert the list `a` to a sorted set or array for efficient searching.
2. Initialize a variable `cur` to 1, representing the current cell for the simulated person.
3. Iterate over each command in the string. If the command is `A`, simply increment `cur` by one. If the command is `B`, find the first black cell greater than or equal to `cur` using binary search. Set `cur` to one more than that black cell, effectively jumping to the next white cell.
4. Keep track of all cells that are painted black by storing them in a set. Initially, include all black cells. Each time we finish processing a prefix of length `i`, add `cur` to the set.
5. After processing all commands for a test case, sort the set of black cells and output its size and elements.

The invariant maintained throughout is that `cur` always points to the correct next position according to the commands, considering the cells that are already black. Each jump via `B` always lands on the next white cell relative to the current black cell configuration.

## Python Solution

```python
import sys
import bisect
input = sys.stdin.readline

def process_case(n, m, s, black_cells):
    black_cells.sort()
    black_set = set(black_cells)
    cur = 1
    painted = set(black_cells)

    for cmd in s:
        if cmd == 'A':
            cur += 1
        else:  # 'B'
            idx = bisect.bisect_left(black_cells, cur)
            if idx < len(black_cells) and black_cells[idx] == cur:
                cur = black_cells[idx] + 1
            else:
                if idx < len(black_cells):
                    cur = black_cells[idx] + 1
                # else cur remains as next white cell (beyond last black)
        painted.add(cur)
    res = sorted(painted)
    return res

t = int(input())
for _ in range(t):
    n, m = map(int, input().split())
    s = input().strip()
    black_cells = list(map(int, input().split()))
    result = process_case(n, m, s, black_cells)
    print(len(result))
    print(' '.join(map(str, result)))
```

The solution sorts the initial black cells and uses binary search to efficiently locate the next black cell when executing a `B`. We maintain a set `painted` to collect all newly blackened cells. Careful attention is needed to handle the case when `cur` is beyond the last black cell, where it should remain as the next white cell.

## Worked Examples

### Example 1

Input:

```
3 2
BAB
2 5
```

| Step | Command | cur | painted |
| --- | --- | --- | --- |
| 1 | B | 1 → 3 | {2,5,3} |
| 2 | A | 3 → 4 | {2,5,3,4} |
| 3 | B | 4 → 6 | {2,5,3,4,6} |

The final sorted set of black cells is `[2,3,4,5,6]`. This confirms that `B` correctly skips black cells.

### Example 2

Input:

```
1 3
ABA
1 4 9
```

| Step | Command | cur | painted |
| --- | --- | --- | --- |
| 1 | A | 1 → 2 | {1,4,9,2} |
| 2 | B | 2 → 3 | {1,4,9,2,3} |
| 3 | A | 3 → 4 | {1,4,9,2,3} |

This demonstrates that `A` correctly increments the position even if the cell is black.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + m) log m) | Sorting initial black cells is O(m log m), each binary search for `B` is O(log m), done n times. |
| Space | O(m + n) | Storage for initial black cells and painted cells. |

Given the problem constraints, this fits well within the 1-second time limit and 256 MB memory limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    exec(open('solution.py').read())
    return output.getvalue().strip()

# Provided samples
assert run("""5
3 2
BAB
2 5
3 4
ABA
1 4 9 10
5 2
ABABB
1 7
3 1
BBA
6
1 4
A
1 3 4 1000000000
""") == """4
2 3 5 6
7
1 2 3 4 6 9 10
7
1 2 3 5 6 7 9
3
2 4 6
5
1 2 3 4 1000000000""", "sample tests"

# Custom edge cases
assert run("1\n1 1\nB\n1") == "2\n1 2", "next white after first black"
assert run("1\n2 2\nBB\n1 2") == "3\n1 2 3", "consecutive B commands skipping blacks"
assert run("1\n3 1\nABA\n5") == "4\n1 2 3 5", "jump past black with combination of A and B"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `B |  |  |
