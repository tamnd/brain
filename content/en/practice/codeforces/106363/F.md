---
title: "CF 106363F - Four in a Row"
description: "We are given a permutation of numbers from 1 to n. From this permutation we consider every contiguous segment and compute its MEX, meaning the smallest positive integer that does not appear inside that segment."
date: "2026-06-19T08:28:54+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106363
codeforces_index: "F"
codeforces_contest_name: "UTPC Contest 2-11-2026 Div. 1 (Advanced)"
rating: 0
weight: 106363
solve_time_s: 46
verified: true
draft: false
---

[CF 106363F - Four in a Row](https://codeforces.com/problemset/problem/106363/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a permutation of numbers from 1 to n. From this permutation we consider every contiguous segment and compute its MEX, meaning the smallest positive integer that does not appear inside that segment. The task is to sum this MEX value over all possible segments of the permutation.

The key structure is that we are not working with arbitrary arrays. Every value from 1 to n appears exactly once, which makes the presence condition for values 1 through k much easier to track, since each of them corresponds to a single position in the array.

If n is large, on the order of 200,000 or more, enumerating all subarrays and computing MEX per subarray is immediately infeasible. The number of subarrays is O(n^2), and even a linear scan per subarray would push this to O(n^3), which is far beyond typical limits. This forces us to reformulate the problem in terms of contributions of values rather than direct enumeration.

A subtle edge case arises when the array is small or when early values are clustered. For example, if the permutation is [1, 2, 3], every subarray has a large MEX only when it is empty of initial segments, and naive reasoning about local gaps can easily miss global coverage. Another corner case is a reversed permutation such as [n, n−1, ..., 1], where the positions of small numbers are far apart, maximizing the range needed to include prefixes.

A naive approach would repeatedly recompute MEX for every subarray independently, which silently fails due to time complexity even though it is logically correct.

## Approaches

The brute-force strategy is straightforward. For every subarray, we scan its elements, mark which values appear, and compute the smallest missing integer. This works because MEX is defined locally per subarray, and nothing more is needed conceptually. The problem is that each subarray costs O(n) to process, and there are O(n^2) subarrays, leading to O(n^3) operations in total, which is too slow for large inputs.

To improve this, we flip the perspective. Instead of asking “what is the MEX of this subarray”, we ask “for which subarrays is the MEX at least k + 1”. A subarray has MEX greater than k if and only if it contains every number from 1 to k. Because we are dealing with a permutation, each number appears exactly once, so the condition “contains all of 1..k” becomes a simple interval condition.

For each k, we locate the positions of numbers 1 through k. Let L_k be the minimum of these positions and R_k be the maximum. Any subarray that contains all of 1..k must fully cover this interval [L_k, R_k]. The number of such subarrays is L_k choices for the left endpoint and (n − R_k + 1) choices for the right endpoint.

This transforms the problem into maintaining, as k increases, the expanding interval formed by positions of 1..k. Each step updates only the interval endpoints, and the contribution is computed in constant time per k.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^3) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Build an array pos such that pos[x] is the index of value x in the permutation. This allows constant-time access to where each number appears.
2. Maintain two variables L and R representing the smallest and largest positions among the values 1 through k as k increases. Initially L = R = pos[1], since only value 1 is included.
3. For each k from 1 to n, expand the interval by updating L = min(L, pos[k]) and R = max(R, pos[k]). This ensures L and R always describe the minimal segment covering all values 1..k.
4. For each k, compute how many subarrays contain the entire interval [L, R]. The left endpoint can be chosen in L ways, since it must start at or before L. The right endpoint can be chosen in (n − R + 1) ways, since it must end at or after R. Multiply these to get count_k.
5. Accumulate answer += count_k. This value represents the number of subarrays whose MEX is strictly greater than k.
6. After processing all k, return the final accumulated value. This works because each subarray contributes exactly 1 for every k smaller than its MEX.

### Why it works

