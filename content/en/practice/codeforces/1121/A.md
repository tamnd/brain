---
title: "CF 1121A - Technogoblet of Fire"
description: "We are given a set of students, each belonging to a school, and each with a power rating. The tournament rule is simple: only the strongest student from each school gets selected. Arkady wants to ensure that a chosen set of k students are selected."
date: "2026-06-12T04:22:15+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1121
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 543 (Div. 2, based on Technocup 2019 Final Round)"
rating: 1100
weight: 1121
solve_time_s: 66
verified: true
draft: false
---

[CF 1121A - Technogoblet of Fire](https://codeforces.com/problemset/problem/1121/A)

**Rating:** 1100  
**Tags:** implementation, sortings  
**Solve time:** 1m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of students, each belonging to a school, and each with a power rating. The tournament rule is simple: only the strongest student from each school gets selected. Arkady wants to ensure that a chosen set of `k` students are selected. Some of these students may not currently be the strongest in their schools. He can manipulate the system by assigning them to new, fictional schools, guaranteeing their selection, but he wants to minimize the number of such fictional schools.

Input includes `n` students with their powers, their schools, and the list of `k` Chosen Ones. Output is the minimal number of new schools Arkady must create to guarantee all `k` Chosen Ones are selected.

Constraints are small (`n` ≤ 100, `m` ≤ n, `k` ≤ n). This allows algorithms that iterate over students and schools multiple times. A naive solution that checks each Chosen One against all schoolmates is feasible. However, we need careful handling of power comparisons and school membership to avoid off-by-one mistakes.

Non-obvious edge cases include:

- A Chosen One is already the strongest in their school. No new school is needed.
- Multiple Chosen Ones in the same school, where only one is strongest. We need multiple new schools for the weaker Chosen Ones.
- All students are already Chosen Ones. Arkady may not need to create any schools at all.

For example, with students `[5, 3]` in school `[1, 1]` and Chosen Ones `[2]`, student 2 is weaker than student 1 in the same school, so one new school is needed. A careless implementation might overlook the per-school maximum and output zero incorrectly.

## Approaches

The brute-force approach checks each Chosen One: for their current school, determine the strongest student. If the Chosen One is weaker than someone else, count one new school. This works because the number of students is small. In worst case, for each of `k` Chosen Ones, we scan up to `n` students, giving `O(n*k)` operations, which is acceptable for `n` ≤ 100.

The insight that optimizes this is that we only care about the strongest student per school. We do not need to sort all students or simulate the Technogoblet fully. We compute the max power for each existing school once, store it, and then for each Chosen One check if their power equals the school's max. If yes, no new school; if no, one new school. This reduces redundant comparisons and simplifies reasoning.

The optimization relies on the property that schools are independent: the selection of a student in one school does not affect another. Therefore, each Chosen One’s need for a new school can be determined in isolation once we know the school maxima.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n*k) | O(1) | Accepted due to small constraints |
| Optimal | O(n + k) | O(m) | Accepted and clean |

## Algorithm Walkthrough

1. Read input values `n`, `m`, `k`, then student powers `p`, student schools `s`, and Chosen Ones `c`. Adjust indices to be zero-based if convenient.
2. Construct an array `school_max` of size `m` to store the strongest student power in each school. Iterate over all students and for each, update `school_max[school[i]]` if `p[i]` is higher.
3. Initialize a counter `new_schools = 0`.
4. Iterate through each Chosen One `ci`. Check the power of `ci` against the maximum power of their current school. If `p[ci]` is less than `school_max[s[ci]]`, increment `new_schools` by one.
5. Print `new_schools`.

Why it works: For each Chosen One, either they are already the strongest in their school and are automatically selected, or they are weaker and need a new school. Because the strongest-per-school property guarantees uniqueness, no Chosen One is double-counted or affected by another's new school. The algorithm correctly counts the minimal number of new schools.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m, k = map(int, input().split())
p = list(map(int, input().split()))
s = list(map(int, input().split()))
c = list(map(int, input().split()))

# convert to zero-based indices
s = [x-1 for x in s]
c = [x-1 for x in c]

school_max = [0] * m
for i in range(n):
    school_max[s[i]] = max(school_max[s[i]], p[i])

new_schools = 0
for ci in c:
    if p[ci] < school_max[s[ci]]:
        new_schools += 1

print(new_schools)
```

Explanation: We first compute `school_max` efficiently in a single pass. Then for each Chosen One, we compare against the school's max to see if a new school is required. Index adjustments avoid off-by-one errors. Using `max` ensures we handle ties correctly, though by problem statement powers are distinct.

## Worked Examples

Sample 1:

Input:

```
7 3 1
1 5 3 4 6 7 2
1 3 1 2 1 2 3
3
```

| Step | school_max | ci | p[ci] | school_max[s[ci]] | new_schools |
| --- | --- | --- | --- | --- | --- |
| Init | [6,7,5] | 3 | 3 | 6 | 0 |
| Check | - | 3 | 3 | 6 | 1 |

Output: 1.

Explanation: Student 3 is weaker than student 5 in school 1, so one new school is required.

Sample 2:

Input:

```
5 3 2
10 20 30 40 50
1 2 2 3 3
2 4
```

| Step | school_max | ci | p[ci] | school_max[s[ci]] | new_schools |
| --- | --- | --- | --- | --- | --- |
| Init | [10,30,50] | 2 | 20 | 30 | 0 |
| Check | - | 2 | 20 | 30 | 1 |
| Check | - | 4 | 40 | 50 | 2 |

Output: 2.

Explanation: Both Chosen Ones are not strongest in their schools; two new schools are required.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + k) | One pass to compute school maxima, one pass for Chosen Ones |
| Space | O(m) | Array storing maximum power per school |

With `n` ≤ 100 and `m` ≤ n, this executes in negligible time and uses minimal memory, well within the limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, m, k = map(int, input().split())
    p = list(map(int, input().split()))
    s = list(map(int, input().split()))
    c = list(map(int, input().split()))
    s = [x-1 for x in s]
    c = [x-1 for x in c]
    school_max = [0] * m
    for i in range(n):
        school_max[s[i]] = max(school_max[s[i]], p[i])
    new_schools = 0
    for ci in c:
        if p[ci] < school_max[s[ci]]:
            new_schools += 1
    return str(new_schools)

# Provided samples
assert run("7 3 1\n1 5 3 4 6 7 2\n1 3 1 2 1 2 3\n3\n") == "1"
assert run("5 3 2\n10 20 30 40 50\n1 2 2 3 3\n2 4\n") == "2"

# Custom cases
assert run("1 1 1\n1\n1\n1\n") == "0", "single student, Chosen One is strongest"
assert run("2 1 1\n2 1\n1 1\n2\n") == "1", "weaker Chosen One needs new school"
assert run("3 2 2\n3 1 2\n1 2 2\n2 3\n") == "1", "multiple schools, one Chosen One weaker"
assert run("5 5 5\n5 4 3 2 1\n1 2 3 4 5\n1 2 3 4 5\n") == "0", "all Chosen Ones already strongest"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 1 | 0 | Minimal input |
| 2 1 1 |  |  |
