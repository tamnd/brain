---
title: "CF 102672B - Crazy dance"
description: "We have n dancers placed on integer coordinates. Several dancers may share the same coordinate. During the dance, every dancer independently moves one unit either left or right with equal probability."
date: "2026-08-07T21:35:36+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102672
codeforces_index: "B"
codeforces_contest_name: "Selection of tasks from Internet olympiads season 2019-20"
rating: 0
weight: 102672
solve_time_s: 74
verified: true
draft: false
---

[CF 102672B - Crazy dance](https://codeforces.com/problemset/problem/102672/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 14s  
**Verified:** yes  

## Solution
## Problem Understanding

We have `n` dancers placed on integer coordinates. Several dancers may share the same coordinate. During the dance, every dancer independently moves one unit either left or right with equal probability.

A dance is successful if the multiset of occupied positions after all moves is exactly the same as before. We are allowed to choose the initial placement of the dancers and need to maximize the probability of a successful dance. The output is the base-2 logarithm of this maximum probability.

The value of `n` can be as large as 40000. This immediately rules out simulation, dynamic programming over the number of dancers, or any approach that depends on the number of possible placements. The solution has to come from finding a mathematical pattern that reduces the answer to a direct formula.

The first hidden constraint comes from parity. Every dancer moves across exactly one gap between two integer coordinates. For the final configuration to match the initial one, every gap must have the same number of dancers crossing it in both directions. That means the total number of dancers must be twice the total number of balanced crossings. As a result, an odd number of dancers can never work.

For example, with one dancer:

```
1
```

the answer is `0`, because the only dancer must move away from its original coordinate.

For an even example:

```
4
```

the optimal probability is `1/8`, so the output is:

```
-3
```

A common mistake is to put all dancers on only two adjacent coordinates. For four dancers, placing two on each side gives only one valid crossing pattern, with probability `1/16`. The better arrangement uses three coordinates with counts `1,2,1`, where the middle pair can exchange in two different ways, giving probability `2/16`.

## Approaches

A brute-force approach would try different placements of dancers and count all possible movement choices that keep the configuration unchanged. The problem is that there are infinitely many possible coordinate choices, and even if we restrict ourselves to a small interval, the number of movement outcomes is `2^n`. For `n = 40000`, even checking a single placement is impossible.

The useful observation is to stop thinking about individual dancers and instead think about gaps. Suppose a gap between two neighboring occupied coordinates has `x` dancers crossing it from left to right. A successful dance requires exactly `x` dancers crossing the same gap from right to left. Therefore every gap is associated with a balanced number of crossings.

Let the numbers of crossings through consecutive gaps be:

```
g1, g2, ..., gk
```

The total number of dancers is exactly:

```
2 * (g1 + g2 + ... + gk)
```

because every crossing contributes one dancer from each side.

For a fixed sequence of gaps, the number of valid movement choices is determined by how many ways each group of dancers can choose their direction. At a position between two gaps `a` and `b`, there are `a + b` dancers, and we must choose which `a` of them go left. This contributes:

```
C(a + b, a)
```

ways.

The remaining question is how to choose the gap sizes to maximize the product of these binomial coefficients. Splitting a crossing count into smaller gaps always helps. The largest contribution comes from making every gap have size `1`.

If there are `n / 2` total crossings and every gap has size one, the arrangement becomes:

```
1, 2, 2, ..., 2, 1
```

The two ends contribute one possible choice each, while every middle position contributes:

```
C(2,1) = 2
```

There are `n / 2 - 1` middle positions, so the number of successful movement assignments is:

```
2^(n/2 - 1)
```

The total number of possible dances is:

```
2^n
```

so the maximum probability is:

```
2^(n/2 - 1) / 2^n = 2^(-n/2 - 1)
```

Therefore the answer is simply:

```
-n/2 - 1
```

for even `n`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(1) | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of dancers `n`. The only information needed is the parity of `n`, because the optimal probability depends only on whether the number of dancers can be split into balanced crossings.
2. If `n` is odd, output `0`. A successful dance would require every dancer to be paired with a dancer crossing the same gap in the opposite direction, which is impossible with an odd number of dancers.
3. If `n` is even, output `-n/2 - 1`. This is the logarithm of the probability obtained by using unit-sized gaps everywhere.

Why it works:

Every successful dance corresponds to balanced crossings across every gap. The total number of crossings is fixed at `n/2`. Dividing these crossings into more gaps increases the number of independent choices. The best possible split is making every gap contain exactly one crossing. This creates the maximum possible number of valid movement assignments, namely `2^(n/2-1)`. Since all `2^n` direction choices are equally likely, the probability is exactly `2^(-n/2-1)`.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    if n % 2:
        print(0)
    else:
        print(-n // 2 - 1)

solve()
```

The implementation only checks whether the number of dancers is even. There is no need to store positions or simulate any movements because the optimal probability is determined entirely by the parity and size of `n`.

The expression `-n // 2 - 1` works because Python's integer division is exact for even `n`. No floating point calculation is needed, which avoids precision problems in the logarithm output.

## Worked Examples

For the first sample:

Input:

```
4
```

The number of dancers is even, so:

| Variable | Value |
| --- | --- |
| n | 4 |
| n / 2 | 2 |
| answer | -2 - 1 = -3 |

The probability is `2^-3 = 1/8`, matching the sample.

For the second sample:

Input:

```
1
```

The number of dancers is odd.

| Variable | Value |
| --- | --- |
| n | 1 |
| n % 2 | 1 |
| answer | 0 |

A successful dance is impossible, so the required output is `0`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a parity check and arithmetic operation are performed. |
| Space | O(1) | No additional data structures are used. |

The solution easily fits the constraints because it performs a constant amount of work even for the maximum value of `n`.

## Test Cases

```python
import sys
import io

def solve_io(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    n = int(sys.stdin.readline())
    if n % 2:
        out = "0\n"
    else:
        out = str(-n // 2 - 1) + "\n"

    sys.stdin = old_stdin
    return out

assert solve_io("4\n") == "-3\n", "sample 1"
assert solve_io("1\n") == "0\n", "sample 2"

assert solve_io("2\n") == "-2\n", "two dancers"
assert solve_io("6\n") == "-4\n", "three crossing pairs"
assert solve_io("40000\n") == "-20001\n", "maximum size"
assert solve_io("3\n") == "0\n", "odd number of dancers"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2` | `-2` | Smallest possible even case |
| `6` | `-4` | Formula for larger even values |
| `40000` | `-20001` | Maximum constraint handling |
| `3` | `0` | Odd parity impossibility |

## Edge Cases

For `n = 1`, there is no possible balancing. The only dancer must move to a different coordinate, so the probability is zero and the algorithm prints `0`.

For odd values such as:

```
5
```

a naive formula might still try to compute a logarithm value. The crossing argument shows this cannot happen because successful dances require every crossing to be paired, meaning the total number of dancers must be even. The algorithm detects this immediately and prints `0`.

For the smallest even case:

```
2
```

the formula gives:

```
-2 / 2 - 1 = -2
```

which corresponds to probability `1/4`. Two dancers placed next to each other must swap positions, and exactly one of the four possible movement choices succeeds.

For large inputs such as:

```
40000
```

the solution does not construct the placement or enumerate possibilities. It directly computes:

```
-20000 - 1 = -20001
```

so there are no overflow or performance concerns.

This can also be shortened into a contest-style editorial format if you want a version closer to what would appear on Codeforces.
