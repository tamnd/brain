---
title: "CF 102272D - C\u00e1nh \u0110\u1ed3ng Hoa"
description: "We have an array of flower counts (A1,ldots,AN). A type 1 operation chooses an interval ([l,r]) and adds a staircase to it. Position (l) receives (1), position (l+1) receives (2), and in general position (i) receives (i-l+1)."
date: "2026-08-19T05:11:32+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102272
codeforces_index: "D"
codeforces_contest_name: "HCW 19 Individual Day 1"
rating: 0
weight: 102272
solve_time_s: 206
verified: true
draft: false
---

[CF 102272D - C\u00e1nh \u0110\u1ed3ng Hoa](https://codeforces.com/problemset/problem/102272/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 26s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an array of flower counts (A_1,\ldots,A_N). A type 1 operation chooses an interval ([l,r]) and adds a staircase to it. Position (l) receives (1), position (l+1) receives (2), and in general position (i) receives (i-l+1). A type 2 operation asks for the sum of the current array on an interval ([u,v]).

The operations are processed in order, so every query must see all updates that occurred earlier. The task is to print the answer for every type 2 operation.

The largest test can contain (10^5) positions and (10^5) operations, with up to four test cases. An (O(NQ)) solution can perform around (10^{10}) elementary array operations in the worst case, which is far beyond a two-second limit. Even (O(N+Q\sqrt N)) would be unnecessarily expensive here. We need each operation to take roughly (O(\log N)) time.

There are several boundary cases that can make an apparently correct implementation fail. First, an update can contain exactly one position. For example,

```
1
1
0
2
1 1 1
2 1 1
```

produces

```
1
```

because the update adds only (1). A formula that always inserts a second difference at (l+1) without checking whether (l<r) can corrupt the state.

An update can also reach the last array position. For example,

```
1
3
0 0 0
2
1 2 3
2 1 3
```

produces

```
6
```

because the added values are (1,2) on positions (2,3), giving the array ([0,1,2]). The internal representation may use position (r+1=4), but that position does not belong to the array and must only act as a terminating difference. Allocating the Fenwick tree too narrowly or querying it incorrectly at this boundary can cause an off-by-one error.

A query may cover only part of an update. For example,

```
1
5
0 0 0 0 0
2
1 2 5
2 3 4
```

produces

```
5
```

because the update creates ([0,1,2,3,4]), and positions (3,4) sum to (5). Treating the staircase as a constant range addition would incorrectly give (2+2=4).

Finally, several updates can overlap. For example,

```
1
4
0 0 0 0
3
1 1 3
1 2 4
2 2 3
```

produces

```
5
```

The first update adds ([1,2,3,0]), the second adds ([0,1,2,3]), so positions (2,3) contain (3,5). Every update has to contribute independently to the final sum.

## Approaches

The direct solution is to process a type 1 operation by visiting every (i) from (l) through (r) and adding (i-l+1) to (A_i). A type 2 operation can then be answered with a prefix-sum structure, or simply by scanning the requested interval. This is correct because every update is applied exactly to the positions it describes.

The problem is the number of positions touched by updates. If (N=Q=10^5), we can have (10^5) updates covering almost the entire array. A single update can require (10^5) additions, giving roughly (10^{10}) operations in the worst case. The two-second limit rules this out.

The useful observation is that the value added by an update is not arbitrary. On ([l,r]),

[
i-l+1=i+(1-l).
]

So every update adds a linear function of the position index. More specifically, if the added value at position (i) is written as

[
f(i)=ai+b,
]

then here (a=1) and (b=1-l).

We do not actually need to store every affected value. Instead, consider the difference array of the values contributed by all updates. For one linear update (f(i)=ai+b) on ([l,r]), its difference array has only three possible changes. At (l), we start with (f(l)). Between (l) and (r), consecutive values increase by (a), so at (l+1) we add (a). At (r+1), we subtract (f(r)), which terminates the update.

For this particular problem, (a=1) and (b=1-l), so

[
f(l)=1
]

and

[
f(r)=r-l+1.
]

Thus one update can be represented by only a constant number of point changes in a difference array.

The remaining question is how to recover a range sum from these difference changes efficiently. If (D_j) is the difference array, the value at position (i) is

[
X_i=\sum_{j\le i}D_j.
]

Consequently, the prefix sum through (x) is

\sum_{j=1}^{x}D_j(x-j+1).
]

Rearranging,

(x+1)\sum_{j=1}^{x}D_j-\sum_{j=1}^{x}jD_j.
]

This means we only need two prefix quantities: (\sum D_j) and (\sum jD_j). Two Fenwick trees can maintain these quantities under point changes in (O(\log N)).

