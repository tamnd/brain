---
title: "CF 470H - Array Sorting"
description: "We are given an array of integers. The first number in the input is the array size n, and the next n integers are the array elements. The task is simply to output the same elements arranged in non-decreasing order."
date: "2026-05-30T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special"]
categories: ["algorithms"]
codeforces_contest: 470
codeforces_index: "H"
codeforces_contest_name: "Surprise Language Round 7"
rating: 2300
weight: 470
solve_time_s: 78
verified: true
draft: false
---

[CF 470H - Array Sorting](https://codeforces.com/problemset/problem/470/H)

**Rating:** 2300  
**Tags:** *special  
**Solve time:** 1m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers. The first number in the input is the array size `n`, and the next `n` integers are the array elements. The task is simply to output the same elements arranged in non-decreasing order.

Although this problem appeared as a joke problem connected to the FALSE programming language, from an algorithmic perspective it is just a sorting task.

The constraints are extremely small. The array contains at most 10 elements, and every value is between 1 and 100. With only 10 numbers, even very inefficient sorting methods are fast enough. An algorithm with quadratic complexity performs at most about 100 comparisons, which is negligible. Standard library sorting is also easily sufficient.

The main challenge is actually parsing the input correctly. The entire input is provided on a single line, so a solution that expects multiple lines could fail if written carelessly.

A common edge case is when the array already appears in sorted order.

Input:

```
4 1 2 3 4
```

Correct output:

```
1 2 3 4
```

The algorithm should leave the ordering unchanged after sorting.

Another edge case is when all values are equal.

Input:

```
5 7 7 7 7 7
```

Correct output:

```
7 7 7 7 7
```

Some incorrect implementations accidentally remove duplicates by using a set before sorting.

A third case is the minimum allowed size.

Input:

```
1 42
```

Correct output:

```
42
```

The solution must handle a single-element array without attempting invalid accesses.

## Approaches

The most direct approach is brute-force sorting. Since the array contains at most ten elements, we could repeatedly find the smallest remaining value, or use a quadratic algorithm such as bubble sort or selection sort. Such methods are correct because they gradually move elements into their proper sorted positions. For `n = 10`, even an `O(n²)` algorithm performs only around one hundred comparisons.

The natural improvement is to use the language's built-in sorting routine. Python's `sort()` and `sorted()` functions are highly optimized and guaranteed to produce the array in non-decreasing order. Their asymptotic complexity is `O(n log n)`, although with such tiny input sizes the exact complexity is irrelevant.

The brute-force approach works because the input is very small, but built-in sorting is simpler, shorter, and less error-prone. Since the task only asks for a sorted array and imposes no additional constraints, using the standard sorting function is the cleanest solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (Bubble/Selection Sort) | O(n²) | O(1) | Accepted |
| Optimal (Built-in Sort) | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read all integers from the input.
2. Extract the first value as `n`.
3. Take the next `n` values as the array.
4. Sort the array in non-decreasing order.
5. Output the sorted values separated by spaces.

The sorting step directly produces the required order, so no additional processing is necessary.

### Why it works

Sorting rearranges the elements so that for every pair of adjacent positions `i` and `i + 1`, the condition `a[i] ≤ a[i + 1]` holds. Since a correct sorting algorithm preserves all elements and places them in this order, the resulting sequence is exactly the non-decreasing arrangement requested by the problem.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    data = list(map(int, sys.stdin.read().split()))
    if not data:
        return

    n = data[0]
    arr = data[1:1 + n]

    arr.sort()

    print(*arr)

if __name__ == "__main__":
    solve()
```

The solution reads all integers from standard input and stores them in a list. The first number is the array size, and the following `n` numbers form the array itself.

The call to `arr.sort()` rearranges the elements into non-decreasing order. Python's built-in sorting implementation is fully sufficient for the tiny limits in this problem.

When printing, `print(*arr)` automatically places spaces between elements, matching the required output format.

One subtle point is slicing exactly `n` values with `data[1:1 + n]`. This follows the input specification precisely and avoids accidentally including extra values if malformed input were present.

## Worked Examples

### Example 1

Input:

```
3 3 1 2
```

| Step | n | Array |
| --- | --- | --- |
| Read input | 3 | [3, 1, 2] |
| Sort | 3 | [1, 2, 3] |
| Output | 3 | [1, 2, 3] |

The array is rearranged into ascending order, which is exactly the required result.

### Example 2

Input:

```
5 7 7 3 1 7
```

| Step | n | Array |
| --- | --- | --- |
| Read input | 5 | [7, 7, 3, 1, 7] |
| Sort | 5 | [1, 3, 7, 7, 7] |
| Output | 5 | [1, 3, 7, 7, 7] |

This example demonstrates that duplicates are preserved. Sorting changes only the order, not the multiplicity of values.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Built-in sorting dominates the running time |
| Space | O(n) | Python's sorting implementation may use auxiliary memory |

With `n ≤ 10`, the running time is effectively instantaneous. Both the time and memory usage are far below the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    data = list(map(int, sys.stdin.read().split()))
    n = data[0]
    arr = data[1:1 + n]
    arr.sort()

    return " ".join(map(str, arr))

# provided sample
assert run("3 3 1 2\n") == "1 2 3", "sample 1"

# minimum size
assert run("1 42\n") == "42", "single element"

# already sorted
assert run("4 1 2 3 4\n") == "1 2 3 4", "already sorted"

# all equal
assert run("5 7 7 7 7 7\n") == "7 7 7 7 7", "duplicates preserved"

# maximum size
assert run("10 10 9 8 7 6 5 4 3 2 1\n") == "1 2 3 4 5 6 7 8 9 10", "reverse order"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 42` | `42` | Minimum array size |
| `4 1 2 3 4` | `1 2 3 4` | Already sorted input |
| `5 7 7 7 7 7` | `7 7 7 7 7` | Duplicate preservation |
| `10 10 9 8 7 6 5 4 3 2 1` | `1 2 3 4 5 6 7 8 9 10` | Reverse-order array and maximum size |

## Edge Cases

Consider the minimum-size input:

```
1 42
```

The algorithm reads `n = 1` and extracts the array `[42]`. Sorting a single-element array leaves it unchanged. The output is:

```
42
```

No special handling is required.

Consider an array where all values are identical:

```
5 7 7 7 7 7
```

The extracted array is `[7, 7, 7, 7, 7]`. After sorting, the array remains exactly the same. The output is:

```
7 7 7 7 7
```

This confirms that duplicates are preserved.

Consider an already sorted array:

```
4 1 2 3 4
```

The algorithm reads `[1, 2, 3, 4]`, performs sorting, and obtains the same sequence. The output is:

```
1 2 3 4
```

This demonstrates that the algorithm does not disturb a correct ordering and still produces the required result.
