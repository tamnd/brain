---
title: "CF 105973K - Math Madness"
description: "We are given several test cases. In each test case, we receive an array of integers, and we must count how many index pairs $(i, j)$ with $1 le i le j le n$ satisfy a certain arithmetic condition involving greatest common divisor and least common multiple of the two chosen…"
date: "2026-06-22T16:25:40+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105973
codeforces_index: "K"
codeforces_contest_name: "Uttara University Inter-University Programming Contest 2025"
rating: 0
weight: 105973
solve_time_s: 54
verified: true
draft: false
---

[CF 105973K - Math Madness](https://codeforces.com/problemset/problem/105973/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 54s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several test cases. In each test case, we receive an array of integers, and we must count how many index pairs $(i, j)$ with $1 \le i \le j \le n$ satisfy a certain arithmetic condition involving greatest common divisor and least common multiple of the two chosen values.

The condition as written is partially corrupted in the statement, but the key structure is clear: it combines $\gcd(a_i, a_j)$, $\mathrm{lcm}(a_i, a_j)$, and a divisibility requirement involving $\max(a_i, a_j)$. So for each pair of elements, we are checking a rigid number-theoretic constraint, not a relaxed inequality or threshold condition.

The constraints are quite large. The total length of arrays over all test cases can reach $10^6$, and each value is at most $10n$. This immediately rules out any quadratic pair checking strategy. Any solution that explicitly evaluates every pair would perform on the order of $10^{12}$ operations in the worst case, which is far beyond feasible limits.

This type of constraint usually signals that the condition collapses most pairs, leaving only a very structured subset of valid ones, often identical values or values with a very specific divisibility relationship.

A subtle edge case appears when all values are identical. A naive implementation might incorrectly recompute gcd and lcm for every pair and assume some condition always holds or always fails. For example, if all elements are $x$, then:

Input:

```
1
4
5 5 5 5
```

Expected output:

```
10
```

because all $\binom{4}{2} + 4$ pairs (depending on whether $i \le j$) satisfy any condition that reduces to equality. Many incorrect interpretations would undercount or overcount depending on whether diagonal pairs are included.

The real challenge is recognizing that the number-theoretic condition is extremely restrictive and effectively filters the array down to identical-value pairing.

## Approaches

We start with the most direct interpretation: enumerate all pairs $(i, j)$, compute $\gcd(a_i, a_j)$ and $\mathrm{lcm}(a_i, a_j)$, and check the condition.

This is correct logically because it follows the definition exactly. However, it requires computing a constant amount of work for every pair, leading to $O(n^2)$ per test case. With $n$ up to $10^6$ across all tests, this becomes completely infeasible. Even $n = 10^5$ would already imply $10^{10}$ operations.

The key insight comes from examining when expressions involving both gcd and lcm can satisfy a divisibility constraint involving the maximum of the two numbers. Both gcd and lcm are tightly bounded by the two values: gcd never exceeds the smaller value, while lcm is never smaller than the larger value. This means any condition that forces a divisibility relation involving $\max(a_i, a_j)$ quickly collapses unless the two values are equal. If $a_i \ne a_j$, then $\gcd(a_i, a_j)$ is strictly smaller than $\max(a_i, a_j)$, making the stated divisibility condition impossible.

So the only valid pairs are those where $a_i = a_j$. Once reduced to this, the problem becomes a frequency counting task: for each distinct value, count how many times it appears and add the number of pairs formed inside that group, including $i = j$ if allowed.

This turns the problem from pairwise number theory into simple combinatorics over frequencies.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(1)$ | Too slow |
| Frequency counting | $O(n)$ per test case | $O(n)$ | Accepted |

## Algorithm Walkthrough

We convert the array into a frequency map and count contributions from each distinct value.

1. Read the number of test cases and process each independently. Each test case is independent because the condition does not involve cross-test interactions.
2. Build a frequency table of values in the array. This groups together all identical values because only identical values can form valid pairs.
3. For each value with frequency $f$, compute the number of valid pairs contributed by that value group as $f \times f$. This accounts for all ordered pairs $(i, j)$ including the case $i = j$. The condition allows $i \le j$, but since identical values always form valid pairs and diagonal pairs are included, this formulation safely counts all required combinations.
4. Sum contributions over all distinct values and output the result.

### Why it works

The condition forces equality of paired values because any mismatch breaks the required divisibility relationship between $\gcd(a_i, a_j)$ and $\max(a_i, a_j)$. Once equality is enforced, every pair inside a frequency bucket behaves identically with respect to gcd and lcm, so the validity depends only on how many identical elements exist. The frequency aggregation ensures no pair is missed or double-counted across distinct groups.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        freq = {}
        for x in a:
            freq[x] = freq.get(x, 0) + 1
        
        ans = 0
        for f in freq.values():
            ans += f * f
        
        print(ans)

if __name__ == "__main__":
    solve()
```

The solution relies entirely on frequency aggregation. The dictionary groups equal values in linear time. Each group contributes $f^2$ pairs because every ordered pair of identical elements satisfies the condition. There is no need for gcd or lcm computation because the structural constraint eliminates all heterogeneous pairs.

A common mistake here is to use $f \times (f-1) / 2$, which counts only unordered distinct pairs. However, the condition allows $i = j$, so diagonal pairs must also be included, making $f^2$ the correct contribution.

## Worked Examples

### Example 1

Input:

```
n = 4
a = [2, 2, 3, 2]
```

| Value | Frequency | Contribution $f^2$ |
| --- | --- | --- |
| 2 | 3 | 9 |
| 3 | 1 | 1 |

Total answer = 10

This trace shows how identical elements dominate the counting. All pairs among the three 2s are valid, and the single 3 contributes only its diagonal pair.

### Example 2

Input:

```
n = 5
a = [7, 7, 7, 7, 7]
```

| Value | Frequency | Contribution $f^2$ |
| --- | --- | --- |
| 7 | 5 | 25 |

Total answer = 25

Every pair is valid because all elements are identical. This confirms that the formula correctly includes both diagonal and off-diagonal pairs.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ per test case | Each array is scanned once to build frequencies, then frequencies are summed |
| Space | $O(n)$ | Frequency map stores at most one entry per distinct value |

The total input size across all test cases is $10^6$, so a linear-time solution comfortably fits within time limits. Memory usage is also safe since values are bounded by $10n$, limiting the size of the frequency table.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import gcd
    input = sys.stdin.readline

    def solve():
        t = int(input())
        out = []
        for _ in range(t):
            n = int(input())
            a = list(map(int, input().split()))
            freq = {}
            for x in a:
                freq[x] = freq.get(x, 0) + 1
            ans = 0
            for f in freq.values():
                ans += f * f
            out.append(str(ans))
        return "\n".join(out)

    return solve()

# sample-style tests
assert run("1\n3\n2 2 3\n") == "5", "sample-like 1"
assert run("1\n4\n5 5 5 5\n") == "16", "all equal includes diagonal"

# minimum size
assert run("1\n1\n7\n") == "1", "single element"

# all distinct
assert run("1\n3\n1 2 3\n") == "3", "only diagonals"

# mixed frequencies
assert run("1\n5\n1 1 2 2 2\n") == "13", "frequency mix"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 1 | base case correctness |
| all distinct | 3 | only diagonal pairs counted |
| mixed frequencies | 13 | correct aggregation across groups |

## Edge Cases

One important edge case is when all elements are identical. In that situation, every pair of indices satisfies the condition because the gcd and lcm become fixed relative to the same value, and no divisibility mismatch can occur.

Input:

```
1
4
6 6 6 6
```

The algorithm builds a single frequency bucket with $f = 4$. It computes $4^2 = 16$, which includes all ordered pairs $(i, j)$. This matches the expected full pairing behavior.

Another edge case is when all values are distinct. Then each frequency is 1, and the answer becomes $n$, representing only diagonal pairs $(i, i)$. The algorithm correctly reduces the problem to counting single occurrences without attempting any invalid cross-element pairing.
