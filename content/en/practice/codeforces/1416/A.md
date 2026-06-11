---
title: "CF 1416A - k-Amazing Numbers"
description: "We are given an array whose values are between 1 and n. For every length k, we look at all subarrays of length k. A value x is considered valid if every such subarray contains at least one occurrence of x. Among all valid values, we must output the smallest one."
date: "2026-06-11T07:02:37+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "implementation", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1416
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 673 (Div. 1)"
rating: 1500
weight: 1416
solve_time_s: 148
verified: true
draft: false
---

[CF 1416A - k-Amazing Numbers](https://codeforces.com/problemset/problem/1416/A)

**Rating:** 1500  
**Tags:** binary search, data structures, implementation, two pointers  
**Solve time:** 2m 28s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array whose values are between `1` and `n`.

For every length `k`, we look at **all** subarrays of length `k`. A value `x` is considered valid if every such subarray contains at least one occurrence of `x`. Among all valid values, we must output the smallest one. If no value appears in every length-`k` subarray, the answer is `-1`.

Another way to think about the condition is this: if a value `x` is missing from some length-`k` subarray, then `x` is not a candidate. We need values that are impossible to avoid when taking any segment of length `k`.

The total size of all test cases is at most `3 · 10^5`. Any solution that processes every `k` separately or scans all subarrays for each value will be far too slow. With `n = 3 · 10^5`, we usually need something close to `O(n log n)` or `O(n)` per test case.

The tricky part is that the answer must be produced for every `k` from `1` to `n`, so we need a way to characterize when a value becomes valid for a given segment length.

Consider the array:

```
1 2 1
```

For `k = 2`, the segments are `[1,2]` and `[2,1]`. Value `1` appears in both, so the answer is `1`.

A careless approach might only count total occurrences. Since `2` appears once and `1` appears twice, it may seem that frequency is what matters. It is not. The positions matter much more than the count.

Another important case is:

```
1 2 3 4 5
```

Every value appears exactly once.

For `k = 3`, the segments are:

```
[1,2,3]
[2,3,4]
[3,4,5]
```

Only value `3` appears in all of them, so the answer is `3`.

A frequency-based approach completely misses this behavior.

One more edge case is a value appearing many times but with a large gap:

```
1 1 1 2 1
```

Value `1` appears four times, but if there were a long stretch without it, some segment could avoid it. What matters is the largest distance between consecutive occurrences, not the total number of occurrences.

## Approaches

A brute-force solution would process every `k` independently. For each value, we could check whether every length-`k` subarray contains that value.

One way is to generate all `n-k+1` subarrays and track which values appear in each of them. Even with optimizations, this quickly becomes at least `O(n²)` and often `O(n³)`. With `n = 3 · 10^5`, such approaches are hopeless.

The key observation comes from looking at a single value `x`.

Suppose the occurrences of `x` are at positions:

```
p1, p2, ..., pm
```

Add two virtual positions:

```
0 and n+1
```

Now consider the gaps:

```
p1 - 0
p2 - p1
...
pm - p(m-1)
(n+1) - pm
```

Let the largest gap be `g`.

What does this mean?

If there is a gap of length `g`, then between those two consecutive occurrences there are `g-1` positions containing no `x`.

A segment of length `g-1` can fit entirely inside that gap, avoiding `x` completely.

So `x` cannot be present in every segment of length `g-1`.

On the other hand, any segment of length `g` must cross at least one occurrence of `x`, because there is no gap large enough to hold `g` consecutive positions without `x`.

This gives a very useful characterization:

A value `x` appears in every subarray of length `k` if and only if

```
k ≥ largest_gap(x)
```

Therefore every value has a threshold:

```
need[x] = largest_gap(x)
```

For all `k ≥ need[x]`, value `x` is valid.

Now the problem becomes:

For each `k`, find the smallest value whose threshold is at most `k`.

This is much easier.

We compute `need[x]` for every value. Then for each value `x`, it becomes a candidate starting from position `need[x]`. We store:

```
ans[need[x]] = min(ans[need[x]], x)
```

After that, a prefix minimum sweep propagates candidates to larger `k`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) to O(n³) | O(n²) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Create a list of occurrence positions for every value from `1` to `n`.
2. For each array position `i`, append `i` to the occurrence list of `a[i]`.
3. For every value `x`, compute its maximum gap.

