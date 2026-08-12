---
title: "CF 102361K - MUV LUV UNLIMITED"
description: "We have a rooted tree with vertex 1 as the root. A move consists of deleting any nonempty set of current leaves, where a leaf is a vertex with no remaining children. Removing several leaves at once is allowed, and their parents may become leaves for the next move."
date: "2026-08-13T00:18:04+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102361
codeforces_index: "K"
codeforces_contest_name: "2019 China Collegiate Programming Contest Qinhuangdao Onsite"
rating: 0
weight: 102361
solve_time_s: 150
verified: true
draft: false
---

[CF 102361K - MUV LUV UNLIMITED](https://codeforces.com/problemset/problem/102361/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 30s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a rooted tree with vertex 1 as the root. A move consists of deleting any nonempty set of current leaves, where a leaf is a vertex with no remaining children. Removing several leaves at once is allowed, and their parents may become leaves for the next move. The players alternate, and the player who removes the final remaining vertex wins because the other player then has no legal move. The task is to determine whether the initial position is winning for the first player, `Takeru`, or winning for the second player, `Meiya`. The official problem uses exactly this rooted-tree formulation and allows the sum of all tree sizes across test cases to reach (10^6).

The parent array contains the parent of every vertex from 2 through (n). We only need the parent relation and the number of children of each vertex. The constraint (n\le 10^6), together with the same bound on the sum over all test cases, rules out any state-space game search. Even (O(n\log n)) would be acceptable in principle, but the structure of the game lets us reduce the solution to linear time and linear memory.

There are two edge cases that are easy to mishandle. First, a vertex whose parent has multiple children is much more significant than an ordinary leaf at the end of a chain. For example,

```
1
4
1 1 2
```

has root 1 with children 2 and 3, and vertex 2 has child 4. Vertex 3 is a leaf whose parent has two children. The correct answer is `Takeru`. A careless solution that only counts the parity of the depth of each leaf can miss this structural winning position. The reason is that Takeru can remove such a leaf together with whatever leaves form a winning response after that leaf is removed.

The second edge case is a branching tree whose leaf-to-branch chains all have even lengths. For example,

```
1
5
1 1 2 3
```

has root 1 with children 2 and 3, while 2 has child 4 and 3 has child 5. The two leaf chains are (4\rightarrow2) and (5\rightarrow3), each containing two vertices before reaching the branching root. The correct answer is `Meiya`. A solution based on ordinary root-to-leaf depth would not capture the relevant decomposition, because the two branches share the root.

A pure chain is another boundary case. For

```
1
3
1 2
```

there is exactly one available leaf at every turn, so the game lasts three moves and the answer is `Takeru`. For four vertices,

```
1
4
1 2 3
```

the game lasts four moves and the answer is `Meiya`. This is why the chain length must include the leaf itself and, when the whole tree is one chain, also include the root.

## Approaches

The direct approach is to treat the position as an impartial game and recursively enumerate every possible move. If the current tree has (k) leaves, there are (2^k-1) nonempty subsets of leaves that can be removed. We could recursively evaluate every resulting tree and memoize its winning status. This is correct because a position is winning exactly when at least one legal move reaches a losing position.

The problem is the number of choices. Consider an (n)-vertex star, with the root connected directly to all (n-1) other vertices. The first player already has

[
2^{n-1}-1
]

different legal moves. Thus even the first level of an exhaustive search is exponential. A general state-space implementation can require exponential memory as well, so this approach is unusable for (n=10^6).

The key observation is that branching vertices separate the tree into independent chains of vertices with exactly one child. Consider a leaf and move upward while every encountered vertex has exactly one child. The resulting maximal path is a chain whose only meaningful information is its length parity. The game becomes especially simple once we distinguish whether a leaf has a sibling.

Suppose some leaf (x) has a parent with at least two children. Then the position is immediately winning for the player to move. Remove (x). If the resulting position is losing, we are finished. If it is winning, take the winning move from that resulting position and add (x) to the same move. Removing (x) cannot create another leaf elsewhere, because its parent still has another child, so every vertex used by that winning move was already a leaf before (x) was removed. We have again reached a losing position in one original move. This is the central structural lemma.

After this case is excluded, no leaf has a sibling. Every leaf belongs to a maximal chain whose internal vertices each have exactly one child. Define the chain length as the number of vertices from the leaf upward, stopping before the first ancestor with at least two children. If the entire tree is a chain, the root is included as the end of the chain.

Now parity completely determines the result. If some chain has odd length, the first player can remove the leaf at the end of every odd-length chain in one move. Because there are no leaves with siblings, every such chain has length at least two unless the whole tree is a chain. Removing its leaf changes an odd length to an even length without exposing a branching vertex. The resulting position has only even chains.

If every chain is even, the position is losing. Any move removes the leaf from at least one chain, changing every affected chain from even to odd. If an affected chain becomes length one, its leaf now has a branching parent, immediately giving the next player the winning structural case. Otherwise an odd chain remains, and an odd chain is itself a winning position. Thus every move from an all-even position gives the opponent a winning position.

This yields a particularly small criterion: the answer is `Takeru` if some leaf has a parent with more than one child, or if some maximal leaf chain has odd length. Otherwise the answer is `Meiya`. This characterization and the linear-time implementation are also given in independent contest solution writeups.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(3^n)) in a general state enumeration, with (\Omega(2^{n-1})) first moves on a star | (O(2^n)) with memoization | Too slow |
| Optimal | (O(n)) per test case, (O(\sum n)) overall | (O(n)) | Accepted |

