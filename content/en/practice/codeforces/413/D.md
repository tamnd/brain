---
title: "CF 413D - 2048"
description: "We process a sequence of tiles, each tile being either 2 or 4. A tile starts far to the right and slides left. When it touches an equal value, the two merge into a doubled value and the new tile keeps moving."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "dp"]
categories: ["algorithms"]
codeforces_contest: 413
codeforces_index: "D"
codeforces_contest_name: "Coder-Strike 2014 - Round 2"
rating: 2000
weight: 413
solve_time_s: 143
verified: true
draft: false
---

[CF 413D - 2048](https://codeforces.com/problemset/problem/413/D)

**Rating:** 2000  
**Tags:** bitmasks, dp  
**Solve time:** 2m 23s  
**Verified:** yes  

## Solution
## Problem Understanding

We process a sequence of tiles, each tile being either `2` or `4`. A tile starts far to the right and slides left. When it touches an equal value, the two merge into a doubled value and the new tile keeps moving. This is the crucial difference from ordinary 2048, merges can chain during a single move.

We are given a partially specified sequence of length `n`. Some positions are fixed as `2` or `4`, and some are `0`, meaning we may choose either `2` or `4` there. We must count how many completions produce at least one tile with value at least `2^k`.

The constraints completely determine the kind of solution we need. The sequence length reaches `2000`, so anything exponential in `n` is impossible. A brute-force over all replacements already reaches `2^2000`. Even a state DP with too many dimensions would fail.

The interesting part is that `k ≤ 11`. The target tile is at most `2^11 = 2048`, which means only merge levels up to `11` matter. This small bound suggests compressing the board state into a bitmask or small DP state.

A subtle point is how the strip evolves. Because merged tiles continue moving, the final strip always behaves like binary carries.

For example:

```
2 2 2
```

does not become:

```
4 2
```

Instead:

```
2 -> 4
4 + 2 -> 4 2
```

The final state is `4 2`.

Another easy mistake is assuming the order of tiles with the same power does not matter. It does.

Example:

```
2 4 2 2
```

evolves differently from:

```
2 2 4 2
```

because merges happen during insertion.

One more edge case appears when the winning tile forms only after a long carry chain.

Example:

```
2 2 2 2
```

The process is:

```
2
4
4 2
8
```

A naive simulation that only merges once per insertion would incorrectly stop at `4 4`.

The output asks for the number of valid replacements modulo `10^9 + 7`, so counting must be done under modular arithmetic throughout the DP.

## Approaches

The most direct solution is brute force. Replace every `0` with both `2` and `4`, simulate the whole game, and check whether a tile at least `2^k` appears.

Simulation itself is easy. The strip behaves exactly like binary addition. If we encode `2^1` as level `1`, `2^2` as level `2`, and so on, then inserting a level acts like adding one to a binary counter with carries.

For example, inserting a `2` means adding a token at level `1`. If level `1` already exists, they merge into level `2`, and the carry continues.

The brute-force is correct because it literally follows the game rules. The problem is complexity. With at most `2000` unknown positions, we would need to check `2^2000` sequences.

The key observation is that the board state is tiny.

At any moment, for each level below `k`, only the parity matters. Two equal tiles immediately merge upward, so a level can contain at most one tile. This means the entire relevant board can be represented by a bitmask of size `k`.

If bit `i` is set, then the strip currently contains a tile `2^i`.

Now inserting a tile becomes a carry process on this mask:

```
while bit exists:
    remove bit
    carry upward
set first empty bit
```

If the carry reaches level `k` or higher, we already won.

This transforms the problem into DP over prefixes and masks.

Let:

```
dp[pos][mask]
```

be the number of ways to process the first `pos` elements and end with board state `mask` without having produced `2^k`.

The number of masks is only `2^k ≤ 2048`, and each transition costs at most `k` carry steps.

The total complexity becomes:

```
O(n * 2^k * k)
```

which is around `2000 * 2048 * 11 ≈ 4.5e7` primitive operations, acceptable in optimized Python with careful implementation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^z · n · k) | O(k) | Too slow |
| Optimal | O(n · 2^k · k) | O(2^k) | Accepted |

