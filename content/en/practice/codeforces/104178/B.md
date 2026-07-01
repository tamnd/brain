---
title: "CF 104178B - Moo"
description: "We are given a set of chickens, each with a positive weight. We also have a fixed number of biscuits. The goal is to distribute biscuits so that every chicken receives a nonnegative integer amount, and all chickens receive biscuits in strict proportion to their weights."
date: "2026-07-02T00:46:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104178
codeforces_index: "B"
codeforces_contest_name: "BdOI Preliminary 2023"
rating: 0
weight: 104178
solve_time_s: 46
verified: true
draft: false
---

[CF 104178B - Moo](https://codeforces.com/problemset/problem/104178/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of chickens, each with a positive weight. We also have a fixed number of biscuits. The goal is to distribute biscuits so that every chicken receives a nonnegative integer amount, and all chickens receive biscuits in strict proportion to their weights. This means there exists some common ratio such that the number of biscuits assigned to each chicken equals that ratio multiplied by its weight.

If we pick a ratio $k$, then chicken $i$ must receive $f[i] = k \cdot w[i]$. The total number of biscuits used is then $k \cdot (w_1 + w_2 + \dots + w_n)$. Since biscuits cannot be split, both $k$ and all $f[i]$ must be integers, which is already guaranteed if we choose integer $k$.

The task is to maximize the number of biscuits distributed while ensuring we do not exceed $m$, and the proportionality condition is preserved exactly.

The input size allows up to 200,000 weights, and the sum of weights can be large in value since each weight is up to $10^9$, while $m$ can be as large as $10^{15}$. This immediately rules out any approach that tries all candidate distributions or performs per-biscuit simulation. Any solution must reduce the problem to a few arithmetic operations over the entire array.

A subtle issue arises if we think of distributing independently per chicken. For example, greedily giving each chicken up to $m$ proportionally will fail because any deviation from a single global ratio breaks the constraint.

Edge cases are mostly structural:

If all weights are equal, the distribution must also be uniform, and the answer reduces to dividing $m$ equally among $n$ parts. For example, $n=3$, weights $1,1,1$, $m=10$ gives total $9$ because only multiples of $3$ are valid totals.

If weights have no common scaling compatibility with $m$, the answer can be zero. For example, $w=[1,5,2,3,1]$, $m=10$, sum is $12$, and the largest multiple of $12$ not exceeding $10$ is $0$.

## Approaches

The brute-force interpretation is to try every possible assignment of integer biscuits to each chicken and check whether ratios match. That immediately explodes: even if we restrict ourselves to valid proportional assignments, we would still need to test every possible scaling factor $k$, and for each, compute total biscuits and verify constraints. The number of candidate $k$ values is up to $m$, which is $10^{15}$, making this infeasible.

The key simplification comes from recognizing that the proportional condition forces all valid distributions into a single one-parameter family. Once weights are fixed, every valid solution is determined only by a scalar multiplier $k$. The total biscuits used is always $k \cdot S$, where $S$ is the sum of all weights.

So the problem reduces to finding the largest integer $k$ such that:

$$k \cdot S \le m$$

This is a direct integer division, and once $k$ is known, the total biscuits distributed is exactly $k \cdot S$.

No combinatorics, no gcd structure beyond recognizing the linearity, and no per-element optimization is needed.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over k or assignments | $O(m)$ or worse | $O(1)$ | Too slow |
| Sum + division | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Read all weights and compute their total sum $S$. This compresses all structure of the problem into a single scalar because proportional allocation collapses everything into a shared multiplier.
2. If $S = 0$, the distribution is trivially zero, but in this problem weights are strictly positive, so this case never occurs.
3. Compute the maximum valid scaling factor $k = \lfloor m / S \rfloor$. This ensures that total biscuits $k \cdot S$ does not exceed the available amount.
4. Output the total biscuits $k \cdot S$.

The reason this is sufficient is that any valid proportional distribution must scale all weights equally, and there is no freedom to redistribute surplus or partial values across elements.

### Why it works

All valid distributions lie on a one-dimensional line in $n$-dimensional space, defined by the vector of weights. Any valid solution must be an integer multiple of this vector. The constraint $\sum f[i] \le m$ restricts us to prefixes of this line, and the maximum feasible point is exactly the largest integer multiple that does not exceed $m$.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    w = list(map(int, input().split()))
    
    s = sum(w)
    print((m // s) * s)

if __name__ == "__main__":
    solve()
```

The solution works by collapsing the entire array into its sum. The division $m // s$ computes how many full proportional layers of biscuits we can distribute. Multiplying back by $s$ reconstructs the total number of biscuits used.

The only subtle point is using integer division; floating-point arithmetic would introduce precision risk given $10^{15}$ scale.

## Worked Examples

### Example 1

Input:

```
3 12
1 1 3
```

Here $S = 5$.

| Step | Sum S | m | k = m//S | Answer |
| --- | --- | --- | --- | --- |
| 1 | 5 | 12 | 2 | 10 |

So we can distribute 2 full proportional units: $2, 2, 6$.

This confirms that proportional scaling preserves exact ratios.

### Example 2

Input:

```
5 10
1 5 2 3 1
```

Here $S = 12$.

| Step | Sum S | m | k = m//S | Answer |
| --- | --- | --- | --- | --- |
| 1 | 12 | 10 | 0 | 0 |

Since even one full proportional unit exceeds the budget, no biscuits can be distributed.

This demonstrates the boundary case where the answer collapses to zero.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Single pass to compute sum of weights |
| Space | $O(1)$ | Only aggregate sum is stored |

The constraints allow up to 200,000 weights, and a single linear pass is easily within limits. The arithmetic operations are constant time.

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
    n, m = map(int, input().split())
    w = list(map(int, input().split()))
    s = sum(w)
    print((m // s) * s)

# provided samples
assert run("3 12\n1 1 3\n") == "10"
assert run("5 10\n1 5 2 3 1\n") == "0"
assert run("1 5\n7\n") == "5"

# custom cases
assert run("2 100\n1 1\n") == "100"
assert run("4 9\n2 2 2 2\n") == "8"
assert run("3 7\n2 2 2\n") == "6"
assert run("3 5\n2 2 2\n") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 100 / 1 1 | 100 | full divisibility scaling |
| 4 9 / 2 2 2 2 | 8 | uniform weights with remainder |
| 3 7 / 2 2 2 | 6 | floor scaling works |
| 3 5 / 2 2 2 | 0 | no feasible scaling |

## Edge Cases

If all weights are identical, the algorithm reduces to dividing $m$ by $n \cdot w$. For example, input:

```
3 10
2 2 2
```

gives $S=6$, $k=1$, result $6$. Even though $10$ is not divisible by $6$, we correctly avoid partial allocation.

If $m < S$, the algorithm immediately returns zero. For example:

```
4 3
1 1 1 1
```

Here $S=4$, so no valid proportional assignment exists under the budget.

If one weight is much larger than others, it does not change the structure because scaling applies globally. For instance:

```
3 100
1 1 50
```

We get $S=52$, $k=1$, result $52$, showing that imbalance does not introduce any per-element decision.
