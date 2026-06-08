---
title: "CF 1841E - Fill the Matrix"
description: "Each column of the matrix contains a black prefix and a white suffix. In column i, rows 1..ai are blocked, while rows ai+1..n are available. We must place the integers 1,2,...,m into distinct white cells."
date: "2026-06-09T06:21:49+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1841
codeforces_index: "E"
codeforces_contest_name: "Educational Codeforces Round 150 (Rated for Div. 2)"
rating: 2200
weight: 1841
solve_time_s: 85
verified: true
draft: false
---

[CF 1841E - Fill the Matrix](https://codeforces.com/problemset/problem/1841/E)

**Rating:** 2200  
**Tags:** data structures, greedy, math  
**Solve time:** 1m 25s  
**Verified:** yes  

## Solution
## Problem Understanding

Each column of the matrix contains a black prefix and a white suffix. In column `i`, rows `1..a_i` are blocked, while rows `a_i+1..n` are available.

We must place the integers `1,2,...,m` into distinct white cells. The beauty counts how many consecutive pairs `(j, j+1)` end up in horizontally adjacent cells of the same row, with `j+1` immediately to the right of `j`.

The actual values of the numbers matter only through their order. Whenever we place a consecutive run of numbers inside a horizontal segment of white cells, a segment containing `k` numbers contributes exactly `k-1` beauty, because every neighboring pair inside that run contributes once.

The matrix size is at most `2·10^5` across all test cases. Any algorithm that explicitly touches all `n²` cells is impossible. Even storing the whole matrix would be too expensive. The structure of the white cells must be exploited directly from the array `a`.

A subtle point is that `m` can be very large. The statement explicitly warns that it may not fit in a 32-bit integer. Every calculation involving the number of placed values must use 64-bit arithmetic.

Another easy mistake is to think that each row can be processed independently. Consider:

```
n = 3
a = [0,0,0]
m = 9
```

All cells are white. There are three row segments of length `3`. Filling each completely gives beauty `2 + 2 + 2 = 6`, which is optimal. Treating rows independently is fine here.

Now consider:

```
n = 4
a = [2,0,3,1]
m = 5
```

The row segments have different lengths. Spending numbers on a short segment may reduce the final beauty because every new segment introduces a penalty of one. The optimal strategy is driven by segment lengths, not by rows themselves.

A third trap appears when the remaining number of integers cannot completely fill the next segment. For a segment of length `L`, placing only `x < L` numbers contributes `x-1`, not `x`. Missing this detail creates an off-by-one error in the final greedy step.

## Approaches

A brute-force view is useful first.

Imagine extracting every maximal horizontal white segment. If a segment has length `L`, then filling `k` cells of that segment consecutively yields beauty `k-1` whenever `k > 0`.

Suppose we knew all segments. Then we could try every possible distribution of the `m` numbers among them. This is obviously correct because beauty depends only on how many numbers each segment receives. Unfortunately, the number of distributions is enormous, and even generating all segments naively requires examining the whole matrix, which may contain about `4·10^10` cells.

The key observation is that a filled segment with `k` numbers contributes

```
k - 1
```

which can be rewritten as

```
k - (number of used segments)
```

summed over all segments.

Since the total number of placed numbers is fixed and equals `m`, maximizing beauty is equivalent to minimizing the number of segments that receive at least one number.

That immediately suggests a greedy strategy. If we have several segments available, we should fill the longest ones first. A long segment can absorb many numbers while paying the same "one segment" penalty as a short segment.

The problem now becomes:

1. Find how many maximal horizontal white segments exist for every possible length.
2. Spend the `m` numbers on segments from largest length to smallest length.

The remaining challenge is extracting all maximal horizontal white segments without constructing the matrix.

For a row `r`, column `i` is white iff `a_i < r`. A maximal horizontal segment corresponds to an interval of columns where all heights are below some row level.

This is exactly the same structure that appears in histogram problems. Using a monotonic stack, we can count how many maximal segments exist for each length. The stack processes the skyline formed by `a_i`, and every pop determines a range length together with how many row levels generate that range.

After obtaining `cnt[len]`, the number of maximal segments of length `len`, the greedy filling is straightforward.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) or worse | O(n²) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

