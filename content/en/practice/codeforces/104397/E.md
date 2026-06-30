---
title: "CF 104397E - Course Selection"
description: "Each test case describes a student’s selected set of courses, where every course belongs to one of several categories and contributes a small integer number of credits."
date: "2026-06-30T23:08:48+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104397
codeforces_index: "E"
codeforces_contest_name: "The 21st UESTC Programming Contest Final"
rating: 0
weight: 104397
solve_time_s: 84
verified: false
draft: false
---

[CF 104397E - Course Selection](https://codeforces.com/problemset/problem/104397/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 24s  
**Verified:** no  

## Solution
## Problem Understanding

Each test case describes a student’s selected set of courses, where every course belongs to one of several categories and contributes a small integer number of credits. The goal is to verify whether this selection satisfies a collection of graduation requirements that impose lower bounds on different credit groupings.

For every test case, we are given global thresholds for total credits, total coursework credits, compulsory session credits, degree course credits, and several constraints that further split degree and professional courses into finer subcategories. Then we are given a list of courses, each with a name, a category label, and its credit value. The task is simply to decide whether the sums of credits across the relevant categories meet all required minimums, including the additional requirement that at least one public foundational course must be present.

The constraints are deliberately small: at most 100 test cases, each with at most 100 courses, and each course has at most 10 credits. This immediately rules out anything beyond linear processing per test case. A single pass accumulating category totals is sufficient, since even an O(n²) approach would be unnecessary but still technically passable. The structure of the problem is not algorithmically complex, but correctness depends on carefully separating overlapping categories and not double counting or misclassifying any course.

A subtle issue arises from the fact that categories overlap conceptually. For example, professional courses include both professional foundational and professional elective courses, and degree courses include public foundational plus professional foundational. A naive mistake is to treat these as disjoint or to forget that some requirements are nested sums over multiple categories.

Another easy mistake is forgetting the “at least one public foundational course” requirement. For example:

Input:

```
a b c d e f g = 10 8 2 5 5 2 2
n = 2
Course1: professional foundational, 6 credits
Course2: professional elective, 4 credits
```

Even if all numeric inequalities are satisfied, the answer must be NO because there is no public foundational course.

This kind of failure does not show up in sum-based checks unless the category presence constraint is explicitly tracked.

## Approaches

The brute-force view is to simulate all requirements directly from the list of courses. For each requirement, we recompute the relevant sum by scanning all courses and checking their category. Since there are only a constant number of requirements, this is already straightforward, but even then it repeats work unnecessarily. In the worst case, for each of the constant number of constraints we traverse up to 100 courses, resulting in around 10⁴ operations per test case, which is still trivial under the limits.

However, this repetition is unnecessary because every constraint depends only on a few fixed aggregates: totals per category and overall sums. The key observation is that every course contributes independently to a small set of accumulators. Once we classify each course exactly once, all required checks reduce to constant-time comparisons.

So instead of repeatedly scanning the list, we maintain running totals for total credits, compulsory sessions, public foundational, professional foundational, professional elective, and other elective categories. From these we derive degree course credits and professional course credits directly by summation.

This reduces the entire problem to a single pass aggregation per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Re-scan per constraint | O(T · n · k) | O(n) | Accepted but redundant |
| Single-pass aggregation | O(T · n) | O(1) | Accepted |

## Algorithm Walkthrough

We process each test case independently and reduce the course list into a few counters.

1. Initialize all counters to zero. These include total credits, course credits, compulsory session credits, public foundational credits, professional foundational credits, professional elective credits, and other elective credits. We also maintain a boolean flag indicating whether at least one public foundational course appears.
2. Read each course one by one. For every course, add its credit value to the total credit counter. This ensures we can later check the global requirement without revisiting the list.
3. If the course is a compulsory session, add its credits to the compulsory counter. This isolates non-academic session requirements from coursework requirements.
4. If the course is a public foundational course, increment its dedicated counter and mark the boolean flag as true. This flag is necessary because the requirement is not numeric alone but requires existence of at least one such course.
5. If the course is a professional foundational course, add its credits to both the professional foundational counter and also to the broader professional course grouping.
6. If the course is a professional elective course, add its credits to the professional elective counter and also to the professional course grouping.
7. If the course is an interdisciplinary elective or other elective course, it contributes only to total credits and course credits but not to professional or degree-specific aggregates.
8. After processing all courses, compute derived totals: course credits equal total credits minus compulsory session credits, degree course credits equal public foundational plus professional foundational credits, and professional course credits equal professional foundational plus professional elective credits.
9. Finally, verify all constraints simultaneously. If any condition fails, output NO; otherwise output YES.

The correctness comes from the fact that every course is classified exactly once, and each requirement is expressed purely as a sum over disjoint or intentionally overlapping groups. Since all group definitions are faithfully accumulated during a single pass, no constraint can be miscomputed later.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    T = int(input())
    for _ in range(T):
        a, b, c, d, e, f, g = map(int, input().split())
        n = int(input())

        total = 0
        compulsory = 0

        pub = 0
        prof_f = 0
        prof_e = 0

        for _ in range(n):
            name = input().rstrip()
            typ = input().rstrip()
            val = int(input())

            total += val

            if typ == "compulsory sessions":
                compulsory += val
            elif typ == "public foundational courses":
                pub += val
            elif typ == "professional foundational courses":
                prof_f += val
            elif typ == "professional elective courses":
                prof_e += val

        course = total - compulsory
        degree = pub + prof_f
        prof = prof_f + prof_e

        ok = True
        ok &= total >= a
        ok &= course >= b
        ok &= compulsory >= c
        ok &= degree >= d
        ok &= prof >= e
        ok &= prof_f >= f
        ok &= prof_e >= g
        ok &= pub > 0

        print("YES" if ok else "NO")

if __name__ == "__main__":
    solve()
```

The implementation mirrors the aggregation strategy directly. Each course is read exactly once and immediately contributes to the relevant counters. The only subtle part is ensuring that “course credits” excludes compulsory sessions, which is handled explicitly by subtracting compulsory from total at the end. The public foundational requirement is enforced using a separate flag via `pub > 0`, since it is not just a sum constraint in spirit but an existence constraint.

## Worked Examples

Consider a simplified example.

Input:

```
1
10 8 2 5 5 2 2
3
A
public foundational courses
3
B
professional foundational courses
4
C
compulsory sessions
2
```

| Step | total | compulsory | pub | prof_f | prof_e | degree | course |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A | 3 | 0 | 3 | 0 | 0 | 3 | 3 |
| B | 7 | 0 | 3 | 4 | 0 | 7 | 7 |
| C | 9 | 2 | 3 | 4 | 0 | 7 | 7 |

After processing all courses, total credits are 9, course credits are 7, compulsory credits are 2, degree credits are 7, professional credits are 4, professional foundational is 4, and professional elective is 0.

The final check fails the total credit requirement since 9 is less than 10, so the output is NO.

This trace shows that all constraints are evaluated independently and only the final comparison decides validity.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(T · n) | Each course is processed exactly once with constant-time updates |
| Space | O(1) | Only a fixed number of counters are maintained |

The constraints cap both T and n at 100, so the total number of operations is at most 10,000 per run, which is comfortably within limits.

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
        a, b, c, d, e, f, g = map(int, input().split())
        n = int(input())

        total = 0
        compulsory = 0
        pub = 0
        prof_f = 0
        prof_e = 0

        for _ in range(n):
            name = input().rstrip()
            typ = input().rstrip()
            val = int(input())

            total += val
            if typ == "compulsory sessions":
                compulsory += val
            elif typ == "public foundational courses":
                pub += val
            elif typ == "professional foundational courses":
                prof_f += val
            elif typ == "professional elective courses":
                prof_e += val

        course = total - compulsory
        degree = pub + prof_f
        prof = prof_f + prof_e

        ok = (
            total >= a and
            course >= b and
            compulsory >= c and
            degree >= d and
            prof >= e and
            prof_f >= f and
            prof_e >= g and
            pub > 0
        )

        out.append("YES" if ok else "NO")

    return "\n".join(out)

# provided sample
assert run("""1
28 24 4 15 15 6 7
15
Socialism with Chinese Characteristics
public foundational courses
2
Matrix Theory
professional foundational courses
3
Optimization Theory
professional foundational courses
3
Communication Network Theory
professional elective courses
2
Bayesian Learning and Random Matrix
professional elective courses
2
Image and Video Processing
professional foundational courses
2
Graph Theory
professional foundational courses
3
Machine Learning
professional elective courses
2
Visual Data Analysis
professional elective courses
2
Guidance on Writing Graduate Thesis
other elective courses
1
Graduate English
public foundational courses
3
Teaching Practice
compulsory sessions
1
Academic Activities
compulsory sessions
1
General Education Elective Courses
compulsory sessions
1
Academic Exchange
compulsory sessions
1
""") == "YES"

# custom: missing public foundational
assert run("""1
10 5 0 5 5 2 2
2
A
professional foundational courses
5
B
professional elective courses
5
""") == "NO"

# custom: all constraints satisfied minimal
assert run("""1
5 3 0 2 2 1 1
2
A
public foundational courses
2
B
professional elective courses
3
""") == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| sample | YES | full constraint satisfaction |
| missing public foundational | NO | existence constraint handling |
| minimal valid case | YES | correct aggregation and thresholds |

## Edge Cases

A key edge case is when all numeric constraints are satisfied but no public foundational course exists. In such a case, the aggregated sums look correct, but the boolean requirement fails. The algorithm handles this explicitly through the `pub > 0` check, so the final decision correctly becomes NO.

Another edge case is when compulsory sessions dominate total credits. Since course credits exclude compulsory sessions, it is possible for total ≥ a to hold while course ≥ b fails. The subtraction `course = total - compulsory` ensures this distinction is preserved exactly as required.

A final edge case is when multiple categories overlap conceptually but not operationally, such as professional foundational courses contributing to both degree and professional totals. Because both accumulators are updated at the same time, no double counting or omission occurs, and the derived sums remain consistent across all constraints.
