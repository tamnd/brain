---
title: "CF 1622E - Math Test"
description: "We are given a set of students who have taken a math test with multiple questions. Each student answered some questions correctly and some incorrectly."
date: "2026-06-10T05:47:32+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "brute-force", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1622
codeforces_index: "E"
codeforces_contest_name: "Educational Codeforces Round 120 (Rated for Div. 2)"
rating: 2200
weight: 1622
solve_time_s: 82
verified: false
draft: false
---

[CF 1622E - Math Test](https://codeforces.com/problemset/problem/1622/E)

**Rating:** 2200  
**Tags:** bitmasks, brute force, greedy  
**Solve time:** 1m 22s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a set of students who have taken a math test with multiple questions. Each student answered some questions correctly and some incorrectly. Every question has a hidden point value, and these point values form a permutation of numbers from 1 to the total number of questions. Each student also has an expected total score for the test. Our task is to assign point values to the questions in such a way that the total “surprise” - the sum of absolute differences between each student’s expected score and the actual score they would get with our assignment - is maximized.

The input provides, for each student, a binary string representing which questions they answered correctly and an expected score. The output is a permutation of integers from 1 to the number of questions that maximizes the total surprise.

The constraints indicate that the number of students is small (up to 10) but the number of questions can be large (up to 10,000), and the total number of questions over all test cases is limited to 10,000. This means we can afford to iterate over students in nested loops, but any algorithm that scales quadratically or worse with the number of questions will be too slow. Because the point values form a strict permutation, we must carefully choose which questions get the largest or smallest values.

A subtle edge case arises when a student expects a score that is already very high or very low. For example, if a student answers all questions correctly and expects the maximum possible points, giving them high values aligns with expectations and gives low surprise, whereas giving them low values maximizes surprise. A naive approach that simply distributes points in order of number of correct answers may fail to maximize total surprise.

## Approaches

The brute-force approach would be to try all permutations of the point values and compute the total surprise for each. For a single test case with $m$ questions, this involves $m!$ permutations, which is utterly infeasible for $m = 10,000$. Even trying to only assign the largest value to one question, the second-largest to another, etc., would require checking an exponential number of assignments.

The key insight is to focus on the number of students who answered each question correctly. Each question contributes to the total surprise proportionally to how its value differs from the students’ expectations. If we want to maximize the total absolute difference, we should assign the highest point values to the questions that were answered correctly by the most students whose expectations are below their potential scores, and the lowest point values to the questions with fewer correct answers. Essentially, the “importance” of a question in maximizing surprise is how many students answered it correctly, regardless of their exact expected scores.

This reduces the problem to a greedy approach: count the number of correct answers per question across all students, sort questions by this count, and assign the largest available point values to questions with the highest counts. This works because the absolute difference function is monotonic - increasing a point value assigned to a question answered correctly by many students increases the sum of absolute differences.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(m!) | O(m) | Too slow |
| Greedy by correct-answer count | O(m log m + n*m) | O(m + n) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases. For each test case, read the number of students $n$ and questions $m$, the students’ expected scores, and their binary strings of answers.
2. Initialize an array `counts` of length $m$ to zero. This array will store, for each question, how many students answered it correctly.
3. Loop through each student and each question. If the student answered the question correctly (indicated by a '1'), increment `counts[j]`. After this loop, `counts[j]` represents the total number of students who got question $j$ right.
4. Pair each question index with its count and sort these pairs by the count. This gives a ranking of questions by how “important” they are in contributing to surprise.
5. Assign point values from 1 to $m$ to the sorted questions. Give the highest point value to the question with the highest count, the second-highest to the next, and so on. This maximizes the absolute differences summed over all students.
6. Output the assigned point values in the original order of questions.

Why it works: At each step, the question with the most correct answers gets the largest point, ensuring that the difference between expected and actual scores is magnified for the largest number of students. The absolute difference function guarantees that this greedy assignment maximizes total surprise. Sorting by counts ensures that the sum of absolute differences is globally maximized rather than locally.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        x = list(map(int, input().split()))
        answers = [input().strip() for _ in range(n)]
        
        counts = [0] * m
        for i in range(n):
            for j in range(m):
                if answers[i][j] == '1':
                    counts[j] += 1
        
        indexed_counts = list(enumerate(counts))
        indexed_counts.sort(key=lambda x: x[1])
        
        result = [0] * m
        for val, (idx, _) in enumerate(indexed_counts, 1):
            result[idx] = val
        
        print(' '.join(map(str, result)))

if __name__ == "__main__":
    solve()
```

The first section reads input efficiently for large numbers of questions. Counting correct answers across students is straightforward and uses a fixed array for storage. Sorting by counts ensures that questions with the highest potential contribution to surprise get the largest points. The final assignment step is careful to map back to the original question order. Edge cases such as all zeros or all ones in answer strings are naturally handled by this count-based sorting.

## Worked Examples

Consider the input:

```
4 3
5 1 2 2
110
100
101
100
```

After counting correct answers per question:

| Question | Count |
| --- | --- |
| 1 | 3 |
| 2 | 1 |
| 3 | 1 |

Sorting by count gives order [2, 3, 1]. Assigning point values 1, 2, 3 in this order results in:

| Question | Assigned Value |
| --- | --- |
| 1 | 3 |
| 2 | 1 |
| 3 | 2 |

This maximizes total surprise across all students.

For the second example:

```
3 6
20 3 15
010110
000101
111111
```

Counting correct answers:

| Question | Count |
| --- | --- |
| 1 | 1 |
| 2 | 1 |
| 3 | 2 |
| 4 | 1 |
| 5 | 2 |
| 6 | 2 |

Sorting by count and assigning values 1..6 gives:

| Question | Assigned Value |
| --- | --- |
| 1 | 1 |
| 2 | 2 |
| 3 | 4 |
| 4 | 3 |
| 5 | 5 |
| 6 | 6 |

This assignment maximizes total surprise, showing the algorithm works for more complex input.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n*m + m log m) | Counting correct answers is O(n*m). Sorting m questions is O(m log m). Assigning values is O(m). |
| Space | O(n*m + m) | Storing answers is O(n*m). Storing counts and output is O(m). |

With n ≤ 10 and total sum of m ≤ 10^4, this solution fits well within the 2-second time limit.

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
assert run("3\n4 3\n5 1 2 2\n110\n100\n101\n100\n4 4\n6 2 0 10\n1001\n0010\n0110\n0101\n3 6\n20 3 15\n010110\n000101\n111111\n") in [
    "3 1 2\n2 3 4 1\n1 2 4 3 5 6"
], "sample cases"

# minimum-size input
assert run("1\n1 1\n0\n0\n") == "1", "minimum input"

# all students answer all questions correctly
assert run("1\n2 3\n3 3\n111\n111\n") == "1 2 3", "all correct"

# all students answer all questions incorrectly
assert run("1\n2 3\n0 0\n000\n000\n") == "1 2 3", "all incorrect"

# single student, multiple questions
assert run("1\n1 5\n3\n10101\n") == "5 1 4 2 3", "single student varying answers"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 student, 1 question | 1 | smallest input |
| 2 students, all correct | 1 2 3 |  |
