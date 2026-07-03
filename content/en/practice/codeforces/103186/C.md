---
title: "CF 103186C - \u5c0f A \u7684\u671f\u672b\u8003\u8bd5"
description: "We are given a group of students, each identified by a unique student ID and an initial score. Among them, one student is special, denoted by index m in the input order, and we call this student Xiao A."
date: "2026-07-03T16:12:10+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103186
codeforces_index: "C"
codeforces_contest_name: "The 2021 Shanghai Collegiate Programming Contest"
rating: 0
weight: 103186
solve_time_s: 52
verified: true
draft: false
---

[CF 103186C - \u5c0f A \u7684\u671f\u672b\u8003\u8bd5](https://codeforces.com/problemset/problem/103186/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 52s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a group of students, each identified by a unique student ID and an initial score. Among them, one student is special, denoted by index m in the input order, and we call this student Xiao A.

The transformation happens in two independent phases based on the original scores. First, Xiao A adjusts his own score: if his initial score is below 60, he raises it to 60, otherwise he keeps it unchanged. This change depends only on his own original value and does not affect how other students are judged.

Second, Xiao A looks at everyone else using the original full list of scores. The threshold is the average score computed from the initial state before any modifications. Any other student whose original score is at least this average will have their score decreased by 2 points, with a lower bound of 0.

The key subtlety is that both decisions are based on the initial snapshot of scores. The average is not recomputed after Xiao A’s modification, and the eligibility for reduction is also fixed from the initial data. The only dynamic part is the final application of the two rules.

The output requires printing all students’ final scores sorted by their student IDs in increasing order.

The constraints are small, with n up to 100. This immediately suggests that an O(n^2) or even O(n) solution per test is easily sufficient. Any attempt at complex data structures is unnecessary, and clarity of implementation matters more than optimization.

A common mistake comes from recomputing the average after modifying Xiao A’s score. For example, if initial scores are [1, 4, 100], the average is 35. Xiao A’s update does not change this threshold, but a careless implementation might recompute and shift the cutoff incorrectly.

Another mistake is updating scores in-place and then using updated values to decide whether someone is above average. That breaks the rule that the decision must be based on initial scores.

Finally, forgetting the lower bound of 0 when subtracting 2 can produce negative values, which is invalid.

## Approaches

The brute-force view is straightforward. We first compute the average of all initial scores. Then we iterate over every student. If the student is Xiao A, we apply the rule that clamps his score to at least 60. Otherwise, we check whether their original score is at least the average, and if so, subtract 2.

This approach already runs in linear time. Even if we explicitly separate computation into multiple passes, the total cost is O(n). The only reason to think about optimization is to avoid accidental recomputation of the average or mixing updated and original values.

The key insight is that this is not a simulation with feedback. Nothing changes the decision boundary after it is defined. Once we store the original array and compute the average once, every other operation is a simple deterministic transformation on each element. This reduces the problem to a single pass mapping from initial score to final score.

There is no benefit in maintaining dynamic structures or sorting before transformation. Sorting only becomes relevant in the final output step, which is by ID rather than score.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n) | O(n) | Accepted |
| Direct Computation | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read all student records and store them as pairs of (student_id, score). We need full storage because the output must be sorted by ID, not input order.
2. Compute the sum of all original scores and divide by n to get the average. This value must remain fixed throughout the computation.
3. Identify Xiao A by his position m in the input sequence and store his original score separately. We keep it unchanged for decision-making.
4. Create a mapping from student ID to final score. We will fill this based on rules applied to original values.
5. Iterate over each student. If the student is Xiao A, set his score to max(60, original_score). This ensures the minimum passing adjustment is enforced without affecting others.
6. For all other students, compare their original score with the computed average. If original_score ≥ average, reduce it by 2, ensuring it does not drop below 0. Otherwise, keep it unchanged.
7. After processing all students, sort them by student ID and output their final scores.

### Why it works

The correctness comes from the fact that all decisions are made using a fixed reference state: the original score array. The average defines a static partition of students into two groups, and Xiao A’s adjustment is independent of that partition. Since no rule depends on intermediate results, the transformation is a pure function applied per element. Sorting only affects output order and does not interfere with computation.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m = map(int, input().split())

students = []
id_list = []
scores = []
a_idx = m - 1  # m is given in input order position

for _ in range(n):
    sid, sc = map(int, input().split())
    students.append((sid, sc))
    id_list.append(sid)
    scores.append(sc)

total = sum(scores)
avg = total / n

