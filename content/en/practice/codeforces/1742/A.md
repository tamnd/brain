---
title: "CF 1742A - Sum"
description: "For each test case, we receive three integers. The task is to determine whether any one of these three numbers can be expressed as the sum of the other two."
date: "2026-06-09T16:12:51+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1742
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 827 (Div. 4)"
rating: 800
weight: 1742
solve_time_s: 119
verified: true
draft: false
---

[CF 1742A - Sum](https://codeforces.com/problemset/problem/1742/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 1m 59s  
**Verified:** yes  

## Solution
## Problem Understanding

For each test case, we receive three integers. The task is to determine whether any one of these three numbers can be expressed as the sum of the other two.

Since there are only three values, there are exactly three possible ways the condition can be true:

If `a + b = c`, or `a + c = b`, or `b + c = a`.

The constraints are extremely small. Even the maximum number of test cases is only 9261, and each test case contains just three integers between 0 and 20. This means we can afford to check every possible relationship directly. The total amount of work is tiny, only a few arithmetic operations per test case.

A subtle edge case appears when zeros are involved.

Consider:

```
0 0 0
```

The correct answer is `YES` because `0 + 0 = 0`. A careless solution that assumes the sum must be strictly larger than the addends would incorrectly return `NO`.

Another edge case occurs when all numbers are equal but nonzero.

```
20 20 20
```

The correct answer is `NO`. None of the numbers equals the sum of the other two because `20 + 20 = 40`. A careless solution that only checks whether two values are equal could mistakenly return `YES`.

One more case is when the largest number is not given in a particular position.

```
15 7 8
```

The correct answer is `YES` because `7 + 8 = 15`. A solution that checks only `a + b == c` would miss this valid configuration.

## Approaches

The most direct brute-force idea is to test every possible choice of a target number. Since there are only three numbers, we can check whether the first equals the sum of the other two, whether the second equals the sum of the other two, and whether the third equals the sum of the other two.

This approach is correct because these three checks exactly cover every way one number could be the sum of the remaining two.

For each test case, we perform three additions and three comparisons. Even at the maximum of 9261 test cases, this is only a few tens of thousands of operations, which is trivial.

The key observation is that the problem itself already has only three possible cases. There is no need for sorting, searching, or any more elaborate technique. The entire task reduces to evaluating the three valid equations directly.

The brute-force and optimal solutions are effectively the same here because the search space is constant.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(1) | O(1) | Accepted |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases.
2. For each test case, read `a`, `b`, and `c`.
3. Check whether `a + b == c`.

If this is true, one number is the sum of the other two, so the answer is `YES`.
4. Check whether `a + c == b`.

This covers the case where the second number is the sum.
5. Check whether `b + c == a`.

This covers the remaining possibility where the first number is the sum.
6. If at least one of the three checks is true, print `YES`. Otherwise print `NO`.

### Why it works

Exactly one of three numbers can only be the sum of the other two in one of three equations:

`a + b = c`, `a + c = b`, or `b + c = a`.

The algorithm checks all three possibilities. If any valid relationship exists, one of these comparisons succeeds and the algorithm prints `YES`. If all three comparisons fail, then no number equals the sum of the other two, so the correct answer is `NO`.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())

for _ in range(t):
    a, b, c = map(int, input().split())

    if a + b == c or a + c == b or b + c == a:
        print("YES")
    else:
        print("NO")
```

The first line reads the number of test cases. Each iteration reads three integers.

The condition inside the `if` statement directly implements the three equations discussed in the algorithm. Using logical OR means the answer becomes `YES` as soon as any valid sum relationship is found.

There are no boundary-condition concerns beyond checking all three possibilities. The numbers are very small, so integer overflow is impossible in Python. The order of the checks does not matter because every valid configuration is tested.

## Worked Examples

### Example 1

Input:

```
1
1 4 3
```

| a | b | c | a+b==c | a+c==b | b+c==a | Answer |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 4 | 3 | False | True | False | YES |

Here, `1 + 3 = 4`, so the second condition succeeds. The example shows why we must check all three equations rather than only `a + b == c`.

### Example 2

Input:

```
1
20 20 20
```

| a | b | c | a+b==c | a+c==b | b+c==a | Answer |
| --- | --- | --- | --- | --- | --- | --- |
| 20 | 20 | 20 | False | False | False | NO |

All numbers are equal, but none equals the sum of the other two. This demonstrates that equality alone is not sufficient.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Three comparisons per test case |
| Space | O(1) | Only a few integer variables are stored |

The work done for each test case is constant and independent of the input values. Even at the maximum number of test cases, the running time is far below the limit and memory usage is negligible.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline
    t = int(input())
    out = []

    for _ in range(t):
        a, b, c = map(int, input().split())

        if a + b == c or a + c == b or b + c == a:
            out.append("YES")
        else:
            out.append("NO")

    return "\n".join(out)

# provided sample
assert run(
"""7
1 4 3
2 5 8
9 11 20
0 0 0
20 20 20
4 12 3
15 7 8
"""
) == """YES
NO
YES
YES
NO
NO
YES""", "sample 1"

# minimum values
assert run(
"""1
0 0 0
"""
) == "YES", "all zeros"

# maximum values
assert run(
"""1
20 20 20
"""
) == "NO", "all maximum values"

# largest value is first
assert run(
"""1
15 7 8
"""
) == "YES", "must check all permutations"

# simple negative case
assert run(
"""1
4 12 3
"""
) == "NO", "no valid sum relation"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 0 0` | `YES` | Zero values still satisfy the condition |
| `20 20 20` | `NO` | Equal values do not automatically work |
| `15 7 8` | `YES` | The summed value may appear in any position |
| `4 12 3` | `NO` | Correct rejection when no equation holds |

## Edge Cases

Consider the input:

```
1
0 0 0
```

The algorithm evaluates:

`0 + 0 == 0`, which is true.

Since one of the checks succeeds, it prints `YES`. This correctly handles the special case where all values are zero.

Consider the input:

```
1
20 20 20
```

The algorithm evaluates:

`20 + 20 == 20` → false

`20 + 20 == 20` → false

`20 + 20 == 20` → false

All checks fail, so it prints `NO`. This correctly handles equal nonzero values.

Consider the input:

```
1
15 7 8
```

The algorithm evaluates:

`15 + 7 == 8` → false

`15 + 8 == 7` → false

`7 + 8 == 15` → true

The third condition succeeds, so the answer is `YES`. This shows why checking only one ordering would be incorrect.
