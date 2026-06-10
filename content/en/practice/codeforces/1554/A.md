---
title: "CF 1554A - Cherry"
description: "We are given an array of positive integers. For every subarray that contains at least two elements, we compute the product of its largest element and its smallest element. The task is to find the maximum such product among all possible subarrays."
date: "2026-06-10T12:52:55+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1554
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 735 (Div. 2)"
rating: 800
weight: 1554
solve_time_s: 102
verified: true
draft: false
---

[CF 1554A - Cherry](https://codeforces.com/problemset/problem/1554/A)

**Rating:** 800  
**Tags:** greedy  
**Solve time:** 1m 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of positive integers. For every subarray that contains at least two elements, we compute the product of its largest element and its smallest element. The task is to find the maximum such product among all possible subarrays.

A direct reading of the definition suggests considering every pair of endpoints and computing the minimum and maximum inside that range. The challenge is that a test case can contain up to $10^5$ elements, and the total number of elements across all test cases reaches $3 \cdot 10^5$. Any algorithm that examines all $O(n^2)$ subarrays is immediately too slow, since that would require around $10^{10}$ operations in the worst case.

The values themselves are as large as $10^6$. Since the answer is a product of two array values, it can reach $10^{12}$, so 64-bit integer arithmetic is required. Python handles this automatically.

A subtle point is that the best subarray is not necessarily long. Consider:

```
3
2 4 3
```

The subarray $[4,3]$ gives $4 \cdot 3 = 12$, while the larger subarray $[2,4,3]$ gives only $4 \cdot 2 = 8$. Expanding a range can decrease the minimum and make the product worse.

Another easy mistake is assuming that the answer must involve the global maximum element. For example:

```
4
100 1 50 50
```

The subarray $[50,50]$ gives $2500$, while every subarray containing 100 also contains 1, producing at most $100$. Focusing only on the largest value misses the correct answer.

A third pitfall is integer overflow in languages such as C++ if 32-bit integers are used:

```
2
1000000 1000000
```

The correct answer is $10^{12}$, which does not fit in a 32-bit signed integer.

## Approaches

The brute-force idea is straightforward. For every pair of endpoints $(l,r)$, compute the minimum and maximum within that subarray and update the answer. This is correct because it explicitly evaluates every candidate range.

The problem is the running time. There are $O(n^2)$ subarrays, and recomputing the minimum and maximum for each one takes $O(n)$. That leads to $O(n^3)$ time. Even if we maintain minimum and maximum incrementally and reduce the complexity to $O(n^2)$, it is still far too slow for $n=10^5$.

The key observation comes from understanding what happens when a subarray contains more than two elements.

Suppose a subarray has minimum value $m$ and maximum value $M$. Both of these values appear somewhere inside the subarray. Consider the segment between the positions of $m$ and $M$. That segment is also a subarray, and its minimum is still $m$ while its maximum is still $M$. The product remains $m \cdot M$.

Now look at the two positions where $m$ and $M$ occur. Moving from one position to the other, there must be at least one pair of adjacent elements. Among those adjacent pairs, one pair has product at least $m \cdot M$. Why? Every value on that path lies between $m$ and $M$, so any adjacent pair consists of values within that interval. The maximum achievable answer always ends up being realized by some adjacent pair.

An even simpler way to see it is that for a subarray whose minimum is $m$ and maximum is $M$, the answer contributed by that subarray is exactly $mM$. The pair $(m,M)$ must appear somewhere in the array with only values between them separating them. Examining adjacent pairs is sufficient, and this is the intended observation for this problem.

So instead of checking all subarrays, we only need to check every adjacent pair and compute:

$$a_i \cdot a_{i+1}$$

The maximum of these products is the answer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ to $O(n^3)$ | $O(1)$ | Too slow |
| Optimal | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases.
2. For each test case, read the array.
3. Initialize the answer as 0.
4. Iterate through all adjacent pairs $(a_i, a_{i+1})$.
5. Compute their product and update the answer if this product is larger.
6. After processing all adjacent pairs, print the answer.

The reason this works is that every candidate answer obtainable from a longer subarray can also be achieved by considering the minimum and maximum values inside that range, and the maximum possible product ultimately appears among adjacent elements. Since every adjacent pair is checked, the optimal value cannot be missed.

### Why it works

Let an optimal subarray have minimum value $m$ and maximum value $M$. The value contributed by that subarray is $mM$.

Focus on the positions where $m$ and $M$ occur. Every element between those positions lies between $m$ and $M$ inclusive. Along this path there is an adjacent pair whose product is at least $mM$. Since the optimal subarray already produces $mM$, the global optimum must equal the maximum product of some adjacent pair.

The algorithm checks every adjacent pair exactly once, so it necessarily finds that maximum product.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())

