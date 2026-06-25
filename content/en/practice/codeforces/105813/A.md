---
title: "CF 105813A - Thomas"
description: "We are asked to construct a large collection of binary strings of fixed length $n$, with a single restriction on how any two chosen strings may differ. Each string is made of zeros and ones."
date: "2026-06-25T23:42:55+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105813
codeforces_index: "A"
codeforces_contest_name: "Rutgers University Programming Contest Spring 2025"
rating: 0
weight: 105813
solve_time_s: 43
verified: true
draft: false
---

[CF 105813A - Thomas](https://codeforces.com/problemset/problem/105813/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to construct a large collection of binary strings of fixed length $n$, with a single restriction on how any two chosen strings may differ.

Each string is made of zeros and ones. The forbidden situation is when two different strings differ in exactly one position, meaning you can turn one into the other by flipping a single bit and nothing else. Equivalently, their Hamming distance must never be exactly 1.

The task is not to optimize a value or answer a query, but to explicitly output any largest possible set that satisfies this constraint.

The constraint $n \le 15$ suggests that the full space of $2^n$ strings is small enough to reason about structurally rather than simulate pairwise checking. A naive approach that compares all pairs of strings would involve about $2^n$ candidates and $O(2^{2n})$ pair checks, which is already borderline for $n=15$ because it means roughly a billion comparisons.

A subtle edge case appears when $n=1$. There are only two strings: "0" and "1", and they differ in exactly one position. This means we cannot take both, and any correct solution must output only one of them. A careless construction that assumes symmetry or parity patterns without checking this case may incorrectly output both strings.

For larger $n$, small examples clarify structure. For $n=2$, the optimal answer is $\{00, 11\}$. The pair $\{01, 10\}$ is equally valid, but mixing any of these pairs breaks the rule because 00 differs from 01 in one bit.

This hints that adjacency in the hypercube graph of binary strings is the real constraint: we are selecting a largest set of vertices with no edge inside the set.

## Approaches

The brute-force viewpoint is to treat each binary string as a node in an $n$-dimensional hypercube graph, where edges connect strings differing in exactly one bit. The problem becomes selecting the largest subset of vertices with no internal edge, which is the classic maximum independent set problem on this graph.

A direct brute-force would enumerate all subsets of vertices and check validity. With $2^n$ vertices, the number of subsets is $2^{2^n}$, which becomes completely infeasible even for $n=5$. Even restricting to checking pairwise conflicts inside a chosen subset leads to exponential explosion.

The key structural observation is that the hypercube is bipartite. Any binary string can be classified by the parity of its bit count. Flipping one bit always changes parity, so every edge connects a even-parity string to an odd-parity string. This splits the entire graph into two independent partitions where no edges exist inside a partition.

Once this is recognized, the maximum independent set is simply the larger of the two partitions, which in a hypercube are equal in size. Therefore either all even-parity strings or all odd-parity strings forms a valid optimal solution, and both have size $2^{n-1}$.

This reduces the task from a combinatorial search over subsets to a deterministic construction based on parity.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over subsets | $O(2^{2^n} \cdot n)$ | $O(2^n)$ | Too slow |
| Parity-based construction | $O(n 2^n)$ | $O(2^n)$ | Accepted |

## Algorithm Walkthrough

The optimal construction relies on grouping all binary strings by whether they contain an even or odd number of ones, then selecting one group entirely.

1. Iterate over all integers from 0 to $2^n - 1$. Each integer represents a binary string of length $n$. This encoding allows direct bit manipulation without string operations.
2. For each number, count how many bits are set to 1. This count determines whether the string belongs to the even or odd parity class.
3. Choose one parity class as the answer set. A natural choice is all strings with even parity, since it includes the all-zero string and keeps implementation simple.
4. For every number whose parity matches the chosen class, convert it into a binary string of length $n$ and store it.
5. Output the size of this set followed by all strings.

The non-obvious part is why parity is sufficient. The reason is that flipping a single bit always toggles parity, so any two strings inside the same parity class must differ in at least two positions. This guarantees the constraint is satisfied automatically without explicit checking.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())

    res = []
    for mask in range(1 << n):
        if bin(mask).count("1") % 2 == 0:
            res.append(mask)

    print(len(res))
    for mask in res:
        s = format(mask, f"0{n}b")
        print(s)

