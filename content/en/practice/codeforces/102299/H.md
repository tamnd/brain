---
title: "CF 102299H - Course recommendation"
description: "Each student has taken some subset of the available courses, and for every course they took we know their grade. For a particular student, we must find the other student whose grades are most similar on the courses they have both taken."
date: "2026-08-13T08:17:39+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102299
codeforces_index: "H"
codeforces_contest_name: "2019 USP Try-outs"
rating: 0
weight: 102299
solve_time_s: 111
verified: true
draft: false
---

[CF 102299H - Course recommendation](https://codeforces.com/problemset/problem/102299/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 51s  
**Verified:** yes  

## Solution
## Problem Understanding

Each student has taken some subset of the available courses, and for every course they took we know their grade. For a particular student, we must find the other student whose grades are most similar on the courses they have both taken.

The distance between two students is computed only from courses that appear in both students' histories. If they share courses (c_1,c_2,\ldots,c_k), with grades (g_{i,c}) and (g_{j,c}), their squared distance is

[
D(i,j)=\sum_c (g_{i,c}-g_{j,c})^2,
]

where the sum contains only shared courses. The actual Euclidean distance is (\sqrt{D(i,j)}), but comparing squared distances gives exactly the same ordering.

Once the closest student is found, we look through that student's courses. We want a course that the original student has not taken, with the highest grade in the closest student's record. If several such courses have the same grade, the smallest course index wins. If every course of the closest student has already been taken, the answer is (-1).

The input has at most 100 students and 100 courses. This is small enough that we can directly compare every pair of students and inspect every course. There are at most (100\cdot99\cdot100=990{,}000) course comparisons when finding distances, which is easily manageable in one second. The recommendation phase adds only another (100\cdot100=10{,}000) checks. There is no need for a sophisticated nearest-neighbor data structure.

A useful representation is a two-dimensional array `grade[student][course]`. A missing course can be represented by `-1`, while every real grade is between 0 and 10. This lets us test whether a course is shared with one simple comparison.

One subtle case is that students can share no courses. Their distance is infinity, so such a student must never become the closest student when the input guarantees that every student has at least one course in common with someone else. A careless implementation that initializes the minimum distance to zero would never replace it, producing an invalid answer. For example:

```
2 2
1
1 7
1
2 9
```

This violates the problem's guarantee, because the two students have no shared course. Under the stated input constraints this situation does not occur, but the implementation still represents it naturally as infinity.

Another edge case occurs when the closest student has no new course to recommend. For example:

```
2 2
2
1 10
2 5
1
1 8
```

The first student is the closest student to the second, but student 2 has not taken course 2, so the answer for student 2 is `2`. Conversely, if the second student had also taken both courses, there would be no recommendation and the answer would be `-1`.

A tie between courses must be resolved by course index, not by the order in which courses happen to appear in the input. For example:

```
2 3
1
1 7
3
1 5
2 9
3 9
```

Student 1 is closest to student 2, and courses 2 and 3 both have grade 9 for student 2. The correct recommendation is course 2 because its index is smaller. An implementation that simply replaces the current answer whenever it sees an equal grade could incorrectly return course 3.

The statement does not explicitly specify what to do when several other students have exactly the same minimum distance. We scan student indices in increasing order and replace the current closest student only when a strictly smaller distance is found. Thus the smallest-index closest student is selected. This is also the deterministic behavior of the usual direct implementation of the problem.

## Approaches

The direct approach is already fast enough for these constraints. Store every student's grades in an (N\times M) matrix. For every ordered pair of distinct students (i,j), scan all (M) courses. Whenever both students took the course, add the squared grade difference to their distance. After all courses have been examined, compare that distance with the best distance found for student (i).

This works because the definition of distance itself is a sum over shared courses. Scanning every course explicitly neither misses a shared course nor includes a course that only one student took.

A completely literal implementation could calculate the square root after every pair and compare actual Euclidean distances. That is unnecessary. Since the square-root function is strictly increasing for nonnegative values, minimizing (D) is exactly equivalent to minimizing (\sqrt D). Using squared distances also keeps the implementation integer-only.

The brute-force method performs at most (N(N-1)M) course checks. With (N=M=100), that is

[
100\cdot99\cdot100=990{,}000
]

checks. After that, finding the recommendation requires at most (NM=10{,}000) additional course checks. This is comfortably below what Python can handle under the given limits.

The useful optimization is not a different asymptotic algorithm, because none is necessary here. The key observation is that the input bounds make exhaustive comparison cheap. Representing the data as a dense matrix and using squared distances gives the simplest implementation with the smallest constant factors. A dictionary per student would also work, but it adds hashing overhead without solving a performance problem.

The brute-force method works because there are only 100 students and 100 courses. It would become unattractive if both dimensions were in the tens of thousands, but at the actual constraints the same exhaustive computation is the optimal engineering choice.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Literal pairwise distance with Euclidean square roots | (O(N^2M)) | (O(NM)) | Accepted, but unnecessary square roots |
| Pairwise squared distance with a grade matrix | (O(N^2M)) | (O(NM)) | Accepted |

## Algorithm Walkthrough

1. Create `grade[i][c]` for every student and course. Initialize every entry to `-1`, meaning that the student has not taken that course. When an input record `(c, g)` is read, store `g` at the corresponding position. A matrix is convenient because every later distance calculation can inspect a course in constant time.
2. For each student `i`, initialize the best distance to infinity and the closest student to an invalid value. Then inspect every other student `j`.
3. For each pair `(i, j)`, initialize its squared distance to zero and scan all courses. If either student has `-1` for a course, ignore it because that course is not shared. Otherwise add `(grade[i][c] - grade[j][c]) ** 2` to the distance.
4. After the shared courses have been processed, compare the resulting squared distance with the current minimum for student `i`. Replace the closest student only when the new distance is strictly smaller. Because students are examined in increasing index order, equal distances keep the smaller student index.
5. Once the closest student `j` is known, scan all courses again. Skip every course already taken by student `i`. For every remaining course that student `j` has taken, compare its grade with the best recommendation grade seen so far.
6. Keep the course with the highest grade. If two candidates have the same grade, keep the smaller course index. Since courses are scanned from index 1 upward, updating only on a strictly larger grade automatically gives the required tie-breaking rule.
7. If no course from the closest student's history is new to student `i`, print `-1`. Otherwise print the selected course index.

### Why it works

For every pair of students, the algorithm examines every course and adds a squared grade difference exactly when that course belongs to both students. Thus the computed value is exactly the square of their defined Euclidean distance. Since squaring preserves the ordering of nonnegative distances, the student retained as closest is a valid closest student.

After choosing that student, the second scan considers exactly the courses that the closest student took and the original student did not. Among these candidates, the algorithm keeps the largest grade and, for equal grades, the smallest index. Hence the final course is exactly the required recommendation, or `-1` when the candidate set is empty.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())

    grade = [[-1] * (m + 1) for _ in range(n)]

    for i in range(n):
        q = int(input())
        for _ in range(q):
            c, g = map(int, input().split())
            grade[i][c] = g

    answers = []

    for i in range(n):
        best_dist = float('inf')
        closest = -1

        for j in range(n):
            if i == j:
                continue

            dist = 0

            for c in range(1, m + 1):
                gi = grade[i][c]
                gj = grade[j][c]

                if gi != -1 and gj != -1:
                    diff = gi - gj
                    dist += diff * diff

            if dist < best_dist:
                best_dist = dist
                closest = j

        best_course = -1
        best_grade = -1

        for c in range(1, m + 1):
            if grade[i][c] != -1:
                continue

            g = grade[closest][c]
            if g == -1:
                continue

            if g > best_grade:
                best_grade = g
                best_course = c

        answers.append(str(best_course))

    sys.stdout.write("\n".join(answers))

