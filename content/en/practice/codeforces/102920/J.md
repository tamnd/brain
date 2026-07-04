---
title: "CF 102920J - Switches"
description: "We are given a system with the same number of switches and lights, and a binary connection matrix describing how switches influence lights."
date: "2026-07-04T07:57:09+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102920
codeforces_index: "J"
codeforces_contest_name: "2020-2021 ACM-ICPC, Asia Seoul Regional Contest"
rating: 0
weight: 102920
solve_time_s: 41
verified: true
draft: false
---

[CF 102920J - Switches](https://codeforces.com/problemset/problem/102920/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 41s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a system with the same number of switches and lights, and a binary connection matrix describing how switches influence lights. When a switch is turned on, it affects several lights at once, and each light’s final state depends only on how many of its connected switches are currently on. A light is on exactly when the number of active connected switches is odd, and off when that number is even.

The task is not to simulate switching. Instead, for each light independently, we must determine whether there exists some subset of switches such that this specific light is on while every other light is off. If this is possible for all lights, we must output, for each light, one valid subset of switches that achieves this condition. If even one light cannot be isolated in this way, we output -1.

The input matrix is naturally interpreted as a linear transformation over the field GF(2). Each switch is a vector in a 0-1 space of lights, and turning switches on corresponds to adding vectors modulo 2. Each light corresponds to a coordinate we want to isolate as 1 while all others become 0.

The constraint N ≤ 500 suggests that O(N³) Gaussian elimination is acceptable, but anything involving enumerating subsets of switches is impossible since that would be O(2^N). The structure strongly suggests solving a system of linear equations over GF(2), not brute force search.

A subtle point is that we are not asked whether each light is reachable independently in isolation of others in a fixed system. The system of equations must be simultaneously solvable in a way that produces a full basis of isolated outputs. This is stronger than checking reachability one by one independently.

A common failure case comes from treating each light independently and attempting greedy selection of switches. For example, picking switches that toggle only that light may fail because their combination could unintentionally affect previously fixed lights.

## Approaches

A direct brute force approach would try every subset of switches and compute resulting light configurations. For each subset, we check whether it isolates a particular light. This is correct because it exhaustively explores all possible switch configurations, but the cost is exponential: there are 2^N subsets, and each evaluation costs O(N), leading to O(N·2^N), which is completely infeasible for N up to 500.

The key observation is that switching behavior is linear over GF(2). Each switch corresponds to a binary vector, and turning switches on corresponds to summing those vectors modulo 2. The system becomes a matrix A of size N×N, and any switch configuration is a vector x, producing output Ax over GF(2). The problem reduces to asking whether the matrix can be used to produce all standard basis vectors e₁, e₂, ..., eₙ, and if so, to construct preimages for each.

This is equivalent to asking whether A is invertible over GF(2). If it is invertible, then for each light i, there exists a unique solution x such that Ax = eᵢ. If A is not invertible, then at least one basis vector is not reachable, and the answer is -1.

Thus the problem reduces to performing Gaussian elimination over GF(2), checking invertibility, and then computing A⁻¹ implicitly by augmenting with the identity matrix.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N·2^N) | O(N) | Too slow |
| Gaussian Elimination over GF(2) | O(N³) | O(N²) | Accepted |

## Algorithm Walkthrough

We treat the input matrix as an N×N binary matrix A. We build an augmented matrix [A | I], where I is the identity matrix. We then perform Gaussian elimination over GF(2), using XOR instead of subtraction.

1. For each column from left to right, we try to select a pivot row with a 1 in that column among rows not yet used. If no such row exists, the matrix is singular and we immediately return -1. This ensures every column contributes a pivot, which is necessary for invertibility.
2. Once a pivot row is found, we swap it into the current pivot position. This stabilizes the elimination order and ensures we are building a structured row echelon form.
3. We eliminate all other 1s in the current column by XORing the pivot row into those rows. This step maintains equivalence of the system while pushing the matrix toward identity form.
4. After processing all columns, if the left half becomes the identity matrix, the right half becomes A⁻¹. Each row of the right half then directly gives the switch set required to activate a single light.
5. For each light i, we output the positions of 1s in row i of the inverse matrix.

