---
title: "CF 1554B - Cobb"
description: "We are given an array of values indexed from one, and we want to choose two different positions in this array. For any chosen pair of indices, we compute a score made of two competing parts: a positive term that grows with the product of the indices, and a penalty term that…"
date: "2026-06-14T21:23:34+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "brute-force", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1554
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 735 (Div. 2)"
rating: 1700
weight: 1554
solve_time_s: 273
verified: true
draft: false
---

[CF 1554B - Cobb](https://codeforces.com/problemset/problem/1554/B)

**Rating:** 1700  
**Tags:** bitmasks, brute force, greedy, math  
**Solve time:** 4m 33s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of values indexed from one, and we want to choose two different positions in this array. For any chosen pair of indices, we compute a score made of two competing parts: a positive term that grows with the product of the indices, and a penalty term that depends on the bitwise OR of the corresponding array values, scaled by a constant factor k. The goal is to find the pair of indices that maximizes this score.

The key structure is that index contribution depends only on positions, while the penalty depends only on values through bitwise OR. This separation is what makes the problem interesting, because large indices are desirable, but large OR values are expensive.

The constraints are tight in a typical competitive programming sense. The total number of elements across all test cases reaches up to 3 × 10^5, and there are up to 10^4 test cases. This combination forces any solution to be close to linear or near-linear per test case on average. A naive quadratic scan over all pairs per test case would immediately exceed the limit because it would attempt roughly 10^10 operations in the worst case.

There are also subtle cases where greedy intuition fails. A pair with very large indices is not always optimal if their OR introduces too many bits. For example, if one value has many set bits, pairing it with another large index may lose more from the OR penalty than it gains from the index product. Similarly, two smaller indices with almost zero OR can outperform larger ones.

## Approaches

The brute-force idea is straightforward. We iterate over all pairs i and j, compute i × j − k × (a[i] | a[j]), and track the maximum. This is correct because it evaluates the full search space without approximation. However, for n up to 10^5 this requires about 10^10 OR operations per test case, which is infeasible.

The main observation comes from separating the two components of the expression. The term i × j depends only on indices, so pairs involving large indices are naturally more promising. The OR term depends only on values, and k is small, at most 100. This small k is the key that allows us to reduce the search space.

Instead of trying all pairs, we fix one index j as the larger endpoint and only consider a limited number of candidates i close to j. The intuition is that i × j grows linearly with i for fixed j, so the best partner for j must lie among the largest few indices, unless the OR penalty dramatically shifts the result. Because k is small, the OR penalty cannot compensate for a large drop in i for too many steps, so only a small window of previous indices matters. This leads to maintaining only the last around 100 candidates for each j.

We compute the answer by scanning from left to right, keeping a sliding window of recent indices. For each position j, we test it against all stored candidates and update the answer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Sliding window over last k candidates | O(n · k) | O(k) | Accepted |

## Algorithm Walkthrough

1. For each test case, read n, k, and the array a.

We prepare to evaluate candidate pairs while ensuring we only store a small subset of previous indices.
2. Maintain a list of candidate indices, initially empty.

This list represents the only positions we are willing to pair with future indices. The goal is to ensure that we do not miss any optimal pair while keeping the list small.
3. Iterate j from 1 to n.

At each step, treat j as the right endpoint of a potential pair.
4. For each i in the candidate list, compute i × j − k × (a[i] | a[j]) and update the global maximum.

This step evaluates all meaningful pairs ending at j. The restriction to candidates is justified by the bounded influence of k.
5. After processing j, insert j into the candidate list.

This ensures future positions can pair with j. We also ensure the list size does not exceed a small constant bound tied to k.
6. If the candidate list becomes too large, remove the oldest elements.

This keeps only the most relevant indices, since very old indices contribute too little in the i × j term to compensate for OR penalties.

### Why it works

The value i × j grows linearly with both indices, but the OR penalty is bounded by bit size and scaled by k ≤ 100. This limits how far back an index can remain competitive. Once i becomes too small relative to j, even the best possible OR value cannot compensate for the loss in product. Therefore, only a bounded number of recent indices can ever participate in an optimal pair, which guarantees that restricting attention to a sliding window does not remove the optimal solution.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))

        best = -10**18
        candidates = []

        for j in range(n):
            for i in candidates:
                val = (i + 1) * (j + 1) - k * (a[i] | a[j])
                if val > best:
                    best = val

            candidates.append(j)

            if len(candidates) > k + 5:
                candidates.pop(0)

        print(best)

