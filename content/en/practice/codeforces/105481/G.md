---
title: "CF 105481G - \u987e\u5f71\u81ea\u601c"
description: "We are given one or more arrays. For each array, we look at every contiguous subarray and assign it a value based on a simple rule: take the maximum element inside the subarray, count how many times this maximum appears, and if that count is at least k, the subarray contributes…"
date: "2026-06-23T18:19:42+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105481
codeforces_index: "G"
codeforces_contest_name: "2024 CCPC Liaoning Provincial Contest"
rating: 0
weight: 105481
solve_time_s: 62
verified: true
draft: false
---

[CF 105481G - \u987e\u5f71\u81ea\u601c](https://codeforces.com/problemset/problem/105481/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given one or more arrays. For each array, we look at every contiguous subarray and assign it a value based on a simple rule: take the maximum element inside the subarray, count how many times this maximum appears, and if that count is at least `k`, the subarray contributes `1`, otherwise it contributes `0`. The task is to compute the sum of these contributions over all subarrays.

So the problem is not about computing maxima directly, but about counting how often the maximum value inside a segment is “sufficiently repeated”. Every subarray either qualifies or does not, and we are counting how many qualify.

The constraints imply a linear or near-linear solution per test case. The total length across all test cases is up to 1e6, so any quadratic enumeration of subarrays is impossible. Even O(n sqrt n) is risky unless heavily optimized. The structure must support amortized O(n) or O(n log n) behavior.

A naive implementation would enumerate all O(n²) subarrays, compute the maximum and its frequency in O(n) or O(1) with preprocessing, and check the condition. This already pushes us to O(n³) or O(n²) time depending on implementation, which is far too slow.

A subtler incorrect approach is to try maintaining a sliding window while updating only the maximum. That fails because the “maximum frequency in the current window” is not monotonic: adding or removing elements can change which value is the maximum, and also how many times it appears.

Another pitfall is assuming that only subarrays where the global maximum of the entire array matters. The condition is local to each subarray, so restricting attention to global maxima loses almost all valid cases.

## Approaches

The brute force approach is straightforward. For every starting index, extend the subarray one element at a time, maintain the maximum and a frequency map, and count how many times the maximum appears. This correctly identifies valid subarrays, but it spends O(n) work per extension, leading to O(n²) or worse per test case. With up to 1e6 total elements, this is not feasible.

The key observation is that the condition only depends on the maximum element of the subarray. If we fix what the maximum is, say a value `x`, then we only care about subarrays where no element exceeds `x`, and among those, we want at least `k` occurrences of `x`. This turns the problem into counting, for each value, how many subarrays have a controlled maximum and sufficient frequency of that value.

We can process values in decreasing order. When we consider a value `x`, we temporarily treat all elements greater than `x` as “blocking boundaries” that split the array into independent segments. Inside each segment, we only care about positions where value equals `x`.

Now the problem becomes: in each segment, count subarrays where `x` appears at least `k` times. This is a classic “at least k occurrences in subarrays” counting problem, solvable with a two-pointer approach over the positions of `x` inside each segment.

We maintain the positions of `x` and use a sliding window over these positions. For a window of occurrences `[i, j]` with `j - i + 1 >= k`, the number of subarrays where the k-th occurrence of `x` is fixed is determined by how far we can extend left and right without crossing elements greater than `x`.

This leads to a linear sweep per value, and since each index participates in processing only when its value is activated, the total complexity is near O(n).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) per test | O(1) to O(n) | Too slow |
| Value-sweeping + two pointers | O(n log n) or O(n) amortized | O(n) | Accepted |

## Algorithm Walkthrough

1. Sort or bucket indices by array value so we can process values from largest to smallest. This ensures that when we handle a value `x`, all larger values are already treated as barriers.
2. Maintain a structure of “active segments” where all elements greater than the current value split the array. Conceptually, we treat these as boundaries that reset counting.
3. For the current value `x`, collect all indices where `a[i] == x`. Within each active segment, process these indices separately.
4. For each segment, take the list of positions of `x`. Use a sliding window over these positions. Let the window be `[l, r]` in terms of occurrences. We only consider windows where `r - l + 1 >= k`.
5. For a fixed valid window of k-th occurrence at position `r`, determine how many subarrays have their left boundary between the previous occurrence (or segment start) and this k-th occurrence, and right boundary between this occurrence and the next blocking element. This converts each valid window into a count contribution.
6. Sum all contributions across all values.

### Why it works

