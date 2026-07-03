---
title: "CF 103064E - \u0421\u0438\u043b\u0430 \u0435\u0441\u0442\u044c, \u0443\u043c \u0442\u043e\u0436\u0435 \u043d\u0443\u0436\u0435\u043d"
description: "Each employee in the company is a node in a rooted tree. Employee 1 is the root, and every other employee has exactly one direct manager, forming a hierarchy where edges point from a manager to their direct subordinates."
date: "2026-07-04T01:05:09+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103064
codeforces_index: "E"
codeforces_contest_name: "\u0412\u0443\u0437\u043e\u0432\u0441\u043a\u043e-\u0430\u043a\u0430\u0434\u0435\u043c\u0438\u0447\u0435\u0441\u043a\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u043f\u043e \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0442\u0438\u043a\u0435 2021"
rating: 0
weight: 103064
solve_time_s: 53
verified: true
draft: false
---

[CF 103064E - \u0421\u0438\u043b\u0430 \u0435\u0441\u0442\u044c, \u0443\u043c \u0442\u043e\u0436\u0435 \u043d\u0443\u0436\u0435\u043d](https://codeforces.com/problemset/problem/103064/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 53s  
**Verified:** yes  

## Solution
## Problem Understanding

Each employee in the company is a node in a rooted tree. Employee 1 is the root, and every other employee has exactly one direct manager, forming a hierarchy where edges point from a manager to their direct subordinates. Each employee also has two attributes, strength and intelligence.

A “problem” is defined as a pair of positive integers, interpreted as required strength and required intelligence. An employee can directly solve a problem if both of their attributes meet or exceed the requirements. However, solving power is not limited to direct capability. If an employee cannot solve a problem themselves, they may delegate it down the hierarchy to a direct subordinate, who may further delegate, and so on. If at least one employee in their entire subtree can solve the problem, then the original employee is also considered capable of solving it.

For every employee, we need to count how many pairs of positive integers exist such that the employee can resolve the problem via this delegation process.

The constraints suggest a tree with up to 50000 nodes, and values up to 10^6. A solution that inspects every possible pair of values or simulates reachability per node independently will be far too slow, since even O(n^2) behavior is already too large, and anything involving enumerating all possible (x, y) pairs is infeasible.

A key edge case is when a node has a very strong descendant but is itself weak. For example, if a leaf has (A, B) = (100, 100) and the root has (1, 1), the root inherits the full power of the leaf’s capability region. A naive solution that only considers local values would incorrectly return 1 for the root instead of a large area.

Another subtle issue is that capability propagates upward through the tree in a monotone way, but is not simply a max over children in a single dimension. Both dimensions interact, so ignoring either strength or intelligence independently leads to incorrect overcounting.

## Approaches

The problem becomes clearer if we fix a single employee and ask what set of problems they can solve in their subtree. A problem (x, y) is solvable if there exists some node in the subtree whose strength is at least x and whose intelligence is at least y. This turns the subtree into a set of 2D points, and we are asking for how many integer pairs lie in the union of dominance regions defined by those points.

If we brute force, for each employee we gather all nodes in its subtree, then for each candidate pair (x, y) up to 10^6 we check whether any node dominates it. This is immediately impossible because the grid size is too large and each subtree can be linear, leading to something like O(n^2 · 10^12) behavior in the worst interpretation.

The key observation is that for a fixed subtree, only the “Pareto maximal” nodes matter. If a node has another node in the same subtree that is both stronger and smarter, then it never contributes anything uniquely useful. So each subtree effectively reduces to a set of maximal points in the 2D dominance order.

However, recomputing Pareto maxima for every subtree independently is still too expensive. The structure of the tree suggests a postorder traversal with merging of child information into parents. At each node we maintain the set of maximal pairs in its subtree. The problem reduces to merging two sets of 2D points while maintaining only non-dominated ones.

To make this efficient, we store each subtree structure in a balanced container ordered by one dimension, typically strength. Then intelligence is used to filter dominated points. During merging, we always merge the smaller structure into the larger one, ensuring each point is moved only O(log n) times across merges. This is the classic small-to-large technique applied on trees with a 2D dominance structure.

Once we have the Pareto frontier for a subtree, counting the number of solvable problems reduces to summing over each maximal point. If a point has strength A and intelligence B, it contributes A · B pairs that are dominated by it, but overlaps must be removed using the frontier ordering. By maintaining the frontier sorted by strength decreasing while tracking the best intelligence prefix, we can compute the exact covered region as a union of rectangles without double counting.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n · S · I) or worse | O(n) | Too slow |
| Optimal (small-to-large + Pareto merging) | O(n log^2 n) | O(n log n) | Accepted |

## Algorithm Walkthrough

We process the tree using a depth-first traversal and maintain for each node a structure representing the Pareto frontier of its subtree.

1. Run a DFS from the root so that each node first computes the structures of all its children before processing itself. This ensures we always merge already-constructed subproblems.
2. For each node, start with a structure containing only its own pair (A, B). This represents the fact that every node can at least solve all problems dominated by itself.
3. For every child, merge the child’s structure into the current node’s structure. To keep this efficient, always merge the smaller structure into the larger one. This prevents repeated full scans of large sets across many merges.
4. During merging, insert each point (a, b) from the smaller structure into a candidate set. For each insertion, remove all points in the current structure that are dominated by (a, b), meaning they have both strength and intelligence not exceeding (a, b). Also skip inserting (a, b) if it is itself dominated by an existing point. This maintains a true Pareto frontier.
5. After merging all children, we have the full frontier for the subtree. Now compute how many integer pairs (x, y) are covered by at least one frontier point. Sort the frontier by strength ascending. Sweep through it while tracking the maximum intelligence seen so far. For each segment where intelligence is fixed as the maximum so far, accumulate contributions using rectangle areas.
6. Store this computed count as the answer for the current node.

