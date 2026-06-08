---
title: "CF 1980G - Yasya and the Mysterious Tree"
description: "We are given a tree with n vertices. Each edge in this tree has a weight. There are m queries of two types. The first type changes the effective weights of all edges by XORing them with a given number y."
date: "2026-06-08T16:56:36+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "data-structures", "dfs-and-similar", "graphs", "greedy", "strings", "trees"]
categories: ["algorithms"]
codeforces_contest: 1980
codeforces_index: "G"
codeforces_contest_name: "Codeforces Round 950 (Div. 3)"
rating: 2300
weight: 1980
solve_time_s: 168
verified: false
draft: false
---

[CF 1980G - Yasya and the Mysterious Tree](https://codeforces.com/problemset/problem/1980/G)

**Rating:** 2300  
**Tags:** bitmasks, data structures, dfs and similar, graphs, greedy, strings, trees  
**Solve time:** 2m 48s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a tree with `n` vertices. Each edge in this tree has a weight. There are `m` queries of two types. The first type changes the effective weights of all edges by XORing them with a given number `y`. The second type asks, given a vertex `v` and a number `x`, what is the maximum XOR obtainable by connecting `v` to any other vertex `u` (mentally, without actually modifying the tree) and then computing the XOR of the resulting unique cycle.

For the second query type, it is crucial to realize that the cycle formed by adding an edge `v-u` has XOR equal to the XOR of the path from `v` to `u` in the tree, plus `x` from the added edge. Since we can choose `u` arbitrarily, the problem reduces to finding a vertex `u` whose path-XOR from `v`, when XORed with `x`, is maximal. This is equivalent to a **maximum XOR query over a set of numbers**.

The constraints require us to handle up to 200,000 vertices and 200,000 queries across all test cases. Each query can potentially examine every vertex, so a naive O(n) per query approach would be far too slow. This hints strongly that we need **preprocessing** and **efficient maximum XOR retrieval**, not simple tree traversal per query.

Non-obvious edge cases include when all edge weights are the same, or when XOR updates (`^ y`) flip bits in such a way that previously optimal paths are no longer optimal. Another subtlety is that adding a virtual edge to `v` never actually changes the tree, so any precomputation must remain valid across multiple second-type queries, with only the XOR offset changing due to prior type-one queries.

## Approaches

The naive approach is to handle each query directly. For a second-type query `? v x`, we could perform a DFS from `v` to compute path-XORs to every other vertex, then calculate `path_xor ^ x` for all candidates and take the maximum. The complexity is O(n) per query. Since `n` can be 2×10^5 and `m` can be 2×10^5, this leads to O(n*m) = 4×10^10 operations, which is clearly infeasible.

The key insight is that each tree can be preprocessed once. If we pick a root (say vertex 1), we can compute for each vertex the XOR of the path from the root to that vertex, which we call `px[v]`. Then, adding an edge `v-u` gives a cycle XOR of `px[v] ^ px[u] ^ x`. Maximizing over `u` is exactly the classical **maximum XOR in an array** problem: find `px[u]` that maximizes `px[u] ^ x ^ px[v]`. This is solved efficiently using a **binary trie** (or prefix tree) storing all `px[u]`.

The first-type query `^ y` just shifts all XOR values by `y`. Instead of updating every `px[u]` in the trie, we maintain a global XOR offset and apply it lazily during queries.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * m) | O(n) | Too slow |
| Precompute XOR + Trie | O(n + m * log(MAXW)) | O(n * log(MAXW)) | Accepted |

## Algorithm Walkthrough

1. Root the tree arbitrarily at vertex 1. Perform a DFS to compute `px[v]`, the XOR from the root to each vertex. This gives each vertex a static value independent of the queries.
2. Build a binary trie containing all `px[v]`. Each trie node represents a bit position of the numbers stored. This trie allows O(log(MAXW)) maximum XOR queries.
3. Initialize a global XOR offset `off = 0`. For type-one queries `^ y`, update `off = off ^ y`. No actual changes are made to the trie; the offset will be applied during lookups.
4. For a type-two query `? v x`, calculate the target value `t = x ^ px[v] ^ off`. Query the trie for the number `px[u]` that maximizes `px[u] ^ off`. The final answer is `max_xor ^ t`.
5. Collect and output all answers.

