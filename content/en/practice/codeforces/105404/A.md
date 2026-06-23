---
title: "CF 105404A - No More Ties!"
description: "We are given several independent scenarios. In each scenario, a contest has a list of participant scores and only the top k participants are supposed to qualify."
date: "2026-06-23T17:16:58+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105404
codeforces_index: "A"
codeforces_contest_name: "XXIV Spain Olympiad in Informatics, Online Qualifier 2"
rating: 0
weight: 105404
solve_time_s: 70
verified: true
draft: false
---

[CF 105404A - No More Ties!](https://codeforces.com/problemset/problem/105404/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 10s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several independent scenarios. In each scenario, a contest has a list of participant scores and only the top `k` participants are supposed to qualify. The issue is that qualification depends purely on score ranking, but ties in scores can make it impossible to decide exactly who belongs to the top `k` without looking at additional tie-breaking rules like penalty time.

For each test case, we must determine whether the score cutoff between the top `k` and the rest is clean or ambiguous. A clean separation means that all participants in the top `k` positions have strictly higher scores than everyone outside. An ambiguous separation happens when the boundary crosses a group of equal scores, meaning some participants on the border have identical scores and cannot be uniquely split into “qualified” and “not qualified” using only scores.

The output is a binary decision per test case. We print a positive answer when the partition is clean, and a tie warning when the boundary lies inside an equal-score group.

The constraints allow up to 100 test cases and up to 10,000 participants per case. A solution that sorts each test case independently is easily fast enough since sorting 10,000 elements costs about `O(n log n)` which is well within limits even for 100 cases. Any approach that tries to compare every pair of participants is unnecessary but would still likely pass at this scale; however, it is conceptually too slow and obscures the structure of the problem.

A subtle corner case appears when the `k`-th score is equal to the `(k+1)`-th score. In that situation, there is no way to decide who belongs in the top `k` without external rules. Another case is when all scores are identical, where every possible cutoff is ambiguous regardless of `k`.

Example of ambiguity:

Input: `n = 5, k = 3, scores = [10, 10, 10, 5, 1]`

Here the top three are all 10s, but any ordering among them is fine, and the cutoff is clean, so this is actually fine.

Example of tie issue:

Input: `n = 5, k = 2, scores = [10, 10, 10, 5, 1]`

The second and third positions both have score 10, so selecting exactly two from the three tied contestants is impossible without tie-breakers. Output must indicate ambiguity.

The core question reduces to checking whether the boundary between index `k` and `k+1` in sorted order crosses equal values.

## Approaches

The most direct way to reason about the problem is to simulate the ranking process. One could sort participants by score in descending order and then inspect the cutoff position. After sorting, we examine the score at position `k` and compare it with the score at position `k+1`. If they differ, the boundary is clean. If they are equal, the boundary lies inside a tie group and the split is ambiguous.

A brute-force variant might try, for each participant, to determine whether they can be part of some valid top `k` assignment under tie constraints, but this quickly becomes unnecessary complexity. The structure of the problem guarantees that only the relationship between the `k`-th and `(k+1)`-th largest values matters. Everything else is irrelevant because ordering inside groups of equal values does not change feasibility.

The key insight is that only the cutoff boundary matters, not the full ranking. Once scores are sorted, the entire decision reduces to a single comparison between two adjacent elements.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Full simulation of ranking assignments | O(n²) | O(n) | Too slow |
| Sort and check boundary | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases. Each test case is processed independently because no state is shared.
2. For each test case, read `n` and `k`, then read the list of scores. The order of input is irrelevant since ranking depends only on sorting.
3. Sort the scores in descending order. This produces the exact ranking from best to worst, so the cutoff between qualified and non-qualified participants becomes contiguous in the array.
4. Identify the score at index `k - 1` (0-based indexing). This represents the lowest score among the qualified group if we take the top `k`.
5. Identify the score at index `k`. This represents the highest score among the non-qualified group.
6. Compare these two values. If they are equal, the cutoff lies inside a tie group and we cannot separate participants cleanly. Otherwise, the split is valid.
7. Output `"EMPATE"` when the boundary is ambiguous and `"BIEN"` when it is clean.

### Why it works

After sorting, all equal values form contiguous blocks. Any valid selection of top `k` elements must take a prefix of this sorted array except when the boundary falls inside one of these blocks. If the `k`-th and `(k+1)`-th elements are equal, the prefix cut splits a block of identical scores, meaning multiple valid choices exist for who is inside or outside the top `k`. If they differ, every element in the prefix strictly dominates every element outside, so the partition is uniquely determined by scores alone.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, k = map(int, input().split())
    arr = list(map(int, input().split()))
    
    arr.sort(reverse=True)
    
    if arr[k - 1] == arr[k]:
        print("EMPATE")
    else:
        print("BIEN")
```

The solution reads each test case, sorts the scores in descending order, and then performs a single comparison at the cutoff boundary. The critical implementation detail is using `k - 1` and `k` due to 0-based indexing. This is the most common source of errors in this problem because mixing 1-based and 0-based positions shifts the boundary incorrectly.

Sorting in reverse order ensures the highest scores are at the front, making the top `k` contiguous. No additional data structures are needed since only two positions matter after sorting.

## Worked Examples

### Example 1

Input:

`n = 5, k = 2, scores = [10, 10, 10, 5, 1]`

| Step | Sorted Scores | arr[k-1] | arr[k] | Decision |
| --- | --- | --- | --- | --- |
| After sort | [10, 10, 10, 5, 1] | 10 | 10 | EMPATE |

This shows a tie at the boundary. The second and third elements are identical, so there is no unique way to choose exactly two participants from the top group.

### Example 2

Input:

`n = 5, k = 3, scores = [8, 13, 10, 14, 1]`

| Step | Sorted Scores | arr[k-1] | arr[k] | Decision |
| --- | --- | --- | --- | --- |
| After sort | [14, 13, 10, 8, 1] | 10 | 8 | BIEN |

Here the boundary is between 10 and 8, which are distinct. The top 3 are uniquely determined by score alone.

These traces confirm that only the equality of the boundary pair matters, and internal ordering inside equal-value blocks does not affect the decision.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t · n log n) | Each test case sorts `n` scores |
| Space | O(n) | Storage for the score list per test case |

The constraints allow up to 10,000 elements per test case, so sorting is efficient enough even in the worst case. The algorithm performs a small constant amount of work after sorting, keeping runtime comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n, k = map(int, input().split())
        arr = list(map(int, input().split()))
        arr.sort(reverse=True)
        out.append("EMPATE" if arr[k-1] == arr[k] else "BIEN")
    return "\n".join(out) + "\n"

# provided sample
assert run("""5
2 1
1 1
10 5
5 8 0 9 2 0 3 0 1 1
5 1
8 13 10 14 1
3 1
0 1 1
10 8
5 7 4 2 3 2 2 7 7 3
""") == """EMPATE
BIEN
BIEN
EMPATE
EMPATE
"""

# all equal values
assert run("""1
5 3
7 7 7 7 7
""") == "EMPATE\n"

# clear separation
assert run("""1
6 3
9 8 7 6 5 4
""") == "BIEN\n"

# boundary tie only
assert run("""1
4 2
10 10 5 1
""") == "EMPATE\n"

# minimum n
assert run("""1
2 1
1 0
""") == "BIEN\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal | EMPATE | full tie group makes cutoff ambiguous |
| strictly decreasing | BIEN | clean boundary after sort |
| boundary tie | EMPATE | equal values across cutoff |
| minimum size | BIEN | base case correctness |

## Edge Cases

When all scores are identical, sorting produces a uniform array. For any `k`, the pair `arr[k-1]` and `arr[k]` are equal, so the algorithm correctly outputs `"EMPATE"`. This reflects that no score-based partition can separate participants.

When the cutoff happens inside a tie group, such as `[10, 10, 10, 5]` with `k = 2`, sorting yields `[10, 10, 10, 5]` and the comparison is between `10` and `10`, producing `"EMPATE"`. This matches the fact that any choice of two among the three top scores is indistinguishable by score alone.

When there is a strict drop at the boundary, such as `[9, 8, 7, 6]` with `k = 2`, the comparison is between `8` and `7`, producing `"BIEN"`. The prefix of size `k` is uniquely determined because every selected score is strictly larger than every excluded score.