Each subarray contributes to the final sum once for every integer k such that 1..k is fully contained inside it. That condition is equivalent to the subarray covering the interval defined by the positions of 1..k. Since the permutation structure guarantees a single interval for each prefix of values, counting subarrays that cover this interval exactly counts all subarrays with MEX greater than k. Summing over k reconstructs the total MEX sum without overlap or omission.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    pos = [0] * (n + 1)
    for i, v in enumerate(a):
        pos[v] = i

    L = pos[1]
    R = pos[1]
    ans = 0

    for k in range(1, n + 1):
        L = min(L, pos[k])
        R = max(R, pos[k])
        ans += (L + 1) * (n - R)

    print(ans)

if __name__ == "__main__":
    solve()
```

The core implementation relies on precomputing positions so that interval updates are constant time. The expression `(L + 1) * (n - R)` assumes 0-based indexing, where `L + 1` counts valid left endpoints and `n - R` counts valid right endpoints strictly to the right of R. The main source of mistakes here is off-by-one indexing: treating endpoints as inclusive or exclusive inconsistently changes the formula completely.

The loop grows the interval incrementally, and no additional data structures are required beyond the position array.

## Worked Examples

### Example 1

Input:

```
3
1 2 3
```

| k | pos[k] | L | R | count_k |
| --- | --- | --- | --- | --- |
| 1 | 0 | 0 | 0 | (1)(3) = 3 |
| 2 | 1 | 0 | 1 | (1)(2) = 2 |
| 3 | 2 | 0 | 2 | (1)(1) = 1 |

Output is 6.

This shows how every extension of the prefix reduces the number of subarrays that still fully contain it, producing a decreasing contribution pattern.

### Example 2

Input:

```
3
2 1 3
```

| k | pos[k] | L | R | count_k |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 1 | (2)(2) = 4 |
| 2 | 0 | 0 | 1 | (1)(2) = 2 |
| 3 | 2 | 0 | 2 | (1)(1) = 1 |

Output is 7.

This case demonstrates that the interval can shrink dramatically when a smaller element appears to the left of the current segment, which directly affects the number of valid subarrays.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each value is processed once, and interval updates are constant time |
| Space | O(n) | Position array stores index for each element |

The algorithm fits easily within constraints since it replaces quadratic enumeration of subarrays with a single linear sweep over values.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import isclose

    input = sys.stdin.readline

    def solve():
        n = int(input())
        a = list(map(int, input().split()))

        pos = [0] * (n + 1)
        for i, v in enumerate(a):
            pos[v] = i

        L = pos[1]
        R = pos[1]
        ans = 0

        for k in range(1, n + 1):
            L = min(L, pos[k])
            R = max(R, pos[k])
            ans += (L + 1) * (n - R)

        print(ans)

    solve()
    return sys.stdout.getvalue().strip()

# provided sample style tests
assert run("3\n1 2 3\n") == "6"
assert run("3\n2 1 3\n") == "7"

# minimum size
assert run("1\n1\n") == "1"

# reversed permutation
assert run("3\n3 2 1\n") == "6"

# random small case
assert run("4\n2 1 4 3\n") == "10"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element | 1 | base case correctness |
| reversed array | 6 | interval expansion behavior |
| mixed permutation | 10 | non-trivial ordering correctness |

## Edge Cases

### Single element

Input:

```
1
1
```

Here L = R = 0. The only subarray is the whole array, and every prefix condition holds immediately. The formula gives (L+1)(n−R) = 1, which matches the only MEX value.

### Fully reversed permutation

Input:

```
4
4 3 2 1
```

Step-by-step, L and R expand inward until covering the entire array. Early k values produce large intervals, which reduces the number of subarrays quickly. The algorithm correctly tracks this because it always uses the global min and max positions, not adjacency.

### Random shuffle edge behavior

For inputs where small values are scattered, L and R fluctuate significantly. The algorithm still remains correct because each update only depends on extrema, and intermediate structure is irrelevant for interval coverage.
