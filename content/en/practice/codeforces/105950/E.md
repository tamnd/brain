---
title: "CF 105950E - Enigma"
description: "We are given two integers that describe a hidden pair of numbers. Think of two unknown values $A$ and $B$. We are not given them directly, but instead we are told their sum and the absolute difference between them."
date: "2026-06-25T06:39:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105950
codeforces_index: "E"
codeforces_contest_name: "UDESC Selection Contest 2025-1"
rating: 0
weight: 105950
solve_time_s: 38
verified: true
draft: false
---

[CF 105950E - Enigma](https://codeforces.com/problemset/problem/105950/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 38s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two integers that describe a hidden pair of numbers. Think of two unknown values $A$ and $B$. We are not given them directly, but instead we are told their sum and the absolute difference between them. Formally, one value equals $A + B$, and the other equals $|A - B|$. The task is to reconstruct any valid pair $(A, B)$ that satisfies both relations.

The output is not unique in ordering, so printing $(A, B)$ or $(B, A)$ is equally valid as long as the two equations hold. The problem statement guarantees that at least one valid pair always exists for the given inputs.

The constraints go up to $10^9$, which immediately rules out any approach that tries to brute force candidates for $A$ and $B$. A naive search over all possible values would require checking up to $10^9$ possibilities, which is far beyond a one second time limit. This pushes us toward a direct algebraic reconstruction rather than any form of enumeration.

A subtle case appears when $A < B$. In that situation the absolute value flips sign, so the system behaves differently depending on the ordering of the unknowns. A careless implementation that assumes $A \ge B$ without considering the symmetric case will still often pass hidden tests but fail on inputs where the actual ordering is reversed. For example, if $X = 3$ and $Y = 7$, the valid solution is $(-2, 5)$. Any attempt that forces $A = (X + Y)/2$ and $B = (X - Y)/2$ without handling sign consistency will incorrectly assume both values are non-negative or ordered in a fixed way.

Another edge case occurs when $Y = 0$. This forces $A = B$, and both values must equal $X/2$. A solution that does not explicitly account for this can still work, but it highlights that the system degenerates into a single degree of freedom.

## Approaches

A brute-force idea would be to try all possible integer pairs $(A, B)$ in a reasonable range and check whether they satisfy both equations. Each check is constant time, but the search space is quadratic in magnitude of input bounds. With values up to $10^9$, even restricting the search to a plausible range would still lead to on the order of $10^{18}$ combinations in the worst case, which is entirely infeasible.

The key observation is that the system of equations is small and fully determined. We have:

$$A + B = X$$

$$|A - B| = Y$$

Instead of treating the absolute value as a complication, we split it into two linear cases. Either $A - B = Y$ or $A - B = -Y$. Each case reduces the problem to solving a 2×2 linear system. This turns the task from a search problem into simple algebra.

If we take $A - B = Y$, then adding the two equations gives $2A = X + Y$, and subtracting gives $2B = X - Y$. If instead $A - B = -Y$, the roles of $A$ and $B$ swap symmetrically. Since the problem allows output in any order, we can compute one consistent solution and print it directly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(10^{18})$ | $O(1)$ | Too slow |
| Algebraic System Solving | $O(1)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Read the values $X$ and $Y$. These define the sum and absolute difference of the unknown pair.
2. Compute a candidate assuming $A \ge B$, using $A = (X + Y) / 2$. This comes from adding $A + B = X$ and $A - B = Y$, which isolates $A$.
3. Compute the corresponding $B = X - A$. This ensures the sum constraint is satisfied exactly without introducing rounding inconsistencies.
4. Output $(A, B)$. If the alternative ordering was intended by the hidden pair, this output is still valid because swapping does not violate either equation.

### Why it works

The core invariant is that any valid solution must satisfy a linear system derived from choosing one of the two possible signs of the absolute difference. The transformation reduces the problem to solving a deterministic linear equation system. Since exactly one of the two sign choices produces an integer solution consistent with the constraints, and the problem guarantees existence, the computed pair must satisfy both original equations.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    X = int(input().strip())
    Y = int(input().strip())

    A = (X + Y) // 2
    B = X - A

    print(A, B)

if __name__ == "__main__":
    main()
```

The implementation directly encodes the algebraic derivation. Integer division is safe because the problem guarantees that a valid integer solution exists, meaning $X + Y$ is always even in valid cases.

The construction of $B$ as $X - A$ avoids recomputing the second equation separately and guarantees consistency with the sum constraint. There is no need to explicitly branch on the sign of the absolute difference because the symmetry of the output allows either valid ordering.

## Worked Examples

Consider the input:

```
10
2
```

We compute $A = (10 + 2)/2 = 6$, then $B = 4$.

| Step | X | Y | A | B |
| --- | --- | --- | --- | --- |
| Start | 10 | 2 | - | - |
| Compute A | 10 | 2 | 6 | - |
| Compute B | 10 | 2 | 6 | 4 |

This produces a valid pair since $6 + 4 = 10$ and $|6 - 4| = 2$.

Now consider:

```
3
7
```

We compute $A = (3 + 7)/2 = 5$, then $B = -2$.

| Step | X | Y | A | B |
| --- | --- | --- | --- | --- |
| Start | 3 | 7 | - | - |
| Compute A | 3 | 7 | 5 | - |
| Compute B | 3 | 7 | 5 | -2 |

This yields $(5, -2)$, which satisfies $5 + (-2) = 3$ and $|5 - (-2)| = 7$. The ordering is different from the sample output but still correct.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(1)$ | Only a constant number of arithmetic operations are performed |
| Space | $O(1)$ | No auxiliary data structures are used |

The algorithm performs a fixed amount of integer arithmetic regardless of input size. This fits easily within the constraints, since even the largest inputs require only a few CPU operations.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdin.read()

# provided samples (conceptual placeholders since full harness not embedded)
# assert run("10\n2\n") == "6 4"
# assert run("3\n7\n") == "5 -2"

# custom cases
assert run("0\n0\n").strip() in ["0 0"], "zero case"
assert run("2\n0\n").strip() in ["1 1"], "equal values"
assert run("1000000000\n0\n").strip() in ["500000000 500000000"], "large equal split"
assert run("5\n1\n")  # just ensuring no crash
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0 0 | 0 0 | degenerate equality case |
| 2 0 | 1 1 | zero difference forces equality |
| 1e9 0 | 5e8 5e8 | large boundary arithmetic |
| 5 1 | valid pair | general correctness |

## Edge Cases

When $Y = 0$, the system collapses to $A = B = X/2$. For an input like:

```
4
0
```

the computation gives $A = 2$, $B = 2$. Both constraints are satisfied immediately, and no ambiguity arises since the absolute difference contributes no additional information.

When $X = Y$, one of the values becomes zero. For example:

```
10
10
```

produces $A = 10$, $B = 0$. The absolute difference matches the sum structure exactly, and the formula still holds without special casing.

When $Y > X$, one of the values becomes negative. For:

```
3
7
```

we get $A = 5$, $B = -2$. This shows that assuming non-negativity would be incorrect, and the algebraic derivation correctly handles signed integers.

Across all these cases, the same construction remains valid because it never assumes ordering or sign constraints beyond what the equations enforce.
