---
title: "CF 1057A - Bmail Computer Network"
description: "We are given a growing network of routers that forms a tree rooted at router 1. Every router except the first was added one by one, and each new router was directly connected to exactly one earlier router."
date: "2026-06-15T09:46:40+07:00"
tags: ["codeforces", "competitive-programming", "*special", "dfs-and-similar", "trees"]
categories: ["algorithms"]
codeforces_contest: 1057
codeforces_index: "A"
codeforces_contest_name: "Mail.Ru Cup 2018 - Practice Round"
rating: 900
weight: 1057
solve_time_s: 292
verified: true
draft: false
---

[CF 1057A - Bmail Computer Network](https://codeforces.com/problemset/problem/1057/A)

**Rating:** 900  
**Tags:** *special, dfs and similar, trees  
**Solve time:** 4m 52s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a growing network of routers that forms a tree rooted at router 1. Every router except the first was added one by one, and each new router was directly connected to exactly one earlier router. This means every router has a single parent, and router 1 is the original root with no parent.

The input gives, for each router from 2 to n, the index of the router it was attached to when it was created. From this information, we can reconstruct the tree structure, but the task does not ask for the entire structure. Instead, we are only interested in one specific route: the unique path from router 1 to router n.

Because each router has exactly one parent, there is exactly one simple path from node 1 to node n in this tree. The output must list the nodes on this path in order.

The constraint n up to 200000 implies that any solution must be linear or near-linear. A quadratic approach that repeatedly searches or rebuilds paths would be too slow because it could perform on the order of 10^10 operations in the worst case. A single pass reconstruction or a simple traversal is required.

A subtle issue appears if one tries to “simulate upward walking” without storing parents. If we do not record parent pointers explicitly, we might repeatedly recompute ancestry, which leads to repeated scans and becomes inefficient. Another potential mistake is building adjacency lists and running a DFS from 1 to n without ensuring correctness of path reconstruction, which could accidentally return a full traversal path instead of the unique simple path.

## Approaches

A brute-force way to solve the problem is to construct the full tree using adjacency lists and then run a depth-first search from node 1 until node n is found. During DFS, we maintain a current path and return it once we reach n. This works because the graph is a tree, so there is exactly one path between any two nodes.

However, this approach risks unnecessary exploration of large subtrees. In the worst case, the DFS may traverse nearly all edges before finding node n, leading to O(n) traversal. While O(n) is actually acceptable, the implementation is more complex than needed and can easily be written incorrectly if backtracking is mishandled.

The key observation is that we do not need to search at all. Each node explicitly stores its parent. This means we can reconstruct the path from n back to 1 by repeatedly following parent pointers. Once we reach node 1, we reverse the collected sequence to obtain the path in the correct direction.

This reduces the problem to a simple pointer-chasing process that is guaranteed linear in the length of the path, which is at most n.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| DFS search from 1 to n | O(n) | O(n) | Accepted but unnecessary |
| Parent chain reconstruction | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We use the fact that every node has exactly one parent except node 1.

1. Read the parent array where p[i] gives the parent of node i. We conceptually define p[1] = 0 since it has no parent.
2. Start from node n and repeatedly move to its parent, storing each visited node in a list. This builds the path in reverse order.
3. Stop when we reach node 1, because it is the root of the tree.
4. Reverse the collected list so that it starts from 1 and ends at n.
5. Output the resulting sequence.

Each step is safe because the parent relationship always leads strictly toward smaller indices, so we cannot cycle or loop indefinitely.

### Why it works

The parent pointers define a rooted tree structure. In a tree, every node has exactly one simple path to the root. Following parent links from any node must eventually reach the root because indices strictly decrease along edges (p[i] < i). This guarantees termination. Since there is only one path upward from n, the sequence we collect is exactly the unique path from n to 1, and reversing it produces the required path from 1 to n.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    p = [0] * (n + 1)

    vals = list(map(int, input().split()))
    for i in range(2, n + 1):
        p[i] = vals[i - 2]

    path = []
    cur = n

    while cur != 0:
        path.append(cur)
        cur = p[cur]

    path.reverse()
    print(*path)

if __name__ == "__main__":
    solve()
```

The solution first reconstructs the parent array in direct index form for constant-time access. It then starts from node n and follows parent pointers until reaching the root. The collected list is reversed at the end because the traversal naturally goes from child to parent, while the required output is from root to target.

A common mistake is forgetting to stop exactly at node 1 or incorrectly initializing the parent of node 1, which would cause an invalid lookup. Another issue is appending nodes in the wrong order and forgetting to reverse at the end.

## Worked Examples

### Example 1

Input:

```
8
1 1 2 2 3 2 5
```

We reconstruct parents:

| Node | Parent |
| --- | --- |
| 1 | 0 |
| 2 | 1 |
| 3 | 1 |
| 4 | 2 |
| 5 | 2 |
| 6 | 3 |
| 7 | 2 |
| 8 | 5 |

We trace backward from 8:

| Step | Current | Path so far |
| --- | --- | --- |
| 1 | 8 | [8] |
| 2 | 5 | [8, 5] |
| 3 | 2 | [8, 5, 2] |
| 4 | 1 | [8, 5, 2, 1] |

After reversing: [1, 2, 5, 8]

This confirms that the algorithm correctly follows parent pointers until the root and reconstructs the unique path.

### Example 2

Input:

```
5
1 2 3 4
```

Parents:

2→1, 3→2, 4→3, 5→4

Trace from 5:

| Step | Current | Path so far |
| --- | --- | --- |
| 1 | 5 | [5] |
| 2 | 4 | [5, 4] |
| 3 | 3 | [5, 4, 3] |
| 4 | 2 | [5, 4, 3, 2] |
| 5 | 1 | [5, 4, 3, 2, 1] |

Reversed result: [1, 2, 3, 4, 5]

This shows that even in a perfectly linear chain, the algorithm behaves consistently and produces the full path.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each node is visited at most once while following parent pointers |
| Space | O(n) | Parent array plus path storage |

The algorithm runs in linear time, which is optimal since we may need to output up to n nodes. Memory usage is also linear and fits comfortably within the constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()

    def solve():
        n = int(input())
        p = [0] * (n + 1)
        vals = list(map(int, input().split()))
        for i in range(2, n + 1):
            p[i] = vals[i - 2]

        path = []
        cur = n
        while cur != 0:
            path.append(cur)
            cur = p[cur]

        print(*path[::-1])

    with redirect_stdout(out):
        solve()

    return out.getvalue().strip()

# provided sample
assert run("8\n1 1 2 2 3 2 5\n") == "1 2 5 8"

# custom 1: minimum size
assert run("2\n1\n") == "1 2"

# custom 2: linear chain
assert run("5\n1 2 3 4\n") == "1 2 3 4 5"

# custom 3: star-shaped tree
assert run("6\n1 1 1 1 1\n") == "1 6"

# custom 4: mixed structure
assert run("7\n1 2 2 3 3 4\n") == "1 2 3 4 7"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 node case | 1 2 | minimal tree correctness |
| chain structure | 1 2 3 4 5 | deep path reconstruction |
| star tree | 1 6 | direct parent jumps |
| mixed structure | 1 2 3 4 7 | general correctness |

## Edge Cases

A key edge case is when the tree is a straight chain from 1 to n. In that situation, every node points to the previous one, so the algorithm must traverse the maximum possible depth. Starting from n, we repeatedly follow parents: n → n−1 → … → 1. The collected reversed path correctly outputs the entire sequence from 1 to n without any branching ambiguity.

Another edge case is a star-shaped tree where every node connects directly to 1. In that case, the parent of n is 1, so the path is just n → 1 reversed into 1 → n. The algorithm handles this without any special casing because it does not rely on structure, only parent pointers.

A third subtle case is when n is small, such as n = 2. Here the loop still executes correctly once, collects [2, 1], and reverses it into [1, 2], showing that the termination condition handles the root cleanly.