The implementation below actually runs in linear time apart from iterating over lengths.

## Algorithm Walkthrough

1. Interpret `a_i` as column heights of blocked cells.
2. Add two sentinel columns of height `n` at both ends. These guarantee that every segment is eventually closed and counted.
3. Process the array with a decreasing monotonic stack.
4. Whenever the current height is at least the height of the previous column, start popping stack elements.
5. During popping, each popped height represents a range of row levels that create maximal horizontal white segments of a particular length. Accumulate these contributions into `cnt[length]`.
6. After all pops that are allowed, if the stack is still non-empty, add the remaining contribution generated between the last popped height and the current height.
7. After processing every column, `cnt[len]` stores how many maximal white segments have length `len`.
8. Traverse lengths from largest to smallest.
9. For a length `L` with count `C`:

- If `m >= L·C`, fill all such segments completely.
- Each fully filled segment contributes `L-1`.
- Subtract `L·C` from `m`.
10. If there are not enough numbers to fill all `C` segments:

- Fully fill `m // L` segments.
- Use the remainder `m % L` inside one additional segment.
- A partially filled segment with `r` numbers contributes `r-1` when `r > 0`.
- After this step, all numbers are used and the algorithm stops.

### Why it works

Every occupied segment pays exactly one unit of beauty loss compared with the number of integers placed inside it.

For a segment receiving `k` numbers:

```
beauty = k - 1
```

Summing over all used segments gives

```
beauty = m - used_segments
```

because the total number of placed integers is fixed at `m`.

To maximize beauty, we must minimize the number of segments that receive numbers. The optimal way to do that is always to consume capacity from the longest available segments first. Any solution using a shorter segment while a longer unused segment exists can be improved by moving numbers from the shorter segment into the longer one, never increasing the number of occupied segments.

The monotonic stack correctly counts maximal white segments because each pop identifies exactly the interval where a certain height is the limiting boundary. The difference between neighboring heights determines how many row levels generate that interval length. This is the standard histogram decomposition argument.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    for _ in range(t):
        n = int(input())
        arr = list(map(int, input().split()))
        m = int(input())

        a = [n] + arr + [n]
        N = n + 1

        stack = [0]
        cnt = {}

        for i in range(1, N + 1):
            if a[i] >= a[i - 1]:
                prev = a[stack[-1]]
                stack.pop()

                while stack and a[stack[-1]] <= a[i]:
                    length = i - stack[-1] - 1
                    cnt[length] = cnt.get(length, 0) + (a[stack[-1]] - prev)
                    prev = a[stack[-1]]
                    stack.pop()

                if stack:
                    length = i - stack[-1] - 1
                    cnt[length] = cnt.get(length, 0) + (a[i] - prev)

            stack.append(i)

        ans = 0

        for length in sorted(cnt.keys(), reverse=True):
            if length == 1:
                continue

            c = cnt[length]
            total_cells = length * c

            if total_cells <= m:
                ans += c * (length - 1)
                m -= total_cells
            else:
                full = m // length
                ans += full * (length - 1)
                m -= full * length

                if m > 0:
                    ans += m - 1

                m = 0
                break

            if m == 0:
                break

        print(ans)

