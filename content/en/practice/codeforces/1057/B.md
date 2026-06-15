---
title: "CF 1057B - DDoS"
description: "We are given a timeline of server activity measured second by second. Each position in the array tells us how many requests arrived during that second. The task is to find a contiguous time window where the total number of requests is “too large” compared to its duration."
date: "2026-06-15T09:50:55+07:00"
tags: ["codeforces", "competitive-programming", "*special", "brute-force"]
categories: ["algorithms"]
codeforces_contest: 1057
codeforces_index: "B"
codeforces_contest_name: "Mail.Ru Cup 2018 - Practice Round"
rating: 1400
weight: 1057
solve_time_s: 548
verified: false
draft: false
---

[CF 1057B - DDoS](https://codeforces.com/problemset/problem/1057/B)

**Rating:** 1400  
**Tags:** *special, brute force  
**Solve time:** 9m 8s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a timeline of server activity measured second by second. Each position in the array tells us how many requests arrived during that second. The task is to find a contiguous time window where the total number of requests is “too large” compared to its duration. Concretely, a segment from time i to time j is considered suspicious if the sum of requests in that segment is strictly greater than 100 times the number of seconds in that segment.

The output is not the number of such segments or whether one exists, but the maximum possible length of a contiguous segment that satisfies this inequality. If no segment satisfies it at all, the answer is zero.

The constraint n up to 5000 immediately rules out any cubic solution. A triple nested enumeration over all segments and recomputing sums would still pass marginally in Python only with heavy optimization, but anything worse than O(n^2) will be too slow. This points us toward either a quadratic approach with prefix sums or a more clever linear technique.

A subtle edge case arises when all values are small. In such cases, no segment will ever exceed the threshold, and the correct answer is zero. Another edge case occurs when a single element already exceeds 100, in which case the answer is at least 1. A naive implementation that checks only total sums without properly subtracting segment length can incorrectly accept or reject such cases.

## Approaches

A direct way to solve the problem is to consider every possible segment [l, r], compute its sum, and compare it against 100 times its length. Using prefix sums, the sum of any segment can be computed in O(1), so checking all segments takes O(n^2). For n = 5000, this leads to about 25 million checks, which is acceptable in Python.

The brute-force works because it explicitly evaluates every candidate segment, but it becomes inefficient because it recomputes or checks too many overlapping intervals.

The key observation is that the condition depends only on the sum of a segment and its length. Prefix sums allow constant-time segment sum queries, eliminating repeated work. Since there is no monotonic structure that would allow binary search or sliding window, the clean quadratic enumeration is already optimal for this constraint.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^3) without prefix sums, O(n^2) with prefix sums | O(n) | Too slow in naive form, borderline but accepted with prefix sums |
| Optimal | O(n^2) | O(n) | Accepted |

## Algorithm Walkthrough

1. Build a prefix sum array where prefix[i] stores the total requests from day 1 to i. This allows fast computation of any segment sum. The reason this is useful is that every candidate segment must be evaluated against a sum condition.
2. Iterate over all possible left endpoints l from 1 to n. Each l defines the start of a candidate time window.
3. For each l, iterate over all possible right endpoints r from l to n. This enumerates every possible contiguous segment exactly once.
4. Compute the sum of the segment [l, r] using prefix sums as prefix[r] - prefix[l - 1]. This avoids recomputing sums from scratch.
5. Compute the length of the segment as r - l + 1, then check whether sum > 100 * length.
6. If the condition holds, update the answer with the maximum length seen so far.
7. After all iterations, return the best length, or 0 if none were valid.

### Why it works

Every valid segment is checked exactly once. Since we evaluate the condition directly for each segment using exact arithmetic, no approximation or heuristic is involved. The prefix sum ensures correctness of segment sums, and the nested iteration guarantees completeness over all possible contiguous intervals.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))

prefix = [0] * (n + 1)
for i in range(n):
    prefix[i + 1] = prefix[i] + a[i]

ans = 0

for l in range(n):
    for r in range(l, n):
        total = prefix[r + 1] - prefix[l]
        length = r - l + 1
        if total > 100 * length:
            if length > ans:
                ans = length

print(ans)
```

The solution relies entirely on prefix sums to make segment sum queries constant time. The outer loop fixes the start of a segment, and the inner loop expands the end. The comparison is done directly using the problem’s inequality, and the maximum valid length is tracked.

The only subtle point is indexing: prefix is built with one-based indexing so that segments starting at zero are handled cleanly as prefix[r+1] - prefix[l].

## Worked Examples

### Example 1

Input:

```
5
100 200 1 1 1
```

We compute prefix sums as:

prefix = [0, 100, 300, 301, 302, 303]

We check segments:

| l | r | sum | length | valid |
| --- | --- | --- | --- | --- |
| 0 | 0 | 100 | 1 | no |
| 0 | 1 | 300 | 2 | yes |
| 0 | 2 | 301 | 3 | yes |
| 0 | 3 | 302 | 4 | no |
| 1 | 1 | 200 | 1 | yes |
| 1 | 2 | 201 | 2 | yes |
| 2 | 4 | 3 | 3 | no |

The longest valid segment is [0, 2] with length 3.

This shows that extending a segment can eventually break the condition even if shorter prefixes satisfy it, so all endpoints must be checked explicitly.

### Example 2

Input:

```
4
0 0 0 0
```

All prefix sums are zero, so every segment has sum 0. Since 0 is never greater than 100 * length, no segment is valid. The answer is 0.

This confirms that the algorithm correctly handles the absence of any qualifying segment without producing a false positive.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2) | two nested loops over all segment endpoints, each check is O(1) using prefix sums |
| Space | O(n) | prefix sum array stores n+1 integers |

The quadratic complexity fits comfortably within limits for n up to 5000, since about 25 million iterations are acceptable in Python when each iteration is a constant-time arithmetic check.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))

    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + a[i]

    ans = 0
    for l in range(n):
        for r in range(l, n):
            total = prefix[r + 1] - prefix[l]
            length = r - l + 1
            if total > 100 * length:
                ans = max(ans, length)

    return str(ans)

# provided sample
assert run("5\n100 200 1 1 1\n") == "3"

# all zeros
assert run("4\n0 0 0 0\n") == "0"

# single large element
assert run("3\n0 0 500\n") == "1"

# no valid segment
assert run("3\n10 20 30\n") == "0"

# full valid segment
assert run("3\n200 200 200\n") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all zeros | 0 | no segment satisfies condition |
| single large element | 1 | minimal valid segment |
| increasing small values | 0 | ensures no false positives |
| all large values | full length | full range validity |

## Edge Cases

A critical edge case is when only single elements can satisfy the condition. For example, if the array contains a value like 150 among small values, only segments of length 1 centered on that element may be valid. The algorithm handles this naturally because it checks every (l, r) pair including r = l, so no special casing is needed.

Another case is when a segment starts valid but becomes invalid when extended. For instance, a prefix may have a high initial value followed by many small values that dilute the average. Since the algorithm does not assume monotonicity and explicitly checks all endpoints, it correctly captures the maximum valid length instead of greedily extending or stopping early.
