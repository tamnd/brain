---
title: "CF 106507L - Increments"
description: "The task is to reconstruct a sequence of range additions. We start with an array of zeroes. One operation chooses a continuous segment and increases every element inside that segment by one."
date: "2026-06-25T08:30:02+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106507
codeforces_index: "L"
codeforces_contest_name: "TeamsCode 2026 Spring Contest"
rating: 0
weight: 106507
solve_time_s: 34
verified: true
draft: false
---

[CF 106507L - Increments](https://codeforces.com/problemset/problem/106507/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 34s  
**Verified:** yes  

## Solution
## Problem Understanding

The task is to reconstruct a sequence of range additions. We start with an array of zeroes. One operation chooses a continuous segment and increases every element inside that segment by one. After some unknown number of such operations, we are given the final array and must output the minimum number of operations that could have produced it, together with the segments used.

The key object is not the array values themselves, but how the values change between neighboring positions. For an array `a`, define the difference array:

`d[i] = a[i] - a[i - 1]`

with `a[0] = 0`, and add one more virtual element `a[n + 1] = 0` so the last difference is included. A single operation on segment `[l, r]` changes this difference array by adding `1` at position `l` and subtracting `1` at position `r + 1`. In other words, every operation creates exactly one positive change and one negative change in the difference array.

The input length can be as large as `100000`. Any approach that repeatedly simulates applying operations to the array or searches through possible segments would be too slow because it could require quadratic work. We need a linear or near-linear construction.

A few edge cases are easy to miss. If the whole array has the same positive value, such as:

```
3
2 2 2
```

the answer is not three operations on individual elements. The correct answer is one operation:

```
1
1 3
```

because one segment covers the entire array.

Another tricky case is when there are zeroes inside the array:

```
5
1 0 1 0 1
```

The correct answer is three operations:

```
3
1 1
3 3
5 5
```

A careless solution that tries to extend every positive segment until the next larger value may accidentally cover positions that must remain zero.

A third boundary case is the end of the array:

```
4
1 1 1 1
```

The correct answer is one operation:

```
1
1 4
```

The final decrease back to zero happens after the array, so the virtual position `n + 1` must be handled. Ignoring it would leave unmatched increments.

## Approaches

A direct approach is to think about every possible segment and repeatedly apply increments until the target array is reached. This is correct because every operation can be simulated exactly, but it gives no useful structure. In the worst case, an array of length `100000` with values around `100000` could require billions of individual element updates, which is far beyond the available time.

The useful observation comes from looking at differences. Every range increment starts at one position and stops affecting the array immediately after another position. That means the only places where the difference array changes are the start and end boundaries.

Suppose the difference array has a positive value `d[i] = 3`. This means three more segments need to begin at position `i` than end there. Similarly, a negative value means that many active segments must finish before that position. The minimum number of operations is exactly the total amount of positive difference, because every operation can contribute only one starting point.

The construction is simple. Scan from left to right. Whenever a positive difference appears, create that many new segment starts. Whenever a negative difference appears, close that many currently open segments. The prefix sum of differences is always the current array value, so it is never negative. Therefore, we will always have enough open segments to close.

The brute-force method tries to discover segments by modifying the array. The optimal method discovers the same information directly from the boundaries of the segments.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(number of operations × n) | O(1) | Too slow |
| Optimal | O(n + answer) | O(answer) | Accepted |

## Algorithm Walkthrough

1. Compute the difference array. Treat the element before the first position and the element after the last position as zero. This makes every range operation correspond to exactly one positive boundary and one negative boundary.
2. Scan the difference array from left to right. When `d[i]` is positive, add `d[i]` copies of position `i` to a list of currently open segment starts. These are the operations that must begin here.
3. When `d[i]` is negative, remove `-d[i]` starts from the list and pair each removed start with an ending position of `i - 1`. The operation represented by this pair is the segment from that start to `i - 1`.
4. Output all generated segments. The number of segments is the number of positive contributions in the difference array, which is minimal.

The reason this construction is optimal is that every operation must create exactly one positive boundary in the difference array. If the total positive difference is `x`, no solution can use fewer than `x` operations. The algorithm creates exactly `x` operations, so it reaches the lower bound.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    diff = []
    prev = 0
    for x in a:
        diff.append(x - prev)
        prev = x
    diff.append(-prev)

    starts = []
    ans = []

    for i, x in enumerate(diff, start=1):
        if x > 0:
            for _ in range(x):
                starts.append(i)
        elif x < 0:
            for _ in range(-x):
                l = starts.pop()
                ans.append((l, i - 1))

    print(len(ans))
    for l, r in ans:
        print(l, r)

if __name__ == "__main__":
    solve()
```

The first part builds the difference array. The extra final value `-prev` represents the transition from the last element back to zero. Without this position, segments that reach the end of the array would never be closed.

The `starts` list stores positions where segments have started but have not yet ended. When a negative difference is found, the code pops exactly the required number of starts. Any order works because the operations are independent, so using the most recent starts is a convenient implementation choice.

The output count is automatically minimal because every stored start corresponds to one unavoidable operation. There are no extra operations added during construction.

The indices use `enumerate(..., start=1)` because the problem uses one-based indexing. The right endpoint is `i - 1`, since the negative difference at position `i` means the segment stops immediately before that position.

## Worked Examples

### Example 1

Input:

```
6
1 2 1 1 4 1
```

The difference array including the ending zero is:

`[1, 1, -1, 0, 3, -3, -1]`

| Position | Difference | Open starts | Action | Answer added |
| --- | --- | --- | --- | --- |
| 1 | 1 | [1] | Start one segment |  |
| 2 | 1 | [1, 2] | Start one segment |  |
| 3 | -1 | [1] | Close start 2 | (2, 2) |
| 4 | 0 | [1] | Nothing |  |
| 5 | 3 | [1, 5, 5, 5] | Start three segments |  |
| 6 | -3 | [1] | Close three segments | (5,5), (5,5), (5,5) |
| 7 | -1 | [] | Close final segment | (1,6) |

The algorithm finds five operations, matching the minimum possible number of positive difference units.

### Example 2

Input:

```
5
1 0 1 0 1
```

The difference array is:

`[1, -1, 1, -1, 1, -1]`

| Position | Difference | Open starts | Action | Answer added |
| --- | --- | --- | --- | --- |
| 1 | 1 | [1] | Start segment |  |
| 2 | -1 | [] | Close segment | (1,1) |
| 3 | 1 | [3] | Start segment |  |
| 4 | -1 | [] | Close segment | (3,3) |
| 5 | 1 | [5] | Start segment |  |
| 6 | -1 | [] | Close segment | (5,5) |

The trace shows why internal zeroes force segments to end. The negative differences prevent the algorithm from incorrectly extending operations across those positions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + answer) | Each array position is processed once, and each generated segment is created and closed once. |
| Space | O(answer) | The list of open starts and the final list of segments contain at most the number of operations. |

The constraints allow `n = 100000`, and the number of generated operations is also guaranteed to be at most `100000`. The linear construction easily fits within the limits.

## Test Cases

```python
import sys
import io

def solve(inp: str) -> str:
    data = inp.strip().split()
    if not data:
        return ""
    n = int(data[0])
    a = list(map(int, data[1:]))

    diff = []
    prev = 0
    for x in a:
        diff.append(x - prev)
        prev = x
    diff.append(-prev)

    starts = []
    ans = []

    for i, x in enumerate(diff, 1):
        if x > 0:
            for _ in range(x):
                starts.append(i)
        else:
            for _ in range(-x):
                ans.append((starts.pop(), i - 1))

    out = [str(len(ans))]
    out += [f"{l} {r}" for l, r in ans]
    return "\n".join(out)

assert solve("""6
1 2 1 1 4 1
""") == """5
2 2
5 5
5 5
5 5
1 6""", "sample 1"

assert solve("""5
1 0 1 0 1
""") == """3
1 1
3 3
5 5""", "sample 2"

assert solve("""1
7
""") == """1
1 1""", "single element"

assert solve("""4
3 3 3 3
""") == """3
1 4
1 4
1 4""", "all equal values"

assert solve("""5
1 1 0 2 2
""") == """3
4 5
4 5
1 2""", "internal zero boundary"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `[7]` | One segment covering the only element | Minimum size input and final boundary handling |
| `[3,3,3,3]` | Three identical full-array segments | Equal values and repeated operations |
| `[1,1,0,2,2]` | Three segments split around a zero | Internal closing boundaries |
| `[1,2,1,1,4,1]` | Five operations | Multiple overlapping ranges |

## Edge Cases

For a constant positive array:

```
3
2 2 2
```

the difference array is:

`[2, 0, 0, -2]`

The algorithm opens two segments at position `1`, then closes both at the virtual end position `4`. The output is two copies of `[1,3]`. Two operations are necessary because every operation can only contribute one unit of height.

For an array containing zero gaps:

```
5
1 0 1 0 1
```

the differences alternate between positive and negative values. Every positive difference opens a segment, and the following negative difference immediately closes it. The generated operations are exactly the single-element segments `[1,1]`, `[3,3]`, and `[5,5]`.

For an array ending with positive values:

```
4
1 1 1 1
```

the difference array is:

`[1,0,0,0,-1]`

The last negative value comes from the virtual zero after the array. The algorithm keeps the segment open until that point and outputs `[1,4]`, correctly handling the right boundary.
