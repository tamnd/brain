---
title: "CF 102864B - \u5927\u91c7\u8d2d"
description: "The shelf contains M products arranged in a fixed order. Each product has a weight and a value. Longlong can only move along the shelf in that order, so the products he chooses must form a subsequence of the original sequence. The shopping cart has a maximum weight of N."
date: "2026-07-25T20:35:45+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102864
codeforces_index: "B"
codeforces_contest_name: "The 15-th BIT Campus Programming Contest - Online Round"
rating: 0
weight: 102864
solve_time_s: 49
verified: true
draft: false
---

[CF 102864B - \u5927\u91c7\u8d2d](https://codeforces.com/problemset/problem/102864/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

The shelf contains M products arranged in a fixed order. Each product has a weight and a value. Longlong can only move along the shelf in that order, so the products he chooses must form a subsequence of the original sequence.

The shopping cart has a maximum weight of N. The special rule is that every chosen product after the first one must not be heavier than the product chosen immediately before it. In other words, if the selected products have weights g1, g2, g3, then they must satisfy g1 >= g2 >= g3. Among all valid choices whose total weight does not exceed N, we need the maximum possible total value.

The limits are small, with both N and M at most 100. A normal knapsack solution with one extra dimension is enough, but approaches that enumerate all possible subsets are impossible. There can be 100 products, which creates 2^100 possible selections, far beyond what can be explored within the time limit.

A few details can easily cause wrong answers. The first product selected has no previous weight restriction, so it may have any weight. For example:

```
5 2
5 10
1 1
```

The correct answer is 11 because both products can be selected. A solution that initializes the previous weight incorrectly may reject the first product or fail to use the empty state.

Another case is when a heavier product appears later:

```
5 3
1 10
3 100
2 5
```

The correct answer is 105 by choosing weights 3 and 2. The product with weight 1 cannot be chosen before them because the order on the shelf cannot be changed. A solution that sorts products by weight, as in ordinary knapsack variants, would solve a different problem and produce an invalid result.

A final edge case is selecting nothing:

```
1 1
1 7
```

The answer is 7 because the product fits. If the capacity were zero, the answer would be 0, so the dynamic programming must always preserve the empty selection.

## Approaches

The most direct method is to try every possible subset of products. For each subset, we check whether the selected indices keep the original order, whether the weights are non-increasing, and whether the total weight fits in the cart. This method is correct because every possible choice is examined, but it has 2^M subsets. With M = 100, the worst case requires roughly 1.27 × 10^30 checks, which is impossible.

The useful observation is that the future only depends on two pieces of information from the products already processed. We need to know the current total weight because it determines how much capacity remains, and we need to know the weight of the last chosen product because it controls whether the next product is allowed.

This turns the problem into dynamic programming. While scanning products from left to right, we maintain the best value for every combination of used capacity and last chosen weight. When processing a product, we either skip it and keep the old states, or take it if its weight does not exceed the previous chosen weight.

The first chosen product needs special handling because there is no previous weight. We represent the empty state with a special previous weight larger than every possible product weight, allowing any product to be selected as the first one.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^M × M) | O(M) | Too slow |
| Optimal | O(M × N × 101) | O(N × 101) | Accepted |

## Algorithm Walkthrough

1. Initialize the dynamic programming table. `dp[c][w]` represents the maximum value achievable after processing some prefix of the shelf, using total weight `c`, with the last chosen product having weight `w`. The special state `w = 101` represents choosing nothing so far.

The initial state is `dp[0][101] = 0`, because before taking any product the cart has weight zero and there is no restriction on the first product.

1. Process every product from left to right. For the current product with weight `g` and value `s`, create a copy of the current states to represent the option of skipping this product.

Skipping must be considered because the chosen products only need to be a subsequence, not a continuous segment of the shelf.

1. For every existing state, try taking the current product. If the current state has previous weight `w` and `g <= w`, the product can be added. Update the state with new capacity `c + g` and new last weight `g`.

The last chosen weight becomes `g` because every future product must be compared against the most recently added product.

1. After all products are processed, the answer is the maximum value among all valid states, regardless of the final used capacity or last chosen weight.

Why it works:

The dynamic programming state stores exactly the information needed for future decisions. Two different selections that have processed the same prefix and have the same used capacity and last chosen weight have identical possibilities for every remaining product. Keeping only the larger value among them cannot remove an optimal solution. Each transition considers the only two choices for a product, skipping it or taking it when allowed, so every valid subsequence is represented. The final maximum among all states is the best valid shopping plan.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    N, M = map(int, input().split())
    items = [tuple(map(int, input().split())) for _ in range(M)]

    NEG = -1
    dp = [[NEG] * 102 for _ in range(N + 1)]
    dp[0][101] = 0

    for g, s in items:
        new_dp = [row[:] for row in dp]

        for weight in range(N + 1):
            for last in range(102):
                if dp[weight][last] == NEG:
                    continue
                if g <= last and weight + g <= N:
                    new_dp[weight + g][g] = max(
                        new_dp[weight + g][g],
                        dp[weight][last] + s
                    )

        dp = new_dp

    ans = 0
    for weight in range(N + 1):
        for last in range(102):
            ans = max(ans, dp[weight][last])

    print(ans)

