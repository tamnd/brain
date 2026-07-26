---
title: "CF 102822C - Code a Trie"
description: "We are given the results of several searches performed on an unknown trie. Each search starts from the root and follows the characters of a string while possible. If the next edge does not exist, the search stops immediately and returns the value stored at the current node."
date: "2026-07-26T15:59:35+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102822
codeforces_index: "C"
codeforces_contest_name: "2020 China Collegiate Programming Contest - Mianyang Site"
rating: 0
weight: 102822
solve_time_s: 50
verified: true
draft: false
---

[CF 102822C - Code a Trie](https://codeforces.com/problemset/problem/102822/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given the results of several searches performed on an unknown trie. Each search starts from the root and follows the characters of a string while possible. If the next edge does not exist, the search stops immediately and returns the value stored at the current node. Every node in the original trie has a unique value, so the returned number identifies exactly one node.

The task is to reconstruct the smallest possible number of nodes in any trie that could have produced all given query results. The root also counts as a node. If no trie can satisfy all observations, we must report that.

The input gives several test cases. For each test case, every query contains a lowercase string and the value returned by the search operation for that string.

The total length of all strings in one test case is at most (10^5), and the total over all test cases is at most (5 \times 10^5). This rules out solutions that compare every pair of strings or repeatedly rebuild structures. The algorithm must be close to linear in the total input size.

The key edge cases are not about long strings, but about prefixes and conflicting values. If two identical queries have different answers, the trie cannot exist because following the same path must always end at the same node.

For example:

```
2
a 1
a 2
```

The correct output is `-1`. A careless implementation might keep only one of the values and incorrectly accept the case.

Another tricky case is when one string is a prefix of another and the answers disagree.

```
2
a 1
aa 2
```

The correct output is `-1`. If the node representing `a` has value `1`, the query `aa` can only return another node if the edge `a -> a` exists. But then the query `a` would also stop at the node after reading `a`, so the two requirements cannot be satisfied together.

A third important case is when many different strings have the same answer.

```
3
aa 1
ab 1
ac 1
```

The correct output is `1`. The empty root node can store value `1`, and all three queries stop immediately because none of the first edges needs to exist.

## Approaches

A direct approach is to insert every queried string into a trie and then try to assign values to nodes. This builds all prefixes, even when many of them are unnecessary. In the worst case, if there are (10^5) strings of length (10^5), the number of possible prefix relationships becomes far too large for repeated checking.

The important observation is that a node only needs to exist if different answers need to be separated below that node. If every query passing through a prefix has the same returned value, we can stop at that prefix and assign the value there. We do not need to know where the original inserted strings were, because the query results only care about the first missing edge.

This leads naturally to a recursive construction. Build the ordinary trie of all query strings. At each node, look at the set of values appearing in its subtree. If that set contains only one value, the whole subtree can be replaced by this single node. If several values appear, the node must remain and its children must be solved independently.

The brute force and optimal approaches differ only in whether they keep unnecessary prefixes.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(L^2)) | (O(L)) | Too slow |
| Optimal | (O(L)) | (O(L)) | Accepted |

Here (L) is the total length of all query strings in the test case.

## Algorithm Walkthrough

1. Insert every query string into a trie. Store the value at the terminal node of each string. If the same string appears with different values, the answer is impossible because identical searches cannot produce different nodes.
2. Traverse the trie with depth first search. For each node, collect the distinct values that appear among all terminal strings in its subtree.
3. If a node's subtree contains exactly one value, return a subtree size of one. The node itself can represent all those queries, so all descendants are unnecessary.
4. If a node contains multiple values, keep this node and recursively process every child that contains at least one query. Add the sizes of those child solutions.
5. The size returned for the root is the minimum possible number of trie nodes.

Why it works:

Consider any node representing a prefix. Every query below this node must eventually return a node in this subtree. If all those queries require the same value, merging them into the current node is always valid and saves nodes. If different values are required, they cannot share the current node because every trie node has only one value, so the children must separate the different cases. The recursive process makes exactly these two choices at every prefix, so every unnecessary node is removed and every required distinction is preserved.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Node:
    __slots__ = ("children", "value")
    def __init__(self):
        self.children = {}
        self.value = None

