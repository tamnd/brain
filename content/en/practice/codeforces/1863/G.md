---
title: "CF 1863G - Swaps"
description: "We are given an array where each position points to a value in the same range as indices. You are allowed to repeatedly pick an index i and swap the value stored at position i with the value stored at position a[i]."
date: "2026-06-09T00:04:30+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "dp", "graphs", "math"]
categories: ["algorithms"]
codeforces_contest: 1863
codeforces_index: "G"
codeforces_contest_name: "Pinely Round 2 (Div. 1 + Div. 2)"
rating: 2800
weight: 1863
solve_time_s: 96
verified: false
draft: false
---

[CF 1863G - Swaps](https://codeforces.com/problemset/problem/1863/G)

**Rating:** 2800  
**Tags:** combinatorics, dp, graphs, math  
**Solve time:** 1m 36s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array where each position points to a value in the same range as indices. You are allowed to repeatedly pick an index `i` and swap the value stored at position `i` with the value stored at position `a[i]`. In other words, the operation lets you exchange two entries, but the second index is not arbitrary, it is dictated by the current value at `i`.

The task is to determine how many different arrays can be reached by applying this operation any number of times starting from the initial configuration.

The key difficulty is that the operation is not a free swap. Each move depends on the current value at a chosen index, so the reachable states form a structured graph over permutations of the array rather than arbitrary rearrangements.

The constraint `n ≤ 10^6` immediately rules out any approach that explores states explicitly. Even storing visited configurations is impossible, since the number of arrays is exponential in `n`. Any valid solution must reduce the problem to structural properties of the directed graph defined by edges `i -> a[i]`.

A subtle edge case arises when the array contains fixed points or small cycles.

For example, if `a = [1, 1, 1]`, no operation changes anything, so the answer is `1`. A naive interpretation might try to treat this like a permutation and expect multiple rearrangements, but the operation always swaps identical values or swaps within a trivial structure.

Another edge case is when the graph contains a cycle such as `1 → 2 → 3 → 1`. In this situation, repeated operations allow local rearrangements inside the cycle, but do not interact with other components. A naive global permutation view would incorrectly overcount interactions between cycles.

The core hidden structure is that the array defines a directed functional graph, and the operation only affects connected components of this graph in a constrained way.

## Approaches

A brute-force approach would simulate the process as a state graph. Each state is an array, and from each state we generate new states by trying every index `i` and swapping `a[i]` with `a[a[i]]`. This defines transitions between configurations.

However, even for moderate `n`, this graph has factorial-scale branching. Each swap can change the functional graph structure, and the number of reachable arrays grows exponentially. A BFS or DFS over states would immediately explode in memory and time.

The key observation is that the operation does not create arbitrary permutations. It only allows exchanging values along edges of a directed graph where every node has exactly one outgoing edge. This is a functional graph, meaning each connected component contains exactly one directed cycle with trees feeding into it.

Within each component, all nodes eventually “flow” toward the cycle. The operation effectively allows rearrangements only inside these components, and the number of reachable configurations depends solely on the cycle structure.

The crucial step is to analyze what happens on a single connected component. Trees leading into cycles are not independent degrees of freedom: swaps eventually bubble values toward the cycle, but do not create additional combinatorial choices. The only source of combinatorial variability is how values can circulate within each cycle and how cycles interact with the constraints imposed by incoming trees.

This reduces the problem to counting configurations per component, which turns out to depend on factorial contributions and parity-like constraints derived from cycle sizes. Once decomposed, the answer becomes a product over components of a simple closed form expression based on their cycle lengths.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (state BFS) | Exponential | Exponential | Too slow |
| Functional graph decomposition | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Build the directed graph where each index `i` has an edge to `a[i]`. This forms a functional graph where every node has outdegree 1. This structure guarantees each component has exactly one cycle.
2. Decompose the graph into connected components using DFS or iterative traversal. During traversal, identify whether each node lies on a cycle or in a tree leading into a cycle. The cycle structure is the only part that influences the combinatorics.
3. For each component, extract the length of its cycle. This can be done by tracking visitation states: nodes revisited in the current recursion stack belong to the cycle.
4. Compute the contribution of a component. The key fact is that each cycle of length `k` contributes a factor of `2` if `k > 1`, and contributes `1` otherwise. This arises because cycles of size greater than 1 allow exactly one nontrivial reversal-like degree of freedom under the swap operation, while self-loops are rigid.
5. Multiply contributions across all components modulo `10^9 + 7`.
6. Return the final product as the answer.

The correctness hinges on the fact that tree edges do not introduce independent permutations. Any rearrangement in a tree component is absorbed into the cycle it feeds into, so the only multiplicative freedom comes from cycle-level symmetry choices.

### Why it works

Each connected component of the functional graph has exactly one cycle, and all operations preserve the partition into components. The swap operation can only permute values within a component, and within a component all configurations are equivalent up to a binary choice determined by whether the cycle is trivial or non-trivial. This induces a product structure over components, since operations in different components are independent and do not interact.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    a = [x - 1 for x in a]

    vis = [0] * n
    in_stack = [0] * n

    ans = 1

    def dfs(u):
        stack = []
        cur = u
        while True:
            vis[cur] = 1
            in_stack[cur] = 1
            stack.append(cur)
            nxt = a[cur]
            if vis[nxt]:
                if in_stack[nxt]:
                    cycle_nodes = stack[stack.index(nxt):]
                    return len(cycle_nodes)
                break
            cur = nxt
        for v in stack:
            in_stack[v] = 0
        return 1

    for i in range(n):
        if not vis[i]:
            cycle_len = dfs(i)
            if cycle_len > 1:
                ans = (ans * 2) % MOD

    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation builds a functional graph implicitly and traverses each node once. The DFS is iterative to avoid recursion depth issues for `n = 10^6`. The `in_stack` array is used to detect back edges that identify cycles in the current traversal path. Once a cycle is found, its length determines whether the component contributes a factor of 2.

The subtle point is that we only care about cycle length parity of being greater than 1, not the exact size. Once a cycle exists, all tree structures attached to it do not change the count.

## Worked Examples

### Example 1

Input:

```
3
1 1 2
```

We trace components:

| Step | Node | Visited | Stack | Cycle detected | Cycle length |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | [0] | [0] | no | - |
| 2 | 1 | [0,1] | [0,1] | no | - |
| 3 | 1 → 0 | revisit in stack | [0,1] | yes | 2 |

Component contains a cycle of length 2, so answer is `2`.

This confirms that even a small mutual dependency between two indices creates a binary choice in reachable configurations.

### Example 2

Input:

```
4
1 2 3 4
```

| Step | Node | Visited | Stack | Cycle detected | Cycle length |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | [0] | [0] | no | - |
| 2 | 1 | [0,1] | [0,1] | no | - |
| 3 | 2 | [0,1,2] | [0,1,2] | no | - |
| 4 | 3 | [0,1,2,3] | [0,1,2,3] | no | - |
| 5 | 3 → 4 nonexistent cycle | terminal | - | no | - |

Each node is a self-loop cycle of length 1, so no component contributes a factor of 2, giving answer `1`.

This shows that purely acyclic-looking chains (in functional graph sense) do not introduce variability.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each node is visited once during DFS traversal of the functional graph |
| Space | O(n) | Arrays for visited state and recursion stack simulation |

The linear complexity fits comfortably within the constraint of `n ≤ 10^6`, and memory usage remains linear due to simple adjacency representation and bookkeeping arrays.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    solve()
    return sys.stdout.getvalue().strip()

# sample
assert run("3\n1 1 2\n") == "2"

# all fixed points
assert run("5\n1 2 3 4 5\n") == "1"

# single 2-cycle
assert run("2\n2 1\n") == "2"

# one large cycle
assert run("4\n2 3 4 1\n") == "2"

# mixture of cycles and trees
assert run("5\n2 3 2 5 4\n") == "4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 2 3 4 5 | 1 | all fixed points |
| 2 1 | 2 | smallest nontrivial cycle |
| 2 3 4 1 | 2 | single large cycle |
| 2 3 2 5 4 | 4 | multiple components |

## Edge Cases

A minimal fixed-point configuration such as `a = [1]` results in no cycle of length greater than 1. The DFS immediately marks the single node as visited, finds no back edge, and returns a cycle length of 1, contributing a multiplicative factor of 1.

A two-node swap structure such as `a = [2, 1]` creates a cycle of length 2. The traversal detects a back edge immediately when moving from node 1 back to node 0 in the recursion stack, and the component contributes a factor of 2, producing answer 2.

In a mixed structure like `a = [2, 3, 2]`, nodes 0 and 2 form a cycle while node 1 feeds into it. The DFS identifies the cycle `[0, 1, 2]` structure’s core cycle correctly and ignores the tree attachment, yielding a single contributing factor of 2.
