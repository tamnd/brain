---
title: "CF 160C - Find Pair"
description: "We are given an array of n integers. From this array, we form every ordered pair (a[i], a[j]), including pairs where i = j. Since both positions are chosen independently, there are exactly n² pairs. All these pairs are sorted lexicographically."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 160
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 111 (Div. 2)"
rating: 1700
weight: 160
solve_time_s: 107
verified: true
draft: false
---

[CF 160C - Find Pair](https://codeforces.com/problemset/problem/160/C)

**Rating:** 1700  
**Tags:** implementation, math, sortings  
**Solve time:** 1m 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of `n` integers. From this array, we form every ordered pair `(a[i], a[j])`, including pairs where `i = j`. Since both positions are chosen independently, there are exactly `n²` pairs.

All these pairs are sorted lexicographically. That means pairs are ordered first by the first value, and if those are equal, by the second value.

The task is to output the `k`-th pair in this sorted order.

The constraints completely rule out generating all pairs directly. When `n = 10^5`, the total number of pairs becomes `10^10`, which is far beyond what can fit in memory or be processed in time. Even iterating over all pairs once would already be impossible under a 1 second limit.

This forces us to exploit the structure of lexicographic ordering instead of constructing the list explicitly.

A subtle point is that the array may contain duplicate values. The ordering is based on values, not indices. If the array is `[1, 1, 2]`, then pairs starting with `1` appear multiple times because there are two occurrences of `1`.

For example:

```
Input:
3 4
1 1 2
```

All pairs after sorting are:

```
(1,1)
(1,1)
(1,2)
(1,1)
(1,1)
(1,2)
(2,1)
(2,1)
(2,2)
```

The 4-th pair is `(1,1)`.

A careless implementation that compresses duplicates into unique values would produce the wrong multiplicities.

Another easy mistake is mixing 0-based and 1-based indexing for `k`.

Consider:

```
Input:
2 1
5 7
```

Sorted pairs:

```
(5,5)
(5,7)
(7,5)
(7,7)
```

The first pair is `(5,5)`.

If we subtract one from `k` too late or too early, we may accidentally return `(5,7)` instead.

Large values also matter because `k` can be as large as `n² = 10^10`. A 32-bit integer is not enough in some languages. Python handles this naturally, but in C++ we would need `long long`.

## Approaches

The brute-force idea is straightforward. Generate all `n²` ordered pairs, sort them lexicographically, then print the `k`-th pair.

This works because lexicographic sorting directly matches the problem statement. The issue is scale. With `n = 10^5`, the number of pairs becomes `10^10`. Even storing the pairs would require enormous memory, and sorting them would be completely infeasible.

The key observation is that lexicographic ordering has a very regular structure after sorting the original array.

Suppose the sorted array is:

```
b[0], b[1], ..., b[n-1]
```

Then every pair beginning with `b[0]` comes first, followed by every pair beginning with `b[1]`, and so on.

Each element contributes exactly `n` consecutive pairs as the first component.

For example, if:

```
b = [1, 2, 5]
```

then the sorted pairs are grouped like this:

```
First element = 1:
(1,1), (1,2), (1,5)

First element = 2:
(2,1), (2,2), (2,5)

First element = 5:
(5,1), (5,2), (5,5)
```

This means the first element of the answer can be found by determining which block of size `n` contains the `k`-th pair.

Once the first value is fixed, the second value is determined by the position inside that block.

Duplicates complicate things slightly because several consecutive indices may contain the same value. If a value appears `cnt` times, then all pairs starting with that value occupy `cnt * n` consecutive positions.

The second component is also chosen from the sorted array. After we identify the first value, we only need to determine which element of the sorted array corresponds to the remaining offset.

This reduces the problem to arithmetic on sorted positions instead of explicit pair generation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n² log n²) | O(n²) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the array and sort it.

Lexicographic order depends only on values, so sorting the array reveals the exact structure of the pair ordering.
2. Convert `k` to 0-based indexing by subtracting 1.

This makes block calculations easier because integer division works naturally with 0-based offsets.
3. Compute the index of the first element as `first_idx = k // n`.

Every element in the sorted array contributes exactly `n` pairs as the first component. Dividing by `n` tells us which block contains the answer.
4. Let `first_value = b[first_idx]`.

This is the first number of the answer pair.
5. Count how many times `first_value` appears in the sorted array.

Suppose it appears `cnt` times and its first occurrence is at index `l`.

Then all pairs beginning with `first_value` occupy one large contiguous segment of size `cnt * n`.
6. Compute how far the desired pair is inside this segment.

The number of pairs before this segment is `l * n`.

So:

```
offset = k - l * n
```
7. The second element is determined by:

```
second_idx = offset // cnt
```

Each distinct second value repeats `cnt` times because there are `cnt` identical choices for the first component.
8. Output:

```
(first_value, b[second_idx])
```

### Why it works

After sorting the array, lexicographic ordering groups pairs by their first component. Every occurrence of a value contributes a full block of `n` pairs.

If a value appears multiple times, those blocks become adjacent because the first components are equal. Inside this combined segment, the second elements appear in sorted order, and each one repeats exactly `cnt` times, once for every occurrence of the first value.

The algorithm identifies exactly which segment contains the `k`-th pair, then determines which repeated second value corresponds to the remaining offset. Since the structure matches lexicographic ordering exactly, the produced pair must be correct.

