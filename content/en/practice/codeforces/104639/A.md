---
title: "CF 104639A - Qualifiers Ranking Rules"
description: "We are given the ordered results of two separate programming contests. Each contest ranks individual teams, but what ultimately matters is the performance of universities rather than individual teams."
date: "2026-06-29T16:55:11+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104639
codeforces_index: "A"
codeforces_contest_name: "The 2023 ICPC Asia EC Regionals Online Contest (I)"
rating: 0
weight: 104639
solve_time_s: 56
verified: true
draft: false
---

[CF 104639A - Qualifiers Ranking Rules](https://codeforces.com/problemset/problem/104639/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 56s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given the ordered results of two separate programming contests. Each contest ranks individual teams, but what ultimately matters is the performance of universities rather than individual teams.

For each contest, a university is represented by multiple teams, but only its best-performing team matters. So the first step in both contests is to compress the team-level ranking into a university-level ranking by keeping, for each university, the best (earliest) position it appears in that contest’s list.

Once we have two rankings of universities, one per contest, we need to merge them into a single final ordering. The merge rule behaves like a stable merge of two sorted lists: we repeatedly compare universities based on their rank in each contest. If a university appears earlier in the first contest ranking than another, it is considered better; if they have the same rank position across contests, the one from the first contest is prioritized.

After merging, duplicates appear because universities show up in both lists. We keep only the first occurrence of each university in the merged sequence, preserving order.

The output is the final deduplicated ranking of universities.

The constraints allow up to 10^4 teams per contest, so a naive O(n^2) comparison or repeated scanning for best ranks is already borderline but still possibly acceptable in Python. However, the merge step must be linear after preprocessing, otherwise it will TLE if implemented with repeated list removals or repeated membership checks in lists.

A subtle failure case appears if one tries to directly merge team lists without collapsing to university rankings first. That would incorrectly treat multiple teams of the same university as separate competitors.

Another edge case arises when a university appears only in one contest. It still must appear in the final ranking and should be merged correctly without artificial penalties.

## Approaches

A direct approach is to simulate the entire process literally. For each contest, scan the ranked list and, for every university, store the first occurrence index as its score. This produces two dictionaries mapping university to rank.

Then we repeatedly build a merged sequence. At each step, we compare all remaining universities not yet placed and select the best according to the comparison rule, append it, and remove it from consideration. This is equivalent to repeatedly selecting the minimum under a custom ordering.

The issue is that this selection step is expensive. If there are U universities, selecting the next best requires scanning O(U) candidates, repeated O(U) times, leading to O(U^2). With U up to 10^4, this becomes around 10^8 operations, which is too slow in Python.

The key observation is that after converting each contest into a ranking list of unique universities, both lists are already sorted in the desired order. The final rule is exactly a stable merge of two sorted sequences, where comparison is lexicographic based on rank positions in each list, with a tie-break favoring the first list.

This reduces the problem to merging two pre-sorted lists using two pointers, followed by deduplication using a set.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force selection | O(U^2) | O(U) | Too slow |
| Two-pointer merge | O(n + m) | O(U) | Accepted |

## Algorithm Walkthrough

We first compress each contest’s team list into a unique university ranking.

1. Read the first contest list from top to bottom. For each university, if it has not been seen before, record it in order. This produces the first ranking list. The same is done for the second contest. This step is valid because only the best team per university matters, and the earliest occurrence corresponds to the best rank.
2. Treat these two lists as ordered sequences. We now merge them using two pointers, one pointing at each list. At each step, we compare the current candidates from both lists.
3. If both pointers point to different universities, we append the one that should appear earlier in the final ordering. The ordering rule is that earlier position in the first list dominates; otherwise we compare positions in the second list. Practically, this is equivalent to merging based on the pair (rank_in_first, rank_in_second), with missing values treated as infinity.
4. If one list is exhausted, we append the remaining elements from the other list.
5. During merging, we maintain a set of already output universities. If a university has already been output, we skip it. This is necessary because a university can appear in both lists, and duplicates must be removed in the final output.
6. Continue until both lists are fully processed.

After these steps, the output list contains each university exactly once in the correct merged order.

### Why it works

Each contest list is already sorted by increasing rank. The merge rule defines a consistent ordering between any two universities based on their relative positions in these two sorted sequences. Because the comparison is transitive and consistent with lexicographic ordering of rank pairs, the merged sequence produced by the two-pointer process preserves global ordering. Deduplication does not affect correctness because once a university appears in the merged order, any later occurrence represents a strictly worse position and can be safely ignored.

## Python Solution

```python
import sys
input = sys.stdin.readline

def build_ranking(arr):
    seen = set()
    res = []
    for x in arr:
        if x not in seen:
            seen.add(x)
            res.append(x)
    return res

def solve():
    n, m = map(int, input().split())
    a = [input().strip() for _ in range(n)]
    b = [input().strip() for _ in range(m)]

    r1 = build_ranking(a)
    r2 = build_ranking(b)

    pos1 = {u: i for i, u in enumerate(r1)}
    pos2 = {u: i for i, u in enumerate(r2)}

    i = j = 0
    used = set()
    out = []

    while i < len(r1) or j < len(r2):
        while i < len(r1) and r1[i] in used:
            i += 1
        while j < len(r2) and r2[j] in used:
            j += 1

        if i >= len(r1) and j >= len(r2):
            break
        if i >= len(r1):
            u = r2[j]
            j += 1
        elif j >= len(r2):
            u = r1[i]
            i += 1
        else:
            u1 = r1[i]
            u2 = r2[j]

            if pos1.get(u1, float('inf')) < pos1.get(u2, float('inf')):
                u = u1
                i += 1
            elif pos1.get(u1, float('inf')) > pos1.get(u2, float('inf')):
                u = u2
                j += 1
            else:
                if pos2.get(u1, float('inf')) <= pos2.get(u2, float('inf')):
                    u = u1
                    i += 1
                else:
                    u = u2
                    j += 1

        if u not in used:
            used.add(u)
            out.append(u)

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution first compresses duplicate universities in each contest list, preserving only first occurrences because those represent best team ranks. It then builds position maps so comparisons can be done in constant time. The merging loop carefully advances pointers while skipping already used universities to avoid redundant processing. The tie-breaking condition ensures deterministic behavior when universities have equal relative ordering.

## Worked Examples

Consider a small case:

Input:

```
5 4
A
B
A
C
D
B
C
E
C
```

First contest unique ranking becomes A, B, C, D. Second becomes B, C, E.

| Step | i pointer | j pointer | chosen | output |
| --- | --- | --- | --- | --- |
| 1 | A | B | A | A |
| 2 | B | B | B (tie handled by first list preference) | A B |
| 3 | C | C | C | A B C |
| 4 | D | E | D | A B C D |
| 5 | - | E | E | A B C D E |

This confirms that the merge respects both rankings and preserves stability in tie situations.

Another case:

Input:

```
3 3
X
Y
Z
Z
Y
X
```

First ranking: X, Y, Z. Second ranking: Z, Y, X.

| Step | r1 | r2 | chosen | output |
| --- | --- | --- | --- | --- |
| 1 | X | Z | X | X |
| 2 | Y | Z | Y | X Y |
| 3 | Z | Z | Z | X Y Z |

This shows that even when rankings are reversed, the merge still produces a consistent deterministic order.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Each list is scanned once to build rankings and once during merging |
| Space | O(u) | Stores position maps and output list of unique universities |

The linear complexity fits comfortably within the constraints of 10^4 entries per contest, and dictionary operations ensure constant-time comparisons during merging.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    import contextlib
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# sample-like case
assert run("""5 4
A
B
A
C
D
B
C
E
C
""") == "A\nB\nC\nD\nE"

# reverse ordering
assert run("""3 3
X
Y
Z
Z
Y
X
""") == "X\nY\nZ"

# single university
assert run("""3 2
UNI
UNI
UNI
UNI
UNI
""") == "UNI"

# disjoint sets
assert run("""3 3
A
B
C
D
E
F
""") == "A\nB\nC\nD\nE\nF"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single repeated university | UNI | deduplication correctness |
| reversed rankings | X Y Z | tie-breaking stability |
| disjoint sets | merged order | simple concatenation case |
| duplicate-heavy input | correct unique output | first-occurrence compression |

## Edge Cases

One edge case is when a university appears many times in a single contest list. For example, if input is `A A A A B`, the compression step ensures only `A B` remains. During execution, the algorithm ignores later occurrences because the `seen` set filters them immediately. Without this step, the merge logic would incorrectly treat repeated occurrences as separate entries and produce duplicates.

Another edge case occurs when a university appears only in one contest. For example, if `X` is in the first ranking but not in the second, its position in `pos2` defaults to infinity. During comparison, this ensures it is placed purely according to the first contest order, which matches the intended rule that absence in a contest should not penalize it.

A final case is full reversal between contests. Even when the two rankings are opposite, the pairwise comparison rule guarantees a deterministic ordering because every comparison resolves based on a consistent lexicographic ordering of rank pairs, and ties are broken by preferring the first contest.
