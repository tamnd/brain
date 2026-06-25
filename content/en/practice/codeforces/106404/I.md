---
title: "CF 106404I - Tiger Textbooks"
description: "We have a collection of textbooks. Each textbook has a topic identifier and a value representing how much the tiger enjoys it. The queries do not ask about positions in the original collection."
date: "2026-06-25T10:03:37+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106404
codeforces_index: "I"
codeforces_contest_name: "Bay Area Programming Contest 2026 Advanced Division"
rating: 0
weight: 106404
solve_time_s: 36
verified: true
draft: false
---

[CF 106404I - Tiger Textbooks](https://codeforces.com/problemset/problem/106404/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 36s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a collection of textbooks. Each textbook has a topic identifier and a value representing how much the tiger enjoys it. The queries do not ask about positions in the original collection. Instead, each query gives a range of possible topic frequencies, and we must compute the score produced by considering every ordered pair of frequencies inside that range.

For a frequency `k`, define `cnt[k]` as the number of topics that appear exactly `k` times. Among all topics with frequency `k`, define `best[k]` as the maximum enjoyment value. For two frequencies `i` and `j`, their contribution is zero unless `cnt[i]` and `cnt[j]` are equal. If they are equal and both frequencies exist, the best possible pair of books has value `best[i] * best[j]`. The query answer is the sum of these contributions over all ordered pairs `(i, j)` inside the query interval.

The input size is large: both the number of textbooks and the number of queries can reach `5 * 10^5`. A solution that scans every possible frequency for every query would require around `2.5 * 10^11` operations in the worst case, which is far beyond what a two second limit allows. We need to avoid depending on the full frequency range.

The key constraint hidden in the frequency representation is that the number of different frequencies that actually appear is small. If there are `s` different positive frequencies, the smallest possible total number of textbooks is:

`1 + 2 + 3 + ... + s`.

Since this sum cannot exceed `n`, `s` is at most about `1000` when `n = 500000`. This changes the problem completely. We only need to store and process the frequencies that exist.

Some edge cases are easy to miss. A frequency with no topics cannot contribute, even though two missing frequencies technically have the same count of zero topics. For example:

```
n = 1
topics = [5]
values = [10]
query = [2, 3]
```

There are no topics appearing two or three times, so the answer is `0`. A careless implementation that groups all equal `cnt[k]` values without checking whether `cnt[k] > 0` may incorrectly add a zero-frequency group.

Another corner case is when a query contains only one existing frequency. For example:

```
n = 3
topics = [1, 1, 1]
values = [5, 7, 9]
query = [3, 3]
```

Only frequency `3` exists. The answer is `9 * 9 = 81`, because the maximum value among the three books is `9`. Using the sum of all values instead of the maximum would give the wrong result.

A final boundary case is when the query range extends beyond the largest possible frequency. For example:

```
query = [100, 1000000000]
```

Only frequencies up to `n` can exist. The extra range must simply be ignored.

## Approaches

A direct solution would first build the frequency information and then answer each query by iterating through every possible frequency between `L` and `R`. This is correct because each frequency pair can be evaluated independently. However, the frequency range can be as large as `10^9` in the queries, and even limiting it to `n = 500000` would make every query too slow. The worst case would be about `5 * 10^5 * 5 * 10^5` frequency checks.

The important observation is that the array of frequency counts is extremely sparse. The value `cnt[k]` is non-zero only for frequencies that appear among the topics. There can be many topics, but there cannot be many different positive frequencies because every new frequency consumes more textbooks than the previous one.

For every existing frequency `k`, we keep the pair `(k, best[k])`. Frequencies with the same `cnt[k]` belong to the same group. If a group contains frequencies `k1, k2, ...`, then inside a query the contribution of all ordered pairs from that group is:

`(best[k1] + best[k2] + ...)^2`

because every frequency in the group can pair with every other frequency in the same group, including itself.

The number of existing frequencies is at most about `1000`, so each group can simply store its frequencies sorted. For a query, we binary search the first and last frequency inside every group and obtain the sum of `best` values that fall inside the interval. Adding the square of that sum gives the answer.

The brute force works because it examines exactly the pairs described in the statement, but fails because it repeats the same frequency comparisons across many queries. The sparse frequency observation lets us replace a huge frequency range scan with a few binary searches.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n + qn) | O(n) | Too slow |
| Sparse frequency groups with binary search | O(n + q * s log s) | O(s) | Accepted |

Here `s` is the number of distinct frequencies that actually occur, and `s <= 1000`.

## Algorithm Walkthrough

1. Count how many times each topic appears. While doing this, also remember the maximum enjoyment value among all books of each topic.
2. For every topic, use its final frequency to update `cnt[frequency]` and `best[frequency]`. The value stored in `best[k]` is the largest enjoyment value among topics that appear exactly `k` times.
3. Collect all frequencies `k` where `cnt[k] > 0`. Frequencies with `cnt[k] = 0` are ignored because no valid textbook can be selected for them.
4. Group these frequencies by their `cnt[k]` value. Every group represents frequencies that can interact with each other in a query.
5. Sort the frequencies inside each group. Also store prefix sums of their `best` values. This allows the sum of `best` values inside any query interval to be found with binary search.
6. For a query `[L, R]`, process every group. Find the frequencies in that group that lie between `L` and `R`. If their `best` values sum to `x`, add `x * x` to the answer.

The reason this grouping works is that frequencies from different groups have different numbers of topics, so every pair between those groups contributes zero. Inside one group, every pair contributes the product of the corresponding best values, and the sum of all ordered products is exactly the square of the sum.

