---
title: "CF 1720B - Interesting Sum"
description: "We have an array and must choose a subarray that is not the entire array. After choosing it, the array is split into two parts: The chosen subarray itself, and all elements outside that subarray."
date: "2026-06-09T19:26:17+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "data-structures", "greedy", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1720
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 815 (Div. 2)"
rating: 800
weight: 1720
solve_time_s: 131
verified: false
draft: false
---

[CF 1720B - Interesting Sum](https://codeforces.com/problemset/problem/1720/B)

**Rating:** 800  
**Tags:** brute force, data structures, greedy, math, sortings  
**Solve time:** 2m 11s  
**Verified:** no  

## Solution
## Problem Understanding

We have an array and must choose a subarray that is not the entire array. After choosing it, the array is split into two parts:

The chosen subarray itself, and all elements outside that subarray.

The beauty is defined as:

- The difference between the maximum and minimum element outside the chosen subarray.
- Plus the difference between the maximum and minimum element inside the chosen subarray.

We want the largest possible beauty.

The array length can be as large as $10^5$ across all test cases. Any solution that tries all possible subarrays is immediately ruled out. There are $O(n^2)$ subarrays, and even checking one subarray efficiently would not save such an approach. We need something around $O(n \log n)$ or better per test case.

The most dangerous part of the problem is that the chosen segment can be anywhere, while the formula depends only on maximum and minimum values. A naive implementation may focus too much on positions, even though the expression is entirely determined by extreme values.

Consider an array where all values are equal:

```
3 3 3 3
```

Every maximum equals every minimum, both inside and outside the segment. The answer is:

```
0
```

A solution that assumes there must be some positive contribution would fail here.

Another tricky case is:

```
1 2 3 100 200
```

The optimal segment is not formed by the largest values alone. The answer is:

```
297
```

The key is that the segment and its complement together can separate the global extremes into different groups.

A final example:

```
1 5 6 10
```

The answer is:

```
10
```

Choosing segment `[1]` gives:

$$(10-5)+(1-1)=5$$

which is not optimal. The best partition places the two smallest values in one group and the two largest values in the other:

$$(5-1)+(10-6)=8$$

Actually, choosing groups `{1,10}` and `{5,6}` is impossible because groups must come from a segment and its complement, but after understanding the underlying property we will see that the answer depends only on the four extreme values after sorting.

## Approaches

A brute-force solution would enumerate every possible proper subarray. For each subarray, we would compute the maximum and minimum inside it and outside it, then evaluate the beauty.

The brute-force is correct because it directly checks every valid choice. The problem is the number of choices. There are $O(n^2)$ subarrays. Even with sophisticated preprocessing, handling all of them is far too expensive for $n=10^5$.

The breakthrough comes from looking at what the formula actually uses. It never cares about the order of elements. It only cares about maximum and minimum values of two groups.

Suppose we sort the array:

$$b_1 \le b_2 \le \dots \le b_n$$

The beauty is:

$$(\text{max}_1-\text{min}_1)+(\text{max}_2-\text{min}_2)$$

Every element that is not one of the minima or maxima of a group contributes nothing directly. Only four values matter:

- minimum of group 1
- maximum of group 1
- minimum of group 2
- maximum of group 2

To maximize the sum of two ranges, we want the minima to be as small as possible and the maxima to be as large as possible.

The smallest two values of the entire array must become the two minima of the groups, and the largest two values must become the two maxima of the groups.

After sorting, those values are:

$$b_1,\ b_2,\ b_{n-1},\ b_n$$

One group gets $b_1$ as its minimum and $b_n$ as its maximum, while the other group gets $b_2$ as its minimum and $b_{n-1}$ as its maximum.

The resulting beauty is:

$$(b_n-b_1)+(b_{n-1}-b_2)$$

which simplifies to:

$$b_n+b_{n-1}-b_1-b_2$$

Once we realize the answer depends only on the two smallest and two largest values, the problem becomes trivial: sort the array and compute that expression.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ or worse | $O(1)$ | Too slow |
| Optimal | $O(n \log n)$ | $O(1)$ extra (excluding sort) | Accepted |

## Algorithm Walkthrough

1. Read the array.
2. Sort the array in nondecreasing order.
3. Let:

- $b_1$ be the smallest element.
- $b_2$ be the second smallest element.
- $b_{n-1}$ be the second largest element.
- $b_n$ be the largest element.
4. Compute:

$$(b_n+b_{n-1})-(b_1+b_2)$$

This is exactly:

$$(b_n-b_1)+(b_{n-1}-b_2)$$

which is the maximum possible beauty.

1. Output the result.

### Why it works

The beauty only depends on the minimum and maximum of each of the two resulting groups. Interior elements never affect the value directly.

For any partition into two nonempty groups, the two minima come from some pair of array elements and the two maxima come from some pair of array elements. To maximize the sum of the two ranges, we want the minima as small as possible and the maxima as large as possible. The best possible choice is exactly the two smallest elements serving as the minima and the two largest elements serving as the maxima.

After sorting, those values are fixed: $b_1, b_2, b_{n-1}, b_n$. Their contribution is

$$(b_n-b_1)+(b_{n-1}-b_2)$$

and no other selection of minima and maxima can produce a larger sum.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())

