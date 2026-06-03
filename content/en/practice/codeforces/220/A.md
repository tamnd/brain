---
title: "CF 220A - Little Elephant and Problem"
description: "We are given an array that was originally sorted in non-decreasing order. At some point, either nothing happened or exactly one pair of elements may have been swapped."
date: "2026-06-04T01:54:05+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 220
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 136 (Div. 1)"
rating: 1300
weight: 220
solve_time_s: 93
verified: true
draft: false
---

[CF 220A - Little Elephant and Problem](https://codeforces.com/problemset/problem/220/A)

**Rating:** 1300  
**Tags:** implementation, sortings  
**Solve time:** 1m 33s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array that was originally sorted in non-decreasing order. At some point, either nothing happened or exactly one pair of elements may have been swapped.

The question is whether the current array can be transformed into a fully sorted array using at most one swap of any two positions. If the answer is yes, we print `"YES"`. Otherwise we print `"NO"`.

The array length can be as large as $10^5$. Any algorithm that tries every possible swap would need roughly $n^2$ attempts. With $n = 10^5$, that means around $10^{10}$ possibilities, which is completely infeasible within a 2-second time limit. We need something close to $O(n \log n)$ or $O(n)$.

A subtle aspect of the problem is that values are not necessarily distinct. Duplicates make some intuitive approaches fail.

Consider:

```
4
1 3 2 2
```

The sorted array is:

```
1 2 2 3
```

The current array differs from the sorted one at positions 2 and 4 only, so a single swap fixes it. The correct answer is:

```
YES
```

A careless solution that only looks for inversions may incorrectly conclude that more work is needed.

Another important case is when the array is already sorted:

```
5
1 2 2 3 4
```

The answer is still:

```
YES
```

because zero swaps is allowed. The requirement is "at most one swap", not "exactly one swap".

A third edge case appears when more than two positions disagree with the sorted order:

```
4
4 3 2 1
```

The sorted version is:

```
1 2 3 4
```

All four positions differ. No single swap can fix all of them, so the answer is:

```
NO
```

A solution that only checks whether the number of inversions is small would fail here.

## Approaches

A straightforward brute-force method is to try every possible swap, including the possibility of performing no swap. For each choice, we check whether the resulting array is sorted.

There are $O(n^2)$ possible swaps. Checking whether an array is sorted takes $O(n)$ time. The total complexity becomes $O(n^3)$.

For $n = 10^5$, this is hopelessly slow. Even $O(n^2)$ would already be too large.

The key observation comes from comparing the current array with its fully sorted version.

Suppose we create a sorted copy of the array. Any position where the current array and the sorted array already match does not need to change. A single swap can affect only two positions. Consequently, if more than two positions differ from the sorted array, one swap can never make the arrays identical.

This turns the problem into a very simple check.

Construct the sorted version of the array. Count how many indices contain different values in the original and sorted arrays.

If the number of mismatched positions is:

- 0, the array is already sorted.
- 2, swapping those two positions fixes the array.
- More than 2, one swap is insufficient.

Because every swap changes exactly two positions, the answer is `"YES"` precisely when the mismatch count is at most 2.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^3)$ | $O(1)$ | Too slow |
| Optimal | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Read the array.
2. Create a sorted copy of the array.

The sorted copy represents the target configuration we want to reach.
3. Compare the original array and the sorted array position by position.

Count how many indices contain different values.
4. If the number of mismatches is at most 2, print `"YES"`.

A single swap affects exactly two positions. Zero mismatches means the array is already sorted, while two mismatches correspond to the two positions involved in the swap.
5. Otherwise, print `"NO"`.

### Why it works

Let the sorted copy be $b$.

If the original array can be sorted using at most one swap, then all positions except possibly the two swapped positions must already match $b$. Thus the number of mismatches between the original array and $b$ cannot exceed 2.

Conversely, if there are exactly two mismatched positions, exchanging the values at those positions makes both positions match the sorted array simultaneously. If there are zero mismatches, the array is already sorted.

