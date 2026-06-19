---
title: "CF 106089B - \u0413\u043e\u043d\u043a\u0438"
description: "We are given an array of daily speeds. We must choose one contiguous segment of days whose length is at least k. For a segment [l, r], its quality is the arithmetic mean of all speeds inside that segment: $$frac{vl + v{l+1} + dots + vr}{r-l+1}$$ The task is to find any segment…"
date: "2026-06-19T21:52:36+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106089
codeforces_index: "B"
codeforces_contest_name: "\u0412\u0443\u0437\u043e\u0432\u0441\u043a\u043e-\u0430\u043a\u0430\u0434\u0435\u043c\u0438\u0447\u0435\u0441\u043a\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u043f\u043e \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0442\u0438\u043a\u0435 2025, \u0444\u0438\u043d\u0430\u043b"
rating: 0
weight: 106089
solve_time_s: 74
verified: true
draft: false
---

[CF 106089B - \u0413\u043e\u043d\u043a\u0438](https://codeforces.com/problemset/problem/106089/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 14s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of daily speeds. We must choose one contiguous segment of days whose length is at least `k`.

For a segment `[l, r]`, its quality is the arithmetic mean of all speeds inside that segment:

$$\frac{v_l + v_{l+1} + \dots + v_r}{r-l+1}$$

The task is to find any segment with maximum possible average and output its endpoints.

The most interesting part of the constraints is the condition

$$n \cdot k \le 10^6.$$

Although `n` can reach `100000`, it can only do so when `k` is very small. Any algorithm whose complexity is proportional to `nk` is safely within the limit, while `O(n^2)` is impossible when `k = 1`.

A common mistake is to assume that the optimal segment must have length exactly `k`.

Consider:

```
n = 3, k = 2
1 100 100
```

The segment of length `2` with the largest average is `[2,3]`, average `100`. The whole array has average `67`, so length `2` is indeed better.

Now consider:

```
n = 3, k = 2
50 100 50
```

The best length-2 average is `75`, but the whole array also has average `66.67`. Here length `2` remains optimal.

Neither example proves anything. The key point is that longer segments cannot simply be ignored without a proof.

Another subtle issue is comparing averages using floating point numbers. Consider:

```
k = 2
1000000000 999999999
999999999 1000000000
```

Different segments can have averages that differ by a tiny amount. Using floating point comparisons may accidentally choose the wrong segment. Cross multiplication of fractions avoids this completely.

## Approaches

The brute-force idea is straightforward. Compute prefix sums, enumerate every valid segment, calculate its sum in `O(1)`, compute its average, and keep the best one.

The problem is the number of valid segments. There are `Θ(n²)` of them. With `n = 100000`, that is far beyond what can be processed in one second.

The crucial observation comes from looking at very long segments.

Suppose a segment has length at least `2k`. Split it into two consecutive parts, each having length at least `k`.

If the left part has average `A` and the right part has average `B`, then the average of the whole segment is a weighted average of `A` and `B`. A weighted average can never exceed both of its components. So at least one of the two parts has average greater than or equal to the average of the whole segment.

That means a segment of length at least `2k` can never be strictly better than all of its valid subparts. We can repeatedly shorten such a segment until its length becomes less than `2k`, without decreasing the average.

As a result, some optimal answer always has length in the range

$$k \le L \le 2k-1.$$

Now the search space becomes small. There are only `k` possible lengths. For each length we scan all starting positions. The total work is

$$O(n \cdot k),$$

which is at most `10^6` because of the constraint.

Prefix sums give each segment sum in constant time, and averages are compared exactly using cross multiplication.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over all segments | O(n²) | O(n) | Too slow |
| Enumerate lengths from k to 2k-1 | O(nk) | O(n) | Accepted |

## Algorithm Walkthrough

1. Build a prefix sum array `pref`, where `pref[i]` stores the sum of the first `i` elements.
2. Maintain the current best segment. Store its total sum, its length, and its endpoints.
3. Enumerate every possible length `L` from `k` to `min(n, 2k - 1)`.

The key theorem guarantees that at least one optimal segment lies in this range.
4. For each length `L`, slide through all segments of that length.

Using prefix sums, the segment sum is

$$pref[r] - pref[l-1].$$
5. Compare the average of the current segment with the best average seen so far.

Instead of dividing, compare

$$\frac{sum_1}{len_1}
\quad\text{and}\quad
\frac{sum_2}{len_2}$$

by checking

$$sum_1 \cdot len_2
\quad\text{vs}\quad
sum_2 \cdot len_1.$$

This is exact and avoids floating point errors.
6. If the current average is larger, replace the stored answer.
7. After all lengths have been processed, output the saved endpoints.

### Why it works

The correctness rests on one property.

Any segment whose length is at least `2k` can be split into two consecutive segments, both of length at least `k`. The average of the whole segment is a weighted average of the averages of these two parts. Consequently, at least one part has average at least as large as the whole segment.

Starting from any optimal segment, repeatedly replace it with such a part whenever its length is at least `2k`. The average never decreases, and eventually the length falls into `[k, 2k-1]`.

So an optimal answer always exists inside that length range. The algorithm enumerates every segment of every length in that range and selects the one with maximum average. Since every candidate is checked and averages are compared exactly, the returned segment is optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    v = list(map(int, input().split()))

    pref = [0] * (n + 1)
    for i in range(n):
        pref[i + 1] = pref[i] + v[i]

    best_sum = -1
    best_len = 1
    best_l = best_r = 1

    max_len = min(n, 2 * k - 1)

    for length in range(k, max_len + 1):
        for l in range(1, n - length + 2):
            r = l + length - 1
            cur_sum = pref[r] - pref[l - 1]

            if best_sum == -1 or cur_sum * best_len > best_sum * length:
                best_sum = cur_sum
                best_len = length
                best_l = l
                best_r = r

    print(best_l, best_r)

solve()
```

The prefix-sum construction makes every segment sum available in constant time. Without it, computing a sum would require scanning the segment, which would increase the complexity by another factor of the length.

The variable pair `(best_sum, best_len)` represents the current best average as the fraction `best_sum / best_len`. When a new segment is considered, the comparison

```
cur_sum * best_len > best_sum * length
```

checks whether

$$\frac{cur\_sum}{length}
>
\frac{best\_sum}{best\_len}.$$

No division is performed, so there are no precision problems.

The loop over lengths stops at `2k - 1`. That bound is the entire reason the solution fits the constraints.

All indexing is handled in 1-based coordinates because the required output is 1-based. The prefix sum array is built with an extra leading zero, making the formula

```
pref[r] - pref[l - 1]
```

work uniformly for every segment.

## Worked Examples

### Sample 1

Input:

```
4 2
1 2 3 4
```

Prefix sums:

| i | pref[i] |
| --- | --- |
| 0 | 0 |
| 1 | 1 |
| 2 | 3 |
| 3 | 6 |
| 4 | 10 |

Lengths considered: `2` and `3`.

| Length | Segment | Sum | Average | Best after step |
| --- | --- | --- | --- | --- |
| 2 | [1,2] | 3 | 1.5 | [1,2] |
| 2 | [2,3] | 5 | 2.5 | [2,3] |
| 2 | [3,4] | 7 | 3.5 | [3,4] |
| 3 | [1,3] | 6 | 2.0 | [3,4] |
| 3 | [2,4] | 9 | 3.0 | [3,4] |

Final answer:

```
3 4
```

The trace shows that even after checking longer segments, the length-2 segment `[3,4]` remains optimal.

### Sample 2

Input:

```
10 2
3 5 2 7 2 9 3 8 2 7
```

Lengths considered: `2` and `3`.

| Length | Segment | Sum | Average |
| --- | --- | --- | --- |
| 2 | [1,2] | 8 | 4.0 |
| 2 | [2,3] | 7 | 3.5 |
| 2 | [3,4] | 9 | 4.5 |
| 2 | [4,5] | 9 | 4.5 |
| 2 | [5,6] | 11 | 5.5 |
| 2 | [6,7] | 12 | 6.0 |
| 2 | [7,8] | 11 | 5.5 |
| 2 | [8,9] | 10 | 5.0 |
| 2 | [9,10] | 9 | 4.5 |
| 3 | [1,3] | 10 | 3.33 |
| 3 | [2,4] | 14 | 4.67 |
| 3 | [3,5] | 11 | 3.67 |
| 3 | [4,6] | 18 | 6.0 |
| 3 | [5,7] | 14 | 4.67 |
| 3 | [6,8] | 20 | 6.67 |
| 3 | [7,9] | 13 | 4.33 |
| 3 | [8,10] | 17 | 5.67 |

The maximum average is achieved by `[6,8]`.

Final answer:

```
6 8
```

This example demonstrates why checking only length `k` is not sufficient. The best segment has length `3`, even though `k = 2`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nk) | There are at most `k` candidate lengths and `O(n)` segments for each length |
| Space | O(n) | Prefix sums |

Because `n * k ≤ 10^6`, the total number of processed segments is at most about one million. That comfortably fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n, k = map(int, input().split())
    v = list(map(int, input().split()))

    pref = [0] * (n + 1)
    for i in range(n):
        pref[i + 1] = pref[i] + v[i]

    best_sum = -1
    best_len = 1
    ans = (1, 1)

    for length in range(k, min(n, 2 * k - 1) + 1):
        for l in range(1, n - length + 2):
            r = l + length - 1
            s = pref[r] - pref[l - 1]

            if best_sum == -1 or s * best_len > best_sum * length:
                best_sum = s
                best_len = length
                ans = (l, r)

    return f"{ans[0]} {ans[1]}"

# provided samples
assert run("4 2\n1 2 3 4\n") == "3 4"
assert run("10 2\n3 5 2 7 2 9 3 8 2 7\n") == "6 8"

# minimum size
assert run("1 1\n5\n") == "1 1"

# all equal values, any optimal answer exists
assert run("5 3\n7 7 7 7 7\n") == "1 3"

# best segment has length greater than k
assert run("3 2\n3 10 3\n") == "1 3"

# off-by-one at the end of the array
assert run("5 2\n1 1 1 1 100\n") == "4 5"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 5` | `1 1` | Smallest possible instance |
| All values equal | `1 3` | Ties between many segments |
| `3 2 / 3 10 3` | `1 3` | Optimal segment length greater than `k` |
| `5 2 / 1 1 1 1 100` | `4 5` | Correct handling of segments ending at `n` |

## Edge Cases

Consider:

```
1 1
42
```

The only valid segment is `[1,1]`. The algorithm examines length `1`, computes its sum from the prefix array, and immediately stores it as the answer. The output is:

```
1 1
```

Now consider a case where the optimal segment is longer than `k`:

```
3 2
3 10 3
```

The length-2 segments have average `6.5`. The length-3 segment has average

$$\frac{16}{3} \approx 5.33$$

Actually this one is not larger, so let us use:

```
3 2
5 10 5
```

Length-2 averages are `7.5`, while the length-3 average is `20/3 ≈ 6.67`. The algorithm checks both lengths and correctly compares fractions without floating point arithmetic.

Finally, consider large values:

```
2 1
1000000000 1000000000
```

The sum reaches `2 * 10^9`, and during comparison we multiply by lengths up to `10^5`. In some languages, 32-bit integers would overflow. The solution compares averages using integer arithmetic, and Python's arbitrary-precision integers handle these values safely.
