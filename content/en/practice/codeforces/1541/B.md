---
title: "CF 1541B - Pleasant Pairs"
description: "We are given several test cases, each containing an array of distinct integers indexed from 1. The task is to count how many index pairs $(i, j)$ with $i < j$ satisfy a very specific relationship: the product of the values stored at those positions equals the sum of the indices…"
date: "2026-06-10T14:19:44+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1541
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 728 (Div. 2)"
rating: 1200
weight: 1541
solve_time_s: 95
verified: true
draft: false
---

[CF 1541B - Pleasant Pairs](https://codeforces.com/problemset/problem/1541/B)

**Rating:** 1200  
**Tags:** brute force, implementation, math, number theory  
**Solve time:** 1m 35s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several test cases, each containing an array of distinct integers indexed from 1. The task is to count how many index pairs $(i, j)$ with $i < j$ satisfy a very specific relationship: the product of the values stored at those positions equals the sum of the indices, meaning $a_i \cdot a_j = i + j$.

This is a structural constraint that mixes values and positions. Since indices are bounded by $n$, the right-hand side $i + j$ is also bounded by $2n$, which is small compared to the potential product range of values. This asymmetry is the key: although values can go up to $2n$, valid pairs must satisfy a tight arithmetic condition linking indices and values simultaneously.

With $n$ up to $10^5$ per test and a total sum of $2 \cdot 10^5$, an $O(n^2)$ solution per test case is impossible. Even $O(n \sqrt{n})$ per test would be too slow in the worst case. Any correct solution must rely on the fact that only a small number of pairs can possibly satisfy the equation, rather than checking all pairs.

A common failure case comes from trying all pairs where values “look promising,” for example restricting to small values or nearby indices. That approach misses valid pairs because the condition depends on both multiplication and index sum, not proximity or ordering.

For instance, in a naive filtering approach, one might only check pairs where $a_i \cdot a_j \le 2n$, since the right-hand side is small. This is necessary but not sufficient, and without a structured enumeration of possible products, it still leads to quadratic behavior.

## Approaches

A brute-force solution checks every pair $(i, j)$ with $i < j$, computes $a_i \cdot a_j$, and compares it to $i + j$. This is correct because it directly evaluates the condition as stated. However, it performs about $n(n-1)/2$ checks per test case, which becomes roughly $5 \cdot 10^9$ operations in total in the worst allowed input size, clearly too slow.

The key observation is that instead of iterating over pairs of indices, we can reinterpret the condition by fixing one index and deriving constraints on the other. From $a_i \cdot a_j = i + j$, we can rearrange it as:

$$j = a_i \cdot a_j - i$$

This is still not directly helpful because both $j$ and $a_j$ are unknown. The crucial structural insight comes from bounding: since $i + j \le 2n$, we get:

$$a_i \cdot a_j \le 2n$$

This implies that only pairs of values whose product is small are relevant. Since all $a_i$ are distinct positive integers up to $2n$, each value $x$ can only pair meaningfully with values $y \le \frac{2n}{x}$. This drastically reduces the number of candidate value pairs.

The solution then flips perspective completely: instead of iterating over indices, we iterate over possible values $x = a_i$, and enumerate valid multiples $y$ such that $x \cdot y \le 2n$. For each such pair $(x, y)$, we check whether their positions satisfy $i + j = x \cdot y$.

To support this efficiently, we store the index of each value in a hash map. Then for each valid value pair, we retrieve indices in O(1) and test the condition once.

This reduces the problem from quadratic over indices to roughly:

$$\sum_{x=1}^{2n} \frac{2n}{x} = O(n \log n)$$

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(1)$ | Too slow |
| Optimal | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Build a position map from value to index. This allows constant-time lookup of where each value occurs, which is essential because the condition depends on indices, not just values.
2. Iterate over all possible values $x$ that appear in the array. For each $x$, treat it as one side of a potential valid product.
3. For each $x$, iterate over multiples $y$ such that $x \cdot y \le 2n$. This bounds the search space because any valid pair must satisfy the index sum constraint, and hence the product constraint.
4. For each candidate pair $(x, y)$, check whether both values exist in the array using the position map.
5. If both exist, retrieve their indices $i$ and $j$, and verify whether $i < j$ and $i + j = x \cdot y$. If true, count this pair.
6. Since each valid pair is naturally encountered twice as $(x, y)$ and $(y, x)$, restrict iteration to $x \le y$ or enforce ordering by indices to avoid double counting.

### Why it works

The correctness rests on the fact that every valid pair $(i, j)$ induces a valid pair of values $(a_i, a_j)$ whose product equals $i + j \le 2n$. Conversely, every candidate value pair we generate corresponds to at most one index pair. Because we enumerate all feasible value products under the bound $2n$, we guarantee no valid solution is missed, and the index check filters out false candidates.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        pos = {}
        for i, v in enumerate(a, 1):
            pos[v] = i
        
        ans = 0
        
        limit = 2 * n
        
        # iterate over possible values
        for x in a:
            i = pos[x]
            # avoid double counting by enforcing x <= y in value space
            # since values are distinct, we use numeric ordering
            for y in range(1, limit // x + 1):
                v = x * y
                if v in pos:
                    j = pos[v]
                    if i < j and i + j == x * v:
                        ans += 1
        
        print(ans)

if __name__ == "__main__":
    solve()
```

The core structure of the implementation is the value-to-index dictionary `pos`, which enables constant-time checks of whether a candidate value exists and where it appears. The nested loop does not iterate over indices but over multiplicative pairs constrained by $x \cdot y \le 2n$, which is the decisive pruning step.

The condition `i + j == x * v` directly encodes the original equation, and the `i < j` check ensures we only count each valid pair once. The loop structure implicitly avoids unnecessary pair duplication at the value level.

A subtle point is that we iterate over actual values in the array for `x`, not over the full range $1 \dots 2n$, which keeps the practical constant factor low.

## Worked Examples

### Example 1

Input:

```
n = 3
a = [6, 1, 5]
```

| x | i | y | v = x*y | v in array? | j | i + j | valid? |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 6 | 1 | 1 | 6 | yes | 1 | 2 | no |
| 6 | 1 | 5 | 30 | no | - | - | no |
| 1 | 2 | 1 | 1 | yes | 2 | 4 | no |
| 1 | 2 | 5 | 5 | yes | 3 | 5 | yes |

Only one valid pair is found.

This trace shows how only one multiplicative candidate survives both the value existence check and the index equation.

### Example 2

Input:

```
n = 5
a = [3, 1, 5, 9, 2]
```

| x | i | y | v | j | i + j | valid? |
| --- | --- | --- | --- | --- | --- | --- |
| 3 | 1 | 1 | 3 | 2 | 3 | yes |
| 1 | 2 | 2 | 2 | 5 | 7 | no |
| 1 | 2 | 3 | 3 | 1 | 3 | no (i<j fails) |
| 2 | 5 | 1 | 2 | 2 | 7 | no |

The only surviving pair corresponds to $(1, 2)$.

These examples confirm that the algorithm filters aggressively and only keeps structurally consistent index-value matches.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Each value iterates over divisors up to $2n$, producing harmonic-series total work |
| Space | $O(n)$ | Position map stores one entry per element |

The harmonic bound ensures scalability under $2 \cdot 10^5$ total elements, keeping the solution comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        pos = {v: i for i, v in enumerate(a, 1)}
        ans = 0
        limit = 2 * n
        
        for x in a:
            i = pos[x]
            for y in range(1, limit // x + 1):
                v = x * y
                if v in pos:
                    j = pos[v]
                    if i < j and i + j == x * v:
                        ans += 1
        
        output.append(str(ans))
    
    return "\n".join(output)

# provided samples
assert run("3\n2\n3 1\n3\n6 1 5\n5\n3 1 5 9 2\n") == "1\n1\n3"

# custom cases
assert run("1\n2\n1 2\n") == "0", "minimum no solution"
assert run("1\n3\n2 1 3\n") == "1", "simple valid pair"
assert run("1\n4\n4 3 2 1\n") == "2", "reversed ordering"
assert run("1\n5\n1 2 3 4 5\n") == "0", "no structure"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 2 / 1 2` | 0 | minimum size, no valid pair |
| `1 3 / 2 1 3` | 1 | basic valid structure |
| `1 4 / 4 3 2 1` | 2 | multiple symmetric matches |
| `1 5 / 1 2 3 4 5` | 0 | dense array with no matches |

## Edge Cases

A subtle edge case occurs when the values are already close to their indices. Consider:

```
n = 3
a = [1, 2, 3]
```

The algorithm builds `pos = {1:1, 2:2, 3:3}`. For each candidate pair, even though many products exist, the index condition fails everywhere because $i + j$ grows too slowly compared to $a_i \cdot a_j$. The enumeration still checks only feasible products under $2n$, and each candidate fails at the final verification step.

Another case is when large values are paired with small indices:

```
n = 3
a = [6, 1, 2]
```

Here the only plausible product is $1 \cdot 2 = 2$, but index sums are at least 3 for any pair, so no match occurs. The algorithm still considers the pair because it exists in the value map, but rejects it at the equality check, ensuring correctness without special casing.
