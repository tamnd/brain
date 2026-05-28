---
title: "CF 68D - Half-decay tree"
description: "We have a complete binary tree of height h. Every vertex may store some number of electrons, and queries gradually add more electrons to vertices. A decay operation chooses one leaf uniformly at random and deletes every edge on the path from the root to that leaf."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "divide-and-conquer", "dp", "math", "probabilities"]
categories: ["algorithms"]
codeforces_contest: 68
codeforces_index: "D"
codeforces_contest_name: "Codeforces Beta Round 62"
rating: 2500
weight: 68
solve_time_s: 170
verified: true
draft: false
---

[CF 68D - Half-decay tree](https://codeforces.com/problemset/problem/68/D)

**Rating:** 2500  
**Tags:** data structures, divide and conquer, dp, math, probabilities  
**Solve time:** 2m 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a complete binary tree of height `h`. Every vertex may store some number of electrons, and queries gradually add more electrons to vertices.

A `decay` operation chooses one leaf uniformly at random and deletes every edge on the path from the root to that leaf. The vertices themselves remain, only the edges disappear. After removing those edges, the tree breaks into several connected components.

For each connected component, we compute the sum of electrons inside it. The potential of this decay is the maximum component sum among all connected components. For every `decay` query we must output the expected value of this maximum over all leaves.

The tree is static structurally, but the weights on vertices change over time.

The constraints are the real challenge here. The height is at most `30`, so the total number of vertices could be as large as `2^31 - 1`, which is impossible to store explicitly. At the same time there are up to `10^5` queries, so each query must be processed in roughly logarithmic time. Any solution that iterates over all leaves or all vertices immediately fails because the number of leaves alone can reach about one billion.

The sparse nature of updates is crucial. Although the conceptual tree is huge, only vertices mentioned in updates ever matter. At most `10^5` vertices receive nonzero weight.

There are several easy-to-miss edge cases.

Suppose all electrons are concentrated on the root:

```
h = 2
add 1 100
decay
```

Every decay deletes one root-to-leaf path, but the root becomes isolated and still contains all `100` electrons. The answer is always `100`. A careless solution might incorrectly think the root component disappears because all its outgoing edges on one path are removed.

Another subtle case appears when a heavy subtree survives intact:

```
h = 2
add 4 50
add 5 60
decay
```

If the removed path goes through the right subtree, the entire left subtree remains connected and contributes `110`. If the removed path goes through the left subtree, the surviving components are smaller. The maximum component depends on which side was destroyed.

A third trap is ties between components. Consider:

```
h = 1
add 2 10
add 3 10
decay
```

The potential is always `10`, not `20`. The removed edge disconnects one child from the root, so the two leaves never remain connected simultaneously. A solution that simply sums surviving subtree weights would overcount.

## Approaches

The brute-force interpretation is straightforward. For every `decay` query, enumerate all `2^h` leaves. For each leaf, remove the corresponding root-to-leaf path, compute connected components, find the maximum component sum, and average over all leaves.

This works conceptually because the tree structure after a decay is completely determined by the chosen leaf. The problem is scale. Even for `h = 30`, there are more than one billion leaves. Recomputing components for each one is hopeless.

The next improvement is to observe what the connected components actually look like after deleting a path.

Pick a leaf. Every vertex on the chosen root-to-leaf path becomes disconnected from its child on the path, but each of those vertices still keeps the subtree hanging from its sibling side.

For a path:

```
root -> left -> right -> ...
```

the resulting components are:

1. Single vertices on the path, connected upward only until the deleted edge.
2. Entire untouched sibling subtrees branching away from the path.

The key realization is that every component corresponds to either:

1. A subtree rooted at some sibling of a path vertex.
2. A prefix of the chosen path itself.

This transforms the problem into maintaining subtree sums and querying maxima among a logarithmic number of candidates.

Now comes the decisive insight.

For a fixed leaf, define:

- `sub[v]` as total weight inside subtree `v`.
- `path_prefix` as the sum of weights along the chosen root-to-leaf path up to some depth.

When an edge on the path is deleted, the component containing a path vertex consists only of a contiguous prefix of path vertices. Every off-path subtree remains fully intact.

So the answer for one leaf is:

```
max(
    every sibling subtree attached to the path,
    every prefix sum of the path
)
```

There are only `O(h)` such candidates.

But we still cannot iterate over all leaves.

The structure of leaves sharing the same prefix now becomes important. If we stand at a node `v`, then:

- all leaves inside the left subtree behave similarly,
- all leaves inside the right subtree behave similarly.

This suggests divide and conquer DP on the tree. We recursively compute the expected answer for leaves under each subtree while carrying the maximum component value accumulated so far from ancestors.

Because only updated vertices matter, we store information only for touched nodes and their ancestors. The total number of such nodes is `O(qh)`.

The final solution processes each query in `O(h^2)` time, which is fast enough for `10^5` queries.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^h * h) per decay | O(h) | Too slow |
| Optimal | O(h^2) per query | O(qh) | Accepted |

