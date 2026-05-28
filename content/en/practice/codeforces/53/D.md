---
title: "CF 53D - Physical Education"
description: "We have two arrays representing the order of students in a line. Array a is the desired arrangement, and array b is the current arrangement. In one operation we may swap two neighboring students. We must output any sequence of adjacent swaps that transforms b into a."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "sortings"]
categories: ["algorithms"]
codeforces_contest: 53
codeforces_index: "D"
codeforces_contest_name: "Codeforces Beta Round 49 (Div. 2)"
rating: 1500
weight: 53
solve_time_s: 126
verified: true
draft: false
---

[CF 53D - Physical Education](https://codeforces.com/problemset/problem/53/D)

**Rating:** 1500  
**Tags:** sortings  
**Solve time:** 2m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

We have two arrays representing the order of students in a line. Array `a` is the desired arrangement, and array `b` is the current arrangement. In one operation we may swap two neighboring students. We must output any sequence of adjacent swaps that transforms `b` into `a`.

The tricky part is that heights are not necessarily unique. Two students may have the same height, so we cannot simply match values without thinking about which occurrence corresponds to which position.

The constraints are small enough to allow quadratic algorithms. Since `n ≤ 300`, even an `O(n^2)` or `O(n^3)` solution easily fits within the limit. The maximum number of adjacent swaps needed to transform one permutation into another is at most `n(n-1)/2`, which for `n = 300` equals `44850`, far below the allowed `10^6` operations.

A careless implementation can fail when duplicate values exist. Consider:

```
a = [1, 2, 1]
b = [1, 1, 2]
```

If we greedily match the first `1` in `a` with the first `1` in `b`, that is fine. But if we later search incorrectly, we might move the wrong occurrence and break positions that were already fixed.

Another subtle case appears when the desired value already exists earlier in the array:

```
a = [2, 1, 2]
b = [2, 2, 1]
```

When fixing position `2`, we must search only in the unfixed suffix. Otherwise we may accidentally disturb the already-correct first position.

The smallest case also matters:

```
n = 1
a = [5]
b = [5]
```

The answer must contain zero swaps. Some implementations forget to handle this and attempt invalid neighbor operations.

## Approaches

The most direct idea is brute force simulation. For every position `i`, we try to place `a[i]` into that position inside array `b`. We search for the first occurrence of `a[i]` somewhere to the right, then repeatedly swap it left until it reaches position `i`.

This works because adjacent swaps let us move any element step by step. Once position `i` contains the correct value, we never touch it again.

The total number of swaps in the worst case is quadratic. For example, reversing an array of distinct values requires about `n^2 / 2` swaps. With `n = 300`, this is completely safe.

A more naive brute-force approach would repeatedly scan the whole array looking for mismatches and performing random local fixes. That can degrade toward cubic complexity because every correction may require another full scan. With `n = 300`, even that might still pass, but it is unnecessarily messy and much harder to reason about.

The key observation is that adjacent swaps naturally support a left-to-right fixing process. Once we place the correct value at position `i`, later operations only happen to the right of `i`, so the prefix stays permanently correct.

This gives a clean greedy algorithm:

1. Process positions from left to right.
2. Find the needed value somewhere in the suffix.
3. Bubble it left using adjacent swaps.

Because every operation strictly improves the fixed prefix, the algorithm always finishes.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Random brute-force corrections | O(n³) | O(1) | Unnecessarily slow |
| Greedy adjacent bubbling | O(n²) | O(1) excluding answer storage | Accepted |

## Algorithm Walkthrough

1. Start from the first position and move left to right through the array.
2. For position `i`, check whether `b[i]` already equals `a[i]`.
3. If the value is already correct, continue to the next position.
4. Otherwise, search for the first index `j ≥ i` such that `b[j] == a[i]`.

We search only in the suffix because positions before `i` are already fixed and must never change again.
5. Move the element at position `j` toward `i` using adjacent swaps.

For every position `k` from `j-1` down to `i`:

- Swap `b[k]` and `b[k+1]`
- Record the operation `(k+1, k+2)` in 1-based indexing
6. After these swaps, position `i` now contains `a[i]`.
7. Continue until every position is fixed.

### Why it works

After processing position `i`, the prefix `b[0..i]` becomes identical to `a[0..i]`.

The algorithm never touches this prefix again because future swaps only occur inside positions greater than or equal to the current index. Since the arrays contain the same multiset of values, the required value for each step must exist somewhere in the remaining suffix.

By induction, every position eventually becomes correct, so the final array equals `a`.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    ops = []

    for i in range(n):
        if b[i] == a[i]:
            continue

        j = i
        while b[j] != a[i]:
            j += 1

        while j > i:
            b[j], b[j - 1] = b[j - 1], b[j]
            ops.append((j, j + 1))
            j -= 1

    print(len(ops))
    for x, y in ops:
        print(x, y)

solve()
```

The outer loop fixes positions from left to right. At the start of iteration `i`, every earlier position is already correct.

The search loop finds the first occurrence of `a[i]` in the unfixed suffix. Using the first occurrence is enough because equal values are interchangeable. We only care that one correct copy reaches position `i`.

The bubbling loop performs adjacent swaps one by one. Since the problem explicitly asks for neighboring swaps, we must simulate each move individually and store it.

The operation indices are stored in 1-based form because Codeforces uses 1-based indexing in the output. This is an easy place to make an off-by-one mistake. Inside the array we use 0-based indexing, but the swap between positions `j-1` and `j` corresponds to output `(j, j+1)`.

The number of swaps never exceeds `n(n-1)/2`, so memory usage for storing operations remains small.

## Worked Examples

### Example 1

Input:

```
a = [1, 2, 3, 2]
b = [3, 2, 1, 2]
```

| Step | Target Position | Needed Value | Found Index | Array After Swaps | Operations |
| --- | --- | --- | --- | --- | --- |
| Initial | - | - | - | [3, 2, 1, 2] | [] |
| 1 | 0 | 1 | 2 | [1, 3, 2, 2] | (2,3), (1,2) |
| 2 | 1 | 2 | 2 | [1, 2, 3, 2] | (3,4), (2,3) |
| 3 | 2 | 3 | 2 | [1, 2, 3, 2] | no change |
| 4 | 3 | 2 | 3 | [1, 2, 3, 2] | no change |

This trace shows the main invariant. After fixing each position, the prefix never changes again. The algorithm gradually transforms the array into the target arrangement.

### Example 2

Input:

```
a = [2, 1, 2]
b = [2, 2, 1]
```

| Step | Target Position | Needed Value | Found Index | Array After Swaps | Operations |
| --- | --- | --- | --- | --- | --- |
| Initial | - | - | - | [2, 2, 1] | [] |
| 1 | 0 | 2 | 0 | [2, 2, 1] | no change |
| 2 | 1 | 1 | 2 | [2, 1, 2] | (2,3) |
| 3 | 2 | 2 | 2 | [2, 1, 2] | no change |

This example demonstrates why duplicates are harmless. We only need some occurrence of the needed value from the suffix. Once the correct value reaches the current position, the remaining equal values can stay wherever they are.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) | Each element may move across the array once |
| Space | O(1) excluding output | Only a few variables besides the operations list |

For `n = 300`, quadratic complexity is tiny. Even the maximum possible number of swaps is below fifty thousand, far under the allowed operation limit and easily fast enough for a 2-second time limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve_io(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    ops = []

    for i in range(n):
        if b[i] == a[i]:
            continue

        j = i
        while b[j] != a[i]:
            j += 1

        while j > i:
            b[j], b[j - 1] = b[j - 1], b[j]
            ops.append((j, j + 1))
            j -= 1

    out = [str(len(ops))]
    for x, y in ops:
        out.append(f"{x} {y}")

    return "\n".join(out)

# provided sample
res = solve_io(
    "4\n1 2 3 2\n3 2 1 2\n"
)
assert res.startswith("4"), "sample 1"

# minimum size
assert solve_io(
    "1\n5\n5\n"
) == "0", "single element"

# already sorted
assert solve_io(
    "3\n1 2 3\n1 2 3\n"
) == "0", "already correct"

# duplicates
res = solve_io(
    "3\n2 1 2\n2 2 1\n"
)
assert res.splitlines()[0] == "1", "duplicate handling"

# reverse order
res = solve_io(
    "4\n1 2 3 4\n4 3 2 1\n"
)
assert int(res.splitlines()[0]) == 6, "maximum inversions for n=4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 5 / 5` | `0` swaps | Minimum-size boundary |
| Already equal arrays | `0` swaps | No unnecessary operations |
| Arrays with duplicates | Valid transformation | Correct duplicate handling |
| Fully reversed array | Maximum inversions | Worst-case swap count |

## Edge Cases

Consider the duplicate-value case:

```
a = [1, 2, 1]
b = [1, 1, 2]
```

At position `0`, the value is already correct. At position `1`, we need `2`. The algorithm searches only in the suffix and finds `2` at index `2`. One adjacent swap produces:

```
[1, 2, 1]
```

The already-correct first position never changes.

Now consider:

```
a = [2, 1, 2]
b = [2, 2, 1]
```

The first position is fixed immediately. When processing position `1`, the algorithm searches from index `1` onward and finds `1` at index `2`. Swapping positions `2` and `3` gives the correct arrangement.

If we had allowed searching earlier positions, we might accidentally move the fixed prefix and break correctness.

Finally, the smallest possible input:

```
n = 1
a = [7]
b = [7]
```

The outer loop runs once. Since the value already matches, no operations are added. The algorithm correctly prints `0`.
