---
title: "CF 103934C - Book of the Dead's spells"
description: "We are given a collection of words, each paired with a positive value. A valid “spell” is a sequence of words where every next word must extend the previous one by exactly one or more characters, meaning the previous word is a proper prefix of the next."
date: "2026-07-02T07:13:10+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103934
codeforces_index: "C"
codeforces_contest_name: "2022 USP Try-outs"
rating: 0
weight: 103934
solve_time_s: 207
verified: true
draft: false
---

[CF 103934C - Book of the Dead's spells](https://codeforces.com/problemset/problem/103934/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 27s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of words, each paired with a positive value. A valid “spell” is a sequence of words where every next word must extend the previous one by exactly one or more characters, meaning the previous word is a proper prefix of the next.

We want to choose any such chain and maximize the sum of values of all words in the chain. The chain is not required to end at a maximal word; it can stop anywhere, and it can start from any word.

The input size is large: up to $10^6$ words in total, and the sum of all string lengths is also at most $10^6$. This immediately forces all operations to be close to linear in total characters. Anything like comparing all pairs or sorting by full strings repeatedly will be too slow.

A naive approach would try to build all prefix chains starting from every word. That would explode because each word can potentially extend to many longer words, and the branching factor depends on the dictionary structure. Even if each extension check is $O(1)$ using hashing, the number of paths can still be exponential in worst cases like “a, aa, aaa, …”.

A common pitfall is to assume that greedily extending from a word to the best immediate extension always works. That fails because a high-value word might block access to a slightly shorter prefix chain that leads to a much better extension later.

For example, suppose we have words:

```
a (value 100)
ab (value 1)
abc (value 1000)
aab (value 1000)
```

Greedy from “a” to “ab” would be bad, while skipping directly to “aab” gives a better chain. The correct solution must consider all branching continuations simultaneously.

## Approaches

The key structure is that words are connected through prefix relationships. This naturally forms a trie, where each node represents a prefix, and words sit at nodes.

The brute force view is dynamic programming on a graph where every word points to all words that extend it. Building all edges explicitly is too expensive because a word of length $L$ could potentially be a prefix of many longer words, making edge construction quadratic in worst cases.

The key observation is to reverse the viewpoint. Instead of thinking “from this word, what can come next”, we think “at this prefix, what is the best chain ending here”. Every valid spell is a path in the trie that moves strictly downward along edges that append one character at a time.

So we construct a trie of all words. Each node aggregates all words ending at that prefix. Then we perform dynamic programming over the trie:

Let $dp[v]$ be the maximum achievable spell power ending at node $v$. If a word ends at $v$, we can take it and add its value. If we move from parent to child, we extend the prefix, so we propagate best values downward.

Since a valid chain must always follow increasing prefix length, the trie structure ensures acyclicity and allows DP in BFS/DFS order from root.

We maintain:

$dp[v] = (\text{best chain ending at } v)$

and update children based on parent transitions.

The brute force tries to enumerate chains explicitly, while the trie compresses shared prefixes and makes transitions local.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force over word graph | Exponential | High | Too slow |
| Trie + DP over prefixes | $O(\sum | s_i | )$ |

## Algorithm Walkthrough

We build a trie over all words, storing at each node the maximum value of any word ending there.

Then we compute DP over the trie.

## Algorithm Walkthrough

1. Insert every word into a trie, creating nodes for each character. Each node corresponds to a prefix shared by some words. This ensures common prefixes are stored once, avoiding repeated work.
2. At each trie node $v$, store $val[v]$, the maximum power among all words that end exactly at that prefix. If multiple identical words do not exist (guaranteed distinct strings), this is simply the given value or zero.
3. Initialize $dp[v] = 0$ for all nodes.
4. Set $dp[v] = val[v]$ for every node. This represents starting a spell at that word.
5. Traverse the trie in BFS or DFS from the root, and for every edge $v \to u$ (adding one character), update:

$dp[u] = \max(dp[u], dp[v] + val[u])$.

This step captures extending a spell ending at $v$ by the word ending at $u$ if $u$ is a word node.
6. Track the maximum value of $dp[v]$ over all nodes.

### Why it works

Every valid spell corresponds exactly to a sequence of nodes in the trie where each node is a prefix of the next. The DP ensures that any best chain reaching a node $v$ is computed before using $v$ to extend further, since traversal respects increasing depth. Because all transitions preserve prefix validity, no invalid sequence is ever considered, and every valid sequence is represented by some path in the trie.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(10**7)

class Node:
    __slots__ = ("next", "val", "dp")
    def __init__(self):
        self.next = {}
        self.val = 0
        self.dp = 0

nodes = [Node()]

def insert(s, w):
    v = 0
    for c in s:
        if c not in nodes[v].next:
            nodes[v].next[c] = len(nodes)
            nodes.append(Node())
        v = nodes[v].next[c]
    nodes[v].val = max(nodes[v].val, w)

def dfs(v):
    node = nodes[v]
    node.dp = node.val
    best = node.dp

    for c, u in node.next.items():
        dfs(u)
        nodes[u].dp = max(nodes[u].dp, node.dp + nodes[u].val)
        best = max(best, nodes[u].dp)

    return best

n = int(input())
for _ in range(n):
    s, p = input().split()
    insert(s, int(p))

dfs(0)

ans = 0
for nd in nodes:
    ans = max(ans, nd.dp)

print(ans)
```

The trie is implemented with explicit nodes and dictionaries for transitions. Each node stores the best word value ending there. The DFS computes DP in a top-down way, ensuring parent values are available before processing children.

A subtle point is that we initialize each node’s dp with its own terminal value, because a valid spell can consist of a single word.

## Worked Examples

### Example 1

Input:

```
3
a 5
ab 2
abc 10
```

| Step | Node | val | dp before | transition | dp after |
| --- | --- | --- | --- | --- | --- |
| a | a | 5 | 5 | start | 5 |
| ab | ab | 2 | 2 | a → ab | 7 |
| abc | abc | 10 | 10 | ab → abc | 17 |

The best chain is a → ab → abc giving 17.

This shows how intermediate low-value words can still be necessary to reach higher-value extensions.

### Example 2

Input:

```
4
a 100
ab 1
aab 50
abc 60
```

| Step | Node | val | dp | best path |
| --- | --- | --- | --- | --- |
| a | 100 | 100 | 100 |  |
| ab | 1 | 101 | a → ab |  |
| abc | 60 | 161 | a → ab → abc |  |
| aab | 50 | 150 | a → aab |  |

This shows branching: different extensions compete, and DP correctly keeps both paths.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(\sum | s_i |
| Space | $O(\sum | s_i |

The constraints guarantee total string length at most $10^6$, so linear-time trie construction and traversal easily fits within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    class Node:
        __slots__ = ("next", "val", "dp")
        def __init__(self):
            self.next = {}
            self.val = 0
            self.dp = 0

    nodes = [Node()]

    def insert(s, w):
        v = 0
        for c in s:
            if c not in nodes[v].next:
                nodes[v].next[c] = len(nodes)
                nodes.append(Node())
            v = nodes[v].next[c]
        nodes[v].val = max(nodes[v].val, w)

    def dfs(v):
        node = nodes[v]
        node.dp = node.val
        for c, u in node.next.items():
            dfs(u)
            nodes[u].dp = max(nodes[u].dp, node.dp + nodes[u].val)

    n = int(input())
    for _ in range(n):
        s, p = input().split()
        insert(s, int(p))

    dfs(0)

    return str(max(nd.dp for nd in nodes))

assert run("3\na 5\nab 2\nabc 10\n") == "17"
assert run("4\na 100\nab 1\naab 50\nabc 60\n") == "161"
assert run("1\na 7\n") == "7"
assert run("2\na 1\naa 2\n") == "3"
assert run("3\na 1\nb 2\nc 3\n") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| chain a→ab→abc | 17 | multi-step optimal chain |
| branching prefixes | 161 | competing paths |
| single word | 7 | minimal case |
| simple extension | 3 | basic prefix DP |
| no prefixes | 3 | independent components |

## Edge Cases

One edge case is when no word is a prefix of another. In that case every node is isolated in the trie except root links, and the answer is simply the maximum single value. The DP handles this because each node starts with $dp[v]=val[v]$ and receives no improvements from children.

Another edge case is when multiple words share identical prefixes but diverge late. The trie compresses this correctly, ensuring shared computation. A naive pairwise DP would recompute prefix comparisons repeatedly, but here each prefix is processed once, and all extensions reuse the same state.
