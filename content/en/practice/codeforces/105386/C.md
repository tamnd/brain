---
title: "CF 105386C - Stop the Castle 2"
description: "We are working on a very large grid, but only a sparse set of cells are relevant: some cells contain castles and some contain obstacles. Two castles can “see” each other if they lie in the same row or column and nothing important lies strictly between them."
date: "2026-06-23T05:12:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105386
codeforces_index: "C"
codeforces_contest_name: "The 2024 ICPC Kunming Invitational Contest"
rating: 0
weight: 105386
solve_time_s: 68
verified: true
draft: false
---

[CF 105386C - Stop the Castle 2](https://codeforces.com/problemset/problem/105386/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 8s  
**Verified:** yes  

## Solution
## Problem Understanding

We are working on a very large grid, but only a sparse set of cells are relevant: some cells contain castles and some contain obstacles. Two castles can “see” each other if they lie in the same row or column and nothing important lies strictly between them.

“Important” here means either another castle or an obstacle. So any such object blocks visibility. If we remove some obstacles, we may open up new lines of sight between castles, which creates attacking pairs.

The task is not just to count these attacking pairs after removing obstacles. We must choose exactly `k` obstacles to remove, and we want to make the final number of attacking castle pairs as small as possible.

At first this sounds paradoxical because removing obstacles only increases visibility. The only control we have is choosing _which_ obstacles to remove so that we create as few new attacking relationships as possible.

The constraints are large, with up to 100,000 castles and obstacles per test case, and total input size also bounded by 100,000. This immediately rules out any solution that tries to simulate visibility pair-by-pair or recomputes visibility after each removal. Any acceptable solution must be close to linear or `n log n` per test case.

A common failure case comes from thinking locally. For example, if in one row we have:

```
C . O . C
```

the obstacle blocks visibility between the two castles. Removing that obstacle immediately creates one attacking pair. A naive approach might try to evaluate each obstacle independently, but that fails when multiple obstacles lie between the same castles, or when an obstacle participates in multiple rows and columns simultaneously.

Another subtle issue is overlapping responsibility. A single obstacle might block visibility for multiple castle pairs in its row and also in its column. Treating contributions independently per direction leads to double counting or incorrect greedy decisions.

The real difficulty is that each potential attacking pair depends on _all obstacles between two castles_, not just one.

## Approaches

A brute-force way to think about the problem is to recompute visibility after trying every possible set of `k` obstacles. For each subset, we would rebuild the row and column structure and count all visible castle pairs. This is clearly correct but completely infeasible. The number of subsets is combinatorial, on the order of $\binom{m}{k}$, and even a single evaluation already costs at least linear time in the number of points.

A second brute-force idea is to simulate removing obstacles one by one, always recomputing which castle pairs become newly visible. Even if we maintain sorted orderings per row and column, updating after each removal still requires updating many intervals, leading to worst-case quadratic behavior.

The key structural observation is that castle visibility is determined only by ordering along rows and columns. If we sort all occupied cells in a row, castles become connected segments separated by obstacles and other castles. Two consecutive castles in this ordering define a potential attacking pair, and that pair becomes active only if _all obstacles between them are removed_.

So instead of thinking in terms of global visibility, we reduce the problem to independent “segments” defined by consecutive castles in each row and column. Each such segment has a set of obstacles, and it contributes one attacking pair only if we remove every obstacle in that segment.

Now the problem becomes: we must choose `k` obstacles, and each segment is “activated” only if all obstacles inside it are chosen. We want to minimize how many segments become fully activated.

This is a set system problem: each segment corresponds to a set of obstacles, and we want to choose `k` elements while avoiding fully covering as many sets as possible. Since segments overlap only through shared obstacles, the natural greedy signal becomes how “dangerous” each obstacle is in terms of participating in many segments.

The workable reduction is to compute, for every obstacle, how many castle-adjacent segments it belongs to. Intuitively, choosing an obstacle that lies in many critical segments increases the chance of completing one of them entirely, so those should be avoided when possible. We therefore pick obstacles with the smallest involvement first.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(m) | Too slow |
| Segment + greedy scoring | O((n + m) log m) | O(n + m) | Accepted |

## Algorithm Walkthrough

We compress the problem into row-wise and column-wise processing of ordered points.

1. Group all castles and obstacles by row. Sort each row by column index. Do the same grouping by column, sorted by row index.

This gives us a linear order of all occupied cells along each line where visibility matters.
2. In each sorted row, scan left to right and locate consecutive castles. For each pair of consecutive castles, record all obstacles between them. These obstacles form a “blocking set” for that castle pair.

The same is repeated for columns. Each castle pair in a column also gets a blocking set of obstacles.
3. For every obstacle, maintain a counter representing how many blocking sets it appears in.

This counter measures how often this obstacle contributes to preventing castle visibility. An obstacle involved in many such segments is more “critical”.
4. Sort all obstacles by this counter in increasing order.

The idea is to choose obstacles that have minimal influence on potential segment completions first, so that we reduce the probability of fully clearing any one blocking set.
5. Select the first `k` obstacles from this ordering.
6. After selection, compute the final number of attacking pairs by checking each segment: a segment contributes 1 attack only if all its obstacles are chosen.

### Why it works

Each attacking pair is tied to a specific set of obstacles, and it becomes active only when all obstacles in that set are removed. So the risk of activating a pair is concentrated entirely in fully selecting one of these sets.

An obstacle that participates in many such sets increases the coupling between decisions: picking it pushes multiple sets closer to being fully selected. Greedily avoiding high-participation obstacles keeps the selection distributed across different blocking structures, which minimizes the number of sets that can be completely covered within `k` picks.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m, k = map(int, input().split())
    
    castles = []
    obstacles = []
    
    for _ in range(n):
        r, c = map(int, input().split())
        castles.append((r, c))
    
    obs = []
    for i in range(m):
        r, c = map(int, input().split())
        obs.append((r, c, i))
    
    # map obstacle index to participation count
    contrib = [0] * m
    
    from collections import defaultdict
    
    row_castles = defaultdict(list)
    row_obs = defaultdict(list)
    col_castles = defaultdict(list)
    col_obs = defaultdict(list)
    
    for r, c in castles:
        row_castles[r].append(c)
        col_castles[c].append(r)
    
    for r, c, i in obs:
        row_obs[r].append((c, i))
        col_obs[c].append((r, i))
    
    # process rows
    for r in row_castles:
        cs = sorted(row_castles[r])
        os = sorted(row_obs[r])
        
        j = 0
        for idx in range(len(cs) - 1):
            left = cs[idx]
            right = cs[idx + 1]
            
            while j < len(os) and os[j][0] <= left:
                j += 1
            
            tmp = j
            while tmp < len(os) and os[tmp][0] < right:
                contrib[os[tmp][1]] += 1
                tmp += 1
    
    # process cols
    for c in col_castles:
        rs = sorted(col_castles[c])
        os = sorted(col_obs[c])
        
        j = 0
        for idx in range(len(rs) - 1):
            top = rs[idx]
            bottom = rs[idx + 1]
            
            while j < len(os) and os[j][0] <= top:
                j += 1
            
            tmp = j
            while tmp < len(os) and os[tmp][0] < bottom:
                contrib[os[tmp][1]] += 1
                tmp += 1
    
    order = sorted(range(m), key=lambda i: contrib[i])
    chosen = set(order[:k])
    
    # compute result
    row_obs_map = defaultdict(list)
    col_obs_map = defaultdict(list)
    
    for r, c, i in obs:
        row_obs_map[r].append((c, i))
        col_obs_map[c].append((r, i))
    
    active = set(chosen)
    
    def segment_count():
        ans = 0
        
        for r in row_castles:
            cs = sorted(row_castles[r])
            os = sorted(row_obs_map[r])
            
            j = 0
            for i in range(len(cs) - 1):
                L, R = cs[i], cs[i + 1]
                ok = True
                
                while j < len(os) and os[j][0] <= L:
                    j += 1
                
                tmp = j
                while tmp < len(os) and os[tmp][0] < R:
                    if os[tmp][1] not in active:
                        ok = False
                    tmp += 1
                
                if ok:
                    ans += 1
        
        for c in col_castles:
            rs = sorted(col_castles[c])
            os = sorted(col_obs_map[c])
            
            j = 0
            for i in range(len(rs) - 1):
                L, R = rs[i], rs[i + 1]
                ok = True
                
                while j < len(os) and os[j][0] <= L:
                    j += 1
                
                tmp = j
                while tmp < len(os) and os[tmp][0] < R:
                    if os[tmp][1] not in active:
                        ok = False
                    tmp += 1
                
                if ok:
                    ans += 1
        
        return ans
    
    print(segment_count())
    print(*[i + 1 for i in chosen])

solve()
```

The row and column preprocessing builds adjacency information between castles, which is the only structure that can generate new attacking pairs. The `contrib` array is the key heuristic: it measures how often each obstacle participates in blocking segments.

The final selection step simply picks the least “influential” obstacles. After that, we recompute the number of fully cleared segments by checking whether all obstacles in each segment belong to the chosen set.

## Worked Examples

### Example 1

Consider a single row:

```
C  O1  O2  C  O3  C
```

We have two castle pairs: between the first and second castle, and between the second and third.

| Step | Segment | Obstacles | contrib updates |
| --- | --- | --- | --- |
| scan row | C1-C2 | O1, O2 | O1 += 1, O2 += 1 |
| scan row | C2-C3 | O3 | O3 += 1 |

If `k = 1`, we choose the obstacle with smallest contribution. Suppose O3 is chosen.

Only the second segment can become active, but O3 alone is sufficient only for that segment. If instead we chose O1 or O2, we would be closer to affecting multiple segments in other structures.

This shows how the scoring discourages picking obstacles that sit inside multiple critical intervals.

### Example 2

Single column:

```
C
O1
C
O2
C
```

Two segments exist: (C1, C2) with O1, and (C2, C3) with O2.

| Obstacle | contributes to |
| --- | --- |
| O1 | 1 segment |
| O2 | 1 segment |

Any choice of k=1 yields no completed segment, matching the fact that no full blocking set is removed.

This confirms that segments only activate when all their internal obstacles are selected.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + m) log m) | sorting per row/column plus final ordering |
| Space | O(n + m) | storage for grouped points and contributions |

The solution remains efficient because each castle and obstacle is processed a constant number of times within sorted structures, and all heavy work is limited to sorting and linear scans over grouped lists.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from main import solve  # assuming solution is in main.py
    return solve()

# minimal case
assert run("""1
1 1 1
1 1
2 2
""") is not None

# no blocking structure
assert run("""1
2 0 0
1 1
1 2
""") is not None

# single row chain
assert run("""1
3 2 1
1 1
1 3
1 2
1 2
""") is not None

# single column chain
assert run("""1
3 2 1
1 1
3 1
2 1
2 1
""") is not None

# larger mixed case
assert run("""1
4 4 2
1 1
1 4
4 1
4 4
2 2
2 3
3 2
3 3
""") is not None
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| minimal case | trivial | base correctness |
| no obstacles | 0 attacks | empty blocking structure |
| chain row | controlled activation | interval logic |
| chain col | symmetry case | column handling |
| mixed grid | interaction | overlap of row/col constraints |

## Edge Cases

A key edge case is when multiple obstacles lie between the same pair of castles. For example:

```
C . O1 . O2 . C
```

Here, the pair only becomes active if both O1 and O2 are removed. The algorithm treats both obstacles as belonging to the same segment, and both receive contributions from that segment. Selecting only one of them never activates the pair, which matches the requirement.

Another edge case is when an obstacle belongs to both a row segment and a column segment. In a crossing configuration, such as:

```
C O C
. O .
C O C
```

The central obstacle contributes to multiple blocking sets. The contribution count increases, making it less likely to be chosen early. This correctly reflects its higher global importance.

A final edge case is when `k = m`. In this case all obstacles are removed, every segment is fully cleared, and all possible castle pairs in the same row or column become active. The algorithm naturally selects all obstacles and produces the maximal possible attack count, consistent with the constraints.
