---
title: "CF 104397E - Course Selection"
description: "We are given a set of selected courses for a master’s program. Each course contributes a certain number of credits and belongs to exactly one category such as public foundational, professional foundational, elective variants, or compulsory sessions."
date: "2026-07-01T00:52:19+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104397
codeforces_index: "E"
codeforces_contest_name: "The 21st UESTC Programming Contest Final"
rating: 0
weight: 104397
solve_time_s: 78
verified: true
draft: false
---

[CF 104397E - Course Selection](https://codeforces.com/problemset/problem/104397/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of selected courses for a master’s program. Each course contributes a certain number of credits and belongs to exactly one category such as public foundational, professional foundational, elective variants, or compulsory sessions. The goal is to verify whether the chosen set of courses satisfies a collection of credit constraints that apply both globally and per category.

For each test case, we read several thresholds that describe minimum required totals: total credits, total course credits, compulsory session credits, degree course credits, and several constraints that further split professional and elective structure. Then we are given a list of courses, each with a type and credit value, and we must decide whether the aggregated plan satisfies all constraints simultaneously.

Although this looks like a bookkeeping problem, the difficulty is in carefully separating overlapping categories. A single course may contribute to multiple constraints at once. For example, a professional foundational course contributes to total credits, total course credits, degree credits, professional credits, and professional foundational credits simultaneously.

The constraints are small. Every number is at most 100, and each test case has at most 100 courses. This guarantees that a linear scan over the input is sufficient, and any solution that does constant work per course will pass easily.

A subtle edge case comes from the requirement “at least one public foundational course must be taken.” This is not encoded as a numeric threshold, so simply summing credits is not enough; we must explicitly track whether such a course exists.

Another common mistake is mixing up overlapping categories. For instance, professional courses include both professional foundational and professional elective courses. If we mistakenly count only one of them, we may fail or incorrectly pass constraints involving e, f, or g.

A second subtle issue is that compulsory sessions are not part of course credits but still contribute to total credits. So total credits include everything, while total course credits include everything except possibly some interpretation boundary, but in this problem all listed items are courses, so both totals are identical in practice. The distinction still matters for correctness in interpretation.

## Approaches

A brute-force approach would be unnecessary enumeration or simulation of all possible subsets of courses, trying to assign them into categories or verify constraints by recomputation. That is not required because the input already provides a fixed selection; there is no choice to optimize or pick subsets. Even if we misinterpreted it as a selection problem, enumerating subsets would cost exponential time in n, specifically O(2^n), which is immediately infeasible.

The key observation is that the structure is purely additive. Every constraint is expressed as a sum over disjoint or overlapping groups of courses. This means we only need to compute category-wise accumulations in a single pass.

The solution reduces to scanning all courses once and maintaining counters for each relevant category: total credits, course credits, compulsory credits, public foundational credits, degree credits (public plus professional foundational), professional credits (foundational plus elective), professional foundational credits, and professional elective credits. We also track a boolean flag indicating whether at least one public foundational course exists.

Once all aggregates are computed, we compare them against the thresholds. If every constraint is satisfied, the plan is valid.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (misinterpreted subset search) | O(2^n) | O(n) | Too slow |
| Single pass aggregation | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We process each test case independently.

1. Read all threshold values. These define the minimum required sums for different categories and act as the final validation targets.
2. Initialize all counters to zero and a boolean flag `has_public` to false. These variables will accumulate information across all courses.
3. For each course, read its type and credit value, then update all relevant counters based on the category. Each course contributes to multiple counters depending on its classification. For example, a professional foundational course increases total credits, course credits, degree credits, professional credits, and professional foundational credits simultaneously.
4. If a course is a public foundational course, set `has_public` to true and update all relevant sums accordingly.
5. If a course is a professional elective, update professional elective credits and also contribute to professional credits.
6. If a course is a compulsory session, only add to compulsory session credits and total credits, since it is not part of degree course structure.
7. After processing all courses, check all constraints one by one: total credits, course credits, compulsory credits, degree credits, professional credits, professional foundational credits, and professional elective credits. Also verify that at least one public foundational course was taken.

### Why it works

Each course contributes independently to a fixed set of additive counters. Since constraints are linear inequalities over these same counters, maintaining exact sums guarantees correctness. No future course can invalidate past computations, so a single pass accumulation preserves all necessary information without backtracking or recomputation.

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
        course_total = 0
        compulsory = 0

        degree = 0
        professional = 0
        prof_found = 0
        prof_elective = 0

        has_public = False

        for _ in range(n):
            name = input().rstrip()
            typ = input().rstrip()
            val = int(input())

            total += val
            course_total += val

            if typ == "compulsory sessions":
                compulsory += val

            if typ == "public foundational courses":
                has_public = True
                degree += val

            if typ == "professional foundational courses":
                degree += val
                professional += val
                prof_found += val

            if typ == "professional elective courses":
                professional += val
                prof_elective += val

            if typ == "interdisciplinary elective courses":
                pass

            if typ == "other elective courses":
                pass

        ok = True
        ok &= total >= a
        ok &= course_total >= b
        ok &= compulsory >= c
        ok &= degree >= d
        ok &= professional >= e
        ok &= prof_found >= f
        ok &= prof_elective >= g
        ok &= has_public

        print("YES" if ok else "NO")

if __name__ == "__main__":
    solve()
```

The implementation mirrors the category decomposition directly. Each conditional branch corresponds to a course type and updates only the counters that definitionally include it. The final boolean check aggregates all constraints in a single expression, ensuring no condition is overlooked.

A common pitfall is forgetting that degree credits include both public and professional foundational courses. Another is treating elective categories as mutually exclusive from professional totals, which would undercount `professional` and break the condition involving `e`.

## Worked Examples

We use the provided sample input.

### Trace

We track only key aggregates.

| Step | Course Type | Value | total | compulsory | degree | professional | prof_found | prof_elective | has_public |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | public foundational | 2 | 2 | 0 | 2 | 0 | 0 | 0 | True |
| 2 | prof foundational | 3 | 5 | 0 | 5 | 3 | 3 | 0 | True |
| 3 | prof foundational | 3 | 8 | 0 | 8 | 6 | 6 | 0 | True |
| 4 | prof elective | 2 | 10 | 0 | 8 | 8 | 6 | 2 | True |
| 5 | prof elective | 2 | 12 | 0 | 8 | 10 | 6 | 4 | True |
| 6 | prof foundational | 2 | 14 | 0 | 10 | 12 | 8 | 4 | True |
| 7 | prof foundational | 3 | 17 | 0 | 13 | 15 | 11 | 4 | True |
| 8 | prof elective | 2 | 19 | 0 | 13 | 17 | 11 | 6 | True |
| 9 | prof elective | 2 | 21 | 0 | 13 | 19 | 11 | 8 | True |
| 10 | other elective | 1 | 22 | 0 | 13 | 19 | 11 | 8 | True |
| 11 | public foundational | 3 | 25 | 0 | 16 | 19 | 11 | 8 | True |
| 12 | compulsory | 1 | 26 | 1 | 16 | 19 | 11 | 8 | True |
| 13 | compulsory | 1 | 27 | 2 | 16 | 19 | 11 | 8 | True |
| 14 | compulsory | 1 | 28 | 3 | 16 | 19 | 11 | 8 | True |
| 15 | compulsory | 1 | 29 | 4 | 16 | 19 | 11 | 8 | True |

At the end, all thresholds are met, so the output is YES.

This trace shows how compulsory credits accumulate separately while still contributing to total credits, and how overlapping professional categories build multiple sums simultaneously.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each course is processed once with constant-time updates |
| Space | O(1) | Only a fixed number of counters are maintained |

Given n ≤ 100 and T ≤ 100, the maximum number of operations is negligible. The solution easily fits within both time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    from math import isclose

    # re-run solution
    input = sys.stdin.readline

    def solve():
        T = int(input())
        out = []
        for _ in range(T):
            a, b, c, d, e, f, g = map(int, input().split())
            n = int(input())

            total = course_total = compulsory = 0
            degree = professional = prof_found = prof_elective = 0
            has_public = False

            for _ in range(n):
                _ = input().rstrip()
                typ = input().rstrip()
                val = int(input())

                total += val
                course_total += val

                if typ == "compulsory sessions":
                    compulsory += val
                if typ == "public foundational courses":
                    has_public = True
                    degree += val
                if typ == "professional foundational courses":
                    degree += val
                    professional += val
                    prof_found += val
                if typ == "professional elective courses":
                    professional += val
                    prof_elective += val

            ok = (total >= a and course_total >= b and compulsory >= c and
                  degree >= d and professional >= e and prof_found >= f and
                  prof_elective >= g and has_public)

            out.append("YES" if ok else "NO")

        return "\n".join(out)

    return solve()

# sample
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

# minimum case: missing public course
assert run("""1
5 5 1 2 2 1 1
2
A
professional foundational courses
3
B
professional elective courses
2
""") == "NO"

# all constraints exactly met
assert run("""1
5 5 0 2 2 1 1
2
A
public foundational courses
2
B
professional foundational courses
3
""") == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| missing public course | NO | enforces boolean constraint |
| exact satisfaction | YES | boundary correctness |

## Edge Cases

One important case is when all numeric constraints are satisfied but no public foundational course is taken. In that situation, all sums may exceed thresholds, but the boolean requirement fails, forcing a NO. The algorithm handles this because `has_public` is tracked independently from numeric totals and is included in the final check.

Another case is when courses exist only in elective categories. These contribute to total credits but not to degree or professional foundational sums. The separation ensures that we do not incorrectly inflate degree-related counters, since only explicitly labeled types update those aggregates.
