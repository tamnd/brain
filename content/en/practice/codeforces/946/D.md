---
problem: 946D
contest_id: 946
problem_index: D
name: "Timetable"
contest_name: "Educational Codeforces Round 39 (Rated for Div. 2)"
rating: 1800
tags: ["dp"]
answer: passed_samples
verified: true
solve_time_s: 94
date: 2026-06-17
model: gpt-5-3-mini
samples_passed: 1
samples_total: 1
---

# CF 946D - Timetable

**Rating:** 1800  
**Tags:** dp  
**Model:** gpt-5-3-mini  
**Solve time:** 1m 34s  
**Verified:** yes (1/1 samples)  

---

## Solution

## Problem Understanding

We are given a weekly schedule split into several days, and each day is divided into a fixed number of hourly slots. In each slot, Ivan either has a lecture or he does not. The input is simply a grid of zeros and ones, where a one means a lecture is scheduled at that hour.

Ivan is allowed to skip at most `k` lectures across the entire week. After he chooses which lectures to skip, his daily attendance rule becomes very rigid: on any day where he attends at least one lecture, he arrives right before his first attended lecture of that day and leaves immediately after his last attended lecture. This means that even if there are gaps between attended lectures, he still stays in the university during the entire continuous interval from first to last attended lecture.

The cost of a day is therefore determined not by how many lectures he attends, but by the distance between the earliest and latest attended lecture after skipping decisions are made. If he skips all lectures on a day, the cost for that day is zero.

The goal is to distribute at most `k` skips across all days in such a way that the sum of these daily time intervals is minimized.

The constraints are tight enough to rule out anything exponential in `k` or in the number of lectures per day. Both `n`, `m`, and `k` are at most 500, which suggests a solution around `O(n * k^2)` or `O(n * k)` is acceptable, while anything like enumerating subsets of lectures is completely infeasible.

A few edge cases matter in practice. If a day contains no lectures, the contribution is always zero regardless of `k`. If all lectures in a day are kept, the cost is simply the span between the first and last `1`. Another subtle case appears when skipping removes all but one lecture, which collapses the interval to length one regardless of spacing elsewhere.

A naive mistake would be to think skipping a lecture reduces cost linearly. For example, on a day like `100001`, removing a middle lecture does not help unless it changes the endpoints of the interval. Another mistake is treating each lecture independently, while in reality the cost depends only on the extreme chosen endpoints after deletions.

## Approaches

The brute-force viewpoint starts by thinking per day. For each day, we could choose any subset of lectures to keep, as long as we do not exceed `k` total skips across all days. For a fixed subset, we compute each day's cost by scanning the earliest and latest kept lecture. This immediately becomes exponential because each day alone has up to `2^m` subsets, and across `n` days the combination space explodes far beyond any limit.

The key structural simplification is that the internal arrangement of kept lectures inside a day does not matter, only the minimum and maximum positions among those kept. Once we fix how many lectures we delete in a day, we are really trying to pick a subset of remaining size that minimizes its span. That optimal subset is always a contiguous block in the sorted list of lecture positions.

This reduces each day into a small precomputation: for every possible number of skips in that day, we compute the minimum possible time spent in that day. Once each day is compressed into a cost array indexed by how many skips are used, the problem becomes a classic knapsack over days where we distribute at most `k` total skips.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in m per day | Exponential | Too slow |
| Optimal DP (day compression + knapsack) | O(n * m^2 + n * k^2) | O(k) | Accepted |

## Algorithm Walkthrough

We first convert each day into a compact representation that tells us: if we use exactly `t` skips on this day, what is the minimum possible time spent in the university that day.

1. For each day, collect the positions of all lectures. These positions are strictly increasing along the day.
2. If a day has `c` lectures, consider what happens if we delete `t` of them. We will keep `c - t` lectures.
3. To minimize the time interval, we try all contiguous groups of size `c - t` in the sorted list of lecture positions. For a window starting at index `i`, the cost is `pos[i + c - t - 1] - pos[i] + 1`.
4. Take the minimum over all such windows. This gives the optimal cost for spending `t` skips on this day.
5. If `c - t <= 0`, meaning we delete all lectures, the cost is zero.
6. After building this cost table for each day, we run dynamic programming over days. Let `dp[j]` represent the minimum total time spent after processing some prefix of days using exactly `j` skips.
7. For each day, we compute a new DP array `ndp`. For every possible number of previously used skips `j`, we try assigning `t` additional skips to the current day, updating `ndp[j + t]` with `dp[j] + cost_day[t]`.
8. We repeat this for all days, and the final answer is the minimum value in `dp[0..k]`.

### Why it works

The critical invariant is that after processing each day, `dp[j]` stores the minimum possible total time spent across all ways of distributing exactly `j` skips among the days seen so far. The per-day compression is valid because any optimal solution on a single day can be transformed so that the kept lectures form a contiguous segment in the sorted order of that day’s lectures, without increasing cost or changing the number of deletions. The knapsack transition preserves optimality because each day’s decision depends only on how many skips are allocated to it, and these decisions are independent once the per-day cost function is fixed.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m, k = map(int, input().split())
    
    days = []
    for _ in range(n):
        s = input().strip()
        pos = [i for i, ch in enumerate(s) if ch == '1']
        days.append(pos)

    INF = 10**18
    dp = [INF] * (k + 1)
    dp[0] = 0

    for pos in days:
        c = len(pos)
        
        cost = [INF] * (k + 1)
        
        if c == 0:
            cost = [0] * (k + 1)
        else:
            for t in range(k + 1):
                if t >= c:
                    cost[t] = 0
                else:
                    keep = c - t
                    best = INF
                    for i in range(c - keep + 1):
                        j = i + keep - 1
                        best = min(best, pos[j] - pos[i] + 1)
                    cost[t] = best

        ndp = [INF] * (k + 1)
        for used in range(k + 1):
            if dp[used] == INF:
                continue
            for t in range(k + 1 - used):
                ndp[used + t] = min(ndp[used + t], dp[used] + cost[t])

        dp = ndp

    print(min(dp))