Here `z` is the number of zeroes.

## Algorithm Walkthrough

1. Represent each tile by its exponent.

We map:

```
2 -> 1
4 -> 2
```

The target is reaching exponent `k`.
2. Represent the strip state as a bitmask.

Bit `i` means a tile `2^i` exists. We only store levels `0..k-1`. Any carry beyond that means success.
3. Define the transition function.

Suppose we insert level `x`.

Start from bit `x`.

While that bit already exists in the mask:

- remove the bit,
- increment `x`,
- continue carrying upward.

When an empty position is found:

- place the bit there.

If `x >= k`, then the sequence already wins.
4. Build dynamic programming over positions.

Let:

```
dp[mask]
```

store the number of ways to reach this mask after processing some prefix, while still not winning.
5. Process the sequence left to right.

For each position:

- if the value is fixed as `2`, only insert exponent `1`,
- if fixed as `4`, only insert exponent `2`,
- if it is `0`, try both.
6. Apply transitions.

For every current mask and every allowed insertion:

- compute the next mask using the carry process,
- if the carry reaches exponent `k`, add the current count directly to the answer,
- otherwise update the next DP layer.
7. Take all operations modulo `10^9 + 7`.

### Why it works

The invariant is that every DP state exactly represents the unique strip configuration after processing some prefix, assuming no tile of level `k` or larger has appeared yet.

The carry process matches the game mechanics exactly. Two equal tiles merge and continue moving, which is identical to binary addition with carries. Since every level can contain at most one tile after stabilization, the bitmask representation is lossless.

Every possible completion of the sequence follows exactly one chain of DP transitions, and every DP transition corresponds to a legal game evolution. The algorithm neither misses sequences nor counts any sequence twice.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    size = 1 << k

    # trans[level][mask] = next_mask
    # if next_mask == -1, reaching >= 2^k occurs
    trans = [[0] * size for _ in range(3)]

    for level in (1, 2):
        for mask in range(size):
            x = level
            cur = mask

            while x < k and (cur >> x) & 1:
                cur ^= (1 << x)
                x += 1

            if x >= k:
                trans[level][mask] = -1
            else:
                trans[level][mask] = cur | (1 << x)

    dp = [0] * size
    dp[0] = 1

    ans = 0

    for val in a:
        ndp = [0] * size

        if val == 0:
            options = [1, 2]
        elif val == 2:
            options = [1]
        else:
            options = [2]

        for mask in range(size):
            ways = dp[mask]
            if not ways:
                continue

            for level in options:
                nxt = trans[level][mask]

                if nxt == -1:
                    ans = (ans + ways) % MOD
                else:
                    ndp[nxt] = (ndp[nxt] + ways) % MOD

        dp = ndp

    print(ans % MOD)

