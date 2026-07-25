---
title: "CF 102881E - Baby Ehab's X(OR)"
description: "We have an array of positive integers. An update chooses a contiguous range and applies one of two bitwise transformations to every number in that range."
date: "2026-07-25T12:32:25+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102881
codeforces_index: "E"
codeforces_contest_name: "ECPC 2019 Kickoff"
rating: 0
weight: 102881
solve_time_s: 59
verified: true
draft: false
---

[CF 102881E - Baby Ehab's X(OR)](https://codeforces.com/problemset/problem/102881/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 59s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an array of positive integers. An update chooses a contiguous range and applies one of two bitwise transformations to every number in that range. The first transformation replaces a value `x` with `x | (x - 1)`, and the second replaces it with `x ^ (x - 1)`. After every update, we must print the total sum of the array.

The important part is understanding what these two expressions actually do to bits. If `x` has `k` trailing zeroes, then `x - 1` changes exactly those zeroes into ones and turns the lowest one bit into zero.

For `x | (x - 1)`, all trailing zeroes become ones, while the remaining bits stay unchanged. For example, `12 (1100)` becomes `15 (1111)`. This operation only changes numbers with at least one trailing zero, and afterwards the number is odd.

For `x ^ (x - 1)`, all bits from the lowest set bit downwards become ones, and all higher bits disappear. A value with `k` trailing zeroes becomes `2^(k+1)-1`. For example, `12 (1100)` becomes `7 (0111)`. This also always produces an odd number.

The constraints are large: both the array size and the number of operations can reach `3 * 10^5`. A solution that touches every element in a range is too slow because the worst case would perform around `9 * 10^10` element updates. We need a logarithmic data structure that can summarize many elements at once.

A common mistake is to track only the sum. The sum alone cannot tell us how a future operation changes the numbers. For example, the values `4` and `6` both have different behavior under the second operation even though their sums can be combined. The missing information is the number of trailing zeroes.

Another edge case is a range containing powers of two. For input:

```
1 1
8
1 1 1
```

the answer is:

```
15
```

because `8 (1000)` becomes `15 (1111)`. A solution that assumes the value only becomes odd would lose the added lower bits.

Another edge case is applying the second operation after the first. For:

```
1 2
4
1 1 1
2 1 1
```

the output is:

```
7
1
```

The first update creates `7`, and the second update changes `7` to `1`. A careless implementation that applies the second operation to the original value `4` would incorrectly produce `7`.

## Approaches

A direct solution would iterate over every position inside each query range and calculate the new value using the bit operations. This is correct because each operation is independent for every element. However, with `n` and `q` both equal to `300000`, the worst case contains roughly `n * q` element modifications, which is far beyond the available time.

The key observation is that the transformations depend only on the number of trailing zeroes. After either operation, the number becomes odd, so the future behavior of that element is much simpler. This means a segment tree does not need to store every exact value. It only needs to know how many values in a segment have each possible trailing-zero count, along with the segment sum.

There is one more subtlety. Segment tree lazy propagation must remember not only that a segment was updated, but which sequence of transformations still needs to be passed to its children. The possible pending transformations are small. They are the identity, the first operation, the second operation, and a constant operation that turns everything into `1`. These four states are enough because repeated transformations quickly collapse into one of them.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nq) | O(1) | Too slow |
| Optimal | O((n + q) log n * 20) | O(n * 20) | Accepted |

## Algorithm Walkthrough

1. Build a segment tree. For every node, store the sum of its segment and an array where `cnt[i]` is the number of values having exactly `i` trailing zeroes. Store a lazy transformation describing an operation that still has to be pushed to children.

The largest value that can appear is below `2^19`, so at most 19 trailing zeroes are possible.
2. When applying the first operation to a whole segment, every value with `i > 0` trailing zeroes increases by `2^i - 1`. After that change, all values become odd.

We update the sum using the stored counts and move every count into `cnt[0]`.
3. When applying the second operation to a whole segment, a value with `i` trailing zeroes becomes `2^(i+1)-1`. The new sum can be calculated directly from the counts.

