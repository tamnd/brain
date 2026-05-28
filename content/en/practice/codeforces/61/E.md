---
title: "CF 61E - Enemy is weak"
description: "We are given an array of distinct integers representing the power of soldiers standing in a line. We need to count how many index triples (i, j, k) satisfy two conditions at the same time: - The positions are ordered as i < j < k - The values are strictly decreasing as a[i] a[j]…"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "trees"]
categories: ["algorithms"]
codeforces_contest: 61
codeforces_index: "E"
codeforces_contest_name: "Codeforces Beta Round 57 (Div. 2)"
rating: 1900
weight: 61
solve_time_s: 114
verified: true
draft: false
---

[CF 61E - Enemy is weak](https://codeforces.com/problemset/problem/61/E)

**Rating:** 1900  
**Tags:** data structures, trees  
**Solve time:** 1m 54s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of distinct integers representing the power of soldiers standing in a line. We need to count how many index triples `(i, j, k)` satisfy two conditions at the same time:

- The positions are ordered as `i < j < k`
- The values are strictly decreasing as `a[i] > a[j] > a[k]`

Another way to think about it is this: for every middle position `j`, we want to know how many larger elements exist before it and how many smaller elements exist after it. Every combination of those choices forms one valid decreasing triplet.

The constraints completely determine the kind of algorithm we need. The array size can reach `10^6`, which rules out anything quadratic, let alone cubic. Even an `O(n^2)` solution would require around `10^12` operations in the worst case, far beyond what fits in 5 seconds. The target complexity must be close to linear or `O(n log n)`.

The values themselves can be as large as `10^9`, so we cannot directly build arrays indexed by value. Any data structure that depends on value ranges needs coordinate compression first.

One subtle issue is integer overflow. The number of decreasing triplets can be extremely large. For example, if the array is strictly decreasing and `n = 10^6`, the answer is:

$$\binom{10^6}{3}$$

That is around `1.67 × 10^17`, which does not fit in 32-bit integers. Python handles this automatically, but in C++ the answer must be stored in `long long`.

Another easy mistake is mishandling the “strictly greater” condition. Suppose the array were:

```
4
5 5 4 3
```

The problem guarantees distinct values, so this input is invalid, but many generic implementations accidentally use `>=` or `<=` logic. If duplicates were present, incorrect inequality handling would silently overcount. The correct condition is strictly decreasing at every step.

A more realistic edge case is a strictly increasing array:

```
5
1 2 3 4 5
```

The correct answer is `0` because no decreasing triple exists. A careless implementation that mixes up left and right counts may accidentally count increasing patterns instead.

Another important scenario is when all valid triples share the same middle element. For example:

```
5
5 4 3 2 1
```

Every triple is valid here, giving:

$$\binom{5}{3} = 10$$

This case stresses whether the algorithm correctly combines “greater on the left” with “smaller on the right”.

## Approaches

The brute-force solution directly follows the definition. We try every triple `(i, j, k)` with `i < j < k` and check whether the values form a strictly decreasing sequence.

```
for i:
    for j > i:
        for k > j:
            check a[i] > a[j] > a[k]
```

This is correct because every possible triple is examined exactly once. The problem is the running time. The number of triples is:

$$\binom{n}{3}$$

For `n = 10^6`, that is roughly `1.67 × 10^17` iterations, which is completely impossible.

The key observation is that the middle index `j` determines everything. If we already know:

- how many elements before `j` are greater than `a[j]`
- how many elements after `j` are smaller than `a[j]`

then the number of valid triples using `j` as the middle element is simply:

$$\text{leftGreater}[j] \times \text{rightSmaller}[j]$$

This transforms the problem from searching over triples into answering frequency queries.

Now the task becomes:

- While scanning from left to right, count how many previous values are greater than the current one.
- While scanning from right to left, count how many later values are smaller than the current one.

Those are classic prefix-frequency queries, which can be handled efficiently with a Fenwick Tree.

Because array values are up to `10^9`, we first compress them into ranks from `1` to `n`. Since all values are distinct, compression preserves ordering exactly.

Each Fenwick Tree operation takes `O(log n)`, and we perform a constant number of operations per element. That gives total complexity `O(n log n)`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(n^3)` | `O(1)` | Too slow |
| Optimal | `O(n log n)` | `O(n)` | Accepted |

## Algorithm Walkthrough

1. Read the array and coordinate-compress its values.

We sort the distinct values and assign ranks from `1` to `n`. Fenwick Trees work on compact integer indices, so compression lets us preserve comparisons while avoiding huge arrays.
2. Create an array `left_greater`.

`left_greater[i]` will store how many earlier elements are larger than `a[i]`.
3. Scan the array from left to right using a Fenwick Tree.

At each position:

- Query how many processed elements are less than or equal to the current value.
- Subtract that from the number of processed elements to get how many are greater.
- Store that count in `left_greater[i]`.
- Insert the current value into the Fenwick Tree.

The reason subtraction works is that every previous element is either greater or not greater, and all values are distinct.
4. Reset the Fenwick Tree.

We now reuse it for suffix information.
5. Create an array `right_smaller`.

`right_smaller[i]` will store how many later elements are smaller than `a[i]`.
6. Scan the array from right to left.

At each position:

- Query how many already-seen values are strictly smaller than the current value.
- Store that result in `right_smaller[i]`.
- Insert the current value into the Fenwick Tree.

Since we move from right to left, the tree always contains exactly the elements after the current index.
7. Compute the final answer.

For every position `i`, add:

$$\text{left\_greater}[i] \times \text{right\_smaller}[i]$$

Every valid triplet has exactly one middle index, so this counts each decreasing triple once.

### Why it works

For any fixed middle index `j`, a valid triplet is completely determined by choosing:

- one index `i < j` with `a[i] > a[j]`
- one index `k > j` with `a[k] < a[j]`

The choices are independent, so the number of triplets centered at `j` is the product of those two counts.

The left-to-right Fenwick pass correctly tracks all elements before `j`, and the right-to-left pass correctly tracks all elements after `j`. Since every decreasing triplet has a unique middle position, summing over all `j` counts every valid triplet exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def update(self, idx, delta):
        while idx <= self.n:
            self.bit[idx] += delta
            idx += idx & -idx

    def query(self, idx):
        res = 0
        while idx > 0:
            res += self.bit[idx]
            idx -= idx & -idx
        return res

def solve():
    n = int(input())
    arr = list(map(int, input().split()))

    # coordinate compression
    vals = sorted(arr)
    rank = {v: i + 1 for i, v in enumerate(vals)}
    comp = [rank[x] for x in arr]

    left_greater = [0] * n
    right_smaller = [0] * n

    bit = Fenwick(n)

    # left greater counts
    for i in range(n):
        x = comp[i]

        less_or_equal = bit.query(x)
        left_greater[i] = i - less_or_equal

        bit.update(x, 1)

    bit = Fenwick(n)

    # right smaller counts
    for i in range(n - 1, -1, -1):
        x = comp[i]

        right_smaller[i] = bit.query(x - 1)

        bit.update(x, 1)

    ans = 0

    for i in range(n):
        ans += left_greater[i] * right_smaller[i]

    print(ans)

solve()
```

The Fenwick Tree stores frequency counts of already-processed compressed values. The `update` operation inserts a value, and `query(idx)` returns how many inserted values have compressed rank at most `idx`.

Coordinate compression is necessary because values can be as large as `10^9`. Fenwick Trees require dense integer indices, so we remap values into the range `1...n` while preserving ordering.

During the left-to-right pass, the tree contains exactly the elements before the current index. `bit.query(x)` tells us how many earlier values are smaller than or equal to the current value. Since all values are distinct, this is equivalent to counting strictly smaller values. Subtracting from `i`, the number of previous elements, gives the count of greater values.

The right-to-left pass is slightly different. Here we directly query `x - 1`, which counts strictly smaller elements among the suffix already inserted into the tree.

One easy off-by-one mistake is forgetting that Fenwick Trees are usually 1-indexed. Compression starts from `1`, not `0`, specifically to avoid infinite loops in `update`.

Another subtle detail is using two separate passes instead of trying to compute both directions simultaneously. The meaning of the tree depends entirely on traversal direction. Reusing the same tree without resetting it would mix prefix and suffix information incorrectly.

## Worked Examples

### Example 1

Input:

```
3
3 2 1
```

Compressed values remain `[3, 2, 1]`.

Left-to-right pass:

| i | value | less_or_equal | left_greater |
| --- | --- | --- | --- |
| 0 | 3 | 0 | 0 |
| 1 | 2 | 0 | 1 |
| 2 | 1 | 0 | 2 |

Right-to-left pass:

| i | value | smaller_right | right_smaller |
| --- | --- | --- | --- |
| 2 | 1 | 0 | 0 |
| 1 | 2 | 1 | 1 |
| 0 | 3 | 2 | 2 |

Final computation:

| i | left_greater | right_smaller | contribution |
| --- | --- | --- | --- |
| 0 | 0 | 2 | 0 |
| 1 | 1 | 1 | 1 |
| 2 | 2 | 0 | 0 |

Total answer = `1`.

This trace shows the central idea clearly. Only index `1` can serve as the middle element of a decreasing triplet.

### Example 2

Input:

```
5
5 1 4 2 3
```

Compressed values are `[5, 1, 4, 2, 3]`.

Left-to-right pass:

| i | value | less_or_equal | left_greater |
| --- | --- | --- | --- |
| 0 | 5 | 0 | 0 |
| 1 | 1 | 0 | 1 |
| 2 | 4 | 1 | 1 |
| 3 | 2 | 1 | 2 |
| 4 | 3 | 2 | 2 |

Right-to-left pass:

| i | value | smaller_right | right_smaller |
| --- | --- | --- | --- |
| 4 | 3 | 0 | 0 |
| 3 | 2 | 0 | 0 |
| 2 | 4 | 2 | 2 |
| 1 | 1 | 0 | 0 |
| 0 | 5 | 4 | 4 |

Final computation:

| i | left_greater | right_smaller | contribution |
| --- | --- | --- | --- |
| 0 | 0 | 4 | 0 |
| 1 | 1 | 0 | 0 |
| 2 | 1 | 2 | 2 |
| 3 | 2 | 0 | 0 |
| 4 | 2 | 0 | 0 |

Total answer = `2`.

The valid triplets are `(5,4,2)` and `(5,4,3)`. This example demonstrates why the middle index viewpoint is powerful. Index `2` contributes exactly two triplets because it has one larger element before it and two smaller elements after it.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n log n)` | Each Fenwick update and query takes `O(log n)`, and we perform a constant number per element |
| Space | `O(n)` | Compression arrays, Fenwick Tree, and helper arrays all scale linearly |

With `n = 10^6`, `O(n log n)` is fast enough in Python when implemented carefully with Fenwick Trees and fast I/O. The memory usage also fits comfortably within the 256 MB limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    class Fenwick:
        def __init__(self, n):
            self.n = n
            self.bit = [0] * (n + 1)

        def update(self, idx, delta):
            while idx <= self.n:
                self.bit[idx] += delta
                idx += idx & -idx

        def query(self, idx):
            res = 0
            while idx > 0:
                res += self.bit[idx]
                idx -= idx & -idx
            return res

    n = int(input())
    arr = list(map(int, input().split()))

    vals = sorted(arr)
    rank = {v: i + 1 for i, v in enumerate(vals)}
    comp = [rank[x] for x in arr]

    left_greater = [0] * n
    right_smaller = [0] * n

    bit = Fenwick(n)

    for i in range(n):
        x = comp[i]
        left_greater[i] = i - bit.query(x)
        bit.update(x, 1)

    bit = Fenwick(n)

    for i in range(n - 1, -1, -1):
        x = comp[i]
        right_smaller[i] = bit.query(x - 1)
        bit.update(x, 1)

    ans = 0

    for i in range(n):
        ans += left_greater[i] * right_smaller[i]

    return str(ans)

# provided sample
assert run("3\n3 2 1\n") == "1", "sample 1"

# minimum size, no valid triplet
assert run("3\n1 2 3\n") == "0", "strictly increasing"

# minimum size, exactly one triplet
assert run("3\n3 2 1\n") == "1", "strictly decreasing"

# larger decreasing case
assert run("5\n5 4 3 2 1\n") == "10", "all triples valid"

# mixed ordering
assert run("5\n5 1 4 2 3\n") == "2", "mixed arrangement"

# off-by-one style check
assert run("4\n4 1 3 2\n") == "1", "single valid triplet"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3 / 1 2 3` | `0` | No decreasing triplets exist |
| `3 / 3 2 1` | `1` | Smallest nontrivial valid case |
| `5 / 5 4 3 2 1` | `10` | Every triple is valid |
| `5 / 5 1 4 2 3` | `2` | Mixed ordering with selective contributions |
| `4 / 4 1 3 2` | `1` | Detects off-by-one mistakes in Fenwick queries |

