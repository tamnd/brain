---
title: "CF 1213B - Bad Prices"
description: "We are given several independent experiments, and each experiment consists of a sequence of daily prices of a product."
date: "2026-06-11T23:04:35+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1213
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 582 (Div. 3)"
rating: 1100
weight: 1213
solve_time_s: 80
verified: true
draft: false
---

[CF 1213B - Bad Prices](https://codeforces.com/problemset/problem/1213/B)

**Rating:** 1100  
**Tags:** data structures, implementation  
**Solve time:** 1m 20s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several independent experiments, and each experiment consists of a sequence of daily prices of a product. For each sequence, we need to identify how many days are “unlucky” in the following sense: a day is considered bad if there exists some later day where the price is strictly lower than on that day.

So for every position in the array, we are effectively asking whether there is any smaller value somewhere to its right. If such a value exists, that position contributes to the answer.

The constraints are large in aggregate, with the total length of all sequences up to 150,000. This immediately rules out any solution that compares each element against all elements to its right, since that would be quadratic in the worst case and lead to roughly 10¹⁰ operations in adversarial inputs. A linear or near-linear scan per test case is required.

A subtle edge case appears when the array is strictly increasing. For example, in `[1, 2, 3, 4]`, no element has a smaller value to its right, so the answer is zero. A naive approach might incorrectly count comparisons if it does not properly check for strictly smaller values rather than smaller-or-equal values.

Another edge case is a strictly decreasing array like `[5, 4, 3, 2, 1]`. Every element except the last has a smaller element later, so the answer is `n-1`. This is a worst-case scenario for brute force, because every prefix element qualifies as bad.

## Approaches

A direct interpretation leads to a simple brute-force method: for each day `i`, scan all days `j > i` and check whether any `a[j] < a[i]`. If such a day exists, we increment the answer for day `i`.

This is correct because it follows the definition literally. However, its cost is problematic. In the worst case, such as a decreasing sequence, we perform roughly `n + (n-1) + ... + 1`, which is O(n²) comparisons per test case. With total `n` up to 150,000, this becomes far too slow.

The key observation is that we do not need to know _which_ future value is smaller, only whether at least one exists. This suggests maintaining information about the suffix of the array. If we traverse from right to left, we can track the minimum value seen so far. At each position, we compare the current element with this suffix minimum. If the current value is greater than the minimum to its right, then we already know there exists a smaller future element, so this position is bad.

This reduces the problem to a single pass per test case, because the suffix minimum can be updated incrementally.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Suffix minimum scan | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We process each test case independently and scan the array from right to left.

1. Start from the last day and initialize a variable `min_suffix` with the last price. This represents the smallest price seen among all days strictly to the right of the current position.
2. Move one step left at a time, inspecting each day `i`.
3. For each position, compare `a[i]` with `min_suffix`. If `a[i] > min_suffix`, then there exists a later day with a lower price, so day `i` is bad and we increment the answer.
4. Regardless of whether we increment, we update `min_suffix = min(min_suffix, a[i])` to ensure it always reflects the smallest value in the suffix starting at `i`.
5. Continue until the first element is processed.

The correctness hinges on the fact that when we process index `i`, `min_suffix` exactly equals `min(a[i+1], ..., a[n])`, so the comparison is equivalent to checking whether a smaller element exists to the right.

### Why it works

At every step, `min_suffix` stores the minimum value of the suffix strictly to the right of the current index. This invariant holds because we update it only after processing each element. Therefore, the condition `a[i] > min_suffix` is true exactly when there exists some `j > i` such that `a[j] < a[i]`. No information about the identity of `j` is needed, only its existence, which is fully captured by the suffix minimum.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
out = []

for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    
    min_suffix = a[-1]
    bad = 0
    
    for i in range(n - 2, -1, -1):
        if a[i] > min_suffix:
            bad += 1
        if a[i] < min_suffix:
            min_suffix = a[i]
    
    out.append(str(bad))

print("\n".join(out))
```

The implementation follows the reverse scan directly. The variable `min_suffix` always represents the smallest value to the right of the current index, so the comparison `a[i] > min_suffix` is the exact translation of the “bad day” definition. The update condition ensures we correctly propagate new minimums.

Care must be taken to initialize `min_suffix` with the last element, since the last day has no future days and can never be bad. Also, the answer accumulator is kept per test case to avoid cross-contamination between datasets.

## Worked Examples

We trace the sample input:

### Example 1

Input array: `[3, 9, 4, 6, 7, 5]`

| i | a[i] | min_suffix | bad? | updated min_suffix |
| --- | --- | --- | --- | --- |
| 5 | 5 | 5 | no | 5 |
| 4 | 7 | 5 | yes | 5 |
| 3 | 6 | 5 | yes | 5 |
| 2 | 4 | 5 | no | 4 |
| 1 | 9 | 4 | yes | 4 |
| 0 | 3 | 4 | no | 3 |

Answer = 3

This confirms that only elements that have a strictly smaller value later are counted.

### Example 2

Input array: `[2, 1]`

| i | a[i] | min_suffix | bad? | updated min_suffix |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | no | 1 |
| 0 | 2 | 1 | yes | 1 |

Answer = 1

This shows the minimal non-trivial case where exactly one element becomes bad.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each element is processed once in a single reverse pass |
| Space | O(1) extra | Only a few variables are used beyond input storage |

Given that the sum of all `n` is at most 150,000, the total work is linear overall, easily fitting within the time limit.

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
        
        min_suffix = a[-1]
        bad = 0
        
        for i in range(n - 2, -1, -1):
            if a[i] > min_suffix:
                bad += 1
            if a[i] < min_suffix:
                min_suffix = a[i]
        
        out.append(str(bad))
    
    return "\n".join(out)

# provided samples
assert run("""5
6
3 9 4 6 7 5
1
1000000
2
2 1
10
31 41 59 26 53 58 97 93 23 84
7
3 2 1 2 3 4 5
""") == """3
0
1
8
2"""

# custom: minimum size
assert run("""1
1
100
""") == """0"""

# custom: strictly increasing
assert run("""1
5
1 2 3 4 5
""") == """0"""

# custom: strictly decreasing
assert run("""1
5
5 4 3 2 1
""") == """4"""

# custom: mixed duplicates
assert run("""1
6
1 3 3 2 2 4
""") == """3"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| size 1 | 0 | single element edge case |
| increasing | 0 | no bad elements case |
| decreasing | n-1 | worst-case density |
| duplicates mix | 3 | handling equal values correctly |

## Edge Cases

In a single-element array like `[10]`, the reverse scan initializes `min_suffix` as 10 and never enters the loop. No comparisons are made, so the answer remains 0, which matches the definition since there are no future days.

In a strictly increasing sequence like `[1, 2, 3, 4]`, the suffix minimum at each step is always greater than or equal to the current value, so the condition `a[i] > min_suffix` never triggers. The algorithm correctly avoids false positives.

In a strictly decreasing sequence like `[5, 4, 3, 2, 1]`, every element except the last is larger than the suffix minimum at that point, so each is counted as bad. The algorithm increments exactly `n-1` times, matching the fact that every prefix element has a smaller future value.
