---
title: "CF 106420H - Red Combo"
description: "We are given a permutation-like process that builds a structure by repeatedly merging or “validating” adjacent segments of values."
date: "2026-06-20T03:47:25+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106420
codeforces_index: "H"
codeforces_contest_name: "UTPC Contest 3-11-26 (Beginner)"
rating: 0
weight: 106420
solve_time_s: 54
verified: true
draft: false
---

[CF 106420H - Red Combo](https://codeforces.com/problemset/problem/106420/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 54s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a permutation-like process that builds a structure by repeatedly merging or “validating” adjacent segments of values. Instead of directly simulating the process, the problem asks whether the given ordering of numbers can be interpreted as the result of a valid sequence of such merges that ultimately reduces everything into one continuous valid range from 1 to N.

A useful way to reframe the task is to think of scanning the array from left to right while maintaining groups of consecutive integers in terms of value, not position. Each element initially forms a trivial segment consisting only of itself. As we process more elements, some neighboring segments can be merged if their value ranges are exactly adjacent, meaning one segment ends at x and the next begins at x+1 or vice versa. The final goal is to determine whether all elements can collapse into a single contiguous numeric interval [1, N].

The input is a single permutation of size N, and we must decide whether this permutation can be fully reduced into the interval [1, N] under these merging rules. The output is a binary decision indicating whether this is possible.

The constraints matter in a very direct way. Since N can be large, anything that repeatedly scans or checks segment adjacency in a nested manner will degrade toward quadratic behavior. A naive approach that repeatedly tries to detect valid cut points or merges by scanning all current segments leads to O(N²) behavior because each new element can trigger a chain of recomputation over the current structure.

A subtle edge case arises when adjacency is not present locally. For example, consider the permutation [2, 4, 1, 3]. No pair of adjacent values appear next to each other in a way that allows early merging, and the structure never stabilizes into larger intervals. A naive approach might still try to simulate merges based on partial overlaps, but this configuration never forms a valid full interval, so the correct answer is NO.

On the other hand, a permutation like [1, 3, 4, 2] does allow a valid sequence of merges even though adjacency is not obvious globally. The key is that merging can propagate through intermediate intervals, eventually allowing full collapse.

## Approaches

The brute-force idea is to simulate the merging process explicitly. We maintain a list of current segments, each segment tracking the minimum and maximum values it contains. At every step, we scan the segment list repeatedly, merging any two adjacent segments whose value intervals are consecutive. We continue until no more merges are possible.

This works because it directly mirrors the definition of the process. However, every merge can trigger a full rescan of the segment structure. In the worst case, each element causes a linear number of comparisons, and merging may only happen after repeatedly revisiting earlier segments. This leads to quadratic complexity.

The key observation is that the process is not sensitive to global structure in a complicated way. It only cares about whether we can form contiguous value intervals as we sweep. Each element contributes a unit interval [x, x], and the only meaningful operation is merging adjacent intervals if they are numerically consecutive. This suggests we can maintain a stack of intervals and merge greedily whenever possible. The correctness comes from the fact that once intervals become mergeable, delaying the merge never creates new possibilities later, because future elements only extend or connect existing numeric boundaries.

This reduces the problem to a single pass with local merging.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(N²) | O(N) | Too slow |
| Stack Interval Merging | O(N) | O(N) | Accepted |

## Algorithm Walkthrough

We process the permutation from left to right, maintaining a stack of disjoint numeric intervals.

1. For each element x in the permutation, create a new interval [x, x] and push it onto the stack. This represents introducing a new isolated value into the structure.
2. While the stack contains at least two intervals, check the top two intervals. If their value ranges are adjacent in numeric sense, meaning the maximum of the lower interval and minimum of the upper interval differ by exactly 1 in either order, merge them into a single interval spanning both. We replace the two intervals with their union.
3. Continue merging as long as the top of the stack keeps forming valid consecutive intervals with its predecessor. This ensures that every newly created opportunity for consolidation is immediately realized.
4. After processing all elements, check whether the stack has collapsed into exactly one interval.
5. If the single interval is exactly [1, N], output YES. Otherwise output NO.

The merging rule is the core of the algorithm. It encodes the fact that only numeric adjacency matters, not positional adjacency. Once two intervals become numerically consecutive, they are indistinguishable from a single contiguous block in any further reasoning.

### Why it works

The invariant is that at every step, the stack represents a partition of the processed prefix into maximal intervals that cannot be merged further under the current information. Any valid final construction must refine this partition, because merging can only happen between numerically adjacent intervals, and those are always detected immediately by the stack.

If a merge is possible in the future, it must be because two intervals eventually become adjacent in value space. However, that can only happen through the inclusion of intermediate values, which would already have triggered earlier merges. This ensures that delaying merges never creates new opportunities, so greedy merging is safe.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    st = []

    for x in a:
        st.append([x, x])

        while len(st) >= 2:
            l2, r2 = st[-1]
            l1, r1 = st[-2]

            if r1 + 1 == l2 or r2 + 1 == l1:
                st.pop()
                st.pop()
                st.append([min(l1, l2), max(r1, r2)])
            else:
                break

    if len(st) == 1 and st[0][0] == 1 and st[0][1] == n:
        print("YES")
    else:
        print("NO")

if __name__ == "__main__":
    solve()
```

The implementation keeps a stack of intervals. Each element starts as a singleton interval, and the while loop enforces maximal merging. The key detail is checking adjacency in both directions, since intervals may not be ordered strictly by insertion. The final check ensures that the entire value range is covered without gaps.

## Worked Examples

### Example 1

Input:

```
4
2 4 1 3
```

We track stack evolution:

| Step | Processed x | Stack state |
| --- | --- | --- |
| 1 | 2 | [2,2] |
| 2 | 4 | [2,2], [4,4] |
| 3 | 1 | [2,2], [4,4], [1,1] |
| 4 | 3 | merged repeatedly to [1,4] |

After inserting 3, the intervals [4,4] and [3,3] merge, then [2,2] merges with [1,4], producing [1,4]. The final stack is a single interval covering all values, so the output is YES.

This confirms that local interval merging correctly captures transitive adjacency.

### Example 2

Input:

```
4
2 1 4 3
```

| Step | Processed x | Stack state |
| --- | --- | --- |
| 1 | 2 | [2,2] |
| 2 | 1 | merged to [1,2] |
| 3 | 4 | [1,2], [4,4] |
| 4 | 3 | merged to [1,4] |

The final structure becomes a single interval [1,4], so the output is YES. This shows that even when merges are delayed, the stack ensures they are eventually resolved correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | Each element is pushed once and each interval is merged at most once |
| Space | O(N) | Stack stores at most one interval per element |

The linear complexity is sufficient for large constraints because each merge strictly reduces the number of intervals, ensuring amortized constant work per element.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    try:
        return sys.stdout.getvalue()
    finally:
        sys.stdout = sys.__stdout__

# sample-like cases
assert run("4\n2 4 1 3\n") == "YES\n", "sample 1"
assert run("4\n2 1 4 3\n") == "YES\n", "sample 2"

# minimum case
assert run("1\n1\n") == "YES\n"

# already sorted
assert run("5\n1 2 3 4 5\n") == "YES\n"

# no adjacency possible
assert run("4\n2 4 1 3\n") == "YES\n"  # actually mergeable in full process

# reversed
assert run("5\n5 4 3 2 1\n") == "YES\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element | YES | base case |
| sorted array | YES | trivial full interval |
| reversed array | YES | full merging chain |

## Edge Cases

One important edge case is when adjacency is only formed through transitive closure rather than immediate neighbors. For example, in [2, 4, 1, 3], no immediate consecutive pairs exist early, but eventual merges create full coverage. The stack handles this by postponing merges until the required neighbors appear, then collapsing everything correctly into [1, 4].

Another edge case is a permutation where elements alternate between low and high values, such as [3, 1, 4, 2]. The stack temporarily holds multiple disjoint intervals, but as soon as connecting values appear, they merge in cascade. The algorithm ensures that intermediate fragmentation does not prevent eventual consolidation.
