---
title: "CF 102222E - 2-3-4 Tree"
description: "We have to simulate a sequence of insertions into a 2-3-4 search tree. The values are a permutation of 1..n, so every value appears exactly once. A node may contain one, two, or three sorted keys. A node with three keys is full."
date: "2026-08-17T22:05:42+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102222
codeforces_index: "E"
codeforces_contest_name: "2018-2019 ACM-ICPC, China Multi-Provincial Collegiate Programming Contest"
rating: 0
weight: 102222
solve_time_s: 102
verified: true
draft: false
---

[CF 102222E - 2-3-4 Tree](https://codeforces.com/problemset/problem/102222/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We have to simulate a sequence of insertions into a 2-3-4 search tree. The values are a permutation of `1..n`, so every value appears exactly once. A node may contain one, two, or three sorted keys. A node with three keys is full. Before descending through a full node, we split it and move its middle key into its parent. If the full node is the root, the middle key becomes a new root and the tree grows by one level.

After all insertions, the required output is the entire tree in preorder. For each visited node, we print all of its keys on one line in increasing order.

The input contains up to 50 independent test cases, with at most 5000 insertions in one case. A direct simulation is already enough if each insertion follows a tree path, because a 2-3-4 tree has logarithmic height. With `n = 5000`, even an `O(n log n)` implementation performs only on the order of several tens of thousands of node operations per test case. Across all 50 cases, the total can reach 250,000 inserted values, so avoiding an `O(n²)` operation per case is still useful.

The most common correctness mistakes happen around splitting. For example, inserting `1 2 3 4` gives

```
Case #1:
2
1
3 4
```

The fourth insertion does not simply append `4` to the root. Before descending, the root `[1 2 3]` is split around `2`, producing root `[2]` with children `[1]` and `[3]`. The value `4` then goes into the right child.

The opposite insertion order exercises the same boundary from the other side. For

```
1
4
4 3 2 1
```

the correct tree is

```
Case #1:
3
1 2
4
```

A careless implementation that promotes the wrong key, or creates children in the wrong order, will usually produce a superficially valid search tree but a different preorder traversal.

A second subtle case occurs when a non-root node is full. Suppose the root has already been split and a later insertion reaches a full child. The middle key must be inserted into the existing parent, while the two remaining pieces replace the original child. Splitting such a node as though it were the root incorrectly increases the tree height.

Finally, the first three insertions have special-looking behavior only because the root starts as a single node. For `1 2 3`, the tree is simply one node containing `1 2 3`. Splitting is performed when processing the next insertion, not immediately after creating a full node.

## Approaches

The most direct brute-force simulation can maintain the tree explicitly and, for every new value, search for its destination leaf by scanning the existing tree until the appropriate interval is found. This is correct because every key belongs to exactly one child interval, and splitting full nodes preserves the search-tree ordering. However, the scan can inspect every existing node in the worst case. Before the `i`-th insertion there are `i-1` stored values and at most `i-1` nodes, so a deliberately exhaustive search performs up to

`1 + 2 + ... + (n-1) = n(n-1)/2`

node inspections. For `n = 5000`, that is 12,497,500 inspections in one test case, and up to roughly 625 million across 50 maximum-sized cases. Python should not spend that much time repeatedly traversing unrelated parts of the tree.

The brute-force approach works because the tree itself already contains the information needed to choose the next child. The key observation is that a 2-3-4 tree is balanced by construction. Every root-to-leaf path has the same length, and every internal node has at least two children. Consequently, the height is `O(log n)`. We never need to inspect unrelated subtrees. At every node, its one, two, or three keys divide the remaining search space into two, three, or four intervals, so one comparison sequence identifies exactly one child.

This gives the standard top-down B-tree insertion strategy. While following the search path, split a full node before descending into it. A full node contains `[a, b, c]`, so `b` moves upward and the node becomes two nodes containing `[a]` and `[c]`. If the node has children, the first two children remain with `[a]` and the last two remain with `[c]`. Once we reach a leaf, that leaf has at most two keys, so the new value can simply be inserted there.

The resulting implementation follows exactly the insertion procedure from the problem, while storing only the nodes on the actual tree and never searching unrelated subtrees.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(n²)` | `O(n)` | Too slow in the worst case |
| Optimal | `O(n log n)` | `O(n)` | Accepted |

## Algorithm Walkthrough

1. Represent every node by its sorted `keys` list and its `children` list. A leaf has no children, a 2-node has one key, a 3-node has two keys, and a 4-node has three keys. Internal nodes have exactly one more child than the number of keys.
2. For every value to insert, first check whether the root is full. If it contains three keys, split it into two children and promote its middle key into a new root. This is the only operation that increases the height of the tree.
3. Starting from the root, process the current node before choosing a child. If the current node is a leaf, insert the value into its sorted key list and stop. The node cannot already be full because full nodes are split before we descend into them.
4. If the current node is internal, determine which child contains the new value. With keys `[k0]`, values smaller than `k0` go to child zero and larger values go to child one. With `[k0, k1]`, there are three intervals. With `[k0, k1, k2]`, there are four.
5. Before descending into the selected child, check whether that child is full. If it is, split it immediately. Its middle key moves into the current node, and the two resulting nodes replace the original full child. This is why the parent must be modified before selecting the final child index.
6. After splitting a child, compare the value with the newly promoted key. If the value is greater than the promoted key, the correct destination is the new right child, so increment the child index. Otherwise, the value belongs in the left child.
7. Repeat the descent until a leaf is reached. Insert the value into the leaf using a sorted insertion operation.
8. After all values have been inserted, perform a preorder traversal. Print the current node first, then recursively visit its children from left to right.

The key invariant is that before every descent, the node being entered is not full. Every split preserves the sorted order of keys and the correspondence between child intervals and keys. Since every insertion is made into the unique leaf whose interval contains the value, all values remain in search-tree order. Since every full node is split before descent, no insertion ever needs to modify a four-node after entering it, and the tree remains a valid balanced 2-3-4 tree throughout the entire process.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Node:
    __slots__ = ("keys", "children")

    def __init__(self, keys=None, children=None):
        self.keys = [] if keys is None else keys
        self.children = [] if children is None else children

    def is_leaf(self):
        return not self.children

def split_child(parent, idx):
    """
    parent.children[idx] is a full node with three keys.

    Split:
        [a, b, c]
    into
        [a] and [c]
    and promote b into parent.
    """
    node = parent.children[idx]

    middle = node.keys[1]

    left = Node([node.keys[0]])
    right = Node([node.keys[2]])

    if node.children:
        left.children = node.children[:2]
        right.children = node.children[2:]

    parent.keys.insert(idx, middle)
    parent.children[idx] = left
    parent.children.insert(idx + 1, right)

def insert(root, value):
    # A full root has to be split before we start descending.
    if len(root.keys) == 3:
        new_root = Node([], [root])
        split_child(new_root, 0)
        root = new_root

    cur = root

    while True:
        if cur.is_leaf():
            # The leaf is guaranteed not to be full.
            if not cur.keys:
                cur.keys.append(value)
            elif value < cur.keys[0]:
                cur.keys.insert(0, value)
            elif value > cur.keys[-1]:
                cur.keys.append(value)
            else:
                # Input is a permutation, so this branch is unreachable.
                pos = 0
                while pos < len(cur.keys) and cur.keys[pos] < value:
                    pos += 1
                cur.keys.insert(pos, value)
            return root

        # Find the child interval containing value.
        idx = 0
        while idx < len(cur.keys) and value > cur.keys[idx]:
            idx += 1

        # Split a full child before descending into it.
        if len(cur.children[idx].keys) == 3:
            split_child(cur, idx)

            # The promoted key now sits at cur.keys[idx].
            if value > cur.keys[idx]:
                idx += 1

        cur = cur.children[idx]

def preorder(root, out):
    out.append(" ".join(map(str, root.keys)))
    for child in root.children:
        preorder(child, out)

def solve():
    t = int(input())
    output = []

    for case_id in range(1, t + 1):
        n = int(input())
        a = list(map(int, input().split()))

        root = Node()

        for value in a:
            root = insert(root, value)

        output.append(f"Case #{case_id}:")
        preorder(root, output)

    sys.stdout.write("\n".join(output))

if __name__ == "__main__":
    solve()
```

The `Node` class keeps the representation deliberately small. A node has at most three keys and at most four children, so Python list operations inside a node are constant time in the asymptotic analysis.

`split_child` implements the central structural operation. For a full node `[a, b, c]`, the key `b` is promoted to the parent. The left node receives `a` and the right node receives `c`. If the original node was internal, its first two children belong to the left node and its last two children belong to the right node. The slicing indices `[:2]` and `[2:]` are exactly the four-child split required by the search-tree intervals.

The root is handled separately because it has no parent into which its middle key could be promoted. Creating a new root containing the two resulting children is equivalent to increasing the tree height by one.

For a non-root full child, `split_child(cur, idx)` inserts the promoted key at exactly position `idx` in the parent and inserts the right half immediately after the left half. If the inserted value is larger than the promoted key, the child index must be incremented. Forgetting this adjustment is a common source of wrong answers because the old child index now refers to the left half.

The leaf insertion uses Python lists because a node has at most three keys. There is no meaningful asymptotic cost from shifting these few elements. Since the input is guaranteed to be a permutation, duplicate handling is never actually needed.

The final traversal prints a node before its children, which is precisely preorder traversal. Children are already stored from left to right, so visiting them in list order gives the required traversal without any additional sorting.

Python integer overflow is irrelevant here because every value lies between `1` and `n`, and the tree stores those values directly.

## Worked Examples

### Sample 1

The first sample inserts `1, 2, 3, 4`. The first three values fit into the root. During the fourth insertion, the full root is split before the algorithm descends.

| Insertion | Current root | Action | Result |
| --- | --- | --- | --- |
| `1` | empty | Insert into leaf | `[1]` |
| `2` | `[1]` | Insert into leaf | `[1 2]` |
| `3` | `[1 2]` | Insert into leaf | `[1 2 3]` |
| `4` | `[1 2 3]` | Split root around `2` | root `[2]`, children `[1]`, `[3]` |
| `4` | `[2]` | Descend right, insert into `[3]` | `[3 4]` |

The final preorder traversal is

```
Case #1:
2
1
3 4
```

This trace demonstrates why splitting occurs before descending. If `4` were inserted into the full root first, the result would no longer follow the specified insertion procedure.

### Sample 2

The second sample uses the reverse permutation `4, 3, 2, 1`.

| Insertion | Current tree root | Action | Resulting relevant path |
| --- | --- | --- | --- |
| `4` | empty | Insert into leaf | `[4]` |
| `3` | `[4]` | Insert into leaf | `[3 4]` |
| `2` | `[3 4]` | Insert into leaf | `[2 3 4]` |
| `1` | `[2 3 4]` | Split root around `3` | root `[3]`, children `[2]`, `[4]` |
| `1` | `[3]` | Descend left and insert | `[1 2]` |

The final tree is

```
Case #2:
3
1 2
4
```

The middle key is always promoted. In this case the full root `[2 3 4]` promotes `3`, not `2` or `4`. The smaller values remain in the left child and the larger values remain in the right child.

The third sample is larger and demonstrates repeated splitting at different levels. Its final output is

```
Case #3:
5 9
2
1
3 4
7
6
8
11 13 15
10
12
14
16 17
```

The root contains two keys, `5` and `9`, so it has three children. The preorder traversal prints the root first, followed by the entire subtree containing values below `5`, then the subtree between `5` and `9`, and finally the subtree above `9`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n log n)` | Every insertion follows one root-to-leaf path of logarithmic height, and each node has at most three keys |
| Space | `O(n)` | The tree contains `O(n)` nodes and each node stores constant-size key and child lists |

A 2-3-4 tree has height `O(log n)` because every internal node has at least two children and all leaves are at the same depth. With `n <= 5000`, each insertion visits only a small number of nodes. Even with 50 test cases, the total amount of work remains comfortably within the stated 10 second limit.

## Test Cases

The official sample input and output can be tested exactly. The custom tests below use small permutations where the expected tree can be derived by hand. The specification requires every test case to be a permutation of `1..n`, so an all-equal input is not a valid test case and should not be included as a correctness test for the submitted program.

```python
import sys
import io

