---
title: "CF 1637A - Sorting Parts"
description: "We have an array and we are forced to perform exactly one operation. We choose a position that splits the array into two non-empty parts. Then we sort the left part and the right part independently."
date: "2026-06-10T04:34:28+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1637
codeforces_index: "A"
codeforces_contest_name: "Codeforces Global Round 19"
rating: 800
weight: 1637
solve_time_s: 83
verified: true
draft: false
---

[CF 1637A - Sorting Parts](https://codeforces.com/problemset/problem/1637/A)

**Rating:** 800  
**Tags:** brute force, sortings  
**Solve time:** 1m 23s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an array and we are forced to perform exactly one operation. We choose a position that splits the array into two non-empty parts. Then we sort the left part and the right part independently. The question is whether there exists some split such that the final whole array is still not sorted.

For each test case, we must answer `"YES"` if at least one split produces an unsorted array, and `"NO"` if every possible split produces a globally sorted array.

The total number of elements over all test cases is only $10^4$, so even quadratic algorithms would fit comfortably inside the limits. That means performance is not really the challenge here. The difficulty lies in recognizing the structure hidden inside the operation.

One easy mistake is to think that sorting both pieces separately always produces a sorted array. Consider

```
3
2 2 1
```

Choosing the split after the first element gives

```
[2] + [2,1]
```

After sorting each side:

```
[2] + [1,2]
```

which becomes

```
[2,1,2]
```

and is not sorted. The correct answer is `"YES"`.

Another situation that can mislead a careless solution is an already sorted array:

```
5
1 2 2 4 4
```

No matter where we split, the largest element of the left side never exceeds the smallest element of the right side. Every resulting array stays sorted, so the answer is `"NO"`.

Duplicates also deserve attention. For example,

```
4
1 3 3 2
```

Splitting after the third element gives

```
[1,3,3] + [2]
```

After sorting, nothing changes:

```
[1,3,3,2]
```

which is still unsorted. Equal values are harmless, only a strict inversion matters.

## Approaches

A direct approach tries every possible split. For each position, we sort the prefix and suffix independently, concatenate them, and check whether the whole array is sorted. There are $n-1$ possible split points, and each attempt performs two sorts and one linear check. The worst case is roughly $O(n^2 \log n)$. With $n\le10^4$, this would still pass, but it performs much more work than necessary.

The reason brute force works is that after sorting each piece, the only possible place where disorder can remain is at the boundary between the two pieces. Inside each piece, everything is already sorted.

Suppose we split after position $i$. After sorting, the left part ends with its maximum element, and the right part begins with its minimum element. The entire array is sorted exactly when

$$\max(\text{left}) \le \min(\text{right})$$

If instead

$$\max(\text{left}) > \min(\text{right}),$$

then these two boundary elements create an inversion and the final array is not sorted.

Now observe something even simpler. If the original array contains any inversion $a_i>a_j$ with $i<j$, then taking the split between those positions places the larger value somewhere in the left half and the smaller value somewhere in the right half. After sorting internally, the left half still contains that larger value as part of its maximum and the right half still contains the smaller value as part of its minimum, so the boundary remains inverted.

That means the answer is `"YES"` exactly when the original array itself is not sorted.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n² log n) | O(n) | Accepted but unnecessary |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the array.
2. Scan adjacent pairs from left to right because a non-decreasing array must satisfy $a_i\le a_{i+1}$ everywhere.
3. If some adjacent pair satisfies $a_i>a_{i+1}$, the array already contains an inversion. Output `"YES"`.

A single adjacent inversion is enough because choosing the split between those two elements makes the left maximum larger than the right minimum.

1. If no such pair exists, the array is already sorted in non-decreasing order. Output `"NO"`.

### Why it works

