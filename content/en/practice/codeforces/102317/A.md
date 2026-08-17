---
title: "CF 102317A - Majestic 10"
description: "The problem asks us to process several basketball players. Each player has exactly three statistics, such as points, rebounds, or assists. A statistic counts as a \"double\" when it is at least 10."
date: "2026-08-17T10:13:37+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102317
codeforces_index: "A"
codeforces_contest_name: "UCF Locals 2016"
rating: 0
weight: 102317
solve_time_s: 59
verified: true
draft: false
---

[CF 102317A - Majestic 10](https://codeforces.com/problemset/problem/102317/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 59s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem asks us to process several basketball players. Each player has exactly three statistics, such as points, rebounds, or assists. A statistic counts as a "double" when it is at least 10. For each player, we must print the three original statistics, then describe whether the player has zero, one, two, or three such statistics.

The four possible descriptions are `zilch` for zero statistics reaching 10, `double` for exactly one, `double-double` for exactly two, and `triple-double` for all three. The input contains a positive number of players, followed by three integer statistics for every player. Each statistic lies between 0 and 100 inclusive.

The constraints make this a direct linear scan. There are only three values per player, so processing one player takes a constant amount of work. The statement does not impose an upper bound on the number of players, but even a very large number of players only requires constant work per player, giving an O(n) algorithm where n is the number of players. There is no reason to consider sorting, dynamic programming, graph algorithms, or any quadratic operation.

The main boundary case is the value 10 itself. Since 10 counts as a double, the comparison must be `>= 10`, not `> 10`. For example,

```
1
10 0 0
```

produces

```
10 0 0
double
```

A careless implementation using `> 10` would incorrectly print `zilch`.

The opposite boundary is 9, which does not count. For example,

```
1
9 9 9
```

produces

```
9 9 9
zilch
```

Checking only whether a value is positive would incorrectly classify this player.

All three statistics can qualify simultaneously. For example,

```
1
10 20 30
```

produces

```
10 20 30
triple-double
```

A chain of independent `if` statements that prints an answer immediately for the first qualifying statistic could incorrectly stop at `double`. The correct approach counts all qualifying statistics before choosing the description.

The zero case also matters. For

```
1
0 1 9
```

the output is

```
0 1 9
zilch
```

The player still has three valid statistics, but none reaches the threshold.

## Approaches

The straightforward approach is already optimal in asymptotic terms. For every player, inspect the three statistics one by one and count how many satisfy `value >= 10`. Because there are exactly three statistics, this requires at most three comparisons per player, followed by one selection among four possible strings. For n players, the worst case is exactly 3n threshold comparisons, plus O(n) work for producing the output.

There is no genuinely faster asymptotic technique to discover here. The answer depends independently on every one of the three statistics, so an algorithm must at least read the input values. The key observation is that the entire state of a player can be represented by one small integer, the number of statistics reaching 10. Once that count is known, the required message follows directly.

The brute-force and optimal approaches are consequently the same linear scan. The useful optimization is conceptual rather than asymptotic: instead of writing four separate cases based on the actual values, reduce each player to the count of qualifying statistics. That makes the boundary condition explicit and prevents overlapping conditions from producing the wrong message.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(1) | Accepted |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of players. This tells us exactly how many groups of three statistics must be processed.
2. For each player, read the three statistics and initialize a counter to zero. The counter will represent the number of doubles earned by this player.
3. Check each of the three statistics against the threshold 10 using `>=`. Increment the counter whenever the statistic is at least 10. The inclusive comparison is required because a value of exactly 10 qualifies.
4. Choose the message corresponding to the counter. A count of 0 maps to `zilch`, 1 to `double`, 2 to `double-double`, and 3 to `triple-double`.
5. Print the original three statistics followed by the selected message. Print a blank line after the player's result, matching the required output format.

The invariant is simple: after processing any prefix of the three statistics, the counter equals exactly the number of processed statistics that are at least 10. Each statistic contributes one to the counter if and only if it qualifies, so after all three have been processed the counter is exactly the number of doubles. The final mapping from 0 through 3 is exhaustive, so the selected message must be correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    output = []

    names = ["zilch", "double", "double-double", "triple-double"]

    for _ in range(n):
        stats = list(map(int, input().split()))

        doubles = sum(value >= 10 for value in stats)
        output.append(f"{stats[0]} {stats[1]} {stats[2]}\n{names[doubles]}")

    sys.stdout.write("\n\n".join(output) + "\n\n")

if __name__ == "__main__":
    solve()
```

The `names` array directly encodes the four possible answers. Its index is the number of statistics satisfying the threshold, so `names[doubles]` avoids a longer chain of conditional statements.

Python treats `True` as 1 and `False` as 0, which makes `sum(value >= 10 for value in stats)` a compact way to count qualifying statistics. The comparison remains inclusive, so 10 is handled correctly.

The original statistics are stored so they can be reproduced exactly in the required order. Since there are only three values per player, this uses constant memory per player. The `output` list stores the generated output for all players before writing it once, which also keeps I/O efficient when there are many players.

There is no integer overflow issue because every input statistic is at most 100 and the counter can only be 0, 1, 2, or 3. The final `"\n\n"` gives every player's output block the required blank line, including the final player.

## Worked Examples

For Sample 1, the input contains four players. The processing can be traced as follows.

| Player | Statistics | Qualifying values | `doubles` | Message |
| --- | --- | --- | --- | --- |
| 1 | 5 0 8 | none | 0 | `zilch` |
| 2 | 30 10 50 | 30, 10, 50 | 3 | `triple-double` |
| 3 | 20 5 20 | 20, 20 | 2 | `double-double` |
| 4 | 5 100 6 | 100 | 1 | `double` |

The resulting output is

```
5 0 8
zilch

30 10 50
triple-double

20 5 20
double-double

5 100 6
double
```

This example exercises every possible value of the counter, from zero through three. It also confirms that exactly 10 qualifies because the second player's middle statistic is 10.

A second useful example focuses on the threshold itself and on values immediately below and above it.

```
3
9 10 11
0 0 0
10 10 10
```

| Player | Statistics | After first check | After second check | After third check | Message |
| --- | --- | --- | --- | --- | --- |
| 1 | 9 10 11 | 0 | 1 | 2 | `double-double` |
| 2 | 0 0 0 | 0 | 0 | 0 | `zilch` |
| 3 | 10 10 10 | 1 | 2 | 3 | `triple-double` |

The corresponding output is

```
9 10 11
double-double

0 0 0
zilch

10 10 10
triple-double
```

The first player demonstrates both sides of the boundary in a single row. The value 9 is rejected, while 10 and 11 are accepted. The third player confirms that three qualifying values produce `triple-double`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each of the n players has exactly three statistics checked, so the work per player is constant. |
| Space | O(n) | The implementation stores the generated output for all players before writing it. The algorithm itself requires O(1) auxiliary space per player. |

The problem has a constant amount of computation per player, so the running time grows linearly with the number of players. Even if the input contains a very large number of players, the algorithm performs only three threshold checks per player and does not perform any nested scan. The statistic values themselves are tiny, so memory used by the algorithm is independent of their magnitude.

## Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline
    n = int(input())
    output = []

    names = ["zilch", "double", "double-double", "triple-double"]

    for _ in range(n):
        stats = list(map(int, input().split()))
        doubles = sum(value >= 10 for value in stats)
        output.append(f"{stats[0]} {stats[1]} {stats[2]}\n{names[doubles]}")

    sys.stdout.write("\n\n".join(output) + "\n\n")

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided sample
assert run(
    """4
5 0 8
30 10 50
20 5 20
5 100 6
"""
) == (
    """5 0 8
zilch

30 10 50
triple-double

20 5 20
double-double

5 100 6
double

"""
), "sample 1"

# Minimum-size input
assert run(
    """1
0 0 0
"""
) == (
    """0 0 0
zilch

"""
), "minimum-size case"

# All values equal to the threshold
assert run(
    """1
10 10 10
"""
) == (
    """10 10 10
triple-double

"""
), "threshold is inclusive"

# Values immediately around the threshold
assert run(
    """3
9 9 9
9 10 11
11 9 10
"""
) == (
    """9 9 9
zilch

9 10 11
double-double

11 9 10
double-double

"""
), "boundary values"

# Large stress case
large_n = 100000
large_input = str(large_n) + "\n" + ("100 0 0\n" * large_n)
large_expected = ("100 0 0\ndouble\n\n" * large_n)
assert run(large_input) == large_expected, "large input"

print("All tests passed.")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 0 0 0` | `zilch` | Minimum-size input and zero qualifying statistics |
| `1 / 10 10 10` | `triple-double` | Inclusive threshold and all three qualifying |
| `3 / 9 9 9`, `9 10 11`, `11 9 10` | `zilch`, `double-double`, `double-double` | Values immediately below, at, and above the boundary |
| 100000 players with `100 0 0` | `double` for every player | Large input and linear-time behavior |

## Edge Cases

The most dangerous boundary case is exactly 10. For

```
1
10 0 0
```

the algorithm examines 10 first, evaluates `10 >= 10` as true, and changes `doubles` from 0 to 1. The remaining values do not qualify, so the final count is 1 and the output is `double`. An implementation using `>` would produce the wrong answer.

The lower boundary behaves symmetrically. For

```
1
9 9 9
```

each comparison `9 >= 10` is false, leaving the counter at 0. The output is `zilch`. This catches implementations that accidentally test whether a statistic is positive rather than whether it reaches the required threshold.

The all-qualifying case is

```
1
10 10 10
```

The counter becomes 1 after the first value, 2 after the second, and 3 after the third. The final lookup is `names[3]`, which gives `triple-double`. A solution that prints as soon as it finds its first qualifying statistic would fail here.

The no-qualifying case is

```
1
0 0 0
```

The counter remains zero throughout the scan, so `names[0]` gives `zilch`. This also confirms that zero is a normal statistic value and does not require special input handling.

Finally, the output format itself can cause an otherwise correct solution to fail. For multiple players, each player's original statistics must be followed by its message, and a blank line separates the output blocks. The solution constructs one complete block per player and joins those blocks with two newline characters, preventing the statistics and message from different players from being accidentally mixed.