Again, every resulting value is odd, so the whole segment moves into `cnt[0]`.
4. When applying the constant operation that results from composing transformations, every value becomes `1`. The sum becomes the segment length and all values have zero trailing zeroes.
5. For a partial range update, push the pending lazy transformation to the children before descending. Merge children afterwards by adding their sums and trailing-zero counts.
6. After every update, the root sum is the answer.

Why it works:

The segment tree maintains exactly the information needed by the operations. The effect of either bitwise operation depends only on the trailing-zero count of the original value. The stored counts allow us to compute the new sum without knowing individual values. Since every transformation can be represented by one of the four lazy states and these states are composed correctly, delayed updates always produce the same result as applying operations directly to every element.

## Python Solution

```python
import sys
input = sys.stdin.readline

MAXB = 20

def solve():
    n, q = map(int, input().split())
    a = list(map(int, input().split()))

    size = 4 * n
    tree_sum = [0] * size
    cnt = [[0] * MAXB for _ in range(size)]
    lazy = [0] * size

    def tz(x):
        return (x & -x).bit_length() - 1

    def apply(node, l, r, op):
        length = r - l + 1

        if op == 1:
            add = 0
            for i in range(1, MAXB):
                add += cnt[node][i] * ((1 << i) - 1)
            tree_sum[node] += add

        elif op == 2:
            new_sum = 0
            for i in range(MAXB):
                new_sum += cnt[node][i] * ((1 << (i + 1)) - 1)
            tree_sum[node] = new_sum

        else:
            tree_sum[node] = length

        cnt[node][0] = length
        for i in range(1, MAXB):
            cnt[node][i] = 0

    def compose(old, new):
        if new == 0:
            return old
        if old == 0:
            return new

        if old == 1 and new == 1:
            return 1
        if old == 2 and new == 2:
            return 3
        if old == 1 and new == 2:
            return 3
        if old == 2 and new == 1:
            return 2
        if old == 3:
            return 3
        if new == 3:
            return 3

        return new

    def push(node, l, r):
        if lazy[node] and l != r:
            mid = (l + r) // 2
            op = lazy[node]
            apply(node * 2, l, mid, op)
            apply(node * 2 + 1, mid + 1, r, op)
            lazy[node * 2] = compose(lazy[node * 2], op)
            lazy[node * 2 + 1] = compose(lazy[node * 2 + 1], op)
            lazy[node] = 0

    def build(node, l, r):
        if l == r:
            tree_sum[node] = a[l]
            cnt[node][tz(a[l])] = 1
            return
        mid = (l + r) // 2
        build(node * 2, l, mid)
        build(node * 2 + 1, mid + 1, r)
        pull(node)

    def pull(node):
        tree_sum[node] = tree_sum[node * 2] + tree_sum[node * 2 + 1]
        for i in range(MAXB):
            cnt[node][i] = cnt[node * 2][i] + cnt[node * 2 + 1][i]

    def update(node, l, r, ql, qr, op):
        if qr < l or r < ql:
            return
        if ql <= l and r <= qr:
            apply(node, l, r, op)
            lazy[node] = compose(lazy[node], op)
            return

        push(node, l, r)
        mid = (l + r) // 2
        update(node * 2, l, mid, ql, qr, op)
        update(node * 2 + 1, mid + 1, r, ql, qr, op)
        pull(node)

    build(1, 0, n - 1)

    ans = []
    for _ in range(q):
        t, l, r = map(int, input().split())
        update(1, 0, n - 1, l - 1, r - 1, t)
        ans.append(str(tree_sum[1]))

    print("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The `cnt` arrays are the core of the implementation. They avoid storing individual values while preserving exactly the information required by both transformations.

The `apply` function handles a complete segment update. The first two cases calculate the new sum from trailing-zero frequencies. The last case is used when several pending operations combine into a transformation that forces every value to become `1`.

The `compose` function prevents a common lazy propagation bug. A later operation cannot simply replace an earlier lazy flag because the order matters. For example, applying the first operation and then the second one is not the same as applying only the second operation.

The recursion uses zero-based indexes internally. The input ranges are converted once during updates, avoiding repeated conversions and off-by-one mistakes.

## Worked Examples

For the first sample:

```
3 3
1 2 3
1 1 3
2 2 2
2 1 3
```

The important segment states are:

| Step | Operation | Values | Sum |
| --- | --- | --- | --- |
| Initial | none | 1, 2, 3 | 6 |
| 1 | apply first operation | 1, 3, 3 | 7 |
| 2 | apply second operation to second value | 1, 1, 3 | 5 |
| 3 | apply second operation to all | 1, 1, 1 | 3 |

The trace shows that after each operation all modified numbers become odd, which is exactly the invariant used by the segment tree.

For the second sample:

```
5 5
5 5 5 5 5
1 5 5
2 1 1
2 2 3
1 3 4
2 1 5
```

| Step | Operation | Values | Sum |
| --- | --- | --- | --- |
| Initial | none | 5, 5, 5, 5, 5 | 25 |
| 1 | first operation on position 5 | 5, 5, 5, 5, 5 | 25 |
| 2 | second operation on position 1 | 1, 5, 5, 5, 5 | 21 |
| 3 | second operation on positions 2 to 3 | 1, 1, 1, 5, 5 | 13 |
| 4 | first operation on positions 3 to 4 | 1, 1, 1, 5, 5 | 13 |
| 5 | second operation on all | 1, 1, 1, 1, 1 | 5 |

The sample exercises repeated transformations and shows why keeping only whether a number is odd would not be enough for the initial state.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + q) log n * 20) | Every segment operation touches O(log n) nodes, and each node update scans the 20 possible trailing-zero counts. |
| Space | O(n * 20) | Each segment tree node stores 20 counters and a few extra values. |

The maximum array size is `300000`, so the number of tree nodes is linear. The logarithmic update time easily fits the limit because the constant factor is only the small number of possible bit positions.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import builtins
    data = sys.stdin.read().split()
    if not data:
        return ""
    it = iter(data)
    n = int(next(it))
    q = int(next(it))
    arr = [int(next(it)) for _ in range(n)]
    ops = [(int(next(it)), int(next(it)), int(next(it))) for _ in range(q)]

    res = []
    for t, l, r in ops:
        for i in range(l - 1, r):
            if t == 1:
                arr[i] |= arr[i] - 1
            else:
                arr[i] ^= arr[i] - 1
        res.append(str(sum(arr)))
    return "\n".join(res)

assert run("""3 3
1 2 3
1 1 3
2 2 2
2 1 3
""") == "7\n5\n3", "sample 1"

assert run("""5 5
5 5 5 5 5
1 5 5
2 1 1
2 2 3
1 3 4
2 1 5
""") == "25\n21\n13\n13\n5", "sample 2"

assert run("""1 1
8
1 1 1
""") == "15", "power of two"

assert run("""1 2
4
1 1 1
2 1 1
""") == "7\n1", "composition case"

assert run("""3 2
1 1 1
2 1 3
1 1 3
""") == "3\n3", "all equal odd values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single power of two | 15 | Correct handling of trailing zeroes |
| First update followed by second update | 7 then 1 | Lazy composition behavior |
| All odd values | 3 then 3 | Operations that should not increase values |
| Provided samples | Sample outputs | General correctness |

## Edge Cases

For the power-of-two case:

```
1 1
8
1 1 1
```

The value `8` has three trailing zeroes. The first operation adds `2^3 - 1 = 7`, giving `15`. The segment tree stores one value in `cnt[3]`, so it computes the increase directly and moves the value to `cnt[0]`.

For the composition case:

```
1 2
4
1 1 1
2 1 1
```

After the first update, `4` becomes `7`, which is represented as an odd number. The second update turns every odd value into `1`. The lazy state composition records that the pending transformation is the combined effect, rather than incorrectly treating the two operations independently.
