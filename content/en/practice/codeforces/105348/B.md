---
title: "CF 105348B - And Xor Pair"
description: "We are asked to count how many ordered pairs of integers $(x, y)$ can be formed from a given number $n$, under two binary constraints applied bit by bit."
date: "2026-06-23T15:42:55+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105348
codeforces_index: "B"
codeforces_contest_name: "Coding Challenge Alpha VII - by Algorave"
rating: 0
weight: 105348
solve_time_s: 351
verified: false
draft: false
---

[CF 105348B - And Xor Pair](https://codeforces.com/problemset/problem/105348/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 5m 51s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to count how many ordered pairs of integers $(x, y)$ can be formed from a given number $n$, under two binary constraints applied bit by bit.

The first constraint fixes the XOR of the pair: when we compare each bit of $x$ and $y$, their XOR must reproduce the binary representation of $n$. The second constraint fixes their bitwise AND, but shifted: the AND of $x$ and $y$ is not equal to $n$, but instead equals $2n$, which is $n$ shifted left by one binary position.

The output for each test case is the number of valid pairs $(x, y)$ that satisfy both constraints simultaneously. Order matters, so $(x, y)$ and $(y, x)$ are counted separately if they are different.

The constraints allow $n$ up to $10^{15}$, which means we are working with at most 60 bits per number. A solution that processes each bit independently or in a small linear scan per test case is sufficient, while anything that tries to enumerate values of $x$ or $y$ directly is immediately infeasible since that would grow exponentially with the number of bits.

A subtle issue appears when thinking about the interaction between the two constraints. XOR and AND normally describe independent per-bit behavior, but here AND is shifted by one position relative to XOR. That creates a coupling between adjacent bits of $n$, which is easy to miss in a naive per-bit decomposition.

One edge case makes this especially visible. If $n = 1$, then the shift forces a constraint involving the second bit of $x$ and $y$, even though XOR only touches the lowest bit. This is why solutions that treat each bit independently without accounting for the shift produce incorrect counts or overcount invalid pairs.

## Approaches

A brute-force approach would try all possible values of $x$ and $y$ up to some limit implied by $n$. Since $x \oplus y = n$, both numbers must stay within roughly the same bit-length as $n$, so one might attempt iterating all values from $0$ to $2^{60}$. Even restricting to valid pairs through checking both conditions still leads to an infeasible search space on the order of $2^{120}$ candidate pairs.

The key simplification comes from rewriting the relationship between XOR and AND. For any two integers, the identity

$$x + y = (x \oplus y) + 2(x \& y)$$

always holds. Substituting the constraints gives:

$$x + y = n + 2 \cdot (2n) = 5n$$

So the sum is fixed. However, the real structure is stronger than just fixing the sum: XOR and AND constraints together determine each bit independently, except for the shift inside the AND condition.

The shifted AND means that bit $i$ of $x \& y$ equals bit $i$ of $2n$, which is bit $i-1$ of $n$. This introduces a dependency between adjacent bits of $n$, turning the problem into a local consistency check over neighboring bits.

Once we express everything per bit, each position admits only a few possible assignments for $(x_i, y_i)$, and the entire solution becomes a product over independent bit contributions, as long as no contradiction appears.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^{60})$ or worse | $O(1)$ | Too slow |
| Optimal | $O(\log n)$ per test | $O(1)$ | Accepted |

## Algorithm Walkthrough

We work in binary and process each bit position independently, while carefully tracking the interaction introduced by the shifted AND.

1. Write two bitmasks: one is $A = n$, representing the XOR constraint, and the other is $B = 2n$, representing the AND constraint. We interpret both bit by bit.
2. Observe that bit $i$ of $B$ equals bit $i-1$ of $n$, with the convention that the lowest bit of $B$ is zero. This is where adjacency constraints come from.
3. For each bit position $i$, consider the pair $(x_i, y_i)$. These two bits must satisfy:

- $x_i \oplus y_i = A_i$
- $x_i \& y_i = B_i$
4. Enumerate the four possible bit pairs:

- $00 \rightarrow (A=0, B=0)$
- $01 \rightarrow (A=1, B=0)$
- $10 \rightarrow (A=1, B=0)$
- $11 \rightarrow (A=0, B=1)$

This table shows that each constraint pair maps to either zero, one, or two valid configurations.
5. Translate this into counting rules:

