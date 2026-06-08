---
title: "CF 1915C - Can I Square?"
description: "We are given several buckets, and each bucket contains some number of unit squares. All squares are identical and have side length 1. The question is simple: if we take every square from every bucket, can they be arranged to form one larger square with no squares left over?"
date: "2026-06-08T19:55:54+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1915
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 918 (Div. 4)"
rating: 800
weight: 1915
solve_time_s: 121
verified: true
draft: false
---

[CF 1915C - Can I Square?](https://codeforces.com/problemset/problem/1915/C)

**Rating:** 800  
**Tags:** binary search, implementation  
**Solve time:** 2m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several buckets, and each bucket contains some number of unit squares. All squares are identical and have side length 1.

The question is simple: if we take every square from every bucket, can they be arranged to form one larger square with no squares left over?

If the total number of unit squares is $S$, then a larger square can be built exactly when its area is $S$. Since the area of a square must be a perfect square number, the task reduces to checking whether the sum of all bucket contents is a perfect square.

The constraints are small enough that we can process every element exactly once. Across all test cases, the total number of values is at most $2 \cdot 10^5$, so an $O(n)$ solution per test case is easily fast enough. Any approach that repeatedly searches or iterates over the same values would be unnecessary.

One subtle point is that individual values can be as large as $10^9$. Since there can be up to $2 \cdot 10^5$ numbers overall, the total sum can become very large. In languages with fixed-size integer types, using a type that is too small would overflow. Python integers grow automatically, so this is not an issue here.

Another easy mistake is checking only whether the square root is an integer using floating-point arithmetic. Large numbers can suffer from precision issues. For example:

```
1
2
1000000000 1000000000
```

The sum is $2000000000$, which is not a perfect square. Floating-point rounding can occasionally cause incorrect comparisons for large values. Using an integer square root avoids that risk.

A different edge case occurs when there is only one bucket:

```
1
1
9
```

The total number of squares is 9, which equals $3^2$, so the correct answer is:

```
YES
```

A careless implementation that tries to construct dimensions explicitly rather than checking the area could overcomplicate this case.

## Approaches

The most direct idea is to compute the total number of unit squares and then determine whether that number can be written as $k^2$ for some integer $k$.

A brute-force version would repeatedly try values of $k$ until $k^2$ reaches or exceeds the total sum. If the sum is $S$, this requires up to $\sqrt{S}$ iterations. Since the sum can be extremely large, this becomes impractical. For example, a sum near $2 \cdot 10^{14}$ would require around $1.4 \cdot 10^7$ checks.

The key observation is that the arrangement of squares does not matter. Only the total count matters. Once we know the total area, the problem becomes a perfect-square test.

Instead of searching for a square root manually, we can compute the integer square root of the sum. Let

$$r = \lfloor \sqrt{S} \rfloor.$$

If $r^2 = S$, then $S$ is a perfect square and the answer is "YES". Otherwise, the answer is "NO".

This reduces the problem to a single pass through the input values plus one square-root computation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n + \sqrt{S})$ | $O(1)$ | Too slow |
| Optimal | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases.
2. For each test case, read $n$ and the array of bucket contents.
3. Compute the total number of unit squares:

$$S = \sum a_i$$

Since every square must be used, this total is exactly the area of the final figure.
4. Compute the integer square root $r$ of $S$.

The integer square root is the largest integer whose square does not exceed $S$.
5. Check whether $r^2 = S$.

If equality holds, $S$ is a perfect square and a square can be formed.
6. Output `"YES"` when $r^2 = S$, otherwise output `"NO"`.

### Why it works

A square with side length $k$ has area $k^2$. The total number of available unit squares is $S$, so any square built from all pieces must have area exactly $S$.

If $S$ is a perfect square, choose side length $k = \sqrt{S}$ and the construction is possible.

If $S$ is not a perfect square, no integer side length can produce area $S$, so constructing a square is impossible.

The algorithm checks exactly this necessary and sufficient condition, which guarantees correctness.

