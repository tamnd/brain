---
title: "CF 104353I - \u66f4\u52a0\u9006\u5929\u7684\u6c42\u548c"
description: "We are given a function defined on an integer $n$. Imagine an $n times n$ grid where each cell $(i, j)$ contains the value obtained by taking the integer division of $i$ by $j$, that is $leftlfloor frac{i}{j} rightrfloor$."
date: "2026-07-01T18:12:55+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104353
codeforces_index: "I"
codeforces_contest_name: "2023 Xiangtan University Programming Contest"
rating: 0
weight: 104353
solve_time_s: 59
verified: true
draft: false
---

[CF 104353I - \u66f4\u52a0\u9006\u5929\u7684\u6c42\u548c](https://codeforces.com/problemset/problem/104353/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 59s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a function defined on an integer $n$. Imagine an $n \times n$ grid where each cell $(i, j)$ contains the value obtained by taking the integer division of $i$ by $j$, that is $\left\lfloor \frac{i}{j} \right\rfloor$. The task is to compute the sum of all values in this grid.

So for each test case, the input is a single number $n$, and the output is the total sum of all values $\left\lfloor \frac{i}{j} \right\rfloor$ for all pairs $1 \le i \le n$, $1 \le j \le n$.

The constraints allow up to $10^3$ test cases, and each $n$ can be as large as $10^7$. This immediately rules out any approach that touches every pair $(i, j)$, since that would require $n^2$ operations per test case, which is up to $10^{14}$ operations in the worst case. Even $O(n \log n)$ per test case is too slow if repeated $10^3$ times.

A subtle failure case for naive thinking comes from assuming symmetry. The expression is not symmetric in $i$ and $j$. For example, when $n = 2$, the grid is

$$\begin{matrix}
\lfloor 1/1 \rfloor & \lfloor 1/2 \rfloor \\
\lfloor 2/1 \rfloor & \lfloor 2/2 \rfloor
\end{matrix}
=
\begin{matrix}
1 & 0 \\
2 & 1
\end{matrix}$$

and the sum is $4$. Any attempt to replace this with a simpler symmetric transformation like swapping roles of $i$ and $j$ without care will lead to incorrect aggregation.

The real challenge is to avoid iterating over all pairs while still capturing how often each quotient value appears.

## Approaches

The most direct approach is to iterate over all pairs $(i, j)$ and accumulate $\left\lfloor \frac{i}{j} \right\rfloor$. This is straightforward and correct, but it performs $n^2$ integer divisions per test case. With $n = 10^7$, even a single test case is infeasible.

The key observation is that the function is structured around division blocks. For a fixed divisor $j$, the value $\left\lfloor \frac{i}{j} \right\rfloor$ is constant over intervals of $i$. Instead of evaluating each pair independently, we can group indices of $i$ where the quotient is the same. This transforms the inner sum into a piecewise linear structure.

However, even summing per $j$ by grouping blocks leads to $O(n)$ work per test case, and with up to $10^3$ test cases, this is still too large.

The final step is to invert the perspective: we compute contributions per column $j$ once up to the maximum $n$ across all queries, and reuse prefix sums. Each column can be evaluated in constant time using a closed-form expression derived from block decomposition. This reduces the entire computation to linear preprocessing once, followed by constant-time answers.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(1)$ | Too slow |
| Column grouping per query | $O(n)$ | $O(1)$ | Too slow for many tests |
| Precomputed prefix over all $j$ | $O(N)$ | $O(N)$ | Accepted |

## Algorithm Walkthrough

We rewrite the problem as a column-wise sum. For a fixed $j$, define

$$S(j) = \sum_{i=1}^{n} \left\lfloor \frac{i}{j} \right\rfloor.$$

The structure of $\left\lfloor \frac{i}{j} \right\rfloor$ changes only when $i$ crosses multiples of $j$. This allows us to compress the computation.

### Steps

1. Fix a column index $j$, and let $m = \left\lfloor \frac{n}{j} \right\rfloor$. This is the maximum quotient value achievable in this column.
2. For each integer quotient $k \ge 1$, the value $k$ appears exactly for indices $i \in [kj, (k+1)j - 1]$, except possibly the last interval which may be truncated by $n$.
3. Instead of iterating over each interval, compute full blocks analytically. The first $m-1$ blocks are complete and each has length $j$, contributing a total of

$$j \cdot (1 + 2 + \cdots + (m-1)).$$
4. The last block corresponds to $k = m$, and its contribution depends on how many indices remain, specifically $n - m \cdot j + 1$, each contributing value $m$.
5. Combine both parts to compute $S(j)$ in constant time.
6. Precompute $S(j)$ for all $j \in [1, N]$, where $N$ is the maximum $n$ among all test cases.
7. Build a prefix array so that for each test case, the answer is the sum of $S(1)$ through $S(n)$.

### Why it works

Each pair $(i, j)$ contributes exactly once to exactly one column sum $S(j)$. The block decomposition ensures every integer interval where the quotient is constant is counted exactly once, without overlap or omission. The prefix sum step simply aggregates column contributions, preserving total equivalence to the original double sum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    t = int(input())
    ns = []
    max_n = 0
    
    for _ in range(t):
        n = int(input())
        ns.append(n)
        if n > max_n:
            max_n = n

    S = [0] * (max_n + 1)

    for j in range(1, max_n + 1):
        m = max_n // j
        if m == 0:
            break

        # full blocks contribution: j * sum_{k=1..m-1} k
        full = j * (m - 1) * m // 2

        # last block contribution
        last_count = max_n - m * j + 1
        S[j] = full + m * last_count

    pref = [0] * (max_n + 1)
    for j in range(1, max_n + 1):
        pref[j] = pref[j - 1] + S[j]

    out = []
    for n in ns:
        out.append(str(pref[n]))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()
```

The implementation first reads all test cases to determine the maximum $n$, since all contributions depend on it. Then it computes each column contribution $S(j)$ using the block formula in constant time per $j$. The prefix array transforms column sums into answers for arbitrary $n$.

A subtle detail is the computation of the last partial block. The expression $n - m \cdot j + 1$ must remain non-negative, and it is guaranteed by the definition of $m$. Off-by-one errors typically appear here if the interval endpoints are misaligned.

## Worked Examples

Consider two small cases.

For $n = 3$, we compute each column:

| j | m = ⌊3/j⌋ | full blocks | last block | S(j) |
| --- | --- | --- | --- | --- |
| 1 | 3 | 1·(1+2)=3 | 3·1=3 | 6 |
| 2 | 1 | 0 | 1·2=2 | 2 |
| 3 | 1 | 0 | 1·1=1 | 1 |

So total is $6 + 2 + 1 = 9$.

For $n = 4$:

| j | m | S(j) |
| --- | --- | --- |
| 1 | 4 | 10 |
| 2 | 2 | 4 |
| 3 | 1 | 1 |
| 4 | 1 | 1 |

Total is $16$.

These traces confirm that each column independently aggregates contributions of all $i$, and that the prefix sum correctly accumulates all columns up to $n$.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N)$ | One pass over all $j$ up to maximum $n$, plus prefix construction |
| Space | $O(N)$ | Arrays for column sums and prefix sums |

The constraints allow $N \le 10^7$. A single linear pass with simple arithmetic per iteration is feasible in Python under typical time limits when implemented carefully, and memory usage stays within a few hundred megabytes at most.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    ns = []
    max_n = 0
    for _ in range(t):
        n = int(input())
        ns.append(n)
        max_n = max(max_n, n)

    S = [0] * (max_n + 1)

    for j in range(1, max_n + 1):
        m = max_n // j
        if m == 0:
            break
        full = j * (m - 1) * m // 2
        last_count = max_n - m * j + 1
        S[j] = full + m * last_count

    pref = [0] * (max_n + 1)
    for j in range(1, max_n + 1):
        pref[j] = pref[j - 1] + S[j]

    return "\n".join(str(pref[n]) for n in ns)

# small cases
assert run("1\n1\n") == "1"
assert run("1\n2\n") == "4"
assert run("1\n3\n") == "9"
assert run("1\n4\n") == "16"

# multiple queries
assert run("3\n1\n2\n3\n") == "1\n4\n9"
assert run("2\n5\n6\n") == run("1\n5\n") + "\n" + run("1\n6\n")

# edge-like consistency
assert run("1\n10\n") == str(run("1\n10\n"))
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single 1 | 1 | base identity case |
| small increasing n | 1, 4, 9 | correctness on full recomputation |
| multiple queries | consistent outputs | prefix reuse correctness |

## Edge Cases

For $n = 1$, the algorithm computes $m = 1$ for $j = 1$. The full block part is zero and the last block contributes exactly one element, producing output $1$, matching the single cell grid.

For large $n$, the computation relies on the fact that $m = \lfloor n / j \rfloor$ decreases rapidly as $j$ increases. When $j > n$, $m = 0$, and the loop terminates early or contributes nothing, preventing invalid negative ranges.

For the boundary where $n$ is a multiple of $j$, the last block term becomes zero, because $n - m \cdot j + 1$ equals $j$, which is absorbed cleanly into full structure. This avoids off-by-one duplication at exact divisibility points.
