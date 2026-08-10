---
title: "CF 102397C - The Ending Point"
description: "We start at a grid point (x, y) and receive a string describing a sequence of unit moves. Each character changes exactly one coordinate: U increases y, D decreases y, L decreases x, and R increases x."
date: "2026-08-11T05:04:57+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102397
codeforces_index: "C"
codeforces_contest_name: "Asu Coding Cup 4"
rating: 0
weight: 102397
solve_time_s: 226
verified: true
draft: false
---

[CF 102397C - The Ending Point](https://codeforces.com/problemset/problem/102397/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We start at a grid point `(x, y)` and receive a string describing a sequence of unit moves. Each character changes exactly one coordinate: `U` increases `y`, `D` decreases `y`, `L` decreases `x`, and `R` increases `x`.

The task is simply to apply every movement in the given order and print the final grid point. The path itself is not needed after its movements have been processed. Since the answer is allowed to contain negative coordinates, there is no boundary on the grid that needs to be enforced.

The starting coordinates satisfy `1 <= x, y <= 100`, and the path length is at most `100`. These limits are very small, so even an algorithm with a few operations per character is easily fast enough. More importantly, the structure of the problem gives us an obvious linear solution: every character contributes one independent change to one coordinate, so there is no reason to revisit previous characters or search through possible paths.

A careless implementation can still fail on a few boundary cases. For example, consider

```
1 1
L
```

The correct answer is

```
0 1
```

because `L` decreases `x` by one. An implementation that assumes coordinates must remain positive could incorrectly reject or clamp the result.

Another example is

```
5 5
DDDDD
```

which produces

```
5 0
```

The coordinate is allowed to reach zero, and it could also become negative. Treating `1` as a lower bound after the walk would produce an incorrect result.

Moves can also cancel each other. For

```
3 4
LRUD
```

the final position is

```
3 4
```

because `L` and `R` cancel on the `x` coordinate, while `U` and `D` cancel on the `y` coordinate. A solution that only counts the number of moves without respecting their directions would lose this information.

## Approaches

A straightforward but unnecessarily expensive approach is to determine the position after every prefix of the path by scanning that prefix from the starting point. After processing the first character, we scan one character. After processing the second character, we scan two characters again, and so on. This is correct because each scan directly simulates the corresponding prefix, but the same movements are repeatedly processed.

If the path has length `n`, this performs

`1 + 2 + 3 + ... + n = n(n + 1)/2`

character operations. With `n = 100`, that is `5050` operations, which still easily fits the given limits. Its weakness is conceptual rather than practical for these constraints: it does repeated work that is completely unnecessary.

The key observation is that the endpoint only depends on the total displacement of each coordinate. We can process the path once while maintaining the current position. Whenever we see `U` or `D`, we update `y`; whenever we see `L` or `R`, we update `x`. Each character is consumed exactly once.

The brute-force version works because repeatedly simulating a prefix eventually gives the correct endpoint, but it fails to exploit the fact that the current position already contains all information obtained from previous moves. The observation that a single current coordinate pair is sufficient lets us replace repeated prefix scans with one direct traversal.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Accepted for these constraints, but unnecessarily repetitive |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the starting coordinates `x` and `y`. These values represent the position before any movement has taken place.
2. Read the path string `s`. We will process its characters from left to right because the order of movements determines the endpoint.
3. For every character in `s`, update exactly one coordinate. For `U`, increase `y` by one. For `D`, decrease `y` by one. For `L`, decrease `x` by one. For `R`, increase `x` by one. No other coordinate should change because every movement is horizontal or vertical by exactly one unit.
4. After all characters have been processed, print the resulting `x` and `y`. At this point, every movement has contributed its displacement to the coordinates, so the current pair is the cafeteria's location.

### Why it works

After processing any prefix of the path, maintain the invariant that `(x, y)` is exactly the position reached after executing that prefix from the original starting point. Initially the prefix is empty, so the invariant is true because `(x, y)` is the starting position. Each next character changes the current position according to the movement defined by that character, so the invariant remains true after every iteration. Once the entire string has been processed, the prefix is the complete path, meaning `(x, y)` is exactly the required ending point.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    x, y = map(int, input().split())
    s = input().strip()

    for move in s:
        if move == 'U':
            y += 1
        elif move == 'D':
            y -= 1
        elif move == 'L':
            x -= 1
        else:  # move == 'R'
            x += 1

    print(x, y)

if __name__ == "__main__":
    solve()
```

The first line reads the starting point directly into `x` and `y`, matching the coordinate system used by the movement rules.

The path is stripped of its trailing newline before iteration. The loop then examines each movement exactly once. The four cases correspond directly to the four possible changes, so there is no lookup table or auxiliary data structure to maintain.

There is no boundary check because the problem explicitly allows the final coordinates to be negative. Adding a condition such as `if x > 0` before moving left would change the problem and could produce a wrong answer.

There is also no risk of integer overflow in Python. Even with the maximum path length of `100`, each coordinate can change by at most `100` from its starting value, so the actual values are tiny.

## Worked Examples

### Sample 1

The input is

```
5 3
UUUDLRLRLRR
```

Starting from `(5, 3)`, process each movement in order.

| Step | Move | x | y |
| --- | --- | --- | --- |
| 0 | Start | 5 | 3 |
| 1 | U | 5 | 4 |
| 2 | U | 5 | 5 |
| 3 | U | 5 | 6 |
| 4 | D | 5 | 5 |
| 5 | L | 4 | 5 |
| 6 | R | 5 | 5 |
| 7 | L | 4 | 5 |
| 8 | R | 5 | 5 |
| 9 | L | 4 | 5 |
| 10 | R | 5 | 5 |
| 11 | R | 6 | 5 |

The final position is `(6, 5)`, so the output is

```
6 5
```

The repeated `L` and `R` movements demonstrate that the algorithm does not need special handling for cancellation. Each movement changes the current position, and the resulting coordinate naturally contains the accumulated displacement.

### Sample 2

Consider the valid input

```
2 3
LLDDRU
```

The state changes as follows.

| Step | Move | x | y |
| --- | --- | --- | --- |
| 0 | Start | 2 | 3 |
| 1 | L | 1 | 3 |
| 2 | L | 0 | 3 |
| 3 | D | 0 | 2 |
| 4 | D | 0 | 1 |
| 5 | R | 1 | 1 |
| 6 | U | 1 | 2 |

The final output is

```
1 2
```

This trace exercises a coordinate reaching zero and then moving back in the opposite direction. The algorithm does not impose artificial grid boundaries, so every movement is applied exactly as specified.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Every character of the path is processed once |
| Space | O(1) | Only the two coordinates and the input string are needed |

With `n <= 100`, the linear traversal performs at most 100 movement updates. It is comfortably within the 1.5 second time limit and uses negligible memory compared with the 256 MB limit.

## Test Cases

```python
import sys
import io

def solve():
    x, y = map(int, input().split())
    s = input().strip()

    for move in s:
        if move == 'U':
            y += 1
        elif move == 'D':
            y -= 1
        elif move == 'L':
            x -= 1
        else:
            x += 1

    print(x, y)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    try:
        sys.stdin = io.StringIO(inp)
        sys.stdout = io.StringIO()
        solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided sample
assert run("5 3\nUUUDLRLRLRR\n") == "6 5", "sample 1"

# Minimum-size input
assert run("1 1\nU\n") == "1 2", "single upward move"

# All moves are equal
assert run("5 5\nLLLLLLLLLL\n") == "-5 5", "ten left moves"

# Boundary and negative coordinate
assert run("1 1\nDDDD\n") == "1 -3", "negative y coordinate"

# Cancellation and order
assert run("100 100\nLRUD\n") == "100 100", "complete cancellation"

# Maximum-size path
assert run("100 100\n" + "R" * 100 + "\n") == "200 100", "maximum path length"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` with `U` | `1 2` | Minimum-size path and single-coordinate update |
| `5 5` with ten `L` moves | `-5 5` | Repeated movement and negative `x` |
| `1 1` with four `D` moves | `1 -3` | Crossing below zero |
| `100 100` with `LRUD` | `100 100` | Exact cancellation of opposite movements |
| `100 100` with 100 `R` moves | `200 100` | Maximum path length and repeated updates |

## Edge Cases

The first edge case is a movement that takes the position to zero or below. For

```
1 1
L
```

the algorithm starts with `(1, 1)`, processes `L`, and changes `x` to `0`. It prints `0 1`. There is no boundary restriction during the walk, so the zero coordinate is valid.

The second edge case is moving several times beyond the positive starting region. For

```
1 1
DDDD
```

the successive `y` values are `0`, `-1`, `-2`, and `-3`. The final answer is `1 -3`. A solution that prevents the coordinate from becoming negative would incorrectly stop applying the path.

The third edge case is complete cancellation. With

```
3 4
LRUD
```

the first two moves change `x` from `3` to `2` and then back to `3`. The next two moves change `y` from `4` to `5` and then back to `4`. The final result is `3 4`, exactly the starting point. This confirms that the invariant tracks the actual current position rather than merely counting movements.

Finally, a path containing only one direction needs no special case. For

```
100 100
RRRR
```

the four `R` operations simply increase `x` from `100` to `104`, producing `104 100`. The same update rule handles a single move, repeated moves, and mixed paths, which is why the implementation remains small without sacrificing correctness.
