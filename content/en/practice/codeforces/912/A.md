---
title: "CF 912A - Tricky Alchemy"
description: "We have two kinds of crystals available: yellow and blue. Producing each type of ball consumes crystals in a fixed recipe. A yellow ball requires 2 yellow crystals. A green ball requires 1 yellow crystal and 1 blue crystal. A blue ball requires 3 blue crystals."
date: "2026-06-13T00:49:11+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 912
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 456 (Div. 2)"
rating: 800
weight: 912
solve_time_s: 252
verified: true
draft: false
---

[CF 912A - Tricky Alchemy](https://codeforces.com/problemset/problem/912/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 4m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

We have two kinds of crystals available: yellow and blue.

Producing each type of ball consumes crystals in a fixed recipe. A yellow ball requires 2 yellow crystals. A green ball requires 1 yellow crystal and 1 blue crystal. A blue ball requires 3 blue crystals.

The input gives the current stock of yellow crystals `A` and blue crystals `B`, followed by the required numbers of yellow, green, and blue balls: `x`, `y`, and `z`.

Our task is to determine how many additional crystals must be purchased so that all requested balls can be produced. We are free to buy both yellow and blue crystals, and we want the minimum total number of extra crystals.

The constraints go up to $10^9$. Such values immediately rule out any simulation that creates balls one by one or repeatedly subtracts crystals. Even a linear algorithm in the number of balls would be far too slow. Since the input consists of only five integers, we should expect a constant-time arithmetic solution.

A common mistake is to treat shortages independently for each ball type instead of first computing the total crystal requirements.

Consider:

```
A = 2, B = 1
x = 1, y = 1, z = 0
```

The required yellow crystals are $2 \cdot 1 + 1 = 3$. The required blue crystals are $1$.

We are short exactly one yellow crystal, so the answer is `1`.

A careless approach that checks each ball recipe separately might double count shortages.

Another easy mistake is subtracting available crystals from the total requirement and allowing negative deficits to reduce the answer.

Example:

```
A = 100, B = 0
x = 1, y = 0, z = 0
```

Only 2 yellow crystals are needed. The surplus 98 yellow crystals cannot compensate for missing blue crystals in other situations. Each color must be handled independently. The correct additional amount here is `0`, not a negative number.

A final edge case occurs when one color has a surplus and the other has a shortage.

```
A = 10, B = 1
x = 0, y = 0, z = 1
```

We need 3 blue crystals and have only 1. The answer is `2`, even though yellow crystals are abundant. Crystal colors are not interchangeable.

## Approaches

The most direct idea is to think about producing every requested ball one by one. For each yellow ball we would consume two yellow crystals, for each green ball one yellow and one blue crystal, and for each blue ball three blue crystals. If crystals run out, we count how many more must be purchased.

This approach is correct because it follows the recipes exactly. The problem is that the number of balls can reach $10^9$. Simulating each ball would require billions of operations, which is impossible within the time limit.

The key observation is that the order of production does not matter. Every yellow ball always consumes 2 yellow crystals. Every green ball always consumes 1 yellow and 1 blue crystal. Every blue ball always consumes 3 blue crystals.

Instead of simulating production, we can compute the total crystal requirements directly.

The total yellow crystals needed are:

$$2x + y$$

The total blue crystals needed are:

$$y + 3z$$

Once these totals are known, we compare them with the available supplies.

If the required yellow crystals exceed `A`, we must buy the difference. Otherwise we buy none. The same logic applies to blue crystals.

The answer is simply the sum of the two shortages.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(x + y + z) | O(1) | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the available yellow and blue crystals, `A` and `B`.
2. Read the required numbers of yellow, green, and blue balls, `x`, `y`, and `z`.
3. Compute the total yellow crystals needed as `2 * x + y`.

Every yellow ball contributes 2 yellow crystals, and every green ball contributes 1 yellow crystal.
4. Compute the total blue crystals needed as `y + 3 * z`.

Every green ball contributes 1 blue crystal, and every blue ball contributes 3 blue crystals.
5. Compute the yellow shortage as `max(0, needed_yellow - A)`.

If we already have enough yellow crystals, the shortage should be zero rather than negative.
6. Compute the blue shortage as `max(0, needed_blue - B)`.
7. Output the sum of the two shortages.

### Why it works

The recipes determine exactly how many yellow and blue crystals are consumed by each requested ball. Adding these contributions gives the unique total requirement for each crystal color.

Yellow crystals can only satisfy yellow requirements, and blue crystals can only satisfy blue requirements. Because the two colors are independent, the minimum number of additional crystals is simply the sum of the missing yellow crystals and the missing blue crystals. Any surplus of one color cannot reduce the shortage of the other.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    A, B = map(int, input().split())
    x, y, z = map(int, input().split())

    needed_yellow = 2 * x + y
    needed_blue = y + 3 * z

    answer = max(0, needed_yellow - A) + max(0, needed_blue - B)
    print(answer)

solve()
```

The first two lines read the available crystal counts and the requested ball counts.

The variables `needed_yellow` and `needed_blue` store the total crystal requirements derived directly from the recipes. This avoids any simulation.

The calls to `max(0, ...)` are crucial. If we already have enough crystals of a color, that color contributes zero to the answer. Allowing negative values here would incorrectly let a surplus of one color reduce the total.

Python integers automatically handle values larger than 32-bit limits, although even in languages with fixed-size integers, the largest expression is only a few billion and fits comfortably in 64-bit types.

## Worked Examples

### Example 1

Input:

```
4 3
2 1 1
```

| Step | Value |
| --- | --- |
| Available yellow | 4 |
| Available blue | 3 |
| Needed yellow | 2×2 + 1 = 5 |
| Needed blue | 1 + 3×1 = 4 |
| Yellow shortage | 5 − 4 = 1 |
| Blue shortage | 4 − 3 = 1 |
| Answer | 1 + 1 = 2 |

The production requires five yellow crystals and four blue crystals. Since only four yellow and three blue crystals are available, one additional crystal of each color must be purchased.

### Example 2

Input:

```
10 10
1 1 1
```

| Step | Value |
| --- | --- |
| Available yellow | 10 |
| Available blue | 10 |
| Needed yellow | 2×1 + 1 = 3 |
| Needed blue | 1 + 3×1 = 4 |
| Yellow shortage | 0 |
| Blue shortage | 0 |
| Answer | 0 |

This example shows that extra crystals do not affect the answer. Since all requirements are already satisfied, no purchases are needed.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a fixed number of arithmetic operations are performed |
| Space | O(1) | No data structures proportional to input size are used |

The algorithm performs a handful of additions, multiplications, and comparisons regardless of the input values. This easily fits within the 1 second time limit and 256 MB memory limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    A, B = map(int, input().split())
    x, y, z = map(int, input().split())

    needed_yellow = 2 * x + y
    needed_blue = y + 3 * z

    return str(
        max(0, needed_yellow - A) +
        max(0, needed_blue - B)
    ) + "\n"

# provided sample
assert run("4 3\n2 1 1\n") == "2\n", "sample 1"

# minimum values
assert run("0 0\n0 0 0\n") == "0\n", "all zeros"

# only yellow shortage
assert run("1 100\n1 0 0\n") == "1\n", "need one more yellow crystal"

# only blue shortage
assert run("100 1\n0 0 1\n") == "2\n", "need two more blue crystals"

# large boundary values
assert run("1000000000 1000000000\n1000000000 1000000000 1000000000\n") == "4000000000\n", "large numbers"

# exactly enough crystals
assert run("5 4\n2 1 1\n") == "0\n", "perfect match"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 0 / 0 0 0` | `0` | Minimum values |
| `1 100 / 1 0 0` | `1` | Yellow shortage only |
| `100 1 / 0 0 1` | `2` | Blue shortage only |
| Large $10^9$ values | `4000000000` | Handles large arithmetic safely |
| `5 4 / 2 1 1` | `0` | Exact resource match |

## Edge Cases

Consider the case where no crystals and no balls are involved:

```
0 0
0 0 0
```

The algorithm computes:

```
needed_yellow = 0
needed_blue = 0
```

Both shortages are zero, so the output is:

```
0
```

This confirms that the formula handles empty requirements correctly.

Consider a case with a surplus of one color:

```
10 1
0 0 1
```

The algorithm computes:

```
needed_yellow = 0
needed_blue = 3
```

The shortages become:

```
yellow = max(0, 0 - 10) = 0
blue = max(0, 3 - 1) = 2
```

The output is:

```
2
```

The extra yellow crystals are ignored because crystal colors cannot be exchanged.

Consider a case where one requirement is exactly satisfied:

```
5 4
2 1 1
```

The algorithm computes:

```
needed_yellow = 5
needed_blue = 4
```

The shortages are:

```
yellow = 0
blue = 0
```

The output is:

```
0
```

This verifies that equality is handled correctly and does not produce an unnecessary purchase.

Finally, consider:

```
2 1
1 1 0
```

The requirements are:

```
needed_yellow = 3
needed_blue = 1
```

The shortages are:

```
yellow = 1
blue = 0
```

The answer is:

```
1
```

This demonstrates why shortages must be computed independently for each color. A deficit in yellow crystals cannot be offset by blue crystals.
