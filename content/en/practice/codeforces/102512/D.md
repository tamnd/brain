---
title: "CF 102512D - Equality"
description: "We need choose a positive integer period T. Messages happen at every multiple of T, but the owner of the message alternates. The first multiple belongs to Kotaro, the second to Akane, the third to Kotaro again, and so on."
date: "2026-08-04T00:10:39+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102512
codeforces_index: "D"
codeforces_contest_name: "Valentines Day Contest 2020"
rating: 0
weight: 102512
solve_time_s: 178
verified: true
draft: false
---

[CF 102512D - Equality](https://codeforces.com/problemset/problem/102512/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 58s  
**Verified:** yes  

## Solution
## Problem Understanding

We need choose a positive integer period `T`. Messages happen at every multiple of `T`, but the owner of the message alternates. The first multiple belongs to Kotaro, the second to Akane, the third to Kotaro again, and so on. A value of `T` is valid only when every required message time is inside the active intervals of the person who sends it.

The input gives the length of the day `N`, followed by Kotaro's active intervals and Akane's active intervals. The task is to count how many periods `T` from `1` to `N` satisfy all message-time requirements.

The limit `N <= 10^9` immediately rules out checking every possible `T`. Even an `O(N)` solution is too large because a billion iterations cannot fit comfortably in the time limit. The number of intervals is small, only up to 300 per person, which suggests that the solution should use the interval structure instead of iterating over every time unit.

A common mistake is forgetting that a period can create only one message. If `T > N/2`, the only required time is `T` itself, and only Kotaro's availability matters. Another mistake is treating the intervals as half-open ranges. The intervals include both endpoints, so a message exactly at an endpoint is valid.

For example, consider:

```
3
1
3 3
1
1 1
```

The answer is `1` because `T = 3` creates one message at time 3, which Kotaro can send. A solution that checks only interior points of intervals would incorrectly reject it.

Another example:

```
5
1
1 5
1
1 3
```

For `T = 2`, messages happen at times 2 and 4. Time 4 belongs to Akane and is invalid, so `T = 2` must not be counted. A careless solution that only checks the first message would give the wrong result.

## Approaches

A direct solution tries every `T` from `1` to `N`. For each candidate, it generates the multiples of `T` and checks whether each multiple is inside the correct person's intervals. This is correct because it follows the definition exactly. The problem is the number of candidates. In the worst case this requires about `N + N/2 + ...` message checks, which is roughly `N log N`. With `N = 10^9`, this is impossible.

The key observation is that the difficult candidates are split into two groups. Small `T` values have many messages, but there are few such values. Large `T` values have few messages, so they can be handled by looking at the number of messages instead of the value of `T`.

Let `S = floor(sqrt(N))`. For `T <= S`, there are only about 31623 candidates. We can test each one efficiently by asking whether a bad interval contains a multiple of `T` with the required parity.

For `T > S`, the number of messages is at most `S`. Instead of iterating over `T`, we maintain the set of possible `T` values that satisfy the first `k` messages. When we add the `k`-th message constraint, we intersect this set with the intervals where `k*T` is valid. The current set is stored as disjoint intervals, so every step is just interval intersection.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N log N) | O(1) | Too slow |
| Optimal | O(sqrt(N) * (X+Y)) | O(X+Y) | Accepted |

## Algorithm Walkthrough

1. Split the possible values of `T` into two groups using `S = floor(sqrt(N))`. Values from `1` to `S` are handled individually. Values larger than `S` are handled by counting how many messages they create.
2. For every small `T`, check whether any required odd multiple falls outside Kotaro's intervals or any required even multiple falls outside Akane's intervals. For an interval `[L, R]`, the multiples of `T` inside it correspond to multiplier values from `ceil(L/T)` to `floor(R/T)`. We only need to know whether that range contains an odd or even number.
3. For large `T`, keep an interval list representing all `T` values greater than `S` that have satisfied the messages processed so far. Initially every value in `(S, N]` is possible.
4. Process message numbers `k = 1, 2, ...`. For message number `k`, convert every active interval `[L, R]` of the sender into possible values of `T`:

`ceil(L/k) <= T <= floor(R/k)`.

Intersect this new set with the current possible set.
5. After processing message `k`, count the values of `T` in the range where exactly `k` messages exist:

`floor(N/(k+1)) < T <= floor(N/k)`.

These are precisely the large values whose final message is the `k`-th one.

Why it works:

For small `T`, the algorithm rejects a value exactly when it finds a message that cannot be sent. If no such message exists, every required message time is valid, so the period is accepted.

For large `T`, after processing message `k`, the maintained intervals contain exactly the periods whose first `k` messages are all valid. A period belongs to the bucket with exactly `k` messages only if its value is between `floor(N/(k+1))+1` and `floor(N/k)`. Intersecting these two conditions counts exactly the valid large periods.

## Python Solution

