---
title: "CF 105833A - Anti-Diagonal Game"
description: "We have a string S of length N + 1, where each position on the anti-diagonal of a grid is labeled either A or B. A token starts at (0, 0) in an (N + 1) × (N + 1) grid. Players alternate moves, and each move increases either the row index or the column index by one."
date: "2026-06-26T03:55:34+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105833
codeforces_index: "A"
codeforces_contest_name: "NUS CS3233 Final Team Contest 2025"
rating: 0
weight: 105833
solve_time_s: 52
verified: true
draft: false
---

[CF 105833A - Anti-Diagonal Game](https://codeforces.com/problemset/problem/105833/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 52s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a string `S` of length `N + 1`, where each position on the anti-diagonal of a grid is labeled either `A` or `B`.

A token starts at `(0, 0)` in an `(N + 1) × (N + 1)` grid. Players alternate moves, and each move increases either the row index or the column index by one. The game stops as soon as the token reaches a cell `(i, j)` with `i + j = N`.

The anti-diagonal cell `(i, N - i)` corresponds to character `S[i]`.

If that character is `A`, Alice wins. If it is `B`, Bob wins.

Alice moves first and both players play optimally. The task is not to solve a single game instance. Instead, among all `2^(N+1)` possible strings `S`, we must count how many make Alice the winner. The answer is required modulo `10^9 + 3233`.

The key constraint is `N ≤ 100000`. Any solution that examines all strings is impossible. Even a dynamic program over the entire game graph would be unnecessary. The intended solution is a closed-form counting argument, leading to logarithmic time because only a modular exponentiation is needed.

A common mistake is to think that every character of the string matters. In reality, optimal play collapses the game to only two central positions when `N` is odd, and only three central positions when `N` is even. The rest of the string is completely irrelevant.

For example, with `N = 1`, the string has length `2`.

```
AA
AB
BA
BB
```

Alice can choose either anti-diagonal endpoint directly. She wins in the first three cases and loses only for `BB`.

For `N = 2`, only the triple `(S0,S1,S2)` matters. The winning strings are:

```
AAA
AAB
BAA
```

which matches the sample answer `3`.

## Approaches

A brute-force approach would enumerate all `2^(N+1)` strings. For each string, we could solve the game by minimax on the grid. This is correct because it directly follows the game definition. Unfortunately, even for `N = 50`, the number of strings is already astronomically large, so this direction is hopeless.

The breakthrough comes from understanding the geometry of the game.

After exactly `N` moves, the token reaches the anti-diagonal. The actual path only determines which anti-diagonal cell is reached. Optimal play lets the players control the balance between row moves and column moves.

Consider first an odd value `N = 2K + 1`. Alice makes the last move. A pairing strategy shows that after her moves she can always force the token onto one of the two central anti-diagonal cells, corresponding to indices `K` and `K + 1`. Conversely, if both of those cells are losing for her, Bob can force the game so that Alice's final move must choose between exactly those two losing cells. Thus Alice wins if and only if at least one of `S[K]` or `S[K+1]` is `A`.

Now consider an even value `N = 2K`. Alice chooses the first move, after which Bob becomes the first player in an odd-length subgame. If Alice moves one way, the relevant central pair becomes `(S[K-1], S[K])`. If she moves the other way, the relevant central pair becomes `(S[K], S[K+1])`. Bob wins an odd subgame unless both cells in its central pair are `A`. Consequently Alice wins exactly when at least one of these pairs consists entirely of `A`.

For odd `N`, among the four assignments of the central pair, three are winning:

```
AA, AB, BA
```

Only `BB` loses.

For even `N`, among the eight assignments of the central triple `(S[K-1], S[K], S[K+1])`, exactly three are winning:

```
AAA, AAB, BAA
```

The counts become:

For odd `N = 2K + 1`:

```
3 * 2^(N-1)
= 3 * 4^K
```

For even `N = 2K`:

```
3 * 2^(N-2)
= 3 * 4^(K-1)
```

Both expressions simplify to

```
3 * 4^floor((N-1)/2)
```

which is exactly the final formula.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^(N+1)) | O(1) | Too slow |
| Optimal | O(log N) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read `N`.
2. Compute `e = floor((N - 1) / 2)`.
3. Compute `4^e mod (10^9 + 3233)` using fast modular exponentiation.
4. Multiply the result by `3`.
5. Take the final value modulo `10^9 + 3233`.
6. Output the answer.

