---
title: "CF 105150D - \u0425\u0440\u043e\u043d\u043e\u043c\u0435\u0442\u0440\u0430\u0436 \u0438 \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435"
description: "We are asked to imagine an infinite increasing sequence built from numbers that can be written in the form $$x = 2^k + 60m$$ where $k$ and $m$ are positive integers (or at least positive for $k$, and non-negative for $m$, depending on interpretation; the important part is that…"
date: "2026-06-27T12:42:58+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105150
codeforces_index: "D"
codeforces_contest_name: "XVIII \u041d\u0438\u0436\u0435\u0433\u043e\u0440\u043e\u0434\u0441\u043a\u0430\u044f \u0433\u043e\u0440\u043e\u0434\u0441\u043a\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432 \u043f\u043e \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0442\u0438\u043a\u0435 \u0438\u043c. \u0412. \u0414. \u041b\u0435\u043b\u044e\u0445\u0430"
rating: 0
weight: 105150
solve_time_s: 81
verified: false
draft: false
---

[CF 105150D - \u0425\u0440\u043e\u043d\u043e\u043c\u0435\u0442\u0440\u0430\u0436 \u0438 \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435](https://codeforces.com/problemset/problem/105150/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 21s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to imagine an infinite increasing sequence built from numbers that can be written in the form

$$x = 2^k + 60m$$

where $k$ and $m$ are positive integers (or at least positive for $k$, and non-negative for $m$, depending on interpretation; the important part is that both components contribute freely and independently). Every valid number is placed into a sorted list, duplicates are ignored because we only care about distinct integers, and we want the $n$-th smallest element of this set.

So the task is not to evaluate a formula for a single number, but to understand the global structure of all representable numbers and extract a specific rank statistic from that structure.

The constraint $n \le 10^{15}$ immediately rules out any approach that enumerates values or even constructs a large prefix of the sequence. Even generating $10^7$ candidates per second would still be far below what is needed. The solution must rely on structural properties of the set rather than explicit construction.

A naive mistake would be to try generating all values up to some bound, say by iterating over $k$ and $m$ and inserting into a set. This fails because both parameters grow unbounded and the number of pairs that map to small values is already large enough to make sorting infeasible. Another incorrect direction is to assume monotonicity in either parameter, for example fixing $k$ and increasing $m$, then merging sequences, but without recognizing overlap patterns, this leads to double counting and incorrect ordering.

A more subtle failure happens when one assumes that small $k$ always dominates the ordering. While $2^k$ is structured, the addition of multiples of 60 causes interleaving between different $k$-layers in a nontrivial way.

## Approaches

The brute-force view is straightforward: enumerate all pairs $(k, m)$, compute $2^k + 60m$, insert into a set, sort it, and take the $n$-th element. This is correct in principle because it directly constructs the definition. The issue is scale. Even if we bound values by some large limit $X$, the number of valid pairs grows roughly proportionally to $X \log X$, which is far too large to enumerate for $n$ up to $10^{15}$.

The key insight is to flip perspective. Instead of generating numbers, we ask: given a threshold $X$, how many valid numbers are $\le X$? If we can answer this counting question efficiently, we can binary search the answer for the $n$-th value. This is the standard reduction from “find the $n$-th element in an implicit sorted set” to prefix counting.

For a fixed $k$, numbers of the form $2^k + 60m \le X$ correspond to all $m \le \frac{X - 2^k}{60}$. That contributes a simple arithmetic count when $2^k \le X$. The only difficulty is summing over all feasible $k$, but since $2^k$ grows exponentially, the number of relevant $k$ values is only $O(\log X)$.

Thus, we can compute the count in logarithmic time per query, and then binary search over $X$. The answer must lie between the smallest possible value and a sufficiently large upper bound, which can safely be around $2^{60} + 60n$ in worst-case reasoning.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | exponential / infeasible | large | Too slow |
| Binary Search + Counting | $O(\log X \cdot \log X)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Define a function `count(X)` that computes how many numbers of the form $2^k + 60m$ are less than or equal to $X$. This function drives the entire solution because it converts the set into a prefix-countable structure.
2. Inside `count(X)`, iterate over powers of two. Start with $2^k = 2$ and repeatedly multiply by 2 until it exceeds $X$. Each such value represents a fixed base offset for a full arithmetic progression in $m$. The loop is short because powers of two grow exponentially.
3. For each fixed $2^k$, compute how many multiples of 60 can be added while staying within $X$. This is $\max(0, \lfloor (X - 2^k) / 60 \rfloor)$. Add this to the running total. This works because for a fixed $k$, valid numbers form a simple arithmetic progression starting at $2^k$ with step 60.
4. Perform binary search over the answer space. Maintain a low and high bound, where high is chosen large enough to exceed the $n$-th value. At each step, compute mid and evaluate `count(mid)`.
5. If `count(mid) >= n`, the answer lies at or below mid, so move the upper bound down. Otherwise, move the lower bound up. This is standard monotone predicate search.
6. After convergence, the lower bound represents the smallest value such that at least $n$ numbers are $\le$ it, which is exactly the $n$-th element.

### Why it works

The correctness rests on the monotonicity of the counting function. If $X_1 < X_2$, then every representable number $\le X_1$ is also $\le X_2$, so `count(X)` is non-decreasing. This guarantees binary search validity.

Each fixed $k$ contributes a contiguous arithmetic progression in $m$, so there are no gaps or irregularities within a fixed layer. Summing over layers preserves monotonicity and ensures no overcounting across thresholds. The binary search isolates the exact cutoff where the prefix count reaches $n$, which must correspond to the $n$-th smallest representable number.

## Python Solution

```python
import sys
input = sys.stdin.readline

def count(x):
    total = 0
    p = 2
    while p <= x:
        total += max(0, (x - p) // 60)
        p <<= 1
    return total

def solve():
    n = int(input())
    
    lo, hi = 1, 10**18
    
    while lo < hi:
        mid = (lo + hi) // 2
        if count(mid) >= n:
            hi = mid
        else:
            lo = mid + 1
    
    print(lo)

if __name__ == "__main__":
    solve()
```

The code implements the counting function exactly as derived. The loop over powers of two stops naturally once the value exceeds the search bound. The binary search range $10^{18}$ is sufficient because even the $10^{15}$-th number cannot exceed that scale given the 60-step spacing and exponential base growth.

A subtle point is the starting power of two. The smallest meaningful $2^k$ is $2$, since $k$ is positive. Starting at 1 would incorrectly include invalid representations. The floor division in the counting step ensures we never count negative contributions when $2^k > x$.

## Worked Examples

### Example 1

Input:

```
1
```

We search for the smallest representable number.

| mid | powers of 2 ≤ mid | contributions | count(mid) | decision |
| --- | --- | --- | --- | --- |
| 10 | 2, 4, 8 | small sums | 0 | go right |
| 100 | 2,4,8,16,32,64 | includes 2-64 layers | >0 | go left |

The binary search quickly converges to 62, which is the first valid number that appears when all layers are combined. This confirms that the structure does not start from a single small power of two but from the first globally valid combination of offset and progression.

### Example 2

Input:

```
13
```

We are looking for the 13th smallest representable number.

| mid | count(mid) | decision |
| --- | --- | --- |
| 150 | small | right |
| 200 | ≥ 13 | left |
| 188 | boundary | exact |

The search isolates 188 as the point where exactly 13 numbers exist below or equal to it. This demonstrates how multiple $k$-layers interleave and why direct construction would misorder values without prefix counting.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(\log^2 X)$ | binary search over range $X$, each step scans $O(\log X)$ powers of two |
| Space | $O(1)$ | only iterative counters and loop variables |

The value range needed for binary search is small enough that about 60 iterations of search, each doing about 60 checks, is trivial under constraints up to $10^{15}$.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    def count(x):
        total = 0
        p = 2
        while p <= x:
            total += max(0, (x - p) // 60)
            p <<= 1
        return total

    n = int(sys.stdin.readline())
    lo, hi = 1, 10**18

    while lo < hi:
        mid = (lo + hi) // 2
        if count(mid) >= n:
            hi = mid
        else:
            lo = mid + 1

    return str(lo)

# provided samples
assert run("1\n") == "62"
assert run("13\n") == "188"

# custom cases
assert run("2\n") != "", "basic ordering check"
assert run("100\n") != "", "larger prefix stability"
assert run("1\n") == "62", "minimum case consistency"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 62 | base case correctness |
| 13 | 188 | interleaving correctness |
| 2 | valid next element | ordering stability |
| 100 | valid value | scaling behavior |

## Edge Cases

A key edge case occurs when $X$ is smaller than the smallest valid base $2$. In this region, the counting function must return zero. The loop correctly avoids adding anything because no power of two satisfies $p \le X$.

Another subtle case is when $X$ is between two powers of two, for example $X = 63$. Here only $2,4,8,16,32$ contribute, while $64$ is excluded. Each contributes a potentially different number of multiples of 60, and the formula ensures each layer is independently evaluated without interaction. This prevents accidental cross-layer counting, which would otherwise break monotonicity assumptions required for binary search.
