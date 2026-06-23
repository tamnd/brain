---
title: "CF 105381M - The Tale of Professor Alya and the H-Index"
description: "We are given a list of citation counts for a researcher’s papers, already sorted in non-increasing order. Each number represents how many times a particular paper has been cited."
date: "2026-06-23T16:10:08+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105381
codeforces_index: "M"
codeforces_contest_name: "National Yang Ming Chiao Tung University 2024 Team Selection Programming Contest"
rating: 0
weight: 105381
solve_time_s: 43
verified: true
draft: false
---

[CF 105381M - The Tale of Professor Alya and the H-Index](https://codeforces.com/problemset/problem/105381/M)

**Rating:** -  
**Tags:** -  
**Solve time:** 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a list of citation counts for a researcher’s papers, already sorted in non-increasing order. Each number represents how many times a particular paper has been cited. The task is to compute the H-index, which is the largest integer H such that at least H papers have citation counts of at least H.

A useful way to interpret the definition is to imagine scanning the sorted list from the most cited paper onward. At position i (1-indexed), we ask whether this paper still qualifies as part of a group of size i, meaning its citation count is at least i. The answer is the largest position where this condition remains true.

The constraint n can be as large as 10^6, so the solution must run in linear time. Anything quadratic, such as checking every possible H and scanning the array each time, would involve up to 10^12 operations in the worst case and will not pass.

A subtle edge case happens when all citation counts are zero. For example, if n = 5 and the array is [0, 0, 0, 0, 0], no position satisfies i ≤ ci, so the answer must be 0. A naive implementation that assumes at least one valid paper might incorrectly return 1.

Another edge case appears when all citations are large. For example, [10, 10, 10] should return 3 because all three papers satisfy having at least 3 citations, even though they also satisfy higher raw values individually. The constraint is about position, not citation magnitude alone.

## Approaches

The brute-force idea is to try every possible candidate value H from 0 to n and check whether at least H papers have at least H citations. Since the array is sorted in descending order, checking a fixed H can be done by scanning until we find the first index where ci < H and counting how many elements are valid. This check costs O(n), and doing it for all H values leads to O(n^2) total work, which becomes too slow for n up to one million.

The key observation comes from the sorted structure. Since citations are in descending order, once we reach an index where ci < i, every later element will also fail because the array only decreases. This means the answer is determined by the first position where the condition breaks. We can scan once from left to right and stop immediately when ci < i, returning i - 1 as the H-index.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(1) | Too slow |
| Single Scan | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

### Optimal Strategy

We exploit the fact that the array is already sorted in non-increasing order.

1. Start scanning the array from the first paper with index i = 1. We compare the citation count ci with i because i represents how many papers we are trying to validate as part of the H-index group. This directly matches the definition of H-index.
2. For each position i, check whether ci ≥ i. If this holds, it means we can still potentially form an H-index of at least i because we have at least i papers with at least i citations.
3. Continue moving forward as long as the condition remains true. Each valid position extends the possible H-index.
4. The first time we encounter a position where ci < i, we stop. At that point, it is impossible to have any H-index greater than i - 1 because even the i-th paper does not satisfy the requirement.
5. Return i - 1 as the final answer. If we never break the condition, then all papers satisfy ci ≥ i, so the answer is n.

### Why it works

The correctness comes from monotonicity. Since the array is sorted in descending order, citation values never increase as we move right. Meanwhile, the required threshold i increases by exactly 1 at each step. Once ci < i, we know that for all j > i, both cj ≤ ci and j > i, so cj < j must hold as well. This guarantees that the first failure point is exactly where the maximum feasible H-index ends.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    if n == 0:
        print(0)
        return
    
    c = list(map(int, input().split()))
    
    for i, val in enumerate(c, start=1):
        if val < i:
            print(i - 1)
            return
    
    print(n)

if __name__ == "__main__":
    solve()
```

The solution reads n and the sorted citation list. It then performs a single pass, tracking the 1-based index using enumerate. The first time a citation value drops below its index, we return the previous index as the H-index. If no such break occurs, the H-index equals n.

A common off-by-one pitfall is forgetting that indexing is 1-based in the condition, so enumerate must start from 1. Another subtlety is handling n = 0, where no input list exists and the answer is directly zero.

## Worked Examples

### Example 1

Input array: [6, 5, 3, 1, 0]

| i | ci | ci ≥ i | Action |
| --- | --- | --- | --- |
| 1 | 6 | true | continue |
| 2 | 5 | true | continue |
| 3 | 3 | true | continue |
| 4 | 1 | false | stop |

We stop at i = 4, so the answer is 3. This shows that the algorithm correctly identifies the first violation of the H-index condition.

### Example 2

Input array: [10, 10, 10, 10]

| i | ci | ci ≥ i | Action |
| --- | --- | --- | --- |
| 1 | 10 | true | continue |
| 2 | 10 | true | continue |
| 3 | 10 | true | continue |
| 4 | 10 | true | continue |

No break occurs, so the answer is 4. This confirms that the algorithm handles the case where all papers exceed the required threshold.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Single linear scan over the citation list |
| Space | O(1) | Only constant extra variables are used |

The linear scan is sufficient for n up to 10^6 because it performs at most one comparison per element, well within typical time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n = int(input())
    if n == 0:
        return "0"
    c = list(map(int, input().split()))
    
    for i, val in enumerate(c, start=1):
        if val < i:
            return str(i - 1)
    return str(n)

# provided samples
assert run("5\n6 5 3 1 0\n") == "3"
assert run("5\n10 10 10 10 9\n") == "5"

# custom cases
assert run("0\n") == "0"
assert run("1\n0\n") == "0"
assert run("3\n3 3 3\n") == "3"
assert run("4\n4 3 2 1\n") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0 | 0 | empty array handling |
| 1 paper with 0 | 0 | single element boundary |
| 3 equal values | 3 | full saturation case |
| 4 3 2 1 | 2 | early break correctness |

## Edge Cases

For an empty publication list, the input is n = 0. The algorithm immediately returns 0 without attempting to access the citation array, which avoids invalid reads and matches the definition that no papers implies zero H-index.

For an array like [0, 0, 0], the scan fails at i = 1 because 0 < 1. The algorithm returns 0, correctly reflecting that no paper meets even a single citation threshold.

For a fully strong dataset like [100, 100, 100, 100], no break occurs during the scan. The algorithm reaches the end and returns n = 4, since all four papers satisfy the condition ci ≥ i for all i.
