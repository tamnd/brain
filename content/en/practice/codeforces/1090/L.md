---
title: "CF 1090L - Berland University"
description: "There are t students and n lectures. A student passes if they attend at least k lectures. Lectures alternate between two auditoriums. Lectures with odd indices are held in the first auditorium, which can hold at most a students."
date: "2026-06-13T04:06:21+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1090
codeforces_index: "L"
codeforces_contest_name: "2018-2019 Russia Open High School Programming Contest (Unrated, Online Mirror, ICPC Rules, Teams Preferred)"
rating: 2000
weight: 1090
solve_time_s: 421
verified: true
draft: false
---

[CF 1090L - Berland University](https://codeforces.com/problemset/problem/1090/L)

**Rating:** 2000  
**Tags:** greedy, math  
**Solve time:** 7m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

There are `t` students and `n` lectures. A student passes if they attend at least `k` lectures.

Lectures alternate between two auditoriums. Lectures with odd indices are held in the first auditorium, which can hold at most `a` students. Lectures with even indices are held in the second auditorium, which can hold at most `b` students.

We are free to decide which students attend each lecture, as long as the capacity of the corresponding auditorium is not exceeded. A student may attend any subset of lectures.

The task is to determine the maximum number of students who can end up attending at least `k` lectures.

The values can be as large as $10^9$, which immediately rules out any simulation over students or lectures. Even an $O(n)$ algorithm is impossible because `n` itself may be $10^9$. The solution must use only a constant number of arithmetic operations.

The subtle part of the problem is that lecture attendance is not tied to specific students beforehand. We can completely rearrange attendance from lecture to lecture. What matters is the total number of available seats across all lectures of each auditorium type.

### Non-obvious edge cases

Consider:

```
10 3 4 4 5
```

There are only three lectures, but passing requires attending five lectures. No student can possibly pass.

The correct answer is:

```
0
```

A careless solution that only counts total available seats might incorrectly produce a positive answer.

Now consider:

```
5 4 5 3 3
```

There are two lectures in each auditorium type.

Total available seats:

```
2 * 5 + 2 * 3 = 16
```

Each passing student needs three attendances.

Since $16 / 3 = 5$, all five students can pass.

The correct answer is:

```
5
```

This example shows that the answer is not determined by the smaller auditorium alone.

Another important case is:

```
100000 100000 100000 100000 1
```

Passing requires only one lecture.

Every student can attend exactly one lecture and pass.

The answer is:

```
100000
```

The number of students itself becomes the limiting factor.

## Approaches

A brute-force mindset would try to assign students to lectures and track how many lectures each student attends. This quickly becomes impossible because both the number of students and the number of lectures may reach $10^9$.

The key observation is that the identities of students do not matter. We only care about how many attendance slots exist.

Suppose we want exactly `x` students to pass.

Each of these students must attend at least `k` lectures. Across all passing students, we need at least:

$$x \cdot k$$

attendance slots.

How many attendance slots are available?

Let

$$o = \left\lceil \frac{n}{2} \right\rceil$$

be the number of odd-indexed lectures and

$$e = \left\lfloor \frac{n}{2} \right\rfloor$$

be the number of even-indexed lectures.

The total number of available seats over the entire course is

$$S = o \cdot a + e \cdot b.$$

If we want `x` students to pass, we need

$$xk \le S.$$

At first glance this suggests

$$x \le \left\lfloor \frac{S}{k} \right\rfloor.$$

However, there is one more restriction. A single student cannot attend more than all available lectures.

A student can attend at most `n` lectures. If `k > n`, passing is impossible.

If `k ≤ n`, then the attendance slots can always be distributed among the chosen students. The only remaining limitation is that we cannot pass more than `t` students.

Hence the answer becomes:

$$\min\left(t,\left\lfloor\frac{S}{k}\right\rfloor\right).$$

The only exception is when `k > n`, in which case the answer is zero.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force attendance assignment | Impossible for constraints | Impossible | Too slow |
| Arithmetic counting | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute the number of lectures held in the first auditorium:

$$o = \frac{n+1}{2}$$

using integer division.
2. Compute the number of lectures held in the second auditorium:

$$e = \frac{n}{2}.$$
3. If `k > n`, output `0`.

No student can attend more than `n` lectures.
4. Compute the total number of attendance slots:

$$S = o \cdot a + e \cdot b.$$
5. Compute the maximum number of students that could receive at least `k` attendances:

$$\left\lfloor \frac{S}{k} \right\rfloor.$$
6. The final answer is the smaller of this value and `t`, because there are only `t` students available.

### Why it works

Every passing student consumes at least `k` attendance slots. Since there are exactly `S` attendance slots available during the whole course, no more than $\lfloor S/k \rfloor$ students can pass.

Conversely, when `k ≤ n`, any collection of `x` students with

$$xk \le S$$

can be assigned enough lecture visits. The only resource being consumed is attendance capacity, and the total capacity is exactly `S`. Since a student may attend up to all `n` lectures, there is no additional bottleneck.

Thus the maximum feasible number of passing students is exactly

$$\min\left(t,\left\lfloor\frac{S}{k}\right\rfloor\right).$$

## Python Solution

```python
import sys
input = sys.stdin.readline

t, n, a, b, k = map(int, input().split())

if k > n:
    print(0)
else:
    odd_lectures = (n + 1) // 2
    even_lectures = n // 2

    total_slots = odd_lectures * a + even_lectures * b

    print(min(t, total_slots // k))
```

The implementation follows the mathematical derivation directly.

The first check handles the only impossible scenario, namely requiring more lecture attendances than exist in the course.

The counts of odd and even lectures are computed with integer arithmetic. For odd `n`, the first auditorium receives one extra lecture because lecture numbering starts from one.

All calculations fit comfortably inside 64-bit integers. The largest possible value is roughly

$$10^9 \cdot 10^9 = 10^{18},$$

which is still safe in Python.

## Worked Examples

### Example 1

Input:

```
10 3 4 4 3
```

| Variable | Value |
| --- | --- |
| t | 10 |
| n | 3 |
| a | 4 |
| b | 4 |
| k | 3 |
| odd lectures | 2 |
| even lectures | 1 |
| total slots | 12 |
| total_slots // k | 4 |
| answer | 4 |

Output:

```
4
```

There are only twelve attendance opportunities. Each passing student needs three, so at most four students can pass.

### Example 2

Input:

```
100 9 6 3 6
```

| Variable | Value |
| --- | --- |
| t | 100 |
| n | 9 |
| a | 6 |
| b | 3 |
| k | 6 |
| odd lectures | 5 |
| even lectures | 4 |
| total slots | 42 |
| total_slots // k | 7 |
| answer | 7 |

Output:

```
7
```

Forty-two attendance slots exist in total. Since every passing student needs six attendances, exactly seven students can pass.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a few arithmetic operations |
| Space | O(1) | Constant extra memory |

The constraints reach $10^9$, so any solution depending on the number of students or lectures would be infeasible. A constant-time arithmetic solution easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    t, n, a, b, k = map(int, input().split())

    if k > n:
        return "0"

    odd = (n + 1) // 2
    even = n // 2
    total = odd * a + even * b

    return str(min(t, total // k))

# provided samples
assert run("10 3 4 4 3\n") == "4"
assert run("10 3 4 4 5\n") == "0"
assert run("100000 100000 100000 100000 1\n") == "100000"
assert run("5 4 5 3 3\n") == "5"
assert run("100 9 6 3 6\n") == "7"

# custom cases
assert run("1 1 1 1 1\n") == "1"
assert run("1 1 1 1 2\n") == "0"
assert run("100 2 1 1 1\n") == "2"
assert run("1000000000 1000000000 1000000000 1000000000 1000000000\n") == "1000000000"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1 1 1` | `1` | Minimum valid instance |
| `1 1 1 1 2` | `0` | `k > n` impossibility |
| `100 2 1 1 1` | `2` | Student count limits answer |
| Large $10^9$ values | `1000000000` | Overflow safety |

## Edge Cases

Consider:

```
10 3 4 4 5
```

The algorithm first checks `k > n`. Since `5 > 3`, no student can attend enough lectures. It immediately returns:

```
0
```

Now consider:

```
5 4 5 3 3
```

We compute:

$$o = 2,\quad e = 2$$

and

$$S = 2 \cdot 5 + 2 \cdot 3 = 16.$$

Then:

$$\left\lfloor \frac{16}{3} \right\rfloor = 5.$$

Since there are exactly five students, the answer is:

```
5
```

Finally consider:

```
100000 100000 100000 100000 1
```

Every attendance slot can create a passing student because only one lecture is required. The formula gives a value much larger than the number of students, so the final `min(t, ...)` correctly caps the answer at:

```
100000
```

This demonstrates why the student count must be included in the final computation.
