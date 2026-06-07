---
title: "CF 486A - Calculating Function"
description: "We are given a single integer n and asked to evaluate the alternating sum $$-1 + 2 - 3 + 4 - 5 + dots + (-1)^n n.$$ The sign of each term depends on its position. Odd numbers are subtracted and even numbers are added. The output is the final value of this sum."
date: "2026-06-07T17:26:54+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 486
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 277 (Div. 2)"
rating: 800
weight: 486
solve_time_s: 94
verified: true
draft: false
---

[CF 486A - Calculating Function](https://codeforces.com/problemset/problem/486/A)

**Rating:** 800  
**Tags:** implementation, math  
**Solve time:** 1m 34s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single integer `n` and asked to evaluate the alternating sum

$$-1 + 2 - 3 + 4 - 5 + \dots + (-1)^n n.$$

The sign of each term depends on its position. Odd numbers are subtracted and even numbers are added. The output is the final value of this sum.

The constraint is the key part of the problem. The value of `n` can be as large as $10^{15}$. A direct simulation that iterates from `1` to `n` would require up to one quadrillion iterations, which is completely impossible within a one second time limit. Even $10^8$ operations would already be too much, so we need a mathematical formula that computes the answer in constant time.

A common mistake is mishandling the parity of `n`.

Consider:

Input:

```
1
```

The sum is simply `-1`, so the correct output is:

```
-1
```

A careless implementation that assumes every pair contributes `1` and returns `n/2` would incorrectly produce `0`.

Another edge case appears when `n` is odd.

Input:

```
5
```

The sum is:

$$-1 + 2 - 3 + 4 - 5 = -3.$$

The correct output is:

```
-3
```

If we use the formula for even `n` without treating odd values separately, we would incorrectly return `2`.

The largest allowed value also deserves attention.

Input:

```
1000000000000000
```

The answer is:

```
500000000000000
```

Languages with fixed-size integer types could overflow in some problems of this scale. Python integers automatically expand, so no special handling is required.

## Approaches

The most direct solution is to compute the sum exactly as written. We start from zero, iterate through every integer from `1` to `n`, subtract odd values, add even values, and print the result.

This approach is correct because it follows the definition term by term. The problem is its running time. When `n = 10^{15}`, the algorithm would perform roughly one quadrillion iterations. Such a program would never finish within the time limit.

The structure of the expression gives us a much better idea. Look at consecutive pairs:

$$(-1 + 2) = 1$$

$$(-3 + 4) = 1$$

$$(-5 + 6) = 1$$

Every complete odd-even pair contributes exactly `1`.

When `n` is even, all numbers are grouped into pairs. There are `n/2` pairs, so the answer is simply:

$$\frac{n}{2}.$$

When `n` is odd, the first `n-1` numbers form `(n-1)/2` complete pairs, contributing:

$$\frac{n-1}{2}.$$

The last remaining term is `-n`, so:

$$\frac{n-1}{2} - n = -\frac{n+1}{2}.$$

This gives a constant-time solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(1) | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the integer `n`.
2. Check whether `n` is even.
3. If `n` is even, output `n // 2`.

Every odd-even pair contributes exactly `1`, and there are `n/2` such pairs.
4. Otherwise, output `-(n + 1) // 2`.

The first `n-1` numbers form complete pairs, and the final unpaired term is `-n`.

### Why it works

For every odd integer `k`, the consecutive terms `-k` and `k+1` contribute:

$$-k + (k+1) = 1.$$

When `n` is even, the entire sequence consists of exactly `n/2` such pairs, giving a total of `n/2`.

When `n` is odd, the first `n-1` terms form `(n-1)/2` pairs whose contribution is `(n-1)/2`. The remaining term is `-n`, producing

$$\frac{n-1}{2} - n = -\frac{n+1}{2}.$$

These formulas match the original sum exactly, so the algorithm is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())

if n % 2 == 0:
    print(n // 2)
else:
    print(-(n + 1) // 2)
```

The program begins by reading `n`.

The parity of `n` completely determines the answer. For even values, every number belongs to a complete pair and each pair contributes `1`, so we print `n // 2`.

For odd values, one negative term remains unpaired at the end. The closed-form result is `-(n + 1) // 2`.

The implementation uses integer arithmetic only. Python's arbitrary-precision integers safely handle values up to and beyond $10^{15}$.

## Worked Examples

### Example 1

Input:

```
4
```

| Step | n | Condition | Result |
| --- | --- | --- | --- |
| Read input | 4 | Even | - |
| Apply formula | 4 | Even | 4 // 2 = 2 |

Output:

```
2
```

This example shows the even case. The terms form two pairs:

$$(-1+2) + (-3+4) = 1+1 = 2.$$

### Example 2

Input:

```
5
```

| Step | n | Condition | Result |
| --- | --- | --- | --- |
| Read input | 5 | Odd | - |
| Apply formula | 5 | Odd | -(5 + 1) // 2 = -3 |

Output:

```
-3
```

This example shows the odd case. The first four numbers contribute `2`, and the final term `-5` changes the result to `-3`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a few arithmetic operations are performed |
| Space | O(1) | No additional data structures are used |

The algorithm performs a constant amount of work regardless of the size of `n`. Even when `n = 10^{15}`, the running time is effectively instantaneous and easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(sys.stdin.readline())

    if n % 2 == 0:
        return str(n // 2)
    else:
        return str(-(n + 1) // 2)

# provided sample
assert run("4\n") == "2", "sample 1"

# custom cases
assert run("1\n") == "-1", "minimum input"
assert run("2\n") == "1", "small even case"
assert run("5\n") == "-3", "small odd case"
assert run("1000000000000000\n") == "500000000000000", "maximum even value"
assert run("999999999999999\n") == "-500000000000000", "maximum odd value"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `-1` | Minimum allowed input |
| `2` | `1` | Smallest even case |
| `5` | `-3` | Odd-number formula |
| `1000000000000000` | `500000000000000` | Largest even value |
| `999999999999999` | `-500000000000000` | Largest odd value |

## Edge Cases

Consider the smallest possible input:

```
1
```

The algorithm detects that `n` is odd and computes:

$$-\frac{1+1}{2} = -1.$$

The output is:

```
-1
```

This matches the original sum, which contains only one term.

Now consider an odd value where one term remains unpaired:

```
5
```

The algorithm computes:

$$-\frac{5+1}{2} = -3.$$

The actual sum is:

$$-1+2-3+4-5=-3.$$

The result matches exactly.

Finally, consider the largest odd input:

```
999999999999999
```

The algorithm computes:

$$-\frac{999999999999999+1}{2} = -500000000000000.$$

No iteration is performed, so the running time remains constant. Python's integer arithmetic handles the value safely, producing the correct answer immediately.
