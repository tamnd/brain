---
title: "CF 105271A - ACC triangle"
description: "We are given two types of resources: one type represents single “A” pieces and the other represents “C” pieces. Using these, we want to build a triangular structure where row i contains exactly one A followed by i−1 C’s. So the structure grows row by row."
date: "2026-06-23T06:57:57+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105271
codeforces_index: "A"
codeforces_contest_name: "Almaty Code Cup 2024"
rating: 0
weight: 105271
solve_time_s: 52
verified: true
draft: false
---

[CF 105271A - ACC triangle](https://codeforces.com/problemset/problem/105271/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 52s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two types of resources: one type represents single “A” pieces and the other represents “C” pieces. Using these, we want to build a triangular structure where row i contains exactly one A followed by i−1 C’s.

So the structure grows row by row. The first row needs 1 A and 0 C. The second row needs 1 A and 1 C. The third row needs 1 A and 2 C, and so on. Every additional row increases the number of required C’s, while always consuming exactly one A.

The task is to determine the maximum height h such that all rows from 1 to h can be built without exceeding the available x A’s and y C’s.

The constraint x, y ≤ 10^18 forces the solution to avoid any simulation over rows. A linear construction would require up to 10^18 iterations in the worst case, which is impossible in one second. Even logarithmic per-test overhead is fine, but anything depending on h directly is not.

A subtle failure case comes from greedy row construction without planning. For example, if x is large but y is small, a naive approach might try to build until C’s run out per row, but miscount the cumulative C usage. Another issue is forgetting that A usage is strictly linear in height while C usage grows quadratically.

For instance, if x = 10 and y = 3, a naive row-by-row approach might attempt 4 rows because A’s allow it, but row 4 would require 6 C’s in total, which is impossible.

## Approaches

A direct simulation builds rows one by one. For each row i, we subtract one A and i−1 C’s from the available pool. This works because the structure is deterministic, so we can greedily construct until resources are exhausted. However, in the worst case the number of rows can be as large as 10^9 or more, making this infeasible.

The key observation is that resource consumption depends only on the height h, not on intermediate choices. After building h rows, total A usage is exactly h, and total C usage is the sum 0 + 1 + 2 + ... + (h−1), which equals h(h−1)/2. This transforms the problem into checking feasibility of a single h.

Now the task becomes finding the maximum h such that both constraints hold: h ≤ x and h(h−1)/2 ≤ y. The first constraint is linear, the second is quadratic. The quadratic constraint can be solved directly using a closed-form expression derived from the inequality, so no binary search is required.

We compute the largest h satisfying h(h−1)/2 ≤ y using the quadratic formula and then take the minimum with x.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(h) | O(1) | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute the maximum possible height limited only by A’s. This is simply x, since each row consumes exactly one A.
2. Compute the maximum height allowed by C’s by solving the inequality h(h−1)/2 ≤ y. This comes from summing the required C’s across all rows.
3. Rearrange the inequality into h² − h − 2y ≤ 0, which is a standard quadratic constraint.
4. Compute the positive root of the corresponding equation h = (1 + sqrt(1 + 8y)) / 2 and take its floor. This gives the largest integer h that does not violate the C constraint.
5. The final answer is the smaller of the two limits: one from A’s and one from C’s.

### Why it works

The structure enforces that each row independently consumes exactly one A, so A usage is linear in height. The C requirement accumulates deterministically as a prefix sum, so any valid height is fully characterized by a single scalar inequality. Because both constraints are monotone in h, once a height becomes invalid, all larger heights are also invalid, ensuring the computed maximum is globally optimal.

## Python Solution

```python
import sys
import math
input = sys.stdin.readline

def solve():
    x, y = map(int, input().split())
    
    # limit from A's
    h_a = x
    
    # limit from C's: h(h-1)/2 <= y
    # solve h^2 - h - 2y <= 0
    disc = 1 + 8 * y
    h_c = (1 + math.isqrt(disc)) // 2
    
    print(min(h_a, h_c))

if __name__ == "__main__":
    solve()
```

The implementation separates the two constraints cleanly. The A constraint is direct since each row consumes exactly one A. The C constraint is handled using integer square root to avoid floating-point precision issues, since y can be as large as 10^18. Using `math.isqrt` ensures exact integer arithmetic.

The final `min` combines both constraints because a valid triangle must satisfy both simultaneously.

## Worked Examples

### Example 1

Input: x = 4, y = 6

| Step | h from A | h from C | Current answer |
| --- | --- | --- | --- |
| compute limits | 4 | solve h(h−1)/2 ≤ 6 → h = 4 | 4 |

Here, both constraints allow height 4. Checking C usage: 0+1+2+3 = 6, exactly matching available C’s, so full height is achievable.

### Example 2

Input: x = 4, y = 5

| Step | h from A | h from C | Current answer |
| --- | --- | --- | --- |
| compute limits | 4 | solve h(h−1)/2 ≤ 5 → h = 3 | 3 |

Even though A’s allow 4 rows, C’s break at height 4 since it requires 6 C’s. The limiting factor is therefore C, and the answer becomes 3.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only arithmetic operations and one integer square root |
| Space | O(1) | No additional data structures |

The solution comfortably fits within constraints since it performs constant-time computation regardless of input size up to 10^18.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import isqrt

    x, y = map(int, input().split())
    h_a = x
    disc = 1 + 8 * y
    h_c = (1 + isqrt(disc)) // 2
    return str(min(h_a, h_c))

# provided samples (interpreted)
assert run("4 6") == "4"
assert run("4 5") == "3"

# minimum case
assert run("1 0") == "1"

# only C limits
assert run("1000000000000000000 0") == "1"

# tight triangular C bound
assert run("10 45") == "10"

# x limits strongly
assert run("3 1000000000000000000") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 0 | 1 | minimum resources |
| 10^18 0 | 1 | C = 0 extreme case |
| 10 45 | 10 | perfect triangular number |
| 3 10^18 | 3 | A constraint dominates |

## Edge Cases

One edge case is when y = 0. In this case, only rows that require no C’s are possible. That means only the first row can exist regardless of x. The formula gives disc = 1, so h_c = 1, and the final answer becomes min(x, 1), which is correct.

Another edge case is when x is much smaller than the C-limited height. For example x = 2 and y is extremely large. The C formula may yield a large h_c, but the final answer correctly caps at 2 since A’s are consumed linearly and immediately become the bottleneck.

A third case is when y exactly matches a triangular number. For y = 6, the formula yields h_c = 4 exactly because 1 + 2 + 3 = 6, confirming that equality boundaries are handled without off-by-one errors due to integer square root flooring behavior.
