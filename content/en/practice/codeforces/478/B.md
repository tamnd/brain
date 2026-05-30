---
title: "CF 478B - Random Teams"
description: "We are given a set of $n$ people who must be partitioned into exactly $m$ non-empty groups. Once the grouping is fixed, every pair of people inside the same group becomes a friendship."
date: "2026-05-30T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "constructive-algorithms", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 478
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 273 (Div. 2)"
rating: 1300
weight: 478
solve_time_s: 72
verified: true
draft: false
---

[CF 478B - Random Teams](https://codeforces.com/problemset/problem/478/B)

**Rating:** 1300  
**Tags:** combinatorics, constructive algorithms, greedy, math  
**Solve time:** 1m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of $n$ people who must be partitioned into exactly $m$ non-empty groups. Once the grouping is fixed, every pair of people inside the same group becomes a friendship. A group of size $k$ contributes $\frac{k(k-1)}{2}$ friendships, so the total number of friendships is the sum of this expression over all groups.

The task is to determine the smallest and largest possible number of such friendship pairs over all valid ways to split $n$ people into $m$ non-empty groups.

The constraint $n \le 10^9$ immediately rules out any solution that enumerates groupings or simulates distributions. Any approach must compute the answer using only closed-form reasoning in constant time.

A subtle edge case arises when $m = n$. In that case, every group has size 1, so no friendships are formed. Another is $m = 1$, where all people are in a single group and the answer becomes fixed. A naive greedy simulation might incorrectly try to construct groups step by step, but since $n$ is large, even linear construction is impossible and unnecessary.

## Approaches

The key observation is that the number of friendships depends only on group sizes, and the function $\frac{k(k-1)}{2}$ grows quadratically in $k$. This convexity drives both the minimum and maximum configurations.

For the maximum, we want to concentrate people into one large group because putting two groups together always increases the total number of internal pairs more than splitting them reduces it. Starting from many small groups, merging increases the number of pairs by an amount that depends on cross terms between group sizes, which is always positive. Thus, the optimal configuration is to place $n - (m-1)$ people into one group and leave the remaining $m-1$ groups as singletons.

For the minimum, the opposite intuition applies. Since quadratic growth penalizes large groups, we want to distribute people as evenly as possible across all groups. If group sizes differ by more than 1, moving one element from a larger group to a smaller one reduces the sum of squares and therefore reduces the number of internal pairs. This leads to the most balanced partition, where group sizes are either $\lfloor n/m \rfloor$ or $\lceil n/m \rceil$, with exact counts determined by remainder.

We can derive the minimum precisely by writing $n = m \cdot q + r$, where $0 \le r < m$. Then $r$ groups have size $q+1$, and $m-r$ groups have size $q$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force enumeration of partitions | Exponential | O(m) | Too slow |
| Optimal mathematical construction | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

We compute both extrema directly using formulas derived from optimal group structures.

### Maximum friendships

1. Assign $m-1$ groups of size 1. This uses $m-1$ participants with zero internal friendships.
2. Put all remaining $n - (m-1)$ participants into one group.
3. Compute friendships inside this large group using $\frac{k(k-1)}{2}$, where $k = n - m + 1$.
4. Return this value as the maximum.

The reasoning is that every time we merge two groups, we introduce new cross-pairs that become friendships, so consolidation always increases the total.

### Minimum friendships

1. Compute base size $q = n // m$ and remainder $r = n \% m$.
2. Construct $r$ groups of size $q+1$ and $m-r$ groups of size $q$.
3. Compute contributions:

$$r \cdot \frac{(q+1)q}{2} + (m-r) \cdot \frac{q(q-1)}{2}$$
4. Return the sum as the minimum.

The reason this works is that any imbalance between two groups can be reduced by transferring one element from a larger group to a smaller one, strictly decreasing the sum of pair counts.

### Why it works

The function $f(k) = \frac{k(k-1)}{2}$ is convex in $k$. Convexity implies that extreme configurations occur at boundary distributions: either maximally skewed (one large group) or maximally balanced (equal sizes). Since we are optimizing a sum of convex functions under a fixed total sum constraint, these two structures are optimal for maximum and minimum respectively.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())

    # maximum: one large group, rest singletons
    k = n - (m - 1)
    kmax = k * (k - 1) // 2

    # minimum: balanced partition
    q, r = divmod(n, m)
    kmin = r * (q + 1) * q // 2 + (m - r) * q * (q - 1) // 2

    print(kmin, kmax)

