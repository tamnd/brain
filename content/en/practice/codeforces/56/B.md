---
title: "CF 56B - Spoilt Permutation"
description: "We start from the sorted permutation 1 2 3 ... n. Someone chooses exactly one contiguous segment and reverses it. We are given the final permutation and must determine whether it could have been produced by exactly one such reversal. The task is not to sort the array."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 56
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 52 (Div. 2)"
rating: 1300
weight: 56
solve_time_s: 102
verified: true
draft: false
---

[CF 56B - Spoilt Permutation](https://codeforces.com/problemset/problem/56/B)

**Rating:** 1300  
**Tags:** implementation  
**Solve time:** 1m 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We start from the sorted permutation `1 2 3 ... n`. Someone chooses exactly one contiguous segment and reverses it. We are given the final permutation and must determine whether it could have been produced by exactly one such reversal.

The task is not to sort the array. We only need to identify a segment `[l, r]` such that reversing that segment in the original sorted array produces the given permutation. If no such segment exists, we print `0 0`.

The constraints are small, `n ≤ 1000`, so even quadratic algorithms are acceptable. An `O(n^2)` solution performs around one million operations in the worst case, which is trivial within a 2-second limit. This means we do not need sophisticated data structures or advanced algorithms. A clean implementation is more important than micro-optimizations.

The tricky part is not efficiency, it is correctness around edge cases.

One easy mistake is forgetting that the reversal must come from the original sorted array, not from some intermediate permutation. Consider:

```
5
1 3 2 5 4
```

A careless approach might notice two decreasing segments and try to combine them somehow. But one reversal cannot simultaneously swap both `(2,3)` and `(4,5)`. The correct output is:

```
0 0
```

Another subtle case happens when the permutation is already sorted:

```
4
1 2 3 4
```

The statement requires reversing a segment with different endpoints. No reversal changes the array into itself unless we reverse a length-1 segment, which is forbidden because `l < r`. The correct answer is:

```
0 0
```

A naive implementation that simply searches for mismatches might incorrectly print something like `1 1`.

A third edge case is when the reversed segment touches the boundaries:

```
5
5 4 3 2 1
```

Here the entire array was reversed, so the correct answer is:

```
1 5
```

Off-by-one mistakes are common here because the segment starts at the first element and ends at the last.

## Approaches

The brute-force idea is straightforward. Since the original permutation is always `1 2 3 ... n`, we can try every possible pair `(l, r)`, reverse that segment, and check whether the result matches the input permutation.

There are `O(n^2)` possible segments. Reversing and comparing arrays costs `O(n)` time, so the total complexity becomes `O(n^3)`. With `n = 1000`, this means roughly one billion operations in the worst case, which is too slow in Python.

The structure of the problem gives us a much better observation. If the permutation was created by reversing one segment, then everywhere outside that segment the numbers must still appear in their original positions.

That means the first index where `a[i] != i + 1` must be the left endpoint of the reversed segment. Similarly, once we start moving through the reversed segment, the values must decrease exactly as a reversal would produce.

For example:

```
1 6 5 4 3 2 7 8
```

The first mismatch occurs at position `2`. From there, the numbers decrease until position `6`. Reversing that interval in the original sorted array reconstructs the permutation exactly.

This reduces the task to identifying one candidate segment and verifying it. We only scan the array a constant number of times, so the complexity becomes linear.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n³) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the permutation.
2. Find the first position `l` where `a[l] != l + 1`.

If no such position exists, the permutation is already sorted, so no valid reversal exists. Print `0 0`.
3. Starting from `l`, extend `r` while the sequence is strictly decreasing.

A reversed segment taken from a sorted array must appear in decreasing order in the final permutation. This step identifies the maximal candidate segment.
4. Reverse the subarray from `l` to `r`.

We perform the reversal directly on a copy of the permutation to test whether this operation restores the sorted order.
5. Check whether the resulting array equals `1 2 3 ... n`.

If yes, print `l + 1` and `r + 1` using 1-based indexing.

Otherwise, print `0 0`.

### Why it works

The first incorrect position must belong to the reversed segment, because positions before it already match the original sorted permutation.

Inside the reversed segment, values must appear in decreasing order. Since the original array was strictly increasing, reversing any contiguous portion flips that order exactly once. Extending `r` while the sequence decreases identifies the only possible candidate segment.

If reversing that segment restores the sorted array, then the permutation was produced by exactly one reversal. If it does not, no other segment can work, because any valid segment must start at the first mismatch and follow the decreasing pattern created by reversal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    l = -1

    for i in range(n):
        if a[i] != i + 1:
            l = i
            break

    if l == -1:
        print(0, 0)
        return

    r = l

    while r + 1 < n and a[r] > a[r + 1]:
        r += 1

    b = a[:]
    b[l:r + 1] = reversed(b[l:r + 1])

    if b == list(range(1, n + 1)):
        print(l + 1, r + 1)
    else:
        print(0, 0)