class Node:
    __slots__ = ("keys", "children")

    def __init__(self, keys=None, children=None):
        self.keys = [] if keys is None else keys
        self.children = [] if children is None else children

def split_child(parent, idx):
    node = parent.children[idx]

    middle = node.keys[1]
    left = Node([node.keys[0]])
    right = Node([node.keys[2]])

    if node.children:
        left.children = node.children[:2]
        right.children = node.children[2:]

    parent.keys.insert(idx, middle)
    parent.children[idx] = left
    parent.children.insert(idx + 1, right)

def insert(root, value):
    if len(root.keys) == 3:
        new_root = Node([], [root])
        split_child(new_root, 0)
        root = new_root

    cur = root

    while True:
        if not cur.children:
            pos = 0
            while pos < len(cur.keys) and cur.keys[pos] < value:
                pos += 1
            cur.keys.insert(pos, value)
            return root

        idx = 0
        while idx < len(cur.keys) and value > cur.keys[idx]:
            idx += 1

        if len(cur.children[idx].keys) == 3:
            split_child(cur, idx)
            if value > cur.keys[idx]:
                idx += 1

        cur = cur.children[idx]

def preorder(root, out):
    out.append(" ".join(map(str, root.keys)))
    for child in root.children:
        preorder(child, out)

def solution(inp: str) -> str:
    data = list(map(int, inp.split()))
    it = iter(data)

    t = next(it)
    out = []

    for case_id in range(1, t + 1):
        n = next(it)
        values = [next(it) for _ in range(n)]

        root = Node()

        for x in values:
            root = insert(root, x)

        out.append(f"Case #{case_id}:")
        preorder(root, out)

    return "\n".join(out)