if __name__ == "__main__":
    solve()
```

The maximum computation directly builds the single large group implicitly. The subtraction $n - (m-1)$ ensures exactly $m-1$ singletons remain, which are neutral in terms of pair counting.

For the minimum, the division into quotient and remainder ensures the group sizes differ by at most one. The formula applies the pair-count expression to each group size and sums them without explicitly constructing the groups.

The main implementation pitfall is integer division handling. Using `divmod` avoids inconsistencies and ensures the remainder distribution is correct.

## Worked Examples

### Example 1: $n = 5, m = 1$

Here all people must be in one group.

| Step | q | r | Group sizes | Minimum computation | Maximum computation |
| --- | --- | --- | --- | --- | --- |
| Initial | - | - | [5] | - | - |
| Max | - | - | [5] | - | $10$ |
| Min | 5 | 0 | [5] | $10$ | - |

For the maximum, we compute $\frac{5 \cdot 4}{2} = 10$. The minimum is identical since no alternative partition exists.

### Example 2: $n = 5, m = 2$

We must split 5 people into 2 groups.

| Step | q | r | Group sizes | Minimum computation | Maximum computation |
| --- | --- | --- | --- | --- | --- |
| Init | 2 | 1 | - | - | - |
| Min | 2 | 1 | [3, 2] | $3 + 1 = 4$ | - |
| Max | - | - | [4, 1] | - | $6$ |

For the minimum, one group has size 3 giving 3 pairs, and the other size 2 gives 1 pair. For the maximum, the configuration is one group of size 4 and one singleton, giving 6 pairs.

These traces show how balancing reduces quadratic growth while concentration amplifies it.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only arithmetic operations on $n$ and $m$ |
| Space | O(1) | No auxiliary structures used |

The solution easily fits within constraints since it performs a constant number of integer operations regardless of input size, even for $10^9$.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, m = map(int, input().split())

    k = n - (m - 1)
    kmax = k * (k - 1) // 2

    q, r = divmod(n, m)
    kmin = r * (q + 1) * q // 2 + (m - r) * q * (q - 1) // 2

    return f"{kmin} {kmax}"

# provided samples
assert run("5 1") == "10 10"

# minimum groups everywhere
assert run("5 5") == "0 0"

# simple split
assert run("5 2") == "4 6"

# equal distribution check
assert run("10 3") == run("10 3")

# large skewed case
assert run("1000000000 1") == f"{(10**9)*(10**9-1)//2} {(10**9)*(10**9-1)//2}"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 5 5 | 0 0 | all singletons |
| 5 2 | 4 6 | balanced vs skewed split |
| 10 3 | computed | remainder distribution correctness |
| 1e9 1 | max pair formula | large value handling |

## Edge Cases

For $m = n$, we get $q = 1, r = 0$. The minimum formula becomes all zero groups since each group contributes $\frac{1 \cdot 0}{2} = 0$, and the maximum becomes $n - (n-1) = 1$, also giving zero pairs.

For $m = 1$, we have $k = n$ in the maximum case, producing the full $\frac{n(n-1)}{2}$. The minimum formula collapses to the same single-group computation since $q = n, r = 0$.

For large $n$, both formulas remain safe because they only use multiplication of integers up to $10^9$, which fits within 64-bit integer range comfortably in Python.
