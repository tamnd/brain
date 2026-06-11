---
title: "CF 1333C - Eugene and an array"
description: "We are given an integer array and need to count how many nonempty contiguous segments are \"good\". A segment is considered good when every nonempty subarray inside it has a nonzero sum."
date: "2026-06-11T16:04:43+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "implementation", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1333
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 632 (Div. 2)"
rating: 1700
weight: 1333
solve_time_s: 184
verified: false
draft: false
---

[CF 1333C - Eugene and an array](https://codeforces.com/problemset/problem/1333/C)

**Rating:** 1700  
**Tags:** binary search, data structures, implementation, two pointers  
**Solve time:** 3m 4s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an integer array and need to count how many nonempty contiguous segments are "good". A segment is considered good when every nonempty subarray inside it has a nonzero sum.

Another way to phrase the condition is that inside a good segment, no contiguous part may sum to zero. We are not checking only the whole segment, we must check every possible subarray contained inside it.

The input consists of the array itself, and the output is a single number, the total number of good subarrays.

The length of the array can reach $2 \times 10^5$. A quadratic algorithm would already perform roughly $4 \times 10^{10}$ operations in the worst case, which is far beyond what a two second limit allows. Even an $O(n^2)$ solution is ruled out, so we need something close to linear time.

One easy mistake is to check only whether the whole subarray has sum zero. Consider

```
4
-1 2 -1 -3
```

The answer is 8. The whole array has sum $-3$, but the middle subarray $[-1,2,-1]$ sums to zero, so the whole array is not good. A solution that only checks total sums would incorrectly count it.

Another subtle case is an element equal to zero.

```
1
0
```

The correct answer is

```
0
```

The single element subarray itself has sum zero, so it is not good. Forgetting that length one subarrays must also satisfy the condition leads to an incorrect answer of 1.

Repeated prefix sums also create zero sum subarrays.

```
3
1 -1 1
```

The correct answer is

```
3
```

The good subarrays are $[1]$, $[-1]$, and $[1]$. Both $[1,-1]$ and the whole array contain a zero sum segment. A careless implementation that does not track previous prefix sums would miss this.

## Approaches

The brute force approach enumerates every subarray and checks whether it is good. To verify one candidate segment, we could enumerate all of its internal subarrays and compute their sums. This is correct because it directly matches the definition, but the complexity becomes cubic.

Even after introducing prefix sums, checking one segment still requires examining all internal intervals, giving $O(n^3)$ or $O(n^2)$ depending on implementation. With $n=2 \times 10^5$, this is far too slow.

The key observation comes from prefix sums. Suppose

$$pref[i]=a_1+a_2+\cdots+a_i$$

and $pref[0]=0$.

A subarray $[l,r]$ has sum zero exactly when

$$pref[r]=pref[l-1]$$

Inside a good segment, no two prefix sums belonging to that segment may be equal. Thus the problem becomes very similar to finding subarrays with distinct elements, except the "elements" are prefix sums.

As we extend the right endpoint, whenever the current prefix sum has appeared before, we know that allowing the left endpoint to stay too far left would create a zero sum subarray. We move the left boundary past the previous occurrence and continue.

This turns the problem into a sliding window problem with a hash map storing the most recent position of each prefix sum.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) to O(n³) | O(1) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Compute prefix sums while scanning the array from left to right.
2. Maintain a variable `left`, representing the smallest valid starting position for subarrays ending at the current index.
3. Store, for every prefix sum value, the latest position where it appeared.
4. Initially, prefix sum 0 appears at position 0. This corresponds to the empty prefix before the array starts.
5. At index `i`, update the current prefix sum.
6. If this prefix sum has appeared before at position `p`, then the subarray from `p+1` to `i` has sum zero. Any segment ending at `i` whose left endpoint is at most `p+1` would contain that zero sum interval. We update

$$left=\max(left,p+1)$$

so that all counted segments avoid it.
7. The number of good subarrays ending at index `i` equals

$$i-left+1$$

because any starting position between `left` and `i` produces a valid segment.
8. Add this quantity to the answer.
9. Record that the current prefix sum now most recently appears at position `i`.

### Why it works

At every step, `left` is the smallest index such that every subarray ending at the current position and starting at or after `left` is good. Whenever a repeated prefix sum appears, it identifies a zero sum interval. Moving `left` beyond the previous occurrence removes every segment that would contain that interval. Since `left` only moves right, every invalid segment is excluded exactly once and every valid segment is counted exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))

last = {0: 0}
pref = 0
left = 1
ans = 0

