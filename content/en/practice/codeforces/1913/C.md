---
title: "CF 1913C - Game with Multiset"
description: "We are maintaining a dynamic collection of powers of two. Each time we receive an ADD operation, we insert a value of the form $2^x$ into the multiset."
date: "2026-06-08T20:07:41+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "bitmasks", "brute-force", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1913
codeforces_index: "C"
codeforces_contest_name: "Educational Codeforces Round 160 (Rated for Div. 2)"
rating: 1300
weight: 1913
solve_time_s: 87
verified: true
draft: false
---

[CF 1913C - Game with Multiset](https://codeforces.com/problemset/problem/1913/C)

**Rating:** 1300  
**Tags:** binary search, bitmasks, brute force, greedy  
**Solve time:** 1m 27s  
**Verified:** yes  

## Solution
## Problem Understanding

We are maintaining a dynamic collection of powers of two. Each time we receive an ADD operation, we insert a value of the form $2^x$ into the multiset. Each GET operation asks a reachability question: can we pick some subset of the currently available numbers whose sum equals a target $w$.

The key feature is that every element is a pure power of two, and duplicates are allowed because the multiset can contain repeated inserts of the same power. That turns the structure into something close to a binary representation system, but with the twist that we may have multiple “coins” of the same value.

The constraints force us to process up to $10^5$ operations online. Each GET query may involve a target up to $10^9$, so we cannot try all subsets or even do per-query exponential reasoning. Any solution that tries to enumerate subsets or run a knapsack-style DP per query will immediately fail, since $2^{30}$ subset combinations per query is already far beyond the limit.

A subtle issue appears when multiple identical powers accumulate. For example, if we insert three $2^0$ elements, we can form sums like 1, 2, or 3 using only those ones. A naive approach that treats each power independently without considering counts will fail here. The correct interpretation is that each exponent behaves like a bounded number of identical coins, and carries between bits become possible.

Another failure case is treating each GET independently with a fresh greedy decomposition but forgetting that previous ADD operations accumulate state. Since the multiset evolves, recomputing from scratch per query would also be too slow.

## Approaches

The brute-force interpretation is straightforward: for each GET query, consider all subsets of the multiset and check whether any subset sums to $w$. If there are $k$ elements currently in the multiset, this requires checking $2^k$ subsets, which grows exponentially. Even for $k = 40$, this becomes infeasible, and here $k$ can reach $10^5$.

A second naive improvement is to maintain all subset sums via a dynamic programming set. After each ADD, we merge new sums by adding the new power to all existing sums. This still doubles the number of reachable sums per insert in the worst case, leading again to exponential growth.

The key observation is that all values are powers of two. That means every number contributes to exactly one binary position, and combining them behaves like binary addition with possible carries. Instead of tracking subsets, we only need to track how many copies of each exponent exist.

Let $c[i]$ be the number of elements equal to $2^i$. To answer whether we can form $w$, we try to interpret $w$ in binary and greedily match bits from lowest to highest, using available counts and carrying surplus upward. This reduces the problem to a bounded coin system on binary weights, where greedy carry propagation is valid because each weight is exactly double the previous one.

This transforms each GET query into a small loop over at most 31 bits.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^n)$ per query | $O(n)$ | Too slow |
| Optimal | $O(30)$ per query | $O(30)$ | Accepted |

## Algorithm Walkthrough

We maintain an array `cnt` where `cnt[i]` stores how many times $2^i$ has been inserted.

1. For an ADD $x$, increment `cnt[x]` by one. This directly records the availability of that power.
2. For a GET $w$, simulate building $w$ bit by bit from lowest power to highest.
3. For each bit position $i$, compute whether we currently need a unit of $2^i$ from $w$.
4. Add available coins `cnt[i]` to a running “supply” at that level. This supply represents how many units of $2^i$ we can use.
5. If the current bit of $w$ is 1, we must consume one unit of $2^i$. If supply is zero, the answer is immediately NO because we cannot satisfy this bit.
6. After satisfying the requirement, any remaining supply at level $i$ is carried upward as $2^{i+1}$, since two $2^i$ can form one $2^{i+1}$.
7. Continue this process up to the maximum bit of $w$, and finally check whether leftover carry is irrelevant or can be absorbed.

The key idea is that we never discard excess; everything propagates upward exactly like binary addition with resource pooling.

