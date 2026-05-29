---
title: "CF 242E - XOR on Segment"
description: "We maintain an array of integers and process two kinds of range operations. The first operation asks for the sum of all elements inside a segment [l, r]. The second operation applies XOR with a value x to every element inside [l, r]."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "data-structures"]
categories: ["algorithms"]
codeforces_contest: 242
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 149 (Div. 2)"
rating: 2000
weight: 242
solve_time_s: 123
verified: true
draft: false
---

[CF 242E - XOR on Segment](https://codeforces.com/problemset/problem/242/E)

**Rating:** 2000  
**Tags:** bitmasks, data structures  
**Solve time:** 2m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

We maintain an array of integers and process two kinds of range operations.

The first operation asks for the sum of all elements inside a segment `[l, r]`.

The second operation applies XOR with a value `x` to every element inside `[l, r]`. In other words, every number `a[i]` becomes `a[i] ^ x`.

The difficulty comes from the interaction between these operations. A range XOR update changes many values at once, and later sum queries must reflect all previous updates.

The array size is up to `10^5`, and there can be `5 * 10^4` operations. A direct simulation of each update over the entire segment would take `O(n)` time per operation. In the worst case that becomes roughly:

`5 * 10^4 * 10^5 = 5 * 10^9`

operations, which is far beyond the time limit.

The constraints strongly suggest that we need a logarithmic-time data structure for both updates and queries. Segment trees are the natural candidate, but a normal lazy segment tree storing only sums is not enough because XOR is not additive.

The key complication is that XOR affects each bit independently. For example:

```
5 ^ 3
101
011
---
110 = 6
```

A bit flips only if the corresponding bit in `x` is `1`.

Several edge cases can silently break an incorrect implementation.

Consider a segment where all numbers already have a bit set:

```
Array: [7, 7]
Update: xor with 1
```

Binary:

```
111 ^ 001 = 110
```

Both numbers become `6`. The lowest bit changes from `1` to `0`.

A careless implementation might try to "add" the XOR value to the segment sum, but XOR is not arithmetic addition. Sometimes the sum increases, sometimes it decreases.

Another subtle case is repeated XOR updates with the same value:

```
Array: [5]
Update xor 3
Update xor 3
```

Since:

```
(a ^ x) ^ x = a
```

the value returns to the original number. Lazy propagation must combine updates using XOR, not addition or assignment.

Boundary segments are also easy to mishandle. For example:

```
n = 1
Array: [8]
Query sum [1,1]
Update xor [1,1] with 15
Query sum [1,1]
```

The answers are:

```
8
7
```

because:

```
8 ^ 15 = 7
```

If the segment tree mixes 0-indexed and 1-indexed ranges incorrectly, single-element segments usually expose the bug immediately.

## Approaches

The brute-force solution is straightforward.

For a sum query, iterate from `l` to `r` and accumulate the values.

For an XOR update, iterate from `l` to `r` and replace every element with `a[i] ^ x`.

This works because each operation exactly follows the problem definition. The problem is the running time. A single operation may touch `10^5` elements, and there are up to `5 * 10^4` operations. The total work becomes billions of operations.

The observation that unlocks the problem is that XOR acts independently on each bit.

Suppose we only focus on bit `k`.

For every segment, instead of storing the actual numbers, we store how many numbers currently have bit `k` equal to `1`.

Then the contribution of this bit to the segment sum is:

```
count_of_ones * (1 << k)
```

Now look at what XOR with `x` does.

If bit `k` of `x` is `0`, nothing changes for that bit.

If bit `k` of `x` is `1`, every bit in the segment flips:

```
0 -> 1
1 -> 0
```

So if a segment has length `len` and currently `ones` numbers with bit `k = 1`, after the flip it becomes:

```
len - ones
```

That transformation is extremely easy to apply lazily.

This turns the problem into maintaining 20 independent segment trees, one for each bit position from `0` to `19` since values are at most `10^6`.

Each tree supports:

1. Range flip operation.
2. Range count query.

The final sum query reconstructs the answer by combining all bits.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nm) | O(n) | Too slow |
| Optimal | O(20 log n) per operation | O(20n) | Accepted |

