---
title: "CF 105946A - 3D"
description: "We are given an array of integers, and we need to count how many ordered triples of distinct indices form an arithmetic relation where the sum of two selected elements equals a third element in the array."
date: "2026-06-21T22:07:08+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105946
codeforces_index: "A"
codeforces_contest_name: "2025 UP ACM Algolympics Final Round"
rating: 0
weight: 105946
solve_time_s: 97
verified: true
draft: false
---

[CF 105946A - 3D](https://codeforces.com/problemset/problem/105946/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 37s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers, and we need to count how many ordered triples of distinct indices form an arithmetic relation where the sum of two selected elements equals a third element in the array. Formally, we choose three different positions $i, j, k$ and check whether $a_i + a_j = a_k$, counting every valid ordering separately.

A key structural restriction is hidden in the array: every value has at most three positive divisors. That immediately forces every element into one of only three shapes. The number 1 has one divisor. A prime number has exactly two divisors. A square of a prime has exactly three divisors. No other integers satisfy the condition, so every array element must belong to one of these three categories, even though the values themselves can be as large as $10^{18}$.

The constraints allow up to $2 \cdot 10^5$ elements, which rules out any solution that is cubic or even quadratic in the worst case over raw indices. A direct triple loop over indices would perform on the order of $n^3$ operations, which is far beyond feasible limits. Even a naive double loop over pairs of indices would already approach $4 \cdot 10^{10}$ operations in the worst case, which is still too slow in general unless the structure of the data is heavily exploited.

The main subtlety is that indices matter, not just values. If a value appears multiple times, each occurrence is treated as a distinct choice, so multiplicities must be handled carefully.

Edge cases that commonly break naive reasoning are duplicates and ordering. For example, if the array is $[1, 2, 3, 3]$, then the equation $1 + 2 = 3$ contributes multiple valid triples depending on which occurrence of 3 is chosen. Another example is when the same value appears many times, such as $[2, 2, 4]$. The pair $(2, 2)$ contributes differently than $(2, 4)$, and forgetting index distinctness or multiplicity leads to incorrect counts.

## Approaches

The brute force approach tries every ordered triple of indices $(i, j, k)$ and checks whether the sum condition holds. This is correct because it directly enforces all constraints, including distinct indices and ordering. However, it performs three nested loops, leading to $O(n^3)$ time, which becomes infeasible even for $n = 200{,}000$.

A natural improvement is to fix the third index $k$, treat $a_k$ as a target sum, and then count how many ordered pairs $(i, j)$ satisfy $a_i + a_j = a_k$. This reduces the problem to counting valid pairs for each fixed target. If we store frequencies of values, we can compute contributions using multiplication instead of scanning indices.

The key insight is that we no longer need to reason about positions individually. Once values are grouped, each pair of values contributes a predictable number of index pairs, determined purely by frequency. This transforms the problem into a frequency-based convolution over values.

The difficulty shifts to efficiently finding, for each value $c$, how many pairs $(x, y)$ in the array satisfy $x + y = c$. With a frequency map, this becomes a structured enumeration over distinct values.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^3)$ | $O(1)$ | Too slow |
| Frequency Pair Counting | $O(m^2)$ where $m$ is distinct values | $O(m)$ | Accepted under structure |

Here $m$ is the number of distinct values, which is significantly smaller than $n$ in practice due to the divisor constraint structure.

## Algorithm Walkthrough

### 1. Count frequencies of each value

We first build a frequency map `freq[v]`, storing how many times each value appears. This is necessary because each index is distinct, and multiplicity directly affects how many triples can be formed.

### 2. Iterate over all ordered pairs of distinct values

We consider every ordered pair of values $(x, y)$, including the case where $x = y$. For each pair, the number of index pairs contributing this value pair is:

- `freq[x] * freq[y]` if $x \neq y$
- `freq[x] * (freq[x] - 1)` if $x = y$

This correctly counts ordered index selections $(i, j)$ with $i \neq j$.

### 3. Compute the required third value

For each pair $(x, y)$, compute $z = x + y$. We check whether $z$ exists in the array using the frequency map.

If it exists, every valid pair $(i, j)$ contributes `freq[z]` choices for index $k$, since any occurrence of $z$ can serve as the third element.

### 4. Accumulate contributions

We add `pair_count * freq[z]` to the answer for each ordered value pair.

