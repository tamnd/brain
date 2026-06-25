---
title: "CF 105993B - Let's Go Swimming!"
description: "The problem gives two proposed swimming times from two judges. Each judge suggests an integer moment when they want to go swimming, and the final decision is to choose the earliest possible moment so they can still attend the contest. The task is to output that earliest time."
date: "2026-06-25T13:27:59+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105993
codeforces_index: "B"
codeforces_contest_name: "Latakia and Tartus Collegiate Programming Contest 2025"
rating: 0
weight: 105993
solve_time_s: 34
verified: true
draft: false
---

[CF 105993B - Let's Go Swimming!](https://codeforces.com/problemset/problem/105993/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 34s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem gives two proposed swimming times from two judges. Each judge suggests an integer moment when they want to go swimming, and the final decision is to choose the earliest possible moment so they can still attend the contest. The task is to output that earliest time.

The input contains two positive integers representing the two suggested times. The output is the smaller of the two values because any larger choice would only delay the swimming trip without helping them.

The constraints keep both values at most 1000. This is small enough that even a direct simulation would work, but simulation is unnecessary because the answer depends only on the ordering of the two numbers. The available operations are effectively constant, so the solution runs instantly regardless of the exact input size.

The main edge cases come from equal values and from the smaller value appearing in either position. A careless solution that always prints the first number would fail when the second proposal is earlier.

For example, if the input is:

```
4 2
```

the correct output is:

```
2
```

Printing the first number would incorrectly choose a later swimming time.

Another case is:

```
7 7
```

The correct output is:

```
7
```

The two choices are identical, so either one is valid. A solution that only handles the strict less than case and forgets equality could produce incorrect behavior.

## Approaches

The straightforward approach is to compare every possible time between the two proposals and keep the smallest one. This works because the answer must be one of the two proposed times. However, even this description is already more work than necessary because there is no range to search. The only meaningful operation is deciding which of the two values is smaller.

The key observation is that the problem asks for a minimum of exactly two values. The minimum can be found directly with a single comparison, reducing the whole task to constant time.

The brute force and optimal approaches are effectively the same in complexity here because the input has only two numbers, but the direct comparison expresses the actual structure of the problem.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k) | O(1) | Unnecessary |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the two proposed swimming times from the input.
2. Compare the two values and choose the smaller one. The smaller time is always the earliest moment when both judges can agree to go swimming.
3. Print the chosen value.

Why it works: the only possible answers are the two proposed times. If the first time is smaller, choosing the second would delay the trip. If the second time is smaller, choosing the first would also delay it. When they are equal, both represent the same moment. The comparison always selects a valid minimum.

## Python Solution

```python
import sys
input = sys.stdin.readline

a, b = map(int, input().split())
print(min(a, b))
```

The program reads both integers in one line and uses Python's built in minimum operation. This directly matches the mathematical definition of the answer.

There are no loops or extra data structures, so there are no boundary conditions involving indices. Equality is handled automatically because `min` returns the shared value when both inputs are the same.

## Worked Examples

### Sample 1

Input:

```
4 2
```

The execution state is:

| Step | a | b | Chosen value |
| --- | --- | --- | --- |
| Read input | 4 | 2 | none |
| Compare values | 4 | 2 | 2 |
| Print answer | 4 | 2 | 2 |

The second proposal is earlier, so the algorithm selects it.

### Sample 2

Input:

```
5 9
```

The execution state is:

| Step | a | b | Chosen value |
| --- | --- | --- | --- |
| Read input | 5 | 9 | none |
| Compare values | 5 | 9 | 5 |
| Print answer | 5 | 9 | 5 |

The first proposal is already the earliest possible time.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | The program performs one comparison between two numbers. |
| Space | O(1) | Only the two input values are stored. |

The constraints are easily satisfied because the algorithm does not depend on the magnitude of the numbers or require any iteration.

## Test Cases

```python
import sys, io

def solve():
    import sys
    input = sys.stdin.readline
    a, b = map(int, input().split())
    print(min(a, b))

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    out = sys.stdout.getvalue()
    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return out

assert run("4 2\n") == "2\n", "sample 1"
assert run("5 9\n") == "5\n", "sample 2"

assert run("1 1\n") == "1\n", "equal values"
assert run("1000 999\n") == "999\n", "maximum boundary values"
assert run("999 1000\n") == "999\n", "reverse ordering"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | `1` | Equal proposals are handled correctly. |
| `1000 999` | `999` | Larger boundary values and second value being smaller. |
| `999 1000` | `999` | First value being smaller. |

## Edge Cases

For the equal values case:

```
1 1
```

The algorithm compares the values and finds that neither is smaller. The minimum operation returns `1`, which is correct because both judges chose the same moment.

For the second value being earlier:

```
10 3
```

The algorithm does not assume the first number has any priority. It compares both values and selects `3`, avoiding the common mistake of returning the first input.

For the largest allowed values:

```
1000 1000
```

Both numbers are valid and equal. The algorithm still performs a single comparison and outputs `1000` without any special handling.
