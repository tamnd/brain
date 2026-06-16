---
title: "CF 928A - Login Verification"
description: "We are given a proposed username and a collection of already-registered usernames. The task is to decide whether the new one is “safe” to use, meaning it is not considered equivalent to any existing username under a set of transformation rules."
date: "2026-06-17T03:06:50+07:00"
tags: ["codeforces", "competitive-programming", "*special", "strings"]
categories: ["algorithms"]
codeforces_contest: 928
codeforces_index: "A"
codeforces_contest_name: "VK Cup 2018 - \u041a\u0432\u0430\u043b\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u044f 1"
rating: 1200
weight: 928
solve_time_s: 77
verified: true
draft: false
---

[CF 928A - Login Verification](https://codeforces.com/problemset/problem/928/A)

**Rating:** 1200  
**Tags:** *special, strings  
**Solve time:** 1m 17s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a proposed username and a collection of already-registered usernames. The task is to decide whether the new one is “safe” to use, meaning it is not considered equivalent to any existing username under a set of transformation rules.

Two usernames are considered equivalent if one can be transformed into the other by repeatedly applying character substitutions. These substitutions define equivalence classes of characters: case changes between uppercase and lowercase letters are always allowed, certain letters and digits can be swapped in specific ways, and some characters are effectively interchangeable through chains of these rules. The key idea is that we are not comparing strings literally, but comparing their canonical meanings under these equivalences.

The input constraints are small: at most 1000 existing usernames, each with length up to 50. This immediately suggests that an O(n · L) approach is sufficient, since even checking every character of every string is only about 50,000 operations. Any solution that preprocesses or normalizes each string independently will easily fit within limits.

A subtle issue arises from ambiguity in the transformation rules. A naive approach might assume only a few direct substitutions matter, but the rules form equivalence chains. For example, if character A can become B and B can become C, then A and C are also equivalent. Ignoring transitive closure leads to incorrect comparisons.

Another pitfall is treating transformations as directional. The rules are explicitly bidirectional, so every substitution must be interpreted as an undirected equivalence relation.

Finally, a careless solution might compare strings character-by-character after a simple normalization like lowercasing. This fails because digit-letter relationships exist (like 0 and O, or 1 and multiple letters), which are not handled by case normalization alone.

## Approaches

The brute-force idea is straightforward: for each existing login, attempt to determine whether it can be transformed into the new login using the allowed character substitutions. This would require running a search or BFS/DFS over character transformations for every pair of strings. Since each string has length up to 50, and there are up to 1000 existing strings, this quickly becomes expensive if we explore transformation states per character position. In the worst case, each character comparison could branch into several alternatives, leading to exponential blowup per comparison.

The key observation is that we do not actually need to simulate transformations. We only need a consistent representation of each character such that two characters are equivalent if and only if they map to the same representative. This turns the problem into a classic equivalence-class construction problem. Once we map every character into a canonical form, every login becomes a normalized string, and we simply check whether any normalized existing login matches the normalized new login.

This reduces the problem from graph search over strings to a simple preprocessing of a finite character set followed by linear comparisons.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Transformation Search | O(n · L · branching) | O(L) | Too slow |
| Canonical Mapping + Comparison | O(n · L + alphabet handling) | O(1) | Accepted |

## Algorithm Walkthrough

We first construct equivalence classes over characters. Since the alphabet is small and fixed (letters, digits, underscore), we can safely hardcode or union-find the relationships implied by the transformation rules.

1. Initialize a disjoint-set union (DSU) structure over all possible characters. Each character starts in its own set because initially we assume no equivalences.
2. For every transformation rule, merge the corresponding characters into the same set. Each merge expresses that two characters are interchangeable in the final representation.
3. After all unions are performed, define a canonical representative for each character, for example the lexicographically smallest character in its set.
4. Convert the new login string into its canonical form by replacing every character with its representative.
5. For each existing login, also convert it into its canonical form using the same mapping.
6. Compare each normalized existing login with the normalized new login.
7. If any match is found, the new login conflicts and we output “No”. Otherwise, we output “Yes”.

The reason this works is that the DSU construction collapses all transitive equivalences into a single class. Any valid transformation sequence between two characters corresponds exactly to them belonging to the same connected component in the equivalence graph. By replacing each character with its component representative, we ensure that all equivalent characters map to the same symbol, and all non-equivalent characters map differently.

## Python Solution

```python
import sys
input = sys.stdin.readline

class DSU:
    def __init__(self):
        self.parent = {}
        self.rank = {}

    def find(self, x):
        if x not in self.parent:
            self.parent[x] = x
            self.rank[x] = 0
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1

# Build equivalence relations according to the problem rules
dsu = DSU()

def add_equiv(a, b):
    dsu.union(a, b)

# case-insensitive letters
for c in "abcdefghijklmnopqrstuvwxyz":
    add_equiv(c, c.upper())
    add_equiv(c.upper(), c)

# 'O' and '0'
add_equiv('O', '0')
add_equiv('0', 'O')

# '1' and {l, I}
add_equiv('1', 'l')
add_equiv('1', 'I')
add_equiv('l', 'I')

# closure is handled by DSU

def normalize(s):
    return ''.join(dsu.find(c) for c in s)

s = input().strip()
n = int(input())
target = normalize(s)

for _ in range(n):
    t = input().strip()
    if normalize(t) == target:
        print("No")
        sys.exit()

print("Yes")
```

The solution builds a union-find structure over characters and merges all pairs that are declared equivalent. The `normalize` function converts any login into its canonical representation by replacing each character with its DSU root. The comparison then becomes exact string equality.

A subtle implementation detail is ensuring that all characters appearing in input are initialized in DSU lazily, since not all symbols are necessarily present in predefined unions. Another important point is that union operations must reflect symmetry explicitly, even if the rules already imply bidirectionality.

## Worked Examples

### Example 1

Input:

```
1_wat
2
2_wat
wat_1
```

We compute canonical representations.

| Step | String | Normalized |
| --- | --- | --- |
| 1 | 1_wat | a form like r1_wat (varies by DSU root choice) |
| 2 | 2_wat | different root for 2 → mismatch |
| 3 | wat_1 | 1 merges with l/I, so matches first |

We compare:

- new login vs "2_wat": mismatch
- new login vs "wat_1": match

So the answer is “Yes”.

This shows how equivalence between digits and letters can create matches that are not obvious from raw strings.

### Example 2

Input:

```
Codeforces
1
codef0rces
```

| Step | String | Normalized |
| --- | --- | --- |
| 1 | Codeforces | unified case folding + O/0 equivalence |
| 2 | codef0rces | 0 becomes O, case differences vanish |

After normalization both strings become identical, so we detect a conflict and output “No”.

This demonstrates why simple case normalization alone is insufficient: digit-letter equivalence is essential.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n · L α(26)) | Each string is scanned once and each character lookup is nearly constant due to DSU path compression |
| Space | O(1) | The character universe is fixed and small |

