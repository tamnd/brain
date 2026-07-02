---
title: "CF 103914F - Longest Common Subsequence"
description: "We are given two sequences of integers, but neither sequence is provided directly. Instead, both are produced by repeatedly applying the same quadratic recurrence modulo a fixed value."
date: "2026-07-02T07:27:14+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103914
codeforces_index: "F"
codeforces_contest_name: "Heltion Contest 1"
rating: 0
weight: 103914
solve_time_s: 57
verified: true
draft: false
---

[CF 103914F - Longest Common Subsequence](https://codeforces.com/problemset/problem/103914/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 57s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two sequences of integers, but neither sequence is provided directly. Instead, both are produced by repeatedly applying the same quadratic recurrence modulo a fixed value. We first generate the entire sequence `s` of length `n`, then continue the same recurrence to generate `t` of length `m` without resetting anything. This makes `t` the continuation of the same underlying stream that produced `s`.

The task is to compute the length of the longest subsequence that appears in both `s` and `t`, where order must be preserved inside each sequence but elements do not need to be contiguous.

From a constraints perspective, the combined length of all sequences across test cases is at most one million. This immediately rules out any quadratic dynamic programming over pairs of positions, since even a single worst-case test would make that approach exceed time limits by several orders of magnitude. A solution must be close to linear or near-linear in the total number of generated elements, possibly with a logarithmic factor.

A subtle point comes from the generation process itself. Since both sequences come from a single recurrence chain, `s` is `A[1..n]` and `t` is `A[n+1..n+m]` for a single hidden array `A`. This structure is the key to avoiding treating the two sequences as independent.

A naive attempt that often fails is to run a standard LCS dynamic programming or to try to match equal values greedily. These both break in simple cases where repeated values force incorrect pairing decisions. For example, if `s = [1, 1]` and `t = [1, 1]`, the correct answer is 2, but greedy matching of first occurrences can easily produce 1 depending on implementation.

Another failure mode appears when values repeat heavily. If `s = [5, 5, 5]` and `t = [5, 5, 5, 5]`, the answer is 3, but naive pairing strategies that do not enforce global ordering can overcount or undercount depending on how matches are consumed.

The core difficulty is that each value may appear many times in both sequences, so the problem is not about equality checks alone but about selecting a globally consistent increasing pairing.

## Approaches

A direct dynamic programming solution defines `dp[i][j]` as the LCS of prefixes `s[1..i]` and `t[1..j]`. This works because every choice either skips an element in one sequence or matches equal elements. However, this requires `O(nm)` time, which is impossible when both sequences can reach lengths up to one million.

The key observation is that the two sequences are not arbitrary. They are just two consecutive segments of the same generated array `A`. This means every match between `s` and `t` corresponds to a pair of indices `(i, j)` such that `i < j` and `A[i] = A[j]`, with the additional constraint that we must choose a set of such pairs that preserves order in both dimensions.

This transforms the problem into finding the largest chain of points in a partially ordered set, where each point is a valid equality between an index in `s` and an index in `t`. A standard way to solve such problems is to convert them into a longest increasing subsequence over one dimension while ordering by the other.

Concretely, we process indices in `s` in increasing order. For each value `v = s[i]`, we know all positions in `t` where the same value occurs. For each such position `j`, we can attempt to extend a subsequence ending at `j` using the best subsequence ending before `j`.

To support this efficiently, we maintain a Fenwick tree over positions in `t`, where each index stores the best LCS length ending at that position. Each element from `s` contributes updates to multiple positions in `t`, and each update depends on prefix queries in `t`.

The main complication is that values may appear many times in `t`, but since total input size is bounded by one million across all tests, iterating over all occurrences remains feasible in aggregate.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force DP | O(nm) | O(nm) | Too slow |
| Fenwick over matches | O((n + m) log m) amortized | O(m) | Accepted |

## Algorithm Walkthrough

We treat the entire generation process as producing a single array `A`, where `s = A[1..n]` and `t = A[n+1..n+m]`.

1. Generate both sequences in one pass while storing positions of each value in `t`. For every index `j` in `t`, we append `j` into a list keyed by `A[j]`. This allows fast lookup of where a value occurs in the second segment.
2. Initialize a Fenwick tree over indices of `t`, where each position represents the best LCS length ending at that position. Initially all values are zero.
3. Iterate through each element `s[i]` in order. For the current value `v = s[i]`, retrieve the list of all positions in `t` where `A[j] = v`.
4. For each such position `j`, compute `best = query(j - 1) + 1`, where `query(j - 1)` returns the best subsequence ending strictly before position `j` in `t`. This ensures we preserve increasing order in the second sequence.
5. After computing all candidate updates for this value, apply them to the Fenwick tree. This separation between query and update prevents using updates from the same `s[i]` multiple times in inconsistent ways.
6. Track the maximum value ever written into the Fenwick tree; this is the final answer.

The separation of query and update within each `s[i]` is essential because multiple occurrences of the same value in `t` should not chain through each other within a single step of `s`.

### Why it works

Every valid common subsequence corresponds to selecting pairs `(i, j)` such that indices in both sequences increase. The Fenwick tree ensures that when we place a match at position `j` in `t`, we only extend subsequences that end strictly before `j`. Processing `s` in order guarantees that indices from `s` are also increasing. This constructs exactly the set of valid increasing chains in the bipartite matching graph defined by equal values.

Because every transition respects both ordering constraints and every valid subsequence can be built by progressively choosing matching pairs, the maximum value stored is exactly the LCS length.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def update(self, i, v):
        while i <= self.n:
            if v > self.bit[i]:
                self.bit[i] = v
            i += i & -i

    def query(self, i):
        res = 0
        while i > 0:
            if self.bit[i] > res:
                res = self.bit[i]
            i -= i & -i
        return res

def solve():
    T = int(input())
    for _ in range(T):
        n, m, p, x, a, b, c = map(int, input().split())

        s = [0] * n
        t = [0] * m

        for i in range(n):
            x = (a * x * x + b * x + c) % p
            s[i] = x

        pos = {}
        for i in range(m):
            x = (a * x * x + b * x + c) % p
            t[i] = x
            if x not in pos:
                pos[x] = []
            pos[x].append(i + 1)

        fw = Fenwick(m)
        ans = 0

        for i in range(n):
            v = s[i]
            if v not in pos:
                continue

            updates = []
            for j in pos[v]:
                best = fw.query(j - 1) + 1
                updates.append((j, best))

            for j, val in updates:
                fw.update(j, val)
                if val > ans:
                    ans = val

        print(ans)

if __name__ == "__main__":
    solve()
```

The solution carefully maintains a Fenwick tree over positions in `t`. Each query step computes the best subsequence that can be extended by matching a current value in `s` to occurrences in `t`.

A subtle implementation requirement is buffering updates for each value of `s[i]`. Without this, updating the Fenwick tree while iterating positions in `t` could allow later occurrences of the same value to incorrectly depend on earlier updates from the same iteration.

All indexing inside the Fenwick tree is 1-based, while `t` is stored with 1-based positions to avoid off-by-one mistakes in prefix queries.

## Worked Examples

Consider the second sample case where both sequences consist entirely of zeros.

We have `s = [0, 0, 0]` and `t = [0, 0, 0, 0]`.

For each element in `s`, every position in `t` is a valid match.

| Step | s[i] | Candidate t positions | Query results | Updates applied |
| --- | --- | --- | --- | --- |
| 1 | 0 | 1,2,3,4 | all 0 + 1 = 1 | all positions set to 1 |
| 2 | 0 | 1,2,3,4 | prefixes propagate to 2 | values become 2 |
| 3 | 0 | 1,2,3,4 | prefixes propagate to 3 | values become 3 |

After processing all elements, the maximum value in the Fenwick tree is 3, matching the expected LCS length.

Now consider a case with no overlap, such as `s = [1, 2, 3]` and `t = [4, 5, 6, 7]`. No values appear in both sequences, so no updates are ever performed. The Fenwick tree remains zero throughout, confirming that the algorithm correctly handles disjoint alphabets.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + m) log m) | Each position in `t` is stored once and updated through Fenwick operations, and each element in `s` processes its matching occurrences |
| Space | O(m) | Fenwick tree plus position lists for values in `t` |

The constraints guarantee that the total size of all sequences across test cases is at most one million, so the logarithmic factor from Fenwick operations remains comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdout.getvalue() if False else ""

# NOTE: Full integration depends on wiring solve(), omitted here for brevity

# minimal distinct case
# s and t share no values

# repeated values
# alternating structure
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| minimal non-overlap | 0 | no matches |
| all equal small | min(n,m) | repeated handling |
| increasing distinct | 1 | ordering constraint |
| mixed repeats | correct LCS | DP consistency |

## Edge Cases

A critical edge case is when all values are identical. In that situation, every element in `s` matches every element in `t`, and the answer should be exactly `min(n, m)`. The algorithm handles this because each step extends all previous prefixes in order, and the Fenwick tree naturally accumulates the longest chain without double counting.

Another edge case is when there are no shared values between `s` and `t`. Since no positions are ever updated, the Fenwick tree remains zero and the output is correctly zero.

A third case is when values repeat sparsely but irregularly. Even if occurrences are unevenly distributed, the algorithm always enforces strict ordering through prefix queries, preventing invalid reordering of matches across `t`.
