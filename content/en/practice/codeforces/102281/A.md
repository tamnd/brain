---
title: "CF 102281A - \u041f\u0440\u043e\u0441\u0442\u0430\u044f \u0437\u0430\u0434\u0430\u0447\u0430"
description: "We have a single pile of n cookies. Two players remove cookies alternately, with Professor X moving first. A legal move removes p^k cookies, where p is prime and k is a nonnegative integer. Since k = 0 is allowed, removing exactly 1 cookie is always legal."
date: "2026-08-13T09:18:30+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102281
codeforces_index: "A"
codeforces_contest_name: "2011, IV \u0421\u0430\u043c\u0430\u0440\u0441\u043a\u0430\u044f \u043e\u0431\u043b\u0430\u0441\u0442\u043d\u0430\u044f \u043c\u0435\u0436\u0432\u0443\u0437\u043e\u0432\u0441\u043a\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e"
rating: 0
weight: 102281
solve_time_s: 76
verified: true
draft: false
---

[CF 102281A - \u041f\u0440\u043e\u0441\u0442\u0430\u044f \u0437\u0430\u0434\u0430\u0447\u0430](https://codeforces.com/problemset/problem/102281/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 16s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a single pile of `n` cookies. Two players remove cookies alternately, with Professor X moving first. A legal move removes `p^k` cookies, where `p` is prime and `k` is a nonnegative integer. Since `k = 0` is allowed, removing exactly `1` cookie is always legal. The player who removes the last cookie wins.

The task is to determine which professor wins under optimal play. If X wins, we also need to output one legal first move that leaves Professor Y in a losing position.

The input contains one integer `n`, the initial number of cookies, with `1 <= n <= 10^9`. A dynamic programming solution over all positions would already require working with up to one billion states, which is far beyond the available time and memory. Even an optimized sieve or prime generation does not address the real issue, because the game itself has a much simpler structure. The winning strategy can be determined using only `n mod 6`.

There are several small cases where an implementation based on an incomplete list of moves can fail. For `n = 1`, X can remove `1 = 2^0`, so the correct output is `X WINS` followed by `1`. A solution that treats the exponent as positive would incorrectly claim that X has no move.

For `n = 4`, X wins by removing `4 = 2^2`, leaving zero cookies. Thus the correct output is `X WINS` followed by `4`. This catches implementations that only generate prime numbers and forget higher prime powers.

For `n = 6`, the correct output is `Y WINS`. The tempting move `2` leaves `4`, but `4` is itself winning for the next player. In fact every legal move from `6` leaves a non-multiple of `6`, and every non-multiple of `6` is winning.

For `n = 12`, the correct output is again `Y WINS`. The same argument applies because `12` is divisible by `6`. A careless implementation that only checks whether `n` itself is a legal move, rather than analyzing the resulting position, can get this case wrong.

## Approaches

A direct game solver would classify every position from `0` through `n`. Position `0` is losing because the player to move has no cookies. For each positive position, we would try every prime power not exceeding that position. The position is winning if at least one move reaches a losing position, and losing if every legal move reaches a winning position.

This recurrence is correct because the game is finite. Once a move is made, the number of cookies strictly decreases, so positions can be classified from smaller values to larger values. The problem is its size. Even considering only prime moves, there are `50,847,534` primes not exceeding `10^9`. A naive DP has up to one billion states, and checking many legal moves for each state leads to an enormous number of operations, far outside a 1.5 second limit. Adding prime powers does not improve the situation.

The brute force works because the game graph is acyclic, but it fails because it treats all positions as unrelated. The key observation is that the legal moves interact perfectly with residues modulo `6`.

Every legal move is a prime power. None of these numbers is divisible by `6`, because a prime power has only one prime divisor. Now consider a position divisible by `6`. Subtracting any legal move produces a number that is not divisible by `6`. Conversely, every nonzero residue modulo `6` can be removed directly by one of the five small legal moves:

`1` is `p^0`, `2` and `3` are prime, `4 = 2^2`, and `5` is prime.

Suppose `n` has residue `1` modulo `6`. Removing `1` reaches a multiple of `6`. For residue `2`, remove `2`; for residue `3`, remove `3`; for residue `4`, remove `4`; and for residue `5`, remove `5`. Thus every non-multiple of `6` has a move to a multiple of `6`.

This gives the complete characterization. Exactly the positive multiples of `6` are losing positions. From a multiple of `6`, every legal move goes to a non-multiple of `6`, which is winning. From every non-multiple of `6`, one of `1, 2, 3, 4, 5` reaches a multiple of `6`, giving the current player a winning move.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force DP | At least O(n * pi(n)) | O(n) | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the initial number of cookies `n`. Only its remainder modulo `6` matters, because the losing positions are exactly the positive multiples of `6`.
2. Compute `r = n % 6`. If `r == 0`, output `Y WINS`. There is no winning first move for X because every legal move has a nonzero residue modulo `6`, so the resulting pile is not divisible by `6`.
3. If `r != 0`, output `X WINS` and choose `r` as X's first move. The value `r` is always legal: `1` is a zero-th power of any prime, `2` and `3` are primes, `4` is `2^2`, and `5` is prime.
4. After removing `r`, the remaining number is `n - r`, which is divisible by `6`. Professor Y is consequently in a losing position. Whatever legal move Y makes, the resulting number is not divisible by `6`, so X can again move back to a multiple of `6`. Repeating this strategy eventually leaves zero cookies for X to take.

### Why it works

The invariant is that X can always return the game to a multiple of `6` after Y's move. A multiple of `6` cannot move to another multiple of `6`, because no legal move is divisible by `6`. On the other hand, from every non-multiple of `6`, X can remove its residue modulo `6`, and that residue is always one of the legal moves `1, 2, 3, 4, 5`. Thus multiples of `6` are exactly the losing positions, and the algorithm both identifies the winner and supplies a winning first move.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())

    move = n % 6

    if move == 0:
        print("Y WINS")
    else:
        print("X WINS")
        print(move)

if __name__ == "__main__":
    solve()
```

The program reads the only input value and computes its remainder modulo `6`. There is no need to generate primes, because the only moves we ever explicitly choose are the five smallest relevant prime powers.

When the remainder is zero, the position is losing, so only the first output line is printed. When the remainder is nonzero, that remainder itself is a legal move and is printed on the second line.

The boundary `n = 1` works automatically: `1 % 6 = 1`, so X removes one cookie. There are no overflow concerns in Python, and even in a fixed-width language all values involved are at most `10^9`.

The order of operations also matters conceptually. We must test `n % 6` before choosing a move. A remainder of zero means there is no move that preserves divisibility by `6`, while a nonzero remainder gives exactly the move needed to reach the losing class.

## Worked Examples

The first official sample has `n = 10`.

| `n` | `n % 6` | Decision | First move |
| --- | --- | --- | --- |
| 10 | 4 | X wins | 4 |
| 6 | 0 | Y is losing |  |

After X removes `4`, six cookies remain. The number `6` is divisible by `6`, so it is a losing position for the player whose turn it is. This gives the required output `X WINS` followed by `4`. The example also shows why the winning move does not have to be a prime, because `4 = 2^2` is a legal prime power.

The second official sample has `n = 12`.

| `n` | `n % 6` | Decision | First move |
| --- | --- | --- | --- |
| 12 | 0 | Y wins | none |

Twelve cookies are already a multiple of `6`. Every legal move removes a number not divisible by `6`, so every move available to X gives Y a winning position. Hence the output is simply `Y WINS`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | One modulo operation and constant-size output |
| Space | O(1) | Only a few integer variables are stored |

The input can be as large as `10^9`, but the algorithm never iterates up to `n` and never constructs the set of prime powers. Its running time and memory usage are constant, so it is comfortably within the 1.5 second and 128 MB limits.

## Test Cases

```python
import sys
import io

def solve():
    n = int(input())
    move = n % 6

    if move == 0:
        print("Y WINS")
    else:
        print("X WINS")
        print(move)

def run(inp: str) -> str:
    global input

    old_stdin = sys.stdin
    old_input = input

    try:
        sys.stdin = io.StringIO(inp)
        input = sys.stdin.readline

        old_stdout = sys.stdout
        sys.stdout = io.StringIO()

        solve()
        result = sys.stdout.getvalue()

        sys.stdout = old_stdout
        return result
    finally:
        sys.stdin = old_stdin
        input = old_input

# Provided samples
assert run("10\n") == "X WINS\n4\n", "sample 1"
assert run("12\n") == "Y WINS\n", "sample 2"

# Minimum-size input
assert run("1\n") == "X WINS\n1\n", "minimum n"

# Small losing position
assert run("6\n") == "Y WINS\n", "first positive multiple of 6"

# Maximum-size input
assert run("1000000000\n") == "X WINS\n4\n", "maximum n"

# Boundary immediately before a multiple of 6
assert run("11\n") == "X WINS\n5\n", "residue 5"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `X WINS` / `1` | Minimum input and the zero-th power move |
| `6` | `Y WINS` | First positive losing position |
| `1000000000` | `X WINS` / `4` | Maximum input and residue `4` |
| `11` | `X WINS` / `5` | Boundary immediately before a multiple of `6` |

## Edge Cases

For `n = 1`, the algorithm computes `1 % 6 = 1`. It selects move `1`, which is legal because `1 = 2^0`, and the remaining pile is zero. The output is `X WINS` followed by `1`.

For `n = 4`, the remainder is `4`. The algorithm chooses move `4`, and `4` is legal because `4 = 2^2`. The pile becomes zero immediately, so X wins. This case verifies that the move set contains prime powers beyond the primes themselves.

For `n = 6`, the remainder is zero, so the algorithm reports `Y WINS`. If X removes `1`, `2`, `3`, `4`, or `5`, the remaining pile is respectively `5`, `4`, `3`, `2`, or `1`, all non-multiples of `6`. Each of those positions lets the next player remove the corresponding residue and return to a multiple of `6`.

For `n = 12`, exactly the same argument applies. Every legal move leaves one of the residues `1, 2, 3, 4, 5` modulo `6`, so X cannot move to another losing position. Y can always answer by removing that residue and restore divisibility by `6`.

For the maximum value `n = 1,000,000,000`, the remainder is `4`, so the program outputs `X WINS` and `4`. The resulting pile contains `999,999,996` cookies, which is divisible by `6`. The magnitude of `n` has no effect on the number of operations performed.