Start with previous position `0`. For every occurrence position `p`, update:

```
gap = p - previous
```

Keep the largest such gap.

After processing all occurrences, also consider:

```
(n + 1) - last_occurrence
```

This handles the suffix after the final occurrence.
4. Let this largest gap be `need[x]`.

Value `x` is valid for every `k ≥ need[x]`.
5. Create an array `ans` initialized with infinity.
6. For every value `x` that appears at least once, update:

```
ans[need[x]] = min(ans[need[x]], x)
```

We record the smallest value whose threshold is exactly `need[x]`.
7. Perform a prefix minimum sweep:

```
ans[k] = min(ans[k], ans[k-1])
```

for all `k` from `2` to `n`.

Once a value becomes valid, it remains valid for all larger segment lengths.
8. Replace any remaining infinity entries with `-1`.
9. Output `ans[1] ... ans[n]`.

### Why it works

For a value `x`, the largest distance between consecutive occurrences (including array boundaries) determines the longest region without `x`.

A subarray can avoid `x` exactly when it fits completely inside such a region. The largest possible length of a subarray avoiding `x` is `largest_gap(x) - 1`.

Consequently, every subarray of length `k` contains `x` precisely when `k ≥ largest_gap(x)`.

The algorithm computes this threshold for every value. A value becomes a valid candidate starting from its threshold and remains valid afterwards. Taking the minimum value among all candidates for each `k` produces exactly the required k-amazing number.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    out = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        pos = [[] for _ in range(n + 1)]

        for i, x in enumerate(a, start=1):
            pos[x].append(i)

        INF = n + 1
        ans = [INF] * (n + 1)

        for value in range(1, n + 1):
            if not pos[value]:
                continue

            mx_gap = 0
            prev = 0

            for p in pos[value]:
                mx_gap = max(mx_gap, p - prev)
                prev = p

            mx_gap = max(mx_gap, n + 1 - prev)

            ans[mx_gap] = min(ans[mx_gap], value)

        for k in range(2, n + 1):
            ans[k] = min(ans[k], ans[k - 1])

        result = []

        for k in range(1, n + 1):
            if ans[k] == INF:
                result.append("-1")
            else:
                result.append(str(ans[k]))

        out.append(" ".join(result))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The occurrence lists are the foundation of the solution. For each value we only need the positions where it appears, because the largest gap between appearances completely determines when that value becomes valid.

The boundary positions `0` and `n+1` are handled implicitly through `prev = 0` and the final check `n + 1 - prev`. Forgetting either boundary is the most common bug in this problem. A value appearing at the first position still leaves a prefix gap of size `1`, and a value appearing at the last position still leaves a suffix gap of size `1`.

The array `ans` stores information by threshold. If `need[x] = 5`, then value `x` first becomes valid at `k = 5`. The prefix minimum pass converts these threshold entries into answers for all larger lengths.

## Worked Examples

### Example 1

Input:

```
5
1 2 3 4 5
```

Occurrence gaps:

| Value | Positions | Largest Gap |
| --- | --- | --- |
| 1 | [1] | 5 |
| 2 | [2] | 4 |
| 3 | [3] | 3 |
| 4 | [4] | 4 |
| 5 | [5] | 5 |

After inserting values by threshold:

| k | Stored minimum |
| --- | --- |
| 1 | INF |
| 2 | INF |
| 3 | 3 |
| 4 | 2 |
| 5 | 1 |

After prefix minima:

| k | Answer |
| --- | --- |
| 1 | -1 |
| 2 | -1 |
| 3 | 3 |
| 4 | 2 |
| 5 | 1 |

Output:

```
-1 -1 3 2 1
```

This example shows that a value occurring only once can still become the answer for large enough segment lengths.

### Example 2

Input:

```
6
1 3 1 5 3 1
```

Occurrence analysis:

