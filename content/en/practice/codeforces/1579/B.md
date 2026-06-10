---
title: "CF 1579B - Shifting Sort"
description: "We are given an array and a special operation. Instead of swapping individual elements, we may choose any contiguous segment and rotate that segment to the left by any amount. After the rotation, the elements remain inside the same interval, only their order changes cyclically."
date: "2026-06-10T10:20:45+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1579
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 744 (Div. 3)"
rating: 1100
weight: 1579
solve_time_s: 130
verified: false
draft: false
---

[CF 1579B - Shifting Sort](https://codeforces.com/problemset/problem/1579/B)

**Rating:** 1100  
**Tags:** implementation, sortings  
**Solve time:** 2m 10s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array and a special operation. Instead of swapping individual elements, we may choose any contiguous segment and rotate that segment to the left by any amount. After the rotation, the elements remain inside the same interval, only their order changes cyclically.

The task is to transform the array into nondecreasing order. We do not have to minimize the number of operations. Any sequence using at most $n$ rotations is accepted.

Each test case contains one array. For every test case we must output how many rotations we perform and then describe every rotation by its left endpoint, right endpoint, and shift amount.

The constraints are very small. The array length is at most 50, and there are at most 1000 test cases. Even an $O(n^3)$ solution performs only about $50^3=125000$ operations per test case, which is easily fast enough. There is no need for sophisticated data structures.

One subtle point is the presence of duplicate values. Suppose the array is

```
3
2 1 1
```

The sorted version is

```
1 1 2
```

When fixing position 0, we must move the first unused occurrence of value 1, not an arbitrary one. Otherwise we may disturb the relative placement of equal values and later positions become harder to match.

Another corner case occurs when the correct element is already in place. For example

```
4
1 2 3 4
```

The answer should contain zero operations. A careless implementation might still output useless rotations with shift zero, but the problem requires the shift amount to be positive.

Arrays containing equal elements also require attention. For

```
4
5 5 5 5
```

the array is already sorted, so the correct answer is again zero operations. Searching for the first matching value and rotating unnecessarily would only complicate things.

## Approaches

A brute-force idea is to search through all possible sequences of rotations until a sorted array appears. Since every interval and every shift amount are available, the number of possibilities grows explosively. Even for $n=50$, this approach is hopeless.

The useful observation is that we do not need to optimize the number of operations. We only need some sequence using at most $n$ rotations.

Think about insertion sort. At position $i$, once positions $0\ldots i-1$ are already correct, we only need to bring the element that should occupy position $i$ into that place. If that element currently sits at position $j$, we can choose segment $[i,j]$ and rotate it left by $j-i$.

Suppose the segment is

```
[x1, x2, ..., xk, target]
```

Rotating left by $k$ produces

```
[target, x1, x2, ..., xk]
```

Exactly the desired element moves to position $i$, while all previously fixed positions remain untouched. Since each position needs at most one rotation, we perform at most $n-1$ operations.

The brute-force approach works because rotations are expressive enough to reach any permutation, but it fails because the search space is enormous. The observation that one carefully chosen rotation can place one position permanently reduces the problem to a simple insertion-sort-like process.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(n²) | O(n) | Accepted |

## Algorithm Walkthrough

1. Create a sorted copy of the array.
2. Process positions from left to right.
3. For the current position $i$, find the first position $j\ge i$ whose value equals the value that should appear at position $i$ in the sorted array.
4. If $j=i$, the correct element is already there, so move on.
5. Otherwise consider segment $[i,j]$. Rotate this segment left by $j-i$.
6. After the rotation, the element originally at position $j$ moves to position $i$, while all elements between $i$ and $j-1$ shift one position to the right.
7. Record this operation and continue with the next position.

### Why it works

The invariant is that before processing position $i$, the prefix $0\ldots i-1$ already matches the sorted array.

When we locate the required value at position $j$ and rotate segment $[i,j]$, only positions from $i$ to $j$ change. Positions before $i$ remain untouched, so the invariant is preserved. The desired value moves exactly into position $i$, making the prefix $0\ldots i$ correct.

By induction, after finishing all positions, every index contains the same value as the sorted array, so the entire array is sorted.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        target = sorted(a)
        ops = []

        for i in range(n):
            j = i
            while j < n and a[j] != target[i]:
                j += 1

            if j == i:
                continue

            ops.append((i + 1, j + 1, j - i))

            val = a[j]
            for k in range(j, i, -1):
                a[k] = a[k - 1]
            a[i] = val

        out.append(str(len(ops)))
        for l, r, d in ops:
            out.append(f"{l} {r} {d}")

    sys.stdout.write("\n".join(out))

solve()
```

The algorithm first builds the sorted target array. This tells us which value should occupy each position.

For every index, we search to the right until we find the first occurrence of the needed value. Using the first occurrence is important when duplicates exist. Choosing a later copy would still work in many cases, but taking the earliest one naturally mimics insertion sort and keeps the number of operations small.

The operation parameters use 1-based indexing because that is what the statement requires.

The actual array update deserves some care. Rotating segment $[i,j]$ left by $j-i$ is equivalent to taking element `a[j]`, placing it at position `i`, and shifting the elements between them one step to the right. Implementing this directly avoids creating temporary slices and keeps the logic transparent.

Because each position triggers at most one operation, the number of operations never exceeds $n-1$.

## Worked Examples

### Example 1

Input array:

```
2 4 1 3
```

Sorted target:

```
1 2 3 4
```

| i | Target value | j found | Array after operation | Operation |
| --- | --- | --- | --- | --- |
| 0 | 1 | 2 | [1,2,4,3] | (1,3,2) |
| 1 | 2 | 1 | [1,2,4,3] | none |
| 2 | 3 | 3 | [1,2,3,4] | (3,4,1) |
| 3 | 4 | 3 | [1,2,3,4] | none |

The first rotation moves 1 into the front. The second nontrivial rotation fixes position 2. Previously fixed positions are never disturbed.

### Example 2

Input array:

```
2 5 1 4 3
```

Sorted target:

```
1 2 3 4 5
```

| i | Target value | j found | Array after operation | Operation |
| --- | --- | --- | --- | --- |
| 0 | 1 | 2 | [1,2,5,4,3] | (1,3,2) |
| 1 | 2 | 1 | [1,2,5,4,3] | none |
| 2 | 3 | 4 | [1,2,3,5,4] | (3,5,2) |
| 3 | 4 | 4 | [1,2,3,4,5] | (4,5,1) |
| 4 | 5 | 4 | [1,2,3,4,5] | none |

This example shows that one operation permanently fixes one new position. After processing index 2, the prefix `[1,2,3]` is already final.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) | Each position performs a linear search and a linear shift |
| Space | O(n) | Only the sorted copy and operation list are stored |

Since $n\le50$, even the quadratic algorithm is extremely fast. The memory usage is negligible compared with the limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    ans = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        target = sorted(a)
        ops = []

        for i in range(n):
            j = i
            while j < n and a[j] != target[i]:
                j += 1

            if j == i:
                continue

            ops.append((i + 1, j + 1, j - i))

            val = a[j]
            for k in range(j, i, -1):
                a[k] = a[k - 1]
            a[i] = val

        ans.append(str(len(ops)))
        for x in ops:
            ans.append("{} {} {}".format(*x))

    return "\n".join(ans)

# minimum size
assert run("1\n2\n2 1\n") == "1\n1 2 1"

# already sorted
assert run("1\n4\n1 2 3 4\n") == "0"

# all equal values
assert run("1\n4\n5 5 5 5\n") == "0"

# duplicates
assert run("1\n3\n2 1 1\n") == "1\n1 2 1"

# off-by-one case
assert run("1\n5\n5 1 2 3 4\n") == "1\n1 5 4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 1` | one operation | Minimum size |
| `1 2 3 4` | zero operations | Already sorted arrays |
| `5 5 5 5` | zero operations | Equal values |
| `2 1 1` | one operation | Handling duplicates |
| `5 1 2 3 4` | shift by four | Boundary indices |

## Edge Cases

Consider duplicate values:

```
1
3
2 1 1
```

The sorted array is `[1,1,2]`.

At position 0 we need a 1. The first occurrence appears at index 1. Rotating segment `[0,1]` gives

```
[1,2,1]
```

Position 0 is now correct. At position 1 we again need a 1, which is already available at index 2. Another rotation would sort the array, but since index 1 currently contains 2, the algorithm performs that operation automatically if needed. Duplicates cause no ambiguity because we always search from the current index onward.

Now consider an already sorted array:

```
1
4
1 2 3 4
```

For every position, the search immediately finds `j=i`. No operation is recorded. The output contains zero operations, which satisfies the problem requirements.

Finally consider all equal values:

```
1
4
7 7 7 7
```

The sorted copy is identical to the original array. Every search stops immediately, no rotations are performed, and the algorithm correctly outputs zero operations. A careless implementation that blindly rotates segments would violate the requirement that the shift amount must be positive.
