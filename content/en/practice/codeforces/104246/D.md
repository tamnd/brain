---
title: "CF 104246D - Distribute the Pizza"
description: "A pizza is cut into identical slices, and each slice is a sector defined by a fixed central angle θ. The radius r is irrelevant for the distribution question because all slices are congruent; what matters is only how many equal angular pieces the full 360° circle is partitioned…"
date: "2026-07-01T23:01:55+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104246
codeforces_index: "D"
codeforces_contest_name: "CodeSmash 2021 by RAPL"
rating: 0
weight: 104246
solve_time_s: 83
verified: false
draft: false
---

[CF 104246D - Distribute the Pizza](https://codeforces.com/problemset/problem/104246/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 23s  
**Verified:** no  

## Solution
## Problem Understanding

A pizza is cut into identical slices, and each slice is a sector defined by a fixed central angle θ. The radius r is irrelevant for the distribution question because all slices are congruent; what matters is only how many equal angular pieces the full 360° circle is partitioned into.

From the statement, we are not directly given the number of slices. Instead, we are told the slice angle θ, which implicitly defines the number of slices as 360 / θ, and we are guaranteed this is an integer for every test case.

Two people want to split the pizza so that both receive an integer number of whole slices, and both get the same number of slices. Since slices cannot be subdivided, the problem reduces to checking whether the total number of slices is even.

The input size is small, with up to 2400 test cases and constant-time arithmetic per case. This strongly suggests that any O(1) per test case solution is sufficient, and even simple arithmetic or modular checks are well within limits. Anything involving iteration over slices or factoring is unnecessary.

A subtle edge case arises when θ is large, such as θ = 360. In that case, there is only one slice, and it is impossible to split it equally between two people. Another corner case is θ = 180, where there are exactly two slices and a fair split is possible.

## Approaches

A direct way to think about the problem is to first compute the number of slices n = 360 / θ. Once we have n, the question becomes whether n can be divided into two equal integers, meaning whether n is divisible by 2.

The brute-force mindset would be to simulate cutting the pizza or explicitly counting slices, but that is already unnecessary since the slice count is determined by a simple division. Any approach that iterates around the circle or builds slices explicitly would still run in constant time per case but is conceptually overkill.

The key observation is that fairness between two people is equivalent to asking whether the total number of identical units is even. The geometry and radius play no role beyond guaranteeing that slices are congruent; only the parity of the slice count matters.

Thus the problem reduces to checking whether (360 / θ) % 2 == 0, which can be rewritten as checking whether 360 / θ is even.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Direct slice counting | O(1) | O(1) | Accepted |
| Optimal parity check | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read θ for each test case and compute the number of slices n as 360 divided by θ. The problem guarantees divisibility, so no rounding issues occur.
2. Check whether n is divisible by 2. This determines whether the slices can be partitioned into two equal groups without breaking any slice.
3. If n is even, output "YES". Otherwise, output "NO".

### Why it works

Each slice is an indivisible unit of resource. Any valid distribution assigns whole slices only, so the problem reduces to partitioning n identical objects into two equal-sized sets. Such a partition exists if and only if n is even. No geometric property other than the total count influences feasibility, so parity is both necessary and sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        r, theta = map(int, input().split())
        n = 360 // theta
        if n % 2 == 0:
            print("YES")
        else:
            print("NO")

if __name__ == "__main__":
    solve()
```

The solution reads each test case independently and ignores r, since it does not affect the number of slices. The integer division 360 // θ is safe because the problem guarantees that θ divides 360. The parity check directly encodes the feasibility condition.

A common implementation mistake is attempting floating-point division for 360 / θ and then checking parity, which can introduce precision issues in other problems. Here, using integer division avoids any such risk and aligns with the discrete structure of slices.

## Worked Examples

Consider θ values that produce different slice counts.

### Example 1

Input:

```
r = 10, θ = 45
```

Here n = 360 / 45 = 8.

| Step | Value |
| --- | --- |
| θ | 45 |
| n = 360 / θ | 8 |
| n % 2 | 0 |
| Output | YES |

Since 8 slices can be split into 4 and 4, the output is YES.

### Example 2

Input:

```
r = 5, θ = 60
```

Here n = 360 / 60 = 6.

| Step | Value |
| --- | --- |
| θ | 60 |
| n = 6 |  |
| n % 2 | 0 |
| Output | YES |

This shows an even slice count still yields a valid split.

### Example 3

Input:

```
r = 8, θ = 120
```

Here n = 360 / 120 = 3.

| Step | Value |
| --- | --- |
| θ | 120 |
| n = 3 |  |
| n % 2 | 1 |
| Output | NO |

This demonstrates the failure case when slices are odd in number.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case requires constant-time arithmetic and a modulo check |
| Space | O(1) | No additional data structures are used beyond a few variables |

The constraints allow up to 2400 test cases, so a linear scan over input is trivial within time limits. Each iteration performs only a couple of integer operations, ensuring the solution runs comfortably within 1 second.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = []
    input = sys.stdin.readline

    t = int(input())
    for _ in range(t):
        r, theta = map(int, input().split())
        n = 360 // theta
        out.append("YES" if n % 2 == 0 else "NO")

    return "\n".join(out)

# provided samples
assert run("3\n10 45\n5 40\n8 60\n") == "YES\nNO\nYES"

# custom cases
assert run("1\n1 360\n") == "NO", "single slice"
assert run("1\n1 180\n") == "YES", "two slices"
assert run("1\n10 90\n") == "YES", "four slices"
assert run("1\n10 120\n") == "NO", "three slices"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 360 | NO | single slice cannot be split |
| 1 180 | YES | minimal valid even split |
| 1 90 | YES | typical even case |
| 1 120 | NO | odd number of slices case |

## Edge Cases

When θ = 360, the pizza consists of a single slice. The algorithm computes n = 1, detects odd parity, and correctly returns NO.

When θ = 180, there are exactly two slices. The computation yields n = 2, and parity is even, producing YES, matching the only possible fair split.

When θ = 1 or any small divisor of 360, the algorithm still behaves consistently because it relies only on integer arithmetic and parity, so no precision or scaling issues arise.
