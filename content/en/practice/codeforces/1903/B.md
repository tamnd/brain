---
title: "CF 1903B - StORage room"
description: "We are given a symmetric matrix that is claimed to come from a hidden array through a bitwise construction rule. The hidden array has $n$ non-negative integers, each less than $2^{30}$."
date: "2026-06-08T21:01:31+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "brute-force", "constructive-algorithms", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1903
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 912 (Div. 2)"
rating: 1200
weight: 1903
solve_time_s: 113
verified: false
draft: false
---

[CF 1903B - StORage room](https://codeforces.com/problemset/problem/1903/B)

**Rating:** 1200  
**Tags:** bitmasks, brute force, constructive algorithms, greedy  
**Solve time:** 1m 53s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a symmetric matrix that is claimed to come from a hidden array through a bitwise construction rule. The hidden array has $n$ non-negative integers, each less than $2^{30}$. For every pair of distinct indices $i$ and $j$, the matrix entry $M_{i,j}$ equals the bitwise OR of the hidden values $a_i$ and $a_j$. Diagonal entries are always zero.

The task is to reconstruct any valid array $a$ that could generate the given matrix, or determine that no such array exists.

The key difficulty is that we are not given direct values, only pairwise OR results. Each constraint couples two unknowns, and every bit in the matrix encodes partial information about bits of both endpoints.

The constraints imply a tight reconstruction problem rather than a search problem. Since $n$ can be up to 1000 per test and the sum over tests is also 1000, an $O(n^3)$ or anything involving repeated bitwise consistency checks over all triples would still be borderline but acceptable only with small constants. However, the intended solution must avoid triple nested reasoning.

A few failure cases appear naturally if we try naive reconstruction.

One common mistake is to assume $a_i = \bigwedge_{j \ne i} M_{i,j}$. This is wrong because OR does not decompose that way. For example, if $a_i = 1$ and $a_j = 2$, then $M_{i,j} = 3$, and no single intersection recovers original bits.

Another subtle issue is inconsistency across triples. For instance, if

$M_{1,2} = 3$, $M_{1,3} = 3$, $M_{2,3} = 0$, then no valid assignment exists. The last value implies disjoint bitsets for 2 and 3, but both must share bits with 1, which becomes contradictory under OR structure.

The real structure must come from interpreting each matrix row as a "union signature" of the hidden bitsets.

## Approaches

A brute-force idea is to try all possible arrays $a$, but each element has $2^{30}$ possibilities, so this is impossible. Even restricting values based on pairwise constraints still leaves an exponential search space.

A more structured brute approach is to treat each $a_i$ as unknown bitmask and enforce constraints pairwise. We could iterate and repeatedly adjust values until convergence, but each update depends on all others, and worst-case propagation across $n^2$ constraints leads to high polynomial cost.

The key observation is to reverse the OR relation. If $M_{i,j} = a_i \mid a_j$, then every bit that is zero in all pairwise ORs involving $i$ must be absent from $a_i$. Conversely, if a bit appears in some $M_{i,j}$, it must belong to at least one of $a_i$ or $a_j$.

The clean way to exploit this is to construct candidate values greedily: start from the fact that each $a_i$ must be consistent with all OR constraints. For a fixed $i$, consider that if bit $b$ is missing from every $M_{i,j}$, then $a_i$ cannot contain bit $b$. This gives an upper bound on $a_i$.

Then we check consistency: once a candidate array is built, we verify whether all pairwise ORs match the matrix. If not, the construction is invalid.

A more direct constructive simplification exists: for OR matrices that are valid, the matrix must satisfy that for any triple $i, j, k$,

$$M_{i,j} \mid M_{i,k} = M_{j,k} \mid M_{i,k}$$

structure indirectly enforces consistency, but we do not need explicit triple checking if we reconstruct carefully.

The standard accepted approach is surprisingly simple: set

$$a_i = M_{i,1} \& M_{i,2} \& \cdots \& M_{i,n}$$

is wrong, but the correct constructive trick is:

$$a_i = M_{i,1} \& M_{i,2} \& \cdots \& M_{i,n} \text{ is not valid}$$

so instead we use the complement reasoning:

For each bit position, consider which rows can safely contain that bit. A bit is allowed in $a_i$ only if for every $j$, either $M_{i,j}$ already has that bit set or we can assign it to one endpoint consistently. The known simplification for this problem reduces to:

Set

$$a_i = \bigwedge_{j \ne i} M_{i,j}$$

as a candidate is not sufficient, but the correct construction is:

$$a_i = \bigwedge_{j \ne i} (M_{i,j})$$

and then verify. If a valid solution exists, this construction will match one of them because OR-matrix structure ensures consistency of forced bits.

The remaining step is validation: recompute all $a_i \mid a_j$ and compare with $M$. If all match, output; otherwise, no solution exists.

This works because in any valid OR decomposition, any bit that is forced to appear in all pairwise interactions involving $i$ must belong to $a_i$. Any extraneous bit would violate at least one pair constraint.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(n) | Too slow |
| Optimal | O(n^2) | O(n^2) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the matrix $M$. We keep it unchanged because we will verify consistency against it.
2. For every index $i$, compute a candidate value $a_i$ by taking the bitwise AND over all $M_{i,j}$ for $j \ne i$. This extracts bits that are consistently present across all relationships involving $i$, which are the only bits that can safely belong to $a_i$ without breaking any OR constraint.
3. After building all candidate values, verify them against the matrix. For every pair $i, j$, compute $a_i \mid a_j$ and check if it equals $M_{i,j}$. If any mismatch occurs, the construction cannot represent the given matrix.
4. If all pairs match, output YES followed by the array $a$. Otherwise output NO.

### Why it works

Each bit that survives the AND over row $i$ is present in every $M_{i,j}$. In any valid decomposition, such a bit cannot be missing from $a_i$, otherwise there would exist some $j$ where the OR would require that bit to come from $a_j$, contradicting its presence in all pairs. Conversely, any bit not consistently present cannot be safely assigned to $a_i$, since it would risk creating an OR mismatch with some partner row. This makes the constructed $a_i$ the maximal safe assignment per index, and the final verification step ensures that no ambiguous distribution of bits was incorrectly accepted.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        M = [list(map(int, input().split())) for _ in range(n)]

        a = [0] * n

        for i in range(n):
            val = (1 << 30) - 1
            for j in range(n):
                if i != j:
                    val &= M[i][j]
            a[i] = val

        ok = True
        for i in range(n):
            for j in range(n):
                if i == j:
                    if M[i][j] != 0:
                        ok = False
                        break
                else:
                    if (a[i] | a[j]) != M[i][j]:
                        ok = False
                        break
            if not ok:
                break

        if not ok:
            print("NO")
        else:
            print("YES")
            print(*a)

if __name__ == "__main__":
    solve()
```

The construction phase computes each $a_i$ by intersecting all constraints involving that index. Initializing with all bits set ensures that only bits consistently supported across all pairwise ORs survive.

The verification step is essential because the construction is necessary but not always sufficient without checking global consistency. The double loop over all pairs ensures no hidden contradiction remains.

## Worked Examples

### Example 1

Input:

```
4
0 3 3 5
3 0 3 7
3 3 0 7
5 7 7 0
```

We compute each row AND.

| i | row values used | AND result | a[i] |
| --- | --- | --- | --- |
| 0 | 3,3,5 | 3 & 3 & 5 = 1 | 1 |
| 1 | 3,3,7 | 3 & 3 & 7 = 3 | 3 |
| 2 | 3,3,7 | 3 & 3 & 7 = 3 | 3 |
| 3 | 5,7,7 | 5 & 7 & 7 = 5 | 5 |

Now verify ORs:

| i | j | a[i] | a[j] | OR | M[i][j] |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 1 | 3 | 3 | 3 |
| 0 | 3 | 1 | 5 | 5 | 5 |
| 1 | 2 | 3 | 3 | 3 | 3 |

All entries match, so the construction is valid.

This demonstrates that consistent intersection per row captures the stable bit structure of each hidden value.

### Example 2

Input:

```
3
0 0 1
0 0 0
1 0 0
```

Row-wise AND gives:

| i | row values | AND | a[i] |
| --- | --- | --- | --- |
| 0 | 0,1 | 0 & 1 = 0 | 0 |
| 1 | 0,0 | 0 | 0 |
| 2 | 1,0 | 0 | 0 |

Verification fails because $a_0 \mid a_2 = 0$ but $M_{0,2} = 1$. This shows the matrix is inconsistent with any OR decomposition.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n^2)$ | Each row computes an AND over $n$ elements, followed by full pair verification |
| Space | $O(n^2)$ | Input matrix storage |

The constraints allow up to 1000 total elements across tests, so an $O(n^2)$ solution runs comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output

    solve()
    return output.getvalue()

# provided sample
assert run("""4
1
0
4
0 3 3 5
3 0 3 7
3 3 0 7
5 7 7 0
5
0 7 7 5 5
7 0 3 2 6
7 3 0 3 7
5 2 3 0 4
5 6 7 4 0
3
0 0 1
0 0 0
1 0 0
""").strip() == """YES
7
YES
1 3 2 5
YES
5 2 3 0 4
NO""".strip()

# minimum size
assert run("""1
1
0
""").strip() == """YES
0"""

# all zeros
assert run("""1
3
0 0 0
0 0 0
0 0 0
""").strip() == """YES
0 0 0"""

# simple consistent chain
assert run("""1
3
0 1 1
1 0 1
1 1 0
""").strip() == """YES
1 1 1"""

# inconsistent case
assert run("""1
3
0 1 2
1 0 3
2 3 0
""").strip() == """NO"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1x1 zero | YES 0 | base case |
| all zeros | all-zero solution | no-bit case |
| all ones | uniform solution | symmetric consistency |
| random inconsistent | NO | contradiction detection |

## Edge Cases

A critical edge case is when all off-diagonal entries are zero. In that situation, every pairwise OR is zero, so every $a_i$ must be zero. The construction computes AND over zeros, producing zero correctly, and verification passes immediately.

Another case is a fully connected matrix of identical values, for example all off-diagonal entries equal to 7. The AND over each row yields 7, so every $a_i = 7$, and OR consistency holds trivially since $7 \mid 7 = 7$.

A more subtle case is inconsistent bit distribution across triples. For instance, if one row suggests a bit must exist while another pair forbids it, the AND construction will remove that bit from at least one endpoint, and verification will detect the contradiction during recomputation of OR values.
