---
title: "CF 114B - PFAST Inc."
description: "We are given a small group of people and a list of pairs who cannot work together. We need to choose the largest possible subset such that every pair inside the chosen group is compatible. This is naturally a graph problem. Think of each volunteer as a vertex."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "brute-force", "graphs"]
categories: ["algorithms"]
codeforces_contest: 114
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 86 (Div. 2 Only)"
rating: 1500
weight: 114
solve_time_s: 139
verified: true
draft: false
---

[CF 114B - PFAST Inc.](https://codeforces.com/problemset/problem/114/B)

**Rating:** 1500  
**Tags:** bitmasks, brute force, graphs  
**Solve time:** 2m 19s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a small group of people and a list of pairs who cannot work together. We need to choose the largest possible subset such that every pair inside the chosen group is compatible.

This is naturally a graph problem. Think of each volunteer as a vertex. If two people dislike each other, we add an edge between them. The task becomes finding the largest subset of vertices with no edges between any two of them. In graph theory, this is called a maximum independent set.

The number of volunteers is at most 16, which completely changes how we should think about the problem. A general maximum independent set problem is NP-hard, but with only 16 vertices we can afford exhaustive search over all subsets. There are only $2^{16} = 65536$ subsets, which is tiny for modern hardware. Even if we spend a few hundred operations checking each subset, the total work easily fits within the time limit.

A naive recursive backtracking approach without pruning can still become messy because it repeatedly recomputes compatibility checks between overlapping states. Since the search space is already small enough, iterating over every bitmask directly is simpler and safer.

There are several edge cases that can silently break an implementation.

One common mistake is treating the incompatibility relation as directed instead of undirected.

Input:

```
2 1
Alice
Bob
Alice Bob
```

The correct answer is any single person. If we only mark `Alice -> Bob` but forget `Bob -> Alice`, then the subset `{Bob, Alice}` may incorrectly appear valid depending on iteration order.

Another easy bug is forgetting that names are case-sensitive.

Input:

```
2 0
Petya
petya
```

These are different people. The correct answer contains both names. Converting names to lowercase would merge them incorrectly.

A subtler issue appears when checking whether a subset is valid. Suppose we only verify that every chosen node has at least one compatible neighbor. That condition is meaningless because compatibility must hold for every pair.

Input:

```
3 2
A
B
C
A B
B C
```

The valid maximum team is `{A, C}` with size 2. A careless local check could incorrectly allow all three.

Finally, the output must be sorted lexicographically. The internal indexing order is arbitrary and depends on input order, so printing selected names directly from indices may produce the wrong format.

## Approaches

The most direct solution is brute force over all subsets of people.

For every subset, we test whether all selected members are pairwise compatible. If yes, we compare its size with the best answer found so far.

The simplest compatibility check examines every pair inside the subset. With $n = 16$, there are $2^{16}$ subsets and at most $16^2$ pair checks per subset. That gives roughly:

$$2^{16} \times 16^2 \approx 1.6 \times 10^7$$

operations, which is already acceptable in Python.

The brute force works because the constraints are extremely small. The issue is not asymptotic infeasibility, but implementation cleanliness and avoiding unnecessary repeated checks.

The key observation is that subsets are naturally represented as bitmasks. Each person corresponds to one bit. We can also store, for every person, a bitmask of people they conflict with.

Now validating a subset becomes very fast. For a chosen person `i`, if:

$$mask \& bad[i] \neq 0$$

then the subset contains someone incompatible with `i`, so the subset is invalid.

This converts pairwise checking into compact bit operations.

The problem structure makes bitmasking ideal because:

1. The universe size is tiny.
2. Every subset must be considered anyway.
3. Compatibility relationships are static.
4. Bit operations are extremely fast.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force with pair checking | $O(2^n \cdot n^2)$ | $O(n^2)$ | Accepted |
| Bitmask optimization | $O(2^n \cdot n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Read all names and assign each person an index from `0` to `n-1`.

Working with integer indices allows us to use compact bitmasks instead of strings during computation.
2. Build a mapping from name to index.

This lets us convert incompatibility pairs from strings into numeric vertex IDs efficiently.
3. Create an array `bad` where `bad[i]` is a bitmask of everyone incompatible with person `i`.

If person `i` dislikes person `j`, then set bit `j` inside `bad[i]`, and also set bit `i` inside `bad[j]`.
4. Iterate through every subset `mask` from `0` to `(1 << n) - 1`.

Each bitmask represents one possible team.
5. For each subset, check whether it is valid.

Iterate through all people `i`. If person `i` is inside the subset and:

$$mask \& bad[i] \neq 0$$

then some incompatible teammate is also inside the subset, so this subset cannot be used.
6. If the subset is valid, compare its size with the current best answer.

Use `mask.bit_count()` to compute the team size efficiently.
7. Store the best subset found.

Any maximum solution is acceptable, so ties do not matter.
8. Extract the names belonging to the best subset.

Sort them lexicographically before printing because the problem requires sorted output.

### Why it works

A subset is valid exactly when no incompatible pair appears together inside it.

The array `bad[i]` contains every person who conflicts with `i`. During validation, the expression:

$$mask \& bad[i]$$

checks whether the current subset contains any incompatible partner of `i`.

If this expression is nonzero for some selected person `i`, then the subset violates the requirement and must be rejected.

If the expression is zero for every selected person, then no conflicting pair exists anywhere inside the subset, so the subset is valid.

Since the algorithm examines every possible subset, the largest valid one found is guaranteed to be optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())

    names = [input().strip() for _ in range(n)]

    idx = {}
    for i, name in enumerate(names):
        idx[name] = i

    bad = [0] * n

    for _ in range(m):
        a, b = input().split()

        u = idx[a]
        v = idx[b]

        bad[u] |= (1 << v)
        bad[v] |= (1 << u)

    best_mask = 0
    best_size = 0

    for mask in range(1 << n):
        ok = True

        for i in range(n):
            if (mask >> i) & 1:
                if mask & bad[i]:
                    ok = False
                    break

        if ok:
            size = mask.bit_count()

            if size > best_size:
                best_size = size
                best_mask = mask

    ans = []

    for i in range(n):
        if (best_mask >> i) & 1:
            ans.append(names[i])

    ans.sort()

    print(best_size)
    print(*ans, sep="\n")

solve()
```

The first section reads names and converts them into integer indices. This is essential because bitmask operations only work cleanly with numeric IDs.

The `bad` array stores incompatibility masks. If `bad[3]` has bits 1 and 5 set, then person 3 cannot work with persons 1 and 5.

The subset loop enumerates every possible team. Since `n <= 16`, the total number of subsets is only 65536.

The validation step is the core of the solution. For each selected person `i`, we test whether any forbidden teammate also exists in the subset. The expression:

```
mask & bad[i]
```

returns a nonzero integer exactly when at least one conflicting person is present.

The implementation checks all selected vertices independently. Even though this may detect the same bad pair twice, the constant factor is tiny and the logic stays very clear.

The output phase collects selected names and sorts them lexicographically. This detail is easy to forget because the internal subset order follows input order, not dictionary order.

## Worked Examples

### Example 1

Input:

```
3 1
Petya
Vasya
Masha
Petya Vasya
```

Index assignment:

| Name | Index |
| --- | --- |
| Petya | 0 |
| Vasya | 1 |
| Masha | 2 |

Conflict masks:

| Person | bad mask | Meaning |
| --- | --- | --- |
| Petya | 010 | conflicts with Vasya |
| Vasya | 001 | conflicts with Petya |
| Masha | 000 | conflicts with nobody |

Subset trace:

| Mask | Members | Valid | Size |
| --- | --- | --- | --- |
| 000 | {} | Yes | 0 |
| 001 | {Petya} | Yes | 1 |
| 010 | {Vasya} | Yes | 1 |
| 011 | {Petya, Vasya} | No | - |
| 100 | {Masha} | Yes | 1 |
| 101 | {Petya, Masha} | Yes | 2 |
| 110 | {Vasya, Masha} | Yes | 2 |
| 111 | {Petya, Vasya, Masha} | No | - |

The maximum valid size is 2. One acceptable answer is `{Masha, Petya}`.

This trace demonstrates how invalid subsets are rejected immediately once a conflicting pair appears.

### Example 2

Input:

```
4 3
A
B
C
D
A B
B C
C D
```

Conflict masks:

| Person | Conflicts |
| --- | --- |
| A | B |
| B | A, C |
| C | B, D |
| D | C |

Subset trace for larger candidates:

| Mask | Members | Valid | Size |
| --- | --- | --- | --- |
| 0011 | {A, B} | No | - |
| 0101 | {A, C} | Yes | 2 |
| 1001 | {A, D} | Yes | 2 |
| 1010 | {B, D} | Yes | 2 |
| 1100 | {C, D} | No | - |
| 1111 | {A, B, C, D} | No | - |

No valid subset of size 3 exists, so the answer size is 2.

This example shows that incompatibility is purely pairwise. Even though `A` and `D` are both indirectly connected through other people, they can still belong to the same team.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(2^n \cdot n)$ | Every subset is checked against all people |
| Space | $O(n)$ | We store one conflict mask per person |

With $n \le 16$, the algorithm performs roughly:

$$65536 \times 16 \approx 10^6$$

basic iterations, which is comfortably inside the limit. Memory usage is negligible.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def solve():
        n, m = map(int, input().split())

        names = [input().strip() for _ in range(n)]

        idx = {}
        for i, name in enumerate(names):
            idx[name] = i

        bad = [0] * n

        for _ in range(m):
            a, b = input().split()

            u = idx[a]
            v = idx[b]

            bad[u] |= (1 << v)
            bad[v] |= (1 << u)

        best_mask = 0
        best_size = 0

        for mask in range(1 << n):
            ok = True

            for i in range(n):
                if (mask >> i) & 1:
                    if mask & bad[i]:
                        ok = False
                        break

            if ok:
                size = mask.bit_count()

                if size > best_size:
                    best_size = size
                    best_mask = mask

        ans = []

        for i in range(n):
            if (best_mask >> i) & 1:
                ans.append(names[i])

        ans.sort()

        out = [str(best_size)]
        out.extend(ans)

        return "\n".join(out)

    return solve()

# provided sample
assert run(
"""3 1
Petya
Vasya
Masha
Petya Vasya
"""
) == "2\nMasha\nPetya"

# minimum size
assert run(
"""1 0
Solo
"""
) == "1\nSolo"

# everyone compatible
assert run(
"""3 0
A
B
C
"""
) == "3\nA\nB\nC"

# complete conflict graph
out = run(
"""4 6
A
B
C
D
A B
A C
A D
B C
B D
C D
"""
)

assert out in {
    "1\nA",
    "1\nB",
    "1\nC",
    "1\nD"
}

# case-sensitive names
assert run(
"""2 0
Petya
petya
"""
) == "2\nPetya\npetya"

# chain conflicts
out = run(
"""4 3
A
B
C
D
A B
B C
C D
"""
)

assert out in {
    "2\nA\nC",
    "2\nA\nD",
    "2\nB\nD"
}
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single person | Team size 1 | Minimum constraint handling |
| No conflicts | Everyone selected | Full subset selection |
| Complete graph | Only one person | Conflict checking correctness |
| `Petya` vs `petya` | Both selected | Case-sensitive names |
| Chain conflicts | Maximum independent set | Nontrivial graph structure |

## Edge Cases

Consider the case where incompatibility is mistakenly treated as directed.

Input:

```
2 1
Alice
Bob
Alice Bob
```

The algorithm stores both:

```
bad[Alice] |= Bob
bad[Bob] |= Alice
```

Now when checking subset `{Alice, Bob}`, both people detect a conflict, so the subset is rejected correctly.

Consider case-sensitive names.

Input:

```
2 0
Petya
petya
```

The mapping dictionary stores two separate keys:

```
{
    "Petya": 0,
    "petya": 1
}
```

Since no conflict exists, subset `11` is valid and both names appear in the answer.

Consider a graph where indirect connections should not matter.

Input:

```
3 2
A
B
C
A B
B C
```

The subset `{A, C}` corresponds to mask `101`.

For `A`:

```
mask & bad[A] = 101 & 010 = 0
```

For `C`:

```
mask & bad[C] = 101 & 010 = 0
```

The subset is valid because only direct incompatibilities matter.

Finally, consider the fully disconnected graph.

Input:

```
4 0
A
B
C
D
```

All `bad[i]` masks are zero. Every subset passes validation, and the algorithm eventually selects mask `1111`, containing all four people.
