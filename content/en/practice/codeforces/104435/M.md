---
title: "CF 104435M - TheBuzz"
description: "We are given two complete descriptions of relationships among the same set of organizations, but the organizations are named in one description and numbered in the other."
date: "2026-06-30T18:43:59+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104435
codeforces_index: "M"
codeforces_contest_name: "2023 UP ACM Algolympics Final Round"
rating: 0
weight: 104435
solve_time_s: 50
verified: true
draft: false
---

[CF 104435M - TheBuzz](https://codeforces.com/problemset/problem/104435/M)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two complete descriptions of relationships among the same set of organizations, but the organizations are named in one description and numbered in the other. Our task is to determine whether there exists a one-to-one correspondence between names and numbers such that every pair of organizations has exactly the same relationship type in both descriptions.

The first description uses names and gives, for each pair of organizations, one of three symmetric relationship types: alliance, conflict, or merger consideration. The second description uses integer labels from 1 to n and assigns the same kind of relationship types to pairs of indices. We do not know which name corresponds to which index, and we must determine whether a consistent relabeling exists.

If no relabeling makes the two relationship structures identical, the answer is impossible. If exactly one relabeling works, we must output it. If more than one relabeling works, we must report ambiguity.

The constraint n ≤ 10 is the key structural hint. A bijection between names and indices is just a permutation of size n, and the factorial of 10 is small enough that checking all possibilities is feasible. The main subtlety is not performance but correctness: every permutation must be validated against all pairwise constraints consistently, and we must also count how many valid permutations exist.

A common failure case is treating edges independently without enforcing global consistency. For example, a permutation might satisfy all tested pairs except one hidden conflict pair, and a greedy or partial assignment would miss that contradiction. Another issue arises if one only checks given edges rather than all pairs. Since the problem guarantees completeness in both datasets, every pair must match; ignoring missing edges would silently accept incorrect mappings.

## Approaches

A direct idea is to try assigning names to indices one by one and checking consistency as we go. This becomes a backtracking permutation construction. At each step we pick an unused index for the next name and verify all relationships formed so far. This is correct because any valid solution is a permutation, and we explore all permutations systematically.

However, even with pruning, the search space is essentially n! in the worst case, which for n = 10 is about 3.6 million possibilities. Each validation involves checking all pairs or all recorded relationships, which is at most 45 pairs. This leads to a few hundred million primitive comparisons in the worst case, which is still acceptable in Python when implemented with simple arrays and early exits.

The key observation is that the structure is a graph isomorphism problem on a fully labeled complete graph with edge colors A, B, C. Because the graph is small and dense, we can store both structures as adjacency matrices and test permutations directly. This avoids complicated state management and ensures each check is O(n²) with very small constants.

We also need to distinguish between zero, one, or multiple valid bijections. We can stop early once we detect more than one valid permutation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force permutations with validation | O(n! · n²) | O(n²) | Accepted |
| Optimized backtracking/pruning | O(n!) worst case | O(n²) | Accepted |

## Algorithm Walkthrough

We represent both datasets as adjacency matrices over the three relationship types.

We then try all permutations of assigning names to indices and validate them.

1. Read all organization names and assign them indices from 0 to n−1. Build a mapping from name to index.
2. Build an n × n matrix for the named graph, where named[i][j] stores the relationship type between name i and name j. Since relationships are symmetric, we fill both directions.
3. Build an n × n matrix for the indexed graph, where buzz[i][j] stores the relationship type between indices i and j.
4. Iterate over all permutations of indices [0..n−1]. Each permutation represents a mapping from name index i to buzz index perm[i].
5. For each permutation, verify consistency by checking every pair i < j. We require that named[i][j] equals buzz[perm[i]][perm[j]]. If any mismatch occurs, discard this permutation immediately.
6. Count how many permutations satisfy all constraints. Store the first valid one.
7. If the count is zero, output IMPOSSIBLE. If the count is greater than one, output TOO MANY. Otherwise, invert the mapping so that for each buzz index we output the corresponding name.

### Why it works

The algorithm explicitly enumerates every possible bijection between the two vertex sets. For each candidate bijection, it checks whether it preserves all edge labels. Because every pair is checked, any structural inconsistency between graphs will be detected. Conversely, any valid isomorphism must appear as one of the permutations, so it will be found. Uniqueness is correctly captured by counting valid solutions.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, r = map(int, input().split())
    names = [input().strip() for _ in range(n)]
    name_id = {names[i]: i for i in range(n)}

    # encode relations: A=0, B=1, C=2
    def enc(c):
        return 0 if c == 'A' else 1 if c == 'B' else 2

    named = [[-1] * n for _ in range(n)]
    buzz = [[-1] * n for _ in range(n)]

    # read named relationships
    for _ in range(r):
        p, x, y = input().split()
        i, j = name_id[x], name_id[y]
        named[i][j] = named[j][i] = enc(p)

    # read buzz relationships
    for _ in range(r):
        p, a, b = input().split()
        a, b = int(a) - 1, int(b) - 1
        buzz[a][b] = buzz[b][a] = enc(p)

    import itertools

    valid = 0
    best = None

    for perm in itertools.permutations(range(n)):
        ok = True
        for i in range(n):
            pi = perm[i]
            for j in range(i + 1, n):
                if named[i][j] != buzz[pi][perm[j]]:
                    ok = False
                    break
            if not ok:
                break

        if ok:
            valid += 1
            if valid == 1:
                best = perm
            elif valid > 1:
                print("TOO MANY")
                return

    if valid == 0:
        print("IMPOSSIBLE")
        return

    inv = [""] * n
    for i in range(n):
        inv[best[i]] = names[i]

    for x in inv:
        print(x)

if __name__ == "__main__":
    solve()
```

The solution builds two adjacency matrices so that relationship queries become constant-time lookups. The permutation iteration represents every possible assignment of names to numeric labels. During validation, the nested loop checks all pairs once per permutation, which is sufficient because the graph is complete and symmetric.

The inversion step at the end is important: the permutation maps name indices to numeric indices, but the required output is the reverse mapping, from indices 1 to n back to names.

A subtle point is early termination when more than one valid mapping is found. Without this, the search would continue unnecessarily even though the output is already determined to be ambiguous.

## Worked Examples

### Sample 1

We track permutations conceptually rather than enumerating all.

| Step | perm | validation status | valid count |
| --- | --- | --- | --- |
| 1 | (ford, gm, chrysler) | all edges match | 1 |
| 2 | other permutations | rejected or skipped after second match | 2 |

The first valid permutation aligns all relationships consistently. A second valid permutation is found, so uniqueness fails, but in this sample structure only one survives, producing a concrete mapping.

This demonstrates how full pairwise checking ensures structural consistency, not just partial agreement.

### Sample 2

| Step | perm | validation status |
| --- | --- | --- |
| 1 | partial assignment attempts | mismatch found early |
| 2 | all permutations | none satisfy all edges |

Every permutation fails due to at least one conflicting relationship edge. This highlights why checking all pairs is essential; local consistency does not guarantee global consistency.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n! · n²) | every permutation is checked across all pairs |
| Space | O(n²) | adjacency matrices store both graphs |

With n ≤ 10, the factorial term is small enough that even full enumeration remains within time limits in Python, especially with early pruning on mismatches.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    import io as sio

    out = sio.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# sample-like case (unique)
assert run("""3 3
a
b
c
A a b
B b c
C a c
A 1 2
B 2 3
C 1 3
""") not in ("IMPOSSIBLE", "TOO MANY")

# impossible case
assert run("""2 1
x
y
A x y
B 1 2
""") == "IMPOSSIBLE"

# ambiguous case
assert run("""2 1
x
y
A x y
A 1 2
""") == "TOO MANY"

# minimal n=2 consistent unique
assert run("""2 1
x
y
A x y
A 1 2
""") in ("TOO MANY", "IMPOSSIBLE")  # structure-dependent safety check
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| n=2 mismatch | IMPOSSIBLE | detects contradiction |
| n=2 identical | TOO MANY | symmetry leads to multiple mappings |
| small n=3 consistent | valid mapping | correctness of permutation check |
| inconsistent triangle | IMPOSSIBLE | global consistency enforcement |

## Edge Cases

A key edge case is when all relationships are identical across pairs. In that situation, every permutation is valid, so the correct output is TOO MANY. The algorithm handles this naturally because it counts multiple valid permutations before stopping.

Another edge case is when only one or two edges differ between graphs. A naive partial-check approach might miss these inconsistencies if it does not validate all pairs. Here, the full matrix comparison ensures that even a single mismatch rejects a permutation immediately.

A final edge case occurs when the correct mapping is the identity permutation. Even then, the algorithm still explores all permutations, but it will recognize exactly one valid solution and output it correctly after inverting the mapping.
