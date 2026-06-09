---
title: "CF 1691A - Beat The Odds"
description: "We are given a sequence of integers, and we need to remove as few numbers as possible so that every pair of consecutive numbers in the remaining sequence sums to an even number. The sum of two numbers is even if both numbers are even or both are odd."
date: "2026-06-09T23:08:13+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1691
codeforces_index: "A"
codeforces_contest_name: "CodeCraft-22 and Codeforces Round 795 (Div. 2)"
rating: 800
weight: 1691
solve_time_s: 113
verified: true
draft: false
---

[CF 1691A - Beat The Odds](https://codeforces.com/problemset/problem/1691/A)

**Rating:** 800  
**Tags:** brute force, greedy, math  
**Solve time:** 1m 53s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of integers, and we need to remove as few numbers as possible so that every pair of consecutive numbers in the remaining sequence sums to an even number. The sum of two numbers is even if both numbers are even or both are odd. Therefore, the condition translates into the requirement that the remaining sequence must consist of all even numbers or all odd numbers in consecutive positions. We are not constrained by the original order of the numbers, but we must preserve the sequence we keep; we cannot reorder elements.

The input consists of multiple test cases. Each test case provides the length of the sequence and the sequence itself. The total number of elements across all test cases does not exceed 100,000. This bound implies that any solution with worse than linear complexity relative to the sequence length may be too slow. Algorithms with O(n^2) behavior would perform roughly 10 billion operations in the worst case and are ruled out. Linear or linearithmic approaches are feasible.

A subtle edge case is when the sequence is already valid, such as `[3, 5, 9, 7]`. Here, no removal is needed because consecutive pairs are all even. Another tricky case is when the sequence alternates parity like `[2, 3, 4, 5]`. A naive approach that only looks at the first violation might remove the wrong element and require more removals than necessary. The correct approach requires understanding the total counts of odd and even numbers to determine the minimum removals.

## Approaches

The brute-force approach would iterate through the sequence and attempt to remove elements greedily whenever a consecutive pair sums to an odd number. We could try removing either the first or the second element of the violating pair and recursively continue checking the sequence. This method works because removing a number breaks the violation, but it quickly becomes inefficient. Each removal could lead to a recursive call that examines almost the entire remaining sequence, yielding worst-case complexity of O(n^2). For n up to 100,000, this is too slow.

The key insight is that a consecutive pair sums to an even number only if both numbers share the same parity. This means that the final sequence must contain numbers all of the same parity. Therefore, the optimal solution is simply to decide whether to keep all even numbers or all odd numbers. The minimum number of removals is the smaller of the counts of even numbers and odd numbers. We do not need to simulate removing individual elements or check each pair, because parity is independent of position. This observation reduces the problem to a linear scan to count parity, giving O(n) time per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(1) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases. Each test case will be processed independently.
2. For each test case, read the sequence length and the sequence itself.
3. Initialize two counters: one for even numbers and one for odd numbers.
4. Iterate through the sequence. For each element, increment the even counter if it is divisible by 2, otherwise increment the odd counter.
5. Compute the minimum between the count of even numbers and the count of odd numbers. This is the minimum number of removals required because keeping the larger group preserves the maximum number of elements while satisfying the consecutive sum condition.
6. Print this minimum number for the test case.

Why it works: After counting the parity of all numbers, we know exactly how many elements we must remove to make all remaining numbers share the same parity. This guarantees that every consecutive pair will sum to an even number. No other configuration can produce fewer removals because any mix of odd and even numbers inevitably produces at least as many violations as the size of the smaller group.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    even_count = sum(1 for x in a if x % 2 == 0)
    odd_count = n - even_count
    print(min(even_count, odd_count))
```

The code reads all inputs efficiently using fast I/O. It counts the number of even and odd numbers in one pass, then prints the minimum of the two counts. Using `n - even_count` to compute the odd count avoids a second loop, making the code cleaner and slightly faster. Edge cases are naturally handled: if all numbers are even, `odd_count` is zero, so the minimum is zero, correctly indicating no removal is needed.

## Worked Examples

### Example 1

Input sequence: `[2, 4, 3, 6, 8]`

| Element | Parity | even_count | odd_count |
| --- | --- | --- | --- |
| 2 | even | 1 | 0 |
| 4 | even | 2 | 0 |
| 3 | odd | 2 | 1 |
| 6 | even | 3 | 1 |
| 8 | even | 4 | 1 |

The minimum of `even_count` and `odd_count` is 1. Removing the single odd number 3 results in `[2,4,6,8]`, which satisfies the condition.

### Example 2

Input sequence: `[3, 5, 9, 7, 1, 3]`

| Element | Parity | even_count | odd_count |
| --- | --- | --- | --- |
| 3 | odd | 0 | 1 |
| 5 | odd | 0 | 2 |
| 9 | odd | 0 | 3 |
| 7 | odd | 0 | 4 |
| 1 | odd | 0 | 5 |
| 3 | odd | 0 | 6 |

The minimum of `even_count` and `odd_count` is 0. No removal is needed because all numbers are odd, so consecutive sums are even.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | One pass through the sequence to count even and odd numbers |
| Space | O(n) | Storing the sequence temporarily; counters use O(1) |

Given the total n across all test cases does not exceed 100,000, the total operations are well under 200,000, which fits comfortably within the 1-second time limit.

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
        even_count = sum(1 for x in a if x % 2 == 0)
        odd_count = n - even_count
        print(min(even_count, odd_count))
    return output.getvalue().strip()

# Provided samples
assert run("2\n5\n2 4 3 6 8\n6\n3 5 9 7 1 3\n") == "1\n0", "sample 1"

# Custom cases
assert run("1\n3\n2 4 6\n") == "0", "all even, no removal"
assert run("1\n4\n1 3 5 7\n") == "0", "all odd, no removal"
assert run("1\n4\n2 3 4 5\n") == "2", "alternating parity"
assert run("1\n1\n42\n") == "0", "single element"
assert run("1\n6\n2 2 2 1 1 1\n") == "3", "half-half sequence"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 elements all even | 0 | No removal needed |
| 4 elements all odd | 0 | No removal needed |
| Alternating even/odd | 2 | Correct calculation of minimum removals |
| Single element | 0 | Edge case with n = 1 |
| Half-even, half-odd | 3 | Proper handling when counts are equal |

## Edge Cases

If the sequence has all elements of the same parity, the algorithm correctly outputs 0. For example, `[2,4,6]` results in `even_count=3`, `odd_count=0`, `min(even_count, odd_count)=0`. If the sequence alternates parity, such as `[2,3,4,5]`, the counts are `even_count=2`, `odd_count=2`, yielding a minimum removal of 2. This ensures the algorithm never underestimates removals. Single-element sequences are handled naturally: `even_count` or `odd_count` is 1, the other is 0, so the minimum is 0. The solution is robust across all valid inputs.
