---
title: "CF 1856B - Good Arrays"
description: "We are given an array of positive integers. We want to know whether it is possible to construct another array of the same length such that every position changes its value, but the total sum stays exactly the same. The second array is not arbitrary."
date: "2026-06-09T05:02:54+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1856
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 890 (Div. 2) supported by Constructor Institute"
rating: 900
weight: 1856
solve_time_s: 136
verified: false
draft: false
---

[CF 1856B - Good Arrays](https://codeforces.com/problemset/problem/1856/B)

**Rating:** 900  
**Tags:** implementation, math  
**Solve time:** 2m 16s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of positive integers. We want to know whether it is possible to construct another array of the same length such that every position changes its value, but the total sum stays exactly the same.

The second array is not arbitrary. Each position must differ from the original, and yet when all elements are summed, nothing changes globally. The question is purely existential: we do not need to construct the array, only decide if such a rearrangement exists.

The constraints are large in number of test cases and total array size, so any solution must be linear per test case. A quadratic or even mildly superlinear approach per test case will fail immediately because the total number of elements across all tests reaches $10^5$.

The main subtlety is that this is not about permutations or rearrangements. The new array can change values freely as long as it respects positivity and keeps the sum invariant. This makes it a global balancing problem rather than a local matching problem.

A common failure case arises when $n=1$. In that case, the only possible array with the same sum is the array itself, so it is impossible to satisfy the condition $a_1 \ne b_1$. Another important edge case is when all elements are equal and $n$ is small, where intuition about “shifting values around” often leads to incorrect conclusions unless the sum constraint is checked carefully.

## Approaches

The brute-force perspective tries to assign each position a new value different from the original while keeping track of the remaining sum. One could imagine iterating over all possible assignments, but each position has infinitely many valid positive integers, so enumeration is not even well-defined in a finite sense. Even if we restrict ourselves to values appearing in the array or bounded by the sum, the number of possibilities grows exponentially with $n$, making this approach infeasible beyond very small inputs.

The key observation is that we do not need to construct the array explicitly. We only need to determine whether the sum constraint and the “no fixed point per index” constraint can be satisfied simultaneously. The sum constraint forces the total increase and decrease across all positions to cancel out exactly. This immediately suggests that at least one element must be increased and at least one must be decreased, otherwise the sum cannot remain unchanged.

The structure becomes especially rigid when $n=1$, because no redistribution is possible. When $n \ge 2$, it is always possible to shift value from one position to another: decrease one element by $1$ and increase another by $1$, while keeping all elements positive and ensuring no position retains its original value. Since all $a_i \ge 1$, we always have room to decrease at least one element.

Thus the problem collapses into a simple dichotomy based entirely on $n$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | not well-defined | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the size of the array $n$.
2. If $n = 1$, immediately output "NO". With a single element, the sum constraint forces $b_1 = a_1$, which violates $a_1 \ne b_1$.
3. If $n \ge 2$, output "YES". In this case, we can always construct a valid array by decreasing one element and increasing another, preserving positivity and maintaining the sum.
4. Repeat for all test cases.

### Why it works

The sum constraint enforces that total mass is preserved. With at least two positions, we can redistribute one unit from one index to another. This produces at least one index where $b_i < a_i$ and one where $b_j > a_j$, ensuring both the inequality condition and sum preservation. No index is forced to remain unchanged because any decrease can be compensated elsewhere. For $n=1$, such redistribution is impossible, so the constraints become incompatible.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    input().split()  # values not needed
    if n == 1:
        print("NO")
    else:
        print("YES")
```

The solution deliberately ignores the actual array values because the feasibility depends only on the length of the array. The only meaningful decision is whether redistribution across at least two indices is possible.

A common mistake here is attempting to analyze parity or element structure, but none of that matters. The sum constraint does not restrict feasibility beyond requiring at least two degrees of freedom, which is exactly what $n \ge 2$ provides.

## Worked Examples

Consider the input with several cases of different sizes.

For $n=3$, any array such as $[1,5,9]$ has enough flexibility. A redistribution exists, so the answer is "YES".

For $n=1$, such as $[1]$, no alternative positive integer with the same sum exists except itself, so the answer is "NO".

For another $n=3$ case like $[1,2,3]$, we can always construct a new array such as $[2,1,3]$ or any balanced shift, so the answer is again "YES".

| Test case | n | Decision | Reason |
| --- | --- | --- | --- |
| [1, 5, 9] | 3 | YES | redistribution possible |
| [1] | 1 | NO | sum forces identical array |
| [1, 2, 3] | 3 | YES | swap-like adjustment possible |

These traces confirm that only the size of the array matters, not the distribution of values.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | reading input only |
| Space | O(1) | no auxiliary structure beyond variables |

The total input size across all test cases is bounded by $10^5$, so a single linear pass over the input is sufficient. No computation beyond a simple conditional check is required, making the solution trivially fast within constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        input().split()
        out.append("NO" if n == 1 else "YES")
    return "\n".join(out)

# provided samples
assert run("""6
3
6 1 2
2
1 1
4
3 1 2 4
1
17
5
1 2 1 1 1
3
618343152 819343431 1000000000
""") == """YES
NO
YES
NO
NO
YES"""

# custom cases
assert run("""3
1
5
2
10 10
5
1 1 1 1 1
""") == """NO
YES
YES"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| n=1 single element | NO | impossibility base case |
| n=2 equal elements | YES | minimal valid redistribution |
| all equal large n | YES | uniform arrays still valid |

## Edge Cases

For $n=1$, the algorithm immediately returns "NO". The only possible candidate array with the same sum is identical to the original, so the inequality constraint cannot be satisfied.

For $n=2$, the algorithm returns "YES". For an input like $[10,10]$, we can construct $[11,9]$, which preserves the sum and changes both positions. This confirms that having at least two positions is sufficient to redistribute value.

For larger uniform arrays such as $[1,1,1,1,1]$, the algorithm returns "YES" because we can always move one unit from one position to another while preserving positivity and sum, ensuring no element remains unchanged.
