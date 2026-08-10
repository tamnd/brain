---
title: "CF 102397F - Weird Game"
description: "There are n cupcakes on the table, and Mahmoud makes the first move. On each turn, the current player may eat exactly one cupcake. If the current number of cupcakes is even, the player also has the option to eat exactly half of them."
date: "2026-08-11T05:11:50+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102397
codeforces_index: "F"
codeforces_contest_name: "Asu Coding Cup 4"
rating: 0
weight: 102397
solve_time_s: 412
verified: true
draft: false
---

[CF 102397F - Weird Game](https://codeforces.com/problemset/problem/102397/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 6m 52s  
**Verified:** yes  

## Solution
## Problem Understanding

There are `n` cupcakes on the table, and Mahmoud makes the first move. On each turn, the current player may eat exactly one cupcake. If the current number of cupcakes is even, the player also has the option to eat exactly half of them. The player who faces exactly one cupcake loses immediately, so the game ends when a turn begins with `1`.

The task is to determine which player wins when both players choose their moves optimally. The input contains one integer `n`, representing the initial number of cupcakes. The output is `Mahmoud` if the first player has a winning strategy and `Bashar` otherwise.

The constraint `n <= 10^9` is the key difficulty. A solution that examines every value from `1` through `n` would require up to one billion states, which is far beyond what a 1.5 second time limit can support. Even an `O(n)` dynamic program is too slow here. We need to reduce the game to a constant-time property of `n`.

The smallest states reveal several edge cases that can fool a direct implementation. For `n = 1`, Mahmoud loses immediately because the starting position already contains one cupcake, so the correct output is `Bashar`. A careless implementation that first tries to make a move would incorrectly treat this as a normal game state.

For `n = 2`, Mahmoud can eat one cupcake and leave `1`, so Bashar loses and the answer is `Mahmoud`. The half operation also exists here, but it produces the same state, which means an implementation that assumes the half operation is always meaningfully different could mishandle this boundary.

For `n = 3`, Mahmoud can only eat one cupcake, leaving `2`. Bashar then leaves `1`, so Mahmoud loses. The correct output is `Bashar`. This is the smallest odd losing position after `1` and is useful for catching solutions that only check whether `n` is greater than one.

For `n = 4`, the correct answer is `Mahmoud`. Mahmoud can eat one cupcake and leave `3`. Bashar is then forced to leave `2`, and Mahmoud leaves `1`. The key point is that Mahmoud does not need to use the half operation. A solution that always chooses `n / 2` when possible can produce the wrong winner.

## Approaches

A direct approach is to classify every number of cupcakes as either winning or losing. A position is losing if every legal move gives the opponent a winning position. It is winning if at least one legal move gives the opponent a losing position. Starting with `1` as losing, we can compute the answer for `2, 3, ..., n`.

This dynamic program is correct because every move from `x` leads to a smaller number, either `x - 1` or `x / 2`. Consequently, when we process `x`, the result of every possible destination is already known. However, it requires examining up to `n` states. For `n = 10^9`, that means roughly one billion state evaluations, and checking the available transitions can bring the work close to two billion transition checks. The memory requirement would also be `O(n)` if the whole table were stored.

The brute-force computation works because the game graph always moves toward smaller numbers, but it fails because the upper bound is too large. The observation that unlocks the faster solution comes from looking at the parity of the positions. The position `1` is losing. Every odd number greater than `1` has only one possible move, from `x` to `x - 1`, which is even. Every even number has a move to `x - 1`, which is odd. If all odd positions are losing and all even positions are winning, this relationship reproduces itself for every larger number.

An odd position is therefore losing because its only move leads to an even winning position. An even position is winning because eating one cupcake leads to an odd losing position. The half operation does not disturb this classification: when an even number is halved, the result can be either even or odd, but an even position already has a winning move to `n - 1`, so the extra move cannot make it losing.

The entire game consequently depends only on whether the initial number of cupcakes is odd or even. If `n` is even, Mahmoud wins. If `n` is odd, Bashar wins.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force DP | O(n) | O(n) | Too slow |
| Optimal parity observation | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the initial number of cupcakes `n`. The only property we need after deriving the game pattern is its parity.
2. If `n` is even, output `Mahmoud`. An even position is winning because Mahmoud can eat exactly one cupcake and leave `n - 1`, which is odd and therefore losing for the next player.
3. If `n` is odd, output `Bashar`. Mahmoud can only move from an odd number `n` to the even number `n - 1`, and an even position is winning for the player who receives it.
4. The special case `n = 1` is already covered by the odd case. Mahmoud starts with one cupcake and loses, so the output is `Bashar`.

### Why it works

The invariant is that every odd number of cupcakes is a losing position and every even number is a winning position. The base case `1` is losing. For an odd `n > 1`, the only legal move is to `n - 1`, which is even and therefore winning for the opponent. Thus the odd position is losing. For an even `n`, eating one cupcake moves to `n - 1`, which is odd and therefore losing for the opponent, so the even position is winning. This proves the classification for every positive integer, including the full range up to `10^9`.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())

