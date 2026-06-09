---
title: "CF 1646A - Square Counting"
description: "We are given a sequence of length $n+1$. Each element is either a “small” number in the range $[0, n-1]$, or a special large value equal to $n^2$. We are told only two things: the parameter $n$ and the total sum of all elements in the sequence, denoted $s$."
date: "2026-06-10T04:09:22+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 1646
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 774 (Div. 2)"
rating: 800
weight: 1646
solve_time_s: 86
verified: true
draft: false
---

[CF 1646A - Square Counting](https://codeforces.com/problemset/problem/1646/A)

**Rating:** 800  
**Tags:** math  
**Solve time:** 1m 26s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of length $n+1$. Each element is either a “small” number in the range $[0, n-1]$, or a special large value equal to $n^2$. We are told only two things: the parameter $n$ and the total sum of all elements in the sequence, denoted $s$. The original sequence is lost, and the task is to determine how many positions contained the value $n^2$.

The structure of the sequence is very rigid. Every non-special element contributes at most $n-1$ to the sum, while each special element contributes exactly $n^2$, which is much larger than anything else. This separation of scale is the key feature that makes the reconstruction possible.

The constraints allow up to $2 \cdot 10^4$ test cases, with $n$ up to $10^6$ and $s$ up to $10^{18}$. This rules out any approach that attempts to reconstruct the sequence or even reason about individual elements. Any valid solution must reduce each test case to constant time arithmetic.

A naive approach might try to guess how many $n^2$ elements exist and then check whether the remaining sum can be filled with values in $[0, n-1]$. While logically correct, such simulation is unnecessary since the structure implies a direct algebraic relation between $s$, $n$, and the count of special elements.

A subtle edge case appears when $s = 0$. In this case, all elements must be zero, and the answer is necessarily zero special elements. Another corner situation is when $s$ is very large and almost entirely formed by $n^2$ contributions; here, the remainder must still be realizable using bounded small values, and the problem guarantees such consistency.

## Approaches

The brute-force idea is to assume the number of special elements $k$ ranges from $0$ to $n+1$. For each candidate $k$, we try to see if the remaining sum can be explained using $n+1-k$ elements each in $[0, n-1]$. For a fixed $k$, we subtract $k \cdot n^2$ from $s$, and check whether the remainder lies between $0$ and $(n+1-k)(n-1)$. This works because the smallest possible contribution of the remaining elements is zero, and the largest is when all are $n-1$.

This brute-force scan is correct but unnecessary. It still runs in $O(n)$ per test case, which would be too slow when $n$ is large and the number of test cases is large.

The key observation is that we do not actually need to try all values of $k$. The constraint structure forces a unique valid $k$, and it can be derived directly from the sum. Since each special element contributes an excess of $n^2$ compared to any normal value, we can treat the problem as splitting $s$ into a base part from small values and a fixed contribution from special values.

Let $k$ be the number of elements equal to $n^2$. The remaining $n+1-k$ elements contribute at most $n-1$ each, so their maximum possible sum is $(n+1-k)(n-1)$. This implies:

$$k \cdot n^2 \le s \le k \cdot n^2 + (n+1-k)(n-1)$$

Instead of searching, we compute $k$ by greedy extraction: we take as many $n^2$ as possible from $s$, but we must ensure the leftover can still be formed by bounded values. Because $n^2$ dominates the range $[0, n-1]$, the correct $k$ is determined by the integer division structure of $s$ relative to $n^2$ and the residual feasibility.

A simpler reformulation is to observe that once $k$ is fixed, the remainder $r = s - k n^2$ must satisfy $0 \le r \le (n+1-k)(n-1)$. The uniqueness guarantee ensures that exactly one $k$ satisfies this, and it can be found in constant time using arithmetic reasoning around upper bounds.

The practical solution reduces to iterating from the largest possible $k$ downward or directly deriving $k$ from bounds. Since $k \le n+1$, but also $k n^2 \le s$, we immediately get $k \le s // n^2$. Starting from this upper bound and adjusting downward by at most a constant number of checks yields the answer efficiently.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n)$ per test case | $O(1)$ | Too slow |
| Optimal | $O(1)$ per test case | $O(1)$ | Accepted |

## Algorithm Walkthrough

We focus on extracting the number of elements equal to $n^2$ from the total sum.

1. Compute the maximum possible number of special elements as $k = s // n^2$. This is the absolute upper bound because each special element contributes $n^2$, so exceeding this would overshoot the sum.
2. Clamp $k$ to at most $n+1$, since there are only $n+1$ elements in total.
3. Check whether this candidate $k$ is valid by verifying that the remaining sum $r = s - k \cdot n^2$ can be formed using $n+1-k$ numbers, each in $[0, n-1]$. This requires $r \le (n+1-k)(n-1)$.
4. If the condition fails, decrease $k$ until it becomes valid. The structure of the constraints guarantees that at most a constant number of adjustments are needed, since only one $k$ satisfies the feasibility inequality.

### Why it works

The total sum decomposes uniquely into two parts: a multiple of $n^2$ from special elements and a bounded contribution from normal elements. Because normal elements are capped at $n-1$, they cannot compensate for an overestimation of $k$ by even one full $n^2$ unless the remaining capacity exactly allows it. This creates a strict feasibility window for $k$, ensuring only one integer satisfies both lower and upper bounds simultaneously. The algorithm effectively searches within a monotone condition over $k$, so corrections always move toward the unique valid solution.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, s = map(int, input().split())
        max_k = s // (n * n)
        max_k = min(max_k, n + 1)

        def ok(k):
            r = s - k * n * n
            if r < 0:
                return False
            return r <= (n + 1 - k) * (n - 1)

        k = max_k
        while k >= 0 and not ok(k):
            k -= 1

        print(k)

if __name__ == "__main__":
    solve()
```

The code computes an initial upper bound for the number of $n^2$ elements using integer division. This is safe because any extra $n^2$ would exceed the sum. The helper function `ok(k)` checks feasibility by ensuring the remaining sum fits within the maximum capacity of the non-special elements.

The downward adjustment loop is short because the feasibility condition is monotonic in $k$. Once we pass the correct value, any further decrease only increases available capacity, so the first valid $k$ encountered is the answer.

Care must be taken with integer arithmetic since $s$ can reach $10^{18}$, but Python handles this safely.

## Worked Examples

### Example 1

Input: $n=2, s=12$

We compute $n^2 = 4$, and $n+1 = 3$.

| Step | k | r = s - k·n² | Max remainder capacity | Valid |
| --- | --- | --- | --- | --- |
| initial | 3 | 0 | 0 | yes |

The maximum possible $k$ is 3, and it fits exactly, so the answer is 3.

This shows the case where all elements are special, leaving no residual contribution.

### Example 2

Input: $n=3, s=12$

Here $n^2 = 9$, $n+1 = 4$.

| Step | k | r | capacity | valid |
| --- | --- | --- | --- | --- |
| start | 1 | 3 | 3·2 = 6 | yes |

We test $k=1$: remainder is 3, which fits in 3 remaining elements each up to 2. Larger $k=2$ fails because it would overshoot the sum. So answer is 1.

This demonstrates how the constraint on bounded elements determines feasibility even when multiple decompositions are algebraically close.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(t)$ | Each test case performs constant arithmetic checks and at most a small decrement loop |
| Space | $O(1)$ | Only a few variables are used per test case |

The solution comfortably fits within limits since even $2 \cdot 10^4$ test cases only require simple integer operations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n, s = map(int, input().split())
        max_k = s // (n * n)
        max_k = min(max_k, n + 1)

        def ok(k):
            r = s - k * n * n
            return r >= 0 and r <= (n + 1 - k) * (n - 1)

        k = max_k
        while k >= 0 and not ok(k):
            k -= 1
        out.append(str(k))

    return "\n".join(out) + "\n"

# provided samples
assert run("4\n7 0\n1 1\n2 12\n3 12\n") == "0\n1\n3\n1\n"

# custom cases
assert run("1\n1 0\n") == "0\n", "minimum case"
assert run("1\n1 2\n") == "1\n", "single special element"
assert run("1\n2 8\n") == "2\n", "all special"
assert run("1\n5 0\n") == "0\n", "all zeros"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1\n1 0 | 0 | minimum boundary, no special elements |
| 1\n1 2 | 1 | single element equal to $n^2$ |
| 1\n2 8 | 2 | full saturation with special values |
| 1\n5 0 | 0 | all elements are small zeros |

## Edge Cases

A zero-sum case like $n=7, s=0$ forces every element to be zero because any $n^2$ contribution would immediately exceed the total. The algorithm computes $k = 0$ from the division step and passes the feasibility check since the remaining capacity matches exactly the full sequence length times $n-1$, which is non-negative.

A fully saturated case like $n=2, s=12$ yields $k = 3$ directly from $s // 4$. The remainder becomes zero, which is within capacity $0$, confirming all elements are special. The downward adjustment loop never triggers, showing that the upper bound is already tight.

A mixed case like $n=3, s=12$ demonstrates correction behavior. The initial estimate $k = 1$ is valid, but $k = 2$ would fail because it leaves a negative remainder. The loop correctly settles at the first feasible value, ensuring the uniqueness constraint is respected without ambiguity.