## Python Solution

```python
import sys
from bisect import bisect_left, bisect_right

input = sys.stdin.readline

n, k = map(int, input().split())
a = list(map(int, input().split()))

a.sort()

k -= 1

first_idx = k // n
first_value = a[first_idx]

left = bisect_left(a, first_value)
right = bisect_right(a, first_value)

cnt = right - left

offset = k - left * n
second_idx = offset // cnt

print(first_value, a[second_idx])
```

The solution begins by sorting the array because lexicographic pair order directly follows sorted value order.

After converting `k` into 0-based indexing, the expression `k // n` identifies which group of pairs the answer belongs to. Every index contributes exactly `n` pairs as the first component, so integer division isolates the correct block immediately.

The next step finds the full range of equal values using `bisect_left` and `bisect_right`. This is necessary because duplicate first values merge into one larger segment in the lexicographic ordering.

The expression:

```
offset = k - left * n
```

removes all pairs belonging to smaller first values. What remains is the position inside the segment where the first component equals `first_value`.

Inside this segment, every second value appears exactly `cnt` times consecutively. Dividing by `cnt` gives the correct second element index.

One subtle point is that `second_idx` refers directly to the sorted array. We do not compress duplicates because repeated values must remain repeated in the ordering.

Another subtle detail is using integer division everywhere. Since the ordering forms perfectly regular blocks, floor division maps positions to values without any binary search or simulation.

## Worked Examples

### Example 1

Input:

```
2 4
2 1
```

Sorted array:

```
[1, 2]
```

After converting to 0-based indexing:

```
k = 3
```

| Step | Value |
| --- | --- |
| `first_idx = k // n` | `3 // 2 = 1` |
| `first_value` | `2` |
| `left` | `1` |
| `right` | `2` |
| `cnt` | `1` |
| `offset = k - left*n` | `3 - 2 = 1` |
| `second_idx = offset // cnt` | `1 // 1 = 1` |
| Answer | `(2, 2)` |

This example shows the simplest possible block structure. Every value appears once, so each first component owns exactly one block of size `n`.

### Example 2

Input:

```
3 2
3 1 5
```

Sorted array:

```
[1, 3, 5]
```

After converting to 0-based indexing:

```
k = 1
```

| Step | Value |
| --- | --- |
| `first_idx = k // n` | `1 // 3 = 0` |
| `first_value` | `1` |
| `left` | `0` |
| `right` | `1` |
| `cnt` | `1` |
| `offset = k - left*n` | `1 - 0 = 1` |
| `second_idx = offset // cnt` | `1 // 1 = 1` |
| Answer | `(1, 3)` |

This trace demonstrates how the second component is selected inside the block corresponding to the first value.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates the runtime |
| Space | O(n) | The sorted array is stored |

The solution easily fits the constraints. Sorting `10^5` integers is fast enough for a 1 second limit in Python, and all remaining operations are constant time or logarithmic due to binary search.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from bisect import bisect_left, bisect_right

def solve():
    input = sys.stdin.readline

    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    a.sort()

    k -= 1

    first_idx = k // n
    first_value = a[first_idx]

    left = bisect_left(a, first_value)
    right = bisect_right(a, first_value)

    cnt = right - left

    offset = k - left * n
    second_idx = offset // cnt

    print(first_value, a[second_idx])

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out.strip()

# provided samples
assert run("2 4\n2 1\n") == "2 2", "sample 1"
assert run("3 2\n3 1 5\n") == "1 3", "sample 2"

# minimum size
assert run("1 1\n42\n") == "42 42", "single element"

# all equal values
assert run("3 5\n7 7 7\n") == "7 7", "all equal"

# duplicate handling
assert run("3 4\n1 1 2\n") == "1 1", "duplicate multiplicity"

# last possible pair
assert run("2 4\n1 5\n") == "5 5", "largest k"

print("All tests passed")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 42` | `42 42` | Minimum-size array |
| `3 5 / 7 7 7` | `7 7` | All values identical |
| `3 4 / 1 1 2` | `1 1` | Duplicate multiplicities handled correctly |
| `2 4 / 1 5` | `5 5` | Largest valid `k` |

## Edge Cases

Consider the duplicate-heavy case:

```
Input:
3 4
1 1 2
```

Sorted array:

```
[1, 1, 2]
```

All pairs in order are:

```
(1,1)
(1,1)
(1,2)
(1,1)
(1,1)
(1,2)
(2,1)
(2,1)
(2,2)
```

The correct answer is the 4-th pair, `(1,1)`.

The algorithm computes:

```
k = 3
first_idx = 1
first_value = 1
cnt = 2
offset = 3
second_idx = 1
```

which gives `(1,1)`.

This works because the algorithm preserves multiplicities instead of compressing equal values.

Now consider the smallest possible input:

```
Input:
1 1
42
```

There is only one pair:

```
(42,42)
```

The algorithm computes:

```
k = 0
first_idx = 0
second_idx = 0
```

and returns `(42,42)` correctly.

Finally, consider the largest lexicographic pair:

```
Input:
2 4
1 5
```

Sorted pairs are:

```
(1,1)
(1,5)
(5,1)
(5,5)
```

The 4-th pair is `(5,5)`.

The algorithm finds:

```
k = 3
first_idx = 1
first_value = 5
offset = 1
second_idx = 1
```

which correctly points to the last pair in the ordering.
