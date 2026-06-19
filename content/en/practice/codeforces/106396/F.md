---
title: "CF 106396F - \u6597\u95ef\u5c06"
description: "The task is essentially a direct comparison between two integers. Each test case provides two numbers, and the output depends only on their relative ordering. If both values are identical, the result is a draw."
date: "2026-06-19T18:06:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106396
codeforces_index: "F"
codeforces_contest_name: "Tiangong University 2025 ICPC Team Selection Contest II (Online Mirror)"
rating: 0
weight: 106396
solve_time_s: 39
verified: true
draft: false
---

[CF 106396F - \u6597\u95ef\u5c06](https://codeforces.com/problemset/problem/106396/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 39s  
**Verified:** yes  

## Solution
## Problem Understanding

The task is essentially a direct comparison between two integers. Each test case provides two numbers, and the output depends only on their relative ordering. If both values are identical, the result is a draw. If the first value is larger, one participant wins; otherwise the other participant wins.

From an algorithmic perspective, the input size is irrelevant because there is no structure to process beyond reading and comparing two numbers. Even if the problem had many test cases, each one is still independent and requires only constant time work.

Since each operation is a simple comparison and output decision, even extremely large inputs would not threaten performance. Any solution that avoids unnecessary parsing overhead or extra data structures will comfortably run within limits.

The only subtle edge case is equality. A naive implementation that only checks greater-than and less-than without explicitly handling equality could accidentally fall through logic branches and produce incorrect output or default behavior. For example, if both numbers are equal and the program only checks `a > b` and otherwise prints a fixed loser, it would incorrectly assign a winner instead of declaring a draw.

Example of correct behavior:

Input: `5 5`

Output: `Pingju`

A careless conditional chain might treat this as the “else” case of `a > b`, incorrectly printing a winner instead of recognizing equality.

## Approaches

The brute-force approach would still be to compare the two numbers directly. There is no meaningful alternative interpretation of the problem that introduces complexity such as searching, sorting, or graph traversal. Any attempt to simulate or transform the input would only add unnecessary overhead.

The key observation is that the problem reduces entirely to a three-way comparison between two integers. Once this is recognized, the solution becomes a single conditional check. No preprocessing or auxiliary data structures are required.

The optimal solution simply branches on equality first, then determines which value is larger.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Direct comparison logic | O(1) | O(1) | Accepted |
| Any extended simulation | O(1) | O(1) | Accepted but unnecessary |

## Algorithm Walkthrough

1. Read two integers `a` and `b` from input. These represent the two competitors’ scores or values.
2. Check whether `a` is equal to `b`. If they match exactly, output `"Pingju"`, since neither side has an advantage.
3. If they are not equal, compare them directly. If `a > b`, output `"Liang"`.
4. Otherwise, `a < b`, so output `"Chuang"`.

The structure of the decision ensures that equality is handled before ordering comparisons, preventing ambiguity.

### Why it works

The problem defines a total order comparison over two values with a special case for equality. Since every pair of integers must satisfy exactly one of `a == b`, `a > b`, or `a < b`, the branching logic partitions the input space completely without overlap. Each branch corresponds to exactly one valid outcome, ensuring correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    a, b = map(int, input().split())
    if a == b:
        print("Pingju")
    elif a > b:
        print("Liang")
    else:
        print("Chuang")

if __name__ == "__main__":
    solve()
```

The solution reads a single line of input and immediately parses two integers. The comparison order is important: equality must be checked first, since it is the only case that does not fit into a strict inequality classification.

The output strings are fixed and depend only on the comparison outcome. No additional formatting or computation is required.

## Worked Examples

### Example 1

Input:

```
3 3
```

| Step | a | b | Condition | Output |
| --- | --- | --- | --- | --- |
| 1 | 3 | 3 | a == b | Pingju |

This confirms the equality branch. Both values match, so the algorithm correctly returns a draw.

### Example 2

Input:

```
7 2
```

| Step | a | b | Condition | Output |
| --- | --- | --- | --- | --- |
| 1 | 7 | 2 | a != b | - |
| 2 | 7 | 2 | a > b | Liang |

This demonstrates the greater-than branch. The first value dominates, so the correct winner is produced.

### Example 3

Input:

```
1 9
```

| Step | a | b | Condition | Output |
| --- | --- | --- | --- | --- |
| 1 | 1 | 9 | a != b | - |
| 2 | 1 | 9 | a < b | Chuang |

This confirms the final fallback case when the second value is larger.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only one comparison between two integers |
| Space | O(1) | No additional data structures used |

The computation per test case is constant, so even large numbers of cases would remain trivial under typical constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    input = _sys.stdin.readline

    a, b = map(int, input().split())
    if a == b:
        return "Pingju"
    elif a > b:
        return "Liang"
    else:
        return "Chuang"

# sample-like cases
assert run("3 3") == "Pingju"
assert run("7 2") == "Liang"
assert run("1 9") == "Chuang"

# custom edge cases
assert run("0 0") == "Pingju"
assert run("-1 -5") == "Liang"
assert run("-10 -2") == "Chuang"
assert run("1000000000 999999999") == "Liang"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 3 | Pingju | equality handling |
| -1 -5 | Liang | negative number comparison |
| 1 9 | Chuang | basic less-than branch |
| 0 0 | Pingju | zero equality edge case |
| 1e9 1e9-1 | Liang | large value boundary |

## Edge Cases

For equality, the algorithm explicitly checks `a == b` before any inequality logic. For input `5 5`, execution stops immediately at the equality branch and prints `"Pingju"`.

For negative numbers, consider input `-3 -10`. The comparison still behaves normally: `-3 > -10`, so the algorithm reaches the greater-than branch and outputs `"Liang"`. No special handling is needed because integer ordering is total over negatives as well.

For large values like `10^9 10^9`, equality still triggers the first branch, ensuring correct draw behavior even at boundary magnitudes.
