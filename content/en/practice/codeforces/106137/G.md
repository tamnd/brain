---
title: "CF 106137G - White-Black Balanced Subtrees"
description: "We have a rooted tree whose root is vertex 1. Every vertex has one of two colors, black or white. For each vertex, we consider the subtree that starts at that vertex and contains all descendants of that vertex, including the vertex itself."
date: "2026-06-25T11:31:00+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106137
codeforces_index: "G"
codeforces_contest_name: "BFS  BFS - MTA"
rating: 0
weight: 106137
solve_time_s: 30
verified: true
draft: false
---

[CF 106137G - White-Black Balanced Subtrees](https://codeforces.com/problemset/problem/106137/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 30s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a rooted tree whose root is vertex `1`. Every vertex has one of two colors, black or white. For each vertex, we consider the subtree that starts at that vertex and contains all descendants of that vertex, including the vertex itself. A subtree is called balanced when the number of black vertices inside it is exactly the same as the number of white vertices inside it. The task is to count how many vertices have a balanced subtree.

The input describes the tree through parent pointers. For every vertex from `2` to `n`, we are given its parent, which is always a smaller numbered vertex. The color string gives the color of every vertex in order.

The constraints are the main reason the solution needs to be based on a single tree traversal. The total number of vertices over all test cases is at most `2 * 10^5`, so an `O(n)` or `O(n log n)` approach is comfortable. A solution that repeatedly explores every subtree would become too slow because a chain-shaped tree can make the sum of subtree sizes reach `O(n^2)`, which is around `4 * 10^10` operations for large inputs.

The key edge cases are caused by subtree sizes and color counts being local to each vertex.

Consider a tree with one vertex besides the root:

```
2
1
BW
```

The root subtree contains one black and one white vertex, so the answer is `1`. A careless solution that only checks leaves would miss the root.

Another case is:

```
3
1 1
BBB
```

Every subtree contains only black vertices, so the answer is `0`. A solution that only compares subtree sizes with color counts and forgets the color contribution would produce an incorrect result.

A final boundary case is a chain:

```
4
1 2 3
BWBW
```

The subtrees from bottom to top contain:

```
vertex 4: B
vertex 3: WB
vertex 2: BWB
vertex 1: BWBW
```

Only vertices `1` and `3` are balanced, so the answer is `2`. Implementations that process parents before children can use incomplete information and fail on this structure.

## Approaches

The direct approach is to start a DFS from every vertex. During the DFS of a chosen vertex, we count black and white vertices in its subtree and check whether the two counts are equal. This is correct because each vertex is independently checked against the exact definition of a balanced subtree.

The problem is the repeated work. In a chain of `n` vertices, the subtree of vertex `1` has `n` vertices, the subtree of vertex `2` has `n-1` vertices, and so on. The total number of visited vertices becomes:

```
n + (n - 1) + (n - 2) + ... + 1 = O(n^2)
```

For `n = 200000`, this is far beyond what can run within the time limit.

The tree structure gives us a better way. The subtree of a vertex is exactly the union of its children's subtrees plus the vertex itself. When we finish processing all children of a vertex, we already know everything needed to compute the color balance of that vertex.

Instead of storing two separate counts, we can store one value. Let black contribute `-1` and white contribute `+1`. The sum of a subtree is zero exactly when the number of black and white vertices is equal. A postorder DFS calculates this sum for every vertex and increments the answer whenever the sum becomes zero.

The brute-force method works because it repeatedly reconstructs each subtree's color count. The observation that every subtree is built from already processed child subtrees lets us reuse that information and reduce the problem to one traversal.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Build the adjacency list of children from the parent array. Each vertex only needs access to its direct children because the subtree information will be collected from the bottom upward.
2. Run a DFS starting from the root. The traversal must finish all children before processing the current vertex because the current subtree depends on the already computed values of its descendants.
3. For a vertex `u`, start its balance with `+1` if it is white and `-1` if it is black. Then add the balances returned by all child vertices.
4. After combining all children, check whether the balance of `u` is zero. If it is, the subtree of `u` contains equal numbers of black and white vertices, so increase the answer.
5. Return the computed balance of `u` to its parent. The parent will use this value as part of its own subtree calculation.

Why it works:

The invariant is that after DFS finishes a vertex `u`, the returned value is exactly the difference between white and black vertices inside the subtree of `u`. The base contribution of `u` represents its own color, and every child contributes the already correct difference of its subtree. Since the whole subtree is the vertex itself plus all child subtrees, the computed sum is correct. A subtree is balanced exactly when this difference is zero, so every balanced subtree is counted once and no unbalanced subtree is counted.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        children = [[] for _ in range(n)]

        parents = list(map(int, input().split()))
        for i, p in enumerate(parents, start=1):
            children[p - 1].append(i)

        s = input().strip()

        ans = 0
        balance = [0] * n

        stack = [(0, 0)]
        order = []

        while stack:
            u, state = stack.pop()
            if state == 0:
                stack.append((u, 1))
                for v in children[u]:
                    stack.append((v, 0))
            else:
                order.append(u)

        for u in order:
            cur = 1 if s[u] == 'W' else -1
            for v in children[u]:
                cur += balance[v]

            balance[u] = cur
            if cur == 0:
                ans += 1

        out.append(str(ans))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The input is converted into a child adjacency list. The vertices are numbered from zero internally, which avoids repeatedly subtracting one during traversal.

The iterative DFS creates a postorder sequence. A recursive DFS is also possible, but Python recursion depth is too small for a tree that is a long chain. The explicit stack simulates recursion while safely handling the maximum depth.

The `order` list contains vertices after all their descendants have been added. Processing this list from left to right gives the same effect as a postorder DFS. By the time a vertex is handled, every child already has its final balance.

The value stored in `balance[u]` is the color difference of the whole subtree. Using `+1` and `-1` avoids storing two counters and makes the balanced condition a simple zero comparison.

## Worked Examples

### Sample 1

Input:

```
7
1 1 2 3 3 5
WBBWWBW
```

The important state after processing each vertex is:

| Vertex | Own value | Child contribution | Final balance | Balanced |
| --- | --- | --- | --- | --- |
| 4 | +1 | 0 | +1 | No |
| 6 | -1 | 0 | -1 | No |
| 5 | +1 | -1 | 0 | Yes |
| 2 | -1 | +1 | 0 | Yes |
| 7 | +1 | 0 | +1 | No |
| 3 | +1 | +1 | +2 | No |
| 1 | +1 | +2 | +3 | No |

The traversal finds two zero balances, so the answer is `2`. The example shows why every vertex must be checked after its children are merged.

### Sample 2

Input:

```
2
1
BW
```

| Vertex | Own value | Child contribution | Final balance | Balanced |
| --- | --- | --- | --- | --- |
| 2 | -1 | 0 | -1 | No |
| 1 | +1 | -1 | 0 | Yes |

Only the root contains equal amounts of both colors, giving answer `1`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Every vertex is inserted into the traversal stack once and processed once. |
| Space | O(n) | The adjacency list, traversal stack, order list, and balance array each store linear information. |

The total number of vertices across all test cases is `2 * 10^5`, so the linear traversal fits easily within the required limits.

## Test Cases

```python
import sys
import io

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

assert run("""3
7
1 1 2 3 3 5
WBBWWBW
2
1
BW
8
1 2 3 4 5 6 7
BWBWBWBW
""") == "2\n1\n4", "provided samples"

assert run("""1
2
1
BW
""") == "1", "two opposite colors"

assert run("""1
3
1 1
BBB
""") == "0", "all black"

assert run("""1
4
1 2 3
BWBW
""") == "2", "chain structure"

assert run("""1
6
1 1 1 1 1
WWWWWW
""") == "0", "all white"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Two vertices with opposite colors | 1 | Checks the smallest balanced subtree. |
| All vertices black | 0 | Checks that equal subtree size is not enough without color balance. |
| A chain of vertices | 2 | Checks postorder processing and deep trees. |
| All vertices white | 0 | Checks the opposite color extreme. |

## Edge Cases

For the smallest balanced case:

```
2
1
BW
```

The DFS first processes vertex `2`. Its balance is `-1`, so it is not counted. The root receives that value and adds its own `+1`, producing `0`. The answer becomes `1`.

For a tree where every vertex has the same color:

```
3
1 1
BBB
```

Each leaf returns `-1`. The root combines both children and its own `-1`, resulting in `-3`. No vertex reaches balance zero, so the algorithm outputs `0`.

For a chain:

```
4
1 2 3
BWBW
```

The traversal finishes vertex `4` first, then `3`, then `2`, then `1`. Their balances are `-1`, `0`, `-1`, and `0` respectively. The answer is `2`, and the example confirms that the algorithm depends on child results being ready before parent processing.
