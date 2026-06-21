---
title: "CF 105900B - Boundless Deck"
description: "We are given an infinite collection of cards where each card is labeled by a power of a fixed integer $n$. The first card has value $n^0$, the second $n^1$, the third $n^2$, and so on."
date: "2026-06-21T15:17:34+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105900
codeforces_index: "B"
codeforces_contest_name: "VI UnBalloon Contest Mirror"
rating: 0
weight: 105900
solve_time_s: 59
verified: true
draft: false
---

[CF 105900B - Boundless Deck](https://codeforces.com/problemset/problem/105900/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 59s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an infinite collection of cards where each card is labeled by a power of a fixed integer $n$. The first card has value $n^0$, the second $n^1$, the third $n^2$, and so on. From this deck, a “move” is formed by selecting any finite subset of cards, and the value of the move is simply the sum of the selected card values.

So every move corresponds to choosing some indices $i$, and summing $n^i$. Since each card can either be chosen or not chosen, every move is essentially a subset sum over powers of $n$.

All possible moves are then sorted by their resulting sum, and we are asked for the $k$-th smallest sum in this ordering.

The constraints are large: both $n$ and $k$ can be up to $10^9$. This immediately rules out any attempt to explicitly generate subsets or even enumerate values up to $k$ by simulation. The number of subsets grows exponentially with the number of cards considered, so a naive approach would explode even for modest cutoffs.

A subtle point is understanding whether the empty subset is included. The examples clarify that it is not, since the sequence starts from 1, not 0. That means we only consider non-empty subsets.

A typical failure case comes from trying to generate sums greedily or using a priority queue over subsets. For example, even with just powers $1, n, n^2$, the number of subsets is already 8, and expanding this structure to reach $k = 10^9$ is impossible.

The real difficulty is recognizing the structure of these sums in sorted order.

## Approaches

A brute-force approach would attempt to generate all subsets of indices and compute their sums, then sort them. Even if we tried to generate them incrementally, the number of subsets grows as $2^m$ where $m$ is the number of considered powers. To reach values around $k$, we would need $m$ large enough that $2^m \ge k$, meaning $m \approx 30$ already suffices for $k \le 10^9$. However, explicitly enumerating subsets and sorting them still requires storing around a billion values in the worst case, which is impossible.

The key insight is to stop thinking of subsets as combinatorial objects and instead reinterpret the sum structure. Each subset corresponds to choosing whether to include each power $n^i$. This is exactly a binary choice per index, so every move corresponds to a binary string, and the value is the evaluation of that binary string in base $n$ using digits only 0 and 1.

Now the crucial observation is that sorting these values by their numeric value is equivalent to sorting their binary representations interpreted as numbers with positional weights $n^i$. Since higher powers dominate lower ones (because $n \ge 2$), this ordering aligns perfectly with the natural ordering of binary integers interpreted in standard base-2 positional significance.

This means the $k$-th smallest value corresponds exactly to writing $k$ in binary, and interpreting each bit as whether to include the corresponding power of $n$. The $i$-th bit contributes $n^i$ to the final sum.

So instead of generating subsets, we directly decode $k$ into binary.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Enumeration | $O(2^m \log 2^m)$ | $O(2^m)$ | Too slow |
| Binary Representation Mapping | $O(\log k)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We want to compute the value represented by the binary form of $k$, where each bit corresponds to selecting a power of $n$.

1. Read $n$ and $k$. We treat $k$ as a rank in the sorted list of subset sums.
2. Convert $k$ into its binary representation. Each bit position $i$ tells us whether $n^i$ is included in the subset.
3. Initialize a running answer as 0 and a current power value as 1, representing $n^0$.
4. Iterate over bits of $k$ from least significant to most significant. For each bit:

If the bit is 1, add the current power of $n$ to the answer.
5. After processing each bit, multiply the current power by $n$ (modulo $10^9+7$) to move to the next exponent.
6. Output the final accumulated sum modulo $10^9+7$.

The reason multiplication by $n$ works is that each step shifts us from $n^i$ to $n^{i+1}$, matching the structure of the deck.

### Why it works

Every subset corresponds uniquely to a binary string, and its value is a positional number system with base $n$ and digits restricted to 0 or 1. Since $n \ge 2$, higher indices always dominate lower ones, ensuring that sorting by value is identical to sorting by the integer value of the binary mask. Thus the rank order of subset sums matches the natural order of integers $k = 1, 2, 3, \dots$, and the binary representation of $k$ directly encodes the required subset.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def solve():
    n, k = map(int, input().split())

    ans = 0
    power = 1

    while k > 0:
        if k & 1:
            ans = (ans + power) % MOD
        power = (power * n) % MOD
        k >>= 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The code directly implements the binary decomposition idea. The variable `power` tracks $n^i$ as we scan bits of $k$. Each time we encounter a set bit, we add the corresponding power into the result. The modulo is applied at every step to avoid overflow.

A subtle implementation detail is that we never precompute all powers up to 30 or 31 explicitly. Instead, we build them iteratively, which is sufficient since $k \le 10^9$ implies at most 30 bits.

## Worked Examples

### Example 1: $n = 3, k = 3$

Binary of $k$ is `11`.

| Bit index | Bit value | Current power $3^i$ | Contribution | Running sum |
| --- | --- | --- | --- | --- |
| 0 | 1 | 1 | 1 | 1 |
| 1 | 1 | 3 | 3 | 4 |

Final answer is 4.

This matches the sequence: $1, 3, 4, 9, 10, \dots$, where the third term is 4.

### Example 2: $n = 3, k = 4$

Binary of $k$ is `100`.

| Bit index | Bit value | Current power $3^i$ | Contribution | Running sum |
| --- | --- | --- | --- | --- |
| 0 | 0 | 1 | 0 | 0 |
| 1 | 0 | 3 | 0 | 0 |
| 2 | 1 | 9 | 9 | 9 |

Final answer is 9.

This corresponds to selecting only $3^2$, which is the fourth smallest subset sum.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(\log k)$ | We process one bit of $k$, at most about 30 operations |
| Space | $O(1)$ | Only a few integer variables are maintained |

The solution is easily fast enough for $k \le 10^9$, since the number of iterations is bounded by the number of bits in $k$.

## Test Cases

```python
import sys, io

MOD = 10**9 + 7

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, k = map(int, sys.stdin.readline().split())

    ans = 0
    power = 1
    while k > 0:
        if k & 1:
            ans = (ans + power) % MOD
        power = (power * n) % MOD
        k >>= 1

    return str(ans)

# provided samples
assert run("3 3\n") == "4"
assert run("3 5\n") == "10"

# custom cases
assert run("2 1\n") == "1", "minimum k"
assert run("2 2\n") == "2", "single higher bit"
assert run("10 7\n") == str(1 + 10 + 100), "mixed binary structure"
assert run("3 1\n") == "1", "smallest non-empty subset"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 1 | 1 | smallest possible subset |
| 2 2 | 2 | single high-bit selection |
| 10 7 | 111 | multi-bit accumulation correctness |
| 3 1 | 1 | base case correctness |

## Edge Cases

One edge case is when $k$ is a power of two. For example, $k = 8$ corresponds to binary `1000`, meaning only $n^3$ is selected. The algorithm naturally handles this because only a single bit contributes, and all lower powers are ignored.

Another case is when all lower bits are set, such as $k = 7$ giving `111`. Here the sum becomes $1 + n + n^2$. The iterative accumulation correctly builds this without needing any special handling.

A final subtle case is large $n$. Since all arithmetic is modulo $10^9+7$, intermediate powers are safely reduced, and multiplication never overflows typical integer limits in Python, but modular reduction still keeps values bounded and consistent.
