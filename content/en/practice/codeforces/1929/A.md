---
title: "CF 1929A - Sasha and the Beautiful Array"
description: "We are given an array of integers, and we may rearrange its elements in any order. The beauty of a particular arrangement is defined as the sum of differences between consecutive elements: $$(a2-a1)+(a3-a2)+cdots+(an-a{n-1})$$ Our task is to choose the ordering that produces the…"
date: "2026-06-08T18:38:35+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1929
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 926 (Div. 2)"
rating: 800
weight: 1929
solve_time_s: 100
verified: true
draft: false
---

[CF 1929A - Sasha and the Beautiful Array](https://codeforces.com/problemset/problem/1929/A)

**Rating:** 800  
**Tags:** constructive algorithms, greedy, math, sortings  
**Solve time:** 1m 40s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers, and we may rearrange its elements in any order.

The beauty of a particular arrangement is defined as the sum of differences between consecutive elements:

$$(a_2-a_1)+(a_3-a_2)+\cdots+(a_n-a_{n-1})$$

Our task is to choose the ordering that produces the largest possible beauty.

The input contains multiple test cases. For each test case, we receive the array elements and must output the maximum beauty achievable after rearranging them.

The constraints are very small. The array length is at most 100, and there are at most 500 test cases. Even an $O(n^2)$ solution would be easily fast enough. The challenge is not performance, but recognizing the mathematical simplification hidden inside the beauty formula.

A common mistake is to think that the arrangement itself matters in a complicated way. For example, one might try placing small and large numbers alternately:

```
1 100 2 99
```

and compute

$$(100-1)+(2-100)+(99-2)=98$$

This looks large, but it is not optimal. A simpler arrangement,

```
1 2 99 100
```

gives

$$(2-1)+(99-2)+(100-99)=99$$

Another edge case occurs when all values are equal:

```
5 5 5
```

Every difference is zero, so the answer must be:

```
0
```

A careless implementation that assumes the answer is always positive would fail here.

A third important case is the minimum array size:

```
2
1 10
```

The beauty is simply $10-1=9$, because there is only one consecutive difference.

## Approaches

A brute-force solution would generate every permutation of the array, compute its beauty, and keep the maximum.

This works because it directly checks every possible arrangement. For an array of length $n$, there are $n!$ permutations. Even for $n=10$, that is already 3,628,800 permutations. Since $n$ can be 100, brute force is completely impossible.

The key observation comes from expanding the beauty formula:

$$(a_2-a_1)+(a_3-a_2)+\cdots+(a_n-a_{n-1})$$

All intermediate terms cancel:

$$-a_2+a_2,\quad -a_3+a_3,\quad \ldots$$

Only the first and last elements remain:

$$a_n-a_1$$

This means the beauty of any arrangement depends only on its first and last elements.

Once the problem is reduced to maximizing

$$a_n-a_1,$$

the answer becomes obvious. We should place the smallest value first and the largest value last. Then the beauty becomes

$$\max(a)-\min(a).$$

No other arrangement can do better because no element is smaller than the minimum and no element is larger than the maximum.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n! \cdot n)$ | $O(n)$ | Too slow |
| Optimal | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Read the array.
2. Find the minimum element of the array.
3. Find the maximum element of the array.
4. Output the difference between the maximum and minimum values.

The reason this works is that the beauty formula always telescopes into:

$$a_n-a_1.$$

To maximize that quantity, we place the smallest value at the beginning and the largest value at the end.

### Why it works

The beauty expression is a telescoping sum. Every interior element appears exactly twice: once with a positive sign and once with a negative sign. These contributions cancel each other.

As a result, the beauty of any arrangement equals the last element minus the first element. The largest possible value is obtained by choosing the global maximum as the last element and the global minimum as the first element. Their difference is exactly $\max(a)-\min(a)$, which is the largest achievable beauty.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())

for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    print(max(a) - min(a))
```

The implementation follows the mathematical observation directly.

For each test case, the array is read once. Python's built-in `max()` and `min()` functions scan the array and return the largest and smallest values. Their difference is the answer.

There are no tricky boundary conditions. Arrays of length two work naturally because the answer is simply the difference between the larger and smaller element. Arrays with identical values also work because the maximum and minimum are equal, producing zero.

The values can be as large as $10^9$, but Python integers easily handle them without overflow concerns.

## Worked Examples

### Example 1

Input array:

```
2 1 3
```

| Step | Value |
| --- | --- |
| Minimum | 1 |
| Maximum | 3 |
| Answer | 3 - 1 = 2 |

Output:

```
2
```

This demonstrates the core idea. Although several rearrangements are possible, the maximum beauty is simply the difference between the largest and smallest values.

### Example 2

Input array:

```
100 54 80 43 90
```

| Step | Value |
| --- | --- |
| Minimum | 43 |
| Maximum | 100 |
| Answer | 100 - 43 = 57 |

Output:

```
57
```

One optimal arrangement is:

```
43 54 80 90 100
```

whose beauty is

$$(54-43)+(80-54)+(90-80)+(100-90)=57.$$

The trace confirms that only the smallest and largest values matter.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | One scan for the minimum and maximum values |
| Space | $O(1)$ | Only a few variables besides the input array |

With $n \le 100$ and at most 500 test cases, this solution runs comfortably within the limits. The total work is only a few tens of thousands of operations.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    t = int(input())
    ans = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        ans.append(str(max(a) - min(a)))

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
3
2 1 3
3
69 69 69
5
100 54 80 43 90
4
3 4 3 3
2
2 1
"""
) == """2
0
57
1
1"""

# minimum size
assert run(
"""1
2
1 10
"""
) == "9"

# all equal
assert run(
"""1
5
7 7 7 7 7
"""
) == "0"

# already sorted
assert run(
"""1
6
1 2 3 4 5 6
"""
) == "5"

# large values
assert run(
"""1
3
1000000000 1 999999999
"""
) == "999999999"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 / 1 10` | `9` | Minimum valid array size |
| `7 7 7 7 7` | `0` | All values equal |
| `1 2 3 4 5 6` | `5` | Already sorted input |
| `1000000000 1 999999999` | `999999999` | Large integer values |

## Edge Cases

### All elements are equal

Input:

```
1
3
5 5 5
```

The algorithm computes:

| Quantity | Value |
| --- | --- |
| Minimum | 5 |
| Maximum | 5 |
| Answer | 0 |

Output:

```
0
```

Every possible rearrangement produces the same array values, so every consecutive difference cancels out.

### Array of length two

Input:

```
1
2
1 10
```

The algorithm computes:

| Quantity | Value |
| --- | --- |
| Minimum | 1 |
| Maximum | 10 |
| Answer | 9 |

Output:

```
9
```

With only two elements, the beauty consists of exactly one difference, which is maximized by placing the smaller value first.

### Unsorted array with repeated values

Input:

```
1
4
3 4 3 3
```

The algorithm computes:

| Quantity | Value |
| --- | --- |
| Minimum | 3 |
| Maximum | 4 |
| Answer | 1 |

Output:

```
1
```

Repeated values do not change the argument. The telescoping sum still reduces to last minus first, so only the global minimum and maximum matter.
