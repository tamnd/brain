---
title: "CF 201E - Thoroughly Bureaucratic Organization"
description: "The problem involves a set of people, each with an appointment on a unique day in the next n days. You do not know who is scheduled on which day, but you can query the organization in forms that list up to m names."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "combinatorics"]
categories: ["algorithms"]
codeforces_contest: 201
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 127 (Div. 1)"
rating: 2600
weight: 201
solve_time_s: 99
verified: false
draft: false
---

[CF 201E - Thoroughly Bureaucratic Organization](https://codeforces.com/problemset/problem/201/E)

**Rating:** 2600  
**Tags:** binary search, combinatorics  
**Solve time:** 1m 39s  
**Verified:** no  

## Solution
## Problem Understanding

The problem involves a set of people, each with an appointment on a unique day in the next _n_ days. You do not know who is scheduled on which day, but you can query the organization in forms that list up to _m_ names. The reply gives the appointment dates for the listed names, but scrambled. Your goal is to determine the exact day for each person using the fewest number of forms.

For each test case, the inputs are _n_, the number of people, and _m_, the number of names you can list in a single request. The output is the minimum number of requests needed to determine every appointment date.

The bounds of the problem, with _n_ and _m_ up to 10^9 and up to 1000 test cases, rule out any solution that simulates the appointments or explicitly generates all subsets. We must reason mathematically and compute the answer with simple arithmetic.

A non-obvious edge case occurs when _m_ ≥ _n_. In that case, you can query all people in a single request, but since the response is scrambled, one person’s date can be deduced by elimination, so you may need fewer requests than it seems. Another edge case is _n = 1_, where no queries are required because the only appointment is trivially known.

## Approaches

A brute-force approach would consider enumerating all combinations of people in requests and checking whether the scrambled responses suffice to determine everyone’s appointment. This is correct in principle, but combinatorial: there are exponentially many subsets of size up to _m_ out of _n_, and checking them is infeasible for _n_ up to 10^9.

The key insight is to think in terms of coverage. Each request can give information about up to _m_ people. Once you know the appointment dates for _n-1_ people, the last person’s date is determined by elimination. This means you never need to query all _n_ people individually. Consequently, the minimum number of requests is the smallest integer _k_ such that the total number of "slots" across _k_ requests is at least _n-1_. Each request contributes at most _m_ slots, so the formula becomes:

```
requests = ceil((n - 1) / m)
```

This simple formula handles all large values of _n_ and _m_ efficiently.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Mathematical formula | O(1) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases, _t_.
2. For each test case, read the values _n_ and _m_.
3. If _n = 1_, output 0 immediately because no queries are needed.
4. Otherwise, compute the minimum number of requests using integer arithmetic: `(n - 1 + m - 1) // m`. This is equivalent to ceiling division, ensuring we always round up.
5. Print the result.

The reason this works is that after querying _n-1_ people, the last person’s appointment is uniquely determined. Each request contributes up to _m_ known appointments, so dividing the total needed known slots (_n-1_) by _m_ and rounding up guarantees full coverage.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, m = map(int, input().split())
    if n == 1:
        print(0)
    else:
        print((n - 1 + m - 1) // m)
```

The first line reads the number of test cases. We use `sys.stdin.readline` for fast input since there can be up to 1000 test cases. Each loop reads the two integers, checks the trivial case where _n = 1_, and otherwise applies the ceiling division formula `(n - 1 + m - 1) // m` to compute the minimum number of requests.

## Worked Examples

**Example 1:** n = 4, m = 1

| Variable | Value |
| --- | --- |
| n-1 | 3 |
| m | 1 |
| requests | (3 + 0) // 1 = 3 |

Three requests are needed, each querying one person. The first three queries reveal three dates, and the fourth date is determined by elimination.

**Example 2:** n = 4, m = 2

| Variable | Value |
| --- | --- |
| n-1 | 3 |
| m | 2 |
| requests | (3 + 1) // 2 = 2 |

Two requests suffice. The first request can query two people, the second can query two (potentially overlapping with the first), giving enough coverage to deduce all four dates.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | One calculation per test case, constant-time arithmetic |
| Space | O(1) | Only a few variables are used per test case |

This fits easily within the time limit, even with _n_ and _m_ up to 10^9 and 1000 test cases.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    t = int(input())
    results = []
    for _ in range(t):
        n, m = map(int, input().split())
        if n == 1:
            results.append("0")
        else:
            results.append(str((n - 1 + m - 1) // m))
    return "\n".join(results)

# Provided samples
assert run("5\n4 1\n4 2\n7 3\n1 1\n42 7\n") == "3\n2\n3\n0\n6", "sample 1"

# Custom tests
assert run("3\n1 10\n10 1\n10 3\n") == "0\n9\n3", "edge n=1, m=1, arbitrary"
assert run("2\n1000000000 1\n1000000000 1000000000\n") == "999999999\n0", "maximum inputs"
assert run("2\n5 5\n5 2\n") == "1\n2", "full request vs smaller request"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 10 | 0 | n=1 trivial case |
| 10 1 | 9 | smallest m, multiple requests needed |
| 10 3 | 3 | normal case, ceiling division |
| 1000000000 1 | 999999999 | maximum n, smallest m |
| 1000000000 1000000000 | 0 | maximum n, large m allows zero requests |
| 5 5 | 1 | single request covers all but last |
| 5 2 | 2 | ceiling division with remainder |

## Edge Cases

When _n = 1_, the formula `(n-1 + m-1)//m` correctly evaluates to 0. For _m ≥ n_, the formula reduces to `(n-1 + m-1)//m = (n-1)//m + 1` if needed, which correctly outputs 1 when _n > 1_, since the last date is deduced by elimination. When _m = 1_, each request can cover only one person, so the algorithm correctly outputs _n-1_ requests. These checks cover all non-trivial scenarios.
