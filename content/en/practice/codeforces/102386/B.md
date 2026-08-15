---
title: "CF 102386B - \u0422\u0443\u0440\u043d\u0438\u0440 \u0423\u0440\u0424\u0423"
description: "We need to judge one round of Rock-Paper-Scissors-Lizard-Spock. The first input line is the move chosen by the first player, and the second line is the move chosen by the second player. Each move is one of Rock, Scissors, Paper, Lizard, or Spock."
date: "2026-08-15T18:36:15+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102386
codeforces_index: "B"
codeforces_contest_name: "\u041a\u0432\u0430\u043b\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u043e\u043d\u043d\u044b\u0439 \u0442\u0443\u0440 \u0423\u0440\u0430\u043b\u044c\u0441\u043a\u043e\u0433\u043e \u0447\u0435\u0442\u0432\u0435\u0440\u0442\u044c\u0444\u0438\u043d\u0430\u043b\u0430 \u0427\u0435\u043c\u043f\u0438\u043e\u043d\u0430\u0442\u0430 \u043c\u0438\u0440\u0430 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e 2019"
rating: 0
weight: 102386
solve_time_s: 378
verified: false
draft: false
---

[CF 102386B - \u0422\u0443\u0440\u043d\u0438\u0440 \u0423\u0440\u0424\u0423](https://codeforces.com/problemset/problem/102386/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 6m 18s  
**Verified:** no  

## Solution
## Problem Understanding

We need to judge one round of Rock-Paper-Scissors-Lizard-Spock. The first input line is the move chosen by the first player, and the second line is the move chosen by the second player. Each move is one of `Rock`, `Scissors`, `Paper`, `Lizard`, or `Spock`.

Every move defeats exactly two other moves. `Scissors` defeats `Paper` and `Lizard`, `Paper` defeats `Rock` and `Spock`, `Rock` defeats `Lizard` and `Scissors`, `Lizard` defeats `Spock` and `Paper`, and `Spock` defeats `Scissors` and `Rock`. If both players choose the same move, the result is a tie.

The program must print `First` when the first move defeats the second, `Second` when the reverse is true, and `Tie` when the moves are equal.

There is no variable-sized input here. Exactly two strings are read, and each belongs to a fixed set of five possible values. Consequently, even a method that explicitly considers every possible pair of moves performs at most 25 comparisons. There is no meaningful large-`n` performance issue in this problem, so an O(1) solution is sufficient and easily fits any normal Codeforces limit.

The main edge cases come from treating the game as ordinary Rock-Paper-Scissors or from forgetting that every move has two winning opponents. For example,

```
Rock
Rock
```

must produce `Tie`. A careless implementation that only checks whether the first move beats the second could fall through to `Second` instead of handling equality first.

Another case is

```
Lizard
Spock
```

which produces `First`. Lizard defeats Spock, even though neither move belongs to the three standard choices from ordinary Rock-Paper-Scissors. An implementation containing only the classic three relationships would give an incorrect result.

A third useful boundary case is

```
Spock
Paper
```

which produces `Second`, because Paper defeats Spock. Checking only one of the two winning relationships for each move would miss this case.

## Approaches

A direct brute-force solution can explicitly enumerate all 25 ordered pairs of moves and associate each pair with its result. Since there are only five possible moves for each player, the worst case is exactly 25 pair checks. This approach is already fast enough, because 25 is a constant independent of the input size. There is no input size at which this particular brute-force method becomes too slow.

A more natural implementation uses the structure of the game itself. We store the ten directed winning relationships, then check whether the first player's move is one of the moves that defeats the second player's move. If so, the first player wins. Otherwise, if the moves are equal, the result is a tie. Every remaining pair must mean that the second player wins, because the rules define a winner for every pair of distinct moves.

The key observation is that the entire game is a fixed graph with only five vertices. Each move is a vertex, and an edge from `A` to `B` means that `A` defeats `B`. We do not need to search this graph or build anything dynamically. A constant-sized lookup structure directly represents all possible winning relationships.

The two approaches have the following complexity.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Enumerate all 25 possible pairs | O(1) | O(1) | Accepted |
| Winning-relation lookup | O(1) | O(1) | Accepted |

The lookup approach is preferable because it represents the rules directly and avoids a long chain of special cases.

## Algorithm Walkthrough

1. Read the two moves into `first` and `second`. There are exactly two input lines, so no test-case loop is needed.
2. If `first == second`, print `Tie`. Equal moves never defeat each other, regardless of which move they are.
3. Store the two moves defeated by each possible move. For example, `Rock` is associated with `Lizard` and `Scissors`, while `Spock` is associated with `Rock` and `Scissors`.
4. Check whether `second` belongs to the set of moves defeated by `first`. If it does, print `First`.
5. If the moves are different and the first move does not defeat the second, print `Second`. Every distinct pair has exactly one winner, so there is no fourth outcome to consider.

### Why it works

For every move `A`, the lookup structure contains exactly the two moves that `A` defeats according to the game rules. After the equality check, the two players have distinct moves. If the second move appears in the winning set of the first move, the rules say that the first player wins. Otherwise, the first player cannot defeat the second, and because every distinct pair has a winner, the second player must win. Thus every possible input reaches exactly its correct result.

## Python Solution

```python
import sys
input = sys.stdin.readline

first = input().strip()
second = input().strip()

wins = {
    "Rock": {"Lizard", "Scissors"},
    "Scissors": {"Paper", "Lizard"},
    "Paper": {"Rock", "Spock"},
    "Lizard": {"Spock", "Paper"},
    "Spock": {"Scissors", "Rock"},
}

if first == second:
    print("Tie")
elif second in wins[first]:
    print("First")
else:
    print("Second")
```

The dictionary `wins` is the complete representation of the game graph. Each key is one possible first-player move, and its value contains exactly the two moves that it defeats.

The equality check comes before the winning lookup because equality has its own result, `Tie`. Without this check, an equal pair would incorrectly fall into the `Second` case.

The expression `second in wins[first]` checks precisely the condition needed for the first player to win. If it is false after the moves have already been shown to differ, the second player necessarily wins.

There are no indexes, loops over input data, or arithmetic operations here, so there are no boundary or integer-overflow concerns. The `.strip()` calls remove the newline characters produced by `readline()` while preserving the exact move names.

## Worked Examples

### Sample 1

The input is:

```
Rock
Paper
```

The relevant state changes are:

| Step | `first` | `second` | Condition | Result |
| --- | --- | --- | --- | --- |
| Read input | `Rock` | `Paper` | Both moves stored | Continue |
| Equality check | `Rock` | `Paper` | `first == second` is false | Continue |
| Winning lookup | `Rock` | `Paper` | `Paper` is not defeated by `Rock` | `Second` |

`Rock` defeats `Lizard` and `Scissors`, not `Paper`. Since the moves differ, the only remaining winner is the second player. The program prints `Second`.

### Sample 2

The input is:

```
Rock
Rock
```

The trace is:

| Step | `first` | `second` | Condition | Result |
| --- | --- | --- | --- | --- |
| Read input | `Rock` | `Rock` | Both moves stored | Continue |
| Equality check | `Rock` | `Rock` | `first == second` is true | `Tie` |

The lookup is never needed. This demonstrates why equality must be handled before checking the winning relationships.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only two strings are read and one constant-sized lookup is performed. |
| Space | O(1) | The dictionary contains exactly five keys and ten winning relationships. |

The input size is fixed at two moves from a five-element set, so the algorithm performs only a constant number of operations and uses a constant amount of memory. It comfortably fits the problem's time and memory limits.

## Test Cases

```python
import sys
import io

def solve():
    first = input().strip()
    second = input().strip()

    wins = {
        "Rock": {"Lizard", "Scissors"},
        "Scissors": {"Paper", "Lizard"},
        "Paper": {"Rock", "Spock"},
        "Lizard": {"Spock", "Paper"},
        "Spock": {"Scissors", "Rock"},
    }

    if first == second:
        return "Tie"
    if second in wins[first]:
        return "First"
    return "Second"

def run(inp: str) -> str:
    global input
    old_stdin = sys.stdin
    old_input = input

    try:
        sys.stdin = io.StringIO(inp)
        input = sys.stdin.readline
        return solve()
    finally:
        sys.stdin = old_stdin
        input = old_input

# Provided samples
assert run("Rock\nPaper\n") == "Second", "sample 1"
assert run("Rock\nRock\n") == "Tie", "sample 2"
assert run("Lizard\nSpock\n") == "First", "sample 3"

# All equal values
assert run("Spock\nSpock\n") == "Tie", "equal moves"

# Reverse direction of a winning relationship
assert run("Paper\nRock\n") == "First", "Paper defeats Rock"
assert run("Rock\nPaper\n") == "Second", "Paper defeats Rock"

# Second winning relationship of a move
assert run("Spock\nRock\n") == "Second", "Rock defeats Spock"
assert run("Spock\nScissors\n") == "First", "Spock defeats Scissors"

# Lizard's two different winning relationships
assert run("Lizard\nPaper\n") == "First", "Lizard defeats Paper"
assert run("Paper\nLizard\n") == "Second", "Lizard defeats Paper"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `Spock / Spock` | `Tie` | Equality handling for another move |
| `Paper / Rock` | `First` | One direction of a winning relationship |
| `Spock / Rock` | `Second` | The second player winning with the first move's opponent |
| `Lizard / Paper` | `First` | The second winning edge of Lizard |
| `Paper / Lizard` | `Second` | Reversing the same relationship |

The problem does not actually have a separate minimum-size or maximum-size parameter. Each test case always contains exactly two moves, so the relevant boundary is the complete set of five possible values. The tests above cover all structural cases, including equal moves and both directions of several relationships.

## Edge Cases

The first edge case is equality. For

```
Rock
Rock
```

the algorithm reads both moves, finds that `first == second`, and immediately returns `Tie`. It does not attempt to treat `Rock` as defeating itself, because self-comparisons are excluded by the game rules.

The second edge case is a move with two distinct ways to win. Consider

```
Lizard
Spock
```

The dictionary entry for `Lizard` is `{Spock, Paper}`. Since `Spock` is present, the condition `second in wins[first]` is true and the result is `First`. This catches implementations that remember only one of Lizard's two winning relationships.

The third edge case is the reversed pair

```
Paper
Lizard
```

The entry for `Paper` is `{Rock, Spock}`, so `Lizard` is not present. The moves are not equal, so the algorithm reaches the final branch and prints `Second`. This confirms that the relation is directional and cannot be treated as an undirected connection.

The fourth edge case is Spock's less obvious interaction with Rock:

```
Spock
Rock
```

`Rock` appears in `wins["Spock"]`, so the algorithm prints `First`. Reversing the input to

```
Rock
Spock
```

makes the lookup fail, and the algorithm prints `Second`. These two inputs together verify that the direction of every relationship is being interpreted correctly.
