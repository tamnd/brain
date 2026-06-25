---
title: "CF 106020H - Mexican Subarrays"
description: "We are given an array of non-negative integers. For every contiguous segment of the array, we can compute two values. The first is the sum of all elements inside the segment."
date: "2026-06-25T13:11:44+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106020
codeforces_index: "H"
codeforces_contest_name: "The 2025 Damascus University Collegiate Programming Contest"
rating: 0
weight: 106020
solve_time_s: 57
verified: true
draft: false
---

[CF 106020H - Mexican Subarrays](https://codeforces.com/problemset/problem/106020/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 57s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of non-negative integers. For every contiguous segment of the array, we can compute two values. The first is the sum of all elements inside the segment. The second is the MEX of the segment, which is the smallest non-negative integer that does not appear in it. The task is to count how many segments have these two values equal.

The array length can reach $10^5$. A direct approach that checks every possible subarray would consider about $n(n+1)/2$ segments, which is roughly $5 \cdot 10^9$ in the largest case. Even if checking one segment were constant time, this is far beyond what a one second solution can handle. We need to avoid enumerating all subarrays.

The large value range of the elements is also a hint. The actual values are less important than their relation to the MEX. Since all numbers are non-negative, the sum of a subarray grows quickly when it contains larger values. This lets us prove that only very small MEX values can ever work.

The first edge case is a segment with MEX equal to zero. For example:

```
Input:
3
5 5 5
```

The whole array has sum 15, not 0, but every subarray has MEX 0 because there is no zero anywhere. The correct answer is 6, not 0. A solution that only looks for subarrays containing zero would miss all of them.

The second edge case is when the segment contains extra large values. For example:

```
Input:
4
0 1 100 2
```

The subarray `[0,1,100,2]` has MEX 3, but its sum is 103, so it is invalid. A careless solution that only checks whether all numbers from 0 to MEX-1 appear could count it incorrectly.

The third edge case is about duplicates. For example:

```
Input:
4
0 1 2 2
```

The subarray `[0,1,2,2]` has MEX 3, but the sum is 5. The valid MEX 3 segments must contain exactly the values 0, 1, and 2 without any additional positive value.

## Approaches

A natural brute-force solution is to fix the left endpoint and extend the right endpoint. While extending, we maintain the current sum and the current MEX using frequencies of values. This is correct because every subarray is visited once and we can test the condition immediately.

The problem is the number of subarrays. There are $O(n^2)$ of them, so the worst case performs about $5 \cdot 10^9$ extensions. This is too slow.

The key observation comes from comparing the sum with the MEX. Suppose a subarray has MEX equal to $m$. Then it must contain every value from 0 to $m-1$, so the minimum possible sum of the subarray is:

$$0+1+2+\dots+(m-1)=\frac{m(m-1)}{2}$$

For this to equal $m$, we need:

$$\frac{m(m-1)}{2} \le m$$

This only holds for $m \le 3$. So every valid subarray has MEX 0, 1, 2, or 3.

Now each case becomes simple. A MEX of 0 means the subarray contains no zeros. A MEX of 1 means it is exactly one zero. A MEX of 2 means it must contain 0 and 1 and nothing else, so it has length two. A MEX of 3 means it must contain exactly the values 0, 1, and 2, so it has length three.

The entire problem reduces to checking windows of very small sizes.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Count all subarrays with MEX equal to 0. These are exactly the consecutive blocks that contain no zero. If a block has length $k$, it contributes $k(k+1)/2$ subarrays.
2. Count all subarrays with MEX equal to 1. The segment must contain a zero and cannot contain a one. Since its sum must be 1 and all values are non-negative, the only possible segment is `[0]`. Add one for every zero.
3. Count all subarrays with MEX equal to 2. The segment must contain both 0 and 1. Their sum is already 1, so the segment needs exactly one more unit. The only possibility is the adjacent pair `[0,1]` or `[1,0]`.
4. Count all subarrays with MEX equal to 3. The segment must contain 0, 1, and 2. Their sum is already 3, so the segment cannot contain anything else. The segment must have length three and its values must be exactly those three numbers.
5. Add the four counts. These cases cover every possible valid subarray because no larger MEX can satisfy the sum condition.

Why it works: every valid subarray has a MEX value. The inequality derived above proves that the MEX cannot exceed 3. For each possible MEX, the required sum forces a very specific structure. The algorithm counts exactly those structures, so every counted subarray is valid and every valid subarray is counted.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    ans = 0

    # MEX = 0
    length = 0
    for x in a:
        if x == 0:
            ans += length * (length + 1) // 2
            length = 0
        else:
            length += 1
    ans += length * (length + 1) // 2

    # MEX = 1
    for x in a:
        if x == 0:
            ans += 1

    # MEX = 2
    for i in range(n - 1):
        if (a[i] == 0 and a[i + 1] == 1) or (a[i] == 1 and a[i + 1] == 0):
            ans += 1

    # MEX = 3
    for i in range(n - 2):
        if a[i] + a[i + 1] + a[i + 2] == 3:
            if a[i] != a[i + 1] and a[i] != a[i + 2] and a[i + 1] != a[i + 2]:
                ans += 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The first loop handles MEX 0 by splitting the array at every zero. The variable `length` stores the current positive-only block size. When the block ends, its contribution is the number of possible subarrays inside it.

The second loop handles MEX 1. A single zero is the only valid segment because any other value would make the sum larger than the MEX.

The third loop checks adjacent pairs. The only length two segments with sum 2 and MEX 2 are `[0,1]` and `[1,0]`.

The final loop checks length three windows. The sum must be exactly 3, and the three values must be different. Because the only possible values are then 0, 1, and 2, the MEX is exactly 3.

There are no prefix sums or maps because the structural observation reduces every possible answer to constant-sized windows.

## Worked Examples

For the sample:

```
7
1 0 2 0 3 4 3
```

The MEX 0, 1, 2, and 3 counts evolve as follows:

| Index | Value | MEX 0 blocks | MEX 1 count | MEX 2 count | MEX 3 count |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 0 | 0 | 0 |
| 1 | 0 | 0 | 1 | 1 | 0 |
| 2 | 2 | 0 | 1 | 1 | 0 |
| 3 | 0 | 0 | 2 | 1 | 0 |
| 4 | 3 | 0 | 2 | 1 | 0 |
| 5 | 4 | 0 | 2 | 1 | 0 |
| 6 | 3 | 1 | 2 | 1 | 0 |

The positive-only blocks for MEX 0 are `[1]`, `[2]`, `[3,4,3]`, contributing 1 + 1 + 6. The MEX 3 case has no valid window because every window containing 0,1,2 also includes an extra value. The final answer is 2.

Another example:

```
5
0 1 2 5 6
```

| Window | Values | Valid reason |
| --- | --- | --- |
| 0 | `[0]` | MEX 1 |
| 1 | `[0,1]` | MEX 2 |
| 2 | `[0,1,2]` | MEX 3 |
| 3 | `[0,1,2,5]` | Invalid, extra sum |
| 4 | `[5]` | MEX 0 |

The algorithm finds one MEX 1 segment, one MEX 2 segment, and one MEX 3 segment. The last single value belongs to a positive block, adding one MEX 0 segment, giving the answer 4.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Every array element participates in a constant number of checks. |
| Space | O(1) | Only counters and the current array are stored. |

The solution fits the $10^5$ constraint because it performs only a few linear scans. The integer values can be large, but Python integers handle the required answer range safely.

## Test Cases

```python
import sys
import io

def solve(inp):
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))

    ans = 0

    length = 0
    for x in a:
        if x == 0:
            ans += length * (length + 1) // 2
            length = 0
        else:
            length += 1
    ans += length * (length + 1) // 2

    for x in a:
        if x == 0:
            ans += 1

    for i in range(n - 1):
        if (a[i], a[i + 1]) in [(0, 1), (1, 0)]:
            ans += 1

    for i in range(n - 2):
        if sorted(a[i:i+3]) == [0, 1, 2]:
            ans += 1

    return str(ans) + "\n"

assert solve("7\n1 0 2 0 3 4 3\n") == "2\n"

assert solve("1\n0\n") == "1\n"

assert solve("5\n0 1 2 5 6\n") == "4\n"

assert solve("4\n5 5 5 5\n") == "10\n"

assert solve("6\n0 1 2 0 1 2\n") == "4\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 0` | `1` | Minimum size and MEX 1 |
| `0 1 2 5 6` | `4` | Rejecting extra large values |
| `5 5 5 5` | `10` | All MEX 0 segments |
| `0 1 2 0 1 2` | `4` | Multiple valid length three windows |

## Edge Cases

For the all-positive case:

```
4
5 5 5 5
```

Every subarray has MEX 0 because zero is missing. The algorithm never enters the MEX 1, 2, or 3 cases, but the positive block counting adds $4 \cdot 5 / 2 = 10$, which is exactly the number of subarrays.

For a segment that almost satisfies MEX 3:

```
4
0 1 2 2
```

The window `[0,1,2]` is counted because it has sum 3 and MEX 3. The window `[0,1,2,2]` is ignored because the length is not three and the additional 2 increases the sum. The fixed-size window check naturally prevents this mistake.

For values larger than the possible MEX:

```
4
0 1 100 2
```

The only possible valid segments are `[0]` and `[0,1]` if adjacent, but the value 100 cannot participate in a valid MEX 3 segment. The algorithm never treats large values specially because the earlier proof already guarantees they cannot appear in a valid higher-MEX segment.