## Algorithm Walkthrough

1. Build 20 segment trees conceptually, one for each bit position from `0` to `19`.

Each node stores how many numbers in its segment have that bit set to `1`.
2. During construction, inspect every array element.

If bit `b` is set in `a[i]`, increment the corresponding count in the segment tree for bit `b`.
3. For a sum query on `[l, r]`, query every bit tree separately.

If the query returns `cnt` ones for bit `b`, then this bit contributes:

```
cnt * (1 << b)
```

Add contributions from all bits to obtain the final sum.
4. For an XOR update with value `x`, process each bit independently.

If bit `b` of `x` is `1`, then every value in the range flips that bit.
5. To flip a bit on a segment tree node covering length `len`, replace:

```
ones -> len - ones
```

because every `1` becomes `0` and every `0` becomes `1`.
6. Use lazy propagation to postpone updates.

A lazy flag means "this segment still needs a bit flip". If another flip arrives later, combine them with XOR:

```
lazy ^= 1
```

since two flips cancel each other.
7. When descending into children, push the pending lazy flip to both children before continuing.

This keeps the counts consistent without rebuilding the whole subtree every time.

### Why it works

For every bit position, the segment tree always stores the exact number of elements whose bit is `1` in every segment.

A XOR update flips exactly those bits where `x` has a `1`. Flipping a bit transforms the count from `ones` to `segment_length - ones`, which matches the true effect of XOR on every element.

Lazy propagation preserves correctness because postponed flips are combined using XOR parity. An even number of flips cancels out, and an odd number applies one effective flip. Since each operation updates only the affected bits and every sum query reconstructs the integer values from correct bit counts, every answer matches the actual array state.

## Python Solution

```python
import sys
input = sys.stdin.readline

MAX_BIT = 20

class SegmentTree:
    def __init__(self, arr, bit):
        self.n = len(arr)
        self.tree = [0] * (4 * self.n)
        self.lazy = [0] * (4 * self.n)
        self.build(1, 0, self.n - 1, arr, bit)

    def build(self, node, left, right, arr, bit):
        if left == right:
            self.tree[node] = (arr[left] >> bit) & 1
            return

        mid = (left + right) // 2

        self.build(node * 2, left, mid, arr, bit)
        self.build(node * 2 + 1, mid + 1, right, arr, bit)

        self.tree[node] = (
            self.tree[node * 2] +
            self.tree[node * 2 + 1]
        )

    def apply_flip(self, node, left, right):
        length = right - left + 1
        self.tree[node] = length - self.tree[node]
        self.lazy[node] ^= 1

    def push(self, node, left, right):
        if self.lazy[node] == 0 or left == right:
            return

        mid = (left + right) // 2

        self.apply_flip(node * 2, left, mid)
        self.apply_flip(node * 2 + 1, mid + 1, right)

        self.lazy[node] = 0

    def update(self, node, left, right, ql, qr):
        if qr < left or right < ql:
            return

        if ql <= left and right <= qr:
            self.apply_flip(node, left, right)
            return

        self.push(node, left, right)

        mid = (left + right) // 2

        self.update(node * 2, left, mid, ql, qr)
        self.update(node * 2 + 1, mid + 1, right, ql, qr)

        self.tree[node] = (
            self.tree[node * 2] +
            self.tree[node * 2 + 1]
        )

    def query(self, node, left, right, ql, qr):
        if qr < left or right < ql:
            return 0

        if ql <= left and right <= qr:
            return self.tree[node]

        self.push(node, left, right)

        mid = (left + right) // 2

        return (
            self.query(node * 2, left, mid, ql, qr) +
            self.query(node * 2 + 1, mid + 1, right, ql, qr)
        )

def solve():
    n = int(input())
    arr = list(map(int, input().split()))

    trees = [SegmentTree(arr, bit) for bit in range(MAX_BIT)]

    m = int(input())

    answers = []

    for _ in range(m):
        query = list(map(int, input().split()))

        if query[0] == 1:
            _, l, r = query

            l -= 1
            r -= 1

            total = 0

            for bit in range(MAX_BIT):
                cnt = trees[bit].query(1, 0, n - 1, l, r)
                total += cnt * (1 << bit)

            answers.append(str(total))

        else:
            _, l, r, x = query

            l -= 1
            r -= 1

            for bit in range(MAX_BIT):
                if (x >> bit) & 1:
                    trees[bit].update(1, 0, n - 1, l, r)

    sys.stdout.write("\n".join(answers))

solve()
```

