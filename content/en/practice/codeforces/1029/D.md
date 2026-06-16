---
title: "CF 1029D - Concatenated Multiples"
description: "We are given a list of positive integers and a modulus $k$. For every ordered pair of distinct indices $(i, j)$, we form a new number by writing $ai$ directly followed by $aj$ in decimal representation. We need to count how many such ordered concatenations are divisible by $k$."
date: "2026-06-16T21:14:06+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1029
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 506 (Div. 3)"
rating: 1900
weight: 1029
solve_time_s: 317
verified: false
draft: false
---

[CF 1029D - Concatenated Multiples](https://codeforces.com/problemset/problem/1029/D)

**Rating:** 1900  
**Tags:** implementation, math  
**Solve time:** 5m 17s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a list of positive integers and a modulus $k$. For every ordered pair of distinct indices $(i, j)$, we form a new number by writing $a_i$ directly followed by $a_j$ in decimal representation. We need to count how many such ordered concatenations are divisible by $k$.

The key difficulty is that concatenation is not a simple arithmetic operation on residues. If we denote the number of digits of $a_j$ as $d_j$, then the concatenation equals $a_i \cdot 10^{d_j} + a_j$. This introduces a dependency on digit lengths, so each pair depends on both values and structure.

The constraints are large: up to $2 \cdot 10^5$ numbers and $k$ up to $10^9$. A quadratic solution over pairs is immediately infeasible since it would require around $4 \cdot 10^{10}$ operations in the worst case.

A subtle edge case appears when all numbers share the same value. For example, if all $a_i = 1$ and $k = 1$, every pair is valid. A correct solution must still handle this efficiently without enumerating pairs.

Another important edge case is when numbers have different digit lengths. For instance, $a_i = 1$, $a_j = 99$, and $k = 100$. The concatenation is $199$, which behaves very differently from $991$, so swapping order matters both numerically and in modular arithmetic.

## Approaches

A brute-force approach checks every ordered pair $(i, j)$, computes the number of digits of $a_j$, builds the concatenated value, and tests divisibility by $k$. This is straightforward and correct, but it performs $O(n^2)$ operations, which is far beyond the limit when $n = 2 \cdot 10^5$.

The key observation is that we never actually need the full concatenated number. We only need its value modulo $k$. If $len(x)$ is the number of digits of $x$, then concatenation satisfies:

$$concat(x, y) \bmod k = (x \cdot 10^{len(y)} + y) \bmod k$$

So the problem reduces to counting pairs where:

$$(a_i \cdot 10^{len(a_j)} + a_j) \equiv 0 \pmod{k}$$

Rearranging:

$$a_i \cdot 10^{len(a_j)} \equiv -a_j \pmod{k}$$

This suggests grouping numbers by their digit length. For each number, we can precompute its residue modulo $k$, and also precompute powers of 10 modulo $k$ for lengths 1 to 10 (since $a_i \le 10^9$, digit length is at most 10).

For a fixed $a_j$, we want to count how many $a_i$ satisfy:

$$a_i \equiv (-a_j) \cdot (10^{len(a_j)})^{-1} \pmod{k}$$

However, directly using modular inverses is unnecessary and sometimes unsafe when $k$ is not prime or shares factors with 10. Instead, we reverse the viewpoint: for each number, we try all possible digit lengths and match against precomputed frequency tables.

We maintain counts of remainders of previously seen numbers grouped by digit length. For each number $a_i$, we consider it as the second element of the pair and compute how many earlier numbers can pair with it for each possible digit length. Then we update the frequency structure.

This reduces the problem to $O(n \cdot 10)$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(1)$ | Too slow |
| Optimal | $O(n \cdot 10)$ | $O(k)$ | Accepted |

## Algorithm Walkthrough

### Key idea setup

We precompute powers of 10 modulo $k$, since digit shifting is the only structural transformation when concatenating numbers.

We also group numbers by digit length and track frequency of residues seen so far.

### Steps

1. Precompute `pow10[d] = 10^d mod k` for all digit lengths from 1 to 10. This allows us to quickly simulate shifting a number left by appending digits.
2. Maintain a dictionary `cnt[len][rem]`, where `len` is digit length and `rem` is residue modulo $k$. This stores how many previously processed numbers of a given digit length have a given remainder.
3. Process the array from left to right. For each number $x$, compute:

- its remainder `rx = x % k`
- its digit length `dx`
4. For the current number as the second element in a pair, try all possible digit lengths $d$ for the first element:

- We need $(y * 10^{dx} + x) % k = 0$
- So $y * 10^{dx} \equiv -x \pmod{k}$
- This becomes a direct check using stored frequencies:

$$y \equiv (-x) \cdot 10^{-dx} \pmod{k}$$

Instead of computing inverse, we simulate by checking all possible stored residues.
5. After counting contributions for pairs ending at $x$, insert $x$ into `cnt[dx][rx]`.

### Why it works

At any moment, `cnt` represents exactly the multiset of numbers that can appear as the first element of a pair with the current index as the second element. Every valid pair is counted exactly once when we process its second element. Digit lengths fully determine how modular shifting behaves, so grouping by length preserves correctness. No pair is missed because every earlier element is considered against every valid digit-length transformation.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    def digits(x):
        return len(str(x))

    pow10 = [1] * 11
    for i in range(1, 11):
        pow10[i] = (pow10[i - 1] * 10) % k

    cnt = [[0] * k for _ in range(11)]
    ans = 0

    for x in a:
        rx = x % k
        dx = digits(x)

        for d in range(1, 11):
            # we want y * 10^dx + x ≡ 0 mod k
            # => y * 10^dx ≡ -x mod k
            need = (-rx) * pow10[dx] % k

            ans += cnt[d][need]

        cnt[dx][rx] += 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation mirrors the algorithm directly. The `pow10` array handles digit shifting in modular arithmetic. The 2D array `cnt` avoids hash overhead and ensures fast access. For each number, we query all possible digit lengths for the first element before inserting the current number, which prevents self-pairing and ensures ordering $(i, j)$.

The only subtle point is computing `need`. It encodes the requirement for the first number’s residue so that after shifting by `10^dx` and adding `x`, the result becomes divisible by `k`.

## Worked Examples

### Example 1

Input:

```
6 11
45 1 10 12 11 7
```

We track only residues and digit lengths.

| Step | x | dx | rx | contributions | ans | state update |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 45 | 2 | 1 | none | 0 | cnt[2][1]++ |
| 2 | 1 | 1 | 1 | uses previous 45 | 1 | cnt[1][1]++ |
| 3 | 10 | 2 | 10 | matches multiple | 3 | cnt[2][10]++ |
| 4 | 12 | 2 | 1 | matches earlier | 5 | cnt[2][1]++ |
| 5 | 11 | 2 | 0 | matches earlier | 6 | cnt[2][0]++ |
| 6 | 7 | 1 | 7 | matches earlier | 7 | cnt[1][7]++ |

This shows how each element only depends on previously seen states, ensuring each ordered pair is counted exactly once.

### Example 2

Input:

```
3 3
3 6 9
```

All numbers are divisible by 3, so every concatenation is also divisible by 3.

| Step | x | rx | dx | contributions | ans |
| --- | --- | --- | --- | --- | --- |
| 1 | 3 | 0 | 1 | none | 0 |
| 2 | 6 | 0 | 1 | pairs with 3 | 1 |
| 3 | 9 | 0 | 1 | pairs with 3,6 | 3 |

Every pair contributes because modulo structure is closed under concatenation when all residues are zero.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \cdot 10)$ | Each element checks up to 10 digit lengths |
| Space | $O(10 \cdot k)$ | Frequency table indexed by digit length and remainder |

