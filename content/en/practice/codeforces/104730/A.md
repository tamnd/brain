---
title: "CF 104730A - \u0423\u043d\u0438\u043a\u0430\u043b\u044c\u043d\u0430\u044f \u043f\u0435\u0441\u043d\u044f"
description: "We are given two collections of strings, each of size $n$. We must arrange them into a single sequence of length $2n$, but the positions are fixed by parity: every odd position must contain a string from the first collection, and every even position must contain a string from…"
date: "2026-06-29T02:39:10+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104730
codeforces_index: "A"
codeforces_contest_name: "Moscow team school olympiad (MKOSHP) 2023"
rating: 0
weight: 104730
solve_time_s: 71
verified: true
draft: false
---

[CF 104730A - \u0423\u043d\u0438\u043a\u0430\u043b\u044c\u043d\u0430\u044f \u043f\u0435\u0441\u043d\u044f](https://codeforces.com/problemset/problem/104730/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 11s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two collections of strings, each of size $n$. We must arrange them into a single sequence of length $2n$, but the positions are fixed by parity: every odd position must contain a string from the first collection, and every even position must contain a string from the second collection.

After constructing this alternating sequence, we partition it into adjacent pairs $(1,2), (3,4), \dots, (2n-1,2n)$. Each pair contributes a score equal to the length of the longest suffix shared by the two strings in that pair. The goal is to assign strings so that the total sum of these suffix similarities across all pairs is maximized.

A key structural constraint is that we are not free to pair arbitrarily within or across sets. Every element from the first set must be paired with exactly one element from the second set, and the contribution of a pair depends only on their shared suffix structure.

The constraints are large: $n \le 2 \cdot 10^5$, and the total length of all strings across each set is bounded by $2 \cdot 10^5$. This rules out any solution that compares all pairs of strings directly, since even checking all cross pairs would already require up to $O(n^2)$ comparisons.

A subtle pitfall appears when thinking greedily about pairing each string with the best matching candidate independently. A string that shares a long suffix with many others might be repeatedly chosen, blocking better global pairings. For example, if multiple strings end in the same long suffix, pairing them locally without coordination can reduce the total score even if each local choice looks optimal.

The task is therefore a global matching problem over suffix similarity, not a set of independent optimizations.

## Approaches

A direct approach is to compute the suffix similarity for every pair between the first and second set, then solve a weighted bipartite matching problem where edge weights are these suffix lengths. That is correct in principle, since each valid pairing contributes independently. However, the graph is complete bipartite with $n^2$ edges, and computing or even storing these weights is impossible under the constraints.

The key observation is that suffix structure can be encoded incrementally using a trie built on reversed strings. If we reverse all strings, then a suffix becomes a prefix in the reversed representation. This transforms the problem into pairing strings based on longest common prefix (LCP).

In a trie of reversed strings, each node corresponds to a prefix, and strings sharing a long suffix correspond to sharing a deep node in this trie. The contribution of a pair is exactly the depth of their lowest common ancestor in the trie.

Instead of explicitly evaluating all pairs, we process the trie bottom-up. At each node, we combine unmatched strings from the two groups passing through that node. Pairing is always best done as early as possible at the deepest node they share, since deeper nodes represent longer common suffixes. This naturally leads to a greedy matching strategy on the trie, where we propagate counts upward and accumulate matches locally.

The brute-force works because it explicitly compares all pairs and selects an optimal assignment, but fails when $n^2$ interactions become infeasible. The trie-based aggregation replaces pairwise reasoning with structural grouping, reducing the problem to linear traversal over the total string length.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2 \cdot L)$ | $O(n^2)$ | Too slow |
| Trie + Bottom-up matching | ( O(\sum | s | ) ) |

## Algorithm Walkthrough

1. Reverse every string in both sets. This converts suffix matching into prefix matching, allowing us to use a trie structure. The reason this matters is that tries naturally encode shared prefixes as shared paths.
2. Build a single trie containing all reversed strings. At each terminal node, store whether the string came from the first or second set.
3. Perform a depth-first traversal of the trie. At each node, we collect two values from children: how many unmatched strings from set A and set B are present in this subtree.
4. After merging children into the current node, compute how many matches can be formed at this node. If we have $a$ strings from the first set and $b$ from the second set, we can match $\min(a, b)$ pairs at this depth.
5. Add to the answer: $\min(a, b) \times \text{depth}$. This captures the contribution of all pairs whose longest common prefix ends exactly at this node.
6. Propagate the leftovers upward: after matching, pass $|a - b|$ unmatched strings to the parent node, keeping track of which side remains dominant.

### Why it works

Every valid pair of strings has a unique deepest trie node where their paths intersect. That node represents the longest common prefix of the reversed strings, which corresponds exactly to the longest common suffix of the original strings. Matching at that node captures their full contribution. Any attempt to delay matching higher in the trie would only pair strings with shorter common prefixes, reducing the total contribution. Because matching is always performed greedily at the deepest possible point, each unit of flow is accounted for exactly once at its correct depth, ensuring optimality.

## Python Solution

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(10**7)