| Value | Positions | Largest Gap |
| --- | --- | --- |
| 1 | [1,3,6] | 3 |
| 2 | [] | - |
| 3 | [2,5] | 3 |
| 4 | [] | - |
| 5 | [4] | 4 |

Threshold insertion:

| k | Stored minimum |
| --- | --- |
| 3 | 1 |
| 4 | 5 |

Prefix minima:

| k | Answer |
| --- | --- |
| 1 | -1 |
| 2 | -1 |
| 3 | 1 |
| 4 | 1 |
| 5 | 1 |
| 6 | 1 |

Output:

```
-1 -1 1 1 1 1
```

This trace demonstrates the monotonic property. Once value `1` becomes valid at `k = 3`, it remains valid for every larger `k`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each occurrence is processed a constant number of times |
| Space | O(n) | Occurrence lists and answer arrays store O(n) data |

Across all test cases, the total `n` is at most `3 · 10^5`, so the overall complexity remains `O(3 · 10^5)`. This comfortably fits within the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    def input():
        return sys.stdin.readline()

    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        pos = [[] for _ in range(n + 1)]

        for i, x in enumerate(a, start=1):
            pos[x].append(i)

        INF = n + 1
        ans = [INF] * (n + 1)

        for value in range(1, n + 1):
            if not pos[value]:
                continue

            prev = 0
            mx_gap = 0

            for p in pos[value]:
                mx_gap = max(mx_gap, p - prev)
                prev = p

            mx_gap = max(mx_gap, n + 1 - prev)
            ans[mx_gap] = min(ans[mx_gap], value)

        for k in range(2, n + 1):
            ans[k] = min(ans[k], ans[k - 1])

        out.append(
            " ".join(
                "-1" if ans[k] == INF else str(ans[k])
                for k in range(1, n + 1)
            )
        )

    return "\n".join(out)

# provided samples
assert run(
"""3
5
1 2 3 4 5
5
4 4 4 4 2
6
1 3 1 5 3 1
"""
) == (
"""-1 -1 3 2 1
-1 4 4 4 2
-1 -1 1 1 1 1"""
), "sample"

# minimum size
assert run(
"""1
1
1
"""
) == "1", "single element"

# all equal
assert run(
"""1
4
2 2 2 2
"""
) == "2 2 2 2", "all equal values"

# alternating pattern
assert run(
"""1
5
1 2 1 2 1
"""
) == "-1 1 1 1 1", "alternating occurrences"

# boundary gap check
assert run(
"""1
3
1 2 3
"""
) == "-1 2 1", "prefix and suffix gaps"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `[1]` | `1` | Smallest possible instance |
| `[2,2,2,2]` | `2 2 2 2` | Repeated value with gap size 1 |
| `[1,2,1,2,1]` | `-1 1 1 1 1` | Multiple occurrences and threshold propagation |
| `[1,2,3]` | `-1 2 1` | Correct handling of boundary gaps |

## Edge Cases

Consider:

```
1
3
1 2 3
```

Value `2` appears in the middle. Its gaps are:

```
2 - 0 = 2
4 - 2 = 2
```

Largest gap is `2`, so it becomes valid for `k = 2`.

Value `1` has largest gap `3`, so it becomes valid only for `k = 3`.

The output is:

```
-1 2 1
```

Without accounting for the virtual positions `0` and `n+1`, this answer would be wrong.

Now consider:

```
1
4
2 2 2 2
```

The gaps are all `1`, so `need[2] = 1`.

The algorithm places value `2` at `ans[1]`, and the prefix minimum sweep propagates it to every larger `k`.

Output:

```
2 2 2 2
```

This verifies that a value occurring everywhere is immediately valid for all segment lengths.

Finally consider:

```
1
5
1 2 1 2 1
```

For value `1` the gaps are:

```
1, 2, 2, 2
```

Largest gap is `2`, so every segment of length at least `2` must contain a `1`.

The algorithm records:

```
need[1] = 2
```

and produces:

```
-1 1 1 1 1
```

This example shows why the largest gap, not the frequency, is the quantity that determines validity.
