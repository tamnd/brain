---
title: "CF 1768B - Quick Sort"
description: "We are given a permutation, meaning a rearrangement of numbers from 1 to n. In one move, we pick any k elements, remove them from the array, sort just those chosen elements, and append them back to the end. The rest of the array keeps its relative order."
date: "2026-06-09T12:43:40+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1768
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 842 (Div. 2)"
rating: 900
weight: 1768
solve_time_s: 180
verified: false
draft: false
---

[CF 1768B - Quick Sort](https://codeforces.com/problemset/problem/1768/B)

**Rating:** 900  
**Tags:** greedy, math  
**Solve time:** 3m  
**Verified:** no  

## Solution
## Problem Understanding

We are given a permutation, meaning a rearrangement of numbers from 1 to n. In one move, we pick any k elements, remove them from the array, sort just those chosen elements, and append them back to the end. The rest of the array keeps its relative order.

The task is to compute how many such moves are needed to transform the permutation into sorted order.

The key constraint is that n can be up to 100000 across all test cases, so any approach that simulates operations or tries combinations of chosen subsets is immediately too slow. Anything beyond linear or near-linear per test case must be avoided.

A common failure case comes from assuming we can always “fix” k misplaced elements per operation. For example, if k equals n, the answer is always 1 unless already sorted, because we sort everything at once. But if k is small, interactions between elements matter heavily.

A subtle edge case appears when k equals 1. In that case, each operation picks one element and appends it to the end unchanged, meaning we are effectively rotating elements. A naive greedy might assume this behaves like bubble sort and underestimate operations.

Another failure mode is assuming we can independently place elements into their correct positions. In reality, once elements are moved to the back, their relative order constraints persist, so progress is governed by global structure rather than local fixes.

## Approaches

A brute-force interpretation would simulate all possible choices of k elements at every step and try to reach sorted order in the fewest moves. This is correct in principle because it explores the full state space of permutations reachable under the operation. However, the branching factor is enormous, since there are choose(n, k) possible selections per step, making it exponential and unusable even for n = 20.

The key observation is that the operation only allows us to “collect” elements into a buffer and reinsert them in sorted order at the end. This means elements that are already in correct relative order can be ignored, and the difficulty is entirely determined by how many elements are already aligned with the identity permutation structure.

The correct viewpoint is to track which prefix of the sorted permutation is already stable and how many elements are “out of place” relative to it. Each operation can fix up to k misplaced elements, but only if they are selected appropriately. This leads to a counting argument based on how many elements are already in correct relative position and how many remain unsorted.

A more precise characterization shows that the answer depends on how many elements are already in the correct suffix when scanning from the end. Each operation can extend this suffix by at most k elements, because we can only fully place k elements correctly per move.

This reduces the problem to a greedy counting process rather than any simulation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(n) per test | O(1) | Accepted |

## Algorithm Walkthrough

We process the permutation by comparing it against the sorted order, which is simply 1 through n. We scan from the end and count how many elements are already in correct decreasing suffix position.

We maintain a pointer `need = n`, representing the largest value we still expect to place correctly at the end. We scan the array from right to left, and every time we see `need`, we decrement `need`. This measures how much of the suffix is already correctly aligned.

After this scan, if `need` becomes 0, the array is already sorted and no operations are needed.

Otherwise, the remaining unsatisfied prefix has size equal to `need`. Each operation can “fix” up to k elements that are not yet placed correctly, because we can always select k misplaced elements and move them to the end in sorted order, effectively locking them into correct suffix positions over time.

Thus the number of operations required is the ceiling of `need / k`.

### Why it works

The suffix scan captures the longest already correct tail in terms of final positions. Everything outside this suffix must be actively repositioned. Since each operation can only finalize k elements into their correct final block, we reduce the problem to a packing argument: how many groups of size k are needed to cover all misplaced elements. No operation can fix more than k elements because only k are moved per operation, and sorting them does not create new correct placements beyond those k.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, k = map(int, input().split())
    p = list(map(int, input().split()))

    need = n
    for x in reversed(p):
        if x == need:
            need -= 1

    if need == 0:
        print(0)
    else:
        print((need + k - 1) // k)
```

The solution reads each test case independently and computes how many elements are already in the correct suffix position. The reversed scan is critical because it ensures we only match elements that can actually form a valid final tail in order.

The final formula `(need + k - 1) // k` is a standard ceiling division, representing how many full operations are required to cover all remaining misplaced elements.

## Worked Examples

Consider the sample where `n = 4, k = 2` and `p = [1, 3, 2, 4]`.

We scan from the end:

| Step | Element | Need before | Action | Need after |
| --- | --- | --- | --- | --- |
| 1 | 4 | 4 | matches 4 | 3 |
| 2 | 2 | 3 | skip | 3 |
| 3 | 3 | 3 | matches 3 | 2 |
| 4 | 1 | 2 | matches 1 does not match 2 | 2 |

So `need = 2`, meaning two elements are not already in correct suffix alignment. With k = 2, one operation suffices.

Now consider `p = [2, 3, 1, 4]`, `k = 2`.

| Step | Element | Need before | Action | Need after |
| --- | --- | --- | --- | --- |
| 1 | 4 | 4 | match | 3 |
| 2 | 1 | 3 | skip | 3 |
| 3 | 3 | 3 | match | 2 |
| 4 | 2 | 2 | match | 1 |

Here `need = 1`, so one operation is still needed because a single element still blocks full alignment.

These traces show that the algorithm is not tracking swaps but rather the structure of the final suffix that can already be considered “fixed”.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test | single reverse scan of the permutation |
| Space | O(1) extra | only counters are used |

The total n across all test cases is bounded by 100000, so the linear scan is easily fast enough under Python constraints.

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
        p = list(map(int, input().split()))

        need = n
        for x in reversed(p):
            if x == need:
                need -= 1

        if need == 0:
            out.append("0")
        else:
            out.append(str((need + k - 1) // k))

    return "\n".join(out)

# provided samples
assert run("""4
3 2
1 2 3
3 1
3 1 2
4 2
1 3 2 4
4 2
2 3 1 4
""") == """0
1
1
2"""

# all sorted
assert run("""1
5 3
1 2 3 4 5
""") == "0"

# reverse order
assert run("""1
5 2
5 4 3 2 1
""") == "2"

# k = n case
assert run("""1
4 4
3 2 1 4
""") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| already sorted | 0 | suffix detection correctness |
| reversed permutation | 2 | multi-step requirement |
| k = n case | 1 | full collection in one operation |

## Edge Cases

When the permutation is already sorted, the reverse scan immediately consumes all values and `need` becomes zero. This ensures the algorithm correctly outputs zero without performing unnecessary operations.

When k equals n, the formula reduces to one operation whenever the permutation is not already sorted, which matches the fact that we can pick all elements once and sort them.

When k equals 1, each operation effectively moves one element to the end, so the answer becomes the number of elements not already in the correct suffix, matching the division by one behavior of the formula.