for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))

    ans = 0

    for i in range(n - 1):
        ans = max(ans, a[i] * a[i + 1])

    print(ans)
```

The solution follows the observation directly.

The loop runs from index 0 to index $n-2$, which guarantees that every adjacent pair is processed exactly once. For each pair, their product is computed and compared against the current best answer.

The answer variable starts at 0 because all array values are positive, so every valid product is positive as well.

Python integers automatically support values larger than $2^{31}-1$, so products up to $10^{12}$ are handled safely without any special care.

## Worked Examples

### Example 1

Input:

```
3
2 4 3
```

| i | Pair | Product | Current Answer |
| --- | --- | --- | --- |
| 0 | (2, 4) | 8 | 8 |
| 1 | (4, 3) | 12 | 12 |

Final answer:

```
12
```

The best adjacent pair is $(4,3)$. This matches the optimal subarray $[4,3]$.

### Example 2

Input:

```
4
3 2 3 1
```

| i | Pair | Product | Current Answer |
| --- | --- | --- | --- |
| 0 | (3, 2) | 6 | 6 |
| 1 | (2, 3) | 6 | 6 |
| 2 | (3, 1) | 3 | 6 |

Final answer:

```
6
```

This example shows that several different subarrays may achieve the same optimum. The algorithm only needs the maximum value, not the range that produces it.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | One pass over adjacent pairs |
| Space | $O(1)$ | Only a few variables are used |

The total number of processed elements across all test cases is at most $3 \cdot 10^5$. A linear scan per test case is easily fast enough within the 1-second limit, and the memory usage remains constant.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        ans = 0
        for i in range(n - 1):
            ans = max(ans, a[i] * a[i + 1])

        out.append(str(ans))

    print("\n".join(out))

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    result = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return result

# provided sample
assert run(
"""4
3
2 4 3
4
3 2 3 1
2
69 69
6
719313 273225 402638 473783 804745 323328
"""
) == """12
6
4761
381274500335
"""

# minimum size
assert run(
"""1
2
5 7
"""
) == """35
"""

# all equal values
assert run(
"""1
5
4 4 4 4 4
"""
) == """16
"""

# off-by-one check, best pair at the end
assert run(
"""1
5
1 2 3 4 100
"""
) == """400
"""

# large values
assert run(
"""1
2
1000000 1000000
"""
) == """1000000000000
"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 / 5 7` | `35` | Smallest possible array |
| `4 4 4 4 4` | `16` | All values equal |
| `1 2 3 4 100` | `400` | Best adjacent pair at the last position |
| `1000000 1000000` | `1000000000000` | Large products and integer safety |

## Edge Cases

Consider the smallest valid input:

```
1
2
5 7
```

There is only one adjacent pair. The algorithm computes $5 \cdot 7 = 35$ and returns 35. Since every valid subarray must contain both elements, this is necessarily correct.

Consider an array where a longer subarray looks tempting:

```
1
3
2 4 3
```

The algorithm checks products 8 and 12, returning 12. The larger subarray $[2,4,3]$ has minimum 2 and maximum 4, giving only 8. The scan correctly identifies that extending the range can reduce the product.

Consider very large values:

```
1
2
1000000 1000000
```

The adjacent product is:

$$1000000 \times 1000000 = 1000000000000$$

The algorithm stores and prints this value directly. Python's arbitrary-precision integers avoid overflow issues.

Consider a case where the global maximum element is not part of the answer:

```
1
4
100 1 50 50
```

The adjacent products are:

| Pair | Product |
| --- | --- |
| (100, 1) | 100 |
| (1, 50) | 50 |
| (50, 50) | 2500 |

The algorithm returns 2500. Any approach that tries to force the global maximum value 100 into the answer would fail on this example.
