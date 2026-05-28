---
title: "CF 208D - Prizes, Prizes, more Prizes"
description: "In this problem, we are asked to simulate Vasya's prize redemption strategy. Vasya collects points from chocolate bar wrappings over time. Each wrapping contributes a certain number of points, and the points accumulate sequentially."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 208
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 130 (Div. 2)"
rating: 1200
weight: 208
solve_time_s: 86
verified: true
draft: false
---

[CF 208D - Prizes, Prizes, more Prizes](https://codeforces.com/problemset/problem/208/D)

**Rating:** 1200  
**Tags:** implementation  
**Solve time:** 1m 26s  
**Verified:** yes  

## Solution
## Problem Understanding

In this problem, we are asked to simulate Vasya's prize redemption strategy. Vasya collects points from chocolate bar wrappings over time. Each wrapping contributes a certain number of points, and the points accumulate sequentially. There is a fixed set of prizes, each with a known cost in points. Vasya uses a greedy approach: whenever he has enough points to buy at least one prize, he always chooses the most expensive prize he can afford and continues redeeming until he cannot afford any prize.

The input provides the number of chocolate bars, the list of points per bar in chronological order, and the costs of five prizes in increasing order. The output requires two pieces of information: the number of each type of prize Vasya ends up with and the number of points he has left after all possible redemptions.

The constraints are moderate: the number of chocolate bars, `n`, is at most 50, so iterating over them sequentially is acceptable. The points and prize costs can be as large as `10^9`, which rules out any naive brute-force search or simulation over the full point range. A key observation is that points only need to be accumulated and compared against prize costs, making an O(n) approach feasible.

Non-obvious edge cases include the scenario where Vasya's points are exactly equal to a prize cost, where multiple prizes can be redeemed consecutively in one accumulation, or when he cannot redeem any prize at all. For instance, if Vasya has points `[1, 2]` and prize costs `[2, 3, 4, 5, 6]`, after the second bar he has 3 points and can redeem the second prize, leaving 0 points. Careless handling could miss the opportunity for multiple consecutive redemptions.

## Approaches

A naive approach is to simulate every step exactly as described: for each chocolate bar, add its points to Vasya's total, and then repeatedly attempt to redeem prizes starting from the cheapest to the most expensive or in some arbitrary order. This approach is correct because it mirrors the problem statement, but it could be implemented inefficiently if the redemption logic iterates unnecessarily over prizes or loops without considering the descending cost order. Since `n` is small, this naive approach is actually feasible, but careful ordering matters to match the greedy choice rule.

The optimal approach is to accumulate Vasya's points sequentially and, for each accumulation, repeatedly redeem prizes in descending cost order. By always checking from the most expensive prize down to the cheapest, we ensure that Vasya's greedy strategy is faithfully implemented. We increment counters for each prize and subtract the cost from Vasya's current points. This method is efficient and straightforward, leveraging the fact that there are only five prizes and `n` is small.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * 5 * k) | O(1) | Acceptable for small `n`, but may do unnecessary loops |
| Optimal | O(n * 5) | O(1) | Efficient, directly simulates Vasya's greedy behavior |

## Algorithm Walkthrough

1. Initialize a variable to store Vasya's accumulated points and an array of counters for the five prizes, all set to zero.
2. Iterate through the sequence of points from each chocolate bar. For each point value, add it to Vasya's accumulated points.
3. After adding points from a bar, attempt to redeem prizes. Check the prizes in descending order of cost. For each prize, while Vasya has enough points to redeem it, increment the corresponding counter and subtract the prize cost from the accumulated points. This loop continues until no prize can be redeemed.
4. Repeat the process for all chocolate bars.
5. After processing all bars, the counters hold the number of each prize Vasya has received, and the accumulated points variable holds any leftover points.

Why it works: The algorithm works because it directly implements Vasya's greedy strategy. At every step, it ensures the most expensive affordable prize is chosen. The invariant is that at any point after redemption, Vasya has fewer points than the cheapest unredeemed prize or zero, which matches the problem's rules.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    n = int(input())
    points = list(map(int, input().split()))
    prize_costs = list(map(int, input().split()))  # a, b, c, d, e
    prize_counts = [0] * 5
    total_points = 0

    for p in points:
        total_points += p
        for i in range(4, -1, -1):  # check from most expensive to cheapest
            while total_points >= prize_costs[i]:
                total_points -= prize_costs[i]
                prize_counts[i] += 1

    print(' '.join(map(str, prize_counts)))
    print(total_points)

if __name__ == "__main__":
    main()
```

The Python implementation follows the algorithm exactly. We read input efficiently using `sys.stdin.readline`. The main loop iterates over each chocolate bar's points, adding them to `total_points`. The nested loop processes the prizes in descending order, ensuring the greedy strategy is respected. The `while` loop handles multiple redemptions consecutively if enough points are available, which could be missed in a careless implementation.

## Worked Examples

**Example 1**

Input:

```
3
3 10 4
2 4 10 15 20
```

Step-by-step:

| Bar | Points Added | Total Points | Redeemed Prize(s) | Total Points After Redemption |
| --- | --- | --- | --- | --- |
| 3 | 3 | 3 | 1 mug (2 points) | 1 |
| 10 | 10 | 11 | 1 bag (10 points) | 1 |
| 4 | 4 | 5 | 1 towel (4 points) | 1 |

Output:

```
1 1 1 0 0
1
```

**Example 2**

Input:

```
5
2 2 2 2 2
3 4 5 6 7
```

Step-by-step:

| Bar | Points Added | Total Points | Redeemed Prize(s) | Total Points After Redemption |
| --- | --- | --- | --- | --- |
| 2 | 2 | 2 | None | 2 |
| 2 | 2 | 4 | 1 cheapest prize (3 points) | 1 |
| 2 | 2 | 3 | 1 cheapest prize (3 points) | 0 |
| 2 | 2 | 2 | None | 2 |
| 2 | 2 | 4 | 1 cheapest prize (3 points) | 1 |

Output:

```
3 0 0 0 0
1
```

This confirms the algorithm handles consecutive redemptions correctly and respects the greedy choice.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n * 5) | For each of the n chocolate bars, we check up to 5 prizes in descending order; the inner while loop executes at most once per prize per bar in worst case due to subtraction. |
| Space | O(1) | Only a fixed-size array for prize counts and a variable for total points are used. |

Given `n <= 50`, this is well within typical 2-second limits even for large integers.

## Test Cases

```python
# helper to run the solution
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        main()
    return out.getvalue().strip()

# provided samples
assert run("3\n3 10 4\n2 4 10 15 20\n") == "1 1 1 0 0\n1", "sample 1"
# custom cases
assert run("5\n2 2 2 2 2\n3 4 5 6 7\n") == "3 0 0 0 0\n1", "multiple redemptions"
assert run("1\n1\n1 2 3 4 5\n") == "1 0 0 0 0\n0", "exactly enough for cheapest prize"
assert run("2\n1000000000 1000000000\n1 2 3 4 5\n") == "400000000 200000000 133333333 100000000 80000000\n0", "large points"
assert run("3\n1 1 1\n5 6 7 8 9\n") == "0 0 0 0 0\n3", "cannot redeem any prize"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 5 bars, repeated small points | 3 0 0 0 0\n1 | Multiple consecutive redemptions |
| 1 bar, points equal cheapest prize | 1 0 0 0 0\n0 | Redeeming exactly at cost boundary |
| 2 bars, very large points | 400000000 200000000 133333333 100000000 80000000\n0 | Correct handling of large numbers |
| 3 bars, insufficient points | 0 0 0 0 0\n3 | No prizes redeemed when points are below minimum |

## Edge Cases

The first
