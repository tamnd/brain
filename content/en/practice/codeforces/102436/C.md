---
title: "CF 102436C - Painting Plan"
description: "We have (n) segments on a number line. The original endpoints have been lost as pairs. We only know all (2n) endpoint coordinates, sorted into an array (x1 < x2 < dots < x{2n}), and we know that the union of the original segments has total length exactly (k)."
date: "2026-08-09T00:10:50+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102436
codeforces_index: "C"
codeforces_contest_name: "Innopolis Open 2019-2020, qualification, contest 1"
rating: 0
weight: 102436
solve_time_s: 132
verified: true
draft: false
---

[CF 102436C - Painting Plan](https://codeforces.com/problemset/problem/102436/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

We have (n) segments on a number line. The original endpoints have been lost as pairs. We only know all (2n) endpoint coordinates, sorted into an array (x_1 < x_2 < \dots < x_{2n}), and we know that the union of the original segments has total length exactly (k).

We must reconstruct any pairing of the (2n) coordinates into (n) segments whose union has length (k). The output uses indices of the sorted endpoint array, not the coordinates themselves. If no pairing produces the required union length, we print `No`. Otherwise we print `Yes` followed by the (n) pairs of indices. The original statement guarantees that all coordinates are distinct.

The constraints are the key to the intended solution. There can be as many as 7000 segments, so there are 14000 endpoints. The target union length (k) is at most 30000. A DP whose state only depends on the current position and a length up to (k) is plausible, while anything exponential in (n) is immediately impossible. The intended solution uses the structure of the sorted endpoints to turn the reconstruction into a knapsack-style DP, and the large state dimension is handled with bitsets.

The first edge case is a target smaller than the minimum possible union. For example,

```
2 1
0 1 2 3
```

The four endpoints can be paired as ([0,1]) and ([2,3]), giving union length (2). Every other pairing produces a union of length at least (2), so the correct output is `No`. A careless implementation that only checks whether (k) can be formed as an arbitrary difference between coordinates might incorrectly accept it.

The second edge case is exactly the minimum union length. For

```
2 2
0 1 2 3
```

the adjacent pairing ([0,1]), ([2,3]) gives union length (2), so the answer is `Yes`. A solution that assumes some intervals must intersect can miss this completely disjoint configuration.

The third edge case is a completely nested configuration. For

```
2 3
0 1 2 3
```

the segments ([0,3]) and ([1,2]) have union length (3). The endpoints must be paired as ((1,4)) and ((2,3)). Pairing adjacent endpoints gives length (2), so merely taking the minimum pairing is not enough.

The fourth edge case is (k=0). Since all coordinates are distinct, every segment has positive length, so the union of even one segment has positive length. Thus

```
1 0
0 1
```

must produce `No`. An implementation that treats zero as the empty DP state without checking that every endpoint must eventually be used would get this wrong.

## Approaches

The most direct brute-force approach is to try every possible pairing of the (2n) endpoints. There are ((2n-1)!!) different pairings. For each pairing, we could sort the resulting intervals by their left endpoint and calculate the length of their union in (O(n)). The total work is thus (O(n(2n-1)!!)). Even (n=20) is already far beyond practical limits, while the actual constraint is (n=7000). The brute force is correct because it literally checks every possible reconstruction, but its search space grows much too quickly.

There is a much stronger way to look at the sorted endpoints.

Suppose we temporarily pair every adjacent pair:

[
(x_1,x_2),(x_3,x_4),\ldots,(x_{2n-1},x_{2n}).
]

These intervals are disjoint and give the smallest possible union for these endpoints. Call their lengths

[
a_i=x_{2i+2}-x_{2i+1}
]

using zero-based indexing.

Now consider two consecutive pairs. Instead of keeping

[
(x_{2i},x_{2i+1}),\quad(x_{2i+2},x_{2i+3}),
]

we can merge their union into one connected component by pairing the four endpoints in nested order:

[
(x_{2i},x_{2i+3}),\quad(x_{2i+1},x_{2i+2}).
]

The union is then simply the interval from the first endpoint to the last endpoint. The extra amount contributed when the next pair is absorbed is

[
b_i=x_{2i+1}-x_{2i-1}
]

for (i>0).

This gives a particularly convenient representation. Every connected component of the final union contains a consecutive block of endpoint coordinates. Since each endpoint is used exactly once, a component containing (2m) endpoints can be represented by nesting those endpoints. Consequently, the whole reconstruction can be viewed as partitioning the (n) adjacent endpoint pairs into consecutive blocks.

For a block covering pair indices (l) through (r), its union is

[
[x_{2l},x_{2r+1}],
]

whose length is

a_l+b_{l+1}+b_{l+2}+\cdots+b_r.
]

