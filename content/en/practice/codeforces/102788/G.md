---
title: "CF 102788G - Alice And Bob"
description: "The game is played on a row of positive integers. Alice moves first. On a turn, a player chooses two neighboring numbers that have a common divisor greater than one. The chosen pair is simplified by dividing both numbers by their greatest common divisor."
date: "2026-08-03T15:12:20+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102788
codeforces_index: "G"
codeforces_contest_name: "2017-2018 ICPC Central Quarter Final of Northeastern European Regional Collegiate Programming Contest"
rating: 0
weight: 102788
solve_time_s: 106
verified: true
draft: false
---

[CF 102788G - Alice And Bob](https://codeforces.com/problemset/problem/102788/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 46s  
**Verified:** yes  

## Solution
## Problem Understanding

The game is played on a row of positive integers. Alice moves first. On a turn, a player chooses two neighboring numbers that have a common divisor greater than one. The chosen pair is simplified by dividing both numbers by their greatest common divisor. When no neighboring pair shares any divisor, the current player has no legal move and loses.

The task is not to find the final array itself, but only which player reaches the losing position. The input consists of the length of the row and the initial values in that row. The output is the name of the player who wins with optimal play.

The numbers can be as large as $10^9$, but there are only 50 of them. A direct game search is not possible because the order of moves creates many possible states. However, each operation strictly removes prime factors from the array. A number at most $10^9$ contains at most 29 prime factors with multiplicity, so the total number of possible removals is small. This suggests looking for a monotonic process instead of exploring all game states.

The key observation is that every move reduces the total amount of prime factor information in the array. More precisely, if a move divides two numbers by their gcd, every prime factor removed disappears from both numbers. No operation can ever introduce a new common divisor between neighbors. Because of this monotonic behavior, the game has no strategic branching effect on the parity of the number of moves. Any sequence of legal moves reaches the same terminal state after the same number of moves.

A common mistake is to think that choosing a different pair can change the winner. For example, with:

```
3
2 6 3
```

choosing the first pair gives `[1, 3, 3]`, and then one more move is possible. Choosing the second pair gives `[2, 2, 1]`, and again one more move is possible. Both paths require two moves, so Bob wins.

Another edge case is when all neighboring pairs are already coprime:

```
2
5 7
```

The answer is `Bob`, because Alice cannot make a move at all. A solution that assumes at least one operation exists would incorrectly count a move.

A final subtle case is when one operation removes several prime factors at once:

```
2
60 30
```

The gcd is 30, so the move directly creates `[2, 1]`. Counting only one common prime instead of the full gcd would overestimate the number of moves.

## Approaches

The brute-force approach is to treat every possible choice of adjacent numbers as a branch in a game tree. For each state, we recursively try every legal move and determine whether there exists a move that forces the opponent into a losing state. This is correct for impartial games, but it is completely impractical here. Even a small array can have many possible move orders, and the number of states grows exponentially.

The important structure is that the game does not actually require minimax. Every move only removes prime factors and never changes them into something else. If we look at the whole process as repeatedly applying reductions, the order of reductions does not affect the number of reductions needed until all adjacent pairs become coprime.

The brute-force works because it follows the definition of optimal play, but it fails because it explores many equivalent orders of the same reductions. The observation that the process is confluent lets us replace game search with a simple simulation. We can repeatedly apply any available move and only count how many moves happen. If the count is odd, Alice made the last move. If it is even, Bob made the last move.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | $O(n \cdot F)$ | $O(1)$ | Accepted |

Here $F$ is the maximum number of moves. Since every move removes at least one prime factor from two numbers and the total number of prime factors is small, $F$ is bounded.

## Algorithm Walkthrough

1. Store the array and repeatedly search for an adjacent pair whose gcd is greater than one. Such a pair represents a legal move because both numbers can be reduced.
2. When a legal pair is found, divide both numbers by their gcd and increase the move counter. The exact pair chosen does not matter because all valid choices lead to the same final move parity.
3. Continue until no adjacent pair has gcd greater than one. At this point the game has ended because the next player has no legal move.
4. If the number of moves is odd, print `Alice`. Otherwise print `Bob`.

Why it works:

The invariant behind the algorithm is that the array only loses prime factors. A move cannot create a new divisor relationship, so every legal operation is part of the same reduction process. Since the terminal position and the parity of the number of reductions are independent of the order of moves, counting any valid sequence gives the correct winner.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    moves = 0

    while True:
        changed = False

        for i in range(n - 1):
            g = math.gcd(a[i], a[i + 1])
            if g > 1:
                a[i] //= g
                a[i + 1] //= g
                moves += 1
                changed = True
                break

        if not changed:
            break

    print("Alice" if moves % 2 else "Bob")

if __name__ == "__main__":
    solve()
```

The loop searches for one available move at a time. We stop after the first successful reduction in each pass because the next state is all that matters, not which particular legal move was selected.

The gcd calculation uses Python's built-in Euclidean algorithm, which easily handles values up to $10^9$. Integer division is safe because the gcd always divides both selected numbers exactly.

The only possible implementation mistake is forgetting that a gcd of 1 is not a legal move. Dividing by 1 would create an infinite loop because the state would not change.

## Worked Examples

For the input:

```
3
2 4 2
```

| Step | Array | Chosen pair | GCD | Moves |
| --- | --- | --- | --- | --- |
| Start | [2, 4, 2] | [2,4] | 2 | 0 |
| 1 | [1, 2, 2] | [2,2] | 2 | 1 |
| 2 | [1,1,1] | none | - | 2 |

The game ends after two moves, so Alice cannot make the last move. Bob wins.

For the input:

```
4
3 9 6 18
```

| Step | Array | Chosen pair | GCD | Moves |
| --- | --- | --- | --- | --- |
| Start | [3,9,6,18] | [9,6] | 3 | 0 |
| 1 | [3,3,2,18] | [3,3] | 3 | 1 |
| 2 | [3,1,2,18] | [2,18] | 2 | 2 |
| 3 | [3,1,1,9] | none | - | 3 |

The number of moves is odd, so Alice makes the final move and wins.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \cdot F)$ | Each iteration scans the row, and $F$ is the number of reductions. |
| Space | $O(1)$ | Only the input array and counters are stored. |

The maximum number of reductions is small because every move permanently removes prime factors. With $n \le 50$ and values at most $10^9$, the simulation easily fits the limits.

## Test Cases

```python
import sys
import io
import math

def run(inp: str) -> str:
    data = inp.strip().split()
    n = int(data[0])
    a = list(map(int, data[1:]))

    moves = 0
    while True:
        ok = False
        for i in range(n - 1):
            g = math.gcd(a[i], a[i + 1])
            if g > 1:
                a[i] //= g
                a[i + 1] //= g
                moves += 1
                ok = True
                break
        if not ok:
            break

    return ("Alice" if moves % 2 else "Bob") + "\n"

assert run("3\n2 4 2\n") == "Bob\n", "sample 1"
assert run("4\n3 9 6 18\n") == "Alice\n", "sample 2"

assert run("2\n5 7\n") == "Bob\n", "no moves"
assert run("2\n60 30\n") == "Alice\n", "large gcd removal"
assert run("5\n2 2 2 2 2\n") == "Bob\n", "repeated equal values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `5 7` | Bob | Checks the initial losing position. |
| `60 30` | Alice | Checks removing a gcd with many prime factors at once. |
| `2 2 2 2 2` | Bob | Checks repeated reductions and parity handling. |

## Edge Cases

For the case:

```
2
5 7
```

the algorithm scans the only adjacent pair, finds gcd equal to 1, and performs no moves. The counter remains zero, so Bob wins.

For the case:

```
3
2 6 3
```

the algorithm may choose either adjacent pair. Choosing `[2,6]` creates `[1,3,3]`, and the next pass removes the gcd of the last pair. Choosing `[6,3]` creates `[2,2,1]`, followed by one more reduction. Both paths have the same parity, so the result is still Bob.

For the case:

```
2
60 30
```

the gcd is 30, not just one prime factor. The operation produces `[2,1]` immediately. The algorithm counts one move and correctly returns Alice.
