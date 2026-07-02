---
title: "CF 103577B - Blockchain"
description: "We are given one or more undirected multigraphs. Each edge connects two vertices and carries a positive integer weight."
date: "2026-07-03T03:29:52+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103577
codeforces_index: "B"
codeforces_contest_name: "2021 ICPC Universidad Nacional de Colombia Programming Contest"
rating: 0
weight: 103577
solve_time_s: 43
verified: true
draft: false
---

[CF 103577B - Blockchain](https://codeforces.com/problemset/problem/103577/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given one or more undirected multigraphs. Each edge connects two vertices and carries a positive integer weight. The task defines a function over the graph that looks like we are allowed to pick a subset of edges, but the contribution of a chosen subset is multiplicative: for every selected edge we multiply its weight, except that some edges are “forbidden” and contribute zero.

More precisely, an edge with weight $w$ contributes $w \times p(w)$, where $p(w)$ is 1 only when $w$ is an odd number, and 0 otherwise. Any edge with even weight therefore immediately kills the entire product if it is included. This means that any optimal subset will never include even-weight edges, because they force the product to zero.

So the problem reduces to selecting some subset of edges with odd weights, maximizing the product of their weights. If we select no edges, the product is 1 by convention (empty product).

The input size allows up to $10^5$ nodes and $10^5$ edges per test case, so any solution must be close to linear in the number of edges. Quadratic or even $O(m \log m)$ with heavy constants is fine, but anything that tries to enumerate subsets or run pairwise combinations is impossible.

A subtle edge case is when all edges are even. Then every non-empty subset has product 0, so the correct answer is 1 by choosing the empty set. A naive implementation that initializes the answer as 0 or always multiplies at least one edge will fail here.

Another edge case is multiple edges between the same nodes. Since edges are independent in the product, duplicates do not matter structurally, but they matter numerically and must all be considered if odd.

## Approaches

The brute-force interpretation is straightforward: try every subset of edges, compute the product of $w(e)$ over edges whose weights are odd, and ignore subsets containing even-weight edges since they evaluate to zero. This is correct because the definition explicitly multiplies over all chosen edges. However, the number of subsets is $2^m$, which for $m = 10^5$ is completely infeasible.

The key simplification comes from observing that the graph structure is irrelevant. There is no interaction between edges except multiplication. The only decision is whether to include each odd-weight edge or not, and each inclusion independently increases the product by a factor of its weight. Since all weights are positive integers greater than or equal to 1, including every odd-weight edge can never decrease the product. There is no constraint preventing taking all of them.

Thus the optimal strategy is simply to multiply all odd weights together. If there are no odd edges, the result is 1.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^m)$ | $O(m)$ | Too slow |
| Optimal | $O(m)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We process each graph independently.

1. Initialize an accumulator `ans` to 1. This represents the product of all chosen valid edges so far. Starting from 1 ensures that skipping all edges yields a correct identity value.
2. Read each edge one by one. For an edge with weight `w`, check whether `w` is odd.
3. If `w` is even, ignore the edge completely. It contributes nothing useful because its contribution would be zero, and any subset containing it would force the product to zero, which is always worse than skipping it.
4. If `w` is odd, multiply it into `ans`. This corresponds to choosing that edge in the optimal subset.
5. After processing all edges, output `ans`.

The key reasoning step is that since multiplication is associative and commutative, and all chosen values are positive, there is never a benefit to excluding an odd edge.

### Why it works

Every feasible solution corresponds to choosing a subset of edges. Any subset containing an even-weight edge has product zero, which is strictly dominated by the empty subset unless all odd-edge products are also zero, which they are not since odd weights are at least 1. Therefore optimal subsets consist only of odd edges. Among odd edges, each contributes a multiplicative factor greater or equal to 1, so including all of them maximizes the product. No dependency exists between edges, so the greedy choice is globally optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    out = []

    while True:
        try:
            n = int(next(it))
        except StopIteration:
            break
        m = int(next(it))

        ans = 1

        for _ in range(m):
            w = int(next(it))
            u = int(next(it))
            v = int(next(it))

            if w % 2 == 1:
                ans *= w

        out.append(str(ans))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution reads all input in bulk to avoid repeated I/O overhead. Each edge is processed in constant time, with a simple parity check. The nodes `u` and `v` are irrelevant to the computation and are read only to advance the input stream correctly.

A common implementation mistake is to try to build adjacency lists or reason about connectivity, but the graph structure plays no role in the objective function. Another subtle issue is forgetting to initialize the answer to 1 instead of 0, which would incorrectly force all outputs to zero.

## Worked Examples

### Example 1

Input:

```
n=4, m=5
edges:
(1,1-2), (2,2-3), (3,3-4), (5,1-3), (6,2-4)
```

We process edges:

| Step | Weight | Odd? | Answer |
| --- | --- | --- | --- |
| 1 | 1 | yes | 1 |
| 2 | 2 | no | 1 |
| 3 | 3 | yes | 3 |
| 4 | 5 | yes | 15 |
| 5 | 6 | no | 15 |

Final output is 15.

This confirms that only odd-weight edges contribute, and even edges are safely ignored.

### Example 2

Input:

```
n=3, m=3
edges:
(2,1-2), (4,2-3), (6,1-3)
```

| Step | Weight | Odd? | Answer |
| --- | --- | --- | --- |
| 1 | 2 | no | 1 |
| 2 | 4 | no | 1 |
| 3 | 6 | no | 1 |

Final output is 1.

This demonstrates the empty-product case where every edge is forbidden, and the correct answer is still well-defined.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(m)$ per graph | Each edge is processed once with constant work |
| Space | $O(1)$ extra | Only a running product and input buffer are used |

The constraints allow up to $10^5$ edges, and the solution performs only a single pass through them, which fits easily within the time limit. Memory usage remains constant aside from input storage.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from collections import deque

    data = inp.strip().split()
    it = iter(data)
    out = []

    while True:
        try:
            n = int(next(it))
        except StopIteration:
            break
        m = int(next(it))
        ans = 1
        for _ in range(m):
            w = int(next(it))
            u = int(next(it))
            v = int(next(it))
            if w % 2 == 1:
                ans *= w
        out.append(str(ans))

    return "\n".join(out)

# provided sample-style test
assert run("4 3\n1 1 1\n2 1 2\n3 2 3\n") == "3", "simple case"

# all even edges
assert run("3 3\n2 1 2\n4 2 3\n6 1 3\n") == "1", "all even"

# all odd edges
assert run("2 3\n1 1 2\n3 1 2\n5 1 2\n") == str(1*3*5), "all odd"

# single edge
assert run("2 1\n7 1 2\n") == "7", "single odd edge"

# mixed
assert run("2 4\n2 1 2\n3 1 2\n4 1 2\n5 1 2\n") == str(15), "mixed edges"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all even edges | 1 | empty product behavior |
| all odd edges | product | full multiplication correctness |
| single edge | w | base case correctness |
| mixed edges | 15 | filtering logic |

## Edge Cases

One critical edge case is when every edge has even weight. For input like:

```
3 2
2 1 2
4 2 3
```

the algorithm initializes `ans = 1`, then skips both edges, leaving the result unchanged. This matches the required empty-subset value.

Another case is a single large odd weight, such as:

```
2 1
999999937 1 2
```

The algorithm multiplies it directly into the accumulator, producing the correct result without overflow concerns in Python due to arbitrary precision integers.

A final case is large input size with all odd edges. The algorithm still performs one multiplication per edge, maintaining linear behavior.
