---
title: "CF 102775E - \u041a\u0430\u043c\u0435\u043d\u044c, \u043d\u043e\u0436\u043d\u0438\u0446\u044b, \u0431\u0443\u043c\u0430\u0433\u0430..."
description: "The game has seven possible moves, and two players each choose one move. The first word in the input is the move of the cheerful controller, and the second word is the move of the sad controller."
date: "2026-07-27T20:38:22+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102775
codeforces_index: "E"
codeforces_contest_name: "ICPC Central Russia Regional Contest (CRRC 20), \u0427\u0435\u043c\u043f\u0438\u043e\u043d\u0430\u0442 \u0426\u0435\u043d\u0442\u0440\u0430\u043b\u044c\u043d\u043e\u0439 \u0420\u043e\u0441\u0441\u0438\u0438, \u043a\u0432\u0430\u043b\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u043e\u043d\u043d\u044b\u0439 \u0440\u0430\u0443\u043d\u0434"
rating: 0
weight: 102775
solve_time_s: 42
verified: true
draft: false
---

[CF 102775E - \u041a\u0430\u043c\u0435\u043d\u044c, \u043d\u043e\u0436\u043d\u0438\u0446\u044b, \u0431\u0443\u043c\u0430\u0433\u0430...](https://codeforces.com/problemset/problem/102775/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 42s  
**Verified:** yes  

## Solution
## Problem Understanding

The game has seven possible moves, and two players each choose one move. The first word in the input is the move of the cheerful controller, and the second word is the move of the sad controller. The task is to determine the result from the perspective of the cheerful controller: output `1` if the first player wins, `-1` if the second player wins, and `0` if both chose the same move.

The number of possible moves is fixed at seven, so there is no large input size to optimize around. The main difficulty is not performance, but representing the rules correctly. A direct simulation of all cases is enough because there are only a small number of possible pairs. Even an approach checking every possible combination performs only a constant amount of work.

The input contains exactly two strings, so memory usage is naturally constant. There is no need for data structures that grow with the input size. The time limit is easily satisfied by any solution that performs only a few dictionary lookups or comparisons.

The main mistakes come from incomplete handling of the rules. A careless implementation might only store half of the winning relations and forget that the winner depends on the order of the two players. For example, with the input:

```
stone scissors
```

the correct output is:

```
1
```

because stone beats scissors. A program that checks only whether the second move can beat the first may reverse the result.

Another common mistake is forgetting the draw case. For example:

```
ax ax
```

has the correct output:

```
0
```

because equal moves always result in a tie. A program that only searches for winning pairs might incorrectly report a loss because it cannot find a winning relation.

## Approaches

The straightforward approach is to list every winning pair for the cheerful controller. When the first move and second move are read, we check whether this exact pair appears among the winning combinations. If it does, the answer is `1`. If the reverse pair appears, the second controller wins and the answer is `-1`. If neither happens, the moves are equal and the answer is `0`.

This brute-force idea is already fast enough because the game has only seven moves. There are at most 49 possible ordered pairs of moves, and checking them requires a fixed number of operations.

A more structured implementation stores all winning relations in a set. This changes the solution from manually checking many conditions to performing a single membership test. The key observation is that the rules describe a directed relation: one move can defeat another move, but the reverse is not always true. A set of ordered pairs represents exactly this structure.

The brute-force solution works because the state space is tiny, but it can become difficult to maintain if the number of moves grows. The observation that the rules are simply a collection of directed edges lets us represent the game compactly and answer the query with constant-time lookups.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(1) | O(1) | Accepted |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the two chosen moves. The first value belongs to the cheerful controller and the second value belongs to the sad controller, so keeping this order is necessary for determining the sign of the answer.
2. Store all winning pairs of moves where the first element beats the second element. Each pair is directed because `stone` beating `scissors` does not mean `scissors` beats `stone`.
3. Check whether the pair `(first_move, second_move)` is present in the winning set. If it is present, the cheerful controller wins and the answer is `1`.
4. Check whether the pair `(second_move, first_move)` is present. If it is present, the sad controller wins because the second player's move defeats the first player's move.
5. If neither ordered pair exists, the only remaining possibility is that both moves are the same. Output `0`.

The reason this works is that every non-draw game state has exactly one winning direction. The stored relations contain every possible victory, so one of the two ordered pairs must be found when there is a winner. Equal moves create no winning relation in either direction, which naturally produces a draw.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    first, second = input().split()

    wins = {
        ("stone", "scissors"),
        ("stone", "controller"),
        ("stone", "knife"),
        ("scissors", "paper"),
        ("scissors", "pliers"),
        ("scissors", "controller"),
        ("paper", "ax"),
        ("paper", "stone"),
        ("paper", "pliers"),
        ("pliers", "stone"),
        ("pliers", "knife"),
        ("pliers", "ax"),
        ("knife", "controller"),
        ("knife", "paper"),
        ("knife", "scissors"),
        ("ax", "knife"),
        ("ax", "scissors"),
        ("ax", "stone"),
        ("controller", "pliers"),
        ("controller", "ax"),
        ("controller", "paper"),
    }

    if (first, second) in wins:
        print(1)
    elif (second, first) in wins:
        print(-1)
    else:
        print(0)

if __name__ == "__main__":
    solve()
```

The input section reads exactly two strings and keeps their order because the first value always represents the cheerful controller.

The `wins` set contains ordered pairs. Using a set avoids a long chain of conditional statements and makes the relationship between the game rules and the implementation direct. Each lookup is constant time.

The first membership check asks whether the cheerful controller has a winning move. The second check reverses the pair and asks whether the sad controller wins. Equal moves or any impossible pair reach the final branch and produce a draw.

There are no boundary calculations, loops, or numeric operations, so issues like overflow or off-by-one errors cannot appear. The only implementation detail that requires care is writing every winning relation with the correct direction.

## Worked Examples

### Sample 1

Input:

```
stone paper
```

Trace:

| Step | First move | Second move | Checked pair | Result |
| --- | --- | --- | --- | --- |
| 1 | stone | paper | (stone, paper) | Not in wins |
| 2 | stone | paper | (paper, stone) | In wins |
| 3 | stone | paper | Output | -1 |

The first player does not have a winning relation against paper. The reversed relation exists because paper defeats stone, so the sad controller wins.

### Sample 2

Input:

```
ax ax
```

Trace:

| Step | First move | Second move | Checked pair | Result |
| --- | --- | --- | --- | --- |
| 1 | ax | ax | (ax, ax) | Not in wins |
| 2 | ax | ax | (ax, ax) | Not in wins |
| 3 | ax | ax | Output | 0 |

Neither player has a winning relation because both selected the same move. The algorithm correctly identifies the draw.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | The algorithm performs two set lookups containing a fixed number of moves. |
| Space | O(1) | The winning relation contains a fixed number of pairs independent of input size. |

The solution easily fits the limits because the entire computation is constant time and uses only a small fixed amount of memory.

## Test Cases

```python
import sys
import io

def solve():
    first, second = input().split()

    wins = {
        ("stone", "scissors"),
        ("stone", "controller"),
        ("stone", "knife"),
        ("scissors", "paper"),
        ("scissors", "pliers"),
        ("scissors", "controller"),
        ("paper", "ax"),
        ("paper", "stone"),
        ("paper", "pliers"),
        ("pliers", "stone"),
        ("pliers", "knife"),
        ("pliers", "ax"),
        ("knife", "controller"),
        ("knife", "paper"),
        ("knife", "scissors"),
        ("ax", "knife"),
        ("ax", "scissors"),
        ("ax", "stone"),
        ("controller", "pliers"),
        ("controller", "ax"),
        ("controller", "paper"),
    }

    if (first, second) in wins:
        return "1"
    if (second, first) in wins:
        return "-1"
    return "0"

def run(inp: str) -> str:
    old_stdin = sys.stdin
    try:
        sys.stdin = io.StringIO(inp)
        return solve()
    finally:
        sys.stdin = old_stdin

assert run("stone paper\n") == "-1", "sample 1"
assert run("ax ax\n") == "0", "sample 2"

assert run("stone scissors\n") == "1", "direct win"
assert run("controller paper\n") == "1", "controller special move"
assert run("paper ax\n") == "1", "reverse direction check"
assert run("knife stone\n") == "-1", "second player win"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| stone paper | -1 | Checks a case where the second player wins. |
| ax ax | 0 | Checks the draw condition. |
| stone scissors | 1 | Checks a direct first-player victory. |
| controller paper | 1 | Checks one of the special move interactions. |
| paper ax | 1 | Checks that the stored direction is handled correctly. |
| knife stone | -1 | Checks reversed winning relations. |

## Edge Cases

For equal moves, the algorithm checks both directions and finds no winning pair. For the input:

```
ax ax
```

the pair `(ax, ax)` is absent from the winning set, and the reversed pair is identical and also absent. The final branch outputs `0`, which matches the rules.

For a reversed victory, the order of the input matters. With:

```
knife stone
```

the pair `(knife, stone)` is not a winning relation. The reversed pair `(stone, knife)` exists because stone defeats knife. The algorithm outputs `-1`, correctly assigning the victory to the second controller.

For the special move `controller`, the implementation treats it like every other move. With:

```
controller ax
```

the pair `(controller, ax)` exists, so the first controller wins and the answer is `1`. This confirms that uncommon moves are not accidentally ignored or handled differently.

I can also adapt this into a shorter Codeforces-style editorial format if you need something closer to an official contest explanation.
