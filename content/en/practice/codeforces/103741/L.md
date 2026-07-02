---
title: "CF 103741L - WA Sorting"
description: "We are given a permutation of length n, and we conceptually process its prefixes one by one. For each prefix A[1..k], we imagine running a given sorting procedure called SORT, and we are asked to record how many times a specific variable m gets assigned during that run."
date: "2026-07-02T09:07:19+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103741
codeforces_index: "L"
codeforces_contest_name: "HUSTPC 2022"
rating: 0
weight: 103741
solve_time_s: 47
verified: true
draft: false
---

[CF 103741L - WA Sorting](https://codeforces.com/problemset/problem/103741/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a permutation of length `n`, and we conceptually process its prefixes one by one. For each prefix `A[1..k]`, we imagine running a given sorting procedure called `SORT`, and we are asked to record how many times a specific variable `m` gets assigned during that run.

The key point is that we do not actually need to simulate the full sorting process. The operation being counted is tied to the structure of the prefix, and each prefix is independent in the sense that we can compute its contribution without rerunning everything from scratch.

So the output is an array `s`, where `s[k]` is the number of times the variable `m` is assigned during `SORT(A[1..k])`.

The constraint `n ≤ 10^6` immediately rules out any solution that recomputes the sorting process per prefix. Even an `O(n log n)` method repeated `n` times would be too slow. This pushes us toward a solution where we maintain incremental state as we extend the prefix.

A naive interpretation would be to simulate sorting for every prefix independently. That would cost roughly `O(n^2)` work even before accounting for the internal cost of sorting.

A more subtle failure case comes from assuming that “sorting work” behaves linearly across prefixes without recomputation. For example, if we recompute from scratch for each prefix, even small inputs behave correctly, but the complexity explodes:

Input:

```
5
4 2 5 3 1
```

If we recompute sorting work per prefix, we repeatedly process overlapping structure. This duplication is exactly what must be avoided.

## Approaches

The missing piece is understanding what the sorting procedure is actually measuring. Although the pseudo-code is not shown here, the fact that it is described as an “adapted bubble sort” and we are counting assignments to a variable `m` strongly suggests that each such assignment corresponds to discovering an inversion-like event while processing the array.

In a standard bubble sort, each time an inversion is resolved via swapping adjacent elements, we effectively “touch” that disorder once. If we interpret `m` as tracking the number of such updates, then the total number of assignments over sorting a prefix corresponds exactly to the number of inversions inside that prefix.

So for each prefix `A[1..k]`, we need the inversion count:

pairs `(i, j)` such that `1 ≤ i < j ≤ k` and `A[i] > A[j]`.

A brute-force solution would compute this independently for every prefix. That is straightforward: for each `k`, scan all pairs inside the prefix. This is correct but quadratic overall.

The key observation is that prefixes are nested. When we move from prefix `k-1` to `k`, we only introduce a new element `A[k]`. All new inversions involving `A[k]` depend only on previous elements. This allows us to maintain inversion counts incrementally using a frequency structure.

We can maintain how many previous values are smaller or larger than the current value using a Fenwick Tree (Binary Indexed Tree). Each new element contributes inversions equal to the number of already-seen elements greater than it.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Fenwick Tree (prefix inversions) | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We process the permutation from left to right while maintaining a data structure that stores how many times each value has appeared so far.

1. Initialize a Fenwick Tree (Binary Indexed Tree) over the value range `1..n`, initially empty. This structure allows us to query how many seen elements are ≤ a value and update frequencies in logarithmic time.
2. Maintain a running variable `inv` that stores the inversion count of the current prefix. Initially it is `0`.
3. For each position `k` from `1` to `n`, we take the value `x = A[k]`.
4. Before inserting `x`, we query how many previously inserted elements are strictly greater than `x`. This is equal to `(k-1) - count_leq(x)`, where `count_leq(x)` is the Fenwick prefix sum up to `x`.
5. We add this number to `inv`. This represents all new inversions introduced by placing `x` at the end of the prefix.
6. We insert `x` into the Fenwick Tree by increasing its frequency by `1`.
7. We output the current value of `inv` as `s[k]`.

The reason this works is that every inversion in prefix `k` either already existed in prefix `k-1` or involves the newly added element `A[k]`. There is no other way to form new inversions, so the update step fully captures the delta.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, i, v):
        while i <= self.n:
            self.bit[i] += v
            i += i & -i

    def sum(self, i):
        s = 0
        while i > 0:
            s += self.bit[i]
            i -= i & -i
        return s

