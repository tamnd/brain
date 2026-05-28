---
title: "CF 18C - Stripe"
description: "We have a strip of cells, and each cell contains an integer. We may cut the strip only between adjacent cells, which spl"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "implementation"]
categories: ["algorithms"]
codeforces_contest: 18
codeforces_index: "C"
codeforces_contest_name: "Codeforces Beta Round 18 (Div. 2 Only)"
rating: 1200
weight: 18
solve_time_s: 103
verified: true
draft: false
---

[CF 18C - Stripe](https://codeforces.com/problemset/problem/18/C)

**Rating:** 1200  
**Tags:** data structures, implementation  
**Solve time:** 1m 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a strip of cells, and each cell contains an integer. We may cut the strip only between adjacent cells, which splits the array into a left part and a right part. The task is to count how many cut positions produce two non-empty parts with equal sums.

For example, if the array is:

```
[1, 2, 3, 3]
```

cutting after the second element gives:

```
[1, 2] | [3, 3]
```

The left sum is `3`, the right sum is `6`, so this cut is invalid.

The input size reaches `10^5`, which immediately rules out algorithms that repeatedly recompute sums for every cut. A quadratic solution would perform roughly `10^10` operations in the worst case, which is far beyond what fits inside a 2 second limit. The target complexity is linear time, or something very close to it.

The numbers may also be negative, so we cannot rely on monotonic behavior. Prefix sums can increase or decrease arbitrarily. Any solution based on two pointers or greedy expansion would fail because the total does not move in a predictable direction.

There are several easy-to-miss edge cases.

Consider a single element:

```
1
5
```

There is no valid cut because both pieces must contain at least one element. The correct answer is:

```
0
```

A careless implementation that checks all indices from `0` to `n` could accidentally count empty partitions.

Another tricky case appears when the total sum is odd:

```
4
1 2 3 5
```

The total is `11`. Two equal integer halves are impossible, so the answer must be:

```
0
```

Some implementations still scan all cuts even though no solution can exist.

Negative values are another source of mistakes:

```
5
2 -2 2 -2 0
```

The total sum is `0`, and there are several valid cuts. Any approach that assumes prefix sums only grow will break here.

Finally, the cut position itself matters. We cannot cut after the last element because the right side would be empty. For example:

```
2
1 -1
```

The total sum is `0`, but there is only one possible cut, after the first element:

```
[1] | [-1]
```

The sums are not equal, so the answer is `0`.

## Approaches

The most direct solution is to try every possible cut and independently compute the sum of the left and right parts.

Suppose we cut after index `i`. We can compute:

```
left_sum  = sum(a[0..i])
right_sum = sum(a[i+1..n-1])
```

If the sums match, we increment the answer.

This approach is correct because it explicitly checks every legal partition. The problem is efficiency. Computing a sum over a range takes `O(n)` time if done naively, and there are `n - 1` possible cuts. The total complexity becomes `O(n^2)`.

With `n = 100000`, this means roughly:

```
100000 * 100000 = 10^10
```

operations in the worst case, which is far too slow.

The key observation is that neighboring cuts overlap heavily. When we move the cut one step to the right, almost all elements stay in the same partition. Recomputing sums from scratch wastes work.

This naturally suggests prefix sums.

If we know the total sum of the entire array, then for a cut after index `i`:

```
left_sum  = prefix[i]
right_sum = total_sum - prefix[i]
```

The condition becomes:

```
prefix[i] == total_sum - prefix[i]
```

which simplifies to:

```
2 * prefix[i] == total_sum
```

Now each cut can be checked in constant time. We scan the array once, maintain a running prefix sum, and count how many positions satisfy the equality.

This reduces the complexity from quadratic to linear.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the array and compute its total sum.

We need the total because every right-side sum can be written as:

```
total_sum - left_sum
```
2. Initialize a running prefix sum as `0` and the answer as `0`.

The prefix sum represents the sum of the left partition for the current cut.
3. Iterate through the array from index `0` to `n - 2`.

We stop at `n - 2` because the cut must leave at least one element on the right side.
4. Add the current element to the prefix sum.

After adding `a[i]`, the prefix sum equals the sum of the left partition if we cut after index `i`.
5. Check whether:

```
prefix_sum * 2 == total_sum
```

If this condition holds, then the left and right partitions have equal sums.
6. If the condition is true, increment the answer.
7. After processing all valid cut positions, print the answer.

### Why it works

At every step, the running prefix sum equals the sum of the left partition created by cutting after the current index. The right partition must then have sum:

```
total_sum - prefix_sum
```

A cut is valid exactly when:

```
prefix_sum == total_sum - prefix_sum
```

The algorithm checks this condition for every legal cut position exactly once. Since every possible cut is examined and the equality test is mathematically equivalent to the original requirement, the algorithm cannot miss a valid cut or count an invalid one.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))

total_sum = sum(a)

prefix_sum = 0
answer = 0

