---
title: "CF 1971A - My First Sorting Problem"
description: "The task asks us to read pairs of small integers and output each pair in sorted order: the smaller number first, then the larger number."
date: "2026-06-08T17:19:28+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1971
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 944 (Div. 4)"
rating: 800
weight: 1971
solve_time_s: 88
verified: true
draft: false
---

[CF 1971A - My First Sorting Problem](https://codeforces.com/problemset/problem/1971/A)

**Rating:** 800  
**Tags:** implementation, sortings  
**Solve time:** 1m 28s  
**Verified:** yes  

## Solution
## Problem Understanding

The task asks us to read pairs of small integers and output each pair in sorted order: the smaller number first, then the larger number. Each test case consists of two integers, $x$ and $y$, and the input begins with a number $t$ representing how many such pairs we need to process. The output must contain the corresponding sorted pair for each test case.

The constraints are extremely tight: both integers are between 0 and 9 inclusive, and there can be up to 100 test cases. Because the numbers are so small, we do not need complex data structures or sorting algorithms. The algorithm only needs to determine which of the two integers is smaller and which is larger, a single comparison per test case.

Non-obvious edge cases arise when the two integers are equal. For instance, if the input pair is $3$ and $3$, the output must be $3 3$. A naive approach that swaps only when $x > y$ works correctly here, but forgetting the equality case or attempting subtraction-based tricks could lead to incorrect results. Another minor edge case is when both numbers are zero, which also requires the output $0 0$.

## Approaches

The brute-force approach is already optimal in this scenario. For each pair, you compare $x$ and $y$. If $x > y$, you swap them; otherwise, leave them as is. This method is correct because every pair has only two elements, and a single comparison suffices to order them. The operation count for the worst-case input, with 100 test cases, is 100 comparisons, which is trivial.

There is no need for a more advanced technique such as a full sort, because the problem size and structure make the single-comparison method both simple and efficient. The key insight is recognizing that sorting two numbers is just a comparison and conditional assignment, and the large sorting machinery would be unnecessary overhead.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(t) | O(1) | Accepted |
| Optimal | O(t) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the integer $t$ representing the number of test cases. This sets up the number of iterations we will perform.
2. For each test case, read the two integers $x$ and $y$.
3. Compare the two integers. If $x > y$, swap their values. This guarantees that $x$ is always the smaller or equal number.
4. Print $x$ and $y$ in order, separated by a space. This is the required output format.
5. Repeat steps 2-4 for all test cases.

Why it works: the invariant maintained throughout the algorithm is that after the comparison and possible swap, the first number of the pair is never greater than the second. Since the output specification only requires the pair to be in non-decreasing order, this invariant ensures correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    x, y = map(int, input().split())
    if x > y:
        x, y = y, x
    print(x, y)
```

The code first reads $t$ using `input()`. The loop runs exactly $t$ times, processing one test case per iteration. `map(int, input().split())` parses the two integers from each line. The conditional swap ensures the smaller number comes first, and `print(x, y)` outputs them correctly. Since Python handles small integers natively, no special considerations for boundaries or overflows are needed.

## Worked Examples

### Example 1

Input: `1 9`

| x | y | Condition x > y? | Output |
| --- | --- | --- | --- |
| 1 | 9 | False | 1 9 |

Explanation: 1 is less than 9, no swap occurs. Output matches the sorted order.

### Example 2

Input: `8 4`

| x | y | Condition x > y? | Output |
| --- | --- | --- | --- |
| 8 | 4 | True | 4 8 |

Explanation: 8 is greater than 4, so the swap occurs, producing the correct ascending order.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case requires a single comparison and optional swap. With t ≤ 100, this is negligible. |
| Space | O(1) | No additional memory proportional to t is required, only temporary variables for x and y. |

The algorithm is comfortably within the limits of 1-second runtime and 256 MB memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    t = int(input())
    for _ in range(t):
        x, y = map(int, input().split())
        if x > y:
            x, y = y, x
        print(x, y)
    return output.getvalue().strip()

# Provided sample
assert run("10\n1 9\n8 4\n1 4\n3 4\n2 0\n2 4\n6 9\n3 3\n0 0\n9 9\n") == \
"1 9\n4 8\n1 4\n3 4\n0 2\n2 4\n6 9\n3 3\n0 0\n9 9"

# Custom cases
assert run("1\n0 0\n") == "0 0", "both zero"
assert run("1\n9 0\n") == "0 9", "maximum boundary"
assert run("1\n5 5\n") == "5 5", "equal values"
assert run("3\n1 2\n2 1\n3 3\n") == "1 2\n1 2\n3 3", "mixed ordering"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 0` | `0 0` | Both numbers are the smallest possible value |
| `9 0` | `0 9` | Swap needed for maximum and minimum values |
| `5 5` | `5 5` | Both numbers equal, no swap needed |
| `1 2\n2 1\n3 3` | `1 2\n1 2\n3 3` | Mixed orderings with equal numbers included |

## Edge Cases

When the two numbers are equal, for instance `3 3`, the algorithm compares them. Since the condition `x > y` is false, no swap occurs. The printed output remains `3 3`, which is correct. For the input `0 0`, the same logic applies, maintaining the invariant that the first number is never greater than the second. For a maximum boundary input like `9 0`, the swap ensures the output `0 9`. The algorithm consistently handles all scenarios because it relies on a single, simple comparison.