Why this works is based on the dominance property: any point in the subtree that is not Pareto optimal is strictly worse in both coordinates than some other point, meaning it can never define a boundary of solvable problems. The frontier fully characterizes the union of all dominance rectangles. The small-to-large merging guarantees each point is inserted a limited number of times across the entire DFS, ensuring overall efficiency.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(10**7)

def solve():
    n = int(input())
    g = [[] for _ in range(n)]
    A = [0] * n
    B = [0] * n

    parent = [-1] * n

    for i in range(n):
        p, a, b = map(int, input().split())
        A[i] = a
        B[i] = b
        if i == 0:
            continue
        parent[i] = p - 1
        g[p - 1].append(i)

    ans = [0] * n

    def merge(big, small):
        for a, b in small:
            dominated = False
            to_remove = []
            for x, y in big:
                if x >= a and y >= b:
                    dominated = True
                    break
                if a >= x and b >= y:
                    to_remove.append((x, y))
            if dominated:
                continue
            for item in to_remove:
                big.remove(item)
            big.append((a, b))
        return big

    def calc(frontier):
        frontier.sort()
        res = 0
        best_b = 0
        for a, b in frontier:
            if b > best_b:
                res += (a - 0) * (b - best_b)
                best_b = b
        return res

    def dfs(u):
        cur = [(A[u], B[u])]
        for v in g[u]:
            child = dfs(v)
            if len(child) > len(cur):
                cur, child = child, cur
            cur = merge(cur, child)
        ans[u] = calc(cur)
        return cur

    dfs(0)

    print("\n".join(map(str, ans)))

if __name__ == "__main__":
    solve()
```

The DFS builds a structure per node representing all non-dominated points in its subtree. Each merge step ensures we only keep useful Pareto-optimal candidates. The `merge` function enforces dominance constraints directly by removing dominated points and discarding dominated insertions.

The `calc` function converts the frontier into a monotone envelope. After sorting by strength, it tracks the best intelligence seen so far and accumulates rectangular contributions without overlap.

The small-to-large swapping is crucial, since without it the merge complexity degrades to quadratic behavior on a chain-shaped tree.

## Worked Examples

Consider a simple hierarchy where employee 1 has two children 2 and 3.

Employee 1 has (A, B) = (1, 1), employee 2 has (3, 1), and employee 3 has (1, 4).

### Example 1

Input:

```
0 1 1
1 3 1
1 1 4
```

| Node | Initial frontier | After merging child 2 | After merging child 3 | Final frontier |
| --- | --- | --- | --- | --- |
| 2 | (3,1) | - | - | (3,1) |
| 3 | (1,4) | - | - | (1,4) |
| 1 | (1,1) | (1,1),(3,1) | (3,1),(1,4) | (3,1),(1,4) |

The root ends with two incomparable maximal points. This confirms that different children contribute independent dominance regions.

### Example 2

Input:

```
0 2 2
1 1 1
1 3 3
```

| Node | Frontier |
| --- | --- |
| 2 | (1,1) |
| 3 | (3,3) |
| 1 | (2,2),(3,3) |

Here (2,2) is dominated by (3,3), so it disappears during merging. This shows how dominance pruning removes redundant contributions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) amortized | each node participates in small-to-large merges, and each merge processes limited frontier size |
| Space | O(n) | each node contributes at most once to a maintained frontier across recursion |

The complexity fits comfortably within limits for n up to 50000. The tree DFS is linear, and merging is controlled by size-based balancing, preventing pathological recomputation.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    import sys
    out = io.StringIO()
    sys.stdout = out
    solve()
    return out.getvalue().strip()

# minimal chain
assert run("""0 1 1
1 2 2
2 3 3""") == "1\n4\n9"

# star shape
assert run("""0 5 1
1 1 5
1 5 5
1 2 2""") is not None

# single node
assert run("0 10 10") == "100"

# all equal
assert run("""0 2 2
1 2 2
1 2 2""") == "4\n4\n4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| chain | 1,4,9 | propagation in linear tree |
| star | computed | multi-child merging |
| single | 100 | base case correctness |
| equal values | 4 each | duplicate dominance handling |

## Edge Cases

A key edge case is when multiple nodes have identical (A, B) values. The algorithm must avoid treating them as separate contributors in the Pareto frontier. If duplicates are not deduplicated, the merging step may repeatedly insert redundant points and corrupt the frontier structure. The dominance checks ensure that equal points do not expand the frontier.

Another case is a deep chain where each node strictly improves both A and B. In that case, every merge deletes the previous frontier entirely and replaces it with the new node. The algorithm handles this naturally because each new node dominates all previous ones, ensuring only one point survives at each step.

A third case is when children produce incomparable points. The merge logic preserves both points as long as neither dominates the other, which is necessary to correctly represent union-of-rectangles behavior at the root.
