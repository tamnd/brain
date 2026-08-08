---
title: "CF 102441H - Not A + B"
description: "For each test case, we receive two positive integers a and b. We have to print some integer c between 1 and 50 such that c is different from a + b. There is no requirement to find the smallest or largest valid value, so any value satisfying the condition is accepted."
date: "2026-08-08T13:36:53+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102441
codeforces_index: "H"
codeforces_contest_name: "2018-2019 9th BSUIR Open Programming Championship. Final"
rating: 0
weight: 102441
solve_time_s: 56
verified: true
draft: false
---

[CF 102441H - Not A + B](https://codeforces.com/problemset/problem/102441/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 56s  
**Verified:** yes  

## Solution
## Problem Understanding

For each test case, we receive two positive integers `a` and `b`. We have to print some integer `c` between `1` and `50` such that `c` is different from `a + b`. There is no requirement to find the smallest or largest valid value, so any value satisfying the condition is accepted.

The bounds make the problem extremely small. There are at most `10^3` test cases, and both input numbers are at most `50`. Even an approach that checks every possible value of `c` from `1` through `50` performs at most `50 * 10^3 = 50,000` checks, which is far below what a one-second limit can challenge. The constraints do not rule out brute force at all. The real goal is to recognize that the bounds on `a` and `b` give us an even simpler constant answer.

The key edge case is the smallest possible values. If `a = 1` and `b = 1`, their sum is `2`, so `c = 1` is still valid. A careless solution might think that choosing one of the input numbers is unsafe, but here `a` and `b` are both positive, so their sum is always strictly greater than either individual number. For example, for input `1 1`, outputting `1` is correct because `1 != 2`.

The same reasoning handles the largest values. If `a = 50` and `b = 50`, the sum is `100`, while `c` must be at most `50`. Thus every permitted value of `c` is automatically different from the sum. In particular, `c = 1` is valid.

The important boundary is not actually the upper limit of `50`, but the fact that both `a` and `b` are at least `1`. Because of that, `a + b >= 2`, so the fixed value `c = 1` can never equal the sum.

The statement's sample formatting is damaged in the supplied text. The original sample has three test cases, `(1, 2)`, `(3, 4)`, and `(5, 6)`, with one possible output being `12`, `34`, and `42`. Those outputs demonstrate that the answer is not unique.

## Approaches

A direct brute-force solution would try every candidate `c` from `1` to `50` and stop as soon as it finds one satisfying `c != a + b`. This is correct because the loop examines every value allowed by the output constraints, so if a solution exists, the loop will encounter it. Under the given constraints, even the worst case performs only `50` comparisons per test case, or at most `50,000` comparisons for all `10^3` test cases. Thus brute force is not too slow here and is fully accepted.

The brute-force approach works because the candidate range is tiny, but we can do better by looking at the arithmetic structure. Since `a >= 1` and `b >= 1`, we always have `a + b >= 2`. The value `1` is an allowed output, and it can never equal a sum of two positive input values. That eliminates the search completely.

The observation that `1` is guaranteed to be different from `a + b` lets us replace up to `50` candidate checks with one assignment. We do not even need to calculate the sum.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(50t), effectively O(t) | O(1) | Accepted |
| Optimal | O(t) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `t`. Each test case is independent, so the same fixed construction can be used every time.
2. For each pair `a, b`, output `1`. This is the right choice because both numbers are positive, so `a + b` is at least `2`.
3. Repeat this for all test cases. There is no need to inspect the actual values of `a` and `b`, because the lower bound `1` is enough to prove the answer is valid.

### Why it works

For every test case, `a >= 1` and `b >= 1`. Hence `a + b >= 2`. The algorithm outputs `c = 1`, so `c < a + b` and consequently `c != a + b`. Also, `1 <= c <= 50`, so the output satisfies the required range. The same argument applies independently to every test case, which proves that the algorithm can never produce an invalid answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())

for _ in range(t):
    a, b = map(int, input().split())
    print(1)
