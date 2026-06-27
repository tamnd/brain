---
title: "CF 105028B - Sequence Duplication"
description: "We are given two sequences. The first sequence a is the pattern we want to match, and the second sequence b is a base sequence that is repeated endlessly, but only a finite number of times. If we repeat b exactly k times, we get a long sequence made of k consecutive copies of b."
date: "2026-06-28T01:36:57+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105028
codeforces_index: "B"
codeforces_contest_name: "TheForces Round #28 (Epic-Forces)"
rating: 0
weight: 105028
solve_time_s: 79
verified: false
draft: false
---

[CF 105028B - Sequence Duplication](https://codeforces.com/problemset/problem/105028/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 19s  
**Verified:** no  

## Solution
## Problem Understanding

We are given two sequences. The first sequence `a` is the pattern we want to match, and the second sequence `b` is a base sequence that is repeated endlessly, but only a finite number of times. If we repeat `b` exactly `k` times, we get a long sequence made of `k` consecutive copies of `b`.

The task is to find the smallest number of repetitions `k` such that `a` can be found as a subsequence inside this repeated sequence. If even infinite repetition of `b` cannot form `a` as a subsequence, we must return `-1`.

A subsequence means we scan left to right and pick elements without reordering, possibly skipping elements.

The key difficulty is that `k` is not given. We must determine how many full passes over `b` are required to “consume” all elements of `a` in order.

The constraints allow up to 200,000 total elements across all test cases. That immediately rules out any approach that tries to explicitly build `dup(b, k)` or simulate matching against growing copies of `b` for many candidate values of `k`. Anything worse than linear or near-linear per test will fail.

A subtle edge case appears when some element of `a` never appears in `b`. For example, `a = [1]`, `b = [2, 3]`. No amount of repetition helps, and the answer must be `-1`. A naive greedy scan that resets incorrectly might still loop and falsely assume progress is possible unless it explicitly checks reachability in `b`.

Another tricky case happens when matching `a` requires restarting in the middle of a copy of `b`. For example, `b = [1, 2, 3]`, `a = [2, 3, 1, 2]`. We may finish a full pass of `b` before completing `a`, so we need multiple cycles, and we must count how many times we wrap around `b`.

## Approaches

A direct simulation approach is straightforward. We try to match `a` against `b`, moving a pointer in `a` whenever we find a matching element in `b`. Once we reach the end of `b`, we increment a counter for how many full copies we have used and restart scanning `b` from the beginning. We continue until either `a` is fully matched or we detect that progress is impossible.

This works because subsequence matching is greedy in nature: whenever we can match the next element of `a`, we should match it at the earliest possible position in `b`.

However, the naive implementation becomes inefficient if we restart scanning `b` too many times and repeatedly scan from scratch. In the worst case, each element of `a` might require a full traversal of `b`, leading to O(nm) behavior, which is too slow when both arrays are large.

The key observation is that the behavior inside each repetition of `b` is identical. Instead of repeatedly scanning `b`, we can preprocess positions of each value in `b` and “jump” to the next valid occurrence using binary search. This turns each step of matching `a` into a logarithmic or amortized constant operation.

We maintain a pointer into a virtual infinite `b`. For each `a[i]`, we find the next occurrence in `b` that is strictly after our current position within the cycle. If no such occurrence exists, we jump to the next cycle and continue from the first occurrence in `b`, incrementing `k`.

This reduces the problem to efficiently finding next positions in a cyclic array.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n · k · m) | O(1) | Too slow |
| Preprocessed Position + Binary Search | O((n + m) log m) | O(m) | Accepted |

## Algorithm Walkthrough

We process each test case independently.

1. We build a mapping from each value in `b` to the list of indices where it appears. This allows fast lookup of where we can place each element of `a`. The ordering of indices is crucial because we need the next valid position.
2. We initialize two variables: `pos`, which tracks our current index inside one copy of `b` (starting at 0), and `k`, which counts how many full copies of `b` we have used so far (starting at 1 if matching is possible).
3. We iterate through each element `x` in `a`. For each `x`, we consult its list of positions in `b`. If this list is empty, we immediately conclude the answer is `-1` because `x` never appears in `b`.
4. We try to find the smallest index in the list that is strictly greater than `pos`. This is the next place we can match `x` without violating order inside the current copy of `b`. If such a position exists, we update `pos` to it and continue.
5. If no such position exists, it means we must move to the next repetition of `b`. We increment `k`, reset `pos` to the first occurrence of `x` in `b`, and continue. This reflects wrapping around to a new copy of `b`.
6. After processing all elements of `a`, the final value of `k` is the minimum number of copies needed.

### Why it works

At every step, we always place each element of `a` at the earliest possible valid position in the repeated structure. This greedy placement ensures we never artificially delay matches and therefore never increase the number of required repetitions unnecessarily. Any alternative placement that delays a match would only push us further in `b` and potentially require an additional cycle earlier, never fewer.