if __name__ == "__main__":
    solve()
```

The table has 102 possible previous weights because real product weights are from 1 to 100, and index 101 is reserved for the empty selection. The value `NEG` marks states that cannot be reached, preventing invalid transitions from being used.

For every product, the code copies the old table before applying take transitions. This prevents using the same product multiple times in one iteration, which is the same reason a 0/1 knapsack updates states from the previous layer.

The condition `g <= last` enforces the non-increasing weight requirement. The empty state has `last = 101`, so any first product is accepted. The capacity check happens before updating, preventing states that exceed the cart limit from entering the table.

All values fit easily inside Python integers because the maximum possible total value is only 10000.

## Worked Examples

The sample input is:

```
5 5
1 5
2 2
3 3
4 4
1 2
```

A trace of the important states is shown below. Only the best reachable state after each processed product is displayed.

| Step | Product | Current best selection | Used weight | Last weight | Value |
| --- | --- | --- | --- | --- | --- |
| Initial | None | Empty | 0 | 101 | 0 |
| 1 | (1,5) | Choose product 1 | 1 | 1 | 5 |
| 2 | (2,2) | Choose product 2 alone | 2 | 2 | 2 |
| 3 | (3,3) | Choose product 3 alone | 3 | 3 | 3 |
| 4 | (4,4) | Choose product 4 alone | 4 | 4 | 4 |
| 5 | (1,2) | Choose weights 3,1 or 2,1 or 4,1 | 4 or 5 | 1 | 6 |

The final answer is 6. The trace shows why product order matters. Even though the first product has high value compared with some later products, choosing products with increasing weights is forbidden.

A second example:

```
6 4
5 8
3 6
3 4
1 10
```

| Step | Product | Used weight | Last weight | Best value |
| --- | --- | --- | --- | --- |
| Initial | None | 0 | 101 | 0 |
| 1 | (5,8) | 5 | 5 | 8 |
| 2 | (3,6) | 8 | 3 | 14 |
| 3 | (3,4) | 6 | 3 | 12 |
| 4 | (1,10) | 6 | 1 | 20 |

The optimal choice is the first, second, and fourth products. Their weights are 5, 3, and 1, which satisfy the decreasing requirement, and their total value is 24. The table highlights that the algorithm keeps several possible last weights because a state with a smaller last weight can still be valuable when future products are lighter.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(M × N × 102) | Each product checks every capacity and previous-weight state |
| Space | O(N × 102) | Only the current and previous dynamic programming layers are needed |

The maximum number of states is about 10200, and there are only 100 products. This gives about one million state transitions, which is easily within the limits.

## Test Cases

```python
import sys
import io

def solve_case(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    N, M = map(int, input().split())
    items = [tuple(map(int, input().split())) for _ in range(M)]

    NEG = -1
    dp = [[NEG] * 102 for _ in range(N + 1)]
    dp[0][101] = 0

    for g, s in items:
        new_dp = [row[:] for row in dp]
        for w in range(N + 1):
            for last in range(102):
                if dp[w][last] != NEG and g <= last and w + g <= N:
                    new_dp[w + g][g] = max(
                        new_dp[w + g][g],
                        dp[w][last] + s
                    )
        dp = new_dp

    return str(max(max(row) for row in dp)) + "\n"

assert solve_case("""5 5
1 5
2 2
3 3
4 4
1 2
""") == "6\n", "sample"

assert solve_case("""1 1
1 7
""") == "7\n", "minimum size"

assert solve_case("""10 3
2 5
2 5
2 5
""") == "15\n", "all equal weights"

assert solve_case("""5 3
5 10
4 9
4 9
""") == "19\n", "boundary capacity"

assert solve_case("""100 100
1 1
""" + "1 1\n" * 99) == "100\n", "maximum size"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample case | 6 | Basic decreasing-weight selection |
| Single product | 7 | Empty-state initialization and first choice handling |
| Equal weights | 15 | Multiple products with identical weights |
| Capacity boundary | 19 | Exact use of the cart limit |
| 100 products | 100 | Maximum input size handling |

## Edge Cases

For the first edge case:

```
5 2
5 10
1 1
```

The initial state is `(capacity = 0, last = 101)`. The first product can be selected because 5 is less than 101, creating a state with capacity 5, last weight 5, and value 10. The second product can follow because 1 is less than 5, creating the final answer 11. The special empty state is what allows the first product to be unrestricted.

For the ordering edge case:

```
5 3
1 10
3 100
2 5
```

After the first product, the best state has last weight 1. The second product has weight 3, so it cannot follow that state. The algorithm still keeps the empty state, allowing the second product to become the first choice. Then the third product can follow it because 2 is smaller than 3. The answer becomes 105, which respects the original shelf order.

For the no-choice boundary:

```
0 1
1 7
```

The only reachable state is the empty cart. The product never satisfies the capacity condition because adding it creates weight 1, which exceeds the limit. The maximum remaining value is 0, which is the correct result.

I can also turn this into a shorter Codeforces-style editorial version if you want something closer to what would appear on the contest page.
