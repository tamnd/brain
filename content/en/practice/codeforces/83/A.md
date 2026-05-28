---
title: "CF 83A - Magical Array"
description: "We are given an integer array and need to count how many contiguous subarrays are \"magical\". A subarray is magical when its minimum value is equal to its maximum value. A minimum and maximum can only be equal if every element inside the subarray is the same."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 83
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 72 (Div. 1 Only)"
rating: 1300
weight: 83
solve_time_s: 88
verified: true
draft: false
---

[CF 83A - Magical Array](https://codeforces.com/problemset/problem/83/A)

**Rating:** 1300  
**Tags:** math  
**Solve time:** 1m 28s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an integer array and need to count how many contiguous subarrays are "magical". A subarray is magical when its minimum value is equal to its maximum value.

A minimum and maximum can only be equal if every element inside the subarray is the same. That observation completely changes the problem. Instead of thinking about arbitrary subarrays, we only care about consecutive blocks of equal numbers.

For example, in the array:

```
2 1 1 4
```

the consecutive equal-value blocks are:

```
[2]
[1 1]
[4]
```

Every single-element subarray is magical, and the block `[1 1]` also contributes the subarray `[1, 1]` of length 2.

The array length can be as large as $10^5$. A quadratic algorithm that checks every subarray would examine roughly:

$$\frac{n(n+1)}{2}$$

subarrays, which becomes about $5 \times 10^9$ when $n = 10^5$. That is far beyond what fits in a 2-second limit.

The constraints strongly suggest that we need a linear or near-linear solution.

There are a few easy-to-miss edge cases.

Consider an array where all elements are different:

```
5
1 2 3 4 5
```

The correct answer is `5`, because only single-element subarrays qualify. A careless implementation might accidentally count longer ranges if it only checks endpoints.

Now consider an array where all elements are equal:

```
4
7 7 7 7
```

Every subarray is magical. The answer is:

$$\frac{4 \cdot 5}{2} = 10$$

A buggy implementation might only count maximal equal segments once instead of counting all subarrays inside them.

Another subtle case is when equal blocks appear multiple times:

```
6
1 1 2 2 2 1
```

The last `1` does not connect with the first block of `1`s because subarrays must be contiguous. The correct answer comes from treating each equal segment independently:

```
2 + 6 + 1 = 9
```

where:

$$\frac{2 \cdot 3}{2} = 3$$

for the first block,

$$\frac{3 \cdot 4}{2} = 6$$

for the middle block,

and

$$1$$

for the last element.

## Approaches

The brute-force idea is straightforward. Enumerate every possible subarray, compute its minimum and maximum, and count it if they are equal.

For a subarray `a[l:r]`, the condition:

```
min(a[l:r]) == max(a[l:r])
```

means all elements are identical.

A naive implementation would use three nested operations:

1. Choose the left endpoint.
2. Choose the right endpoint.
3. Scan the subarray to compute minimum and maximum.

That costs $O(n^3)$.

Even if we optimize the minimum and maximum incrementally, we still examine all $O(n^2)$ subarrays. With $10^5$ elements, that is still far too slow.

The key observation is that a subarray is magical if and only if every element inside it is equal.

That means magical subarrays never cross between different values. They exist entirely inside contiguous runs of identical numbers.

Suppose we have a block of length $k$:

```
x x x x ... x
```

Every subarray inside this block is magical.

The number of subarrays inside a length-$k$ segment is:

$$\frac{k(k+1)}{2}$$

because:

- there are $k$ subarrays of length 1,
- $k-1$ of length 2,
- $k-2$ of length 3,
- and so on.

So the whole problem reduces to:

1. Find lengths of maximal contiguous equal segments.
2. Sum $\frac{k(k+1)}{2}$ over all segments.

We can scan the array once while tracking the current segment length. That gives a linear-time solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) to O(n³) | O(1) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the array size and the array itself.
2. Initialize the answer variable to `0`.
3. Start scanning the array from left to right while maintaining the length of the current block of equal values.
4. Set the current block length to `1` for the first element.
5. For each next element:

1. If it is equal to the previous element, extend the current block by increasing the length.
2. Otherwise, the previous block has ended. Add:

$$\frac{len \cdot (len + 1)}{2}$$

to the answer, then start a new block with length `1`.

The formula counts all subarrays entirely inside that equal-value segment.

1. After the loop finishes, add the contribution of the final block, since the array may end while we are still inside a segment.
2. Print the total answer.

### Why it works

Every magical subarray consists entirely of equal values. Such a subarray must lie completely inside one maximal contiguous equal segment.

For a segment of length $k$, every possible contiguous subarray inside it is magical, and there are exactly:

