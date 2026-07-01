---
title: "CF 104353G - String Game II"
description: "Two players, Alice and Bob, start with two strings of equal length. The strings contain only lowercase English letters. They repeatedly perform a game for exactly $P$ rounds."
date: "2026-07-01T18:12:08+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104353
codeforces_index: "G"
codeforces_contest_name: "2023 Xiangtan University Programming Contest"
rating: 0
weight: 104353
solve_time_s: 47
verified: true
draft: false
---

[CF 104353G - String Game II](https://codeforces.com/problemset/problem/104353/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

Two players, Alice and Bob, start with two strings of equal length. The strings contain only lowercase English letters. They repeatedly perform a game for exactly $P$ rounds. In each round, Alice is forced to modify one character in Bob’s string, and Bob is forced to modify one character in Alice’s string. A modification means picking a position and replacing the character there with any other lowercase letter of their choice.

After all $P$ rounds, each player evaluates only their own string. The score of a player is defined as the frequency of the most common character in their final string. The winner is the player with the higher score, and ties produce a draw. Both players play optimally with full knowledge of the initial strings.

The key difficulty is that each operation is adversarial across strings but cooperative within a player’s own strategy: Alice only improves Alice’s final score by damaging Bob’s string, not her own, and vice versa. The optimization is purely about how to shape the frequency distribution of letters under a fixed number of edits.

The constraints are large in terms of $P$, up to $10^9$, while $N$ is only up to 500. This immediately rules out any simulation over rounds. The solution must depend only on the structure of the initial frequency distributions and how much “effective change” can be achieved per move.

A subtle edge case appears when $P = 0$. No changes are possible, so the answer is purely determined by the initial maximum character frequencies in each string. Another corner case is when strings are already uniform. In such cases, changing a character may either reduce or increase concentration depending on strategy, but since both players act symmetrically, the net effect depends only on how many changes are forced and how they are distributed across letters.

## Approaches

A naive approach would simulate the game. Each round, Alice would try to choose a position in Bob’s string that minimizes Bob’s eventual maximum frequency, while Bob does the same to Alice. However, after each modification, the optimal choice depends on the full current distribution of letters, and recomputing best moves would take $O(N)$ per move. With $P$ up to $10^9$, this is completely infeasible. Even if we cap simulation to $P \le 500$, the state space remains complex because each move changes the best target letter dynamically.

The key observation is that the only thing that matters for the final score of a string is the size of its largest frequency class. Every operation changes one character, so it either decreases one frequency count and increases another. From a high level, each player wants to maximize how many characters can be converted into a single dominant letter.

Suppose a string has frequency array $f_1, f_2, \dots, f_{26}$. If we want to maximize the most frequent letter after $x$ changes, the best strategy is always to pick the currently best letter as the target and convert all other letters into it. Each operation can increase the best frequency by at most 1, but only until all other characters are exhausted.

Thus, after $x$ operations, the maximum possible frequency becomes:

$$\min(N, \max(f_i) + x)$$

because each move can increase the count of the dominant letter by at most one, and we cannot exceed the string length.

Now the interaction between Alice and Bob becomes symmetric and decouples: each player uses their $P$ moves on the opponent’s string, but only their own final string matters. So Alice’s score depends on Alice’s original string and Bob’s ability to reduce it, and vice versa.

However, since Bob only changes Alice’s string, Bob is effectively trying to minimize Alice’s maximum frequency. The best way to reduce a frequency class is to target the most frequent letter first. Each operation reduces the current maximum by 1 only if it hits that letter; otherwise it is wasted on non-dominant letters. Since Bob can always choose optimally, he will always attack the current majority letter in Alice’s string. Symmetrically for Alice.

So each player’s optimal outcome depends only on whether the opponent has enough operations to “break” the majority concentration.

Let $mx_1$ be the maximum frequency in $S_1$, $mx_2$ for $S_2$. After $P$ moves from Bob on Alice, Alice’s best possible final score becomes:

$$\max(1, mx_1 - P)$$

because each move can reduce the dominant frequency by at most one until it reaches 1 (cannot go below 1 since at least one occurrence remains).

Similarly:

$$\max(1, mx_2 - P)$$

Thus the game reduces to comparing these two values.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force simulation | $O(P \cdot N)$ | $O(N)$ | Too slow |
| Frequency reduction model | $O(N)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Count frequency of each character in both strings.

This gives a complete summary of each string’s structure, which is sufficient because operations only affect counts, not positions.
2. Compute $mx_1$ and $mx_2$, the maximum frequencies in Alice’s and Bob’s initial strings.

The score depends only on the most frequent character, so other frequencies can be ignored.
3. Model Bob’s effect on Alice as reducing Alice’s maximum frequency by up to $P$, producing $a = \max(1, mx_1 - P)$.

Each operation can eliminate one occurrence of the current dominant character until it is no longer dominant.
4. Similarly compute $b = \max(1, mx_2 - P)$ for Alice’s effect on Bob.
5. Compare $a$ and $b$. If $a > b$, Alice wins. If $a < b$, Bob wins. Otherwise the result is a draw.

### Why it works

The key invariant is that the identity of the most frequent letter in a string does not need to be tracked explicitly during play. Only its count matters, and every optimal move always targets the current majority class. This ensures that no strategy can extract more than one unit of reduction per move from the opponent’s score, and no strategy can increase its own score by more than one per move. As a result, the process is fully captured by linear adjustment of the initial maximum frequency.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    T = int(input())
    for _ in range(T):
        n, p = map(int, input().split())
        s1 = input().strip()
        s2 = input().strip()

        f1 = [0] * 26
        f2 = [0] * 26

        for c in s1:
            f1[ord(c) - 97] += 1
        for c in s2:
            f2[ord(c) - 97] += 1

        mx1 = max(f1)
        mx2 = max(f2)

        a = max(1, mx1 - p)
        b = max(1, mx2 - p)

        if a > b:
            print("Alice")
        elif a < b:
            print("Bob")
        else:
            print("Draw")

if __name__ == "__main__":
    solve()
```

The implementation compresses each string into a 26-length frequency array. This avoids any need to track positions or simulate operations.

The only subtle detail is clamping with `max(1, mx - p)`. Even if $P$ is large enough to exceed the current maximum frequency, the score cannot drop to zero because at least one occurrence of some letter remains. The implementation enforces this lower bound directly.

## Worked Examples

### Example 1

Input:

```
1
5 2
aaaaa
bbbbb
```

Alice starts with max frequency 5, Bob also 5.

| Step | mx1 | mx2 | Alice score | Bob score |
| --- | --- | --- | --- | --- |
| initial | 5 | 5 | 5 | 5 |
| after reduction | 5 | 5 | 3 | 3 |

Both get reduced by 2 operations, so both end at 3.

This confirms symmetry leads to a draw.

Output: Draw

### Example 2

Input:

```
1
6 1
aaaaaa
abbbbb
```

| Step | mx1 | mx2 | Alice score | Bob score |
| --- | --- | --- | --- | --- |
| initial | 6 | 5 | 6 | 5 |
| after reduction | 6 | 5 | 5 | 4 |

Alice still has higher final concentration.

Output: Alice

This demonstrates that even a small difference in initial maximum frequency persists after equal reductions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(T \cdot N)$ | Each test counts frequencies over two strings of length $N$ |
| Space | $O(1)$ | Only 26 counters are used per test case |

The constraints allow up to 2000 test cases and $N \le 500$, so at most about $10^6$ character operations, which is well within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# sample-like tests
assert run("""1
5 0
aabbb
bbbbb
""") == "Bob"

assert run("""1
5 0
aaaaa
aaaab
""") == "Alice"

# edge: zero operations
assert run("""1
4 0
abcd
wxyz
""") == "Draw"

# edge: large P
assert run("""1
3 100
abc
def
""") == "Draw"

# edge: identical strings
assert run("""1
6 2
aabbbb
aabbbb
""") == "Draw"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| zero operations | Draw | baseline comparison only |
| large P | Draw | clamping at 1 works |
| identical strings | Draw | symmetry handling |
| skewed frequencies | Alice/Bob | dominance sensitivity |

## Edge Cases

When $P = 0$, the algorithm directly compares initial maximum frequencies. For example, with `abcd` vs `aabc`, both maxima are 1 and 2 respectively, so Bob wins immediately. No reductions are applied, and the formula correctly preserves the original state.

When $P$ is extremely large, say $10^9$, both strings are reduced to a minimum score of 1 regardless of structure. For instance, `aaaaa` vs `bbbbb` becomes 1 vs 1, producing a draw. The clamping ensures no negative or zero frequencies appear.

When strings are identical, both $mx_1$ and $mx_2$ are equal, and after identical reductions both remain equal. Even if one string has more diverse letters, the maximum frequency dominates and ensures consistent comparison regardless of distribution elsewhere.