Hence the array is sortable in at most one swap if and only if the mismatch count is at most 2.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    b = sorted(a)

    mismatches = 0
    for x, y in zip(a, b):
        if x != y:
            mismatches += 1

    print("YES" if mismatches <= 2 else "NO")

if __name__ == "__main__":
    solve()
```

The implementation follows the algorithm directly.

The sorted copy `b` is the target arrangement. We then scan both arrays simultaneously and count positions where the values differ.

The crucial observation is that we count mismatched positions rather than inversions. Duplicates can make inversion-based reasoning unreliable, while comparison against the sorted array captures exactly which positions are incorrect.

No special handling is needed for already sorted arrays. In that case the mismatch count is zero, and the condition `mismatches <= 2` naturally returns `"YES"`.

Python integers easily handle values up to $10^9$, so there are no overflow concerns.

## Worked Examples

### Example 1

Input:

```
2
1 2
```

Sorted copy:

```
1 2
```

| Position | Original | Sorted | Mismatch Count |
| --- | --- | --- | --- |
| 1 | 1 | 1 | 0 |
| 2 | 2 | 2 | 0 |

Final mismatch count is 0.

Output:

```
YES
```

This demonstrates the case where no swap is needed.

### Example 2

Input:

```
3
3 1 2
```

Sorted copy:

```
1 2 3
```

| Position | Original | Sorted | Mismatch Count |
| --- | --- | --- | --- |
| 1 | 3 | 1 | 1 |
| 2 | 1 | 2 | 2 |
| 3 | 2 | 3 | 3 |

Final mismatch count is 3.

Output:

```
NO
```

Three positions disagree with the sorted array. Since one swap can affect only two positions, sorting in a single swap is impossible.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Sorting dominates the running time |
| Space | $O(n)$ | The sorted copy of the array is stored |

With $n \le 10^5$, an $O(n \log n)$ solution runs comfortably within the limits. The additional array of size $n$ also fits easily within the memory limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    n = int(input())
    a = list(map(int, input().split()))

    b = sorted(a)
    mismatches = sum(x != y for x, y in zip(a, b))

    return ("YES" if mismatches <= 2 else "NO") + "\n"

# provided sample
assert run("2\n1 2\n") == "YES\n", "sample 1"

# one swap fixes array
assert run("3\n2 1 3\n") == "YES\n", "single swap"

# requires more than one swap
assert run("4\n4 3 2 1\n") == "NO\n", "multiple swaps needed"

# all equal values
assert run("5\n7 7 7 7 7\n") == "YES\n", "all equal"

# duplicates with one valid swap
assert run("4\n1 3 2 2\n") == "YES\n", "duplicates"

# minimum size, unsorted
assert run("2\n2 1\n") == "YES\n", "minimum size"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 / 2 1` | YES | Smallest non-trivial array |
| `4 / 4 3 2 1` | NO | More than two mismatches |
| `5 / 7 7 7 7 7` | YES | All values identical |
| `4 / 1 3 2 2` | YES | Duplicate values handled correctly |
| `3 / 2 1 3` | YES | Exactly one swap needed |

## Edge Cases

Consider an already sorted array:

```
5
1 2 2 3 4
```

The sorted copy is identical.

```
Original: 1 2 2 3 4
Sorted:   1 2 2 3 4
```

Mismatch count is 0, so the algorithm prints:

```
YES
```

This matches the requirement that zero swaps is allowed.

Consider duplicates:

```
4
1 3 2 2
```

The sorted copy is:

```
1 2 2 3
```

Comparing positions:

```
1 = 1
3 ≠ 2
2 = 2
2 ≠ 3
```

There are exactly two mismatches. Swapping those two positions yields the sorted array, so the algorithm outputs:

```
YES
```

Consider a case needing more than one swap:

```
4
4 3 2 1
```

Sorted copy:

```
1 2 3 4
```

Every position differs, giving four mismatches. Since one swap can repair at most two positions, the algorithm outputs:

```
NO
```

The mismatch-count criterion captures all such cases correctly.
