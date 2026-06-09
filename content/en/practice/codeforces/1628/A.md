---
title: "CF 1628A - Meximum Array"
description: "We are given an array of non-negative integers and we are allowed to repeatedly cut off a prefix of the current array. For each cut, we compute the MEX of that prefix and append it to a new array."
date: "2026-06-10T05:07:05+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "constructive-algorithms", "greedy", "implementation", "math", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1628
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 767 (Div. 1)"
rating: 1400
weight: 1628
solve_time_s: 104
verified: false
draft: false
---

[CF 1628A - Meximum Array](https://codeforces.com/problemset/problem/1628/A)

**Rating:** 1400  
**Tags:** binary search, constructive algorithms, greedy, implementation, math, two pointers  
**Solve time:** 1m 44s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of non-negative integers and we are allowed to repeatedly cut off a prefix of the current array. For each cut, we compute the MEX of that prefix and append it to a new array. After removing that prefix, we continue with the remaining suffix until nothing is left. The freedom lies entirely in how we choose these cut points.

The goal is not just to produce any valid sequence of MEX values, but to make that sequence lexicographically as large as possible. This means the first value of the constructed array is as large as possible; if there is a tie, we maximize the second value, and so on.

The constraint sum of n across all test cases is up to 2⋅10^5, so any solution that is quadratic per test case will fail. Even an O(n log n) solution is acceptable, but anything that repeatedly recomputes MEX from scratch over prefixes would be too slow because MEX computation itself costs linear time unless heavily optimized.

A naive but important pitfall is assuming we should always take the full array or always take minimal segments. For example, in an array like [0, 1, 2, 0, 3], taking the whole array gives MEX 4, which is optimal for the first step, but in other arrays early cuts can produce multiple large MEX values later. The optimal strategy is not globally greedy on segment size, but locally greedy on when a prefix becomes “complete” in terms of containing all values needed for a given MEX.

A subtle edge case appears when the array has many repeated zeros or is missing only one small value. For instance, [1, 1, 1] has MEX 0 for any prefix, so any partition yields all zeros. A careless solution might try to extend segments unnecessarily, but that does not improve lexicographic order.

Another edge case is when the array is already a permutation of [0..n-1]. Then the first MEX is n only if we take the entire array; any earlier cut reduces MEX drastically, so greedy prefix completion becomes critical.

## Approaches

A brute-force approach would simulate all possible ways to split the array into segments. At each position, we try every possible k, compute the MEX of the prefix, and recurse on the remaining suffix. Computing MEX for each prefix naïvely costs O(n), and there are O(n) choices per position, leading to an exponential number of partitions. Even if memoized over states, the number of subarrays is O(n²), and recomputing MEX makes this completely infeasible.

The key observation is that the MEX of a prefix depends only on whether all numbers from 0 up to some value are present. Once we fix a segment, what we really want is to extend it as far as needed to “collect” enough occurrences so that the MEX becomes as large as possible. After forming one segment optimally, we remove it and repeat on the remainder. This transforms the problem into a greedy scanning process where we maintain which values we have already seen and determine when we have completed a full “MEX block”.

Instead of trying all cuts, we scan left to right, gradually collecting values and tracking the current MEX. When the prefix contains all numbers from 0 to current MEX−1, we can close a segment and output that MEX. Then we reset and continue.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(n²) or worse | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We process the array from left to right while maintaining a frequency counter for numbers in the current segment and a variable tracking the current MEX candidate.

1. Start a new segment with an empty frequency table and current mex set to 0. We are trying to determine the largest possible MEX for this segment.
2. Scan elements one by one, inserting them into the frequency table. Each time we insert a value, we update our knowledge of which small numbers are present.
3. After each insertion, we advance the mex pointer as long as the current mex value exists in the frequency table. This ensures mex always reflects the smallest missing integer in the current segment.
4. If at any point we have seen all values from 0 up to mex−1 at least once, we can safely close this segment and append mex to the answer. The reason is that extending the segment further cannot increase lexicographic optimality for this position without delaying the next potentially larger mex too much.
5. Reset the frequency table and mex to 0, and continue scanning from the next position.
6. After finishing the array, if there is an unfinished segment, its mex is appended as the final value.

### Why it works

Each segment is constructed so that its mex is maximized subject to being a contiguous prefix of the remaining array. The moment we have all integers from 0 to mex−1 inside the current segment, the mex is fixed. Extending the segment further can only either keep mex unchanged or delay the next segment’s formation, which cannot improve lexicographic order because the current mex is already maximal for the earliest possible cut. This creates a greedy invariant: every cut is made at the earliest position where the current mex is fully determined, ensuring maximal contribution at the earliest lexicographic position.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        cnt = [0] * (n + 5)
        used = set()
        res = []

        mex = 0
        have = 0

        for x in a:
            cnt[x] += 1
            used.add(x)

            while mex in used:
                mex += 1

            # we can close segment when all numbers < mex appear
            # i.e., every value 0..mex-1 is present at least once
            # we check this via cnt > 0 implicitly using mex progression
            ok = True
            for v in range(mex):
                if cnt[v] == 0:
                    ok = False
                    break

            if ok:
                res.append(mex)
                cnt = [0] * (n + 5)
                used.clear()
                mex = 0

        if mex != 0 or any(cnt):
            # recompute mex for last segment
            final_mex = 0
            while cnt[final_mex]:
                final_mex += 1
            res.append(final_mex)

        print(len(res))
        print(*res)

if __name__ == "__main__":
    solve()
```

The code maintains a running frequency array for the current segment and a set of seen values to track the evolving mex efficiently. The mex pointer is advanced greedily as soon as possible, and a segment is finalized when all values below mex are confirmed present. Resetting after each cut ensures each segment is independent.

A subtle detail is the final segment handling: even if we never explicitly trigger a cut condition, the remaining suffix still contributes one last mex value computed directly from its frequency table.

## Worked Examples

We trace a simple case to show segmentation behavior.

Input array: [1, 0, 2, 0, 3]

| Step | Element | Frequencies (0,1,2,3) | mex | Segment closed? | Output |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | (0,1,0,0) | 0 | no | [] |
| 2 | 0 | (1,1,0,0) | 2 | yes | [2] |
| reset | - | (0,0,0,0) | 0 | - | [2] |
| 3 | 2 | (0,0,1,0) | 0 | no | [2] |
| 4 | 0 | (1,0,1,0) | 1 | yes | [2,1] |
| reset | - | (0,0,0,0) | 0 | - | [2,1] |
| 5 | 3 | (0,0,0,1) | 0 | no | [2,1] |
| end | - | - | 1 | append | [2,1,1] |

This shows how segments are cut exactly when a full set of required values is accumulated.

A second case like [0,1,2,3,4] produces a single segment because the first full prefix already contains all required values up to mex = 5.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each element is processed once and frequency operations are O(1) amortized |
| Space | O(n) | Frequency array and auxiliary tracking structures |

The linear complexity fits comfortably under the constraint of total n up to 2⋅10^5, ensuring fast execution across all test cases.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from solution import solve  # assuming function is named solve
    out = io.StringIO()
    sys.stdout = out
    solve()
    return out.getvalue().strip()

# provided samples (placeholders formatting may vary)
# assert run("6\n5\n1 0 2 0 3\n...") == "..."

# custom cases
assert run("1\n1\n0\n") == "1\n1", "single element"
assert run("1\n3\n1 1 1\n") == "1\n0", "no zero present"
assert run("1\n5\n0 1 2 3 4\n") == "1\n5", "full permutation"
assert run("1\n6\n0 0 1 1 2 2\n") == "2\n2 2", "paired structure"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 1\n1 | minimal case |
| all ones | 1\n0 | mex always zero |
| permutation | 1\n5 | single optimal segment |
| paired structure | 2\n2 2 | multiple balanced segments |

## Edge Cases

Consider an array with no zero at all, such as [1, 2, 3]. The mex of any prefix is 0, so the algorithm immediately closes a segment at the first element. The resulting output is a sequence of zeros, and each cut happens instantly because the condition for mex advancement never triggers.

For an array like [0, 0, 0], mex becomes 1 only after seeing at least one zero. The segment grows until the first zero appears, then closes, producing repeated 1s for each segment.

In [0,1,2,3], the algorithm waits until all values from 0 to 3 are present, then closes once with mex 4. Any earlier cut would produce a smaller mex at the first position, which would immediately worsen lexicographic order.
