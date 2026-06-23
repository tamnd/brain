---
title: "CF 105454E - \u041a\u043e\u043c\u0430\u043d\u0434\u044b \u043d\u0430 \u041f\u0420\u041e\u0428\u041f"
description: "We are given a group of $n$ people and want to form teams of exactly three distinct members. However, not every triple is allowed because there are $m$ forbidden pairs of people who cannot appear together in the same team."
date: "2026-06-23T17:38:53+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105454
codeforces_index: "E"
codeforces_contest_name: "\u041f\u0435\u0440\u043c\u0441\u043a\u0430\u044f \u0440\u0435\u0433\u0438\u043e\u043d\u0430\u043b\u044c\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e 2024"
rating: 0
weight: 105454
solve_time_s: 83
verified: false
draft: false
---

[CF 105454E - \u041a\u043e\u043c\u0430\u043d\u0434\u044b \u043d\u0430 \u041f\u0420\u041e\u0428\u041f](https://codeforces.com/problemset/problem/105454/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 23s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a group of $n$ people and want to form teams of exactly three distinct members. However, not every triple is allowed because there are $m$ forbidden pairs of people who cannot appear together in the same team. A valid team is any set of three people such that no forbidden pair appears inside that trio.

The task is to count how many valid triples can be formed from the given people, where order does not matter and each person can be used multiple times across different teams. Two teams are considered different if at least one person is different between them.

The constraint $n \le 300$ is the key structural hint. A naive enumeration over all triples is already feasible in isolation because $\binom{300}{3} \approx 4.5 \cdot 10^6$, but checking validity per triple using a lookup structure still keeps it within time limits. However, since we must also handle up to $m \le 45{,}000$ forbidden pairs, the solution must support fast adjacency checks.

A subtle edge case is when there are no valid triples at all due to dense restrictions. For example, if every pair involving a particular person is forbidden, then no triple containing them works, but triples among other nodes may still exist. Another edge case is when there are no forbidden pairs at all, in which case the answer is simply $\binom{n}{3}$.

A second non-obvious issue is indexing by names. Since input uses strings, efficient mapping to integer indices is required; otherwise repeated string comparisons inside triple loops would be too slow.

## Approaches

The brute-force idea is straightforward: iterate over all triples $(i, j, k)$ with $i < j < k$, and check whether any of the three pairs is forbidden. With a boolean adjacency matrix or hash set, each check is $O(1)$, so the full enumeration runs in $O(n^3)$ time, about 27 million iterations at worst for $n=300$. This is already near the limit but still acceptable in optimized Python if implemented carefully.

The key observation is that we do not need to construct anything beyond fast pair lookup. There is no deeper combinatorial structure like DP or inclusion-exclusion needed, because constraints only eliminate local pairs inside each triple. That means every candidate triple can be validated independently.

We convert names into indices, build a forbidden adjacency matrix (or set of bitsets), then directly count valid triples by scanning all combinations. Any more complex strategy would add overhead without improving asymptotic complexity, since the output itself is $\Theta(n^3)$ in worst case enumeration.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force triple check | $O(n^3)$ | $O(n^2)$ | Accepted |
| Any advanced optimization | Not needed | Higher overhead | Slower in practice |

## Algorithm Walkthrough

1. Read all names and assign each a unique integer index from 0 to $n-1$. This allows constant-time access to relationships.
2. Create a 2D boolean structure `bad[i][j]` indicating whether pair $(i, j)$ is forbidden. We symmetrize it so both directions are marked. This ensures constant-time checking later.
3. Initialize an answer counter to zero. This will accumulate the number of valid triples.
4. Iterate over all triples $i < j < k$. For each triple, check the three pairwise relationships: $(i, j)$, $(i, k)$, and $(j, k)$.
5. If none of these pairs is forbidden, increment the answer. Otherwise skip the triple.
6. Output the final count modulo $10^9 + 13$.

The reason this works is that every invalid triple must contain at least one forbidden pair, and every valid triple contains none. Since we enumerate all unordered triples exactly once, and each is checked independently, the count is exact.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 13

def solve():
    n, m = map(int, input().split())
    
    name_to_idx = {}
    for i in range(n):
        name = input().strip()
        name_to_idx[name] = i

    bad = [[False] * n for _ in range(n)]

    for _ in range(m):
        a, b = input().split()
        a = name_to_idx[a]
        b = name_to_idx[b]
        bad[a][b] = True
        bad[b][a] = True

    ans = 0

    for i in range(n):
        for j in range(i + 1, n):
            if bad[i][j]:
                continue
            for k in range(j + 1, n):
                if not bad[i][k] and not bad[j][k]:
                    ans += 1

    print(ans % MOD)

if __name__ == "__main__":
    solve()
```

The solution begins by mapping each name to an index, which avoids repeated string comparisons inside the triple loop. The adjacency matrix `bad` is symmetric, so each forbidden pair is stored twice, allowing a single lookup regardless of order.

The triple loop is structured in increasing indices to guarantee each combination is counted exactly once. Inside, we prune early using `bad[i][j]`, since if the first pair is invalid, the whole triple is invalid. This small optimization reduces unnecessary inner loop iterations in dense graphs.

Finally, we only increment the answer when all three pair checks pass.

## Worked Examples

### Sample 1

Input:

```
5 3
anton borya vitya gosha denis
anton borya
vitya gosha
borya denis
```

We index:

```
anton=0, borya=1, vitya=2, gosha=3, denis=4
```

Forbidden pairs:

(0,1), (2,3), (1,4)

We enumerate triples:

| i | j | k | (i,j) | (i,k) | (j,k) | valid |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 1 | 2 | bad | - | - | no |
| 0 | 1 | 3 | bad | - | - | no |
| 0 | 1 | 4 | bad | - | - | no |
| 0 | 2 | 3 | ok | bad | bad | no |
| 0 | 2 | 4 | ok | ok | ok | yes |
| 0 | 3 | 4 | ok | ok | ok | yes |
| ... |  |  |  |  |  |  |

Valid triples are exactly two, matching output 2.

This confirms the pruning logic correctly eliminates any triple containing a forbidden pair.

### Sample 2

Input:

```
8 3
anna bella cindy dora elsa fiona ginny hannah
cindy ginny
cindy hannah
anna cindy
```

Forbidden pairs restrict all triples involving `cindy` heavily. The algorithm still enumerates all combinations, but most are filtered out when checking `bad`.

The valid count accumulates to 41, consistent with systematic enumeration over remaining unconstrained combinations.

This demonstrates that even when one vertex is highly constrained, the algorithm remains correct because it never assumes uniform density, it only checks pairwise validity.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n^3)$ | All unordered triples are enumerated once, each checked in constant time |
| Space | $O(n^2)$ | Boolean matrix stores forbidden relationships between all pairs |

With $n \le 300$, the maximum number of iterations is about 4.5 million, which is well within typical limits in Python when using simple array lookups.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdout.getvalue() if False else solve_capture(inp)

def solve_capture(inp: str) -> str:
    import sys
    input = iter(inp.splitlines()).__next__

    n, m = map(int, input().split())
    name_to_idx = {}
    for i in range(n):
        name_to_idx[input().strip()] = i

    bad = [[False]*n for _ in range(n)]
    for _ in range(m):
        a, b = input().split()
        a = name_to_idx[a]
        b = name_to_idx[b]
        bad[a][b] = bad[b][a] = True

    ans = 0
    for i in range(n):
        for j in range(i+1, n):
            if bad[i][j]:
                continue
            for k in range(j+1, n):
                if not bad[i][k] and not bad[j][k]:
                    ans += 1

    return str(ans % (10**9 + 13))

# provided samples
assert solve_capture("""5 3
anton
borya
vitya
gosha
denis
anton borya
vitya gosha
borya denis
""") == "2"

assert solve_capture("""8 3
anna
bella
cindy
dora
elsa
fiona
ginny
hannah
cindy ginny
cindy hannah
anna cindy
""") == "41"

# minimal case
assert solve_capture("""3 0
a
b
c
""") == "1"

# all forbidden pairs
assert solve_capture("""3 3
a
b
c
a b
a c
b c
""") == "0"

# star constraint
assert solve_capture("""4 3
a
b
c
d
a b
a c
a d
""") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 people, no constraints | 1 | base combinatorics |
| full forbidden triangle | 0 | complete elimination |
| star node | 1 | localized constraints |

## Edge Cases

When $n = 3$ and there are no forbidden pairs, the algorithm checks exactly one triple and accepts it, producing 1. The loop structure naturally handles this without special casing.

When all pairs are forbidden, every triple check fails at the first or second comparison. For example with $i=0, j=1, k=2$, at least one of `bad[i][j]`, `bad[i][k]`, `bad[j][k]` is true, so the counter never increments.

When a single node is incompatible with everyone else, such as `a` forbidden with all others, every triple containing `a` is rejected during the `(i,j)` or later checks. The remaining $n-1$ nodes still form valid triples among themselves, and the enumeration naturally counts only those combinations without modification.