## Edge Cases

Consider the strictly increasing array:

```
5
1 2 3 4 5
```

During the left-to-right pass, every earlier value is smaller, so `left_greater` becomes:

```
[0, 0, 0, 0, 0]
```

The right-to-left pass still finds smaller suffix values, but every final contribution contains a zero factor:

```
left_greater[i] * right_smaller[i] = 0
```

The final answer is correctly `0`.

Now consider the fully decreasing array:

```
5
5 4 3 2 1
```

The algorithm computes:

```
left_greater  = [0, 1, 2, 3, 4]
right_smaller = [4, 3, 2, 1, 0]
```

The contributions become:

```
0*4 + 1*3 + 2*2 + 3*1 + 4*0
= 0 + 3 + 4 + 3 + 0
= 10
```

That matches the expected value:

$$\binom{5}{3} = 10$$

This confirms that the multiplication logic correctly counts every possible pairing of larger-left and smaller-right elements.

Finally, examine a case where only one middle index contributes:

```
5
5 1 4 2 3
```

At index `2` with value `4`:

- One larger element exists before it: `5`
- Two smaller elements exist after it: `2` and `3`

The algorithm multiplies these counts:

```
1 * 2 = 2
```

No other index contributes. This demonstrates why separating the problem by middle element avoids both undercounting and double-counting.