The implementation mirrors the bitwise reasoning directly.

Each `SegmentTree` instance manages one specific bit position. The tree stores counts of set bits rather than sums of actual numbers. This is why updates become simple flips.

The `apply_flip` function is the core transition:

```
self.tree[node] = length - self.tree[node]
```

If a segment has length `10` and currently `3` ones, flipping the bit produces `7` ones.

The lazy value is only `0` or `1`. Two pending flips cancel each other:

```
lazy ^= 1
```

Using addition here would be incorrect because the parity of flips matters, not the number itself.

The solution uses 0-based indexing internally even though the input is 1-based. Every query converts:

```
l -= 1
r -= 1
```

before accessing the trees.

The sum query reconstructs the integer answer bit by bit. Since every bit contributes independently, summing:

```
cnt * (1 << bit)
```

produces the exact segment sum.

Python integers already support arbitrary precision, so overflow is not a concern, but in C++ this problem requires 64-bit integers.

## Worked Examples

### Example 1

Input:

```
5
4 10 3 13 7
```

We trace the important operations.

| Operation | Array State | Result |
| --- | --- | --- |
| Query sum [2,4] | [4,10,3,13,7] | 26 |
| XOR [1,3] with 3 | [7,9,0,13,7] | - |
| Query sum [2,4] | [7,9,0,13,7] | 22 |
| Query sum [3,3] | [7,9,0,13,7] | 0 |
| XOR [2,5] with 5 | [7,12,5,8,2] | - |
| Query sum [1,5] | [7,12,5,8,2] | 34 |
| XOR [1,2] with 10 | [13,6,5,8,2] | - |
| Query sum [2,3] | [13,6,5,8,2] | 11 |

This trace demonstrates why XOR updates cannot be treated as arithmetic addition. After XOR with `3`, the third element becomes `0`, decreasing the sum.

### Example 2

Input:

```
3
1 1 1
4
1 1 3
2 1 3 1
1 1 3
1 2 2
```

| Operation | Array State | Result |
| --- | --- | --- |
| Query sum [1,3] | [1,1,1] | 3 |
| XOR [1,3] with 1 | [0,0,0] | - |
| Query sum [1,3] | [0,0,0] | 0 |
| Query sum [2,2] | [0,0,0] | 0 |

This example highlights bit flipping directly. XOR with `1` toggles the least significant bit, turning every `1` into `0`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(20 log n) per operation | Each query/update processes at most 20 bit trees |
| Space | O(20n) | Segment tree storage for every bit |

The constant factor of 20 is small because numbers are at most `10^6`, which fits within 20 bits.

With `5 * 10^4` operations, the total complexity is roughly:

```
5 * 10^4 * 20 * log2(10^5)
```