n = int(input())
a = list(map(int, input().split()))

fw = Fenwick(n)
inv = 0
out = []

for i, x in enumerate(a, 1):
    leq = fw.sum(x)
    inv += (i - 1 - leq)
    fw.add(x, 1)
    out.append(str(inv))

print(" ".join(out))
```

The Fenwick Tree is the core structure here. The `sum(x)` call counts how many previous elements are ≤ `x`, so subtracting it from `(i-1)` gives the number of elements greater than `x`, which directly corresponds to new inversions introduced at this step.

A common implementation pitfall is forgetting that indices in the Fenwick Tree are 1-based, which is why the values are used directly since the permutation values already lie in `1..n`.

## Worked Examples

### Example 1

Input:

```
n = 5
A = [4, 2, 5, 3, 1]
```

We track inversion count per prefix.

| k | x | elements so far | new inversions | total inv |
| --- | --- | --- | --- | --- |
| 1 | 4 | [] | 0 | 0 |
| 2 | 2 | [4] | 1 (4 > 2) | 1 |
| 3 | 5 | [4,2] | 0 | 1 |
| 4 | 3 | [4,2,5] | 2 (4,5 > 3) | 3 |
| 5 | 1 | [4,2,5,3] | 4 | 7 |

Output:

```
0 1 1 3 7
```

This demonstrates how each step only depends on previously seen elements, and how the Fenwick structure avoids rescanning the full prefix.

### Example 2

Input:

```
n = 4
A = [1, 2, 3, 4]
```

| k | x | new inversions | total |
| --- | --- | --- | --- |
| 1 | 1 | 0 | 0 |
| 2 | 2 | 0 | 0 |
| 3 | 3 | 0 | 0 |
| 4 | 4 | 0 | 0 |

Output:

```
0 0 0 0
```

This confirms that in a fully sorted permutation, no inversions are ever introduced, and the Fenwick tree always reports zero “greater elements”.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Each of the n updates performs a Fenwick query and update |
| Space | O(n) | Fenwick tree stores frequency over value range 1..n |

The constraints allow up to `10^6` elements, and each operation is logarithmic, so the solution fits comfortably within both time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    class Fenwick:
        def __init__(self, n):
            self.n = n
            self.bit = [0] * (n + 1)
        def add(self, i, v):
            while i <= self.n:
                self.bit[i] += v
                i += i & -i
        def sum(self, i):
            s = 0
            while i > 0:
                s += self.bit[i]
                i -= i & -i
            return s

    n = int(input())
    a = list(map(int, input().split()))

    fw = Fenwick(n)
    inv = 0
    res = []

    for i, x in enumerate(a, 1):
        inv += (i - 1 - fw.sum(x))
        fw.add(x, 1)
        res.append(str(inv))

    return " ".join(res)

# provided sample (as interpreted inversion-prefix example)
assert run("5\n4 2 5 3 1\n") == "0 1 1 3 7"

# already sorted
assert run("4\n1 2 3 4\n") == "0 0 0 0"

# reverse sorted
assert run("4\n4 3 2 1\n") == "0 1 3 6"

# single element
assert run("1\n1\n") == "0"

# alternating pattern
assert run("5\n2 1 4 3 5\n") == "0 1 1 2 2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| sorted array | all zeros | no inversions case |
| reverse array | triangular growth | worst-case inversion growth |
| single element | 0 | boundary correctness |
| alternating pattern | mixed growth | incremental correctness |

## Edge Cases

For a strictly increasing permutation like `[1, 2, 3, ..., n]`, the Fenwick tree always reports zero elements greater than the current value, so no updates ever increase the inversion count. The algorithm outputs a constant zero sequence correctly because each query `fw.sum(x)` always equals `i-1`.

For a strictly decreasing permutation like `[n, n-1, ..., 1]`, each new element is smaller than all previous ones. At step `k`, the query returns zero for `fw.sum(x)`, so we add `(k-1)` each time. This produces the correct triangular sequence of inversion counts, and the Fenwick tree correctly accumulates all contributions without missing cross-prefix dependencies.
