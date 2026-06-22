---
title: "CF 105437C - Repainting Balls"
description: "We start with a collection of balls colored red, yellow, and green, with counts a, b, and c. We are allowed to repeatedly pick any single ball and repaint it into one of the other two colors."
date: "2026-06-23T03:40:40+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105437
codeforces_index: "C"
codeforces_contest_name: "ICPC 2024-2025 NERC, Southern and Volga Russia Qualifier"
rating: 0
weight: 105437
solve_time_s: 111
verified: false
draft: false
---

[CF 105437C - Repainting Balls](https://codeforces.com/problemset/problem/105437/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 51s  
**Verified:** no  

## Solution
## Problem Understanding

We start with a collection of balls colored red, yellow, and green, with counts `a`, `b`, and `c`. We are allowed to repeatedly pick any single ball and repaint it into one of the other two colors. Each repaint operation changes only one ball and only its color, while the total number of balls stays fixed.

The goal is to reach a configuration where exactly two colors remain present and those two colors appear in equal quantity. In other words, after all repainting, one of the colors must disappear entirely, and the remaining two colors must each contain exactly half of all balls.

The total number of balls is fixed as `N = a + b + c`. If we end up using exactly two colors with equal counts, each must contain `N / 2` balls, so `N` must be even. This already introduces a structural constraint: if the total number of balls is odd, no sequence of repainting can produce two equal integer-sized groups.

The bounds allow each of `a`, `b`, and `c` to be as large as one million. This makes any approach that simulates repainting or tries all configurations over individual balls impossible, since the total number of balls can reach three million. We need a solution that works in constant or logarithmic time per test case.

A few subtle edge cases are worth keeping in mind. If all balls already belong to two colors but are uneven, such as `a = 2, b = 5, c = 4`, the answer might still be impossible because the total sum is odd. Another subtle case is when all three colors are equal, where no color elimination happens naturally, but we can still force one color to disappear optimally if the parity condition is satisfied.

## Approaches

A brute-force strategy would be to simulate repainting operations directly. At each step, we could pick a ball from a color that is currently in excess and repaint it toward a deficient color. While this eventually reaches a valid configuration when possible, the number of possible sequences grows exponentially with the number of balls. Even a single test case with a few million balls makes this completely infeasible.

A more structured view comes from reframing the final state. We are not interested in the sequence of operations, only in the final assignment of colors. The final configuration always consists of choosing exactly two colors out of three, and distributing all balls into those two colors such that each ends with exactly `N / 2` balls.

So the problem becomes: for each pair of colors, what is the minimum number of balls we must repaint to transform the initial distribution into a balanced split between those two colors?

Suppose we fix a pair, say red and yellow, and force all green balls to be reassigned into either red or yellow. The optimal strategy is to keep as many already correctly colored balls as possible. Any red ball assigned to red is already correct, and any yellow ball assigned to yellow is also correct. Green balls can never be kept, since green does not exist in the final configuration.

Thus for a chosen pair, the best possible number of already-correct balls is determined by how many red balls can stay red and how many yellow balls can stay yellow, subject to both final colors reaching exactly `N / 2`.

The key simplification is that we never need to explicitly simulate redistributions. We only need to count how many balls can remain in their original color while respecting capacity `N / 2` for each of the two chosen colors.

This reduces the problem to checking all three possible pairs of colors and taking the best outcome.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force repaint simulation | Exponential | O(1) | Too slow |
| Try 3 color pairs with greedy counting | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

We define `N = a + b + c` and `half = N / 2`.

1. If `N` is odd, return `-1` immediately. A valid final state requires two equal integer groups whose sum is `N`, which is impossible when `N` is odd.
2. Consider each possible choice of the two surviving colors: `(R, Y)`, `(R, G)`, and `(Y, G)`.
3. For a fixed pair, compute how many balls can stay in their original color. For example, if we choose `(R, Y)`, then only red balls staying red and yellow balls staying yellow contribute to the unchanged count.
4. For each color in the chosen pair, we can keep at most `min(original_count, half)` balls in that color. This is because even if a color has more than `half` balls initially, we cannot keep more than `half` of them, since the final target for that color is exactly `half`.
5. Sum these contributions to get the number of kept balls for that pair. The number of repaint operations needed is `N - kept`.
6. Take the minimum repaint cost over all three pairs.

The reason this greedy counting works is that each color’s contribution to each target bucket is independent except for the fixed capacity constraint `half`. We always prefer to keep a ball in its original color because repainting can only increase the cost, and there is no benefit to moving a correctly placed ball elsewhere when capacity is still available.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    a = int(input())
    b = int(input())
    c = int(input())

    n = a + b + c
    if n % 2 == 1:
        print(-1)
        return

    half = n // 2

    def cost(x, y):
        kept = min(x, half) + min(y, half)
        return n - kept

    ans = min(
        cost(a, b),
        cost(a, c),
        cost(b, c)
    )
    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation directly encodes the observation that only the final choice of the two surviving colors matters. The helper function `cost(x, y)` computes the optimal repaint count for a fixed pair by counting how many balls can remain in-place in those two colors. The subtraction from `n` converts preserved balls into required repaint operations.

A subtle point is that we never explicitly track the third color inside `cost`. This is intentional because every ball of the excluded color must be repainted regardless of distribution, so it does not affect the optimization between the two chosen colors.

## Worked Examples

### Sample 1

Input:

`a = 2, b = 3, c = 1`

Here `N = 6`, so `half = 3`.

| Pair | kept from first | kept from second | total kept | cost |
| --- | --- | --- | --- | --- |
| (R, Y) | min(2,3)=2 | min(3,3)=3 | 5 | 1 |
| (R, G) | 2 | 1 | 3 | 3 |
| (Y, G) | 3 | 1 | 4 | 2 |

The best choice is `(R, Y)` with cost `1`.

This shows that even though green exists, it is optimal to eliminate it and balance the other two colors.

### Sample 2

Input:

`a = 2, b = 5, c = 4`

Here `N = 11`, which is odd.

Since `half` would not be an integer, it is impossible to split all balls into two equal groups. No sequence of repainting can change parity, so the output is `-1`.

This case confirms that parity is a hard feasibility constraint independent of redistribution logic.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only constant arithmetic and three fixed cases are evaluated |
| Space | O(1) | No auxiliary structures beyond a few integers |

The solution easily fits within constraints because all computations are direct formula evaluations without iteration over balls or states.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    a = int(sys.stdin.readline())
    b = int(sys.stdin.readline())
    c = int(sys.stdin.readline())

    n = a + b + c
    if n % 2 == 1:
        return "-1\n"

    half = n // 2

    def cost(x, y):
        kept = min(x, half) + min(y, half)
        return str(n - kept) + "\n"

    ans = min(
        int(cost(a, b)),
        int(cost(a, c)),
        int(cost(b, c))
    )
    return str(ans) + "\n"

# provided samples
assert run("2\n3\n1\n") == "1\n"
assert run("2\n5\n4\n") == "-1\n"
assert run("10\n10\n10\n") == "10\n"

# custom cases
assert run("1\n1\n1\n") == "-1\n", "odd total impossible"
assert run("4\n4\n0\n") == "0\n", "already balanced two colors"
assert run("6\n1\n5\n") == "1\n", "optimal elimination of smallest imbalance"
assert run("1000000\n1000000\n1000000\n") == "1000000\n", "max boundary"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1,1,1 | -1 | parity failure |
| 4,4,0 | 0 | already valid configuration |
| 6,1,5 | 1 | non-trivial balancing choice |
| 1e6,1e6,1e6 | 1e6 | performance and scaling correctness |

## Edge Cases

When all three colors are present and the total is odd, such as `2, 5, 4`, the algorithm immediately rejects the case because no redistribution can fix parity. The computation never proceeds to pair evaluation, so there is no risk of producing a misleading minimum.

When one color is zero, for example `4, 4, 0`, the pair `(R, Y)` yields `min(4,4) + min(4,4) = 8`, so cost is zero. This correctly reflects that the system already satisfies the requirement without any repainting.

When all values are equal, such as `10, 10, 10`, each pair behaves symmetrically and the result depends only on capacity `half`. The algorithm naturally converges to repainting exactly one full color group worth of balls, which matches the optimal redistribution strategy.
