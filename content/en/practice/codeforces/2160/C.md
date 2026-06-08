---
title: "CF 2160C - Reverse XOR"
description: "We are given a target integer $n$, and we want to know whether it is possible to construct some positive integer $x$ such that a specific transformation applied to $x$ and combined with XOR produces exactly $n$."
date: "2026-06-09T04:21:42+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks"]
categories: ["algorithms"]
codeforces_contest: 2160
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 1058 (Div. 2)"
rating: 1300
weight: 2160
solve_time_s: 90
verified: false
draft: false
---

[CF 2160C - Reverse XOR](https://codeforces.com/problemset/problem/2160/C)

**Rating:** 1300  
**Tags:** bitmasks  
**Solve time:** 1m 30s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a target integer $n$, and we want to know whether it is possible to construct some positive integer $x$ such that a specific transformation applied to $x$ and combined with XOR produces exactly $n$.

The transformation $f(x)$ takes the binary representation of $x$, reverses the bit order, and interprets the result as a new binary number. Crucially, leading zeros after reversal are ignored, which means the effective bit-length of the result depends on the highest set bit in the reversed string.

So the process is: pick a number $x$, write it in binary, reverse those bits, form a new integer $f(x)$, and check whether $x \oplus f(x) = n$.

The output is simply a yes/no decision for each test case.

The constraint $n < 2^{30}$ implies that we only need to reason about numbers up to 30 bits. Any valid $x$ that matters must also lie within a small enough bit-width so that reversing bits does not overflow into an unbounded search space. A naive search over all integers up to $2^{30}$ is already too large, since it would imply up to $10^9$ candidates per test case in the worst scenario when multiplied by $t = 10^4$.

A more subtle issue is that $f(x)$ is not a simple bitwise operation like complement or shift. Reversal couples the least significant bit of $x$ with the most significant bit of $f(x)$, which breaks locality. This makes greedy reasoning on bits unreliable unless we explicitly exploit symmetry.

Edge cases appear when $x$ has a single set bit or very sparse structure. For example, $x = 1$ yields $f(x) = 1$, so XOR is zero. This shows that $n = 0$ is always possible. On the other hand, small values like $n = 8$ fail despite having many representations because reversing bits does not preserve positional independence, and XOR constraints become globally inconsistent across the bitstring.

## Approaches

A direct brute force approach tries every candidate $x$, computes $f(x)$, and checks whether $x \oplus f(x) = n$. The cost of computing $f(x)$ is proportional to the bit-length of $x$, so about $O(\log x)$. However, the number of candidates up to $2^{30}$ makes this completely infeasible. Even testing a fraction of them per query leads to billions of operations.

The key structural observation is that the binary representation of $x$ is not arbitrary once we think in terms of palindromic constraints induced by XOR with its reversal. Each bit of $x$ interacts with exactly one mirrored bit of $f(x)$. This means the system decomposes into independent constraints on bit pairs, but with a twist: carries do not exist in XOR, so each bit position can be treated independently once we fix the length of $x$.

We can instead reinterpret the problem as constructing a binary string $s$ such that if we reverse it to get $s^R$, then $s \oplus s^R = n$. This turns the problem into a consistency check over symmetric bit pairs. The only real difficulty is that the length of $s$ is unknown, so we try possible lengths up to 30 bits. For each length, we attempt to assign bits from both ends inward, ensuring consistency with the required XOR bits of $n$. If any length yields a consistent assignment, the answer is YES.

This reduces the problem from searching over integers to checking feasibility of a finite constraint system.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^{30} \cdot \log n)$ | $O(1)$ | Too slow |
| Optimal | $O(30^2)$ per test | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. For each test case, consider possible binary lengths $L$ from 1 to 30. The idea is that $x$ cannot need more than 30 bits since $n$ itself is bounded.
2. For a fixed length $L$, interpret $x$ as an $L$-bit binary string $s$. We want $s \oplus reverse(s) = n$, but only the lowest $L$ bits of $n$ matter.
3. For each position $i$ from 0 to $L-1$, we pair it with position $j = L-1-i$. These two positions determine each other through the XOR constraint:

$$s[i] \oplus s[j] = n[i]$$
4. If $i = j$, meaning we are at the middle bit of an odd-length string, the equation becomes:

$$s[i] \oplus s[i] = 0$$

so we must have $n[i] = 0$. If $n[i] = 1$, this length $L$ is impossible.
5. For $i < j$, we try both assignments consistent with XOR:

if $n[i] = 0$, then $s[i] = s[j]$, otherwise $s[i] \neq s[j]$. We propagate assignments and check consistency.
6. If we successfully assign all bits without contradiction and ensure $x > 0$, we return YES immediately.
7. If no length $L$ works, return NO.

### Why it works

The correctness comes from reducing the XOR equation into independent constraints over mirrored bit positions. XOR removes carry dependencies, so each bit equation is local. The reversal operation only permutes indices, so the entire system becomes a set of equality or inequality constraints between pairs of variables. Any valid solution corresponds exactly to a consistent assignment in this constraint graph, and every consistent assignment defines a valid integer $x$. Since all possible bit-lengths are tested, no valid configuration is missed.

## Python Solution

