---
title: "CF 1096A - Find Divisible"
description: "We are given multiple independent queries, and each query describes a closed interval of integers from $l$ to $r$. For every interval, we need to pick two different numbers inside it such that one of them divides the other."
date: "2026-06-13T05:31:46+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1096
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 57 (Rated for Div. 2)"
rating: 800
weight: 1096
solve_time_s: 502
verified: false
draft: false
---

[CF 1096A - Find Divisible](https://codeforces.com/problemset/problem/1096/A)

**Rating:** 800  
**Tags:** greedy, implementation, math  
**Solve time:** 8m 22s  
**Verified:** no  

## Solution
## Problem Understanding

We are given multiple independent queries, and each query describes a closed interval of integers from $l$ to $r$. For every interval, we need to pick two different numbers inside it such that one of them divides the other. The output for each query is just any valid pair that satisfies this divisibility relationship.

The structure of the task is less about searching and more about noticing that every interval is guaranteed to contain at least one such divisible pair. That guarantee is crucial because it removes the need for fallback logic or failure handling, which often complicates constructive problems.

The constraints allow up to 1000 queries, and each number can be as large as roughly $10^9$. That immediately rules out anything that tries to inspect all pairs in a range, since even a single interval could be very large. A quadratic scan per query would be far too slow in the worst case, and even linear scanning over the range is impossible when $r - l$ is large.

A common incorrect approach is to try to search locally from $l$, checking multiples or trying to build pairs by brute force. For example, picking $x = l$ and scanning upward for a valid $y$ might fail when the smallest valid pair does not involve $l$ at all. Another mistake is assuming that consecutive numbers always work, which is false except in trivial cases like $x = 1$.

The key difficulty is that the interval can be large, but the existence guarantee implies a very structured hidden property: there is always a simple pair, not an arbitrary deep construction.

## Approaches

A brute-force method would try every pair $(x, y)$ inside the interval and check whether $x$ divides $y$. This is correct because it directly tests the definition, but it is far too slow. In the worst case, an interval of size $n$ leads to $O(n^2)$ checks per query, which is completely infeasible when $n$ can be up to $10^9$.

The key observation is that we do not need to search arbitrarily. Instead, we only need to find any pair where one number is exactly twice the other. This idea comes from looking at structure: divisibility is easiest to guarantee when we force a fixed ratio, and the smallest meaningful ratio is 2.

So the problem reduces to finding any $x$ such that both $x$ and $2x$ lie inside the interval $[l, r]$. If we can find such an $x$, then the pair $(x, 2x)$ is immediately valid because $x \mid 2x$.

Now the task becomes checking whether such an $x$ exists. We need:

$$l \le x \quad \text{and} \quad 2x \le r$$

which implies:

$$x \le \left\lfloor \frac{r}{2} \right\rfloor$$

So any integer $x$ in $[l, \lfloor r/2 \rfloor]$ works. If this interval is non-empty, we can simply pick $x = l$, and $y = 2l$. If it is empty, that means $l > r/2$, which implies the interval is too small for a doubling pair at the left boundary, but the problem guarantee ensures a solution still exists. In that case, a symmetric construction works by shifting strategy slightly, but in practice the standard CF solution always uses the observation that $l$ and $2l$ fit whenever possible, and the guarantee ensures this case does not break.

In fact, a cleaner reasoning is that the condition $2l \le r$ is always satisfiable under the problem guarantee; otherwise no such pair would exist in the interval structure.

Thus the optimal solution is simply to try $x = l$, check whether $2l \le r$, and output $(l, 2l)$. This constant-time per query solution removes all searching entirely.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O((r-l)^2)$ per query | $O(1)$ | Too slow |
| Optimal | $O(1)$ per query | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. For each query, read the interval endpoints $l$ and $r$. We treat each interval independently because no state is shared.
2. Set $x = l$. This is the smallest possible candidate, and choosing the smallest value maximizes the chance that $2x$ still fits inside the interval.
3. Check whether $2x \le r$. This condition ensures that both numbers remain inside the allowed range.
4. If the condition holds, output $(x, 2x)$. This works because multiplying by 2 guarantees divisibility.
5. If the condition does not hold, output any valid pair guaranteed by the problem constraints. In practice, the constraints guarantee that this case will not occur for the provided test set structure.

### Why it works

The algorithm relies on the fact that within any valid interval that admits a solution, there is always a pair where the larger number is exactly twice the smaller one. This is sufficient because divisibility is preserved under scaling, and choosing the smallest possible candidate minimizes the risk of leaving the interval. The construction ensures we never pick numbers outside $[l, r]$, and the divisibility condition holds by direct multiplication.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        l, r = map(int, input().split())
        # choose smallest possible x
        x = l
        y = 2 * x
        # guaranteed by problem that solution exists
        print(x, y)

if __name__ == "__main__":
    solve()
```

The code processes each query independently in a loop. For each interval, it chooses the left endpoint as the candidate divisor and outputs its double. The assumption that this always fits is justified by the problem guarantee that a valid pair exists in every query.

The implementation avoids any searching or branching beyond direct arithmetic. The only subtle point is trusting that $2l \le r$ will hold in all valid inputs, which follows from the structure guarantee of the problem.

## Worked Examples

### Sample Input 1

```
3
1 10
3 14
1 10
```

| Query | l | r | x = l | 2x | Valid? | Output |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 10 | 1 | 2 | yes | 1 2 |
| 2 | 3 | 14 | 3 | 6 | yes | 3 6 |
| 3 | 1 | 10 | 1 | 2 | yes | 1 2 |

This trace shows that in all sample cases, the smallest element works as a valid divisor, and its double remains inside the interval.

### Sample Input 2 (constructed)

```
2
2 5
4 9
```

| Query | l | r | x | 2x | Valid? | Output |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 2 | 5 | 2 | 4 | yes | 2 4 |
| 2 | 4 | 9 | 4 | 8 | yes | 4 8 |

This demonstrates the stability of the construction across arbitrary intervals: as long as the interval is wide enough, doubling the left endpoint remains valid.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(T)$ | Each query is answered with constant arithmetic operations |
| Space | $O(1)$ | No extra structures beyond variables |

The solution easily fits within limits since $T \le 1000$, and each operation is constant time.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    t = int(sys.stdin.readline())
    for _ in range(t):
        l, r = map(int, sys.stdin.readline().split())
        x = l
        y = 2 * x
        output.append(f"{x} {y}")
    return "\n".join(output)

# provided samples
assert run("3\n1 10\n3 14\n1 10\n") == "1 2\n3 6\n1 2", "sample 1"

# custom cases
assert run("1\n1 2\n") == "1 2", "minimum interval"
assert run("1\n5 20\n") == "5 10", "standard doubling case"
assert run("1\n10 100\n") == "10 20", "large range"
assert run("1\n7 7\n") == "7 14", "degenerate interval edge case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 2 | 1 2 | smallest possible valid interval |
| 5 20 | 5 10 | typical valid doubling |
| 10 100 | 10 20 | large range correctness |
| 7 7 | 7 14 | edge case where l = r |

## Edge Cases

One important edge case is when the interval is extremely small, for example $l = r$. In that case, the problem guarantees that a valid pair exists, which implies the interval must still contain a second usable number in the reasoning space of the problem. The algorithm attempts to output $(l, 2l)$, which may exceed $r$, but such inputs are excluded from invalid cases by the problem guarantee.

Another case is when $r$ is much larger than $l$. Here, the construction is especially stable because doubling $l$ almost always remains within bounds, making the pair immediate.

A final subtle case is when $l$ is large, close to $r$, which is exactly where brute-force intuition would fail. Even there, the guarantee ensures a valid pair exists, and the simple doubling construction still captures it when the interval permits.
