---
title: "CF 102566C - Emojis"
description: "We have several arrays of emoji values. The goal is not to sort the entire array. Instead, we may choose a contiguous part of the array and delete some elements inside that part so that the remaining elements are in non-decreasing order."
date: "2026-08-06T20:54:13+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102566
codeforces_index: "C"
codeforces_contest_name: "AGM 2020, Qualification Round"
rating: 0
weight: 102566
solve_time_s: 89
verified: true
draft: false
---

[CF 102566C - Emojis](https://codeforces.com/problemset/problem/102566/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 29s  
**Verified:** yes  

## Solution
## Problem Understanding

We have several arrays of emoji values. The goal is not to sort the entire array. Instead, we may choose a contiguous part of the array and delete some elements inside that part so that the remaining elements are in non-decreasing order. Elements before and after that chosen part do not matter and do not count as deletions.

The first value we must output is the maximum possible number of emojis that can remain. The second value is the minimum number of deleted emojis needed inside the chosen interval to obtain such an optimal sequence.

The constraints force a near-linear solution. A single test case can contain up to 100000 values, and the sum of all sizes is at most 1000000. Trying every interval already gives quadratic work, around 10^10 operations for the largest case, which is far beyond the limit. We need an O(N log N) method.

A common mistake is to compute only the longest non-decreasing subsequence length and output N minus that value. That counts emojis outside the chosen interval as removed, which is not allowed. For example, the array `1 2 3 100 0` has a longest non-decreasing subsequence of length 4 using `1 2 3 100`, but the answer removes only the `0` if the whole interval is chosen. The outside elements are not automatically deleted.

Another edge case is when the whole array is already non-decreasing. For input `1 2 2 5`, the correct output is `4 0`. A solution that always counts removed elements as `N - length` can accidentally work here but fail on arrays where the best subsequence is inside a smaller interval.

## Approaches

The brute-force approach is to try every possible interval, compute the longest non-decreasing subsequence inside it, and keep the best answer. There are O(N^2) intervals, and computing a subsequence for each interval is already expensive, so the total work becomes O(N^3) in a direct implementation.

The key observation is that the remaining emojis must form a non-decreasing subsequence of the original array. The maximum number of kept emojis is the longest non-decreasing subsequence. The extra condition about deletions means we must remember where that subsequence starts and ends, because only the elements between those positions can be removed.

We can use the patience sorting idea for the longest non-decreasing subsequence. While processing the array, we maintain the smallest possible ending value for every subsequence length. Alongside that information, we keep enough position data to reconstruct the best interval containing an optimal subsequence.

The subsequence length gives the first answer. Once the chosen optimal subsequence has first index `l` and last index `r`, the number of deletions is `(r - l + 1) - length`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N^3) | O(N) | Too slow |
| Optimal | O(N log N) | O(N) | Accepted |

## Algorithm Walkthrough

1. Compress the values only for ordering purposes and process the array from left to right. We need to know, for every value, the best non-decreasing subsequence that can be extended by the current element.
2. Use a Fenwick tree over the compressed values. Each Fenwick node stores the best subsequence state ending with values in that prefix. A state contains the subsequence length, its starting position, and its ending position.
3. For the current value `a[i]`, query all previous values that are less than or equal to it. The best returned state can be extended because adding `a[i]` keeps the sequence non-decreasing.
4. Create a new state by increasing the length by one and setting the ending position to `i`. Update the Fenwick tree at the compressed position of `a[i]`.
5. After processing all elements, choose the state with the largest length. If several states have the same length, choose the one with the smallest interval size.
6. The answer length is the chosen state length. The number of removed emojis is the size of its interval minus the kept length.

Why it works:

Every valid final message corresponds to a non-decreasing subsequence inside some interval. The Fenwick tree considers every possible predecessor relation, because a value can extend exactly the subsequences ending with a value not greater than itself. The stored best states preserve the candidates that can lead to an optimal result, so the final maximum length is the longest possible non-decreasing subsequence and the chosen interval is the smallest one among optimal solutions.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve_case(a):
    vals = sorted(set(a))
    comp = {v: i + 1 for i, v in enumerate(vals)}
    m = len(vals)

    bit = [(0, 0, 0)] * (m + 2)

    def better(x, y):
        if x[0] != y[0]:
            return x if x[0] > y[0] else y
        if x[0] == 0:
            return x
        sx = x[2] - x[1] + 1
        sy = y[2] - y[1] + 1
        return x if sx < sy else y

    def query(i):
        ans = (0, 0, 0)
        while i:
            ans = better(ans, bit[i])
            i -= i & -i
        return ans

    def update(i, value):
        while i <= m:
            bit[i] = better(bit[i], value)
            i += i & -i

    answer = (0, 0, 0)

    for i, x in enumerate(a):
        prev = query(comp[x])
        if prev[0] == 0:
            cur = (1, i, i)
        else:
            cur = (prev[0] + 1, prev[1], i)
        update(comp[x], cur)
        answer = better(answer, cur)

    return answer[0], answer[2] - answer[1] + 1 - answer[0]

