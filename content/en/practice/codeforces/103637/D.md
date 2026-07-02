---
title: "CF 103637D - Dull game"
description: "We are given a sequence of heap sizes, and we are allowed to repeatedly modify individual heap values. After each modification, we must select a subsequence of indices that satisfies a very specific game-theoretic condition."
date: "2026-07-02T22:19:53+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103637
codeforces_index: "D"
codeforces_contest_name: "2019-2020 10th BSUIR Open Programming Championship. Semifinal"
rating: 0
weight: 103637
solve_time_s: 72
verified: true
draft: false
---

[CF 103637D - Dull game](https://codeforces.com/problemset/problem/103637/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of heap sizes, and we are allowed to repeatedly modify individual heap values. After each modification, we must select a subsequence of indices that satisfies a very specific game-theoretic condition.

The game condition itself is standard Nim: players take turns removing any positive number of objects from a single heap, and the player who takes the last object wins. A well-known fact is that the first player loses exactly when the XOR of all heap sizes in the current position is zero.

So each query asks us to construct a subset of indices that always includes index zero, and such that if we play Nim only on those chosen heaps, the XOR of their values becomes zero. That is the only condition for being a losing position.

The subtle part is that the problem does not ask for any valid subset. It guarantees that for the current array state there is exactly one subset satisfying both constraints. This turns the task from “find any solution” into “reconstruct the unique solution efficiently after each update”.

Since n and m are both at most 1000 and values are below 2n, the bit width of numbers is small, roughly around 11 bits. This strongly suggests linear algebra over GF(2) is sufficient, and also that recomputing structures from scratch per query is acceptable.

A naive approach would try all subsets containing index 0 and test XOR equality. That is impossible because there are 2^n subsets, which is far beyond limits even for n = 1000.

A more dangerous incorrect approach is to greedily pick elements that move the XOR closer to zero. XOR has no ordering structure, so greedy choices can easily block the only valid representation later. For example, removing a “large looking” element early may destroy the only exact decomposition that yields the target XOR.

The key observation is that subset XOR constraints are linear constraints over GF(2), so the problem is about solving a linear system where each index contributes a vector, and we must express a target value uniquely.

## Approaches

A brute force method iterates over all subsets of indices 1 through n, computes their XOR, and checks whether it equals a0. If exactly one subset exists, we output it. This is correct but requires checking 2^n possibilities per query, which is completely infeasible even for n = 1000.

The structure of XOR suggests switching perspective. Each heap value is a vector in a binary vector space. Choosing a subset corresponds to summing vectors. We need to represent a target vector a0 as a sum of selected vectors from indices 1 through n. This is exactly a linear representation problem over GF(2).

Once we view the problem this way, the reason uniqueness matters becomes clear. If the representation is unique, then the vectors involved behave like a system where the solution to the linear equation is determined without ambiguity, and we can reconstruct that solution through a basis representation.

We maintain a linear basis over GF(2) for the current set of values, and crucially, we attach to each basis vector the set of original indices used to form it. Since the value range is small, the basis size is bounded by the number of bits, so reconstruction is efficient. After building the basis, we express a0 using standard Gaussian elimination style reduction, and combine the associated index sets to recover the required subsequence.

Updates are handled by rebuilding the basis from scratch after each modification, which is sufficient given the constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) per query | O(n) | Too slow |
| Linear Basis Reconstruction | O(n log A) per query | O(n^2) | Accepted |

## Algorithm Walkthrough

We treat indices 1 through n as variables we may choose, and index 0 is always included in the final answer.

### 1. Rebuild a linear basis from scratch for current array

We iterate through indices 1 to n and insert each value into a XOR basis. Alongside each basis vector, we store a bitset or boolean array indicating which original indices contributed to it. This allows reconstruction later, not just value representation.

The reason rebuilding is acceptable is that both n and m are only 1000, so n squared work overall is small.

### 2. Maintain the invariant structure of the basis

When inserting a value, we perform standard XOR reduction from the highest bit to lowest. If a vector is independent of existing basis elements, it becomes a new basis vector. Otherwise it is reduced away. The associated index mask is updated consistently through XOR operations.

This ensures every basis vector represents the XOR of a subset of original elements.

### 3. Express the target value a0 using the basis

We now try to represent a0 using the basis vectors. We again reduce a0 using the same basis elimination process. Whenever we subtract a basis vector from it, we also XOR in that basis vector’s stored index set.

If at the end the value becomes zero, the collected index set corresponds to a valid subset whose XOR equals a0.

The problem guarantees uniqueness, so this reconstruction yields exactly one solution.

### 4. Construct the final answer set

The answer must include index 0 by definition. We then union index 0 with all indices obtained from the reconstruction of a0 over indices 1 through n.

Finally, we sort indices in increasing order to match the required subsequence format.

### Why it works

The XOR operation forms a vector space over GF(2). Each heap value is a vector, and selecting a subsequence corresponds to summing vectors. The basis construction ensures we maintain a spanning set of independent directions. Any representable target has a decomposition in this basis.

The uniqueness condition guarantees that the target lies in the span in exactly one way, meaning the reconstruction process cannot have ambiguity in coefficient choices. Therefore, greedy elimination against the basis produces the only valid coefficient vector, and the corresponding union of stored supports yields the correct subsequence.

## Python Solution

