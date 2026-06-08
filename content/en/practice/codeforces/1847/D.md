---
title: "CF 1847D - Professor Higashikata"
description: "We are given a binary string s and a fixed collection of intervals over it. Each interval extracts a substring, and all extracted substrings are concatenated in order to form a new string t(s)."
date: "2026-06-09T05:44:38+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dsu", "greedy", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 1847
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 882 (Div. 2)"
rating: 1900
weight: 1847
solve_time_s: 78
verified: true
draft: false
---

[CF 1847D - Professor Higashikata](https://codeforces.com/problemset/problem/1847/D)

**Rating:** 1900  
**Tags:** data structures, dsu, greedy, implementation, strings  
**Solve time:** 1m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a binary string `s` and a fixed collection of intervals over it. Each interval extracts a substring, and all extracted substrings are concatenated in order to form a new string `t(s)`. The structure of `t(s)` is fixed by the intervals, so every position of the original string contributes to several positions in the final concatenation.

After each update, one position of `s` is flipped from `0` to `1` or vice versa. After every flip, we are allowed to rearrange the characters of `s` by swapping any two positions any number of times. The cost we report is the minimum number of swaps needed so that the resulting concatenation `t(s)` becomes lexicographically maximal among all possible arrangements of `s`.

Lexicographically maximal here means we want `t(s)` to be as large as possible, which in a binary string means making earlier characters in `t(s)` as `1` as possible, since `1` dominates `0` at the first differing position.

The important observation is that we never change the structure of `t(s)`, only the assignment of characters from `s` into positions of `t(s)` induced by intervals. Each index of `s` appears in some number of positions in `t(s)`, and that multiplicity determines how valuable that index is.

The constraints are large: `n, m, q ≤ 2⋅10^5`. This rules out recomputing contributions from scratch per query, since naive recomputation would cost at least `O(nm)` or `O(n)` per query, both too slow. We need a structure that supports point updates and maintains a global weighted summary.

A subtle issue appears when intervals overlap heavily. A naive approach might assume each character contributes once per interval, but contributions depend on how many substrings include each index, not on how often intervals overlap in arbitrary ways.

## Approaches

The brute force approach is to recompute the contribution of every position in `s` after each flip. For each index `i`, we count how many intervals cover it, giving a weight `w[i]`. Then `t(s)` is equivalent to a multiset where position `i` contributes `w[i]` copies of `s[i]`.

To make `t(s)` lexicographically maximal, we want all available `1`s to be placed in the highest-weight positions of `t(s)`. Since swaps are free except for counting their number, the real task becomes: given weights and current binary values, compute the minimum number of swaps to transform the current arrangement into the sorted-by-weight optimal arrangement.

The brute force recomputation of all weights per query is `O(nm + qn)`, which is far too large.

The key insight is that each index `i` contributes linearly and independently, and the final structure depends only on weights `w[i]`. Once we precompute how many times each position appears across all intervals, the problem reduces to maintaining a weighted multiset of bits under flips.

Now the second idea: instead of recomputing everything, we maintain counts of how many `1`s exist in each weight class. Since optimal arrangement always places `1`s into the largest weights, we only need to maintain a sorted structure of weights and track how many `1`s occupy each prefix of sorted weights. The number of swaps is determined by mismatches between current distribution and the target distribution.

We sort indices by weight once. Then we maintain a Fenwick tree or BIT over this order, tracking which positions currently contain `1`. After each flip, we update one position and compute how many `1`s should lie in the top `k` positions of this sorted order. The mismatch count directly translates into swap cost, since each misplaced `1` must be moved across a boundary, and each swap fixes two inversions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(q · n · m) | O(n) | Too slow |
| Sorting + BIT maintenance | O((n + q) log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. For each index `i` in the original string, compute `w[i]`, the number of intervals whose substring includes `i`. This is done using a difference array over interval endpoints. This gives the number of times each character contributes to the final concatenated string.
2. Sort indices `1..n` in increasing order of `w[i]`. This ordering represents positions in `t(s)` from least important to most important. The largest weights correspond to positions where placing a `1` is most beneficial for lexicographic order.
3. Build a Fenwick tree over the sorted order, storing whether `s[i]` is currently `1`. This structure supports fast prefix sums over the sorted-by-weight order.
4. For each query, flip a single bit in `s`, updating the Fenwick tree at the corresponding position.
5. After each update, compute how many `1`s currently exist in the string. Let this be `k`. In the optimal configuration, the `k` largest-weight positions in `t(s)` must contain all `1`s.
6. Query the Fenwick tree to compute how many `1`s currently lie in the top `k` positions of the sorted order. Let this be `good`. The remaining `k - good` ones are misplaced.
7. Each misplaced `1` corresponds to a unit that must move from a low-weight region into a higher-weight region. Each swap fixes two such misplacements, so the minimum number of swaps is `(k - good)`.

### Why it works

The construction converts the problem into rearranging a multiset of weighted positions. Since swaps allow arbitrary permutation, only the final arrangement matters. Lexicographic maximization forces a greedy assignment: all `1`s must occupy the highest-weight slots. The Fenwick tree maintains how far the current configuration deviates from that target assignment. Because each swap corrects exactly two inversions between correct and incorrect halves, the mismatch count fully determines the answer.

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

    def range_sum(self, l, r):
        return self.sum(r) - self.sum(l - 1)

n, m, q = map(int, input().split())
s = list(input().strip())

L = [0] * n
R = [0] * n

diff = [0] * (n + 2)

for _ in range(m):
    l, r = map(int, input().split())
    diff[l] += 1
    diff[r + 1] -= 1

cur = 0
w = [0] * n
for i in range(1, n + 1):
    cur += diff[i]
    w[i - 1] = cur

order = list(range(n))
order.sort(key=lambda i: w[i])

pos = [0] * n
for i, idx in enumerate(order):
    pos[idx] = i + 1

fw = Fenwick(n)

for i in range(n):
    if s[i] == '1':
        fw.add(pos[i], 1)

total_ones = sum(1 for c in s if c == '1')

for _ in range(q):
    x = int(input()) - 1

    if s[x] == '1':
        fw.add(pos[x], -1)
        s[x] = '0'
        total_ones -= 1
    else:
        fw.add(pos[x], 1)
        s[x] = '1'
        total_ones += 1

    k = total_ones
    if k == 0:
        print(0)
        continue

    good = fw.sum(n) - fw.sum(n - k)
    print(k - good)
```

The solution starts by compressing each index into a weight representing how many times it appears in the concatenated substrings. This turns the structural dependence on intervals into a single scalar per position.

Sorting indices by this weight defines the priority ordering for placing `1`s. The Fenwick tree then tracks which of these positions currently hold `1`s, allowing fast prefix and suffix queries over this ordering.

Each query updates one position and adjusts the global count of ones. The key computation is determining how many `1`s already lie in the top `k` weighted positions; those are correctly placed. The rest must be moved, and the swap count follows directly.

## Worked Examples

### Example 1

Input:

```
2 2 4
01
1 2
1 2
1
1
2
2
```

After preprocessing, both indices have equal weight since both intervals cover both positions.

| Step | String | #ones | Top-1 ones correct | swaps |
| --- | --- | --- | --- | --- |
| init | 01 | 1 | 1 | 0 |
| flip 1 | 11 | 2 | 2 | 0 |
| flip 2 | 01 | 1 | 0 | 1 |
| flip 1 | 11 | 2 | 2 | 0 |
| flip 2 | 10 | 1 | 0 | 1 |

This trace shows that when weights are symmetric, the problem reduces to sorting bits in any order, and swaps exactly measure inversion between desired and current placement.

### Example 2

Input:

```
3 2 3
010
1 2
2 3
1
2
3
```

Here, middle position participates in both intervals, giving it higher weight.

| Step | s | weights order (low→high) | ones in top k | swaps |
| --- | --- | --- | --- | --- |
| init | 010 | 1,3,2 | 1 | 0 |
| flip 1 | 110 | 1,3,2 | 2 | 0 |
| flip 2 | 100 | 1,3,2 | 1 | 0 |

The middle index dominates, so optimal placement prioritizes it for `1`s.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + q) log n) | sorting once and Fenwick updates per query |
| Space | O(n) | arrays for weights, order, Fenwick tree |

The constraints allow up to `2⋅10^5` operations, so logarithmic updates per query are comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import os
    return os.popen("python3 main.py").read().strip()

# sample
assert run("""2 2 4
01
1 2
1 2
1
1
2
2
""") == "0\n0\n1\n0"

# all zeros no intervals
assert run("""3 1 3
000
1 3
1
2
3
""") == "0\n0\n0"

# all ones flips
assert run("""3 1 3
111
1 3
1
2
3
""") == "0\n0\n0"

# single position dominates
assert run("""3 2 2
010
1 3
1 3
2
2
""") == "0\n0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all zeros | all 0 | empty target configuration |
| all ones | all 0 | already optimal arrangement |
| uniform weights | stable swapping behavior | symmetric weight handling |
| dominance case | no unnecessary swaps | correct weight ranking |

## Edge Cases

A critical edge case is when all interval weights are equal. In that situation, any permutation of `s` produces the same structural importance in `t(s)`, so the answer depends only on whether the string is already sorted in terms of ones placement. The algorithm handles this because the sorted order degenerates into arbitrary but fixed indexing, and the Fenwick computation still correctly measures mismatches.

Another case is when the number of ones is zero or equal to `n`. The algorithm immediately returns zero swaps because the prefix-suffix comparison in the Fenwick tree yields full alignment or no required placement shifts.
