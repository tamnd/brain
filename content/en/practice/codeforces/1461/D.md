---
title: "CF 1461D - Divide and Summarize"
description: "We start with an array and repeatedly apply a very specific splitting rule. For any current array, compute $$mid = leftlfloor frac{min + max}{2} rightrfloor$$ All elements whose value is at most mid form one group, and all elements whose value is greater than mid form the other."
date: "2026-06-11T02:22:34+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "data-structures", "divide-and-conquer", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1461
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 689 (Div. 2, based on Zed Code Competition)"
rating: 1600
weight: 1461
solve_time_s: 126
verified: true
draft: false
---

[CF 1461D - Divide and Summarize](https://codeforces.com/problemset/problem/1461/D)

**Rating:** 1600  
**Tags:** binary search, brute force, data structures, divide and conquer, implementation, sortings  
**Solve time:** 2m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

We start with an array and repeatedly apply a very specific splitting rule.

For any current array, compute

$$mid = \left\lfloor \frac{\min + \max}{2} \right\rfloor$$

All elements whose value is at most `mid` form one group, and all elements whose value is greater than `mid` form the other. After the split, we keep exactly one of the two groups and discard the other.

For every query value `s`, we must decide whether there exists some sequence of such choices that produces an array whose element sum is exactly `s`.

The most important observation is that the split depends only on values, not on positions. Relative order is preserved, but after sorting the array, every split becomes a split of a contiguous value range. That turns the process into a recursive partitioning of the sorted array.

The constraints are large enough that we cannot simulate every query independently. Across all test cases, both the total number of array elements and the total number of queries are at most `10^5`. Any solution around `O(nq)` would be far too slow because it could require about `10^{10}` operations in the worst case. We need something close to `O(n log n)` preprocessing and then very fast query handling.

Several edge cases are easy to miss.

Consider an array where all values are equal:

```
[5, 5, 5, 5]
```

The computed `mid` is also `5`, so every element goes to the left part and the right part is empty. No further split is possible. The only achievable sum is `20`. A careless recursive implementation might recurse forever because the range never shrinks.

Consider:

```
[1, 2]
```

The total sum `3` is achievable without performing any split. Some solutions only record sums after splitting and forget to include the current segment itself. Then query `3` would incorrectly return "No".

Another subtle case is:

```
[1, 1, 100]
```

The first split separates `[1,1]` and `[100]`. Achievable sums are `102`, `2`, and `100`. Query `101` must be rejected even though it lies between achievable sums. The problem is not asking for arbitrary subset sums. Only sums produced by the recursive splitting process matter.

## Approaches

A brute-force interpretation is to explicitly follow every possible sequence of choices. From each current array we may keep either the left part or the right part, creating a binary recursion tree. Every reachable array contributes one achievable sum.

This is correct because it directly matches the definition of the process. Unfortunately, representing arrays and repeatedly repartitioning them is expensive. In the worst case we repeatedly scan large arrays and create many copies. With up to `10^5` elements overall, this approach quickly becomes impractical.

The key observation is that after sorting, every recursive state corresponds to a contiguous segment of the sorted array.

Suppose the sorted array segment is `a[l...r]`. The split threshold is

$$mid = \left\lfloor \frac{a[l] + a[r]}{2} \right\rfloor$$

Since the segment is sorted, all values `<= mid` form a prefix of the segment and all values `> mid` form a suffix. The split position can be found with binary search.

Now we no longer need to track actual arrays. A state is completely described by the index interval `[l, r]`.

Every such segment has a well-defined sum. Any segment that appears during this recursive process corresponds to an achievable array, so we can precompute all achievable sums and store them in a set.

Once all achievable sums are known, each query becomes a simple membership test.

The recursion is efficient because every split divides the value range. A segment is processed only once, and binary search locates the partition point.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in number of splits | Exponential | Too slow |
| Optimal | O(n log n + q) | O(n) | Accepted |

## Algorithm Walkthrough

1. Sort the array.

After sorting, every split corresponds to separating a contiguous segment into two contiguous subsegments.
2. Build a prefix-sum array.

This allows the sum of any segment `[l, r]` to be computed in constant time.
3. Start a recursive procedure on the whole sorted array segment.

The initial segment represents the original array, whose sum is always achievable.
4. For a segment `[l, r]`, compute its sum and insert it into a set.

Every recursive segment corresponds to a valid array obtainable through the allowed operations.
5. If `a[l] == a[r]`, stop.

All values in the segment are identical. Any further split would place every element on the same side, so recursion must terminate.
6. Compute

$$mid = \left\lfloor \frac{a[l] + a[r]}{2} \right\rfloor$$
7. Use binary search to find the first position whose value is greater than `mid`.

This identifies the boundary between the left and right groups exactly as defined by the problem.
8. If the boundary does not actually split the segment, stop.

This prevents useless recursion when one side would be empty.
9. Recursively process the left segment.
10. Recursively process the right segment.
11. After preprocessing finishes, answer every query by checking whether its value exists in the set of achievable sums.

### Why it works

The recursion exactly mirrors the allowed operation.

For any recursive segment `[l, r]`, the values inside it are precisely the elements of some array that can appear during the process. The segment sum is therefore achievable and must be recorded.

Conversely, every legal split in the original process partitions elements according to the threshold `mid`. In a sorted segment, that partition is exactly the binary-search split used by the algorithm. The recursion explores both resulting segments, so every array that can ever appear is represented.

Thus the set built by the recursion contains all achievable sums and only achievable sums. Query answering reduces to checking membership in that set.

## Python Solution

```python
import sys
from bisect import bisect_right

input = sys.stdin.readline

def solve():
    t = int(input())

    answers = []

    for _ in range(t):
        n, q = map(int, input().split())
        a = sorted(map(int, input().split()))

        pref = [0] * (n + 1)
        for i in range(n):
            pref[i + 1] = pref[i] + a[i]

        possible = set()

        def dfs(l, r):
            seg_sum = pref[r + 1] - pref[l]
            possible.add(seg_sum)

            if a[l] == a[r]:
                return

            mid = (a[l] + a[r]) // 2
            p = bisect_right(a, mid, l, r + 1)

            if p == l or p == r + 1:
                return

            dfs(l, p - 1)
            dfs(p, r)

        dfs(0, n - 1)

        for _ in range(q):
            s = int(input())
            answers.append("Yes" if s in possible else "No")

    sys.stdout.write("\n".join(answers))

if __name__ == "__main__":
    solve()
```

The first step sorts the array because the splitting rule depends only on values. Once sorted, every recursive state becomes a contiguous index range.

The prefix-sum array allows segment sums to be computed in constant time. Without it, each recursive call would need to scan its entire segment, increasing complexity significantly.

The `possible` set stores every achievable sum. As soon as a segment is visited, its sum is inserted because that segment itself represents a valid obtainable array.

The stopping condition `a[l] == a[r]` is critical. When all values are equal, no meaningful split exists. Omitting this check can create infinite recursion.

`bisect_right` finds the first value strictly greater than `mid`, matching the problem definition exactly. Values equal to `mid` belong to the left part.

The check

```
if p == l or p == r + 1:
    return
```

protects against empty partitions. Such a split would not reduce the segment.

Finally, each query is answered in constant expected time using set membership.

## Worked Examples

### Example 1

Array:

```
[1, 2, 3, 4, 5]
```

Sorted array is unchanged.

| Segment | Min | Max | Mid | Sum | Split |
| --- | --- | --- | --- | --- | --- |
| [1,2,3,4,5] | 1 | 5 | 3 | 15 | [1,2,3] and [4,5] |
| [1,2,3] | 1 | 3 | 2 | 6 | [1,2] and [3] |
| [1,2] | 1 | 2 | 1 | 3 | [1] and [2] |
| [1] | 1 | 1 | - | 1 | stop |
| [2] | 2 | 2 | - | 2 | stop |
| [3] | 3 | 3 | - | 3 | stop |
| [4,5] | 4 | 5 | 4 | 9 | [4] and [5] |
| [4] | 4 | 4 | - | 4 | stop |
| [5] | 5 | 5 | - | 5 | stop |

The achievable sums are:

```
{1,2,3,4,5,6,9,15}
```

Query `9` returns "Yes", while query `8` returns "No".

This example shows that only sums corresponding to recursive segments are valid.

### Example 2

Array:

```
[3, 1, 3, 1, 3]
```

After sorting:

```
[1, 1, 3, 3, 3]
```

| Segment | Min | Max | Mid | Sum | Split |
| --- | --- | --- | --- | --- | --- |
| [1,1,3,3,3] | 1 | 3 | 2 | 11 | [1,1] and [3,3,3] |
| [1,1] | 1 | 1 | - | 2 | stop |
| [3,3,3] | 3 | 3 | - | 9 | stop |

The achievable sums are:

```
{11, 2, 9}
```

Query `3` returns "No" even though the value `3` exists in the array.

This demonstrates that the task is not about choosing arbitrary subsets.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n + q) | Sorting dominates preprocessing, recursion uses binary searches over generated segments |
| Space | O(n) | Prefix sums, recursion states, and achievable-sum set |

