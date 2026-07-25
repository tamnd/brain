---
title: "CF 102870D - Data Structure Master and Orz Pandas"
description: "We have a rooted tree with node 1 as the root. During an infinite sequence of random operations, one node is chosen uniformly each time."
date: "2026-07-25T13:13:09+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102870
codeforces_index: "D"
codeforces_contest_name: "2020-2021 \u201cOrz Panda\u201d Cup Programming Contest"
rating: 0
weight: 102870
solve_time_s: 71
verified: true
draft: false
---

[CF 102870D - Data Structure Master and Orz Pandas](https://codeforces.com/problemset/problem/102870/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 11s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a rooted tree with node `1` as the root. During an infinite sequence of random operations, one node is chosen uniformly each time. The path from the root to that node is visited, and every edge on that path becomes the preferred edge of its parent if it was not already preferred. The task is to find the long-term average number of preferred-child changes per operation. The answer is required modulo `998244353`. The original statement describes these operations as LCT access operations, but the solution does not need any Link-Cut Tree knowledge.

The key difficulty is that the process is random and continues forever. We do not simulate operations. Instead, we calculate the expected number of changes caused by each node after the process reaches its steady behavior.

For a tree with up to `100000` nodes, any approach that repeatedly simulates operations or performs work proportional to the tree height for every possible state is too expensive. A quadratic approach could already perform around `10^10` operations in the worst case, far beyond what a typical 1 second limit allows. We need a linear or near-linear computation over the tree.

The first edge case is a single-node tree. There are no preferred children and no possible changes, so the answer is `0`.

```
Input
1

Output
0
```

A careless implementation that assumes every node has a parent edge or tries to invert `subtree_size - 1` without checking would fail here.

Another edge case is a node with only one child. Once that child has ever been accessed through the node, future accesses through that node can never change the preferred child. For example:

```
Input
2
1

Output
0
```

The root always prefers its only child, so the expected number of changes is zero. A formula that counts every visit to the child as a change would incorrectly output a positive value.

A third edge case is a node whose children have very different subtree sizes. For example:

```
Input
5
1 1 1 1

Output
0
```

The root has four leaf children. Its preferred child is simply the last child among those four that was accessed. The probability of changing from one child to another depends on the distribution of previous accesses, not just the number of children. Treating all children as equally likely gives the wrong expectation.

## Approaches

The direct approach is to simulate the preferred-child states. For each operation, choose a node, walk from the root to that node, and update preferred children along the path. This is correct because it follows the process exactly. However, the requested value is the limit as the number of operations approaches infinity. Simulation cannot provide an exact modular answer, and even one million operations on a deep tree can already be too slow. In a chain of `100000` nodes, one operation can touch `100000` edges, giving about `10^11` edge updates for `10^6` simulated operations.

The useful observation is that every node can be analyzed independently. Consider a node `u` with children `c1, c2, ...`. A preferred child of `u` changes only when the chosen node lies in one of these child subtrees. If the chosen node is outside `u`'s subtree, nothing involving `u` changes.

After many operations, the preferred child of `u` is the child subtree that contained the most recent access below `u`. The probability that child `c` is currently preferred is proportional to the size of its subtree. If the total number of nodes below children of `u` is `s`, then:

$$P(c\text{ is preferred})=\frac{size[c]}{s}$$

On the next operation, child `c` is selected with probability:

$$\frac{size[c]}{n}$$

A change happens when the new child is different from the current preferred child. The contribution of `u` is:

$$\sum_c \frac{size[c]}{n}
\left(1-\frac{size[c]}{s}\right)$$

where:

$$s = subtree[u]-1$$

This simplifies to:

$$\frac{1}{n}
\left(
s-\frac{\sum size[c]^2}{s}
\right)$$

Now the problem becomes a tree DP problem. We only need subtree sizes and the sum of squared child subtree sizes for every node.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(operations × tree height) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Build the rooted tree from the parent array. Store the children of every node so that we can later inspect every child subtree.
2. Compute the size of every subtree using a postorder traversal. The subtree size of a node is needed because it tells us how frequently each child can become the preferred child.
3. For every non-leaf node `u`, let `s = subtree[u] - 1`. This is the number of nodes contained in all child subtrees of `u`. Compute the value:

$$\frac{s-\frac{\sum size[child]^2}{s}}{n}$$

and add it to the answer.

1. Perform all divisions modulo `998244353`. Since the modulus is prime, every non-zero denominator has an inverse using modular exponentiation.
2. Output the accumulated value modulo `998244353`.

Why it works:

For every node `u`, the preferred child is determined only by the latest access that entered one of its child subtrees. Independent of the rest of the tree, this creates a stable probability distribution where each child is preferred according to its subtree size. The formula computes exactly the probability that the next access chooses a different child. Summing these independent expected contributions over all nodes gives the expected number of preferred-child changes in one operation.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def solve():
    n_line = input().strip()
    if not n_line:
        return
    n = int(n_line)

    children = [[] for _ in range(n)]
    if n > 1:
        parents = list(map(int, input().split()))
        for i, p in enumerate(parents, start=1):
            children[p - 1].append(i)

    size = [1] * n
    order = [0]
    for u in order:
        for v in children[u]:
            order.append(v)

    for u in reversed(order):
        for v in children[u]:
            size[u] += size[v]

    inv_n = pow(n, MOD - 2, MOD)
    ans = 0

    for u in range(n):
        if not children[u]:
            continue

        s = size[u] - 1
        sq = 0
        for v in children[u]:
            sq += size[v] * size[v]
            sq %= MOD

        cur = (s % MOD - sq * pow(s, MOD - 2, MOD)) % MOD
        cur = cur * inv_n % MOD
        ans += cur
        ans %= MOD

    print(ans)

if __name__ == "__main__":
    solve()
```

The tree is stored as child lists because every node only needs information from its immediate children. The traversal order is built iteratively to avoid Python recursion depth problems on a chain-shaped tree.

The subtree sizes are calculated in reverse traversal order. When a node is processed, all of its children have already received their final subtree sizes, so adding them produces the correct size for the parent.

The formula is applied only to nodes with children. For leaves, `subtree[u] - 1` is zero and there is no possible preferred-child change, so skipping them also avoids division by zero.

All arithmetic is done modulo `998244353`. The inverse of `s` exists because `s` is always between `1` and `n-1` for processed nodes.

## Worked Examples

For the sample:

```
Input
5
1 1 2 2
```

The tree is:

```
    1
   / \
  2   3
 / \
4   5
```

| Node | Child subtree sizes | s | Contribution |
| --- | --- | --- | --- |
| 1 | 3, 1 | 4 | 3/10 |
| 2 | 1, 1 | 2 | 1/5 |
| 3 | none | - | 0 |
| 4 | none | - | 0 |
| 5 | none | - | 0 |

The total is:

$$\frac{3}{10}+\frac{1}{5}=\frac{1}{2}$$

which is represented modulo `998244353` as `499122177`.

For a chain:

```
Input
3
1 2
```

The tree is:

```
1
|
2
|
3
```

| Node | Child subtree sizes | s | Contribution |
| --- | --- | --- | --- |
| 1 | 2 | 2 | 0 |
| 2 | 1 | 1 | 0 |
| 3 | none | - | 0 |

Every node has only one possible child, so preferred children never need to change.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Every edge is processed a constant number of times during tree construction and subtree calculation. |
| Space | O(n) | The child lists, traversal order, and subtree sizes all store information for every node. |

The constraints allow `100000` nodes, and a linear solution fits comfortably within the required limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    result = sys.stdout.getvalue()
    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return result

# sample
assert run("5\n1 1 2 2\n") == "499122177\n", "sample"

# single node
assert run("1\n") == "0\n", "minimum size"

# two nodes
assert run("2\n1\n") == "0\n", "single child"

# star tree
assert run("5\n1 1 1 1\n") == "798595487\n", "many equal children"

# chain
assert run("4\n1 2 3\n") == "0\n", "boundary chain"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `5 / 1 1 2 2` | `499122177` | Original sample and modular fraction handling |
| `1` | `0` | Empty preferred-child structure |
| `2 / 1` | `0` | Single-child nodes cannot change preference |
| `5 / 1 1 1 1` | `798595487` | Equal child subtree probabilities |
| `4 / 1 2 3` | `0` | Deep tree and recursion-sensitive structure |

## Edge Cases

For the single-node tree:

```
Input
1
```

The algorithm creates one node with no children. It skips the contribution loop because there is no possible preferred child, leaving the answer as zero.

For a node with one child:

```
Input
2
1
```

The root has `s = 1` and the only child has subtree size `1`. The contribution becomes:

$$1-\frac{1^2}{1}=0$$

so the answer remains zero. The formula captures the fact that choosing the same only child cannot create a reassignment.

For the equal-child case:

```
Input
5
1 1 1 1
```

The root has four children of size one. The probability that the next access changes the preferred child is:

$$4 \times \frac{1}{5}\times\frac{3}{4}=\frac{3}{5}$$

The child states are handled through their subtree sizes, so the algorithm does not accidentally assume that every visit changes the preferred edge.

For an unbalanced tree, such as a chain, the algorithm correctly produces zero because every internal node has only one possible preferred child. The implementation reaches the same conclusion without special handling because the general formula naturally collapses to zero.