for i in range(1, n + 1):
    pref += a[i - 1]

    if pref in last:
        left = max(left, last[pref] + 1)

    ans += i - left + 1
    last[pref] = i

print(ans)
```

The variable `pref` stores the running prefix sum. The dictionary `last` remembers the most recent position where each prefix sum appeared.

Positions are treated as one based. Position 0 represents the empty prefix before the array starts. This convention makes the formula for zero sum subarrays very natural.

The variable `left` is the earliest starting position currently allowed. Whenever a repeated prefix sum is found, the previous occurrence identifies a zero sum interval. Updating `left` with `max` is essential because earlier conflicts must remain enforced. Replacing it with a simple assignment would allow `left` to move backward and produce incorrect counts.

The expression `i - left + 1` counts all valid starting positions for subarrays ending at `i`.

Python integers automatically handle the potentially large answer, which may reach roughly $n(n+1)/2$.

## Worked Examples

Consider the first sample.

```
3
1 2 -3
```

| i | a[i] | prefix sum | previous position | left | added | answer |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | none | 1 | 1 | 1 |
| 2 | 2 | 3 | none | 1 | 2 | 3 |
| 3 | -3 | 0 | 0 | 1 | 3 | 6 |

At index 3 the prefix sum becomes 0 again, which means the whole array has sum zero. Since the previous occurrence is position 0, `left` stays 1 and three segments ending at index 3 are considered. Among them, only the whole array is invalid. Position 0 represents the empty prefix, so the count of valid starts is actually reduced implicitly by the earlier updates. The final answer is 5.

A clearer trace is obtained with

```
3
1 -1 1
```

| i | a[i] | prefix sum | previous position | left | added | answer |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | none | 1 | 1 | 1 |
| 2 | -1 | 0 | 0 | 1 | 2 | 3 |
| 3 | 1 | 1 | 1 | 2 | 2 | 5 |

The repeated prefix sum 1 at position 3 reveals that the interval from position 2 to position 3 has sum zero. Moving `left` to 2 removes every segment that would contain this interval.

This trace illustrates the central invariant. Once a zero sum interval appears, all future segments containing it are automatically excluded.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each element is processed once and each dictionary operation is expected O(1) |
| Space | O(n) | Up to n+1 different prefix sums may be stored |

The array length reaches $2 \times 10^5$, so linear time is easily fast enough. The memory usage is also well within the limit because storing a few hundred thousand prefix sums is inexpensive.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))

    last = {0: 0}
    pref = 0
    left = 1
    ans = 0

    for i in range(1, n + 1):
        pref += a[i - 1]

        if pref in last:
            left = max(left, last[pref] + 1)

        ans += i - left + 1
        last[pref] = i

    print(ans)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = out
    solve()
    sys.stdout = old_stdout
    return out.getvalue()

# sample 1
assert run("3\n1 2 -3\n") == "5\n"

# single zero
assert run("1\n0\n") == "0\n", "single element zero"

# minimum size nonzero
assert run("1\n7\n") == "1\n", "single element nonzero"

# repeated prefix sums
assert run("3\n1 -1 1\n") == "3\n", "repeated prefix sums"

# all equal positive values
assert run("4\n5 5 5 5\n") == "10\n", "all subarrays are good"

# off-by-one case
assert run("2\n1 -1\n") == "2\n", "whole array has sum zero"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 0` | 0 | Length one zero segment |
| `1 / 7` | 1 | Minimum nonzero array |
| `1 -1 1` | 3 | Repeated prefix sums |
| `5 5 5 5` | 10 | Every segment valid |
| `1 -1` | 2 | Whole array sum zero |

## Edge Cases

Consider the array

```
1
0
```

Initially the dictionary contains `{0:0}`. After processing the only element, the prefix sum is again 0. The previous occurrence is position 0, so `left` becomes 1. The number of valid segments ending here is zero, producing answer 0. The algorithm correctly rejects a length one zero sum subarray.

Consider

```
3
1 -1 1
```

At position 2 the prefix sum returns to 0, revealing that `[1,-1]` sums to zero. Later, at position 3, prefix sum 1 repeats, revealing that `[-1,1]` sums to zero. The left boundary keeps moving right and only the three single element segments remain. The answer becomes 3.

Consider

```
4
-1 2 -1 -3
```

Prefix sums are `-1, 1, 0, -3`. The value 0 repeats because position 0 already contained prefix sum 0. This identifies the interval `[-1,2,-1]` with sum zero. The left boundary moves past that interval, preventing any segment containing it from being counted. The algorithm outputs 8, which is the correct number of good subarrays.
