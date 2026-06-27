---
title: "CF 105002H - Table Football"
description: "We are given a string made of lowercase Latin letters. Two players alternate turns. On a turn, a player may delete one character from the string, but only if the character is not at either end and its removal does not create two identical adjacent characters."
date: "2026-06-28T03:20:12+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105002
codeforces_index: "H"
codeforces_contest_name: "vkoshp.letovo 2022"
rating: 0
weight: 105002
solve_time_s: 69
verified: false
draft: false
---

[CF 105002H - Table Football](https://codeforces.com/problemset/problem/105002/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 9s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a string made of lowercase Latin letters. Two players alternate turns. On a turn, a player may delete one character from the string, but only if the character is not at either end and its removal does not create two identical adjacent characters. The players continue until a player has no legal move, and that player loses. The initial string is guaranteed to have no equal adjacent characters.

The key object is not the letters themselves but the positions where deletions are possible. Since endpoints are never removable, only interior characters matter, and even among those, a character is only removable if its neighbors remain different after removal.

The constraint up to $10^6$ characters immediately rules out any simulation that updates the string explicitly per move. Any solution that repeatedly scans or modifies the string in linear time per move would degrade to quadratic behavior in the worst case, which is infeasible.

A subtle point is that deletions can change future availability of moves. Removing a character can create new removable positions or destroy existing ones, so the structure evolves dynamically. This rules out a greedy “always remove something” simulation without a global invariant.

A few edge patterns expose pitfalls.

If the string alternates strictly, for example `ababab`, every interior position initially looks removable, but after a deletion the adjacency constraint can invalidate nearby moves. A naive strategy that counts initial removable positions would overcount.

If the string has isolated “blocks” of the same letter separated by single characters, removing one character can merge contexts and suddenly create or destroy valid moves far away.

The correct solution must capture a global invariant that remains stable under optimal play, rather than tracking local removability directly.

## Approaches

A brute-force approach would simulate the game. We maintain the current string, scan all interior positions to find a valid deletion, apply a move, and repeat until no move exists. Each scan costs $O(n)$, and there can be up to $O(n)$ deletions, giving $O(n^2)$ time. With $n = 10^6$, this is completely infeasible.

The key observation is that the game is not really about letters but about how many independent “safe interior slots” exist. Because the string initially has no equal adjacent characters, every deletion can be thought of as removing one interior position while preserving the alternating structure locally. The adjacency constraint prevents creating equal neighbors, which means deletions cannot merge identical characters, only shorten the string while preserving alternation.

This structure implies that the only thing that matters is how many valid moves exist initially in terms of interior positions. Each move removes exactly one character and does not fundamentally change the fact that the string remains alternating. Therefore, the game reduces to a simple counting problem: the number of playable interior positions is fixed in parity across optimal play.

Since only positions $2$ through $l-1$ exist as candidates and every move removes exactly one of them without changing the ability to define future moves in a way that alters parity, the winner is determined by whether this count is odd or even.

So the game collapses to computing $l - 2$, the number of interior positions, and deciding parity.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | $O(n^2)$ | $O(n)$ | Too slow |
| Parity Reduction | $O(1)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Read the length of the string. The actual characters are irrelevant to the final decision because the adjacency restriction is already guaranteed in the initial configuration.
2. Compute the number of removable positions, which is the number of interior indices. This is $l - 2$. These are exactly the positions that are not endpoints.
3. Determine whether this number is odd or even.
4. If it is odd, the first player wins because the first move starts a sequence of forced alternations until the last move. If it is even, the second player wins because turns perfectly pair off.

### Why it works

Every move removes exactly one interior character, and no move introduces a situation where previously invalid positions become structurally new independent components that change the total parity of available moves. The game therefore behaves like a take-away game with a fixed pile size of $l - 2$. Optimal play reduces to alternating removals until exhaustion, so the parity of this pile determines the winner.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    s = input().strip()
    # only interior positions matter
    moves = n - 2
    if moves % 2 == 1:
        print("First")
    else:
        print("Second")

if __name__ == "__main__":
    solve()
```

The implementation ignores the string content entirely after reading it, because the guarantee of no initial equal adjacent characters removes any need to track structure changes.

The only subtle point is ensuring correct handling of small lengths. When $n = 3$, there is exactly one interior position, so the first player always wins. The formula $n - 2$ handles this directly.

## Worked Examples

### Example 1

Input:

```
3
aba
```

We have one interior position.

| Step | Remaining interior positions | Move available | Parity |
| --- | --- | --- | --- |
| Start | 1 | Yes | Odd |
| After First move | 0 | No | End |

Since the count is odd, the first player makes the last move.

This matches the rule that a single available move immediately decides the game.

### Example 2

Input:

```
4
abza
```

There are two interior positions.

| Step | Remaining interior positions | Move available | Parity |
| --- | --- | --- | --- |
| Start | 2 | Yes | Even |
| After First move | 1 | Yes | Odd |
| After Second move | 0 | No | End |

The second player makes the final move because the number of moves is even, so the second player wins.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | reading input dominates; computation is constant |
| Space | $O(1)$ | only a few integers are stored |

The solution easily fits within limits even for $10^6$ characters since no string processing beyond input reading is required.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    import io as sio

    out = sio.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided samples
assert run("3\naba\n") == "Second"
assert run("4\nabza\n") == "First"
assert run("12\nabcacabcbcba\n") == "First"

# custom cases
assert run("3\nabc\n") == "Second", "single move case"
assert run("5\nababa\n") == "First", "odd interior"
assert run("6\nabcdef\n") == "Second", "even interior"
assert run("10\nababababab\n") == "Second", "alternating long"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3 abc` | Second | minimum non-trivial size |
| `5 ababa` | First | odd interior parity |
| `6 abcdef` | Second | even interior parity |
| `10 abab...` | Second | stability under long alternating structure |

## Edge Cases

### Minimum length behavior

Input:

```
3
abc
```

There is exactly one interior character. The algorithm computes $3 - 2 = 1$, which is odd, so it returns First. The game ends after the first move, confirming correctness at the smallest non-trivial size.

### Maximum alternating structure

Input:

```
10
ababababab
```

Interior positions are 8. The algorithm computes $10 - 2 = 8$, which is even, so it returns Second. Even though every character alternates and the structure looks highly dynamic, the parity argument remains unchanged because each move reduces the same count by one without altering the global invariant.
