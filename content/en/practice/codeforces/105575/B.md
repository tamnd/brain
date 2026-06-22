---
title: "CF 105575B - A Typical Codeforces Round"
description: "Each problem instance consists of three arrays of length $n$, which we can think of as per-problem parameters. For each index $i$, there are fixed values $ai$, $bi$, and $ci$."
date: "2026-06-22T12:52:59+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105575
codeforces_index: "B"
codeforces_contest_name: "Southeast University 6th Programming Competition Competition (Winter, Novice Group) \u4e1c\u5357\u5927\u5b66\u7b2c\u516d\u5c4a\u7a0b\u5e8f\u8bbe\u8ba1\u7ade\u8d5b\u51ac\u5b63\u8d5b\uff08\u65b0\u624b\u7ec4\uff09"
rating: 0
weight: 105575
solve_time_s: 47
verified: true
draft: false
---

[CF 105575B - A Typical Codeforces Round](https://codeforces.com/problemset/problem/105575/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

Each problem instance consists of three arrays of length $n$, which we can think of as per-problem parameters. For each index $i$, there are fixed values $a_i$, $b_i$, and $c_i$. After reading these arrays, the input provides $n$ additional pairs $(t, s)$, one per index $i$, and each pair determines how much contribution index $i$ adds to the final answer.

For each index $i$, we compute a candidate score based on $t$ and $s$. If $s \le 0$, that index contributes nothing. Otherwise, we evaluate a linear expression that decreases with both $t$ and $s$, and then compare it against a fixed cap $c_i$. The contribution of index $i$ is the maximum between the capped value $c_i$ and the computed expression. Summing these contributions over all indices produces the final answer.

The constraints implied by the problem description and the reference solution indicate that all arithmetic fits comfortably within 32-bit signed integers. This removes any need for big integer handling or modular arithmetic. The algorithm runs in linear time over $n$, so values of $n$ up to at least $10^5$ or $10^6$ are intended to be handled in a single pass.

A subtle case arises when $s \le 0$. In that case, the index is skipped entirely. A naive implementation might still compute the formula and include it, leading to incorrect negative contributions.

For example, suppose $a_i = 100$, $b_i = 2$, $c_i = 10$, and the input gives $t = 5$, $s = 0$. The correct output contribution is $0$. A careless implementation that ignores the $s \le 0$ guard would compute $100 - 2 \cdot 5 - 50 \cdot (0 - 1) = 100 - 10 + 50 = 140$, then incorrectly take $\max(10, 140) = 140$, which is invalid because the problem explicitly suppresses such entries.

Another edge case is when the computed expression becomes negative or extremely small. In that case, the cap $c_i$ dominates. If an implementation forgets the maximum operation and always uses the computed expression, it will systematically undercount in such cases.

## Approaches

The straightforward way to approach the problem is to process each index independently, compute the expression directly, and accumulate the result. For each $i$, we read its parameters $a_i$, $b_i$, $c_i$, and its query values $t_i$, $s_i$, then evaluate the formula exactly as described. Since each index is independent, no preprocessing or data structure is required.

This brute-force method already matches the structure of the problem. Each index contributes exactly once, and each contribution is computed in constant time. The total work is therefore proportional to $n$. There is no meaningful optimization beyond careful implementation.

The key observation is that nothing links different indices. All arrays are accessed at the same position, and each computation is self-contained. This eliminates any need for sorting, prefix structures, or dynamic programming. The only real task is evaluating a fixed arithmetic expression per index and applying a conditional maximum.

Because of this structure, any attempt to introduce more complex machinery would be unnecessary overhead. The optimal solution is simply the brute-force evaluation with correct handling of edge conditions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n)$ | $O(n)$ | Accepted |
| Optimal | $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Read the integer $n$, which determines how many independent contributions we must compute. Every subsequent value is aligned by index, so index $i$ in all arrays refers to the same logical item.
2. Read arrays $a$, $b$, and $c$. These represent fixed parameters used in the per-index scoring formula. Storing them allows direct indexed access during the final computation phase.
3. For each index $i$, read a pair $(t, s)$. These are the dynamic inputs that modify how the score is computed for that specific position.
4. If $s \le 0$, skip this index and add nothing to the answer. This condition reflects a problem-level constraint that disables contribution when the second parameter is non-positive.
5. Otherwise compute the candidate value

$$x = a_i - b_i \cdot t - 50 \cdot (s - 1).$$

