---
title: "CF 492A - Vanya and Cubes"
description: "Vanya wants to build a pyramid using exactly the pattern described by triangular numbers. The first level contains 1 cube. The second level contains 1 + 2 = 3 cubes. The third level contains 1 + 2 + 3 = 6 cubes."
date: "2026-06-07T17:44:56+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 492
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 280 (Div. 2)"
rating: 800
weight: 492
solve_time_s: 132
verified: true
draft: false
---

[CF 492A - Vanya and Cubes](https://codeforces.com/problemset/problem/492/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 2m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

Vanya wants to build a pyramid using exactly the pattern described by triangular numbers. The first level contains 1 cube. The second level contains 1 + 2 = 3 cubes. The third level contains 1 + 2 + 3 = 6 cubes. In general, level `i` requires the sum of the first `i` positive integers.

We are given the total number of cubes available, `n`. Our task is to determine the largest number of complete levels that can be built before running out of cubes.

The constraint is very small. The number of cubes is at most `10^4`, which means even a simple simulation is fast enough. The number of levels that can possibly be built is much smaller than `10^4` because each new level requires more cubes than the previous one. A straightforward iterative solution easily fits within the limits.

A common mistake is forgetting that each level itself is a triangular number.

Consider:

```
Input:
4
```

The first level uses 1 cube and the second level uses 3 cubes. Together they require 4 cubes, so the answer is:

```
2
```

A careless implementation might incorrectly assume level `i` needs exactly `i` cubes and return 3.

Another subtle case occurs when the cubes run out exactly after finishing a level.

```
Input:
10
```

The levels require 1, 3, and 6 cubes.

The total is:

```
1 + 3 + 6 = 10
```

The correct answer is:

```
3
```

An implementation that stops as soon as the remaining cubes become zero before counting the completed level would incorrectly return 2.

## Approaches

The most direct idea is to build the pyramid level by level. For each level, compute how many cubes that level requires, subtract it from the remaining supply, and continue while enough cubes remain.

This brute-force simulation is already fast enough. Since `n ≤ 10000`, the number of levels is tiny. Even if we repeatedly compute triangular numbers, the amount of work is negligible.

The key observation is that the number of cubes required for level `i` is itself a triangular number:

$$1 + 2 + \cdots + i = \frac{i(i+1)}{2}$$

So while constructing the pyramid, we only need to keep track of the current level and its required cubes. Whenever we can afford the next level, we subtract its cost and increase the height.

Because the levels must be built in order and every level has a fixed cost, greedily taking levels from the top down is the only possible valid construction. The moment we cannot afford the next level, no taller pyramid can exist.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(h²) | O(1) | Accepted |
| Optimal Simulation | O(h) | O(1) | Accepted |

Here `h` is the final pyramid height, which is at most around 30 for `n ≤ 10000`.

## Algorithm Walkthrough

1. Read the number of available cubes `n`.
2. Initialize `height = 0`.
3. Initialize `level = 1`.
4. Compute the number of cubes required for the current level using:

$$\frac{\text{level}(\text{level}+1)}{2}$$
5. If enough cubes remain, subtract that amount from `n`, increase `height`, and move to the next level.

This corresponds to successfully completing one more layer of the pyramid.
6. Repeat until the next level requires more cubes than remain available.
7. Output `height`.

### Why it works

At every iteration, the algorithm maintains the invariant that all levels from 1 through `height` have been fully constructed and the remaining value of `n` equals the cubes left after building them.

The next possible action is uniquely determined: either the next level can be completed or it cannot. If it can, building it increases the height by one. If it cannot, any taller pyramid would also require that same unfinished level, which is impossible. Thus the algorithm stops exactly at the maximum achievable height.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())

height = 0
level = 1

while True:
    need = level * (level + 1) // 2

    if n < need:
        break

    n -= need
    height += 1
    level += 1

print(height)
```

The variable `level` represents the next layer we are trying to build. The expression

```
level * (level + 1) // 2
```

computes the triangular number for that level.

Whenever enough cubes remain, we spend those cubes and record one more completed level. The loop terminates exactly when the next required layer cannot be completed.

The most common off-by-one mistake is incrementing `level` before calculating its cost. Doing so would skip the first layer of size 1. Another common mistake is checking for zero remaining cubes instead of checking whether the next level is affordable. Exact fits such as `n = 10` must still count the final completed level.

## Worked Examples

### Example 1

Input:

```
1
```

| Level | Cubes Needed | Cubes Remaining Before | Action | Height |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | Build level | 1 |
| 2 | 3 | 0 | Stop | 1 |

Output:

```
1
```

This demonstrates the smallest possible input. After building the first level, there are no cubes left, and the next level cannot be started.

### Example 2

Input:

```
20
```

| Level | Cubes Needed | Cubes Remaining Before | Action | Height |
| --- | --- | --- | --- | --- |
| 1 | 1 | 20 | Build level | 1 |
| 2 | 3 | 19 | Build level | 2 |
| 3 | 6 | 16 | Build level | 3 |
| 4 | 10 | 10 | Build level | 4 |
| 5 | 15 | 0 | Stop | 4 |

Output:

```
4
```

This trace shows an exact fit after the fourth level. The algorithm correctly counts that level before stopping.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(h) | One iteration per completed level |
| Space | O(1) | Only a few integer variables are stored |

Since `n ≤ 10000`, the height of the pyramid is very small. The loop executes only a few dozen times in the worst case, making the solution easily fit within the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    n = int(input())

    height = 0
    level = 1

    while True:
        need = level * (level + 1) // 2

        if n < need:
            break

        n -= need
        height += 1
        level += 1

    print(height)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    global input
    input = sys.stdin.readline

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out

# provided sample
assert run("1\n") == "1\n", "sample 1"

# custom cases
assert run("4\n") == "2\n", "exactly two levels"
assert run("10\n") == "3\n", "exactly three levels"
assert run("19\n") == "3\n", "just short of fourth level"
assert run("10000\n") == "21\n", "maximum input range"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `4` | `2` | Exact completion of two levels |
| `10` | `3` | Exact completion of three levels |
| `19` | `3` | Stops just before next level |
| `10000` | `21` | Largest constraint value |

## Edge Cases

Consider the exact-fit case:

```
Input:
10
```

The algorithm builds levels requiring 1, 3, and 6 cubes. The remaining cubes become zero after completing the third level. The next level requires 10 cubes, which is not affordable, so the answer is 3. This verifies that finishing a level exactly is counted correctly.

Consider a value just below the next threshold:

```
Input:
19
```

The first three levels consume:

```
1 + 3 + 6 = 10
```

Nine cubes remain. The fourth level requires 10 cubes, so construction stops and the answer is 3. This checks the boundary where the next level is almost affordable but not quite.

Consider the minimum input:

```
Input:
1
```

The first level requires exactly one cube, so it is completed. No cubes remain afterward, and the algorithm outputs 1. This confirms correct handling of the smallest valid value.

Consider a larger exact-fit situation:

```
Input:
20
```

The required cubes are:

```
1 + 3 + 6 + 10 = 20
```

All four levels can be built, and the algorithm outputs 4. This verifies that multiple consecutive exact completions are handled correctly.
