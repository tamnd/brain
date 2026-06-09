---
title: "CF 1719A - Chip Game"
description: "We have an $n times m$ board and a chip that starts in the lower-left corner. On each turn, a player chooses exactly one direction, either up or right, and moves the chip by any odd number of cells in that direction. The chip cannot leave the board."
date: "2026-06-09T19:33:38+07:00"
tags: ["codeforces", "competitive-programming", "games", "math"]
categories: ["algorithms"]
codeforces_contest: 1719
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 814 (Div. 2)"
rating: 800
weight: 1719
solve_time_s: 99
verified: true
draft: false
---

[CF 1719A - Chip Game](https://codeforces.com/problemset/problem/1719/A)

**Rating:** 800  
**Tags:** games, math  
**Solve time:** 1m 39s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an $n \times m$ board and a chip that starts in the lower-left corner. On each turn, a player chooses exactly one direction, either up or right, and moves the chip by any odd number of cells in that direction. The chip cannot leave the board.

The game ends when the chip reaches a position from which no legal move exists. Since players alternate turns and both play optimally, we need to determine whether the starting position is winning for the first player, Burenka, or losing for the first player, in which case Tonya wins.

The input consists of several independent game boards. For each board, we must print the winner assuming perfect play.

The constraints are the main clue that a mathematical solution exists. Both dimensions can be as large as $10^9$, which makes any approach that explores board states impossible. Even a single board contains up to $10^{18}$ cells, and there can be $10^4$ test cases. The solution must be reducible to a simple formula computed in constant time per test case.

A common mistake is to focus on the exact coordinates of the chip instead of the parity structure of the game.

Consider the board:

```
1 1
```

There are no cells above or to the right, so the first player has no move. The correct answer is:

```
Tonya
```

A careless implementation that assumes the first player always has at least one odd move would fail here.

Another tricky case is:

```
2 2
```

The only legal moves are one step up or one step right. Either move immediately gives the opponent the final move. The correct answer is:

```
Tonya
```

Many players initially guess that every board larger than $1 \times 1$ is winning, which is not true.

A final example is:

```
1 4
```

The first player can move three cells right and finish the game instantly. The correct answer is:

```
Burenka
```

Any approach based only on board size rather than parity would struggle to explain why $1 \times 4$ and $1 \times 3$ behave differently.

## Approaches

The most direct approach is to model every board position as a game state and compute whether it is winning or losing. Let a state represent the chip's current coordinates. A state is winning if there exists a move to a losing state, and losing if every legal move leads to winning states.

This recursion is correct because it follows the standard definition of impartial games. Unfortunately, it becomes infeasible almost immediately. Even for a modest $1000 \times 1000$ board there are one million states, and each state may have hundreds of outgoing moves. The actual constraints allow dimensions up to $10^9$, making state exploration completely impossible.

To find a pattern, compute a few small boards manually. Let $f(n,m)$ denote the game state when the chip starts at the lower-left corner of an $n \times m$ board.

The terminal position is $f(1,1)$, which is losing.

Now examine small values:

| Board | Result |
| --- | --- |
| 1×1 | L |
| 1×2 | W |
| 1×3 | L |
| 1×4 | W |
| 2×1 | W |
| 2×2 | L |
| 2×3 | W |
| 3×3 | L |

A clear pattern appears. Positions where $n$ and $m$ have the same parity are losing. Positions where their parities differ are winning.

Why does parity matter?

A move changes exactly one coordinate by an odd number. Adding an odd number always flips parity. So every move flips the parity of exactly one dimension.

Represent a state only by the parity pair:

$$(n \bmod 2,\; m \bmod 2)$$

The losing state $(1,1)$ corresponds to the terminal board $1 \times 1$.

If both dimensions have the same parity, every legal move changes exactly one parity bit, producing a state with different parities.

If the dimensions have different parities, there is always a move that makes them equal. Since moving by an odd amount flips one parity, we can choose a legal odd move that reduces one dimension appropriately and reaches a same-parity state.

Thus:

- Same parity $\rightarrow$ losing.
- Different parity $\rightarrow$ winning.

The entire game collapses to a parity check.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential / state-DP over board positions | O(nm) | Too slow |
| Optimal | O(1) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Read $n$ and $m$.
2. Compute the parity of both dimensions using $n \bmod 2$ and $m \bmod 2$.
3. If the parities are equal, print `"Tonya"`.

These positions are losing because every move flips exactly one parity and sends the game to a different-parity position.
4. Otherwise, print `"Burenka"`.

From a different-parity position, the first player can always make an odd move that creates equal parities, placing the opponent in a losing state.

### Why it works

The key invariant is that every legal move flips the parity of exactly one dimension. This means the game can be analyzed entirely through the parity pair $(n \bmod 2, m \bmod 2)$.

States with equal parities are losing because every move reaches a different-parity state. States with different parities are winning because there exists a move to an equal-parity state. Since every position belongs to exactly one of these two categories, the classification is complete and correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())

