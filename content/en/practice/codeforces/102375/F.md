---
title: "CF 102375F - \u041f\u0440\u0430\u0432\u0438\u043b\u044c\u043d\u044b\u0439 \u043f\u043e\u0434\u043c\u043d\u043e\u0433\u043e\u0443\u0433\u043e\u043b\u044c\u043d\u0438\u043a"
description: "We have a regular polygon with (N) vertices, and we want to keep some of those vertices so that the kept vertices themselves form a regular polygon. The goal is to minimize the number of kept vertices."
date: "2026-08-14T13:02:37+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102375
codeforces_index: "F"
codeforces_contest_name: "\u041a\u0432\u0430\u043b\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u043e\u043d\u043d\u044b\u0439 \u0440\u0430\u0443\u043d\u0434 \u0427\u0435\u043c\u043f\u0438\u043e\u043d\u0430\u0442\u0430 \u0421\u0435\u0432\u0435\u0440\u043e-\u0417\u0430\u043f\u0430\u0434\u0430 \u0420\u043e\u0441\u0441\u0438\u0438 \u0438 \u041c\u043e\u0441\u043a\u0432\u044b ICPC 2019"
rating: 0
weight: 102375
solve_time_s: 130
verified: false
draft: false
---

[CF 102375F - \u041f\u0440\u0430\u0432\u0438\u043b\u044c\u043d\u044b\u0439 \u043f\u043e\u0434\u043c\u043d\u043e\u0433\u043e\u0443\u0433\u043e\u043b\u044c\u043d\u0438\u043a](https://codeforces.com/problemset/problem/102375/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 10s  
**Verified:** no  

## Solution
## Problem Understanding

We have a regular polygon with (N) vertices, and we want to keep some of those vertices so that the kept vertices themselves form a regular polygon. The goal is to minimize the number of kept vertices.

The vertices of the original polygon are equally spaced around its circumference. If we select every (t)-th vertex, the selected vertices are also equally spaced, and we get a regular polygon with (N/t) vertices, provided that (t) divides (N). Equivalently, the number (k) of vertices in the smaller regular polygon must be a divisor of (N).

There is one restriction that matters: a polygon must have at least three vertices. So the answer is the smallest divisor of (N) that is at least (3).

The value of (N) can reach (10^{12}). That rules out algorithms that inspect a linear number of candidates, since (10^{12}) iterations is far beyond what a competitive programming solution can afford. On the other hand, (\sqrt{10^{12}}=10^6), so a trial division algorithm that checks only divisors up to the square root is easily practical.

There are two edge cases that can fool a straightforward square-root search. First, a prime number such as (N=5) has no proper divisor at all, so the answer is (5), not some nonexistent smaller polygon. Second, an even number such as (N=14) has the divisor (2), but a 2-gon is not allowed. The next possible divisor is (7), which is larger than (\sqrt{14}). A search that only checks (3,4,\ldots,\lfloor\sqrt N\rfloor) would incorrectly return (14). The special role of the divisor (2) must consequently be handled explicitly.

For (N=4), the only divisors are (1,2,4), so the answer is (4). This is another boundary case for handling the factor (2), because (N/2=2) is not a valid polygon.

## Approaches

The direct approach is to try every possible number of selected vertices (k) from (3) through (N), and check whether (k) divides (N). The first divisor found is the answer, because every valid regular subpolygon corresponds exactly to a divisor of (N). This is correct, but for (N=10^{12}) it can perform almost (10^{12}) divisibility checks, which is much too slow.

The structure of divisors gives us the needed reduction. If an integer (N) has a divisor (d) other than (1) and (N), then it also has the complementary divisor (N/d). At least one of these two is at most (\sqrt N). This means that for odd (N), if there is a valid proper divisor at all, some divisor between (3) and (\sqrt N) must exist. We can search that small range directly.

The only complication is the factor (2). If (N) is even, (2) is automatically its smallest prime divisor, but (2) cannot be the answer. Its complementary divisor (N/2) can be the smallest valid divisor and may be larger than (\sqrt N). For example, (14=2\cdot7), and (7>\sqrt{14}). We therefore treat (N/2) as an additional candidate whenever it is at least (3).

We scan divisors from (3) upward. The first divisor found is automatically the smallest possible answer. If none is found, then an odd (N) must be prime, so the answer is (N). For even (N), the remaining candidate is (N/2), except when that candidate equals (2), as happens for (N=4).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(N)) | (O(1)) | Too slow |
| Optimal | (O(\sqrt N)) | (O(1)) | Accepted |

## Algorithm Walkthrough

1. Read (N). We need the smallest divisor of (N) that is at least (3).
2. If (N=3), immediately return (3). There is no smaller valid polygon, and this also avoids any special handling around the square root.
3. If (N) is even, set a candidate answer to (N/2) when (N/2\ge3). This handles cases such as (14=2\cdot7), where the smallest valid divisor is larger than (\sqrt N). For (N=4), (N/2=2) is invalid, so the candidate remains (N).
4. Try every integer (d) from (3) through (\lfloor\sqrt N\rfloor). If (N\bmod d=0), then (d) is a valid polygon size. Since the values are tested in increasing order, the first such (d) is the smallest possible answer, so return it immediately.
5. If the search finishes without finding a divisor, return the candidate from step 3, or (N) if there was no valid candidate. For odd (N), this means (N) is prime. For even (N), it means that (N/2) is the only possible proper divisor greater than (2) that could be the answer.

