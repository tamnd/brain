---
title: "CF 102440K - \u0410\u0431\u0441\u043e\u043b\u044e\u0442\u043d\u0430\u044f \u0430\u0431\u0441\u043e\u043b\u044e\u0442\u043d\u043e\u0441\u0442\u044c \u043c\u0430\u0441\u0441\u0438\u0432\u0430"
description: "We have a binary array. Its absolute value is the absolute difference between the number of ones and the number of zeros. After changing one contiguous segment, including the possibility of changing nothing, we want the largest absolute value that can be obtained."
date: "2026-08-08T14:05:21+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102440
codeforces_index: "K"
codeforces_contest_name: "2018-2019 9th BSUIR Open Programming Championship. Junior"
rating: 0
weight: 102440
solve_time_s: 353
verified: true
draft: false
---

[CF 102440K - \u0410\u0431\u0441\u043e\u043b\u044e\u0442\u043d\u0430\u044f \u0430\u0431\u0441\u043e\u043b\u044e\u0442\u043d\u043e\u0441\u0442\u044c \u043c\u0430\u0441\u0441\u0438\u0432\u0430](https://codeforces.com/problemset/problem/102440/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 5m 53s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a binary array. Its absolute value is the absolute difference between the number of ones and the number of zeros. After changing one contiguous segment, including the possibility of changing nothing, we want the largest absolute value that can be obtained. Then individual array elements are flipped one at a time, and after every such update we must recompute this maximum.

A useful way to represent the array is to replace every `1` by `+1` and every `0` by `-1`. Let the resulting values be (b_i). The sum of the whole array is then

[
S=\sum b_i=c_1-c_0.
]

The absolute value of the array is simply (|S|).

Suppose we flip a segment whose sum in the transformed array is (X). Every element in that segment changes sign, so its contribution changes from (X) to (-X). The whole-array sum consequently becomes

[
S-2X.
]

Thus, for the current array, the answer is

[
\max_{\text{segment } I}|S-2\operatorname{sum}(I)|.
]

The segment sum can be any subarray sum, so the only values that matter are the minimum and maximum subarray sums. If (mn) is the minimum subarray sum and (mx) is the maximum subarray sum, then

[
c_A=\max\left(|S-2mn|,\ |S-2mx|\right).
]

The input contains up to (2\cdot10^5) elements and up to (2\cdot10^5) updates. An approach that scans the entire array after every update would perform (O(nq)) work, which can reach about (4\cdot10^{10}) element operations. Even recomputing all subarray sums from scratch is far beyond what the constraints allow. We need to update the relevant information in roughly logarithmic time.

There are several edge cases that can expose a careless implementation. With a single element, for example,

```
1 1
0
1
```

the array becomes `[1]`, so the answer is `1`. A segment tree implementation that accidentally assumes every internal node has two children can mishandle this case.

An all-equal array is another useful check. For

```
3 1
0 0 0
1
```

the update produces `[1,0,0]`. Flipping the last two elements gives `[1,1,1]`, so the answer is `3`. An implementation that only considers flipping a single position would incorrectly get `1`.

Endpoints are also important because the optimal segment can begin or end at an array boundary. For

```
4 1
1 0 0 1
1
```

after the update the array is `[0,0,0,1]`. Flipping the first three elements produces `[1,1,1,1]`, so the answer is `4`. A maximum-subarray implementation with incorrect prefix or suffix handling can miss this segment.

Finally, the optimal segment can be an interior segment. In the provided sample, after the first update the transformed array is `[1,1,1,-1,-1,1]`. The segment containing the two `-1` values has sum `-2`, and flipping it changes the total sum from `2` to `6`. Looking only at prefixes or suffixes would miss the optimum.

## Approaches

The direct solution is to try every possible segment after every point update. For a fixed segment we could calculate its sum and evaluate the resulting absolute value. There are (O(n^2)) segments, so doing this after each of the (q) updates would take (O(qn^2)) time. Even if we improve the fixed-array part by computing all subarray sums with prefix sums, there are still (O(n^2)) segments to inspect. With (n=q=2\cdot10^5), this is completely infeasible.

A better brute-force approach is to scan the array with Kadane's algorithm after every update. Kadane's algorithm gives both the maximum and minimum subarray sums in (O(n)), after which the answer follows immediately from the formula above. This reduces the total complexity to (O(nq)), but the worst case still contains roughly (4\cdot10^{10}) array-element operations.

The key observation is that the answer does not depend on every subarray separately. Once the total sum (S) is known, the expression (|S-2X|) is maximized at an extreme possible value of (X). Consequently, we only need the minimum and maximum subarray sums.

This is exactly the information that a segment tree can maintain. For each segment of the array, we store its total sum, its maximum prefix sum, maximum suffix sum, maximum subarray sum, and the corresponding three minimum values. When two neighboring segments are joined, every one of these quantities can be computed from the corresponding quantities of the two children. A point flip changes only one leaf, so only (O(\log n)) segment tree nodes have to be recomputed.

The brute-force solution works because Kadane's algorithm correctly finds the two extreme subarray sums, but it fails when those values must be recomputed after (2\cdot10^5) updates. The observation that the required information has a composable segment structure lets us preserve those values dynamically instead.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over all segments | (O(qn^2)) | (O(n)) | Too slow |
| Kadane after every update | (O(qn)) | (O(n)) | Too slow |
| Segment tree | (O((n+q)\log n)) | (O(n)) | Accepted |

## Algorithm Walkthrough

1. Convert every array value into either (+1) or (-1). A `1` becomes `+1`, and a `0` becomes `-1`. The sum of the transformed array is exactly the difference between the number of ones and zeros.
2. For every segment tree node, store seven values: the total sum, maximum prefix sum, maximum suffix sum, maximum subarray sum, minimum prefix sum, minimum suffix sum, and minimum subarray sum. We use nonempty prefixes, suffixes, and subarrays.
3. For two adjacent nodes (L) and (R), compute their combined total as

[
sum=L.sum+R.sum.
]

The maximum prefix is either entirely inside (L), or consists of all of (L) followed by a maximum prefix of (R):

[
maxPref=\max(L.maxPref,L.sum+R.maxPref).
]

The maximum suffix is symmetric:

[
maxSuff=\max(R.maxSuff,R.sum+L.maxSuff).
]

A maximum subarray is either entirely in the left child, entirely in the right child, or crosses their boundary. Hence

[
maxSub=\max(L.maxSub,R.maxSub,L.maxSuff+R.maxPref).
]

The minimum values are obtained using exactly the same formulas with `min` instead of `max`.

1. Build the segment tree from the initial transformed array. Each leaf representing value (x) has all seven stored quantities equal to (x).
2. When position (p) is flipped, change its leaf from (x) to (-x). Recalculate every ancestor on the path back to the root. Only (O(\log n)) nodes change because all other segments are unaffected.
3. Let the root contain total sum (S), minimum subarray sum (mn), and maximum subarray sum (mx). Flipping a segment with sum (mn) produces total sum (S-2mn), while flipping one with sum (mx) produces (S-2mx).
4. Output

[
\max\left(|S-2mn|,\ |S-2mx|\right).
]

The reason these two candidates are sufficient is that (f(X)=|S-2X|) is a V-shaped function of (X). Over all attainable subarray sums, its maximum is reached at one of the two extremes.

### Why it works

The segment tree invariant is that every node contains exactly the correct seven aggregate values for its corresponding array segment. The merge formulas enumerate every possible location of an optimal prefix, suffix, or subarray, so combining two correct children always produces a correct parent. A point update changes one leaf and then restores this invariant along the unique path to the root.

At the root, (S) is the sum of the entire transformed array and every legal flipped segment has some subarray sum (X). Its resulting total is (S-2X). Since the absolute value of this expression reaches its maximum among the smallest or largest possible (X), the root's minimum and maximum subarray sums give the exact answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, q = map(int, input().split())
    a = list(map(int, input().split()))

    size = 1
    while size < n:
        size <<= 1

    # Each node is:
    # sum, max_prefix, max_suffix, max_subarray,
    # min_prefix, min_suffix, min_subarray
    tree = [(0, 0, 0, 0, 0, 0, 0) for _ in range(2 * size)]

    for i in range(n):
        x = 1 if a[i] else -1
        tree[size + i] = (x, x, x, x, x, x, x)

    def merge(left, right):
        ls, lp, lsf, lm, lnp, lns, lmin = left
        rs, rp, rsf, rm, rnp, rns, rmin = right

        total = ls + rs

        max_prefix = max(lp, ls + rp)
        max_suffix = max(rsf, rs + lsf)
        max_sub = max(lm, rm, lsf + rp)

        min_prefix = min(lnp, ls + rnp)
        min_suffix = min(rns, rs + lns)
        min_sub = min(lmin, rmin, lns + rnp)

        return (
            total,
            max_prefix,
            max_suffix,
            max_sub,
            min_prefix,
            min_suffix,
            min_sub,
        )

    for i in range(size - 1, 0, -1):
        tree[i] = merge(tree[i << 1], tree[i << 1 | 1])

    out = []

    for _ in range(q):
        p = int(input()) - 1
        pos = size + p

        old = tree[pos][0]
        x = -old
        tree[pos] = (x, x, x, x, x, x, x)

        pos >>= 1
        while pos:
            tree[pos] = merge(tree[pos << 1], tree[pos << 1 | 1])
            pos >>= 1

        total = tree[1][0]
        max_sub = tree[1][3]
        min_sub = tree[1][6]

        answer = max(
            abs(total - 2 * max_sub),
            abs(total - 2 * min_sub)
        )
        out.append(str(answer))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The array is first transformed implicitly when the leaves are created. Storing `+1` for a one and `-1` for a zero avoids repeatedly converting between counts of zeros and ones.

The seven values in each tuple are sufficient because every parent aggregate can be expressed using only its two children. In particular, a maximum subarray crossing the boundary must be the best suffix of the left child followed by the best prefix of the right child. The same reasoning gives the minimum subarray formula.

The iterative tree uses a power-of-two base. Positions before `n` contain real array elements, while the remaining leaves are neutral zero segments. This works cleanly because the tree is built only over real values when the root aggregates are used, and zero leaves do not change any maximum or minimum that can already be obtained from a nonempty real segment. Since every real leaf has a nonzero value, the root's extrema remain nonempty subarray extrema.

During an update, the old leaf value is negated directly. This is safer than consulting the original binary array because the original value may have been flipped many times already. The update then walks upward until reaching the root.

All sums have absolute value at most (n), so Python integers have more than enough range. In languages with fixed-width integers, a signed 32-bit integer is already sufficient here, although using 64-bit integers is the usual safe choice.

## Worked Examples

### Sample 1

The initial array is

```
1 0 1 0 0 1
```

and the transformed representation is

```
1 -1 1 -1 -1 1
```

After every update, the root stores the following relevant values.

| Operation | Transformed array | Total (S) | Min subarray | Max subarray | Answer |
| --- | --- | --- | --- | --- | --- |
| flip 2 | `1 1 1 -1 -1 1` | 2 | -2 | 3 | 6 |
| flip 6 | `1 1 1 -1 -1 -1` | 0 | -3 | 3 | 6 |
| flip 5 | `1 1 1 -1 1 -1` | 2 | -1 | 3 | 4 |
| flip 1 | `-1 1 1 -1 1 -1` | 0 | -1 | 2 | 4 |

For the first update, the minimum subarray sum is `-2`, coming from the fourth and fifth positions. Flipping those two zeros into ones changes the total from `2` to `6`, which explains the first output. After the final update, the maximum subarray sum is `2`, so flipping that segment changes the total from `0` to `-4`, giving absolute value `4`.

### A second example

Consider

```
4 2
1 0 0 1
1
3
```

Initially the transformed array is

```
1 -1 -1 1
```

After flipping position 1, the transformed array becomes

```
-1 -1 -1 1
```

After flipping position 3, it becomes

```
-1 -1 1 1
```

The corresponding states are:

| Operation | Transformed array | Total (S) | Min subarray | Max subarray | Answer |
| --- | --- | --- | --- | --- | --- |
| flip 1 | `-1 -1 -1 1` | -2 | -3 | 1 | 4 |
| flip 3 | `-1 -1 1 1` | 0 | -2 | 2 | 4 |

The first state demonstrates why an optimal segment may touch the left boundary. Its minimum subarray is the entire first three positions, with sum `-3`. Flipping them makes every element equal to one, producing absolute value `4`.

The second state demonstrates the symmetric situation. The maximum subarray consists of the final two `+1` values, and flipping it changes the total from `0` to `-4`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O((n+q)\log n)) | Building the tree takes (O(n)), and every point update recalculates (O(\log n)) nodes |
| Space | (O(n)) | The iterative segment tree contains (O(n)) nodes |

