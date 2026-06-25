---
title: "CF 106020B - Free Problems"
description: "This problem is a small output only trick hidden inside a normal programming contest format. The judges ask whether you want a free problem. The only accepted response is the exact string Yee. Any other text, including common confirmations such as Yes, is rejected."
date: "2026-06-25T13:10:06+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106020
codeforces_index: "B"
codeforces_contest_name: "The 2025 Damascus University Collegiate Programming Contest"
rating: 0
weight: 106020
solve_time_s: 46
verified: true
draft: false
---

[CF 106020B - Free Problems](https://codeforces.com/problemset/problem/106020/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 46s  
**Verified:** yes  

## Solution
## Problem Understanding

This problem is a small output only trick hidden inside a normal programming contest format. The judges ask whether you want a free problem. The only accepted response is the exact string `Yee`. Any other text, including common confirmations such as `Yes`, is rejected.

The input section is effectively irrelevant for the solution. Even if the judge provides some input stream, the required answer does not depend on its contents. The program only needs to print the required word.

The constraints imply that there is no need to analyze data, store arrays, build graphs, or perform any computation. A solution that reads the entire input or performs unnecessary work would still pass for normal limits, but it solves a harder problem than the one being asked. The intended operation count is constant, which is the only reasonable approach for a problem where the output is fixed.

The main edge cases are not about algorithms but about exact output matching. A common mistake is printing `Yes` because it sounds like the correct answer. For example, the output for the problem is:

```
Yes
```

The correct output is not this string, so the submission is rejected.

Another mistake is adding extra text. For example:

```
Yee!
```

is different from the required output because the exclamation mark changes the string. The judge compares the output exactly.

## Approaches

A brute force approach would try to understand the story, read input values, simulate the interaction, or search for a hidden condition that decides the answer. This fails as a strategy because there is no changing condition to compute. The number of possible inputs is irrelevant because every case has the same answer.

The key observation is that the problem is testing attention to the exact output requirement rather than algorithmic skill. Once we recognize that the answer is a fixed string, the whole solution reduces to printing that string.

The brute force idea is effectively unbounded in unnecessary work, while the intended solution uses one output operation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(input size) | O(input size) | Too slow in spirit and unnecessary |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Ignore the input because it does not influence the answer. The required output is determined entirely by the statement.
2. Print the exact string `Yee`. The capitalization and spelling must match because the judge checks the output text directly.

Why it works:

The only condition needed for acceptance is producing the required response. Since the same response is valid for every possible test case, printing it directly always satisfies the judge.

## Python Solution

```python
import sys
input = sys.stdin.readline

print("Yee")
```

The solution contains only one operation that matters: printing the required answer. There are no boundary conditions, loops, data structures, or arithmetic operations to get wrong.

The program does not need to consume the input. Python automatically exits after printing, and the judge only checks the produced output. The exact spelling of `Yee` is the only implementation detail that matters.

## Worked Examples

Since every possible input produces the same output, the traces are identical.

Sample 1:

| Step | Action | Output |
| --- | --- | --- |
| 1 | Program starts | empty |
| 2 | Print fixed answer | Yee |

This trace shows that the algorithm does not depend on any provided values.

Sample 2:

| Step | Action | Output |
| --- | --- | --- |
| 1 | Program starts | empty |
| 2 | Print fixed answer | Yee |

This demonstrates that even a completely different input cannot change the result.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | The program performs one print operation. |
| Space | O(1) | No variables or data structures are stored. |

The solution fits any reasonable time and memory limit because it does constant work regardless of input size.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    print("Yee")

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

# provided samples style
assert run("") == "Yee\n", "empty input"
assert run("1\n") == "Yee\n", "arbitrary input"

# custom cases
assert run("100 200 300\n") == "Yee\n", "input should not matter"
assert run("abc\n") == "Yee\n", "non numeric input should not matter"
assert run("999999999999999999\n") == "Yee\n", "large input should not matter"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Empty input | Yee | Confirms no input is required |
| `1` | Yee | Confirms normal input is ignored |
| Large number | Yee | Confirms there is no dependency on values |
| Arbitrary text | Yee | Confirms the solution only prints the fixed answer |

## Edge Cases

For the case where someone prints `Yes` instead of `Yee`, the algorithm fails because the output string is different. The correct execution is simply printing `Yee`, which matches the required response exactly.

For the case where someone prints additional characters, such as `Yee!`, the algorithm also fails because output comparison is character based. The correct trace is a single print operation producing only `Yee`.

For any input at all, such as a large number or unrelated text, the algorithm performs the same action. It does not parse the input, so there are no overflow issues, indexing mistakes, or invalid assumptions about the data.