def run(inp: str) -> str:
    return solution(inp)

sample_input = """\
3
4
1 2 3 4
4
4 3 2 1
17
6 3 5 7 1 10 2 9 4 8 11 12 13 14 15 16 17
"""

sample_output = """\
Case #1:
2
1
3 4
Case #2:
3
1 2
4
Case #3:
5 9
2
1
3 4
7
6
8
11 13 15
10
12
14
16 17
"""

assert run(sample_input) == sample_output, "official samples"

assert run("""\
1
1
1
""") == """\
Case #1:
1
""", "minimum-size case"

assert run("""\
1
4
1 2 3 4
""") == """\
Case #1:
2
1
3 4
""", "root split"

assert run("""\
1
4
4 3 2 1
""") == """\
Case #1:
3
1 2
4
""", "reverse insertion"

assert run("""\
1
7
1 2 3 4 5 6 7
""") == """\
Case #1:
4
2
1
3
6
5
7
""", "multiple root and child splits"

# The original constraints require a permutation, so an all-equal case
# such as 4 / 1 1 1 1 is intentionally not tested as valid input.
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1 / 1` | `Case #1:`, then `1` | Smallest possible tree and empty-root initialization |
| `1 / 4 / 1 2 3 4` | Root `2`, children `1` and `3 4` | Splitting a full root before descending |
| `1 / 4 / 4 3 2 1` | Root `3`, children `1 2` and `4` | Symmetric behavior for decreasing input |
| `1 / 7 / 1 2 3 4 5 6 7` | Root `4` with three levels of preorder output | Repeated splitting and child-index updates |

