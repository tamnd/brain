---
title: "CF 190D - Non-Secret Cypher"
description: "We are given an array of integers and a number k. We need to count how many contiguous subarrays contain some value at least k times. The condition is not about having k distinct equal pairs or anything global across the subarray."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 190
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 120 (Div. 2)"
rating: 1900
weight: 190
solve_time_s: 96
verified: true
draft: false
---

[CF 190D - Non-Secret Cypher](https://codeforces.com/problemset/problem/190/D)

**Rating:** 1900  
**Tags:** two pointers  
**Solve time:** 1m 36s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers and a number `k`. We need to count how many contiguous subarrays contain some value at least `k` times.

The condition is not about having `k` distinct equal pairs or anything global across the subarray. A subarray is valid if there exists at least one number whose frequency inside that subarray is at least `k`.

For example, with:

```
1 2 1 2
k = 2
```

the subarray `[1,2,1]` is valid because the value `1` appears twice. The subarray `[2,1,2]` is also valid because `2` appears twice.

The array length goes up to `4 * 10^5`, which immediately rules out anything quadratic. A naive `O(n^2)` solution would require roughly `1.6 * 10^11` operations in the worst case, far beyond what fits into a 3 second time limit.

The values themselves can be as large as `10^9`, so we cannot use a direct frequency array indexed by value. We need a hash map or dictionary for frequencies.

The answer can also become very large. If every subarray is valid, the count is:

$\frac{n(n+1)}{2}$

For `n = 4 * 10^5`, this is around `8 * 10^10`, so 64-bit arithmetic is required.

Several edge cases are easy to mishandle.

Consider:

```
1 1
5
```

Every subarray is valid because every subarray contains some element at least once. The answer is `1`. A careless sliding window implementation may accidentally shrink too early and miss this case.

Another tricky case is when the valid condition appears multiple times inside the same window:

```
5 2
1 1 1 1 1
```

Every subarray of length at least `2` is valid, so the answer is `10`. If we count only the first time a window becomes valid and forget that extending the right boundary preserves validity, we undercount badly.

A different subtle case is when the window stops being valid after removing one element:

```
5 3
1 2 1 1 3
```

The valid subarrays are:

```
[1,2,1,1]
[1,2,1,1,3]
```

Answer = `2`.

If we shrink the left pointer too aggressively after finding a valid window, we may skip one of these.

## Approaches

The brute-force approach checks every subarray independently.

For each starting position `l`, we extend the right endpoint `r` one step at a time and maintain frequencies of elements inside the current subarray. As soon as some frequency reaches `k`, we count that subarray as valid.

This is correct because every subarray is examined exactly once and we explicitly test the required condition.

The problem is the number of subarrays. There are:

$\frac{n(n+1)}{2}$

possible subarrays, which is about `8 * 10^10` when `n = 4 * 10^5`.

Even with constant-time updates, this is far too slow.

The key observation is that validity is monotonic with respect to extending the right boundary.

Suppose a window `[l, r]` already contains some value at least `k` times. Then every larger window `[l, r+1]`, `[l, r+2]`, and so on is also valid, because frequencies never decrease when we extend the window.

This monotonic behavior is exactly what two pointers exploit efficiently.

We maintain a sliding window `[l, r]` and frequencies of elements inside it.

For each left boundary `l`, we move `r` rightward until the window becomes valid. Once validity is reached, every larger right endpoint is automatically valid. If the first valid position is `r`, then all subarrays ending at `r, r+1, ..., n-1` are valid.

That contributes `n - r` subarrays immediately.

Then we move `l` forward by one position and restore the invariant.

Each pointer moves at most `n` times, giving linear complexity.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Create a frequency dictionary and initialize two pointers:

`l = 0` and `r = 0`.
2. Expand the right pointer while the current window is not valid.

Each time we include `a[r]`, increment its frequency.
3. The moment some value reaches frequency `k`, the current window becomes valid.

This is the smallest valid window starting at `l` because `r` only moved forward until validity first appeared.
4. If the window is valid at position `r`, then every subarray:

```
[l, r], [l, r+1], [l, r+2], ...
```

is also valid.

Add `n - r` to the answer.
5. Remove `a[l]` from the window and move `l` one step right.

This prepares the next iteration for the next starting position.
6. Repeat until `l` reaches the end of the array.

### Why it works

The algorithm maintains this invariant:

```
Before counting for a fixed left boundary l,
r is the smallest index such that [l, r] is valid.
```

Because `r` only moves forward, we never revisit work already done.

When `[l, r]` first becomes valid, every larger right endpoint also remains valid since frequencies can only increase when extending the window. That is why adding `n - r` counts exactly all valid subarrays starting at `l`.

No valid subarray is missed because every starting position is processed once, and the smallest valid ending position is found for that start.

No invalid subarray is counted because counting begins only after the frequency condition becomes true.

## Python Solution

```python
import sys
from collections import defaultdict

input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    freq = defaultdict(int)

    ans = 0
    r = 0
    good = False

    for l in range(n):
        while r < n and not good:
            freq[a[r]] += 1

            if freq[a[r]] >= k:
                good = True

            r += 1

        if good:
            ans += n - r + 1

        freq[a[l]] -= 1

        if freq[a[l]] < k:
            good = False

    print(ans)

if __name__ == "__main__":
    solve()
```

The frequency dictionary stores counts for the current sliding window. Since array values can be as large as `10^9`, coordinate compression is unnecessary, and a hash map is the simplest choice.

The variable `good` tracks whether the current window already contains some value with frequency at least `k`.

The right pointer `r` always points one position past the current window, which is a standard half-open interval convention. After inserting `a[r]`, we increment `r` immediately. That is why the contribution formula becomes:

```
n - r + 1
```

At the moment counting happens, the actual valid window ends at `r - 1`.

The removal order is important. We first subtract `a[l]` from the frequency map, then check whether the window lost validity. Reversing this order produces incorrect results when the removed element was exactly the one providing frequency `k`.

The total complexity is linear because each element enters and leaves the window once.

## Worked Examples

### Example 1

Input:

```
4 2
1 2 1 2
```

| l | r after expansion | Window | Valid? | Added | Answer |
| --- | --- | --- | --- | --- | --- |
| 0 | 3 | [1,2,1] | Yes | 2 | 2 |
| 1 | 4 | [2,1,2] | Yes | 1 | 3 |
| 2 | 4 | [1,2] | No | 0 | 3 |
| 3 | 4 | [2] | No | 0 | 3 |

The first valid window starting at index `0` is `[1,2,1]`. Every extension of it is also valid, so we count two subarrays immediately:

```
[1,2,1]
[1,2,1,2]
```

The same logic applies for the second starting position.

### Example 2

Input:

```
5 3
1 2 1 1 3
```

| l | r after expansion | Window | Valid? | Added | Answer |
| --- | --- | --- | --- | --- | --- |
| 0 | 4 | [1,2,1,1] | Yes | 2 | 2 |
| 1 | 5 | [2,1,1,3] | No | 0 | 2 |
| 2 | 5 | [1,1,3] | No | 0 | 2 |
| 3 | 5 | [1,3] | No | 0 | 2 |
| 4 | 5 | [3] | No | 0 | 2 |

The only valid windows start at index `0`.

Once `[1,2,1,1]` becomes valid, extending it with `3` preserves the condition, giving exactly two valid subarrays.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each pointer moves at most `n` times |
| Space | O(n) | Frequency dictionary may store all distinct values |

With `n = 4 * 10^5`, linear time easily fits the limit. The memory usage is also safe because at most `n` distinct values appear.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from collections import defaultdict

def solve():
    input = sys.stdin.readline

    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    freq = defaultdict(int)

    ans = 0
    r = 0
    good = False

    for l in range(n):
        while r < n and not good:
            freq[a[r]] += 1

            if freq[a[r]] >= k:
                good = True

            r += 1

        if good:
            ans += n - r + 1

        freq[a[l]] -= 1

        if freq[a[l]] < k:
            good = False

    print(ans)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdout = sys.__stdout__
    return out.getvalue()

# provided sample
assert run("4 2\n1 2 1 2\n") == "3\n", "sample 1"

# minimum size
assert run("1 1\n5\n") == "1\n", "single element"

# all equal values
assert run("5 2\n1 1 1 1 1\n") == "10\n", "all equal"

# no valid subarray
assert run("5 3\n1 2 3 4 5\n") == "0\n", "all distinct"

# boundary condition
assert run("5 3\n1 2 1 1 3\n") == "2\n", "exactly one valid starting point"

# off-by-one stress
assert run("3 2\n1 1 2\n") == "2\n", "windows ending at array boundary"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 5` | `1` | Minimum input and `k = 1` |
| `5 2 / 1 1 1 1 1` | `10` | Every long enough subarray valid |
| `5 3 / 1 2 3 4 5` | `0` | No repeated values |
| `5 3 / 1 2 1 1 3` | `2` | Exact threshold handling |
| `3 2 / 1 1 2` | `2` | Right boundary off-by-one correctness |

## Edge Cases

Consider:

```
1 1
5
```

The window becomes valid immediately after inserting the first element because frequency `1 >= k`.

The algorithm adds:

```
n - r + 1 = 1
```

which correctly counts the only subarray.

Now consider:

```
5 2
1 1 1 1 1
```

Every subarray of length at least `2` is valid.

For `l = 0`, the first valid window ends at index `1`, so we add `4`.

For `l = 1`, again the first valid window length is `2`, so we add `3`.

The sequence of additions becomes:

```
4 + 3 + 2 + 1 = 10
```

which matches the correct answer.

Finally, consider:

```
5 3
1 2 1 1 3
```

The first valid window is:

```
[1,2,1,1]
```

The algorithm adds `2` because both:

```
[1,2,1,1]
[1,2,1,1,3]
```

are valid.

Then the leftmost `1` is removed, reducing its frequency from `3` to `2`. The window becomes invalid again, so no additional invalid subarrays are accidentally counted.