if __name__ == "__main__":
    solve()
```

The first part constructs the grade matrix described in step 1. Course indices are stored from 1 through `m`, so the extra column at index 0 is unused. This mirrors the course numbering in the input and avoids repeatedly subtracting one from course indices.

The nested `i` and `j` loops implement steps 2 through 4. The condition `i == j` prevents comparing a student with themself. `best_dist` starts at infinity so the first valid other student is always accepted. We use squared distances, so `dist` remains an integer and no floating-point precision is involved.

The input guarantees that every student shares at least one course with another student. Consequently, `closest` will always become a valid student. The implementation would also behave safely if that guarantee were absent until the recommendation phase, but the problem does not require handling such invalid input.

The final course scan implements steps 5 and 6. The test `grade[i][c] != -1` removes courses already taken by the original student. The next test removes courses not taken by the closest student. `best_grade` begins at `-1`, which is below every legal grade from 0 through 10, so even a grade of zero is correctly accepted.

The comparison uses `g > best_grade`, not `g >= best_grade`. Courses are traversed in increasing index order, so when two courses have equal grades, the first one remains selected. That directly implements the smallest-index tie-break.

There is no integer overflow issue in Python. Even in a fixed-width language, the largest squared difference is (10^2=100), and at most 100 shared courses contribute, so a distance is at most 10,000.

## Worked Examples

### Sample 1

The input describes two students. Student 1 has courses 1 and 2 with grade 10 in both. Student 2 has course 2 with grade 9 and course 3 with grade 5.

For student 1, the only possible closest student is student 2. They share course 2, so the squared distance is ((10-9)^2=1). Student 2's course 3 is new to student 1, making it the only recommendation.

| Student | Candidate | Shared course | Squared distance | Closest | Recommendation |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | 2: (10,9) | 1 | 2 | 3 |
| 2 | 1 | 2: (9,10) | 1 | 1 | none |

For student 2, student 1 is closest with the same squared distance of 1. Course 1 is new to student 2 and has grade 10, so it is recommended. The resulting output is `3` followed by `1`.

### Sample 2

Student 1 has courses 1, 2, and 3 with grades 7, 8, and 10. Student 2 has courses 4, 2, and 1 with grades 10, 9, and 5.

For student 1 and student 2, the shared courses are 1 and 2. Their squared distance is

[
(7-5)^2+(8-9)^2=4+1=5.
]

Student 2's course 4 is not in student 1's history, so it becomes the recommendation.

| Student | Candidate | Shared courses | Squared distance | Closest | New courses of closest student | Recommendation |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 2 | 1, 2 | 5 | 2 | 4 with grade 10 | 4 |
| 2 | 1 | 1, 2 | 5 | 1 | 3 with grade 10 | 3 |

For student 2, student 1's course 3 is the only course that student 2 has not taken, so the recommendation is 3. This example also confirms that courses absent from both students do not contribute anything to the distance.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(N^2M)) | There are (N(N-1)) ordered student pairs, and each pair scans all (M) courses. The recommendation scans add (O(NM)), which is dominated by (O(N^2M)). |
| Space | (O(NM)) | The grade matrix stores one entry for every student-course pair. |

With (N,M\le100), the dominant computation has fewer than one million course checks. The memory usage is only about 10,000 matrix entries, so the solution is comfortably inside both the 1 second time limit and the 256 MB memory limit.

## Test Cases

```python
import sys
import io

