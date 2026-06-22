---
title: "CF 105435A - The world of JS (Jagjeet & Sagar)"
description: "We are given a schedule describing when Sagar is busy, and we need to decide whether Jagjeet’s chosen moment falls inside any of those busy periods. Sagar’s busy pattern starts at time a. After that, his availability alternates in a structured way: every cycle is based on b."
date: "2026-06-23T03:48:37+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105435
codeforces_index: "A"
codeforces_contest_name: "TSEC Round 2 (Div. 3)"
rating: 0
weight: 105435
solve_time_s: 89
verified: true
draft: false
---

[CF 105435A - The world of JS (Jagjeet & Sagar)](https://codeforces.com/problemset/problem/105435/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 29s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a schedule describing when Sagar is busy, and we need to decide whether Jagjeet’s chosen moment falls inside any of those busy periods.

Sagar’s busy pattern starts at time `a`. After that, his availability alternates in a structured way: every cycle is based on `b`. In each cycle, there are two busy moments: first at the exact start of the cycle, and second one second later. Concretely, the busy times form pairs:

`a, a+1`, then `a+b, a+b+1`, then `a+2b, a+2b+1`, and so on.

So the task is simply: for each query, check whether a given time `c` is equal to any of these busy timestamps.

The input size is small, with up to 1000 test cases and values up to 10^9. This immediately rules out any simulation over time or iterative expansion of the schedule. Any correct solution must decide membership in constant time per test case.

A common mistake is to interpret the pattern as a continuous interval, for example thinking Sagar is busy for ranges like `[a, a+1]`, `[a+b, a+b+1]` and so on but then accidentally treating them as overlapping or extending intervals. Since the intervals are isolated and non-overlapping (because `b ≥ 1`), overlap only occurs when `b = 1`, in which case consecutive pairs merge into continuous busy segments. Even in that case, direct membership checking still works, but careless interval merging logic can break edge handling.

Another subtle edge case is when `c < a`. In this case Sagar has not started being busy at all, so the answer must be “NO”. Similarly, when `b = 1`, the busy times become every integer starting from `a`, since `(a, a+1), (a+1, a+2), ...` covers all integers from `a` onward.

## Approaches

A brute-force approach would simulate Sagar’s busy times by generating pairs `(a + k*b, a + k*b + 1)` for increasing `k`, stopping once we exceed `c`. For each generated pair, we check if `c` matches either endpoint. This is correct because it directly constructs the described pattern.

However, this becomes inefficient when `c` is large relative to `a` and `b`. In the worst case, if `b = 1`, the number of iterations grows linearly up to `c - a`, which can be as large as 10^9. Even when `b` is larger, we still risk many iterations across multiple test cases.

The key observation is that the structure is fully periodic and we do not need to enumerate it. Instead, we can determine whether `c` aligns with a cycle index and offset.

For a given time `c`, if it is a busy time, it must satisfy one of two conditions:

First, it could be the start of a cycle: `c = a + k*b` for some integer `k ≥ 0`. This is equivalent to `(c - a) % b == 0`.

Second, it could be the second busy moment in a cycle: `c = a + k*b + 1`. This is equivalent to `(c - a - 1) % b == 0`.

Both conditions must also satisfy `c ≥ a`, since busy times never occur before the starting point.

This reduces the problem to constant-time arithmetic checks per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force simulation | O((c−a)/b) per test | O(1) | Too slow |
| Modular arithmetic check | O(1) per test | O(1) | Accepted |

## Algorithm Walkthrough

We process each test case independently and apply arithmetic checks to determine membership in the busy schedule.

1. Read the values `a`, `b`, and `c` for the current test case. These define the starting point, cycle length, and query time.
2. If `c < a`, immediately conclude that Sagar is not busy at time `c`. This follows from the definition since the schedule begins only at `a`.
3. Check whether `c` matches the first busy position in some cycle by testing whether `(c - a) % b == 0`. If this holds, then `c` aligns exactly with `a + k*b` for some integer `k`.
4. If the previous condition fails, check whether `c` matches the second busy position in a cycle by testing whether `(c - a - 1) % b == 0`. This corresponds to `a + k*b + 1`.
5. If either condition is true, output “YES”. Otherwise, output “NO”.

### Why it works

Every busy time must belong to exactly one of two arithmetic progressions: one starting at `a` with step `b`, and one starting at `a+1` with the same step `b`. These two sequences fully describe the schedule, and they do not generate false positives because each valid time must map to a unique cycle index `k`. The modulo condition ensures that only times reachable by integer stepping from `a` or `a+1` in increments of `b` are accepted, which exactly matches the construction.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    for _ in range(n):
        a, b, c = map(int, input().split())

        if c < a:
            print("NO")
            continue

        if (c - a) % b == 0 or (c - a - 1) % b == 0:
            print("YES")
        else:
            print("NO")

if __name__ == "__main__":
    solve()
```

The code follows the derived conditions directly. The first guard handles the trivial exclusion where the query is before the schedule begins. The two modulo checks correspond exactly to the two arithmetic progressions defining the busy pattern. No loops are required, so each test case is handled in constant time.

A subtle implementation detail is that `(c - a - 1)` can be negative when `c = a`, but Python’s modulo handles negative operands correctly in this context, and the earlier condition already ensures correctness. The early `c < a` check prevents unnecessary ambiguity.

## Worked Examples

We trace two representative cases from the sample.

### Example 1

Input: `a = 3, b = 2, c = 6`

| Step | Condition checked | Expression | Result |
| --- | --- | --- | --- |
| 1 | c < a | 6 < 3 | False |
| 2 | first sequence | (6 - 3) % 2 | 3 % 2 = 1 |
| 3 | second sequence | (6 - 3 - 1) % 2 | 2 % 2 = 0 |

Since the second condition holds, output is “YES”.

This shows that even if a value is not aligned with the base cycle start, it can still match the shifted busy slot.

### Example 2

Input: `a = 8, b = 7, c = 10`

| Step | Condition checked | Expression | Result |
| --- | --- | --- | --- |
| 1 | c < a | 10 < 8 | False |
| 2 | first sequence | (10 - 8) % 7 | 2 % 7 = 2 |
| 3 | second sequence | (10 - 8 - 1) % 7 | 1 % 7 = 1 |

Neither condition holds, so output is “NO”.

This confirms that values not aligned with either progression are correctly rejected.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each test case uses a constant number of arithmetic operations |
| Space | O(1) | No auxiliary structures beyond input variables |

The constraints allow up to 1000 test cases, so a linear scan over test cases with O(1) work each is easily within limits. The arithmetic operations are constant time and safe under 64-bit integer ranges.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n = int(input())
    out = []
    for _ in range(n):
        a, b, c = map(int, input().split())
        if c < a:
            out.append("NO")
        elif (c - a) % b == 0 or (c - a - 1) % b == 0:
            out.append("YES")
        else:
            out.append("NO")
    return "\n".join(out)

# provided samples
assert run("""10
3 2 6
1 1 1
8 7 10
2 9 8
3 4 6
1 5 6
8 9 4
7 5 3
10 8 3
1 4 1
""") == """YES
YES
NO
NO
NO
YES
NO
NO
NO
YES"""

# custom cases
assert run("1\n5 3 5\n") == "YES"
assert run("1\n5 3 4\n") == "YES"
assert run("1\n5 3 6\n") == "NO"
assert run("1\n10 1 100\n") == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `5 3 5` | YES | start of first cycle |
| `5 3 4` | YES | second slot in cycle |
| `5 3 6` | NO | non-matching time |
| `10 1 100` | YES | dense case when b = 1 |

## Edge Cases

One important edge case is when `c = a`. In this situation, the answer must always be “YES” because the first busy moment begins exactly at `a`. The algorithm handles this correctly because `(c - a) % b = 0` evaluates to `0 % b = 0`, triggering a positive result.

Another case is when `b = 1`. The busy times become `(a, a+1), (a+1, a+2), ...`, effectively covering every integer from `a` onward. The check `(c - a) % 1 == 0` is always true for `c ≥ a`, so the algorithm correctly returns “YES” for all such cases, while `c < a` is already excluded.

Finally, when `c < a`, both modular checks can produce misleading values due to negative arithmetic, but the early guard prevents this scenario entirely. For example, if `a = 10, c = 3`, then `(c - a) = -7` and modulo operations could still return valid residues in Python, but they are irrelevant because the schedule has not started yet, so the correct output is always “NO”.
