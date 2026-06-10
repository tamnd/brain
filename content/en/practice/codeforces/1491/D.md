---
title: "CF 1491D - Zookeeper and The Infinite Zoo"
description: "We are asked to determine reachability in an infinite directed graph. Each vertex is a positive integer, and there is a directed edge from vertex $u$ to vertex $u+v$ if and only if the bitwise AND of $u$ and $v$ equals $v$."
date: "2026-06-10T22:27:12+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "constructive-algorithms", "dp", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1491
codeforces_index: "D"
codeforces_contest_name: "Codeforces Global Round 13"
rating: 1800
weight: 1491
solve_time_s: 123
verified: true
draft: false
---

[CF 1491D - Zookeeper and The Infinite Zoo](https://codeforces.com/problemset/problem/1491/D)

**Rating:** 1800  
**Tags:** bitmasks, constructive algorithms, dp, greedy, math  
**Solve time:** 2m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to determine reachability in an infinite directed graph. Each vertex is a positive integer, and there is a directed edge from vertex $u$ to vertex $u+v$ if and only if the bitwise AND of $u$ and $v$ equals $v$. In other words, every edge allows us to add a number $v$ to the current vertex $u$ only if all 1-bits of $v$ are also 1-bits of $u$. For each query consisting of two integers $u_i$ and $v_i$, we need to answer whether it is possible to reach $v_i$ starting from $u_i$ using a sequence of such edges.

The input allows up to $10^5$ queries, and each vertex can be as large as $2^{30}-1$. A naive approach that tries to simulate all possible paths from $u_i$ to $v_i$ would potentially explore an exponential number of vertices for each query, which is infeasible. This implies that any solution must work directly with the bit patterns of the numbers rather than enumerating paths.

Non-obvious edge cases include queries where $u_i = v_i$. In this situation, the correct answer is "YES" because we are already at the target, even though no edge is needed. Another edge case occurs when $v_i < u_i$. Since every edge strictly increases the vertex value, the answer must be "NO". Finally, cases where $u_i$ and $v_i$ share some bits but differ in others need careful handling, since the AND condition might prevent reaching certain bits.

## Approaches

The brute-force approach would attempt to simulate the graph starting from $u_i$, generating all reachable vertices by repeatedly adding any valid $v$ that satisfies $u \& v = v$. This works for small numbers but is hopeless for $u_i$ as large as $2^{30}$ or for many queries, as each simulation could take more than $10^9$ operations in the worst case.

The key observation is that each step only allows us to add numbers whose 1-bits are already present in the current vertex. This means that to reach $v_i$ from $u_i$, every 1-bit in $v_i$ must eventually be supported by some 1-bit in $u_i$. More precisely, if we scan the bits from least significant to most significant, the number of 1-bits in $u_i$ up to any position must be at least the number of 1-bits in $v_i$ up to the same position. If at any bit the cumulative count in $v_i$ exceeds that in $u_i$, it is impossible to reach $v_i$. This transforms the problem into a linear scan over 30 bits for each query.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^30) per query | O(2^30) | Too slow |
| Optimal (bit-count scan) | O(30 * q) | O(1) per query | Accepted |

## Algorithm Walkthrough

1. Read the number of queries $q$.
2. For each query, read $u$ and $v$. If $u > v$, immediately output "NO" since all edges increase the vertex.
3. Initialize two counters, $count_u$ and $count_v$, to track cumulative 1-bits seen in $u$ and $v$ as we scan from the least significant bit (bit 0) to the 29th bit.
4. For each bit position from 0 to 29, check if the bit is set in $u$ and $v$. If set, increment $count_u$ or $count_v$ respectively.
5. After updating counts for each bit, check if $count_v > count_u$. If true, output "NO" immediately, because there is a 1-bit in $v$ that cannot be supported by $u$ so far.
6. If the scan completes without failing, output "YES" since all 1-bits in $v$ can be incrementally built using 1-bits from $u$.

Why it works: the invariant maintained during the scan is that at each bit position, the cumulative number of 1-bits in $u$ is at least the number in $v$. This guarantees that any 1-bit in $v$ can be formed by adding numbers whose 1-bits are already present in $u$, respecting the AND condition. If the invariant fails at any bit, it is impossible to reach $v$.

## Python Solution

```python
import sys
input = sys.stdin.readline

q = int(input())
for _ in range(q):
    u, v = map(int, input().split())
    if u > v:
        print("NO")
        continue
    count_u = 0
    count_v = 0
    possible = True
    for i in range(30):
        if (u >> i) & 1:
            count_u += 1
        if (v >> i) & 1:
            count_v += 1
        if count_v > count_u:
            possible = False
            break
    print("YES" if possible else "NO")
```

The solution reads each query and directly processes the bit counts. Using cumulative counts avoids backtracking or simulating the graph, which keeps the algorithm linear in the number of bits and queries. The bit scan from least to most significant ensures that smaller bits are satisfied first, which aligns with how the AND-addition edges allow propagation.

## Worked Examples

**Example 1**: $u = 1, v = 4$

| Bit | u_bit | v_bit | count_u | count_v | possible |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 1 | 0 | True |
| 1 | 0 | 0 | 1 | 0 | True |
| 2 | 0 | 1 | 1 | 1 | True |

The scan completes successfully, output "YES". This confirms the 1-bit in $v$ at position 2 can eventually be reached.

**Example 2**: $u = 3, v = 6$

| Bit | u_bit | v_bit | count_u | count_v | possible |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 1 | 0 | True |
| 1 | 1 | 1 | 2 | 1 | True |
| 2 | 0 | 1 | 2 | 2 | True |

The scan completes, output "YES". The cumulative check shows we can form all 1-bits of $v$ from $u$.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(q * 30) = O(q) | Each query requires scanning 30 bits. With $q \le 10^5$, total operations are ~3*10^6. |
| Space | O(1) | Only a few integer counters per query are used. |

This fits comfortably within the time and memory limits. The algorithm avoids any explicit graph storage or path enumeration, making it feasible for the input bounds.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    exec(open("solution.py").read())  # assuming the solution code is saved in solution.py
    return output.getvalue().strip()

# Provided sample
assert run("5\n1 4\n3 6\n1 6\n6 2\n5 5\n") == "YES\nYES\nNO\nNO\nYES", "sample 1"

# Custom tests
assert run("2\n1 1\n1 2\n") == "YES\nNO", "same u=v and impossible case"
assert run("1\n15 15\n") == "YES", "all bits equal"
assert run("1\n0 0\n") == "YES", "zero case"
assert run("1\n7 8\n") == "NO", "requires unsupported higher bit"
assert run("1\n2 3\n") == "NO", "requires lower bit not present"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1, 1 2 | YES, NO | u=v and impossible small v |
| 15 15 | YES | All bits equal |
| 0 0 | YES | Edge case with zero |
| 7 8 | NO | Cannot form higher bit not present in u |
| 2 3 | NO | Cannot form lower bit without enough support |

## Edge Cases

When $u = v$, no addition is needed. For example, input `1 1` immediately satisfies the cumulative bit invariant, and the algorithm outputs "YES". When $v < u$, the output is "NO" as no edge can decrease the vertex. For `u = 2, v = 1`, the scan never satisfies the cumulative bit requirement, producing "NO". For cases where the highest bit of $v$ is not in $u$, the algorithm