### Why it works

For odd `N`, optimal play depends only on the two central anti-diagonal positions. Alice wins unless both are labeled `B`, giving exactly `3` winning assignments of those two positions.

For even `N`, optimal play depends only on the three central positions. Alice wins precisely for the three assignments `AAA`, `AAB`, and `BAA`.

All remaining characters of the string never affect the outcome and can be chosen freely. After counting the free positions, both parity cases collapse to the same closed form:

$$3 \cdot 4^{\lfloor (N-1)/2 \rfloor}.$$

The algorithm evaluates exactly this formula.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 3233

def main():
    n = int(input())
    exp = (n - 1) // 2
    ans = 3 * pow(4, exp, MOD)
    print(ans % MOD)

if __name__ == "__main__":
    main()
```

The implementation is almost a direct translation of the mathematical formula.

`exp = (n - 1) // 2` computes the exponent appearing in the closed form. Python's built-in three-argument `pow` performs modular exponentiation in logarithmic time, which is much faster than repeatedly multiplying.

The multiplication by `3` is done afterward, and the final modulo operation keeps the result inside the required range.

There are no tricky boundary conditions. The smallest input is `N = 1`, which gives exponent `0`, and `pow(4, 0, MOD)` correctly returns `1`, producing the answer `3`.

## Worked Examples

### Example 1

Input:

```
2
```

Here `N = 2`.

| Variable | Value |
| --- | --- |
| `exp` | `(2 - 1) // 2 = 0` |
| `4^exp mod M` | `1` |
| Answer | `3 * 1 = 3` |

Output:

```
3
```

This is exactly the sample. The only winning triples are `AAA`, `AAB`, and `BAA`.

### Example 2

Input:

```
5
```

| Variable | Value |
| --- | --- |
| `exp` | `(5 - 1) // 2 = 2` |
| `4^exp mod M` | `16` |
| Answer | `3 * 16 = 48` |

Output:

```
48
```

For `N = 5`, only the two central positions matter. Three of their four assignments are winning, and the remaining four characters are free, giving `3 * 2^4 = 48`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log N) | Modular exponentiation |
| Space | O(1) | Constant extra memory |

With `N` up to `100000`, this is easily within the limits. The running time is dominated by a single modular power computation.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

MOD = 10**9 + 3233

def solve():
    n = int(input())
    print((3 * pow(4, (n - 1) // 2, MOD)) % MOD)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    global input
    input = sys.stdin.readline

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out

# provided sample
assert run("2\n") == "3\n", "sample"

# minimum N
assert run("1\n") == "3\n", "N=1"

# odd N
assert run("3\n") == "12\n", "3 * 4^1"

# even N
assert run("4\n") == "12\n", "3 * 4^1"

# larger value
assert run("5\n") == "48\n", "3 * 4^2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `3` | Smallest possible input |
| `2` | `3` | Sample case |
| `3` | `12` | Odd `N` formula |
| `4` | `12` | Even `N` formula |
| `5` | `48` | Larger exponent |

## Edge Cases

For `N = 1`, the game ends after Alice's first move.

Input:

```
1
```

The relevant pair is simply `(S0,S1)`. Alice loses only when both are `B`. There are `3` winning strings, and the formula gives:

$$3 \cdot 4^0 = 3.$$

For `N = 2`, only the central triple matters.

Input:

```
2
```

The winning triples are:

```
AAA
AAB
BAA
```

Exactly three assignments work, so the answer is `3`.

For a large odd value such as `N = 99999`, it would be impossible to enumerate strings. The algorithm still performs only one modular exponentiation:

$$3 \cdot 4^{49999} \pmod{10^9+3233}.$$

The running time remains logarithmic in the exponent, which is easily fast enough.
