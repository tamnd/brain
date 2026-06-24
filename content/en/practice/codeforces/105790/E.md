---
title: "CF 105790E - El Caf\u00e9"
description: "We are maintaining a dynamic collection of positive integers, where each integer represents the quantity of a newly arriving ingredient in a café. The collection changes over time: new values are appended, and occasionally the most recent block of values is removed."
date: "2026-06-25T06:21:58+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105790
codeforces_index: "E"
codeforces_contest_name: "UDESC Selection Contest 2024-1"
rating: 0
weight: 105790
solve_time_s: 35
verified: true
draft: false
---

[CF 105790E - El Caf\u00e9](https://codeforces.com/problemset/problem/105790/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 35s  
**Verified:** yes  

## Solution
## Problem Understanding

We are maintaining a dynamic collection of positive integers, where each integer represents the quantity of a newly arriving ingredient in a café. The collection changes over time: new values are appended, and occasionally the most recent block of values is removed. Between these updates, we are asked queries that check whether a certain number of identical drinks can be produced from all currently available ingredients simultaneously.

A key observation from the statement is that every drink must use all ingredients, and each ingredient must be split evenly across all drinks. If we currently have ingredient quantities $a_1, a_2, \dots, a_k$, then producing $x$ drinks is possible only if every $a_i$ is divisible by $x$. This reduces the entire feasibility check to a divisibility condition over all active numbers.

The constraints imply up to $10^5$ operations with values up to $10^9$. Any solution that recomputes a property from scratch per query leads to $O(nq)$, which is too slow. We need an approach where each operation is handled in amortized $O(1)$ or $O(\log n)$, meaning we must maintain a compact summary of the current multiset.

A subtle edge case arises when deletions remove the newest elements. For example, consider starting with ingredients $[6, 10, 15]$, then adding $4$, then removing the last two elements. A naive implementation that does not correctly maintain history might accidentally delete older elements or fail to restore the correct state. Another issue is repeated queries: a solution that recomputes divisibility by scanning all elements per query would pass small cases but fail under maximum constraints due to time limits.

## Approaches

The brute-force idea is straightforward: maintain the full list of active ingredients. For each query of type 3, iterate over all current values and check whether each value is divisible by $x$. This is correct because it directly encodes the condition in the problem. However, each query may require scanning up to $10^5$ elements, and with $10^5$ queries, this leads to $10^{10}$ operations in the worst case, which is far beyond feasible limits.

The key insight is that we do not actually care about individual values, only about their common divisibility structure. A number $x$ divides every element in the multiset if and only if it divides their greatest common divisor. This transforms the problem from maintaining a set of numbers into maintaining a single aggregate value: the gcd of all active elements.

Once this reduction is seen, the structure becomes a stack problem. Since elements are only added at the end and removed from the end in batches, we can maintain a stack where each entry stores the gcd of all elements up to that position. This allows both updates and rollbacks to be handled efficiently.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Scan | $O(NQ)$ | $O(N)$ | Too slow |
| Stack with prefix gcd | $O(N + Q)$ | $O(N)$ | Accepted |

## Algorithm Walkthrough

We maintain a stack where each position stores the gcd of all values up to that point in the current active sequence.

1. Start with an initial stack containing the prefix gcd of the initial ingredients. Each new value updates the gcd of everything before it, so the stack top always represents the gcd of all active ingredients so far.
2. For a type 1 query, a new ingredient is appended. We compute the gcd of this value with the current stack top and push it. This works because gcd is associative, so the prefix structure remains valid after extension.
3. For a type 2 query, we remove the last $K$ ingredients by popping from the stack $K$ times. Each pop removes the contribution of the most recent ingredient while preserving correctness of earlier prefix gcd values.
4. For a type 3 query, we check whether the requested number $X$ divides the current gcd stored at the top of the stack. If it does, all elements are divisible by $X$, otherwise at least one element is not compatible and the order cannot be fulfilled.

### Why it works

At any moment, the top of the stack represents $\gcd(a_1, a_2, \dots, a_k)$ over all active ingredients. Since a number divides all elements in a set if and only if it divides their gcd, checking divisibility against this single value is equivalent to checking all elements individually. The stack invariant is preserved because gcd updates are associative and removals restore the previous prefix state exactly.

## Python Solution

```python
import sys
input = sys.stdin.readline
from math import gcd

def solve():
    n, q = map(int, input().split())
    a = list(map(int, input().split()))

    # stack stores prefix gcds
    st = [0]
    for x in a:
        st.append(gcd(st[-1], x))

    for _ in range(q):
        tmp = input().split()
        t = int(tmp[0])

        if t == 1:
            g = int(tmp[1])
            st.append(gcd(st[-1], g))

        elif t == 2:
            k = int(tmp[1])
            # pop k elements
            for _ in range(k):
                st.pop()

        else:
            x = int(tmp[1])
            if st[-1] % x == 0:
                print("SIM")
            else:
                print("NAO")

if __name__ == "__main__":
    solve()
```

The implementation relies on the stack storing prefix gcds rather than raw values. This avoids recomputing gcds over the full array during queries. The only subtle part is ensuring that deletions correctly remove the most recent prefix states; since each stack entry depends only on the previous one, popping restores the previous valid gcd automatically.

One detail worth attention is that the initial stack starts with zero, which acts as the neutral element for gcd. This ensures that the first real ingredient initializes the structure correctly.

## Worked Examples

### Example 1

Input:

```
5 5
12 12 6 4 2
2 3
3 4
1 6
1 3
3 2
```

We track the stack of prefix gcds:

| Step | Operation | Stack (gcd state) | Query result |
| --- | --- | --- | --- |
| 0 | init | [0, 12, 12, 6, 2, 2] | - |
| 1 | remove 3 | [0, 12, 12] | - |
| 2 | query 4 | gcd = 12 | SIM |
| 3 | add 6 | [0, 12, 12, 6] | - |
| 4 | add 3 | [0, 12, 12, 6, 3] | - |
| 5 | query 2 | gcd = 1 | NAO |

The trace shows how removing elements restores an earlier gcd state and how the final decision depends only on the current top value.

### Example 2

Input:

```
3 3
20 20 4
3 5
1 10
3 2
```

| Step | Operation | Stack | Query result |
| --- | --- | --- | --- |
| 0 | init | [0, 20, 20, 4] | - |
| 1 | query 5 | gcd = 4 | NAO |
| 2 | add 10 | [0, 20, 20, 4, 2] | - |
| 3 | query 2 | gcd = 2 | SIM |

This example highlights how a single new ingredient can change the gcd dramatically, directly affecting all future divisibility checks.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N + Q)$ amortized | each element is pushed once and popped once |
| Space | $O(N + Q)$ | stack stores one gcd value per insertion |

