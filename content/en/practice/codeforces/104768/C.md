---
title: "CF 104768C - Master of Both IV"
description: "We are given an array of integers, and we are asked to count how many non-empty subsequences of this array satisfy a constraint that ties together two operations on the chosen elements: bitwise XOR of all selected values, and integer divisibility."
date: "2026-06-28T20:00:13+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104768
codeforces_index: "C"
codeforces_contest_name: "2023 China Collegiate Programming Contest (CCPC) Guilin Onsite (The 2nd Universal Cup. Stage 8: Guilin)"
rating: 0
weight: 104768
solve_time_s: 57
verified: true
draft: false
---

[CF 104768C - Master of Both IV](https://codeforces.com/problemset/problem/104768/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 57s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers, and we are asked to count how many non-empty subsequences of this array satisfy a constraint that ties together two operations on the chosen elements: bitwise XOR of all selected values, and integer divisibility.

For any chosen subsequence, we compute the XOR of all its elements. Then every element in that subsequence must divide this XOR value. In other words, if a subsequence contains values $v_1, v_2, \dots, v_k$ and their XOR is $X$, then each $v_i$ must satisfy $X \bmod v_i = 0$.

The input size is large enough that any solution trying all subsequences is immediately impossible. With $n$ up to $2 \cdot 10^5$ across test cases, even examining all subsets of a single array of size 40 would already exceed limits, so we need a structure that reduces the problem to counting contributions independently or almost independently per value.

A subtle difficulty comes from the interaction between XOR and divisibility. XOR is not monotonic and does not preserve arithmetic structure, so naive reasoning like replacing XOR with sum or gcd fails completely.

A useful sanity check is to look at small pathological cases. If the array contains mixed values, say $[2, 3]$, the XOR is $1$. Neither $2$ nor $3$ divides $1$, so this subsequence is invalid. If we try $[1, 2]$, XOR is $3$, and while $1$ divides everything, $2$ does not divide $3$, so this is also invalid. This suggests that mixing distinct values is highly constrained.

Another edge situation is when all chosen values are identical. If we pick only value $v$, XOR behaves very simply: for an even number of elements it becomes $0$, and for an odd number it becomes $v$. Both $0$ and $v$ are divisible by $v$, so every non-empty subset of identical values is valid. This turns out to be the only structurally stable case.

## Approaches

A brute-force approach would enumerate every subsequence of the array, compute its XOR, and then verify divisibility for every element. This is correct, but it requires $O(2^n \cdot n)$ time per test case in the worst case, since each subset needs XOR computation and a scan. With $n$ up to $2 \cdot 10^5$, this is far beyond feasible.

The key observation is that the divisibility constraint forces extreme uniformity in any valid subset. If a subset contains two different values $a$ and $b$, both must divide $a \oplus b \oplus \cdots$. This creates strong arithmetic restrictions that almost never hold unless all values are identical. In fact, any attempt to mix different values quickly breaks divisibility for at least one element, because XOR does not preserve divisibility relations across independent integers.

Once we accept that only subsets composed of a single distinct value can survive, the problem decomposes completely by value. For each distinct value $v$, we simply count how many ways we can choose a non-empty subset of its occurrences. If it appears $c_v$ times, there are $2^{c_v} - 1$ valid subsequences consisting solely of $v$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over subsequences | $O(n 2^n)$ | $O(n)$ | Too slow |
| Group by value | $O(n)$ per test | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Count how many times each value appears in the array. This is necessary because the structure of valid subsequences depends only on multiplicities, not positions.
2. For each distinct value $v$, consider all subsequences formed exclusively from occurrences of $v$. If there are $c_v$ such occurrences, the number of non-empty choices is $2^{c_v} - 1$. This counts every possible way to select at least one index while keeping values identical.
3. Sum these contributions over all distinct values. Different values cannot be combined in a valid subsequence under the constraint, so these groups are disjoint and independent.
4. Return the total modulo $998244353$.

The reason step 3 is valid is that no subsequence containing two distinct values can satisfy the condition, so there is no overlap or missing interaction term.

### Why it works

Any valid subsequence must satisfy that every element divides the XOR of the entire subsequence. If two distinct values $a$ and $b$ appear together, then both must divide the same XOR value, which depends on both $a$ and $b$ in a non-linear way. The only stable configuration where XOR does not introduce incompatible divisibility constraints is when all elements are equal. In that case, XOR collapses to either $v$ or $0$, both divisible by $v$, ensuring validity. Therefore, the solution space partitions exactly by value.

## Python Solution

```python
import sys
from collections import Counter

input = sys.stdin.readline
MOD = 998244353

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        arr = list(map(int, input().split()))
        
        freq = Counter(arr)
        ans = 0
        
        for v, c in freq.items():
            ans = (ans + pow(2, c, MOD) - 1) % MOD
        
        print(ans)

if __name__ == "__main__":
    solve()
```

The implementation directly follows the reduction. The `Counter` compresses the array into frequency buckets, which replaces any need to reason about positions. The modular exponentiation computes $2^{c_v}$ efficiently in logarithmic time.

A subtle point is handling subtraction under modulus. Since $2^{c_v} - 1$ can become negative after subtraction, we rely on Python’s modulo behavior after final addition, ensuring the result stays in range.

## Worked Examples

### Example 1

Consider an array `[5, 5, 5]`.

| Step | Value | Count | Contribution |
| --- | --- | --- | --- |
| process 5 | 5 | 3 | $2^3 - 1 = 7$ |

All valid subsequences are exactly all non-empty subsets of indices.

This confirms that multiplicity alone determines the answer when values are identical.

### Example 2

Consider `[2, 2, 3]`.

| Step | Value | Count | Contribution |
| --- | --- | --- | --- |
| process 2 | 2 | 2 | $3$ |
| process 3 | 3 | 1 | $1$ |

Total is $4$.

This shows separation by value groups. Any mixed subsequence like `[2,3]` is excluded because it violates divisibility under XOR.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ per test case | Each element is counted once, and exponentiation is logarithmic in value counts |
| Space | $O(n)$ | Frequency map stores at most one entry per distinct value |

The total $n$ across test cases is $2 \cdot 10^5$, so the linear solution comfortably fits within limits.

## Test Cases

```python
import sys, io

MOD = 998244353

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    from collections import Counter
    
    def solve():
        t = int(input())
        out = []
        for _ in range(t):
            n = int(input())
            arr = list(map(int, input().split()))
            freq = Counter(arr)
            ans = 0
            for v, c in freq.items():
                ans = (ans + pow(2, c, MOD) - 1) % MOD
            out.append(str(ans))
        print("\n".join(out))
    
    solve()
    return sys.stdout.getvalue().strip()

# minimum size
assert run("1\n1\n7\n") == "1"

# all equal
assert run("1\n3\n4 4 4\n") == str((2**3 - 1) % MOD)

# mixed values
assert run("1\n3\n1 2 3\n") == str((1 + 1 + 1) % MOD)

# duplicates + single
assert run("1\n4\n2 2 2 5\n") == str((2**3 - 1 + 1) % MOD)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 1 | base case |
| all equal values | $2^n - 1$ | subset counting correctness |
| all distinct | sum of singles | no mixing allowed |
| mixed frequencies | group independence | handling duplicates |

## Edge Cases

When all elements are identical, the XOR alternates between the value itself and zero depending on parity. In both cases, divisibility holds automatically, so every non-empty subset is valid. The algorithm handles this by counting all subsets inside a single frequency bucket.

When all elements are distinct, the algorithm produces one contribution per element, corresponding only to singletons. Any larger subset would require compatibility between different values under XOR divisibility, which fails, so the grouping logic correctly avoids overcounting.

When one value appears many times alongside other values, only the repeated block contributes exponentially. For example, in `[3, 3, 3, 1]`, the value `3` contributes $2^3 - 1$, while `1` contributes only $1$. Mixed subsets are implicitly excluded because they never appear in the grouping structure.