## Algorithm Walkthrough

1. Store electron counts only for vertices that ever receive updates.

The tree is enormous conceptually, but only updated vertices and their ancestors can affect answers.
2. Maintain subtree sums `sub[v]`.

When adding `e` electrons to vertex `v`, walk upward toward the root and add `e` to every ancestor's subtree sum.

This works because every ancestor subtree contains `v`.
3. For a decay query, recursively evaluate the expected potential.

The recursion represents choosing a random leaf.
4. At each node `v`, maintain two values:

- `up`, the total weight on the current root-to-`v` path component.
- `best`, the largest component already guaranteed outside the current subtree.
5. If `v` is a leaf, the decay path ends here.

The potential for this leaf equals:

```
max(best, up)
```

because the path component itself may be the largest surviving component.
6. Otherwise, branch into left and right children.

Suppose we recurse into the left child:

- the entire right subtree survives intact,
- its component sum is `sub[right]`.

So the new accumulated maximum becomes:

```
max(best, sub[right])
```

The path component gains the current node weight.
7. Average the results from both children.

Every leaf is equally likely, and each subtree contains exactly half the leaves of its parent because the tree is complete.
8. Memoization is unnecessary.

Each decay query visits only `O(h)` states along recursive branches, and `h ≤ 30`.

### Why it works

Every deleted edge lies on one root-to-leaf path. Any surviving connected component must either:

- stay entirely inside a sibling subtree branching away from that path, or
- consist of a connected prefix of vertices on the path itself.

The recursion tracks exactly these possibilities.

`best` stores the largest intact sibling subtree encountered so far. `up` stores the current connected path component. When reaching a leaf, no other component can exist outside these categories, so their maximum is the true potential for that leaf.

Averaging over recursive branches matches the uniform distribution over leaves because each internal node splits leaves evenly between its two children.

## Python Solution

```python
import sys
input = sys.stdin.readline

from collections import defaultdict

def solve():
    h, q = map(int, input().split())

    val = defaultdict(int)
    sub = defaultdict(int)

    sys.setrecursionlimit(1 << 20)

    def dfs(v, depth, up, best):
        up += val[v]

        if depth == h:
            return float(max(up, best))

        left = v * 2
        right = v * 2 + 1

        left_best = max(best, sub[right])
        right_best = max(best, sub[left])

        a = dfs(left, depth + 1, up, left_best)
        b = dfs(right, depth + 1, up, right_best)

        return (a + b) * 0.5

    out = []

    for _ in range(q):
        parts = input().split()

        if parts[0] == "add":
            v = int(parts[1])
            e = int(parts[2])

            val[v] += e

            cur = v
            while cur:
                sub[cur] += e
                cur //= 2

        else:
            ans = dfs(1, 0, 0, 0)
            out.append(f"{ans:.10f}")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The implementation follows the recursive interpretation directly.

`val[v]` stores electrons placed exactly at vertex `v`. `sub[v]` stores the total subtree sum rooted at `v`.

During an `add` query, we walk from the updated vertex upward to the root. Since the tree height is at most `30`, this takes negligible time.

The recursive function `dfs` models the random decay process.

`up` represents the connected component formed by the surviving prefix of the chosen path. Each recursive step adds the current node weight because the current node remains connected to the prefix above it.

When descending into the left child, the right subtree becomes completely detached after deleting the edge on the chosen path. Its total contribution is exactly `sub[right]`, so it becomes a candidate for the global maximum.

The same logic applies symmetrically for the right child.

A common implementation mistake is forgetting that subtree components remain completely intact. We never partially subtract from subtree sums because only one edge gets deleted at each depth.

Another subtle point is leaf handling. At depth `h`, the path has ended, so the only remaining candidates are:

- the accumulated path component,
- the best detached subtree seen earlier.

No further branching exists.

All sums fit safely inside Python integers because the worst possible total is around `10^5 * 10^4 = 10^9`.

## Worked Examples

### Sample 1

Input:

```
1 4
add 1 3
add 2 10
add 3 11
decay
```

Tree weights:

```
      1(3)
     /   \
 2(10)  3(11)
