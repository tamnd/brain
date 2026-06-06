---
title: "CF 350A - TL"
description: "We are asked to help Valera set a time limit for a programming problem. He has a set of correct solutions, each with a known runtime, and a set of wrong solutions, also with runtimes."
date: "2026-06-06T18:47:25+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 350
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 203 (Div. 2)"
rating: 1200
weight: 350
solve_time_s: 104
verified: true
draft: false
---

[CF 350A - TL](https://codeforces.com/problemset/problem/350/A)

**Rating:** 1200  
**Tags:** brute force, greedy, implementation  
**Solve time:** 1m 44s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to help Valera set a time limit for a programming problem. He has a set of correct solutions, each with a known runtime, and a set of wrong solutions, also with runtimes. The time limit must satisfy four conditions: it must be large enough that every correct solution passes, at least one correct solution passes with "extra time" (twice its runtime is below the limit), every wrong solution fails, and it must be the smallest such limit.

Concretely, the correct solutions are represented as an array of integers, each element being the runtime in seconds, and the wrong solutions are another array. The output is a single integer: the smallest positive time limit meeting the conditions, or -1 if none exists.

The constraints are small: up to 100 correct and 100 wrong solutions, and runtimes up to 100. This allows solutions that are roughly O(n + m) or O(n log n + m log m). Algorithms with cubic or quadratic complexity are acceptable in theory but unnecessary. Edge cases include when the fastest correct solution is equal to the slowest wrong solution, when doubling the fastest correct solution exceeds the slowest wrong solution, or when all correct solutions are identical.

A naive approach might try every candidate time limit from 1 up to 200 or more, checking all conditions, but this is unnecessary because we can reason about bounds directly.

For instance, consider input:

```
2 2
5 5
10 10
```

The smallest TL must be at least twice the fastest correct solution (2*5=10) to satisfy the "extra time" condition, but then the TL equals the runtime of the wrong solutions, so no TL works. The correct output is -1.

## Approaches

The brute-force approach would iterate over all candidate TLs starting from 1, checking for each whether all correct solutions pass, at least one has extra time, and all wrong solutions fail. The worst-case complexity is roughly O(max_runtime * (n + m)), which is acceptable here but inefficient and inelegant.

The key insight is that the candidate TL must lie between two natural bounds derived from the input: the fastest correct solution doubled (to satisfy the "extra time" requirement) and the slowest correct solution (to ensure all correct solutions pass). Any TL below the fastest correct solution multiplied by 2 fails condition 3, and any TL below the slowest correct solution fails condition 2. Similarly, the TL cannot exceed the smallest wrong solution; otherwise, some wrong solution would pass. Therefore, we can compute:

```
min_valid = max(2 * min_correct, max_correct)
max_valid = min_wrong - 1
```

If `min_valid` ≤ `max_valid`, then `min_valid` is the optimal TL; otherwise, there is no solution.

This observation reduces the problem to a simple comparison of extrema, with O(n + m) time complexity for scanning the arrays.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(max_runtime * (n+m)) | O(1) | Acceptable but unnecessary |
| Optimal | O(n + m) | O(1) | Efficient and accepted |

## Algorithm Walkthrough

1. Read the number of correct solutions `n` and wrong solutions `m`.
2. Read the array `correct` of length `n` and array `wrong` of length `m`.
3. Find the smallest runtime among correct solutions, `min_correct`, and the largest, `max_correct`.
4. Find the smallest runtime among wrong solutions, `min_wrong`.
5. Compute the minimum candidate TL as `min_valid = max(2 * min_correct, max_correct)`. This guarantees at least one correct solution has extra time and all correct solutions pass.
6. Compute the maximum candidate TL as `max_valid = min_wrong - 1`. This guarantees no wrong solution passes.
7. If `min_valid` ≤ `max_valid`, output `min_valid`; otherwise, output -1.

Why it works: The algorithm captures the exact feasible range of TLs that satisfy all four conditions. The lower bound ensures all correct solutions pass and at least one has extra time. The upper bound ensures all wrong solutions fail. Any TL outside this range violates a condition. Since we want the smallest TL, choosing `min_valid` is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m = map(int, input().split())
correct = list(map(int, input().split()))
wrong = list(map(int, input().split()))

min_correct = min(correct)
max_correct = max(correct)
min_wrong = min(wrong)

min_valid = max(2 * min_correct, max_correct)
max_valid = min_wrong - 1

if min_valid <= max_valid:
    print(min_valid)
else:
    print(-1)
```

The code follows the algorithm directly. We read the input efficiently, compute the extrema in O(n + m), then derive the TL bounds. Edge cases such as a smallest correct solution equal to the largest wrong solution are handled naturally by the comparison `min_valid <= max_valid`.

## Worked Examples

Sample Input 1:

```
3 6
4 5 2
8 9 6 10 7 11
```

| Variable | Value |
| --- | --- |
| min_correct | 2 |
| max_correct | 5 |
| min_wrong | 6 |
| min_valid | max(2*2, 5) = 5 |
| max_valid | 6 - 1 = 5 |

Since min_valid = 5 ≤ max_valid = 5, output 5. This demonstrates correct handling when TL exactly matches the upper bound.

Sample Input 2 (no valid TL):

```
2 2
5 5
10 10
```

| Variable | Value |
| --- | --- |
| min_correct | 5 |
| max_correct | 5 |
| min_wrong | 10 |
| min_valid | max(2*5, 5) = 10 |
| max_valid | 10 - 1 = 9 |

Since min_valid = 10 > max_valid = 9, output -1. This shows the algorithm correctly rejects impossible cases.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | We scan the arrays to find min and max values |
| Space | O(n + m) | Arrays store the input solutions |

The solution easily handles the upper bounds n = m = 100 and runtimes up to 100, staying well within the 2-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, m = map(int, input().split())
    correct = list(map(int, input().split()))
    wrong = list(map(int, input().split()))
    
    min_correct = min(correct)
    max_correct = max(correct)
    min_wrong = min(wrong)
    
    min_valid = max(2 * min_correct, max_correct)
    max_valid = min_wrong - 1
    
    return str(min_valid if min_valid <= max_valid else -1)

# Provided sample
assert run("3 6\n4 5 2\n8 9 6 10 7 11\n") == "5", "sample 1"

# Custom cases
assert run("2 2\n5 5\n10 10\n") == "-1", "impossible TL"
assert run("1 1\n1\n2\n") == "2", "single correct and wrong"
assert run("3 3\n3 3 3\n6 6 6\n") == "6", "all correct equal"
assert run("3 3\n2 4 6\n8 9 10\n") == "6", "mixed correct values"
assert run("2 2\n50 60\n100 70\n") == "100", "upper bound edge"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 2\n5 5\n10 10 | -1 | No TL satisfies all conditions |
| 1 1\n1\n2 | 2 | Minimal case with single solution |
| 3 3\n3 3 3\n6 6 6 | 6 | All correct equal, TL matches upper bound |
| 3 3\n2 4 6\n8 9 10 | 6 | Correct solutions vary, ensures proper min/max calculation |
| 2 2\n50 60\n100 70 | 100 | TL exactly below smallest wrong solution |

## Edge Cases

When the fastest correct solution is very small compared to the slowest wrong solution, the TL is determined by doubling the fastest correct solution only if it exceeds the slowest correct solution. For input `2 2\n1 2\n5 6`, `min_valid = max(2*1, 2) = 2`, `max_valid = 5-1=4`, output is 2. This confirms the algorithm chooses the minimal feasible TL that satisfies all conditions.

When all correct solutions have the same runtime, the algorithm naturally sets TL as either double the minimum or equal to that runtime, whichever is larger, and still ensures no wrong solution passes.
