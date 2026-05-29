---
title: "CF 252A - Little Xor"
description: "We are given a sequence of non-negative integers and we want to pick a contiguous block of elements such that when we take the bitwise XOR of everything inside that block, the result is as large as possible."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation"]
categories: ["algorithms"]
codeforces_contest: 252
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 153 (Div. 2)"
rating: 1100
weight: 252
solve_time_s: 81
verified: false
draft: false
---

[CF 252A - Little Xor](https://codeforces.com/problemset/problem/252/A)

**Rating:** 1100  
**Tags:** brute force, implementation  
**Solve time:** 1m 21s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a sequence of non-negative integers and we want to pick a contiguous block of elements such that when we take the bitwise XOR of everything inside that block, the result is as large as possible. The task is to return that maximum achievable XOR over all possible subarrays.

The input size is small, with at most 100 elements, and each value fits within 30 bits. This immediately tells us that even cubic or quadratic solutions are acceptable, because the total number of subarrays is bounded by roughly 5,000 and each XOR computation can be done in constant time if we preprocess prefix XORs.

The structure of XOR over segments has one subtle property that often causes mistakes: XOR is not monotonic, so extending a segment can increase or decrease the result unpredictably. This rules out greedy strategies that try to extend a single best window.

A common incorrect attempt is to maintain a running window and adjust endpoints greedily. For example, in an array like `[1, 2, 3, 0]`, a greedy extension might pick `[1, 2] = 3`, then adding `3` gives `0`, which looks worse and might be prematurely discarded. But later segments like `[2, 3] = 1` or `[1, 2, 3] = 0` show that local decisions do not reflect global optimality.

Another pitfall is recomputing XOR of each segment from scratch in O(n) time, leading to O(n^3) behavior. While still technically fine for n = 100, it is unnecessary and hides a simpler structure.

## Approaches

The brute-force idea is straightforward: try every pair of endpoints (l, r), compute XOR of that segment, and track the maximum. There are O(n^2) segments, and each XOR computation can be done in O(n) if done naively, giving O(n^3). This works because n is small, but it repeats work heavily.

The key observation is that XOR over a segment can be computed in O(1) using prefix XORs. If we define prefix[i] as XOR of elements from index 0 to i, then the XOR of a segment [l, r] is simply prefix[r] XOR prefix[l - 1]. This reduces the inner computation cost and removes redundancy.

Once this is available, we can evaluate all subarrays in O(1) each, making the whole scan O(n^2). With n ≤ 100, this is more than sufficient.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (recompute each segment) | O(n^3) | O(1) | Accepted but inefficient |
| Prefix XOR + enumeration | O(n^2) | O(n) | Accepted |

## Algorithm Walkthrough

1. Build a prefix XOR array where each position stores XOR of all elements up to that index. This allows constant-time segment queries.
2. Iterate over all possible left endpoints of a segment. Each index becomes a candidate start of a subarray.
3. For each start index, iterate over all possible right endpoints from that start to the end of the array. This enumerates every contiguous segment exactly once.
4. For each pair (l, r), compute XOR of the segment using prefix values. This avoids recomputing XOR from scratch and keeps each evaluation O(1).
5. Maintain a variable tracking the maximum XOR seen so far and update it after evaluating each segment.

### Why it works

The algorithm evaluates every possible contiguous segment exactly once, and computes its XOR correctly using the identity that prefix XOR cancels shared prefixes. Since XOR is associative and self-inverse, prefix cancellation guarantees correctness of segment extraction. Because all segments are checked, the maximum found must be the global maximum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    prefix = [0] * n
    prefix[0] = a[0]
    for i in range(1, n):
        prefix[i] = prefix[i - 1] ^ a[i]

    ans = 0

    for l in range(n):
        for r in range(l, n):
            if l == 0:
                cur = prefix[r]
            else:
                cur = prefix[r] ^ prefix[l - 1]
            if cur > ans:
                ans = cur

    print(ans)

if __name__ == "__main__":
    solve()
```

The solution begins by constructing prefix XOR values so that any segment query becomes a constant-time operation. The nested loops then enumerate all possible segments. The conditional branch inside handles the boundary case where the segment starts at index 0, since there is no prefix to subtract.

The comparison `cur > ans` is safe because all values are non-negative integers, so initializing `ans = 0` correctly captures the minimum possible answer.

## Worked Examples

### Example 1

Input:

```
5
1 2 1 1 2
```

We compute prefix XOR:

| i | a[i] | prefix[i] |
| --- | --- | --- |
| 0 | 1 | 1 |
| 1 | 2 | 3 |
| 2 | 1 | 2 |
| 3 | 1 | 3 |
| 4 | 2 | 1 |

Now we evaluate segments:

| l | r | XOR |
| --- | --- | --- |
| 0 | 0 | 1 |
| 0 | 1 | 3 |
| 1 | 2 | 3 |
| 2 | 4 | 2 |

The maximum observed value is 3, which matches the expected result.

This trace shows how different segments can produce the same optimal value, and why exhaustive checking is required.

### Example 2

Input:

```
1
7
```

| l | r | XOR |
| --- | --- | --- |
| 0 | 0 | 7 |

The only possible segment is the array itself, so the answer is trivially 7. This confirms that the algorithm correctly handles minimal input sizes without special casing beyond prefix initialization.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2) | two nested loops over all subarrays, each XOR computed in O(1) |
| Space | O(n) | prefix XOR array |

With n ≤ 100, the algorithm performs at most 10,000 segment evaluations, each constant time. This is comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import sys

    n = int(sys.stdin.readline())
    a = list(map(int, sys.stdin.readline().split()))

    prefix = [0] * n
    prefix[0] = a[0]
    for i in range(1, n):
        prefix[i] = prefix[i - 1] ^ a[i]

    ans = 0
    for l in range(n):
        for r in range(l, n):
            cur = prefix[r] if l == 0 else (prefix[r] ^ prefix[l - 1])
            ans = max(ans, cur)
    return str(ans)

# provided sample
assert run("5\n1 2 1 1 2\n") == "3"

# custom cases
assert run("1\n0\n") == "0", "single zero"
assert run("2\n5 5\n") == "5", "equal elements XOR cancels"
assert run("3\n1 2 4\n") == "7", "full range best"
assert run("4\n8 1 2 3\n") == "11", "mixed bits"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 0` | 0 | minimum size, zero handling |
| `2 5 5` | 5 | XOR cancellation behavior |
| `1 2 4` | 7 | full segment optimality |
| `8 1 2 3` | 11 | non-trivial mixed structure |

## Edge Cases

For a single-element array like `[0]`, the prefix array is `[0]`, and the only segment evaluated is `(0, 0)`, producing XOR `0`. The algorithm correctly returns `0` without requiring special handling.

For repeated identical elements such as `[5, 5]`, prefix values become `[5, 0]`. The segment `[0, 1]` yields `5 XOR 5 = 0`, while single-element segments yield `5`. The algorithm correctly identifies that the best choice is any single element.

For alternating patterns like `[1, 2, 3]`, prefix values are `[1, 3, 0]`. The segment `[0, 2]` yields `0`, while `[0, 1]` yields `3` and `[1, 2]` yields `1`. The algorithm correctly explores all candidates and selects `3`, showing that optimal segments are not necessarily the longest ones.
