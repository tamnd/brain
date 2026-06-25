---
title: "CF 106431D - Tao of Trees (treaps)"
description: "The task is to maintain a binary search tree with treap rules. Each node has a key, which determines its position in the search tree, and a height value, which acts like a priority."
date: "2026-06-25T09:39:33+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106431
codeforces_index: "D"
codeforces_contest_name: "Entrenamiento OIE Nivel Experto - Semana 12"
rating: 0
weight: 106431
solve_time_s: 35
verified: true
draft: false
---

[CF 106431D - Tao of Trees (treaps)](https://codeforces.com/problemset/problem/106431/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 35s  
**Verified:** yes  

## Solution
## Problem Understanding

The task is to maintain a binary search tree with treap rules. Each node has a key, which determines its position in the search tree, and a height value, which acts like a priority. Smaller heights must always be closer to the root, so every parent has a smaller height than its children.

The input is a sequence of commands applied to an initially empty tree. An insertion gives a new key and height and must place the node exactly where the treap rules require. A deletion removes a key while preserving the remaining structure. A print operation outputs the tree using the required recursive representation, showing every node as `key/height` and recursively showing its children.

The key difficulty is that normal binary search tree insertion is not enough. Adding nodes at leaves can violate the height ordering, so insertion must rebuild parts of the tree. The constraints allow many operations, with keys up to $10^5$ and heights up to $10^9$. A solution that walks through every node for every update would become quadratic when many commands are processed. We need each modification to touch only the height of the tree, which is expected to be logarithmic because treaps remain balanced with high probability.

Several edge cases are easy to mishandle.

If the inserted node has the smallest height, it becomes the root. For example:

```
ADD 5 10
ADD 3 1
PRINT
```

The output is:

```
3/1(,5/10)
```

A solution that always inserts by key would incorrectly keep `5` as the root.

Deleting a node with two children requires joining its two remaining sides, not simply removing the node. For example:

```
ADD 2 2
ADD 1 1
ADD 3 3
DEL 2
PRINT
```

The correct output is:

```
1/1(,3/3)
```

A careless deletion can leave an invalid tree or lose one subtree.

The split operation also has a boundary condition. Splitting by key `k` must place the key `k` itself in the left result. If the comparison is changed from `<=` to `<`, inserting and deleting around existing keys will produce incorrect trees.

## Approaches

A direct solution would store the tree as an ordinary binary search tree and simulate every operation recursively. Searching by key is easy, and insertion can place a node as a leaf. The problem is that leaf insertion ignores heights. A sequence of increasing keys with increasing heights creates a chain:

```
1
 \
  2
   \
    3
     \
      4
```

After $n$ insertions, a single operation may traverse $O(n)$ nodes, giving $O(n^2)$ work over all commands.

The important observation is that the height values already describe where nodes belong. The node with the smallest height in a treap must be the root. All nodes with smaller keys belong to its left subtree, and all larger keys belong to its right subtree. This means a treap can be changed by combining two primitive operations.

`split` divides a treap into two valid treaps around a key. `join` combines two valid treaps where every key in the first is smaller than every key in the second. Both operations recursively move down one path, because every recursive call discards one side of the tree. Since the expected height of a treap is logarithmic, these operations are efficient.

Insertion becomes a split around the new key, creating the new single node, then joining the pieces back together. Deletion becomes two splits that isolate the target node, followed by one join of the remaining parts.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nq) | O(n) | Too slow |
| Treap split/join | O(q log n) expected | O(n) | Accepted |

## Algorithm Walkthrough

1. To insert a node `(k, h)`, split the current treap by `k`. The left tree contains every key smaller than or equal to `k`, and the right tree contains every larger key. This creates the correct separation required for a binary search tree.
2. Create a new treap containing only `(k, h)`. Join the left part with this node, then join the result with the right part. The join operation chooses the root using heights, so the height condition is automatically restored.
3. To delete key `k`, split the tree by `k`, producing a left part containing keys up to `k` and a right part containing larger keys.
4. Split the left part by `k - 1`. The second split separates all smaller keys from the single node with key `k`.
5. Discard the isolated node and join the two remaining trees. Since every key in the left tree is smaller than every key in the right tree, the result is a valid treap.
6. For printing, recursively print the current node. If a child is missing, print an empty position. Otherwise, print the child subtree in parentheses.

Why it works:

The invariant is that every subtree always satisfies both treap properties: keys follow binary search tree ordering and heights follow heap ordering. `split` preserves this because it only changes parent-child relationships while recursively rebuilding affected paths. `join` preserves it because the root must be the node with the smallest height among the two input trees, and the recursive calls continue the same reasoning on the remaining subtrees. Since insertion and deletion are composed only of these valid operations, every intermediate and final tree remains a correct treap.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Node:
    __slots__ = ("key", "height", "left", "right")

    def __init__(self, key, height):
        self.key = key
        self.height = height
        self.left = None
        self.right = None

def join(a, b):
    if a is None:
        return b
    if b is None:
        return a

    if a.height < b.height:
        a.right = join(a.right, b)
        return a
    else:
        b.left = join(a, b.left)
        return b

def split(root, key):
    if root is None:
        return None, None

    if root.key <= key:
        left_part, right_part = split(root.right, key)
        root.right = left_part
        return root, right_part
    else:
        left_part, right_part = split(root.left, key)
        root.left = right_part
        return left_part, root