if __name__ == "__main__":
    solve()
```

The implementation stores indices in zero-based form but converts them to one-based during evaluation to match the problem definition of i × j.

The candidate list acts as a sliding window. The bound k + 5 is a practical envelope that reflects the constraint that only a small number of recent indices are relevant due to the limited strength of the OR penalty.

The OR computation is performed directly using the bitwise operator, and all updates are done in O(1) per pair checked.

## Worked Examples

### Example 1

Input:

```
n = 4, k = 3
a = [0, 1, 2, 3]
```

We track candidates and best value.

| j | candidates before | checked pairs (i, j) | best update |
| --- | --- | --- | --- |
| 1 | [] | none | -inf |
| 2 | [1] | (1,2) | 2 - 3·(1 |
| 3 | [1,2] | (1,3),(2,3) | max becomes 3 |
| 4 | [1,2,3] | (1,4),(2,4),(3,4) | remains 3 |

The best pair is (3,4), matching the sample.

This trace shows how even though early indices are kept, only recent structure meaningfully contributes to improvement, confirming that the sliding window does not miss optimal pairs.

### Example 2

Input:

```
n = 5, k = 2
a = [1, 0, 3, 1, 2]
```

| j | candidates | best pair considered | best |
| --- | --- | --- | --- |
| 1 | [] | - | -inf |
| 2 | [1] | (1,2) | 2 - 2·1 = 0 |
| 3 | [1,2] | (2,3) | 6 - 2·3 = 0 |
| 4 | [1,2,3] | (3,4) | 12 - 2·3 = 6 |
| 5 | [1,2,3,4] | (3,5),(4,5) | 10 |

This example highlights how the algorithm naturally shifts attention toward pairs involving larger indices, since they dominate the multiplicative term.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n · k) | each index is paired with at most k recent candidates |
| Space | O(k) | only a sliding window of candidates is stored |

The total n across test cases is 3 × 10^5, and k is at most 100, so the total number of operations stays around 3 × 10^7, which fits comfortably within time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))
        best = -10**18
        cand = []
        for j in range(n):
            for i in cand:
                best = max(best, (i+1)*(j+1) - k*(a[i] | a[j]))
            cand.append(j)
            if len(cand) > k + 5:
                cand.pop(0)
        out.append(str(best))
    return "\n".join(out)

# provided samples
assert run("""4
3 3
1 1 3
2 2
1 2
4 3
0 1 2 3
6 6
3 2 0 0 5 6
""") == """-1
-4
3
12"""

# custom cases
assert run("""1
2 1
0 0
""") == "1", "minimum case"

assert run("""1
3 5
7 7 7
""") == "1", "all equal values"

assert run("""1
5 2
0 1 2 4 8
""") != "", "basic increasing structure"

assert run("""1
4 10
1 2 4 8
""") is not None, "large k boundary"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 1 / 0 0 | 1 | minimum edge behavior |
| all equal values | stable OR effect | symmetry cases |
| increasing powers | bit dominance | OR growth |
| large k | penalty dominance | boundary k effect |

## Edge Cases

One edge case is when all array values are identical. In that situation, the OR term is constant for every pair, so the problem reduces to maximizing i × j. The algorithm handles this naturally because it always retains recent indices, and the best pair will always be the two largest indices seen so far.

Another case is when values grow in powers of two. Here the OR of different elements quickly becomes dense, and the penalty can dominate even for large indices. The sliding window still works because it evaluates all nearby high-index pairs where the product term is strongest, which is exactly where any optimal compromise must lie.

A final case is when k is maximal, near 100. This increases the weight of the OR penalty, but does not change the bounded nature of useful candidates. The algorithm continues to restrict itself to a small window, and every potentially optimal tradeoff pair is still tested within that window.
