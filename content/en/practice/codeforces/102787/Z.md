---
title: "CF 102787Z - Trick or Treap"
description: "The problem maintains a collection of ordered groups of treap nodes. A node is created with a value, and its identifier is the query number that created it."
date: "2026-07-27T19:19:15+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102787
codeforces_index: "Z"
codeforces_contest_name: "Algorithms Thread Treaps Contest"
rating: 0
weight: 102787
solve_time_s: 63
verified: true
draft: false
---

[CF 102787Z - Trick or Treap](https://codeforces.com/problemset/problem/102787/Z)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 3s  
**Verified:** yes  

## Solution
# Problem Understanding

The problem maintains a collection of ordered groups of treap nodes. A node is created with a value, and its identifier is the query number that created it. Groups behave like sequences: when two groups are joined, the whole group containing one node is placed before the whole group containing the other node. A group can also be cut after a given number of nodes, separating its prefix from its suffix. Queries ask for the sum of all values inside the group containing a particular node.

The input is a stream of up to $5 \cdot 10^5$ operations. Since every operation must be processed online, rebuilding groups or scanning their contents is impossible. A solution that touches every node during each merge, split, or query can reach $O(q^2)$, which is far beyond what an 8 second limit can handle. We need each operation to work in logarithmic time.

The tricky cases come from the fact that node identifiers do not describe positions. A node can move anywhere inside its group after merges and splits.

For example, after:

```
5
1 10
1 20
2 1 2
4 1
4 2
```

the output is:

```
30
30
```

A careless solution that remembers only the original group of each node will fail because nodes 1 and 2 become part of the same ordered sequence.

Another edge case is splitting a group containing the queried node but leaving that node on either side of the cut.

For example:

```
4
1 5
1 7
2 1 2
3 2 1
4 2
```

The output is:

```
7
```

Before the split, the sequence is `[1, 2]`. Splitting after the first node creates `[1]` and `[2]`. Node 2 is no longer in the first group, so storing only the old root would give the wrong answer.

A final boundary case is splitting near the end of a group:

```
3
1 8
3 1 1
4 1
```

The output is:

```
8
```

The split does nothing because the group has only one node. An implementation that assumes both resulting parts exist can corrupt parent pointers.

## Approaches

A direct approach is to store every group as a list. Creating a node is easy, and querying a group means summing its list. The problem appears when operations move whole groups or split them. Merging two large groups requires copying or linking many elements, and splitting requires walking to the cut position. In the worst case, $5 \cdot 10^5$ operations can each touch $5 \cdot 10^5$ nodes, giving about $2.5 \cdot 10^{11}$ operations.

The structure of the operations gives the key observation. Groups are not arbitrary sets, they are ordered sequences. The required operations are exactly the operations supported by an implicit treap: concatenate two sequences, split a sequence by position, and maintain aggregate information such as the sum of values.

The remaining challenge is answering which sequence contains a given node. Each treap node stores a parent pointer. Following parent pointers reaches the current root of its group. Because the treap height is logarithmic on average, finding the group is also logarithmic.

The brute force works because it models the groups directly, but fails because it ignores that the groups are dynamic sequences. The observation that every operation is a sequence operation lets us represent every group with an implicit treap and keep all operations fast.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(q^2)$ | $O(q)$ | Too slow |
| Optimal | $O(q \log q)$ expected | $O(q)$ | Accepted |

## Algorithm Walkthrough

1. When a creation query appears, create one implicit treap node. Its value is the given value, its size is one, and its sum is that value. Store its index so future queries can access this node directly.
2. For a merge query, find the roots of the two referenced nodes. If they are already in the same treap, nothing changes. Otherwise, merge the two treaps, placing the first root before the second root. The implicit treap merge operation preserves the sequence order while keeping the tree balanced.
3. For a split query, find the root of the referenced node. Split that treap after the first $z$ nodes. The two resulting treaps represent the prefix and suffix groups. The node itself may end up in either part, which is why we must rely on parent pointers rather than stored group identifiers.
4. For a sum query, climb from the referenced node through parent pointers until reaching the group root. The root stores the sum of its entire treap, so that value is the answer.

Why it works:

The invariant is that every treap represents exactly one current group, and the in-order traversal of the treap is the order of nodes inside that group. Merge keeps the in-order sequence equal to the concatenation of the two groups. Split divides the in-order sequence at the requested position, so both resulting groups contain exactly the correct nodes. The stored subtree sums are updated after every structural change, making the root sum equal to the sum of the whole group. Parent pointers always connect every node to the current root of its treap, so a node query always reaches the correct group.

## Python Solution

```python
import sys
input = sys.stdin.readline

import random
sys.setrecursionlimit(1 << 25)

left = [0]
right = [0]
parent = [0]
size = [0]
total = [0]
value = [0]
priority = [0]

def pull(x):
    if x:
        size[x] = size[left[x]] + size[right[x]] + 1
        total[x] = total[left[x]] + total[right[x]] + value[x]

def merge(a, b):
    if not a:
        if b:
            parent[b] = 0
        return b
    if not b:
        parent[a] = 0
        return a
    if priority[a] > priority[b]:
        right[a] = merge(right[a], b)
        if right[a]:
            parent[right[a]] = a
        pull(a)
        parent[a] = 0
        return a
    else:
        left[b] = merge(a, left[b])
        if left[b]:
            parent[left[b]] = b
        pull(b)
        parent[b] = 0
        return b

def split(t, k):
    if not t:
        return 0, 0
    if size[left[t]] >= k:
        a, b = split(left[t], k)
        left[t] = b
        if b:
            parent[b] = t
        pull(t)
        parent[t] = 0
        if a:
            parent[a] = 0
        return a, t
    else:
        a, b = split(right[t], k - size[left[t]] - 1)
        right[t] = a
        if a:
            parent[a] = t
        pull(t)
        parent[t] = 0
        if b:
            parent[b] = 0
        return t, b

def root_of(x):
    while parent[x]:
        x = parent[x]
    return x

def new_node(v):
    idx = len(value)
    left.append(0)
    right.append(0)
    parent.append(0)
    size.append(1)
    total.append(v)
    value.append(v)
    priority.append(random.randrange(1 << 60))
    return idx

def solve():
    q = int(input())
    ans = []
    nodes = [0] * (q + 1)

    for i in range(1, q + 1):
        query = list(map(int, input().split()))
        t = query[0]

        if t == 1:
            nodes[i] = new_node(query[1])

        elif t == 2:
            y, z = query[1], query[2]
            a = root_of(nodes[y])
            b = root_of(nodes[z])
            if a != b:
                merge(a, b)

        elif t == 3:
            y, z = query[1], query[2]
            r = root_of(nodes[y])
            if size[r] > z:
                split(r, z)

        else:
            y = query[1]
            ans.append(str(total[root_of(nodes[y])]))

    print("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The arrays represent the fields of the treap nodes. Using arrays instead of Python objects reduces memory overhead because the maximum number of nodes is $5 \cdot 10^5$.

`merge` and `split` are the standard implicit treap operations. After every pointer change, `pull` recalculates the subtree size and sum. Parent pointers are updated during these operations because they are required later when finding a node's current group.

The `root_of` function does not need path compression. The treap height is expected to stay logarithmic because priorities are random, so walking upward is fast enough.

The split condition uses `size[left[t]]` because implicit treaps decide positions from the size of the left subtree. This avoids any off-by-one mistakes when separating the first $z$ nodes.

## Worked Examples

Using the sample input:

```
10
1 38788
3 1 1
3 1 2
1 56200
3 1 2
3 1 2
4 4
3 4 4
4 1
3 4 6
```

| Step | Operation | Group containing node 4 | Sum |
| --- | --- | --- | --- |
| 1 | Create node 1 with 38788 | [1] | 38788 |
| 2 | Split after 1 | [1] | 38788 |
| 3 | Split after 2 | [1] | 38788 |
| 4 | Create node 4 with 56200 | [4] | 56200 |
| 5 | Split after 2 | [4] | 56200 |
| 6 | Split after 2 | [4] | 56200 |
| 7 | Query node 4 | [4] | 56200 |

The first trace shows that splitting a single-node group leaves the group unchanged.

A second example:

```
5
1 10
1 20
2 1 2
4 1
4 2
```

| Step | Operation | Sequence | Sum |
| --- | --- | --- | --- |
| 1 | Create node 1 | [10] | 10 |
| 2 | Create node 2 | [20] | 20 |
| 3 | Merge node 1 group before node 2 group | [10,20] | 30 |
| 4 | Query node 1 | [10,20] | 30 |
| 5 | Query node 2 | [10,20] | 30 |

This demonstrates that nodes keep their identity while their surrounding sequence changes.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(q \log q)$ expected | Each operation performs a constant number of treap merges, splits, or root searches. |
| Space | $O(q)$ | One treap node is created for each creation query. |

The largest input contains half a million operations. The logarithmic expected cost of each treap operation keeps the total work around several million recursive calls, which fits comfortably in the memory and time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    old_out = sys.stdout
    sys.stdout = out
    solve()
    sys.stdout = old_out
    sys.stdin = old
    return out.getvalue()

assert run("""10
1 38788
3 1 1
3 1 2
1 56200
3 1 2
3 1 2
4 4
3 4 4
4 1
3 4 6
""") == "56200\n38788\n"

assert run("""5
1 10
1 20
2 1 2
4 1
4 2
""") == "30\n30\n"

assert run("""1
1 5
""") == ""

assert run("""6
1 1
1 1
1 1
2 1 2
2 2 3
4 1
""") == "3\n"

assert run("""5
1 8
1 9
2 1 2
3 1 1
4 1
""") == "8\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single creation | No output | Minimum-size input |
| Two merged nodes | 30 | Basic merge and query |
| Three equal values | 3 | Repeated equal values |
| Split after merge | 8 | Boundary split behavior |

## Edge Cases

For the merge identity issue:

```
5
1 10
1 20
2 1 2
4 1
4 2
```

The algorithm stores nodes separately at creation time, then the merge operation creates one treap containing both nodes. Both parent chains now reach the same root, so both queries return the combined sum.

For splitting around the queried node:

```
4
1 5
1 7
2 1 2
3 2 1
4 2
```

The treap sequence `[5,7]` is split into `[5]` and `[7]`. Node 2 becomes the root of the second treap, so its root sum is 7. The parent traversal finds that new root instead of using stale information.

For a split that cannot separate anything:

```
3
1 8
3 1 1
4 1
```

The algorithm checks the group size before splitting. Since the size is not larger than the requested prefix length, the operation leaves the treap untouched and the query still sees sum 8.