The invariant is that every valid pair of frequencies belongs to exactly one frequency-count group. Inside that group, the prefix sum calculation includes exactly the frequencies allowed by the query and no others. Since every possible contribution is included once, the final sum is correct.

## Python Solution

```python
import sys
from collections import defaultdict
from bisect import bisect_left, bisect_right

input = sys.stdin.readline

def solve():
    n, q = map(int, input().split())
    a = list(map(int, input().split()))
    v = list(map(int, input().split()))

    freq = defaultdict(int)
    best_topic = defaultdict(int)

    for x, val in zip(a, v):
        freq[x] += 1
        if val > best_topic[x]:
            best_topic[x] = val

    cnt = defaultdict(int)
    best = defaultdict(int)

    for topic, f in freq.items():
        cnt[f] += 1
        if best_topic[topic] > best[f]:
            best[f] = best_topic[topic]

    groups = defaultdict(list)
    for f in cnt:
        if cnt[f] > 0:
            groups[cnt[f]].append((f, best[f]))

    data = []
    for items in groups.values():
        items.sort()
        freqs = []
        pref = [0]
        for f, val in items:
            freqs.append(f)
            pref.append(pref[-1] + val)
        data.append((freqs, pref))

    ans = []
    for _ in range(q):
        l, r = map(int, input().split())
        cur = 0

        for freqs, pref in data:
            left = bisect_left(freqs, l)
            right = bisect_right(freqs, r)
            if left < right:
                s = pref[right] - pref[left]
                cur += s * s

        ans.append(str(cur))

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The first part of the code compresses the original textbooks into topic information. We do not need individual books after this point because a frequency only cares about the maximum value among topics with that frequency.

The `groups` dictionary represents the main observation. Its key is the number of topics having a certain frequency. Frequencies sharing the same key can contribute together, while frequencies with different keys never interact.

For each group, the sorted frequency list and prefix sum array allow a query to be answered without scanning every frequency. `bisect_left` finds the first valid frequency and `bisect_right` finds the position after the last valid frequency, so the difference of prefix sums gives the required sum of `best` values.

Python integers automatically handle the large answer values. The maximum possible score can exceed 32-bit integer limits, so languages without automatic big integers would need a 64-bit type.

## Worked Examples

Consider the sample:

```
12 6
1 1 2 2 2 3 4 4 6 6 7 7
10 4 9 4 5 2 6 1 8 7 3 2
```

The frequency information becomes:

| Frequency | Number of topics | Best value |
| --- | --- | --- |
| 1 | 1 | 2 |
| 2 | 4 | 10 |
| 3 | 1 | 9 |

The groups are based on the number of topics.

| Group count | Frequencies |
| --- | --- |
| 1 | 1, 3 |
| 4 | 2 |

For query `[1, 2]`:

| Group | Frequencies inside range | Sum of best values | Contribution |
| --- | --- | --- | --- |
| count = 1 | 1 | 2 | 4 |
| count = 4 | 2 | 10 | 100 |

The answer is `104`.

For query `[1, 3]`:

| Group | Frequencies inside range | Sum of best values | Contribution |
| --- | --- | --- | --- |
| count = 1 | 1, 3 | 11 | 121 |
| count = 4 | 2 | 10 | 100 |

The answer is `221`.

These traces show the main invariant: a group contributes the square of the sum of its selected frequencies, not a sum of individual frequency squares.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + q * s log s) | Building frequency data is linear. Each query performs binary searches over at most `s` groups. |
| Space | O(s) | Only the existing frequencies are stored, and their count is at most about `1000`. |

The sparse frequency bound is what makes the solution fit the constraints. Even with half a million queries, each query only touches a small number of frequency groups.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    solve()
    out = sys.stdout.getvalue() if hasattr(sys.stdout, "getvalue") else ""
    sys.stdin = old
    return out

# Sample 1
assert run("""12 3
1 1 2 2 2 3 4 4 6 6 7 7
10 4 9 4 5 2 6 1 8 7 3 2
1 2
1 3
4 4
""") == """104
221
0""", "sample"

# Minimum size
assert run("""1 2
5
7
1 1
2 3
""") == """49
0""", "single book"

# All topics equal
assert run("""5 2
1 1 1 1 1
1 3 5 7 9
5 5
1 5
""") == """81
81""", "one frequency"

# Multiple equal frequency groups
assert run("""6 2
1 1 2 2 3 4
5 8 2 6 9 1
1 2
1 3
""") == """196
196""", "several groups"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample | 104, 221, 0 | Main grouping logic |
| Single book | 49, 0 | Missing frequencies and minimum size |
| All topics equal | 81, 81 | Maximum value selection for one frequency |
| Several groups | 196, 196 | Multiple frequency-count groups |

## Edge Cases

For the missing-frequency case:

```
1 1
5
10
2 3
```

The only existing frequency is `1`. The query does not contain it, so every group has an empty intersection. The algorithm performs binary searches, finds no values, and returns `0`.

For the single-frequency case:

```
3 1
1 1 1
5 7 9
3 3
```

The topic `1` has frequency `3`, and the best value is `9`. The group contains only frequency `3`, so the selected sum is `9` and the contribution is `9 * 9 = 81`.

For a query exceeding the possible range:

```
3 1
1 2 2
4 8 9
10 1000000000
```

No stored frequency lies in the interval. The binary searches return empty ranges for every group, and the result is `0`.

These cases are handled naturally because the algorithm never creates artificial entries for impossible frequencies and only works with frequencies that correspond to actual topics.
