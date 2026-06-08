---
title: "CF 1919A - Wallet Exchange"
description: "Alice and Bob each start with a wallet containing some number of coins. On every turn, the current player may either keep the wallets as they are or swap the two wallets. After that choice, they must remove exactly one coin from the wallet they currently hold."
date: "2026-06-08T19:33:36+07:00"
tags: ["codeforces", "competitive-programming", "games", "math"]
categories: ["algorithms"]
codeforces_contest: 1919
codeforces_index: "A"
codeforces_contest_name: "Hello 2024"
rating: 800
weight: 1919
solve_time_s: 125
verified: true
draft: false
---

[CF 1919A - Wallet Exchange](https://codeforces.com/problemset/problem/1919/A)

**Rating:** 800  
**Tags:** games, math  
**Solve time:** 2m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

Alice and Bob each start with a wallet containing some number of coins. On every turn, the current player may either keep the wallets as they are or swap the two wallets. After that choice, they must remove exactly one coin from the wallet they currently hold.

A move is legal only if the wallet the player ends up holding contains at least one coin before removing the coin. The first player who cannot make a legal move loses.

For each test case, we are given the initial coin counts `a` and `b`. Both players play perfectly, and we must determine whether the winner is Alice, who moves first, or Bob.

The constraints are surprisingly large. Each wallet may contain up to `10^9` coins, and there can be up to `1000` test cases. Any approach that simulates the game move by move is immediately impossible. A single game could last roughly `a + b` turns, which may be about `2 · 10^9` moves. We need a direct mathematical characterization of winning and losing positions.

The tricky part is that the ability to swap wallets makes the game look more complicated than a simple pile-removal game. A common mistake is to focus on which player owns which wallet. Ownership changes constantly and is actually irrelevant. Another mistake is to assume the larger wallet always matters more. Small examples show that only the total number of coins ends up determining the winner.

Consider the position:

```
a = 1, b = 1
```

The total number of coins is 2. Alice removes one coin, Bob removes one coin, and then no coins remain. Alice is the next player and loses. The correct answer is `Bob`.

Now consider:

```
a = 1, b = 4
```

The total number of coins is 5. Since there are five removable coins in total, the game lasts exactly five moves. Alice makes moves 1, 3, and 5, so Bob is unable to move afterward. The correct answer is `Alice`.

A careless approach that tries to track wallet ownership may miss this much simpler pattern.

## Approaches

The most direct idea is to model the game state as `(a, b, turn)` and recursively determine whether each position is winning or losing. From every state, the current player has up to two choices: swap or do not swap. After the choice, one coin is removed from the current wallet.

For tiny values this works. We can enumerate all reachable positions and observe the game tree. The problem is that the state space grows with the wallet sizes. Since `a` and `b` may be as large as `10^9`, such a search is completely infeasible.

To find a pattern, examine what actually changes during a move.

Every legal move removes exactly one coin from the game. No move ever creates coins. Swapping only changes who currently holds which wallet. The total number of coins decreases by exactly one every turn.

Let

```
S = a + b
```

Initially there are `S` coins in total. Since each move removes exactly one coin, there can be exactly `S` moves before all coins disappear.

The crucial observation is that as long as at least one coin exists somewhere, the current player can always make a move. If their current wallet is empty, they simply swap and take the non-empty wallet. The only time a move is impossible is when both wallets contain zero coins.

That means the game length is completely fixed. It is exactly `S` moves, regardless of strategy.

Once the length is fixed, the game becomes trivial. Alice makes moves numbered

```
1, 3, 5, ...
```

and Bob makes moves numbered

```
2, 4, 6, ...
```

If `S` is odd, Alice performs the last move and Bob faces the empty position. Alice wins.

If `S` is even, Bob performs the last move and Alice faces the empty position. Bob wins.

The entire game reduces to checking the parity of `a + b`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in game length | Exponential | Too slow |
| Optimal | O(1) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Read `a` and `b`.
2. Compute the total number of coins:

```
S = a + b
```

Every move removes exactly one coin, so `S` is also the exact number of moves in the game.
3. Check whether `S` is odd or even.

If `S` is odd, Alice makes the final move and wins.

If `S` is even, Bob makes the final move and wins.
4. Output the corresponding winner.

### Why it works

The key invariant is that every legal move decreases the total number of coins by exactly one. No move can change this. Also, whenever at least one coin remains somewhere, the current player can obtain a non-empty wallet by swapping if necessary. Consequently, the game never ends early.

The game must continue until all `a + b` coins have been removed. Since the total number of moves is fixed and equals `a + b`, the winner is determined solely by the parity of that number. An odd number of moves means Alice takes the final move, while an even number means Bob takes the final move.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())