def add(root, key, height):
    left, right = split(root, key)
    return join(join(left, Node(key, height)), right)

def delete(root, key):
    middle, right = split(root, key)
    left, _ = split(middle, key - 1)
    return join(left, right)

def build_string(root):
    if root is None:
        return ""

    value = f"{root.key}/{root.height}"

    if root.left is None and root.right is None:
        return value

    return value + "(" + build_string(root.left) + "," + build_string(root.right) + ")"

def solve():
    root = None
    out = []

    for line in sys.stdin:
        if not line.strip():
            continue

        cmd = line.split()

        if cmd[0] == "ADD":
            root = add(root, int(cmd[1]), int(cmd[2]))
        elif cmd[0] == "DEL":
            root = delete(root, int(cmd[1]))
        else:
            out.append(build_string(root))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The `Node` class stores only the information needed for the treap property. No parent pointers or extra metadata are required because every modification can rebuild the affected path recursively.

`split` is the core operation. When the current node belongs to the left result, its right child must be split further, because larger keys may still need to move to the right result. The symmetric case handles nodes larger than the split key.

`join` compares heights because the smallest height must become the root. The losing side is recursively attached below that root. The comparison direction is easy to reverse accidentally, which would create a max heap instead of the required min heap.

Deletion uses `split(root, key)` followed by `split(left_side, key - 1)`. Since keys are integers and unique, this isolates exactly one node. Using `key` in the second split would incorrectly keep the node being removed.

Python integers do not overflow, so the large height values are safe. The recursion depth is expected to stay logarithmic because treaps are balanced with high probability.

## Worked Examples

Consider:

```
ADD 1 23
ADD 2 19
ADD 4 95
ADD 6 13
```

The state changes as follows:

| Operation | Root | Left subtree | Right subtree |
| --- | --- | --- | --- |
| ADD 1 23 | 1/23 | empty | empty |
| ADD 2 19 | 2/19 | 1/23 | empty |
| ADD 4 95 | 2/19 | 1/23 | 4/95 |
| ADD 6 13 | 6/13 | 2/19 | empty |

The last insertion places `6` at the root because its height is the smallest. The previous root becomes part of the left subtree because all smaller keys must remain on that side.

Another example:

```
ADD 1 74
ADD 2 23
ADD 3 91
ADD 4 43
DEL 2
```

| Operation | Root | Important change |
| --- | --- | --- |
| ADD 1 74 | 1/74 | Initial node |
| ADD 2 23 | 2/23 | New smaller height becomes root |
| ADD 3 91 | 2/23 | Added to right side |
| ADD 4 43 | 2/23 | Height 43 moves above 3/91 |
| DEL 2 | 4/43 | Left and right parts are joined |

This demonstrates that deletion does not replace a node arbitrarily. The join operation reconstructs the only treap satisfying both ordering rules.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(q log n) expected | Every split and join follows one treap path, and each command uses a constant number of them. |
| Space | O(n) | Each node is stored once, with recursion using expected logarithmic stack space. |

The constraints require avoiding linear scans. The expected logarithmic behavior of treaps makes every command efficient enough for the input size.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    data = sys.stdin.read().splitlines()
    sys.stdin = old

    root = None
    ans = []

    for line in data:
        cmd = line.split()
        if not cmd:
            continue
        if cmd[0] == "ADD":
            root = add(root, int(cmd[1]), int(cmd[2]))
        elif cmd[0] == "DEL":
            root = delete(root, int(cmd[1]))
        else:
            ans.append(build_string(root))

    return "\n".join(ans)

assert run("""ADD 1 23
PRINT
ADD 2 19
PRINT
""") == """1/23
2/19(1/23,)"""

assert run("""ADD 1 1
ADD 2 2
ADD 3 3
ADD 4 4
ADD 5 5
PRINT
""") == "1/1(,2/2(,3/3(,4/4(,5/5))))"

assert run("""ADD 5 10
ADD 3 1
PRINT
""") == "3/1(,5/10)"

assert run("""ADD 2 2
ADD 1 1
ADD 3 3
DEL 2
PRINT
""") == "1/1(,3/3)"

assert run("""PRINT
""") == ""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Two increasing inserts | `2/19(1/23,)` | Root replacement by height |
| Increasing keys and heights | A chain-shaped treap | Split and join boundary behavior |
| New minimum height | `3/1(,5/10)` | Insertion of a new root |
| Delete root with two children | `1/1(,3/3)` | Correct deletion through joins |
| Empty print | Empty output | Empty tree handling |

## Edge Cases

When a new node has the smallest height, every existing node must move below it. For input:

```
ADD 5 10
ADD 3 1
PRINT
```

The first split separates the old tree from the new key position. The new node has height `1`, so `join` makes it the root. The output is:

```
3/1(,5/10)
```

When deleting a node with two children, both remaining sides must survive. For:

```
ADD 2 2
ADD 1 1
ADD 3 3
DEL 2
PRINT
```

The first split isolates the root and the right side. The second split separates the left child. Joining the remaining trees creates:

```
1/1(,3/3)
```

The algorithm never chooses a replacement manually, so it avoids breaking the height ordering.

A common off-by-one mistake is the second split during deletion. The command:

```
DEL 2
```

must remove only key `2`, not all keys up to `2`. The second split uses `key - 1`, leaving every smaller key in the left tree and isolating the target node alone. This preserves all keys and keeps the final join valid.
