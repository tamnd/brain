---
title: "CF 466C - Number of Ways"
description: "We are given a sequence of integers arranged in a line, and we want to split it into three contiguous segments. The cut points must produce three non-empty parts, and each part must have exactly the same sum."
date: "2026-05-30T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "data-structures", "dp", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 466
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 266 (Div. 2)"
rating: 1700
weight: 466
solve_time_s: 78
verified: true
draft: false
---

[CF 466C - Number of Ways](https://codeforces.com/problemset/problem/466/C)

**Rating:** 1700  
**Tags:** binary search, brute force, data structures, dp, two pointers  
**Solve time:** 1m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of integers arranged in a line, and we want to split it into three contiguous segments. The cut points must produce three non-empty parts, and each part must have exactly the same sum.

In other words, we are looking for two cut positions in the array that divide it into a prefix, a middle segment, and a suffix, where all three segments sum to the same value.

The input size can be very large, up to 500,000 elements. That immediately rules out any solution that tries all pairs of cut positions directly, since that would involve checking on the order of $n^2$ configurations, which is far beyond what can be computed in two seconds. We need something closer to linear or near-linear time.

A first important structural constraint is that if the total sum of the array is not divisible by three, the answer is automatically zero. No matter how we split, equal-sum partitioning is impossible in that case.

There are a few subtle edge cases that break naive thinking:

One is when many prefix sums match the required third of the total, but there is no valid suffix alignment. For example, in `[0, 0, 0, 0]`, every prefix sum is zero, and every split seems valid at first glance, but only cut positions that preserve three non-empty parts are valid, and overcounting happens if we do not enforce ordering of cuts.

Another edge case is when the target sum is zero. This is dangerous because zero-sum prefixes can occur very frequently, and naive counting can accidentally treat overlapping choices as independent when they are not. For example, in `[0, 0, 0]`, only one valid split exists even though multiple prefix positions satisfy partial conditions.

The key difficulty is enforcing that the first cut happens before the second cut, while still counting combinations efficiently.

## Approaches

The brute-force idea is straightforward. We try every pair of cut indices $i, j$ such that $1 \le i < j < n$. For each pair, we compute the sums of the three segments and check equality. Even if we precompute prefix sums to get segment sums in O(1), we still have O(n²) pairs. With $n = 5 \cdot 10^5$, this would require on the order of $10^{11}$ checks, which is infeasible.

The key observation is that the problem reduces to reasoning about prefix sums and fixed target values. Let total sum be $S$. If a valid split exists, each segment must sum to $S/3$. Let this value be $T$. We are then looking for indices where prefix sum equals $T$ (first cut), and indices where prefix sum equals $2T$ (second cut). The constraint is that the second cut must come after the first.

This transforms the problem into counting ordered pairs of prefix-sum hits: every position where prefix sum equals $T$ can potentially pair with later positions where prefix sum equals $2T$. Instead of searching all pairs explicitly, we scan once from left to right, counting how many valid first-cut positions we have seen so far.

We maintain a counter of how many times we have encountered prefix sum $T$. When we reach a position where prefix sum equals $2T$, every previously seen $T$ position forms a valid pair with it, so we add that counter to the answer.

This reduces the problem to a single pass over the array.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Prefix sum counting | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We define prefix sums while scanning the array once.

1. Compute total sum $S$. If $S$ is not divisible by 3, return 0 immediately, because no equal partition exists.
2. Set target $T = S / 3$. We now look for prefix sum values equal to $T$ and $2T$.
3. Initialize a running prefix sum `pref = 0`, a counter `count_T = 0`, and an answer `ans = 0`.
4. Iterate through the array from index 0 to n − 1, updating `pref += a[i]`.
5. Whenever `pref == 2T` and we are not at the last element, we add `count_T` to `ans`. This works because every earlier position where `pref == T` can serve as the first cut.
6. Whenever `pref == T` and we are not at the last position, increment `count_T`.
7. Continue until the end of the array.

### Why it works

The algorithm relies on the fact that valid decompositions correspond exactly to ordered pairs of prefix-sum hits at $T$ and $2T$. Any valid split must choose a first cut at some index where prefix sum is $T$, and a second cut later where prefix sum is $2T$. By scanning left to right, we ensure that when we reach a $2T$ position, all valid $T$ positions before it have already been counted, and each produces exactly one valid triple partition. This preserves a one-to-one mapping between counted pairs and valid splits.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    total = sum(a)
    if total % 3 != 0:
        print(0)
        return
    
    target = total // 3
    pref = 0
    count_first = 0
    ans = 0
    
    for i in range(n):
        pref += a[i]
        
        if i < n - 1 and pref == 2 * target:
            ans += count_first
        
        if i < n - 1 and pref == target:
            count_first += 1
    
    print(ans)

if __name__ == "__main__":
    solve()
```

The solution begins by reading the array and computing its total sum. The divisibility check is essential because it eliminates impossible cases early and prevents unnecessary traversal logic.

The variable `pref` maintains the prefix sum dynamically, avoiding recomputation. The key subtlety is the order of updates: when we reach a position where `pref == 2 * target`, we first use the current `count_first` before potentially updating it later. This ensures correctness in cases where both conditions could interact across indices.

The condition `i < n - 1` ensures that the second cut is not placed at the very end, preserving a non-empty third segment.

## Worked Examples

We use the sample input:

Input:

```
5
1 2 3 0 3
```

Here total sum is 9, so target is 3.

### Trace

| i | a[i] | prefix | count_first | ans | event |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 1 | 0 | 0 | none |
| 1 | 2 | 3 | 1 | 0 | pref == T |
| 2 | 3 | 6 | 1 | 1 | pref == 2T, add 1 |
| 3 | 0 | 6 | 1 | 2 | pref == 2T again |
| 4 | 3 | 9 | 1 | 2 | end |

The trace shows that there are two valid ways to choose a first cut at prefix sum 3 and a second cut at prefix sum 6.

This confirms that repeated occurrences of $2T$ correctly accumulate all earlier valid $T$ positions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | single pass over array with constant work per element |
| Space | O(1) | only a few counters are used |

The algorithm fits comfortably within constraints for $n = 5 \cdot 10^5$, since it performs only linear scanning and constant-time arithmetic per element.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    from sys import stdin
    n = int(stdin.readline())
    a = list(map(int, stdin.readline().split()))
    
    total = sum(a)
    if total % 3 != 0:
        return "0"
    
    target = total // 3
    pref = 0
    count_first = 0
    ans = 0
    
    for i in range(n):
        pref += a[i]
        if i < n - 1 and pref == 2 * target:
            ans += count_first
        if i < n - 1 and pref == target:
            count_first += 1
    
    return str(ans)

# provided sample
assert run("5\n1 2 3 0 3\n") == "2"

# all zeros small
assert run("3\n0 0 0\n") == "1"

# no solution due to indivisible sum
assert run("4\n1 1 1 1\n") == "0"

# multiple zeros creating many prefixes
assert run("5\n0 0 0 0 0\n") == "6"

# minimal invalid size
assert run("2\n1 2\n") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3\n0 0 0` | `1` | minimal valid split |
| `4\n1 1 1 1` | `0` | indivisible sum |
| `5\n0 0 0 0 0` | `6` | many zero-sum prefixes |
| `2\n1 2` | `0` | too small for 3 parts |

## Edge Cases

A key edge case is when the array contains many zeros, which makes prefix sums equal to both $T$ and $2T$ extremely frequently.

For input:

```
5
0 0 0 0 0
```

Total sum is 0, so $T = 0$. Every prefix sum is 0.

Walking through the algorithm:

At each index except the last, every position increments `count_first` and also contributes to `ans` when reaching later positions. The structure of the scan ensures that each valid ordered pair of cuts is counted exactly once, because each second cut accumulates all previous first cuts.

This demonstrates that even in degenerate cases where all values are identical, the ordering constraint is preserved purely through the single-pass accumulation logic.