The constraints allow up to 50,000 character operations, which is trivial. Even with DSU overhead, the solution runs comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    output = []

    class DSU:
        def __init__(self):
            self.parent = {}
            self.rank = {}

        def find(self, x):
            if x not in self.parent:
                self.parent[x] = x
                self.rank[x] = 0
            if self.parent[x] != x:
                self.parent[x] = self.find(self.parent[x])
            return self.parent[x]

        def union(self, a, b):
            ra, rb = self.find(a), self.find(b)
            if ra == rb:
                return
            if self.rank[ra] < self.rank[rb]:
                ra, rb = rb, ra
            self.parent[rb] = ra
            if self.rank[ra] == self.rank[rb]:
                self.rank[ra] += 1

    dsu = DSU()

    for c in "abcdefghijklmnopqrstuvwxyz":
        dsu.union(c, c.upper())
        dsu.union(c.upper(), c)

    dsu.union('O', '0')
    dsu.union('0', 'O')

    dsu.union('1', 'l')
    dsu.union('1', 'I')
    dsu.union('l', 'I')

    def norm(s):
        return ''.join(dsu.find(c) for c in s)

    s = input().strip()
    n = int(input())
    target = norm(s)

    for _ in range(n):
        t = input().strip()
        if norm(t) == target:
            return "No"
    return "Yes"

# provided sample
assert run("1_wat\n2\n2_wat\nwat_1\n") == "Yes"

# same string direct conflict
assert run("a\n1\na\n") == "No"

# case-insensitive match
assert run("Code\n1\ncode\n") == "No"

# digit-letter equivalence
assert run("1\n1\nl\n") == "No"

# underscore unaffected
assert run("a_b\n1\nab\n") == "Yes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| a vs a | No | exact identical matching |
| Code vs code | No | case-insensitivity |
| 1 vs l | No | digit-letter equivalence |
| a_b vs ab | Yes | underscore is not equivalent |

## Edge Cases

A subtle edge case is when equivalence chains span multiple steps. For instance, if a character connects indirectly through several substitutions, a naive pairwise comparison would miss the relationship. The DSU handles this by collapsing transitive connections into a single root. For an input like `l`, existing `I`, and intermediate `1`, all three end up sharing the same representative, so the normalized forms correctly coincide.

Another edge case is mixing case and digit transformations simultaneously. For example, a string containing both `O` and `o` or `0` must still resolve consistently. Since both case-folding and digit-letter unions are applied in the same structure, the final representative is stable regardless of transformation order.

Finally, underscores are isolated symbols with no equivalences. The algorithm never unions them with anything, so they remain fixed points, ensuring strings differing only by underscores are correctly distinguished.