So while scanning the pair indices from left to right, there are exactly two choices. We can start a new component, paying (a_i), or extend the current component, paying (b_i).

This is now a 0/1 knapsack-style problem. At position (i), the DP records which total lengths are reachable. The target capacity is (k), which is at most 30000. The published solution uses a C++ bitset for exactly this reason.

The final difficulty is reconstruction. A normal boolean DP would need to remember a predecessor for every pair of position and length, which is (O(nk)) memory. Instead, we keep one bitset for every position saying which reachable states used the `extend` transition. In Python, an arbitrary-precision integer acts as a compact bitset, so one integer can represent all (k+1) states at once.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n(2n-1)!!)) | (O(n)) | Too slow |
| Ordinary DP | (O(nk)) | (O(nk)) for reconstruction | Too slow in Python, memory-heavy |
| Bitset DP | (O(nk/W)) word operations | (O(nk/W)) for reconstruction | Accepted |

Here (W) is the number of bits processed by one machine-word-level bitset operation. In Python, the same idea is implemented by arbitrary-precision integers, whose shifts and bitwise operations process many DP states simultaneously.

## Algorithm Walkthrough

1. Compute the length (a_i=x_{2i+1}-x_{2i}) of the basic adjacent pair at position (i). Also compute (b_i=x_{2i+1}-x_{2i-1}) for every (i>0). Starting a component at (i) costs (a_i), while extending the component through (i) costs (b_i).
2. Represent the reachable DP states as one integer `dp`. Bit (s) is set exactly when total union length (s) can be obtained after processing the current prefix. Initially only length zero is reachable, so `dp = 1`.
3. At position (i), shifting `dp` left by (a_i) represents starting a new component at (i). Shifting it left by (b_i) represents extending the component from the previous pair into (i). The union of these two bitsets gives the new reachable states.
4. Store which newly reachable states came from the `b_i` transition. If both transitions can reach the same state, prefer the `a_i` transition. This arbitrary tie-breaking is useful because it means one stored bit is enough to identify the predecessor during reconstruction.
5. After all (n) positions have been processed, inspect bit (k). If it is not set, no valid partition of the endpoint sequence exists, so print `No`.
6. If bit (k) is set, walk backwards through the DP. At position (i), check whether the stored `b_i` bit is set for the current target length. If it is, the current component was extended, so subtract (b_i). Otherwise it was started here, so subtract (a_i).
7. The recovered choices divide the (n) adjacent endpoint pairs into consecutive blocks. For every block ([l,r]), pair its endpoints in nested order. The outermost segment uses positions (2l) and (2r+1), the next uses (2l+1) and (2r), and so on.
8. Convert the zero-based endpoint positions into the required one-based indices and print the resulting (n) segments.

### Why it works

The central invariant is that every possible union of the original segments can be represented using consecutive connected components of the sorted endpoint sequence. Within one component, nesting the endpoints produces exactly that component's interval, while different components remain disjoint. Thus a valid reconstruction is equivalent to partitioning the (n) adjacent endpoint pairs into consecutive blocks.

For a block starting at (l) and ending at (r), its union length is exactly (a_l+\sum_{i=l+1}^{r}b_i). The DP considers precisely the two possibilities at every position: starting a new block or extending the previous block. Hence every DP path corresponds to a valid block partition, and every valid block partition corresponds to a DP path. If bit (k) is reachable, the reconstructed choices produce a union of exactly (k); if it is unreachable, no valid reconstruction exists.