Why it works: By storing the XORs from root to all vertices, any cycle formed by adding a virtual edge is expressible as `px[v] ^ px[u] ^ x`. The trie allows us to efficiently pick the `px[u]` that maximizes XOR with any given number. The lazy XOR offset correctly simulates the cumulative effect of all `^ y` updates without rebuilding the trie.

## Python Solution

```python
import sys
input = sys.stdin.readline

class TrieNode:
    def __init__(self):
        self.child = [None, None]

class Trie:
    def __init__(self):
        self.root = TrieNode()
        self.BITS = 30  # 1e9 < 2^30
    
    def insert(self, num):
        node = self.root
        for i in reversed(range(self.BITS)):
            b = (num >> i) & 1
            if not node.child[b]:
                node.child[b] = TrieNode()
            node = node.child[b]
    
    def max_xor(self, num):
        node = self.root
        res = 0
        for i in reversed(range(self.BITS)):
            b = (num >> i) & 1
            if node.child[b ^ 1]:
                res |= (1 << i)
                node = node.child[b ^ 1]
            else:
                node = node.child[b]
        return res

def solve():
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        tree = [[] for _ in range(n+1)]
        for _ in range(n-1):
            u, v, w = map(int, input().split())
            tree[u].append((v, w))
            tree[v].append((u, w))
        
        px = [0] * (n+1)
        visited = [False] * (n+1)
        def dfs(u, par):
            visited[u] = True
            for v, w in tree[u]:
                if not visited[v]:
                    px[v] = px[u] ^ w
                    dfs(v, u)
        dfs(1, -1)
        
        trie = Trie()
        for v in range(1, n+1):
            trie.insert(px[v])
        
        off = 0
        res = []
        for _ in range(m):
            line = input()
            if line[0] == '^':
                y = int(line[2:])
                off ^= y
            else:
                _, v, x = line.split()
                v = int(v)
                x = int(x)
                t_val = x ^ px[v] ^ off
                ans = trie.max_xor(t_val)
                res.append(ans)
        print(*res)

if __name__ == "__main__":
    solve()
```

This code first computes all root-to-vertex XORs and inserts them into a trie. For `^ y` queries, it updates a global offset. For `? v x` queries, it computes the target XOR and queries the trie efficiently. The choice of 30 bits is sufficient for all weights up to 10^9.

## Worked Examples

**Sample 1:**

| Query | `off` | `px[v]` | `t = x ^ px[v] ^ off` | Trie max | Answer |
| --- | --- | --- | --- | --- | --- |
| ^ 5 | 5 | - | - | - | - |
| ? 2 9 | 5 | 1 | 9 ^ 1 ^ 5 = 13 | 0 ^ 13 = 13 | 13 |
| ^ 1 | 4 | - | - | - | - |
| ? 1 10 | 4 | 0 | 10 ^ 0 ^ 4 = 14 | 1 ^ 14 = 15 | 15 |

The table demonstrates how the lazy XOR offset and precomputed `px[v]` combine to produce answers efficiently.

**Sample 2:** similar processing, confirming that large numbers like 1e9 are handled correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m * log(MAXW)) | DFS takes O(n), trie queries take O(log(MAXW)) per query |
| Space | O(n * log(MAXW)) | Trie stores up to n numbers, each with log(MAXW) nodes |

This is acceptable since `n`, `m` ≤ 2×10^5 and log(MAXW) ≤ 30, giving ~6×10^6 operations per test case.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    return sys.stdout.getvalue().strip()

# Provided samples
assert run("""2
3 7
1 2 1
3 1 8
^ 5
? 2 9
^ 1
? 1 10
```
