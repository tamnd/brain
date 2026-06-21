---
title: "CF 105902E - Binary Banter: Counting Combinatorial Bits"
description: "We are given a number $n$, and for every integer $i$ from $0$ to $n$, we look at the entire $i$-th row of Pascal’s triangle. For each entry in that row, we take the binomial coefficient $binom{i}{j}$, reduce it modulo 2, and sum all those values."
date: "2026-06-22T03:02:35+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105902
codeforces_index: "E"
codeforces_contest_name: "2025 Fujian Normal University Programming Contest"
rating: 0
weight: 105902
solve_time_s: 57
verified: true
draft: false
---

[CF 105902E - Binary Banter: Counting Combinatorial Bits](https://codeforces.com/problemset/problem/105902/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 57s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a number $n$, and for every integer $i$ from $0$ to $n$, we look at the entire $i$-th row of Pascal’s triangle. For each entry in that row, we take the binomial coefficient $\binom{i}{j}$, reduce it modulo 2, and sum all those values. Finally, we sum this quantity over all rows from $0$ to $n$.

So the task is to compute how many odd entries appear in each Pascal row up to $n$, add those counts together, and output the result modulo $998244353$.

The constraints make it clear that $n$ can be as large as $10^{18}$, and there can be up to $3 \cdot 10^5$ test cases. Any solution that tries to iterate over all values up to $n$ is impossible, since even a single test case could require up to $10^{18}$ operations. The intended solution must depend only on the binary representation of $n$, which has at most 60 bits.

A subtle issue arises from the meaning of “$\binom{i}{j} \mod 2$”. We are not summing binomial coefficients themselves, but only their parity. This changes the structure completely: values collapse to 0 or 1, and the problem becomes combinatorial rather than arithmetic. Another potential pitfall is attempting to compute binomial coefficients or factorials directly, which is infeasible for large $i$ and also unnecessary.

## Approaches

A direct interpretation would compute, for each $i$, all $i+1$ binomial coefficients, reduce them modulo 2, and count how many are odd. This already costs $O(i)$ per row, and over all rows up to $n$ it becomes $O(n^2)$, which is far beyond any feasible limit even for small $n$.

The key simplification comes from understanding when binomial coefficients are odd. By Lucas’ theorem in base 2, a binomial coefficient $\binom{i}{j}$ is odd if and only if every bit set in $j$ is also set in $i$. In other words, the number of odd entries in row $i$ equals the number of subsets of the set bits of $i$, which is $2^{\mathrm{popcount}(i)}$.

This transforms the problem into computing

$$\sum_{i=0}^{n} 2^{\mathrm{popcount}(i)}.$$

Now the structure is clearer. Each number contributes a value depending only on how many ones appear in its binary representation. This suggests working over bits rather than iterating over values.

The brute-force idea fails because it enumerates all numbers up to $n$, but the observation that the function depends only on bit counts allows us to split the range by the highest set bit and reduce the problem recursively.

We use the identity that all numbers in a full block of $2^k$ values contribute independently per bit, giving a closed form for complete blocks and a recursive relation for the remaining prefix.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n)$ per test | $O(1)$ | Too slow |
| Bit recursion | $O(\log n)$ per test | $O(\log n)$ | Accepted |

## Algorithm Walkthrough

We define a function $S(x)$ as the required sum from $0$ to $x$, meaning $S(x) = \sum_{i=0}^{x} 2^{\mathrm{popcount}(i)}$.

1. If $x = 0$, return 1 because the only number is 0, whose popcount is 0, contributing $2^0 = 1$.
2. Find the highest power of two not exceeding $x$, say $2^k$. This partitions the range $[0, x]$ into two parts: numbers from $0$ to $2^k - 1$, and numbers from $2^k$ to $x$.
3. For the full block $[0, 2^k - 1]$, every number is exactly a $k$-bit number. Each bit independently contributes either 0 or 1, and a set bit contributes a factor of 2 in the weight. This makes the total contribution equal to $(1 + 2)^k = 3^k$.
4. For numbers in $[2^k, x]$, every number has the highest bit set, contributing a fixed factor of 2. Removing that bit leaves a smaller number in $[0, x - 2^k]$, so the contribution becomes $2 \cdot S(x - 2^k)$.
5. Combine both parts:

