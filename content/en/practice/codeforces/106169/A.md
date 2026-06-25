---
title: "CF 106169A - Borg Cube"
description: "A cube has six face values: top, bottom, left, right, front, back. Every corner of the cube touches exactly three faces. The value hidden at a corner is defined as the product of the three face values meeting at that corner. There are eight corners in total."
date: "2026-06-25T11:07:50+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106169
codeforces_index: "A"
codeforces_contest_name: "2025-2026 ICPC NERC, Kyrgyzstan Regional Contest"
rating: 0
weight: 106169
solve_time_s: 40
verified: true
draft: false
---

[CF 106169A - Borg Cube](https://codeforces.com/problemset/problem/106169/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 40s  
**Verified:** yes  

## Solution
## Problem Understanding

A cube has six face values:

`top, bottom, left, right, front, back`.

Every corner of the cube touches exactly three faces. The value hidden at a corner is defined as the product of the three face values meeting at that corner.

There are eight corners in total. The required code is the sum of the values of all eight corners.

The input gives the six face values. We must compute the sum of the eight corner products.

The constraints are extremely small. Each face value is at most 500, so even a direct enumeration of all corners is trivial. The largest possible corner value is:

`500 × 500 × 500 = 125,000,000`

and the sum of eight such values is `1,000,000,000`, which matches the stated output bound. Standard integer arithmetic is sufficient.

The only subtle part is correctly identifying all eight corners. Each corner must contain exactly one face from each opposite pair:

Top or Bottom.

Left or Right.

Front or Back.

A common mistake is to accidentally miss some corners or count one twice.

Consider:

```
1 1 1 1 1 1
```

Every corner value equals 1, so the answer is:

```
8
```

If only seven corners are counted, the result becomes 7.

Another easy mistake is mixing up opposite faces. For example:

```
1 2 3 4 5 6
```

One corner is `top × left × front = 1 × 3 × 5 = 15`.

A product such as `top × bottom × front` is invalid because top and bottom never meet at the same corner.

## Approaches

The most direct solution is to explicitly compute all eight corner products and add them together.

The corners are:

`(top,left,front)`

`(top,left,back)`

`(top,right,front)`

`(top,right,back)`

`(bottom,left,front)`

`(bottom,left,back)`

`(bottom,right,front)`

`(bottom,right,back)`

This requires only eight multiplications of three numbers and a few additions, which is effectively constant time.

There is also a useful algebraic observation. Every corner chooses one face from each opposite pair. Expanding

```
(top + bottom)
× (left + right)
× (front + back)
```

produces exactly the eight corner products, each appearing once.

For example, choosing `top` from the first parenthesis, `right` from the second, and `back` from the third contributes the corner product:

```
top × right × back
```

Since all eight combinations appear exactly once, the desired sum is simply:

```
(top + bottom)
× (left + right)
× (front + back)
```

This turns the problem into a single formula.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Enumeration | O(1) | O(1) | Accepted |
| Product of Sums | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the six face values: top, bottom, left, right, front, and back.
2. Compute the sum of the opposite vertical faces:

```
top + bottom
```
3. Compute the sum of the opposite horizontal faces:

```
left + right
```
4. Compute the sum of the opposite front-back faces:

```
front + back
```
5. Multiply these three sums together.

Expanding the product generates every valid corner combination exactly once.
6. Output the result.

### Why it works

Every corner is formed by choosing one face from each pair of opposite faces. The three pairs are:

```
(top, bottom)
(left, right)
(front, back)
```

The expression

```
(top + bottom)
× (left + right)
× (front + back)
```

contains one term for every possible choice from these three pairs. Since there are `2 × 2 × 2 = 8` choices, the expansion contains exactly the eight corner products and nothing else. Their sum is precisely the required code.

## Python Solution

```python
import sys
input = sys.stdin.readline

top, bottom, left, right, front, back = map(int, input().split())

answer = (top + bottom) * (left + right) * (front + back)

print(answer)
```

The implementation follows the formula directly.

The six values are read in the order specified by the statement. The expression computes the sum over all corner products without explicitly listing the corners.

Since the maximum answer is at most `10^9`, Python's integer type easily handles it. There are no indexing issues, loops, or boundary conditions to worry about.

## Worked Examples

### Example 1

Input:

```
1 2 3 4 4 5
```

| Variable | Value |
| --- | --- |
| top + bottom | 3 |
| left + right | 7 |
| front + back | 9 |
| answer | 3 × 7 × 9 = 189 |

Output:

```
189
```

This example demonstrates the expansion idea. The value 189 equals the sum of all eight explicitly computed corner products.

### Example 2

Input:

```
1 1 1 1 1 1
```

| Variable | Value |
| --- | --- |
| top + bottom | 2 |
| left + right | 2 |
| front + back | 2 |
| answer | 2 × 2 × 2 = 8 |

Output:

```
8
```

Every corner product equals 1, and there are eight corners, so the answer is 8.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | A fixed number of arithmetic operations |
| Space | O(1) | Only a few variables are stored |

The algorithm performs constant work regardless of the input values. It comfortably fits within any reasonable contest limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    top, bottom, left, right, front, back = map(int, input().split())
    return str((top + bottom) * (left + right) * (front + back))

# provided sample
assert run("1 2 3 4 4 5\n") == "189", "sample 1"

# minimum values
assert run("1 1 1 1 1 1\n") == "8", "all ones"

# asymmetric values
assert run("1 2 3 4 5 6\n") == "231", "general case"

# all maximum values
assert run("500 500 500 500 500 500\n") == "1000000000", "upper bound"

# one large pair, others small
assert run("500 1 1 1 1 1\n") == "2004", "boundary arithmetic"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1 1 1 1` | `8` | Every corner contributes equally |
| `1 2 3 4 5 6` | `231` | General non-symmetric case |
| `500 500 500 500 500 500` | `1000000000` | Maximum possible answer |
| `500 1 1 1 1 1` | `2004` | Correct handling of uneven values |

## Edge Cases

Consider:

```
1 1 1 1 1 1
```

The algorithm computes:

```
(1 + 1)(1 + 1)(1 + 1)
= 2 × 2 × 2
= 8
```

All eight corners contribute exactly 1. The result confirms that every corner is counted once.

Consider:

```
1 2 3 4 5 6
```

The algorithm computes:

```
(1 + 2)(3 + 4)(5 + 6)
= 3 × 7 × 11
= 231
```

Expanding the product yields the eight valid corner products:

```
1·3·5
1·3·6
1·4·5
1·4·6
2·3·5
2·3·6
2·4·5
2·4·6
```

and their sum is 231. No invalid combination such as `top × bottom × front` appears in the expansion.

Finally, for the largest allowed values:

```
500 500 500 500 500 500
```

the algorithm computes:

```
1000 × 1000 × 1000
= 1,000,000,000
```

which matches the maximum possible answer and remains safely within integer limits.
