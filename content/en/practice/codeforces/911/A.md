---
title: "CF 911A - Nearest Minimums"
description: "We are given an array of integers. Among all values in the array, there is a smallest value, and the problem guarantees that this minimum value appears at least twice. Our task is to find the smallest distance between any two occurrences of that minimum value."
date: "2026-06-12T10:19:32+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 911
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 35 (Rated for Div. 2)"
rating: 1100
weight: 911
solve_time_s: 210
verified: true
draft: false
---

[CF 911A - Nearest Minimums](https://codeforces.com/problemset/problem/911/A)

**Rating:** 1100  
**Tags:** implementation  
**Solve time:** 3m 30s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers. Among all values in the array, there is a smallest value, and the problem guarantees that this minimum value appears at least twice.

Our task is to find the smallest distance between any two occurrences of that minimum value. The distance between positions is simply the difference between their indices.

For example, in the array:

```
[5, 2, 7, 2, 9]
```

the minimum value is `2`, appearing at indices `1` and `3`. Their distance is `3 - 1 = 2`, so the answer is `2`.

The array size can be as large as `100000`. With this constraint, an algorithm that compares every pair of positions would require roughly `10^10` operations in the worst case, which is far beyond what can run within a 2-second time limit. We need a solution that processes the array in linear time.

A few edge cases deserve attention.

Consider an array where every element is the minimum:

```
4
1 1 1 1
```

The minimum appears at indices `0, 1, 2, 3`. The nearest pair is adjacent, so the answer is `1`. A careless implementation that only compares the first and last occurrence would incorrectly return `3`.

Consider a case where minimum values are separated unevenly:

```
5
2 8 2 3 2
```

The minimum appears at indices `0, 2, 4`. Distances are `2` and `2`, so the answer is `2`. We must examine all consecutive occurrences, not just one pair.

Another important case is the smallest valid input:

```
2
3 3
```

The minimum occurs at both positions, and the answer is `1`. Off-by-one mistakes in index calculations often show up on this boundary case.

## Approaches

A straightforward solution is to first locate all occurrences of the minimum value, then compare every pair of those occurrences and take the smallest distance.

This works because the answer is defined as the minimum distance between two positions containing the minimum value. If there are `k` occurrences, we could examine all `k(k-1)/2` pairs and compute their distances.

The problem appears when many elements are equal to the minimum. In the worst case, all `100000` elements are minimums. Then we would need about:

```
100000 × 99999 / 2 ≈ 5 × 10^9
```

pair comparisons, which is far too slow.

The key observation is that after we know the minimum value, only its positions matter. Suppose the minimum occurs at positions:

```
p1 < p2 < p3 < ... < pk
```

If we want the smallest distance between any two occurrences, it must occur between two consecutive positions in this sorted list.

Why? If we take positions `pi` and `pj` with `j > i + 1`, then there is at least one occurrence between them. The distance `pj - pi` is larger than either neighboring gap inside that interval. Such a pair can never produce the minimum distance.

That means we only need to examine consecutive occurrences of the minimum value.

We can first find the minimum element of the array. Then we scan the array again, remembering the most recent position where the minimum appeared. Every time we find another occurrence, we compute the distance to the previous one and update the answer.

This gives a linear-time solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the array.
2. Find the minimum value in the array.
3. Initialize `last = -1` to represent that no occurrence of the minimum has been seen yet.
4. Initialize `answer` with a very large value.
5. Scan the array from left to right.
6. Whenever the current element equals the minimum value:

1. If `last` already stores a previous occurrence, compute the distance `current_index - last`.
2. Update `answer` if this distance is smaller.
3. Store the current index in `last`.
7. After the scan finishes, print `answer`.

The reason this works is that the scan naturally encounters minimum occurrences in increasing index order. Each computed distance is exactly the gap between two consecutive occurrences of the minimum value.

### Why it works

Let the positions of the minimum value be:

```
p1 < p2 < p3 < ... < pk
```

The algorithm computes all distances:

```
p2 - p1
p3 - p2
...
pk - p(k-1)
```

Consider any non-consecutive pair `pi` and `pj` with `j > i + 1`. Its distance is:

```
pj - pi
```

Inside this interval there is at least one consecutive gap. That consecutive gap is less than or equal to `pj - pi`. Consequently, the smallest possible distance between two occurrences must appear among consecutive occurrences.

Since the algorithm checks every consecutive pair exactly once and takes the minimum of those distances, it always returns the correct answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    mn = min(a)

    last = -1
    ans = n

    for i in range(n):
        if a[i] == mn:
            if last != -1:
                ans = min(ans, i - last)
            last = i

    print(ans)

if __name__ == "__main__":
    solve()
```

The first step is finding the minimum value of the array. Only occurrences of this value can contribute to the answer, so all other elements can be ignored afterward.

The variable `last` stores the most recent index where the minimum value appeared. When another occurrence is found, the distance between the two indices is exactly the gap between consecutive minimums.

The variable `ans` tracks the smallest gap seen so far. It is initialized to `n`, which is safely larger than any valid answer because the maximum distance between two indices in an array of length `n` is `n - 1`.

A common mistake is updating `last` before computing the distance. Doing so would compare an index with itself and always produce zero. The correct order is to compute the gap first, then update `last`.

There are no overflow concerns because index differences are at most `99999`, well within Python's integer range.

## Worked Examples

### Example 1

Input:

```
2
3 3
```

Minimum value is `3`.

| i | a[i] | last before | Distance | ans after | last after |
| --- | --- | --- | --- | --- | --- |
| 0 | 3 | -1 | - | 2 | 0 |
| 1 | 3 | 0 | 1 | 1 | 1 |

Output:

```
1
```

This example shows the smallest valid input. The algorithm correctly detects the second occurrence and computes the distance to the previous one.

### Example 2

Input:

```
6
4 1 7 1 9 1
```

Minimum value is `1`.

| i | a[i] | last before | Distance | ans after | last after |
| --- | --- | --- | --- | --- | --- |
| 0 | 4 | -1 | - | 6 | -1 |
| 1 | 1 | -1 | - | 6 | 1 |
| 2 | 7 | 1 | - | 6 | 1 |
| 3 | 1 | 1 | 2 | 2 | 3 |
| 4 | 9 | 3 | - | 2 | 3 |
| 5 | 1 | 3 | 2 | 2 | 5 |

Output:

```
2
```

This trace demonstrates the core invariant. At every minimum occurrence, `last` contains the previous minimum position, so each computed distance is a gap between consecutive minimums.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One pass to find the minimum and one pass to compute nearest occurrences |
| Space | O(1) | Only a few variables are used regardless of input size |

With `n ≤ 100000`, linear time is easily fast enough. The memory usage remains constant, far below the available limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    def input():
        return sys.stdin.readline()

    n = int(input())
    a = list(map(int, input().split()))

    mn = min(a)

    last = -1
    ans = n

    for i in range(n):
        if a[i] == mn:
            if last != -1:
                ans = min(ans, i - last)
            last = i

    return str(ans)

# provided sample
assert run("2\n3 3\n") == "1", "sample 1"

# minimum size input
assert run("2\n1 1\n") == "1", "minimum size"

# all values equal
assert run("4\n5 5 5 5\n") == "1", "all equal"

# uneven gaps between minimums
assert run("5\n2 8 2 3 2\n") == "2", "multiple minimum positions"

# nearest pair at the end
assert run("6\n1 7 8 9 1 1\n") == "1", "adjacent minimums at end"

# larger spacing
assert run("7\n4 1 5 6 7 1 8\n") == "4", "distance calculation"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 / 1 1` | `1` | Smallest legal input |
| `4 / 5 5 5 5` | `1` | All elements are minimums |
| `5 / 2 8 2 3 2` | `2` | Multiple minimum occurrences |
| `6 / 1 7 8 9 1 1` | `1` | Adjacent minimums produce answer |
| `7 / 4 1 5 6 7 1 8` | `4` | Correct index difference computation |

## Edge Cases

### All elements are equal

Input:

```
4
1 1 1 1
```

The minimum value is `1`, appearing at indices `0, 1, 2, 3`.

The algorithm computes distances:

```
1 - 0 = 1
2 - 1 = 1
3 - 2 = 1
```

The minimum of these values is `1`, which is the correct answer. Looking only at the first and last occurrence would incorrectly produce `3`.

### Minimum values with uneven spacing

Input:

```
5
2 8 2 3 2
```

The minimum value is `2`, appearing at indices `0, 2, 4`.

The algorithm computes:

```
2 - 0 = 2
4 - 2 = 2
```

The answer becomes `2`.

This demonstrates why checking consecutive occurrences is sufficient. The non-consecutive pair `(0, 4)` has distance `4`, which is larger and cannot be optimal.

### Smallest valid input

Input:

```
2
3 3
```

The minimum value appears at indices `0` and `1`.

The first occurrence sets `last = 0`. The second occurrence produces:

```
1 - 0 = 1
```

The algorithm outputs `1`, which is the only possible distance in a two-element array. This case confirms that initialization and boundary handling are correct.
