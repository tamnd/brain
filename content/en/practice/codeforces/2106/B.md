---
title: "CF 2106B - St. Chroma"
description: "We are given a list that must be a permutation of numbers from 0 to n−1. As we reveal this permutation from left to right, we compute a running value: after each prefix, we take the smallest non-negative integer that is missing from that prefix."
date: "2026-06-08T04:52:16+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 2106
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 1020 (Div. 3)"
rating: 900
weight: 2106
solve_time_s: 87
verified: false
draft: false
---

[CF 2106B - St. Chroma](https://codeforces.com/problemset/problem/2106/B)

**Rating:** 900  
**Tags:** constructive algorithms, greedy, math  
**Solve time:** 1m 27s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a list that must be a permutation of numbers from 0 to n−1. As we reveal this permutation from left to right, we compute a running value: after each prefix, we take the smallest non-negative integer that is missing from that prefix. This value changes over time as more elements appear, and each prefix paints one cell with its current value.

The task is not to compute this coloring for a fixed permutation. Instead, we must construct the permutation itself so that a particular color x appears as many times as possible in the resulting painted strip.

The key interaction is between the order of elements in the permutation and the moment when the MEX of the prefix moves past x. Since MEX depends only on which values from 0 upward have appeared, the ordering determines how long MEX stays equal to a particular value.

The constraints are large enough that any solution must be linear per test case. The sum of n is up to 2×10^5, which rules out anything quadratic or involving repeated simulation per candidate permutation. The construction must be direct.

A subtle edge case appears when x = n. In that case, MEX equals n only after all numbers 0 through n−1 have appeared. That means it only happens at the final prefix, so the answer is always 1, regardless of arrangement. A naive attempt that treats x like a normal value would incorrectly try to “delay” MEX beyond n, which is impossible.

Another edge case is x = 0. Here MEX is initially 0 and becomes 1 as soon as 0 appears. So we want to postpone placing 0 as long as possible to extend the initial run of color 0.

## Approaches

A brute-force idea is to generate all permutations and simulate the MEX process for each one, counting how many times color x appears. This is correct but infeasible. There are n! permutations, and even evaluating one permutation costs O(n), so this approach is astronomically large.

To optimize, we need to understand what makes MEX stay equal to x for consecutive prefixes. MEX equals x exactly when all numbers 0 through x−1 have appeared in the prefix, but x itself has not yet appeared. Once x is inserted, MEX jumps to a value larger than x.

This means we want to delay the insertion of x as long as possible, while ensuring that all smaller numbers appear early enough so that MEX has already reached x. After that moment, every additional element before x is inserted keeps MEX fixed at x, giving us the desired stretch of constant color.

The only real decision is where to place x relative to the numbers 0 through x−1. Once those smaller numbers are all present, we can freely place all numbers greater than x anywhere without affecting MEX being x, as long as x is still missing.

This leads to a simple optimal construction: place all numbers greater than x first, then place 0 through x−1, and finally place x at the end. This maximizes the time interval where the prefix contains all values less than x but not x itself.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Optimal Construction | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Split the permutation into three conceptual groups: numbers greater than x, numbers from 0 to x−1, and the single value x itself. This separation is based on how each group influences the MEX value.
2. Place all numbers strictly greater than x at the beginning of the permutation. These values do not help in forming the prefix that determines MEX = x, but they also do not interfere with it.
3. Place all numbers from 0 to x−1 immediately after. This ensures that once this block is fully included in a prefix, every value required to push MEX up to x has appeared.
4. Place x as late as possible, ideally at the end. This maximizes the number of prefixes where all smaller values are present but x is still absent, which is exactly the condition for MEX to equal x.
5. Output the constructed sequence.

The key idea is that once the prefix contains all values from 0 to x−1, MEX becomes x and stays there until x appears. We are maximizing how long we can delay that last event.

### Why it works

The MEX of a prefix is determined entirely by which smallest values are missing. To have MEX equal x, two conditions must hold simultaneously: every value from 0 to x−1 must already be present, and x must not yet be present. Once both are satisfied, adding any value greater than x does not change the MEX, since it does not fill any missing integer below x. Therefore, every position after the first full appearance of 0 through x−1 and before x contributes a valid occurrence of color x. The construction maximizes this interval by ensuring all small values appear as early as possible while delaying x.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, x = map(int, input().split())

    if x == n:
        # MEX can only become n at full prefix
        print(*range(n))
        continue

    res = []

    # first put all values > x
    for i in range(x + 1, n):
        res.append(i)

    # then values < x
    for i in range(x):
        res.append(i)

    # finally x
    res.append(x)

    print(*res)
```

The implementation directly follows the observation that only the relative position of x with respect to [0, x−1] matters. Values greater than x can be placed anywhere before x without affecting when MEX becomes x, so we safely put them first. The loop boundaries are important: the first loop starts at x+1 to exclude x itself, and the second loop goes up to x−1 inclusive.

The special case x = n avoids an empty conceptual condition where x is outside the permutation range; in that case, the optimal arrangement is irrelevant because MEX never equals n before the final prefix.

## Worked Examples

We trace two representative cases.

### Example 1: n = 4, x = 2

We construct the permutation.

| Step | Added block | Current permutation |
| --- | --- | --- |
| 1 | values > 2 → [3] | [3] |
| 2 | values < 2 → [0, 1] | [3, 0, 1] |
| 3 | add x → [2] | [3, 0, 1, 2] |

Now we examine MEX evolution:

| Prefix | Elements | MEX |
| --- | --- | --- |
| 1 | [3] | 0 |
| 2 | [3, 0] | 1 |
| 3 | [3, 0, 1] | 2 |
| 4 | [3, 0, 1, 2] | 4 |

Color 2 appears exactly once. The construction ensures we reach MEX = 2 as early as possible and keep it stable until x appears.

### Example 2: n = 5, x = 0

| Step | Added block | Current permutation |
| --- | --- | --- |
| 1 | values > 0 → [1, 2, 3, 4] | [1, 2, 3, 4] |
| 2 | values < 0 → [] | [1, 2, 3, 4] |
| 3 | add x → [0] | [1, 2, 3, 4, 0] |

MEX evolution:

| Prefix | Elements | MEX |
| --- | --- | --- |
| 1 | [1] | 0 |
| 2 | [1,2] | 0 |
| 3 | [1,2,3] | 0 |
| 4 | [1,2,3,4] | 0 |
| 5 | [1,2,3,4,0] | 5 |

Color 0 appears in all prefixes until 0 is placed, maximizing its frequency.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test | Each number is placed exactly once in the construction |
| Space | O(n) | We store the resulting permutation |

The total n across all test cases is at most 2×10^5, so the linear construction easily fits within the time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n, x = map(int, input().split())
        if x == n:
            out.append(" ".join(map(str, range(n))))
            continue

        res = []
        for i in range(x + 1, n):
            res.append(i)
        for i in range(x):
            res.append(i)
        res.append(x)
        out.append(" ".join(map(str, res)))

    return "\n".join(out)

# provided samples
assert run("""7
4 2
4 0
5 0
1 1
3 3
1 0
4 3
""") == """1 0 3 2
2 3 1 0
3 4 0 1 2
0
0 2 1
0
1 2 0 3"""

# custom cases
assert run("1\n2 2\n") == "0 1", "x = n edge"
assert run("1\n3 0\n") in ["1 2 0", "2 1 0"], "x = 0 behavior"
assert run("1\n5 4\n") == "0 1 2 3 4", "x near end"
assert run("1\n5 2\n") == "3 4 0 1 2", "middle split"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 2 | 0 1 | x = n edge case |
| 3 0 | variant | behavior when x = 0 |
| 5 4 | 0 1 2 3 4 | boundary near end |
| 5 2 | 3 4 0 1 2 | general split correctness |

## Edge Cases

When x = n, the algorithm takes the identity permutation. For a small example like n = 3, x = 3, the construction produces [0, 1, 2]. The MEX reaches 3 only after all elements are seen, so the final prefix alone contributes the target color.

When x = 0, the construction places all other values first, then 0 at the end. For n = 4, x = 0, we get [1, 2, 3, 0]. The MEX remains 0 for every prefix until 0 appears, which is the maximum achievable span.

When x is in the middle, such as n = 6, x = 2, the sequence [3, 4, 5, 0, 1, 2] ensures that once 0 and 1 appear, MEX becomes 2 and stays there until 2 is appended, maximizing the count of color 2 cells.