The total sum of `n` and the total sum of `q` over all test cases is at most `10^5`. An `O(n log n + q)` solution easily fits within the time limit, and `O(n)` memory is comfortably below the memory limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from bisect import bisect_right

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []

    for _ in range(t):
        n, q = map(int, input().split())
        a = sorted(map(int, input().split()))

        pref = [0] * (n + 1)
        for i in range(n):
            pref[i + 1] = pref[i] + a[i]

        possible = set()

        def dfs(l, r):
            possible.add(pref[r + 1] - pref[l])

            if a[l] == a[r]:
                return

            mid = (a[l] + a[r]) // 2
            p = bisect_right(a, mid, l, r + 1)

            if p == l or p == r + 1:
                return

            dfs(l, p - 1)
            dfs(p, r)

        dfs(0, n - 1)

        for _ in range(q):
            s = int(input())
            out.append("Yes" if s in possible else "No")

    return "\n".join(out)

# provided sample
assert run(
"""2
5 5
1 2 3 4 5
1
8
9
12
6
5 5
3 1 3 1 3
1
2
3
9
11
"""
) == """Yes
No
Yes
No
Yes
No
Yes
No
Yes
Yes"""

# minimum size
assert run(
"""1
1 3
7
7
1
14
"""
) == """Yes
No
No"""

