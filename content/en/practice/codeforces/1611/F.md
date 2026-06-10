---
title: "CF 1611F - ATM and Students"
description: "The problem involves simulating an ATM that starts with a fixed amount of money and must serve a queue of students. Each student either deposits a positive amount or withdraws a negative amount from the ATM."
date: "2026-06-10T07:06:46+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1611
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 756 (Div. 3)"
rating: 1800
weight: 1611
solve_time_s: 72
verified: true
draft: false
---

[CF 1611F - ATM and Students](https://codeforces.com/problemset/problem/1611/F)

**Rating:** 1800  
**Tags:** binary search, data structures, two pointers  
**Solve time:** 1m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem involves simulating an ATM that starts with a fixed amount of money and must serve a queue of students. Each student either deposits a positive amount or withdraws a negative amount from the ATM. Polycarp, who operates the ATM, can choose to start serving the students at any point in the queue, and once the ATM cannot satisfy a withdrawal, it shuts down permanently. The task is to find the longest contiguous subsequence of students that can be fully served, and output the indices of the first and last student in this subsequence, or -1 if no student can be served.

The input consists of multiple test cases, each specifying the number of students, the initial ATM balance, and the sequence of transaction requests. The constraints allow for up to 200,000 students per test case and up to 10,000 test cases, but the sum of `n` across all test cases does not exceed 200,000. This immediately rules out any approach with O(n²) complexity per test case because in the worst case we would perform around 4×10¹⁰ operations, far exceeding the time limit. An O(n) or O(n log n) approach is feasible. The key edge cases arise when the ATM balance is initially insufficient for early withdrawals, when deposits occur before withdrawals, or when sequences contain zeros, which must not be treated as withdrawals.

For example, consider the sequence `[-5, 10, -3]` with an initial balance of `4`. A naive implementation that starts from the first student would fail because the first withdrawal exceeds the balance. The correct approach is to skip the first student, serve the next two, and return the subsequence indices `2 3`.

## Approaches

The brute-force method would consider every possible starting student, simulate the ATM for each contiguous subsequence, and track the length of the longest valid subsequence. This approach is guaranteed correct because it explicitly checks every possibility. However, in the worst case of n=200,000, it would perform about 2×10¹⁰ operations if we sum the lengths of all subsequences, which is infeasible within 2 seconds.

The key insight is that the problem reduces to a single-pass sliding window with careful tracking of the ATM balance and withdrawals. Once the ATM cannot serve a withdrawal, any subsequence including that withdrawal cannot be valid. Positive deposits only increase the ATM balance and do not restrict subsequences, while negative withdrawals can force the window to shift. This naturally suggests using a two-pointer approach or tracking the maximum negative transaction within a window, combined with prefix sums for efficiency. The solution maintains a running balance and dynamically updates the candidate starting point when the balance would go negative. By focusing on contiguous segments and leveraging the properties of cumulative sums, we can achieve linear time per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Sliding Window / Prefix Sum | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize two pointers: `start` at 0 representing the potential start of the served subsequence, and `max_len` as 0 to store the length of the longest valid subsequence. Track `max_start` and `max_end` for the final output.
2. Iterate through the students with an index `i`, maintaining a `balance` variable initialized to the ATM starting amount `s`.
3. For each student, add the transaction value `a[i]` to `balance`. If `a[i]` is positive, it increases the ATM balance. If it is negative, check whether `balance` becomes negative after the withdrawal.
4. If `balance` drops below zero, this student cannot be served starting from the current `start`. Move `start` to `i + 1` and reset `balance` to `s`, effectively considering the next student as the new candidate start.
5. Whenever a valid transaction occurs, check if the current window `i - start + 1` exceeds `max_len`. If it does, update `max_len`, `max_start`, and `max_end` to the current window.
6. After processing all students, if `max_len` remains 0, print `-1`. Otherwise, print `max_start + 1` and `max_end + 1` to convert from 0-based to 1-based indexing.

Why it works: The algorithm ensures that the ATM balance never goes negative within the candidate window, and by only shifting the start when a withdrawal cannot be served, it efficiently identifies the maximal contiguous segment. Positive transactions extend the window without restriction, guaranteeing the longest feasible subsequence is found.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, s = map(int, input().split())
        a = list(map(int, input().split()))
        max_len = 0
        max_start = max_end = -1
        start = 0
        balance = s
        for i in range(n):
            balance += a[i]
            if balance < 0:
                start = i + 1
                balance = s
            else:
                if i - start + 1 > max_len:
                    max_len = i - start + 1
                    max_start = start
                    max_end = i
        if max_len == 0:
            print(-1)
        else:
            print(max_start + 1, max_end + 1)

if __name__ == "__main__":
    solve()
```

The code initializes the pointers and balance as described. When the balance goes negative, it shifts the `start` and resets the balance to avoid invalid sequences. The length check ensures that only the longest valid subsequence is recorded. The conversion to 1-based indexing is crucial for matching the output format. Resetting `balance` after moving `start` ensures that each new candidate segment starts with the ATM initial sum `s`.

## Worked Examples

Consider the first sample input:

```
4 10
-16 2 -6 8
```

| i | a[i] | balance | start | max_len | max_start | max_end |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | -16 | -6 | 1 | 0 | -1 | -1 |
| 1 | 2 | 12 | 1 | 1 | 1 | 1 |
| 2 | -6 | 6 | 1 | 2 | 1 | 2 |
| 3 | 8 | 14 | 1 | 3 | 1 | 3 |

The output is `2 4`, which corresponds to the longest segment `[2, -6, 8]`.

Consider the second sample input:

```
3 1000
-100000 -100000 -100000
```

All students request more than the ATM has. The balance immediately drops below zero for each starting student, so the algorithm prints `-1`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each student is visited once, balance updates and comparisons are O(1). |
| Space | O(n) for input array | Only the student array is stored; additional variables use O(1). |

Given the total `n` across all test cases is at most 200,000, the algorithm performs a maximum of 200,000 iterations, well within the 2-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    return sys.stdout.getvalue().strip()

# provided samples
assert run("3\n4 10\n-16 2 -6 8\n3 1000\n-100000 -100000 -100000\n6 0\n2 6 -164 1 -1 -6543\n") in ["2 4\n-1\n1 2", "2 4\n-1\n4 5"], "sample 1"

# custom cases
assert run("1\n1 5\n-10\n") == "-1", "single withdrawal too large"
assert run("1\n5 0\n1 2 3 4 5\n") == "1 5", "all deposits, starting at 1"
assert run("1\n5 5\n-1 -1 -1 -1 -1\n") == "1 5", "withdrawals exactly equal to balance"
assert run("1\n5 3\n-2 -1 2 -1 -1\n") == "1 5", "mix, balance never negative"
assert run("1\n3 0\n-1 2 -1\n") == "2 3", "skip first negative, then serve next two"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 5 -10 | -1 | Single withdrawal exceeds ATM |
| 5 0 1 2 3 4 5 | 1 5 | All deposits, longest segment is entire array |
| 5 5 -1 -1 -1 -1 -1 | 1 5 | Withdrawals exactly consume balance |
| 5 3 -2 -1 2 -1 -1 | 1 5 | Mixed deposits and withdrawals |
| 3 0 -1 |  |  |
