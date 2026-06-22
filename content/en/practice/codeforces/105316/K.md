---
title: "CF 105316K - Marks"
description: "Each test case describes a classroom snapshot. For every test case, we are given several students, and for each student we receive exactly eight integers representing their scores in eight different subjects."
date: "2026-06-23T06:12:52+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105316
codeforces_index: "K"
codeforces_contest_name: "2024 Aleppo Collegiate Programming Contest"
rating: 0
weight: 105316
solve_time_s: 47
verified: true
draft: false
---

[CF 105316K - Marks](https://codeforces.com/problemset/problem/105316/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

Each test case describes a classroom snapshot. For every test case, we are given several students, and for each student we receive exactly eight integers representing their scores in eight different subjects. The task is to compress each student’s record into a single number by adding the eight subject scores together, then output one total per student.

The structure is hierarchical: first we read how many test cases there are, then for each test case we read how many students belong to that case, and then we process each student independently. No interaction exists between students or between test cases, so each sum can be computed immediately once the eight numbers are read.

The constraints are small enough that any straightforward processing strategy is sufficient. The number of test cases is at most 100, and each test case has at most 100 students. Each student contributes exactly 8 integers, so the total number of integers processed across the entire input is at most 100 × 100 × 8 = 80000. This is comfortably within limits for a simple linear scan.

A common implementation pitfall comes from incorrectly handling input structure. One mistake is reading all numbers in a flat sequence without respecting test case boundaries, which can still produce correct sums but in the wrong grouping. Another issue is forgetting to reset per-test-case loops, leading to printing cumulative results across test cases rather than per student. For example, if a programmer accumulates sums in a single variable across students, the output might incorrectly grow across lines instead of resetting per student.

## Approaches

The most direct approach is to read each student’s eight scores and compute their sum immediately. This is correct because each student’s final result depends only on their own eight values, with no dependency on other students or test cases. The brute-force interpretation is essentially the same as the optimal solution: explicitly summing all eight integers for every student.

If we describe it as a naive strategy, one might imagine storing all student scores first in a structure and then iterating again to compute sums. That would still be correct but introduces unnecessary overhead in both memory and time complexity due to the extra storage and second pass. The actual work done per student is always constant, since it is just eight additions.

The key observation is that the problem has no coupling between elements. Each student forms an independent block of eight values, so processing can be done in a streaming fashion. This removes any need for arrays or preprocessing.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (store then sum) | O(n) | O(n) | Accepted |
| Optimal (streaming sum) | O(n) | O(1) | Accepted |

Here n refers to the total number of integers processed, or equivalently the total number of students multiplied by eight.

## Algorithm Walkthrough

We process the input test case by test case, and inside each test case we handle each student independently.

1. Read the number of test cases. This defines how many independent groups of data we will process.
2. For each test case, read the number of students. This controls how many lines of student data follow.
3. For each student, read exactly eight integers from the input line. These represent fixed-width feature vectors.
4. Compute the sum of these eight integers immediately as they are read. This avoids storing unnecessary intermediate data.
5. Output the computed sum for that student before moving to the next student.
6. Repeat until all students in the current test case are processed, then move to the next test case.

The reason we can safely output immediately per student is that there is no future dependency. Once the eight values are read, the result is fully determined and cannot change based on any other input.

### Why it works

The correctness rests on the fact that the mapping from input to output is separable across students. Each output value is a deterministic function of exactly eight input integers. Since no transformation uses shared state across students or test cases, computing each sum in isolation produces the globally correct result. The algorithm is effectively evaluating a set of independent arithmetic expressions.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        for _ in range(n):
            nums = list(map(int, input().split()))
            out.append(str(sum(nums)))
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution reads input using fast I/O because the number of lines can be up to 10,000 in the worst case. For each student line, it converts the eight integers into a list and computes their sum directly.

One subtle implementation detail is buffering output. Instead of printing line by line, results are collected into a list and printed once at the end. This avoids repeated I/O overhead, which can matter in Python even for small constraints.

Another important detail is ensuring that each student line is handled independently. The loop structure guarantees that no state is carried between students or between test cases.

## Worked Examples

### Example 1

Input:

```
1
2
1 2 3 4 5 6 7 8
10 3 4 5 6 7 8 2
```

| Step | Student | Values | Sum |
| --- | --- | --- | --- |
| 1 | 1 | 1 2 3 4 5 6 7 8 | 36 |
| 2 | 2 | 10 3 4 5 6 7 8 2 | 45 |

Output:

```
36
45
```

This trace shows that each student is processed independently, and the result depends only on their own eight numbers.

### Example 2

Input:

```
1
3
5 5 5 5 5 5 5 5
1 1 1 1 1 1 1 1
100 0 0 0 0 0 0 0
```

| Step | Student | Values | Sum |
| --- | --- | --- | --- |
| 1 | 1 | 5 5 5 5 5 5 5 5 | 40 |
| 2 | 2 | 1 1 1 1 1 1 1 1 | 8 |
| 3 | 3 | 100 0 0 0 0 0 0 0 | 100 |

Output:

```
40
8
100
```

This example highlights that values can be uniform or skewed, but the summation logic remains unchanged.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t · n) | Each student requires summing exactly 8 integers, which is constant work per student |
| Space | O(1) auxiliary | No storage proportional to input size is required beyond the current line |

The total number of operations is small even in the maximum case, so the solution runs easily within time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    import io as sio

    out = sio.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided sample
assert run("""1
2
1 2 3 4 5 6 7 8
10 3 4 5 6 7 8 2
""") == "36\n45"

# single student minimal case
assert run("""1
1
1 1 1 1 1 1 1 1
""") == "8"

# multiple test cases
assert run("""2
1
10 10 10 10 10 10 10 10
2
1 2 3 4 5 6 7 8
8 7 6 5 4 3 2 1
""") == "80\n36\n36"

# all zeros except one dominant value
assert run("""1
2
100 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1
""") == "100\n1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single student | 8 | minimal boundary case |
| multiple test cases | mixed sums | correctness across grouped input |
| dominant value | 100, 1 | handling sparse distributions |

## Edge Cases

A minimal case with one student and eight identical values confirms that the algorithm does not depend on any structure beyond summation. For input `1 1 1 1 1 1 1 1`, the loop reads the line once, computes the sum as 8, and outputs immediately, matching the expected behavior.

A case with multiple test cases ensures that no residual state leaks between them. Since the algorithm never accumulates across test cases, each group is processed independently, and the output resets naturally at each boundary.
