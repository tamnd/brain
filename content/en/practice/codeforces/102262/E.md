---
title: "CF 102262E - \u041a\u0440\u0438\u0442\u0438\u0447\u0435\u0441\u043a\u0430\u044f \u0443\u044f\u0437\u0432\u0438\u043c\u043e\u0441\u0442\u044c"
description: "Each cluster is a single indivisible update job. Cluster i contains xi servers, so processing it takes exactly xi units of time. Its allowed time interval starts at ai and ends at ai + xi."
date: "2026-08-17T20:19:58+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102262
codeforces_index: "E"
codeforces_contest_name: "\u0427\u0435\u043c\u043f\u0438\u043e\u043d\u0430\u0442 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e - \u0444\u0438\u043d\u0430\u043b (\u042f\u043d\u0434\u0435\u043a\u0441)"
rating: 0
weight: 102262
solve_time_s: 83
verified: true
draft: false
---

[CF 102262E - \u041a\u0440\u0438\u0442\u0438\u0447\u0435\u0441\u043a\u0430\u044f \u0443\u044f\u0437\u0432\u0438\u043c\u043e\u0441\u0442\u044c](https://codeforces.com/problemset/problem/102262/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 23s  
**Verified:** yes  

## Solution
## Problem Understanding

Each cluster is a single indivisible update job. Cluster `i` contains `x_i` servers, so processing it takes exactly `x_i` units of time. Its allowed time interval starts at `a_i` and ends at `a_i + x_i`. Since the allowed interval has exactly the same length as the required processing time, there is actually only one possible schedule for that cluster: it occupies the whole interval `[a_i, a_i + x_i]`.

We may choose any subset of clusters, but their intervals must not overlap because only one cluster can be updated at a time. If two chosen intervals meet at an endpoint, that is valid: one update can finish at time `t` and the next can start at time `t`.

The value of choosing cluster `i` is `x_i`, because all `x_i` servers in that cluster become updated. The task is thus to choose a maximum-weight set of non-overlapping intervals and output both its total weight and the corresponding zero-based cluster indices.

With `n` up to `10^5`, trying every subset would require up to `2^100000` possibilities, which is completely impossible. Even a quadratic algorithm performs around `10^10` operations in the worst case, far beyond what a one-second limit can handle. We need an `O(n log n)` or similarly efficient solution.

There are several boundary cases that can make an otherwise reasonable implementation wrong. First, intervals that touch must be considered compatible. For example,

```
21 23 2
```

gives intervals `[1,3]` and `[3,5]`. Both can be selected, so the answer is `4` with indices `0 1`. A predecessor search using `< a_i` instead of `<= a_i` would incorrectly reject the second cluster.

Second, the longest individual interval is not necessarily the best answer. For

```
31 44 26 3
```

the intervals are `[1,5]`, `[4,6]`, and `[6,9]`. Choosing clusters `1` and `2` gives `2 + 3 = 5`, which is better than choosing cluster `0` with value `4`. A greedy strategy that simply takes the longest available cluster can therefore fail.

Third, the answer can contain no more than one cluster even when many clusters exist. For

```
31 51 51 5
```

all three intervals are identical, so only one can be processed. The correct maximum is `5`, not `15`.

Finally, all time and answer values can reach roughly `10^14` when summed over `10^5` clusters. Python integers handle this automatically, but a C++ implementation would need `long long`.

## Approaches

The direct brute-force approach considers every subset of clusters. For each subset, we could sort or otherwise inspect its selected intervals, check whether they overlap, and calculate the number of updated servers. This is correct because every possible set of clusters is examined, so the best feasible set must eventually be found.

The problem is the number of subsets. With `n = 10^5`, there are `2^100000` subsets. Even before checking whether those subsets are feasible, this is astronomically too large.

A more useful brute-force dynamic programming formulation sorts the intervals by their ending times. For every interval, we can look at every earlier interval to find the last compatible one. This gives the familiar weighted interval scheduling recurrence, but finding the predecessor by scanning all previous intervals takes `O(n^2)` time. At `n = 10^5`, that is about `5 * 10^9` predecessor checks in the worst case, which is still too slow.

The key observation is that after sorting intervals by their right endpoint, the only information we need from the previous intervals is the best answer whose last interval ends no later than the current interval's start. Since all previous right endpoints are sorted, that predecessor can be found with binary search.

Let an interval be represented as `(start, end, weight, index)`, where

`start = a_i`

`end = a_i + x_i`

`weight = x_i`.

After sorting by `end`, define `dp[i]` as the maximum number of servers that can be updated using the first `i` sorted intervals. For the next interval, there are exactly two possibilities. We either skip it, keeping `dp[i]`, or take it and combine its weight with the best solution ending at or before its start. If `p` is the number of intervals whose end is at most the current start, the recurrence is

`dp[i + 1] = max(dp[i], dp[p] + x_i)`.

Binary search finds `p` in `O(log n)`, reducing the complete algorithm to `O(n log n)`.

The same dynamic programming also lets us reconstruct the selected clusters. Whenever taking the current interval gives a strictly better value, we remember that this interval was chosen and jump back to `p`. Otherwise we move to the previous interval.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(2^n n)` | `O(n)` | Too slow |
| Quadratic DP | `O(n^2)` | `O(n)` | Too slow |
| Optimal weighted interval DP | `O(n log n)` | `O(n)` | Accepted |

## Algorithm Walkthrough

1. Read every cluster and construct its fixed update interval. For cluster `i`, store `(a_i, a_i + x_i, x_i, i)`. The original index is retained because the output must use the cluster numbering from the input.
2. Sort all intervals by their ending time. This ordering makes every predecessor of an interval appear before it, and more importantly, makes all ending times available for binary search.
3. Create an array `ends` containing the sorted ending times. For the current interval with start `s`, use `bisect_right(ends, s)` to find how many intervals end at or before `s`. Call this number `p`. The use of `bisect_right` is deliberate because an interval ending exactly at `s` does not overlap the current interval.
4. Maintain `dp`, where `dp[k]` is the maximum number of updated servers obtainable from the first `k` sorted intervals. Initially `dp[0] = 0`, because selecting nothing updates no servers.
5. Process the intervals from left to right. For the current interval, one option is to skip it, giving `dp[i]`. The other option is to take it, giving `dp[p] + x_i`. Store the larger value in `dp[i + 1]`.
6. Alongside `dp`, store a decision for each position. If taking the current interval is better, record that the interval was selected and remember `p`. If skipping it is at least as good, record that the current interval was skipped. Choosing skip when both values are equal is convenient because it gives a simple deterministic reconstruction, while still preserving an optimal answer.
7. Start from the final DP state and reconstruct the selected clusters backwards. If the current interval was selected, append its original index and jump to `p`. Otherwise move to the preceding DP state. Reverse the collected indices before printing them.

After sorting, the invariant is that `dp[i]` always represents the optimal answer using exactly the first `i` intervals in end-time order. Any optimal solution either excludes the current interval, in which case it is represented by `dp[i]`, or includes it, in which case every other selected interval must end no later than its start and the best such prefix is exactly `dp[p]`. These two cases cover every feasible solution, so the recurrence cannot miss an optimum.

## Python Solution

```python
Pythonimport sysfrom bisect import bisect_right
input = sys.stdin.readline

def solve():    n = int(input())
    intervals = []    for idx in range(n):        a, x = map(int, input().split())        intervals.append((a, a + x, x, idx))
    intervals.sort(key=lambda item: item[1])
    ends = [item[1] for item in intervals]
    dp = [0] * (n + 1)    take = [False] * n    prev = [0] * n
    for i, (start, end, weight, idx) in enumerate(intervals):        p = bisect_right(ends, start, 0, i)
        skip_value = dp[i]        take_value = dp[p] + weight
        if take_value > skip_value:            dp[i + 1] = take_value            take[i] = True            prev[i] = p        else:            dp[i + 1] = skip_value
    answer = []    pos = n
    while pos > 0:        i = pos - 1        if take[i]:            answer.append(intervals[i][3])            pos = prev[i]        else:            pos -= 1
    answer.reverse()
    print(dp[n])    print(*answer)

if __name__ == "__main__":    solve()
```

The input loop converts every cluster into the interval that must actually be occupied. The expression `a + x` is safe because Python integers have arbitrary precision, and the maximum possible value is only around `2 * 10^9` for one endpoint.

After sorting, `ends[i]` is the finishing time of the `i`-th interval. The call to `bisect_right(ends, start, 0, i)` searches only among intervals already processed by the DP. This restriction is useful because intervals after `i` cannot be predecessors of interval `i`. It also handles equal endpoints correctly.

The DP array has one extra element. `dp[0]` represents selecting from an empty prefix, and the interval at sorted position `i` produces the state `dp[i + 1]`. This indexing makes the predecessor `p` directly usable as a DP position.

The reconstruction arrays deserve particular attention. `prev[i]` is meaningful when interval `i` is selected and tells us exactly which DP state was used before it. We jump to that state rather than simply decrementing by one. When the interval was skipped, we move from `pos` to `pos - 1`.

The strict comparison `take_value > skip_value` is not required for correctness of the value, but it gives a deterministic choice when both alternatives are equally good. The statement permits any optimal set, so either choice would be valid.

The final indices are reversed because reconstruction follows the schedule backwards. Their order in the output is actually unrestricted, but reversing them makes the result easier to inspect and keeps them in the same order as the selected intervals.

## Worked Examples

### Sample 1

The first sample, reconstructed from the statement formatting, is

```
41 44 118 512 5
```

The intervals are `[1,5]`, `[4,15]`, `[8,13]`, and `[12,17]`. After sorting by ending time they already appear in this order.

| `i` | Interval | Start | Weight | `p` | Skip | Take | `dp[i+1]` |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | `[1,5]` | 1 | 4 | 0 | 0 | 4 | 4 |
| 1 | `[4,15]` | 4 | 11 | 0 | 4 | 11 | 11 |
| 2 | `[8,13]` | 8 | 4? | 1 | 11 | 9 | 11 |
| 3 | `[12,17]` | 12 | 5 | 1 | 11 | 9 | 11 |

The displayed sample's third cluster has `x = 5`, so its interval is `[8,13]`. Thus its actual take value is `dp[1] + 5 = 9`, and the table's conclusion remains unchanged. The optimal answer is cluster `1`, giving `11` updated servers.

### Sample 2

The second sample is

```
41 44 118 312 5
```

The intervals are `[1,5]`, `[4,15]`, `[8,11]`, and `[12,17]`.

| `i` | Interval | Start | Weight | `p` | Skip | Take | `dp[i+1]` |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | `[1,5]` | 1 | 4 | 0 | 0 | 4 | 4 |
| 1 | `[8,11]` | 8 | 3 | 1 | 4 | 7 | 7 |
| 2 | `[4,15]` | 4 | 11 | 0 | 7 | 11 | 11 |
| 3 | `[12,17]` | 12 | 5 | 2 | 11 | 12 | 12 |

Here the interval `[8,11]` can be followed by `[12,17]` because `11 <= 12`. The resulting total is `4 + 3 + 5 = 12`, using clusters `0`, `2`, and `3`. This example specifically demonstrates why equality in the predecessor condition must be accepted.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n log n)` | Sorting takes `O(n log n)`, and each of the `n` intervals performs one binary search |
| Space | `O(n)` | Intervals, DP values, predecessor information, and reconstruction arrays all require linear space |

For `n = 10^5`, sorting and roughly `10^5` binary searches are well within the intended scale. The algorithm avoids the quadratic predecessor search and uses only linear additional memory, so it fits comfortably within the stated memory limit and is appropriate for a one-second competitive programming limit.

## Test Cases

Because multiple optimal sets may exist and the statement allows their indices in arbitrary order, the testing helper below validates the returned value and the selected set rather than requiring one particular ordering.

```python
Pythonimport sysimport iofrom bisect import bisect_right

def solve_io(data: str) -> str:    it = iter(data.split())    n = int(next(it))
    intervals = []    for idx in range(n):        a = int(next(it))        x = int(next(it))        intervals.append((a, a + x, x, idx))
    intervals.sort(key=lambda item: item[1])    ends = [item[1] for item in intervals]
    dp = [0] * (n + 1)    take = [False] * n    prev = [0] * n
    for i, (start, end, weight, idx) in enumerate(intervals):        p = bisect_right(ends, start, 0, i)
        if dp[p] + weight > dp[i]:            dp[i + 1] = dp[p] + weight            take[i] = True            prev[i] = p        else:            dp[i + 1] = dp[i]
    selected = []    pos = n
    while pos:        i = pos - 1        if take[i]:            selected.append(intervals[i][3])            pos = prev[i]        else:            pos -= 1
    selected.reverse()
    return str(dp[n]) + "\n" + " ".join(map(str, selected)) + "\n"

def run(inp: str) -> str:    return solve_io(inp)

def parse_output(out: str):    lines = out.strip().splitlines()    value = int(lines[0])    indices = list(map(int, lines[1].split())) if len(lines) > 1 and lines[1] else []    return value, indices

def check(inp: str, expected_value: int):    out = run(inp)    value, indices = parse_output(out)
    assert value == expected_value
    data = list(map(int, inp.split()))    n = data[0]    clusters = []    p = 1
    for i in range(n):        a = data[p]        x = data[p + 1]        p += 2        clusters.append((a, x))
    assert len(indices) == len(set(indices))
    intervals = []    total = 0
    for idx in indices:        a, x = clusters[idx]        intervals.append((a, a + x))        total += x
    intervals.sort()
    for i in range(1, len(intervals)):        assert intervals[i - 1][1] <= intervals[i][0]
    assert total == value

# Provided sample 1.assert parse_output(run(    """41 44 118 512 5"""))[0] == 11
# Provided sample 2.assert parse_output(run(    """41 44 118 312 5"""))[0] == 12
# Minimum-size input.check(    """17 3""",    3)
# All intervals are identical, so only one cluster can be chosen.check(    """51 21 21 21 21 2""",    2)
# Touching intervals must be accepted.check(    """31 23 25 2""",    6)
# A long interval is worse than several compatible shorter intervals.check(    """41 62 24 26 2""",    6)
# Large-value stress case.n = 100000large_input = str(n) + "\n" + "\n".join(    f"{2 * i + 1} 1" for i in range(n)) + "\n"check(large_input, n)
print("All tests passed.")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 7 3` | `3` | Minimum-size input and reconstruction of a single interval |
| Five copies of `1 2` | `2` | Overlapping identical intervals and avoiding accidental double counting |
| `1 2`, `3 2`, `5 2` | `6` | Boundary condition where consecutive intervals touch |
| `1 6`, `2 2`, `4 2`, `6 2` | `6` | DP choosing several compatible jobs instead of the longest job |
| `100000` intervals `(2i+1, 1)` | `100000` | Maximum input size, sorting, binary search, and large DP state |

## Edge Cases

For touching intervals, consider

```
31 23 25 2
```

The intervals are `[1,3]`, `[3,5]`, and `[5,7]`. For the second interval, `bisect_right` includes the first interval because its end is exactly `3`, so `p = 1`. For the third interval, both previous intervals can be predecessors, giving `p = 2`. The DP reaches `6`, selecting all three clusters. A strict predecessor condition would incorrectly reduce the result.

For identical intervals, consider

```
31 51 51 5
```

All intervals end at `6`, and after the first interval is selected, every other interval has `p = 0` because none ends before or at the start `1`. The DP therefore keeps the value `5` rather than adding another overlapping interval. The output contains exactly one index and reports `5`.

For a long interval versus several shorter intervals, consider

```
41 62 24 26 2
```

The first cluster occupies `[1,7]` and gives value `6`. The other three occupy `[2,4]`, `[4,6]`, and `[6,8]`, so they can all be selected and also give total value `6`. The DP may choose either optimal arrangement depending on its tie handling. Since it prefers skipping when the values are equal, it keeps the first cluster's solution in the relevant state, but the reported value remains correct.

For a cluster that starts exactly when another one ends, consider

```
210 414 100
```

The intervals are `[10,14]` and `[14,114]`. The second cluster is a valid successor because the first update finishes at `14`, exactly when the second begins. The binary search uses `bisect_right`, so the first interval is included as a predecessor. The algorithm returns `104`, demonstrating the endpoint convention without relying on floating-point time.

For the maximum input size, the generated stress test contains `100000` non-overlapping unit-length intervals. Every interval can be selected, so the answer is `100000`. The algorithm performs one sort and one binary search per interval, rather than comparing every pair, which is exactly the distinction that makes the solution scalable.
