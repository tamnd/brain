---
title: "CF 2195A - Sieve of Erato67henes"
description: "We are given several very small collections of integers, each collection containing at most five numbers, and we are asked whether we can pick some non-empty subset whose product is exactly 67. Each test case is independent."
date: "2026-06-07T20:37:13+07:00"
tags: ["codeforces", "competitive-programming", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 2195
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 1080 (Div. 3)"
rating: 800
weight: 2195
solve_time_s: 71
verified: true
draft: false
---

[CF 2195A - Sieve of Erato67henes](https://codeforces.com/problemset/problem/2195/A)

**Rating:** 800  
**Tags:** math, number theory  
**Solve time:** 1m 11s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several very small collections of integers, each collection containing at most five numbers, and we are asked whether we can pick some non-empty subset whose product is exactly 67.

Each test case is independent. Inside a test case, we are allowed to choose any subset of the given numbers, as long as we choose at least one element, and we multiply all chosen values together. The question is whether there exists any such subset whose product equals 67 exactly.

The constraint that each test case has at most five numbers completely changes the nature of the problem. A set of size five has only $2^5 - 1 = 31$ non-empty subsets, so even brute force enumeration of all subsets is trivial across $10^4$ test cases. This immediately rules out any need for sophisticated number theory or optimization tricks.

A subtle issue arises from the fact that the target value 67 is prime. This means any valid selection must multiply to exactly 67, so the only way to succeed is to pick numbers whose product contains no extra prime factors and exactly matches 67. Since all input values are between 1 and 67 inclusive, the only numbers that can contribute meaningfully are 1 and 67, because every other integer introduces prime factors not compatible with 67.

A naive mistake would be to assume that combinations like 7 and 9 or 3 and 23 might somehow combine into 67. This is impossible because 67 has no non-trivial factorization over integers greater than 1.

Another potential pitfall is forgetting that selecting no elements is forbidden. For example, if no element equals 67 and all elements are 1, a careless implementation might incorrectly conclude success by treating the empty product as 1 and then “scaling up,” but that is not allowed.

Edge cases include:

If the array contains a single element equal to 67, the answer is clearly YES.

Input:

```
1
1
67
```

Output:

```
YES
```

If the array contains only ones and small composite numbers like 2, 3, 5, 7, then no combination can form 67.

Input:

```
1
5
1 2 3 4 5
```

Output:

```
NO
```

This is because any non-one selection introduces factors unrelated to 67.

## Approaches

The brute-force idea is straightforward. We try every non-empty subset of the given numbers, compute its product, and check whether it equals 67. Since $n \le 5$, we have at most 31 subsets, so this is at most 31 multiplications per test case. Across $10^4$ test cases, this is roughly $3.1 \times 10^5$ operations, which is comfortably within limits.

The key observation is that we do not even need to compute full products. The target is a fixed number, 67, which is prime. Any factor other than 1 or 67 immediately makes it impossible to reach 67. This means we only need to check whether we can pick either a single 67, or combine only 1s and a 67. Since multiplying by 1 does nothing, the only meaningful requirement is the presence of at least one 67 in the array. If a 67 exists, we can ignore all other numbers and choose just that element.

So the problem reduces from subset enumeration to a simple existence check.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (all subsets) | $O(t \cdot 2^n)$ | $O(1)$ | Accepted |
| Optimal (check existence of 67) | $O(t \cdot n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. For each test case, read the list of numbers. We only need to determine whether 67 appears at least once, because any valid subset must include a 67 and cannot include any number greater than 1 that is not 67.
2. Scan through the array and check if any element equals 67. The moment we find it, we know a valid subset exists by selecting only that element.
3. If we finish scanning without finding 67, conclude that no subset can produce 67, since all other numbers are either 1 or introduce irreducible factors that cannot form 67.

### Why it works

The correctness comes from the structure of 67. Since 67 is prime, any product equal to 67 must consist of exactly one factor equal to 67 and all other factors equal to 1. No combination of integers greater than 1 other than 67 itself can avoid introducing extra prime factors. Therefore, existence of the number 67 in the array is both necessary and sufficient for the answer to be YES.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    arr = list(map(int, input().split()))
    
    ok = False
    for x in arr:
        if x == 67:
            ok = True
            break
    
    print("YES" if ok else "NO")
```

The solution processes each test case independently and performs a linear scan over at most five numbers. The early break ensures minimal work in cases where 67 appears early.

The key implementation detail is that we do not attempt to compute products at all. That avoids unnecessary integer growth concerns and keeps the logic aligned with the mathematical structure of the target value.

## Worked Examples

### Example 1

Input:

```
5
1 7 6 7 67
```

We track whether 67 appears.

| Step | Current value | Found 67? |
| --- | --- | --- |
| 1 | 1 | No |
| 2 | 7 | No |
| 3 | 6 | No |
| 4 | 7 | No |
| 5 | 67 | Yes |

Once 67 is encountered, we can immediately stop. Any subset containing only this element already gives product 67.

Output is YES.

This trace shows that intermediate values like 7 or 6 do not matter at all, confirming that only exact presence of 67 is relevant.

### Example 2

Input:

```
5
1 3 5 7 8
```

| Step | Current value | Found 67? |
| --- | --- | --- |
| 1 | 1 | No |
| 2 | 3 | No |
| 3 | 5 | No |
| 4 | 7 | No |
| 5 | 8 | No |

No 67 is found, so no subset can produce the required product.

Output is NO.

This trace demonstrates that even though multiple numbers exist, none contribute toward constructing 67, since they introduce incompatible prime factors.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(t \cdot n)$ | Each test case scans at most 5 elements once |
| Space | $O(1)$ | No auxiliary storage beyond a few variables |

The constraints are extremely small per test case, so even a brute-force subset enumeration would pass, but the optimized existence check reduces the solution to constant work per test case in practice.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        arr = list(map(int, input().split()))
        ok = any(x == 67 for x in arr)
        out.append("YES" if ok else "NO")
    return "\n".join(out)

# provided samples
assert run("""2
5
1 7 6 7 67
5
1 3 5 7 8
""") == """YES
NO"""

# single element success
assert run("""1
1
67
""") == "YES"

# single element failure
assert run("""1
1
5
""") == "NO"

# all ones
assert run("""1
5
1 1 1 1 1
""") == "NO"

# mixed small numbers
assert run("""1
5
2 3 4 5 6
""") == "NO"

# multiple test cases
assert run("""3
3
1 1 67
2
7 11
4
67 67 1 1
""") == """YES
NO
YES"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single 67 | YES | minimal positive case |
| single non-67 | NO | minimal negative case |
| all ones | NO | 1s cannot create 67 |
| composite mix | NO | unrelated factors cannot help |
| multiple tests with duplicates | YES/NO mix | correctness across cases |

## Edge Cases

A single-element array containing 67 is the most direct success case. The algorithm reads the single value, detects equality immediately, and returns YES without further work.

An array of only ones is a case where multiplication intuition can mislead. Even though any subset product is 1, no subset can reach 67, so the scan completes without finding 67 and returns NO.

A case with multiple 67s, such as `[67, 67, 1, 1]`, still behaves correctly because the algorithm does not care about count. The first occurrence triggers YES, and the rest are irrelevant.