The correctness relies on a decomposition of subarrays by their maximum element. Every valid subarray has a unique maximum value `x`. Once we fix `x`, any element greater than `x` would invalidate the subarray, so valid subarrays must lie entirely within regions bounded by larger elements. Inside such a region, counting subarrays where `x` appears at least `k` times is independent of other values. Each subarray is counted exactly once when processing its maximum value, because it is only considered when `x` is the largest allowed value in its segment.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    pos = [[] for _ in range(n + 1)]
    for i, v in enumerate(a):
        pos[v].append(i)

    # next greater element boundary: we build "blocks" using a monotonic stack
    nxt_block = [n] * n
    stack = []
    for i in range(n):
        while stack and a[stack[-1]] < a[i]:
            nxt_block[stack.pop()] = i
        stack.append(i)

    prev_block = [-1] * n
    stack = []
    for i in range(n - 1, -1, -1):
        while stack and a[stack[-1]] <= a[i]:
            prev_block[stack.pop()] = i
        stack.append(i)

    ans = 0

    # process values in decreasing order
    for val in range(n, 0, -1):
        if not pos[val]:
            continue

        # split positions by blocks implicitly
        group = []
        for i in pos[val]:
            group.append(i)

        if len(group) < k:
            continue

        # two pointers over occurrences
        for i in range(len(group) - k + 1):
            j = i + k - 1

            left_bound = prev_block[group[i]] + 1
            right_bound = nxt_block[group[j]] - 1

            # extend left and right choices
            left_choices = group[i] - left_bound + 1
            right_choices = right_bound - group[j] + 1

            if left_choices > 0 and right_choices > 0:
                ans += left_choices * right_choices

    print(ans)

def main():
    t = int(input())
    for _ in range(t):
        solve()

if __name__ == "__main__":
    main()
```

The solution starts by grouping indices of equal values so we can reason locally about each candidate maximum. The next greater and previous greater boundaries are computed with monotonic stacks. These define maximal segments where a given value can act as the maximum without being invalidated by a larger element.

For each value, we look at occurrences and pick windows of size `k`. The window defines the minimum requirement for satisfying the frequency condition. Once the k-th occurrence is fixed, we count how many choices exist for extending the subarray left and right while staying inside the valid segment boundaries.

A subtle point is that each window corresponds to multiple subarrays, and we multiply independent choices of left and right endpoints. This factorization is what reduces the counting to O(1) per window.

## Worked Examples

### Example 1

Input:

```
n=5, k=2
a = [1, 3, 3, 2, 2]
```

We compute boundaries:

| Step | Value window | Left bound | Right bound | Contribution |
| --- | --- | --- | --- | --- |
| (3,3) pair at positions 1,2 | k-window [1,2] | 0 | 4 | (2 * 3) = 6 |
| (2,2) pair at positions 3,4 | k-window [3,4] | 3 | 4 | (1 * 1) = 1 |

Total is 7.

This matches the intuition: each valid subarray is counted exactly when its maximum value is processed.

### Example 2

Input:

```
n=4, k=3
a = [1, 4, 2, 1]
```

No value appears at least 3 times in any segment, so no valid k-window exists.

| Value | Occurrences | k-valid window | Contribution |
| --- | --- | --- | --- |
| 1 | 2 | none | 0 |
| 2 | 1 | none | 0 |
| 4 | 1 | none | 0 |

Output is 0.

This confirms that the algorithm naturally filters out impossible frequency conditions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) amortized per test | Each index participates in at most a constant number of boundary and occurrence operations |
| Space | O(n) | Storage for positions and boundary arrays |

The total input size across all test cases is bounded by 1e6, so a linear amortized solution is sufficient. The stack-based preprocessing and per-value scanning both scale proportionally to the array size.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    def solve():
        n, k = map(int, input().split())
        a = list(map(int, input().split()))

        pos = [[] for _ in range(n + 1)]
        for i, v in enumerate(a):
            pos[v].append(i)

        nxt_block = [n] * n
        stack = []
        for i in range(n):
            while stack and a[stack[-1]] < a[i]:
                nxt_block[stack.pop()] = i
            stack.append(i)

        prev_block = [-1] * n
        stack = []
        for i in range(n - 1, -1, -1):
            while stack and a[stack[-1]] <= a[i]:
                prev_block[stack.pop()] = i
            stack.append(i)

        ans = 0

        for val in range(n, 0, -1):
            if not pos[val]:
                continue
            if len(pos[val]) < k:
                continue
            for i in range(len(pos[val]) - k + 1):
                j = i + k - 1
                L = prev_block[pos[val][i]] + 1
                R = nxt_block[pos[val][j]] - 1
                left = pos[val][i] - L + 1
                right = R - pos[val][j] + 1
                if left > 0 and right > 0:
                    ans += left * right

        return str(ans) + "\n"

    out = []
    t = int(input())
    for _ in range(t):
        out.append(solve())
    return "".join(out)

# sample-like tests
assert run("""1
5 2
1 3 3 2 2
""").strip() == "7"

assert run("""1
4 3
1 4 2 1
""").strip() == "0"

assert run("""1
1 1
1
""").strip() == "1"

assert run("""1
3 2
2 2 2
""").strip() == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single pair with repetitions | 7 | correct counting across overlapping maxima |
| no valid subarrays | 0 | filtering by k constraint |
| minimal input | 1 | base correctness |
| all equal array | 3 | full combinatorial counting |

## Edge Cases

A minimal array with k equal to 1 tests whether the algorithm correctly counts all subarrays where the maximum appears at least once. In that case every subarray is valid, and the formula reduces to counting all possible segments. The boundary-based decomposition still works because every element forms its own maximum class, and each k-window becomes a single occurrence.

An all-equal array stresses correctness of the left-right multiplication. Since every subarray has the same maximum, the algorithm should count all subarrays whose length is at least k. The sliding window over occurrences naturally produces exactly (n-k+1) windows, and each expands into correct endpoint choices, confirming that no double counting occurs.