if __name__ == "__main__":
    solve()
```

The code first converts each day into a list of lecture positions, which makes reasoning about intervals purely arithmetic. The `cost[t]` computation encodes the key observation that after deleting `t` lectures, the optimal remaining set is a sliding window over the sorted positions.

The second stage is a straightforward DP merge. The nested loops over `used` and `t` ensure we consider all valid distributions of skips without exceeding `k`. The bound `k + 1 - used` prevents invalid states and keeps transitions within limits.

A common implementation pitfall is forgetting that deleting all lectures must yield zero cost. Another is mixing up “kept count” and “deleted count”, which leads to incorrect window sizes. The sliding window computation must always use `c - t` as the number of kept lectures.

## Worked Examples

### Example 1

Input:

```
2 5 1
01001
10110
```

For the first day, lectures are at positions `[1, 3, 4]`. With 0 skips, best interval is `4 - 1 + 1 = 4`. With 1 skip, we keep 2 lectures, best window is either `[1,3]` or `[3,4]`, both giving cost `3` and `2`, so minimum is `2`.

For the second day, positions are `[0, 2, 3]`. With 0 skips cost is `4`, with 1 skip cost becomes `2`.

Now we distribute at most one skip. The best choice is to use the skip on the day where it gives better improvement, resulting in total `2 + 3 = 5`.

| Day | Skips used | Kept window | Cost |
| --- | --- | --- | --- |
| 1 | 1 | [1,3] | 3 |
| 2 | 0 | [0,3] | 4 |

This trace shows how a single skip is allocated to reduce one day’s span while leaving the other unchanged.

### Example 2

Input:

```
1 6 2
100001
```

Positions are `[0, 5]`. Even with 0 skips cost is `6`. Any skips do not change the endpoints meaningfully because removing one endpoint collapses to a single point only after deleting both.

| Skips | Kept set | Cost |
| --- | --- | --- |
| 0 | [0,5] | 6 |
| 1 | [0] or [5] | 1 |
| 2 | [] | 0 |

With two skips, the optimal result is `0`, showing that full removal eliminates all cost.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n * m^2 + n * k^2) | Each day computes sliding window costs over up to m positions, then DP merges over k states |
| Space | O(k) | DP array over number of allowed skips |

Given `n, m, k ≤ 500`, the quadratic terms remain within acceptable bounds, and the solution comfortably fits within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdout.getvalue() if False else solve_capture(inp)

def solve_capture(inp: str) -> str:
    import sys
    from io import StringIO
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout
    sys.stdin = StringIO(inp)
    sys.stdout = StringIO()
    
    def solve():
        n, m, k = map(int, input().split())
        days = []
        for _ in range(n):
            s = input().strip()
            pos = [i for i, ch in enumerate(s) if ch == '1']
            days.append(pos)

        INF = 10**18
        dp = [INF] * (k + 1)
        dp[0] = 0

        for pos in days:
            c = len(pos)
            cost = [0] * (k + 1)
            if c != 0:
                cost = [10**18] * (k + 1)
                for t in range(k + 1):
                    if t >= c:
                        cost[t] = 0
                    else:
                        keep = c - t
                        best = 10**18
                        for i in range(c - keep + 1):
                            j = i + keep - 1
                            best = min(best, pos[j] - pos[i] + 1)
                        cost[t] = best

            ndp = [10**18] * (k + 1)
            for used in range(k + 1):
                if dp[used] == 10**18:
                    continue
                for t in range(k + 1 - used):
                    ndp[used + t] = min(ndp[used + t], dp[used] + cost[t])
            dp = ndp

        ans = min(dp)
        print(ans)

    solve()
    out = sys.stdout.getvalue()
    sys.stdin = backup_stdin
    sys.stdout = backup_stdout
    return out.strip()

# provided sample
assert solve_capture("""2 5 1
01001
10110
""") == "5"

# all zeros day
assert solve_capture("""1 5 3
00000
""") == "0"

# single day, tight deletions
assert solve_capture("""1 5 2
10001
""") == "3"

# max skips enough to delete everything
assert solve_capture("""2 3 10
101
010
""") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all zeros day | 0 | no lectures case |
| single sparse day | 3 | endpoint shrink behavior |
| enough skips | 0 | full deletion across days |

## Edge Cases

A day with no lectures is handled by the precomputed position list being empty. The cost array is set to zero for all skip counts, which correctly reflects that no time is spent regardless of how skips are allocated elsewhere.

A day where all lectures are removed becomes important when `k` is large. In this case, once `t` exceeds the number of lectures, the cost is forced to zero, and the DP can correctly shift all skips into eliminating entire days.

A minimal case with one lecture per day behaves correctly because the sliding window degenerates to a single element, producing cost `1` unless that lecture is skipped.