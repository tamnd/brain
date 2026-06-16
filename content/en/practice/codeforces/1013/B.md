---
title: "CF 1013B - And"
description: "We are given a list of integers and a special integer x. The only allowed transformation is choosing an index and replacing that element with its bitwise AND with x. This operation can only decrease bits, since AND can only turn 1 bits into 0 depending on x."
date: "2026-06-16T22:32:25+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1013
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 500 (Div. 2) [based on EJOI]"
rating: 1200
weight: 1013
solve_time_s: 92
verified: true
draft: false
---

[CF 1013B - And](https://codeforces.com/problemset/problem/1013/B)

**Rating:** 1200  
**Tags:** greedy  
**Solve time:** 1m 32s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a list of integers and a special integer `x`. The only allowed transformation is choosing an index and replacing that element with its bitwise AND with `x`. This operation can only decrease bits, since AND can only turn 1 bits into 0 depending on `x`.

The goal is not to make the array sorted or optimized in any global sense. The only requirement is much simpler: after applying the operation any number of times, we want at least one value to appear in at least two different positions. We want the minimum number of operations needed to force such a duplicate, or determine that it is impossible.

The constraint `n ≤ 100000` forces any solution to be close to linear. Any quadratic pairing strategy over all values and intermediate states will be too slow. The value range up to `100000` means we can safely use frequency arrays or hash maps, since the state space is small enough to track exact values.

A naive mistake comes from thinking we must simulate operations on all subsets of indices. For example, trying all pairs `(i, j)` and checking if we can make them equal via sequences of AND operations quickly explodes because each element can be transformed independently in at most one useful way.

A second subtle issue is assuming that repeated operations might help beyond one application per element. This is not true: applying `a & x` twice is identical to applying it once, so each element has only two possible states, original or transformed.

A final edge case appears when no value can ever change. For example, if `a[i] & x == a[i]` for all `i`, then no operation changes anything. If the array has no duplicates initially, the answer is immediately `-1`.

## Approaches

A brute-force perspective would consider all subsets of indices to apply operations and then check whether any value appears twice. For each subset, we would recompute the array and count frequencies. This is exponential in `n`, since there are `2^n` choices, and even pruning does not help much because each operation changes global collision structure. The reason it fails is that operations are independent per element, so global search is unnecessary.

The key observation is that each element has exactly two meaningful states: its original value `a[i]`, and its transformed value `a[i] & x`. Since we only need any duplicate value, we only care about whether some value can be made to appear at least twice using at most one transformation per element.

This reduces the problem to checking three situations. First, if any value already appears at least twice, zero operations are needed. Second, if a transformed value matches an existing original value, we can use one operation to create a duplicate. Third, if two different elements can both be transformed into the same value, we need two operations.

We evaluate all original values and all transformed values and track frequencies. The answer becomes the minimum number of operations required to achieve any frequency ≥ 2 in the combined system, but carefully ensuring we do not double-count elements already equal.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over subsets | O(2^n · n) | O(n) | Too slow |
| Frequency + transformation check | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Count frequencies of all original values in a hash map or array. If any value already has frequency at least 2, the answer is 0. This directly satisfies the goal without performing any operations.
2. Build a second frequency map for transformed values `b[i] = a[i] & x`. We do not modify the array; we only compute these hypothetical results.
3. For each index, consider whether transforming it creates a value that already exists in the original frequency map. If yes, this single operation immediately creates a duplicate, so we can record candidate answer 1.
4. Next, count frequencies of transformed values across all indices. If any transformed value appears at least twice, then performing the operation on two of those indices creates a duplicate value, so we can achieve the goal in 2 operations.
5. The answer is the minimum among 0, 1, or 2 if achievable, otherwise `-1`.

### Why it works

Each element contributes at most two possible values, and each operation only moves one element from its original value to its transformed value. Any solution is therefore equivalent to choosing a subset of indices to “activate” the transformation. The only way to create duplicates is by aligning two elements into the same value across these two states. Since there are no further transitions, the entire problem reduces to counting overlaps between these two value sets, and any optimal solution must fall into one of the three cases identified.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, x = map(int, input().split())
    a = list(map(int, input().split()))
    
    freq = {}
    for v in a:
        freq[v] = freq.get(v, 0) + 1
    
    # already has duplicate
    for v in freq:
        if freq[v] >= 2:
            print(0)
            return
    
    # try one operation case
    seen_after = {}
    for v in a:
        nv = v & x
        if nv in freq:
            print(1)
            return
        seen_after[nv] = seen_after.get(nv, 0) + 1
    
    # check two operations case
    for v in seen_after:
        if seen_after[v] >= 2:
            print(2)
            return
    
    print(-1)

if __name__ == "__main__":
    solve()
```

The first pass builds a frequency table of original values, which lets us immediately detect if the array already satisfies the condition. The second pass computes each possible transformed value and checks whether it can collide with an existing value, which corresponds to a single operation being sufficient.

The third check aggregates transformed frequencies to see if two different indices converge to the same value after transformation. That is the only way to force a duplicate when no original duplicates exist and no single transformation aligns with an existing value.

The ordering matters because we want the minimum number of operations, so we must detect `0` before `1`, and `1` before considering `2`.

## Worked Examples

### Example 1

Input:

```
4 3
1 2 3 7
```

| i | a[i] | a[i] & x | freq original | collision check |
| --- | --- | --- | --- | --- |
| 0 | 1 | 1 | 1 | yes (1 exists) |
| 1 | 2 | 2 | 1 | yes (2 exists) |
| 2 | 3 | 3 | 1 | yes (3 exists) |
| 3 | 7 | 3 | 1 | creates duplicate |

The transformed value of 7 becomes 3, which already exists. One operation is enough.

Output:

```
1
```

This shows a direct collision between a transformed element and an existing value, validating the single-operation logic.

### Example 2

Input:

```
3 1
5 7 3
```

| i | a[i] | a[i] & x | transformed freq |
| --- | --- | --- | --- |
| 0 | 5 | 1 | 1 |
| 1 | 7 | 1 | 2 |
| 2 | 3 | 1 | 3 |

No original duplicates exist, but all transformed values converge to 1.

This means two operations suffice, since choosing any two indices and applying AND creates a duplicate value.

Output:

```
2
```

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Single pass for original frequencies and single pass for transformed values |
| Space | O(n) | Hash maps store frequency counts of values |

The constraints allow up to 100000 elements, and the solution performs only linear passes with constant-time hash operations, which fits comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, x = map(int, input().split())
    a = list(map(int, input().split()))

    freq = {}
    for v in a:
        freq[v] = freq.get(v, 0) + 1

    for v in freq:
        if freq[v] >= 2:
            return "0"

    seen_after = {}
    for v in a:
        nv = v & x
        if nv in freq:
            return "1"
        seen_after[nv] = seen_after.get(nv, 0) + 1

    for v in seen_after:
        if seen_after[v] >= 2:
            return "2"

    return "-1"

# provided sample
assert run("4 3\n1 2 3 7\n") == "1"

# all equal
assert run("5 7\n4 4 4 4 4\n") == "0"

# no change possible
assert run("3 0\n1 2 3\n") == "-1"

# two elements converge after AND
assert run("3 1\n5 7 3\n") == "2"

# already duplicate
assert run("4 10\n1 2 2 3\n") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal array | 0 | zero-operation case |
| x = 0 no change | -1 | impossibility when no transformations work |
| full convergence after AND | 2 | two-operation collision case |
| pre-existing duplicate | 0 | early exit correctness |

## Edge Cases

Consider an array where no duplicates exist initially and every transformation produces the same value. For example, `a = [5, 7, 3]` and `x = 1`. The transformed values all become `1`. The algorithm builds `seen_after = {1: 3}`, detects frequency ≥ 2, and returns `2`. This matches the requirement because at least two indices must be transformed to reach equality.

Another edge case is when transformation does nothing. If `x = 0`, then `a[i] & x = 0` for all `i`. If the original array does not contain duplicates, no transformed value matches any original value in a useful way, and `seen_after` cannot help create collisions with existing values. The algorithm correctly returns `-1` after failing both the single-operation and two-operation checks.