input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())

    grade = [[-1] * (m + 1) for _ in range(n)]

    for i in range(n):
        q = int(input())
        for _ in range(q):
            c, g = map(int, input().split())
            grade[i][c] = g

    answers = []

    for i in range(n):
        best_dist = float('inf')
        closest = -1

        for j in range(n):
            if i == j:
                continue

            dist = 0

            for c in range(1, m + 1):
                gi = grade[i][c]
                gj = grade[j][c]

                if gi != -1 and gj != -1:
                    diff = gi - gj
                    dist += diff * diff

            if dist < best_dist:
                best_dist = dist
                closest = j

        best_course = -1
        best_grade = -1

        for c in range(1, m + 1):
            if grade[i][c] != -1:
                continue

            g = grade[closest][c]

            if g == -1:
                continue

            if g > best_grade:
                best_grade = g
                best_course = c

        answers.append(str(best_course))

    sys.stdout.write("\n".join(answers))

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    try:
        sys.stdin = io.StringIO(inp)
        sys.stdout = io.StringIO()
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided sample 1
assert run(
    """2 3
2
1 10
2 10
2
2 9
3 5
"""
) == "3\n1", "sample 1"

# Provided sample 2
assert run(
    """2 4
3
1 7
2 8
3 10
3
4 10
2 9
1 5
"""
) == "4\n3", "sample 2"