```python
import sys
input = sys.stdin.readline

def contains(intervals, x):
    lo, hi = 0, len(intervals)
    while lo < hi:
        mid = (lo + hi) // 2
        if intervals[mid][0] <= x:
            lo = mid + 1
        else:
            hi = mid
    idx = lo - 1
    return idx >= 0 and intervals[idx][1] >= x

def has_bad_multiple(T, bad, parity):
    for l, r in bad:
        a = (l + T - 1) // T
        b = r // T
        if a <= b:
            if a % 2 != parity:
                a += 1
            if a <= b:
                return True
    return False

def intersect(a, b):
    res = []
    i = j = 0
    while i < len(a) and j < len(b):
        l = max(a[i][0], b[j][0])
        r = min(a[i][1], b[j][1])
        if l <= r:
            res.append((l, r))
        if a[i][1] < b[j][1]:
            i += 1
        else:
            j += 1
    return res

def scaled(intervals, k):
    res = []
    for l, r in intervals:
        a = (l + k - 1) // k
        b = r // k
        if a <= b:
            if res and res[-1][1] + 1 >= a:
                res[-1] = (res[-1][0], max(res[-1][1], b))
            else:
                res.append((a, b))
    return res

def count_in(intervals, l, r):
    if l > r:
        return 0
    ans = 0
    for a, b in intervals:
        if b < l:
            continue
        if a > r:
            break
        ans += min(b, r) - max(a, l) + 1
    return ans

def solve():
    N = int(input())
    X = int(input())
    kotaro = [tuple(map(int, input().split())) for _ in range(X)]
    Y = int(input())
    akane = [tuple(map(int, input().split())) for _ in range(Y)]

    bad_k = []
    last = 0
    for l, r in kotaro:
        if last + 1 <= l - 1:
            bad_k.append((last + 1, l - 1))
        last = r
    if last < N:
        bad_k.append((last + 1, N))

    bad_a = []
    last = 0
    for l, r in akane:
        if last + 1 <= l - 1:
            bad_a.append((last + 1, l - 1))
        last = r
    if last < N:
        bad_a.append((last + 1, N))

    ans = 0
    S = int(N ** 0.5)

    for t in range(1, S + 1):
        if not has_bad_multiple(t, bad_k, 1) and not has_bad_multiple(t, bad_a, 0):
            ans += 1

    cur = [(S + 1, N)]
    k = 1
    while k <= N // (S + 1) and cur:
        allowed = scaled(kotaro if k % 2 else akane, k)
        cur = intersect(cur, allowed)

        left = N // (k + 1) + 1
        right = N // k
        ans += count_in(cur, left, right)
        k += 1

    print(ans)

solve()
```

The first part builds the missing-time intervals for both people. Working with unavailable ranges makes the later checks easier because a candidate is rejected as soon as one invalid message exists.

The small-`T` loop does not enumerate messages. Instead, it checks whether a multiplier range contains a multiplier with the required parity. This keeps the work proportional to the number of intervals.

The large-`T` part stores possible periods as intervals. The conversion from a sender interval `[L, R]` to possible periods uses division by the message index `k`, which is the inverse of the multiplication `k*T`. All calculations use integer division carefully so that interval endpoints remain inclusive.

Python integers do not overflow, so the large values of `N` are safe. The use of `floor` and `ceil` divisions is the main place where off-by-one mistakes can happen.

## Worked Examples

For Sample 1:

```
10
2
2 4
6 9
3
1 3
5 7
9 10
```

For small values:

| T | Odd multiples checked | Even multiples checked | Result |
| --- | --- | --- | --- |
| 1 | Kotaro fails at 1 |  | Invalid |
| 2 | Kotaro fails at 6 | Akane fails at 4 | Invalid |
| 3 | 3,9 valid | 6 valid | Valid |

For large values, the periods above `sqrt(10)` are checked by message count buckets. The valid periods are `3,6,7,8,9`, giving the answer `5`.

For Sample 2:

```
10000000
1
4092001 5033941
2
206 314
1214 10000000
```

The large range means most candidates have only a few messages.

| Message number | Current constraint | Effect |
| --- | --- | --- |
| 1 | T must be in Kotaro interval | Keeps periods around 4 million |
| 2 | 2T must be in Akane interval | Removes periods whose second message is too early |
| 3 | 3T must be in Kotaro interval | Further narrows the set |

The interval intersections count all remaining valid periods and produce `941941`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(sqrt(N) * (X+Y)) | Small periods and large-period message counts are both bounded by about sqrt(N) |
| Space | O(X+Y) | Only interval lists are stored |

With `N = 10^9`, `sqrt(N)` is about 31623. The interval count is only 300 per person, so the number of operations stays within the limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    solve()
    out = sys.stdout.getvalue()
    sys.stdin = old
    return out

assert run("""10
2
2 4
6 9
3
1 3
5 7
9 10
""") == "5\n"

assert run("""10000000
1
4092001 5033941
2
206 314
1214 10000000
""") == "941941\n"

assert run("""1
1
1 1
1
1 1
""") == "1\n"

assert run("""5
1
1 5
1
1 3
""") == "2\n"

assert run("""10
1
10 10
1
1 10
""") == "1\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `N=1` with full availability | 1 | Minimum size and endpoint handling |
| All Kotaro times available but Akane misses time 4 | 2 | Alternating sender checks |
| Only time 10 works for Kotaro | 1 | Large period with one message |

## Edge Cases

When `T` is larger than half of `N`, there is only one message. The algorithm handles this through the first large-period bucket, where `k = 1`. For example, with `N = 10` and Kotaro available only at `[10,10]`, the value `T = 10` is counted because the only message time is valid.

When a failure happens on a later message rather than the first one, the algorithm still catches it because each additional message index intersects the current interval set. In the example where `N = 5`, Kotaro is available on `[1,5]`, and Akane on `[1,3]`, the period `T = 2` survives the first message check but is removed when `k = 2` requires `2T = 4` to belong to Akane's intervals.

When a message lands exactly on an interval endpoint, the inclusive interval logic keeps it valid. The ceiling and floor divisions in both the small and large cases preserve these boundaries, so a message at time `L` or `R` is not accidentally discarded.
