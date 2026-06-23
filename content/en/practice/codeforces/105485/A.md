---
title: "CF 105485A - \u6570\u7ec4"
description: "The task describes an array purely as a way to motivate indexing from zero. If an array has length $n$, its valid indices run from $0$ up to $n - 1$. The problem then asks us to output the index of the last element of such an array when only the length $n$ is given."
date: "2026-06-23T18:22:31+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105485
codeforces_index: "A"
codeforces_contest_name: "2024 China Unversity of Geosciences (Wuhan) Freshman Contest"
rating: 0
weight: 105485
solve_time_s: 54
verified: true
draft: false
---

[CF 105485A - \u6570\u7ec4](https://codeforces.com/problemset/problem/105485/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 54s  
**Verified:** yes  

## Solution
## Problem Understanding

The task describes an array purely as a way to motivate indexing from zero. If an array has length $n$, its valid indices run from $0$ up to $n - 1$. The problem then asks us to output the index of the last element of such an array when only the length $n$ is given.

So the input is a single integer representing the size of a conceptual array, and the output is the largest valid index in that array. In other words, we are converting a length into its last position under zero-based indexing.

The constraint $1 \le n \le 100$ implies that the input is extremely small, so any computation from constant time up to linear time would easily pass. However, the structure of the problem does not require iteration over elements or any simulation. The output depends only on a direct arithmetic relationship between the array size and its final index.

There are no meaningful edge cases beyond the smallest possible input. When $n = 1$, the array has a single element at index $0$, so the correct output is $0$. Any approach that incorrectly assumes indices start at one would instead output $1$, which would already be outside the valid range.

## Approaches

A naive interpretation would be to explicitly construct the idea of an array and then compute its last index by iterating over positions. One might imagine creating a sequence from $0$ to $n - 1$, then returning the final element encountered. This works correctly because it mirrors the definition of indexing, but it performs unnecessary work: generating all indices requires $O(n)$ operations even though the final answer is already determined by the length alone. In the worst case, this would mean up to 100 iterations, which is still trivial here, but the structure becomes wasteful for larger constraints.

The key observation is that zero-based indexing defines a fixed relationship: the last valid index is always one less than the size of the array. This eliminates any need to construct or traverse the array. The problem reduces entirely to computing a single subtraction.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (construct indices) | O(n) | O(1) | Accepted but unnecessary |
| Optimal (direct formula) | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the integer $n$ from input, representing the length of the array. The value is guaranteed to be at least 1, so the array always has at least one valid index.
2. Compute $n - 1$, which corresponds to the last valid zero-based index.
3. Output the computed value directly.

### Why it works

In a zero-indexed array, the first element is at index 0 and each additional element increases the index by one. After placing $n$ elements, the final position reached is exactly $n - 1$. This relationship holds for every valid $n$ in the input domain, so computing $n - 1$ always yields the correct last index without exception.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    print(n - 1)

if __name__ == "__main__":
    solve()
```

The solution reads a single integer and immediately applies the derived relationship between array size and last index. The subtraction is performed once, and the result is printed. There is no need for loops, conditionals, or additional memory structures. The use of `strip()` ensures safe parsing even if the input contains trailing whitespace, which is common in competitive programming environments.

## Worked Examples

### Example 1

Input:

```
5
```

| Step | n | Computation | Output |
| --- | --- | --- | --- |
| Read input | 5 | - | - |
| Compute result | 5 | 5 - 1 | 4 |
| Print | 5 | - | 4 |

This shows a standard case where the array has multiple elements. The last valid index is one less than the number of elements, giving 4.

### Example 2

Input:

```
1
```

| Step | n | Computation | Output |
| --- | --- | --- | --- |
| Read input | 1 | - | - |
| Compute result | 1 | 1 - 1 | 0 |
| Print | 1 | - | 0 |

This demonstrates the boundary case where the array contains exactly one element. The only valid index is 0, confirming the correctness of the formula at the smallest possible input.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a single arithmetic operation is performed after reading input |
| Space | O(1) | No additional data structures are used |

The constraints allow up to 100, but the solution does constant work regardless of input size, so it comfortably fits within all limits.

## Test Cases

```python
import sys, io

def solve():
    n = int(sys.stdin.readline().strip())
    print(n - 1)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    solve()
    out = sys.stdout.getvalue()
    sys.stdout = old_stdout
    return out.strip()

# provided sample style cases
assert run("1\n") == "0", "sample-like 1"
assert run("5\n") == "4", "sample-like 5"

# custom cases
assert run("2\n") == "1", "small increment case"
assert run("100\n") == "99", "upper bound case"
assert run("10\n") == "9", "typical case"
assert run("3\n") == "2", "off-by-one check"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 0 | minimum size array |
| 100 | 99 | maximum constraint boundary |
| 2 | 1 | smallest non-trivial transition |
| 3 | 2 | off-by-one correctness |

## Edge Cases

The only structurally meaningful edge case is when the array length is minimal. For input $n = 1$, the computation proceeds directly: reading 1, subtracting 1, and outputting 0. This aligns with the fact that a single-element array has only index 0. Any deviation from the subtraction rule would break this case immediately, which makes it a useful correctness anchor for the entire logic.
