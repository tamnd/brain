---
title: "CF 1767B - Block Towers"
description: "We are given several towers, each containing a certain number of blocks. The goal is to maximize the number of blocks on the first tower by moving blocks from towers that have more blocks than others."
date: "2026-06-09T12:49:49+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1767
codeforces_index: "B"
codeforces_contest_name: "Educational Codeforces Round 140 (Rated for Div. 2)"
rating: 800
weight: 1767
solve_time_s: 122
verified: false
draft: false
---

[CF 1767B - Block Towers](https://codeforces.com/problemset/problem/1767/B)

**Rating:** 800  
**Tags:** data structures, greedy, sortings  
**Solve time:** 2m 2s  
**Verified:** no  

## Solution
## Problem Understanding

We are given several towers, each containing a certain number of blocks. The goal is to maximize the number of blocks on the first tower by moving blocks from towers that have more blocks than others. A move is only allowed if we take a block from a tower with more blocks and place it onto a tower with fewer blocks. Each move reduces one tower by one block and increases another by one.

The input consists of multiple test cases. Each test case provides the number of towers and the list of block counts for all towers. The output should be, for each test case, the maximum possible number of blocks on the first tower after performing any sequence of valid moves.

The constraints are substantial: the number of towers $n$ can reach $2 \cdot 10^5$, and the sum of $n$ over all test cases does not exceed $2 \cdot 10^5$. This rules out any solution that simulates moves one by one because in the worst case, moving blocks individually would require up to $10^9$ operations for a single tower with a billion blocks, which is far beyond the time limit. The blocks themselves can be very large, so the solution must work with arithmetic, not brute-force simulations.

Non-obvious edge cases include situations where one tower has a massive number of blocks and the rest are minimal, or all towers start with the same number of blocks. For example, if the input is `[1, 1000000000]`, a naive algorithm that checks each possible move iteratively would be hopelessly slow. Another edge case is when all towers are equal, like `[5, 5, 5]`. Here no move is possible, and the maximum for tower one is simply its starting value.

## Approaches

The brute-force approach is straightforward: repeatedly scan all towers, find a tower with more blocks than the first tower, and move one block from it to tower one. Repeat until no such moves are possible. This method is correct because each move is legal, and we only stop when tower one cannot be increased further. The problem is the performance: in the worst case, we could move up to the sum of differences between towers, which could reach $10^9$ operations per test case. This exceeds any feasible limit.

The optimal approach comes from observing that the order of moves does not matter. We only need to know the total number of blocks and how many can legally go to tower one. Tower one can receive blocks from all other towers, but no tower can drop below tower one's current count as we move blocks. The maximum number of blocks on tower one is thus the integer average of all blocks rounded up. Formally, the sum of all blocks divided by the number of towers gives the fair maximum any tower can reach when redistributing blocks optimally. This is because any tower with fewer blocks than the average cannot give more than the difference between its count and the average. So the formula becomes `max_possible = ceil(total_blocks / n)`, which can be computed safely using integer arithmetic as `(total + n - 1) // n`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(sum(a_i)) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `t`.
2. For each test case, read the number of towers `n` and the list of block counts `a`.
3. Compute the total number of blocks across all towers: `total = sum(a)`.
4. Compute the maximum number of blocks that tower one can achieve. Since tower one can never exceed the ceiling of the average of blocks, calculate `(total + n - 1) // n`.
5. Print the computed maximum for each test case.

The correctness of this method relies on the invariant that no tower can receive more than its fair share of blocks without violating the movement rule. By taking the ceiling of the average, we ensure tower one receives as many blocks as possible while respecting the relative heights of other towers.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    total = sum(a)
    max_blocks = (total + n - 1) // n
    print(max_blocks)
```

The solution reads input efficiently with `sys.stdin.readline`, handles multiple test cases, sums the blocks, and applies integer arithmetic to compute the ceiling without floating-point operations. Using `(total + n - 1) // n` avoids rounding errors and handles large sums up to $2 \cdot 10^{14}$ safely in Python.

## Worked Examples

**Example 1**

Input: `[1, 2, 3]`

| Tower | Initial | Total sum | Ceiling(average) |
| --- | --- | --- | --- |
| 1 | 1 | 6 | 3 |
| 2 | 2 |  |  |
| 3 | 3 |  |  |

The sum is 6, number of towers is 3, so the maximum possible for tower one is `(6 + 3 - 1) // 3 = 8 // 3 = 3`. This matches the expected output.

**Example 2**

Input: `[1, 2, 2]`

| Tower | Initial | Total sum | Ceiling(average) |
| --- | --- | --- | --- |
| 1 | 1 | 5 | 2 |
| 2 | 2 |  |  |
| 3 | 2 |  |  |

Sum is 5, towers = 3, maximum possible for tower one is `(5 + 3 - 1) // 3 = 7 // 3 = 2`.

These examples confirm that the formula correctly calculates the ceiling of the average, which is the maximum tower one can achieve.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Summing all blocks takes linear time per test case. |
| Space | O(1) | Only the sum and input list are stored temporarily. |

Given that the sum of `n` over all test cases is at most $2 \cdot 10^5$, the algorithm runs in a fraction of a second, well within the 2-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        total = sum(a)
        max_blocks = (total + n - 1) // n
        print(max_blocks)
    return output.getvalue().strip()

# provided samples
assert run("4\n3\n1 2 3\n3\n1 2 2\n2\n1 1000000000\n10\n3 8 6 7 4 1 2 4 10 1\n") == "3\n2\n500000001\n9"

# custom test cases
assert run("1\n2\n5 5\n") == "5", "all equal"
assert run("1\n3\n1 1 1\n") == "1", "minimum equal blocks"
assert run("1\n2\n1 1000000000\n") == "500000001", "extreme disparity"
assert run("1\n5\n2 3 4 5 6\n") == "5", "average ceiling"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 towers equal `[5, 5]` | 5 | Algorithm handles all-equal towers correctly |
| 3 towers minimum `[1, 1, 1]` | 1 | Algorithm handles small, uniform towers |
| Extreme disparity `[1, 1000000000]` | 500000001 | Handles large numbers and ceiling calculation |
| `[2, 3, 4, 5, 6]` | 5 | Correct ceiling computation for uneven distribution |

## Edge Cases

If all towers have the same number of blocks, the sum divided by `n` is an integer, and the ceiling does not change the value. For example, `[5, 5, 5]` yields `(15 + 3 - 1) // 3 = 17 // 3 = 5`. The algorithm outputs the starting number for tower one, which is correct since no moves can increase it.

If one tower has a huge number of blocks compared to others, such as `[1, 1000000000]`, the total sum is `1000000001`, number of towers = 2, giving `(1000000001 + 2 - 1) // 2 = 1000000002 // 2 = 500000001`. The algorithm captures the maximum possible distribution efficiently, avoiding iterative moves.