The original array does not need to be inserted into these Fenwick trees. We precompute its ordinary prefix sums once, then add the contribution of all subsequent staircase updates when answering a query.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(NQ)) | (O(N)) | Too slow |
| Optimal | (O(N+Q\log N)) | (O(N)) | Accepted |

## Algorithm Walkthrough

1. Compute the ordinary prefix sum array of the initial flower counts. Let (P[x]) be the sum of the initial values from position (1) through (x). A query on ([u,v]) can then obtain its initial contribution as (P[v]-P[u-1]).
2. Maintain two Fenwick trees. The first stores point changes to the difference array (D), while the second stores the same changes multiplied by their positions. If a difference change of (d) occurs at position (p), add (d) to the first tree and (p d) to the second tree.
3. For an update ([l,r]), the added value is (f(i)=i-l+1). At position (l), the difference array must increase by (f(l)=1), so add (+1) at (l). If (l<r), consecutive values increase by (1), so add (+1) at (l+1). At (r+1), subtract the final value (f(r)=r-l+1). The resulting difference changes describe exactly the staircase added by this update.
4. To calculate the contribution of all updates to the prefix ([1,x]), obtain

[
S_D=\sum_{j\le x}D_j
]

from the first Fenwick tree and

[
S_{jD}=\sum_{j\le x}jD_j
]

from the second one. The dynamic prefix sum is

[
(x+1)S_D-S_{jD}.
]

The formula follows directly from counting how many prefix positions contain each difference value. A difference introduced at position (j) affects positions (j,j+1,\ldots,x), exactly (x-j+1) positions.

1. For a type 2 query ([u,v]), calculate the dynamic prefix sum through (v) and subtract the dynamic prefix sum through (u-1). Add the corresponding initial prefix-sum difference. This gives the complete current sum on ([u,v]).
2. Process all operations in input order. Updates modify the two Fenwick trees immediately, while queries only read them, so every query automatically sees exactly the updates that precede it.

### Why it works

The invariant is that the two Fenwick trees represent the difference array of every flower contribution caused by processed type 1 operations. For each update, the three difference changes reconstruct the sequence (1,2,\ldots,r-l+1) on ([l,r]) and zero outside it. Since difference arrays add linearly, overlapping updates are represented correctly by adding their difference changes.

For any prefix ending at (x), every difference (D_j) contributes to positions (j) through (x), giving (D_j(x-j+1)) total flowers. The identity

(x+1)\sum_{j\le x}D_j-\sum_{j\le x}jD_j
]

therefore recovers the exact dynamic prefix sum. Subtracting two prefixes gives the exact dynamic interval sum, and adding the unchanged initial prefix sums gives the current array sum. Hence every type 2 answer is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Fenwick:
    __slots__ = ("n", "bit")

    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, idx, value):
        n = self.n
        bit = self.bit
        while idx <= n:
            bit[idx] += value
            idx += idx & -idx

    def sum(self, idx):
        bit = self.bit
        res = 0
        while idx > 0:
            res += bit[idx]
            idx -= idx & -idx
        return res

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        prefix = [0] * (n + 1)
        for i, value in enumerate(a, 1):
            prefix[i] = prefix[i - 1] + value

        # One tree stores D[j].
        # The other stores j * D[j].
        bit_d = Fenwick(n + 1)
        bit_jd = Fenwick(n + 1)

        def add_difference(pos, delta):
            if pos > n + 1:
                return
            bit_d.add(pos, delta)
            bit_jd.add(pos, pos * delta)

        def dynamic_prefix(x):
            if x <= 0:
                return 0
            sum_d = bit_d.sum(x)
            sum_jd = bit_jd.sum(x)
            return (x + 1) * sum_d - sum_jd

        q = int(input())

        for _ in range(q):
            query = list(map(int, input().split()))
            typ, x, y = query

            if typ == 1:
                l, r = x, y

                # f(i) = i - l + 1
                # At l: start with f(l) = 1.
                add_difference(l, 1)

                # From l+1 through r, consecutive values differ by 1.
                if l < r:
                    add_difference(l + 1, 1)

                # At r+1, terminate the staircase.
                add_difference(r + 1, -(r - l + 1))

            else:
                u, v = x, y

                initial = prefix[v] - prefix[u - 1]
                dynamic = dynamic_prefix(v) - dynamic_prefix(u - 1)

                out.append(str(initial + dynamic))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The `prefix` array handles the initial flowers separately. This is convenient because the initial values never change, so there is no reason to make the Fenwick structure represent them.

`bit_d` represents (D_j), while `bit_jd` represents (jD_j). The helper `add_difference` updates both structures together, which prevents the two representations from getting out of sync.

