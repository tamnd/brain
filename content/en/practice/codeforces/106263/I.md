---
title: "CF 106263I - \u5347\u7ea7\u5b9d\u53ef\u68a6"
description: "Each of the six players starts with a level-1 Pokémon. To raise a Pokémon from level $k-1$ to level $k$, we must spend exactly $k-1$ experience crystals. For each player, we are given a target level $ai$."
date: "2026-06-19T16:38:20+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106263
codeforces_index: "I"
codeforces_contest_name: "2025 \u534e\u5357\u5e08\u8303\u5927\u5b66\u201c\u5353\u8d8a\u6559\u80b2\u676f\u201d\u7b97\u6cd5\u4e0e\u7a0b\u5e8f\u8bbe\u8ba1\u7ade\u8d5b\uff08\u65b0\u751f\u8d5b\uff09"
rating: 0
weight: 106263
solve_time_s: 42
verified: true
draft: false
---

[CF 106263I - \u5347\u7ea7\u5b9d\u53ef\u68a6](https://codeforces.com/problemset/problem/106263/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 42s  
**Verified:** yes  

## Solution
## Problem Understanding

Each of the six players starts with a level-1 Pokémon. To raise a Pokémon from level $k-1$ to level $k$, we must spend exactly $k-1$ experience crystals.

For each player, we are given a target level $a_i$. We must determine how many crystals are needed to raise a Pokémon from level 1 all the way to level $a_i$, and output the answers for all six players.

The target levels can be as large as $10^9$. That immediately rules out any approach that simulates level-ups one by one. A single Pokémon might require nearly one billion upgrade steps, which is far beyond what can be processed within a one-second time limit.

The key challenge is not the number of players, since there are always exactly six of them. The challenge is computing the total crystal cost for a very large target level without iterating through every intermediate level.

There are a few edge cases that are easy to mishandle.

Suppose the target level is already 1:

```
1 1 1 1 1 1
```

The correct output is:

```
0 0 0 0 0 0
```

No upgrades are needed. A careless formula might accidentally include an extra term and produce a positive answer.

Consider target level 2:

```
2 2 2 2 2 2
```

The correct output is:

```
1 1 1 1 1 1
```

Only the upgrade from level 1 to level 2 is required, costing exactly 1 crystal. Off-by-one mistakes often appear here.

The largest level is also important:

```
1000000000
```

The answer is approximately $5 \times 10^{17}$, which does not fit inside a 32-bit integer. Languages with fixed-width integer types require 64-bit arithmetic. Python handles this automatically, but the mathematical size should still be kept in mind.

## Approaches

A direct simulation is the most natural starting point. If the target level is $a$, we can add the cost of every upgrade:

$$1 + 2 + 3 + \cdots + (a-1)$$

This works because upgrading from level 1 to level 2 costs 1, from level 2 to level 3 costs 2, and so on until the final upgrade into level $a$.

The problem is the running time. For $a=10^9$, we would perform roughly one billion additions for a single player. Even though there are only six players, billions of operations are far too slow.

The observation is that the required sum is a well-known arithmetic series:

$$1+2+\cdots+n=\frac{n(n+1)}{2}$$

Here $n=a-1$, so the total crystal cost becomes

$$\frac{(a-1)a}{2}$$

This formula computes the answer in constant time, regardless of how large the level is. Since there are only six inputs, we simply apply the formula six times and print the results.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(a) per player | O(1) | Too slow |
| Optimal | O(1) per player | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the six target levels.
2. For each target level $a$, compute the total crystal cost as:

$$\frac{a(a-1)}{2}$$

This is the sum of all upgrade costs from level 1 up to level $a$.
3. Store the six computed values.
4. Output the six answers separated by spaces.

### Why it works

To reach level $a$, the Pokémon must perform every upgrade:

$$1 \to 2,\quad 2 \to 3,\quad \ldots,\quad (a-1)\to a$$

The costs of these upgrades are:

$$1,2,3,\ldots,a-1$$

The total required crystals are exactly the sum of these integers. The arithmetic-series formula states that

$$1+2+\cdots+(a-1)=\frac{a(a-1)}{2}$$

Since the algorithm computes precisely this value for every player, every output is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

levels = list(map(int, input().split()))

ans = [a * (a - 1) // 2 for a in levels]

print(*ans)
```

The program reads the six target levels into a list.

For each level `a`, it evaluates `a * (a - 1) // 2`, which is the arithmetic-series formula derived earlier. Integer division is used because the result is always an integer.

The answers are collected in a list and printed on one line separated by spaces, matching the required output format.

A common off-by-one mistake is to compute `a * (a + 1) // 2`. That would sum from 1 through `a`, but the final upgrade cost is only `a - 1`, so the correct formula is `a * (a - 1) // 2`.

Python integers automatically expand to arbitrary size, so even the largest possible answer for $a=10^9$ is handled safely.

## Worked Examples

### Example 1

Input:

```
10 8 3 4 6 2
```

| Target Level a | Formula | Result |
| --- | --- | --- |
| 10 | 10×9/2 | 45 |
| 8 | 8×7/2 | 28 |
| 3 | 3×2/2 | 3 |
| 4 | 4×3/2 | 6 |
| 6 | 6×5/2 | 15 |
| 2 | 2×1/2 | 1 |

Output:

```
45 28 3 6 15 1
```

This example shows that each answer is simply the triangular number corresponding to $a-1$.

### Example 2

Input:

```
1 2 3 4 5 6
```

| Target Level a | Formula | Result |
| --- | --- | --- |
| 1 | 1×0/2 | 0 |
| 2 | 2×1/2 | 1 |
| 3 | 3×2/2 | 3 |
| 4 | 4×3/2 | 6 |
| 5 | 5×4/2 | 10 |
| 6 | 6×5/2 | 15 |

Output:

```
0 1 3 6 10 15
```

This trace highlights the boundary case where level 1 requires no crystals at all.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Exactly six formula evaluations |
| Space | O(1) | Only a few variables and six outputs are stored |

The input size is fixed at six integers, so the running time is effectively constant. The arithmetic formula avoids any dependence on the target level value, allowing levels up to $10^9$ to be processed instantly.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    levels = list(map(int, input().split()))
    ans = [a * (a - 1) // 2 for a in levels]
    return " ".join(map(str, ans))

# provided sample
assert run("10 8 3 4 6 2\n") == "45 28 3 6 15 1", "sample"

# minimum levels
assert run("1 1 1 1 1 1\n") == "0 0 0 0 0 0", "all level 1"

# all equal values
assert run("5 5 5 5 5 5\n") == "10 10 10 10 10 10", "all equal"

# off-by-one boundary
assert run("2 2 2 2 2 2\n") == "1 1 1 1 1 1", "level 2"

# maximum values
assert run("1000000000 1000000000 1000000000 1000000000 1000000000 1000000000\n") == \
       "499999999500000000 499999999500000000 499999999500000000 499999999500000000 499999999500000000 499999999500000000", \
       "maximum level"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1 1 1 1` | `0 0 0 0 0 0` | No upgrades needed |
| `5 5 5 5 5 5` | `10 10 10 10 10 10` | Repeated values |
| `2 2 2 2 2 2` | `1 1 1 1 1 1` | Off-by-one correctness |
| `1000000000 ...` | `499999999500000000 ...` | Large-number handling |

## Edge Cases

### Target level is already 1

Input:

```
1 1 1 1 1 1
```

For each value:

$$\frac{1\cdot(1-1)}{2}=0$$

The algorithm outputs:

```
0 0 0 0 0 0
```

This is correct because the Pokémon starts at level 1 and needs no upgrades.

### First nontrivial level

Input:

```
2 2 2 2 2 2
```

For each value:

$$\frac{2\cdot1}{2}=1$$

The algorithm outputs:

```
1 1 1 1 1 1
```

Only one upgrade exists, from level 1 to level 2, costing exactly one crystal.

### Maximum level

Input:

```
1000000000 1000000000 1000000000 1000000000 1000000000 1000000000
```

For each value:

$$\frac{1000000000\cdot999999999}{2}
=
499999999500000000$$

The algorithm computes this directly without any iteration. Even though the answer is very large, Python stores it safely and prints the exact value.