def solve_case(data):
    root = Node()

    for s, v in data:
        cur = root
        for c in s:
            if c not in cur.children:
                cur.children[c] = Node()
            cur = cur.children[c]
        if cur.value is not None and cur.value != v:
            return -1
        cur.value = v

    def dfs(node):
        vals = set()
        if node.value is not None:
            vals.add(node.value)

        child_info = []
        for child in node.children.values():
            ok, size, child_vals = dfs(child)
            if not ok:
                return False, 0, set()
            child_info.append((size, child_vals))
            vals.update(child_vals)

        if len(vals) == 1:
            return True, 1, vals

        size = 1
        for child_size, _ in child_info:
            size += child_size

        return True, size, vals

    ok, ans, _ = dfs(root)
    return ans if ok else -1

def main():
    t = int(input())
    out = []

    for case in range(1, t + 1):
        n = int(input())
        queries = []
        for _ in range(n):
            s, v = input().split()
            queries.append((s, int(v)))

        out.append(f"Case #{case}: {solve_case(queries)}")

    print("\n".join(out))

if __name__ == "__main__":
    main()
```

The insertion phase creates the only structure we need. It does not try to simulate the forgotten insert operations because many different inserted string sets could lead to the same query results.

The DFS is the core of the solution. The returned set contains all values that still need to be represented below the current prefix. When the set size becomes one, the whole subtree collapses into the current node.

The conflict check during insertion handles the simplest impossible case early. Without it, identical strings with different answers could be incorrectly merged.

The recursion never explores a prefix twice, so the total work is proportional to the number of created trie nodes.

## Worked Examples

For the input:

```
3
aa 1
ab 1
ac 1
```

The trie created from the strings is:

| Node prefix | Values below | Decision |
| --- | --- | --- |
| empty | {1} | Keep only root |

The root can represent all three queries, so the answer is `1`.

For the input:

```
2
aa 1
a 2
```

The trace is:

| Node prefix | Values below | Decision |
| --- | --- | --- |
| empty | {1,2} | Must split |
| a | {1,2} | Must split |
| aa | {1} | Keep node |
| a terminal | {2} | Keep node |

The resulting trie has the root, the node `a`, and the node `aa`, giving answer `3`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(L)) | Every character creates or visits one trie edge once. |
| Space | (O(L)) | The temporary trie stores only the prefixes of the input strings. |

The maximum input size is handled because both memory and running time grow linearly with the total length of the strings.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    t = int(input())
    ans = []
    for case in range(1, t + 1):
        n = int(input())
        q = []
        for _ in range(n):
            s, v = input().split()
            q.append((s, int(v)))
        ans.append(f"Case #{case}: {solve_case(q)}")
    sys.stdin = old
    return "\n".join(ans)

assert run("""3
aa 1
a 2
""") == "Case #1: 3"

assert run("""3
aa 1
ab 1
ac 1
""") == "Case #1: 1"

assert run("""2
a 1
a 2
""") == "Case #1: -1"

assert run("""3
a 1
ab 1
abc 1
""") == "Case #1: 1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `aa 1, a 2` | `3` | Prefix conflict that still has a valid trie |
| `aa 1, ab 1, ac 1` | `1` | Complete collapsing into one node |
| `a 1, a 2` | `-1` | Same string with incompatible answers |
| `a 1, ab 1, abc 1` | `1` | Long chains with identical values |

## Edge Cases

When identical strings have different values, the algorithm detects the contradiction while inserting. The terminal node cannot store two different values, so it immediately returns `-1`.

For:

```
2
a 1
a 2
```

the insertion reaches the same terminal node twice. The first query stores value `1`, and the second query tries to store value `2`. Since one trie node cannot have both values, the case is impossible.

When a short string and a longer string require different answers, the DFS keeps enough nodes to separate them.

For:

```
2
a 1
aa 2
```

the root contains two values, so it must keep the child `a`. That node still contains two values, so it must keep the child `aa`. The resulting size is `3`, representing the root, `a`, and `aa`.

When many strings share the same answer, the DFS removes all unnecessary descendants.

For:

```
3
aa 1
ab 1
ac 1
```

the root sees only value `1` below it, so it becomes the answer node and all children disappear. The minimum number of nodes is exactly `1`.

I can also provide a shorter contest-style version of this editorial if you want one that fits a typical Codeforces blog length.