for _ in range(t):
    n, m = map(int, input().split())

    if (n & 1) == (m & 1):
        print("Tonya")
    else:
        print("Burenka")
```

The solution only needs the parity of the two dimensions. Using `n & 1` and `m & 1` is a compact way to compute whether each number is odd or even.

The comparison checks whether the parities match. Equal parity means a losing starting position, so Tonya wins. Different parity means a winning starting position, so Burenka wins.

No simulation is required, and there are no overflow concerns because only parity is used. The dimensions may be as large as $10^9$, but the computation remains constant time.

## Worked Examples

### Example 1

Input:

```
5 6
```

| n | m | n % 2 | m % 2 | Same Parity? | Winner |
| --- | --- | --- | --- | --- | --- |
| 5 | 6 | 1 | 0 | No | Burenka |

The dimensions have different parity. Burenka can move to a same-parity position and force a win.

### Example 2

Input:

```
2 2
```

| n | m | n % 2 | m % 2 | Same Parity? | Winner |
| --- | --- | --- | --- | --- | --- |
| 2 | 2 | 0 | 0 | Yes | Tonya |

Both dimensions are even. Every legal move changes exactly one parity and gives the opponent a winning position. The starting state is losing.

These examples illustrate the complete invariant: only parity matters, not the actual board size.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | One parity comparison per test case |
| Space | O(1) | No additional data structures are used |

Even with $10^4$ test cases, the solution performs only a few arithmetic operations per case. It easily fits within the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    t = int(input())
    ans = []

    for _ in range(t):
        n, m = map(int, input().split())
        ans.append("Tonya" if ((n & 1) == (m & 1)) else "Burenka")

    sys.stdout.write("\n".join(ans))

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out

# provided sample
assert run(
"""6
1 1
1 4
5 6
2 2
6 3
999999999 1000000000
"""
) == """Tonya
Burenka
Burenka
Tonya
Burenka
Burenka"""

# minimum board
assert run(
"""1
1 1
"""
) == "Tonya"

# odd-odd
assert run(
"""1
3 5
"""
) == "Tonya"

# even-even
assert run(
"""1
1000000000 1000000000
"""
) == "Tonya"

# parity mismatch
assert run(
"""1
1 2
"""
) == "Burenka"

# large boundary values
assert run(
"""1
999999999 1000000000
"""
) == "Burenka"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | `Tonya` | Terminal position |
| `3 5` | `Tonya` | Odd-odd parity |
| `1000000000 1000000000` | `Tonya` | Even-even parity with maximum values |
| `1 2` | `Burenka` | Smallest parity mismatch |
| `999999999 1000000000` | `Burenka` | Large mixed parity values |

## Edge Cases

### Single Cell Board

Input:

```
1
1 1
```

Execution:

| n | m | n % 2 | m % 2 | Result |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 1 | Tonya |

The parities are equal, so the algorithm outputs `Tonya`. This matches the game because the first player has no legal move.

### Small Even-Even Board

Input:

```
1
2 2
```

Execution:

| n | m | n % 2 | m % 2 | Result |
| --- | --- | --- | --- | --- |
| 2 | 2 | 0 | 0 | Tonya |

The algorithm identifies an equal-parity position and returns `Tonya`. Indeed, every move gives the opponent a winning response.

### Single Row Board

Input:

```
1
1 4
```

Execution:

| n | m | n % 2 | m % 2 | Result |
| --- | --- | --- | --- | --- |
| 1 | 4 | 1 | 0 | Burenka |

The parities differ, so the algorithm outputs `Burenka`. The first player can move three cells right and immediately leave the opponent without a move.

### Maximum Boundary Values

Input:

```
1
999999999 1000000000
```

Execution:

| n | m | n % 2 | m % 2 | Result |
| --- | --- | --- | --- | --- |
| 999999999 | 1000000000 | 1 | 0 | Burenka |

Only parity is examined, so extremely large dimensions are handled exactly the same as small ones. The algorithm still runs in constant time and correctly outputs `Burenka`.