### Why it works

At every bit position $i$, all contributions to that value are indistinguishable: they are all $2^i$. Any pairing or leftover naturally converts into the next bit because $2 \cdot 2^i = 2^{i+1}$. This enforces a strict hierarchy where decisions at lower bits fully determine feasibility without backtracking. The greedy consumption at each bit is safe because failing to satisfy a required bit cannot be fixed by higher bits, while surplus is always optimally reusable via carries.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    m = int(input())
    cnt = [0] * 31

    for _ in range(m):
        t, v = map(int, input().split())

        if t == 1:
            cnt[v] += 1
        else:
            w = v
            carry = 0
            ok = True

            for i in range(31):
                carry += cnt[i]

                if (w >> i) & 1:
                    if carry == 0:
                        ok = False
                        break
                    carry -= 1

                carry //= 2

            if ok:
                print("YES")
            else:
                print("NO")

if __name__ == "__main__":
    solve()
```

The implementation keeps a fixed frequency array of size 31, since $2^{30}$ is enough to cover all values up to $10^9$. Each GET query simulates binary construction of the target using a running carry.

The critical detail is processing bits in increasing order. The carry must always be divided by two after each level to reflect aggregation into the next power of two. Failing to apply this division correctly leads to overcounting resources at higher levels.

## Worked Examples

### Example 1

Input:

```
5
1 0
1 0
1 0
2 3
2 4
```

State evolution:

| Step | Operation | cnt[0] | carry | bit processed | result |
| --- | --- | --- | --- | --- | --- |
| 1 | add 0 | 1 | - | - | - |
| 2 | add 0 | 2 | - | - | - |
| 3 | add 0 | 3 | - | - | - |
| 4 | get 3 | 3 | 3→1→0 | bits 0,1 | YES |
| 5 | get 4 | 3 | insufficient at bit 2 | - | NO |

The first GET succeeds because three ones can form binary 3. The second fails because there is no way to produce a $2^2$ unit.

### Example 2

Input:

```
4
1 1
1 2
2 6
2 7
```

| Step | Operation | cnt[1] | cnt[2] | carry | result |
| --- | --- | --- | --- | --- | --- |
| 1 | add 1 | 1 | 0 | - | - |
| 2 | add 2 | 1 | 1 | - | - |
| 3 | get 6 | 1 | 1 | sufficient | YES |
| 4 | get 7 | 1 | 1 | insufficient | NO |

This demonstrates how combining different powers requires correct carry propagation rather than independent bit checks.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(30m)$ | Each query processes at most 31 bit positions |
| Space | $O(30)$ | Fixed array for exponent counts |

The total work is about $3 \times 10^6$ operations, which is well within limits for $10^5$ queries.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    m = int(input())
    cnt = [0] * 31
    out = []

    for _ in range(m):
        t, v = map(int, input().split())
        if t == 1:
            cnt[v] += 1
        else:
            w = v
            carry = 0
            ok = True
            for i in range(31):
                carry += cnt[i]
                if (w >> i) & 1:
                    if carry == 0:
                        ok = False
                        break
                    carry -= 1
                carry //= 2
            out.append("YES" if ok else "NO")

    return "\n".join(out)

# provided sample
assert run("""5
1 0
1 0
1 0
2 3
2 4
""") == "YES\nNO"

# all equal small powers
assert run("""3
1 2
1 2
2 4
""") == "YES"

# impossible high bit
assert run("""2
1 0
2 2
""") == "NO"

# direct match
assert run("""2
1 5
2 32
""") == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| three 1s forming 3 | YES | basic carry formation |
| two 4s forming 8 | YES | higher-bit carry |
| single 1 cannot form 2 | NO | impossibility |
| single 2^5 query | YES | direct match |

## Edge Cases

One edge case occurs when many small powers accumulate and must cascade through multiple carries. For example, inserting eight copies of $2^0$ should immediately behave like a single $2^3$. The algorithm handles this because each level performs integer division by two, propagating surplus upward repeatedly until stabilization.

Another case is when GET queries request a value larger than any single stored exponent. Even if no single matching power exists, combinations may still work. For instance, two $2^3$ entries can satisfy $2^4$. The carry mechanism ensures that these merges are always accounted for before evaluating higher bits, so the algorithm never falsely rejects valid constructions.