for i in range(n - 1):
    prefix_sum += a[i]

    if prefix_sum * 2 == total_sum:
        answer += 1

print(answer)
```

The first part reads the input and computes the total sum of the array. This gives us immediate access to the right-side sum for every cut.

The variable `prefix_sum` stores the running sum of the left partition. As we iterate through the array, each new element becomes part of the left side.

The loop runs only until `n - 2`. This detail matters. If we allowed `i = n - 1`, the right partition would be empty, which violates the problem statement.

The condition:

```
prefix_sum * 2 == total_sum
```

avoids division entirely. This is cleaner and also avoids issues with odd totals. If the total sum is odd, no integer prefix sum can satisfy the equality, so the condition naturally fails.

Python integers automatically handle large values safely, so overflow is not a concern here. In languages with fixed-width integers, using a 64-bit type would still be recommended.

## Worked Examples

### Example 1

Input:

```
9
1 5 -6 7 9 -16 0 -2 2
```

The total sum is `0`.

| i | a[i] | prefix_sum | right_sum | Valid? | answer |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 1 | -1 | No | 0 |
| 1 | 5 | 6 | -6 | No | 0 |
| 2 | -6 | 0 | 0 | Yes | 1 |
| 3 | 7 | 7 | -7 | No | 1 |
| 4 | 9 | 16 | -16 | No | 1 |
| 5 | -16 | 0 | 0 | Yes | 2 |
| 6 | 0 | 0 | 0 | Yes | 3 |
| 7 | -2 | -2 | 2 | No | 3 |

Final answer:

```
3
```

This trace shows why prefix sums are enough. At each cut, the entire decision depends only on the running total up to that point.

### Example 2

Input:

```
5
2 1 1 2 2
```

The total sum is `8`.

| i | a[i] | prefix_sum | right_sum | Valid? | answer |
| --- | --- | --- | --- | --- | --- |
| 0 | 2 | 2 | 6 | No | 0 |
| 1 | 1 | 3 | 5 | No | 0 |
| 2 | 1 | 4 | 4 | Yes | 1 |
| 3 | 2 | 6 | 2 | No | 1 |

Final answer:

```
1
```

This example demonstrates the standard positive-number case. Only one cut splits the array into equal halves.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | The array is scanned once |
| Space | O(1) | Only a few variables are stored |

A linear scan over `100000` elements easily fits within the time limit. The memory usage stays constant regardless of input size.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))

    total_sum = sum(a)

    prefix_sum = 0
    answer = 0

    for i in range(n - 1):
        prefix_sum += a[i]

        if prefix_sum * 2 == total_sum:
            answer += 1

    print(answer)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    output = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return output.strip()

# provided sample
assert run(
"""9
1 5 -6 7 9 -16 0 -2 2
"""
) == "3", "sample 1"

# minimum size
assert run(
"""1
5
"""
) == "0", "single element"

# all zeros
assert run(
"""5
0 0 0 0 0
"""
) == "4", "every cut works"

# odd total sum
assert run(
"""4
1 2 3 5
"""
) == "0", "odd total"

# negative numbers
assert run(
"""5
2 -2 2 -2 0
"""
) == "3", "negative values"

# off-by-one boundary
assert run(
"""2
1 -1
"""
) == "0", "cannot cut after last element"

# balanced split in middle
assert run(
"""6
1 1 1 1 1 1
"""
) == "1", "single valid split"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 5` | `0` | No cut possible |
| `0 0 0 0 0` | `4` | Every cut is valid |
| `1 2 3 5` | `0` | Odd total sum |
| `2 -2 2 -2 0` | `3` | Negative values and zero total |
| `1 -1` | `0` | Prevents empty right partition |
| `1 1 1 1 1 1` | `1` | Standard balanced split |

## Edge Cases

Consider the smallest possible input:

```
1
5
```

The loop runs over:

```
range(n - 1) = range(0)
```

so no iterations occur. The answer stays `0`, which is correct because we cannot split one element into two non-empty parts.

Now consider an odd total sum:

```
4
1 2 3 5
```

The total sum is `11`.

During the scan:

| i | prefix_sum | prefix_sum * 2 |
| --- | --- | --- |
| 0 | 1 | 2 |
| 1 | 3 | 6 |
| 2 | 6 | 12 |

None equals `11`, so the answer remains `0`. The algorithm naturally rejects impossible cases without special handling.

Next, consider negative values:

```
5
2 -2 2 -2 0
```

The total sum is `0`.

The running prefix sums become:

```
2, 0, 2, 0
```

Whenever the prefix sum is `0`, the remaining suffix also sums to `0`, so those cuts are counted correctly. The algorithm never assumes sums increase monotonically, so negative numbers cause no issues.

Finally, consider the boundary condition:

```
2
1 -1
```

The only legal cut is after index `0`.

The prefix sum becomes `1`, while the right side is `-1`, so the condition fails and the answer is `0`.

The algorithm never checks a cut after the final element because the loop stops at `n - 2`. This avoids accidentally counting an empty right partition.
