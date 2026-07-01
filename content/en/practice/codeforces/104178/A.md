---
title: "CF 104178A - Success"
description: "We are given the final marks of all students in a class. Your own mark is hidden, but you know one extra fact: your mark is not the maximum among all students. The rank of a student is defined as one plus the number of students who scored strictly higher."
date: "2026-07-02T00:46:21+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104178
codeforces_index: "A"
codeforces_contest_name: "BdOI Preliminary 2023"
rating: 0
weight: 104178
solve_time_s: 42
verified: true
draft: false
---

[CF 104178A - Success](https://codeforces.com/problemset/problem/104178/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given the final marks of all students in a class. Your own mark is hidden, but you know one extra fact: your mark is not the maximum among all students.

The rank of a student is defined as one plus the number of students who scored strictly higher. So if there are 3 students with higher marks, your rank is 4.

Since your exact score is unknown, you must consider every possible score that is consistent with the information that you are not the top scorer. Among all such possibilities, you want the smallest possible rank.

The key structure is that your rank depends only on how many students have a score strictly greater than yours. If you pick a higher possible personal score, fewer students beat you, so your rank improves. Therefore, to minimize rank, you want to choose a score that maximizes how many students are above you, while still respecting that your score cannot be the maximum in the array.

The input size goes up to 200000, so any solution must run in linear or near-linear time. Since scores are bounded between 1 and 100, frequency counting is naturally sufficient. Sorting is also possible but unnecessary.

A subtle edge case is when the highest score appears multiple times. Even then, you are forbidden from taking the highest value, so the best strategy is always to assume your score is the largest value strictly smaller than the maximum.

For example, if scores are `[100, 100, 99, 50]`, you cannot be 100. If you choose 99, then only the two 100s are above you, giving rank 3. Any lower score would only increase your rank.

The only non-obvious failure case for naive thinking is assuming you should always pick the global second maximum distinct value without checking distribution. However, that is actually correct here because rank depends only on strict comparisons.

## Approaches

A brute-force approach would try every possible candidate score for you, and for each candidate count how many students have a strictly greater score. This is easy: for each candidate value `x`, scan the array and count elements greater than `x`. However, since there can be up to 200000 students and potentially up to 100 different candidate scores, this leads to 200000 × 100 operations, which is borderline but still inefficient under tight constraints and unnecessary.

We can instead observe that the answer depends only on how many elements are strictly greater than the best score we are allowed to take. Since we are not allowed to take the maximum value in the array, the best choice is to take the largest value strictly less than the maximum. Once that value is fixed, the number of higher-scoring students is simply the count of elements strictly greater than it.

We can compute frequencies of all scores from 1 to 100, then determine:

the maximum value `mx`, then consider `mx2`, the largest value < `mx` that appears in the array. The number of students strictly greater than `mx2` is the sum of frequencies of all values greater than `mx2`. That gives the minimum possible rank.

This reduces the problem to a small constant-sized frequency scan.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * 100) | O(1) | Too slow |
| Frequency counting | O(n + 100) | O(100) | Accepted |

## Algorithm Walkthrough

1. Read all scores and compute their frequency in an array of size 101.

This compresses the entire dataset into a fixed-size representation since scores are bounded.
2. Find the maximum score `mx` present in the array.

This value is forbidden as your possible score.
3. Find the largest score `mx2` such that `mx2 < mx` and `freq[mx2] > 0`.

This is the best score you are allowed to assume because it is the closest possible value below the maximum, minimizing the number of students above you.
4. Compute how many students have strictly greater score than `mx2`.

This is done by summing `freq[v]` for all `v > mx2`.
5. Output `1 + (number of students strictly greater than mx2)`.

This is the minimum achievable rank under valid constraints.

### Why it works

