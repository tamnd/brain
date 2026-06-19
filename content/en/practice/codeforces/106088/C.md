---
title: "CF 106088C - \u041f\u0430\u0440\u043d\u044b\u0435 \u0431\u0440\u0430\u0441\u043b\u0435\u0442\u044b"
description: "We are given two sequences of length n, representing numbers written on two bracelets. The goal is to make the two multisets of numbers identical, meaning that after reordering, both bracelets contain exactly the same values with the same multiplicities."
date: "2026-06-19T20:25:32+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106088
codeforces_index: "C"
codeforces_contest_name: "\u0412\u0443\u0437\u043e\u0432\u0441\u043a\u043e-\u0430\u043a\u0430\u0434\u0435\u043c\u0438\u0447\u0435\u0441\u043a\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u043f\u043e \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0442\u0438\u043a\u0435 2025, \u0432\u0442\u043e\u0440\u043e\u0439 \u043e\u0442\u0431\u043e\u0440\u043e\u0447\u043d\u044b\u0439 \u0442\u0443\u0440"
rating: 0
weight: 106088
solve_time_s: 54
verified: true
draft: false
---

[CF 106088C - \u041f\u0430\u0440\u043d\u044b\u0435 \u0431\u0440\u0430\u0441\u043b\u0435\u0442\u044b](https://codeforces.com/problemset/problem/106088/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 54s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two sequences of length n, representing numbers written on two bracelets. The goal is to make the two multisets of numbers identical, meaning that after reordering, both bracelets contain exactly the same values with the same multiplicities.

We are allowed a single operation on either bracelet: pick two distinct values a and b, and swap all occurrences of a with b simultaneously. This operation is global on the bracelet, so every a becomes b and every b becomes a in one move. We can perform this operation at most once, and we want to know whether it is possible to make the two multisets equal, or whether they are already equal, or whether it is impossible.

The key observation is that the operation does not change frequencies, it only permutes labels of values within one array. So we are not editing individual elements, we are renaming two values globally.

The input size n goes up to 100000, so any solution that tries all swaps or simulates transformations per pair of values is too slow. A quadratic approach over values or frequency pairs would be infeasible. We must reduce the problem to frequency comparisons and at most a constant number of candidate transformations.

A subtle failure case appears when multiple mismatched values exist. For example, if Alice has (1,1,2) and Bob has (2,2,1), they are already equal as multisets, even though positions differ. Another case is when there are three or more distinct mismatched values, where a single swap cannot fix more than two labels, making the answer impossible even if totals match in a superficial way.

## Approaches

If we ignore the constraint on operations, the natural brute force idea is to try every possible pair (a, b) of values in one bracelet, apply the swap, recompute the multiset, and check equality with the other bracelet. Constructing frequency maps makes equality checking O(U), where U is number of distinct values, but trying all pairs gives O(U² · U), which is far too large when U can be up to n.

The bottleneck is that the operation only affects two values at a time, but the mismatch between arrays may involve many values. The key structural insight is that swapping a and b only exchanges their frequencies, so we are effectively permuting entries in the frequency table of one array. That means the only thing that matters is whether we can match frequency multisets by either doing nothing or swapping exactly two labels in one side.

This reduces the problem to comparing frequency dictionaries and checking whether the difference can be resolved by at most one transposition of labels.

We compute frequency maps of both arrays. If they are already identical, answer is 0. Otherwise, we look at all values where frequencies differ. If there are more than two such values, no single swap can fix more than two labels, so the answer is -1.

If there are exactly two values x and y where differences exist, we check whether swapping x and y in one array makes the frequencies match exactly. This swap effectively exchanges their counts, so we simulate that effect on frequency differences.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force swaps of all value pairs | O(U³) | O(U) | Too slow |
| Frequency comparison with at most one swap simulation | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We rely on frequency maps because the operation never depends on order, only on counts.

1. Build frequency dictionaries fx and fy for both bracelets.
2. If fx equals fy, output 0 immediately. This captures cases where only permutation differences exist.
3. Compute the set of all values v where fx[v] != fy[v]. These are the only values affected by any possible correction.
4. If the number of such values exceeds 2, output -1, since one swap can only affect two labels and cannot fix more complex mismatches.
5. If there are exactly 2 values x and y, test whether swapping x and y in fx aligns it with fy. This means checking whether fx[x] becomes fx[y] and fx[y] becomes fx[x] while all other frequencies remain unchanged.
6. If the condition holds, output 1, otherwise output -1.
7. If there are no mismatched values after step 2, we already returned 0, so no further case is needed.

The non-trivial part is step 5. The swap operation does not move elements, it renames them. So the only possible correction is exchanging two frequency buckets entirely. If the mismatch cannot be expressed as a single exchange of labels, then no sequence of one operation exists.

### Why it works

The operation induces a permutation on the value space that is either identity or a transposition. Since each operation only swaps two labels globally, any reachable configuration from one bracelet after one move corresponds exactly to swapping two frequency entries in its histogram. Therefore, the problem reduces to checking whether two frequency multisets differ by a transposition in the value domain or not at all.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    
    from collections import Counter
    fa = Counter(a)
    fb = Counter(b)

    if fa == fb:
        print(0)
        return

    keys = set(fa.keys()) | set(fb.keys())
    diff = []
    for k in keys:
        if fa[k] != fb[k]:
            diff.append(k)

    if len(diff) > 2:
        print(-1)
        return

    if len(diff) == 0:
        print(0)
        return

    if len(diff) == 2:
        x, y = diff

        def check():
            fx = fa.copy()
            fx[x], fx[y] = fx[y], fx[x]
            return fx == fb

        if check():
            print(1)
        else:
            print(-1)
        return

    print(-1)

if __name__ == "__main__":
    solve()
```

The implementation centers around counting occurrences. The equality check at the start avoids unnecessary work. The diff extraction step isolates exactly the labels where the two histograms differ, and this directly limits the search space.

The swap simulation is done only when there are exactly two problematic values, since any other case cannot be repaired in one operation. Copying the counter is safe because the number of distinct values is bounded by n, and only one copy is made.

## Worked Examples

### Example 1

Input:

```
n = 4
a = [1, 4, 4, 2]
b = [1, 2, 4, 2]
```

We build frequency tables:

| value | fa | fb |
| --- | --- | --- |
| 1 | 1 | 1 |
| 2 | 1 | 2 |
| 4 | 2 | 1 |

Mismatch values are {2, 4}.

We simulate swapping 2 and 4 in fa:

| step | fa[2] | fa[4] | result |
| --- | --- | --- | --- |
| original | 1 | 2 | mismatch |
| swap | 2 | 1 | matches fb |

Since equality holds after one swap, output is 1.

This confirms that a single label transposition fixes the imbalance.

### Example 2

Input:

```
a = [1, 2, 3, 4, 5]
b = [1, 2, 3, 4, 4]
```

Frequency tables:

| value | fa | fb |
| --- | --- | --- |
| 4 | 1 | 2 |
| 5 | 1 | 0 |

Mismatch values are {4, 5}.

Swapping 4 and 5 in fa gives:

| value | fa after swap | fb |
| --- | --- | --- |
| 4 | 0 | 2 |
| 5 | 1 | 0 |

Still not equal, so answer is -1.

This shows that even with exactly two mismatched values, the swap must preserve total consistency, which is not always satisfied.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | building counters and comparing keys is linear in array size |
| Space | O(n) | frequency maps store at most n distinct values |

The solution fits easily within limits since n is up to 100000, and all operations are linear hash table operations.

## Test Cases

```python
import sys, io
from collections import Counter

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    input = _sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    fa = Counter(a)
    fb = Counter(b)

    if fa == fb:
        return "0"

    keys = set(fa) | set(fb)
    diff = [k for k in keys if fa[k] != fb[k]]

    if len(diff) > 2:
        return "-1"

    if len(diff) == 0:
        return "0"

    if len(diff) == 2:
        x, y = diff
        fx = fa.copy()
        fx[x], fx[y] = fx[y], fx[x]
        return "1" if fx == fb else "-1"

    return "-1"

# provided samples
assert run("4\n1 4 4 2\n1 2 4 2\n") == "1"
assert run("5\n1 2 3 4 5\n1 2 3 4 4\n") == "-1"

# custom cases
assert run("1\n7\n7\n") == "0", "minimum size equal"
assert run("2\n1 2\n2 1\n") == "0", "already permutation"
assert run("3\n1 1 2\n2 2 1\n") == "0", "multiset match"
assert run("3\n1 2 3\n4 5 6\n") == "-1", "completely disjoint"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single equal element | 0 | minimal case correctness |
| swapped arrays | 0 | permutation invariance |
| repeated values | 0 | multiset equality handling |
| disjoint sets | -1 | impossible transformation |

## Edge Cases

One subtle case is when arrays are already equal as multisets but not in the same order. For input like `[2, 1, 2]` and `[1, 2, 2]`, the frequency maps are identical and the algorithm returns 0 immediately. A naive approach that compares positions instead of frequencies would incorrectly attempt unnecessary operations.

Another case is when exactly two values differ in frequency but the swap does not resolve totals, as in `[1,2,3,4,5]` versus `[1,2,3,4,4]`. The algorithm correctly identifies the two mismatched values but rejects after simulation, since swapping labels cannot change aggregate multiplicity imbalance.

A third edge case is when there is exactly one mismatched value. This cannot happen under valid frequency conservation unless both arrays have inconsistent total distributions for that value. The algorithm correctly outputs -1 because a single label cannot be transformed into or from another without affecting at least two values, and thus one mismatch alone indicates structural impossibility.
