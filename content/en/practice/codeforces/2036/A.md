---
title: "CF 2036A - Quintomania"
description: "A melody here is just a short sequence of integer pitches. Each pitch is an integer between 0 and 127, and what matters is not the absolute values but the differences between neighboring notes."
date: "2026-06-08T10:19:06+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 2036
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 984 (Div. 3)"
rating: 800
weight: 2036
solve_time_s: 61
verified: true
draft: false
---

[CF 2036A - Quintomania](https://codeforces.com/problemset/problem/2036/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 1m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

A melody here is just a short sequence of integer pitches. Each pitch is an integer between 0 and 127, and what matters is not the absolute values but the differences between neighboring notes.

We are asked to check a simple structural property: for every adjacent pair in the sequence, the absolute difference of their values must be either 5 or 7. If every transition in the melody respects this rule, the melody is considered valid, otherwise it is rejected.

Each test case is independent, so the task is repeated checking over multiple small arrays. The size of each melody is small, at most 50 notes, and there are at most 1000 test cases, so even straightforward per-pair checking is comfortably fast.

There are no hidden transformations or global constraints. The only subtlety is remembering that the condition is on absolute difference, not signed difference. A transition like 10 to 17 and 17 to 10 are both valid since both yield difference 7.

A typical mistake in naive implementations is forgetting the absolute value or checking only one direction of the difference. Another issue arises when someone accidentally checks equality of consecutive notes instead of their difference.

Edge cases are mostly about minimal length. If a melody has exactly 2 notes, we only check one interval. For example, input `[1, 6]` is valid since the difference is 5, while `[1, 7]` is invalid since the difference is 6, which is not allowed.

## Approaches

The brute-force approach is almost identical to the definition. For each melody, iterate through all adjacent pairs and verify whether each difference is either 5 or 7. If any pair violates the condition, we immediately reject the melody.

Because each melody has at most 50 notes, this approach performs at most 49 comparisons per test case, and at most 1000 test cases, giving a worst-case of about 50,000 operations. This is already trivial, so there is no need for advanced optimization.

There is no real algorithmic trick hiding here. The key observation is simply that the condition is local: every constraint involves only two consecutive elements, so the whole problem reduces to a single pass validation. There is no dependency between different pairs beyond shared endpoints, so no dynamic programming or preprocessing is required.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(t·n) | O(1) | Accepted |
| Optimal | O(t·n) | O(1) | Accepted |

## Algorithm Walkthrough

We process each melody independently and validate it in a single pass.

1. Read the number of test cases. Each test case describes one melody.
2. For each melody, read the number of notes and the list of integers.
3. Iterate from the second note to the last note.
4. For each index i, compute the absolute difference between a[i] and a[i−1]. This captures the interval between consecutive notes regardless of direction.
5. Check whether this difference is exactly 5 or exactly 7. If not, immediately conclude that the melody is invalid.
6. If the loop finishes without finding a violation, the melody satisfies all constraints and is valid.

The key design choice is the early exit on failure. Once a single invalid interval is found, there is no need to continue scanning the rest of the sequence, since one violation is enough to invalidate the entire melody.

### Why it works

Every requirement in the problem is independent and local to adjacent pairs. The melody is valid if and only if all local constraints are satisfied. The algorithm directly enforces each constraint exactly once. Since no step modifies the sequence or depends on future decisions, there is no way for a valid sequence to be incorrectly rejected or an invalid one to be accepted.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))

    ok = True
    for i in range(1, n):
        diff = abs(a[i] - a[i - 1])
        if diff != 5 and diff != 7:
            ok = False
            break

    print("YES" if ok else "NO")
```

The solution is structured as a straightforward streaming validation. Each test case is processed independently, and we avoid storing anything beyond the current array.

The critical implementation detail is using `abs(a[i] - a[i - 1])`. Without the absolute value, negative differences would incorrectly pass or fail depending on sign. Another important detail is the early `break`, which ensures we stop as soon as we detect a violation.

## Worked Examples

### Example 1

Input:

```
3
3
76 83 88
3
10 15 22
4
1 6 1 6
```

| i | Pair | Difference | Valid so far |
| --- | --- | --- | --- |
| 1 | 76,83 | 7 | YES |
| 2 | 83,88 | 5 | YES |

Result: YES

| i | Pair | Difference | Valid so far |
| --- | --- | --- | --- |
| 1 | 10,15 | 5 | YES |
| 2 | 15,22 | 7 | YES |

Result: YES

| i | Pair | Difference | Valid so far |
| --- | --- | --- | --- |
| 1 | 1,6 | 5 | YES |
| 2 | 6,1 | 5 | YES |
| 3 | 1,6 | 5 | YES |

Result: YES

The first two examples confirm standard forward and mixed transitions, while the third shows that alternating back-and-forth movement is still valid as long as each step respects the allowed distances.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(∑n) | Each test case scans its melody once |
| Space | O(1) | Only a few variables besides input storage |

The total number of elements across all test cases is small enough that a single linear scan per case easily fits within time limits.

## Test Cases

```python
import sys, io

def solve():
    import sys
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        ok = True
        for i in range(1, n):
            d = abs(a[i] - a[i - 1])
            if d != 5 and d != 7:
                ok = False
                break

        out.append("YES" if ok else "NO")

    print("\n".join(out))

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    import io as _io
    buf = _io.StringIO()
    with redirect_stdout(buf):
        solve()
    return buf.getvalue().strip()

# provided samples
assert run("""8
2
114 109
2
17 10
3
76 83 88
8
38 45 38 80 85 92 99 106
5
63 58 65 58 65
8
117 124 48 53 48 43 54 49
5
95 102 107 114 121
10
72 77 82 75 70 75 68 75 68 75
""") == """YES
YES
YES
NO
YES
NO
YES
YES"""

# minimum length valid
assert run("""1
2
0 5
""") == "YES"

# minimum length invalid
assert run("""1
2
0 6
""") == "NO"

# alternating valid pattern
assert run("""1
4
0 5 0 5
""") == "YES"

# single violation in middle
assert run("""1
5
0 5 10 18 23
""") == "NO"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2→5→0→5 | YES | alternating valid steps |
| 0→6 | NO | single invalid edge |
| 0→5→10→18→23 | NO | mid-sequence violation propagation |

## Edge Cases

One edge case is the smallest possible melody length, n = 2. For example, input `0 5` should return YES because there is exactly one interval and it matches the rule. The algorithm handles this correctly because the loop runs once and validates that single difference.

Another case is a sequence that alternates directions but keeps valid step sizes, such as `0 5 0 5`. The differences are 5, 5, and 5, all valid, so the melody passes. The algorithm naturally supports this because it does not assume monotonic movement.

A failure case is when a single invalid transition appears in the middle. For instance `0 5 10 18` has differences 5, 5, and 8. At the step from 10 to 18, the difference is 8, which immediately triggers rejection. The early exit ensures we do not incorrectly continue and overlook the violation.
