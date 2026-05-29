---
title: "CF 302A - Eugeny and Array"
description: "We are given an array containing only 1 and -1. For every query [l, r], we look at the subarray from index l to r."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 302
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 182 (Div. 2)"
rating: 800
weight: 302
solve_time_s: 92
verified: true
draft: false
---

[CF 302A - Eugeny and Array](https://codeforces.com/problemset/problem/302/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 1m 32s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array containing only `1` and `-1`. For every query `[l, r]`, we look at the subarray from index `l` to `r`. We are allowed to rearrange the elements inside that subarray in any order, and we must decide whether it is possible for the total sum of the subarray to become zero.

The order of the numbers does not actually matter for the sum. Rearranging only changes positions, not how many `1`s and `-1`s exist. The real question is whether the chosen segment contains the same number of `1`s and `-1`s.

If a subarray has length `k`, then having sum `0` means exactly half the elements are `1` and the other half are `-1`. That immediately tells us two things. First, the segment length must be even. Second, the number of `1`s must equal the number of `-1`s.

The constraints are large enough that we cannot inspect every query element-by-element. Both `n` and `m` can reach `2 * 10^5`. A naive scan of each query would take `O(length of segment)` time, which becomes roughly `4 * 10^10` operations in the worst case. That is far beyond what fits into a 1 second time limit.

A few edge cases are easy to mishandle.

Consider a segment of odd length:

```
3 1
1 -1 1
1 3
```

The correct answer is:

```
0
```

Even though the counts are close, an odd-length segment can never split evenly into equal numbers of `1` and `-1`.

Another subtle case is a segment with even length but unbalanced counts:

```
4 1
1 1 -1 -1
1 2
```

The segment `[1, 2]` contains two `1`s and no `-1`s. Rearranging changes nothing, so the answer is still `0`.

A careless implementation may also overcomplicate the problem by trying to simulate rearrangements. For example:

```
4 1
1 -1 1 -1
1 4
```

The sum is already `0`, so the answer is `1`. No actual rearrangement logic is needed.

## Approaches

The brute-force approach processes every query independently. For each segment `[l, r]`, we count how many `1`s and `-1`s appear. If the counts match, we print `1`; otherwise we print `0`.

This works because the condition for achieving sum `0` is exactly equality between positive and negative counts. The problem is speed. In the worst case, each query may scan almost the entire array. With `2 * 10^5` queries and `2 * 10^5` elements, the total work becomes quadratic.

The key observation is that the actual values are only `1` and `-1`. A segment can have sum `0` if and only if its length is even and the number of `1`s equals the number of `-1`s. Instead of counting both separately every time, we can count only one category globally.

Suppose we precompute the total number of `1`s in the whole array. Let:

```
ones = number of elements equal to 1
minus = number of elements equal to -1
```

For a query segment of length `len`:

```
len = r - l + 1
```

To make the sum zero, we need:

```
len / 2 <= ones
len / 2 <= minus
```

Why? Because the segment must contain exactly `len / 2` copies of each value. Since rearrangement is unrestricted, only availability matters.

This reduces every query to constant time checks.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nm) | O(1) | Too slow |
| Optimal | O(n + m) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the array and count how many elements are equal to `1`.
2. Compute how many elements are equal to `-1`.
3. For each query, compute the segment length:

```
len = r - l + 1
```
4. If the length is odd, print `0`.

A zero sum requires equal numbers of `1` and `-1`, which is impossible with an odd number of elements.
5. Otherwise, compute:

```
need = len // 2
```

This is how many `1`s and `-1`s the segment must contain.
6. If both global counts satisfy:

```
ones >= need
minus >= need
```

print `1`. Otherwise print `0`.

The reason this works is that rearrangement removes all positional constraints. We only care whether enough copies of each value exist to fill a segment of the required size.

### Why it works

A segment of length `len` has sum `0` exactly when it contains the same number of `1`s and `-1`s. Since every element is either `1` or `-1`, equal counts imply:

```
count(1) = count(-1) = len / 2
```

If `len` is odd, this is impossible immediately.

If `len` is even, then the only remaining question is whether the array contains at least `len / 2` copies of each value. Because rearrangement is allowed freely, positions do not matter at all. The algorithm checks exactly these necessary and sufficient conditions, so every answer is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    arr = list(map(int, input().split()))

    ones = arr.count(1)
    minus = n - ones

    ans = []

    for _ in range(m):
        l, r = map(int, input().split())

        length = r - l + 1

        if length % 2 == 1:
            ans.append("0")
            continue

        need = length // 2

        if ones >= need and minus >= need:
            ans.append("1")
        else:
            ans.append("0")

    print("\n".join(ans))