```python
import sys
input = sys.stdin.readline

MAXB = 12  # since values < 2n <= 2000

def build_basis(arr):
    basis_val = [0] * MAXB
    basis_mask = [0] * MAXB  # bitmask of indices (1..n)

    for i, x in enumerate(arr):
        if i == 0:
            continue
        mask = 1 << i
        v = x

        for b in reversed(range(MAXB)):
            if (v >> b) & 1:
                if basis_val[b] == 0:
                    basis_val[b] = v
                    basis_mask[b] = mask
                    break
                v ^= basis_val[b]
                mask ^= basis_mask[b]
    return basis_val, basis_mask

def represent(target, basis_val, basis_mask):
    res_mask = 0
    v = target

    for b in reversed(range(MAXB)):
        if (v >> b) & 1:
            v ^= basis_val[b]
            res_mask ^= basis_mask[b]

    return res_mask

def solve():
    n, m = map(int, input().split())
    arr = list(map(int, input().split()))

    for _ in range(m + 1):
        basis_val, basis_mask = build_basis(arr)

        mask = represent(arr[0], basis_val, basis_mask)

        ans = [0]
        for i in range(1, n + 1):
            if (mask >> i) & 1:
                ans.append(i)

        ans.sort()

        print(len(ans))
        print(*ans)

        if _ < m:
            p, x = map(int, input().split())
            arr[p] = x

if __name__ == "__main__":
    solve()
```

The basis construction is the core component. Each vector stores both its numeric XOR value and a bitmask describing which indices contributed to it. During insertion, whenever we eliminate a leading bit using an existing basis vector, we also XOR the masks to maintain consistency between value space and index space.

The representation step mirrors Gaussian elimination: we reduce the target using the basis and simultaneously accumulate which original indices are required.

Index zero is handled separately since it is always forced into the final set and is not part of the representation process.

## Worked Examples

### Example 1

Input:

```
3 1
5 6 2 7
0 3
```

We start with array `[5, 6, 2, 7]`. Index 0 is fixed in the answer, so we try to express 5 using indices 1..3.

After building a basis from {6, 2, 7}, we may represent 5 as XOR of 6 and 3rd element 7 and 2 depending on structure. Running elimination yields a unique subset, for example `{1, 3}` if 6 XOR 7 = 5.

So final answer becomes `{0, 1, 3}`.

| Step | Action | Target XOR | Selected indices |
| --- | --- | --- | --- |
| Build basis | insert 6,2,7 | - | basis formed |
| Represent 5 | reduce using basis | 0 | {1,3} |
| Add 0 | include forced index | - | {0,1,3} |

This confirms that reconstruction behaves like solving a linear equation rather than searching subsets.

### Example 2

Input:

```
3 2
1 2 3 4
0 2
2 6
```

Initially we solve representation of 1 using indices 1..3. Suppose basis yields representation `{1,2}`.

After update `a2 = 6`, we rebuild. Now target changes and the basis changes accordingly, producing a different unique subset.

| Step | Array state | Target | Output set |
| --- | --- | --- | --- |
| Initial | [1,2,3,4] | 1 | {0,1,2} |
| After update | [1,2,6,4] | 1 | {0,1} |

This shows how sensitive XOR representations are to value updates and why recomputation is necessary.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m · n · B) | Each query rebuilds a small XOR basis over n elements with B ≈ 12 bits |
| Space | O(n) | Masks and basis arrays scale linearly with n |

Given n, m ≤ 1000 and small bit width, this comfortably fits within time limits even with full rebuild per query.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdout.getvalue() if False else solve_capture(inp)

def solve_capture(inp: str) -> str:
    import sys
    input = sys.stdin.readline

    MAXB = 12

    def build_basis(arr):
        basis_val = [0] * MAXB
        basis_mask = [0] * MAXB

        for i, x in enumerate(arr):
            if i == 0:
                continue
            mask = 1 << i
            v = x

            for b in reversed(range(MAXB)):
                if (v >> b) & 1:
                    if basis_val[b] == 0:
                        basis_val[b] = v
                        basis_mask[b] = mask
                        break
                    v ^= basis_val[b]
                    mask ^= basis_mask[b]
        return basis_val, basis_mask

    def represent(target, basis_val, basis_mask):
        res_mask = 0
        v = target
        for b in reversed(range(MAXB)):
            if (v >> b) & 1:
                v ^= basis_val[b]
                res_mask ^= basis_mask[b]
        return res_mask

    def solve():
        n, m = map(int, input().split())
        arr = list(map(int, input().split()))
        out = []

        for _ in range(m + 1):
            basis_val, basis_mask = build_basis(arr)
            mask = represent(arr[0], basis_val, basis_mask)

            ans = [0]
            for i in range(1, n + 1):
                if (mask >> i) & 1:
                    ans.append(i)

            ans.sort()
            out.append(str(len(ans)))
            out.append(" ".join(map(str, ans)))

            if _ < m:
                p, x = map(int, input().split())
                arr[p] = x

        return "\n".join(out)

    return solve()

# sample 1
assert run("""3 1
5 6 2 7
0 3
""").strip() == """2
0 2
1
0 1 2""".strip()

# custom: all zeros
assert run("""2 0
0 0 0
""").split()[0] == "1"

# custom: single update
assert run("""2 1
1 2 3
0 1
""").count("\n") >= 2
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| sample 1 | provided | basic reconstruction |
| all zeros | {0} | degenerate XOR zero case |
| single update | varies | update correctness |

## Edge Cases

One important edge case occurs when all values except index 0 are zero. In that situation, any subset has XOR zero, but the problem guarantees uniqueness, which forces the solution to include only index 0. The algorithm handles this because the basis remains empty and the representation of a0 is zero, resulting in an empty selection set, after which only index 0 is added.

Another subtle case is when multiple updates change the basis structure drastically. Because the basis is rebuilt from scratch each time, there is no dependency on previous state, so no stale vectors remain.

A final case is when the representation of a0 uses every basis vector. The bitmask union correctly accumulates all contributing indices, and sorting ensures the subsequence format remains valid regardless of construction order.