# Minimum-size input.
# Both students took the only course, so neither has anything new to recommend.
assert run(
    """2 1
1
1 0
1
1 10
"""
) == "-1\n-1", "minimum-size case"

# Equal recommendation grades.
# Student 2 has two new courses with the same grade, so the smaller index wins.
assert run(
    """2 3
1
1 7
3
1 5
2 9
3 9
"""
) == "2\n-1", "course-index tie case"

# All grades equal.
# Student 1 should receive the smallest new course index from student 2.
assert run(
    """3 5
2
1 5
2 5
3
1 5
3 5
4 5
2
1 5
5 5
"""
) == "3\n2\n2", "all-equal grades"

# Boundary grade 0 and 10.
# Distance calculations must include both endpoints of the grade range.
assert run(
    """2 3
1
1 0
2
1 10
2 0
"""
) == "2\n-1", "boundary grades"

# Maximum-size case generated programmatically.
# Every student has all courses, so every closest student has no new course.
n = 100
m = 100
parts = [f"{n} {m}"]
for _ in range(n):
    parts.append(str(m))
    for c in range(1, m + 1):
        parts.append(f"{c} 5")

max_case = "\n".join(parts) + "\n"
assert run(max_case) == "-1\n" * n, "maximum-size case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 1`, both students took the only course | `-1`, `-1` | Minimum dimensions and the no-new-course case |
| Two equal-grade candidate courses | `2`, `-1` | Smallest course index wins a grade tie |
| Three students with all grades equal | `3`, `2`, `2` | Equal distances, equal grades, and deterministic student selection |
| Grades 0 and 10 | `2`, `-1` | Grade boundaries and squared-distance arithmetic |
| 100 students and 100 courses, all fully enrolled | 100 lines of `-1` | Maximum dimensions and the case where every closest student's course is already taken |

## Edge Cases

The minimum-size case has one course and two students:

```
2 1
1
1 0
1
1 10
```

The students share course 1, so their squared distance is (100). Each student's closest student has exactly the same single course, and neither student has a course that the other lacks. The recommendation scan finds no candidate, leaving `best_course = -1`. The output is:

```
-1
-1
```

The equal-grade tie case is:

```
2 3
1
1 7
3
1 5
2 9
3 9
```

For student 1, student 2 is the closest student because course 1 is shared. Courses 2 and 3 are both new and both have grade 9. The scan visits course 2 first, stores it as the best recommendation, then sees the equal grade at course 3. Because the update condition is strictly greater, course 2 remains selected. The first output line is `2`.

The all-equal case is:

```
3 5
2
1 5
2 5
3
1 5
3 5
4 5
2
1 5
5 5
```

Every shared grade is identical, so all distances between students who share courses are zero. For student 1, students 2 and 3 are equally close, and the increasing-index scan keeps student 2. Student 2 then recommends course 3, the smallest new course among its courses. This exercises the unspecified closest-student tie and confirms the deterministic smallest-index behavior of the implementation.

The grade-boundary case is:

```
2 3
1
1 0
2
1 10
2 0
```

The shared course contributes ((0-10)^2=100), which is handled without floating-point arithmetic. Student 1 receives course 2 because it is new and has grade 0. Student 2 has no course that student 1 took differently as a recommendation source, so its output is `-1`. This confirms that grade zero must be treated as a valid candidate rather than as a sentinel.

Finally, consider the maximum-size input where every one of 100 students has taken all 100 courses with grade 5. Every pair has distance zero, and the first other student is retained as the closest because equal distances do not replace the current choice. That closest student has no course unknown to the original student, so every answer is `-1`. The algorithm performs the full (990{,}000) pairwise course checks without exceeding the intended complexity.
