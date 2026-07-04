---
title: "CF 102897H - Hsueh- Draw Progress"
description: "The task is to render a command line progress indicator for multiple scenarios. Each scenario describes a total amount of work and how much of it is already completed."
date: "2026-07-04T09:21:00+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102897
codeforces_index: "H"
codeforces_contest_name: "The 3rd Hangzhou Normal University Freshman Programming Contest"
rating: 0
weight: 102897
solve_time_s: 48
verified: true
draft: false
---

[CF 102897H - Hsueh- Draw Progress](https://codeforces.com/problemset/problem/102897/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 48s  
**Verified:** yes  

## Solution
## Problem Understanding

The task is to render a command line progress indicator for multiple scenarios. Each scenario describes a total amount of work and how much of it is already completed. From this, we must construct a visual bar where completed units are shown as hash characters and remaining units are shown as hyphens. Alongside this bar, we also print a percentage value that represents the fraction of completed work scaled to 100 and rounded down.

Each test case gives two integers, the total number of units and the number of completed units. The output for each case is a single line consisting of a bracketed bar followed by a space and an integer percentage with a percent sign.

The key structural detail is that the progress bar has exactly one character per unit of total work. This means the output is not abstracted or scaled, it directly mirrors the input size.

The constraints allow up to ten test cases and each test case can have up to one hundred thousand units. This means a naive solution that constructs strings in quadratic time would be too slow, but any solution that builds each output line in linear time per test case is comfortably fast. The total work across all test cases is at most one million characters, which is well within typical output limits for one second.

A subtle edge case arises when no progress has been made or when everything is complete. When completed is zero, the bar should contain only hyphens and the percentage should be zero. When completed equals total, the bar should contain only hashes and the percentage should be exactly one hundred. Another edge case is when the total is one, where the bar degenerates into a single character, and rounding behavior must still be correct.

A common mistake is attempting to compute percentage using floating point division and rounding, which can introduce precision issues or incorrect rounding behavior. Another mistake is forgetting that integer division must be floor-based, not rounded to nearest.

## Approaches

A direct way to construct the output is to simulate the progress bar character by character. For each test case, we iterate from zero to n minus one, appending a hash if the index is less than m, otherwise appending a hyphen. After constructing the bar, we compute the percentage using integer division as m multiplied by 100 divided by n. This approach is correct because it directly follows the definition of the output format.

The inefficiency concern comes only from the repeated string concatenation if implemented poorly. If we repeatedly append to immutable strings inside a loop, the complexity can degrade toward quadratic behavior. However, if we construct a list of characters and join once, or use direct multiplication of strings, the construction remains linear.

The key observation is that both parts of the output are fully determined by simple arithmetic and repetition. There is no dependency between positions beyond whether the index is below m. This removes any need for simulation beyond direct construction.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Character-by-character concatenation (naive string append) | O(n^2) worst case | O(n) | Too slow |
| Direct construction using repetition or list join | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the total length n and completed amount m. These two values fully determine both the bar and the percentage.
2. Construct the progress bar by creating a string consisting of m hash characters followed by n minus m hyphens. This works because each position corresponds directly to one unit of work, and completed units always occupy the prefix.
3. Compute the percentage as integer division of m multiplied by 100 by n. This ensures truncation toward zero, matching the required floor behavior.
4. Format the output by wrapping the bar in square brackets, appending a space, then printing the computed percentage followed by a percent sign.

Why it works: the progress bar is a direct encoding of a prefix condition over a fixed-length array. Every valid representation must place all completed units first to match the sample structure, and every remaining unit afterward. The percentage computation is a linear scaling of the same ratio, so both outputs are consistent views of the same underlying fraction.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        bar = "#" * m + "-" * (n - m)
        percent = (m * 100) // n if n > 0 else 0
        sys.stdout.write(f"[{bar}] {percent}%\n")

if __name__ == "__main__":
    solve()
```

The implementation relies on Python’s native string repetition, which is efficient because it constructs the final string in linear time relative to its length. The expression `"#" * m` produces exactly m characters without incremental concatenation overhead. The same applies to the hyphen segment.

The percentage computation uses integer multiplication before division to avoid floating point precision issues. The conditional guard for `n > 0` is technically unnecessary under the constraints, but it makes the computation robust against malformed input.

## Worked Examples

Consider a case where n is 10 and m is 2. The bar must show two completed units followed by eight incomplete ones.

| Step | n | m | Bar construction | Percentage |
| --- | --- | --- | --- | --- |
| 1 | 10 | 2 | "" | - |
| 2 | 10 | 2 | "##--------" | - |
| 3 | 10 | 2 | "##--------" | 20 |

The bar correctly places two hashes at the front, and the percentage is floor(20).

Now consider n equals 5 and m equals 0.

| Step | n | m | Bar construction | Percentage |
| --- | --- | --- | --- | --- |
| 1 | 5 | 0 | "" | - |
| 2 | 5 | 0 | "-----" | - |
| 3 | 5 | 0 | "-----" | 0 |

This confirms that zero progress yields a fully dashed bar and zero percent.

These examples confirm both boundary behavior and consistency between the visual and numeric representations.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each character of the bar is generated exactly once using string repetition |
| Space | O(n) | The output string stores one character per unit of n |

The total work across all test cases is linear in the sum of all n values, which fits comfortably within the limits since n is at most 100000 per test case and there are at most 10 cases.

## Test Cases

```python
import sys, io

def solve_io():
    input = sys.stdin.readline
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        bar = "#" * m + "-" * (n - m)
        percent = (m * 100) // n
        sys.stdout.write(f"[{bar}] {percent}%\n")

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    try:
        solve_io()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# provided sample-style cases
assert run("1\n10 2\n") == "[##--------] 20%\n"
assert run("1\n5 0\n") == "[-----] 0%\n"

# minimum size
assert run("1\n1 0\n") == "[-] 0%\n"
assert run("1\n1 1\n") == "[#] 100%\n"

# full progress
assert run("1\n6 6\n") == "[######] 100%\n"

# mixed case
assert run("2\n3 1\n4 3\n") == "[#--] 33%\n[###-] 75%\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| n=1,m=0 | `[-] 0%` | smallest nontrivial bar |
| n=1,m=1 | `[#] 100%` | full completion edge case |
| n=m | full hashes | saturation correctness |
| multiple cases | multiple lines | handling of T |

## Edge Cases

When m equals zero, the construction produces an empty hash segment and a full hyphen segment. For example, with input n equals 5 and m equals 0, the expression `"#" * 0 + "-" * 5` yields `"-----"`, and the percentage `(0 * 100) // 5` evaluates to zero. The algorithm naturally handles this without special branching because string repetition with zero produces an empty string.

When m equals n, the hyphen segment becomes empty. For n equals 4 and m equals 4, the bar becomes `"####"` and the percentage evaluates to 100. This works because subtracting m from n yields zero, and repeating a string zero times correctly contributes nothing to the output.

When n equals 1, the bar degenerates into a single character. If m is zero, it becomes `"-"`, and if m is one, it becomes `"#"`. The integer division still produces either 0 or 100, matching expected behavior without needing floating point arithmetic.