## Python Solution

```python
import sys
from math import isqrt

input = sys.stdin.readline

t = int(input())

for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))

    total = sum(a)
    root = isqrt(total)

    print("YES" if root * root == total else "NO")
```

The first step computes the total area by summing all bucket contents.

The function `isqrt()` returns the integer square root without using floating-point arithmetic. This avoids precision problems that can occur when numbers become large.

After obtaining `root`, the code checks whether `root * root` equals the original sum. Equality means the sum is a perfect square. Otherwise it is not.

The implementation uses only constant extra memory beyond the input array and processes each element exactly once.

## Worked Examples

### Example 1

Input:

```
1
2
14 2
```

The buckets contain 14 and 2 squares.

| Step | Value |
| --- | --- |
| Sum $S$ | 16 |
| Integer square root $r$ | 4 |
| $r^2$ | 16 |
| Decision | YES |

Since $16 = 4^2$, the total area corresponds exactly to a square.

### Example 2

Input:

```
1
7
1 2 3 4 5 6 7
```

| Step | Value |
| --- | --- |
| Sum $S$ | 28 |
| Integer square root $r$ | 5 |
| $r^2$ | 25 |
| Decision | NO |

The closest square below 28 is 25. Since $25 \neq 28$, the total area is not a perfect square.

This example demonstrates that having many buckets does not matter. Only the final sum matters.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Each value is processed once while computing the sum |
| Space | $O(1)$ | Only a few variables are used beyond the input storage |

The total number of values across all test cases is at most $2 \cdot 10^5$, so a linear scan is easily within the time limit. Memory usage is negligible compared to the available limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from math import isqrt

def solve():
    input = sys.stdin.readline

    t = int(input())
    ans = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        s = sum(a)
        r = isqrt(s)

        ans.append("YES" if r * r == s else "NO")

    sys.stdout.write("\n".join(ans))

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

# provided sample
assert run(
"""5
1
9
2
14 2
7
1 2 3 4 5 6 7
6
1 3 5 7 9 11
4
2 2 2 2
"""
) == "YES\nYES\nNO\nYES\nNO"

# minimum size
assert run(
"""1
1
1
"""
) == "YES"

# single bucket, non-square
assert run(
"""1
1
2
"""
) == "NO"

# all equal values, perfect square total
assert run(
"""1
4
4 4 4 4
"""
) == "YES"

# large boundary-style values
assert run(
"""1
2
1000000000 1000000000
"""
) == "NO"

# perfect square formed from many buckets
assert run(
"""1
9
1 1 1 1 1 1 1 1 1
"""
) == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `n=1, a=[1]` | YES | Smallest valid input |
| `n=1, a=[2]` | NO | Single-bucket non-square total |
| `a=[4,4,4,4]` | YES | All values equal |
| `a=[10^9,10^9]` | NO | Large sums and integer arithmetic |
| Nine ones | YES | Exact square area from many buckets |

## Edge Cases

Consider the smallest possible perfect-square case:

```
1
1
1
```

The sum is $1$. The integer square root is also $1$, and $1^2 = 1$. The algorithm outputs:

```
YES
```

Now consider a single bucket whose count is not a square:

```
1
1
2
```

The sum is $2$. The integer square root is $1$, but $1^2 = 1 \neq 2$. The algorithm correctly outputs:

```
NO
```

Consider a large-value case:

```
1
2
1000000000 1000000000
```

The sum is $2000000000$. The integer square root is $44721$, and

$$44721^2 = 1999967841.$$

Since this differs from the sum, the algorithm outputs:

```
NO
```

This confirms that using an exact integer square root avoids floating-point precision issues.

Finally, consider a perfect-square total spread across many buckets:

```
1
4
2 2 2 3
```

The sum is $9$. The integer square root is $3$, and $3^2 = 9$. The output is:

```
YES
```

The distribution among buckets never matters. Only the total area determines whether a square can be formed.
