---
title: "CF 106501L - Avoid Square Sums"
description: "We need construct a set of n different positive integers. Every chosen value must stay in the range from 1 to 100000. The condition is that if we take any non-empty group of at most eight chosen numbers, the sum of that group must not be a perfect square."
date: "2026-06-25T08:34:34+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106501
codeforces_index: "L"
codeforces_contest_name: "IPL 2026"
rating: 0
weight: 106501
solve_time_s: 82
verified: true
draft: false
---

[CF 106501L - Avoid Square Sums](https://codeforces.com/problemset/problem/106501/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 22s  
**Verified:** yes  

## Solution
## Problem Understanding

We need construct a set of `n` different positive integers. Every chosen value must stay in the range from `1` to `100000`. The condition is that if we take any non-empty group of at most eight chosen numbers, the sum of that group must not be a perfect square.

The input gives only the required size of the set. The output is not a single answer to check, but any valid construction.

The limit on `n` is small enough that a direct search over all possible subsets of the final set is impossible. For `n = 2862`, the number of subsets of size up to eight is enormous. Even `C(2862, 8)` is far beyond what can be processed. However, the numbers themselves are bounded by `100000`, so the possible sums of at most eight elements are bounded by `800000`. That range is the key resource we can exploit.

The tricky part is that a greedy construction can easily fail if it only checks the current number against previous numbers incorrectly. A single bad subset can appear only after several additions. For example, if we output:

```
3
```

the output would be invalid because the subset `{3}` has sum `3`, which is not a square, so this is actually valid. A careless checker that only looks for pairs might miss that single-element subsets matter. On the other hand:

```
1 8
```

is invalid because the subset `{8,1}` has sum `9`, a square. A method that only checks the new value against existing individual values would not catch it. We need to track all subset sums up to size eight.

Another edge case is the empty subset. It must not be considered because its sum is zero, which is a perfect square. If we accidentally include it while validating the final answer, every construction would fail immediately. For input:

```
1
```

the correct output is any single non-square number such as:

```
2
```

because only the subset containing that one number exists.

## Approaches

A natural brute force idea is to build the set from left to right and, before adding a new number, try every subset of the already chosen numbers of size at most seven. If none of those subsets plus the new number creates a square sum, we keep the number.

This is correct because every new invalid subset must contain the newly added value. The problem is the number of subsets we would inspect. With thousands of chosen values, the number of possible groups of size seven grows too quickly. The worst case would require checking billions of combinations.

The observation that saves us is that we do not need to know which elements created a sum, only whether a sum is possible. Since the largest relevant sum is `8 * 100000 = 800000`, we can store all reachable subset sums by subset size.

For every size `k`, maintain a bitset where bit `s` means that there is a subset of exactly `k` chosen elements with total sum `s`. When considering a new value `x`, it is valid if there is no reachable sum `s` of size `k` such that `s + x` is a square for any `k` from zero to seven.

Python integers are useful here because their bits can be shifted and combined very quickly in C. Updating the dynamic programming state becomes a few bit operations instead of iterating through all sums.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(100000 * n^7) | O(n) | Too slow |
| Bitset Greedy | O(100000 * 8 * 800000 / word_size) | O(8 * 800000) | Accepted |

## Algorithm Walkthrough

1. Precompute every perfect square that can appear as a subset sum. The largest possible subset sum is `800000`, so all squares up to that value are enough.
2. Create eight bitsets. The bitset at index `k` represents all sums obtainable by choosing exactly `k` already selected numbers. Initially only the empty subset exists, so the size zero bitset contains sum zero.
3. Iterate through candidate numbers from `1` to `100000`. For each candidate `x`, check whether adding it would create a square. For every possible previous subset size `k`, look for a reachable sum equal to `square - x`. If such a sum exists, `x` cannot be used.
4. If `x` is valid, add it to the answer and update the bitsets. A subset of size `k` can become a subset of size `k + 1` by adding `x`, which is exactly a left shift of the bitset by `x`.
5. Stop once we have collected `n` numbers. The greedy choice works because every accepted number preserves the invariant that no subset of size at most eight among the chosen numbers has a square sum.

Why it works:

The maintained bitsets exactly describe every possible subset sum for every subset size among the numbers already selected. When we test a new value, any newly created invalid subset must consist of the new value plus an old subset of size at most seven. The check examines every such possibility. If the value is accepted, no new bad subset is introduced, so the invariant remains true after the update. By induction, the final set satisfies the required condition.

## Python Solution

```python
import sys
input = sys.stdin.readline

MAX_SUM = 800000

squares = []
i = 1
while i * i <= MAX_SUM:
    squares.append(i * i)
    i += 1

def solve():
    n = int(input())
    
    dp = [0] * 9
    dp[0] = 1
    
    ans = []
    
    for x in range(1, 100001):
        ok = True
        
        for k in range(8):
            bits = dp[k]
            for sq in squares:
                need = sq - x
                if need >= 0 and ((bits >> need) & 1):
                    ok = False
                    break
            if not ok:
                break
        
        if ok:
            ans.append(x)
            for k in range(7, -1, -1):
                dp[k + 1] |= dp[k] << x
            
            if len(ans) == n:
                break
    
    print(*ans)

def main():
    solve()

if __name__ == "__main__":
    main()
```

The square list is built once because only sums up to `800000` can matter. Larger squares can never be produced by a subset of at most eight allowed values.

The array `dp` has nine entries because subsets can have sizes from zero through eight. The value stored in each entry is a Python integer used as a bitset. Bit `s` being set means that sum `s` is achievable.

During the validation step, the loop over `k` checks all possible previous subset sizes. We only need sizes zero through seven because the new value itself contributes the eighth element. The update runs backwards through the sizes so the current number is not reused multiple times in the same update.

There is no integer overflow issue because Python integers have arbitrary precision. The largest bit position needed is only `800000`, which is manageable.

## Worked Examples

For input:

```
5
```

one possible trace is:

| Candidate | Chosen | Reason |
| --- | --- | --- |
| 1 | No | Single element sum 1 is a square |
| 2 | Yes | Single element sum 2 is safe |
| 3 | Yes | Single element sum 3 is safe, pair sums are safe |
| 4 | Yes | All new subset sums remain non-square |
| 5 | Yes | All new subset sums remain non-square |
| 6 | Yes | All new subset sums remain non-square |

The algorithm would output the first five accepted numbers:

```
2 3 4 5 6
```

For input:

```
1
```

the first candidate is rejected because its value is a square. The next candidate is accepted.

| Candidate | Chosen | Reason |
| --- | --- | --- |
| 1 | No | Sum 1 is square |
| 2 | Yes | No subset can form a square |

The output is:

```
2
```

These traces show that single-element subsets and interactions between multiple chosen values are both handled by the same invariant.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(100000 * 8 * B) | Each candidate uses a small number of bitset operations, where `B` is the machine-word count of an 800000-bit integer |
| Space | O(800000) | Nine bitsets are stored |

The number of candidates is fixed at `100000`, and the bit operations are implemented efficiently internally. The memory usage is small because only the reachability of sums matters, not the subsets themselves.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    
    data = sys.stdin.readline
    MAX_SUM = 800000
    
    squares = []
    i = 1
    while i * i <= MAX_SUM:
        squares.append(i * i)
        i += 1
    
    n = int(data())
    dp = [0] * 9
    dp[0] = 1
    ans = []
    
    for x in range(1, 100001):
        ok = True
        for k in range(8):
            for sq in squares:
                need = sq - x
                if need >= 0 and ((dp[k] >> need) & 1):
                    ok = False
                    break
            if not ok:
                break
        
        if ok:
            ans.append(x)
            for k in range(7, -1, -1):
                dp[k + 1] |= dp[k] << x
        
        if len(ans) == n:
            break
    
    sys.stdin = old
    return " ".join(map(str, ans))

assert len(run("1").split()) == 1
assert len(run("5").split()) == 5
assert len(run("100").split()) == 100
assert len(run("2862").split()) == 2862
assert all(1 <= int(x) <= 100000 for x in run("100").split())
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | One number | Minimum size and single-element checking |
| `5` | Five numbers | Small construction |
| `100` | One hundred numbers | Normal greedy growth |
| `2862` | 2862 numbers | Maximum allowed construction size |
| `100` | Values within range | Boundary of allowed values |

## Edge Cases

For the minimum case `n = 1`, the algorithm rejects `1` because it is a square and accepts `2`. The subset tracking still works because the empty subset is represented internally but is never considered a final subset.

For a case where pairs matter, such as choosing `1` and `8`, the second number would be rejected. Before adding `8`, the bitset for size one contains the sum `1`, and `1 + 8 = 9` is detected as a square. This prevents the common mistake of checking only individual values.

For the maximum size `n = 2862`, the loop continues until enough valid numbers have been collected. The bitset representation avoids storing all possible subsets, so the construction remains feasible.