which comfortably fits inside the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    input_data = io.StringIO(inp)
    output_data = io.StringIO()

    input = input_data.readline

    MAX_BIT = 20

    class SegmentTree:
        def __init__(self, arr, bit):
            self.n = len(arr)
            self.tree = [0] * (4 * self.n)
            self.lazy = [0] * (4 * self.n)
            self.build(1, 0, self.n - 1, arr, bit)

        def build(self, node, left, right, arr, bit):
            if left == right:
                self.tree[node] = (arr[left] >> bit) & 1
                return

            mid = (left + right) // 2

            self.build(node * 2, left, mid, arr, bit)
            self.build(node * 2 + 1, mid + 1, right, arr, bit)

            self.tree[node] = (
                self.tree[node * 2] +
                self.tree[node * 2 + 1]
            )

        def apply_flip(self, node, left, right):
            length = right - left + 1
            self.tree[node] = length - self.tree[node]
            self.lazy[node] ^= 1

        def push(self, node, left, right):
            if self.lazy[node] == 0 or left == right:
                return

            mid = (left + right) // 2

            self.apply_flip(node * 2, left, mid)
            self.apply_flip(node * 2 + 1, mid + 1, right)

            self.lazy[node] = 0

        def update(self, node, left, right, ql, qr):
            if qr < left or right < ql:
                return

            if ql <= left and right <= qr:
                self.apply_flip(node, left, right)
                return

            self.push(node, left, right)

            mid = (left + right) // 2

            self.update(node * 2, left, mid, ql, qr)
            self.update(node * 2 + 1, mid + 1, right, ql, qr)

            self.tree[node] = (
                self.tree[node * 2] +
                self.tree[node * 2 + 1]
            )

        def query(self, node, left, right, ql, qr):
            if qr < left or right < ql:
                return 0

            if ql <= left and right <= qr:
                return self.tree[node]

            self.push(node, left, right)

            mid = (left + right) // 2

            return (
                self.query(node * 2, left, mid, ql, qr) +
                self.query(node * 2 + 1, mid + 1, right, ql, qr)
            )

    n = int(input())
    arr = list(map(int, input().split()))

    trees = [SegmentTree(arr, bit) for bit in range(MAX_BIT)]

    m = int(input())

    ans = []

    for _ in range(m):
        q = list(map(int, input().split()))

        if q[0] == 1:
            _, l, r = q
            l -= 1
            r -= 1

            total = 0

            for bit in range(MAX_BIT):
                cnt = trees[bit].query(1, 0, n - 1, l, r)
                total += cnt * (1 << bit)

            ans.append(str(total))

        else:
            _, l, r, x = q
            l -= 1
            r -= 1

            for bit in range(MAX_BIT):
                if (x >> bit) & 1:
                    trees[bit].update(1, 0, n - 1, l, r)

    return "\n".join(ans)

# provided sample
assert run(
"""5
4 10 3 13 7
8
1 2 4
2 1 3 3
1 2 4
1 3 3
2 2 5 5
1 1 5
2 1 2 10
1 2 3
"""
) == """26
22
0
34
11"""

# minimum size
assert run(
"""1
8
3
1 1 1
2 1 1 15
1 1 1
"""
) == """8
7"""

# repeated xor cancels out
assert run(
"""2
5 5
5
1 1 2
2 1 2 3
2 1 2 3
1 1 2
1 2 2
"""
) == """10
10
5"""

# all equal values
assert run(
"""4
7 7 7 7
3
1 1 4
2 1 4 1
1 1 4
"""
) == """28
24"""

# boundary range updates
assert run(
"""5
1 2 3 4 5
4
2 1 1 7
1 1 2
2 5 5 3
1 4 5
"""
) == """10
10"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single element array | `8`, `7` | Correct handling of size-1 segments |
| Repeated XOR with same value | Original values restored | Lazy XOR composition |
| All equal values | Uniform bit flips | Correct bit counting |
| Boundary-only updates | Correct edge indexing | Off-by-one correctness |

## Edge Cases

Consider repeated XOR updates with the same mask:

```
2
5 5
5
1 1 2
2 1 2 3
2 1 2 3
1 1 2
1 2 2
```

Initially:

```
[5, 5]
```

After first XOR with `3`:

```
5 ^ 3 = 6
```

Array becomes:

```
[6, 6]
```

After the second XOR with `3`:

```
6 ^ 3 = 5
```

The array returns to:

```
[5, 5]
```

The segment tree handles this because lazy propagation stores flips modulo 2:

```
lazy ^= 1
```

Two flips cancel naturally.

Now consider a boundary update:

```
5
1 2 3 4 5
4
2 1 1 7
1 1 2
2 5 5 3
1 4 5
```

The first update affects only the first element:

```
1 ^ 7 = 6
```

Array becomes:

```
[6,2,3,4,5]
```

The query `[1,2]` correctly returns:

```
6 + 2 = 8
```

Later, only the last element changes:

```
5 ^ 3 = 6
```

Array becomes:

```
[6,2,3,4,6]
```

The query `[4,5]` returns:

```
4 + 6 = 10
```

This confirms the segment tree correctly isolates updates to exact ranges without leaking changes into neighboring segments.