Why it works: every possible regular subpolygon has a number of vertices dividing (N). Among all valid divisors, the algorithm explicitly considers the only divisor that can be hidden above (\sqrt N), namely (N/2) when (2) divides (N), while every other possible smallest divisor must be at most (\sqrt N). The ascending trial division therefore finds the smallest valid divisor whenever one exists, and the fallback handles the remaining prime or (2)-times-prime cases.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())

    # N itself is always a valid answer.
    ans = n

    # If 2 divides N, then N / 2 is the only possible
    # complementary divisor that can remain above sqrt(N).
    if n % 2 == 0 and n // 2 >= 3:
        ans = n // 2

    d = 3
    while d * d <= n:
        if n % d == 0:
            ans = d
            break
        d += 1

    print(ans)

solve()
```

The initial value `ans = n` represents the case where the original polygon itself is the smallest valid choice. Every divisor of (N) is a possible number of vertices, and (N) is always a valid one because (N\ge3).

The `n % 2 == 0` branch deals with the special divisor (2). We cannot return (2), since a regular polygon needs at least three vertices, but the complementary divisor (n/2) is valid whenever it is at least (3). This is why (N=14) produces (7), even though (7) is greater than (\sqrt{14}).

The loop starts at (3), not (2), because (2) is never a valid answer. It continues while `d * d <= n`, which is the integer form of (d\le\sqrt N) and avoids floating-point calculations. Python integers have arbitrary precision, so `d * d` cannot overflow.

As soon as a divisor is found, the loop stops. Since `d` increases from (3), that divisor is the smallest valid divisor encountered, and hence the answer.

## Worked Examples

For (N=5), the polygon is prime, so no proper divisor can represent the number of vertices of a smaller regular polygon.

| (N) | (ans) initially | (d) | (N\bmod d) | Action |
| --- | --- | --- | --- | --- |
| 5 | 5 | 3 | 2 | No divisor |
| 5 | 5 | End |  | Return 5 |

The loop stops because (3^2>5). No divisor at least (3) was found, so the original pentagon is the smallest possible regular polygon formed by its vertices. This demonstrates the prime-number case.

For (N=21), the divisors relevant to the answer are (3) and (7). The algorithm finds (3) immediately.

| (N) | (ans) initially | (d) | (N\bmod d) | Action |
| --- | --- | --- | --- | --- |
| 21 | 21 | 3 | 0 | Return 3 |

Selecting every seventh vertex of the original 21-gon leaves three equally spaced vertices, so a triangle is possible. Since no polygon with fewer than three vertices is allowed, (3) is optimal. This confirms that the first divisor in ascending order is exactly the desired answer.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(\sqrt N)) | At most (\sqrt N) candidate divisors are tested. |
| Space | (O(1)) | Only a constant number of integer variables are stored. |

With (N\le10^{12}), the loop performs at most about (10^6) iterations. That is small enough for a standard competitive programming time limit, while the (O(N)) brute-force approach could require up to roughly (10^{12}) divisibility checks.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline
    n = int(input())

    ans = n

    if n % 2 == 0 and n // 2 >= 3:
        ans = n // 2

    d = 3
    while d * d <= n:
        if n % d == 0:
            ans = d
            break
        d += 1

    print(ans)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()
    out = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout

    return out

# Provided samples
assert run("5\n") == "5\n", "sample 1"
assert run("21\n") == "3\n", "sample 2"

# Minimum-size input
assert run("3\n") == "3\n", "minimum N"

# N = 4 has divisors 1, 2, 4, and 2 is not a valid polygon
assert run("4\n") == "4\n", "N/2 must not be used when it equals 2"

# 14 = 2 * 7, and 7 is larger than sqrt(14)
assert run("14\n") == "7\n", "even number with answer above sqrt(N)"

# Large boundary value
assert run("1000000000000\n") == "4\n", "maximum N"

# Odd composite whose smallest valid divisor is found by the loop
assert run("49\n") == "7\n", "square of a prime"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3` | `3` | Minimum allowed polygon size |
| `4` | `4` | Correct treatment of the invalid divisor (2) |
| `14` | `7` | Even case where the answer is greater than (\sqrt N) |
| `1000000000000` | `4` | Maximum input boundary and efficient search |
| `49` | `7` | Proper divisor found exactly at (\sqrt N) |

## Edge Cases

For (N=5), the algorithm starts with `ans = 5` and does not create an even-number candidate. The loop would need to test divisors beginning at (3), but (3^2>5), so it performs no useful divisor test and returns (5). A careless implementation that assumes every polygon has a smaller regular subpolygon could incorrectly search for a nonexistent divisor.

For (N=14), the algorithm first sets `ans = 7`, because (14/2=7). The loop tests (d=3), but (14\bmod3\ne0), and then stops because (4^2>14). The stored answer (7) is returned. This is the critical case showing why checking only up to (\sqrt N) is insufficient when the factor (2) is forbidden as an answer.

For (N=4), `n // 2` equals (2), so the even-number branch deliberately does not update `ans`. The loop has no (d\ge3) satisfying (d^2\le4), and the algorithm returns (4). Returning (N/2) unconditionally would produce (2), which does not describe a polygon.

For (N=49), the loop reaches (d=7), and (7^2=49), so the boundary condition `d * d <= n` includes this divisor. Since (7\mid49), the algorithm returns (7). Using `d * d < n` instead would skip the exact-square divisor and incorrectly return (49).

For (N=10^{12}), the algorithm needs only a small number of trial divisions before finding (4). The input itself is huge compared with the number of vertices a linear algorithm could inspect, but its square root is only (10^6), which is precisely why the divisor-based reduction makes the problem tractable.
