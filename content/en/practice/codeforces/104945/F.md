---
title: "CF 104945F - Programming-trampoline-athlon!"
description: "Each team in this competition is described by a name, a count of solved programming problems, and six scores coming from trampoline exercises. The final result of a team is a single total score formed by combining two independent parts."
date: "2026-06-28T07:09:30+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104945
codeforces_index: "F"
codeforces_contest_name: "2023-2024 ICPC Southwestern European Regional Contest (SWERC 2023)"
rating: 0
weight: 104945
solve_time_s: 66
verified: false
draft: false
---

[CF 104945F - Programming-trampoline-athlon!](https://codeforces.com/problemset/problem/104945/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 6s  
**Verified:** no  

## Solution
## Problem Understanding

Each team in this competition is described by a name, a count of solved programming problems, and six scores coming from trampoline exercises. The final result of a team is a single total score formed by combining two independent parts.

The programming part is straightforward: each solved problem contributes a fixed amount of points, so the programming score depends only on the integer $P$. The trampoline part is slightly more structured: from six given judge scores $E_1 \dots E_6$, the highest and lowest values are discarded, and the remaining four are summed. The final team score is the sum of these two components.

The task is not to simulate the competition itself, but to rank teams by their final score and output the best ones. A team is considered a medallist if it is not strictly worse than more than two other teams, which is equivalent to selecting the top few teams by score while respecting ties.

The input size allows up to $10^5$ teams. This immediately rules out anything quadratic such as pairwise comparisons or repeated sorting inside loops. The solution must be at least $O(N \log N)$, and ideally linear or dominated by a single sort.

A subtle point is the tie handling requirement. Teams with equal total score must be ordered by their original input order. This means that even after computing scores, we must preserve stability or explicitly encode order.

One edge case appears when many teams share the same score. For example, if all teams have identical totals, then all of them are effectively tied for first place, and all should be included. A naive interpretation of “top 1000” or “top 3 distinct ranks” can easily lead to wrong truncation if ties are not carefully handled.

Another edge case is arithmetic consistency in trampoline scoring. A careless implementation might forget to drop exactly one maximum and one minimum, or might incorrectly drop multiple identical extrema when duplicates exist. For instance, if the scores are $[10, 10, 9, 1, 1, 1]$, only one 10 and one 1 should be removed, not all occurrences.

## Approaches

A brute-force view starts by computing each team’s total score independently. For each team, we sum $P \cdot 10$ and the trampoline score computed by explicitly sorting six numbers and removing the extremes. This part is already constant work per team.

After computing all scores, we sort the teams by total score in descending order and then take the top candidates. Sorting $10^5$ items is feasible, but the real subtlety is in how many we are required to output. The statement enforces that at most 1000 teams should receive medals, but the actual rule is based on rank: a team qualifies if at most two teams have strictly higher score. This means we may need to include all teams tied at the cutoff boundary.

The optimal approach is therefore identical in structure to the brute force, except that we carefully define sorting and cutoff handling. Once all scores are computed, we perform a single sort by decreasing score and increasing input index. Then we scan from the top, keeping track of how many strictly higher scores have been seen. We stop only after exceeding the allowed rank threshold, but we must include all teams tied at the cutoff score.

This transforms the problem into a single sorting step plus a linear scan, avoiding any repeated comparisons.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(N \log N)$ | $O(N)$ | Acceptable but needs careful tie handling |
| Optimal | $O(N \log N)$ | $O(N)$ | Accepted |

## Algorithm Walkthrough

We compute a total score for each team, then select the top-ranked teams with careful tie preservation.

### Steps

1. Read all teams, assigning each an input index from 0 to $N-1$.

The index is needed to break ties deterministically in input order.
2. For each team, compute trampoline score by sorting its six values.

Remove the smallest and largest element, then sum the remaining four values.

Sorting is safe because there are only six elements, so this is constant time.
3. Compute total score as $10 \cdot P + \text{trampoline sum}$.
4. Store tuples of the form $(-\text{score}, \text{index}, \text{name})$.

Negating score ensures that sorting ascending produces descending score order.
5. Sort all teams by this tuple ordering.

This enforces primary ordering by score and secondary ordering by input order.
6. Traverse the sorted list and select teams while tracking how many strictly higher scores have been seen.

Since the list is sorted, the first distinct score group corresponds to rank 1, the next to rank 2, and so on.
7. Include teams until more than two strictly higher score groups have appeared.

When stopping, ensure that all teams sharing the cutoff score are included.

### Why it works

Sorting by total score partitions teams into contiguous blocks of equal score. Within each block, input order preserves deterministic output. The ranking condition depends only on how many distinct higher score levels exist above a team, which can be tracked during a single pass. Because equal scores are contiguous, we never split a valid medal group, and the cutoff boundary can be handled by finishing the current score block.

## Python Solution

```python
import sys
input = sys.stdin.readline

def trampoline_score(arr):
    arr.sort()
    return sum(arr[1:5])

def solve():
    n = int(input())
    teams = []

    for i in range(n):
        data = input().split()
        name = data[0]
        p = int(data[1])
        e = list(map(int, data[2:]))

        score = 10 * p + trampoline_score(e)
        teams.append((-score, i, name))

    teams.sort()

    result = []
    last_score = None
    distinct_higher = -1

    for idx, (neg_score, i, name) in enumerate(teams):
        score = -neg_score

        if score != last_score:
            distinct_higher += 1
            last_score = score

        if distinc
```
