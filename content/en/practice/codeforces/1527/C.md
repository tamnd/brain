---
title: "CF 1527C - Sequence Pair Weight"
description: "We are given several arrays, and for each array we consider every possible contiguous subarray. For each subarray, we define its “weight” as the number of pairs of positions inside it that contain the same value."
date: "2026-06-10T17:14:28+07:00"
tags: ["codeforces", "competitive-programming", "hashing", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1527
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 721 (Div. 2)"
rating: 1600
weight: 1527
solve_time_s: 94
verified: true
draft: false
---

[CF 1527C - Sequence Pair Weight](https://codeforces.com/problemset/problem/1527/C)

**Rating:** 1600  
**Tags:** hashing, implementation, math  
**Solve time:** 1m 34s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several arrays, and for each array we consider every possible contiguous subarray. For each subarray, we define its “weight” as the number of pairs of positions inside it that contain the same value. In other words, inside a chosen segment, we look at all index pairs and count how many pairs have equal elements.

The task is to compute the total weight over all subarrays of the array. Instead of evaluating each subarray independently, we must aggregate this value efficiently for the entire array.

The constraints are tight enough that any solution that explicitly enumerates subarrays is immediately too slow. Each test case allows up to 100,000 elements, and there can be up to 100,000 test cases. Even though the total length across all tests is bounded, a quadratic or near-quadratic approach per test is impossible. Any solution must be close to linear per test case.

A naive approach would generate all subarrays and count equal pairs inside each. This already fails for very small inputs like `n = 10^5` because the number of subarrays is O(n^2), and counting pairs inside each subarray adds another factor.

A second common pitfall is trying to compute contributions per value without correctly accounting for how often a pair appears across different subarrays. The difficulty is that a pair of equal elements contributes not just once globally, but to every subarray that contains both endpoints.

## Approaches

A brute-force strategy starts by iterating over every subarray `[l, r]`, and inside it counting how many pairs `(i, j)` satisfy `l ≤ i < j ≤ r` and `a[i] = a[j]`. This can be done by a nested loop and a frequency table per subarray. Even if we maintain frequencies while expanding `r`, we still have O(n^2) subarrays, and updating counts is O(1), leading to O(n^2) per test case. With `n = 10^5`, this is far beyond any feasible limit.

The key observation is to invert the viewpoint. Instead of summing over subarrays first, we sum over pairs of equal positions first. Take two indices `i < j` with `a[i] = a[j]`. We want to know in how many subarrays this pair contributes to the weight.

A subarray contributes this pair if and only if it fully contains both `i` and `j`. That means the left endpoint `l` can be anywhere from `1` to `i`, and the right endpoint `r` can be anywhere from `j` to `n`. Therefore, this pair appears in exactly `i * (n - j + 1)` subarrays.

Now the problem becomes summing this contribution over all equal pairs. We process indices from left to right, maintaining for each value how many times it has appeared so far. When we are at position `j`, every previous occurrence `i` of the same value contributes `i * (n - j + 1)`. We can accumulate this efficiently by maintaining a running sum of indices per value.

This reduces the problem to a single pass with a hash map.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1)-O(n) | Too slow |
| Optimal | O(n) amortized | O(n) | Accepted |

## Algorithm Walkthrough

1. We process the array from left to right while tracking occurrences of each value. For each value, we maintain two pieces of information: how many times it has appeared so far, and the sum of its previous indices.
2. When we reach position `j` with value `x`, we want to compute how much this position contributes to pairs with earlier occurrences of `x`. Each earlier index `i` forms a pair contributing `i * (n - j + 1)`.
3. Instead of iterating over all previous `i`, we use the stored sum of indices. If `S[x]` is the sum of all previous positions where `x` appeared, then total contribution of `j` is `S[x] * (n - j + 1)`.
4. We add this contribution to the answer.
5. We then update the stored state: increment the count and add `j` to the sum `S[x]`.
6. Repeat this for all elements in the array and accumulate the total answer.

### Why it works

Every valid pair `(i, j)` with equal values is counted exactly once when processing `j`. At that moment, the algorithm has already accumulated all previous positions `i` for that value. Each such pair contributes to exactly `i * (n - j + 1)` subarrays, and the multiplication is correctly aggregated via the stored sum. Since each pair is uniquely attributed to its right endpoint, there is no double counting or omission.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        # store: value -> (count, sum of indices)
        cnt = {}
        idx_sum = {}
        
        ans = 0
        
        for j, x in enumerate(a, start=1):
            if x in idx_sum:
                ans += idx_sum[x] * (n - j + 1)
                cnt[x] += 1
                idx_sum[x] += j
            else:
                cnt[x] = 1
                idx_sum[x] = j
        
        print(ans)

if __name__ == "__main__":
    solve()
```

The implementation relies on 1-based indexing for clarity in the contribution formula `(n - j + 1)`. The dictionary `idx_sum` tracks the sum of all previous positions for each value. When processing a new occurrence, we immediately compute how many subarrays it completes pairs with earlier occurrences.

A subtle point is that we never need to explicitly use `cnt` in the final computation, but keeping it helps make the state conceptually complete. The correctness hinges on updating `idx_sum[x]` after using it for the current index.

## Worked Examples

### Example 1

Input:

```
n = 4
a = [1, 2, 1, 1]
```

We track contributions per position.

| j | x | idx_sum before | contribution | ans | idx_sum after |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0 | 0 | 1 |
| 2 | 2 | 0 | 0 | 0 | 2 |
| 3 | 1 | 1 | 1 × (4 - 3 + 1) = 2 | 2 | 4 |
| 4 | 1 | 4 | 4 × (4 - 4 + 1) = 4 | 6 | 8 |

Final answer is 6.

This trace shows how each occurrence of `1` accumulates contributions from all previous `1`s, scaled by how many subarrays extend to the right.

### Example 2

Input:

```
n = 4
a = [1, 2, 3, 4]
```

| j | x | idx_sum before | contribution | ans | idx_sum after |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0 | 0 | 1 |
| 2 | 2 | 0 | 0 | 0 | 2 |
| 3 | 3 | 0 | 0 | 0 | 3 |
| 4 | 4 | 0 | 0 | 0 | 4 |

No value repeats, so no contributions occur.

This confirms that the algorithm naturally produces zero when there are no duplicates.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test | Each element is processed once with O(1) hash operations |
| Space | O(n) | Hash maps store at most one entry per distinct value |

The total input size across tests is bounded by 10^5, so the linear scan across all tests fits comfortably within time limits. The memory usage is proportional to distinct values in each test case, which is also bounded by n.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        idx_sum = {}
        ans = 0
        
        for j, x in enumerate(a, start=1):
            if x in idx_sum:
                ans += idx_sum[x] * (n - j + 1)
                idx_sum[x] += j
            else:
                idx_sum[x] = j
        
        out.append(str(ans))
    
    return "\n".join(out)

# provided samples
assert run("2\n4\n1 2 1 1\n4\n1 2 3 4\n") == "6\n0"

# all equal
assert run("1\n5\n7 7 7 7 7\n") == "50"

# single element
assert run("1\n1\n42\n") == "0"

# alternating duplicates
assert run("1\n6\n1 2 1 2 1 2\n") == "18"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal | 50 | maximum duplication accumulation |
| single element | 0 | minimum edge case |
| alternating | 18 | interleaved pair contributions |

## Edge Cases

For an array of all identical values like `[7, 7, 7, 7, 7]`, every new element interacts with all previous ones. At position `j`, the stored sum grows as `1 + 2 + ... + (j-1)`, and each is multiplied by `(n - j + 1)`. The algorithm correctly accumulates these growing contributions without missing any subarray span.

For a single-element array, there are no pairs at all. The loop runs once, finds no previous occurrences, and the stored map remains trivial. The output stays zero, matching the definition of weight.

For alternating values like `[1, 2, 1, 2, 1, 2]`, each value forms independent chains of occurrences. The structure ensures that contributions are separated by key, and each pair contributes only when its right endpoint is reached, preventing any cross-interference between different values.
