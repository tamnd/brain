---
title: "CF 1175A - From Hero to Zero"
description: "We are given a number $n$ and a parameter $k$. Starting from $n$, we want to reach zero using two allowed operations: subtract one, or if the current value is divisible by $k$, replace it with the quotient after dividing by $k$."
date: "2026-06-15T17:25:40+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1175
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 66 (Rated for Div. 2)"
rating: 900
weight: 1175
solve_time_s: 222
verified: true
draft: false
---

[CF 1175A - From Hero to Zero](https://codeforces.com/problemset/problem/1175/A)

**Rating:** 900  
**Tags:** implementation, math  
**Solve time:** 3m 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a number $n$ and a parameter $k$. Starting from $n$, we want to reach zero using two allowed operations: subtract one, or if the current value is divisible by $k$, replace it with the quotient after dividing by $k$. Each operation costs one step, and the goal is to minimize the total number of steps.

This is essentially a process of repeatedly shrinking a number either gradually or by occasional large jumps when divisibility allows. The difficulty is that division is only occasionally available, so we cannot freely “greedily divide” without accounting for the steps required to make the number divisible.

The constraints are extremely large, with $n$ and $k$ up to $10^{18}$. This immediately rules out any simulation that decrements one by one. Even a linear scan in terms of $n$ is impossible, since $10^{18}$ operations is far beyond the time limit. Any valid solution must reduce the number in logarithmic or near-logarithmic phases, typically by skipping long stretches of consecutive subtractions.

A naive approach would simulate the process: if $n$ is not divisible by $k$, subtract one repeatedly until it becomes divisible, then divide. This is correct but can degrade badly when $n$ is large and $k$ is small. For example, if $n = 10^{18}$ and $k = 2$, a naive simulation would repeatedly subtract one to reach an even number, then divide, repeating this pattern many times. The number of steps becomes proportional to $n$, which is infeasible.

Another subtle edge case arises when $k = 1$. Division by one never changes the value, so the only meaningful operation is subtracting one. In that case, the answer is simply $n$. Any implementation that does not guard against this case may loop forever or repeatedly apply a useless division.

## Approaches

The brute-force strategy is to always apply the best available move step by step. At each state, if divisible by $k$, divide; otherwise subtract one. This is locally reasonable because division shrinks the number quickly, and subtraction prepares for future divisions.

This works correctly but fails in efficiency because the subtraction phase dominates runtime. In the worst case, before every division, we may need up to $k-1$ subtractions, and this can repeat many times across the entire range down to zero. Since $n$ is up to $10^{18}$, this leads to an unbounded number of operations.

The key observation is that we never need to simulate subtraction one by one. Instead, we can jump directly to the nearest multiple of $k$. If the current number is $x$, we compute $x \bmod k$. That value tells us exactly how many subtractions are needed to reach a divisible state. We apply them in one aggregated step. After that, if the number is still at least $k$, we perform a division and continue.

This transforms the process into a sequence of large jumps followed by a small number of divisions, reducing the number of iterations to roughly $O(\log_k n)$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n)$ | $O(1)$ | Too slow |
| Optimal | $O(\log n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We repeatedly reduce the number using a combination of batching subtractions and occasional divisions.

1. If $k = 1$, the only useful move is subtracting one, so the answer is $n$. We return immediately. This avoids infinite loops caused by division that changes nothing.
2. While $n \ge k$, we first compute $r = n \bmod k$. This tells us how far we are from the nearest smaller multiple of $k$.
3. We subtract $r$ in one step, reducing $n$ to a multiple of $k$, and add $r$ to the answer. This replaces many unit operations with a single arithmetic jump.
4. We then divide $n$ by $k$, incrementing the answer by one. This is the only valid division step and gives a large reduction in magnitude.
5. We repeat this process until $n < k$, meaning division is no longer possible.
6. Finally, we subtract the remaining $n$ to reach zero, adding $n$ to the answer.

The reason this works is that at every stage we are converting the optimal local strategy into an exact cost decomposition: any valid sequence must eventually remove the same remainder before a division can happen, so paying for it in bulk does not change optimality.

### Why it works

The invariant is that after each iteration, we have accounted for the exact number of subtraction operations needed to bring the current state to the nearest valid division point. Since division is always performed as soon as it becomes possible, and every subtraction is counted exactly once, no alternative ordering of operations can reduce the total cost. Any optimal path must still “clear” the remainder before dividing, so grouping those operations preserves correctness while removing inefficiency.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []
    
    for _ in range(t):
        n, k = map(int, input().split())
        
        if k == 1:
            out.append(str(n))
            continue
        
        steps = 0
        
        while n >= k:
            r = n % k
            steps += r
            n -= r
            n //= k
            steps += 1
        
        steps += n
        out.append(str(steps))
    
    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The code directly implements the batching idea. The modulus operation computes how many decrements are needed before a division. After applying them, we divide once and continue. The loop terminates when the number is smaller than $k$, at which point only subtraction remains.

The special case $k = 1$ is handled explicitly to avoid unnecessary looping and to correctly reflect that only decrementing is possible.

## Worked Examples

### Example 1

Input:

```
n = 59, k = 3
```

| n | n % k | subtractions | division | total steps |
| --- | --- | --- | --- | --- |
| 59 | 2 | 2 | 1 | 3 |
| 19 | 1 | 1 | 1 | 5 |
| 6 | 0 | 0 | 1 | 6 |
| 2 | - | 2 (final) | 0 | 8 |

The process shows repeated compression: each division is preceded by exactly enough subtractions to align the number. The final phase is pure subtraction once the value drops below $k$.

### Example 2

Input:

```
n = 10^18, k = 10
```

| n | n % k | subtractions | division | total steps |
| --- | --- | --- | --- | --- |
| 10^18 | 0 | 0 | 1 | 1 |
| 10^17 | 0 | 0 | 1 | 2 |
| ... | ... | ... | ... | 19 |

This case shows repeated clean divisions because the number is already aligned with powers of 10. The process becomes a pure logarithmic chain.

The trace confirms that the algorithm behaves optimally when divisibility is frequent and still remains efficient when it is not.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(\log_k n)$ | Each division reduces the magnitude by a factor of $k$, and each iteration performs constant work |
| Space | $O(1)$ | Only a few integer variables are maintained |

The runtime is easily fast enough for $t \le 100$ and values up to $10^{18}$, since even in the worst case the number of iterations per test case is small.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    input = sys.stdin.readline
    t = int(input())
    res = []
    
    for _ in range(t):
        n, k = map(int, input().split())
        if k == 1:
            res.append(str(n))
            continue
        
        steps = 0
        while n >= k:
            r = n % k
            steps += r
            n -= r
            n //= k
            steps += 1
        steps += n
        res.append(str(steps))
    
    return "\n".join(res)

# provided samples
assert run("2\n59 3\n1000000000000000000 10\n") == "8\n19"

# custom cases
assert run("1\n1 2\n") == "1", "minimum case"
assert run("1\n10 10\n") == "2", "single division then subtraction"
assert run("1\n100 2\n") == "9", "repeated halving structure"
assert run("1\n5 1\n") == "5", "k=1 edge case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 2 / 1 | 1 | smallest non-zero case |
| 10 10 | 2 | exact divisibility then finish |
| 100 2 | 9 | repeated mixed operations |
| 5 1 | 5 | degenerate division behavior |

## Edge Cases

When $k = 1$, division is always possible but useless. The algorithm explicitly returns $n$, matching the fact that only subtraction reduces the number. For input $n = 5, k = 1$, we directly output 5.

When $n < k$, no division occurs at all. For example, $n = 7, k = 10$, the loop is skipped and the answer is simply 7, since we only subtract down to zero.

When $n$ is exactly divisible by $k$, such as $n = 100, k = 10$, the remainder is zero, so we divide immediately without extra cost. The algorithm correctly performs one step per division until termination.