solve()
```

The first part counts how many `1`s exist globally. Since every other value must be `-1`, the count of negatives is simply `n - ones`.

Each query only depends on the segment length. The actual positions `l` and `r` are irrelevant beyond determining that length. That is the central simplification of the problem.

The odd-length check comes first because it immediately rejects impossible cases. After that, `need = length // 2` represents the required number of each value.

A common mistake is trying to analyze the exact subarray contents. The statement allows rearranging any elements within the chosen range, so only the counts matter.

Another easy off-by-one mistake is computing the length incorrectly. Since both endpoints are inclusive, the correct formula is:

```
r - l + 1
```

## Worked Examples

### Example 1

Input:

```
2 3
1 -1
1 1
1 2
2 2
```

Global counts:

```
ones = 1
minus = 1
```

| Query | Length | Odd? | Need | Enough 1s? | Enough -1s? | Answer |
| --- | --- | --- | --- | --- | --- | --- |
| [1, 1] | 1 | Yes | - | - | - | 0 |
| [1, 2] | 2 | No | 1 | Yes | Yes | 1 |
| [2, 2] | 1 | Yes | - | - | - | 0 |

The first and third queries fail immediately because odd-length segments cannot split evenly into equal counts. The middle query succeeds because the array has one `1` and one `-1`.

### Example 2

Input:

```
6 4
1 1 1 -1 -1 -1
1 2
1 4
2 5
1 6
```

Global counts:

```
ones = 3
minus = 3
```

| Query | Length | Odd? | Need | Enough 1s? | Enough -1s? | Answer |
| --- | --- | --- | --- | --- | --- | --- |
| [1, 2] | 2 | No | 1 | Yes | Yes | 1 |
| [1, 4] | 4 | No | 2 | Yes | Yes | 1 |
| [2, 5] | 4 | No | 2 | Yes | Yes | 1 |
| [1, 6] | 6 | No | 3 | Yes | Yes | 1 |

This trace demonstrates that the exact interval contents do not matter. Every even-length query succeeds because the array globally contains enough copies of both values.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Counting values takes O(n), each query is O(1) |
| Space | O(1) | Only a few counters and variables are stored |

The solution easily fits the limits. With at most `2 * 10^5` queries, constant work per query is necessary. The algorithm performs only simple arithmetic and comparisons after the initial counting step.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n, m = map(int, input().split())
    arr = list(map(int, input().split()))

    ones = arr.count(1)
    minus = n - ones

    ans = []

    for _ in range(m):
        l, r = map(int, input().split())

        length = r - l + 1

        if length % 2 == 1:
            ans.append("0")
            continue

        need = length // 2

        if ones >= need and minus >= need:
            ans.append("1")
        else:
            ans.append("0")

    print("\n".join(ans))

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    return sys.stdout.getvalue()

# provided sample
assert run(
"""2 3
1 -1
1 1
1 2
2 2
"""
) == "0\n1\n0\n", "sample 1"

# minimum size
assert run(
"""1 1
1
1 1
"""
) == "0\n", "single odd segment"

# all equal values
assert run(
"""4 2
1 1 1 1
1 2
1 4
"""
) == "0\n0\n", "no -1 values available"

# balanced array
assert run(
"""6 3
1 1 1 -1 -1 -1
1 2
1 4
1 6
"""
) == "1\n1\n1\n", "all even lengths possible"

# off-by-one boundary checks
assert run(
"""5 3
1 -1 1 -1 1
1 4
2 5
1 5
"""
) == "1\n1\n0\n", "inclusive range lengths"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single element array | `0` | Odd-length segments are impossible |
| All elements equal | All `0` | Need both `1` and `-1` available |
| Fully balanced array | All `1` | Even lengths succeed when counts are sufficient |
| Boundary length checks | Mixed answers | Confirms correct `r - l + 1` handling |

## Edge Cases

Consider the odd-length case:

```
3 1
1 -1 1
1 3
```

The algorithm computes:

```
length = 3
```

Since the length is odd, it immediately prints `0`. A sum of zero would require `1.5` copies of each value, which is impossible.

Now consider an even segment with insufficient negatives:

```
4 1
1 1 1 -1
1 4
```

The algorithm computes:

```
length = 4
need = 2
ones = 3
minus = 1
```

There are enough `1`s but not enough `-1`s. The condition fails, so the output is:

```
0
```

This is correct because a zero-sum segment of length `4` must contain exactly two of each value.

Finally, consider a balanced case:

```
6 1
1 1 -1 -1 1 -1
2 5
```

The segment length is `4`, so:

```
need = 2
```

The global counts are:

```
ones = 3
minus = 3
```

Both conditions succeed, so the algorithm prints `1`.

Even though the queried interval itself may not already sum to zero, rearrangement allows us to place two `1`s and two `-1`s inside the segment, which achieves the required sum.