def main():
    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        x, y = solve_case(a)
        out.append(f"{x} {y}")
    print("\n".join(out))

if __name__ == "__main__":
    main()
```

The Fenwick tree stores information about prefixes of values. Querying a prefix is exactly the operation needed for non-decreasing subsequences, because the previous chosen value must not exceed the current one.

The state stores the starting index rather than only the length. This is the detail that handles the unusual deletion rule. We do not want the number of deletions to include emojis outside the selected interval, so the interval boundaries must be tracked.

The compressed coordinates are necessary because emoji values can be as large as 10^9, but only their relative ordering matters. The number of compressed values is at most N, so all Fenwick operations remain O(log N).

## Worked Examples

For the sample:

`4 3 2 1 5 6 3 3 1 3`

the important states are:

| Index | Value | Best length ending here | Interval |
| --- | --- | --- | --- |
| 0 | 4 | 1 | 0 to 0 |
| 4 | 5 | 2 | 0 to 4 |
| 5 | 6 | 3 | 0 to 5 |
| 7 | 3 | 3 | 3 to 7 |
| 9 | 3 | 4 | 6 to 9 |

The final subsequence is `3 3 1 3`? This candidate is rejected because it is not non-decreasing. The valid optimal state corresponds to the interval containing `1 3 3 3`, with length 4 and interval size 7, so three emojis are removed.

For an already sorted input:

`1 2 2 5`

| Index | Value | Best length ending here | Interval |
| --- | --- | --- | --- |
| 0 | 1 | 1 | 0 to 0 |
| 1 | 2 | 2 | 0 to 1 |
| 2 | 2 | 3 | 0 to 2 |
| 3 | 5 | 4 | 0 to 3 |

The selected interval already contains every element, so the deletion count is zero.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N log N) | Each value performs one Fenwick query and one update |
| Space | O(N) | Coordinate compression and Fenwick storage |

The total number of elements over all test cases is limited to 1000000, so the O(N log N) solution fits comfortably.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    data = sys.stdin.read().strip().split()
    sys.stdin = old

    t = int(data[0])
    idx = 1
    ans = []
    for _ in range(t):
        n = int(data[idx])
        idx += 1
        arr = list(map(int, data[idx:idx+n]))
        idx += n
        x, y = solve_case(arr)
        ans.append(f"{x} {y}")
    return "\n".join(ans)

assert run("""1
10
4 3 2 1 5 6 3 3 1 3
""") == "4 3"

assert run("""1
1
7
""") == "1 0"

assert run("""1
5
2 2 2 2 2
""") == "5 0"

assert run("""1
5
5 4 3 2 1
""") == "1 0"

assert run("""1
6
1 10 2 3 4 5
""") == "5 1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single element | `1 0` | Minimum size handling |
| Equal values | `5 0` | Non-decreasing allows equality |
| Strictly decreasing values | `1 0` | No increasing choice is forced |
| One large value inside an increasing sequence | `5 1` | Correct handling of internal deletions |

## Edge Cases

For a single emoji, the chosen interval contains only that element. The algorithm creates a subsequence of length one and the interval length is also one, so the number of deletions is zero.

For arrays with repeated values, equality must be accepted. The Fenwick query uses values less than or equal to the current value, which is the difference between handling non-decreasing sequences and strictly increasing ones.

For decreasing arrays such as `5 4 3 2 1`, every element can only start a subsequence of length one. The algorithm still returns the correct maximum length and does not invent unnecessary deletions outside the chosen interval.

For cases where the optimal subsequence is surrounded by irrelevant elements, the stored start and end positions prevent counting those outside elements as removals. This is the central difference between this problem and a normal longest subsequence problem.

I can also provide a shorter contest-style editorial version if you want something closer to what would appear on Codeforces.
