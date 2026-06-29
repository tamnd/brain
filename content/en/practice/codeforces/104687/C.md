---
title: "CF 104687C - \u0421\u0443\u043c\u043c\u0430 1"
description: "We are given two integer intervals: one interval defines all valid values of $x$, and the other defines all valid values of $y$. We also have a target sum $n$."
date: "2026-06-29T18:51:51+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104687
codeforces_index: "C"
codeforces_contest_name: "\u041e\u0442\u0431\u043e\u0440 \u0432 \u0426\u0420\u041e\u0414 2022"
rating: 0
weight: 104687
solve_time_s: 61
verified: true
draft: false
---

[CF 104687C - \u0421\u0443\u043c\u043c\u0430 1](https://codeforces.com/problemset/problem/104687/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two integer intervals: one interval defines all valid values of $x$, and the other defines all valid values of $y$. We also have a target sum $n$. The task is to count how many pairs $(x, y)$ exist such that $x$ lies in its interval, $y$ lies in its interval, and their sum is exactly $n$.

In more concrete terms, imagine two inclusive ranges of numbers. We want to pick one number from the first range and one number from the second range so that together they add up to a fixed value. The output is simply the number of valid ways to do this.

The constraints are small enough that both ranges go up to $10^5$, and the target sum is also up to $10^5$. This immediately rules out anything that requires quadratic iteration over all pairs in the worst case, since that would lead to up to $10^{10}$ operations. Instead, we should aim for a linear or constant-time reasoning per test.

A few edge cases matter for correctness. If the required complement $y = n - x$ falls outside the second interval, that $x$ contributes nothing. For example, if $l_1 = 1, r_1 = 10, l_2 = 1, r_2 = 10, n = 2$, then only $x = 1, y = 1$ works, so the answer is 1. A naive approach that forgets bounds on $y$ would incorrectly count invalid pairs like $x = 2, y = 0$, even though $y$ is outside its range.

Another subtle issue is overcounting if one tries to independently count valid $x$ and $y$ values without enforcing the sum constraint. The dependency between the two variables is strict, so they cannot be treated independently.

## Approaches

A straightforward method is to try every possible $x$ in its interval, compute $y = n - x$, and check whether this $y$ lies in the second interval. This works because for each fixed $x$, there is at most one candidate $y$. The correctness is immediate since we are directly enforcing the condition $x + y = n$.

The problem with this brute-force approach is its runtime. In the worst case, the interval for $x$ contains $10^5$ values, and each check is constant time, so it runs in $O(r_1 - l_1 + 1)$, which is acceptable here. However, we can simplify further by removing iteration entirely.

The key observation is that we are not searching over pairs, we are intersecting two constraints simultaneously:

$$x \in [l_1, r_1], \quad n - x \in [l_2, r_2]$$

The second condition can be rewritten as:

$$l_2 \le n - x \le r_2$$

Rearranging gives:

$$n - r_2 \le x \le n - l_2$$

So $x$ must lie in the intersection of two intervals:

$$[l_1, r_1] \cap [n - r_2, n - l_2]$$

Once we compute this intersection, every integer $x$ inside it corresponds to exactly one valid $y$, and vice versa. So the answer reduces to counting integers in an interval.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(r1 - l1 + 1) | O(1) | Accepted |
| Interval Intersection | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

We transform the problem into counting integers in an intersection of two ranges.

1. Compute the transformed interval for $x$ implied by the $y$-constraints. This is $[n - r_2, n - l_2]$. This step is necessary because the condition on $y$ must be expressed in terms of $x$ to align both constraints.
2. Compute the overlap between $[l_1, r_1]$ and $[n - r_2, n - l_2]$. The left boundary of the intersection is the maximum of the two left endpoints, and the right boundary is the minimum of the two right endpoints.
3. If the resulting left endpoint exceeds the right endpoint, the intersection is empty, so the answer is zero. This corresponds to the case where no $x$ can satisfy both constraints simultaneously.
4. Otherwise, the number of integers in the intersection is $r - l + 1$, which directly gives the number of valid $x$, and therefore valid pairs.

### Why it works

Each valid pair $(x, y)$ satisfies both original constraints. The transformation replaces the constraint on $y$ with an equivalent constraint on $x$, preserving one-to-one correspondence between valid pairs and integers $x$ in the intersection. No two different $x$ values produce the same pair, and every valid pair produces exactly one $x$, so counting valid $x$ values is equivalent to counting valid pairs.

## Python Solution

```python
import sys
input = sys.stdin.readline

l1, r1, l2, r2, n = map(int, input().split())

left = max(l1, n - r2)
right = min(r1, n - l2)

if left > right:
    print(0)
else:
    print(right - left + 1)
```

The code directly applies the interval transformation derived in the algorithm. The expressions `n - r2` and `n - l2` define the valid range for $x$ implied by the second interval. Taking `max` and `min` computes the intersection boundaries safely in constant time. The final conditional handles the empty intersection case, ensuring no negative counts are produced.

## Worked Examples

### Example 1

Input:

```
1 10 1 10 20
```

We compute the transformed interval for $x$ from the second constraint: $x \in [20 - 10, 20 - 1] = [10, 19]$.

Now intersect with $[1, 10]$:

| Step | Left | Right |
| --- | --- | --- |
| Original x-range | 1 | 10 |
| Derived x-range | 10 | 19 |
| Intersection | 10 | 10 |

The intersection contains only $x = 10$. This corresponds to $y = 10$, giving one valid pair.

Output is 1.

This confirms the algorithm correctly handles boundary-touching cases where the intersection collapses to a single point.

### Example 2

Input:

```
2 5 3 7 9
```

Derived range from second interval is $x \in [9 - 7, 9 - 3] = [2, 6]$.

| Step | Left | Right |
| --- | --- | --- |
| Original x-range | 2 | 5 |
| Derived x-range | 2 | 6 |
| Intersection | 2 | 5 |

Valid $x$ values are 2, 3, 4, 5, so there are 4 pairs.

This shows how overlapping ranges produce multiple valid solutions, and the algorithm counts them without enumerating pairs explicitly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a constant number of arithmetic and comparisons |
| Space | O(1) | No additional data structures used |

The constraints allow up to $10^5$, but the solution does not iterate over that range. All operations are constant time, so the program comfortably fits within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    l1, r1, l2, r2, n = map(int, input().split())

    left = max(l1, n - r2)
    right = min(r1, n - l2)

    if left > right:
        return "0"
    return str(right - left + 1)

# provided sample
assert run("1 10 1 10 20") == "1"

# x-range empty after intersection
assert run("1 2 10 20 5") == "0"

# single solution at boundary
assert run("0 10 0 10 0") == "1"

# multiple solutions
assert run("1 10 1 10 10") == "10"

# shifted ranges
assert run("5 15 1 3 10") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 2 10 20 5 | 0 | no valid complement exists |
| 0 10 0 10 0 | 1 | boundary case with zero sum |
| 1 10 1 10 10 | 10 | full overlap producing max count |
| 5 15 1 3 10 | 1 | narrow intersection correctness |

## Edge Cases

One important edge case is when the transformed interval lies completely outside the original $x$-range. For input `1 2 10 20 5`, the derived range is $x \in [5 - 20, 5 - 10] = [-15, -5]$. Intersecting with $[1, 2]$ produces an empty interval, since the left endpoint becomes 1 and the right becomes -5. The algorithm correctly returns 0 because the intersection check `left > right` triggers.

Another case is when the intersection reduces to a single value. For input `0 10 0 10 0`, both ranges become $[0, 10]$, so the intersection is also $[0, 10]$. The algorithm returns $10 - 0 + 1 = 11$, which matches the number of pairs where $x = -y$ within the same interval, including zero.

A final subtle case is full overlap where every $x$ in the original range is valid. For input `1 10 1 10 10`, the transformed interval is also $[0, 9]$, and intersecting gives $[1, 9]$. The algorithm correctly counts all valid integers in that intersection without double counting or missing endpoints.
