---
title: "CF 102889H - \u5b9d\u53ef\u68a6\u4e0e\u5206\u652f\u8fdb\u5316"
description: "There are n Pokémon species. Species 1 is the root of the evolution family, and every other species has exactly one parent species that it evolved from. This creates a rooted tree where moving from a parent to a child represents one evolution step."
date: "2026-07-25T12:27:38+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102889
codeforces_index: "H"
codeforces_contest_name: "The 15-th Beihang University Collegiate Programming Contest (BCPC 2020) - Final"
rating: 0
weight: 102889
solve_time_s: 44
verified: true
draft: false
---

[CF 102889H - \u5b9d\u53ef\u68a6\u4e0e\u5206\u652f\u8fdb\u5316](https://codeforces.com/problemset/problem/102889/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 44s  
**Verified:** yes  

## Solution
## Problem Understanding

There are `n` Pokémon species. Species `1` is the root of the evolution family, and every other species has exactly one parent species that it evolved from. This creates a rooted tree where moving from a parent to a child represents one evolution step.

The yard contains `m` Pokémon arranged in a fixed left-to-right order. We want to pick as many of them as possible while keeping their original order. If one selected Pokémon appears before another, the second one must be a descendant of the first one in the evolution tree. The goal is to find the maximum length of such a subsequence.

The sequence order and the tree structure interact. A chosen Pokémon does not need to be an immediate child of the previous one. Any number of evolution steps is allowed, so the next chosen species only needs to lie somewhere inside the subtree of the previous species.

The constraints make a quadratic dynamic programming solution impossible. Both the number of species and the number of Pokémon in the yard can reach `5 * 10^5`, so an algorithm doing `O(nm)` or even `O(m sqrt(n))` operations will not fit in a one second time limit. We need close to linear or `O((n+m) log n)` work.

A common mistake is treating this as a normal longest increasing subsequence problem. The tree relationship is not based on numeric labels, so comparing species numbers gives meaningless results. Another subtle case is that the next selected Pokémon must be a proper descendant, not the same species. For example:

```
2 2
1
1 1
```

The correct answer is `1`. Selecting both Pokémon would require the second species `1` to evolve from the first species `1`, but no evolution happened.

Another edge case is the root species. It has no ancestors, so the first occurrence of the root cannot extend any previous chain. For example:

```
3 3
1 1
2 1 3
```

The correct answer is `2`, using species `1` followed by species `3`. A solution that accidentally treats the root as having a parent may create invalid transitions.

Repeated species also require care. For example:

```
3 4
1 2
2 2 3 3
```

The correct answer is `2`. The two copies of species `2` cannot be chained together, because a species does not evolve into itself. The best chain is species `2` followed by species `3`.

## Approaches

The direct dynamic programming idea is to process the yard from left to right. For every Pokémon at position `i`, define `dp[i]` as the longest valid subsequence ending at this Pokémon. We can compute it by looking at every earlier position `j` and checking whether `a[j]` is an ancestor of `a[i]`. If it is, we can extend that chain.

This approach is correct because every possible previous choice is considered. However, it is far too slow. In the worst case, there are `5 * 10^5` Pokémon, and checking all previous positions requires about `2.5 * 10^11` comparisons, which is impossible.

The key observation is that the only information we need from previous Pokémon is the best chain length among ancestors of the current species. When we finish processing a Pokémon of species `x`, we add its chain length as a candidate answer for future descendants of `x`. Future queries ask for the maximum value stored on the path from the root to a node.

This turns the problem into two tree operations. We need to query the maximum value on a root-to-node path, excluding the node itself, and we need to update one node with a larger value. Heavy-light decomposition breaks any tree path into a small number of contiguous segments. A segment tree over the heavy-light order can then answer and update these segments efficiently.

The brute-force solution works because it explicitly checks all possible predecessors, but fails because there are too many. The tree path maximum observation compresses all relevant predecessors into a small number of ranges.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(m²) | O(m) | Too slow |
| Optimal | O((n + m) log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Build the evolution tree from the parent information. Store every child so that the tree can later be traversed for heavy-light decomposition.
2. Compute the size of every subtree and identify the heavy child of every node. The heavy child is the child with the largest subtree. Following heavy children keeps important paths together, which reduces every root-to-node path into only a logarithmic number of pieces.
3. Assign every node a position in the heavy-light order. Each heavy chain becomes a continuous segment in this order, so a path query can be translated into segment tree range queries.
4. Process the Pokémon in the yard from left to right. For the current species `x`, query the maximum stored value on the path from the root to `parent[x]`. This gives the best previous chain that can evolve into `x`.
5. Set the current chain length to one plus that query result. Then update the position of `x` in the segment tree with this value. Future Pokémon that are descendants of `x` can now use this chain.
6. Track the maximum value produced during the scan and output it after all Pokémon have been processed.

Why the query stops at `parent[x]` is essential. The current species cannot be used as its own predecessor, because the transition requires at least one evolution step.

The correctness follows from the invariant that after processing the first `i` Pokémon, every tree node stores the best subsequence length among processed Pokémon of exactly that species. Therefore, querying the ancestors of the current species returns exactly the best possible previous Pokémon that can precede it. The update preserves this invariant, and every possible ending position is considered, so the maximum stored value is the answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())

    children = [[] for _ in range(n + 1)]
    parent = [0] * (n + 1)
    parent[1] = 0

    if n > 1:
        arr = list(map(int, input().split()))
        for i, p in enumerate(arr, 2):
            parent[i] = p
            children[p].append(i)

    a = list(map(int, input().split()))

    depth = [0] * (n + 1)
    order = [1]
    for x in order:
        for y in children[x]:
            depth[y] = depth[x] + 1
            order.append(y)

    size = [1] * (n + 1)
    heavy = [0] * (n + 1)
    for x in reversed(order):
        best_size = 0
        for y in children[x]:
            size[x] += size[y]
            if size[y] > best_size:
                best_size = size[y]
                heavy[x] = y

    head = [0] * (n + 1)
    pos = [0] * (n + 1)
    rev = [0] * (n + 1)
    cur = 0

    stack = [(1, 1)]
    while stack:
        x, h = stack.pop()
        while x:
            head[x] = h
            cur += 1
            pos[x] = cur
            rev[cur] = x

            for y in children[x]:
                if y != heavy[x]:
                    stack.append((y, y))

            x = heavy[x]

    size_seg = 1
    while size_seg < n:
        size_seg *= 2
    seg = [0] * (size_seg * 2)

    def update(i, val):
        i += size_seg - 1
        if seg[i] >= val:
            return
        seg[i] = val
        i //= 2
        while i:
            nv = seg[i * 2] if seg[i * 2] >= seg[i * 2 + 1] else seg[i * 2 + 1]
            if seg[i] == nv:
                break
            seg[i] = nv
            i //= 2

    def query(l, r):
        if l > r:
            return 0
        l += size_seg - 1
        r += size_seg - 1
        ans = 0
        while l <= r:
            if l & 1:
                if seg[l] > ans:
                    ans = seg[l]
                l += 1
            if not (r & 1):
                if seg[r] > ans:
                    ans = seg[r]
                r -= 1
            l //= 2
            r //= 2
        return ans

    def path_query(x):
        ans = 0
        while head[x] != head[1]:
            val = query(pos[head[x]], pos[x])
            if val > ans:
                ans = val
            x = parent[head[x]]
        val = query(pos[1], pos[x])
        if val > ans:
            ans = val
        return ans

    answer = 0
    for x in a:
        best = 0
        if x != 1:
            best = path_query(parent[x])
        dp = best + 1
        if dp > answer:
            answer = dp
        update(pos[x], dp)

    print(answer)

if __name__ == "__main__":
    solve()
```

The first part of the code builds the tree and computes the heavy-light decomposition. The traversal order is stored iteratively because the tree can contain `5 * 10^5` nodes, and recursive DFS may exceed Python's recursion limit.

The `size` and `heavy` arrays determine which child belongs to the same heavy chain. The decomposition assigns each node a position so that every heavy chain becomes a continuous interval.

The segment tree stores the best subsequence length ending at each species. The update operation uses `max` because a later Pokémon of the same species can only improve the value available to descendants.

The `path_query` function answers ancestor queries. Before querying, the main loop moves to `parent[x]`, which removes the current species from consideration. This prevents invalid transitions between equal species.

All values are at most `m`, so Python integers easily handle them. The iterative segment tree operations avoid recursion depth issues and keep the implementation within the required limits.

## Worked Examples

For the first sample:

```
n = 4, m = 5
parents: 1 1 2
sequence: 1 2 2 3 4
```

The evolution tree has `1` as the parent of `2` and `3`, and `2` as the parent of `4`.

| Position | Species | Best ancestor value | Current dp | Answer |
| --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 1 | 1 |
| 2 | 2 | 1 | 2 | 2 |
| 3 | 2 | 1 | 2 | 2 |
| 4 | 3 | 1 | 2 | 2 |
| 5 | 4 | 2 | 3 | 3 |

The two occurrences of species `2` cannot extend each other. The best chain is `1 -> 2 -> 4`, giving length `3`.

For the second sample:

```
n = 6, m = 6
parents: 1 2 3 4 5
sequence: 1 2 3 4 5 6
```

The tree is a single chain.

| Position | Species | Best ancestor value | Current dp | Answer |
| --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 1 | 1 |
| 2 | 2 | 1 | 2 | 2 |
| 3 | 3 | 2 | 3 | 3 |
| 4 | 4 | 3 | 4 | 4 |
| 5 | 5 | 4 | 5 | 5 |
| 6 | 6 | 5 | 6 | 6 |

Every Pokémon can follow the previous one because each species is a descendant of the preceding species.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + m) log n) | Heavy-light decomposition is linear, and each query or update touches logarithmically many segment tree nodes. |
| Space | O(n) | The tree arrays, decomposition arrays, and segment tree all use linear memory. |

The largest possible input contains half a million species and half a million Pokémon. The solution performs only logarithmic work per Pokémon after a linear preprocessing stage, which fits the constraints.

## Test Cases

```python
import sys
import io

def solve_data(inp):
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n, m = map(int, input().split())

    children = [[] for _ in range(n + 1)]
    parent = [0] * (n + 1)
    if n > 1:
        for i, p in enumerate(map(int, input().split()), 2):
            parent[i] = p
            children[p].append(i)

    a = list(map(int, input().split()))

    depth = [0] * (n + 1)
    order = [1]
    for x in order:
        for y in children[x]:
            depth[y] = depth[x] + 1
            order.append(y)

    size = [1] * (n + 1)
    heavy = [0] * (n + 1)
    for x in reversed(order):
        best = 0
        for y in children[x]:
            size[x] += size[y]
            if size[y] > best:
                best = size[y]
                heavy[x] = y

    head = [0] * (n + 1)
    pos = [0] * (n + 1)
    cur = 0
    stack = [(1, 1)]
    while stack:
        x, h = stack.pop()
        while x:
            cur += 1
            head[x] = h
            pos[x] = cur
            for y in children[x]:
                if y != heavy[x]:
                    stack.append((y, y))
            x = heavy[x]

    s = 1
    while s < n:
        s *= 2
    seg = [0] * (2 * s)

    def update(i, v):
        i += s - 1
        seg[i] = max(seg[i], v)
        i //= 2
        while i:
            seg[i] = max(seg[2 * i], seg[2 * i + 1])
            i //= 2

    def query(l, r):
        if l > r:
            return 0
        l += s - 1
        r += s - 1
        res = 0
        while l <= r:
            if l & 1:
                res = max(res, seg[l])
                l += 1
            if not r & 1:
                res = max(res, seg[r])
                r -= 1
            l //= 2
            r //= 2
        return res

    def get(x):
        res = 0
        while head[x] != head[1]:
            res = max(res, query(pos[head[x]], pos[x]))
            x = parent[head[x]]
        return max(res, query(pos[1], pos[x]))

    ans = 0
    for x in a:
        dp = 1
        if x != 1:
            dp = get(parent[x]) + 1
        ans = max(ans, dp)
        update(pos[x], dp)
    return str(ans) + "\n"

assert solve_data("""4 5
1 1 2
1 2 2 3 4
""") == "3\n", "sample 1"

assert solve_data("""6 6
1 2 3 4 5
1 2 3 4 5 6
""") == "6\n", "sample 2"

assert solve_data("""2 2
1
1 1
""") == "1\n", "same species cannot chain"

assert solve_data("""3 3
1 1
2 1 3
""") == "2\n", "root handling"

assert solve_data("""3 4
1 2
2 2 3 3
""") == "2\n", "duplicate species handling"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| First sample | 3 | Basic branching tree behavior |
| Second sample | 6 | Long single-chain evolution |
| Two root species | 1 | Equal species cannot be consecutive in a chain |
| Root mixed with descendants | 2 | Root has no previous ancestor |
| Repeated intermediate species | 2 | Prevents self-transition mistakes |

## Edge Cases

The first edge case with repeated root species:

```
2 2
1
1 1
```

When processing the first species `1`, the tree has no ancestor query result, so the value stored is `1`. When processing the second species `1`, the algorithm still queries only proper ancestors. Since there are none, it creates another chain of length `1` instead of incorrectly extending the previous root. The answer remains `1`.

The second edge case with the root as the starting point:

```
3 3
1 1
2 1 3
```

The first species `2` queries its parent `1` and receives zero, producing a chain of length `1`. The next species `1` also has no ancestor and produces length `1`. The final species `3` queries its parent `1`, where the previous root occurrence is stored, so it produces length `2`. The algorithm correctly finds the chain `1 -> 3`.

The third edge case with repeated intermediate species:

```
3 4
1 2
2 2 3 3
```

The first species `2` stores length `1`. The second species `2` cannot read that value because the query stops at its parent, which is species `1`, so it also gets length `1`. When species `3` appears, it can use the stored value from species `2`, producing length `2`. The result matches the required evolution rule.