This expression captures a linear decrease in score as $t$ and $s$ increase.
6. Compare this value with the fixed threshold $c_i$ and take the larger one. This ensures each index contributes at least its baseline cap when the computed formula drops too low.
7. Add the result to a running total.
8. After processing all indices, output the accumulated sum.

The correctness hinges on the fact that each index is processed independently and exactly once, so no interactions or ordering effects exist.

### Why it works

Each index contributes a value defined entirely by its own parameters and input pair. The computation is a pure function of $(a_i, b_i, c_i, t_i, s_i)$, and the final answer is the sum of these independent results. The only conditional branch is the $s \le 0$ case, which explicitly defines a zero contribution. Since no step modifies shared state across indices except through addition, the algorithm preserves correctness by construction.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = [0] * (n + 1)
    b = [0] * (n + 1)
    c = [0] * (n + 1)

    for i in range(1, n + 1):
        a[i] = int(input())
    for i in range(1, n + 1):
        b[i] = int(input())
    for i in range(1, n + 1):
        c[i] = int(input())

    ans = 0
    for i in range(1, n + 1):
        t, s = map(int, input().split())
        if s <= 0:
            continue
        val = a[i] - b[i] * t - 50 * (s - 1)
        if val < c[i]:
            val = c[i]
        ans += val

    print(ans)

if __name__ == "__main__":
    solve()
```

The solution reads the three parameter arrays first, ensuring that each index is fully initialized before processing queries. The loop over $t, s$ pairs is synchronized with index $i$, so each computation uses the correct parameters.

The key implementation detail is the early continue when $s \le 0$, which prevents incorrect arithmetic on invalid entries. Another important detail is using direct integer arithmetic without floating-point conversion, since all values remain within safe integer bounds.

## Worked Examples

Consider a small constructed example with $n = 3$.

Input arrays:

$a = [5, 10, 8]$, $b = [1, 2, 3]$, $c = [4, 3, 6]$

Query pairs:

$(t, s)$: $(2, 1), (3, 0), (1, 2)$

For each index:

| i | a[i] | b[i] | c[i] | t | s | computed value | final value |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 5 | 1 | 4 | 2 | 1 | 5 - 2 - 0 = 3 | max(4, 3) = 4 |
| 2 | 10 | 2 | 3 | 3 | 0 | skipped | 0 |
| 3 | 8 | 3 | 6 | 1 | 2 | 8 - 3 - 50 = -45 | max(6, -45) = 6 |

The final answer is $4 + 0 + 6 = 10$.

This trace shows how the $s \le 0$ condition fully removes index 2, and how the cap $c_i$ dominates when the linear expression becomes negative for index 3.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Each index is processed exactly once with constant-time arithmetic operations |
| Space | $O(n)$ | Storage for arrays $a$, $b$, and $c$ |

The runtime is linear in the input size, which is optimal because every index must be read and contributes independently to the final sum. Memory usage is also linear due to storing the three input arrays.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    solve()
    return sys.stdout.getvalue().strip()

# sample-style small case
assert run("2\n1\n2\n3\n1 1\n2 0\n") == "3", "skipped second index"

# all s <= 0
assert run("1\n10\n10\n10\n5 0\n") == "0", "no contributions"

# cap dominates
assert run("1\n5\n10\n100\n1 2\n") == "100", "c_i dominates negative expression"

# linear positive case
assert run("1\n100\n1\n0\n1 1\n") == "99", "direct formula"

# mixed case
assert run("3\n5\n10\n8\n1\n2\n3\n4\n3\n6\n2 1\n3 0\n1 2\n") == "10", "combined behavior"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single s=0 | 0 | skipping logic |
| cap-only case | c_i | max() behavior |
| mixed case | computed sum | interaction of rules |

## Edge Cases

When $s \le 0$, the algorithm explicitly skips computation. For input $t = 10, s = 0$ with any $a_i, b_i, c_i$, the loop executes `continue`, so no arithmetic is performed and the contribution remains zero. This prevents accidental use of a negative shift term $50 \cdot (s - 1)$, which would otherwise incorrectly increase the value.

When the computed expression becomes smaller than $c_i$, the algorithm replaces it with $c_i$. For example, with $a_i = 20$, $b_i = 5$, $c_i = 15$, $t = 3$, $s = 2$, the expression evaluates to $20 - 15 - 50 = -45$. The max operation forces the contribution to $15$, ensuring the result does not drop below the baseline cap.

These cases confirm that the two control rules, skipping invalid entries and enforcing a minimum cap, fully define correct behavior for all possible inputs.