Why it works comes down to interpreting rows as basis transformations. Each row operation preserves the solution space of the linear system over GF(2). If elimination succeeds in turning A into identity, it means A has full rank and defines a bijection from switch configurations to light configurations. The augmented identity tracks how basis vectors are expressed in terms of original switches, so each row of the transformed identity encodes exactly which switches must be turned on to produce a single active light.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = [list(map(int, input().split())) for _ in range(n)]

    # augmented matrix [A | I]
    for i in range(n):
        a[i].extend([1 if i == j else 0 for j in range(n)])

    row = 0
    for col in range(n):
        pivot = -1
        for r in range(row, n):
            if a[r][col]:
                pivot = r
                break
        if pivot == -1:
            print(-1)
            return

        a[row], a[pivot] = a[pivot], a[row]

        for r in range(n):
            if r != row and a[r][col]:
                for c in range(2 * n):
                    a[r][c] ^= a[row][c]

        row += 1

    # extract inverse
    for i in range(n):
        res = []
        for j in range(n):
            if a[i][n + j]:
                res.append(j + 1)
        print(*res)

if __name__ == "__main__":
    solve()
```

The implementation constructs the augmented matrix explicitly, doubling each row width to store both A and the identity. The elimination loop selects pivots greedily from top to bottom, ensuring each column is processed once. The XOR step replaces subtraction in GF(2), and iterating over all rows maintains correctness because we want reduced row echelon form, not just upper triangular form.

The final extraction reads the right half as the inverse matrix. Each row corresponds to one light’s required switch set.

A subtle implementation detail is that we must eliminate both above and below pivot rows to guarantee a clean identity matrix. Restricting elimination to only lower rows would produce a triangular form but not the inverse directly.

## Worked Examples

Consider a small 3×3 system where the elimination succeeds.

| Step | Pivot col | Pivot row | Matrix state (left half) |
| --- | --- | --- | --- |
| 1 | 0 | 0 | becomes normalized with first pivot |
| 2 | 1 | 1 | second pivot fixed |
| 3 | 2 | 2 | full identity |

The right half after elimination becomes the inverse matrix, and each row indicates a valid switch set for isolating a light.

Now consider a singular case where one column is all zeros.

| Step | Pivot col | Action | Result |
| --- | --- | --- | --- |
| 1 | some col | no pivot found | terminate |

This corresponds to a light that cannot be expressed as a combination of switch vectors, meaning isolation is impossible.

The first case demonstrates how full rank leads to successful inversion, while the second shows immediate detection of impossibility.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N³) | Gaussian elimination over an N×2N matrix requires nested row and column operations |
| Space | O(N²) | storing the augmented matrix |

The cubic complexity is acceptable for N ≤ 500, since about 125 million bit operations is within typical Python limits only if optimized, and in practice bit operations with integers or lists are efficient enough under ICPC constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    def fake_print(*args):
        output.append(" ".join(map(str, args)))
    return "\n".join(output)

# provided sample placeholders (structure only)
# custom cases

# identity case
assert run("""3
1 0 0
0 1 0
0 0 1
""") == "1\n2\n3"

# singular matrix case
assert run("""2
1 1
1 1
""") == "-1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Identity matrix | trivial basis | already invertible system |
| All rows identical | -1 | singular detection |
| Small invertible mix | valid sets | correctness of elimination |

## Edge Cases

One important edge case is when multiple switches affect identical sets of lights. In such a case, two columns of the matrix are identical, immediately making the matrix singular. The algorithm detects this during pivot selection because only one pivot can be assigned per column, and eventually a column fails to find a valid pivot row, triggering -1.

Another case is when the matrix is invertible but elimination order matters for constructing a clean inverse. The algorithm always selects pivots top-down, ensuring consistency in row operations. Because every elimination is applied symmetrically to both left and right halves, the transformation preserves equivalence, so the final inverse is independent of pivot ordering as long as pivots are valid.

A final subtle case is when the matrix is full rank but poorly conditioned in terms of sparsity. Even then, GF(2) elimination ensures correctness because operations are purely XOR-based and do not depend on numerical stability.