for _ in range(t):
    a, b = map(int, input().split())
    if (a + b) % 2:
        print("Alice")
    else:
        print("Bob")
```

The implementation follows the mathematical characterization directly.

For each test case we compute `a + b` and inspect its parity. No simulation is needed because strategy does not affect the game length. Every move always consumes exactly one coin, and the game always lasts until all coins are gone.

There are no overflow concerns in Python. Even the maximum possible sum,

```
10^9 + 10^9 = 2 · 10^9
```

fits comfortably within normal integer arithmetic.

The only subtle point is recognizing that swapping never changes the total number of future moves. Once that observation is made, the implementation becomes a one-line decision.

## Worked Examples

### Example 1

Input:

```
a = 1, b = 4
```

| Variable | Value |
| --- | --- |
| a | 1 |
| b | 4 |
| S = a + b | 5 |
| Parity of S | Odd |
| Winner | Alice |

There are exactly five coins in the game, so there will be exactly five moves. Alice takes moves 1, 3, and 5. Bob has no move after the fifth coin is removed.

### Example 2

Input:

```
a = 5, b = 3
```

| Variable | Value |
| --- | --- |
| a | 5 |
| b | 3 |
| S = a + b | 8 |
| Parity of S | Even |
| Winner | Bob |

There are exactly eight removable coins. The eighth move belongs to Bob, so Alice receives the empty position and loses.

These examples illustrate the central invariant: only the total number of coins matters, not how they are distributed between wallets.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) per test case | One addition and one parity check |
| Space | O(1) | Uses only a few variables |

With at most 1000 test cases, the total work is tiny. The solution easily fits within the 1-second time limit and 256 MB memory limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline
    t = int(input())
    ans = []
    for _ in range(t):
        a, b = map(int, input().split())
        ans.append("Alice" if (a + b) % 2 else "Bob")
    print("\n".join(ans))

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return out.getvalue()

# provided sample
assert run(
"""10
1 1
1 4
5 3
4 5
11 9
83 91
1032 9307
839204 7281
1000000000 1000000000
53110 2024
"""
) == (
"""Bob
Alice
Bob
Alice
Bob
Bob
Alice
Alice
Bob
Bob
"""
)

# minimum values
assert run(
"""1
1 1
"""
) == (
"""Bob
"""
), "minimum input"

# odd total
assert run(
"""1
2 3
"""
) == (
"""Alice
"""
), "odd total wins for Alice"

# even total
assert run(
"""1
7 9
"""
) == (
"""Bob
"""
), "even total wins for Bob"

# maximum values
assert run(
"""1
1000000000 1000000000
"""
) == (
"""Bob
"""
), "largest equal values"

# large odd sum
assert run(
"""1
1000000000 999999999
"""
) == (
"""Alice
"""
), "large odd total"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | `Bob` | Smallest legal case |
| `2 3` | `Alice` | Odd total number of coins |
| `7 9` | `Bob` | Even total number of coins |
| `1000000000 1000000000` | `Bob` | Maximum equal values |
| `1000000000 999999999` | `Alice` | Large odd sum near limits |

## Edge Cases

### Both wallets start with one coin

Input:

```
1
1 1
```

The total number of coins is:

```
1 + 1 = 2
```

Two moves occur in total. Bob makes the second move, leaving no coins. Alice has no legal move afterward.

Output:

```
Bob
```

### One wallet is much larger than the other

Input:

```
1
1 1000000000
```

The total number of coins is:

```
1000000001
```

which is odd. The distribution does not matter. The game lasts exactly `1000000001` moves, and Alice takes the final one.

Output:

```
Alice
```

### Equal large wallets

Input:

```
1
1000000000 1000000000
```

The total is:

```
2000000000
```

which is even. Bob always receives the last move.

Output:

```
Bob
```

### Current wallet becomes empty

Suppose at some point the state is:

```
(0, 5)
```

A player is not stuck. They can swap wallets, obtain the wallet containing five coins, and remove one coin. The game only ends when the state becomes:

```
(0, 0)
```

This is exactly why the total move count is fixed at `a + b`, making the parity argument valid.