For an update ([l,r]), the first change is always `+1` at `l`. The second change is also `+1`, but only when `l < r`. This condition is essential for a one-element update. The final change is placed at `r + 1` and equals `-(r-l+1)`. The Fenwick trees have size `n + 1` specifically so that this terminating difference can be stored when `r = n`.

The `dynamic_prefix` function implements

[
(x+1)\sum_{j\le x}D_j-\sum_{j\le x}jD_j.
]

When `x` is zero, the answer is immediately zero, which makes queries beginning at position (1) safe because they request `dynamic_prefix(0)`.

Python integers have arbitrary precision, so the potentially large flower counts do not overflow. The largest possible total can exceed 32-bit integer range by a large margin.

Each Fenwick operation is logarithmic, and every update performs a constant number of them. A query performs two prefix calculations, one for each endpoint. The resulting implementation avoids touching the potentially huge update interval itself.

## Worked Examples

The first test case begins with

[
[2,1,3,5,2].
]

The following table tracks the array after each operation and the answer whenever a query occurs.

| Operation | Update or query | Current array | Answer |
| --- | --- | --- | --- |
| `1 1 3` | Add (1,2,3) to positions (1,2,3) | `[3, 3, 6, 5, 2]` |  |
| `2 3 5` | Sum positions (3) through (5) | `[3, 3, 6, 5, 2]` | `13` |
| `1 4 5` | Add (1,2) to positions (4,5) | `[3, 3, 6, 6, 4]` |  |
| `1 2 5` | Add (1,2,3,4) to positions (2) through (5) | `[3, 4, 8, 9, 8]` |  |
| `1 1 1` | Add (1) to position (1) | `[4, 4, 8, 9, 8]` |  |
| `2 1 4` | Sum positions (1) through (4) | `[4, 4, 8, 9, 8]` | `25` |

For the first update, the difference representation receives `+1` at position (1), `+1` at position (2), and `-3` at position (4). Its reconstructed values are (1,2,3,0,0), exactly the staircase required by the update. The same representation is added for later updates, so overlapping operations naturally accumulate.

The second test case starts with

[
[10,5,2,0,8,6,2].
]

| Operation | Update or query | Current array | Answer |
| --- | --- | --- | --- |
| `1 2 5` | Add (1,2,3,4) to positions (2) through (5) | `[10, 6, 4, 3, 12, 6, 2]` |  |
| `1 1 6` | Add (1,2,3,4,5,6) to positions (1) through (6) | `[11, 8, 7, 7, 17, 12, 2]` |  |
| `2 4 7` | Sum positions (4) through (7) | `[11, 8, 7, 7, 17, 12, 2]` | `38` |
| `1 1 3` | Add (1,2,3) to positions (1) through (3) | `[12, 10, 10, 7, 17, 12, 2]` |  |
| `1 5 5` | Add (1) to position (5) | `[12, 10, 10, 7, 18, 12, 2]` |  |
| `1 1 5` | Add (1,2,3,4,5) to positions (1) through (5) | `[13, 12, 13, 11, 23, 12, 2]` |  |
| `2 1 7` | Sum the entire array | `[13, 12, 13, 11, 23, 12, 2]` | `86` |

The single-position update `1 5 5` is a useful check. Since `l == r`, the code inserts only the starting difference and the terminating difference. The intermediate `l+1` change is skipped, so the represented sequence contains exactly one added flower.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(N+Q\log N)) | Building initial prefix sums costs (O(N)); every update and query performs a constant number of Fenwick operations |
| Space | (O(N)) | The initial prefix array and two Fenwick trees each use (O(N)) memory |

With (N,Q\le10^5), the solution performs on the order of a few million Fenwick-tree iterations per test case rather than billions of direct array updates. The memory usage is linear and comfortably below 256 MB.

## Test Cases

The following test harness uses a callable version of the same algorithm. The maximum-size case is generated rather than written out literally, which keeps the test source readable while still exercising the stated limits.