A sorted array stays sorted after sorting any prefix and suffix independently. Conversely, if the original array contains an inversion, then there must also exist an adjacent inversion. Splitting between those two elements leaves the larger value in the left half and the smaller value in the right half. Sorting each side cannot remove this cross-boundary inversion. Hence the operation produces an unsorted array. These two facts completely characterize the answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())

for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))

    ok = False
    for i in range(n - 1):
        if a[i] > a[i + 1]:
            ok = True
            break

    print("YES" if ok else "NO")
```

The loop over adjacent elements is enough because every unsorted array contains at least one adjacent inversion. Once such a pair is found, we can stop immediately since one witness is sufficient.

The implementation avoids unnecessary sorting and uses only constant extra memory. Boundary conditions are simple because the loop runs from `0` to `n-2`, making `a[i+1]` always valid.

## Worked Examples

Consider the sample

```
3
2 2 1
```

| i | a[i] | a[i+1] | a[i] > a[i+1]? | ok |
| --- | --- | --- | --- | --- |
| 0 | 2 | 2 | No | False |
| 1 | 2 | 1 | Yes | True |

The algorithm finds an adjacent inversion at positions 2 and 3, so the answer is `"YES"`.

This example shows that even though most of the array is ordered, a single inversion is enough.

Consider

```
5
1 2 2 4 4
```

| i | a[i] | a[i+1] | a[i] > a[i+1]? | ok |
| --- | --- | --- | --- | --- |
| 0 | 1 | 2 | No | False |
| 1 | 2 | 2 | No | False |
| 2 | 2 | 4 | No | False |
| 3 | 4 | 4 | No | False |

No adjacent inversion appears, so the answer is `"NO"`.

This confirms that duplicate values do not cause trouble. Only a strict decrease matters.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One pass over the array |
| Space | O(1) | Only a boolean variable is used |

Since the total number of elements across all test cases is at most $10^4$, the linear solution runs comfortably within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        ok = False
        for i in range(n - 1):
            if a[i] > a[i + 1]:
                ok = True
                break

        out.append("YES" if ok else "NO")

    return "\n".join(out)

# provided samples
assert run(
"""3
3
2 2 1
4
3 1 2 1
5
1 2 2 4 4
"""
) == """YES
YES
NO"""

# minimum size, increasing
assert run(
"""1
2
1 2
"""
) == "NO", "already sorted"

# minimum size, decreasing
assert run(
"""1
2
2 1
"""
) == "YES", "single inversion"

# all equal values
assert run(
"""1
5
7 7 7 7 7
"""
) == "NO", "duplicates are allowed"

# inversion near the end
assert run(
"""1
5
1 2 3 5 4
"""
) == "YES", "boundary inversion"

# maximum-size style case
assert run(
"1\n10000\n" + " ".join(map(str, range(1, 10001))) + "\n"
) == "NO", "large sorted array"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `[1,2]` | NO | Minimum size, already sorted |
| `[2,1]` | YES | Minimum size with inversion |
| `[7,7,7,7,7]` | NO | Equal values are valid |
| `[1,2,3,5,4]` | YES | Inversion near the boundary |
| `1,2,...,10000` | NO | Large input performance |

## Edge Cases

Consider

```
1
2
2 1
```

The scan checks the only adjacent pair and finds `2 > 1`. The algorithm outputs `"YES"`. Splitting between the two elements produces `[2] + [1]`, which remains unsorted.

Consider

```
1
5
1 2 2 4 4
```

Every adjacent pair satisfies the non-decreasing condition. The algorithm reaches the end without finding an inversion and outputs `"NO"`. Any split preserves global order because the maximum element on the left never exceeds the minimum element on the right.

Consider

```
1
4
1 3 3 2
```

The scan reaches the pair `(3,2)` and detects an inversion. The answer is `"YES"`. Splitting after the third position gives

```
[1,3,3] + [2]
```

Sorting each part changes nothing, and the final array remains

```
[1,3,3,2]
```

which is not sorted. This example shows that duplicate values do not affect the argument. Only a strict decrease matters.