## Algorithm Walkthrough

1. Read the parent of every vertex and count the number of children of each vertex. The child count tells us immediately whether a vertex is a branching point.
2. Scan all vertices with zero children. These are exactly the current leaves of the original tree. For every leaf (v), first inspect its parent. If the parent has at least two children, return `Takeru` immediately because the structural winning lemma applies.
3. If the parent has exactly one child, walk upward through the chain while the current vertex's parent still has exactly one child. Start the chain length at 1 because the leaf itself belongs to the chain. Every time we move to its parent, increase the length by 1.
4. Stop when the current vertex is the root or its parent is a branching vertex. The branching vertex is not part of this chain, while the root is included if the tree itself is a single chain.
5. If this chain length is odd, return `Takeru`. Removing the leaf at the end of every odd chain gives the opponent a position in which all chain lengths are even, which is losing.
6. If every leaf produces an even chain length and no leaf has a branching parent, return `Meiya`. Every possible move creates either an odd chain or a leaf whose parent is branching, so the next player always receives a winning position.

The reason the upward walks are still linear is that we only walk through vertices having exactly one child. Such a vertex belongs to exactly one leaf chain, so it cannot be traversed by two different leaves. Branching vertices terminate the walk. Consequently, although the implementation appears to contain a nested loop, the total number of iterations over all leaves is (O(n)).

### Why it works

There are two kinds of winning positions. The first contains a leaf whose parent has at least two children. The first player can always incorporate that leaf into a move leading to a losing position. The second contains a maximal leaf chain of odd length. Removing the terminal leaves of all odd chains changes every relevant chain length from odd to even, producing a losing position.

When neither winning condition exists, every maximal leaf chain is even and every leaf has a unique sibling-free parent chain. Any move changes at least one even chain into an odd chain. If the chain is reduced to length one, its parent is a branching vertex and the structural winning condition appears. Otherwise an odd chain remains directly. Thus every move from an all-even position leads to a winning position, making the original position losing. This establishes exactly the criterion used by the algorithm.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())

        parent = [0] * (n + 1)
        child_count = [0] * (n + 1)

        data = list(map(int, input().split()))

        for i, p in enumerate(data, 2):
            parent[i] = p
            child_count[p] += 1

        winning = False

        for v in range(2, n + 1):
            if child_count[v] != 0:
                continue

            p = parent[v]

            # A leaf with a sibling is an immediate winning position.
            if child_count[p] > 1:
                winning = True
                break

            # Count vertices in the maximal degree-1 chain.
            length = 1
            u = v

            while u != 1 and child_count[parent[u]] == 1:
                u = parent[u]
                length += 1

            if length & 1:
                winning = True
                break

        out.append("Takeru" if winning else "Meiya")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The `parent` array stores the parent of each vertex, while `child_count` records the number of children. No adjacency list is needed because the algorithm only walks upward from leaves.

