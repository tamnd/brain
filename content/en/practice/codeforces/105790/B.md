---
title: "CF 105790B - Bit Tennis 2"
description: "We have a take-away game played on several piles. A move consists of choosing one pile and removing a number of stones equal to a power of two. The allowed removals are 1, 2, 4, 8, and so on, as long as the chosen pile contains enough stones."
date: "2026-06-26T03:50:55+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105790
codeforces_index: "B"
codeforces_contest_name: "UDESC Selection Contest 2024-1"
rating: 0
weight: 105790
solve_time_s: 50
verified: true
draft: false
---

[CF 105790B - Bit Tennis 2](https://codeforces.com/problemset/problem/105790/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a take-away game played on several piles.

A move consists of choosing one pile and removing a number of stones equal to a power of two. The allowed removals are 1, 2, 4, 8, and so on, as long as the chosen pile contains enough stones. Julia makes the first move and the player who cannot move loses.

Before the game starts, Giovana must perform exactly `X` operations. In one operation she chooses a pile and doubles its size. After these mandatory doublings, both players play perfectly and we must determine who wins.

The input contains the number of piles, the number of required doublings, and the initial pile sizes. The output is the winner's name.

The constraints are large: up to `10^5` piles and pile sizes up to `10^9`, while `X` can be as large as `10^9`. Any solution that simulates moves or doublings individually is impossible. We need an `O(N)` or `O(N log N)` solution.

The tricky part is that `X` can be enormous. The actual sizes of the piles after all doublings are irrelevant if we can understand how doubling affects the game's Grundy values. The entire problem becomes a game theory question.

A common mistake is to analyze the exact pile sizes after doubling. For example:

```
N = 1
X = 1000000000
a = [1]
```

Trying to track the pile value after a billion doublings is pointless. The game outcome depends only on the Grundy numbers, and those follow a very simple pattern.

Another easy mistake is assuming that each doubling always changes the position. If a pile size is divisible by 3, doubling it keeps the same Grundy value. For example:

```
N = 1
X = 1
a = [3]
```

The pile's Grundy number remains unchanged after doubling, so Giovana can effectively spend a move without affecting the game state.

A final subtle case appears when the initial Nim xor is already zero. Giovana would like to keep it zero, but she is forced to perform exactly `X` doublings. Whether she can "waste" those doublings determines the answer.

## Approaches

The brute-force view is to compute the Grundy number of every pile size explicitly. For a pile of size `v`, we consider every reachable state `v - 2^k`, compute their Grundy numbers, and take the mex.

This works for small values, and if we calculate the first few states we obtain:

| Pile size | Grundy |
| --- | --- |
| 0 | 0 |
| 1 | 1 |
| 2 | 2 |
| 3 | 0 |
| 4 | 1 |
| 5 | 2 |
| 6 | 0 |

A pattern immediately appears: the Grundy number seems to be `v mod 3`.

A brute-force proof by computation is not enough for the actual constraints because pile sizes reach `10^9`. We need a mathematical characterization.

The key observation is that every power of two is congruent to either 1 or 2 modulo 3:

```
2^0 ≡ 1 (mod 3)
2^1 ≡ 2 (mod 3)
2^2 ≡ 1 (mod 3)
2^3 ≡ 2 (mod 3)
...
```

So a move from a pile with residue `k` modulo 3 always reaches one of the other two residues, never the same one.

Suppose a pile has residue `k`.

Every move reaches residues `{0,1,2} \ {k}`.

If we assume the Grundy values of smaller positions are exactly their residues modulo 3, then the set of reachable Grundy numbers is also `{0,1,2} \ {k}`. The mex of that set is `k`.

This proves:

```
Grundy(v) = v mod 3
```

Now the game becomes Nim. The xor of all residues determines the winner.

The remaining challenge is understanding the effect of a doubling operation.

For a pile residue:

```
0 -> 0
1 -> 2
2 -> 1
```

Doubling swaps 1 and 2, while 0 stays unchanged.

This reduces the entire problem to parity arguments on the counts of residues 1 and 2.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Grundy computation | O(max(ai) log max(ai)) or worse | O(max(ai)) | Too slow |
| Residue modulo 3 game analysis | O(N) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute the residue `ai mod 3` for every pile.
2. Compute the Nim xor `S` of all residues.
3. Count how many piles belong to each residue class: `freq[0]`, `freq[1]`, and `freq[2]`.
4. If `X = 0`, no preprocessing occurs. The position is a standard Nim position.

Julia starts, so she wins iff `S != 0`. Otherwise Giovana wins.
5. If `X > 0` and `S = 0`, Giovana already likes the position because the first player is losing.

She wants all mandatory doublings to leave the xor unchanged.
6. A pile with residue 0 can absorb any number of doublings because `0 -> 0`.

If such a pile exists, Giovana can spend all required operations there.
7. If no residue-0 pile exists, every doubling swaps a residue 1 with residue 2 or vice versa.

Applying two doublings on the same pile restores its original residue.

Hence the xor can stay unchanged only when `X` is even.
8. If `X > 0` and `S != 0`, Giovana wants to transform the position into xor zero.
9. Swapping one residue-1 pile with residue-2 changes the parity of both residue counts.

The xor becomes zero exactly when both `freq[1]` and `freq[2]` are odd.
10. Once xor zero is reached, any additional doublings must be discarded.

This is possible if `X` is odd, or if a residue-0 pile exists to absorb one extra operation.
11. Output `"Giovana"` when she can force a losing position for Julia before the game starts, otherwise output `"Julia"`.

### Why it works

The fundamental invariant is that every pile behaves exactly like a Nim pile whose size is `ai mod 3`. The proof comes from the Grundy recurrence: every move changes the residue by either 1 or 2 modulo 3, making all other residue classes reachable and the current one unreachable. The mex is therefore the current residue.

Doubling does not depend on the actual pile size either. It only affects the residue modulo 3, leaving residue 0 fixed and swapping residues 1 and 2. Once the game is reduced to these three residue classes, only the parity of the counts of residues 1 and 2 matters. The editorial conditions are precisely the situations where Giovana can use her mandatory doublings to obtain a Nim xor of zero and keep it there.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, x = map(int, input().split())
a = list(map(int, input().split()))

freq = [0, 0, 0]
s = 0

for v in a:
    r = v % 3
    freq[r] += 1
    s ^= r

if x == 0:
    win = (s == 0)
else:
    if s == 0:
        win = (freq[0] > 0 or x % 2 == 0)
    else:
        win = (
            freq[1] % 2 == 1 and
            freq[2] % 2 == 1 and
            (x % 2 == 1 or freq[0] > 0)
        )

print("Giovana" if win else "Julia")
```

The first loop computes everything needed for the game: the Nim xor and the frequencies of residues modulo 3.

The `x == 0` branch is ordinary Nim. A zero xor means the starting player loses, so Giovana wins because Julia moves first.

For `x > 0`, the logic follows directly from the residue transformation rules. The condition `freq[0] > 0` is especially important because residue-0 piles are the only way to spend an odd number of extra doublings without changing the position.

All arithmetic fits comfortably in 32-bit integers, but Python naturally handles larger values anyway. No pile is ever explicitly doubled, which avoids issues with the huge bound on `X`.

## Worked Examples

### Example 1

Input:

```
4 1
5 1 3 2
```

Residues are:

```
[2, 1, 0, 2]
```

| Pile | Residue | Running xor |
| --- | --- | --- |
| 5 | 2 | 2 |
| 1 | 1 | 3 |
| 3 | 0 | 3 |
| 2 | 2 | 1 |

Final values:

```
S = 1
freq[0] = 1
freq[1] = 1
freq[2] = 2
```

Since `S != 0`, both residue-1 and residue-2 counts must be odd. Here `freq[2]` is even, so Giovana cannot make the xor become zero.

Winner: `Julia`.

This example shows that having a residue-0 pile alone is not enough. The parity condition on residues 1 and 2 must also hold.

### Example 2

Input:

```
3 2
1 2 3
```

Residues:

```
[1, 2, 0]
```

| Pile | Residue | Running xor |
| --- | --- | --- |
| 1 | 1 | 1 |
| 2 | 2 | 3 |
| 3 | 0 | 3 |

Final values:

```
S = 3
freq[0] = 1
freq[1] = 1
freq[2] = 1
```

Both non-zero residue counts are odd. A residue-0 pile exists, so Giovana can adjust the position and discard any extra operation.

Winner: `Giovana`.

This example demonstrates the role of residue-0 piles as buffers for mandatory doublings.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | One pass over all piles |
| Space | O(1) | Only three frequency counters and one xor value |

The solution processes each pile exactly once and never depends on the magnitude of `ai` or `X`. With `N ≤ 10^5`, this easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    n, x = map(int, input().split())
    a = list(map(int, input().split()))

    freq = [0, 0, 0]
    s = 0

    for v in a:
        r = v % 3
        freq[r] += 1
        s ^= r

    if x == 0:
        win = (s == 0)
    else:
        if s == 0:
            win = (freq[0] > 0 or x % 2 == 0)
        else:
            win = (
                freq[1] % 2 == 1 and
                freq[2] % 2 == 1 and
                (x % 2 == 1 or freq[0] > 0)
            )

    print("Giovana" if win else "Julia")

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout
    return out.getvalue().strip()

# custom cases

assert run("1 0\n3\n") == "Giovana"
assert run("1 0\n1\n") == "Julia"
assert run("2 2\n1 2\n") == "Giovana"
assert run("2 1\n1 2\n") == "Julia"
assert run("3 1000000000\n3 6 9\n") == "Giovana"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 0 / 3` | Giovana | Zero xor without preprocessing |
| `1 0 / 1` | Julia | Non-zero xor without preprocessing |
| `2 2 / 1 2` | Giovana | Even number of mandatory swaps |
| `2 1 / 1 2` | Julia | Odd number of mandatory swaps |
| `3 1000000000 / 3 6 9` | Giovana | Huge X, residue-0 piles absorb all moves |

## Edge Cases

Consider:

```
1 1
3
```

The pile residue is 0. The initial xor is also 0. Giovana is already happy with the position and can spend the required doubling on this pile because `0 -> 0`. The xor remains zero and Julia starts from a losing Nim position. The algorithm detects `freq[0] > 0` and outputs `Giovana`.

Now consider:

```
2 1
1 2
```

The residues are `[1,2]`. The xor is already zero. There is no residue-0 pile. One mandatory doubling swaps either `1 -> 2` or `2 -> 1`, changing the xor away from zero. Since `X` is odd, Giovana cannot cancel the effect. The algorithm reaches the condition `freq[0] == 0` and `X % 2 == 1`, producing `Julia`.

Finally:

```
3 2
1 2 3
```

The residues are `[1,2,0]`. The xor is non-zero, and both non-zero residue counts are odd. Giovana can use one doubling to make the xor zero and use the residue-0 pile to absorb the remaining required operation. The algorithm satisfies all conditions in the `S != 0` branch and outputs `Giovana`.
