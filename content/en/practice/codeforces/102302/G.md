---
title: "CF 102302G - Left Stack Game"
description: "We have three stacks arranged from left to right, containing a, b, and c rocks. On every turn, the current player chooses one nonempty stack and removes between 1 and m rocks."
date: "2026-08-13T07:44:08+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102302
codeforces_index: "G"
codeforces_contest_name: "2019 USP-ICMC"
rating: 0
weight: 102302
solve_time_s: 221
verified: true
draft: false
---

[CF 102302G - Left Stack Game](https://codeforces.com/problemset/problem/102302/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 41s  
**Verified:** yes  

## Solution
## Problem Understanding

We have three stacks arranged from left to right, containing `a`, `b`, and `c` rocks. On every turn, the current player chooses one nonempty stack and removes between `1` and `m` rocks. The only restriction is on removing the final rock of a stack: a stack may become empty only when every stack to its left is already empty.

The first stack has no stack to its left, so it can always be emptied. The second stack can be emptied only after the first one has disappeared, and the third stack can be emptied only after both earlier stacks have disappeared. A player who removes the final rock from the whole position wins, so this is a normal-play impartial game. We need to determine whether the initial position is winning for Tomaz or losing for Tomaz under optimal play.

All four input values can reach (10^{18}). That immediately rules out any dynamic programming over the number of rocks, and even a simulation proportional to the number of turns is impossible. The solution has to depend only on arithmetic properties such as residues modulo `m + 1`, with constant or logarithmic running time.

There are two boundary effects that are easy to mishandle. First, a later stack cannot be emptied while an earlier stack is nonempty. For example, with `m = 1` and input `1 1 2`, Tomaz cannot remove the single rock from the second stack on the first move, because the first stack still contains one rock. A solution treating the three stacks as independent subtraction games gets the game state wrong.

The second edge case is that the first stack can always be emptied. With `m = 3` and input `3 1 1 1`, Tomaz removes the only rock from the first stack, Danftito is then forced into the second stack, and Tomaz takes the last rock from the third stack. The correct answer is `Tomaz`. A solution that applies the "cannot empty while something is on the left" restriction to the first stack would incorrectly reject the winning first move.

A third subtle case occurs when a stack is small enough to be emptied in one move. For example, with `m = 3`, a stack containing `1`, `2`, or `3` rocks has a direct move to zero, while a stack containing `4` does not. The optimal formula consequently has a separate treatment for values at most `m`.

## Approaches

A direct recursive solution follows the definition of the game. From a state `(a,b,c)`, try every legal number of rocks to remove from each stack, recursively determine whether the resulting position is winning, and declare the current position winning if at least one move reaches a losing position. This is correct because every move strictly decreases the total number of rocks, so the game graph is finite.

The problem is the number of states and moves. A state can have up to `3m` legal moves, and a game can contain up to `a + b + c` turns. With values as large as (10^{18}), even a hypothetical linear traversal would already be far beyond the limit. The recursive game tree is exponentially worse.

The key observation is that while a stack cannot yet be emptied, subtracting one rock from it is equivalent to playing an ordinary subtraction game on one fewer rock. For a single subtraction game where we may remove `1` through `m` rocks, the Grundy value of a pile of size `x` is `x mod (m + 1)`. Thus, while a stack is locked by a nonempty stack on its left, a pile of `x` rocks behaves like a subtraction pile of size `x - 1`, giving Grundy value `(x - 1) mod (m + 1)`.

This turns the right-hand locked stacks into an ordinary Nim position. The only special event is when the leftmost currently active stack is small enough to be emptied in one move. At that point the game changes from the locked version of the suffix to the fully unlocked version of the suffix. Since there are only three stacks, we can handle this transition explicitly.

The same reasoning can first solve the two-stack game and then use that result as the suffix state for the three-stack game. For a sufficiently large first stack, it cannot be emptied in one move, so the current game is simply the XOR of the first stack's subtraction-game value and the locked suffix value. For a small first stack, a zeroing move is available, and the outcome alternates according to the parity of that first stack, depending on whether the unlocked suffix is winning or losing.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in `a+b+c` | Exponential in `a+b+c` with memoization | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Let `k = m + 1`. A normal subtraction game in which one may remove `1` through `m` rocks has Grundy value `x mod k`.
2. First solve the two-stack position `(b,c)`, because it will be the unlocked suffix of the original three-stack game.
3. While `b` is nonempty, stack `c` cannot be emptied. Its locked value is therefore `(c - 1) mod k`. If `b > m`, stack `b` also cannot be emptied in one move, so the two stacks behave as independent subtraction games with values `b mod k` and `(c - 1) mod k`. The position is losing exactly when their XOR is zero.
4. If `b <= m`, stack `b` can be emptied immediately. If `(c - 1) mod k` is nonzero, the locked suffix has a nonzero Nim value, so the current position is winning because the player can modify the suffix to a zero Nim value.
5. The remaining two-stack case has `(c - 1) mod k = 0`. The locked suffix is then a losing position. Emptying `b` moves directly to the ordinary one-stack game `(c)`. That one-stack position is losing exactly when `c mod k = 0`.
6. Consequently, when `b <= m` and `(c - 1) mod k = 0`, the two-stack position alternates with the parity of `b`. If `(c mod k) != 0`, the unlocked suffix is winning, so odd `b` gives a losing position. If `(c mod k) == 0`, the unlocked suffix is losing, so even `b` gives a losing position.
7. Now compute the locked Grundy value of the original suffix `(b,c)`:
`locked = ((b - 1) mod k) XOR ((c - 1) mod k)`.
This is valid because neither `b` nor `c` may be emptied while `a` is positive.
8. If `a > m`, the first stack cannot be emptied in one move. The whole position is consequently an ordinary disjoint sum of the subtraction game on `a` and the locked suffix. Tomaz wins exactly when
`a mod k XOR locked != 0`.
9. If `a <= m` and `locked != 0`, Tomaz can make a winning move inside the locked suffix, so the position is winning.
10. If `a <= m` and `locked == 0`, every move that changes `b` or `c` goes to a winning position. The only remaining question is what happens when the first stack is reduced to zero. That move reaches the already computed two-stack position `(b,c)`. If that suffix is winning, the states with `a = 1,2,3,...` alternate starting with a losing state at odd `a`. If the suffix is losing, they alternate starting with a losing state at even `a`.

### Why it works

The invariant is that a stack which is forbidden from becoming empty behaves exactly like a subtraction game after removing one conceptual rock from it. Its legal values are `x -> x-d` for `1 <= d <= min(m,x-1)`, which is precisely the ordinary subtraction game on `x-1` rocks. Thus the locked suffix has a standard Nim value obtained by XORing these shifted residues.

The only move not represented by this locked Nim model is the move that empties the current leftmost stack. Such a move changes the rules of the suffix, because the next stack becomes unlockable. For two stacks we compute this unlocked suffix directly, then use it as the terminal outcome of the first stack. Since a small first stack can move to every smaller positive size and can also move to zero, its winning and losing states alternate by parity. For a large first stack, zero is unreachable in one move, so the ordinary XOR characterization applies. These cases cover every legal move, giving exactly the correct outcome.

## Python Solution

```python
import sys
input = sys.stdin.readline

def two_stack_wins(m, b, c):
    k = m + 1

    # While b > 0, c cannot be emptied.
    locked_c = (c - 1) % k

    if b > m:
        return ((b % k) ^ locked_c) != 0

    # b can be emptied immediately.
    if locked_c != 0:
        return True

    # If b is emptied, the remaining game is a normal
    # one-stack subtraction game on c.
    suffix_wins = (c % k) != 0

    # With locked suffix of Grundy value 0, outcomes alternate
    # as b goes through 1, 2, ..., m.
    if suffix_wins:
        # Losing for odd b.
        return (b % 2) == 0
    else:
        # Losing for even b.
        return (b % 2) == 1

def solve():
    m, a, b, c = map(int, input().split())
    k = m + 1

    # Outcome of the suffix after the first stack has been emptied.
    suffix_wins = two_stack_wins(m, b, c)

    # While a > 0, both later stacks are locked against becoming empty.
    locked = ((b - 1) % k) ^ ((c - 1) % k)

    if a > m:
        # The first stack cannot reach zero in one move, so the
        # position is an ordinary disjoint sum.
        first_value = a % k
        wins = (first_value ^ locked) != 0
    else:
        if locked != 0:
            wins = True
        else:
            # locked suffix is a P-position. The only exceptional
            # transition is a -> 0, which reaches the unlocked suffix.
            if suffix_wins:
                # P for odd a.
                wins = (a % 2) == 0
            else:
                # P for even a.
                wins = (a % 2) == 1

    print("Tomaz" if wins else "Danftito")

if __name__ == "__main__":
    solve()
```

The `two_stack_wins` function implements the recursive suffix analysis from the walkthrough. The expression `(c - 1) % k` is the shifted subtraction-game value of `c` while stack `b` is still nonempty.

When `b > m`, the second stack cannot be emptied in one move, so no special transition is reachable. The state is just the XOR of the two locked subtraction games. When `b <= m`, the zeroing transition has to be handled separately.

The main function applies exactly the same idea one level earlier. The value `locked` is the XOR of the shifted values of `b` and `c`. If `a > m`, zero cannot be reached from the first stack, so the ordinary XOR test is sufficient. If `a <= m`, the zeroing transition exists, and the outcome depends on the already computed unlocked suffix.

Python integers have arbitrary precision, so the (10^{18}) bounds require no special overflow handling. The expression `m + 1` is also safe, and modulo operations are performed before the XOR comparisons.

## Worked Examples

### Sample 1

The input is:

```
3 1 1 1
```

Here `m = 3`, so `k = 4`.

| Variable | Value |
| --- | --- |
| `m` | 3 |
| `k` | 4 |
| `a` | 1 |
| `b` | 1 |
| `c` | 1 |
| `(b-1)%k` | 0 |
| `(c-1)%k` | 0 |
| `locked` | 0 |

For the two-stack suffix `(1,1)`, stack `b` is small and the locked value of `c` is zero. Emptying `b` leaves a one-stack game with `c = 1`, which is winning. Thus the two-stack suffix itself is losing.

The original `a = 1` is also small and `locked = 0`. Since the suffix is losing, odd `a` gives a winning position.

The output is:

```
Tomaz
```

The actual winning play is exactly the intuitive sequence: Tomaz empties the first stack, Danftito empties the second, and Tomaz empties the third.

### Custom trace

Consider:

```
1 2 1 1
```

Here `m = 1`, so `k = 2`.

| Variable | Value |
| --- | --- |
| `m` | 1 |
| `k` | 2 |
| `a` | 2 |
| `b` | 1 |
| `c` | 1 |
| `(b-1)%k` | 0 |
| `(c-1)%k` | 0 |
| `locked` | 0 |
| `a%k` | 0 |
| Final result | P |

Since `a = 2 > m`, the first stack cannot be emptied in one move. The locked suffix has value zero, and the first stack has value `2 % 2 = 0`. Their XOR is zero, so the position is losing.

Tomaz can only remove one rock from the first stack, leaving `(1,1,1)`, which is winning for Danftito. This confirms the large-stack XOR case.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | A constant number of modulo, XOR, comparison, and parity operations is performed. |
| Space | O(1) | Only a fixed number of integer variables is stored. |

The input values may be as large as (10^{18}), but the algorithm never iterates over their magnitude. It reduces every relevant stack to a residue modulo `m + 1` and checks a constant number of cases, so it easily fits the 1 second time limit and 256 MB memory limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve_case(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        m, a, b, c = map(int, input().split())
        k = m + 1

        def two_stack_wins(m, b, c):
            k = m + 1
            locked_c = (c - 1) % k

            if b > m:
                return ((b % k) ^ locked_c) != 0

            if locked_c != 0:
                return True

            suffix_wins = (c % k) != 0

            if suffix_wins:
                return (b % 2) == 0
            return (b % 2) == 1

        suffix_wins = two_stack_wins(m, b, c)
        locked = ((b - 1) % k) ^ ((c - 1) % k)

        if a > m:
            wins = ((a % k) ^ locked) != 0
        else:
            if locked != 0:
                wins = True
            elif suffix_wins:
                wins = (a % 2) == 0
            else:
                wins = (a % 2) == 1

        print("Tomaz" if wins else "Danftito")
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided sample
assert solve_case("3 1 1 1\n") == "Tomaz\n", "sample 1"

# Minimum-size parameters, same state as the sample with m = 1.
assert solve_case("1 1 1 1\n") == "Tomaz\n", "minimum values"

# Large first stack whose residue makes the whole position losing.
assert solve_case("1 2 1 1\n") == "Danftito\n", "large-stack XOR boundary"

# All stacks equal, with a modulus boundary.
assert solve_case("3 4 4 4\n") == "Danftito\n", "all equal"

# Maximum-size values, exercising arbitrary-precision arithmetic.
assert solve_case(
    "1000000000000000000 1000000000000000000 "
    "1000000000000000000 1000000000000000000\n"
) == "Tomaz\n", "maximum-size values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3 1 1 1` | `Tomaz` | Provided sample and small-stack unlocking |
| `1 1 1 1` | `Tomaz` | Minimum `m` and minimum stack sizes |
| `1 2 1 1` | `Danftito` | Large first stack and zero XOR boundary |
| `3 4 4 4` | `Danftito` | Equal stacks and values exactly at `m+1` |
| `10^18 10^18 10^18 10^18` | `Tomaz` | Maximum input magnitude and Python integer handling |

## Edge Cases

The first important edge case is that the first stack may always be emptied. For `3 1 1 1`, `a = 1 <= m`, so Tomaz can move directly to `(0,1,1)`. The two-stack suffix `(1,1)` is losing because Danftito must empty the second stack, after which Tomaz takes the final rock. The algorithm computes `locked = 0`, finds the suffix losing, and uses odd `a` to classify the original state as winning.

The second edge case is a later stack that cannot be emptied yet. Consider `1 1 2 1`. Here `k = 2`, and the locked value of the suffix is `((2-1) mod 2) XOR ((1-1) mod 2) = 1`. Because the locked value is nonzero, the current position is immediately winning. The player can play inside the locked suffix without illegally emptying the second stack. Treating `b` as an ordinary heap would miss this restriction.

The third edge case is a first stack larger than `m`. For `1 2 1 1`, the first stack contains two rocks while only one may be removed per move, so it cannot reach zero immediately. The locked suffix has value zero and `a mod 2 = 0`, giving total XOR zero. Tomaz has no move to a losing state, so the answer is `Danftito`. This is exactly the situation where the ordinary Nim decomposition becomes valid again.

The final edge case is a stack exactly at a modulus boundary. With `m = 3`, a pile of `4` has subtraction-game value `4 mod 4 = 0`, while a locked pile of `4` has value `(4-1) mod 4 = 3`. Confusing these two expressions is a classic off-by-one error. The algorithm uses `x % (m+1)` only for a stack that may be emptied, and `(x-1) % (m+1)` for a stack whose emptying is currently forbidden, matching the actual legal moves in each phase.
