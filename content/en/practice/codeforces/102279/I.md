---
title: "CF 102279I - Imitater The Potato"
description: "We have N nonempty stacks, where stack i initially contains Ai cards. Two players alternate moves, with Lowie moving first. A move has exactly one of two forms."
date: "2026-08-16T19:30:31+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102279
codeforces_index: "I"
codeforces_contest_name: "HCW 19 Team Round (ICPC format)"
rating: 0
weight: 102279
solve_time_s: 390
verified: true
draft: false
---

[CF 102279I - Imitater The Potato](https://codeforces.com/problemset/problem/102279/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 6m 30s  
**Verified:** yes  

## Solution
## Problem Understanding

We have `N` nonempty stacks, where stack `i` initially contains `Ai` cards. Two players alternate moves, with Lowie moving first. A move has exactly one of two forms. The player can remove one card from a single nonempty stack, or, if every stack is nonempty, remove one card from every stack simultaneously. Whoever removes the final card wins.

The goal is not to simulate the game. We need to determine whether the initial position is winning for the first player, `lowie`, or losing for the first player, which means `imitater` can force the win.

The constraints are small enough for a linear scan but far too large for game-state enumeration. There can be 1000 stacks, and every stack can contain 1000 cards. A state is described by all stack sizes, so a direct dynamic programming approach could have an enormous number of states. Even with memoization, the number of possible configurations is proportional to the product of the possible values of all stacks, which is astronomical for 1000 stacks. The intended solution should inspect each stack only a constant number of times.

The key quantities are the parity of the total number of cards and, when the number of stacks is even, the parity of the smallest stack. The smallest stack matters because the all-stacks move is legal exactly while the minimum stack is positive.

There are several edge cases that easily break a solution based only on the total number of cards. For example, with

```
2
1 2
```

the total is `3`, which is odd, and Lowie wins. This is the first sample. A solution that considers only whether the number of stacks is even would miss this.

A more subtle case is

```
2
2 2
```

The total is even and the minimum is even, so the correct answer is `imitater`. If Lowie removes one card from either stack, the total becomes odd. If Lowie removes one card from both stacks, the position becomes `(1, 1)`, which is winning for the next player. Looking only at the total parity would incorrectly treat all even-total positions alike.

Another important case is

```
2
1 3
```

Here the total is `4`, but the minimum is odd. Lowie can remove one card from both stacks and reach `(0, 2)`. Only one stack remains, containing two cards, so Imitater loses because Lowie can take those two cards on successive turns. Thus this position is winning for Lowie even though its total is even.

## Approaches

A direct game-theoretic solution would recursively examine every legal move. From a position with `N` nonempty stacks, there can be up to `N` single-stack moves plus the all-stacks move. The recursion is correct because a position is winning exactly when it has at least one move to a losing position, while a position is losing when every legal move goes to a winning position.

The problem is the size of the state space. If stack `i` can contain any value from `0` through `Ai`, there can be up to

[
\prod_{i=1}^{N}(A_i+1)
]

different configurations. With the maximum values, that becomes `1001^1000` possible states. Even if every state were evaluated only once with memoization, examining up to `N+1` moves per state would give `O(N * product(Ai + 1))` work. Without memoization, the game tree is even larger.

The useful observation is that every move changes the total number of cards by a very predictable amount. A single-stack move decreases the total by `1`. An all-stacks move decreases it by `N`.

When `N` is odd, both possible moves change the parity of the total, because both `1` and `N` are odd. Since the terminal state has total `0`, which is even, the player who can move from an odd total to an even total has the winning parity. Consequently, for odd `N`, the initial position is winning exactly when the total is odd.

When `N` is even, the two moves behave differently. A single-stack move changes the parity of the total, while an all-stacks move subtracts an even number and preserves the total parity. This makes the minimum stack relevant, because repeatedly using the all-stacks move is possible only while the minimum remains positive.

For even `N`, the losing positions are exactly those with an even total and an even minimum stack. If the total is odd, Lowie can always move to an even-total losing position. If the total is even but the minimum is odd, Lowie can perform the all-stacks move, making the minimum even while preserving the total parity. If both total and minimum are odd, Lowie instead removes one card from a minimum stack, making both quantities even.

The resulting characterization is therefore simple: Lowie wins if the total is odd, or if `N` is even and the minimum stack is odd. In every other case Imitater wins. This characterization can also be proved directly by showing that every move from a losing position leads to a winning one, and every winning position has a move to a losing one.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(N * product(Ai + 1))` with memoization | `O(product(Ai + 1))` | Too slow |
| Optimal | `O(N)` | `O(1)` auxiliary | Accepted |

## Algorithm Walkthrough

1. Read all stack sizes and compute `sum`, the total number of cards, and `mn`, the smallest stack size. These are the only properties needed by the final decision.
2. If `sum` is odd, output `lowie`. A single-stack move always changes the total parity, and an all-stacks move also changes it when `N` is odd. More generally, when the total is odd, there is always a legal move that reaches a losing even-total position.
3. If `sum` is even and `N` is odd, output `imitater`. Every legal move changes the total from even to odd, so Lowie cannot move directly to another losing even-total position.
4. If `N` is even and `sum` is even, inspect `mn`. If `mn` is odd, output `lowie`, because Lowie can remove one card from every stack. The total stays even because `N` is even, while the minimum becomes even.
5. If `N` is even, `sum` is even, and `mn` is even, output `imitater`. Every single-stack move makes the total odd, while an all-stacks move makes the minimum odd. Both resulting positions are winning for the next player.

### Why it works

Consider the set of positions where the total number of cards is even and either `N` is odd or the minimum stack is even. We claim these are exactly the losing positions.

From such a position, a single-stack move makes the total odd, so the resulting position is winning. If `N` is odd, an all-stacks move also makes the total odd. If `N` is even, an all-stacks move preserves the even total but decreases the minimum by one, making it odd, which gives the next player a winning position.

Now consider every position outside this set. If the total is odd, Lowie can choose a single-stack move when `N` is odd, or choose the appropriate move based on the minimum when `N` is even, reaching a losing position. If the total is even, `N` must be even and the minimum must be odd. The all-stacks move then preserves the even total and makes the minimum even, producing a losing position. Thus every winning position has a move to a losing position, completing the proof.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))

total = sum(a)
mn = min(a)

if total % 2 == 1:
    print("lowie")
elif n % 2 == 1:
    print("imitater")
elif mn % 2 == 1:
    print("lowie")
else:
    print("imitater")
```

The input contains exactly one game, so no test-case loop is needed. We read the array once, then compute its total and minimum.

The first condition handles every odd-total position immediately. This is deliberately checked before the number of stacks because odd total is enough to make the position winning regardless of whether `N` is odd or even.

After the total is known to be even, an odd number of stacks makes the position losing. For even `N`, the answer depends on the minimum stack. An odd minimum gives Lowie the all-stacks move to a losing position, while an even minimum means Imitater can maintain the corresponding losing structure.

Python integers have arbitrary precision, so there is no overflow concern. In fact, the largest possible total is only `1000 * 1000 = 1,000,000`, which would also fit comfortably in a standard 32-bit integer.

## Worked Examples

### Sample 1

The input is:

```
2
1 2
```

The important values are:

| `N` | `sum` | `min` | Decision |
| --- | --- | --- | --- |
| 2 | 3 | 1 | `sum` is odd |
| 2 | 3 | 1 | `lowie` |

Lowie wins immediately by the parity characterization. One concrete winning move is to remove one card from the second stack, producing `(1, 1)`. Imitater must then move, and Lowie can take the last two cards in the resulting game. More directly, the odd total means Lowie can force the terminal even-total state to be reached after his move.

### Sample 2

The input is:

```
3
1 4 3
```

The values are:

| `N` | `sum` | `min` | Decision |
| --- | --- | --- | --- |
| 3 | 8 | 1 | `sum` is even |
| 3 | 8 | 1 | `N` is odd |
| 3 | 8 | 1 | `imitater` |

Since there are three stacks, every legal move removes an odd number of cards: either `1` card or `3` cards. Starting from an even total, Lowie necessarily gives Imitater an odd-total position. The odd-total player is the one with the advantage, so Imitater wins.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(N)` | The array is scanned to compute the sum and minimum. |
| Space | `O(N)` | The input array stores all `N` stack sizes. |

The maximum input contains only 1000 integers, so a single linear scan is easily within the one-second limit. The auxiliary game-theoretic computation after reading the array is constant time, and the memory usage is tiny compared with the 256 MB limit.

## Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline
    n = int(input())
    a = list(map(int, input().split()))

    total = sum(a)
    mn = min(a)

    if total % 2 == 1:
        return "lowie"
    elif n % 2 == 1:
        return "imitater"
    elif mn % 2 == 1:
        return "lowie"
    else:
        return "imitater"

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    try:
        return solve()
    finally:
        sys.stdin = old_stdin

# Provided samples
assert run("2\n1 2\n") == "lowie", "sample 1"
assert run("3\n1 4 3\n") == "imitater", "sample 2"

# Minimum-size input
assert run("1\n1\n") == "lowie", "single stack with one card"

# Single stack with even number of cards
assert run("1\n2\n") == "imitater", "single stack with two cards"

# Even N, even total, even minimum
assert run("2\n2 2\n") == "imitater", "even total and even minimum"

# Even N, even total, odd minimum
assert run("2\n1 3\n") == "lowie", "even total and odd minimum"

# All values equal, even N
assert run("4\n6 6 6 6\n") == "imitater", "all equal even stacks"

# All values equal, even N, odd minimum
assert run("4\n5 5 5 5\n") == "lowie", "all equal odd stacks"

# Maximum-size input
assert run("1000\n" + "1000 " * 999 + "1000\n") == "imitater", \
    "maximum N and Ai"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1` | `lowie` | Minimum possible input and the terminal parity pattern for one stack |
| `1 / 2` | `imitater` | Single-stack even-count boundary |
| `2 / 2 2` | `imitater` | Even `N`, even total, even minimum |
| `2 / 1 3` | `lowie` | Even `N`, even total, odd minimum |
| `4 / 6 6 6 6` | `imitater` | All stacks equal with even minimum |
| `4 / 5 5 5 5` | `lowie` | All stacks equal with odd minimum |
| `1000 / 1000 ... 1000` | `imitater` | Maximum input size and large values |

## Edge Cases

### One stack

For

```
1
2
```

we have `N = 1`, `sum = 2`, and `min = 2`. The total is even, so the algorithm reaches the `N` odd branch and returns `imitater`. With one stack, both legal move descriptions are effectively the same operation, removing one card, so an even number of cards is indeed losing.

For

```
1
1
```

the total is odd, so the first branch returns `lowie`. Lowie removes the only card and wins immediately.

### Even number of stacks with even total and even minimum

For

```
2
2 2
```

we have `sum = 4` and `min = 2`. The total is even, `N` is even, and the minimum is even, so the algorithm returns `imitater`.

A single-stack move produces either `(1, 2)` or `(2, 1)`, both with odd total. An all-stacks move produces `(1, 1)`, where the minimum is odd. Every possible move therefore gives the next player a winning position.

### Even number of stacks with even total and odd minimum

For

```
2
1 3
```

we have `sum = 4` and `min = 1`. The algorithm returns `lowie` because the minimum is odd.

Lowie uses the all-stacks move, producing `(0, 2)`. The all-stacks move is no longer legal because one stack is empty, leaving an ordinary one-stack game with two cards. Imitater must remove one card, and Lowie removes the final card.

This is the case that shows why total parity alone is insufficient when `N` is even.

### Odd number of stacks with even total

For

```
3
1 4 3
```

the total is `8`, which is even, and `N = 3` is odd. The algorithm returns `imitater`.

Every move removes either one card or three cards, both odd quantities. Thus every move flips the parity of the total. Since the starting total is even, Lowie cannot make the final move under optimal play.

### Maximum input

For 1000 stacks each containing 1000 cards, the total is `1,000,000`, which is even, and the minimum is `1000`, also even. Since `N` is even as well, the algorithm returns `imitater`.

Only one scan over the 1000 values is required. The game itself never needs to be simulated, which is exactly what makes the solution practical for the largest allowed input.