if __name__ == "__main__":
    solve()
```

The solution iterates over all bitmasks and filters them by parity. The conversion step uses fixed-width binary formatting to preserve leading zeros, which is necessary because shorter strings would be interpreted incorrectly.

One subtle implementation detail is that counting bits via `bin(mask).count("1")` is sufficient for $n \le 15$, but in higher constraints a faster builtin like `bit_count()` would be preferable. Here it is not performance-critical.

Another important detail is preserving string length exactly $n$, since omitting leading zeros would collapse distinct vertices into ambiguous representations.

## Worked Examples

For $n = 2$, we enumerate masks from 0 to 3.

| mask | binary | ones count | selected |
| --- | --- | --- | --- |
| 0 | 00 | 0 | yes |
| 1 | 01 | 1 | no |
| 2 | 10 | 1 | no |
| 3 | 11 | 2 | yes |

The output set is {00, 11}. This matches the known optimal solution, and no pair differs in exactly one position.

This trace shows that the algorithm does not consider adjacency explicitly. Instead, it relies entirely on parity separation.

For $n = 3$, masks 0 to 7 produce:

| mask | binary | ones count | selected |
| --- | --- | --- | --- |
| 0 | 000 | 0 | yes |
| 1 | 001 | 1 | no |
| 2 | 010 | 1 | no |
| 3 | 011 | 2 | yes |
| 4 | 100 | 1 | no |
| 5 | 101 | 2 | yes |
| 6 | 110 | 2 | yes |
| 7 | 111 | 3 | no |

The resulting set contains 4 strings, which equals $2^{3-1}$, confirming that we are selecting exactly half of the hypercube.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n 2^n)$ | We iterate over all $2^n$ masks and compute bit counts and conversions |
| Space | $O(2^n)$ | We store half of all binary strings in the output set |

The bound $n \le 15$ makes $2^n = 32768$, so the construction is trivial to execute within limits. Memory usage is also small since at most 16384 strings are stored.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque
    import sys as _sys

    n = int(input().strip())
    res = []
    for mask in range(1 << n):
        if bin(mask).count("1") % 2 == 0:
            res.append(format(mask, f"0{n}b"))
    out = str(len(res)) + "\n" + "\n".join(res) + "\n"
    return out

# provided samples
assert run("1\n") == "1\n0\n"
assert run("2\n") == "2\n00\n11\n"

# custom cases
assert run("3\n").splitlines()[0] == "4"
assert run("4\n").splitlines()[0] == "8"
assert run("1\n") in ["1\n0\n", "1\n1\n"]
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| n = 1 | single string | smallest edge case |
| n = 2 | 2 strings | basic structure correctness |
| n = 3 | 4 strings | scaling and parity balance |
| n = 4 | 8 strings | exponential growth pattern |

## Edge Cases

For $n = 1$, only two strings exist: "0" and "1". The parity construction selects only one of them since "1" has odd parity and "0" has even parity. The algorithm outputs exactly one string, matching the constraint that no pair can differ in exactly one position.

For $n = 2$, the full set splits cleanly into two partitions. The algorithm selects exactly {00, 11}. If a naive implementation attempted to greedily include strings without checking global structure, it could accidentally include 01 and 00 together, violating the rule since they differ by one bit.

For $n = 3$, adjacency becomes denser, but parity still guarantees separation. Every string in the chosen set differs from any other in at least two bit positions, which can be verified by direct comparison of representative pairs like 000 and 011.

The construction avoids all such pitfalls because it never reasons locally about pairs, only about global parity structure of the hypercube.
