---
title: "CF 106431C - Tao of Trees (search trees)"
description: "The problem asks us to maintain a binary search tree while a sequence of commands is executed. The tree starts empty."
date: "2026-06-25T09:38:59+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106431
codeforces_index: "C"
codeforces_contest_name: "Entrenamiento OIE Nivel Experto - Semana 12"
rating: 0
weight: 106431
solve_time_s: 37
verified: true
draft: false
---

[CF 106431C - Tao of Trees (search trees)](https://codeforces.com/problemset/problem/106431/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 37s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem asks us to maintain a binary search tree while a sequence of commands is executed. The tree starts empty. An insertion command places a new key into the correct leaf position according to normal binary search tree rules, while ignoring the operation if the key is already present. A deletion command removes a key if it exists, using the standard BST deletion rule: replace a node with two children by its inorder predecessor. A print command asks us to output the current tree using a recursive parenthesized representation.

The input is a stream of operations rather than a single static tree. Each operation changes the structure that later operations observe. The output is the exact shape of the tree after every print request, so storing only the set of keys is not enough. The parent and child relationships must be preserved.

The constraints are designed around simulation. The number of operations can be large enough that rebuilding the whole tree after every command would be wasteful. If there are around 100000 operations, an approach that scans all existing nodes for every operation can reach about 10^10 operations in the worst case, which is far beyond a typical one second limit. The intended approach is to make each tree modification proportional to the current height of the tree. A binary search tree can become a chain, so the worst case height is O(n), but the total number of commands is the real limiting factor and we need to avoid extra full traversals.

The tricky cases are mostly around deletion and printing. For example, deleting a leaf must remove exactly that node.

```
ADD 5
ADD 3
DEL 3
PRINT
```

The output is:

```
5
```

A careless implementation that only marks nodes as deleted but does not disconnect the parent pointer can still print the old child.

Deleting a node with two children is another common mistake.

```
ADD 5
ADD 3
ADD 7
ADD 4
DEL 5
PRINT
```

The correct output is:

```
4(3,7)
```

The predecessor of 5 is 4, so 4 replaces 5. An implementation that chooses the successor instead would create a different tree.

An empty tree is also possible.

```
DEL 10
PRINT
```

The output is:

```

```

The deletion should do nothing because the key does not exist. Printing an empty tree should produce an empty line, not a special marker.

## Approaches

The direct solution is to represent every node with its key and pointers to the left and right children. For an insertion, we start at the root and repeatedly compare the new key with the current node until we find an empty child position. This is exactly how a BST is defined, so the procedure is correct. For deletion, we search for the node and then handle the three cases: no child, one child, or two children. Printing is just a recursive traversal that follows the required format.

The brute force approach would be to store all keys in an array and rebuild the tree whenever a command changes it. This would still be correct, because inserting the same keys in the same order reconstructs the same BST. However, rebuilding after every command costs O(n) work. With up to 100000 operations, this can become roughly O(n²), which is too slow.

The key observation is that a BST operation only needs to inspect the path from the root to the affected key. The rest of the tree is already in a valid state and does not need to be touched. A node deletion also only changes a small number of links around the removed node. This reduces every update to a height traversal.

The remaining issue is printing. A print command has to visit every node because the whole structure must be output. That cost is unavoidable, since the output itself contains the entire tree.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(q²) in the worst case | O(n) | Too slow |
| Optimal | O(qh + total printed nodes) | O(n) | Accepted |

Here q is the number of commands and h is the current tree height.

## Algorithm Walkthrough

1. Store the tree using nodes that contain a key and references to their left and right children. Keep a reference to the root node. The tree structure itself is the information we need for future operations.
2. For an ADD operation, start from the root and compare the new key with each visited node. Move left for a smaller key and right for a larger key. When the next child pointer is empty, attach the new node there. If the key is found during the search, stop because duplicates are ignored.
3. For a DEL operation, search for the target key while remembering the parent node. If the key is missing, return immediately. If the node has no children, remove the corresponding parent pointer. If it has one child, connect the parent directly to that child.
4. If the deleted node has two children, find the rightmost node in its left subtree. This node is the largest key smaller than the deleted key, so replacing the deleted node with it keeps the BST ordering valid. Remove the predecessor from its old location and reconnect the children.
5. For a PRINT operation, recursively produce the representation. A missing node contributes an empty string. A leaf contributes only its key. Any other node contributes its key followed by the representations of its children.

Why it works: the invariant is that after every modification, every node still satisfies the binary search tree ordering rule. Insertions preserve it because the new node is placed exactly at the first valid empty position. Deletions preserve it because replacing a two child node with its inorder predecessor keeps all left subtree values smaller and all right subtree values larger. Since printing only reads the maintained structure, the output always describes the current tree.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(1 << 25)

class Node:
    __slots__ = ("key", "left", "right")
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

root = None

def add(key):
    global root
    if root is None:
        root = Node(key)
        return

    cur = root
    while True:
        if key == cur.key:
            return
        if key < cur.key:
            if cur.left is None:
                cur.left = Node(key)
                return
            cur = cur.left
        else:
            if cur.right is None:
                cur.right = Node(key)
                return
            cur = cur.right

def delete(key):
    global root
    parent = None
    cur = root

    while cur is not None and cur.key != key:
        parent = cur
        if key < cur.key:
            cur = cur.left
        else:
            cur = cur.right

    if cur is None:
        return

    if cur.left is None:
        child = cur.right
        if parent is None:
            root = child
        elif parent.left is cur:
            parent.left = child
        else:
            parent.right = child
    elif cur.right is None:
        child = cur.left
        if parent is None:
            root = child
        elif parent.left is cur:
            parent.left = child
        else:
            parent.right = child
    else:
        pred_parent = cur
        pred = cur.left
        while pred.right is not None:
            pred_parent = pred
            pred = pred.right

        cur.key = pred.key

        if pred_parent.left is pred:
            pred_parent.left = pred.left
        else:
            pred_parent.right = pred.left

def build(cur):
    if cur is None:
        return ""
    if cur.left is None and cur.right is None:
        return str(cur.key)
    return str(cur.key) + "(" + build(cur.left) + "," + build(cur.right) + ")"

def solve(data):
    global root
    root = None
    ans = []

    for line in data.splitlines():
        if not line:
            continue
        parts = line.split()
        if parts[0] == "ADD":
            add(int(parts[1]))
        elif parts[0] == "DEL":
            delete(int(parts[1]))
        else:
            ans.append(build(root))

    return "\n".join(ans)

data = sys.stdin.read()
print(solve(data))
```

The `Node` class stores only the three pieces of information required for a BST. Using iterative insertion and deletion avoids recursion depth issues when the tree becomes a chain.

The insertion routine walks down the tree until it finds a missing pointer. The equality check is done before moving, which prevents duplicate keys from being inserted.

Deletion is the most delicate part. The search keeps the parent because changing the tree requires modifying the pointer that leads to the removed node. In the two child case, the predecessor is found by moving left once and then going as far right as possible. The predecessor cannot have a right child, so after copying its key into the deleted node, it can be removed like a zero or one child case.

The printing function is recursive because the requested format is naturally recursive. The empty string handling is what allows missing children inside a non leaf node to appear correctly, such as `5(3,)`.

## Worked Examples

Consider this sequence:

```
ADD 5
ADD 3
ADD 7
PRINT
DEL 5
PRINT
```

The execution state is:

| Step | Operation | Root | Printed tree |
| --- | --- | --- | --- |
| 1 | ADD 5 | 5 |  |
| 2 | ADD 3 | 5 |  |
| 3 | ADD 7 | 5 |  |
| 4 | PRINT | 5 | 5(3,7) |
| 5 | DEL 5 | 7 |  |
| 6 | PRINT | 7 | 3(,7) |

The deletion replaces 5 with its predecessor 3. The subtree ordering remains valid because everything left of 3 is smaller and everything right of 3 is larger.

A second example:

```
ADD 8
ADD 2
ADD 4
ADD 10
DEL 2
PRINT
DEL 100
PRINT
```

| Step | Operation | Root | Printed tree |
| --- | --- | --- | --- |
| 1 | ADD 8 | 8 |  |
| 2 | ADD 2 | 8 |  |
| 3 | ADD 4 | 8 |  |
| 4 | ADD 10 | 8 |  |
| 5 | DEL 2 | 8 |  |
| 6 | PRINT | 8 | 8(4,10) |
| 7 | DEL 100 | 8 |  |
| 8 | PRINT | 8 | 8(4,10) |

The second deletion has no effect because the key is absent. The trace confirms that invalid operations leave the tree unchanged.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(qh + P) | Each update follows one root to leaf path. Printing costs P, the number of nodes written across all print commands. |
| Space | O(n) | Each existing key occupies one node. |

The solution fits the constraints because it never rebuilds the tree. The only full traversals happen when the output explicitly requires the entire structure.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    return solve(inp).strip()

assert run("""ADD 5
ADD 3
ADD 7
PRINT
""") == "5(3,7)", "basic insert"

assert run("""ADD 5
ADD 3
ADD 7
DEL 5
PRINT
""") == "3(,7)", "delete root with two children"

assert run("""PRINT
DEL 1
PRINT
""") == "", "empty tree"

assert run("""ADD 1
ADD 2
ADD 3
DEL 2
PRINT
""") == "1(,3)", "delete node with one child"

assert run("""ADD 10
ADD 5
ADD 15
ADD 12
DEL 100
PRINT
""") == "10(5,15(12,))", "delete missing key"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Three node insertion | `5(3,7)` | Basic BST construction |
| Removing the root | `3(,7)` | Two child deletion |
| Printing empty tree | empty line | Empty representation |
| Removing a chain node | `1(,3)` | One child replacement |
| Deleting absent value | `10(5,15(12,))` | Ignored invalid operations |

## Edge Cases

For the empty tree case, the input

```
DEL 10
PRINT
```

starts with no root. The deletion search immediately fails, so the root remains empty. Printing calls the recursive function on a missing node and returns an empty string.

For two child deletion, consider:

```
ADD 6
ADD 2
ADD 9
ADD 4
DEL 6
PRINT
```

The node 6 has children on both sides. The algorithm finds 4 as the rightmost node of the left subtree, copies its key into the root, and removes the old 4 position. The output becomes:

```
4(2,9)
```

A solution that simply removes 6 would lose both subtrees.

For duplicate insertion, consider:

```
ADD 5
ADD 5
PRINT
```

The second insertion reaches the existing node with key 5 and stops. The tree remains:

```
5
```

This matters because inserting duplicates would break the assumption that every key appears once, which the deletion logic relies on.