if n % 2 == 0:
    print("Mahmoud")
else:
    print("Bashar")
```

The input consists of a single integer, so one call to `input()` is enough. We convert it to an integer and inspect `n % 2`.

The even branch prints `Mahmoud` because Mahmoud can always remove one cupcake and leave an odd losing position. The odd branch prints `Bashar`, including the boundary case `n = 1`.

There is no need to simulate moves, construct a dynamic programming table, or use recursion. Python integers can represent the given value comfortably, although even a fixed-width 32-bit signed integer would also be sufficient for `10^9`. The modulo operation has no off-by-one issue because the losing condition is exactly odd parity, including `1`.

## Worked Examples

### Sample 1

For the first sample, `n = 4`.

| n | Current player | Available reasoning | Resulting n | Position |
| --- | --- | --- | --- | --- |
| 4 | Mahmoud | Eat 1 | 3 | Losing |
| 3 | Bashar | Eat 1 | 2 | Winning |
| 2 | Mahmoud | Eat 1 | 1 | Losing |
| 1 | Bashar | No move, loses | 1 | Terminal |

The optimal sequence leaves Bashar facing one cupcake. The trace demonstrates the central invariant: even positions are winning and odd positions are losing.

The program sees that `4 % 2 == 0` and immediately prints `Mahmoud`.

### Sample 2

For the second sample, `n = 3`.

| n | Current player | Available move | Resulting n | Position |
| --- | --- | --- | --- | --- |
| 3 | Mahmoud | Eat 1 | 2 | Winning |
| 2 | Bashar | Eat 1 | 1 | Losing |
| 1 | Mahmoud | No move, loses | 1 | Terminal |

Mahmoud is forced to give Bashar an even position. Bashar then gives Mahmoud the terminal position, so Mahmoud loses.

The program sees that `3 % 2 == 1` and prints `Bashar`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only one modulo operation and one output operation are performed |
| Space | O(1) | No data structure grows with `n` |

The maximum input is `10^9`, but the algorithm never iterates up to that value. It performs a constant number of operations, so it comfortably fits within the 1.5 second time limit and uses negligible memory.

## Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline
    n = int(input())

    if n % 2 == 0:
        print("Mahmoud")
    else:
        print("Bashar")

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

# Provided samples
assert run("4\n") == "Mahmoud", "sample 1"
assert run("3\n") == "Bashar", "sample 2"

# Minimum-size input
assert run("1\n") == "Bashar", "n = 1 is immediately losing"

# Smallest even input
assert run("2\n") == "Mahmoud", "n = 2 is winning"

# Odd boundary
assert run("999999999\n") == "Bashar", "large odd input"

# Maximum-size input
assert run("1000000000\n") == "Mahmoud", "maximum even input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `Bashar` | Minimum input and immediate losing state |
| `2` | `Mahmoud` | Smallest winning state and even boundary |
| `999999999` | `Bashar` | Large odd value without simulation |
| `1000000000` | `Mahmoud` | Maximum constraint and large even value |

## Edge Cases

For `n = 1`, the algorithm takes the odd branch and prints `Bashar`. No move is attempted, which correctly models the rule that the player whose turn starts with one cupcake loses.

For `n = 2`, the algorithm takes the even branch and prints `Mahmoud`. Mahmoud can eat one cupcake, producing `1` for Bashar. This also demonstrates why the solution must not treat the half operation as mandatory. Whether Mahmoud considers eating one or half, the position remains winning for him.

For `n = 3`, the algorithm takes the odd branch and prints `Bashar`. Mahmoud can only move to `2`, which is winning for Bashar. Bashar then moves to `1`, leaving Mahmoud with the losing terminal position.

For `n = 4`, the algorithm takes the even branch and prints `Mahmoud`. The winning move is `4 -> 3`. Since `3` is losing, Mahmoud has already established a winning strategy. The half move `4 -> 2` is irrelevant because a winning position only needs one winning move.

For the maximum input `n = 10^9`, the number is even, so the program prints `Mahmoud` after one parity check. No loop depends on the magnitude of `n`, which is exactly why the solution remains constant-time at the largest allowed input.