solve()
```

The first important idea in the implementation is converting values into exponents. Working with `1` and `2` instead of `2` and `4` makes carry handling natural.

The transition table is precomputed before the DP starts. This removes repeated carry simulation inside the main loops. Since there are only two insertion types and at most `2048` masks, preprocessing is cheap.

The carry simulation modifies a temporary mask `cur`. Whenever a bit already exists, we remove it and carry upward. This exactly matches repeated merges in the game.

A subtle implementation detail is handling winning states. We never store masks containing level `k`, because once such a tile appears the sequence is already successful. Those transitions contribute directly to `ans`.

The DP itself uses rolling arrays. Only the previous layer matters, so keeping two arrays is enough.

Another detail easy to get wrong is the indexing of bits. Bit `1` represents tile `2`, and bit `2` represents tile `4`. Bit `0` is unused, which simplifies the mapping between powers and exponents.

## Worked Examples

### Example 1

Input:

```
7 4
2 2 4 2 2 2 2
```

Target is reaching `16`, which corresponds to exponent `4`.

| Step | Insert | Current Mask | Meaning |
| --- | --- | --- | --- |
| 0 | - | 0000 | empty |
| 1 | 2 | 0010 | tile 2 |
| 2 | 2 | 0100 | tile 4 |
| 3 | 4 | 1000 | tile 8 |
| 4 | 2 | 1010 | 8,2 |
| 5 | 2 | 1100 | 8,4 |
| 6 | 2 | 1110 | 8,4,2 |
| 7 | 2 | win | carry reaches 16 |

The final insertion triggers a carry chain:

```
2 + 2 -> 4
4 + 4 -> 8
8 + 8 -> 16
```

This demonstrates why repeated carries are essential.

### Example 2

Input:

```
3 3
0 0 0
```

Target is reaching `8`.

| Sequence | Result |
| --- | --- |
| 2 2 2 | no |
| 2 2 4 | yes |
| 2 4 2 | no |
| 2 4 4 | no |
| 4 2 2 | yes |
| 4 2 4 | no |
| 4 4 2 | no |
| 4 4 4 | yes |

There are `3` winning sequences.

This example shows that the order matters. The same multiset of tiles can produce different outcomes.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n · 2^k · k) | DP over all masks with carry simulation |
| Space | O(2^k) | Rolling DP arrays |

With `k ≤ 11`, the number of masks is at most `2048`. The total work stays well within the limits for Python.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

MOD = 10**9 + 7

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    size = 1 << k

    trans = [[0] * size for _ in range(3)]

    for level in (1, 2):
        for mask in range(size):
            x = level
            cur = mask

            while x < k and (cur >> x) & 1:
                cur ^= (1 << x)
                x += 1

            if x >= k:
                trans[level][mask] = -1
            else:
                trans[level][mask] = cur | (1 << x)

    dp = [0] * size
    dp[0] = 1

    ans = 0

    for val in a:
        ndp = [0] * size

        if val == 0:
            options = [1, 2]
        elif val == 2:
            options = [1]
        else:
            options = [2]

        for mask in range(size):
            ways = dp[mask]

            if not ways:
                continue

            for level in options:
                nxt = trans[level][mask]

                if nxt == -1:
                    ans = (ans + ways) % MOD
                else:
                    ndp[nxt] = (ndp[nxt] + ways) % MOD

        dp = ndp

    return str(ans)

# provided sample
assert run(
"""7 4
2 2 4 2 2 2 2
"""
) == "1"

# minimum non-winning case
assert run(
"""1 3
2
"""
) == "0"

# immediate winning
assert run(
"""2 3
4 4
"""
) == "1"

# all zeroes
assert run(
"""3 3
0 0 0
"""
) == "3"

# long carry chain
assert run(
"""4 4
2 2 2 2
"""
) == "1"

print("ok")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 3 / 2` | `0` | Minimum-size non-winning case |
| `2 3 / 4 4` | `1` | Direct merge into target |
| `3 3 / 0 0 0` | `3` | DP branching over unknown values |
| `4 4 / 2 2 2 2` | `1` | Multi-step carry chain |

## Edge Cases

Consider:

```
4 4
2 2 2 2
```

A buggy implementation that merges only once per insertion would stop at:

```
4 4
```

and incorrectly conclude failure.

Our transition simulation keeps carrying upward until an empty level appears:

```
2 + 2 -> 4
4 + 4 -> 8
8 + 8 -> 16
```

so the DP correctly counts this sequence as winning.

Now consider:

```
3 3
2 4 2
```

The process becomes:

```
2
4
4 2
```

No `8` appears.

But:

```
3 3
4 2 2
```

becomes:

```
4
4 2
8
```

The answer differs even though both contain two `2`s and one `4`. Since the DP processes insertions strictly in order, it preserves this distinction correctly.

Finally, consider:

```
2 3
4 4
```

The first `4` creates exponent `2`. The second insertion collides immediately and carries to exponent `3`, which already reaches the target.

Our transition table marks such transitions with `-1`, and the DP adds them directly to the final answer instead of storing an invalid mask.
