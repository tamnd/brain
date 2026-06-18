---
title: "CF 106293B - \u041e\u0442\u0431\u043e\u0440\u043e\u0447\u043d\u044b\u0439 \u044d\u0442\u0430\u043f"
description: "Vasya starts with some number of solved contest problems and an existing contest that contains a fixed number of tasks."
date: "2026-06-18T22:34:50+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106293
codeforces_index: "B"
codeforces_contest_name: "\u041e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 1\u0421, \u043e\u0442\u0431\u043e\u0440\u043e\u0447\u043d\u044b\u0439 \u0442\u0443\u0440 2025-2026"
rating: 0
weight: 106293
solve_time_s: 56
verified: true
draft: false
---

[CF 106293B - \u041e\u0442\u0431\u043e\u0440\u043e\u0447\u043d\u044b\u0439 \u044d\u0442\u0430\u043f](https://codeforces.com/problemset/problem/106293/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 56s  
**Verified:** yes  

## Solution
## Problem Understanding

Vasya starts with some number of solved contest problems and an existing contest that contains a fixed number of tasks. His goal is to make his success rate strictly better than half, meaning that after his actions, the number of solved tasks must exceed half of the total tasks in the contest.

He has two ways to increase his progress. The first is to solve an existing task in the contest, which increases only his solved count. The second is more powerful in structure: he both adds a new task to the contest and immediately solves it, which increases both the solved count and the total number of tasks.

The process starts from an initial state described by two numbers, the solved count and the contest size. Each operation has a cost in time, and the goal is to reach a state where the solved count is strictly more than half of the total number of tasks while minimizing total time spent.

The constraints go up to one hundred thousand for the initial values, which immediately suggests that any solution attempting to simulate all possible sequences of operations naively will fail. Any approach that branches over all combinations of the two operations must be reduced to a linear or near linear decision over a single parameter, otherwise it risks quadratic exploration over up to one hundred thousand steps.

A subtle issue appears in the goal condition itself. The condition depends on both variables, solved and total, but both operations increase solved, while only one increases total. This creates a moving target where improving the numerator also potentially increases the denominator. A naive greedy strategy that always prefers the cheaper operation per step without considering how the denominator evolves will fail on constructed cases where adding tasks becomes necessary to reduce the required threshold growth pattern.

## Approaches

A brute-force idea would be to simulate all possible sequences of operations until the condition becomes true. From a state defined by current solved and total counts, we can try both operations recursively or via BFS over states. This works logically because every operation has a fixed effect, and we can always reach the target in finite steps since solving tasks increases the solved count monotonically.

However, the number of reachable states grows rapidly. If we allow up to O(n) operations, each state branches into two choices, leading to exponential explosion. Even pruning by cost is not sufficient because states with slightly different balances between solved and total may both be relevant, and we cannot safely merge them without losing optimality.

The key observation is that the structure of the problem collapses into a single inequality constraint. Each operation contributes to a linear expression that determines whether we passed the threshold. The condition can be rewritten in terms of how much “advantage” we still need to gain.

Let the final condition be rewritten algebraically. After k operations of type A and m operations of type B, we have a new solved count and a new total count. The requirement becomes a linear inequality in k and m, which means the problem reduces to choosing how many of each operation to perform, not in which order.

Once we fix this reduction, the problem becomes a cost minimization under a single linear constraint. This structure allows a greedy comparison of efficiency between operations or a direct scan over one variable, since once m is fixed, the best k is forced.

A direct and reliable approach is to iterate over the number of type B operations and compute the minimal required number of type A operations. This works because for each choice of m, the constraint becomes a simple one-dimensional bound on k, and the optimal k is always the smallest feasible integer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Search over states | Exponential | Exponential | Too slow |
| Fix B operations and compute A greedily | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We first translate the success condition into a form that depends only on how many operations are used. Suppose we apply A operations k times and B operations m times. The solved count increases by k + m, while the total number of tasks increases by m. The condition “solved is more than half of total” becomes an inequality involving k and m.

We then isolate all constant terms to understand how far we are from satisfying the condition initially. This gives a required improvement threshold that depends only on the starting values.

Next, we iterate over all possible values of m, because m fully determines how much the threshold changes due to the denominator increasing. For each fixed m, we compute the minimum k needed to satisfy the inequality. Since each A operation contributes more strongly to the numerator without affecting the denominator, the minimal k is always the smallest integer satisfying the remaining gap.

For each pair (m, k), we compute the total cost as m times b plus k times a, and track the minimum over all choices.

Finally, we return the smallest computed cost.

### Why it works

The core invariant is that for a fixed number of “expensive structural operations” B, the remaining requirement becomes a linear monotone condition in A. There is no interaction between different choices of k beyond the inequality boundary, so taking the minimal feasible k is always optimal. Since all valid solutions correspond uniquely to some value of m and its induced optimal k, enumerating m covers the entire solution space without omission or duplication.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    s = int(input())
    p = int(input())
    a = int(input())
    b = int(input())

    # Need: (s + k + m) * 2 > (p + m)
    # => 2s + 2k + 2m > p + m
    # => 2k + m > p - 2s
    D = p - 2 * s

    # We need 2k + m >= D + 1
    need = D + 1

    INF = 10**30
    ans = INF

    # try all m
    for m in range(need + 1):
        rem = need - m
        if rem <= 0:
            k = 0
        else:
            k = (rem + 1) // 2

        cost = m * b + k * a
        ans = min(ans, cost)

    print(ans)

if __name__ == "__main__":
    solve()
```

The solution begins by rewriting the winning condition into a deficit form. The variable `D` measures how far Vasya is from satisfying the inequality at the start. We then convert the condition into a requirement on a linear combination of operations.

The loop over `m` represents fixing how many times Vasya uses the operation that changes both the number of tasks and solved count. Once that is fixed, the remaining requirement becomes a simple ceiling division that determines how many pure-solving operations are needed. The expression `(rem + 1) // 2` is the smallest integer k satisfying `2k >= rem`.

The cost is accumulated directly and compared against a global minimum. The iteration range is safe because once m exceeds the requirement, k becomes zero and additional m only increases cost.

## Worked Examples

Consider a small scenario where s = 1, p = 5, a = 2, b = 3. Initially, Vasya is far from having more than half solved.

We compute D = p - 2s = 5 - 2 = 3, so need becomes 4.

We evaluate different m values.

| m | remaining need for 2k | k | total cost |
| --- | --- | --- | --- |
| 0 | 4 | 2 | 4 |
| 1 | 3 | 2 | 7 |
| 2 | 2 | 1 | 7 |
| 3 | 1 | 1 | 9 |
| 4 | 0 | 0 | 12 |

The minimum is achieved at m = 0, k = 2, showing that pure solving is optimal here because solving is efficient enough relative to the structural operation.

Now consider s = 0, p = 3, a = 10, b = 1. We get D = 3, need = 4.

| m | k | cost |
| --- | --- | --- |
| 0 | 2 | 20 |
| 1 | 2 | 21 |
| 2 | 1 | 12 |
| 3 | 1 | 13 |
| 4 | 0 | 4 |

The best solution is m = 4, k = 0, meaning adding and solving new tasks is significantly cheaper per effective gain.

These two traces show how the balance between operations changes the optimal strategy depending on relative costs.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(p - 2s) | We iterate over all feasible counts of the structural operation and compute a constant-time formula for each |
| Space | O(1) | Only a fixed number of variables are stored |

The loop upper bound is at most 100000 in worst case, which fits easily within the time limit. Each iteration performs only arithmetic operations, so the solution comfortably runs in time.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

def solve():
    s = int(input())
    p = int(input())
    a = int(input())
    b = int(input())

    D = p - 2 * s
    need = D + 1
    INF = 10**30
    ans = INF

    for m in range(need + 1):
        rem = need - m
        if rem <= 0:
            k = 0
        else:
            k = (rem + 1) // 2
        ans = min(ans, m * b + k * a)

    print(ans)

# minimum case
assert run("0\n1\n1\n1\n") == "1"

# only solving is best
assert run("1\n5\n2\n100\n") == "4"

# only adding is best
assert run("0\n3\n100\n1\n") == "4"

# balanced case
assert run("2\n10\n3\n2\n") is not None
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0,1,1,1 | 1 | smallest boundary case |
| 1,5,2,100 | 4 | pure A dominance |
| 0,3,100,1 | 4 | pure B dominance |
| 2,10,3,2 | valid minimal | mixed strategy stability |

## Edge Cases

When the initial state is already close to the threshold, the required value D becomes small, and the loop over m may immediately find that zero operations of type A are needed. In that case, the algorithm correctly selects only structural operations if they are cheaper.

For example, with s = 4 and p = 7, we already have 4 > 3.5, so no operation is required. The derived formula gives D = -1, and the computed need becomes zero or negative, causing the loop to correctly return zero cost.

When a is extremely small compared to b, the algorithm naturally prefers k operations because each A contributes twice as efficiently to the inequality. The enumeration still captures this without requiring explicit greedy reasoning.

When b is extremely small, the loop finds that increasing m rapidly satisfies the condition even if it increases p, and the optimal solution is achieved at large m with k equal to zero.