$$S(x) = 3^k + 2 \cdot S(x - 2^k).$$
6. Precompute powers of 3 and powers of 2 up to 60 bits and evaluate the recursion per test case.

### Why it works

The recursion is valid because every number is uniquely decomposed into its highest set bit and the remaining suffix. The contribution $2^{\mathrm{popcount}(i)}$ factorizes into a fixed contribution from the highest bit and an independent contribution from the lower bits. The full range splits cleanly into disjoint blocks aligned with powers of two, so no value is counted twice and no value is missed.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

pow3 = [1] * 61
for i in range(1, 61):
    pow3[i] = pow3[i - 1] * 3 % MOD

def solve_one(n: int) -> int:
    if n == 0:
        return 1

    # find highest bit
    k = n.bit_length() - 1
    highest = 1 << k

    # full block [0, 2^k - 1]
    res = pow3[k]

    # remainder
    res += 2 * solve_one(n - highest)
    return res % MOD

def main():
    t = int(input())
    for _ in range(t):
        n = int(input())
        print(solve_one(n) % MOD)

if __name__ == "__main__":
    main()
```

The function `solve_one` follows the recursive decomposition directly. The precomputed `pow3[k]` gives the contribution of a complete $k$-bit space. The recursive call handles the remaining suffix after removing the highest bit.

A common mistake is forgetting that the suffix still contributes with the same structure, just scaled by a factor of 2 because the highest bit is always 1 in that segment.

## Worked Examples

Consider $n = 3$. We compute $S(3)$.

| Step | n | k | 3^k contribution | recursive part | result |
| --- | --- | --- | --- | --- | --- |
| 1 | 3 | 1 | 3 | S(1) | 3 + 2·S(1) |
| 2 | 1 | 0 | 1 | S(0) | 1 + 2·1 |

Now $S(1) = 3$, so $S(3) = 3 + 2 \cdot 3 = 9$.

This matches direct enumeration: $1 + 2 + 2 + 4 = 9$.

Now consider $n = 5$.

| Step | n | k | 3^k contribution | recursive part | result |
| --- | --- | --- | --- | --- | --- |
| 1 | 5 | 2 | 9 | S(1) | 9 + 2·S(1) |
| 2 | 1 | 0 | 1 | S(0) | 1 + 2·1 |

So $S(5) = 9 + 2 \cdot 3 = 15$.

This confirms that the recursion correctly splits the range at powers of two and preserves the weight structure.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(\log n)$ per test | Each call removes the highest set bit, reducing the problem size |
| Space | $O(\log n)$ | recursion depth equals number of bits in $n$ |

The binary length of $n$ is at most 60, so the recursion is extremely small even under the maximum number of test cases.

## Test Cases

```python
import sys, io

MOD = 998244353

pow3 = [1] * 61
for i in range(1, 61):
    pow3[i] = pow3[i - 1] * 3 % MOD

def solve_one(n: int) -> int:
    if n == 0:
        return 1
    k = n.bit_length() - 1
    highest = 1 << k
    return (pow3[k] + 2 * solve_one(n - highest)) % MOD

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    t = int(sys.stdin.readline())
    out = []
    for _ in range(t):
        n = int(sys.stdin.readline())
        out.append(str(solve_one(n) % MOD))
    return "\n".join(out)

# provided samples (from statement description)
assert run("1\n3\n") == "9"
assert run("1\n5\n") == "15"

# custom cases
assert run("1\n0\n") == "1", "minimum"
assert run("1\n1\n") == "3", "small edge"
assert run("1\n2\n") == "5", "binary boundary"
assert run("1\n7\n") == "27", "full 3-bit block"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0 | 1 | base case correctness |
| 1 | 3 | smallest non-trivial binary range |
| 2 | 5 | transition across highest bit |
| 7 | 27 | full block formula $3^k$ correctness |

## Edge Cases

For $n = 0$, the recursion must terminate immediately. The function returns 1, matching the fact that only the empty popcount contributes.

For values of the form $2^k - 1$, the recursion never enters the suffix case. The answer becomes exactly $3^k$, and the implementation must ensure the highest bit is computed correctly so that no off-by-one error shifts $k$.

For powers of two such as $n = 8$, the split produces a full block plus a zero suffix. The suffix recursion must return 1 correctly; otherwise the contribution of the highest segment would be undercounted by a factor of 2 in deeper recursion levels.