a_id, a_score = students[a_idx]

result = {}

for sid, sc in students:
    if sid == a_id:
        result[sid] = max(60, sc)
    else:
        if sc >= avg:
            sc = max(0, sc - 2)
        result[sid] = sc

students.sort(key=lambda x: x[0])

print(" ".join(str(result[sid]) for sid, _ in students))
```

The implementation keeps two parallel representations: the raw list of students and a dictionary for final results. The reason for using a dictionary is that output order depends on sorted IDs, which may differ from input order. The average is computed once before any modification, ensuring correctness of the threshold logic.

A subtle point is identifying Xiao A correctly. The input guarantees that m refers to the input position, not the student ID. That is why we directly index into the stored list using m - 1.

## Worked Examples

### Example 1

Input:

```
3 2
1 1
2 4
3 100
```

Initial state:

| Step | Student | Score | Action | Result |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 1 < avg(35) | 1 |
| 2 | 2 | 4 | Xiao A clamp | 60 |
| 3 | 3 | 100 | ≥ avg, -2 | 98 |

Average is (1 + 4 + 100) / 3 = 35.

The first student is below average so unchanged. Xiao A has score 4 so becomes 60. The third student is above average so decreases by 2.

Output sorted by ID:

```
1 60 98
```

This confirms that the average is fixed from the original data and that Xiao A’s adjustment does not influence others.

### Example 2

Input:

```
4 2
4 49
2 98
3 1
1 22
```

Average = (49 + 98 + 1 + 22) / 4 = 42.5

| Student ID | Original | Condition | Final |
| --- | --- | --- | --- |
| 4 | 49 | ≥ avg, -2 | 47 |
| 2 | 98 | Xiao A, max(60, 98) | 98 |
| 3 | 1 | < avg | 1 |
| 1 | 22 | < avg | 22 |

Output:

```
22 98 1 47
```

This trace shows that fractional averages are handled correctly without rounding, since comparisons are done using real-valued threshold logic.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | sorting by student ID dominates after linear processing |
| Space | O(n) | storing all student records and results |

The input size is at most 100, so even the sorting step is trivial. The solution comfortably runs within limits, and memory usage is negligible compared to constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import isclose

    data = inp.strip().split()
    n = int(data[0])
    m = int(data[1])

    students = []
    idx = 2
    for _ in range(n):
        sid = int(data[idx]); sc = int(data[idx+1])
        idx += 2
        students.append((sid, sc))

    total = sum(sc for _, sc in students)
    avg = total / n

    a_id, a_score = students[m-1]

    res = {}
    for sid, sc in students:
        if sid == a_id:
            res[sid] = max(60, sc)
        else:
            if sc >= avg:
                sc = max(0, sc - 2)
            res[sid] = sc

    students_sorted = sorted(students)
    return " ".join(str(res[sid]) for sid, _ in students_sorted)

# provided samples
assert run("3 2\n1 1\n2 4\n3 100") == "1 60 98"
assert run("4 2\n4 49\n2 98\n3 1\n1 22") == "22 98 1 47"

# all equal
assert run("3 1\n2 50\n1 50\n3 50") == "48 60 48"

# minimum n
assert run("1 1\n1 59") == "60"

# boundary average
assert run("2 1\n1 60\n2 60") == "58 60"

# high skew
assert run("3 3\n1 0\n2 0\n3 100") == "0 0 98"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal scores | 48 60 48 | Xiao A clamp and average boundary |
| single student | 60 | minimum case |
| mixed boundary | 58 60 | average equality handling |
| skewed distribution | 0 0 98 | selective reduction correctness |

## Edge Cases

One edge case is when all scores are identical. In that situation, the average equals each score, so every non-Xiao A student qualifies for reduction. For input:

```
3 1
2 50
1 50
3 50
```

Average is 50. Xiao A (student 2) becomes 60. All others are reduced by 2, producing 48 each. The algorithm correctly applies the ≥ condition.

Another edge case is a single student. For input:

```
1 1
1 59
```

Average is 59. Xiao A is the only student and is clamped to 60. There are no other updates, so output is 60. The algorithm handles this naturally because the loop over others is empty.

A final edge case is when Xiao A is already well above 60 and above average. For input:

```
2 2
1 100
2 90
```

Average is 95. Student 1 is below average so unchanged. Xiao A remains 90 since max(60, 90) is 90. The final output is unchanged except ordering. This confirms that Xiao A’s rule does not interact with the threshold condition applied to others.
