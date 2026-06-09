---
title: "CF 1843A - Sasha and Array Coloring"
description: "We are given an array of integers. Every element must be assigned to exactly one color, and we may use any number of colors. For each color, we look at all values assigned to that color."
date: "2026-06-09T06:07:20+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "sortings", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1843
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 881 (Div. 3)"
rating: 800
weight: 1843
solve_time_s: 103
verified: true
draft: false
---

[CF 1843A - Sasha and Array Coloring](https://codeforces.com/problemset/problem/1843/A)

**Rating:** 800  
**Tags:** greedy, sortings, two pointers  
**Solve time:** 1m 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers. Every element must be assigned to exactly one color, and we may use any number of colors.

For each color, we look at all values assigned to that color. Its contribution to the total score is the difference between the largest and smallest value in that group. The goal is to choose a coloring that maximizes the sum of these contributions.

The positions of the elements are irrelevant. The cost of a color depends only on the values inside that color, so after understanding the structure of the problem, we can think purely about the multiset of numbers.

The constraints are very small. Each test case contains at most 50 numbers, and there are at most 1000 test cases. Even an $O(n^2)$ or $O(n^3)$ solution would be completely safe. The challenge is not performance but recognizing the greedy structure hidden in the definition of the cost.

A common mistake is to think that putting all elements into one color is always best because that produces the largest possible range. Consider:

```
4
1 3 6 9
```

One color gives a cost of $9 - 1 = 8$.

A better coloring is:

```
{1, 9}, {3, 6}
```

which gives:

```
(9 - 1) + (6 - 3) = 11
```

Another easy pitfall is forgetting that singleton groups contribute zero. For example:

```
1
5
```

The only possible coloring consists of one group containing the value 5, so the answer is:

```
5 - 5 = 0
```

A solution that blindly pairs values without handling odd lengths carefully can produce incorrect results.

Arrays with all equal values are also important:

```
4
2 2 2 2
```

Every group has maximum equal to minimum, so every contribution is zero and the answer is zero regardless of the coloring.

## Approaches

A brute-force approach would try every possible coloring of the array and compute the resulting cost. This is correct because it explores every valid assignment of elements to colors.

The problem is that the number of colorings grows extremely quickly. Even for modest values of $n$, the number of set partitions becomes enormous. The Bell numbers make exhaustive search infeasible.

To find a better approach, we need to understand what contributes to the score. Every group's contribution is:

$$\max(\text{group}) - \min(\text{group})$$

Only the smallest and largest element of a group matter. Any elements placed between them do not affect that group's contribution.

Suppose the array is sorted:

$$a_0 \le a_1 \le \dots \le a_{n-1}$$

If we create a group using some small value and some large value, the contribution is exactly their difference. To maximize the total sum, we want the largest numbers to act as group maxima and the smallest numbers to act as group minima.

The best possible strategy is to repeatedly pair the current largest unused value with the current smallest unused value. Each such pair contributes:

$$a_r - a_l$$

where $l$ points to the left end and $r$ points to the right end of the sorted array.

Any unpaired middle element, when $n$ is odd, forms a singleton group and contributes zero.

After sorting, the answer becomes:

$$(a_{n-1}-a_0) + (a_{n-2}-a_1) + \cdots$$

This naturally leads to a two-pointer solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(n log n) | O(1) extra (excluding sorting) | Accepted |

## Algorithm Walkthrough

1. Sort the array in non-decreasing order.

After sorting, the smallest values are on the left and the largest values are on the right.
2. Initialize two pointers, `l = 0` and `r = n - 1`.

These pointers represent the smallest and largest unused elements.
3. Initialize the answer to zero.
4. While `l < r`, add `a[r] - a[l]` to the answer.

This pairs the largest remaining value with the smallest remaining value, extracting the maximum possible contribution from those two elements.
5. Move `l` one step right and `r` one step left.

Both elements are now used.
6. Continue until the pointers cross.

If one element remains in the middle, it forms a singleton color whose contribution is zero.
7. Output the accumulated answer.

### Why it works

After sorting, every contribution comes from matching a value that acts as a group's minimum with another value that acts as that group's maximum.

Consider any optimal coloring. The largest element of the entire array can only contribute through being a maximum of some group. To maximize its contribution, it should be paired with the smallest available value. Using a larger minimum would only reduce the difference.

Once the smallest and largest elements are paired, the same argument applies to the remaining elements. Repeatedly matching extremes maximizes every extracted difference.

This produces exactly the sum:

$$(a_{n-1}-a_0)+(a_{n-2}-a_1)+\cdots$$

which is the largest total cost achievable by any coloring.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        a.sort()

        l, r = 0, n - 1
        ans = 0

        while l < r:
            ans += a[r] - a[l]
            l += 1
            r -= 1

        print(ans)

if __name__ == "__main__":
    solve()
```

The first step sorts the array. After sorting, the optimal pairing becomes obvious because the smallest and largest unused elements are always at the ends.

The two pointers `l` and `r` walk inward from both ends. Each iteration adds one optimal pair contribution. Since both endpoints are consumed immediately after use, every element participates in at most one pair.

The condition `l < r` is important. When `n` is odd, one middle element remains unpaired. That element corresponds to a singleton color and contributes zero, so no special handling is required.

All arithmetic fits comfortably inside Python integers. Even though the constraints are tiny, the implementation remains efficient and clean.

## Worked Examples

### Example 1

Input array:

```
1 5 6 3 4
```

Sorted array:

```
1 3 4 5 6
```

| Step | l | r | Pair | Contribution | Answer |
| --- | --- | --- | --- | --- | --- |
| Start | 0 | 4 | - | - | 0 |
| 1 | 0 | 4 | (1, 6) | 5 | 5 |
| 2 | 1 | 3 | (3, 5) | 2 | 7 |

The middle value 4 remains alone and contributes zero. The final answer is 7.

This example shows that splitting the array into multiple groups can produce a larger score than putting everything into one group.

### Example 2

Input array:

```
1 6 3 9
```

Sorted array:

```
1 3 6 9
```

| Step | l | r | Pair | Contribution | Answer |
| --- | --- | --- | --- | --- | --- |
| Start | 0 | 3 | - | - | 0 |
| 1 | 0 | 3 | (1, 9) | 8 | 8 |
| 2 | 1 | 2 | (3, 6) | 3 | 11 |

Final answer:

```
11
```

This trace demonstrates the key greedy idea. Pairing extremes extracts the maximum possible contribution from the remaining values at every stage.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates the running time |
| Space | O(1) extra | Only a few variables are used after sorting |

With $n \le 50$, the running time is tiny. Even across 1000 test cases, sorting such small arrays easily fits within the time limit. Memory usage is negligible.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        a.sort()

        l, r = 0, n - 1
        ans = 0

        while l < r:
            ans += a[r] - a[l]
            l += 1
            r -= 1

        out.append(str(ans))

    return "\n".join(out) + "\n"

# provided sample
assert run(
"""6
5
1 5 6 3 4
1
5
4
1 6 3 9
6
1 13 9 3 7 2
4
2 2 2 2
5
4 5 2 2 3
"""
) == """7
0
11
23
0
5
"""

# minimum size
assert run(
"""1
1
42
"""
) == """0
"""

# all equal values
assert run(
"""1
5
7 7 7 7 7
"""
) == """0
"""

# odd length with middle singleton
assert run(
"""1
5
1 2 3 4 5
"""
) == """6
"""

# maximum-sized style case
assert run(
"""1
50
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 50 50 50 50 50 50 50 50 50 50 50 50 50 50 50 50 50 50 50 50 50 50 50 50 50
"""
) == """1225
"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `[42]` | `0` | Minimum array size |
| `[7,7,7,7,7]` | `0` | All values equal |
| `[1,2,3,4,5]` | `6` | Odd length, singleton middle element |
| 25 ones and 25 fifties | `1225` | Many optimal extreme pairings |

## Edge Cases

Consider the smallest possible input:

```
1
5
```

After sorting, the array remains `[5]`. The pointers start at the same position, so the loop never runs. The answer stays zero, which matches the fact that a singleton color contributes `5 - 5 = 0`.

Consider an odd-length array:

```
5
1 2 3 4 5
```

Sorted order is unchanged. The algorithm computes:

```
(5 - 1) + (4 - 2) = 4 + 2 = 6
```

The value `3` remains unpaired. It corresponds to a singleton group with contribution zero, exactly as required.

Consider all equal values:

```
4
2 2 2 2
```

The algorithm adds:

```
(2 - 2) + (2 - 2) = 0
```

Every possible coloring has zero cost because every group's maximum equals its minimum.

Consider a case where using one color is not optimal:

```
4
1 3 6 9
```

One color gives cost `9 - 1 = 8`.

The algorithm computes:

```
(9 - 1) + (6 - 3) = 11
```

This demonstrates the core insight: splitting the numbers into extreme pairs can produce a larger total range sum than grouping everything together.