The invariant is that after processing `a[i]`, `pos` is the position of `a[i]` in the earliest possible copy of `b` consistent with a valid subsequence construction, and `k` counts exactly how many times we have crossed the boundary of `b`.

## Python Solution

```python
import sys
input = sys.stdin.readline
from bisect import bisect_right

def solve():
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))

        pos_map = {}
        for i, x in enumerate(b):
            if x not in pos_map:
                pos_map[x] = []
            pos_map[x].append(i)

        # feasibility check
        for x in a:
            if x not in pos_map:
                print(-1)
                break
        else:
            k = 1
            pos = -1  # current index in b
            for x in a:
                lst = pos_map[x]
                idx = bisect_right(lst, pos)
                if idx < len(lst):
                    pos = lst[idx]
                else:
                    k += 1
                    pos = lst[0]
            print(k)

if __name__ == "__main__":
    solve()
```

The code first builds `pos_map`, grouping indices of each value in `b`. This structure is what allows us to avoid scanning `b` repeatedly.

The `pos` variable tracks where we last matched inside a copy of `b`. Using `bisect_right`, we efficiently find the next valid occurrence. If none exists, we simulate moving to the next repetition by incrementing `k` and restarting from the first occurrence of that value.

A subtle detail is the initial value `pos = -1`, which ensures the first element can match anywhere in the first copy of `b`.

## Worked Examples

### Example 1

Consider `a = [1, 2, 3]`, `b = [1, 2]`.

| Step | x | pos before | chosen index | k | pos after |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | -1 | 0 | 1 | 0 |
| 2 | 2 | 0 | 1 | 1 | 1 |
| 3 | 3 | 1 | none | - | impossible |

We fail at `3` because it does not exist in `b`, so output is `-1`.

This confirms that missing elements are detected immediately and prevent incorrect continuation.

### Example 2

Let `a = [2, 3, 1, 2]`, `b = [1, 2, 3]`.

| Step | x | pos before | chosen index | k | pos after |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | -1 | 1 | 1 | 1 |
| 2 | 3 | 1 | 2 | 1 | 2 |
| 3 | 1 | 2 | 0 (next cycle) | 2 | 0 |
| 4 | 2 | 0 | 1 | 2 | 1 |

We need 2 copies of `b`.

This trace shows why wrap-around is necessary and how the algorithm correctly counts full cycles only when required.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + m) log m) | Each element of `a` performs a binary search in its list in `b` |
| Space | O(m) | Storage of index lists for elements of `b` |

The total input size across all test cases is bounded by 200,000, so a log-linear solution easily fits within time limits. Memory usage is linear in `m`, which is also safe under the constraints.

## Test Cases

```python
import sys, io
from bisect import bisect_right

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    import sys
    input = sys.stdin.readline

    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))

        pos_map = {}
        for i, x in enumerate(b):
            pos_map.setdefault(x, []).append(i)

        for x in a:
            if x not in pos_map:
                print(-1)
                break
        else:
            k = 1
            pos = -1
            for x in a:
                lst = pos_map[x]
                idx = bisect_right(lst, pos)
                if idx < len(lst):
                    pos = lst[idx]
                else:
                    k += 1
                    pos = lst[0]
            print(k)

    return out.getvalue().strip()

# custom tests

# all elements exist, single cycle
assert run("1\n3 3\n1 2 3\n1 2 3\n") == "1"

# needs multiple cycles
assert run("1\n4 3\n2 3 1 2\n1 2 3\n") == "2"

# impossible case
assert run("1\n2 2\n1 2\n3 4\n") == "-1"

# repeated wrapping
assert run("1\n5 2\n1 2 1 2 1\n1 2\n") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 3 / 1 2 3` | `1` | single pass suffices |
| `2 3 1 2 / 1 2 3` | `2` | wrap-around counting |
| `1 2 / 3 4` | `-1` | impossibility detection |
| `1 2 1 2 1 / 1 2` | `3` | repeated cycles handling |

## Edge Cases

A critical edge case is when the first element of `a` is not present in `b`. For example, `a = [5]`, `b = [1, 2, 3]`. The algorithm checks `pos_map` before any matching begins, so it immediately returns `-1`. Without this check, a naive pointer approach could loop indefinitely or incorrectly reset cycles.

Another case is when `a` is entirely contained within a single traversal of `b`, such as `a = [1, 3]`, `b = [1, 2, 3, 4]`. Here `k` remains `1` because `pos` never requires wrapping. The algorithm never increments `k`, since every next occurrence is found in the current cycle.

A final case is heavy repetition, such as `a = [1, 1, 1, 1]`, `b = [1]`. Each element forces either reuse of the same index or cycle increments. The algorithm correctly increases `k` each time no forward occurrence exists, producing `k = 4`, which matches the number of required repetitions.
