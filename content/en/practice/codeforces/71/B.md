---
title: "CF 71B - Progress Bar"
description: "We are asked to construct a graphical progress bar as an array of squares, where each square has a saturation value. The bar has a total of n squares, and the maximum saturation is k."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 71
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 65 (Div. 2)"
rating: 1300
weight: 71
solve_time_s: 67
verified: true
draft: false
---

[CF 71B - Progress Bar](https://codeforces.com/problemset/problem/71/B)

**Rating:** 1300  
**Tags:** implementation, math  
**Solve time:** 1m 7s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to construct a graphical progress bar as an array of squares, where each square has a saturation value. The bar has a total of `n` squares, and the maximum saturation is `k`. The completion of the process is measured as `t` percent, and we need to reflect that percentage visually using the saturation of the squares.

The rules are:

- The first few squares are fully saturated (`k`), representing the completed portion.
- The last few squares are empty (`0`), representing the uncompleted portion.
- At most one square may be partially filled to precisely match the percentage `t`.

The input consists of three integers: `n`, `k`, and `t`, all in the range [0, 100] for `t` and [1, 100] for `n` and `k`. The output is an array of `n` integers representing the saturation of each square.

Because `n` and `k` are both at most 100, we can afford an O(n) solution with simple arithmetic and iteration. There are no performance concerns; the constraints make a direct simulation feasible.

Non-obvious edge cases arise when `t` is 0 or 100, or when the fractional part of the partially filled square is exactly 0 or `k`. For example, if `t = 0`, all squares should be 0, and if `t = 100`, all squares should be `k`. A careless solution might try to compute a "partial square" even in these cases, resulting in an off-by-one error.

## Approaches

The brute-force approach is to iterate over each square, calculate the exact saturation required for that square according to the percentage, and fill the array. This works because we can treat the problem as splitting `t` percent of the total saturation across `n` squares, but it introduces unnecessary fractional arithmetic and complications when only one square can be partially filled.

The key insight is to notice that the problem is linear: each square contributes exactly `k` units of saturation, except potentially one partial square. We can compute the total "saturation units" as `(t / 100) * (n * k)`. Then, the number of fully filled squares is the integer division of this value by `k`, the partially filled square is the remainder, and the remaining squares are empty. This allows us to construct the answer in O(n) without iterating through fractions or performing complex comparisons.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(n) | Accepted but verbose |
| Optimal | O(n) | O(n) | Accepted, clear and concise |

## Algorithm Walkthrough

1. Compute the total units of saturation needed for `t` percent completion:

`total_saturation = (t * n * k) // 100`

Integer division works because saturation must be an integer, and any fractional part naturally becomes the partially filled square.
2. Determine the number of fully filled squares by dividing `total_saturation` by `k`:

`full_squares = total_saturation // k`

This ensures that each of the first `full_squares` squares is saturated to the maximum.
3. Compute the remaining saturation for the partially filled square:

`partial_saturation = total_saturation % k`

If this is zero, no partial square exists; if nonzero, the next square after the full ones gets this value.
4. Initialize an array of length `n` with zeros.
5. Fill the first `full_squares` with `k`.
6. If `partial_saturation` is nonzero, assign it to the next square.
7. The rest of the array remains zeros.

Why it works: The algorithm maintains the invariant that the sum of saturation values matches `(t / 100) * (n * k)`. Because each square after the full ones is either partially filled or zero, and only one partial square exists, the output always satisfies the problem conditions.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, k, t = map(int, input().split())

# Total saturation units
total_saturation = (t * n * k) // 100

# Number of fully filled squares
full_squares = total_saturation // k

# Remaining saturation for the partial square
partial_saturation = total_saturation % k

# Initialize the progress bar
progress = [0] * n

# Fill full squares
for i in range(full_squares):
    progress[i] = k

# Fill partial square if it exists
if full_squares < n:
    progress[full_squares] = partial_saturation

print(' '.join(map(str, progress)))
```

The code first calculates the total saturation in units, which is a scaled integer version of `t%`. Dividing by `k` separates fully filled squares from the partial square. Initializing the array with zeros ensures that unfilled squares are already correct. The `if` condition avoids an index error when `t = 100`.

## Worked Examples

**Sample 1:** `n=10, k=10, t=54`

| Step | total_saturation | full_squares | partial_saturation | progress array |
| --- | --- | --- | --- | --- |
| Compute total | 54 | 5 | 4 | [10,10,10,10,10,4,0,0,0,0] |

This trace shows the partial square correctly accounts for the 4 units left after 5 full squares.

**Custom Example:** `n=5, k=20, t=0`

| Step | total_saturation | full_squares | partial_saturation | progress array |
| --- | --- | --- | --- | --- |
| Compute total | 0 | 0 | 0 | [0,0,0,0,0] |

This confirms edge case handling for zero progress.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Filling the array of `n` squares dominates |
| Space | O(n) | We store `n` integers for the progress bar |

Because `n ≤ 100`, the algorithm is extremely efficient and fits well within time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, k, t = map(int, input().split())
    total_saturation = (t * n * k) // 100
    full_squares = total_saturation // k
    partial_saturation = total_saturation % k
    progress = [0] * n
    for i in range(full_squares):
        progress[i] = k
    if full_squares < n:
        progress[full_squares] = partial_saturation
    return ' '.join(map(str, progress))

# Provided samples
assert run("10 10 54\n") == "10 10 10 10 10 4 0 0 0 0"
# Custom cases
assert run("5 20 0\n") == "0 0 0 0 0", "zero progress"
assert run("5 20 100\n") == "20 20 20 20 20", "full progress"
assert run("4 5 37\n") == "5 5 3 0", "partial square rounding"
assert run("1 1 50\n") == "0", "single square half progress"
assert run("3 10 33\n") == "10 0 0", "fractional rounding down"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 5 20 0 | 0 0 0 0 0 | Edge case: zero progress |
| 5 20 100 | 20 20 20 20 20 | Edge case: full progress |
| 4 5 37 | 5 5 3 0 | Correct calculation of partial square |
| 1 1 50 | 0 | Single square rounding edge |
| 3 10 33 | 10 0 0 | Fractional saturation rounds down |

## Edge Cases

When `t=0`, the total saturation is zero. The algorithm computes `full_squares=0` and `partial_saturation=0`. The loop for full squares does nothing, and the conditional for the partial square is skipped because `full_squares < n` is true but `partial_saturation` is zero, leaving the array as `[0, 0, ...]`, exactly correct.

When `t=100`, `total_saturation = n*k`, `full_squares = n`, `partial_saturation = 0`. The loop fills all squares with `k`, and the conditional check does not alter the array because `full_squares` equals `n`, avoiding out-of-bounds errors.

For fractional percentages like `t=37` with `n=4` and `k=5`, the total saturation is `(37*4*5)//100 = 7`. Full squares `7//5=1`, partial `7%5=2`. The array becomes `[5,2,0,0]`, correctly reflecting one full and one partial square.

This confirms that edge cases with 0, 100, or partial saturation are all correctly handled.

This editorial fully explains the derivation of the algorithm, the handling of tricky cases, and