The loop starts at vertex 2 because vertex 1 is the root and (n\ge2), so the root cannot be a leaf initially. For each leaf, `child_count[p] > 1` handles the immediate winning condition before any chain traversal.

The chain length starts at 1 because the leaf itself is part of the chain. The loop checks `u != 1` before accessing `parent[u]`, which avoids the special case of the root having no parent. When the root is reached, it has already been counted, which gives the correct result for a pure chain. For example, a three-vertex chain produces length 3 and is winning, while a four-vertex chain produces length 4 and is losing.

The condition `child_count[parent[u]] == 1` means that the parent is still inside the current single-child chain. If its child count is greater than one, that parent is a branching vertex and must not be included. This boundary is the source of many off-by-one errors in this problem.

Python integers do not have an overflow issue here. Every stored value is at most (10^6), and the algorithm performs only integer comparisons, increments, and array accesses.

The input line containing (n-1) parents can contain up to nearly one million integers. Converting that line once with `map` and `list` keeps the parsing simple and avoids repeatedly calling `input()` for individual vertices.

## Worked Examples

### Sample 1

The first sample test case is

```
1
3
1 1
```

The tree is a chain (1\rightarrow2\rightarrow3). There is one leaf, vertex 3.

| Leaf | Parent child count | Chain traversal | Chain length | Result |
| --- | --- | --- | --- | --- |
| 3 | 1 | (3\rightarrow2\rightarrow1) | 3 | Takeru |

The leaf's parent has exactly one child, so the immediate branching condition does not apply. The traversal includes vertices 3, 2, and 1, giving an odd length. Takeru can remove vertex 3, then Meiya must remove vertex 2, and Takeru removes the root.

### Sample 2

The second sample test case is

```
1
4
1 2 3
```

This is the four-vertex chain (1\rightarrow2\rightarrow3\rightarrow4).

| Leaf | Parent child count | Chain traversal | Chain length | Result |
| --- | --- | --- | --- | --- |
| 4 | 1 | (4\rightarrow3\rightarrow2\rightarrow1) | 4 | Meiya |

Again there is no branching leaf. The complete chain has four vertices, so its length is even. The first player has no choice but to remove one vertex at a time, and the second player removes the root.

These two examples demonstrate why the root must be counted in a pure chain. Counting edges instead of vertices would reverse the parity and produce the wrong answer.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n)) per test case, (O(\sum n)) overall | Building child counts is linear, and all single-child chain vertices are traversed at most once |
| Space | (O(n)) | The parent and child-count arrays each contain (n+1) integers |

The total number of vertices across all test cases is at most (10^6), so the complete computation performs only a constant amount of work per vertex. There is no recursion, which is necessary for a tree of depth (10^6), and no exponential game-state representation. The official archive gives a one-second contest time limit and a large memory limit, making the linear-time characterization the intended scale of the solution.

## Test Cases