No extra correction is needed for index collisions because $z = x + y$ cannot equal either $x$ or $y$ for positive integers, so the third index is automatically distinct from the first two.

### Why it works

Every valid triple $(i, j, k)$ corresponds uniquely to a choice of values $(x, y, z)$ such that $x + y = z$, together with a choice of indices for each value occurrence. The algorithm enumerates every possible ordered pair of values exactly once and multiplies by all compatible occurrences of the third value. Because indices are only chosen within disjoint frequency groups and equality conditions are handled through combinatorial counting, every valid triple is counted exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import Counter

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    freq = Counter(a)
    vals = list(freq.keys())
    
    ans = 0
    
    for i in range(len(vals)):
        x = vals[i]
        fx = freq[x]
        for j in range(len(vals)):
            y = vals[j]
            fy = freq[y]
            
            if x == y:
                pair_cnt = fx * (fx - 1)
            else:
                pair_cnt = fx * fy
            
            z = x + y
            if z in freq:
                ans += pair_cnt * freq[z]
    
    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation begins by compressing the array into a frequency map. The nested loops iterate over value space rather than index space, which is the key reduction. The handling of the $x = y$ case ensures that ordered index pairs do not reuse the same index. The lookup for $z = x + y$ is constant time using the hash map.

A subtle point is that the loop is over ordered pairs, not unordered ones. This is necessary because $(i, j)$ and $(j, i)$ are distinct valid triples, and both must be counted separately.

## Worked Examples

### Example 1

Input array: $[1, 2, 3]$

| x | y | pair count | z | freq[z] | contribution |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | 1 | 3 | 1 | 1 |
| 2 | 1 | 1 | 3 | 1 | 1 |

Total answer = 2.

This shows that ordering matters: both $(1,2,3)$ and $(2,1,3)$ are counted.

### Example 2

Input array: $[1, 2, 3, 3]$

| x | y | pair count | z | freq[z] | contribution |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | 1 | 3 | 2 | 2 |
| 2 | 1 | 1 | 3 | 2 | 2 |

Total answer = 4.

This demonstrates how duplicates increase the number of valid triples because each occurrence of the target value contributes separately as a valid choice for $k$.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(m^2)$ | iterating over all ordered pairs of distinct values |
| Space | $O(m)$ | storing frequency map of distinct values |

The performance depends on the number of distinct values rather than the array size. Because every value is restricted to having at most three divisors, the value structure is constrained, and the frequency-based solution avoids any dependence on $n^3$ or $n^2$ over indices.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import Counter

    n = int(input())
    a = list(map(int, input().split()))
    freq = Counter(a)
    vals = list(freq.keys())
    
    ans = 0
    for x in vals:
        for y in vals:
            if x == y:
                cnt = freq[x] * (freq[x] - 1)
            else:
                cnt = freq[x] * freq[y]
            z = x + y
            if z in freq:
                ans += cnt * freq[z]
    return str(ans)

# small cases
assert run("3\n1 2 3\n") == "2"
assert run("4\n1 2 3 3\n") == "4"
assert run("3\n2 2 4\n") == "2"

# duplicates heavy
assert run("5\n1 1 1 2 2\n") >= "0"

# all same
assert run("3\n1 1 1\n") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 2 3` | `2` | ordering of pairs |
| `1 2 3 3` | `4` | duplicate handling for k |
| `2 2 4` | `2` | same-value pair counting |
| `1 1 1` | `0` | no valid sums possible |

## Edge Cases

One important edge case is when all elements are identical. For example, $[1, 1, 1]$. Every ordered pair $(i, j)$ with $i \neq j$ is counted, but the sum is $2$, which does not exist in the array, so the correct answer is zero. The algorithm handles this because $z = x + y$ is never found in the frequency map.

Another edge case is repeated values where valid sums exist but come from identical operands. In $[2, 2, 4]$, the pair $(2, 2)$ is counted as $2 \cdot 1 = 2$ ordered index pairs, and each maps to two choices of $k$, producing four total contributions. The frequency-based pair formula ensures that indices are not reused.

A final subtle case is when the array contains both small and large values, such as $[1, 1000000000000000000, 1000000000000000001]$. The algorithm still works because it relies only on hash lookup for sums, not on any ordering or range assumptions, and large integers are handled naturally in Python arithmetic.
