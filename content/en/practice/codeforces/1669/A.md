---
title: "CF 1669A - Division?"
description: "Each test case gives a single integer representing a Codeforces user rating, and the task is to classify that rating into one of four fixed intervals, each corresponding to a division number. The mapping is purely threshold-based."
date: "2026-06-10T01:54:56+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1669
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 784 (Div. 4)"
rating: 800
weight: 1669
solve_time_s: 93
verified: true
draft: false
---

[CF 1669A - Division?](https://codeforces.com/problemset/problem/1669/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 1m 33s  
**Verified:** yes  

## Solution
## Problem Understanding

Each test case gives a single integer representing a Codeforces user rating, and the task is to classify that rating into one of four fixed intervals, each corresponding to a division number.

The mapping is purely threshold-based. Very low ratings, including negatives, fall into Division 4. As the rating increases, it crosses two intermediate bands before reaching Division 1 for the highest ratings. The output is not a computation but a label derived from where the number lies in this ordered partition of the integer line.

The constraints are large in terms of number of test cases, up to ten thousand. Each test case is independent and requires only a constant amount of work, so the only viable solutions are those that process each input in O(1) time. Anything involving sorting or repeated scanning would be unnecessary overhead but still technically possible within constraints; however, it would be conceptually mismatched and slower than needed.

The only subtlety in this problem comes from boundary handling. The division boundaries are inclusive, so values exactly equal to 1400, 1600, and 1900 must be placed in the higher division bands correctly. A typical mistake is using strict inequalities inconsistently, which can shift boundary values into the wrong division. For example, treating 1400 as Division 4 because of a `< 1400` check instead of `<= 1399` leads to incorrect classification.

## Approaches

A brute-force interpretation would be to explicitly check each division interval in sequence and test membership. Since there are only four ranges, even a naive approach remains constant time per test case. One could imagine storing ranges as pairs and iterating through them, checking whether the rating falls into each interval. This works correctly because the number of intervals is fixed and small, so the worst-case work per test case is still constant.

However, the structure of the problem is simpler than general interval membership. The intervals are contiguous and ordered on the number line, so we do not need iteration or data structures at all. A direct chain of comparisons from lowest threshold to highest is sufficient. Once we detect the correct band, we can immediately return the corresponding division label.

The key observation is that the rating space is partitioned into four monotonic regions defined by three cut points: 1400, 1600, and 1900. This turns the problem into a simple threshold classification problem, where we only need to compare against these cutoffs in increasing order.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (interval scan) | O(1) per test case | O(1) | Accepted |
| Optimal (threshold checks) | O(1) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases. This determines how many independent classifications we will perform.
2. For each rating, compare it against the smallest threshold that defines the top division. If the rating is at least 1900, it must belong to Division 1 because no higher boundary exists.
3. If the rating is below 1900, check whether it is at least 1600. If so, it lies in the second-highest band, since it is guaranteed not to reach Division 1.
4. If the rating is below 1600, check whether it is at least 1400. This identifies the third band, since higher possibilities have already been excluded.
5. If none of the above conditions are met, the rating must be at most 1399, placing it in Division 4.

The ordering of checks matters because each condition eliminates a prefix of the number line. Once a condition succeeds, later checks are irrelevant and must not override the decision.

### Why it works

The rating line is partitioned into four disjoint intervals whose union covers all integers. Each conditional check corresponds to membership in one of these intervals after excluding higher ones. Because the checks proceed from highest threshold to lowest, every rating is assigned to exactly one division, and no overlap or gap is possible due to the inclusive boundary definitions.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    r = int(input())
    
    if r >= 1900:
        print("Division 1")
    elif r >= 1600:
        print("Division 2")
    elif r >= 1400:
        print("Division 3")
    else:
        print("Division 4")
```

The solution reads each rating independently and applies a fixed sequence of comparisons. The first condition handles the top interval, and each subsequent branch handles the next lower range only after excluding all higher ones. This ensures correctness without needing to explicitly encode interval endpoints.

A common mistake is reversing the order of checks, for example testing `r >= 1400` first. That would incorrectly classify all higher ratings into Division 3 or lower unless carefully guarded. The descending order prevents such misclassification.

## Worked Examples

We trace the classification logic on the sample input.

### Example 1

Input:

```
-789
1299
1300
1399
1400
1679
2300
```

| Rating | r ≥ 1900 | r ≥ 1600 | r ≥ 1400 | Output |
| --- | --- | --- | --- | --- |
| -789 | No | No | No | Division 4 |
| 1299 | No | No | No | Division 4 |
| 1300 | No | No | No | Division 4 |
| 1399 | No | No | No | Division 4 |
| 1400 | No | No | Yes | Division 3 |
| 1679 | No | Yes | - | Division 2 |
| 2300 | Yes | - | - | Division 1 |

This trace shows how each rating is filtered down through the thresholds until exactly one branch applies. It also highlights why the order of checks prevents ambiguity at boundary values like 1400 and 1600.

### Example 2

Input:

```
4
1600
1599
1900
-5000
```

| Rating | r ≥ 1900 | r ≥ 1600 | r ≥ 1400 | Output |
| --- | --- | --- | --- | --- |
| 1600 | No | Yes | - | Division 2 |
| 1599 | No | No | Yes | Division 3 |
| 1900 | Yes | - | - | Division 1 |
| -5000 | No | No | No | Division 4 |

This example focuses on boundary-adjacent values, confirming that equality at thresholds is handled correctly due to inclusive comparisons.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case requires a constant number of comparisons and one output. |
| Space | O(1) | No auxiliary data structures are used beyond variables for input parsing. |

The solution scales linearly with the number of test cases, which is optimal because each rating must be read and classified at least once. With up to 10,000 cases, this easily fits within time limits in Python.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        r = int(input())
        if r >= 1900:
            out.append("Division 1")
        elif r >= 1600:
            out.append("Division 2")
        elif r >= 1400:
            out.append("Division 3")
        else:
            out.append("Division 4")
    return "\n".join(out) + "\n"

# provided sample
assert run("""7
-789
1299
1300
1399
1400
1679
2300
""") == """Division 4
Division 4
Division 4
Division 4
Division 3
Division 2
Division 1
"""

# minimum value
assert run("""1
-5000
""") == "Division 4\n"

# boundary checks
assert run("""3
1399
1400
1599
""") == """Division 4
Division 3
Division 3
"""

# higher boundaries
assert run("""3
1600
1899
1900
""") == """Division 2
Division 2
Division 1
"""

# mixed values
assert run("""4
0
1000
2000
1800
""") == """Division 4
Division 4
Division 1
Division 2
"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| -5000 | Division 4 | minimum boundary handling |
| 1399 / 1400 / 1599 | D4 / D3 / D3 | lower and middle boundary correctness |
| 1600 / 1899 / 1900 | D2 / D2 / D1 | upper boundary correctness |
| mixed values | varied | general correctness across all bands |

## Edge Cases

Negative ratings demonstrate that the lowest band extends beyond zero into unbounded negatives. For an input like `-1`, the checks `r >= 1900`, `r >= 1600`, and `r >= 1400` all fail, leaving Division 4 as the correct classification. The algorithm naturally handles this because the final else branch captures everything not covered by higher thresholds.

Boundary values such as 1400, 1600, and 1900 are critical because they sit exactly on division transitions. For example, 1400 must pass the `r >= 1400` check, ensuring Division 3, while 1399 fails all higher checks and falls into Division 4. The strict ordering of conditions guarantees correct placement without requiring explicit interval endpoints.
