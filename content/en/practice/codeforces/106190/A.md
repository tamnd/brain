---
title: "CF 106190A - \u041f\u043e\u0447\u0438\u043d\u043a\u0430 \u0434\u0432\u0438\u0433\u0430\u0442\u0435\u043b\u044f <<\u041f\u0435\u0433\u0430\u0441\u0430>>"
description: "The problem gives two arrays of the same length. One array, call it a, is already fixed and represents the damaged state of a system."
date: "2026-06-25T10:44:52+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106190
codeforces_index: "A"
codeforces_contest_name: "\u041a\u043e\u0433\u043d\u0438\u0442\u0438\u0432\u043d\u044b\u0435 \u0442\u0435\u0445\u043d\u043e\u043b\u043e\u0433\u0438\u0438 2025-2026. \u041f\u0435\u0440\u0432\u044b\u0439 \u043e\u0442\u0431\u043e\u0440"
rating: 0
weight: 106190
solve_time_s: 41
verified: true
draft: false
---

[CF 106190A - \u041f\u043e\u0447\u0438\u043d\u043a\u0430 \u0434\u0432\u0438\u0433\u0430\u0442\u0435\u043b\u044f <<\u041f\u0435\u0433\u0430\u0441\u0430>>](https://codeforces.com/problemset/problem/106190/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 41s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem gives two arrays of the same length. One array, call it `a`, is already fixed and represents the damaged state of a system. We need to construct another array `b` of the same size, with each element between 0 and 10^9, under a very specific constraint: for every position `i`, the absolute difference `|a_i - b_i|` must be odd.

Rephrased in simpler terms, each position is independent, and for every index we must choose a number `b_i` that has the opposite parity from `a_i`. If `a_i` is even, `b_i` must be odd. If `a_i` is odd, `b_i` must be even.

The constraint on the magnitude of values is not restrictive here, because both 0 and 1 are valid representatives for even and odd numbers, and they always lie within the allowed range.

The input size can be large, up to 2·10^5 total elements across all test cases. That immediately suggests that any quadratic or even log-linear per-element heavy computation is unnecessary. A direct linear construction per test case is sufficient, since we only decide each `b_i` independently.

A subtle point worth checking is whether there is any hidden coupling between indices. A naive reading might suggest some global structure, but the condition is purely per element. That removes any need for sorting, dynamic programming, or greedy balancing.

Edge cases are mostly about parity and boundary values. For example, if `a_i = 0`, we must still produce an odd number, and if `a_i = 10^9`, we still need an even or odd adjustment that stays in range. This is always possible.

## Approaches

A brute-force mindset would try to assign values to `b` by scanning all possible candidates for each position and checking whether the parity condition holds. For each index `i`, one might iterate over all values from 0 to 10^9 and pick a valid one. This is correct in principle because the condition is easy to verify, but the search space per element is 10^9 possibilities, which leads to about 10^14 operations in the worst case when `n` is large. That is completely infeasible.

The key observation is that the constraint does not ask for optimization, only feasibility, and it depends solely on parity. Once the condition is reduced to parity matching, each position has exactly two equivalence classes: numbers with the same parity and numbers with the opposite parity. We are always free to pick any representative from the correct class.

This collapses the problem from “search in a huge range” to “choose one of two fixed values per element”. A convenient construction is to map every even `a_i` to 1 and every odd `a_i` to 0. This always satisfies the parity flip condition and stays within bounds.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (try all b values) | O(n · 10^9) | O(1) | Too slow |
| Parity construction | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the array `a`. We do not need to store anything beyond processing each value, but storing simplifies implementation.
2. For each element `a_i`, determine its parity. This is done by checking `a_i % 2`.
3. If `a_i` is even, assign `b_i = 1`. This guarantees `|a_i - b_i|` is odd because even minus odd is always odd.
4. If `a_i` is odd, assign `b_i = 0`. This again guarantees an odd difference because odd minus even is odd.
5. Output the constructed array.

The reasoning behind steps 3 and 4 is that we deliberately force parity inversion using the smallest possible representatives. Using 0 and 1 is sufficient because parity is invariant under addition of 2, and we only care about whether the difference is divisible by 2.

### Why it works

The invariant maintained is that for every index `i`, the parity of `b_i` is always different from the parity of `a_i`. Since parity fully determines whether a difference is even or odd, this guarantees that `|a_i - b_i|` is always odd. No interaction exists between indices, so satisfying each position independently is enough to satisfy the entire array constraint.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    
    res = []
    for x in a:
        if x % 2 == 0:
            res.append(1)
        else:
            res.append(0)
    
    print(*res)
```

The solution reads each test case independently and constructs the answer in a single pass. The only implementation detail that matters is keeping the output generation simple, since printing inside loops can be slower for large inputs.

A common mistake here would be trying to “optimize” values by choosing something like `x + 1` or `x - 1`. That is also valid in many cases, but it is unnecessary and can risk overflow or boundary concerns when `a_i = 10^9`. Using fixed parity representatives avoids all such issues.

## Worked Examples

### Example 1

Input:

```
a = [1, 2, 3]
```

We process each element:

| i | a_i | parity | chosen b_i | |a_i - b_i| |

|---|-----|--------|------------|------------|

| 1 | 1   | odd    | 0          | 1          |

| 2 | 2   | even   | 1          | 1          |

| 3 | 3   | odd    | 0          | 3          |

Output:

```
0 1 0
```

This trace shows that every position independently satisfies the odd-difference condition without requiring any coordination.

### Example 2

Input:

```
a = [0, 4, 7, 10]
```

| i | a_i | parity | chosen b_i | |a_i - b_i| |

|---|-----|--------|------------|------------|

| 1 | 0   | even   | 1          | 1          |

| 2 | 4   | even   | 1          | 3          |

| 3 | 7   | odd    | 0          | 7          |

| 4 | 10  | even   | 1          | 9          |

Output:

```
1 1 0 1
```

This example confirms that even at boundary values like 0 and large even numbers, the construction remains valid and within constraints.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each element is processed once with O(1) work |
| Space | O(n) | Storage for the output array |

The total input size across all test cases is bounded by 2·10^5, so a single linear pass over all elements is easily fast enough within the time limit. Memory usage is also minimal since only the output array is stored per test case.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        res = []
        for x in a:
            res.append(1 if x % 2 == 0 else 0)
        out.append(" ".join(map(str, res)))
    return "\n".join(out)

# provided sample
assert run("""1
3
1 2 3
""") == "0 1 0"

# all equal even
assert run("""1
4
2 2 2 2
""") == "1 1 1 1"

# all equal odd
assert run("""1
5
1 1 1 1 1
""") == "0 0 0 0 0"

# mixed boundaries
assert run("""1
4
0 1 10 11
""") == "1 0 1 0"

# single element
assert run("""1
1
7
""") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all even | all 1s | even handling |
| all odd | all 0s | odd handling |
| mixed | alternating parity output | correctness across values |
| single element | 0 | minimal case |

## Edge Cases

For `a_i = 0`, the construction still works cleanly: since 0 is even, we assign `b_i = 1`, giving `|0 - 1| = 1`, which is odd and within bounds. No special handling is required.

For large values like `a_i = 10^9`, parity is still well-defined, and assigning either 0 or 1 keeps the result valid. There is no risk of overflow or boundary violation because we never attempt to mirror or increment the input value.

For alternating parity inputs, each index is independent, so the output simply flips parity element-wise without any interference, confirming that no global consistency constraints exist.