```

The first line reads the number of test cases. We then process exactly `t` pairs, matching the input format.

The values `a` and `b` are read even though the implementation does not need to use them. Reading them is necessary to consume the input correctly and advance to the next test case.

The output is always `1`. There is no sum calculation, comparison, loop over candidate values, or special case because the positivity of `a` and `b` already proves that `1` cannot equal their sum.

There are no overflow concerns because the given values are tiny, and the implementation does not perform any arithmetic on them anyway. There is also no off-by-one issue in the test-case loop because it executes exactly once for every input pair.

## Worked Examples

Consider the official sample input:

```
3
1 2
3 4
5 6
```

Our construction does not attempt to reproduce the sample output exactly, because the problem accepts any valid `c`.

| Test case | a | b | a + b | c | Valid? |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 2 | 3 | 1 | Yes |
| 2 | 3 | 4 | 7 | 1 | Yes |
| 3 | 5 | 6 | 11 | 1 | Yes |

The first test case also covers the smallest possible value of `a`. Although `a` itself is `1`, the sum is `3`, so printing `1` is completely valid. The other two cases demonstrate that the same construction works without considering the actual size of the sum.

For a second example, consider the maximum possible input values:

```
2
50 50
1 1
```

| Test case | a | b | a + b | c | Valid? |
| --- | --- | --- | --- | --- | --- |
| 1 | 50 | 50 | 100 | 1 | Yes |
| 2 | 1 | 1 | 2 | 1 | Yes |

The first row shows that even when the sum is larger than the entire allowed range for `c`, the fixed answer works. The second row shows the exact minimum possible sum, `2`, which is still larger than `1`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case requires one read and one output. |
| Space | O(1) | Only the current pair of integers and the loop state are stored. |

With at most `10^3` test cases, the algorithm performs only a constant amount of work per case. This is comfortably within the one-second time limit and uses negligible memory compared with the 256 MB limit.

## Test Cases

Because the problem allows multiple correct outputs, the most robust tests verify that every produced value is in `[1, 50]` and differs from `a + b`, rather than requiring a particular valid answer.

```python
import sys
import io

def solve():
    input = sys.stdin.readline

    t = int(input())

    for _ in range(t):
        a, b = map(int, input().split())
        print(1)

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

def validate(inp: str, out: str):
    input_lines = inp.strip().splitlines()
    t = int(input_lines[0])

    tests = []
    for line in input_lines[1:]:
        a, b = map(int, line.split())
        tests.append((a, b))

    answers = list(map(int, out.strip().split()))

    assert len(answers) == t

    for (a, b), c in zip(tests, answers):
        assert 1 <= c <= 50
        assert c != a + b

# Provided sample input.
sample = """\
3
1 2
3 4
5 6
"""
sample_output = run(sample)
validate(sample, sample_output)

# Minimum-size input.
case_min = """\
1
1 1
"""
assert run(case_min) == "1\n"

# Maximum-size input.
case_max = """\
3
50 50
50 1
1 50
"""
assert run(case_max) == "1\n1\n1\n"
validate(case_max, run(case_max))

# All values equal.
case_equal = """\
4
7 7
25 25
49 49
50 50
"""
assert run(case_equal) == "1\n1\n1\n1\n"
validate(case_equal, run(case_equal))

# Boundary sums around the smallest and largest possible values.
case_boundaries = """\
4
1 1
1 2
49 50
50 50
"""
assert run(case_boundaries) == "1\n1\n1\n1\n"
validate(case_boundaries, run(case_boundaries))
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3 / 1 2 / 3 4 / 5 6` | `1 / 1 / 1` | Provided sample structure and non-unique output |
| `1 / 1 1` | `1` | Minimum input values and minimum possible sum |
| `3 / 50 50 / 50 1 / 1 50` | `1 / 1 / 1` | Maximum input values and boundary of the allowed `c` range |
| `4 / 7 7 / 25 25 / 49 49 / 50 50` | `1 / 1 / 1 / 1` | Equal inputs across the full value range |
| `4 / 1 1 / 1 2 / 49 50 / 50 50` | `1 / 1 / 1 / 1` | Smallest and largest possible sums |

## Edge Cases

The minimum case is `a = 1, b = 1`. The algorithm outputs `1`. Their sum is `2`, so the condition `c != a + b` becomes `1 != 2`, which is true. The exact input is `1\n1 1\n`, and the output is `1`.

The case where one input is itself `1` can sometimes cause an unnecessary special case in a careless solution. For `a = 1, b = 2`, the algorithm still outputs `1`. The sum is `3`, so the answer is valid. There is no reason to avoid `1` merely because one of the input values equals `1`.

At the other boundary, consider `a = 50, b = 50`. The sum is `100`, which is outside the permitted output range. The algorithm outputs `1`, and since `1 != 100`, the answer is valid. In fact, every allowed value of `c` would work for this particular test.

Finally, consider equal inputs such as `a = 25, b = 25`. Their sum is `50`, so a careless solution that always outputs `50` would fail. The fixed construction outputs `1`, and `1 != 50`, so it avoids this boundary collision without needing to inspect the sum. This illustrates why choosing the smallest allowed value is stronger than choosing a value near the upper boundary.
