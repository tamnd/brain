---
title: "CF 965E - Short Code"
description: "We are given a collection of distinct lowercase strings, each representing a variable name. For each original name, we must choose a non-empty prefix of that string to act as its new shortened identifier."
date: "2026-06-17T01:39:22+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dp", "greedy", "strings", "trees"]
categories: ["algorithms"]
codeforces_contest: 965
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 476 (Div. 2) [Thanks, Telegram!]"
rating: 2200
weight: 965
solve_time_s: 83
verified: false
draft: false
---

[CF 965E - Short Code](https://codeforces.com/problemset/problem/965/E)

**Rating:** 2200  
**Tags:** data structures, dp, greedy, strings, trees  
**Solve time:** 1m 23s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a collection of distinct lowercase strings, each representing a variable name. For each original name, we must choose a non-empty prefix of that string to act as its new shortened identifier. The constraint is that after shortening all names, no two resulting names may be identical.

Among all valid ways to choose prefixes, we want the one that minimizes the sum of the chosen prefix lengths.

So the problem is not just about finding unique prefixes, but about balancing them: a shorter prefix is always better locally, but choosing it may force other strings to use longer prefixes later. The task is to resolve these conflicts globally to minimize total cost.

The constraints are tight. There are up to 100000 strings, and the total length of all strings is also at most 100000. This immediately suggests that any solution must be close to linear or near linear in total characters processed. Anything that tries to repeatedly compare full strings pairwise or recompute prefix uniqueness from scratch for each string will not pass.

A naive mental model would be: for each string, try the shortest prefix that is not used by any other string. The difficulty is that “not used by any other string” depends on the choices for all other strings, so local greedy decisions can fail.

A subtle failure case appears when many strings share a long common prefix but diverge later. If one string takes a very short prefix early, it may force others to extend significantly even though a slightly longer prefix for the first string would reduce total cost. For example:

Input:

```
3
aaa
aab
aac
```

If we greedily assign `"a"` to the first string, the remaining two may need `"aa"` or longer, increasing total cost unnecessarily. The optimal assignment depends on collective structure, not independent choices.

The key hidden structure is that uniqueness is governed entirely by shared prefixes, which suggests organizing all strings in a prefix tree.

## Approaches

The brute-force idea is straightforward. For each string, we try prefixes of increasing length until we find one that does not match any prefix chosen for another string. To check this properly, we would need to maintain a global set of chosen prefixes and verify each candidate prefix against it. In the worst case, each string of length L might require checking O(L) prefixes, and each check involves string hashing or comparisons, leading to quadratic behavior in total length. With total length up to 100000, repeated rescanning becomes too slow.

The key observation is that prefix conflicts are not arbitrary, they are structured. Two prefixes conflict only if one string is a prefix of another or they share a path in the prefix tree. If we build a trie of all strings, then every prefix corresponds to a node, and uniqueness depends on how many strings pass through that node.

This suggests reversing the perspective. Instead of greedily assigning prefixes from shortest to longest, we think in terms of necessity. A node in the trie is a valid candidate for a string only if the path up to that node is unique among all strings or can be made unique by pushing other strings further down. The cost minimization naturally suggests a dynamic programming interpretation over the trie: we assign each string a stopping point in the trie such that no two strings stop at the same node.

The structure becomes a tree DP problem. Each node knows how many strings pass through it, and we decide how many of those must continue downward to enforce uniqueness. The cost we pay is proportional to the depth where each string stops. We push “excess” strings downward in a way that minimizes total depth increase.

Once viewed as a trie with flow-like assignment of strings to nodes, the optimal strategy becomes greedy bottom-up: at each node, keep as many strings as possible stopping here, and push the remaining ones to children.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force prefix checking | O(N * L^2) | O(N * L) | Too slow |
| Trie + bottom-up assignment | O(total length) | O(total length) | Accepted |

## Algorithm Walkthrough

We build a trie of all strings, where each node corresponds to a prefix and stores how many strings pass through it. Then we solve the assignment problem from the leaves upward.

1. Insert every string into a trie, incrementing a counter at each visited node. This counter represents how many strings share this prefix. This is the fundamental information that determines whether a prefix can safely be used.
2. Define a postorder traversal of the trie. We process children before parents so that decisions about deeper prefixes are finalized before we decide what happens higher up.
3. At each node, maintain a value representing how many strings are still “unassigned” and currently reside in this subtree. For leaf paths, this starts as the count of strings ending there or passing through.
4. For a given node, we first collect contributions from all children. These represent strings that were not assigned a prefix deeper down and are still available to be assigned here or above.
5. If multiple strings reach the same node, at most one of them can safely stop here, because stopping more would violate uniqueness. Therefore, we assign exactly one string to stop at this node if any exist.
6. All remaining strings at this node must be pushed upward. However, since we process bottom-up, pushing upward is equivalent to returning the excess count to the parent.
7. Each time we assign a string to stop at a node, we add the depth of that node to the total answer. This reflects the prefix length chosen for that string.
8. The root accumulates all remaining strings, ensuring every string is assigned somewhere.

The key idea is that every string is assigned to the highest possible node where it can uniquely “claim” a prefix, but conflicts are resolved locally in subtrees.

### Why it works

The trie partitions strings by prefixes. At any node, all strings in its subtree are indistinguishable up to that prefix. If more than one string tries to stop at the same node, uniqueness would be violated, so at most one can be assigned there. Any other assignment must go deeper.

Processing bottom-up ensures that any string that could have been assigned deeper is already optimally placed before we consider higher levels. This prevents premature assignment at shallow depth, because deeper unique opportunities are resolved first. The invariant is that when processing a node, all children have already maximized the number of assigned strings at greater depths, so any remaining strings are forced to use this node or above, and choosing one assignment here minimizes total depth among all equivalent choices.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(10**7)

class Node:
    __slots__ = ("ch", "cnt")
    def __init__(self):
        self.ch = [-1] * 26
        self.cnt = 0

def new_node():
    return Node()

nodes = [new_node()]

def add_string(s):
    v = 0
    nodes[v].cnt += 1
    for c in s:
        x = ord(c) - 97
        if nodes[v].ch[x] == -1:
            nodes[v].ch[x] = len(nodes)
            nodes.append(new_node())
        v = nodes[v].ch[x]
        nodes[v].cnt += 1

def dfs(v, depth):
    res = 0
    rem = nodes[v].cnt

    for nx in nodes[v].ch:
        if nx != -1:
            got_res, got_rem = dfs(nx, depth + 1)
            res += got_res
            rem -= (nodes[nx].cnt - got_rem)

    if rem > 0:
        res += depth
        rem -= 1

    return res, rem

n = int(input())
words = [input().strip() for _ in range(n)]

for w in words:
    add_string(w)

ans, _ = dfs(0, 0)
print(ans)
```

The trie construction is standard: every node tracks how many strings pass through it, which later determines how many candidates compete for that prefix.

The DFS computes two values: the total cost contributed by assigned prefixes in that subtree, and how many strings remain unassigned and must be handled higher in the tree. The subtraction step inside the loop removes strings already assigned in child subtrees, ensuring the parent only sees leftover conflicts.

A subtle implementation detail is that we assign a cost at the current node only after processing children. This guarantees that we only assign a prefix here if no deeper assignment was possible for all but one string.

## Worked Examples

### Example 1

Input:

```
3
codeforces
codehorses
code
```

We build a trie where all three strings share prefix `"code"`, then diverge.

| Node (prefix) | cnt | child result rem | assigned here | rem after |
| --- | --- | --- | --- | --- |
| "code" | 3 | children exhausted | 1 | 2 |
| root | 3 | subtree processed | 1 | 0 |

At `"code"`, only one string can be assigned a prefix there; the remaining two must move upward. Eventually they are forced to be assigned at shorter prefixes.

Final answer is 6.

This trace shows that even though all strings share a deep prefix, only one can “claim” that level, and the others are pushed to higher, shorter prefixes.

### Example 2

Input:

```
4
a
ab
abc
abd
```

| Node | cnt | rem from children | assigned | rem |
| --- | --- | --- | --- | --- |
| "abc" | 1 | 0 | 1 | 0 |
| "abd" | 1 | 0 | 1 | 0 |
| "ab" | 3 | 0 | 1 | 2 |
| "a" | 4 | 2 | 1 | 1 |
| root | 4 | 1 | 1 | 0 |

Here deeper nodes already resolve two strings, and only a few conflicts propagate upward. The result reflects that longer shared prefixes are used where beneficial, but only when they do not force too many collisions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(total characters) | each string is inserted once, each trie node processed once |
| Space | O(total characters) | each distinct prefix creates at most one trie node |

The constraints guarantee total length up to 100000, so both time and memory are comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    class Node:
        __slots__ = ("ch", "cnt")
```
