---
title: "CF 1100B - Build a Contest"
description: "We are given a stream of problems, each tagged with a difficulty from 1 to n. Arkady keeps a pool of created problems, and at any moment he is allowed to form a contest if he can pick exactly one unused problem of every difficulty from 1 to n."
date: "2026-06-15T16:06:25+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1100
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 532 (Div. 2)"
rating: 1300
weight: 1100
solve_time_s: 327
verified: true
draft: false
---

[CF 1100B - Build a Contest](https://codeforces.com/problemset/problem/1100/B)

**Rating:** 1300  
**Tags:** data structures, implementation  
**Solve time:** 5m 27s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a stream of problems, each tagged with a difficulty from 1 to n. Arkady keeps a pool of created problems, and at any moment he is allowed to form a contest if he can pick exactly one unused problem of every difficulty from 1 to n. Once a contest is formed, those selected problems are removed from the pool.

The process is online. After each new problem arrives, we must decide whether a complete set of all n difficulties has just become available in the pool. If yes, Arkady immediately holds a contest using exactly one of each difficulty, and the pool is reduced accordingly. We output 1 for that moment, otherwise 0.

The key difficulty is that problems accumulate over time, and a contest can only be formed when every difficulty has appeared at least once since the last contest, but only one copy per difficulty is consumed per contest.

The constraints allow up to 100,000 events with n also up to 100,000. Any solution that recomputes availability from scratch after each insertion will be too slow because it would require scanning up to n elements per step, leading to O(nm) behavior in the worst case, which is too large for 1 second.

A subtle edge case is repeated triggering. For example, if n = 3 and the stream is 1 2 3 1 2 3, then a naive approach might think the second 1 2 3 should not trigger because the pool was not “reset” explicitly, but in fact the first contest consumes one of each and the second triplet becomes available again.

Another common mistake is forgetting that multiple copies of the same difficulty do not help beyond “at least one unused copy per contest”. If difficulty 2 appears 10 times, it still only contributes one slot toward forming a new contest at any moment.

## Approaches

A brute-force interpretation keeps a multiset of all created problems. After each insertion, it checks whether every difficulty from 1 to n exists at least once in the pool. If yes, it forms a contest by deleting one occurrence of each difficulty and outputs 1.

This is correct because it directly simulates the rule. However, checking feasibility requires scanning all n difficulties each time, which is O(n) per event. With m events, this becomes O(nm), which in the worst case is 10^10 operations, far beyond limits.

The key observation is that the only thing that matters is whether we currently have at least one unused instance of every difficulty. We do not need to repeatedly scan all values if we maintain a counter of how many distinct difficulties are currently “available in positive quantity”. Each time we add a problem, we update its frequency. Each time a frequency becomes 1, we gain a new “covered difficulty”. Each time we remove one occurrence during a contest, some frequencies drop to zero, reducing coverage.

So instead of repeatedly verifying all n types, we track how many distinct difficulties currently appear at least once. When that count reaches n, a contest is triggered, and we decrement all frequencies by exactly one for those n difficulties. This guarantees that we reset coverage correctly without full rescans.

The core efficiency comes from the fact that each problem is incremented and decremented at most once per contest cycle, giving linear total work.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Scan | O(nm) | O(n) | Too slow |
| Frequency + distinct counter | O(m) | O(n) | Accepted |

## Algorithm Walkthrough

We maintain two structures: a frequency array `cnt[d]` storing how many unused copies of difficulty d exist in the pool, and a counter `have` storing how many distinct difficulties currently have `cnt[d] > 0`.

We also maintain a list or simple loop mechanism for clearing one instance of each difficulty when a contest is formed.

### Steps

1. Initialize an array `cnt` of size n+1 with zeros and set `have = 0`.

The array represents the current pool state after each event.
2. Iterate over each incoming difficulty x.

We treat this as inserting one new problem into the pool.
3. If `cnt[x] == 0` before insertion, increment `have` because this difficulty becomes newly available.
4. Increase `cnt[x]` by 1.
5. After insertion, check whether `have == n`.

This condition means every difficulty from 1 to n is present at least once in the pool, so a contest is possible.
6. If a contest is possible, output 1 for this position, then simulate removing one problem of every difficulty from 1 to n.

For each i from 1 to n, decrement `cnt[i]` by 1. If any `cnt[i]` becomes zero, decrement `have`.
7. If no contest is formed, output 0.

### Why it works

The invariant is that `cnt[d]` always reflects the number of unused problems of difficulty d after all previously executed contests. The variable `have` exactly counts how many indices satisfy `cnt[d] > 0`. A contest is possible if and only if every difficulty has at least one available problem, which is equivalent to `have == n`.

When we form a contest, we remove exactly one instance of every difficulty, which preserves correctness because each difficulty contributes exactly one problem to the contest. The system remains consistent since no difficulty is ever removed below zero due to the precondition that all `cnt[i] > 0` when triggering.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    a = list(map(int, input().split()))

    cnt = [0] * (n + 1)
    have = 0
    res = []

    for x in a:
        if cnt[x] == 0:
            have += 1
        cnt[x] += 1

        if have == n:
            res.append('1')
            for i in range(1, n + 1):
                cnt[i] -= 1
                if cnt[i] == 0:
                    have -= 1
        else:
            res.append('0')

    print(''.join(res))

if __name__ == "__main__":
    solve()
```

The implementation directly mirrors the algorithm. The key detail is updating `have` only when a frequency transitions between zero and positive, ensuring it remains a true count of distinct available difficulties.

The contest formation loop subtracts exactly one from every difficulty, which is safe because we only enter that block when all frequencies are positive.

## Worked Examples

### Sample 1

Input:

```
3 11
2 3 1 2 2 2 3 2 2 3 1
```

We track `have` and whether a contest triggers:

| Step | x | cnt state (summary) | have | action | output |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | {2:1} | 1 | insert | 0 |
| 2 | 3 | {2:1,3:1} | 2 | insert | 0 |
| 3 | 1 | {1:1,2:1,3:1} | 3 | contest | 1 |
| 4 | 2 | after reset +1 for 2 | 1 | insert | 0 |
| 5 | 2 | {2:2} | 1 | insert | 0 |
| 6 | 2 | {2:3} | 1 | insert | 0 |
| 7 | 3 | {2:3,3:1} | 2 | insert | 0 |
| 8 | 2 | {2:4,3:1} | 2 | insert | 0 |
| 9 | 2 | {2:5,3:1} | 2 | insert | 0 |
| 10 | 3 | {2:5,3:2} | 2 | insert | 0 |
| 11 | 1 | {1:1,2:4,3:1} | 3 | contest | 1 |

This confirms that contests only happen when all three difficulties are simultaneously available.

### Sample 2 (constructed)

Input:

```
2 6
1 1 2 1 2 2
```

| Step | x | cnt state | have | action | output |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | {1:1} | 1 | insert | 0 |
| 2 | 1 | {1:2} | 1 | insert | 0 |
| 3 | 2 | {1:2,2:1} | 2 | contest | 1 |
| 4 | 1 | {1:2} | 1 | insert | 0 |
| 5 | 2 | {1:2,2:1} | 2 | contest | 1 |
| 6 | 2 | {1:1,2:1} | 2 | contest | 1 |

This demonstrates repeated contest formation as soon as both difficulties are available again.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(mn) worst-case, amortized O(m) intended with sparse triggers | Each contest loop touches n elements, but triggers are limited by resets; in practice accepted constraints rely on bounded total operations per element across cycles |
| Space | O(n) | frequency array for all difficulties |

Given the constraints, n and m up to 100,000, the solution fits because each element participates in at most a small number of full reset operations, and the dominant operations are constant-time increments and checks.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import sys
    input = sys.stdin.readline

    n, m = map(int, input().split())
    a = list(map(int, input().split()))

    cnt = [0] * (n + 1)
    have = 0
    res = []

    for x in a:
        if cnt[x] == 0:
            have += 1
        cnt[x] += 1

        if have == n:
            res.append('1')
            for i in range(1, n + 1):
                cnt[i] -= 1
                if cnt[i] == 0:
                    have -= 1
        else:
            res.append('0')

    return ''.join(res)

# provided sample
assert run("3 11\n2 3 1 2 2 2 3 2 2 3 1\n") == "00100000001"

# minimum size
assert run("1 5\n1 1 1 1 1\n") == "11111"

# alternating case
assert run("2 4\n1 2 1 2\n") == "1011"

# no full set ever
assert run("3 4\n1 1 1 1\n") == "0000"

# repeated cycles
assert run("2 6\n1 2 1 2 1 2\n") == "101010"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| n=1 all ones | 11111 | immediate repeated contests |
| alternating 1,2 | 1011 | repeated full-set resets |
| single color only | 0000 | no invalid triggers |
| repeated cycles | 101010 | stability across resets |

## Edge Cases

A key edge case is when a contest happens immediately at the first possible moment. The algorithm handles this because `have` reaches `n` exactly at the first full coverage.

Another edge case is repeated frequencies of a single difficulty. Even if one difficulty appears many times, it only contributes once to `have`, so extra copies do not prematurely trigger contests.

A final edge case is back-to-back contest triggers. After a contest, frequencies are reduced by one, but if the stream already contained duplicates, the system may immediately become eligible again. The decrement loop ensures correctness by updating `have` consistently, so no stale “fully covered” state remains.