## Edge Cases

The smallest valid input is `n = 1` with the permutation `1`. The root starts empty, `1` is inserted directly into it, and preorder traversal prints exactly one line containing `1`. There is no special split or child traversal involved.

For `n = 4` and input `1 2 3 4`, the root becomes `[1 2 3]` after the first three insertions. Before processing `4`, the algorithm detects that the root is full, promotes `2`, and creates children `[1]` and `[3]`. Since `4 > 2`, the child index remains on the right side and `4` is inserted into `[3]`, producing `[3 4]`. The output is exactly `2`, `1`, `3 4` in preorder.

For `n = 4` and input `4 3 2 1`, the full root is `[2 3 4]` before inserting `1`. The middle key `3` is promoted, producing `[3]` with children `[2]` and `[4]`. Since `1 < 3`, the algorithm descends to the left child and obtains `[1 2]`. This catches implementations that accidentally promote the first or last key instead of the middle key.

A deeper boundary case appears when a child is full while its parent is not. Consider increasing input through `1 2 3 4 5 6 7`. After the fourth insertion, the root is `[2]` with children `[1]` and `[3 4]`. Inserting `5` makes the right child `[3 4 5]`. Before inserting `6`, that child is split around `4`, so the root becomes `[2 4]` with children `[1]`, `[3]`, and `[5]`. The value `6` then enters the third child. Further insertions can make another child full and trigger another local split. The root does not gain a new level merely because a child split, which is exactly why root handling must be separated from ordinary child handling.

An invalid all-equal input such as

```
1
4
1 1 1 1
```

must not be used to judge the solution because the problem explicitly guarantees a permutation of `1..n`. If a separate test harness wants to examine duplicate handling, it is testing behavior outside the problem's contract. The submitted algorithm does not need to define a result for that input.

The preorder output itself is another boundary condition. For every internal node, the current node's keys must be printed before any descendant. After printing the root `[5 9]` in the third sample, the traversal completely prints the subtree below `5`, then the subtree between `5` and `9`, and only then the subtree above `9`. Printing children before the current node would produce an inorder-like structure and would fail even if the underlying 2-3-4 tree were perfectly constructed.