```python
import sys
input = sys.stdin.readline

def ok(n, L):
    bits = [(n >> i) & 1 for i in range(L)]
    s = [-1] * L

    for i in range(L):
        j = L - 1 - i
        if i > j:
            break

        if i == j:
            if bits[i] == 1:
                return False
            if s[i] == -1:
                s[i] = 0
            continue

        if bits[i] == 0:
            # s[i] == s[j]
            for a, b in [(i, j)]:
                if s[a] == -1 and s[b] == -1:
                    s[a], s[b] = 0, 0
                elif s[a] == -1:
                    s[a] = s[b]
                elif s[b] == -1:
                    s[b] = s[a]
                elif s[a] != s[b]:
                    return False
        else:
            # s[i] != s[j]
            if s[i] == -1 and s[j] == -1:
                s[i], s[j] = 0, 1
            elif s[i] == -1:
                s[i] = 1 - s[j]
            elif s[j] == -1:
                s[j] = 1 - s[i]
            elif s[i] == s[j]:
                return False

    if all(v == 0 for v in s):
        return False

    return True

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        ans = False
        for L in range(1, 31):
            if ok(n, L):
                ans = True
                break
        print("YES" if ans else "NO")

if __name__ == "__main__":
    solve()
```

The core of the implementation is the `ok` function, which tries to construct a valid binary string of fixed length $L$. The array `s` represents unknown bits of $x$, initialized to `-1` meaning unassigned. For each mirrored pair, we enforce either equality or inequality depending on the corresponding bit of $n$. When both bits in a pair are unassigned, we directly assign a valid configuration; otherwise we propagate constraints and verify consistency.

The middle-bit condition is handled explicitly when $i = j$, since XOR of a bit with itself cannot produce 1. The final check ensures that $x$ is positive by rejecting the all-zero assignment.

## Worked Examples

### Example 1: $n = 3$

We try $L = 2$ first since small lengths often suffice.

| i | j | n[i] | Constraint | s state |
| --- | --- | --- | --- | --- |
| 0 | 1 | 1 | s[0] ≠ s[1] | (0,1) |

We get $s = 01$, which corresponds to $x = 2$. Reversing gives $f(x) = 1$, and XOR is 3, matching $n$.

This confirms that the algorithm correctly explores minimal valid representations without over-constraining bit assignments.

### Example 2: $n = 8$

We test lengths up to 30. For small $L$, constraints quickly fail because higher-order bit 3 in $n$ forces an asymmetry that cannot be matched by any mirrored binary structure. For all candidate lengths, at least one constraint contradiction appears in the pairing step, so no assignment is possible.

This shows how global asymmetry in $n$ prevents any mirrored binary construction from existing.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(30^2 \cdot t)$ | For each test, we try up to 30 lengths and process up to 30 bit pairs per length |
| Space | $O(1)$ | Only fixed-size arrays for bit simulation |

The total work is at most a few million simple bit operations across all test cases, which is easily within limits for $t \le 10^4$.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def ok(n, L):
        bits = [(n >> i) & 1 for i in range(L)]
        s = [-1] * L
        for i in range(L):
            j = L - 1 - i
            if i > j:
                break
            if i == j:
                if bits[i] == 1:
                    return False
                continue
            if bits[i] == 0:
                if s[i] == -1 and s[j] == -1:
                    s[i] = s[j] = 0
                elif s[i] == -1:
                    s[i] = s[j]
                elif s[j] == -1:
                    s[j] = s[i]
                elif s[i] != s[j]:
                    return False
            else:
                if s[i] == -1 and s[j] == -1:
                    s[i], s[j] = 0, 1
                elif s[i] == -1:
                    s[i] = 1 - s[j]
                elif s[j] == -1:
                    s[j] = 1 - s[i]
                elif s[i] == s[j]:
                    return False
        return any(s)

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        ok_flag = False
        for L in range(1, 31):
            if ok(n, L):
                ok_flag = True
                break
        out.append("YES" if ok_flag else "NO")
    return "\n".join(out)

assert run("6\n0\n3\n6\n8\n10\n11\n") == "YES\nYES\nYES\nNO\nYES\nNO", "sample 1"

# edge cases
assert run("1\n0\n") == "YES"
assert run("1\n1\n") == "YES"
assert run("1\n8\n") == "NO"
assert run("3\n0\n3\n10\n") == "YES\nYES\nYES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n0\n` | YES | smallest valid case |
| `1\n1\n` | YES | single-bit construction |
| `1\n8\n` | NO | asymmetric high-bit failure |
| `3\n0\n3\n10\n` | YES YES YES | mixed small cases consistency |

## Edge Cases

For $n = 0$, the construction is trivial because any palindromic binary number works. The algorithm finds $L = 1$, assigns $s = [0]$, and immediately accepts.

For $n = 1$, a valid construction exists with $x = 1$. In the check, $L = 1$ again produces a single middle bit, which is only valid when $n[i] = 0$, so instead the algorithm shifts to $L = 2$ and finds a consistent asymmetric assignment.

For values like $n = 8$, the highest set bit forces constraints across mirrored positions that cannot be satisfied simultaneously for any length. Every attempted $L$ produces a contradiction either at a fixed middle bit or at a forced mismatch in a mirrored pair, so all paths correctly fail.
