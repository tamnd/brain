---
title: "CF 459C - Pashmak and Buses"
description: "We need to assign each student to one of k buses on each of d days. For every student, we can think of their assignment as a sequence of length d. For example, if d = 3, a student might ride buses (2, 1, 2) over the three days."
date: "2026-05-30T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "constructive-algorithms", "math"]
categories: ["algorithms"]
codeforces_contest: 459
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 261 (Div. 2)"
rating: 1900
weight: 459
solve_time_s: 119
verified: false
draft: false
---

[CF 459C - Pashmak and Buses](https://codeforces.com/problemset/problem/459/C)

**Rating:** 1900  
**Tags:** combinatorics, constructive algorithms, math  
**Solve time:** 1m 59s  
**Verified:** no  

## Solution
## Problem Understanding

We need to assign each student to one of `k` buses on each of `d` days.

For every student, we can think of their assignment as a sequence of length `d`. For example, if `d = 3`, a student might ride buses `(2, 1, 2)` over the three days.

Two students become close friends if their entire sequences are identical. They are allowed to share a bus on some days, but if they share the same bus on every single day, their sequences match and the arrangement is invalid.

The task is to construct assignments for `n` students so that every student has a unique sequence. If that is impossible, we must print `-1`.

The constraints immediately suggest that we are not dealing with a search problem. Both `n` and `d` can reach 1000, while `k` can be as large as `10^9`. A brute-force search through assignments would be hopeless because the number of possible schedules grows exponentially. Since the output itself contains `n × d` numbers, any accepted solution will likely spend most of its time generating the answer directly.

The central question is whether we can give all `n` students distinct sequences of length `d`, where each position can take one of `k` values.

There are exactly `k^d` different sequences of length `d` over an alphabet of size `k`. If `n > k^d`, then even in the best possible arrangement there are not enough distinct sequences, so some pair of students must receive the same sequence. By the pigeonhole principle, the answer is impossible.

Several edge cases are easy to mishandle.

Consider:

```
3 1 2
```

There is only one bus. Every student must ride bus 1 every day. All students receive the same sequence `(1,1)`, so the correct answer is:

```
-1
```

A careless construction that ignores the uniqueness requirement would incorrectly output assignments.

Consider:

```
1 1 1
```

There is only one student. Uniqueness is automatic because there are no pairs of students. The correct output is:

```
1
```

Some implementations incorrectly reject all cases with `k = 1`.

Another subtle case is:

```
8 2 3
```

Since `2^3 = 8`, there are exactly enough distinct sequences. A correct solution must use all possible sequences. An implementation with an off-by-one mistake in its numbering system might generate only seven distinct assignments and incorrectly report failure.

## Approaches

The most direct way to think about the problem is to assign a sequence to every student and then check whether all sequences are distinct.

A brute-force approach would generate assignments day by day, compare every pair of students, and keep modifying schedules until all conflicts disappear. Such a strategy quickly becomes infeasible because the search space contains `k^(n·d)` possible schedules. Even for very small inputs, exhaustive exploration is impossible.

The key observation is that students only need distinct sequences.

Each student's schedule is a length-`d` string over an alphabet of size `k`. The number of possible schedules is exactly `k^d`. This transforms the problem into a numbering problem: assign a different codeword to each student.

The natural way to generate distinct codewords is to write the student indices in base `k`.

Suppose we number students from `0` to `n-1`.

Student `0` corresponds to:

```
000...
```

Student `1` corresponds to:

```
001...
```

Student `2` corresponds to:

```
002...
```

and so on, using exactly `d` base-`k` digits.

If `n ≤ k^d`, then all student indices fit into `d` base-`k` digits. Distinct numbers have distinct digit representations, so every student automatically receives a unique schedule.

The bus numbers in the statement are numbered from `1` to `k`, while base-`k` digits range from `0` to `k-1`. We simply add one when printing.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(n·d) | O(n·d) | Accepted |

## Algorithm Walkthrough

1. Read `n`, `k`, and `d`.
2. Determine whether at least `n` distinct schedules exist.

Compute powers of `k` up to length `d`, stopping early once the value reaches or exceeds `n`.
3. If after `d` multiplications the value is still smaller than `n`, print `-1`.

This means `k^d < n`, so there are not enough distinct sequences for all students.
4. Create a `d × n` answer matrix.

Row `i` will represent the assignments for day `i`.
5. For every student index `s` from `0` to `n-1`, write `s` in base `k`.

Extract exactly `d` digits. Missing higher digits are treated as zero.
6. Store the extracted digits into the answer matrix.

The `i`-th digit determines the bus used on day `i`.
7. After processing all students, add one to every stored digit when printing.

This converts digits `0..k-1` into bus numbers `1..k`.

### Why it works

Every student is assigned the base-`k` representation of a distinct integer between `0` and `n-1`.

Because base-`k` representations are unique, no two students receive the same sequence of digits. Consequently, for any pair of students, there exists at least one day on which their assigned buses differ.

The construction uses exactly `d` digits. Such representations exist for all student indices precisely when `n ≤ k^d`. If `n > k^d`, there are fewer possible sequences than students, so a valid arrangement cannot exist. Thus the algorithm is both necessary and sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k, d = map(int, input().split())

    cnt = 1
    for _ in range(d):
        if cnt >= n:
            break
        cnt *= k

    if cnt < n:
        print(-1)
        return

    ans = [[0] * n for _ in range(d)]

    for student in range(n):
        x = student
        for day in range(d):
            ans[day][student] = x % k
            x //= k

    out = []
    for day in range(d):
        out.append(" ".join(str(ans[day][student] + 1) for student in range(n)))

    sys.stdout.write("\n".join(out))

solve()
```

The first part checks whether enough distinct schedules exist. We never need the exact value of `k^d` once it exceeds `n`, so the multiplication can stop early.

The matrix is organized by days rather than by students because the required output format prints one day per line. This avoids a later transpose operation.

For each student, we repeatedly take `x % k` and divide by `k`. This extracts the base-`k` digits from least significant to most significant. Since every student index is different, their digit vectors are different as well.

A common mistake is forgetting that bus numbers start at `1`. The internal representation uses digits `0..k-1`, so we add one only when printing.

Another frequent bug is trying to compute `k^d` directly. Although Python can handle large integers, it is unnecessary. Early stopping keeps the check simple and efficient.

## Worked Examples

### Example 1

Input:

```
3 2 2
```

Students are numbered `0,1,2`.

| Student | Base-2 Representation (2 digits) |
| --- | --- |
| 0 | 00 |
| 1 | 01 |
| 2 | 10 |

The stored digits by day become:

| Day | Student 0 | Student 1 | Student 2 |
| --- | --- | --- | --- |
| 1 | 0 | 1 | 0 |
| 2 | 0 | 0 | 1 |

After adding one:

| Day | Student 0 | Student 1 | Student 2 |
| --- | --- | --- | --- |
| 1 | 1 | 2 | 1 |
| 2 | 1 | 1 | 2 |

Output:

```
1 2 1
1 1 2
```

This differs from the sample output but is equally valid because all students receive distinct schedules.

### Example 2

Input:

```
8 2 3
```

Since `2^3 = 8`, every possible binary sequence of length three is needed.

| Student | Digits |
| --- | --- |
| 0 | 000 |
| 1 | 001 |
| 2 | 010 |
| 3 | 011 |
| 4 | 100 |
| 5 | 101 |
| 6 | 110 |
| 7 | 111 |

Every sequence appears exactly once. No two students share all three bus assignments.

This example demonstrates the boundary case where `n = k^d` and every available codeword must be used.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n·d) | Each student contributes exactly `d` base-`k` digits |
| Space | O(n·d) | The output matrix stores `d × n` values |

The largest possible output already contains one million numbers because both `n` and `d` can be 1000. An `O(n·d)` construction matches the output size and comfortably fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    n, k, d = map(int, input().split())

    cnt = 1
    for _ in range(d):
        if cnt >= n:
            break
        cnt *= k

    if cnt < n:
        return "-1"

    ans = [[0] * n for _ in range(d)]

    for student in range(n):
        x = student
        for day in range(d):
            ans[day][student] = x % k
            x //= k

    return "\n".join(
        " ".join(str(ans[day][student] + 1) for student in range(n))
        for day in range(d)
    )

# minimum case
assert run("1 1 1\n") == "1"

# impossible case
assert run("3 1 2\n") == "-1"

# boundary n = k^d
out = run("8 2 3\n")
assert out != "-1"

# sample-sized case
out = run("3 2 2\n")
assert out != "-1"

# another impossible boundary
assert run("9 2 3\n") == "-1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1` | `1` | Smallest valid instance |
| `3 1 2` | `-1` | Only one available sequence |
| `8 2 3` | Any valid schedule | Exact capacity boundary `n = k^d` |
| `3 2 2` | Any valid schedule | Basic construction |
| `9 2 3` | `-1` | First impossible value above capacity |

## Edge Cases

Consider:

```
3 1 2
```

The algorithm computes:

```
1^2 = 1
```

Since `1 < 3`, it immediately prints:

```
-1
```

There is only one possible sequence `(1,1)`, so three distinct students cannot be assigned unique schedules.

Consider:

```
1 1 1
```

The capacity check succeeds because `1^1 = 1`. Student `0` receives digit `0`, which becomes bus `1` after adding one:

```
1
```

The single-student case is valid because uniqueness among multiple students is not required.

Consider:

```
8 2 3
```

The capacity check reaches exactly `8`. Student indices `0` through `7` generate all binary strings of length three. Since base-2 representations are unique, every student gets a different schedule and the construction succeeds at the tight boundary.

Consider:

```
9 2 3
```

The algorithm computes:

```
2^3 = 8
```

Since `8 < 9`, it outputs:

```
-1
```

The pigeonhole principle guarantees impossibility because only eight distinct schedules exist while nine students require unique ones.
