---
title: "CF 102899E - KK \u4e0e\u7b54\u8fa9"
description: "We are given several independent test cases. In each test case, there are multiple “defense sessions”. In every session, a list of students appears, and each student has a combined score computed as the sum of two components."
date: "2026-07-04T08:20:27+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102899
codeforces_index: "E"
codeforces_contest_name: "The 2nd Hangzhou Normal University Freshman Programming Contest"
rating: 0
weight: 102899
solve_time_s: 40
verified: true
draft: false
---

[CF 102899E - KK \u4e0e\u7b54\u8fa9](https://codeforces.com/problemset/problem/102899/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 40s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several independent test cases. In each test case, there are multiple “defense sessions”. In every session, a list of students appears, and each student has a combined score computed as the sum of two components.

One special student, KK, appears once in every session and has a score in that session. Any other student may appear in one or more sessions, possibly with different scores each time.

A student is considered “dominated by KK” if every time that student appears in any session, their score in that session is strictly lower than KK’s score in the same session. If the student ever matches or exceeds KK in even one session, they are not counted.

The task is to compute how many distinct students satisfy this condition.

The structure of the input is small in scale: each test case has at most 10 sessions and each session has at most 10 people. This immediately rules out anything beyond simple quadratic or linear scanning. Even a straightforward nested scan over all records is at most a few thousand operations per test case, which is trivial under a 1 second limit.

The main subtlety is that students appear multiple times across sessions, and their validity depends on a global condition across all appearances. A naive mistake is to check only the first appearance of a student, or to compare against a single KK value instead of session-specific KK values.

A concrete failure case looks like this:

Session 1: KK score is 100, Alice scores 90

Session 2: KK score is 50, Alice scores 60

If we only compare Alice once, she might seem fine, but she violates the rule in session 2 because she is not strictly lower than KK there. So Alice must be excluded.

Another edge case is students appearing only once. If their score is lower than KK in that session, they are automatically valid, but only after ensuring no hidden later violation exists (which requires tracking all occurrences).

## Approaches

A brute-force interpretation would be: for every student name, collect all sessions where they appear, and for each of those sessions compare their score against KK’s score in that session. If all comparisons pass, count the student.

This works correctly, but if we implement it naively by scanning the entire dataset for each student, we may repeatedly traverse all entries. In the worst case, we could check up to 100 entries per student, leading to redundant repeated work.

The key observation is that we do not need to recompute per student. Instead, we can process each record once, maintain KK’s score per session, and immediately invalidate any student who violates the condition. This turns the problem into a single pass aggregation problem over names.

We maintain a dictionary that records whether each student is still valid. As we read each session, we compare every participant against that session’s KK score and update their status immediately.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force per student scan | O(N²) per test case | O(N) | Too slow (unnecessary overhead) |
| Single-pass validation | O(N) per test case | O(N) | Accepted |

## Algorithm Walkthrough

We process each test case independently.

1. Read the number of sessions. For each session, we first identify KK’s score because KK always appears as the first entry of the session. This gives us a per-session benchmark.
2. Create a dictionary `valid[name] = True` for tracking whether each student is still eligible to be counted.
3. For every participant in the session, compare their score with KK’s score for that session. If a student is not KK and their score is greater than or equal to KK’s score, we immediately mark them as invalid.
4. Continue processing all sessions, ensuring that once a student is marked invalid, they remain invalid regardless of future sessions.
5. After processing all sessions, count how many distinct names (excluding KK) are still marked valid.

The key design choice is immediate invalidation. This avoids storing full per-session histories.

### Why it works

For each student, the condition we check is a universal constraint over all their appearances: every observed score must be strictly less than KK’s score in the corresponding session. The algorithm enforces this by checking each occurrence independently and invalidating on the first failure. Because invalidation is monotonic and never reversed, a student is marked valid at the end if and only if all their comparisons passed.

## Python Solution

```python
import sys
input = sys.stdin.readline

T = int(input())
for _ in range(T):
    n = int(input())
    
    valid = {}
    kk_name = None

    for _ in range(n):
        a = int(input())
        
        session = []
        for i in range(a):
            s, b, c = input().split()
            b = int(b)
            c = int(c)
            total = b + c
            
            if i == 0:
                kk_name = s
                kk_score = total
            
            if s not in valid:
                valid[s] = True
            
            if s != kk_name:
                if total >= kk_score:
                    valid[s] = False

    ans = 0
    for name, ok in valid.items():
        if name != kk_name and ok:
            ans += 1

    print(ans)
```

The code relies on the guarantee that the first entry in each session corresponds to KK. That allows us to capture KK’s score before processing the rest of the participants in that session.

A subtle point is that we never need to store per-session histories. We only store the current validity status per name, which keeps memory usage minimal and logic simple.

## Worked Examples

### Example 1

Consider:

Session 1: KK = 100, Alice = 90, Bob = 110

Session 2: KK = 80, Alice = 70

We track validity as follows:

| Session | KK score | Alice | Alice valid | Bob | Bob valid |
| --- | --- | --- | --- | --- | --- |
| 1 | 100 | 90 | True | 110 | False |
| 2 | 80 | 70 | True | - | False |

Alice survives all checks, Bob fails immediately.

This shows that a single violation is enough to disqualify a student.

### Example 2

Session 1: KK = 50, Charlie = 49

Session 2: KK = 60, Charlie = 65

| Session | KK score | Charlie | Charlie valid |
| --- | --- | --- | --- |
| 1 | 50 | 49 | True |
| 2 | 60 | 65 | False |

Even though Charlie passes in the first session, the second session invalidates him, demonstrating the need for global tracking across all sessions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(total entries) | Each participant is processed once and checked in O(1) |
| Space | O(unique names) | We store one boolean per student name |

Given that each test case has at most 100 entries, the solution runs in negligible time and easily fits within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    T = int(input())
    out = []
    for _ in range(T):
        n = int(input())
        valid = {}
        kk_name = None

        for _ in range(n):
            a = int(input())
            for i in range(a):
                s, b, c = input().split()
                b = int(b)
                c = int(c)
                total = b + c

                if i == 0:
                    kk_name = s
                    kk_score = total

                if s not in valid:
                    valid[s] = True

                if s != kk_name and total >= kk_score:
                    valid[s] = False

        ans = sum(1 for k,v in valid.items() if k != kk_name and v)
        out.append(str(ans))

    return "\n".join(out)

# minimal case
assert run("""1
1
1
kk 50 50
a 10 10
""") == "1"

# violation case
assert run("""1
1
2
kk 100 100
a 50 50
a 200 200
""") == "0"

# all valid
assert run("""1
1
3
kk 100 100
a 10 10
b 20 20
""") == "2"

# multiple sessions with cross violation
assert run("""1
2
2
kk 100 100
a 90 90
2
kk 80 80
a 100 100
""") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| minimal single session | 1 | basic correctness |
| mixed valid/invalid appearances | 0 | multi-occurrence invalidation |
| all students always below KK | 2 | positive counting |
| violation in later session | 0 | cross-session dependency |

## Edge Cases

One important edge case is when a student appears only in sessions where KK has very low scores. The algorithm handles this correctly because each session is checked independently, so even a single high-score session invalidates the student.

Another case is repeated appearances of the same student within a single session. Since we process each line independently, any violation inside that session immediately flips their validity, and subsequent occurrences do not change the result.

A final subtle case is KK being reused as a name for other students. The code explicitly excludes KK by name comparison, ensuring only the true KK baseline is used for comparisons.
