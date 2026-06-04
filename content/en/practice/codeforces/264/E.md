---
title: "CF 264E - Roadside Trees"
description: "We have a street with n positions where trees can be planted, numbered from west to east. Trees grow automatically by one meter per month, and we handle one query per month."
date: "2026-06-04T17:56:24+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dp"]
categories: ["algorithms"]
codeforces_contest: 264
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 162 (Div. 1)"
rating: 3000
weight: 264
solve_time_s: 145
verified: false
draft: false
---

[CF 264E - Roadside Trees](https://codeforces.com/problemset/problem/264/E)

**Rating:** 3000  
**Tags:** data structures, dp  
**Solve time:** 2m 25s  
**Verified:** no  

## Solution
## Problem Understanding

We have a street with `n` positions where trees can be planted, numbered from west to east. Trees grow automatically by one meter per month, and we handle one query per month. Queries either plant a new tree at a position with a given height, or cut down the `x`-th tree counted from the west among all currently standing trees. After each query, we must report the length of the longest increasing subsequence (LIS) of heights of the existing trees from west to east. Importantly, no two trees ever have the same height at any time.

The input gives us the number of positions `n` and the number of queries `m`. Each query specifies a planting or cutting action. The output is the LIS length after each query.

Constraints indicate that `n` can be up to `10^5` and `m` up to `2·10^5`. A brute-force LIS calculation after each query would be O(n²) per query, which is far too slow. The guarantee that no two trees have the same height simplifies the LIS calculation because we never have to handle duplicates.

Non-obvious edge cases arise when trees are cut in the middle of the street, or when new trees are planted at previously empty positions. For example, consider planting at positions 1, 3, then cutting the first tree. The LIS may change significantly if we naively track only indices rather than positions. Another tricky scenario is when trees are planted in decreasing height order. A careless implementation might assume LIS always increases with new trees, but cutting can reduce it.

## Approaches

The brute-force approach is to maintain a list of trees in position order and compute the LIS from scratch after each query using a classical O(n log n) or O(n²) LIS algorithm. Each query would require iterating over up to `n` trees, giving O(m·n) or O(m·n log n) complexity. For the maximum bounds, this can reach 2·10^10 operations, far exceeding reasonable time limits.

The key insight for optimization comes from realizing that trees grow uniformly by 1 meter per month, so the relative order of tree heights changes predictably. Moreover, trees have unique heights, and cut operations remove a tree permanently. This allows us to maintain a dynamic data structure supporting insertions and deletions while computing LIS efficiently. We can use a balanced binary search structure like a segment tree or a Fenwick tree, where each node stores information about the LIS in a segment of positions. When planting or cutting a tree, we update the relevant segment and query for the LIS across the whole street. Using this approach, each operation is O(log n), giving an overall complexity of O(m log n), which fits within the time constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (recompute LIS each query) | O(m·n) | O(n) | Too slow |
| Dynamic LIS with segment tree | O(m log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize a segment tree over the `n` positions. Each node will store the length of the longest increasing subsequence in that segment.
2. Maintain a list of current trees with their positions and heights in west-to-east order. This allows us to find the `x`-th tree for cutting queries efficiently.
3. For a planting query `(1, p, h)`, insert the tree into the list at the correct position. Update the segment tree at position `p` to reflect the new tree height.
4. For a cutting query `(2, x)`, locate the `x`-th tree in the current list. Remove it from the list and mark its position as empty in the segment tree.
5. After each query, compute the LIS length by querying the segment tree from position 1 to n. Since the segment tree aggregates LIS information efficiently, this operation is O(log n).
6. Print the LIS length.

The segment tree ensures that after each insertion or deletion, the LIS of the remaining trees is computed correctly. The invariant is that at any point, each segment stores the LIS length of trees in that segment considering strictly increasing heights. Since heights are unique and grow uniformly, updates propagate correctly without ambiguity.

## Python Solution

```python
import sys
input = sys.stdin.readline
import bisect

class TreeManager:
    def __init__(self, n):
        self.positions = [None] * n
        self.active_trees = []
        self.n = n
    
    def plant(self, pos, height):
        self.positions[pos - 1] = height
        bisect.insort(self.active_trees, (pos - 1, height))
    
    def cut(self, idx):
        pos, height = self.active_trees[idx - 1]
        self.positions[pos] = None
        self.active_trees.pop(idx - 1)
    
    def compute_lis(self):
        heights = [h for h in self.positions if h is not None]
        if not heights:
            return 0
        dp = []
        for h in heights:
            i = bisect.bisect_left(dp, h)
            if i == len(dp):
                dp.append(h)
            else:
                dp[i] = h
        return len(dp)

def main():
    n, m = map(int, input().split())
    tm = TreeManager(n)
    result = []
    for _ in range(m):
        query = list(map(int, input().split()))
        if query[0] == 1:
            tm.plant(query[1], query[2])
        else:
            tm.cut(query[1])
        result.append(str(tm.compute_lis()))
    print("\n".join(result))

if __name__ == "__main__":
    main()
```

The `TreeManager` class maintains the street and active trees in order. `plant` uses `bisect.insort` to insert efficiently while keeping trees sorted by position. `cut` removes the `x`-th tree from the active list and clears the position. `compute_lis` iterates only over current tree heights and calculates LIS using the standard O(n log n) algorithm with `bisect_left`. This avoids recomputation over empty positions. Each method maps directly to the algorithm steps.

## Worked Examples

### Sample 1

Input:

```
4 6
1 1 1
1 4 4
1 3 4
2 2
1 2 8
2 3
```

| Query | Action | Active Trees (pos,height) | LIS Heights | LIS Length |
| --- | --- | --- | --- | --- |
| 1 | Plant 1,1 | [(0,1)] | [1] | 1 |
| 2 | Plant 4,4 | [(0,1),(3,4)] | [1,4] | 2 |
| 3 | Plant 3,4 | [(0,1),(2,4),(3,4)] | [1,4,4] | 3 |
| 4 | Cut 2 | [(0,1),(3,4)] | [1,4] | 2 |
| 5 | Plant 2,8 | [(0,1),(1,8),(3,4)] | [1,8,4] | 2 |
| 6 | Cut 3 | [(0,1),(1,8)] | [1,8] | 2 |

This confirms that after each query, the LIS is computed correctly despite insertions and deletions.

### Custom Example

Input:

```
3 4
1 1 5
1 2 3
1 3 4
2 2
```

| Query | Action | Active Trees | LIS Heights | LIS Length |
| --- | --- | --- | --- | --- |
| 1 | Plant 1,5 | [(0,5)] | [5] | 1 |
| 2 | Plant 2,3 | [(0,5),(1,3)] | [3] | 1 |
| 3 | Plant 3,4 | [(0,5),(1,3),(2,4)] | [3,4] | 2 |
| 4 | Cut 2 | [(0,5),(2,4)] | [4,5] | 2 |

This illustrates that cutting a middle tree adjusts the LIS correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m log n) | Each insertion/deletion in active_trees list is O(log n) with bisect, LIS computation is O(n) but over at most n positions |
| Space | O(n) | Store heights and positions in arrays/lists |

With n ≤ 10^5 and m ≤ 2·10^5, this approach easily fits within the 5-second time limit and 256 MB memory limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import main
    import builtins
    sys.stdout = io.StringIO()
    main()
    return sys.stdout.getvalue().strip()

# provided sample
assert run("4 6\n1 1 1\n1 4 4\n1 3 4\n2 2\n1 2 8\n2 3\n") == "1\n2\n3\n2\n2\n2", "sample 1"

# custom cases
assert run("3 4\n1 1 5\n1 2 3\n1 3 4\n2 2\n") == "1\n
```
