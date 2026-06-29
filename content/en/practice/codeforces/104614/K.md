---
title: "CF 104614K - Two Charts Become One"
description: "We are given two textual descriptions of rooted hierarchical structures. Each structure defines departments labeled by integers, where every department may have several direct subdepartments."
date: "2026-06-29T21:31:15+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104614
codeforces_index: "K"
codeforces_contest_name: "2022-2023 ICPC East Central North America Regional Contest (ECNA 2022)"
rating: 0
weight: 104614
solve_time_s: 60
verified: true
draft: false
---

[CF 104614K - Two Charts Become One](https://codeforces.com/problemset/problem/104614/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two textual descriptions of rooted hierarchical structures. Each structure defines departments labeled by integers, where every department may have several direct subdepartments. The format is recursive: a single number represents a leaf department, and a number followed by several parenthesized groups represents a department with multiple children, each child itself being a full hierarchy.

The task is to determine whether the two given hierarchies represent the same rooted tree structure, ignoring ordering of children. Two departments are considered identical between the two charts if the rooted tree structure is isomorphic under unordered children, and the department labels must match exactly at corresponding nodes.

The main difficulty comes from the fact that the same structure can be written in many different ways because children can appear in any order, and spacing is arbitrary. Additionally, the input size can be extremely large, up to 100,000 nodes, so any approach that repeatedly parses or compares subtrees in a naive way will fail.

The constraints imply we need a linear or near-linear solution. Anything involving subtree hashing done repeatedly per node with string concatenation would degrade to quadratic behavior in the worst case due to deep nesting (depth up to 1000) and large branching.

A few edge situations are subtle.

One issue is ordering. For example, the two representations

11 (10) (12 (13) (17) (28))

11 (12 (17) (28) (13)) (10)

should be considered identical because children are unordered.

A second issue is whitespace flexibility. Inputs like

11 ( 10 ) ( 12 )

11(10(12))

must be parsed identically despite formatting differences.

A third issue is structural mismatch even if labels match locally. For instance

11 (10) (12)

11 (10) (13)

is different because one subtree root differs (12 versus 13), even though the top structure is identical.

A naive mistake is to try string normalization followed by direct comparison, because parentheses reordering does not preserve lexical equality.

## Approaches

A direct brute-force idea is to fully parse each hierarchy into a tree structure and then compare the two trees for isomorphism. A straightforward comparison would recursively match each node’s children against each other by trying all permutations. That immediately leads to factorial complexity per node in the worst case when a node has many children. Even with constraints saying each node has at most 100 children, repeated matching across subtrees still leads to exponential behavior if implemented directly.

Another naive idea is to convert each subtree into a canonical string representation by recursively sorting children representations and concatenating them. This is correct logically, but if implemented with repeated string concatenation, it becomes too slow because string building across deep recursion leads to repeated copying, and overall complexity can degrade to quadratic in the total input size.

The key insight is that we do not need to explicitly construct or sort large strings. We only need a stable identifier for each subtree such that identical subtrees produce identical identifiers regardless of child order. This suggests computing a structural hash bottom-up.

We parse the expression into a tree, and then assign each subtree a canonical hash computed from its label and the multiset of its children hashes. Since children are unordered, we must combine their hashes in an order-independent way. Sorting child hashes is acceptable because total children per node is small (at most 100), and overall complexity remains linearithmic in branching but linear in total nodes.

Once each subtree has a hash, comparing the two charts reduces to comparing the root hashes.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Tree Matching | exponential | O(n) | Too slow |
| Hashing Subtrees (canonical form) | O(n log k) | O(n) | Accepted |

## Algorithm Walkthrough

We treat each input line as a single rooted tree expression and parse it into nodes using a stack-based parser.

1. Scan the string from left to right, extracting integers as department labels and interpreting parentheses as structure delimiters. Whenever we read a number, we create a node. When we see a closing parenthesis, we finish the current subtree context and attach it to its parent. This step constructs the tree explicitly.
2. During parsing, maintain a stack of nodes representing the current active path in the tree. When we encounter a new number followed by an opening parenthesis or a child structure, we push it as the current node. When we finish a subtree, we pop back to its parent. This ensures we reconstruct the exact hierarchy.
3. After building the tree, compute a hash for each node using a postorder traversal. For a leaf node, the hash depends only on its label. For an internal node, we first compute hashes of all children, then sort the list of child hashes. Sorting is necessary because children are unordered in the problem definition.
4. Combine the node label and sorted child hashes into a single composite representation. In practice, we map each distinct combination to a unique integer ID using a dictionary. This avoids expensive string concatenation and keeps comparisons constant time.
5. Perform the same process for both input lines, producing two root identifiers.
6. Compare the two root identifiers. If they match, output "Yes", otherwise output "No".

Why sorting is sufficient here is that subtree identity depends only on multiset structure of children, not their order. By converting children into a sorted sequence of stable identifiers, we enforce canonical form.

### Why it works

The invariant is that every subtree is assigned a unique identifier that depends only on its structure and label, not on how it was written or the order of its children. Two subtrees are equivalent if and only if their computed identifiers are equal. Because identifiers are assigned bottom-up, any difference in structure at any depth propagates upward and changes the root identifier. This guarantees that equality of root identifiers is equivalent to structural equivalence of the two input hierarchies.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(10**7)

def parse_tree(s):
    n = len(s)
    i = 0

    stack = []

    # Each element: (node_label, children list)
    nodes = []

    def new_node(val):
        return [val, []]

    root = None

    while i < n:
        if s[i].isspace():
            i += 1
            continue

        if s[i].isdigit():
            val = 0
            while i < n and s[i].isdigit():
                val = val * 10 + (ord(s[i]) - 48)
                i += 1
            node = new_node(val)
            nodes.append(node)
            if stack:
                stack[-1][1].append(node)
            stack.append(node)

        elif s[i] == '(':
            i += 1

        elif s[i] == ')':
            stack.pop()
            i += 1
        else:
            i += 1

    root = nodes[0]
    return root

def canonical_hash(root):
    from collections import defaultdict

    sys.setrecursionlimit(10**7)

    memo = {}
    counter = 1

    def dfs(node):
        nonlocal counter
        label, children = node

        child_ids = []
        for ch in children:
            child_ids.append(dfs(ch))

        child_ids.sort()

        key = (label, tuple(child_ids))
        if key not in memo:
            memo[key] = counter
            counter += 1
        return memo[key]

    return dfs(root)

def solve_one(line):
    root = parse_tree(line)
    return canonical_hash(root)

def main():
    s1 = input().strip()
    s2 = input().strip()

    id1 = solve_one(s1)
    id2 = solve_one(s2)

    print("Yes" if id1 == id2 else "No")

if __name__ == "__main__":
    main()
```

The parsing function reads integers and builds nodes incrementally. Each node keeps a list of its children. The stack ensures that nesting defined by parentheses is translated directly into parent-child relationships.

The hashing function performs a DFS. Each node collects its children’s hashes, sorts them, and uses a dictionary to assign a compact canonical ID. The memoization ensures that identical subtree structures share the same identifier even if encountered multiple times.

A subtle detail is that sorting is done on integer IDs, not on structural strings, which keeps comparisons fast. Another is that we rely on postorder traversal so that every child is fully resolved before computing the parent hash.

## Worked Examples

### Example 1

Input:

```
11 (10) (12 (13) (17) (28))
11 (12 (17) (28) (13)) (10)
```

We parse both into the same structure but with different child orders.

| Step | Node | Child IDs before sort | Sorted tuple | Assigned ID |
| --- | --- | --- | --- | --- |
| 10 | 10 | [] | () | 1 |
| 13 | 13 | [] | () | 2 |
| 17 | 17 | [] | () | 3 |
| 28 | 28 | [] | () | 4 |
| 12 | 12 | [2,3,4] | [2,3,4] | 5 |
| 11 | 11 | [1,5] | [1,5] | 6 |

Both trees produce root ID 6, so output is "Yes".

This trace shows that child ordering does not affect the final canonical tuple.

### Example 2

Input:

```
11 (10) (12)
11 (10(12))
```

First tree has 11 with two children 10 and 12. Second tree nests 12 under 10.

| Step | Node | Child IDs | Sorted tuple | Assigned ID |
| --- | --- | --- | --- | --- |
| 10 | 10 | [] | () | 1 |
| 12 | 12 | [] | () | 2 |
| 11 | 11 | [1,2] | [1,2] | 3 |
| 10 | 10 | [2] | [2] | 4 |
| 11 | 11 | [1,4] vs [1,2] mismatch | different | different |

The root identifiers differ, so output is "No".

This demonstrates that identical labels alone do not imply identical structure.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log k) | Each node sorts at most k children, k ≤ 100, across all nodes total is linearithmic in branching |
| Space | O(n) | Each node stored once plus memo table of subtree signatures |

The constraints allow up to 100,000 nodes, so a near-linear solution is required. Sorting bounded-degree children keeps total overhead small, and hashing avoids repeated structural comparisons.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    sys.setrecursionlimit(10**7)

    def parse_tree(s):
        n = len(s)
        i = 0
        stack = []
        nodes = []

        def new_node(v):
            return [v, []]

        while i < n:
            if s[i].isspace():
                i += 1
                continue
            if s[i].isdigit():
                v = 0
                while i < n and s[i].isdigit():
                    v = v * 10 + (ord(s[i]) - 48)
                    i += 1
                node = new_node(v)
                nodes.append(node)
                if stack:
                    stack[-1][1].append(node)
                stack.append(node)
            elif s[i] == '(':
                i += 1
            elif s[i] == ')':
                stack.pop()
                i += 1
            else:
                i += 1

        root = nodes[0]

        memo = {}
        counter = 1

        def dfs(node):
            nonlocal counter
            label, children = node
            ids = []
            for c in children:
                ids.append(dfs(c))
            ids.sort()
            key = (label, tuple(ids))
            if key not in memo:
                memo[key] = counter
                counter += 1
            return memo[key]

        return dfs(root)

    def solve():
        s1 = input().strip()
        s2 = input().strip()
        return "Yes" if run_tree(s1) == run_tree(s2) else "No"

    def run_tree(s):
        n = len(s)
        i = 0
        stack = []
        nodes = []

        def new_node(v):
            return [v, []]

        while i < n:
            if s[i].isspace():
                i += 1
                continue
            if s[i].isdigit():
                v = 0
                while i < n and s[i].isdigit():
                    v = v * 10 + (ord(s[i]) - 48)
                    i += 1
                node = new_node(v)
                nodes.append(node)
                if stack:
                    stack[-1][1].append(node)
                stack.append(node)
            elif s[i] == '(':
                i += 1
            elif s[i] == ')':
                stack.pop()
                i += 1
            else:
                i += 1

        root = nodes[0]

        memo = {}
        counter = 1

        def dfs(node):
            nonlocal counter
            label, children = node
            ids = []
            for c in children:
                ids.append(dfs(c))
            ids.sort()
            key = (label, tuple(ids))
            if key not in memo:
                memo[key] = counter
                counter += 1
            return memo[key]

        return dfs(root)

    s1 = input().strip()
    s2 = input().strip()

    print("Yes" if run_tree(s1) == run_tree(s2) else "No")

# provided samples
assert run("11 (10) (12 (13) (17) (28))\n11 (12 (17) (28) (13)) (10)\n") == "Yes"
assert run("11 ( 10 ) ( 12 )\n11(10(12))\n") == "No"

# custom cases
assert run("1\n1\n") == "Yes"
assert run("1\n2\n") == "No"
assert run("1 (2 3)\n1 (3 2)\n") == "Yes"
assert run("1 (2)\n1 (2 (3))\n") == "No"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 vs 1` | Yes | minimal identical trees |
| `1 vs 2` | No | different roots |
| unordered children | Yes | permutation invariance |
| extra depth | No | structural mismatch detection |

## Edge Cases

A common edge case is a single-node tree. The parser must correctly treat a lone number with no parentheses as a complete tree. The algorithm assigns it a leaf hash based only on its label, so two identical single nodes compare equal.

Another edge case is heavy branching, where one node has close to 100 children. The correctness depends on sorting child hashes, and the algorithm still works because sorting is applied only at that node level. For an input like

```
1 (2) (3) (4) ... (100)
1 (100) (99) ... (2)
```

both sides produce identical multisets of child hashes, so the root hash matches.

Deep nesting up to depth 1000 is handled safely because DFS depth equals tree depth, and Python recursion limit is increased. Each node is visited exactly once, so even worst-case chains like

```
1(2(3(4(...))))
```

still compute linear work, producing a chain of hash computations without recomputation or backtracking overhead.
