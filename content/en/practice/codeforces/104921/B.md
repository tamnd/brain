---
title: "CF 104921B - Good Kid"
description: "We are given a small collection of single-digit numbers. For each test case, we are allowed to pick exactly one of these digits and increase it by one."
date: "2026-06-28T18:07:20+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104921
codeforces_index: "B"
codeforces_contest_name: "Easy_Training"
rating: 0
weight: 104921
solve_time_s: 87
verified: false
draft: false
---

[CF 104921B - Good Kid](https://codeforces.com/problemset/problem/104921/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 27s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a small collection of single-digit numbers. For each test case, we are allowed to pick exactly one of these digits and increase it by one. After that single change, we multiply all the numbers in the collection together and want this product to be as large as possible.

The structure of the input matters: each test case is independent, and each contains at most nine digits. The output for each test case is just one integer, the best possible product after applying the single allowed increment.

The constraint on n is extremely small. With n at most 9 and up to 10^4 test cases, even a solution that tries every possible choice of which digit to increment is easily fast enough. This immediately rules out any need for complex preprocessing or mathematical optimization beyond a direct simulation.

The main subtlety comes from zeros. A naive intuition might suggest that increasing the largest digit is always optimal, but this fails whenever a zero exists. A zero makes the entire product zero, so the only way to get a non-zero result is to convert at least one zero into a one. For example, with digits `[0, 5, 6]`, increasing 6 to 7 still leaves the product zero, while increasing 0 to 1 makes the product `1 * 5 * 6 = 30`, which is strictly better.

Another edge case is when all digits are zero except one. For example `[0, 0, 9]`. Increasing 9 to 10 produces product `0`, while increasing a zero gives `[1, 0, 9]`, still product `0`. In such cases, every move is equivalent, but the brute-force evaluation still correctly handles it.

A final subtle case is when all digits are non-zero and relatively large. Increasing a smaller digit can sometimes outperform increasing the largest one because multiplication is sensitive to distribution. For example `[3, 3, 3]`: increasing one 3 to 4 yields `36`, while increasing any other also yields the same, but in general mixed distributions require checking all positions.

## Approaches

The brute-force idea is straightforward: try every index, temporarily increase that digit by one, compute the product of all elements, and keep the maximum result. Each evaluation costs O(n) multiplications, and there are n choices, so each test case costs O(n²). Since n is at most 9, this is effectively constant time in practice, but it still helps to simplify.

The key observation is that the decision space is tiny. There are only n possible moves, and each move is independent. There is no need for dynamic programming or greedy reasoning because we are not making multiple decisions, only choosing a single position to modify. This collapses the problem into direct enumeration.

The optimization is therefore not about reducing asymptotic complexity but about writing the cleanest evaluation loop: compute the product for each candidate index and track the maximum.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(t · n²) | O(1) | Accepted |
| Optimal Enumeration | O(t · n²) | O(1) | Accepted |

In practice, both are identical here because n is bounded by 9.

## Algorithm Walkthrough

We process each test case independently and evaluate all possible single increments.

1. Read the array of digits for the current test case. We store it as a list so we can simulate modifications easily.
2. Initialize a variable `best` to zero. This will track the maximum product seen across all choices of which digit to increment.
3. For each index `i` in the array, simulate increasing `a[i]` by one. We do not permanently modify the array; instead, we treat it as `a[i] + 1` only for this computation. This avoids accidental carry-over effects between trials.
4. Compute the product of all elements under this modification. Every element except `i` remains unchanged, while position `i` contributes `(a[i] + 1)` instead of `a[i]`.
5. Compare this product with `best` and update `best` if it is larger. This ensures that after considering all choices, we keep the optimal one.
6. Output `best` after all indices have been tested.

### Why it works

The algorithm explicitly evaluates every valid operation allowed by the problem: choosing exactly one index to increment. Each evaluation computes the exact resulting product, so no approximation or heuristic is involved. Since the set of possible outcomes is exactly the set of these n modifications, taking the maximum over all of them guarantees correctness. There is no interaction between choices, so enumerating them independently covers the full solution space.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        best = 0

        for i in range(n):
            prod = 1
            for j in range(n):
                if i == j:
                    prod *= (a[j] + 1)
                else:
                    prod *= a[j]
            best = max(best, prod)

        print(best)

if __name__ == "__main__":
    solve()
```

The implementation mirrors the algorithm directly. The outer loop processes test cases, and the inner loop over `i` selects which digit to increment. A second inner loop computes the product for that choice.

A common implementation pitfall is modifying the array in place and forgetting to revert it, which leads to cascading incorrect results across iterations. Here, the value `(a[j] + 1)` is computed on the fly, avoiding mutation entirely.

Another subtle point is initializing `best` to zero rather than the product of the original array. Since incrementing a zero can produce a strictly better result, starting from zero safely covers all cases without special handling.

## Worked Examples

### Example 1

Input:

`[2, 1, 2, 3]`

We evaluate each possible increment.

| Index incremented | Modified array | Product |
| --- | --- | --- |
| 0 | [3, 1, 2, 3] | 18 |
| 1 | [2, 2, 2, 3] | 24 |
| 2 | [2, 1, 3, 3] | 18 |
| 3 | [2, 1, 2, 4] | 16 |

The best outcome is `24`, achieved by increasing the second element.

This shows that increasing the largest element is not always optimal, since improving the smaller middle value gives a higher product.

### Example 2

Input:

`[0, 5, 6]`

| Index incremented | Modified array | Product |
| --- | --- | --- |
| 0 | [1, 5, 6] | 30 |
| 1 | [0, 6, 6] | 0 |
| 2 | [0, 5, 7] | 0 |

The best choice is clearly to increment the zero. This demonstrates the dominance of eliminating zeros over improving already-large values.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t · n²) | For each test case, we try n possible increments, and each requires multiplying n numbers |
| Space | O(1) | Only constant extra variables beyond the input array |

Given that n ≤ 9 and t ≤ 10^4, the total number of operations is at most about 9 × 9 × 10^4, which is well within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided samples (reconstructed from statement formatting)
assert run("""4
4
2 1 2 3
1
2
5
4 3 2 3 4
9
9 9 9 9 9 9 9 9 9
""") == """24
3
432
430467210"""

# minimum size
assert run("""1
1
0
""") == "1"

# all zeros
assert run("""1
3
0 0 0
""") == "1"

# mixed zeros
assert run("""1
4
0 2 3 4
""") == "24"

# all nines
assert run("""1
3
9 9 9
""") == "900"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single zero | 1 | minimal case, increment converts 0 to 1 |
| all zeros | 1 | ensures at least one increment is always applied |
| mixed zeros | 24 | confirms zero handling dominates strategy |
| all nines | 900 | checks carry-to-10 effect handling |

## Edge Cases

A key edge case is when the array contains zero. For example, input `[0, 2, 3, 4]` produces a zero product unless the zero is incremented. The algorithm correctly evaluates the case where index 0 is incremented, yielding `[1, 2, 3, 4]` and product `24`, which dominates all other choices that still include a zero.

Another case is a single-element array `[0]`. The only move is to increment it, producing `[1]`, so the output is `1`. The algorithm handles this naturally because it still evaluates the only index and computes `(0 + 1)`.

When all digits are large, such as `[9, 9, 9]`, the increment produces a `10`, and the product becomes `900`. The algorithm correctly handles this without treating `10` specially, since integer multiplication in Python naturally supports it.

Finally, when multiple zeros exist, such as `[0, 0, 5]`, any single increment still leaves at least one zero, so most outcomes are zero except when incrementing a zero. The algorithm still compares all cases uniformly and selects the correct best value without needing special-case logic.
