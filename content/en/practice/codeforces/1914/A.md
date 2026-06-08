---
title: "CF 1914A - Problemsolving Log"
description: "Monocarp's contest log is a string of length $n$ where the $i$-th character represents the problem he was working on during minute $i$. Each problem from 'A' to 'Z' has an associated required time to solve: 'A' takes 1 minute, 'B' 2 minutes, up to 'Z' which takes 26 minutes."
date: "2026-06-08T20:01:26+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 1914
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 916 (Div. 3)"
rating: 800
weight: 1914
solve_time_s: 123
verified: true
draft: false
---

[CF 1914A - Problemsolving Log](https://codeforces.com/problemset/problem/1914/A)

**Rating:** 800  
**Tags:** implementation, strings  
**Solve time:** 2m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

Monocarp's contest log is a string of length $n$ where the $i$-th character represents the problem he was working on during minute $i$. Each problem from 'A' to 'Z' has an associated required time to solve: 'A' takes 1 minute, 'B' 2 minutes, up to 'Z' which takes 26 minutes. A problem is considered solved if Monocarp has cumulatively spent at least its required time on it. The goal is to count how many distinct problems he has solved by the end of the contest.

The input consists of multiple test cases, each with the contest duration and the log string. $n$ can be up to 500, and there are up to 100 test cases, so the total work across all test cases is at most $5 \cdot 10^4$ operations. This allows solutions that process the entire string per test case in linear time. A naive approach that checks every problem against the entire string multiple times would be unnecessarily complicated and could introduce errors. Edge cases include a log where Monocarp repeatedly works on one problem without completing it, or a log with multiple solves of the same problem; the algorithm must count each problem at most once after it meets its required time.

## Approaches

The brute-force method would iterate over all 26 problems for each test case and, for each problem, count how many minutes in the log correspond to that problem. If the count meets or exceeds the required time, increment the solved count. This method is correct, but requires up to $26 \cdot n$ operations per test case. With the constraints given, this is acceptable, but it is slightly inefficient because it repeats the same scan multiple times.

The optimal method leverages a direct accumulation of time per problem as we traverse the log once. We maintain an array of 26 counters corresponding to each problem. For each minute, we increment the counter for the problem indicated by the log. After the traversal, we check which counters meet or exceed the required time for their corresponding problems. This method processes each log in $O(n)$ time and $O(1)$ additional space, and it avoids repeated scans. The key insight is that the required time for a problem is strictly determined by its alphabetical index, and we can accumulate time in a single pass without considering order.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(26 * n) | O(26) | Accepted |
| Optimal | O(n) | O(26) | Accepted |

## Algorithm Walkthrough

1. Initialize an array `times[26]` to zero. Each element corresponds to a problem 'A' through 'Z' and will track the cumulative minutes Monocarp spent on that problem.
2. For each character `c` in the contest log, compute its index as `idx = ord(c) - ord('A')` and increment `times[idx]` by one. This step accumulates the time spent on each problem during the contest.
3. Initialize a counter `solved = 0`.
4. Iterate over `i` from 0 to 25, representing problems 'A' through 'Z'. For each problem, check if `times[i] >= i + 1` since problem 'A' requires 1 minute, 'B' 2 minutes, ..., 'Z' 26 minutes. If the condition holds, increment `solved`.
5. Output `solved` as the number of problems Monocarp solved in this test case.

This algorithm works because each problem’s required time is independent, and accumulating time across the log correctly accounts for all minutes spent. The invariant is that after processing the log, `times[i]` accurately represents the total minutes Monocarp spent on problem `chr(ord('A') + i)`. Checking against `i + 1` correctly determines if the problem is solved.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    log = input().strip()
    times = [0] * 26
    for c in log:
        times[ord(c) - ord('A')] += 1
    solved = sum(1 for i in range(26) if times[i] >= i + 1)
    print(solved)
```

We process each test case independently. The array `times` tracks time per problem, and we convert letters to indices using ASCII arithmetic. Summing over the array at the end checks which problems have enough accumulated time. This avoids repeated scanning and guarantees correctness by counting every minute exactly once.

## Worked Examples

Sample input:

```
6
ACBCBC
```

| Minute | Log | times['A'..'C'] | Explanation |
| --- | --- | --- | --- |
| 1 | A | [1,0,0] | 'A' gets 1 minute |
| 2 | C | [1,0,1] | 'C' gets 1 minute |
| 3 | B | [1,1,1] | 'B' gets 1 minute |
| 4 | C | [1,1,2] | 'C' cumulative 2 |
| 5 | B | [1,2,2] | 'B' cumulative 2 |
| 6 | C | [1,2,3] | 'C' cumulative 3 |

Check required times: 'A' 1 → solved, 'B' 2 → solved, 'C' 3 → solved. Total solved = 3.

Sample input:

```
7
AAAAFPC
```

| Minute | Log | times['A'..'F','P','C'] | Explanation |
| --- | --- | --- | --- |
| 1-4 | A | 4 | 'A' cumulative 4 |
| 5 | F | 1 | 'F' cumulative 1 |
| 6 | P | 1 | 'P' cumulative 1 |
| 7 | C | 1 | 'C' cumulative 1 |

Required times: 'A' 1 → solved, 'C' 3 → not solved, 'F' 6 → not solved, 'P' 16 → not solved. Total solved = 1.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each log character is processed once, array sum is O(26) |
| Space | O(26) | Array `times` holds cumulative minutes per problem |

The total operations across all test cases are at most 500 * 100 = 50,000, well within the 2-second time limit. Memory usage is minimal due to the fixed-size array.

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
        log = input().strip()
        times = [0]*26
        for c in log:
            times[ord(c)-ord('A')] += 1
        solved = sum(1 for i in range(26) if times[i] >= i+1)
        print(solved)
    return output.getvalue().strip()

# Provided samples
assert run("3\n6\nACBCBC\n7\nAAAAFPC\n22\nFEADBBDFFEDFFFDHHHADCC\n") == "3\n1\n4"

# Custom cases
assert run("1\n1\nA\n") == "1", "single minute, single problem solved"
assert run("1\n26\nABCDEFGHIJKLMNOPQRSTUVWXYZ\n") == "1", "all problems touched once, only A solved"
assert run("1\n52\nABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ\n") == "2", "all problems twice, only A and B solved"
assert run("1\n500\n" + "A"*500 + "\n") == "1", "large input, all time on A"
assert run("1\n26\nZ"*26 + "\n") == "0", "all time on hardest problem, not solved"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 1 | single-minute log, simplest case |
| 26 letters once | 1 | only 'A' meets requirement |
| 2×26 letters | 2 | accumulation over multiple occurrences |
| 500×A | 1 | large input, check performance |
| 26×Z | 0 | hard problem not solved with insufficient time |

## Edge Cases

If Monocarp spends repeated minutes on one problem without reaching the required threshold, the algorithm correctly reports zero. For example, a log of 5 minutes on problem 'F' (requires 6) results in `times[5] = 5 < 6`, so it is not counted. If multiple solves of the same problem occur, the accumulation correctly counts the total time without double-counting, ensuring correctness even for long repeated sequences.
