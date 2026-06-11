---
title: "CF 1107B - Digital root"
description: "We are asked to answer multiple independent queries. Each query gives two numbers, a position $k$ and a digit $x$ between 1 and 9. For each query, we need to output the $k$-th positive integer whose digital root equals $x$."
date: "2026-06-12T05:22:17+07:00"
tags: ["codeforces", "competitive-programming", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1107
codeforces_index: "B"
codeforces_contest_name: "Educational Codeforces Round 59 (Rated for Div. 2)"
rating: 1000
weight: 1107
solve_time_s: 70
verified: true
draft: false
---

[CF 1107B - Digital root](https://codeforces.com/problemset/problem/1107/B)

**Rating:** 1000  
**Tags:** math, number theory  
**Solve time:** 1m 10s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to answer multiple independent queries. Each query gives two numbers, a position $k$ and a digit $x$ between 1 and 9. For each query, we need to output the $k$-th positive integer whose digital root equals $x$.

The digital root of a number is what remains after repeatedly summing its digits until a single digit remains. For example, numbers like 5, 14, 23, 32 all reduce to 5, while numbers like 2, 11, 20, 29 all reduce to 2.

So each query is effectively asking us to enumerate the infinite increasing sequence of numbers grouped by their digital root and pick the $k$-th element in the group for a given digit.

The constraints matter because $k$ can be as large as $10^{12}$, which immediately rules out any approach that tries to iterate through numbers and compute digital roots one by one. Even checking $10^9$ numbers per query would be far beyond the time limit. Since there are up to $10^3$ queries, we need a direct formula that maps $(k, x)$ to the answer in constant time.

A subtle point is that digital root behaves cyclically with respect to modulo 9. A naive mistake is to assume we can just construct numbers digit by digit or simulate digit sums, but that completely breaks under the input scale.

Edge cases appear when $x = 9$, because digital root 9 corresponds exactly to multiples of 9, not residues congruent to 9 mod 9 in a naive sense unless handled carefully. Another issue is off-by-one behavior when mapping the first element of each group.

For example, for $x = 1$, the sequence starts as:

1, 10, 19, 28, 37, ...

For $x = 9$, it starts as:

9, 18, 27, 36, 45, ...

Any solution must generate these sequences directly without scanning integers.

## Approaches

A brute-force method would process each query independently by iterating over natural numbers, computing their digital root, and collecting matches until reaching the $k$-th one. This works because every number has a well-defined digital root, and we can test membership in $O(\log n)$ time per number. However, in the worst case, if $k = 10^{12}$, we would need to scan up to $10^{12}$ numbers per query, making the solution infeasible.

The key observation is that digital root is determined entirely by a number’s value modulo 9, with the special case that multiples of 9 correspond to digital root 9. This creates a perfect periodic structure: every block of 9 consecutive integers contains exactly one number for each digital root from 1 to 9.

This means the sequence of numbers with a given digital root forms an arithmetic progression with step size 9. Once we identify the first number in the sequence for a given $x$, the $k$-th number is simply that starting point plus $9 \cdot (k-1)$.

For $x = 9$, the first number is 9. For $x \in [1,8]$, the first number is $x$ itself. This gives a direct closed-form solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n \cdot k)$ | $O(1)$ | Too slow |
| Optimal | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

For each query $(k, x)$, we construct the answer directly.

1. Determine the first number in the sequence corresponding to digital root $x$. If $x = 9$, this number is 9. Otherwise it is $x$. This works because single-digit numbers already have themselves as digital roots, and 9 is the first multiple of 9.
2. Once the starting point is fixed, observe that adding 9 preserves the digital root. This is because adding 9 does not change a number’s residue modulo 9 in a way that affects its digital root classification.
3. Compute the answer as:

$$\text{ans} = \text{start} + 9 \cdot (k - 1)$$
4. Output this value for each query independently.

Why it works

The correctness comes from partitioning positive integers into nine arithmetic progressions based on their remainder modulo 9, with the exception that remainder 0 corresponds to digital root 9. Every integer belongs to exactly one progression, and each progression increases by 9 while preserving the same digital root. Therefore, indexing into a progression is equivalent to counting forward by fixed steps, which guarantees that the constructed $k$-th element is exactly the required number.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    for _ in range(n):
        k, x = map(int, input().split())
        start = 9 if x == 9 else x
        print(start + 9 * (k - 1))

if __name__ == "__main__":
    solve()
```

The solution reads each query and computes the answer in constant time. The key implementation detail is handling $x = 9$ separately, since it corresponds to the arithmetic progression starting at 9 rather than 0 or 9 modulo 9 ambiguity.

## Worked Examples

### Example 1

Input:

```
3
1 5
5 2
3 1
```

| Query | k | x | start | formula | result |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 5 | 5 | 5 + 9·0 | 5 |
| 2 | 5 | 2 | 2 | 2 + 9·4 | 38 |
| 3 | 3 | 1 | 1 | 1 + 9·2 | 19 |

This trace shows that each digital root class behaves like a simple arithmetic progression, and indexing is purely linear.

### Example 2

Input:

```
2
4 9
6 7
```

| Query | k | x | start | formula | result |
| --- | --- | --- | --- | --- | --- |
| 1 | 4 | 9 | 9 | 9 + 9·3 | 36 |
| 2 | 6 | 7 | 7 | 7 + 9·5 | 52 |

This confirms that even the special case $x = 9$ fits seamlessly into the same structure.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Each query is answered with a constant number of arithmetic operations |
| Space | $O(1)$ | No auxiliary structures are required |

The constraints allow up to $10^3$ queries, so a constant-time per query solution is easily sufficient. Even with $k$ up to $10^{12}$, we never iterate up to $k$, only compute a direct formula.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n = int(input())
    out = []
    for _ in range(n):
        k, x = map(int, input().split())
        start = 9 if x == 9 else x
        out.append(str(start + 9 * (k - 1)))
    return "\n".join(out)

# provided samples
assert run("3\n1 5\n5 2\n3 1\n") == "5\n38\n19"

# minimum k
assert run("1\n1 9\n") == "9"

# first element of each class
assert run("3\n1 1\n1 5\n1 9\n") == "1\n5\n9"

# large k
assert run("2\n1000000000000 1\n1000000000000 9\n") == "8999999999991\n8999999999999"

# boundary mix
assert run("2\n2 2\n3 8\n") == "11\n26"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| k=1 cases | 1,5,9 | correct starting points |
| large k | big values | no overflow, correct formula scaling |
| mixed digits | varied outputs | correct handling of all x |

## Edge Cases

For $x = 9$, the sequence is multiples of 9. The algorithm sets `start = 9`, so for input $(k=1, x=9)$, we get 9. For $k=4$, we compute $9 + 27 = 36$, which matches the 4th multiple of 9.

For small values like $x = 1$, the sequence begins at 1. For $(k=1, x=1)$, we get 1. For $(k=3, x=1)$, we compute $1 + 18 = 19$, which matches the direct enumeration 1, 10, 19.

For very large $k$, the computation remains stable because it only uses multiplication and addition on 64-bit safe integers. Python naturally handles big integers, so there is no overflow risk.
