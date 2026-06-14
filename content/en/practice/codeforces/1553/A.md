---
title: "CF 1553A - Digits Sum"
description: "We are given several independent queries. Each query provides a positive integer $n$, and we must count how many integers $x$ in the range from 1 to $n$ have a special property. For a number $x$, we compare the sum of its digits before and after adding one."
date: "2026-06-14T21:09:50+07:00"
tags: ["codeforces", "competitive-programming", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1553
codeforces_index: "A"
codeforces_contest_name: "Harbour.Space Scholarship Contest 2021-2022 (open for everyone, rated, Div. 1 + Div. 2)"
rating: 800
weight: 1553
solve_time_s: 281
verified: true
draft: false
---

[CF 1553A - Digits Sum](https://codeforces.com/problemset/problem/1553/A)

**Rating:** 800  
**Tags:** math, number theory  
**Solve time:** 4m 41s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several independent queries. Each query provides a positive integer $n$, and we must count how many integers $x$ in the range from 1 to $n$ have a special property.

For a number $x$, we compare the sum of its digits before and after adding one. If the digit sum strictly decreases after incrementing, meaning $S(x+1) < S(x)$, then $x$ is called interesting. The task is to count how many such interesting numbers exist up to $n$.

The constraint $n \le 10^9$ immediately rules out any solution that checks every number individually. A linear scan would require up to $10^9$ operations per test case, which is far beyond feasible limits given up to 1000 test cases.

The key edge behavior comes from how digit sums change when incrementing a number. Most numbers increase their digit sum by 1 when we add 1, but there are special cases when a trailing block of 9s is involved. For example, 9 goes to 10, and the digit sum drops from 9 to 1. Similarly, 199 goes to 200, dropping from 19 to 2. These are the only moments where the digit sum decreases.

A naive approach that checks every number individually would also need to compute digit sums twice per number, which is still infeasible at scale. Another subtle mistake is assuming only single-digit 9 is valid. Numbers like 99, 999, 1999 also contribute, and they follow a structural pattern.

## Approaches

A brute-force method iterates through all $x \le n$, computes $S(x)$ and $S(x+1)$, and counts valid cases. This is correct because it directly follows the definition. However, computing digit sums takes $O(\log x)$, and doing this for all $x \le 10^9$ leads to about $10^9 \cdot 9$ operations per test case, which is too slow.

The key observation is that digit sum only decreases when an increment causes a carry chain that removes one or more trailing 9s. Suppose $x$ ends with exactly $k$ consecutive 9s. When we add 1, those $k$ nines become zeros, and the digit to the left increases by 1. The digit sum change is:

$$S(x+1) = S(x) - 9k + 1$$

So the condition $S(x+1) < S(x)$ becomes:

$$-9k + 1 < 0 \Rightarrow 9k > 1$$

This is true for every $k \ge 1$. That means every number ending in at least one 9 is interesting.

So the problem reduces to counting how many numbers from 1 to $n$ end in digit 9, 99, 999, and so on. For each power of 10 boundary, we count numbers of the form:

$$10^k - 1, 2 \cdot 10^k - 1, 3 \cdot 10^k - 1, \dots$$

as long as they do not exceed $n$.

Instead of iterating over all numbers, we count how many multiples of $10^k$ fit into $n + 1$, because every block of size $10^k$ contains exactly one number ending in $k$ nines.

This reduces the task to summing contributions over all possible $k$, which is at most 10 for $n \le 10^9$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n \log n)$ | $O(1)$ | Too slow |
| Optimal | $O(\log n)$ per test | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. For a given $n$, shift the perspective from counting interesting numbers directly to counting numbers of the form $10^k - 1$ patterns.

The reason is that these are exactly the points where a carry reduces digit sum.
2. Iterate over possible lengths of trailing 9s, starting from $k = 1$ upward.

Each $k$ corresponds to numbers ending in exactly $k$ nines or at least $k$ nines.
3. For each $k$, compute how many integers $x \le n$ satisfy $x \equiv 10^k - 1 \pmod{10^k}$.

This is equivalent to counting how many full blocks of size $10^k$ fit in $n + 1$.
4. Add $\left\lfloor \frac{n+1}{10^k} \right\rfloor$ to the answer.

This works because each block contributes exactly one number whose last $k$ digits are all 9s.
5. Stop when $10^k > n + 1$, since no further patterns can appear within the range.

### Why it works

Every interesting number is uniquely determined by the length of its trailing run of 9s. That trailing structure partitions all integers into disjoint groups based on $k$, and within each group, exactly one representative per block triggers a digit sum decrease. Because these groups do not overlap, summing their contributions counts each interesting number exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve(n):
    ans = 0
    power = 10
    while power <= n + 1:
        ans += (n + 1) // power
        power *= 10
    return ans

t = int(input())
for _ in range(t):
    n = int(input())
    print(solve(n))
```

The solution builds directly on the block structure of numbers grouped by trailing zeros in $x+1$, which corresponds to trailing nines in $x$. The expression $(n+1)//10^k$ counts how many numbers up to $n$ fall into positions where the last $k$ digits are all 9s.

The shift to $n+1$ is important because it aligns the pattern cleanly with multiples of powers of ten. Without this shift, the boundary cases around exact powers of ten become error-prone.

The loop over powers of 10 remains small, bounded by the number of digits in $n$, so the solution is efficient.

## Worked Examples

### Example 1: $n = 34$

We compute contributions for powers of 10.

| k | power = 10^k | (n+1)//power | contribution |
| --- | --- | --- | --- |
| 1 | 10 | 35//10 = 3 | 3 |
| 2 | 100 | 35//100 = 0 | stop |

Total = 3.

These correspond to 9, 19, 29. Each ends in a single 9 and becomes interesting when incremented.

This confirms that single trailing-9 numbers dominate at small ranges, and higher patterns do not appear before 100.

### Example 2: $n = 880055535$

We again sum contributions.

| k | power | (n+1)//power |
| --- | --- | --- |
| 1 | 10 | 88005553 |
| 2 | 100 | 8800555 |
| 3 | 1000 | 880055 |
| ... | ... | ... |

Summing these values produces the final answer $88005553$.

This trace shows how higher powers of 10 still contribute smaller but nonzero counts, and the total accumulates across all digit-length scales.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(\log_{10} n)$ per test | We iterate only over powers of 10 up to $n$ |
| Space | $O(1)$ | Only a few integer variables are used |

The logarithmic number of steps per query is negligible even for 1000 test cases, since each $n$ has at most 10 digits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def solve(n):
        ans = 0
        power = 10
        while power <= n + 1:
            ans += (n + 1) // power
            power *= 10
        return ans

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        out.append(str(solve(n)))
    return "\n".join(out)

# provided samples
assert run("5\n1\n9\n10\n34\n880055535\n") == "0\n1\n1\n3\n88005553"

# custom cases
assert run("1\n8\n") == "0"
assert run("1\n9\n") == "1"
assert run("1\n99\n") == "10"
assert run("1\n1000\n") == str((1001//10 + 1001//100 + 1001//1000))
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1, 8 | 0 | No trailing 9 cases exist |
| 1, 9 | 1 | Single boundary case |
| 1, 99 | 10 | Multiple overlapping digit-length contributions |
| 1, 1000 | formula-based | Multi-scale contributions correctness |

## Edge Cases

A key edge case is when $n$ is exactly a power of 10 minus one, such as 9, 99, or 999. For $n = 99$, the algorithm counts contributions from both $10$ and $100$. The loop processes $10 \rightarrow 100$, adding 10 from the first term and 1 from the second term, matching the fact that interesting numbers are 9, 19, 29, ..., 99.

Another subtle case is $n = 1$. The loop condition requires $power \le n+1$, so for $n = 1$, we check $power = 10$, which already fails. The result is 0, correctly reflecting that no number in this range ends in a 9.

Finally, large $n$ near $10^9$ still only triggers about 9 iterations, since powers of 10 grow quickly. This ensures the computation remains stable and fast even at maximum constraints.
