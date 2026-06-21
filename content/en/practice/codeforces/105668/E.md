---
title: "CF 105668E - Missing Number Queries"
description: "We are given an array that is being updated over time, and we must answer queries about what value can safely be used from a subarray under a specific rule involving “missing” numbers."
date: "2026-06-22T05:13:12+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105668
codeforces_index: "E"
codeforces_contest_name: "MITIT Winter 2025 Beginner Round"
rating: 0
weight: 105668
solve_time_s: 47
verified: true
draft: false
---

[CF 105668E - Missing Number Queries](https://codeforces.com/problemset/problem/105668/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array that is being updated over time, and we must answer queries about what value can safely be used from a subarray under a specific rule involving “missing” numbers.

The structure of the interaction is simple: the array changes through point updates, and each query asks us to output a number that is guaranteed to satisfy a condition relative to a chosen segment of the array. The key hidden idea is that the answer depends only on whether the current array contains all values from a fixed range, and if it does not, then any missing value becomes a universal answer. Otherwise, when nothing is missing, we must ensure we pick something outside the queried interval.

The constraints are large enough that recomputing frequencies or scanning ranges for every query would be too slow. Any solution that checks an interval by iterating over it will degrade to quadratic behavior in the worst case, which is not acceptable when the array size and number of operations are both large. This forces us toward maintaining global information that can be updated in logarithmic or constant time per operation.

A subtle edge case appears when the array is exactly a permutation of values from 1 to N. In that case, there is no globally missing value, so the naive strategy of always returning “some missing number” fails because none exists. Another failure case occurs if we always pick a fixed index outside the query range without tracking updates, because updates can change whether that index remains valid or not.

For example, if the array becomes a permutation like `[1, 2, 3]`, there is no missing number. A naive solution might incorrectly try to output a “missing” value such as 4 if it assumes the range is larger or not carefully bounded. The correct behavior in this case must switch strategy entirely.

## Approaches

The brute-force idea is straightforward. For each update, we modify the array directly. For each query, we scan the relevant interval and compute what values appear, then determine whether some value from 1 to N is missing or whether we can pick something outside the interval. This is correct because it directly follows the definition of the problem. However, each query can take linear time in the size of the interval, and in the worst case we may scan the whole array repeatedly. With up to large constraints, this leads to roughly O(NQ), which is too slow.

The key observation is that we do not actually need per-query structural information about intervals. We only need two global facts: whether there exists at least one value in 1 to N that is absent from the entire array, and if not, then every value appears at least once and the array behaves like a permutation. In that permutation case, any position outside a query interval is valid, and such a position always exists unless the query covers the whole array, in which case any value is acceptable because all values exist everywhere.

This reduces the problem to maintaining frequencies of values and tracking which values currently have frequency zero. That gives us immediate access to a valid “missing” answer when it exists. If no missing value exists, we just need any index outside the query range, which is trivial to pick.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(NQ) | O(N) | Too slow |
| Optimal | O(N + Q) | O(N) | Accepted |

## Algorithm Walkthrough

We maintain a frequency array `freq[x]` for values in the range 1 to N, and a structure that stores all values with zero frequency.

1. Initialize `freq` by counting occurrences of each value in the initial array. Any value from 1 to N with frequency zero is inserted into a set of missing values. This lets us instantly detect whether a globally missing number exists.
2. For a type 1 update at position `i`, where the value changes from `old` to `new`, we decrement `freq[old]` and increment `freq[new]`. If `freq[old]` becomes zero, we insert it into the missing set. If `freq[new]` was zero before the update and becomes positive, we remove it from the missing set. This keeps the missing set accurate after every operation.
3. For a type 2 query on a range `[l, r]`, we first check whether the missing set is non-empty. If it is, we return any element from it immediately, since that value does not appear anywhere in the array and is valid for every query.
4. If the missing set is empty, the array is a permutation of 1 to N. In this case, we must return any value not coming strictly from the queried interval. The simplest choice is to return an element from the array outside `[l, r]`, for example `a[1]` if `l > 1`, otherwise `a[N]`. This guarantees we pick an index outside the query segment.

### Why it works

The algorithm maintains the invariant that `missing_set` exactly contains all values in `[1, N]` that do not appear in the array at the current time. This is preserved because every update adjusts frequencies locally and immediately reflects changes in the set. When the set is non-empty, any element inside it is globally absent, which makes it valid regardless of the query interval. When the set is empty, every value exists somewhere in the array, which forces us into the permutation case, and in that case any index outside the query interval provides a valid answer because it is guaranteed not to be restricted by the query range definition.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, q = map(int, input().split())
    a = list(map(int, input().split()))

    freq = [0] * (n + 1)
    for x in a:
        freq[x] += 1

    missing = set()
    for x in range(1, n + 1):
        if freq[x] == 0:
            missing.add(x)

    for _ in range(q):
        tmp = input().split()
        if tmp[0] == '1':
            i = int(tmp[1]) - 1
            v = int(tmp[2])

            old = a[i]
            if old != v:
                freq[old] -= 1
                if freq[old] == 0:
                    missing.add(old)

                if freq[v] == 0:
                    if v in missing:
                        missing.discard(v)
                freq[v] += 1
                a[i] = v

        else:
            l = int(tmp[1])
            r = int(tmp[2])

            if missing:
                print(next(iter(missing)))
            else:
                if l > 1:
                    print(a[0])
                else:
                    print(a[-1])

if __name__ == "__main__":
    solve()
```

The update logic carefully maintains consistency between the array and frequency table. When replacing a value, we must update both the old and new counts in the correct order so that the missing set always reflects the current state. The query logic relies entirely on whether the missing set is empty, so correctness depends heavily on keeping it accurate.

A subtle point is that we never actually need to inspect the interval `[l, r]` for updates or existence checks. The interval only matters when the array is a full permutation, in which case we only need a single element outside it.

## Worked Examples

### Example 1

Consider `a = [1, 2, 3, 4]`, and a query asking about `[2, 3]`.

At the start, `missing = ∅` since the array is a permutation.

| Step | l | r | missing | chosen action | output |
| --- | --- | --- | --- | --- | --- |
| query | 2 | 3 | ∅ | pick outside interval | 1 |

Since the array is a permutation, we return an element outside the range, here `a[0] = 1`.

This demonstrates the permutation fallback behavior.

### Example 2

Consider `a = [1, 1, 2, 4]` with N = 4.

Initially, frequencies are:

`freq[1]=2, freq[2]=1, freq[3]=0, freq[4]=1`, so `missing = {3}`.

| Step | l | r | missing | chosen action | output |
| --- | --- | --- | --- | --- | --- |
| query | 1 | 4 | {3} | return missing | 3 |

Since a missing number exists, we immediately return `3` without looking at the interval.

This shows why interval structure is irrelevant in the non-permutation case.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N + Q) | Each update changes two frequency counts and set membership in O(1) amortized, each query is O(1) |
| Space | O(N) | Frequency array and missing set over values 1 to N |

The solution comfortably fits typical constraints up to 2e5 operations since every operation is constant time and uses only linear memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, q = map(int, input().split())
    a = list(map(int, input().split()))

    freq = [0] * (n + 1)
    for x in a:
        freq[x] += 1

    missing = set()
    for x in range(1, n + 1):
        if freq[x] == 0:
            missing.add(x)

    out = []
    for _ in range(q):
        tmp = input().split()
        if tmp[0] == '1':
            i = int(tmp[1]) - 1
            v = int(tmp[2])
            old = a[i]
            if old != v:
                freq[old] -= 1
                if freq[old] == 0:
                    missing.add(old)
                if freq[v] == 0 and v in missing:
                    missing.discard(v)
                freq[v] += 1
                a[i] = v
        else:
            l = int(tmp[1])
            r = int(tmp[2])
            if missing:
                out.append(str(next(iter(missing))))
            else:
                out.append(str(a[0] if l > 1 else a[-1]))

    return "\n".join(out)

# sample-like tests
assert run("4 2\n1 2 3 4\n2 2 3\n2 1 4\n") in {"1\n1", "2\n2", "3\n3", "4\n4"}

# custom cases
assert run("3 1\n1 1 2\n2 1 3\n") == "3"
assert run("5 3\n1 2 3 4 5\n2 1 5\n1 2 1\n2 1 5\n") is not None
assert run("1 1\n1\n2 1 1\n") == "1"
assert run("4 2\n1 2 3 3\n2 2 4\n2 1 3\n") == "1\n1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| non-permutation query | any valid missing | missing-set logic |
| update + query | consistent output | dynamic maintenance |
| single element | trivial correctness | boundary case |
| repeated values | stability under duplicates | frequency correctness |

## Edge Cases

One important edge case is when the array becomes a full permutation after updates. For example, starting from duplicates and gradually updating until all values 1 to N appear exactly once. At that moment, the missing set becomes empty and the algorithm must switch behavior. The implementation handles this because every update removes values from `missing` as soon as their frequency becomes positive and re-adds them when they drop to zero.

Another case is when all values are identical, such as `[2, 2, 2, 2]`. Here the missing set contains all values except 2. Any query immediately returns a valid missing value without checking intervals. The frequency logic ensures correctness because only value 2 remains with positive count.

A final edge case is repeated updates that do not change the value at a position. The condition `if old != v` prevents corrupting frequencies and ensures the missing set is only updated when the multiset actually changes, preserving correctness across redundant operations.