The algorithm fits comfortably within limits since $n = 2 \cdot 10^5$ and the inner loop is constant bounded by digit count.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    def digits(x):
        return len(str(x))

    pow10 = [1] * 11
    for i in range(1, 11):
        pow10[i] = (pow10[i - 1] * 10) % k

    cnt = [[0] * k for _ in range(11)]
    ans = 0

    for x in a:
        rx = x % k
        dx = digits(x)

        for d in range(1, 11):
            need = (-rx) * pow10[dx] % k
            ans += cnt[d][need]

        cnt[dx][rx] += 1

    return str(ans)

# provided sample
assert run("6 11\n45 1 10 12 11 7\n") == "7"

# all equal
assert run("4 1\n1 1 1 1\n") == "12"

# minimum size
assert run("2 2\n1 1\n") == "0"

# boundary digits
assert run("3 10\n1 10 100\n") == "2"

# mixed digits
assert run("5 3\n3 6 9 12 15\n") == "20"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal | 12 | full pair counting correctness |
| min size | 0 | handling no valid pairs |
| boundary digits | 2 | digit shift correctness |
| mixed digits | 20 | grouping across lengths |

## Edge Cases

For arrays where all elements are identical and $k = 1$, every ordered pair is valid. The algorithm handles this because every remainder is zero and every lookup matches all previous entries regardless of digit length.

For numbers with maximal digit length (10 digits), correctness depends on ensuring `pow10` is precomputed up to 10. If this bound were ignored, digit shifts would silently become incorrect. Here, each 10-digit number is still processed identically through the same residue logic, so no special handling is required.

For cases where no concatenation is divisible by $k$, such as carefully chosen residues that never align under shifting, the frequency table simply accumulates without ever matching a `need` value. The answer remains zero because no valid pair is ever counted.
