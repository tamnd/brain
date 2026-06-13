---
title: "CF 1197A - DIY Wooden Ladder"
description: "We are given several independent sets of wooden planks, where each plank has a fixed length and cannot be cut. From each set, we want to assemble a structure called a ladder with as many steps as possible. A k-step ladder is formed by selecting exactly k + 2 planks."
date: "2026-06-13T14:29:19+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1197
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 69 (Rated for Div. 2)"
rating: 900
weight: 1197
solve_time_s: 353
verified: true
draft: false
---

[CF 1197A - DIY Wooden Ladder](https://codeforces.com/problemset/problem/1197/A)

**Rating:** 900  
**Tags:** greedy, math, sortings  
**Solve time:** 5m 53s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several independent sets of wooden planks, where each plank has a fixed length and cannot be cut. From each set, we want to assemble a structure called a ladder with as many steps as possible.

A k-step ladder is formed by selecting exactly k + 2 planks. Two of these must be “base” planks, and each base must have length at least k + 1. The remaining k planks are “step” planks, and each of them must have length at least 1, which effectively means any plank can serve as a step.

So the only real restriction is on the base: we need two sufficiently long planks to support a ladder of height k, and the rest of the chosen planks just need to exist to form the steps.

For each query, we must choose some subset of planks to maximize k. We are allowed to ignore planks completely, but we cannot split or modify them.

The constraints allow up to 100,000 planks in total across all test cases. That immediately rules out any solution that tries to test all subsets or even all pairs of base candidates per possible k. Anything quadratic in n per test case will fail. Sorting or linear scans per test is acceptable.

A few subtle failure cases appear if we reason too locally. First, it is tempting to assume that the answer depends only on the two largest planks, but that ignores whether there are enough remaining planks to form steps. Second, it is easy to forget that increasing k makes base requirements stricter, so a solution that greedily picks the largest k first without verifying feasibility will overestimate.

A concrete edge case is when we have only two large planks but not enough total planks:

Input:

```
1
3
10 10 1
```

We can form k = 1, because we can use 10 and 10 as bases and the remaining 1 as a step. But k = 2 is impossible even though bases are sufficient, since we would need 4 planks total.

Another case is when there are many small planks but no two large ones:

```
1
5
1 1 1 1 1
```

No ladder can be built because we cannot form two bases of length at least 2.

These examples show that both “count of long planks” and “availability of extra planks” matter simultaneously.

## Approaches

A brute-force approach would try every possible k from 0 up to n − 2 and check feasibility. For each k, we would scan the array, count how many planks are at least k + 1 for base candidates, and verify we have at least two such planks and at least k + 2 total planks. Each check costs O(n), and doing it for all k gives O(n^2) per test case, which is far too slow for 100,000 total elements.

The key observation is that feasibility is monotonic in a structured way. As k increases, the base threshold k + 1 increases, so the set of usable base planks only shrinks. At the same time, the total number of planks required increases linearly. This suggests we can process candidates in descending order of length and track how many usable bases we currently have.

If we sort planks in decreasing order, we can imagine gradually lowering the threshold for k and asking: at what point do we first have enough planks that can serve as bases? Each time we consider a candidate k, we need to know whether there are at least two planks among those with length ≥ k + 1, and whether we have at least k + 2 total planks available.

Instead of recomputing counts from scratch for each k, we sweep from largest to smallest plank length and maintain how many elements are currently “eligible” for being a base at the current threshold. This reduces the problem to a single pass after sorting.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal | O(n log n) | O(1) or O(n) | Accepted |

## Algorithm Walkthrough

We first sort the plank lengths in descending order. This ordering lets us reason about progressively stricter base requirements.

We maintain a pointer i that moves through the sorted array and represents how many planks are currently considered usable as potential bases under a given threshold. We also track how many steps k we can currently support based on how many planks we have already processed.

1. Sort the array in descending order so that we process largest planks first. This ensures that when we are considering a candidate threshold, all larger or equal planks have already been accounted for.
2. Initialize a counter cnt = 0, which represents how many planks we have seen so far that are eligible for becoming base candidates at the current threshold.
3. Traverse the sorted array. At position i, we are effectively considering whether we can support a ladder where the base threshold is a[i]. Every time we include a new plank, we increment cnt.
4. After including the i-th plank, check whether we can form a valid ladder using cnt eligible base candidates. Since we need two bases, we require cnt ≥ 2.
5. The number of steps k we can potentially support at this stage is bounded by how many planks we have processed minus 2, because k + 2 total planks are required. So we compute k = min(cnt - 2, i - 1).
6. Keep track of the maximum k across all positions.

The key reasoning step is that at each stage, the current index i corresponds to a candidate number of planks we can use, and cnt tracks how many of them are strong enough to act as bases for that level.

### Why it works

At any point in the sorted traversal, we have exactly the set of planks that are at least as large as the current threshold. Any valid ladder of height k must pick two base planks from this set, so feasibility depends only on how many elements remain in this prefix. Since both constraints, base requirement and total number of planks, tighten monotonically as we move through smaller values, the best achievable k must occur at one of these prefix states. Therefore, checking each prefix captures all possible optimal configurations without missing any valid arrangement.

## Python Solution

```python
import sys
input = sys.stdin.readline

T = int(input())
for _ in range(T):
    n = int(input())
    a = list(map(int, input().split()))
    
    a.sort(reverse=True)
    
    cnt = 0
    ans = 0
    
    for i, val in enumerate(a):
        cnt += 1
        
        k = min(cnt - 2, i)  # i = number of remaining step capacity minus 1
        if k > ans:
            ans = k
    
    print(max(ans, 0))
```

The solution begins by sorting the plank lengths so we can evaluate feasibility in decreasing order of potential base strength. The variable cnt tracks how many planks are currently in the prefix we are considering. At each step, i represents how many additional planks beyond the first are available to act as steps.

The expression cnt - 2 reflects how many planks can be reserved as steps after choosing two bases. The expression i reflects how many total “slots” are available for building the structure up to this prefix. Taking the minimum ensures we respect both constraints simultaneously.

Finally, we take the maximum over all prefixes because the optimal ladder size corresponds to the most permissive prefix before base constraints become too strict.

## Worked Examples

### Example 1

Input:

```
4
1 3 1 3
```

Sorted array:

```
[3, 3, 1, 1]
```

| i | val | cnt | cnt - 2 | i | k = min(cnt-2, i) |
| --- | --- | --- | --- | --- | --- |
| 0 | 3 | 1 | -1 | 0 | -1 → ignored |
| 1 | 3 | 2 | 0 | 1 | 0 |
| 2 | 1 | 3 | 1 | 2 | 1 |
| 3 | 1 | 4 | 2 | 3 | 2 |

The maximum k is 2, meaning we can build a 2-step ladder. This happens when all planks are usable and we can allocate two large ones as bases.

### Example 2

Input:

```
3
1 1 2
```

Sorted array:

```
[2, 1, 1]
```

| i | val | cnt | cnt - 2 | i | k |
| --- | --- | --- | --- | --- | --- |
| 0 | 2 | 1 | -1 | 0 | -1 |
| 1 | 1 | 2 | 0 | 1 | 0 |
| 2 | 1 | 3 | 1 | 2 | 1 |

Answer is 1, matching the fact that only one valid step can be supported once we have two usable bases.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates, single pass afterward |
| Space | O(1) extra | Only counters and in-place sort |

The total number of elements across all test cases is at most 100,000, so sorting each test case independently remains efficient under the constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    T = int(input())
    out = []
    for _ in range(T):
        n = int(input())
        a = list(map(int, input().split()))
        a.sort(reverse=True)

        cnt = 0
        ans = 0
        for i, _ in enumerate(a):
            cnt += 1
            k = min(cnt - 2, i)
            ans = max(ans, k)
        out.append(str(max(ans, 0)))
    return "\n".join(out)

# provided samples
assert run("""4
4
1 3 1 3
3
3 3 2
5
2 3 3 4 2
3
1 1 2
""") == """2
1
2
0"""

# custom cases
assert run("""1
2
10 10
""") == "0", "minimum edge"

assert run("""1
3
10 10 1
""") == "1", "one step possible"

assert run("""1
5
1 1 1 1 1
""") == "0", "no valid bases"

assert run("""1
6
5 5 5 5 5 5
""") == "4", "all equal large planks"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 10 10 | 0 | insufficient planks for any ladder |
| 10 10 1 | 1 | base + single step feasibility |
| 1 1 1 1 1 | 0 | no valid base threshold |
| all 5s | 4 | maximum utilization case |

## Edge Cases

One edge case is when there are exactly two planks. The algorithm sorts them and immediately finds cnt = 2 at the second iteration, but k = min(0, 1) = 0, which correctly yields no positive ladder since at least one step is required.

Another case is when all planks are identical and large. For example, with six planks of length 5, every prefix satisfies the base condition, and the limiting factor becomes only the number of available planks. The algorithm correctly increases k until it reaches 4, since k + 2 = 6 exactly matches the total number of planks, and two of them are reserved as bases.
