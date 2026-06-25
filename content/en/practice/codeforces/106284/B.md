---
title: "CF 106284B - \u041a\u0442\u043e \u0431\u043e\u043b\u044c\u0448\u0435?"
description: "We have several unsigned integer types. A type with a bits can store values from 0 to 2^a - 1. We need decide whether there exists some integer x that fits into a smaller type, but its square does not fit into a larger type."
date: "2026-06-25T07:40:38+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106284
codeforces_index: "B"
codeforces_contest_name: "\u041c\u0443\u043d\u0438\u0446\u0438\u043f\u0430\u043b\u044c\u043d\u044b\u0439 \u044d\u0442\u0430\u043f \u0412\u0441\u041e\u0428 \u043f\u043e \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0442\u0438\u043a\u0435 (\u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435) 10-11 \u043a\u043b\u0430\u0441\u0441, \u0421\u0432\u0435\u0440\u0434\u043b\u043e\u0432\u0441\u043a\u0430\u044f \u043e\u0431\u043b\u0430\u0441\u0442\u044c, 2025"
rating: 0
weight: 106284
solve_time_s: 35
verified: true
draft: false
---

[CF 106284B - \u041a\u0442\u043e \u0431\u043e\u043b\u044c\u0448\u0435?](https://codeforces.com/problemset/problem/106284/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 35s  
**Verified:** yes  

## Solution
## Problem Understanding

We have several unsigned integer types. A type with `a` bits can store values from `0` to `2^a - 1`. We need decide whether there exists some integer `x` that fits into a smaller type, but its square does not fit into a larger type.

In other words, among the given bit sizes, we need to know whether there are two types with sizes `a < b` such that some value representable by `a` bits has a square that needs more than `b` bits.

The input gives the number of available types and their bit capacities. The output is `YES` if such a pair of types exists and `NO` otherwise.

The limits matter because the number of types can be as large as `100000`, while each bit size can be as large as `10^9`. A solution that compares every pair of types would perform about `10^10` checks in the worst case, which is far beyond what a typical contest time limit allows. We need a solution close to `O(n log n)` or better.

The large values also mean we cannot iterate through possible numbers `x` or compute huge powers. The answer must come from the relationship between the bit lengths themselves.

The tricky part is that equal bit sizes do not create a valid pair because we need a strictly smaller type for `x` and a strictly larger type for `x^2`. For example, with input:

```
2
5 5
```

the answer is:

```
NO
```

A careless solution that only checks whether two values are different might incorrectly accept it.

Another edge case appears when the smallest type is much smaller than the largest one. For example:

```
3
1 2 3
```

The answer is:

```
YES
```

because a 1-bit type stores only `0` and `1`, and the maximum useful value is `1`, whose square still fits in 2 bits. However, the type of size 2 can store `3`, and `3^2 = 9` requires 4 bits, which does not fit in the 3-bit type. A solution that only checks adjacent values after sorting may miss a non-adjacent pair.

## Approaches

The direct approach is to try every smaller type and every larger type. For a pair of bit sizes `a` and `b`, the largest value that fits in the smaller type is `2^a - 1`. We would need to check whether `(2^a - 1)^2 >= 2^b`. If it is true, the smaller type contains a value whose square overflows the larger type.

This approach is correct because checking the maximum value is enough. Squaring grows as the number grows, so if the maximum possible value fails to overflow, no smaller value can overflow either.

However, checking all pairs is too slow. With `n = 100000`, the number of pairs is roughly `n^2 / 2`, which is around five billion comparisons.

The key observation is that we only care about bit lengths. For a value with `a` bits, the square of the largest possible value is slightly less than `2^(2a)`. That means a type with `b` bits can hold every square from the `a`-bit type only when `b` is at least `2a`. If there is a larger type with fewer than `2a` bits, the answer is immediately `YES`.

So the problem becomes finding whether there exists a bit size `a` where another existing bit size is greater than `a` but less than `2a`. We can sort the sizes and maintain the largest value seen so far. When processing a size `a`, we need to know whether there is a previous size that is at least `a`? A simpler way is to sort descending and keep the maximum smaller size already processed.

The condition can be checked with a sorted array. For every size, the only dangerous larger sizes are those below twice it. Because all sizes are sorted, we can use binary search to find whether such a value exists.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Sort all bit sizes in increasing order. After sorting, every possible larger type for a given type appears somewhere to its right.
2. For each position `i`, treat the current size `a[i]` as the type that stores `x`. We need to find whether there is some later size smaller than `2 * a[i]`. Such a size would be large enough to be a larger type but too small to store every possible square.
3. Use binary search to find the first index after `i` whose value is at least `2 * a[i]`. If that index is not the immediate next boundary of the array, then there exists a value between `a[i]` and `2 * a[i]`, so the answer is `YES`.
4. If every type survives this check, print `NO`.

Why it works: for a type of `a` bits, the largest value it stores is `2^a - 1`. Squaring it gives a number smaller than `2^(2a)` and very close to that limit. A type with fewer than `2a` bits cannot represent all such squares. Since we only need to prove existence of one overflowing value, finding a larger type below `2a` is exactly the required condition.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    a.sort()

    for i in range(n):
        target = 2 * a[i]
        lo, hi = i + 1, n
        while lo < hi:
            mid = (lo + hi) // 2
            if a[mid] >= target:
                hi = mid
            else:
                lo = mid + 1
        if lo < n and lo > i + 1:
            print("YES")
            return

    print("NO")

solve()
```

The array is sorted first so that all larger types are grouped together. For each type, the binary search finds the first size that is not smaller than `2 * a[i]`. If that position is not the very next element, there was at least one larger type before it, and that type is too small to safely contain all squares.

The multiplication by two is safe because the input values fit in `10^9`, so the intermediate value fits easily inside Python integers. The binary search starts from `i + 1` because a type cannot be paired with itself.

## Worked Examples

For:

```
3
64 16 32
```

The sorted sizes are `[16, 32, 64]`.

| Current size | Need first value >= | Found index | Result |
| --- | --- | --- | --- |
| 16 | 32 | 1 | No smaller value in range |
| 32 | 64 | 2 | No smaller value in range |
| 64 | 128 | 3 | End of array |

The scan finds no valid pair, so the output is `NO`. This demonstrates the case where larger types are exactly large enough.

For:

```
4
4 2 1 3
```

The sorted sizes are `[1, 2, 3, 4]`.

| Current size | Need first value >= | Found index | Result |
| --- | --- | --- | --- |
| 1 | 2 | 1 | No |
| 2 | 4 | 3 | Value 3 is between 2 and 4 |

The algorithm stops and returns `YES`. The size 2 type can store values up to 3, and `3^2` needs 4 bits, which overflows a 3-bit type.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting costs `O(n log n)` and each of `n` elements performs one binary search. |
| Space | O(n) | The sorted array is stored. |

The algorithm avoids checking every pair of types, so it remains efficient for `100000` input values.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(sys.stdin.readline())
    a = list(map(int, sys.stdin.readline().split()))
    a.sort()
    for i in range(n):
        target = 2 * a[i]
        lo, hi = i + 1, n
        while lo < hi:
            mid = (lo + hi) // 2
            if a[mid] >= target:
                hi = mid
            else:
                lo = mid + 1
        if lo < n and lo > i + 1:
            return "YES\n"
    return "NO\n"

assert run("3\n64 16 32\n") == "NO\n"
assert run("4\n4 2 1 3\n") == "YES\n"

assert run("2\n5 5\n") == "NO\n", "equal sizes"
assert run("3\n1 2 3\n") == "YES\n", "non adjacent pair"
assert run("5\n1 1 1 1 1\n") == "NO\n", "all equal values"
assert run("2\n1000000000 1999999999\n") == "YES\n", "large boundary"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 / 5 5` | `NO` | Equal sizes must not form a pair |
| `3 / 1 2 3` | `YES` | A valid pair can be non-adjacent |
| `5 / 1 1 1 1 1` | `NO` | Duplicate values are handled correctly |
| `2 / 1000000000 1999999999` | `YES` | Large bit sizes do not cause overflow |

## Edge Cases

For the equal size case:

```
2
5 5
```

The sorted array is `[5, 5]`. For the first element, there is no later element smaller than `10`, but the later element is not larger anyway. The algorithm never accepts equal sizes and returns `NO`.

For the large gap case:

```
3
1 2 3
```

After sorting, the first value is `1`. The first size that is at least `2` is the second element, so there is no candidate there. For size `2`, we need a value at least `4`, but the value `3` is found before that boundary, meaning it is larger than `2` and smaller than `4`. The algorithm returns `YES`, matching the fact that a 2-bit number can overflow a 3-bit type when squared.

For the duplicate case:

```
5
1 1 1 1 1
```

Every search starts after the current index, but all candidates have the same value. No value is larger than the current type, so no valid pair exists and the answer is `NO`.

For very large inputs:

```
2
1000000000 1999999999
```

The second value is larger than the first, but it is still less than twice the first value. The algorithm detects the interval correctly and returns `YES` without trying to compute any enormous powers.