## Python Solution

```python
import sys

input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    x = list(map(int, input().split()))

    # a[i] is the length of the basic adjacent pair.
    a = [x[2 * i + 1] - x[2 * i] for i in range(n)]

    # b[i] is the cost of extending the current component
    # from pair i-1 through pair i.
    b = [0] * n
    for i in range(1, n):
        b[i] = x[2 * i + 1] - x[2 * i - 1]

    # Bit s of dp means that total length s is reachable.
    dp = 1

    # For each i, bit s of extend[i] means that state s
    # was reached by taking the b[i] transition.
    extend = [0] * n

    mask = (1 << (k + 1)) - 1

    for i in range(n):
        from_start = dp << a[i]

        if i == 0:
            from_extend = 0
            chosen_extend = 0
        else:
            from_extend = dp << b[i]

            # If both transitions reach the same state, prefer
            # starting a new component.
            chosen_extend = from_extend & ~from_start

        dp = (from_start | from_extend) & mask
        extend[i] = chosen_extend & mask

    if not ((dp >> k) & 1):
        print("No")
        return

    # Reconstruct whether each position extends the previous block.
    used_extend = [False] * n
    cur = k

    for i in range(n - 1, -1, -1):
        if i > 0 and ((extend[i] >> cur) & 1):
            used_extend[i] = True
            cur -= b[i]
        else:
            cur -= a[i]

    # Convert the sequence of choices into consecutive blocks.
    blocks = []
    start = 0

    for i in range(1, n):
        if not used_extend[i]:
            blocks.append((start, i - 1))
            start = i

    blocks.append((start, n - 1))

    # Construct nested pairs inside every block.
    answer = []

    for l, r in blocks:
        while l <= r:
            # Zero-based endpoint positions:
            # 2*l and 2*r+1.
            answer.append((2 * l + 1, 2 * r + 2))
            l += 1
            r -= 1

    print("Yes")
    for u, v in answer:
        print(u, v)

if __name__ == "__main__":
    solve()
```

The first part constructs `a` and `b`. The value `a[i]` is the cost of making pair (i) a separate connected component. The value `b[i]` is the cost of attaching pair (i) to the component immediately before it.

The expression `dp << a[i]` shifts every reachable total by the cost of starting a component. Likewise, `dp << b[i]` represents extending the current component. Because all costs are positive, states larger than (k) can never become useful later, so the mask safely discards them.

The expression `from_extend & ~from_start` records only states for which extension is a valid predecessor but starting a new component is not. This is enough for reconstruction because when both choices are possible, the implementation deliberately chooses the start transition.

The backwards reconstruction subtracts exactly the transition that created the current state. The value `cur` consequently moves through valid predecessor states until it reaches zero.

The block construction uses zero-based endpoint positions internally. For a block from pair (l) to pair (r), the outermost segment connects endpoint positions (2l) and (2r+1). Adding one to both positions gives the required one-based indices. Moving inward produces all remaining nested segments.

No integer overflow is possible in Python. In C++, the original constraints also fit comfortably in ordinary 32-bit integers for the coordinates and target length. The Python implementation's main memory cost is the `extend` array, containing (n) arbitrary-precision bitsets of at most (k+1) bits.

## Worked Examples

### Sample 1

The input is

```
4 9
0 1 3 5 8 9 10 12
```

The adjacent pair lengths are

[
a=[1,2,1,2],
]

and the extension costs are

[
b=[0,4,4,3].
]

The DP evolves as follows.

| Position | Start cost (a_i) | Extend cost (b_i) | Reachable totals after position |
| --- | --- | --- | --- |
| 0 | 1 | unavailable | {1} |
| 1 | 2 | 4 | {3, 5} |
| 2 | 1 | 4 | {4, 6, 7, 9} |
| 3 | 2 | 3 | {6, 7, 8, 9, 10, 11, 12} |

The target (9) is reachable. One valid reconstruction is `start, start, extend, start`, giving blocks ([0,0]), ([1,2]), and ([3,3]).

The corresponding nested block ([1,2]) uses endpoint indices (3,6) and (4,5). Thus one valid answer is

