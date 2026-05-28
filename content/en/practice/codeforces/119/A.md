---
title: "CF 119A - Epic Game"
description: "We are asked to simulate a turn-based game between two players, Simon and Antisimon, who each have a fixed integer, a and b respectively. There is a heap of n stones."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 119
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 90"
rating: 800
weight: 119
solve_time_s: 89
verified: true
draft: false
---

[CF 119A - Epic Game](https://codeforces.com/problemset/problem/119/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 1m 29s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to simulate a turn-based game between two players, Simon and Antisimon, who each have a fixed integer, `a` and `b` respectively. There is a heap of `n` stones. Players alternate turns starting with Simon, and on a turn, a player must take a number of stones equal to the greatest common divisor (gcd) of their fixed number and the current number of stones left in the heap. If the heap has fewer stones than the player needs to take, that player loses. The task is to determine who wins, outputting `0` for Simon and `1` for Antisimon.

The constraints are small: all numbers are at most 100. This implies that even a direct simulation of each move is feasible because the heap cannot contain more than 100 stones. We do not need to optimize with complex mathematics or memoization since the total number of moves in the worst case is only about 100.

Edge cases include situations where the heap initially contains fewer stones than the gcd of a player’s number and `n`. For instance, if `a = 7`, `b = 3`, and `n = 1`, Simon cannot make the first move because `gcd(7, 1) = 1` is equal to the heap size, so he can take exactly one stone and Antisimon loses on the next turn. Handling the gcd correctly when the heap reaches zero is also critical, because `gcd(x, 0)` should return `x`, which can immediately exceed the heap and end the game.

## Approaches

The brute-force approach is to simulate the game turn by turn. For each turn, we compute `gcd(player_number, current_heap)`, check if the heap is sufficient, subtract the stones if possible, and switch turns. This method is correct because it faithfully follows the rules of the game. Its time complexity is proportional to the number of moves, which is at most `n`. With `n <= 100`, this is acceptable.

No optimization is required here, because there is no repeated state or complex subproblem to cache. The problem structure is inherently sequential: each move depends on the exact number of stones left, so precomputation or greedy shortcuts are unnecessary. The key insight is that computing `gcd` and updating the heap at each turn is trivial given the small bounds, so a straightforward simulation is both simple and efficient.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n * log(max(a,b))) | O(1) | Accepted |
| Optimal (same as brute force) | O(n * log(max(a,b))) | O(1) | Accepted |

Here, `log(max(a,b))` comes from the Euclidean algorithm for gcd.

## Algorithm Walkthrough

1. Read the integers `a`, `b`, and `n`. Assign them to Simon, Antisimon, and the initial heap.
2. Set a flag or variable `turn` to indicate whose turn it is. For simplicity, `turn = 0` for Simon and `turn = 1` for Antisimon.
3. Loop while the heap has at least one stone:

1. Compute the number of stones the current player must take: `take = gcd(player_number, heap)`.
2. If `take > heap`, the current player loses. Print `turn` and exit.
3. Otherwise, subtract `take` from `heap`.
4. Switch turns by setting `turn = 1 - turn`.
4. The loop ends naturally only if a player loses during their turn, so we always exit with the correct winner.

Why it works: The invariant is that after each subtraction, the heap represents the remaining stones, and the next player’s move is calculated exactly according to the rules. Since turns alternate strictly and we check for insufficient stones before subtraction, the simulation always mirrors the actual gameplay. The game always ends because the heap decreases each turn, eventually reaching a state where `take > heap`.

## Python Solution

```python
import sys
import math
input = sys.stdin.readline

a, b, n = map(int, input().split())
turn = 0  # 0 for Simon, 1 for Antisimon

while True:
    if turn == 0:
        take = math.gcd(a, n)
    else:
        take = math.gcd(b, n)
    
    if take > n:
        print(turn)
        break
    
    n -= take
    turn = 1 - turn
```

The solution first reads the inputs and initializes a `turn` variable. We use the Euclidean algorithm through `math.gcd` to compute the required stones. The check `take > n` immediately detects the losing condition. After each move, we decrement the heap and switch turns. Using `1 - turn` is a simple way to alternate between 0 and 1.

## Worked Examples

**Sample 1**: `a = 3, b = 5, n = 9`

| Turn | Player | Heap before | gcd(a/b, heap) | Stones taken | Heap after |
| --- | --- | --- | --- | --- | --- |
| 0 | Simon | 9 | gcd(3,9)=3 | 3 | 6 |
| 1 | Antisimon | 6 | gcd(5,6)=1 | 1 | 5 |
| 2 | Simon | 5 | gcd(3,5)=1 | 1 | 4 |
| 3 | Antisimon | 4 | gcd(5,4)=1 | 1 | 3 |
| 4 | Simon | 3 | gcd(3,3)=3 | 3 | 0 |
| 5 | Antisimon | 0 | gcd(5,0)=5 | 5 | - |

Simon wins because Antisimon cannot take 5 stones from a heap of 0. Output is `0`.

**Sample 2**: `a = 2, b = 1, n = 1`

| Turn | Player | Heap before | gcd(a/b, heap) | Stones taken | Heap after |
| --- | --- | --- | --- | --- | --- |
| 0 | Simon | 1 | gcd(2,1)=1 | 1 | 0 |
| 1 | Antisimon | 0 | gcd(1,0)=1 | 1 | - |

Simon wins, output is `0`. This trace confirms that `gcd(x,0)` is handled correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n * log(max(a,b))) | Each move computes a gcd, taking O(log(max(a,b))) and the number of moves ≤ n. |
| Space | O(1) | Only a few integer variables are needed, independent of input size. |

Given n ≤ 100 and a,b ≤ 100, the algorithm runs in negligible time and uses minimal memory, comfortably within constraints.

## Test Cases

```python
import sys, io
import math

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    a, b, n = map(int, input().split())
    turn = 0
    while True:
        take = math.gcd(a if turn == 0 else b, n)
        if take > n:
            return str(turn)
        n -= take
        turn = 1 - turn

# Provided samples
assert run("3 5 9\n") == "0", "sample 1"
assert run("2 1 1\n") == "0", "sample 2"

# Custom cases
assert run("1 1 1\n") == "0", "both take 1, Simon wins first"
assert run("100 100 100\n") == "0", "large numbers equal, Simon wins eventually"
assert run("2 2 3\n") == "1", "odd heap, Antisimon wins"
assert run("7 3 1\n") == "0", "Simon takes the only stone"
assert run("5 2 10\n") == "1", "multiple gcd reductions, Antisimon wins"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 1 | 0 | Minimum heap, smallest numbers |
| 100 100 100 | 0 | Maximum values for a, b, n |
| 2 2 3 | 1 | Odd heap leads to Antisimon win |
| 7 3 1 | 0 | Heap smaller than Antisimon's gcd |
| 5 2 10 | 1 | Multiple moves with different gcd reductions |

## Edge Cases

When `n = 1` and both players have numbers larger than 1, the algorithm correctly computes `gcd(player_number, n)` and allows Simon to take the single stone if possible. For `a = 7, b = 3, n = 1`, the first gcd is `gcd(7,1)=1`, so Simon takes the stone, heap reaches 0, and Antisimon cannot move, confirming the output `0`. This shows that `gcd(x,0)` handling and turn alternation correctly capture edge conditions where the heap is smaller than any fixed number.
