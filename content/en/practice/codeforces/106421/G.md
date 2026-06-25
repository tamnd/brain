---
title: "CF 106421G - Tyson's Taunt"
description: "The problem asks us to look at every contiguous segment of punch timings and decide whether its average timing is inside the acceptable window."
date: "2026-06-25T09:42:16+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106421
codeforces_index: "G"
codeforces_contest_name: "UTPC Contest 3-11-2026 Div. 2 (Advanced)"
rating: 0
weight: 106421
solve_time_s: 36
verified: true
draft: false
---

[CF 106421G - Tyson's Taunt](https://codeforces.com/problemset/problem/106421/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 36s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem asks us to look at every contiguous segment of punch timings and decide whether its average timing is inside the acceptable window. The array contains the recorded timing of each attempt, and we need the total number of non-empty consecutive groups whose average value is at least `a` and at most `b`.

The constraints make the main challenge clear. There can be up to `2 * 10^5` attempts, so checking every segment directly is impossible. There are about `n^2 / 2` contiguous segments, which reaches roughly `2 * 10^10` when `n` is large. A quadratic algorithm cannot fit into the time limit. We need a solution close to `O(n log n)` because that gives only a few million operations for this input size.

The tricky parts come from averages. A segment with a fractional average can still satisfy the condition, so comparing integer sums directly is not enough. For example, the segment `[3, 4]` has average `3.5`. If the allowed range is `[3, 4]`, the answer must include it. A solution that divides using integer arithmetic may incorrectly treat the average as `3`.

Another edge case is when the average is exactly on a boundary. For input:

```
3 5 5
5 5 4
```

the correct output is `3`, because the valid segments are `[5]`, `[5]`, and `[5,5]`. A solution that uses a strict comparison instead of allowing equality would miss these cases.

A second boundary issue appears on the upper side. For input:

```
2 1 3
1 3
```

the segment `[1,3]` has average `2`, so it is valid and the answer is `3`. The upper bound must be handled as "greater than `b` is invalid", not "greater than or equal to `b` is invalid".

## Approaches

The direct approach is to enumerate every starting position and ending position, compute the sum of that segment, divide by its length, and check whether the average belongs to the interval. Prefix sums reduce the cost of finding a segment sum to `O(1)`, but there are still `O(n^2)` segments. In the worst case with `n = 200000`, this means around twenty billion checks, which is far beyond the available time.

The useful observation is that an average condition can be rewritten without division. For a segment with values `x1, x2, ..., xk`, the condition

```
(x1 + x2 + ... + xk) / k >= c
```

is equivalent to

```
(x1 - c) + (x2 - c) + ... + (xk - c) >= 0
```

Now the problem becomes counting subarrays with a transformed sum that is non-negative.

We can split the required interval into two simpler counts:

```
average in [a, b]
=
average >= a
-
average > b
```

The first count uses the transformation `x[i] - a` and asks for subarrays with sum at least zero. The second uses `x[i] - b` and asks for subarrays with sum strictly greater than zero.

For either version, let `pref[i]` be the prefix sum of the transformed array. A subarray `(l, r]` has a valid sum when:

```
pref[r] - pref[l] >= 0
```

which means:

```
pref[r] >= pref[l]
```

So while scanning the array from left to right, we only need to know how many previous prefix sums are smaller than or equal to the current one. This is an order-statistics counting problem. Coordinate compression and a Fenwick tree let us maintain these counts in `O(log n)` time per prefix.

The brute-force method works because it checks exactly the condition we need, but fails because it repeats almost identical work for too many segments. The prefix-sum transformation removes the need to inspect segments individually, and the Fenwick tree counts all valid pairs of prefixes efficiently.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Define a helper function that counts how many subarrays have average at least a chosen value `c`. Subtract `c` from every element and count subarrays whose transformed sum is non-negative. This converts the average comparison into a prefix comparison problem.
2. Build the transformed prefix sums. Start with prefix sum `0` before the array begins. Each new prefix represents the total transformed value of the elements processed so far.
3. Coordinate-compress all prefix sums. Prefix sums can be negative and can be large, so compression lets the Fenwick tree store their relative ordering instead of their actual values.
4. Scan the prefix sums from left to right. For a current prefix `p`, count how many earlier prefixes satisfy `previous <= p`. Every such pair creates a subarray with transformed sum at least zero. Add the count to the answer and insert `p` into the Fenwick tree.
5. Compute the number of subarrays with average greater than `b`. This is almost the same process, except we need `previous < p` because the transformed sum must be strictly positive.
6. Subtract the second count from the first count. The remaining segments are exactly those whose average is between `a` and `b`.

The invariant behind the algorithm is that after processing a prefix, the Fenwick tree contains exactly all earlier prefix sums and their frequencies. Every possible subarray ending at the current position corresponds to one earlier prefix. The tree query counts precisely the prefixes that make the current segment satisfy the transformed inequality, so every valid segment is counted once and every invalid segment is excluded.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, i, v):
        while i <= self.n:
            self.bit[i] += v
            i += i & -i

    def sum(self, i):
        res = 0
        while i:
            res += self.bit[i]
            i -= i & -i
        return res

def count_average_condition(arr, c, strict):
    pref = [0]
    cur = 0
    for x in arr:
        cur += x - c
        pref.append(cur)

    vals = sorted(set(pref))
    index = {v: i + 1 for i, v in enumerate(vals)}

    fw = Fenwick(len(vals))
    ans = 0

    fw.add(index[0], 1)

    for i in range(1, len(pref)):
        pos = index[pref[i]]
        if strict:
            ans += fw.sum(pos - 1)
        else:
            ans += fw.sum(pos)
        fw.add(pos, 1)

    return ans