class Node:
    __slots__ = ("next", "cntA", "cntB")
    def __init__(self):
        self.next = {}
        self.cntA = 0
        self.cntB = 0

def add(root, s, typ):
    v = root
    for ch in s:
        if ch not in v.next:
            v.next[ch] = Node()
        v = v.next[ch]
    if typ == 0:
        v.cntA += 1
    else:
        v.cntB += 1

def dfs(v, depth, res):
    a = v.cntA
    b = v.cntB

    for u in v.next.values():
        da, db = dfs(u, depth + 1, res)
        a += da
        b += db

    m = min(a, b)
    res[0] += m * depth
    a -= m
    b -= m

    return a, b

n = int(input())
root = Node()

for _ in range(n):
    s = input().strip()[::-1]
    add(root, s, 0)

for _ in range(n):
    s = input().strip()[::-1]
    add(root, s, 1)

res = [0]
dfs(root, 0, res)
print(res[0])
```

The solution starts by reversing all strings before inserting them into the trie, ensuring suffix relationships become prefix relationships. Each leaf node increments a counter depending on whether it belongs to the first or second set.

The DFS aggregates counts from children upward. The critical step is the local matching using `min(a, b)` at each node, which represents pairing as many strings as possible with the current prefix. The multiplication by `depth` converts these matches into their actual contribution to the answer.

The return values `a` and `b` represent unmatched strings that could not be paired at deeper nodes and must be considered at higher levels where their common prefix is shorter.

## Worked Examples

### Sample 1

Input sets are:

First set: `dca, cba, dcb, bbb`

Second set: `fea, fea, aba, bbb`

We track aggregation at relevant trie depths.

| Node depth | A count | B count | Matches made | Contribution |
| --- | --- | --- | --- | --- |
| 3 (bbb) | 1 | 1 | 1 | 3 |
| 2 (suffix groups) | 2 | 2 | 2 | 3 × 2 = 4 (cumulative) |
| 1 | 0 | 0 | 0 | 0 |
| root | 0 | 0 | 0 | 0 |

Final sum becomes $6$.

This trace shows that matches are formed greedily at the deepest possible shared suffix nodes, maximizing contribution per pair.

### Sample 2

First set: `a, bc, bcaa`

Second set: `aa, aaa, aaac`

| Node depth | A count | B count | Matches made | Contribution |
| --- | --- | --- | --- | --- |
| 2 ("aa") | 1 | 2 | 1 | 2 |
| 1 | 2 | 1 | 1 | 2 |
| root | 0 | 0 | 0 | 0 |

Total is $4$.

This demonstrates how deeper matches are prioritized before shallower ones, ensuring long suffix overlaps are used whenever possible.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | ( O(\sum | s |
| Space | ( O(\sum | s |

The total number of characters across both sets is bounded by $4 \cdot 10^5$, so the algorithm comfortably fits within time limits. Each operation is linear in the input size, avoiding any quadratic pairing behavior.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    sys.setrecursionlimit(10**7)

    class Node:
        def __init__(self):
            self.next = {}
            self.cntA = 0
            self.cntB = 0

    def add(root, s, typ):
        v = root
        for ch in s:
            if ch not in v.next:
                v.next[ch] = Node()
            v = v.next[ch]
        if typ == 0:
            v.cntA += 1
        else:
            v.cntB += 1

    def dfs(v, depth):
        a = v.cntA
        b = v.cntB
        res = 0
        for u in v.next.values():
            da, db, sub = dfs(u, depth + 1)
            a += da
            b += db
            res += sub
        m = min(a, b)
        res += m * depth
        a -= m
        b -= m
        return a, b, res

    n = int(sys.stdin.readline())
    root = Node()

    for _ in range(n):
        add(root, sys.stdin.readline().strip()[::-1], 0)
    for _ in range(n):
        add(root, sys.stdin.readline().strip()[::-1], 1)

    _, _, ans = dfs(root, 0)
    return str(ans)

# provided samples
assert run("""4
dca
cba
dcb
bbb
fea
fea
aba
bbb
""") == "6"

assert run("""3
a
bc
bcaa
aa
aaa
aaac
""") == "4"

# all-equal
assert run("""2
aaa
aaa
aaa
aaa
""") == "6"

# minimal
assert run("""1
a
a
""") == "1"

# no common suffix except trivial
assert run("""2
ab
cd
ef
gh
""") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all-equal strings | 6 | maximal matching at deepest node |
| single pair | 1 | base case correctness |
| disjoint suffixes | 0 | no false matching |

## Edge Cases

One edge case occurs when all strings in both sets are identical. In that situation, every pair should contribute the full string length. The trie collapses into a single path where both counters accumulate entirely at each depth. At each node, `min(a, b)` extracts matches only at the deepest level first, ensuring every pair is counted exactly once at maximum depth.

Another edge case is when no suffix overlap exists at all. The trie branches immediately at the root, and no deep node contains both types. All `min(a, b)` computations remain zero at positive depth, so the answer remains zero, correctly reflecting that no pair shares a non-empty suffix.
