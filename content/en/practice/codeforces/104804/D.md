---
title: "CF 104804D - \u0420\u044b\u0446\u0430\u0440\u0438"
description: "We are given a bag containing a finite multiset of tokens. Among these tokens, some are special “knight” tokens and the rest are ordinary. From this bag, a player draws a fixed number of tokens uniformly at random without replacement."
date: "2026-06-28T16:51:27+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104804
codeforces_index: "D"
codeforces_contest_name: "Central Russia Regional Contest, 2022, Qualification Contest"
rating: 0
weight: 104804
solve_time_s: 69
verified: true
draft: false
---

[CF 104804D - \u0420\u044b\u0446\u0430\u0440\u0438](https://codeforces.com/problemset/problem/104804/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 9s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a bag containing a finite multiset of tokens. Among these tokens, some are special “knight” tokens and the rest are ordinary. From this bag, a player draws a fixed number of tokens uniformly at random without replacement.

The task is to compute the probability that at least one of the drawn tokens is a knight.

In more concrete terms, we are sampling a subset of size $m$ from a universe of size $n$, where exactly $k$ elements are marked as successful (knights). Every subset of size $m$ is equally likely. We want the probability that the chosen subset intersects the set of knights.

The constraints are very small: $n \le 20$ and $m \le 20$. This immediately signals that combinatorial enumeration or direct computation using binomial coefficients is fully sufficient. There is no need for approximation, simulation, or asymptotically optimized combinatorics.

A subtle edge case appears when $m \ge n$. In that situation, every token is drawn, so the probability becomes either 1 if $k > 0$, or 0 if $k = 0$. Another corner case is $k = 0$, where no knights exist, making the probability trivially 0 regardless of $m$. On the other extreme, if $k \ge 1$ and $m = n$, the answer is exactly 1.

A naive Monte Carlo simulation would converge too slowly and introduce precision issues. Another common mistake is to assume independence of draws, which is incorrect because sampling is without replacement.

## Approaches

The brute-force approach is to enumerate all subsets of size $m$ from $n$ elements, check whether each subset contains at least one knight, and count how many are valid. The total number of subsets is $\binom{n}{m}$, which in the worst case is maximized near $n = 20, m = 10$, giving $\binom{20}{10} = 184,756$. This is small enough to brute force directly, so correctness is immediate.

However, brute force hides the real structure of the problem. The key observation is that we do not need to consider individual arrangements, only counts of how many knights are included in the draw. Instead of counting favorable subsets directly, it is simpler to compute the complement event: drawing zero knights. That event corresponds to choosing all $m$ tokens from the $n-k$ non-knight tokens. This reduces the problem to a single combinatorial ratio.

The probability becomes:

$$P(\text{at least one knight}) = 1 - \frac{\binom{n-k}{m}}{\binom{n}{m}}$$

with the convention that $\binom{a}{b} = 0$ when $b > a$.

This transformation avoids enumerating subsets entirely and replaces the problem with evaluating a few binomial coefficients.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Enumeration | $O(\binom{n}{m} \cdot m)$ | $O(m)$ | Accepted but unnecessary |
| Complement + Combinatorics | $O(1)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

### Step-by-step computation

1. Read integers $n$, $k$, and $m$. These define the total pool, the number of successes, and the sample size respectively.
2. Handle trivial cases first. If $k = 0$, return 0 immediately since no success elements exist. If $m \ge n$, return 1 if $k > 0$, otherwise 0. This avoids invalid combinatorial expressions later.
3. Compute the number of non-knight tokens, which is $n - k$. This represents the “safe-only” pool.
4. Compute the probability of drawing only non-knights, which is:

$$\frac{\binom{n-k}{m}}{\binom{n}{m}}$$

This ratio reflects selecting all $m$ items exclusively from non-knights.
5. Subtract this value from 1 to obtain the probability that at least one knight is present.
6. Print the result with sufficient precision, typically at least 8 decimal places to satisfy the 1e-4 accuracy requirement.

### Why it works

The algorithm partitions all possible $m$-sized subsets into two disjoint categories: those containing at least one knight and those containing none. These two events cover the entire sample space without overlap. The complement event “no knights chosen” is easier to count because it restricts selection entirely to a reduced subset of size $n-k$. Since all subsets of size $m$ are equally likely, the probability is exactly the ratio of favorable subset counts, ensuring correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

from math import comb

def solve():
    n, k, m = map(int, input().split())

    if k == 0:
        print("0.0")
        return

    if m >= n:
        print("1.0")
        return

    total = comb(n, m)
    if n - k < m:
        no_knight = 0
    else:
        no_knight = comb(n - k, m)

    ans = 1.0 - no_knight / total
    print(f"{ans:.10f}")

if __name__ == "__main__":
    solve()
```

The implementation relies directly on Python’s built-in combinatorial function, which is stable and exact for these constraints. The early exits handle degenerate cases where binomial coefficients would otherwise be zero or undefined in a naive sense.

The only subtlety is ensuring correct handling of the case $n-k < m$, where it is impossible to choose $m$ non-knights, making the “no knight” probability zero.

## Worked Examples

### Example 1

Input:

```
5 2 2
```

We compute:

$n = 5$, $k = 2$, so non-knights = 3, and $m = 2$.

| Step | total C(5,2) | no-knight C(3,2) | probability no-knight | final answer |
| --- | --- | --- | --- | --- |
| compute | 10 | 3 | 3/10 | 1 - 0.3 |

Final result is $0.7$.

This confirms the complement logic: the only failure cases are choosing both items from the 3 non-knights.

### Example 2

Input:

```
8 2 4
```

Here $n = 8$, $k = 2$, so non-knights = 6, $m = 4$.

| Step | total C(8,4) | no-knight C(6,4) | probability no-knight | final answer |
| --- | --- | --- | --- | --- |
| compute | 70 | 15 | 15/70 | 1 - 0.2142857 |

Final result is approximately $0.78571429$.

This example shows that even when the sample size is large, the complement remains straightforward to compute.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(1)$ | Constant-time binomial coefficient evaluation for small n |
| Space | $O(1)$ | Only a few integer variables are stored |

The constraints are extremely small, so even repeated combinatorial calculations are trivial. The solution comfortably runs within limits and avoids any probabilistic or iterative computation.

## Test Cases

```python
import sys, io
from math import comb

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, k, m = map(int, input().split())

    if k == 0:
        return "0.0000000000"
    if m >= n:
        return "1.0000000000"

    total = comb(n, m)
    no_knight = comb(n - k, m) if n - k >= m else 0
    ans = 1.0 - no_knight / total
    return f"{ans:.10f}"

# provided samples
assert abs(float(run("5 2 2")) - 0.7) < 1e-9
assert abs(float(run("8 2 4")) - 0.78571429) < 1e-6

# custom cases
assert run("5 0 3") == "0.0000000000"
assert run("5 5 2") == "1.0000000000"
assert run("5 1 5") == "1.0000000000"
assert run("6 3 1") == "0.5000000000"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 5 0 3 | 0.0 | No knights exist |
| 5 5 2 | 1.0 | All tokens are knights |
| 5 1 5 | 1.0 | Full draw guarantees success |
| 6 3 1 | 0.5 | Single draw probability case |

## Edge Cases

One important edge case is when there are no knights. For input `5 0 3`, the algorithm immediately returns 0 before any combinatorics. Any formula-based implementation that forgets this may still compute a ratio but risk division artifacts or unnecessary computation.

Another case is when the draw size equals the bag size, such as `5 2 5`. The complement probability becomes zero because there is no way to avoid selecting knights if at least one exists. The algorithm correctly triggers the `m >= n` branch and returns 1.

A third case occurs when there are too few non-knights to satisfy the draw size. For example, `6 4 4` leaves only 2 non-knights. The computation `comb(2,4)` is treated as zero, correctly implying that every valid draw must include a knight, yielding probability 1.
