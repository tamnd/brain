---
title: "CF 134A - Average Numbers"
description: "We are given an array of positive integers. For every position, we remove that element and compute the arithmetic mean of the remaining numbers. We must find all positions where the removed value itself is exactly equal to that mean. Suppose the array is [1, 2, 3, 4, 5]."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation"]
categories: ["algorithms"]
codeforces_contest: 134
codeforces_index: "A"
codeforces_contest_name: "Codeforces Testing Round 3"
rating: 1200
weight: 134
solve_time_s: 99
verified: true
draft: false
---

[CF 134A - Average Numbers](https://codeforces.com/problemset/problem/134/A)

**Rating:** 1200  
**Tags:** brute force, implementation  
**Solve time:** 1m 39s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of positive integers. For every position, we remove that element and compute the arithmetic mean of the remaining numbers. We must find all positions where the removed value itself is exactly equal to that mean.

Suppose the array is `[1, 2, 3, 4, 5]`. If we remove `3`, the remaining numbers are `1, 2, 4, 5`. Their sum is `12`, and their average is `12 / 4 = 3`, so index `3` is valid.

The array size can reach `2 · 10^5`, which immediately rules out any solution that recomputes sums from scratch for every position. A quadratic algorithm would perform around `4 · 10^10` operations in the worst case, which is far beyond what fits into a 1 second time limit. We need something close to linear time.

The values themselves are small, at most `1000`, but that does not help enough to justify any expensive nested loops. The bottleneck is the number of elements, not the magnitude of the numbers.

One easy mistake is using floating point arithmetic for averages. The condition is exact equality, and floating point comparisons can introduce precision issues. Everything can be handled with integers.

Consider this input:

```
3
1 2 3
```

If we remove `2`, the remaining average is `(1 + 3) / 2 = 2`, so index `2` is valid.

A careless implementation might compute averages as floating point numbers and compare them directly, which is unnecessary and risky.

Another subtle case is when the remaining sum is not divisible by `n - 1`.

```
4
1 1 1 2
```

For the last element, the remaining average is `(1 + 1 + 1) / 3 = 1`, so `2` is not valid.

For the first element, the remaining average is `(1 + 1 + 2) / 3 = 4/3`, which is not an integer. Since array elements are integers, this index cannot work. Forgetting the divisibility check can produce wrong answers.

Arrays where all values are equal are also worth checking:

```
5
7 7 7 7 7
```

Every index is valid because removing any `7` leaves an average of `7`.

## Approaches

The most direct solution is brute force. For every index `i`, remove `a[i]`, compute the sum of all remaining elements, divide by `n - 1`, and check whether the result equals `a[i]`.

The brute force is correct because it follows the definition literally. The problem is the repeated summation. Computing the remaining sum takes `O(n)` time for one position, and we repeat this for all `n` positions, giving `O(n^2)` total complexity.

With `n = 2 · 10^5`, this becomes roughly:

```
2 · 10^5 × 2 · 10^5 = 4 · 10^10
```

operations, which is far too slow.

The key observation is that the sum of the remaining elements can be obtained instantly if we already know the total array sum.

Let:

```
total = sum of all elements
```

If we remove `a[i]`, then:

```
remaining_sum = total - a[i]
```

The condition becomes:

```
a[i] = (total - a[i]) / (n - 1)
```

Instead of actually computing the average as a floating point value, we rearrange the equation:

```
a[i] × (n - 1) = total - a[i]
```

or equivalently:

```
a[i] × n = total
```

This is the entire problem reduced to one simple equality.

Now every position can be checked independently in constant time, giving an `O(n)` solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the array and compute its total sum.

The total sum lets us derive the sum of the remaining elements after removing any position in constant time.
2. Create an empty list `answer` to store valid indices.

We must output indices in increasing order, so scanning from left to right naturally preserves the required order.
3. For every index `i`, check whether:

```
a[i] × n == total
```

This comes directly from rearranging the average condition.
4. If the condition holds, append `i + 1` to the answer list.

The problem uses 1-based indexing, while Python arrays use 0-based indexing.
5. Print the number of valid indices.
6. Print the indices themselves.

### Why it works

For an index `i` to be valid, the value `a[i]` must equal the average of all other elements:

```
a[i] = (total - a[i]) / (n - 1)
```

Multiplying both sides by `n - 1` gives:

```
a[i](n - 1) = total - a[i]
```

Moving terms together:

```
a[i]n = total
```

The algorithm checks exactly this condition for every index. Since the equation is mathematically equivalent to the original definition, every reported index is correct, and every correct index is reported.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    total = sum(a)

    ans = []

    for i in range(n):
        if a[i] * n == total:
            ans.append(i + 1)

    print(len(ans))

    if ans:
        print(*ans)

solve()
```

The first step computes the total sum once. This is the crucial optimization that removes the need for repeated summation.

The condition:

```
a[i] * n == total
```

is the rearranged version of the original average equation. Using integer arithmetic avoids all floating point issues.

The answer list stores 1-based indices because that is what the statement requires. Forgetting the `+1` is a common off-by-one mistake.

The second output line is printed only when there is at least one valid index. The problem allows either omitting the line or printing an empty line when the answer count is zero.

## Worked Examples

### Example 1

Input:

```
5
1 2 3 4 5
```

The total sum is:

```
15
```

| Index | Value | Check `value × n` | Total | Valid |
| --- | --- | --- | --- | --- |
| 1 | 1 | 5 | 15 | No |
| 2 | 2 | 10 | 15 | No |
| 3 | 3 | 15 | 15 | Yes |
| 4 | 4 | 20 | 15 | No |
| 5 | 5 | 25 | 15 | No |

Output:

```
1
3
```

This example shows the simplified condition in action. Instead of recomputing averages repeatedly, every index reduces to one multiplication and one comparison.

### Example 2

Input:

```
5
7 7 7 7 7
```

The total sum is:

```
35
```

| Index | Value | Check `value × n` | Total | Valid |
| --- | --- | --- | --- | --- |
| 1 | 7 | 35 | 35 | Yes |
| 2 | 7 | 35 | 35 | Yes |
| 3 | 7 | 35 | 35 | Yes |
| 4 | 7 | 35 | 35 | Yes |
| 5 | 7 | 35 | 35 | Yes |

Output:

```
5
1 2 3 4 5
```

This confirms that the algorithm correctly handles arrays where every position satisfies the condition.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One pass to compute the sum and one pass to test all indices |
| Space | O(1) excluding output | Only a few variables are used |

The solution comfortably fits the constraints. Even for `n = 2 · 10^5`, the algorithm performs only a few linear passes over the array.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    out = io.StringIO()
    sys.stdout = out

    n = int(input())
    a = list(map(int, input().split()))

    total = sum(a)

    ans = []

    for i in range(n):
        if a[i] * n == total:
            ans.append(i + 1)

    print(len(ans))

    if ans:
        print(*ans)

    sys.stdout = sys.__stdout__

    return out.getvalue()

# provided sample
assert run("5\n1 2 3 4 5\n") == "1\n3\n", "sample 1"

# minimum size, no valid index
assert run("2\n1 2\n") == "0\n", "minimum size"

# all equal values
assert run("4\n6 6 6 6\n") == "4\n1 2 3 4\n", "all equal"

# exactly one valid index
assert run("3\n1 2 3\n") == "1\n2\n", "single valid index"

# no index because average is fractional
assert run("4\n1 1 1 2\n") == "0\n", "fractional averages"

# larger mixed case
assert run("6\n2 2 2 2 2 2\n") == "6\n1 2 3 4 5 6\n", "all positions valid"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 / 1 2` | `0` | Minimum array size |
| `4 / 6 6 6 6` | `4 / 1 2 3 4` | Every position valid |
| `3 / 1 2 3` | `1 / 2` | Single valid index |
| `4 / 1 1 1 2` | `0` | Fractional remaining averages |
| `6 / 2 2 2 2 2 2` | `6 / 1 2 3 4 5 6` | Larger all-equal case |

## Edge Cases

Consider the case where the remaining average is fractional.

Input:

```
4
1 1 1 2
```

The total sum is `5`.

For each position:

| Index | Value | Check `value × n` | Total | Valid |
| --- | --- | --- | --- | --- |
| 1 | 1 | 4 | 5 | No |
| 2 | 1 | 4 | 5 | No |
| 3 | 1 | 4 | 5 | No |
| 4 | 2 | 8 | 5 | No |

Output:

```
0
```

The algorithm never performs division, so it naturally handles non-integer averages correctly.

Now consider an array where all values are identical.

Input:

```
5
9 9 9 9 9
```

The total sum is `45`.

For every index:

```
9 × 5 = 45
```

so every position is accepted.

Output:

```
5
1 2 3 4 5
```

This confirms that the equality condition correctly captures the average relationship even when many indices satisfy it simultaneously.

Finally, consider the smallest possible array size.

Input:

```
2
3 3
```

The total sum is `6`.

For both positions:

```
3 × 2 = 6
```

Both indices are valid because removing one `3` leaves a single remaining element `3`, whose average is still `3`.

Output:

```
2
1 2
```

This verifies that the formula also works correctly for the smallest allowed `n`.