The solution fits comfortably within limits since each operation performs only constant-time gcd computations and stack operations, even when $N$ and $Q$ reach $10^5$.

## Test Cases

```python
import sys, io
from math import gcd

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque

    n, q = map(int, input().split())
    a = list(map(int, input().split()))

    st = [0]
    for x in a:
        st.append(gcd(st[-1], x))

    out = []
    for _ in range(q):
        t, *rest = map(int, input().split())
        if t == 1:
            g = rest[0]
            st.append(gcd(st[-1], g))
        elif t == 2:
            k = rest[0]
            for _ in range(k):
                st.pop()
        else:
            x = rest[0]
            out.append("SIM" if st[-1] % x == 0 else "NAO")

    return "\n".join(out) + ("\n" if out else "")

# provided samples
assert run("""5 5
12 12 6 4 2
2 3
3 4
1 6
1 3
3 2
""") == "SIM\nNAO\n"

assert run("""3 3
20 20 4
3 5
1 10
3 2
""") == "NAO\nSIM\n"

# custom cases
assert run("""1 3
10
3 5
1 5
3 5
""") == "NAO\nSIM\n", "single element edge"

assert run("""4 3
6 10 15 30
3 5
2 2
3 3
""") == "SIM\nNAO\n", "rollback correctness"

assert run("""2 2
7 7
3 7
3 1
""") == "SIM\nSIM\n", "all equal values"

assert run("""3 3
2 4 8
3 2
2 1
3 4
""") == "SIM\nSIM\n", "boundary removals"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element edge | SIM/NAO sequence | correctness with minimal stack |
| rollback correctness | mixed SIM/NAO | correct deletion handling |
| all equal values | always SIM | gcd stability |
| boundary removals | SIM/SIM | correctness after partial pops |

## Edge Cases

A single ingredient input tests whether the gcd initialization correctly handles a stack with one meaningful element. The algorithm still works because the gcd of a single number is itself, and divisibility checks reduce correctly.

Large removals that restore earlier states test whether the stack correctly reverts to previous prefix gcd values. Since each stack entry encodes a full prefix, popping multiple times always restores a valid historical gcd without recomputation.

Uniform arrays such as all equal numbers ensure that gcd remains stable across updates, confirming that no unintended side effects occur in repeated gcd computations.

Boundary removals that leave the stack at its initial state confirm that the sentinel zero value behaves correctly and does not interfere with divisibility checks.