for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))

    a.sort()

    ans = a[-1] + a[-2] - a[0] - a[1]
    print(ans)
```

The first step is sorting the array. Once sorted, the two smallest values are at indices `0` and `1`, while the two largest values are at indices `-1` and `-2`.

The formula

```
a[-1] + a[-2] - a[0] - a[1]
```

is exactly

$$b_n+b_{n-1}-b_1-b_2$$

which is the maximum beauty derived above.

No special handling is required for duplicate values. If all elements are equal, the expression naturally evaluates to zero.

Python integers are arbitrary precision, so there is no overflow concern even though values can reach $10^9$.

## Worked Examples

### Example 1

Input:

```
1
8
1 2 2 3 1 5 6 1
```

After sorting:

```
1 1 1 2 2 3 5 6
```

| Variable | Value |
| --- | --- |
| smallest | 1 |
| second smallest | 1 |
| second largest | 5 |
| largest | 6 |
| answer | 6 + 5 - 1 - 1 = 9 |

Output:

```
9
```

This example shows that only the two smallest and two largest values matter. The middle elements never influence the final formula.

### Example 2

Input:

```
1
5
1 2 3 100 200
```

After sorting:

```
1 2 3 100 200
```

| Variable | Value |
| --- | --- |
| smallest | 1 |
| second smallest | 2 |
| second largest | 100 |
| largest | 200 |
| answer | 200 + 100 - 1 - 2 = 297 |

Output:

```
297
```

This example demonstrates why focusing on extreme values is sufficient. The middle value `3` does not affect the optimum.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Sorting dominates the work |
| Space | $O(1)$ extra | Aside from the array and sorting internals |

The sum of all array lengths across test cases is at most $10^5$. Sorting that many values overall requires roughly $10^5 \log(10^5)$ operations, which easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    t = int(input())
    ans = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        a.sort()
        ans.append(str(a[-1] + a[-2] - a[0] - a[1]))

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
"""4
8
1 2 2 3 1 5 6 1
5
1 2 3 100 200
4
3 3 3 3
6
7 8 3 1 1 8
"""
) == "9\n297\n0\n14"

# minimum size
assert run(
"""1
4
1 2 3 4
"""
) == "4"

# all equal
assert run(
"""1
4
5 5 5 5
"""
) == "0"

# duplicates among extremes
assert run(
"""1
6
1 1 1 10 10 10
"""
) == "18"

# large spread
assert run(
"""1
5
1 1000000000 2 999999999 3
"""
) == "1999999996"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 2 3 4` | `4` | Minimum valid array size |
| `5 5 5 5` | `0` | All values equal |
| `1 1 1 10 10 10` | `18` | Duplicate smallest and largest values |
| `1 1000000000 2 999999999 3` | `1999999996` | Very large values and arithmetic correctness |

## Edge Cases

Consider:

```
1
4
3 3 3 3
```

After sorting:

```
3 3 3 3
```

The algorithm computes:

$$3+3-3-3=0$$

Every possible segment has zero range inside and zero range outside, so the answer is correctly zero.

Consider:

```
1
5
1 2 3 100 200
```

Sorted array:

```
1 2 3 100 200
```

The algorithm uses:

$$200+100-1-2=297$$

The two smallest values become the minima of the two groups and the two largest values become the maxima. No other choice can produce a larger sum of ranges.

Consider:

```
1
6
1 1 5 6 10 10
```

Sorted array:

```
1 1 5 6 10 10
```

The algorithm computes:

$$10+10-1-1=18$$

Duplicate extremes are handled naturally. The formula does not rely on values being distinct, only on their positions in sorted order.

Consider:

```
1
4
1 5 6 10
```

Sorted array:

```
1 5 6 10
```

The algorithm computes:

$$10+6-1-5=10$$

Even though there are very few elements, the same reasoning applies. The answer is determined entirely by the two smallest and two largest values.