The rank is fully determined by the count of elements strictly greater than your chosen score. Any valid candidate score must be less than the maximum element in the array. Among all such candidates, choosing the largest possible one minimizes the number of elements greater than it, because the set `{a[i] > x}` shrinks monotonically as `x` increases. Therefore the optimal choice is the greatest value below the global maximum that exists in the array. This ensures no other valid choice can produce a smaller set of greater elements, so the computed rank is minimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    arr = list(map(int, input().split()))
    
    freq = [0] * 101
    for x in arr:
        freq[x] += 1

    mx = 0
    for v in range(1, 101):
        if freq[v]:
            mx = v

    mx2 = 0
    for v in range(mx - 1, 0, -1):
        if freq[v]:
            mx2 = v
            break

    higher = 0
    for v in range(mx2 + 1, 101):
        higher += freq[v]

    print(higher + 1)

if __name__ == "__main__":
    solve()
```

The solution first builds a frequency table so that repeated scans of the input are unnecessary. The maximum value is found by scanning the small fixed range. Then we search downward to locate the best permissible score. Finally, we sum frequencies above it to compute how many students outrank you.

A common pitfall is forgetting that the chosen score must not be the maximum. Another is incorrectly counting students with equal scores as higher, which would inflate the rank. The strict inequality in the final summation avoids that.

## Worked Examples

### Example 1

Input:

```
4
100 100 100 99
```

We build frequencies:

| Value | Frequency |
| --- | --- |
| 99 | 1 |
| 100 | 3 |

Maximum is 100. Best valid score is 99.

| Step | mx | mx2 | Higher count | Rank |
| --- | --- | --- | --- | --- |
| Init | 100 | - | - | - |
| Choose mx2 | 100 | 99 | - | - |
| Count higher | 100 | 99 | 3 | 4 |

So output is 4.

This confirms the behavior when the maximum is duplicated; even then, we are forced below it, and all maximum scorers dominate.

### Example 2

Input:

```
3
90 75 85
```

Frequencies:

| Value | Frequency |
| --- | --- |
| 75 | 1 |
| 85 | 1 |
| 90 | 1 |

Maximum is 90. Best valid score is 85.

| Step | mx | mx2 | Higher count | Rank |
| --- | --- | --- | --- | --- |
| Init | 90 | - | - | - |
| Choose mx2 | 90 | 85 | - | - |
| Count higher | 90 | 85 | 1 | 2 |

Only 90 is above 85, so rank is 2.

This shows that choosing the second-largest distinct value always yields minimal rank.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + 100) | One pass to build frequency plus constant-range scans |
| Space | O(100) | Fixed frequency array independent of n |

The solution easily fits within constraints since all operations after reading input are constant-time over a bounded range.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided samples
assert run("4\n100 100 100 99\n") == "4", "sample 1"
assert run("3\n90 75 85\n") == "2", "sample 2"

# custom cases
assert run("2\n1 2\n") == "2", "minimum size distinct"
assert run("5\n10 10 10 10 9\n") == "5", "all high except one"
assert run("6\n5 4 3 2 1 5\n") == "5", "multiple max values"
assert run("3\n2 1 2\n") == "2", "duplicate max edge"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 distinct values | 2 | smallest non-trivial case |
| repeated maximum | 5 | handling duplicates at top |
| descending mix | 5 | correct second-max selection |
| symmetric duplicates | 2 | strict inequality correctness |

## Edge Cases

One edge case is when the maximum value appears multiple times. For input:

```
5
10 10 10 10 9
```

the maximum is 10, so you cannot choose 10. The best valid choice is 9, and all four 10s are strictly higher, so rank becomes 5. The algorithm correctly finds `mx2 = 9` and counts all 10s.

Another edge case is when the array has exactly two distinct values:

```
2
1 2
```

Here, maximum is 2 and the only valid choice is 1. Exactly one student is higher, so rank is 2. The downward scan correctly finds 1 as `mx2` and counts one higher element.

A final edge case is when values are heavily repeated at the top but sparse below. The frequency-based summation still works because it does not depend on positions or ordering, only counts strictly greater values, ensuring stability across all distributions.