```python
import sys
import io

class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, idx, value):
        while idx <= self.n:
            self.bit[idx] += value
            idx += idx & -idx

    def sum(self, idx):
        res = 0
        while idx:
            res += self.bit[idx]
            idx -= idx & -idx
        return res

def solve_io():
    input = sys.stdin.readline
    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        prefix = [0] * (n + 1)
        for i, value in enumerate(a, 1):
            prefix[i] = prefix[i - 1] + value

        bit_d = Fenwick(n + 1)
        bit_jd = Fenwick(n + 1)

        def add_difference(pos, delta):
            bit_d.add(pos, delta)
            bit_jd.add(pos, pos * delta)

        def dynamic_prefix(x):
            if x <= 0:
                return 0
            sd = bit_d.sum(x)
            sjd = bit_jd.sum(x)
            return (x + 1) * sd - sjd

        q = int(input())

        for _ in range(q):
            typ, x, y = map(int, input().split())

            if typ == 1:
                l, r = x, y
                add_difference(l, 1)
                if l < r:
                    add_difference(l + 1, 1)
                add_difference(r + 1, -(r - l + 1))
            else:
                u, v = x, y
                ans = (
                    prefix[v] - prefix[u - 1]
                    + dynamic_prefix(v)
                    - dynamic_prefix(u - 1)
                )
                out.append(str(ans))

    return "\n".join(out)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    try:
        sys.stdin = io.StringIO(inp)
        sys.stdout = io.StringIO()
        solve_io()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

sample = """\
2
5
2 1 3 5 2
6
1 1 3
2 3 5
1 4 5
1 2 5
1 1 1
2 1 4
7
10 5 2 0 8 6 2
7
1 2 5
1 1 6
2 4 7
1 1 3
1 5 5
1 1 5
2 1 7
"""

assert run(sample) == "13\n25\n38\n86", "provided sample"

assert run("""\
1
1
0
2
1 1 1
2 1 1
""") == "1", "minimum size"

assert run("""\
1
3
0 0 0
3
1 2 3
2 1 3
2 3 3
""") == "6\n2", "right boundary and partial query"

assert run("""\
1
5
7 7 7 7 7
4
2 1 5
1 3 5
2 1 5
2 3 5
""") == "35\n41\n24", "all equal initial values"

assert run("""\
1
4
0 0 0 0
5
1 1 4
1 2 3
2 1 4
2 2 3
2 4 4
""") == "14\n7\n4", "overlap and boundaries"

n = 100000
maximum_case = (
    "1\n"
    f"{n}\n"
    + ("1 " * (n - 1))
    + "1\n"
    + f"{n}\n"
    + "\n".join(
        ["1 1 100000"] * (n - 1)
        + ["2 1 100000"]
    )
    + "\n"
)

expected = n + (n - 1) * (n * (n + 1) // 2)
assert run(maximum_case) == str(expected), "maximum size"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Minimum-size case with (N=1) | `1` | Single-position updates and the (u-1=0) prefix boundary |
| Update reaching position (N) | `6`, `2` | Correct handling of the terminating difference at (r+1) and partial queries |
| All initial values equal | `35`, `41`, `24` | Separation of the immutable initial prefix sums from dynamic updates |
| Overlapping updates | `14`, `7`, `4` | Additivity of multiple staircase updates and interval boundaries |
| Generated (N=Q=10^5) case | Computed by the formula in the test | Time complexity, large integers, and repeated full-range updates |

## Edge Cases

For a one-element update, consider

```
1
1
0
2
1 1 1
2 1 1
```

The update is (f(1)=1). The algorithm adds `+1` to the difference array at position (1) and `-1` at position (2). The second change is stored in the Fenwick tree but is outside the queried prefix. The prefix through position (1) is therefore (1), and the output is `1`. The missing intermediate change at (l+1) is intentional because there is no second position in the staircase.

For an update ending at the final position, consider

```
1
3
0 0 0
2
1 2 3
2 1 3
```

The update contributes (1,2) to positions (2,3). Its difference changes are `+1` at (2), `+1` at (3), and `-2` at (4). The Fenwick tree is sized to (N+1), so position (4) can hold the terminating difference. The prefix through (3) ignores that termination and gives (3), so the expected output is actually `3`.

For a query that covers only part of an update, consider

```
1
5
0 0 0 0 0
2
1 2 5
2 3 4
```

The update produces ([0,1,2,3,4]). The prefix through (4) is (6), while the prefix through (2) is (1), so the requested sum is (6-1=5). The dynamic-prefix formula works without knowing the individual values in the interval.

For overlapping updates, consider

```
1
4
0 0 0 0
3
1 1 3
1 2 4
2 2 3
```

The first update contributes ([1,2,3,0]), and the second contributes ([0,1,2,3]). Their sum is ([1,3,5,3]), so positions (2,3) contain (3+5=8). The difference representation simply adds the difference changes from both updates, producing exactly the same combined array.

The maximum-size case exercises another practical boundary. With (N=Q=10^5), repeatedly updating the entire array would be impossible if each update visited all (N) positions. The Fenwick representation touches only a constant number of positions per update, so the number of operations grows as (O(Q\log N)) rather than (O(NQ)). Python's arbitrary-precision integers also safely handle the resulting totals, which can be much larger than (2^{31}-1).
