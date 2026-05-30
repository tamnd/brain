---
title: "CF 451A - Game With Sticks"
description: "The game is played on a grid formed by n horizontal sticks and m vertical sticks. Every horizontal stick intersects every vertical stick, creating n m intersection points. On a turn, a player chooses one remaining intersection point."
date: "2026-05-30T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 451
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 258 (Div. 2)"
rating: 900
weight: 451
solve_time_s: 79
verified: true
draft: false
---

[CF 451A - Game With Sticks](https://codeforces.com/problemset/problem/451/A)

**Rating:** 900  
**Tags:** implementation  
**Solve time:** 1m 19s  
**Verified:** yes  

## Solution
## Problem Understanding

The game is played on a grid formed by `n` horizontal sticks and `m` vertical sticks. Every horizontal stick intersects every vertical stick, creating `n * m` intersection points.

On a turn, a player chooses one remaining intersection point. Choosing that point removes the horizontal stick and the vertical stick passing through it. Once those two sticks are removed, every intersection involving either of those sticks disappears as well.

A move is only possible when there is at least one intersection point remaining. The first player is Akshat and the second player is Malvika. Both play optimally, and we must determine who wins.

The input contains only two integers, `n` and `m`. The output is the name of the player who wins under optimal play.

The constraints are very small, both dimensions are at most 100. Even simulation would fit comfortably within the limits. The real challenge is recognizing the game structure and reducing it to a simple observation.

A non-obvious point is that the exact intersection chosen does not matter. For example, in a `3 x 5` grid, selecting any intersection always removes exactly one horizontal stick and one vertical stick. The remaining game state depends only on how many horizontal and vertical sticks are left, not on which specific ones remain.

Consider the input:

```
1 5
```

There is only one horizontal stick. After the first move, that stick is removed, so no intersections remain. Akshat wins immediately. A simulation that focuses on intersection coordinates instead of remaining rows and columns can easily overcomplicate this case.

Another useful example is:

```
2 2
```

The first move removes one row and one column, leaving a `1 x 1` grid. The second move removes the last row and column. No moves remain, so Akshat loses and Malvika wins.

A third example is:

```
3 4
```

Three moves are possible in total. After the third move, either all rows or all columns have been exhausted. Since three is odd, the first player makes the last move and wins.

## Approaches

A brute-force solution would model the entire grid and recursively explore all possible moves. From a state with `r` remaining rows and `c` remaining columns, every move removes one row and one column, producing a state `(r - 1, c - 1)`. Since many choices exist at each step, a naive game tree grows rapidly, even though the constraints are small.

The key observation is that every move always removes exactly one horizontal stick and one vertical stick. Nothing else matters. After one move, the number of remaining rows decreases by one and the number of remaining columns decreases by one.

Suppose we start with `n` rows and `m` columns. The game can continue only while both counts are positive. After each move, both counts decrease by one. Consequently, the total number of moves is exactly:

```
min(n, m)
```

The player who makes the last move wins. Since Akshat moves first, he wins when the number of moves is odd. Malvika wins when the number of moves is even.

The entire game reduces to checking the parity of `min(n, m)`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow and unnecessary |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read `n` and `m`.
2. Compute `moves = min(n, m)`.

Each move consumes exactly one row and one column. Once either rows or columns reach zero, no intersection points remain and the game ends.
3. Check whether `moves` is odd or even.

If the total number of moves is odd, the first player makes the last move.

If the total number of moves is even, the second player makes the last move.
4. Print `"Akshat"` when `moves` is odd, otherwise print `"Malvika"`.

### Why it works

After every move, exactly one row and one column disappear. The game state is completely determined by the counts of remaining rows and columns. Starting from `(n, m)`, after `k` moves the state becomes `(n - k, m - k)`. The game stops when one of these reaches zero, which happens after exactly `min(n, m)` moves. Since players alternate turns, the winner is determined solely by whether this number is odd or even.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m = map(int, input().split())

if min(n, m) % 2 == 1:
    print("Akshat")
else:
    print("Malvika")
```

The implementation directly follows the mathematical observation. First, it computes how many moves the game must contain. That value is `min(n, m)` because every move removes one row and one column.

The parity of this value determines who makes the final move. An odd number of moves means the first player moves last, while an even number means the second player moves last.

There are no tricky boundary conditions because both dimensions are at least one, and the answer depends only on a single parity check.

## Worked Examples

### Example 1

Input:

```
2 2
```

| Step | Remaining Rows | Remaining Columns | Player |
| --- | --- | --- | --- |
| Start | 2 | 2 | Akshat |
| Move 1 | 1 | 1 | Akshat |
| Move 2 | 0 | 0 | Malvika |

Here `min(2, 2) = 2`. The total number of moves is even, so Malvika makes the final move and wins.

### Example 2

Input:

```
3 4
```

| Step | Remaining Rows | Remaining Columns | Player |
| --- | --- | --- | --- |
| Start | 3 | 4 | Akshat |
| Move 1 | 2 | 3 | Akshat |
| Move 2 | 1 | 2 | Malvika |
| Move 3 | 0 | 1 | Akshat |

Here `min(3, 4) = 3`. The total number of moves is odd, so Akshat makes the final move and wins.

This trace demonstrates that only the number of remaining rows and columns matters. The actual intersection selected never changes the move count.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | One minimum operation and one parity check |
| Space | O(1) | Uses only a few variables |

The solution performs a constant amount of work regardless of the input values. It easily satisfies the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import io
import sys

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    n, m = map(int, input().split())
    return "Akshat" if min(n, m) % 2 else "Malvika"

# provided sample
assert run("2 2\n") == "Malvika", "sample 1"

# minimum grid
assert run("1 1\n") == "Akshat", "single move"

# one row only
assert run("1 100\n") == "Akshat", "game ends after one move"

# odd minimum dimension
assert run("3 4\n") == "Akshat", "odd move count"

# even minimum dimension
assert run("4 4\n") == "Malvika", "even move count"

# maximum values
assert run("100 100\n") == "Malvika", "largest constraints"

# asymmetric large grid
assert run("99 100\n") == "Akshat", "odd minimum dimension"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | `Akshat` | Smallest possible game |
| `1 100` | `Akshat` | Single available move |
| `3 4` | `Akshat` | Odd move count |
| `4 4` | `Malvika` | Even move count |
| `100 100` | `Malvika` | Maximum constraints |
| `99 100` | `Akshat` | Large asymmetric case |

## Edge Cases

Consider the input:

```
1 1
```

There is exactly one intersection. Akshat removes it on the first turn, leaving no moves for Malvika. The algorithm computes `min(1, 1) = 1`, which is odd, and correctly returns `Akshat`.

Consider the input:

```
1 5
```

A common mistake is to think there are five possible moves because there are five intersections. In reality, the first move removes the only horizontal stick, eliminating every intersection immediately. The algorithm computes `min(1, 5) = 1` and correctly returns `Akshat`.

Consider the input:

```
100 100
```

A simulation-based solution might unnecessarily model the entire board. The mathematical observation shows there are exactly 100 moves. Since 100 is even, Malvika makes the final move. The algorithm returns `Malvika` in constant time.

Consider the input:

```
2 3
```

The game lasts exactly two moves. After the first move, one row and one column disappear. After the second move, no rows remain. The algorithm computes `min(2, 3) = 2`, detects even parity, and correctly returns `Malvika`. This case confirms that the larger dimension never affects the winner once the smaller dimension is known.