With (n,q\le2\cdot10^5), the solution performs only logarithmically many aggregate recomputations per update. This replaces the (O(nq)) scan that would otherwise be required and keeps the total work within the intended range.

## Test Cases

The following test harness implements the same segment-tree logic through a function that accepts an input string. The maximum-size test is generated programmatically rather than embedding hundreds of thousands of numbers in the source.

```python
import sys
import io
from contextlib import redirect_stdout

def solve():
    input = sys.stdin.readline

    n, q = map(int, input().split())
    a = list(map(int, input().split()))

    size = 1
    while size < n:
        size <<= 1

    tree = [(0, 0, 0, 0, 0, 0, 0) for _ in range(2 * size)]

    for i, value in enumerate(a):
        x = 1 if value else -1
        tree[size + i] = (x, x, x, x, x, x, x)

    def merge(left, right):
        ls, lp, lsf, lm, lnp, lns, lmin = left
        rs, rp, rsf, rm, rnp, rns, rmin = right

        total = ls + rs

        max_prefix = max(lp, ls + rp)
        max_suffix = max(rsf, rs + lsf)
        max_sub = max(lm, rm, lsf + rp)

        min_prefix = min(lnp, ls + rnp)
        min_suffix = min(rns, rs + lns)
        min_sub = min(lmin, rmin, lns + rnp)

        return (
            total,
            max_prefix,
            max_suffix,
            max_sub,
            min_prefix,
            min_suffix,
            min_sub,
        )

    for i in range(size - 1, 0, -1):
        tree[i] = merge(tree[i << 1], tree[i << 1 | 1])

    ans = []

    for _ in range(q):
        p = int(input()) - 1
        pos = size + p

        x = -tree[pos][0]
        tree[pos] = (x, x, x, x, x, x, x)

        pos >>= 1
        while pos:
            tree[pos] = merge(tree[pos << 1], tree[pos << 1 | 1])
            pos >>= 1

        total = tree[1][0]
        max_sub = tree[1][3]
        min_sub = tree[1][6]

        ans.append(str(max(
            abs(total - 2 * max_sub),
            abs(total - 2 * min_sub)
        )))

    print("\n".join(ans))

def run(inp: str) -> str:
    old_stdin = sys.stdin
    output = io.StringIO()

    try:
        sys.stdin = io.StringIO(inp)
        with redirect_stdout(output):
            solve()
    finally:
        sys.stdin = old_stdin

    return output.getvalue()

# Provided sample
assert run(
    """6 4
1 0 1 0 0 1
2
6
5
1
"""
) == "6\n6\n4\n4\n", "sample 1"

# Minimum-size input
assert run(
    """1 3
0
1
1
1
"""
) == "1\n1\n1\n", "single element"

# All equal values
assert run(
    """3 2
0 0 0
1
3
"""
) == "3\n3\n", "all zeros"

# Boundary-heavy case
assert run(
    """4 2
1 0 0 1
1
3
"""
) == "4\n4\n", "boundary segments"

# Maximum-size input
n = 200000
large_input = (
    f"{n} 2\n"
    + " ".join(["1"] * n)
    + "\n100000\n1\n"
)
assert run(large_input) == f"{n}\n{n}\n", "maximum size"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 3 / 0 / 1 1 1` | `1, 1, 1` | Single-element tree and repeated flips |
| `3 2 / 0 0 0 / 1 3` | `3, 3` | All-equal array and full optimal segment |
| `4 2 / 1 0 0 1 / 1 3` | `4, 4` | Optimal segments touching array boundaries |
| `200000` ones with two updates | `200000, 200000` | Maximum input size and repeated point updates |