```
Yes
1 2
3 6
4 5
7 8
```

These represent the intervals ([0,1]), ([3,9]), ([5,8]), and ([10,12]), whose union has length (9). The official sample uses another valid ordering of the same segments.

The trace demonstrates the key invariant: choosing `extend` joins neighboring basic pairs into one connected component, while choosing `start` closes the previous component and begins another.

### Sample 2

The input is

```
3 2
1 2 3 4 5 6
```

Here

[
a=[1,1,1]
]

and

[
b=[0,2,2].
]

The DP evolves as follows.

| Position | Start cost (a_i) | Extend cost (b_i) | Reachable totals after position |
| --- | --- | --- | --- |
| 0 | 1 | unavailable | {1} |
| 1 | 1 | 2 | {2, 3} |
| 2 | 1 | 2 | {3, 4} |

The target (2) disappears after the second transition and is not reachable after all three pairs are processed. The correct output is therefore

```
No
```

This example shows why checking only the minimum possible union is insufficient. The minimum is (3) for three disjoint adjacent segments, while some intermediate totals may be impossible.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(nk/W)) bit operations | Each of the (n) positions performs a constant number of shifts and bitwise operations on (k+1) bits. |
| Space | (O(nk/W)) | One bitset is stored for every position to reconstruct the chosen transitions. |

Here (n\le7000) and (k\le30000), so each stored bitset contains only about 30001 bits, roughly 3.75 KB before Python integer overhead. The entire predecessor history is on the order of a few tens of megabytes, comfortably below the 512 MB memory limit. The bit-parallel DP avoids the roughly (7000\times30000) individual Python-level state updates that an ordinary nested-loop DP would require. The constraints and limits are given in the original statement.

## Test Cases

The test harness below checks the official samples and several structural cases. Since the answer is constructive, it does not compare the exact segment list. Instead, it verifies that the program prints the correct `Yes` or `No`, uses every endpoint exactly once, keeps every segment oriented from left to right, and produces the requested union length.

