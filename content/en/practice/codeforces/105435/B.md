---
title: "CF 105435B - Divisor Query"
description: "We are given a sequence of queries, each describing a numeric interval $[l, r]$. For every query, we are asked to count how many integers inside that interval have a specific property related to their number of divisors."
date: "2026-06-23T03:48:30+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105435
codeforces_index: "B"
codeforces_contest_name: "TSEC Round 2 (Div. 3)"
rating: 0
weight: 105435
solve_time_s: 82
verified: true
draft: false
---

[CF 105435B - Divisor Query](https://codeforces.com/problemset/problem/105435/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 22s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of queries, each describing a numeric interval $[l, r]$. For every query, we are asked to count how many integers inside that interval have a specific property related to their number of divisors. One type of query asks for integers whose divisor count is odd, and the other asks for integers whose divisor count is even.

A key observation comes from number theory rather than simulation. Almost every integer has divisors that pair up: if $d$ divides $n$, then $n/d$ also divides $n$. This pairing suggests that divisor counts are usually even. The only time a divisor does not pair with a distinct partner is when $d = n/d$, meaning $d^2 = n$. That happens exactly when $n$ is a perfect square.

This immediately transforms the problem: numbers with an odd number of divisors are exactly perfect squares, and all other numbers have an even number of divisors. So each query is really asking one of two things over a range: count perfect squares, or count non-perfect squares.

The constraints push us away from any per-number processing inside each query. With up to $10^6$ queries and values up to $10^9$, iterating over ranges or checking divisors per number is impossible. Even logarithmic work per query would be borderline, so the solution must reduce each query to constant time arithmetic after some reasoning or precomputation.

Edge cases arise when $l = r$, where the interval contains a single number, and when the interval spans boundaries of perfect squares. For example, in $[8, 9]$, only 9 is a perfect square, so exactly one number has an odd divisor count. A naive approach that checks divisors directly would still work conceptually, but would time out. Another subtle issue is misunderstanding the parity rule: checking divisors directly per number would fail under time constraints even though logically correct.

## Approaches

A brute-force solution processes each query independently. For every integer in $[l, r]$, we compute its divisor count by iterating up to its square root and counting factor pairs. This correctly identifies whether the divisor count is odd or even. However, the interval size can be large, and with up to $10^6$ queries, this becomes computationally impossible. In the worst case, even a single query over a large range costs $O(\sqrt{n})$ per number, leading to roughly $O((r-l+1)\sqrt{r})$, which is far beyond feasible limits.

The key insight is to stop thinking about divisors explicitly and instead classify numbers by structure. Since only perfect squares have an unpaired divisor, the entire problem reduces to counting perfect squares inside a range. Once this is recognized, each query becomes a simple arithmetic problem: count how many integers $x$ satisfy $l \le x \le r$ and $x = k^2$. That is equivalent to counting integers $k$ such that $\lceil \sqrt{l} \rceil \le k \le \lfloor \sqrt{r} \rfloor$. This reduces every query to constant time using integer square root computations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O((r-l+1)\sqrt{r})$ per query | $O(1)$ | Too slow |
| Optimal | $O(1)$ per query | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Observe that numbers with odd divisor count are exactly perfect squares. This replaces divisor computation with a structural property check.
2. For each query $(type, l, r)$, compute the integer square root bounds of the interval. The smallest $k$ such that $k^2 \ge l$ is $\lceil \sqrt{l} \rceil$, and the largest $k$ such that $k^2 \le r$ is $\lfloor \sqrt{r} \rfloor$.
3. The number of perfect squares in the interval is then $\max(0, \lfloor \sqrt{r} \rfloor - \lceil \sqrt{l} \rceil + 1)$. This directly answers type 1 queries.
4. For type 2 queries, the interval size is $r - l + 1$, and all non-square numbers are counted by subtracting the square count.

Each step converts a combinatorial counting problem into arithmetic over indices of squares rather than over the original values.

### Why it works

Every positive integer has a divisor pairing structure $d \leftrightarrow n/d$. These pairs are distinct unless $d = n/d$, which happens only when $n$ is a perfect square. That single unpaired divisor makes the total count odd. Since there is exactly one such unpaired divisor per square number and none otherwise, counting odd-divisor numbers is equivalent to counting squares. The algorithm relies entirely on this bijection between “odd divisor count” and “square numbers in the interval”, ensuring correctness for all inputs.

## Python Solution

```python
import sys
input = sys.stdin.readline
import math

def solve():
    q = int(input())
    out = []
    
    for _ in range(q):
        t, l, r = map(int, input().split())
        
        left = math.isqrt(l)
        if left * left < l:
            left += 1
        right = math.isqrt(r)
        
        squares = 0
        if right >= left:
            squares = right - left + 1
        
        total = r - l + 1
        
        if t == 1:
            out.append(str(squares))
        else:
            out.append(str(total - squares))
    
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution hinges on `math.isqrt`, which gives a precise integer square root without floating-point errors. The adjustment for the left boundary ensures we correctly handle cases where $l$ is itself a perfect square; otherwise we would incorrectly shift the range.

The total count is computed per query, and the square count is derived purely from integer arithmetic. No precomputation is required because each query is independent.

## Worked Examples

Consider a range where we query both types:

Input:

```
1
1 8 20
```

We compute integer square bounds.

| Step | l | r | floor(sqrt(r)) | ceil(sqrt(l)) | squares | result type 1 | result type 2 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Initial | 8 | 20 | - | - | - | - | - |
| sqrt bounds | 8 | 20 | 4 | 3 | 4-3+1=2 | 2 | 11 |

The perfect squares are 9 and 16, so type 1 returns 2 and type 2 returns the remaining 9 numbers.

Now consider a boundary-heavy case:

Input:

```
1
1 1 10
```

| Step | l | r | floor(sqrt(r)) | ceil(sqrt(l)) | squares | type 1 |
| --- | --- | --- | --- | --- | --- | --- |
| Initial | 1 | 10 | - | - | - | - |
| sqrt bounds | 1 | 10 | 3 | 1 | 3 | 3 |

Squares are 1, 4, 9, giving exactly 3 valid numbers. This confirms correctness when both boundaries are perfect squares.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(q)$ | Each query performs constant-time integer square root operations and arithmetic |
| Space | $O(1)$ | Only a fixed number of variables are used |

The solution comfortably handles $10^6$ queries because each one is reduced to a handful of integer operations. Even in Python, integer square root is fast enough for this scale.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import math

    def solve():
        q = int(input())
        out = []
        for _ in range(q):
            t, l, r = map(int, input().split())
            left = math.isqrt(l)
            if left * left < l:
                left += 1
            right = math.isqrt(r)
            squares = max(0, right - left + 1)
            total = r - l + 1
            if t == 1:
                out.append(str(squares))
            else:
                out.append(str(total - squares))
        return "\n".join(out)

    return solve()

# provided sample (partial format assumed)
assert run("""1
1 1 10
""") == "3"

# all equal bounds
assert run("""1
1 16 16
""") == "1"

# non-square single element
assert run("""1
1 8 8
""") == "0"

# full range mix
assert run("""1
2 1 10
""") == "7"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 10 (type 1) | 3 | correct square counting in range |
| 16 16 | 1 | single perfect square boundary case |
| 8 8 | 0 | single non-square case |
| 2 1 10 | 7 | complement logic correctness |

## Edge Cases

A critical edge case is when $l$ itself is a perfect square. For example, $[9, 9]$. The integer square root of 9 is 3, and since $3^2 = 9$, the lower bound must include 3. The adjustment step in the code ensures we do not mistakenly exclude it.

Another case is when there are no squares in the interval, such as $[8, 8]$. Here $\lfloor \sqrt{8} \rfloor = 2$ and $\lceil \sqrt{8} \rceil = 3$, producing a negative count. The implementation guards against this by clamping at zero implicitly via the `if right >= left` check.

Large intervals such as $[1, 10^9]$ stress the correctness of integer square root boundaries. The algorithm still reduces the problem to counting integers from 1 to 31622, showing that the transformation remains stable even at scale.