$$\frac{k(k+1)}{2}$$

of them.

The algorithm partitions the array into maximal equal segments and counts all subarrays inside each one exactly once. No magical subarray is missed, and no invalid subarray is counted.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))

ans = 0
length = 1

for i in range(1, n):
    if a[i] == a[i - 1]:
        length += 1
    else:
        ans += length * (length + 1) // 2
        length = 1

ans += length * (length + 1) // 2

print(ans)
```

The program keeps track of the current contiguous segment of equal values.

The variable `length` stores the size of the current segment. Whenever the next value matches the previous one, we extend the segment. Otherwise, the segment ends and we add its contribution.

The formula:

$$\frac{k(k+1)}{2}$$

is implemented as:

```
length * (length + 1) // 2
```

Integer division is necessary because the result must remain an integer.

The final addition after the loop is easy to forget. Without it, the last segment would never contribute to the answer.

The solution uses only constant extra memory and scans the array once.

## Worked Examples

### Sample 1

Input:

```
4
2 1 1 4
```

| Index | Value | Current Segment Length | Action | Answer |
| --- | --- | --- | --- | --- |
| 0 | 2 | 1 | Start segment | 0 |
| 1 | 1 | 1 | Previous segment ends, add 1 | 1 |
| 2 | 1 | 2 | Extend segment | 1 |
| 3 | 4 | 1 | Previous segment ends, add 3 | 4 |
| End | - | 1 | Add final segment | 5 |

The segments are:

```
[2]
[1 1]
[4]
```

Their contributions are:

```
1 + 3 + 1 = 5
```

This trace shows that each equal block is processed independently.

### Sample 2

Input:

```
5
1 1 1 2 3
```

| Index | Value | Current Segment Length | Action | Answer |
| --- | --- | --- | --- | --- |
| 0 | 1 | 1 | Start segment | 0 |
| 1 | 1 | 2 | Extend segment | 0 |
| 2 | 1 | 3 | Extend segment | 0 |
| 3 | 2 | 1 | Previous segment ends, add 6 | 6 |
| 4 | 3 | 1 | Previous segment ends, add 1 | 7 |
| End | - | 1 | Add final segment | 8 |

The segments are:

```
[1 1 1]
[2]
[3]
```

The contributions are:

```
6 + 1 + 1 = 8
```

This example demonstrates how a long equal segment contributes many subarrays at once.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | The array is scanned once |
| Space | O(1) | Only a few variables are stored |

A linear scan easily fits within the limit for $n = 10^5$. The memory usage is tiny compared to the 256 MB limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))

    ans = 0
    length = 1

    for i in range(1, n):
        if a[i] == a[i - 1]:
            length += 1
        else:
            ans += length * (length + 1) // 2
            length = 1

    ans += length * (length + 1) // 2

    print(ans)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out

# provided sample
assert run("4\n2 1 1 4\n") == "5\n", "sample 1"

# all elements different
assert run("5\n1 2 3 4 5\n") == "5\n", "all distinct"

# all elements equal
assert run("4\n7 7 7 7\n") == "10\n", "all equal"

# minimum size
assert run("1\n42\n") == "1\n", "single element"

# multiple separated blocks
assert run("6\n1 1 2 2 2 1\n") == "10\n", "multiple segments"

# alternating values
assert run("6\n1 2 1 2 1 2\n") == "6\n", "no long magical subarrays"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 2 3 4 5` | `5` | Only single elements count |
| `7 7 7 7` | `10` | Formula for one large segment |
| `42` | `1` | Minimum input size |
| `1 1 2 2 2 1` | `10` | Separate equal blocks handled independently |
| `1 2 1 2 1 2` | `6` | Alternating values produce only length-1 subarrays |

## Edge Cases

Consider the case where every value is different:

```
5
1 2 3 4 5
```

The algorithm creates five separate segments of length 1.

Their contributions are:

```
1 + 1 + 1 + 1 + 1 = 5
```

No longer subarray is counted because the segment breaks immediately whenever the value changes.

Now consider an array where all values are equal:

```
4
7 7 7 7
```

The scan never breaks the segment. At the end:

```
length = 4
```

The algorithm adds:

$$\frac{4 \cdot 5}{2} = 10$$

which matches the total number of all possible subarrays.

Finally, consider separated equal blocks:

```
6
1 1 2 2 2 1
```

The algorithm processes:

```
[1 1]
[2 2 2]
[1]
```

independently.

The first and last `1` are never merged because the `2`s break contiguity. That correctly prevents counting invalid subarrays like:

```
1 1 2 2 2 1
^           ^
```

which are not magical.
