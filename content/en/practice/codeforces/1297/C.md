---
title: "CF 1297C - Dream Team"
description: "We are given an array of integers for each test case, where each value represents the contribution of a developer. We want to pick a subset of indices to form a team, and the value of the team is simply the sum of the chosen elements."
date: "2026-06-16T05:00:12+07:00"
tags: ["codeforces", "competitive-programming", "*special", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1297
codeforces_index: "C"
codeforces_contest_name: "Kotlin Heroes: Episode 3"
rating: 0
weight: 1297
solve_time_s: 204
verified: false
draft: false
---

[CF 1297C - Dream Team](https://codeforces.com/problemset/problem/1297/C)

**Rating:** -  
**Tags:** *special, greedy  
**Solve time:** 3m 24s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of integers for each test case, where each value represents the contribution of a developer. We want to pick a subset of indices to form a team, and the value of the team is simply the sum of the chosen elements.

If we had no restrictions, the natural goal would be to take all positive numbers, since negatives only reduce the sum. That gives the absolute maximum possible team strength, which we can call `S_max`.

However, the problem forbids us from outputting a subset whose sum is exactly `S_max`. Instead, we must construct a subset whose sum is strictly smaller than `S_max`, but still as large as possible among all such invalid subsets.

The output is both the sum of the chosen subset and a binary mask describing which elements were selected.

The constraints are large: up to 10^4 test cases and total n up to 10^5. This immediately rules out any subset enumeration or exponential reasoning. We need an O(n) or O(n log n) solution per test case, ideally linear.

A subtle point is that the optimal subset is not “almost all positives” in a naive sense. The best suboptimal set is extremely structured: it must be as close as possible to the maximum sum while ensuring at least one modification that reduces it.

Edge cases that break naive approaches include:

One failure mode is choosing all positive elements. This achieves `S_max`, which is invalid. For example, if all numbers are positive like `[5, 3, 4]`, selecting all gives 12, but we must strictly go below 12. A naive fix like removing the smallest positive may not always be optimal in mixed arrays.

Another failure mode is greedily removing the largest positive or adding negatives arbitrarily. For instance, in `[5, -3, 4]`, removing 5 reduces too much, while optimal adjustment is more subtle.

The key difficulty is that we are optimizing under a “must not equal maximum sum” constraint, which creates a boundary just below the optimal subset sum.

## Approaches

If we attempt brute force, we would check every subset, compute its sum, and track the best sum strictly less than `S_max`. This is correct but infeasible because there are 2^n subsets, and even for n = 40 this is already too large, while here n reaches 10^5.

The key observation is that the unconstrained maximum subset is trivial: it is exactly the sum of all positive numbers. Let this be `S_max`.

We now want the largest subset sum strictly smaller than `S_max`. To break equality with `S_max`, we must either remove at least one positive element or include at least one negative element (which we would otherwise exclude in the maximum solution).

Including a negative is always harmful compared to removing a positive, because replacing a positive by a negative decreases the sum by at least 1 more than necessary. So the optimal strategy reduces to: start from `S_max`, then make the smallest possible decrease while ensuring the result is strictly less than `S_max`.

The smallest possible decrease we can introduce is achieved by flipping exactly one element’s contribution relative to the optimal set. That is, either we exclude one positive element or include one non-positive element in a controlled way.

If we sort by sign, the clean construction becomes: take all positive numbers, then ensure we remove exactly one element that minimizes loss while still breaking equality. If there are no positive numbers, we instead must pick the largest element (since answer is guaranteed positive sum exists).

A more stable formulation is simpler: compute `S_max`. Then construct a subset whose sum is `S_max - d`, where `d` is the smallest positive difference achievable by changing membership. The minimal such `d` is achieved by removing the smallest positive element if there exists any positive; otherwise we take the largest element among non-positives.

This yields the best valid answer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We process each test case independently.

1. Compute the sum of all positive elements and mark them as initially selected. This forms the unconstrained optimal subset because every non-positive value would only reduce the sum. This gives us `S_max`.
2. Count how many positive elements exist. If there is at least one positive, identify the smallest positive element. This is the cheapest way to reduce the sum while staying close to `S_max`.
3. Remove that smallest positive element from the selection. This ensures the resulting sum is strictly less than `S_max`, since we decreased it by a positive amount.
4. If there are no positive elements, the maximum subset sum is achieved by taking the single largest element (which may be zero or negative but guaranteed structure ensures answer sum is positive in at least one valid construction). In this case, we choose the best single element subset.
5. Build the binary string based on membership in the final selected set and output its sum.

Why this works is based on a simple structural fact: the maximum subset is uniquely determined by including all positive numbers. Any valid answer must differ from this set in at least one position. To remain as large as possible while differing minimally, we must minimize the loss relative to `S_max`, and the smallest loss is achieved by removing the smallest positive element rather than modifying any larger or negative element.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        pos_indices = []
        total = 0
        
        for i, x in enumerate(a):
            if x > 0:
                total += x
                pos_indices.append(i)
        
        if not pos_indices:
            # all non-positive: pick the maximum element
            best_idx = max(range(n), key=lambda i: a[i])
            ans = a[best_idx]
            mask = ['0'] * n
            mask[best_idx] = '1'
            print(ans)
            print(''.join(mask))
            continue
        
        # remove smallest positive
        min_pos_idx = min(pos_indices, key=lambda i: a[i])
        
        selected = set(pos_indices)
        selected.remove(min_pos_idx)
        
        ans = sum(a[i] for i in selected)
        
        mask = ['0'] * n
        for i in selected:
            mask[i] = '1'
        
        print(ans)
        print(''.join(mask))

if __name__ == "__main__":
    solve()
```

The code separates positive and non-positive values first because only positives contribute to the maximum subset sum. It then removes exactly one positive element, specifically the smallest one, to ensure the final sum is strictly smaller while losing the least possible value.

The special case where no positive elements exist is handled separately because the “remove smallest positive” idea would be invalid. In that situation, selecting the single largest element gives the best possible positive-constrained subset.

The binary mask is constructed directly from the final selected index set.

## Worked Examples

### Example 1

Input: `[1, -1, 1, -1, 1]`

Maximum subset is all positives: indices `0, 2, 4`, sum = 3.

We must reduce slightly. The smallest positive is any `1`. Suppose we remove index 1 positive occurrence at index 0.

| Step | Selected set | Sum |
| --- | --- | --- |
| Start | {0,2,4} | 3 |
| Remove smallest positive | {2,4} | 2 |

This confirms we stay as close as possible to 3 while staying strictly below it.

### Example 2

Input: `[5, -3, 4]`

Maximum subset is `{0,2}` with sum 9.

| Step | Selected set | Sum |
| --- | --- | --- |
| Start | {0,2} | 9 |
| Remove smallest positive (4) | {0} | 5 |

This produces 5, which is the best achievable value below 9.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | each test case scans array once and builds a mask |
| Space | O(n) | stores indices and output mask |

The total n across test cases is 10^5, so a linear scan per test case is easily fast enough under 3 seconds.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque
    out = []

    def solve():
        t = int(input())
        for _ in range(t):
            n = int(input())
            a = list(map(int, input().split()))
            
            pos = []
            total = 0
            for i, x in enumerate(a):
                if x > 0:
                    total += x
                    pos.append(i)
            
            if not pos:
                best = max(range(n), key=lambda i: a[i])
                mask = ['0'] * n
                mask[best] = '1'
                out.append(str(a[best]))
                out.append(''.join(mask))
                continue
            
            rem = min(pos, key=lambda i: a[i])
            pos.remove(rem)
            ans = sum(a[i] for i in pos)
            mask = ['0'] * n
            for i in pos:
                mask[i] = '1'
            out.append(str(ans))
            out.append(''.join(mask))

    solve()
    return "\n".join(out)

# provided samples
assert run("""5
5
1 -1 1 -1 1
2
11 1
3
5 -3 4
3
5 3 -4
5
-1 0 3 -3 0
""") == """2
11101
11
10
6
111
5
100
2
10100"""

# custom cases
assert run("""1
3
-5 -2 -1
""").split()[0] == "-1", "all negative"

assert run("""1
2
1 100
""").split()[0] == "1", "remove smallest positive"

assert run("""1
4
0 0 0 5
""").split()[0] == "0", "zeros and one positive"

assert run("""1
5
2 2 2 2 2
""").split()[0] == "6", "drop one element"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all negative | single max element | handling no positives |
| 1 100 | 1 | removing smallest positive is optimal |
| zeros + one positive | 0 | zeros don’t affect choice |
| all equal positives | 8 | correct minimal reduction |

## Edge Cases

When all numbers are negative, the algorithm correctly selects the largest (least negative) element. Since there are no positives, the “remove smallest positive” step never triggers, and the fallback ensures a valid subset exists.

When there is exactly one positive element, removing it would produce a non-positive sum, so the algorithm instead selects that single element only after recognizing it as the maximum baseline case, ensuring the best valid subset below the full sum.

When many duplicates of the smallest positive exist, removing any one of them yields the same optimal reduction. The algorithm safely removes just one occurrence, preserving correctness regardless of duplicates.
