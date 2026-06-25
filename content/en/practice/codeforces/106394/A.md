---
title: "CF 106394A - Sushi"
description: "The problem is about a row of sushi pieces where every piece belongs to one of two types. A valid meal segment is a contiguous block where the first half contains only one type of sushi and the second half contains only the other type, with both halves having the same size."
date: "2026-06-25T10:09:54+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106394
codeforces_index: "A"
codeforces_contest_name: "RUCP x WiCS Mini-Contest"
rating: 0
weight: 106394
solve_time_s: 49
verified: true
draft: false
---

[CF 106394A - Sushi](https://codeforces.com/problemset/problem/106394/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem is about a row of sushi pieces where every piece belongs to one of two types. A valid meal segment is a contiguous block where the first half contains only one type of sushi and the second half contains only the other type, with both halves having the same size. The task is to find the maximum possible length of such a segment.

The input describes the number of sushi pieces and the type of every piece from left to right. The output is the length of the longest valid contiguous segment.

The key constraint is that the number of sushi pieces can be large, up to around $10^5$. A solution that checks every possible segment would require quadratic work, which means roughly $10^{10}$ operations in the worst case and is far beyond what a normal time limit allows. We need to find a way to process the row in linear time.

The tricky cases come from segments that look balanced but are not actually valid. For example:

```
6
1 2 1 2 1 2
```

The answer is:

```
2
```

A careless approach might see that there are equal numbers of both types in the whole array and choose a longer segment, but the two halves of the chosen segment must each consist of a single type. Alternating sushi does not satisfy the rule.

Another edge case is when the longest segment is formed exactly at the border between two groups:

```
9
2 2 1 1 1 2 2 2 2
```

The answer is:

```
6
```

The valid segment is `2 2 1 1 1 2` or `1 1 1 2 2 2`. The solution must consider every neighboring pair of equal type groups, not just the largest group.

## Approaches

A straightforward approach is to generate every possible continuous segment. For each segment, we check whether it has two halves of equal length and whether each half contains only one sushi type. This is correct because every possible answer is considered. The problem is that there are $O(n^2)$ possible segments, and checking them can add another factor of $n$, leading to an $O(n^3)$ solution in the worst implementation. Even with prefix information reducing validation, the number of candidate segments is still too large.

The important observation is that a valid segment must sit exactly across a boundary where the sushi type changes. Imagine compressing the array into consecutive groups of equal values. A segment can only take some suffix of one group and the same sized prefix of the next group. The maximum length using two neighboring groups is twice the smaller group size.

For example, if the groups are:

```
2 2 2 1 1 1 1
```

the two groups have lengths 3 and 4. We can take three `2`s and three `1`s, giving a segment of length 6. Taking four of the second group is impossible because there are not enough `2`s.

The whole problem becomes finding the maximum value among all adjacent group pairs.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) or worse | O(1) | Too slow |
| Group Compression | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Scan the array from left to right and count the length of every consecutive block of equal sushi types.
2. Store these block lengths in order. A block represents the largest possible contribution from one sushi type before the type changes.
3. For every pair of neighboring blocks, calculate `2 * min(left_block, right_block)`. This is the longest valid segment crossing this boundary because both halves must have the same length.
4. Keep the maximum value among all boundaries and print it.

The reason we only compare neighboring blocks is that a valid segment must contain exactly one transition between types. If there were two or more transitions, one of the halves would contain mixed sushi types.

Why it works:

Every valid segment has a left half of one type and a right half of the other type. The two halves meet at a point where the type changes, so they belong to two adjacent groups in the compressed representation. The segment length is limited by the smaller of those two groups because both halves need equal size. Checking all adjacent groups checks every possible valid segment.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    groups = []
    count = 1

    for i in range(1, n):
        if a[i] == a[i - 1]:
            count += 1
        else:
            groups.append(count)
            count = 1

    groups.append(count)

    ans = 0

    for i in range(len(groups) - 1):
        ans = max(ans, 2 * min(groups[i], groups[i + 1]))

    print(ans)

if __name__ == "__main__":
    solve()
```

The input is read as a single array because the entire algorithm only needs the order of sushi types. The `groups` list stores the lengths of consecutive equal values.

The first loop builds the compressed representation. Whenever the current sushi type differs from the previous one, the current group ends and its length is saved.

The final loop examines each possible boundary between two groups. Multiplying the smaller group length by two gives the largest balanced segment that can cross that boundary.

There are no overflow issues in Python because integers have arbitrary precision. The boundary handling is also simple because the loop only runs while a right neighbor exists.

## Worked Examples

Sample 1:

```
7
2 2 2 1 1 2 2
```

| Position | Current group length | Groups | Answer |
| --- | --- | --- | --- |
| 1 to 3 | 3 | [3] | 0 |
| 4 to 5 | 2 | [3, 2] | 4 |
| 6 to 7 | 2 | [3, 2, 2] | 4 |

The best boundary is between the first two groups. We can take two `2`s and two `1`s.

Sample 2:

```
9
2 2 1 1 1 2 2 2 2
```

| Position | Current group length | Groups | Answer |
| --- | --- | --- | --- |
| 1 to 2 | 2 | [2] | 0 |
| 3 to 5 | 3 | [2, 3] | 4 |
| 6 to 9 | 4 | [2, 3, 4] | 6 |

The middle boundary gives a segment of length 6 because the groups of length 3 and 4 can contribute three pieces each.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Every sushi piece is visited once while creating groups. |
| Space | O(n) | The compressed group list contains at most one entry per group. |

The linear complexity fits the input size because the algorithm avoids generating candidate subarrays and only processes the row once.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))

    groups = []
    cnt = 1

    for i in range(1, n):
        if a[i] == a[i - 1]:
            cnt += 1
        else:
            groups.append(cnt)
            cnt = 1

    groups.append(cnt)

    ans = 0
    for i in range(len(groups) - 1):
        ans = max(ans, 2 * min(groups[i], groups[i + 1]))

    return str(ans) + "\n"

assert run("7\n2 2 2 1 1 2 2\n") == "4\n", "sample 1"
assert run("9\n2 2 1 1 1 2 2 2 2\n") == "6\n", "sample 2"

assert run("2\n1 2\n") == "2\n", "minimum size"
assert run("5\n1 1 1 1 1\n") == "0\n", "all equal values"
assert run("6\n1 2 1 2 1 2\n") == "2\n", "alternating values"
assert run("8\n2 2 2 2 1 1 1 1\n") == "8\n", "large single boundary"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 / 1 2` | `2` | Smallest possible valid transition |
| `5 / 1 1 1 1 1` | `0` | No boundary exists |
| `6 / 1 2 1 2 1 2` | `2` | Alternating values cannot form a long segment |
| `8 / 2 2 2 2 1 1 1 1` | `8` | Entire array is one valid segment |

## Edge Cases

For an array where all sushi types are identical, there is no point where the type changes, so no valid segment can exist.

Example:

```
5
1 1 1 1 1
```

The algorithm creates one group:

```
[5]
```

There are no adjacent groups to compare, so the answer remains `0`.

For alternating sushi types:

```
6
1 2 1 2 1 2
```

The groups are:

```
[1, 1, 1, 1, 1, 1]
```

Every boundary can only create a segment of length `2 * min(1, 1)`, so the maximum is `2`. This prevents incorrectly treating equal counts of both types as enough.

For a case with one large boundary:

```
8
2 2 2 2 1 1 1 1
```

The groups are:

```
[4, 4]
```

The algorithm compares them and gets:

```
2 * min(4, 4) = 8
```

which is the whole array, because the two halves are both made from a single sushi type.