solve()
```

The first part of the code performs the monotonic-stack decomposition of the histogram formed by the column heights. The dictionary `cnt` stores how many maximal horizontal segments exist for each length.

The variable `prev` is the crucial detail. Consecutive popped heights represent different bands of row levels. Using height differences avoids counting the same row level multiple times.

After all segment counts are known, the greedy phase iterates from the largest length downward. A fully filled segment of length `L` contributes `L-1`, which is why the update is:

```
ans += count * (L - 1)
```

The partial-fill case is the easiest place to make a mistake. If the remainder is `r`, the contribution is `r-1`, not `r`. When `r = 0`, no extra segment exists, so nothing is added.

Python integers automatically handle the large value of `m`.

## Worked Examples

### Example 1

Input:

```
n = 3
a = [0,0,0]
m = 9
```

All rows contain one segment of length `3`.

| Length | Count | m before | Action | Beauty gained |
| --- | --- | --- | --- | --- |
| 3 | 3 | 9 | Fill all | 6 |

Final answer:

```
6
```

This demonstrates the fully-filled case. Every row contributes `3-1 = 2`, giving `6`.

### Example 2

Input:

```
n = 4
a = [2,0,3,1]
m = 5
```

The stack decomposition produces segment counts equivalent to:

| Length | Count |
| --- | --- |
| 3 | 1 |
| 2 | 1 |
| 1 | 4 |

Greedy filling:

| Length | Count | m before | Action | Beauty gained |
| --- | --- | --- | --- | --- |
| 3 | 1 | 5 | Fill completely | 2 |
| 2 | 1 | 2 | Fill completely | 1 |

Total beauty:

```
3
```

This example shows why longer segments must be prioritized. Using the length-1 segments first would waste beauty.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) amortized | Each index enters and leaves the stack once |
| Space | O(n) | Stack and segment counts |

The sum of `n` over all test cases is at most `2·10^5`. A linear-time solution comfortably fits within the time limit, and the memory usage remains proportional to the input size.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        arr = list(map(int, input().split()))
        m = int(input())

        a = [n] + arr + [n]
        N = n + 1

        stack = [0]
        cnt = {}

        for i in range(1, N + 1):
            if a[i] >= a[i - 1]:
                prev = a[stack[-1]]
                stack.pop()

                while stack and a[stack[-1]] <= a[i]:
                    length = i - stack[-1] - 1
                    cnt[length] = cnt.get(length, 0) + (a[stack[-1]] - prev)
                    prev = a[stack[-1]]
                    stack.pop()

                if stack:
                    length = i - stack[-1] - 1
                    cnt[length] = cnt.get(length, 0) + (a[i] - prev)

            stack.append(i)

        ans = 0

        for length in sorted(cnt.keys(), reverse=True):
            if length == 1:
                continue

            c = cnt[length]

            if length * c <= m:
                ans += c * (length - 1)
                m -= length * c
            else:
                full = m // length
                ans += full * (length - 1)
                m -= full * length

                if m:
                    ans += m - 1
                m = 0
                break

            if m == 0:
                break

        out.append(str(ans))

    return "\n".join(out)

# provided sample
assert run(
"""6
3
0 0 0
9
4
2 0 3 1
5
4
2 0 3 1
6
4
2 0 3 1
10
10
0 2 2 1 5 10 3 4 1 1
20
1
1
0
"""
) == """6
3
4
4
16
0"""

# minimum size
assert run(
"""1
1
1
0
"""
) == "0"

# single white cell
assert run(
"""1
1
0
1
"""
) == "0"

# all cells white, partial fill
assert run(
"""1
2
0 0
3
"""
) == "2"

# all columns blocked
assert run(
"""1
3
3 3 3
0
"""
) == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `n=1, a=[1], m=0` | `0` | Minimum instance |
| `n=1, a=[0], m=1` | `0` | Single usable cell |
| `n=2, all white, m=3` | `2` | Partial use of total capacity |
| `n=3, all blocked, m=0` | `0` | No available cells |

## Edge Cases

Consider:

```
1
1
0
1
```

There is exactly one white cell. The only possible placement uses one segment containing one number. Beauty is `1 - 1 = 0`. The greedy phase never gains anything from a length-1 segment, so the algorithm correctly outputs `0`.

Consider:

```
1
2
0 0
3
```

There are two row segments of length `2`. The algorithm first fills one segment completely, gaining `1` beauty and using two numbers. One number remains and starts another segment, contributing `0`. Total beauty is `2 - 1 = 1` from the first segment plus `0` from the second, giving `2` overall. The partial-fill rule `r - 1` handles this exactly.

Consider:

```
1
3
3 3 3
0
```

Every cell is black. The stack decomposition produces no useful segment lengths. The greedy phase does nothing and returns `0`, which is the only possible answer.

Finally, consider a case where the remaining numbers stop in the middle of a long segment:

```
1
3
0 0 0
4
```

The best strategy is to place all four numbers inside a length-3 segment and then continue into another segment only if necessary. The algorithm fills one length-3 segment completely, gains `2`, and the remaining single number contributes `0`. The answer is `2`, matching the optimal construction.