solve()
```

The first loop searches for the earliest mismatch between the permutation and the sorted order. This identifies where the reversed segment must begin.

If no mismatch exists, the permutation is already sorted. Since the problem requires `l < r`, we cannot use an empty operation or a length-1 reversal, so the answer becomes `0 0`.

The second loop expands the right boundary while the sequence keeps decreasing. This captures the exact shape produced by reversing an increasing segment from the original permutation.

The line:

```
b[l:r + 1] = reversed(b[l:r + 1])
```

creates the corrected version of the array after undoing the suspected reversal.

Finally, we compare against the sorted permutation. This verification step is essential because a decreasing segment alone is not sufficient. Arrays like:

```
1 5 4 3 2 6 8 7
```

contain multiple disturbed regions and cannot be fixed with one reversal.

Using a copied array avoids modifying the original data accidentally. The boundaries use Python slicing conventions carefully, where `r + 1` is needed because the right endpoint is exclusive.

## Worked Examples

### Example 1

Input:

```
8
1 6 5 4 3 2 7 8
```

| Step | l | r | Array State |
| --- | --- | --- | --- |
| Find first mismatch | 1 | - | 1 6 5 4 3 2 7 8 |
| Extend decreasing segment | 1 | 5 | 1 6 5 4 3 2 7 8 |
| Reverse segment | 1 | 5 | 1 2 3 4 5 6 7 8 |
| Verification | 1 | 5 | Sorted |

Output:

```
2 6
```

The decreasing region `6 5 4 3 2` matches exactly what reversing `[2,6]` would produce from a sorted array.

### Example 2

Input:

```
5
1 3 2 5 4
```

| Step | l | r | Array State |
| --- | --- | --- | --- |
| Find first mismatch | 1 | - | 1 3 2 5 4 |
| Extend decreasing segment | 1 | 2 | 1 3 2 5 4 |
| Reverse segment | 1 | 2 | 1 2 3 5 4 |
| Verification | 1 | 2 | Not sorted |

Output:

```
0 0
```

The first reversal fixes the pair `(3,2)` but leaves `(5,4)` broken. This confirms that one reversal is insufficient.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | We scan the array a constant number of times |
| Space | O(n) | We store a copy of the permutation for verification |

With `n ≤ 1000`, even quadratic solutions would pass comfortably. The linear approach is easily fast enough and keeps the implementation simple and reliable.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def solve():
        n = int(input())
        a = list(map(int, input().split()))

        l = -1

        for i in range(n):
            if a[i] != i + 1:
                l = i
                break

        if l == -1:
            return "0 0"

        r = l

        while r + 1 < n and a[r] > a[r + 1]:
            r += 1

        b = a[:]
        b[l:r + 1] = reversed(b[l:r + 1])

        if b == list(range(1, n + 1)):
            return f"{l + 1} {r + 1}"

        return "0 0"

    return solve()

# provided sample
assert run("8\n1 6 5 4 3 2 7 8\n") == "2 6", "sample 1"

# already sorted
assert run("4\n1 2 3 4\n") == "0 0", "already sorted"

# reverse whole array
assert run("5\n5 4 3 2 1\n") == "1 5", "entire array reversed"

# impossible with one reversal
assert run("5\n1 3 2 5 4\n") == "0 0", "two separate disruptions"

# minimum valid reversal
assert run("2\n2 1\n") == "1 2", "smallest valid segment"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 2 3 4` | `0 0` | Already sorted permutations are invalid |
| `5 4 3 2 1` | `1 5` | Segment may cover the whole array |
| `1 3 2 5 4` | `0 0` | One reversal cannot fix multiple disturbed regions |
| `2 1` | `1 2` | Smallest non-trivial case |

## Edge Cases

Consider the already sorted permutation:

```
4
1 2 3 4
```

The algorithm scans for the first mismatch and finds none, so `l` remains `-1`. At this point it immediately prints:

```
0 0
```

This is correct because the problem requires a reversal with distinct endpoints.

Now consider a reversal touching both boundaries:

```
5
5 4 3 2 1
```

The first mismatch occurs at index `0`. The decreasing scan continues all the way to index `4`. Reversing that segment restores the sorted order exactly, so the algorithm outputs:

```
1 5
```

This confirms that boundary indices are handled correctly.

Finally, examine a permutation with two separate broken regions:

```
5
1 3 2 5 4
```

The first mismatch appears at position `2`. The decreasing segment becomes only `3 2`. Reversing it produces:

```
1 2 3 5 4
```

The array is still not sorted, so verification fails and the algorithm prints:

```
0 0
```

This final verification step prevents false positives from local decreasing segments that do not represent a single global reversal.
