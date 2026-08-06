---
title: "CF 102536I - Glory to Algotzka"
description: "The company hierarchy is a rooted tree. Employee i is the root of the investigated region, and a valid report is any connected set of employees that contains i."
date: "2026-08-06T20:29:57+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102536
codeforces_index: "I"
codeforces_contest_name: "2020 UP ACM Algolympics Final Round"
rating: 0
weight: 102536
solve_time_s: 88
verified: true
draft: false
---

[CF 102536I - Glory to Algotzka](https://codeforces.com/problemset/problem/102536/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 28s  
**Verified:** yes  

## Solution
## Problem Understanding

The company hierarchy is a rooted tree. Employee `i` is the root of the investigated region, and a valid report is any connected set of employees that contains `i`. Because the structure is a tree, this means that whenever we include a descendant, every employee on the path back to `i` must also be included.

Each employee has one of two types. A query asks whether some valid connected set inside the subtree of `i` contains exactly `c` employees of type `C` and exactly `s` employees of type `S`.

The input order has a useful property: every parent appears before its children. This allows dynamic programming to be performed in reverse index order. The limits are asymmetric: there are only `10000` employees, but up to `200000` queries. A solution that explores the tree for every query would need around `2 * 10^9` node visits in the worst case, which is far beyond the time limit. The preprocessing phase must do almost all the work, leaving each query close to constant time.

A common mistake is to store only the possible subtree sizes. That loses information because two connected sets with the same size can contain different numbers of `C` employees.

For example, consider:

```
2 1
0 1
CS
1 1 1
```

The answer is `COMPROMISED` because choosing both employees gives one `C` and one `S`. A solution that only stores possible sizes would know that size `2` is possible, but it would not know the distribution.

Another edge case is a query that asks for a count larger than the subtree size.

```
1 2
0
C
1 0 1
1 2 0
```

The first query is `COMPROMISED`, because the single node is a socialist count of zero and capitalist count of one. The second query is `NOT COMPROMISED`, because there are not enough employees. Any implementation that forgets to check array bounds can incorrectly access invalid states.

## Approaches

The direct solution is to enumerate every connected rooted subtree for each query. This is correct because every possible answer is checked, but the number of connected subtrees can be exponential. Even a path of length `10000` already has a quadratic number of rooted connected choices, and doing this for `200000` queries is impossible.

The first improvement is to preprocess every node. For a node `v`, instead of storing every possible connected subtree, store information for every possible size `t`. Among all connected sets of size `t` rooted at `v`, we only need the minimum and maximum possible number of `C` employees. The key observation is that every value between those two extremes is also possible.

If the minimum number of `C` employees is `a` and the maximum is `b`, transforming the minimum construction into the maximum construction by replacing one chosen node at a time changes the count by at most one each time. The sequence must pass through every value from `a` to `b`.

The dynamic programming state is therefore:

`minC[v][t]` = minimum number of `C` employees in a valid connected set of `t` nodes rooted at `v`.

`maxC[v][t]` is defined similarly.

When combining children, we merge their possible contributions like a tree knapsack. The total merging work is quadratic rather than cubic because a pair of nodes is only combined when their lowest common ancestor is processed.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential per query | O(n) | Too slow |
| Optimal DP | O(n²) preprocessing, O(1) queries | O(n²) | Accepted |

## Algorithm Walkthrough

1. Process nodes from `n` down to `1`. Because parents always have smaller indices than children, every child has already been processed.
2. Initialize the dynamic programming state of a node with the node itself. If the node is `C`, a connected set of size one has one capitalist. If it is `S`, the value is zero.
3. Merge every child into the current node. For every possible number of nodes already taken and every possible number taken from the child subtree, update the minimum and maximum capitalist counts.
4. Store the resulting arrays for every node. A query `(i, c, s)` asks about a connected set of size `c+s`. If `c` lies between `minC[i][c+s]` and `maxC[i][c+s]`, the answer is `COMPROMISED`.

Why it works: the DP stores the extreme possible number of capitalists for every possible size. The interval property proves that no value between these extremes is missing. The query condition checks exactly whether the requested number of capitalists belongs to that interval, while the total size fixes the number of socialists automatically.

## Python Solution

```python
import sys
from array import array

input = sys.stdin.readline

def solve():
    n, q = map(int, input().split())
    parent = list(map(int, input().split()))
    s = input().strip()

    children = [[] for _ in range(n)]
    for i in range(1, n):
        children[parent[i] - 1].append(i)

    INF = 30000
    mins = [None] * n
    maxs = [None] * n

    for v in range(n - 1, -1, -1):
        val = 1 if s[v] == 'C' else 0

        if len(children[v]) == 0:
            mins[v] = array('h', [INF, val])
            maxs[v] = array('h', [-INF, val])
            continue

        if len(children[v]) == 1:
            ch = children[v][0]
            cm = mins[ch]
            cx = maxs[ch]
            mn = array('h', [INF] * (len(cm) + 1))
            mx = array('h', [-INF] * (len(cx) + 1))
            mn[1] = val
            mx[1] = val
            for t in range(1, len(cm)):
                mn[t + 1] = cm[t] + val
                mx[t + 1] = cx[t] + val
            mins[v] = mn
            maxs[v] = mx
            continue

        cur_min = array('h', [INF, val])
        cur_max = array('h', [-INF, val])

        for ch in children[v]:
            cm = mins[ch]
            cx = maxs[ch]
            a = len(cur_min) - 1
            b = len(cm) - 1
            nm = array('h', [INF] * (a + b + 1))
            nx = array('h', [-INF] * (a + b + 1))

            for i in range(1, a + 1):
                if cur_min[i] < nm[i]:
                    nm[i] = cur_min[i]
                if cur_max[i] > nx[i]:
                    nx[i] = cur_max[i]

            for i in range(1, a + 1):
                if cur_min[i] == INF:
                    continue
                for j in range(1, b + 1):
                    if cm[j] != INF:
                        x = cur_min[i] + cm[j]
                        if x < nm[i + j]:
                            nm[i + j] = x
                    if cx[j] != -INF:
                        x = cur_max[i] + cx[j]
                        if x > nx[i + j]:
                            nx[i + j] = x

            cur_min, cur_max = nm, nx

        for i in range(1, len(cur_min)):
            cur_min[i] += val
            cur_max[i] += val

        mins[v] = cur_min
        maxs[v] = cur_max

    out = []
    for _ in range(q):
        i, c, st = map(int, input().split())
        i -= 1
        size = c + st
        if size < len(mins[i]) and mins[i][size] <= c <= maxs[i][size]:
            out.append("COMPROMISED")
        else:
            out.append("NOT COMPROMISED")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The reverse iteration avoids recursion depth issues because the input ordering already gives a valid bottom-up order. Each stored array has one entry per possible connected-set size. The `array('h')` container keeps memory usage low because every stored value is at most `10000`.

The single-child optimization is necessary. Without it, a path-shaped tree would repeatedly merge a large child state and degrade into cubic work. With the optimization, the expensive knapsack merges only happen at branching nodes, where the total amount of pairwise interaction over the whole tree remains quadratic.

The query uses `size = c + s` because every chosen employee is either `C` or `S`. Once the size and capitalist count are fixed, the socialist count is determined.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n² + q) | Tree knapsack preprocessing plus constant time queries |
| Space | O(n²) | All DP intervals are stored for every node |

The largest possible sum of subtree sizes is about `n²/2`, which is around fifty million states for a chain. The compact integer arrays keep this within the generous memory limit.

## Worked Examples

For the sample:

```
5 3
0 1 2 3 4
CSCSC
1 3 2
1 2 2
2 2 1
```

The tree is a chain:

```
1(C)
 |
2(S)
 |
3(C)
 |
4(S)
 |
5(C)
```

The root states include:

| Node | Size | Minimum C | Maximum C |
| --- | --- | --- | --- |
| 1 | 1 | 1 | 1 |
| 1 | 2 | 1 | 1 |
| 1 | 3 | 2 | 2 |
| 1 | 4 | 2 | 2 |
| 1 | 5 | 3 | 3 |

The first query asks for size `5` and `3` capitalists, which is inside the interval, so it is accepted.

The third query asks about node `2` with `3` total employees and `2` capitalists. The possible chain from node `2` has employees `2,3,4,5`, and among size three choices the capitalist count cannot reach two, so it is rejected.

## Test Cases

```
# The solution above can be tested with the following inputs.

sample = """5 3
0 1 2 3 4
CSCSC
1 3 2
1 2 2
2 2 1
"""

case1 = """1 2
0
C
1 1 0
1 0 1
"""

case2 = """3 3
0 1 1
SSS
1 0 3
2 0 2
2 1 1
"""

case3 = """4 3
0 1 1 2
CCCC
1 4 0
1 2 2
2 1 1
"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single node | `COMPROMISED`, `NOT COMPROMISED` | Smallest tree and invalid counts |
| All `S` nodes | Valid socialist-only ranges | All equal values |
| All `C` nodes | Capitalist boundaries | Correct size handling |

## Edge Cases

A single employee tree is handled by initializing only the size one state. No child merge happens, so the answer depends only on the employee's own type.

For a long chain, the single-child transition copies the child's states with a size shift. This avoids the expensive nested merge and keeps the runtime quadratic.

For branching trees, the merge step keeps both extremes. A query requesting a middle value is accepted because the interval property covers every possible capitalist count between the two extremes.
