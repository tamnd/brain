---
title: "CF 105809K - K-token Language Optimization"
description: "We are given an array of length n and a limit k. We want to split the array into the smallest possible number of contiguous segments. Inside every segment, the number of distinct values must not exceed k. The task is not to count all valid partitions."
date: "2026-06-25T15:30:10+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105809
codeforces_index: "K"
codeforces_contest_name: "Code Rush 2025"
rating: 0
weight: 105809
solve_time_s: 40
verified: true
draft: false
---

[CF 105809K - K-token Language Optimization](https://codeforces.com/problemset/problem/105809/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 40s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of length `n` and a limit `k`. We want to split the array into the smallest possible number of contiguous segments. Inside every segment, the number of distinct values must not exceed `k`.

The task is not to count all valid partitions. We only need the minimum number of segments needed to cover the entire array while respecting the distinct-value limit.

The constraints are quite revealing. The array length can reach `10^5`, so any algorithm that examines all subarrays or performs dynamic programming over all intervals is far too expensive. An `O(n²)` solution would require around `10^10` operations in the worst case, which is completely infeasible. We need something close to linear time.

Another useful observation comes from the value range. Every array element satisfies `1 ≤ a[i] ≤ 1000`, and `k ≤ 1000`. Since values are small, maintaining frequencies of elements inside a sliding window is very cheap.

A common mistake is to think that balancing segment lengths might help. The objective is only to minimize the number of segments. Segment sizes themselves are irrelevant.

Consider the array:

```
3 1
1 2 3
```

Every segment may contain at most one distinct value. The only valid partition is:

```
[1] [2] [3]
```

The answer is:

```
3
```

Another easy-to-miss case is:

```
5 2
1 2 1 2 3
```

A careless strategy might cut as soon as the segment already contains `k` distinct values. That would produce:

```
[1 2 1 2] [3]
```

which is actually optimal and gives answer `2`.

The important detail is that a segment may contain exactly `k` distinct values. We only need to cut when adding the next element would increase the count beyond `k`.

A third edge case is when all values are identical:

```
3 1
1 1 1
```

The entire array already satisfies the condition, so the answer is:

```
1
```

Any implementation that blindly creates a new segment whenever it encounters a repeated boundary would fail here.

## Approaches

The most direct brute-force idea is to build segments from left to right and, for every starting position, try all possible ending positions while counting distinct values. Once a segment is chosen, recurse on the remaining suffix.

This works because every valid partition can be explored. The problem is the number of intervals. There are `O(n²)` subarrays, and even checking distinct counts efficiently does not rescue the overall complexity. With `n = 10^5`, such an approach is hopeless.

The key observation is that we only need the minimum number of segments, and each segment is constrained by a maximum number of distinct values.

Suppose we are currently building a segment. As long as adding the next element keeps the number of distinct values at most `k`, extending the segment can never hurt. Making a segment longer only leaves fewer elements for later segments. Since our goal is to minimize the number of segments, we should always extend the current segment as far as possible.

This immediately suggests a greedy strategy. Start a segment, keep adding elements while the segment contains at most `k` distinct values, and the moment the next element would create the `(k+1)`-th distinct value, close the current segment and start a new one from that element.

Why is this greedy choice optimal? Any valid partition must end the current segment no later than the point where the `(k+1)`-th distinct value appears. Our greedy segment is the longest valid one. Replacing any shorter first segment by this longest valid segment cannot increase the number of segments needed later. Repeating the same argument for the remaining suffix proves optimality.

Because values are at most `1000`, we can maintain frequencies and the current number of distinct values in constant time per element. Each element is processed exactly once.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal Greedy Counting Distinct Values | O(n) | O(1000) | Accepted |

## Algorithm Walkthrough

1. Create a frequency array for values `1..1000`.
2. Start with one segment and an empty frequency structure.
3. Traverse the array from left to right.
4. For the current value `x`, check whether it already exists in the current segment.
5. If `x` is new and the current segment already contains exactly `k` distinct values, then adding `x` would violate the constraint. Start a new segment.

Reset all frequencies, reset the distinct counter to zero, and increase the answer by one.
6. Insert `x` into the current segment by updating its frequency.
7. If this is the first occurrence of `x` in the current segment, increase the distinct counter.
8. After processing all elements, output the number of segments.

### Why it works

At any point, the current segment maintained by the algorithm is the longest valid segment ending at the current position. Whenever a new distinct value would make the count exceed `k`, every valid partition is forced to end the current segment before that value. The greedy choice delays the cut as much as possible, producing the largest feasible segment. A larger first segment can never require more segments for the remaining suffix than a smaller first segment. Applying this argument repeatedly yields a partition with the minimum possible number of segments.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, k = map(int, input().split())
a = list(map(int, input().split()))

freq = [0] * 1001
distinct = 0
ans = 1

for x in a:
    if freq[x] == 0 and distinct == k:
        ans += 1
        freq = [0] * 1001
        distinct = 0

    if freq[x] == 0:
        distinct += 1
    freq[x] += 1

print(ans)
```

The implementation follows the greedy strategy exactly.

The variable `distinct` stores the number of different values currently present in the active segment. The frequency array lets us determine in constant time whether a value is appearing for the first time inside that segment.

The subtle part is the order of operations. We must first check whether adding the current value would exceed the distinct-value limit. Only after deciding whether a new segment is needed do we insert the value.

When a new segment starts, the current element belongs to that new segment. This is why the insertion logic runs after the reset.

The value range is bounded by `1000`, so resetting the frequency array costs only `O(1000)` time. Since at most `n` segments can exist and `1000` is a constant, the overall complexity remains linear.

## Worked Examples

### Example 1

Input:

```
3 2
1 2 3
```

| Position | Value | Distinct Before | Action | Segments |
| --- | --- | --- | --- | --- |
| 1 | 1 | 0 | Add | 1 |
| 2 | 2 | 1 | Add | 1 |
| 3 | 3 | 2 | New segment needed | 2 |

Output:

```
2
```

The first segment becomes `[1, 2]`. Adding `3` would create a third distinct value, so a new segment starts.

### Example 2

Input:

```
5 2
1 2 1 2 3
```

| Position | Value | Distinct Before | Action | Segments |
| --- | --- | --- | --- | --- |
| 1 | 1 | 0 | Add | 1 |
| 2 | 2 | 1 | Add | 1 |
| 3 | 1 | 2 | Add | 1 |
| 4 | 2 | 2 | Add | 1 |
| 5 | 3 | 2 | New segment needed | 2 |

Output:

```
2
```

This trace shows why we should keep extending the segment while the distinct count stays within the limit. The first four elements fit in a single segment.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each array element is processed once |
| Space | O(1000) | Frequency array for values 1..1000 |

Since `n` is at most `10^5`, a linear-time solution easily fits within the limits. The memory usage is constant with respect to `n`.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    freq = [0] * 1001
    distinct = 0
    ans = 1

    for x in a:
        if freq[x] == 0 and distinct == k:
            ans += 1
            freq = [0] * 1001
            distinct = 0

        if freq[x] == 0:
            distinct += 1
        freq[x] += 1

    print(ans)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out.getvalue().strip()

# provided samples
assert run("3 1\n1 2 3\n") == "3"
assert run("3 2\n1 2 3\n") == "2"
assert run("3 1\n1 1 1\n") == "1"

# custom cases
assert run("1 1\n7\n") == "1"
assert run("5 5\n1 2 3 4 5\n") == "1"
assert run("6 2\n1 2 1 2 1 2\n") == "1"
assert run("6 2\n1 2 3 1 2 3\n") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 7` | `1` | Minimum-size input |
| `5 5 / 1 2 3 4 5` | `1` | Distinct count exactly equals k |
| `6 2 / 1 2 1 2 1 2` | `1` | Repeated values do not create new segments |
| `6 2 / 1 2 3 1 2 3` | `3` | Multiple forced cuts |

## Edge Cases

Consider:

```
3 1
1 2 3
```

The algorithm starts with segment count `1`. After reading `1`, the segment has one distinct value. Reading `2` would create a second distinct value while `k = 1`, so a new segment begins. The same happens for `3`. The final answer is `3`, which is optimal because every segment may contain only one distinct value.

Now consider:

```
5 2
1 2 1 2 3
```

After processing the first four elements, the segment contains exactly two distinct values, `{1,2}`. When `3` appears, adding it would create a third distinct value. The algorithm starts a new segment and places `3` there. The answer becomes `2`. Any partition with one segment is invalid because the whole array contains three distinct values.

Finally:

```
3 1
1 1 1
```

The distinct count never exceeds one. No cut is ever required, and the algorithm outputs `1`. This confirms that repeated occurrences of an already-present value do not affect the distinct-value limit.
