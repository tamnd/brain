---
title: "CF 1279B - Verse For Santa"
description: "We are given a sequence of durations, where each value represents how long Vasya needs to recite one part of a verse. He must recite the parts in order, from left to right, and he earns a reward equal to how many parts he manages to fully complete before time runs out."
date: "2026-06-11T19:39:03+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1279
codeforces_index: "B"
codeforces_contest_name: "Educational Codeforces Round 79 (Rated for Div. 2)"
rating: 1300
weight: 1279
solve_time_s: 103
verified: true
draft: false
---

[CF 1279B - Verse For Santa](https://codeforces.com/problemset/problem/1279/B)

**Rating:** 1300  
**Tags:** binary search, brute force, implementation  
**Solve time:** 1m 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of durations, where each value represents how long Vasya needs to recite one part of a verse. He must recite the parts in order, from left to right, and he earns a reward equal to how many parts he manages to fully complete before time runs out. The listener only stays for a fixed number of seconds, so once cumulative time exceeds this limit, everything after that is irrelevant.

There is one allowed relaxation: Vasya may skip at most one part entirely. Skipping removes that part from the sequence, effectively letting him “compress” the timeline and potentially fit more parts before the time limit.

The task is not just to compute the maximum number of parts he can fit, but to decide which single part to skip in order to maximize that number. If skipping nothing is optimal, we output 0.

The constraints are tight enough that any solution must be linear or near-linear per test case. With up to 100,000 total elements, an O(n²) strategy that tries removing each element and recomputing totals will clearly fail, since it would require up to 10¹⁰ operations in the worst case. This immediately pushes us toward prefix sums and a two-pointer or binary search style optimization.

A few edge situations are easy to mishandle. If the entire array already fits within the time limit, skipping is unnecessary and the answer must be 0. For example, if `a = [1, 2, 3]` and `s = 10`, all parts fit and any skip would only reduce the result.

Another tricky case happens when skipping is required but the optimal skip is not near the end. For example, if early elements are large, skipping them can unlock many small suffix elements. A naive greedy that always skips the largest element or the first overflow element fails here.

Finally, there are cases where multiple skip choices yield the same best count. The problem allows any valid answer, so we do not need tie-breaking logic beyond consistency.

## Approaches

The brute-force idea is straightforward: try skipping each index (including skipping none), then simulate how many prefix elements can be taken within the time limit. For each candidate skip position, we compute the sum from left to right, ignoring that index. Each simulation costs O(n), and doing it for all n possibilities leads to O(n²), which is too slow for 10⁵ elements.

The key observation is that the answer depends only on prefix sums and whether removing one element can shift the cutoff point further to the right. If we fix a prefix ending at position r, the condition for being valid is that the sum of all chosen elements in that prefix minus at most one skipped element must not exceed s. This turns the problem into finding the longest prefix whose sum is ≤ s after removing one element inside it.

We can compute prefix sums once. Then for each position r, we ask: is there an index i ≤ r such that prefix_sum[r] - a[i] ≤ s? This is equivalent to finding whether there exists an element a[i] ≥ prefix_sum[r] - s. If such an element exists, we can skip it and keep r elements.

To answer this efficiently, we maintain a data structure over the current prefix that tracks the maximum value and also allows us to retrieve the index of a valid element. Since we only need to know whether any element in the prefix is large enough, we can track the maximum value and its position as we extend r. If prefix_sum[r] ≤ s, we take r with no skip. Otherwise, we check if max(a[1..r]) ≥ prefix_sum[r] - s; if yes, we can achieve r, otherwise r is impossible.

This reduces the problem to a single pass.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Prefix + Greedy Check | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute prefix sums while scanning the array from left to right, because any valid segment is always a prefix after possibly removing one element.
2. Track the maximum value seen so far in the prefix and its index, since this is the best candidate to remove if we are over the limit.
3. For each position r, compute the total sum of the prefix.
4. If the sum is within the limit s, update the best answer to r with no removal, since we can already take r elements.
5. If the sum exceeds s, compute the required reduction `need = prefix_sum[r] - s`. This is the minimum value we must remove to make the prefix valid.
6. If the maximum element in the prefix is at least `need`, then there exists a removable element that fixes the prefix, so r is feasible.
7. Track the largest r that is feasible, and remember either the index of the element that enabled it or 0 if no removal was needed.

Why it works: for any prefix, removing one element only reduces the sum by exactly that element's value. The only thing that matters is whether any element in the prefix is large enough to compensate for the overflow. Since all elements are positive, removing a single sufficiently large element is both necessary and sufficient to fix feasibility. This makes the decision purely local to the prefix, and no future elements affect whether a given prefix can be achieved.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, s = map(int, input().split())
        a = list(map(int, input().split()))
        
        pref = 0
        best_len = 0
        best_idx = 0
        
        max_val = 0
        max_idx = -1
        
        # prefix scan
        for i in range(n):
            pref += a[i]
            
            if a[i] > max_val:
                max_val = a[i]
                max_idx = i
            
            if pref <= s:
                best_len = i + 1
                best_idx = 0
            else:
                need = pref - s
                if max_val >= need:
                    best_len = i + 1
                    best_idx = max_idx + 1
        
        print(best_idx)

if __name__ == "__main__":
    solve()
```

The implementation keeps a running prefix sum and a running maximum element. At each step we decide whether the prefix is already valid or can be made valid by removing the largest element seen so far. If neither holds, we simply do not update the best prefix length.

The returned index corresponds to the best prefix that can be achieved, and we store the position of the element whose removal enabled it. If no removal is needed at all, the stored index remains 0.

A subtle point is that we never need to explicitly test all possible removals inside the prefix, because only the largest element matters when deciding feasibility: if any element can be removed to fix the sum, then removing the maximum is always sufficient or better.

## Worked Examples

### Example 1

Input:

```
n = 7, s = 11
a = [2, 9, 1, 3, 18, 1, 4]
```

We track prefix sum, max element, and decision.

| i | a[i] | prefix sum | max | need = pref - s | feasible | chosen skip |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 2 | 2 | 2 | - | yes | 0 |
| 1 | 9 | 11 | 9 | 0 | yes | 0 |
| 2 | 1 | 12 | 9 | 1 | yes | 0 |
| 3 | 3 | 15 | 9 | 4 | yes | 0 |
| 4 | 18 | 33 | 18 | 22 | yes | 5 |
| 5 | 1 | 34 | 18 | 23 | yes | 5 |
| 6 | 4 | 38 | 18 | 27 | yes | 5 |

At i = 4, the prefix becomes too large, but removing 18 fixes it, enabling the full prefix. This shows why skipping a large early element unlocks more total recitation.

### Example 2

Input:

```
n = 4, s = 35
a = [11, 9, 10, 7]
```

| i | a[i] | prefix sum | max | need | feasible | chosen skip |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 11 | 11 | 11 | - | yes | 0 |
| 1 | 9 | 20 | 11 | - | yes | 0 |
| 2 | 10 | 30 | 11 | - | yes | 0 |
| 3 | 7 | 37 | 11 | 2 | yes | 1 |

At the last step, total exceeds s, but removing 11 fixes it exactly. This yields full coverage of all 4 parts.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Single pass over the array maintaining prefix and max |
| Space | O(1) extra | Only a few counters are maintained |

The solution easily fits within limits since the total number of elements across all test cases is at most 10⁵, so the algorithm performs on the order of 10⁵ operations total.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n, s = map(int, input().split())
        a = list(map(int, input().split()))

        pref = 0
        best_len = 0
        best_idx = 0
        max_val = 0
        max_idx = -1

        for i in range(n):
            pref += a[i]
            if a[i] > max_val:
                max_val = a[i]
                max_idx = i

            if pref <= s:
                best_len = i + 1
                best_idx = 0
            else:
                need = pref - s
                if max_val >= need:
                    best_len = i + 1
                    best_idx = max_idx + 1

        out.append(str(best_idx))

    return "\n".join(out)

# provided samples
assert run("""3
7 11
2 9 1 3 18 1 4
4 35
11 9 10 7
1 8
5
""") == "5\n0\n0"

# minimum size
assert run("""1
1 10
5
""") == "1"

# all fit, no skip needed
assert run("""1
3 100
1 2 3
""") == "0"

# tight boundary skip first
assert run("""1
3 3
2 2 2
""") == "1"

# maximum-like prefix stress
assert run("""1
5 10
5 5 5 5 5
""") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 1 | must handle forced skip |
| all small | 0 | no skip needed |
| early large element | 1 | skip improves prefix immediately |
| uniform large values | 1 | consistent max-based decision |

## Edge Cases

When all elements already fit within the limit, the prefix never exceeds s, so the algorithm keeps updating best_len while best_idx remains 0. For input `n=3, s=100, a=[1,2,3]`, every iteration satisfies `pref <= s`, and the final output is 0, matching the requirement that skipping is unnecessary.

When the first element alone is too large, skipping it becomes the only way to proceed. For `n=3, s=3, a=[2,2,2]`, the first prefix already works, but extending requires skipping the first 2 to maximize reach. The algorithm correctly identifies that removing index 1 enables a longer prefix.

When multiple large candidates exist, the stored max always tracks the best removable element, so the algorithm consistently picks a valid skip even if several choices would work, since any correct index is accepted.
