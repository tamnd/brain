---
title: "CF 105023A - Toy Trucks"
description: "We are given a single integer that represents the length of a toy truck in inches. The task is to decide whether this truck can be placed inside a toy box. The only constraint for fitting is that the truck’s length must not exceed 10 inches."
date: "2026-06-28T01:42:57+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105023
codeforces_index: "A"
codeforces_contest_name: "HPI 2024 Novice"
rating: 0
weight: 105023
solve_time_s: 53
verified: true
draft: false
---

[CF 105023A - Toy Trucks](https://codeforces.com/problemset/problem/105023/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 53s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single integer that represents the length of a toy truck in inches. The task is to decide whether this truck can be placed inside a toy box. The only constraint for fitting is that the truck’s length must not exceed 10 inches. If the length is 10 or less, the truck fits; otherwise it does not.

Although the problem is extremely small in structure, it still has the same shape as many decision problems: read a value, compare it against a fixed threshold, and output one of two possible answers based on that comparison.

The input size is minimal, a single integer bounded between 1 and 100. This immediately removes any need for algorithmic optimization or data structures. Even the most naive approach performs constant time work. The time limit of 1 second is irrelevant here, since the computation is a single comparison.

There are no tricky hidden constraints like multiple test cases or large arrays. The only subtle failure mode in problems of this type is incorrect handling of the comparison boundary. For example, treating the condition as strictly less than 10 instead of less than or equal to 10 would incorrectly reject length 10, even though it should be accepted. Similarly, confusing the direction of the inequality would invert all answers.

Concrete edge cases:

An input of 10 should produce YES because it exactly fits the limit. A careless condition like `L < 10` would incorrectly print NO.

An input of 11 should produce NO because it exceeds the maximum allowed size. Any condition using `L <= 11` by mistake would incorrectly accept it.

An input of 1 should produce YES, confirming that the lower bound is not special and everything positive up to 10 is valid.

## Approaches

A brute-force interpretation of this problem would still be trivial: read the integer and check whether it satisfies the constraint by direct comparison. There is no alternative interpretation of the problem that requires searching, sorting, or constructing auxiliary structures. Even if one attempted to frame it as scanning possible box sizes or enumerating fits, the structure collapses immediately because only one value exists.

The key observation is that the feasibility condition is explicitly defined: the truck fits if and only if its length is at most 10. That condition is already the complete solution. There is no hidden state or dependency between inputs, so no transformation beyond evaluation of a boolean expression is required.

Because the entire computation is a single comparison, both brute-force and optimized approaches coincide. The “optimization” is simply recognizing that no additional computation is necessary.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Direct comparison | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the integer L from input. This value represents the truck length that must be validated against the box capacity.
2. Compare L with 10 using a non-strict inequality check. The condition must be L ≤ 10, because equality is explicitly allowed by the problem definition.
3. If the condition holds, output "YES", otherwise output "NO". The output is purely a binary classification of whether the constraint is satisfied.

### Why it works

The algorithm is correct because the problem defines a single necessary and sufficient condition for validity. There are no intermediate transformations or secondary constraints. Every valid input is fully characterized by the inequality L ≤ 10, and every invalid input violates it. The algorithm directly evaluates this predicate, so it cannot misclassify any input as long as the comparison operator is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    L = int(input().strip())
    if L <= 10:
        print("YES")
    else:
        print("NO")

if __name__ == "__main__":
    solve()
```

The solution reads a single integer, trims input safely, and converts it to an integer. The conditional check is the core of the implementation. The boundary condition uses `<= 10`, which is essential because equality is allowed.

The structure is wrapped in a `solve()` function, which is standard practice in competitive programming for clarity and reuse. The main guard ensures the function executes when the script is run directly.

## Worked Examples

### Example 1

Input:

```
43
```

| Step | L | Condition (L ≤ 10) | Output |
| --- | --- | --- | --- |
| Read input | 43 | - | - |
| Evaluate | 43 | False | NO |

The value 43 is compared directly against the threshold 10. Since it exceeds the limit, the condition fails and the output is NO. This confirms that the algorithm correctly rejects oversized trucks.

### Example 2

Input:

```
2
```

| Step | L | Condition (L ≤ 10) | Output |
| --- | --- | --- | --- |
| Read input | 2 | - | - |
| Evaluate | 2 | True | YES |

Here the value is well within the allowed range. The comparison succeeds and the output is YES. This confirms correctness for valid small values.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | The algorithm performs a single input read and one integer comparison |
| Space | O(1) | Only one integer variable is stored |

The constraints guarantee that even the simplest implementation easily fits within limits. The solution performs constant work regardless of input value.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    import io as sysio

    out = sysio.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided samples
assert run("43\n") == "NO"
assert run("2\n") == "YES"

# custom cases
assert run("10\n") == "YES", "boundary inclusive"
assert run("11\n") == "NO", "just above boundary"
assert run("1\n") == "YES", "minimum value"
assert run("100\n") == "NO", "maximum constraint violation"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 10 | YES | boundary inclusion correctness |
| 11 | NO | first invalid value above threshold |
| 1 | YES | minimum valid case |
| 100 | NO | upper bound invalid case |

## Edge Cases

The only meaningful edge case is the boundary at 10. For input 10, the algorithm evaluates `10 ≤ 10`, which is true, so it outputs YES. Any implementation that mistakenly uses a strict inequality would fail here.

For input 11, the condition `11 ≤ 10` evaluates to false, producing NO as expected. This confirms correct rejection of just-out-of-range values.

For input 1, the condition `1 ≤ 10` is true, confirming that the lower bound does not require special handling and the logic is uniformly applied across the entire valid range.
