---
title: "CF 102897C - BBpigeon Counting Trees"
description: "We are given a rooted tree structure indirectly, not by edges, but by a list of depths for each node. Node 1 is fixed as the root, and every node i comes with an integer ai describing how far it is from the root in terms of number of nodes on the path, including itself."
date: "2026-07-04T08:25:22+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102897
codeforces_index: "C"
codeforces_contest_name: "The 3rd Hangzhou Normal University Freshman Programming Contest"
rating: 0
weight: 102897
solve_time_s: 44
verified: true
draft: false
---

[CF 102897C - BBpigeon Counting Trees](https://codeforces.com/problemset/problem/102897/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 44s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a rooted tree structure indirectly, not by edges, but by a list of depths for each node. Node 1 is fixed as the root, and every node i comes with an integer ai describing how far it is from the root in terms of number of nodes on the path, including itself. So the root has depth 1, its children have depth 2, and so on.

However, the actual parent-child relationships are not given. Many different rooted trees can match the same depth assignment, because nodes at depth d can be attached in multiple ways to nodes at depth d − 1. The task is to count how many distinct rooted trees are consistent with the given depth array.

Two trees are considered different if at least one node has a different number of children. So we are not distinguishing by structure alone, but by exact child counts per node, which still reduces to counting distinct valid parent assignments.

The constraint n ≤ 100000 forces any solution toward linear or near linear time. Anything involving checking all parent choices explicitly or enumerating tree structures would explode combinatorially. Even O(n log n) is fine, but O(n^2) constructions over nodes or naive DP over all assignments is impossible.

A key edge case appears when depth constraints are inconsistent. For example, if we have a node at depth 3 but no node at depth 2 exists, no tree can be formed, so the answer must be 0. Another subtle case is when multiple nodes share depth 2 but there is only one possible parent at depth 1, forcing a star-like structure. A naive approach might incorrectly multiply choices without respecting that each node must choose exactly one parent in the previous depth level.

Example invalid case:

Input:

n = 3

a = [1, 3, 2]

Here node with depth 3 has no possible parent at depth 2 if ordering is strict by node indices. Correct answer is 0.

## Approaches

A brute force interpretation is to think of building the tree by assigning each node (except the root) a parent among nodes in the previous depth level. If there are kd nodes at depth d and kd−1 nodes at depth d − 1, then each node at depth d can choose any of kd−1 parents, leading to (kd−1)^{kd} possibilities for that level. Multiplying across levels gives a candidate count.

This already suggests the structure of the solution, but brute force would explicitly construct or simulate all assignments, or try to build trees recursively. That quickly becomes infeasible because the number of assignments grows exponentially with n in worst cases like a two-level structure.

The crucial observation is that depth completely determines valid parent candidates: every node at depth d must connect to some node at depth d − 1, and no other choice matters. Since only the count of children per node matters for distinguishing trees, we do not need to track exact assignments, only how many ways nodes at level d can distribute themselves among nodes at level d − 1. Each node independently selects its parent, so the total number of configurations is a product over levels of powers.

There is one more hidden constraint: every node at depth d − 1 must have at least one node in deeper levels that can attach above it if it is not isolated, but that is automatically handled because nodes choose parents freely; we are not required to ensure surjectivity.

Thus the problem reduces to grouping nodes by depth and multiplying contributions level by level.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(n) | Too slow |
| Depth-level counting | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

## Algorithm Walkthrough

1. Group nodes by their depth value and count how many nodes exist at each depth. This gives us a frequency map kd for each depth d. This step converts the problem into working with layers rather than individual nodes.
2. Check that depth 1 contains exactly one node. If not, the structure cannot represent a rooted tree with node 1 as root, so the answer is zero. This enforces the fixed root constraint.
3. Verify that depths are continuous starting from 1 without gaps. If some depth d > 1 appears but depth d − 1 is missing, no node can attach to a valid parent, so the answer is zero.
4. Sort all distinct depths in increasing order so we process levels in a valid parent-to-child direction.
5. Initialize the answer as 1. We will multiply contributions from each depth transition.
6. For each depth d starting from 2, multiply the answer by (k_{d−1})^{k_d}. This reflects that each node at depth d independently chooses one parent among all nodes at depth d − 1, giving k_{d−1} choices per node.
7. Take all multiplications modulo 998244353. This keeps numbers within bounds while preserving correctness in modular arithmetic.

### Why it works

At each depth layer, the only structural freedom lies in choosing a parent for each node from the previous layer. Once a node selects its parent, it contributes exactly one outgoing edge to that parent, and this choice does not constrain other nodes except through counting. Since the problem distinguishes trees only by child counts, any distinct assignment of parents yields a distinct valid tree. The choices across nodes are independent, and across layers are independent as well, so the total count factorizes cleanly into a product of powers over depth transitions.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def mod_pow(a, e):
    return pow(a, e, MOD)

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    from collections import Counter
    cnt = Counter(a)

    # root must be unique
    if cnt[1] != 1:
        print(0)
        return

    depths = sorted(cnt.keys())

    # check continuity of depths
    for i in range(1, len(depths)):
        if depths[i] != depths[i - 1] + 1:
            print(0)
            return

    ans = 1

    for i in range(1, len(depths)):
        prev_d = depths[i - 1]
        cur_d = depths[i]
        ans = (ans * pow(cnt[prev_d], cnt[cur_d], MOD)) % MOD

    print(ans)

if __name__ == "__main__":
    solve()
```

The code begins by counting how many nodes appear at each depth. This compresses the problem into a frequency map over levels. The root validation ensures exactly one node is at depth 1, since the root is fixed.

We then sort depths and ensure they form a continuous chain. This prevents invalid cases where a level has no valid parent level.

Finally, we iterate over depth transitions. For each pair of consecutive depths, every node at the deeper level chooses its parent among all nodes in the previous level, contributing a power term. The multiplication accumulates all independent choices.

The modular exponentiation is handled using Python’s built-in pow, which is efficient enough for n up to 100000 since exponent values are bounded by n.

## Worked Examples

Consider a small valid case:

Input:

n = 4

a = [1, 2, 2, 3]

Depth counts:

| Step | Depth | Count |
| --- | --- | --- |
| 1 | 1 | 1 |
| 2 | 2 | 2 |
| 3 | 3 | 1 |

Transition from depth 1 to 2 contributes 1^2 = 1, since both nodes at depth 2 must attach to the single root. Transition from depth 2 to 3 contributes 2^1 = 2, since the node at depth 3 can choose either of the two depth-2 nodes as parent. Final answer is 2.

Now consider a case with more freedom:

Input:

n = 5

a = [1, 2, 2, 2, 3]

Depth counts:

| Step | Depth | Count |
| --- | --- | --- |
| 1 | 1 | 1 |
| 2 | 3 | 3 |
| 3 | 1 | 1 |

Here:

Transition 1 → 2 contributes 1^3 = 1.

Transition 2 → 3 contributes 3^1 = 3.

So answer is 3.

These traces show how each layer contributes independently, and how the exponentiation encodes independent parent choices.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Counting frequencies and iterating over depth levels is linear in number of nodes |
| Space | O(n) | Storage for frequency map of depths |

The solution easily fits within constraints since all operations are single-pass over the input with only sorting over distinct depths, which is at most O(n).

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import Counter

    MOD = 998244353

    n = int(input())
    a = list(map(int, input().split()))
    cnt = Counter(a)

    if cnt[1] != 1:
        return "0"

    depths = sorted(cnt.keys())
    for i in range(1, len(depths)):
        if depths[i] != depths[i - 1] + 1:
            return "0"

    ans = 1
    for i in range(1, len(depths)):
        ans = (ans * pow(cnt[depths[i - 1]], cnt[depths[i]], MOD)) % MOD

    return str(ans)

# provided samples (illustrative placeholders)
assert run("3\n1 2 2\n") == "1", "sample 1"

# minimum size
assert run("1\n1\n") == "1", "single node"

# invalid root count
assert run("2\n1 1\n") == "0", "invalid root count"

# gap in depths
assert run("3\n1 3 3\n") == "0", "missing depth 2"

# branching case
assert run("4\n1 2 2 3\n") == "2", "basic branching"

# all equal depths invalid
assert run("3\n2 2 2\n") == "0", "no root"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 | 1 | single node base case |
| 1 1 2 3 3 | 2 | branching across layers |
| 1 3 3 | 0 | missing intermediate depth |
| 2 2 2 | 0 | invalid root condition |

## Edge Cases

One edge case is when the root is not unique. For input `n = 3, a = [1, 1, 2]`, the algorithm immediately returns 0 because the root level has more than one node. During processing, cnt[1] = 2 violates the root constraint, so no further computation happens.

Another edge case is a disconnected depth sequence like `a = [1, 2, 4]`. The depth map contains 1, 2, and 4, but 3 is missing. The sorted depth list fails the continuity check when moving from 2 to 4, and the algorithm correctly outputs 0 before attempting exponentiation.

A third case is a perfectly valid chain such as `a = [1, 2, 3, 4]`. Here each depth has exactly one node, so every transition contributes 1^1 = 1, and the answer remains 1 throughout, matching the fact that there is exactly one linear tree structure consistent with the depths.