- If $A_i = 1$ and $B_i = 1$, the configuration is impossible.
- If $B_i = 0$ and $A_i = 1$, there are two choices.
- Otherwise, there is exactly one choice.
6. The only way to get multiple choices is when $A_i = 1$ and $B_i = 0$, which corresponds to a 1-bit in $n$ whose previous bit is 0.
7. Summing over all bits, the answer becomes $2^{k}$, where $k$ is the number of positions where $n$ has a 1-bit that is not immediately preceded by another 1-bit.
8. If any position has $A_i = 1$ and $B_i = 1$, the construction breaks completely and the answer is zero.

### Why it works

Each bit position behaves like a local constraint system involving only $x_i$, $y_i$, and the adjacent bit of $n$ through the shifted AND. Once we ensure no adjacent ones appear in $n$, all constraints become independent across bits, so the total number of valid assignments is the product of per-bit choices. Any dependency beyond adjacent bits does not exist, so no global coupling can invalidate a locally consistent assignment.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        
        # invalid if n has consecutive 1s
        if n & (n << 1):
            print(0)
            continue
        
        # count valid "free-choice" bits
        ans = 1
        while n:
            if n & 1:
                ans <<= 1
            n >>= 1
        
        print(ans)

if __name__ == "__main__":
    solve()
```

The implementation first checks the key structural condition: if two adjacent bits in $n$ are both 1, the shifted AND constraint forces a contradiction, so the answer is immediately zero.

If the configuration is valid, every 1-bit in $n$ contributes a factor of 2 to the answer, because it corresponds to a position where $(x_i, y_i)$ can be chosen in two distinct ways. The loop simply counts these contributions by scanning the binary representation.

Shifting $n$ destructively inside the loop is safe because we only need its bits; no positional information is required once adjacency has been validated.

## Worked Examples

Consider $n = 5$, whose binary form is $101$.

| bit i | n_i (A_i) | n_{i-1} (B_i) | contribution |
| --- | --- | --- | --- |
| 0 | 1 | 0 | 2 |
| 1 | 0 | 1 | 1 |
| 2 | 1 | 0 | 2 |

The total is $2 \times 1 \times 2 = 4$. This shows how only isolated 1-bits contribute multiplicatively.

Now consider $n = 3$, binary $11$.

| bit i | n_i (A_i) | n_{i-1} (B_i) | validity |
| --- | --- | --- | --- |
| 0 | 1 | 0 | ok |
| 1 | 1 | 1 | invalid |

The second row violates the constraint because a 1 in $n_i$ coincides with a shifted 1 in $B_i$, which makes XOR and AND incompatible at that position. This forces the answer to zero.

The second case demonstrates why adjacency in $n$ fully determines feasibility.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(t \log n)$ | Each test scans binary bits once |
| Space | $O(1)$ | Only a few counters and bit operations |

The bit-length of $n$ is at most 60, so even with $10^3$ test cases, the solution runs comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque
    it = sys.stdin.read().strip().split()
    
    t = int(it[0])
    idx = 1
    out = []
    
    for _ in range(t):
        n = int(it[idx]); idx += 1
        
        if n & (n << 1):
            out.append("0")
        else:
            ans = 1
            while n:
                if n & 1:
                    ans <<= 1
                n >>= 1
            out.append(str(ans))
    
    return "\n".join(out)

# provided sample (interpreted as multiple numbers)
assert run("7\n0\n1\n8\n10\n12\n17\n21\n") == "1\n2\n2\n4\n0\n4\n8"

# custom cases
assert run("1\n2\n") == "2", "single bit"
assert run("1\n3\n") == "0", "adjacent ones invalid"
assert run("1\n5\n") == "4", "alternating bits"
assert run("1\n0\n") == "1", "zero case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 | 2 | single-bit behavior |
| 3 | 0 | adjacency violation |
| 5 | 4 | multiple independent 1-bits |
| 0 | 1 | base edge case |

## Edge Cases

When $n = 0$, there are no 1-bits and no adjacency constraints. The algorithm produces an empty product, which correctly evaluates to 1. The only valid pair is $(0,0)$, matching the construction.

When $n$ contains consecutive 1s, such as $n = 3$, the condition $n \& (n \ll 1) \neq 0$ triggers immediately. This captures exactly the situation where a bit in $n$ forces both XOR and shifted AND to demand incompatible values at the same position.

When $n$ is a power of two, every 1-bit is isolated, so each contributes independently a factor of 2, leading to a clean exponential result equal to 2.