```python
import sys
import io

def solve_instance(n, k, x):
    a = [x[2 * i + 1] - x[2 * i] for i in range(n)]

    b = [0] * n
    for i in range(1, n):
        b[i] = x[2 * i + 1] - x[2 * i - 1]

    dp = 1
    extend = [0] * n
    mask = (1 << (k + 1)) - 1

    for i in range(n):
        from_start = dp << a[i]

        if i == 0:
            from_extend = 0
            chosen_extend = 0
        else:
            from_extend = dp << b[i]
            chosen_extend = from_extend & ~from_start

        dp = (from_start | from_extend) & mask
        extend[i] = chosen_extend & mask

    if not ((dp >> k) & 1):
        return "No\n"

    used_extend = [False] * n
    cur = k

    for i in range(n - 1, -1, -1):
        if i > 0 and ((extend[i] >> cur) & 1):
            used_extend[i] = True
            cur -= b[i]
        else:
            cur -= a[i]

    blocks = []
    start = 0

    for i in range(1, n):
        if not used_extend[i]:
            blocks.append((start, i - 1))
            start = i

    blocks.append((start, n - 1))

    answer = []

    for l, r in blocks:
        while l <= r:
            answer.append((2 * l + 1, 2 * r + 2))
            l += 1
            r -= 1

    out = ["Yes"]
    out.extend(f"{u} {v}" for u, v in answer)
    return "\n".join(out) + "\n"

def run(inp: str) -> str:
    data = list(map(int, inp.split()))
    n, k = data[0], data[1]
    x = data[2:2 + 2 * n]
    return solve_instance(n, k, x)

def verify(inp: str, out: str):
    data = list(map(int, inp.split()))
    n, k = data[0], data[1]
    x = data[2:2 + 2 * n]

    lines = out.strip().splitlines()

    if lines[0] == "No":
        return

    assert lines[0] == "Yes"
    assert len(lines) == n + 1

    used = [False] * (2 * n)
    intervals = []

    for line in lines[1:]:
        u, v = map(int, line.split())
        assert 1 <= u <= 2 * n
        assert 1 <= v <= 2 * n
        assert u < v

        u -= 1
        v -= 1

        assert not used[u]
        assert not used[v]

        used[u] = True
        used[v] = True
        intervals.append((x[u], x[v]))

    assert all(used)

    intervals.sort()

    total = 0
    left, right = intervals[0]

    for l, r in intervals[1:]:
        if l > right:
            total += right - left
            left, right = l, r
        else:
            right = max(right, r)

    total += right - left

    assert total == k

# Official sample 1
sample1 = """\
4 9
0 1 3 5 8 9 10 12
"""
out = run(sample1)
verify(sample1, out)
assert out.splitlines()[0] == "Yes"

# Official sample 2
sample2 = """\
3 2
1 2 3 4 5 6
"""
out = run(sample2)
assert out.strip() == "No"

# Minimum-size input
case_min = """\
1 4
0 4
"""
out = run(case_min)
verify(case_min, out)
assert out.splitlines()[0] == "Yes"

# Minimum possible union, all adjacent gaps equal
case_equal = """\
4 4
0 1 2 3 4 5 6 7
"""
out = run(case_equal)
verify(case_equal, out)
assert out.splitlines()[0] == "Yes"

# Nested configuration, catches block construction
case_nested = """\
2 3
0 1 2 3
"""
out = run(case_nested)
verify(case_nested, out)
assert out.splitlines()[0] == "Yes"

# Impossible value below the minimum
case_too_small = """\
2 1
0 1 2 3
"""
out = run(case_too_small)
assert out.strip() == "No"

# Maximum-size input from the official constraints
n = 7000
x = list(range(2 * n))
case_max = f"{n} {n}\n" + " ".join(map(str, x)) + "\n"
out = run(case_max)
verify(case_max, out)
assert out.splitlines()[0] == "Yes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 4 / 0 4` | `Yes` | Minimum (n), single segment |
| `4 4 / 0 1 2 3 4 5 6 7` | `Yes` | Equal adjacent gaps and minimum union |
| `2 3 / 0 1 2 3` | `Yes` | Nested component construction |
| `2 1 / 0 1 2 3` | `No` | Target below the minimum possible union |
| `7000 7000 / 0 1 ... 13999` | `Yes` | Maximum (n), maximum number of DP positions |

## Edge Cases

For a target smaller than the minimum union, the DP naturally rejects the instance. Consider

```
2 1
0 1 2 3
```

The basic adjacent costs are (a=[1,1]), while the extension cost is (b_1=2). The only reachable totals are (1), (2), and (3), so bit (1) is not set after processing both pairs. The algorithm prints `No`.

For a target exactly equal to the minimum union, consider

```
2 2
0 1 2 3
```

The DP can choose `start` twice, giving (a_0+a_1=1+1=2). The reconstructed blocks are ([0,0]) and ([1,1]), producing segments with indices `(1,2)` and `(3,4)`. Their union has length (2).

For a nested configuration, consider

```
2 3
0 1 2 3
```

The DP can choose `start` for the first pair and `extend` for the second pair. The cost becomes

[
a_0+b_1=1+2=3.
]

The resulting block is ([0,1]). Its nested construction produces `(1,4)` and `(2,3)`, corresponding to ([0,3]) and ([1,2]). Their union is exactly ([0,3]), of length (3).

For (k=0), consider

```
1 0
0 1
```

The only available transition costs (1), so the only reachable state is length (1), not length (0) after all endpoints have been processed. The algorithm consequently prints `No`. The fact that the initial DP state contains zero does not mean the empty construction is a valid answer, because every endpoint must be used in exactly one segment.

Finally, the maximum-size case stresses the reason for using bitsets. With (n=7000), an ordinary Python loop would examine up to (7000\cdot30001), or about 210 million, DP states. The bitset representation processes all possible lengths simultaneously using integer shifts and bitwise operations, which is the central optimization that makes the full constraint practical. The original problem sets exactly these maximum values for (n) and (k).

If you want, I can also turn this into a more compact Codeforces-style editorial, or provide a C++17 version matching the official bitset solution more closely.