def solve():
    n, a, b = map(int, input().split())
    arr = list(map(int, input().split()))

    at_least_a = count_average_condition(arr, a, False)
    greater_than_b = count_average_condition(arr, b, True)

    print(at_least_a - greater_than_b)

if __name__ == "__main__":
    solve()
```

The Fenwick tree stores frequencies of prefix sums rather than their values. The `add` operation inserts the current prefix after it has been used for counting, preventing the empty segment from being counted accidentally.

The first call to `count_average_condition` allows equality, so it queries the number of previous prefixes with value at most the current prefix. The second call requires a strictly positive transformed sum, so it only counts previous prefixes that are strictly smaller.

Python integers handle the potentially large answer automatically. The answer can be as large as the number of subarrays, about `n * (n + 1) / 2`, which is much larger than a 32-bit integer.

## Worked Examples

For the sample:

```
6 7 9
3 4 7 8 9 9
```

the valid subarrays are counted by subtracting those with average above `9` from those with average at least `7`.

| Step | Current prefix for a=7 | Previous prefixes counted | Running count |
| --- | --- | --- | --- |
| Start | 0 | Insert 0 | 0 |
| 1 | -4 | 0 | 0 |
| 2 | -7 | 0 | 0 |
| 3 | -7 | 2 | 2 |
| 4 | -6 | 3 | 5 |
| 5 | -4 | 4 | 9 |
| 6 | -2 | 6 | 15 |

The first pass counts all segments with average at least `7`. The second pass removes the segments with average greater than `9`, leaving the required answer `12`.

A second example:

```
3 5 5
5 5 4
```

For the lower and upper bound, only the exact average matters.

| Step | Prefix after subtracting 5 | Previous prefixes with valid relation | Count added |
| --- | --- | --- | --- |
| Start | 0 | Insert 0 | 0 |
| 1 | 0 | 1 | 1 |
| 2 | 0 | 2 | 2 |
| 3 | -1 | 0 | 0 |

The first count gives all segments with average at least `5`, and the second removes all segments with average greater than `5`. The remaining answer is `3`, matching the three segments with average exactly `5`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Each of the two counting passes processes `n` prefix sums, and every Fenwick operation takes logarithmic time. |
| Space | O(n) | The prefix sums, compressed coordinates, and Fenwick tree each store linear information. |

With `n` up to `200000`, the solution performs about two million logarithmic Fenwick operations, which fits comfortably within the limits.

## Test Cases

```python
import sys
import io

def solve_case(inp):
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    class Fenwick:
        def __init__(self, n):
            self.n = n
            self.bit = [0] * (n + 1)

        def add(self, i, v):
            while i <= self.n:
                self.bit[i] += v
                i += i & -i

        def sum(self, i):
            r = 0
            while i:
                r += self.bit[i]
                i -= i & -i
            return r

    def count(arr, c, strict):
        p = [0]
        s = 0
        for x in arr:
            s += x - c
            p.append(s)

        vals = sorted(set(p))
        mp = {x: i + 1 for i, x in enumerate(vals)}
        fw = Fenwick(len(vals))
        fw.add(mp[0], 1)
        ans = 0

        for x in p[1:]:
            pos = mp[x]
            ans += fw.sum(pos - 1 if strict else pos)
            fw.add(pos, 1)

        return ans

    n, a, b = map(int, input().split())
    arr = list(map(int, input().split()))
    return str(count(arr, a, False) - count(arr, b, True)) + "\n"

assert solve_case("""6 7 9
3 4 7 8 9 9
""") == "12\n"

assert solve_case("""1 5 5
5
""") == "1\n"

assert solve_case("""3 5 5
5 5 4
""") == "3\n"

assert solve_case("""2 1 3
1 3
""") == "3\n"

assert solve_case("""5 10 10
10 10 10 10 10
""") == "15\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `6 7 9 / 3 4 7 8 9 9` | `12` | Original sample behavior |
| `1 5 5 / 5` | `1` | Minimum size and exact boundary |
| `3 5 5 / 5 5 4` | `3` | Equality handling on the lower and upper limits |
| `2 1 3 / 1 3` | `3` | Fractional averages and inclusive upper bound |
| `5 10 10 / 10 10 10 10 10` | `15` | All equal values and large number of valid segments |

## Edge Cases

For the exact-boundary case:

```
3 5 5
5 5 4
```

the transformed values for `c = 5` are `0, 0, -1`. The prefix sums become `0, 0, 0, -1`. Equal prefix sums are counted in the first pass, so `[5]`, `[5]`, and `[5,5]` are included. The strict second pass removes only segments with average above `5`, of which there are none.

For the fractional-average case:

```
2 1 3
1 3
```

the full segment has sum `4` and length `2`, giving average `2`. The transformed array for `c = 1` is `[0, 2]`, so the prefix comparison recognizes the whole segment as valid. The upper-bound pass with `c = 3` does not remove it because its transformed sum is negative.

For all equal values:

```
5 10 10
10 10 10 10 10
```

every possible subarray has average `10`. The first pass counts all `15` subarrays, and the second pass counts zero because no segment has average greater than `10`. The final answer remains `15`, which confirms that equality is handled correctly.