# all equal values
assert run(
"""1
4 3
5 5 5 5
20
5
10
"""
) == """Yes
No
No"""

# simple split
assert run(
"""1
2 3
1 2
1
2
3
"""
) == """Yes
Yes
Yes"""

# uneven values
assert run(
"""1
3 4
1 1 100
2
100
102
101
"""
) == """Yes
Yes
Yes
No"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single element array | Only total sum achievable | Base recursion case |
| All equal values | No further splitting | Infinite-recursion prevention |
| `[1,2]` | Sums 1, 2, and 3 achievable | Correct handling of total segment sum |
| `[1,1,100]` | 101 rejected | Not an arbitrary subset-sum problem |

## Edge Cases

### All values are identical

Input:

```
1
4 2
5 5 5 5
20
10
```

The sorted segment has `a[l] = a[r] = 5`.

The algorithm records sum `20` and immediately stops recursion. The achievable set becomes:

```
{20}
```

Query `20` returns "Yes" and query `10` returns "No". This matches the process because every split would place all elements into the same group.

### Total sum without any split

Input:

```
1
2 1
1 2
3
```

The original array itself is a valid obtainable array because zero operations are allowed.

The algorithm records the root segment sum before attempting any split, so `3` is inserted into the set immediately.

The answer is correctly `"Yes"`.

### Query between achievable sums

Input:

```
1
1 4
1 1 100
101
```

The recursion generates sums:

```
102, 2, 100
```

No segment has sum `101`.

The algorithm answers `"No"` because membership is checked against the exact set of achievable sums, not against any interval or subset-sum criterion.

### Values equal to the split threshold

Input:

```
1
3 2
2 2 3
4
3
```

Here:

```
mid = (2 + 3) // 2 = 2
```

Both occurrences of `2` must belong to the left segment.

`bisect_right` finds the first element strictly greater than `2`, producing segments `[2,2]` and `[3]`.

Achievable sums become:

```
7, 4, 3
```

Queries `4` and `3` both return `"Yes"`. This confirms that values equal to `mid` are handled correctly.
