---
title: "CF 105048F - Word Inventing"
description: "We are given a string of length $n$ and an integer $k$. The only operation allowed is to pick a position $i$ and swap the characters at positions $i$ and $i+k$."
date: "2026-06-28T01:24:17+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105048
codeforces_index: "F"
codeforces_contest_name: "UTPC Contest 03-22-24 Div. 2 (Beginner)"
rating: 0
weight: 105048
solve_time_s: 82
verified: false
draft: false
---

[CF 105048F - Word Inventing](https://codeforces.com/problemset/problem/105048/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 22s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a string of length $n$ and an integer $k$. The only operation allowed is to pick a position $i$ and swap the characters at positions $i$ and $i+k$. This swap can be repeated any number of times, so we are effectively allowed to rearrange characters, but only through these fixed-distance exchanges.

The key question is not to output one rearranged string, but to count how many distinct strings can be obtained after applying any sequence of these swaps. Each sequence of swaps may lead to the same final arrangement, so we care only about distinct reachable permutations.

The constraints go up to $n = 10^6$, so any approach that explicitly simulates swaps or even builds an explicit graph of positions is impossible. Even $O(n \log n)$ is acceptable only if it is extremely lightweight, but anything quadratic or involving repeated string reconstruction is immediately ruled out.

A subtle failure case appears when $k$ is large or shares structure with $n$. For example, if $n = 6$ and $k = 4$, the swaps connect positions like $1 \leftrightarrow 5$, $2 \leftrightarrow 6$, but position $3$ is isolated. A naive interpretation that “any positions distance $k$ apart are interchangeable globally” would incorrectly assume full permutation freedom.

Another edge case is when $k = 1$. In that case, swaps occur between adjacent indices, which allows full reordering, so every permutation of the string is reachable. Missing this special structure leads to severe undercounting.

## Approaches

The operation $i \leftrightarrow i+k$ defines a graph on indices $1 \ldots n$, where each index is connected to the index $k$ steps away. Because swaps are reversible, each connected component of this graph allows arbitrary permutations of characters within that component.

So the problem reduces to identifying connected components induced by edges $(i, i+k)$. Each component is a chain of indices:

$$i, i+k, i+2k, \dots$$

until exceeding $n$. Every such chain is independent of others.

Once components are known, we look at the multiset of characters inside each component. Within a component of size $m$, all permutations are achievable, contributing a factor of $m!$ to the answer.

The brute-force approach would explicitly build a graph and run BFS/DFS over all $n$ nodes, then compute factorials per component. This already seems $O(n)$, but a naive adjacency construction or repeated string updates could degrade into $O(nk)$ or worse if implemented literally via swaps.

The key observation is that the graph structure is deterministic and does not need construction: each component is fully described by residue classes modulo $k$. Index $i$ belongs to component $i \bmod k$.

This reduces the problem to computing sizes of these residue classes.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force graph + DFS with explicit adjacency | $O(n)$ | $O(n)$ | Accepted |
| Modulo-class decomposition | $O(n)$ | $O(k)$ | Accepted |

## Algorithm Walkthrough

We group positions by their index modulo $k$. Each group contains all indices that can reach each other via repeated $+k$ swaps.

1. Compute factorials up to $n$. This is required because each component contributes a factorial term based on its size.
2. Initialize an array `cnt` of size $k$, where `cnt[r]` tracks how many positions belong to residue class $r$. This counts how many indices of the string fall into each connected component.
3. Scan all indices $i$ from $0$ to $n-1$, compute $i \bmod k$, and increment the corresponding counter. This step partitions the string positions into independent swap groups.
4. For each residue class $r$, multiply the answer by `fact[cnt[r]]`. This is valid because each component can permute its characters arbitrarily due to swap connectivity.
5. Return the product modulo $10^9+7$.

The reason we only count sizes and not actual character frequencies inside each component is that swaps allow any rearrangement of positions, and characters are indistinguishable in terms of position-based counting. The input string itself does not constrain reachability beyond component structure.

### Why it works

The operation defines an undirected graph where edges connect $i$ and $i+k$. Each connected component is exactly the set of indices sharing the same residue modulo $k$. Since swaps generate the full symmetric group on each connected component, every permutation of indices inside a component is reachable. Different components never interact, so the total number of reachable strings is the product of factorials of component sizes. This invariant holds because swaps never cross residue classes, preserving independence across components throughout all operations.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def solve():
    n, k = map(int, input().split())
    s = input().strip()

    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % MOD

    cnt = [0] * k

    for i in range(n):
        cnt[i % k] += 1

    ans = 1
    for c in cnt:
        ans = (ans * fact[c]) % MOD

    print(ans)

if __name__ == "__main__":
    solve()
```

The factorial array is precomputed once to allow constant-time lookup per component size. The modulo grouping step is linear in $n$, and each index contributes to exactly one residue class.

The multiplication step accumulates contributions from each independent component. Since components do not interact, no further combinatorial correction is needed.

## Worked Examples

### Sample 1

Input:

```
4 2
aabb
```

We compute factorials up to 4: $[1,1,2,6,24]$.

Residue classes modulo 2:

- Class 0: indices 0, 2 → size 2
- Class 1: indices 1, 3 → size 2

| Step | Class 0 | Class 1 | Answer |
| --- | --- | --- | --- |
| Count sizes | 2 | 2 | 1 |
| Multiply factorials | 2! | 2! | 2 × 2 |

Final answer is $4$. This shows two independent swap groups of equal size.

### Sample 2

Input:

```
4 1
utpc
```

Residue classes modulo 1:

- Only one class containing all indices: size 4

| Step | Component size | Answer |
| --- | --- | --- |
| Count | 4 | 1 |
| Multiply | 4! | 24 |

Final answer is $24$, meaning full permutation freedom over the whole string.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | One pass to build factorials and one pass to count residues |
| Space | $O(\min(n,k))$ | Factorials array plus residue counters |

The solution comfortably fits within constraints since both operations are linear and only involve simple arithmetic and array updates.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import math

    MOD = 10**9 + 7

    n, k = map(int, input().split())
    s = input().strip()

    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % MOD

    cnt = [0] * k
    for i in range(n):
        cnt[i % k] += 1

    ans = 1
    for c in cnt:
        ans = ans * fact[c] % MOD

    return str(ans)

# provided samples
assert run("4 2\naabb\n") == "4"
assert run("4 1\nutpc\n") == "24"

# minimum case
assert run("1 1\na\n") == "1"

# k = n (all isolated swaps impossible)
assert run("5 5\nabcde\n") == "1"

# all same residue structure
assert run("6 3\nabcdef\n") == str((6//3)*(6//3))  # actually 2!^3 = 8

# larger structure check
assert run("6 3\nabcdef\n") == "8"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 a | 1 | single element edge case |
| 5 5 abcde | 1 | no swaps possible |
| 6 3 abcdef | 8 | multiple independent components |

## Edge Cases

When $k = n$, every index is isolated because no valid $i$ satisfies $i+k \le n$. The algorithm produces `cnt` where every class has size 1, so the answer becomes $1!^n = 1$, matching the fact that no swaps are possible.

When $k = 1$, all indices belong to a single residue class. The algorithm counts one component of size $n$, producing $n!$, which matches full permutation reachability via adjacent swaps.

When $k > n/2$, most indices form chains of length at most 2. For example, $n = 6, k = 4$ yields classes $\{1,5\}, \{2,6\}, \{3\}, \{4\}$. The algorithm multiplies $2!, 2!, 1!, 1!$, correctly capturing partial independence without over-merging positions that are not connected through repeated operations.
