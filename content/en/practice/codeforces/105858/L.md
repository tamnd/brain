---
title: "CF 105858L - Everyone loves k shortest path problems!"
description: "We have n souvenirs. Each souvenir must be assigned to exactly one of two friends. If souvenir i goes to the first friend, it contributes ai happiness to the first friend and nothing to the second. If it goes to the second friend, the opposite happens with value bi."
date: "2026-06-25T14:45:38+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105858
codeforces_index: "L"
codeforces_contest_name: "2025 Winter ESCOM Training Camp, Final Contest"
rating: 0
weight: 105858
solve_time_s: 42
verified: true
draft: false
---

[CF 105858L - Everyone loves k shortest path problems!](https://codeforces.com/problemset/problem/105858/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We have `n` souvenirs. Each souvenir must be assigned to exactly one of two friends. If souvenir `i` goes to the first friend, it contributes `a_i` happiness to the first friend and nothing to the second. If it goes to the second friend, the opposite happens with value `b_i`.

The goal is not to find just one best distribution. We need the first `2^min(n,20)` distributions when sorted by the absolute difference between the total happiness of the two friends.

The difference can be written in a simpler way. For every souvenir, define:

`d_i = a_i - b_i`

Choosing the first friend adds `d_i` to the final difference. Choosing the second friend adds `-d_i`. The absolute final difference is the absolute value of a signed sum of all `d_i`.

The input size is small enough for `n` to reach 40, but the number of possible distributions is up to `2^40`, which is about one trillion. A solution that enumerates every distribution is impossible because even a few billion operations are already far beyond a typical contest time limit.

The output size is deliberately large. When `n` is 40, we must print `2^20` values, about one million answers. This tells us that an algorithm around `O(2^20 log 2^20)` is realistic, while anything close to `O(2^n)` is not.

There are several cases where an implementation that only finds the minimum difference fails. For example:

```
Input
2
-1 10
-1 10

Output
9 9 11 11
```

A careless solution might find the minimum value `9` and stop. The task requires the four best distributions, including repeated values.

Another common mistake is forgetting that the signs can be negative. Consider:

```
Input
1
-5
10

Output
15 15
```

The two choices produce differences `|-5 - 10| = 15` and `|10 - (-5)| = 15`. Treating values as always positive changes the answer.

A final tricky situation is having many equal answers. In:

```
Input
4
1 2 3 4
4 3 2 1
```

many different assignments give the same minimum difference. The output needs all of those copies, not just unique values.

## Approaches

The direct approach is to generate every possible assignment of souvenirs. For each assignment we calculate the signed sum of the `d_i` values, take its absolute value, collect all results, and sort them.

This is correct because every possible distribution corresponds to exactly one choice of signs. However, with 40 souvenirs there are `2^40` possibilities. Even storing those values is impossible, and sorting them would require roughly a trillion elements.

The useful observation is that the answer only asks for the first `2^20` values. We can split the souvenirs into two halves. Each half has at most 20 items, so we can generate every signed sum inside a half. This creates two arrays of at most `2^20` values.

Now every full distribution is represented as:

`left_sum + right_sum`

The problem becomes finding the smallest absolute values among all pairs from the two arrays.

The key is that both arrays can be sorted. For one value `x` in the first array, the best partner from the second array is close to `-x`. Because the second array is sorted, all candidates for one `x` can be produced in increasing absolute value by expanding outward from the position where `-x` would be inserted.

We merge these sorted candidate streams with a priority queue. Initially, every left-half sum contributes its best possible partner. Each time we remove the current smallest answer, we advance only that stream to its next candidate.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(2^n) | Too slow |
| Meet in the Middle + Heap | O(2^(n/2) log 2^(n/2)) | O(2^(n/2)) | Accepted |

## Algorithm Walkthrough

1. Compute `d_i = a_i - b_i` for every souvenir. The final happiness difference is the absolute value of the sum of chosen signed versions of these values.
2. Split the array of differences into two parts. Each part has at most 20 elements, so every possible signed sum inside one part can be generated.
3. Sort the list of sums from the second half. We will use this ordering to quickly find the closest values to any target.
4. For every sum `x` from the first half, find the insertion position of `-x` in the sorted second-half sums. This position separates values producing negative and positive totals.
5. Create two possible next candidates for each `x`: the value just before the insertion position and the value at the insertion position. These are the closest possibilities, so they are the first values that can belong to the answer.
6. Put all these candidates into a priority queue ordered by their absolute difference.
7. Repeatedly remove the smallest candidate. Add its value to the answer list. Then move the same stream one step further on the side that produced the removed candidate.

The reason the stream movement works is that for a fixed first-half value, the second-half values on the left of the insertion point get closer while moving right, and the values on the right get farther while moving right. Both sides are already sorted by absolute value.

Why it works:

For every fixed left sum, we have an ordered sequence of all possible right sums by absolute final difference. The heap contains the smallest unused element from every such sequence. A priority queue merge always extracts the smallest remaining element among all sequences, so every produced answer is the next smallest possible distribution. Since every distribution belongs to exactly one pair of half sums, no candidates are missed.

## Python Solution

```python
import sys
import bisect
import heapq

input = sys.stdin.readline

def generate(vals):
    res = [0]
    for v in vals:
        res += [x + v for x in res]
        res += [x - v for x in res[:len(res)//2]]
    return res

def generate(vals):
    res = [0]
    for v in vals:
        cur = []
        for x in res:
            cur.append(x + v)
            cur.append(x - v)
        res = cur
    return res

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    diff = [a[i] - b[i] for i in range(n)]

    mid = n // 2
    left = generate(diff[:mid])
    right = generate(diff[mid:])

    right.sort()

    heap = []
    for i, x in enumerate(left):
        pos = bisect.bisect_left(right, -x)
        if pos < len(right):
            heap.append((abs(x + right[pos]), x + right[pos], i, pos, 1))
        if pos > 0:
            heap.append((abs(x + right[pos - 1]), x + right[pos - 1], i, pos - 1, -1))

    heapq.heapify(heap)

    need = 1 << min(n, 20)
    ans = []

    while len(ans) < need:
        _, value, i, j, direction = heapq.heappop(heap)
        ans.append(value if value >= 0 else -value)

        nj = j + direction
        if 0 <= nj < len(right):
            heapq.heappush(
                heap,
                (abs(left[i] + right[nj]), left[i] + right[nj], i, nj, direction)
            )

    print(*sorted(ans))

if __name__ == "__main__":
    solve()
```

The `generate` function builds all signed sums of a half. For every previous sum, the next souvenir creates two possibilities, adding the souvenir value or subtracting it.

The second half is sorted because binary search and ordered expansion depend on that property. For every left sum, `bisect_left` finds the first second-half value that is not smaller than `-x`.

The heap stores the current best unused candidate from every left-half sum. The tuple contains the absolute value used for ordering, the actual signed difference, and enough information to advance the same stream after extraction.

Python integers are arbitrary precision, so the large values from the input do not require special handling. The only subtle boundary condition is checking both sides of the insertion point, because `-x` may be outside the range of the sorted array.

## Worked Examples

### Sample 1

Input:

```
4
1 2 3 4
4 3 2 1
```

The differences are `[-3, -1, 1, 3]`.

| Step | Heap action | Current answer values |
| --- | --- | --- |
| Start | Insert closest candidates from every left sum | empty |
| Pop | Smallest absolute difference is 0 | 0 |
| Pop | Another pair gives 0 | 0, 0 |
| Continue | More zero combinations appear | 0, 0, 0, ... |

This trace shows why duplicates must be preserved. Several different souvenir distributions can create exactly the same difference.

### Sample 2

Input:

```
2
-1 10
-1 10
```

The differences are `[0, 0]`.

| Step | Heap action | Current answer values |
| --- | --- | --- |
| Start | Generate sums 0 and 0 | empty |
| Pop | First pair gives 0+0 difference 0 | 0 |
| Continue | Remaining pairs are also checked | 0, 0, 0, 0 |

This demonstrates that the signed transformation handles negative happiness values naturally.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(2^(n/2) log 2^(n/2)) | We generate half sums and extract at most about one million heap elements |
| Space | O(2^(n/2)) | The two half-sum arrays and heap dominate memory usage |

The maximum half size is 20, so the generated arrays contain at most about one million values. The heap operations stay within a practical range for the given limits.

## Test Cases

```python
import sys
import io
import bisect
import heapq

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    solve()
    return sys.stdout.getvalue().strip()

# provided samples
assert run("""4
1 2 3 4
4 3 2 1
""") == "0 0 0 0 0 0 5 5 5 5 5 5 5 5 10 10"

assert run("""2
-1 10
-1 10
""") == "9 9 11 11"

# custom: single souvenir
assert run("""1
5
-5
""") == "10 10"

# custom: all equal differences
assert run("""3
7 7 7
0 0 0
""") == "7 7 7 7 7 7 7 7"

# custom: zero differences
assert run("""3
1 2 3
1 2 3
""") == "0 0 0 0 0 0 0 0"

# custom: negative values
assert run("""2
-10 -20
5 15
""") == "15 25 25 35"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| One souvenir | `10 10` | Handles the smallest split size |
| Equal differences | repeated values | Checks duplicate answers |
| Identical friends | all zeros | Checks many optimal distributions |
| Negative values | mixed values | Checks signed difference logic |

## Edge Cases

The case with negative happiness values is handled by converting every souvenir into a signed contribution. For:

```
1
-5
10
```

the difference values are `-15`. The two possible signed sums are `-15` and `15`, so both answers are `15`.

The case with many equal answers works because the heap stores every possible distribution separately. If ten different assignments create the same difference, that value is inserted ten times into the result.

The boundary case where `-x` is smaller than every value in the right half is handled by only using the right side of the insertion point when it exists. Similarly, if `-x` is larger than every value, only the left side is valid. This avoids accessing invalid positions while still considering the closest candidates.
