---
title: "CF 103486M - Sequence"
description: "We are given a sequence of integers and asked to compute a single derived value based on its spread. The “interesting value” is defined as the product of two quantities: the length of the sequence and the range of the sequence, where the range is the difference between the…"
date: "2026-07-03T06:22:45+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103486
codeforces_index: "M"
codeforces_contest_name: "The 15th Jilin Provincial Collegiate Programming Contest"
rating: 0
weight: 103486
solve_time_s: 40
verified: true
draft: false
---

[CF 103486M - Sequence](https://codeforces.com/problemset/problem/103486/M)

**Rating:** -  
**Tags:** -  
**Solve time:** 40s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of integers and asked to compute a single derived value based on its spread. The “interesting value” is defined as the product of two quantities: the length of the sequence and the range of the sequence, where the range is the difference between the largest and smallest element.

So the task reduces to reading all values, identifying the minimum and maximum element, computing their difference, and multiplying that difference by the number of elements.

The constraints are small enough that a single linear scan is sufficient. With up to 10,000 elements, any solution that inspects each element a constant number of times is easily fast enough. Even a few million primitive operations is trivial under a 0.5 second limit in Python if implemented cleanly.

There is one subtle pitfall that can trip up careless implementations: integer range and sign handling. Since values can be negative, the minimum may be negative and the maximum positive, and the range can become large. For example, if the array is `[-100000, 100000]`, the range is `200000`, and multiplying by `n` must be done after computing the correct extremes, not during scanning with partial assumptions.

Another edge case is a single-element array. If `n = 1`, then both maximum and minimum are equal, the range is zero, and the answer must be zero regardless of the value itself. Any implementation that incorrectly initializes min or max without using the first element properly may break here.

## Approaches

A brute-force interpretation might try to compute the range for every possible substructure or repeatedly recompute extrema, but that is unnecessary because the sequence is fixed and we only need global minimum and maximum once.

The straightforward brute idea is: for each element, compare it with all others to determine min and max. That leads to an O(n²) approach because each of the n elements participates in n comparisons. While correct, it is far beyond what is needed and wastes work by recomputing the same global properties repeatedly.

The key observation is that range depends only on two values: the minimum and the maximum of the entire sequence. Once those are known, no other structure matters. This collapses the problem from pairwise comparisons into a single pass accumulation problem.

We can maintain running minimum and maximum while scanning the array once. Each new element updates either the current minimum or maximum in constant time. After the scan, we compute `(max - min) * n`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Single Pass Min/Max | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the integer `n`, which determines how many values we will process. This also defines the multiplier in the final answer.
2. Initialize two variables `mn` and `mx` using the first element of the sequence. This avoids incorrect sentinel values and ensures correctness even when all numbers are negative or identical.
3. Iterate through the remaining elements of the sequence. For each element, compare it against `mn` and update `mn` if it is smaller. Do the same for `mx` if it is larger. This maintains correct global extrema at every step.
4. After processing all elements, compute the range as `mx - mn`. This works because `mx` and `mn` now represent the true maximum and minimum of the full sequence.
5. Multiply the range by `n` to obtain the final “interesting value” and output it.

### Why it works

At every point in the iteration, `mn` and `mx` are exactly the minimum and maximum of the prefix processed so far. This invariant holds because each new element is either ignored or replaces one of them if it extends the boundary. After the final element, the prefix is the entire array, so `mn` and `mx` are the true global extrema. Since the range depends only on these extrema and is independent of ordering, the final computation is exact.

## Python Solution

```python
import sys
input = sys.stdin.readline

n_and_rest = sys.stdin.read().strip().split()
n = int(n_and_rest[0])
arr = list(map(int, n_and_rest[1:]))

mn = arr[0]
mx = arr[0]

for x in arr[1:]:
    if x < mn:
        mn = x
    if x > mx:
        mx = x

answer = (mx - mn) * n
print(answer)
```

The solution reads all input at once to avoid overhead from repeated input calls. This is not strictly required for n up to 10,000 but keeps the implementation clean and robust.

The initialization of `mn` and `mx` from the first element is critical. Using placeholders like `float('inf')` works, but directly anchoring to the array avoids edge-case mistakes and keeps comparisons consistent across integer types.

The final multiplication is done after computing the range, ensuring that intermediate values do not affect correctness.

## Worked Examples

### Example 1

Input:

`n = 3`, array = `[-1, 2, 4]`

| Step | Current Value | mn | mx |
| --- | --- | --- | --- |
| Start | -1 | -1 | -1 |
| Process 2 | 2 | -1 | 2 |
| Process 4 | 4 | -1 | 4 |

Final computation: range = 4 - (-1) = 5, answer = 5 * 3 = 15

This trace shows how the running extrema evolve and how negative values correctly influence the range.

### Example 2

Input:

`n = 5`, array = `[7, 7, 7, 7, 7]`

| Step | Current Value | mn | mx |
| --- | --- | --- | --- |
| Start | 7 | 7 | 7 |
| All others | 7 | 7 | 7 |

Final computation: range = 0, answer = 0

This demonstrates the degenerate case where all values are equal and ensures the algorithm correctly collapses to zero.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each element is visited once to maintain min and max |
| Space | O(1) | Only two variables are used regardless of input size |

The constraints allow up to 10,000 elements, and a single linear scan with constant work per element is comfortably within the time limit. Memory usage is constant, so it is negligible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from builtins import input as _input
    # inline solution
    data = inp.strip().split()
    n = int(data[0])
    arr = list(map(int, data[1:]))

    mn = arr[0]
    mx = arr[0]

    for x in arr[1:]:
        if x < mn:
            mn = x
        if x > mx:
            mx = x

    return str((mx - mn) * n)

assert run("3 -1 2 4") == "15"

# single element
assert run("1 42") == "0"

# all equal
assert run("5 7 7 7 7 7") == "0"

# strictly decreasing
assert run("4 10 5 0 -5") == str((10 - (-5)) * 4)

# already sorted increasing
assert run("4 1 2 3 4") == str((4 - 1) * 4)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 42` | `0` | Single element edge case |
| `5 7 7 7 7 7` | `0` | Constant sequence |
| `4 10 5 0 -5` | `60` | Negative minimum handling |
| `4 1 2 3 4` | `12` | Normal increasing sequence |

## Edge Cases

For a single-element input like `1 100000`, the algorithm initializes both `mn` and `mx` to `100000`. No updates occur during iteration. The range becomes `0`, and multiplying by `n` still yields `0`, matching the definition that a single value has zero spread.

For a fully negative sequence such as `3 -5 -2 -10`, the running minimum becomes `-10` and the maximum becomes `-2`. The range is `8`, and the answer is `24`. The algorithm correctly avoids any assumption that values must be positive, since all comparisons are purely relational.

For a mixed extreme sequence like `2 -100000 100000`, `mn` becomes `-100000` and `mx` becomes `100000`, producing a range of `200000`. The multiplication by `n` gives `400000`, and this confirms that no overflow or sign handling issue occurs because all operations remain within Python’s arbitrary precision integer arithmetic.