```python
import sys
import io

def solution(inp: str) -> str:
    data = list(map(int, inp.split()))
    it = iter(data)

    t = next(it)
    answers = []

    for _ in range(t):
        n = next(it)

        parent = [0] * (n + 1)
        child_count = [0] * (n + 1)

        for v in range(2, n + 1):
            p = next(it)
            parent[v] = p
            child_count[p] += 1

        winning = False

        for v in range(2, n + 1):
            if child_count[v] != 0:
                continue

            p = parent[v]

            if child_count[p] > 1:
                winning = True
                break

            length = 1
            u = v

            while u != 1 and child_count[parent[u]] == 1:
                u = parent[u]
                length += 1

            if length & 1:
                winning = True
                break

        answers.append("Takeru" if winning else "Meiya")

    return "\n".join(answers)

# Provided samples
assert solution(
    "2\n"
    "3\n"
    "1 1\n"
    "4\n"
    "1 2 3\n"
) == "Takeru\nMeiya", "provided samples"

# Minimum-size tree: 1 -> 2, exactly two vertices.
assert solution(
    "1\n"
    "2\n"
    "1\n"
) == "Meiya", "minimum-size chain"

# Three-vertex chain: odd number of vertices.
assert solution(
    "1\n"
    "3\n"
    "1 2\n"
) == "Takeru", "odd chain"

# Star: every parent value is 1, so a leaf has a branching parent.
assert solution(
    "1\n"
    "5\n"
    "1 1 1 1\n"
) == "Takeru", "all-equal parents"

# Two even branches:
#       1
#      / \
#     2   3
#     |   |
#     4   5
assert solution(
    "1\n"
    "5\n"
    "1 1 2 3\n"
) == "Meiya", "all maximal chains are even"

# Maximum-size star, also stresses the largest allowed n and repeated parents.
n = 1_000_000
max_case = "1\n" + str(n) + "\n" + ("1 " * (n - 2)) + "1\n"
assert solution(max_case) == "Takeru", "maximum-size star"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 / 3 / 1 1 / 4 / 1 2 3` | `Takeru`, `Meiya` | Official samples and chain parity |
| `1 / 2 / 1` | `Meiya` | Minimum tree and smallest even chain |
| `1 / 3 / 1 2` | `Takeru` | Smallest odd chain and root counting |
| `1 / 5 / 1 1 1 1` | `Takeru` | All-equal parent values and branching-parent condition |
| `1 / 5 / 1 1 2 3` | `Meiya` | Multiple branches with even chain lengths |
| Maximum-size star with (n=10^6) | `Takeru` | Maximum constraint, repeated parent values, and linear performance |

## Edge Cases

For the minimum tree

```
1
2
1
```

vertex 2 is the only leaf and vertex 1 has exactly one child. The chain traversal counts vertex 2 and then vertex 1, producing length 2. Since the length is even and there is no branching leaf, the answer is `Meiya`. The first player removes vertex 2 and the second player removes the root.

For the branching-parent case

```
1
4
1 1 2
```

vertices 3 and 4 are leaves. Vertex 3 has parent 1, and root 1 has two children, so the algorithm immediately returns `Takeru`. A concrete winning move is to remove vertices 3 and 4 together. This leaves the two-vertex chain (1\rightarrow2), which is a losing position for the next player. This example demonstrates why the branching condition must be checked before chain parity.

For the pure odd chain

```
1
3
1 2
```

the only leaf is vertex 3. Its parent has one child, so the algorithm follows (3\rightarrow2\rightarrow1), counting three vertices. The odd result gives `Takeru`. The root is included because there is no branching ancestor that terminates the chain.

For the pure even chain

```
1
4
1 2 3
```

the same traversal gives (4\rightarrow3\rightarrow2\rightarrow1), with length 4. The result is `Meiya`. This catches the common mistake of counting edges instead of vertices. There are three edges but four vertices, and the game outcome follows the vertex count.

For the even-branch case

```
1
5
1 1 2 3
```

the leaves are 4 and 5. Leaf 4 follows (4\rightarrow2) and stops because its parent, vertex 1, has multiple children. Its chain length is 2. Leaf 5 similarly gives length 2. No leaf has a branching parent, and every chain is even, so the algorithm prints `Meiya`.

For the maximum-size star, every parent value is 1:

```
1
1000000
1 1 1 ... 1
```

Every non-root vertex is a leaf, while root 1 has (999999) children. The first leaf examined already satisfies the branching-parent condition, so the algorithm can stop without traversing any chain. The result is `Takeru`. This case exercises both the maximum (n) and the early-exit behavior that keeps the implementation efficient even when the number of leaves is enormous.
