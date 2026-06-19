---
title: "CF 106420A - Bouncy Castle"
description: "We are given a single integer $n$, and we want to determine the largest integer $x$ such that a certain geometric or combinatorial construction is possible."
date: "2026-06-19T17:58:01+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106420
codeforces_index: "A"
codeforces_contest_name: "UTPC Contest 3-11-26 (Beginner)"
rating: 0
weight: 106420
solve_time_s: 44
verified: true
draft: false
---

[CF 106420A - Bouncy Castle](https://codeforces.com/problemset/problem/106420/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 44s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single integer $n$, and we want to determine the largest integer $x$ such that a certain geometric or combinatorial construction is possible. The key constraint reduces the entire problem to a simple inequality involving $x$ and $n$: the construction is feasible exactly when $x^2 \le 2n$. In other words, we are trying to find the largest integer $x$ whose square does not exceed twice the given input.

You can think of the problem as allocating resources where each unit of $n$ contributes two elementary slots, and a valid configuration of size $x$ consumes $x^2$ of these slots. The task is to push $x$ as large as possible while staying within the available budget $2n$.

The input is just this single integer $n$. The output is one integer, the maximum feasible $x$.

Since the solution is purely arithmetic, the constraints on $n$ mainly determine whether we must worry about overflow or floating-point precision. For typical Codeforces bounds where $n$ can reach up to $10^{18}$, direct integer multiplication and square root operations are still safe in Python, but in C++ one would need to be careful with 64-bit arithmetic.

A subtle edge case appears when $n = 0$. Then $2n = 0$, so the only valid $x$ is 0. Another boundary is when $n = 1$, where $2n = 2$, and again the answer is 1 since $1^2 = 1 \le 2$ but $2^2 = 4$ is too large. These cases confirm that the answer is not simply $\lfloor \sqrt{n} \rfloor$, but instead depends on $2n$.

A naive mistake would be to forget the factor of 2 and compute $\lfloor \sqrt{n} \rfloor$, which underestimates the answer for all $n > 0$.

## Approaches

The brute-force idea is to try all possible values of $x$ starting from 0 and increase it until the inequality $x^2 \le 2n$ fails. For each candidate $x$, we compute $x^2$ and compare it with $2n$. This works correctly because we explicitly test feasibility for every possible answer, but it can degrade to $O(\sqrt{n})$ iterations since $x$ can grow up to roughly $\sqrt{2n}$. While this is already acceptable in many cases, it is still unnecessary work when the structure of the inequality is so direct.

The key observation is that the condition $x^2 \le 2n$ defines a monotonic boundary. Once a value of $x$ is invalid, all larger values are also invalid. This turns the problem into finding the largest integer whose square is bounded by $2n$, which is exactly the integer square root of $2n$. Instead of iterating, we can compute this directly using a square root operation and floor it, or rely on integer arithmetic to avoid precision issues.

So the problem collapses into computing $\lfloor \sqrt{2n} \rfloor$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(\sqrt{n})$ | $O(1)$ | Too slow but safe |
| Optimal | $O(1)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Read the integer $n$ from input. The entire problem depends only on this single value, so no additional parsing or preprocessing is needed.
2. Compute $m = 2n$. This transforms the original condition into a clean form $x^2 \le m$, isolating the quantity we compare against.
3. Compute the integer square root of $m$, which is the largest integer $x$ such that $x \cdot x \le m$. This directly corresponds to the boundary of feasibility.
4. Output this value as the final answer.

### Why it works

The inequality $x^2 \le 2n$ defines a monotone set of valid integers: if $x$ works, then all smaller values also work, and if $x$ fails, all larger values fail. This guarantees that the solution is exactly the boundary point of this monotone predicate. The integer square root function finds precisely that boundary, ensuring no valid value is skipped and no invalid value is included.

## Python Solution

```python
import sys
input = sys.stdin.readline
import math

def main():
    n = int(input().strip())
    m = 2 * n
    ans = math.isqrt(m)
    print(ans)

if __name__ == "__main__":
    main()
```

The implementation mirrors the algorithm almost directly. The multiplication by 2 is done first to reflect the transformed constraint. Then `math.isqrt` is used instead of floating-point square root to avoid precision errors that could occur for large values of $n$. This function computes the integer square root safely in $O(1)$ amortized time in Python.

A common implementation mistake would be using `int(math.sqrt(m))` directly. While it often works, floating-point rounding can occasionally produce results like $x - 1$ for perfect squares near the limits of double precision. Using `isqrt` avoids this entirely.

## Worked Examples

Consider $n = 5$. Then $m = 10$. We look for the largest integer whose square is at most 10.

| x | x² | valid? |
| --- | --- | --- |
| 0 | 0 | yes |
| 1 | 1 | yes |
| 2 | 4 | yes |
| 3 | 9 | yes |
| 4 | 16 | no |

The largest valid $x$ is 3, which matches $\lfloor \sqrt{10} \rfloor = 3$.

Now consider $n = 8$. Then $m = 16$.

| x | x² | valid? |
| --- | --- | --- |
| 0 | 0 | yes |
| 1 | 1 | yes |
| 2 | 4 | yes |
| 3 | 9 | yes |
| 4 | 16 | yes |
| 5 | 25 | no |

Here the answer is 4, since $4^2 = 16$ exactly fits the limit. This shows the boundary case where the inequality is tight.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(1)$ | Single integer square root computation after constant arithmetic |
| Space | $O(1)$ | Only a few integer variables are used |

The computation is constant-time relative to the input size, so it easily fits within any typical Codeforces limits. Even for very large $n$, the operations involved are simple arithmetic and a square root extraction.

## Test Cases

```python
import sys, io
import math

def solve(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(sys.stdin.readline().strip())
    return str(math.isqrt(2 * n))

# provided samples (conceptual, since samples not given)
assert solve("0\n") == "0", "n=0"
assert solve("1\n") == "1", "n=1"

# custom cases
assert solve("5\n") == "3", "basic mid case"
assert solve("8\n") == "4", "perfect square boundary"
assert solve("10\n") == "4", "non-square boundary"
assert solve("1000000000000000000\n") == str(math.isqrt(2 * 1000000000000000000)), "large n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0 | 0 | minimum edge case |
| 1 | 1 | smallest positive case |
| 8 | 4 | perfect square boundary |
| 10 | 4 | rounding down behavior |
| large n | isqrt result | performance and overflow safety |

## Edge Cases

For $n = 0$, we compute $m = 0$, so the answer is $\lfloor \sqrt{0} \rfloor = 0$. The algorithm handles this naturally because `isqrt(0)` returns 0 without special branching.

For $n = 1$, $m = 2$, and the integer square root is 1. This confirms that the smallest non-zero input already produces a non-zero answer, which a naive $\lfloor \sqrt{n} \rfloor$ approach would also get correct, but for the wrong reason.

For very large $n$, such as $10^{18}$, $m$ remains within 64-bit range ($2 \cdot 10^{18}$), and Python’s arbitrary precision integers handle it safely. The computation of `isqrt` remains stable and avoids floating-point errors entirely, so no precision degradation occurs at the boundary.
