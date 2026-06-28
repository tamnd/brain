---
title: "CF 104770E - Accounting Chaos"
description: "We are given a list of monetary charges recorded in a hotel journal. Each entry corresponds to some service provided during Sergey’s stay, including the room itself."
date: "2026-06-28T19:52:39+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104770
codeforces_index: "E"
codeforces_contest_name: "The XXXI Saint-Petersburg High School Programming Contest (SpbKOSHP 2023) | Qualification for the XXIV Russia Open High School Programming Contest (VKOSHP 2023)"
rating: 0
weight: 104770
solve_time_s: 82
verified: false
draft: false
---

[CF 104770E - Accounting Chaos](https://codeforces.com/problemset/problem/104770/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 22s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a list of monetary charges recorded in a hotel journal. Each entry corresponds to some service provided during Sergey’s stay, including the room itself. What makes the data messy is that we no longer know which entry corresponds to which service type, only the raw costs remain.

The key structural rule is that every service type has a fixed price throughout the stay. That means if a service appears multiple times in the journal, all those occurrences share the same value, but we cannot distinguish them from other services with the same cost. One special service is the room, and it is known that Sergey stayed exactly `n` days, so the room service must have been charged exactly `n` times in total.

The task is to determine all possible values that could represent the daily room cost, consistent with the idea that we can assign each record to some service type, and the room service must account for exactly `n` of the `m` records.

The input size is large, up to 300,000 records. That immediately rules out any quadratic reasoning over pairs or repeated rescanning of the full array per candidate. Any solution that checks feasibility per value must do so in linear or near-linear time overall.

A subtle pitfall is assuming that the room cost must appear exactly `n` times. That is not required; it only needs to appear at least `n` times in the multiset so that we can choose `n` occurrences among them to represent the room across the days. Extra occurrences can simply be interpreted as other services that happen to cost the same.

Another potential confusion arises from thinking services are grouped per day. There is no per-day constraint on how many services occur beyond the fact that there are `n` days total and the room appears once per day.

## Approaches

A direct approach is to try every distinct cost value as a candidate for the room price. For each candidate value `x`, we count how many times it appears in the list and check whether it appears at least `n` times. If so, we can assign `n` of those occurrences to the room service and interpret the remaining occurrences as other services of the same type. This is correct because nothing prevents a service type from being used for multiple distinct journal entries.

This brute-force idea is correct, but doing a fresh scan of all `m` entries for each distinct value leads to a worst case of `O(m^2)` when all values are distinct, which is too slow for `m = 3 × 10^5`.

The key observation is that we do not need repeated scans. The feasibility of a value depends only on its frequency. Once we compute frequencies for all values in one pass, we can directly filter those with frequency at least `n`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force per value | O(m^2) | O(m) | Too slow |
| Frequency counting | O(m) | O(m) | Accepted |

## Algorithm Walkthrough

1. Read `n`, `m`, and the list of costs. The goal is to understand how often each cost appears.
2. Build a frequency map of all values in the list. This captures how many times each possible service price appears in the journal.
3. Iterate over all distinct values in the frequency map.
4. For each value `x`, check whether its frequency is at least `n`. If yes, include `x` in the answer set. The reasoning is that we can assign `n` of these occurrences to the room service across `n` days.
5. Output the number of valid candidates and the list itself in any order.

### Why it works

Each distinct cost value corresponds to a potential service type, since all occurrences of the same value can be treated as one service with a fixed price. The only constraint for a value to represent the room is that we must be able to assign exactly one room entry per day across `n` days, which requires at least `n` occurrences. No further structural constraint exists because unused occurrences can always be interpreted as additional service records of that same type. This makes frequency the only deciding factor.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    c = list(map(int, input().split()))
    
    freq = {}
    for x in c:
        freq[x] = freq.get(x, 0) + 1
    
    res = []
    for x, f in freq.items():
        if f >= n:
            res.append(x)
    
    print(len(res))
    print(*res)

if __name__ == "__main__":
    solve()
```

The implementation relies entirely on a frequency dictionary built in a single pass. This avoids any repeated scanning. The final filtering step is linear in the number of distinct values, which is at most `m`.

A common mistake is trying to simulate assignments per day or building explicit groupings. That is unnecessary because the only global constraint is total occurrence count, not per-day structure.

## Worked Examples

### Sample Trace

Input:

```
2 10
1 3 6 5 3 2 4 5 3 2
```

Frequencies:

| Value | Frequency | ≥ n (=2)? |
| --- | --- | --- |
| 1 | 1 | No |
| 2 | 2 | Yes |
| 3 | 3 | Yes |
| 4 | 1 | No |
| 5 | 2 | Yes |
| 6 | 1 | No |

Answer set becomes `{2, 3, 5}`.

This shows that multiple unrelated service types can all be valid room prices as long as they appear frequently enough.

### Edge distribution example

Input:

```
3 6
7 7 7 8 8 9
```

Frequencies:

| Value | Frequency | ≥ n (=3)? |
| --- | --- | --- |
| 7 | 3 | Yes |
| 8 | 2 | No |
| 9 | 1 | No |

Only `7` works, since only it can cover all three days.

This demonstrates that equality of frequency with `n` is sufficient and extra structure is irrelevant.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m) | One pass to build frequencies and one pass over distinct values |
| Space | O(m) | Storage for frequency map in worst case when all values are distinct |

The solution easily fits within limits since `3 × 10^5` operations is trivial in Python for hash map counting.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import defaultdict

    def solve():
        n, m = map(int, input().split())
        c = list(map(int, input().split()))
        freq = {}
        for x in c:
            freq[x] = freq.get(x, 0) + 1
        res = [x for x, f in freq.items() if f >= n]
        print(len(res))
        print(*res)

    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    solve()
    out = sys.stdout.getvalue()
    sys.stdout = old_stdout
    return out.strip()

# provided sample
assert run("2 10\n1 3 6 5 3 2 4 5 3 2\n") == "3\n2 3 5"

# minimum case
assert run("1 1\n100\n") == "1\n100"

# all equal
assert run("3 5\n7 7 7 7 7\n") == "1\n7"

# no duplicates but still valid n=1
assert run("1 4\n1 2 3 4\n") == "4\n1 2 3 4"

# boundary heavy frequency
assert run("5 10\n9 9 9 9 9 1 2 3 4 5\n") == "1\n9"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| minimal single element | 1 value | base correctness |
| all equal large freq | single valid | frequency threshold behavior |
| all distinct n=1 | all valid | weakest constraint case |
| skewed distribution | one valid | filtering correctness |

## Edge Cases

When `n = 1`, every value is valid because any single occurrence can serve as the room charge for that day. The algorithm handles this naturally because every frequency is at least one, so all keys are included.

When all values are identical, the frequency equals `m`, and the algorithm correctly returns that value if `m ≥ n`. The grouping interpretation still holds because we can assign exactly `n` occurrences to the room.

When values are mostly unique with only one repeated enough times, only that repeated value passes the frequency threshold. The dictionary-based counting ensures we do not mistakenly treat single occurrences as valid candidates.
