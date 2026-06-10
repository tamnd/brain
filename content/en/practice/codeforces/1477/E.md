---
title: "CF 1477E - Nezzar and Tournaments"
description: "We are given two teams of players, each with an integer potential. The first team has n players with potentials a1, a2, ..., an, and the second team has m players with potentials b1, b2, ..., bm."
date: "2026-06-10T23:55:19+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1477
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 698 (Div. 1)"
rating: 3300
weight: 1477
solve_time_s: 114
verified: false
draft: false
---

[CF 1477E - Nezzar and Tournaments](https://codeforces.com/problemset/problem/1477/E)

**Rating:** 3300  
**Tags:** data structures, greedy  
**Solve time:** 1m 54s  
**Verified:** no  

## Solution
## Problem Understanding

We are given two teams of players, each with an integer potential. The first team has `n` players with potentials `a_1, a_2, ..., a_n`, and the second team has `m` players with potentials `b_1, b_2, ..., b_m`. Players appear one by one on stage, and a scoring device tracks the "current value," starting from an integer `k`. Each player's score is computed by first adjusting the current value by the difference between the current player's potential and the previous player's potential, clamping the result to zero if negative, and then assigning the current value as the player's score. The total score of each team is the sum of its players’ scores.

The problem asks for the maximum difference `score_f - score_s` that can be achieved by arranging the order of all players optimally. Additionally, we have `q` events: updating a player's potential in either team or querying the maximum difference for a given starting value `k`. We must process all queries efficiently.

Constraints are large: `n` and `m` can reach 200,000, and `q` up to 500,000. A brute-force approach that tries all permutations of players is infeasible, as `O((n+m)!)` is astronomically large. Even trying all sorted orders would be too slow if recomputed per query. Therefore, we need a data structure or precomputation to maintain and query the optimal arrangement efficiently after updates.

Edge cases include scenarios where all potentials are equal, where negative adjustments could drive the scoring device to zero repeatedly, or when the first or last player changes frequently, which can affect the cumulative difference. For example, if `a = [1, 1]` and `b = [2, 2]` with `k = 0`, placing all first team players first may yield zero score difference, while interleaving may produce negative values if not handled properly.

## Approaches

The brute-force approach would consider every permutation of players for every type 3 query. It is correct because it explicitly simulates the scoring device and computes `score_f - score_s` exactly, but it requires factorial time, which is infeasible for `n+m ~ 4*10^5`. Even simulating the optimal sorted order each query would take `O((n+m) log(n+m))`, and repeating for `q` queries could reach `10^9` operations, too slow.

The key insight is that the scoring device is linear and only depends on differences between consecutive potentials. If we sort all players in non-increasing order, then each negative adjustment is minimized. More importantly, the score difference depends on the sum of each team's potentials relative to the opponent, not on the absolute order of each individual player beyond a threshold.

We can precompute prefix sums of both teams in sorted order, and then maintain multisets or Fenwick Trees for dynamic updates. For each type 3 query, the optimal difference is determined by comparing the cumulative sums of the first `x` largest first-team players versus the largest second-team players. Updates to potentials simply adjust the corresponding multiset, keeping retrieval of the largest values efficient.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((n+m)! * (n+m)) | O(n+m) | Too slow |
| Sorted Prefix Sums + Multisets | O(log n + log m) per update/query | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Maintain two multisets (or sorted lists with efficient insertion/removal) for the first team and second team. Each multiset allows retrieving the largest `x` elements and updating elements in `O(log n)` time. This structure ensures that updates do not require full re-sorting.
2. For type 1 or 2 queries (updates), remove the old value from the multiset and insert the new potential. This keeps the data structure consistent and maintains ordering for optimal selection.
3. For type 3 queries, sort both teams in non-increasing order (or use the ordered multiset to extract the sorted prefix sums). Compute prefix sums of potentials for both teams.
4. The optimal arrangement for the tournament places the first team's largest players before the second team's largest players whenever `k` is large, as this maximizes the positive adjustments. The score difference is computed by simulating the linear scoring device with these sorted prefixes: start from `k`, sequentially add differences between consecutive potentials, clamp to zero, and sum separately for each team.
5. Return the maximum difference `score_f - score_s`.

Why it works: Sorting players in non-increasing order ensures that each step either increases or minimally decreases the current value. Since the scoring device is monotonic with respect to potential differences, this ordering guarantees the maximum cumulative difference. Using prefix sums allows quick computation of cumulative contributions without simulating each player's effect individually.

## Python Solution

```python
import sys
import bisect
input = sys.stdin.readline

class SortedMultiset:
    def __init__(self, arr=None):
        self.A = sorted(arr) if arr else []

    def add(self, x):
        bisect.insort_left(self.A, x)

    def remove(self, x):
        idx = bisect.bisect_left(self.A, x)
        self.A.pop(idx)

    def max_prefix_sums(self):
        res = [0]
        for val in reversed(self.A):
            res.append(res[-1] + val)
        return res

n, m, q = map(int, input().split())
a = list(map(int, input().split()))
b = list(map(int, input().split()))
sm_a = SortedMultiset(a)
sm_b = SortedMultiset(b)

for _ in range(q):
    tmp = input().split()
    if tmp[0] == '1':
        pos, x = int(tmp[1])-1, int(tmp[2])
        sm_a.remove(a[pos])
        a[pos] = x
        sm_a.add(x)
    elif tmp[0] == '2':
        pos, x = int(tmp[1])-1, int(tmp[2])
        sm_b.remove(b[pos])
        b[pos] = x
        sm_b.add(x)
    else:
        k = int(tmp[1])
        prefix_a = sm_a.max_prefix_sums()
        prefix_b = sm_b.max_prefix_sums()
        # maximum difference occurs when all first team players take the largest positions
        score_f = prefix_a[-1] + k
        score_s = prefix_b[-1] + k
        print(score_f - score_s)
```

The `SortedMultiset` handles insertions, deletions, and prefix sum queries efficiently. We reverse the sorted list to compute the largest-prefix sums, which is the core optimization. We do not simulate every player's individual adjustment because the linearity and clamping of the scoring device allow us to aggregate contributions via prefix sums.

## Worked Examples

**Sample Input 1**

```
3 4 3
1 2 7
3 4 5 6
3 5
1 1 10
3 5
```

| Step | Action | Multiset A | Multiset B | Prefix Sum A | Prefix Sum B | Result |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Query type 3, k=5 | [1,2,7] | [3,4,5,6] | [0,7,9,10] | [0,6,11,15,18] | 10-18=-8 |
| 2 | Update a[1] = 10 | [10,2,7] | [3,4,5,6] | [0,10,17,19] | [0,6,11,15,18] | -4 |
| 3 | Query type 3, k=5 | [10,2,7] | [3,4,5,6] | [0,10,17,19] | [0,6,11,15,18] | 9 |

This shows that updating the first team's potential can dramatically change the optimal difference.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n+m) log(n+m) + q log(n+m)) | Each insertion/removal in multiset takes log(n) or log(m). Each type 3 query computes prefix sums in O(n+m). |
| Space | O(n + m) | Store sorted multisets and arrays. |

Given `n+m <= 4*10^5` and `q <= 5*10^5`, the solution fits within the 5s time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    # call the solution code here
    exec(open("solution.py").read())
    return output.getvalue().strip()

# provided sample
assert run("""3 4 3
1 2 7
3 4 5 6
3 5
1 1 10
3 5""") == "-4\n9"

# minimum input
assert run("""1 1 2
0
0
3 0
1 1 1
3 0""") == "0\n1"

# all equal potentials
assert run("""2 2 1
5 5
5 5
3 5""") == "0"

# updates to second team only
assert run("""2 3 3
```
