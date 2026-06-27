---
title: "CF 105020H - Cookies"
description: "We are given several independent scenarios. In each scenario there are $n$ cookies in total, among which $a$ are large. Donia wants to eat some cookies, but she must avoid getting caught. The rule is that after she eats cookies, at least $m$ cookies must still remain uneaten."
date: "2026-06-28T01:59:03+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105020
codeforces_index: "H"
codeforces_contest_name: "TCPC Tunisian Collegiate Programming Contest 2022"
rating: 0
weight: 105020
solve_time_s: 73
verified: false
draft: false
---

[CF 105020H - Cookies](https://codeforces.com/problemset/problem/105020/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 13s  
**Verified:** no  

## Solution
## Problem Understanding

We are given several independent scenarios. In each scenario there are $n$ cookies in total, among which $a$ are large. Donia wants to eat some cookies, but she must avoid getting caught. The rule is that after she eats cookies, at least $m$ cookies must still remain uneaten.

The only cookies she cares about eating are the large ones. So she tries to maximize how many of the $a$ large cookies she can remove while still ensuring that the number of remaining cookies is at least $m$.

Rephrased, she starts with $n$ cookies, of which $a$ are “valuable” (large). She removes as many valuable cookies as possible, but she cannot reduce the total remaining count below $m$. The question is how many large cookies can be safely removed.

The constraint $n \le 10^{12}$ immediately rules out any simulation over cookies. The solution must be constant time per test case, since there are up to $10^5$ test cases. Any approach that iterates or constructs anything proportional to $n$ is impossible.

A subtle edge case appears when $n = m$. In that case no cookie can be eaten at all, so the answer must be zero regardless of $a$. Another edge case is when $n - m$ is larger than $a$, meaning there is enough “room” to eat all large cookies but still satisfy the constraint.

A naive mistake is to think only $a$ matters and return $a$, ignoring the restriction from $m$. Another mistake is to interpret the condition as “leave exactly $m$” instead of “at least $m$”, which would incorrectly force equality and reduce flexibility.

For example, if $n=10, m=3, a=7$, a careless approach might think all 7 large cookies can be eaten. But if all 7 are eaten, only 3 remain, which is valid, so the answer is actually 7. This shows that the constraint is about feasibility, not a strict quota.

## Approaches

A brute-force interpretation would try to simulate eating cookies one by one, always preferring large cookies until either all large cookies are eaten or the remaining count would fall below $m$. This works conceptually: at each step we remove one large cookie and check whether remaining cookies are still at least $m$. However, in the worst case we might simulate up to $10^{12}$ removals, which is far beyond any feasible time limit.

The key observation is that the process does not depend on ordering or randomness. The only thing that matters is how many cookies can be removed in total without violating the constraint. If we remove $x$ cookies, then $n - x \ge m$, so $x \le n - m$. This means the total number of cookies we can remove is capped by $n - m$. Since we only want to remove large cookies, the actual number we can take is also limited by how many large cookies exist, which is $a$. So the answer is simply the minimum between the number of large cookies available and the maximum number of cookies that can be removed safely.

This reduces the problem to a direct arithmetic comparison.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n)$ per test case | $O(1)$ | Too slow |
| Optimal | $O(1)$ per test case | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. For each test case, read $n$, $m$, and $a$. These define the total cookies, minimum required remaining cookies, and number of large cookies.
2. Compute how many cookies can be removed in total without violating the condition. Since at least $m$ must remain, at most $n - m$ cookies can be eaten in total.
3. Compare this limit with $a$, since we cannot eat more large cookies than exist.
4. Output the smaller value between $a$ and $n - m$.

The reasoning behind step 2 is that every eaten cookie reduces the remaining count by exactly one, regardless of whether it is large or small. So the constraint depends only on the total number removed, not their type.

### Why it works

At any point, if Donia eats $x$ cookies, the remaining count is exactly $n - x$. The condition requires $n - x \ge m$, which rearranges to $x \le n - m$. So the total number of cookies she can remove is globally bounded by $n - m$. Since she is only interested in large cookies, the best strategy is always to spend this “budget” of removals entirely on large cookies until either the budget is exhausted or she runs out of large cookies. This ensures both maximality and validity.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, m, a = map(int, input().split())
        max_remove = n - m
        if max_remove < 0:
            max_remove = 0
        print(min(a, max_remove))

if __name__ == "__main__":
    solve()
```

The code processes each test case independently. The key computation is `n - m`, which represents the maximum number of cookies that can be removed while still leaving at least $m$ behind. If $n < m$, this value becomes negative, so it is clamped to zero since no removal is allowed.

The final answer is the minimum between this allowable removal budget and the number of large cookies available. This directly implements the derived constraint without any simulation.

## Worked Examples

### Example 1

Input:

```
n = 5, m = 2, a = 3
```

We track how many large cookies can be eaten:

| Step | Remaining capacity (n - x) | Large eaten x | Valid? |
| --- | --- | --- | --- |
| 0 | 5 | 0 | yes |
| 1 | 4 | 1 | yes |
| 2 | 3 | 2 | yes |
| 3 | 2 | 3 | yes |

Here $n - m = 3$, so at most 3 cookies can be removed. Since $a = 3$, we can eat all 3 large cookies.

Output is 3.

### Example 2

Input:

```
n = 6, m = 4, a = 5
```

| Step | Remaining capacity (n - x) | Large eaten x | Valid? |
| --- | --- | --- | --- |
| 0 | 6 | 0 | yes |
| 1 | 5 | 1 | yes |
| 2 | 4 | 2 | yes |
| 3 | 3 | 3 | no |

Here $n - m = 2$, so even though $a = 5$, we can only eat 2 large cookies before violating the constraint.

Output is 2.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(T)$ | Each test case requires only constant-time arithmetic operations |
| Space | $O(1)$ | No extra structures are used |

The solution fits easily within limits since even $10^5$ test cases only require $10^5$ constant operations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import sys

    input = sys.stdin.readline
    t = int(input())
    out = []
    for _ in range(t):
        n, m, a = map(int, input().split())
        max_remove = max(0, n - m)
        out.append(str(min(a, max_remove)))
    return "\n".join(out)

# provided samples
assert run("3\n5 2 1\n5 2 2\n5 5 5\n") == "1\n2\n0", "sample 1"

# custom cases
assert run("1\n1 1 1\n") == "0", "minimum edge"
assert run("1\n1000000000000 1 1000000000000\n") == "999999999999", "large upper bound"
assert run("1\n10 10 5\n") == "0", "exact equality case"
assert run("2\n10 3 20\n6 4 10\n") == "7\n2", "mixed cases"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 1 | 0 | no removal allowed |
| 10^12 scale | large value | handles upper bounds |
| n = m | 0 | boundary condition |
| mixed cases | correct mins | general correctness |

## Edge Cases

When $n = m$, the constraint forces zero removals because any eaten cookie would violate the minimum remaining requirement. The algorithm computes $n - m = 0$, so the final answer becomes $\min(a, 0) = 0$, which matches the requirement exactly.

When $n < m$, which is allowed by constraints, the computed value $n - m$ is negative. The implementation clamps it to zero, meaning no cookies can be eaten. This correctly reflects that the condition is already violated or impossible to satisfy after any removal.

When $a \ge n - m$, the limiting factor becomes the remaining constraint rather than availability of large cookies. The algorithm correctly returns $n - m$, ensuring the full allowable capacity is used.