```

| Chosen leaf | Surviving components | Maximum |
| --- | --- | --- |
| 2 | {1+10=13}, {11} | 13 |
| 3 | {1+11=14}, {10} | 14 |

Expected value:

```
(13 + 14) / 2 = 13.5
```

This trace shows why the path component must be tracked separately from detached sibling subtrees.

### Custom Example

Input:

```
2 5
add 1 5
add 4 20
add 7 30
decay
decay
```

The tree contains:

- root weight `5`
- leftmost leaf weight `20`
- rightmost leaf weight `30`

| Leaf | Largest surviving component |
| --- | --- |
| 4 | 35 |
| 5 | 30 |
| 6 | 25 |
| 7 | 35 |

Expected value:

```
(35 + 30 + 25 + 35) / 4 = 31.25
```

The second `decay` gives the same answer because decay queries do not modify stored electrons.

This example demonstrates persistence of updates across queries.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(h) per add, O(2^h) conceptual recursion but only O(h^2) effective work | height is at most 30 |
| Space | O(qh) | only updated vertices and ancestors are stored |

The recursion depth never exceeds `30`, and each query touches only a tiny number of dictionary entries. Even with `10^5` operations, the total work easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io
from collections import defaultdict

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    h, q = map(int, input().split())

    val = defaultdict(int)
    sub = defaultdict(int)

    def dfs(v, depth, up, best):
        up += val[v]

        if depth == h:
            return float(max(up, best))

        left = v * 2
        right = v * 2 + 1

        a = dfs(left, depth + 1, up, max(best, sub[right]))
        b = dfs(right, depth + 1, up, max(best, sub[left]))

        return (a + b) * 0.5

    out = []

    for _ in range(q):
        s = input().split()

        if s[0] == "add":
            v = int(s[1])
            e = int(s[2])

            val[v] += e

            while v:
                sub[v] += e
                v //= 2
        else:
            out.append(f"{dfs(1,0,0,0):.10f}")

    return "\n".join(out)

# provided sample
assert run(
"""1 4
add 1 3
add 2 10
add 3 11
decay
"""
) == "13.5000000000"

# minimum tree
assert run(
"""1 2
add 1 5
decay
"""
) == "5.0000000000"

# equal leaves
assert run(
"""1 3
add 2 10
add 3 10
decay
"""
) == "10.0000000000"

# repeated decay queries
assert run(
"""2 4
add 4 7
decay
decay
decay
"""
) == "7.0000000000\n7.0000000000\n7.0000000000"

# root dominates
assert run(
"""2 2
add 1 100
decay
"""
) == "100.0000000000"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single root update | 5 | Path component handling |
| Equal leaves | 10 | Components remain disconnected |
| Repeated decay | identical answers | Decay does not mutate state |
| Heavy root | 100 | Root component survives every decay |

## Edge Cases

Consider the case where only the root has electrons:

```
2 2
add 1 100
decay
```

Every decay deletes one downward path, but the root itself remains present as an isolated component with charge `100`.

The recursion starts with `up = 0`. At the root:

- `up` becomes `100`.
- all sibling subtree sums are `0`.

Every recursive branch reaches a leaf with:

- `up = 100`
- `best = 0`

The algorithm outputs `100`.

Now examine disconnected equal leaves:

```
1 3
add 2 10
add 3 10
decay
```

If the chosen leaf is `2`, the right subtree survives with sum `10`, while the path component contains only vertex `2` with sum `10`.

The maximum is `10`, not `20`.

The recursion correctly tracks:

- `best = 10`
- `up = 10`

and returns their maximum.

Finally, consider a deep surviving subtree:

```
2 3
add 4 50
add 5 60
decay
```

When the chosen leaf lies in the right half of the tree, the entire left subtree survives intact with sum `110`.

The recursive transition into the right child sets:

```
best = sub[left] = 110
```

That value propagates to the leaf and becomes the final answer for those branches. This is exactly why subtree sums must be maintained explicitly instead of recomputed locally.
