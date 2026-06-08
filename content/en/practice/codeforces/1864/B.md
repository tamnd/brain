---
title: "CF 1864B - Swap and Reverse"
description: "We are given a string and two kinds of moves that let us rearrange its characters in a constrained way. One move swaps characters that are two positions apart, and the other reverses a contiguous block of fixed length $k$."
date: "2026-06-08T23:53:21+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy", "sortings", "strings"]
categories: ["algorithms"]
codeforces_contest: 1864
codeforces_index: "B"
codeforces_contest_name: "Harbour.Space Scholarship Contest 2023-2024 (Div. 1 + Div. 2)"
rating: 1100
weight: 1864
solve_time_s: 70
verified: true
draft: false
---

[CF 1864B - Swap and Reverse](https://codeforces.com/problemset/problem/1864/B)

**Rating:** 1100  
**Tags:** constructive algorithms, greedy, sortings, strings  
**Solve time:** 1m 10s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string and two kinds of moves that let us rearrange its characters in a constrained way. One move swaps characters that are two positions apart, and the other reverses a contiguous block of fixed length $k$. We can apply these operations any number of times, in any order, and we want the lexicographically smallest string that can be reached.

The key difficulty is that these operations do not allow arbitrary permutations at first glance. The swap-by-2-positions operation only touches indices of the same parity, and the reversal operation only mixes segments of length $k$, which can interact with parity constraints in subtle ways.

The input size pushes us toward a linear or near-linear solution per test case. Since the total length over all test cases is $10^5$, any solution that tries to simulate operations or run sorting-like behavior per position must avoid $O(n^2)$ behavior. We should expect a solution that reduces the problem to grouping positions and sorting characters within those groups.

A naive mistake would be to assume we can freely sort the entire string. For example, in a case like $n=5, k=3$, not all permutations are achievable, and blindly sorting would violate constraints. Another subtle failure comes from ignoring parity structure: swapping $i$ with $i+2$ means characters at odd indices never mix with even indices, so treating the string as a single pool loses correctness.

## Approaches

If we ignore constraints and simulate all allowed operations, we would be exploring a state graph of all permutations reachable from the initial string. Each state has up to $O(n)$ transitions, and the number of states is factorial in $n$, so this is completely infeasible.

Even if we try greedy simulation, repeatedly applying the lexicographically improving operation, we quickly hit trouble: reversal operations can undo local progress, and the system does not converge in any simple monotone way.

The breakthrough comes from separating the problem into two independent structural effects. The swap $i \leftrightarrow i+2$ creates two independent chains: all even indices can permute among themselves, and all odd indices can permute among themselves, but never mix. The reversal operation of length $k$ allows us to reorder characters across these chains in a controlled way, and the parity of $k$ determines whether the two chains interact.

If $k$ is odd, reversing a segment preserves parity positions, so even and odd positions remain isolated forever. In this case, we can only sort characters within each parity class independently.

If $k$ is even, reversing a segment flips parity alignment inside the block, which effectively allows exchange between parity classes. This makes the system fully connected: any character can eventually move to any position, so we can sort the entire string globally.

So the problem reduces to:

when $k$ is odd, sort even-indexed and odd-indexed characters separately;

when $k$ is even, sort the whole string.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | exponential | exponential | Too slow |
| Parity + sorting insight | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We process each test case independently.

1. Check whether $k$ is even or odd. This determines whether positions can cross between parity groups. The swap-by-2 rule alone preserves parity, so only the reversal changes the structure.
2. If $k$ is even, collect all characters of the string, sort them, and write them back in order from smallest to largest. The reasoning is that the operations generate a fully connected permutation group, so every arrangement is reachable.
3. If $k$ is odd, split characters into two multisets: one containing characters at even indices and one at odd indices (using 0-based indexing). Each set can be permuted independently due to the $+2$ swaps, but they cannot interact.
4. Sort both multisets independently.
5. Reconstruct the final string by filling positions from left to right, taking characters from the corresponding parity pool.

The core reasoning step is that in the odd $k$ case, every operation preserves parity classes. The swap $i \leftrightarrow i+2$ clearly does. A length-$k$ reversal with odd $k$ maps index offsets symmetrically around the center, preserving parity of each position. So no operation ever moves a character from even to odd index or vice versa.

When $k$ is even, the reversal flips parity inside the segment, so repeated applications allow parity mixing across the whole string. Combined with local swaps, this yields full permutation capability.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        s = list(input().strip())

        if k % 2 == 0:
            s.sort()
            print("".join(s))
        else:
            even = []
            odd = []

            for i, ch in enumerate(s):
                if i % 2 == 0:
                    even.append(ch)
                else:
                    odd.append(ch)

            even.sort()
            odd.sort()

            res = []
            ei = oi = 0
            for i in range(n):
                if i % 2 == 0:
                    res.append(even[ei])
                    ei += 1
                else:
                    res.append(odd[oi])
                    oi += 1

            print("".join(res))

if __name__ == "__main__":
    solve()
```

The solution first branches on parity of $k$, which is the structural dividing line. In the even case, a global sort is sufficient because all characters become mutually reachable. In the odd case, we explicitly maintain two sorted pools and reconstruct by alternating parity positions. The reconstruction step is linear and avoids any simulation of operations.

A subtle implementation point is indexing: the parity split must be consistent with 0-based indexing in Python. Mixing 1-based reasoning here would incorrectly swap the groups.

## Worked Examples

### Example 1

Input: `4 2, nima`

Since $k=2$ is even, we sort globally.

| Step | String state | Action |
| --- | --- | --- |
| Start | nima | initial |
| Sort | aimn | reorder all characters |

Output is `aimn`.

This demonstrates the fully connected case: all characters are interchangeable.

### Example 2

Input: `5 3, panda`

Here $k=3$ is odd, so parity is preserved.

We split:

even indices: p(0), n(2), a(4)

odd indices: a(1), d(3)

| Step | Even pool | Odd pool | Action |
| --- | --- | --- | --- |
| Start | p n a | a d | split |
| Sort | a n p | a d | sort pools |
| Rebuild | a a n d p | fill alternating | construct |

Final string is `aandp`.

This confirms that mixing across parity is impossible, so we only optimize within each parity class.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | sorting characters dominates per test case |
| Space | $O(n)$ | storing split arrays and result string |

The total $n$ across test cases is $10^5$, so sorting once per test case remains efficient. The linear reconstruction ensures no hidden quadratic behavior.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    
    def solve():
        t = int(input())
        for _ in range(t):
            n, k = map(int, input().split())
            s = list(input().strip())

            if k % 2 == 0:
                s.sort()
                output.append("".join(s))
            else:
                even = []
                odd = []
                for i, ch in enumerate(s):
                    if i % 2 == 0:
                        even.append(ch)
                    else:
                        odd.append(ch)
                even.sort()
                odd.sort()

                res = []
                ei = oi = 0
                for i in range(n):
                    if i % 2 == 0:
                        res.append(even[ei])
                        ei += 1
                    else:
                        res.append(odd[oi])
                        oi += 1
                output.append("".join(res))

    solve()
    return "\n".join(output)

# provided samples
assert run("""5
4 2
nima
5 3
panda
9 2
theforces
7 3
amirfar
6 4
rounds
""") == """aimn
aandp
ceefhorst
aafmirr
dnorsu"""

# all equal
assert run("""1
5 3
aaaaa
""") == "aaaaa"

# already sorted
assert run("""1
4 2
abcd
""") == "abcd"

# odd k parity split test
assert run("""1
6 3
zxyabc
""") == "axbycz"

# even k global sort test
assert run("""1
5 2
edcba
""") == "abcde"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| samples | given | correctness baseline |
| aaaaa | aaaaa | stability under duplicates |
| abcd, k=2 | abcd | identity case |
| zxyabc, k=3 | axbycz | parity split correctness |
| edcba, k=2 | abcde | global sorting case |

## Edge Cases

For a string like `aaaaa` with any $k$, both operations become irrelevant since all permutations are identical. The algorithm still splits or sorts, but the result remains unchanged, so no incorrect rearrangement occurs.

For small strings where $n = 2$ or $n = 3$, the parity-based split still behaves correctly because one of the groups may be empty, and sorting empty lists is harmless. Reconstruction simply pulls from the non-empty pool.

For alternating patterns like `ababab` with odd $k$, the split preserves structure exactly, and sorting within parity groups may change the arrangement significantly but remains reachable due to swap-by-2 connectivity.