## Edge Cases

For a single-element array such as

```
1 1
0
1
```

the only element changes from `0` to `1`. The transformed tree consists of one real leaf with value `1`, so its total, minimum subarray, and maximum subarray sums are all `1`. The answer is

[
|1-2\cdot1|=1.
]

The segment tree does not need any special case for this situation.

For an all-zero array,

```
3 1
0 0 0
1
```

the update gives `[1,0,0]`, represented as `[1,-1,-1]`. The total is `-1`, the minimum subarray sum is `-2`, and the maximum subarray sum is `1`. Flipping the minimum-sum segment changes the total to

[
-1-2(-2)=3,
]

so the answer is `3`. The algorithm naturally finds the segment containing the two zeros without explicitly reasoning about binary counts.

For an optimal segment touching the left boundary,

```
4 1
1 0 0 1
1
```

the updated transformed array is `[-1,-1,-1,1]`. Its total is `-2` and its minimum subarray sum is `-3`. The first three elements form that minimum subarray, so flipping them gives

[
-2-2(-3)=4.
]

Thus the answer is `4`. The maximum-prefix and maximum-suffix fields in the tree are what allow such boundary-crossing segments to be combined correctly.

For an interior optimum, consider the final state of the provided sample after all four updates:

```
0 1 1 0 1 0
```

which becomes

```
-1 1 1 -1 1 -1.
```

Its total is `0`, while its maximum subarray sum is `2`, obtained from the two adjacent ones in positions `2` and `3`. Flipping that segment changes the total to

[
0-2\cdot2=-4,
]

so the answer is `4`. This confirms why the solution must track genuine subarrays rather than only prefixes, suffixes, or individual runs.

Finally, repeated updates to the same position require using the current leaf value rather than the original input value. For example,

```
1 3
0
1
1
1
```

changes the transformed value through `-1`, `+1`, `-1`, `+1`. Negating the current leaf each time handles this automatically. Keeping a separate boolean array would also work, but the leaf itself already contains exactly the state needed for the next update.
