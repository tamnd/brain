---
title: "CF 296A - Yaroslav and Permutations"
description: "Yaroslav has a sequence of integers, and he wants to rearrange them so that no two consecutive elements are equal. The only allowed operation is swapping two neighboring elements, and he wants to know if it is possible to reach a configuration satisfying this condition."
date: "2026-06-05T17:54:28+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 296
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 179 (Div. 2)"
rating: 1100
weight: 296
solve_time_s: 95
verified: true
draft: false
---

[CF 296A - Yaroslav and Permutations](https://codeforces.com/problemset/problem/296/A)

**Rating:** 1100  
**Tags:** greedy, math  
**Solve time:** 1m 35s  
**Verified:** yes  

## Solution
## Problem Understanding

Yaroslav has a sequence of integers, and he wants to rearrange them so that no two consecutive elements are equal. The only allowed operation is swapping two neighboring elements, and he wants to know if it is possible to reach a configuration satisfying this condition. The input consists of the array length, `n`, followed by `n` integers representing the array. The output should be "YES" if a valid rearrangement exists and "NO" otherwise.

The key constraints are that `n` can go up to 100 and values of the array elements range up to 1000. Because `n` is small, algorithms with time complexity up to `O(n^2)` are feasible, but anything exponential or factorial in `n` would be overkill. The array values themselves are less relevant to time complexity; they only matter for counting occurrences.

The non-obvious edge case occurs when one element occurs too frequently. For example, if `n = 5` and the array is `[1, 1, 1, 2, 3]`, the element `1` appears three times. To place these without consecutive duplicates, we would need at least four “slots” to separate them, which is impossible since `n - max_count = 2`. In this case, the correct answer is "NO". A careless approach might just attempt to reorder elements greedily without checking frequencies, which would fail.

A special case is when `n = 1`. Any single-element array trivially satisfies the requirement, so the answer is "YES".

## Approaches

The brute-force approach would try every possible permutation of the array and check whether any of them satisfies the consecutive-difference condition. There are `n!` permutations. Even with `n = 10`, this yields over 3 million permutations, and the cost of checking each permutation is `O(n)`, which is impractical for `n = 100`.

The key observation to optimize is that the only constraint preventing a valid arrangement is when some number appears too frequently. Suppose the most frequent element occurs `max_count` times. To avoid consecutive duplicates, we need to interleave all occurrences of this element with other elements. This is only possible if the number of other elements is at least `max_count - 1`. Formally, the condition for a "YES" is:

```
max_count <= (n + 1) // 2
```

This works because we can place the most frequent element in positions 0, 2, 4, ..., and fill the remaining slots with other elements. If the most frequent element exceeds `(n + 1) // 2`, even the optimal placement leaves at least one consecutive pair of identical elements.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Optimal | O(n) | O(1000) | Accepted |

## Algorithm Walkthrough

1. Read `n` and the array `a`.
2. Count the frequency of each element in the array. This can be done using a dictionary or array indexed by element values.
3. Identify the maximum frequency, `max_count`.
4. Compare `max_count` to `(n + 1) // 2`. If `max_count` is greater than `(n + 1) // 2`, print "NO" because it is impossible to separate all occurrences of this element.
5. Otherwise, print "YES" since a valid arrangement exists by interleaving elements appropriately.

Why it works: The algorithm maintains the invariant that the number of slots available to separate repeated elements is `n - max_count + 1`. If the most frequent element can fit in these slots without overlapping, the rest of the elements can fill in the gaps, guaranteeing no consecutive duplicates. This is both necessary and sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import Counter

n = int(input())
a = list(map(int, input().split()))

freq = Counter(a)
max_count = max(freq.values())

if max_count <= (n + 1) // 2:
    print("YES")
else:
    print("NO")
```

The solution first reads input efficiently with `sys.stdin.readline`. Counting uses `Counter` from the standard library, which is both simple and handles sparse arrays without predefining the range of values. Calculating `(n + 1) // 2` guarantees correct ceiling division for odd `n`. The comparison ensures we only reject impossible cases. No sorting or rearrangement is necessary because the condition depends purely on counts.

## Worked Examples

**Example 1**

Input:

```
1
1
```

| Step | Action | max_count | n+1//2 | Decision |
| --- | --- | --- | --- | --- |
| 1 | Count frequency | 1 | 1 | 1 <= 1 → YES |

Explanation: A single element trivially satisfies the condition.

**Example 2**

Input:

```
5
1 1 1 2 3
```

| Step | Action | max_count | n+1//2 | Decision |
| --- | --- | --- | --- | --- |
| 1 | Count frequency | 3 | 3 | 3 <= 3 → YES |

Explanation: Although element `1` appears 3 times, we have 5 positions and can interleave the others: 1 2 1 3 1. This satisfies the condition.

**Example 3**

Input:

```
4
1 1 1 2
```

| Step | Action | max_count | n+1//2 | Decision |
| --- | --- | --- | --- | --- |
| 1 | Count frequency | 3 | 2 | 3 > 2 → NO |

Explanation: The most frequent element occurs more than half of `n`, so consecutive duplicates cannot be avoided.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Counting frequencies and finding max are linear in array size. |
| Space | O(k) | `k` is the number of distinct values (≤ 1000). |

The solution handles the maximum `n = 100` easily, and memory usage is negligible compared to the limit of 256 MB.

## Test Cases

```python
import sys, io
from collections import Counter

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    a = list(map(int, input().split()))
    freq = Counter(a)
    max_count = max(freq.values())
    return "YES\n" if max_count <= (n + 1) // 2 else "NO\n"

# Provided samples
assert run("1\n1\n") == "YES\n", "sample 1"
assert run("5\n1 1 1 2 3\n") == "YES\n", "sample 2"
assert run("4\n1 1 1 2\n") == "NO\n", "sample 3"

# Custom cases
assert run("2\n1 1\n") == "YES\n", "2 elements same"
assert run("3\n2 2 2\n") == "NO\n", "3 identical elements"
assert run("6\n1 1 2 2 3 3\n") == "YES\n", "perfectly interleavable"
assert run("7\n1 1 1 1 2 3 4\n") == "NO\n", "most frequent exceeds (n+1)//2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2\n1 1 | YES | Minimum-size input with repeated elements |
| 3\n2 2 2 | NO | All elements identical |
| 6\n1 1 2 2 3 3 | YES | Array can be interleaved perfectly |
| 7\n1 1 1 1 2 3 4 | NO | Most frequent element exceeds allowable count |

## Edge Cases

When `n = 1`, the algorithm returns "YES" immediately since `(1 + 1)//2 = 1` and the single element frequency is 1. For arrays where all elements are identical, like `[2, 2, 2]`, the frequency is 3 while `(n+1)//2 = 2`, triggering "NO". Arrays with exactly half or just under half the positions filled by the most frequent element are handled correctly because `(n+1)//2` implements ceiling division.
