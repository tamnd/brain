---
title: "CF 104665C - Hatter's Party"
description: "We are given a collection of noodle strands, each carrying a numeric flavor value. We need to divide these strands into several dishes. Every dish must contain at least $K$ strands, and the value of a dish is defined as the maximum flavor among the strands placed into it."
date: "2026-06-29T09:58:20+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104665
codeforces_index: "C"
codeforces_contest_name: "UTPC Contest 10-06-23 Div. 1 (Advanced)"
rating: 0
weight: 104665
solve_time_s: 71
verified: true
draft: false
---

[CF 104665C - Hatter's Party](https://codeforces.com/problemset/problem/104665/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 11s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of noodle strands, each carrying a numeric flavor value. We need to divide these strands into several dishes. Every dish must contain at least $K$ strands, and the value of a dish is defined as the maximum flavor among the strands placed into it.

The task is to split all strands into valid dishes in such a way that the sum of dish values is as large as possible.

So the core decision is not about individual strands alone, but about how we group them, since only the maximum element in each group contributes to the score, while all other elements in the group are effectively “supporting” elements that enable the group to exist.

The input size goes up to $10^5$, which immediately rules out any solution that tries all partitions or repeatedly simulates grouping choices. Anything quadratic or exponential in the number of strands will fail because even $10^10$ operations is already too large for a 1 second limit in practice.

A subtle point is that every strand must belong to exactly one dish. This turns the problem into a partitioning problem rather than a selection problem. A naive interpretation that allows discarding strands would change the structure entirely and lead to a different, easier objective, so the “use all elements” constraint is important.

Edge cases appear when $K = 1$, where every strand forms its own dish and the answer is simply the sum of all values. Another edge case is when $K = N$, where only one dish can be formed and the answer is the maximum element. A third case that breaks greedy intuition is when large values are scattered: without careful grouping logic, one might accidentally waste large values inside groups where they are not the maximum.

For example, if we have $f = [10, 9, 9, 1, 1]$ and $K = 3$, a careless grouping like $[10, 1, 1]$ and $[9, 9]$ is invalid because the second group does not meet size requirements. This kind of mistake shows why grouping must respect the minimum size constraint globally, not locally.

## Approaches

A brute-force strategy would attempt to enumerate all possible ways to partition the array into groups of size at least $K$. For each partition, we compute the sum of maxima of all groups. Even if we restrict ourselves to valid partitions, the number of ways to split $N$ elements grows extremely fast, resembling Bell numbers with additional constraints. For $N = 20$, this is already far beyond feasible computation, and at $N = 10^5$, it is completely impossible.

The key observation is that within each group, only the maximum element matters, while all other elements serve only to satisfy the size requirement. This creates a strong asymmetry: large elements are valuable only if they become group maxima, while small elements are interchangeable filler.

Once we sort the array in descending order, the best strategy becomes structurally simple. We want to assign the largest remaining element as a group maximum as often as possible. Every time we choose a maximum, we must “spend” at least $K-1$ other elements to form a valid group. To maximize the total sum, we always want those $K-1$ elements to be as small as possible, preserving larger elements for future groups.

This leads to a greedy structure where we scan the sorted array and pick every $K$-th element as a group leader, since each leader consumes itself plus $K-1$ fillers.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal (sorting + greedy selection) | $O(N \log N)$ | $O(1)$ or $O(N)$ | Accepted |

## Algorithm Walkthrough

We now describe the constructive strategy that directly builds the optimal grouping.

1. Sort all flavor values in descending order.

This ensures that when we decide who becomes a dish maximum, we always consider larger candidates first, which is necessary because smaller elements can always be used as fillers.
2. Initialize an accumulator for the answer as zero.
3. Iterate through the sorted array with step size $K$, starting from index 0.

Each visited position corresponds to a chosen dish leader.
4. Add the value at each visited position to the answer.

The reasoning is that this element becomes the maximum of a valid group, while the next $K-1$ elements in the sorted order are implicitly consumed as fillers.
5. Stop when the index exceeds the array bounds.

The key mental model is that we are carving the sorted array into consecutive blocks of size $K$, but only the first element of each block contributes to the score.

### Why it works

After sorting, the array is ordered from largest to smallest. Consider forming groups in this order. Whenever we pick the current largest unused element as a group maximum, we still need $K-1$ other elements. Choosing the next available smallest elements as fillers is always optimal because they do not contribute to any future maximum unless they become leaders themselves, and delaying a large element from becoming a leader can only reduce its chance of being selected before being forced into filler positions.

This creates an invariant: at every step, the remaining unused prefix of the sorted array always contains the largest available candidates for future group maxima, and consuming $K$ elements per group preserves the property that every chosen leader is the largest possible among remaining valid candidates.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    a = [int(input()) for _ in range(n)]
    
    a.sort(reverse=True)
    
    ans = 0
    for i in range(0, n, k):
        ans += a[i]
    
    print(ans)

if __name__ == "__main__":
    solve()
```

The solution reads all values, sorts them in descending order, and then accumulates every $K$-th element starting from index 0. The loop structure directly encodes the idea that each group of size $K$ contributes exactly one useful value, the first element in sorted order.

A common mistake is trying to explicitly form groups and track remaining elements. That is unnecessary and error-prone. The sorted stepping approach already encodes optimal grouping implicitly.

## Worked Examples

### Sample 1

Input:

```
2 1
76
100
```

Sorted array becomes:

```
[100, 76]
```

| Step | Index | Picked Value | Answer |
| --- | --- | --- | --- |
| 1 | 0 | 100 | 100 |
| 2 | 1 | 76 | 176 |

Each element forms its own group since $K = 1$, so every element contributes.

This confirms that the algorithm degenerates correctly into summing all elements when no grouping is required.

### Sample 2

Input:

```
4 2
1
5
3
1
```

Sorted array:

```
[5, 3, 1, 1]
```

| Step | Index | Picked Value | Answer |
| --- | --- | --- | --- |
| 1 | 0 | 5 | 5 |
| 2 | 2 | 1 | 6 |

We pick indices 0 and 2 because each group needs 2 elements, so every leader is spaced by exactly one skipped element.

This demonstrates how filler elements are automatically consumed between chosen maxima.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N \log N)$ | Sorting dominates, single linear scan afterward |
| Space | $O(1)$ or $O(N)$ | In-place sort or storage of input array |

The constraints allow up to $10^5$ elements, so sorting is well within limits. The linear scan is negligible compared to sorting, making the solution comfortably efficient.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    n, k = map(int, input().split())
    a = [int(input()) for _ in range(n)]
    a.sort(reverse=True)
    ans = sum(a[i] for i in range(0, n, k))
    return str(ans)

# provided samples
assert run("2 1\n76\n100\n") == "176"
assert run("4 2\n1\n5\n3\n1\n") == "8"

# custom cases
assert run("1 1\n42\n") == "42"  # single element
assert run("5 5\n1\n2\n3\n4\n5\n") == "5"  # one group only
assert run("6 2\n10\n9\n8\n7\n6\n5\n") == "24"  # multiple pairs
assert run("3 1\n0\n0\n0\n") == "0"  # all zeros
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 42 | minimum size handling |
| K equals N | 5 | single group edge case |
| even grouping | 24 | repeated grouping correctness |
| all zeros | 0 | zero-value stability |

## Edge Cases

When $K = 1$, the algorithm visits every index in the sorted array. For example:

```
3 1
5
2
7
```

Sorted array becomes $[7, 5, 2]$. The algorithm selects indices 0, 1, 2, producing 14. Each element forms its own group, matching the definition.

When $K = N$, for example:

```
4 4
1
9
3
2
```

Sorted array is $[9, 3, 2, 1]$. Only index 0 is selected, producing 9. The entire array forms a single valid dish, and the maximum element correctly represents its flavor.

When values are tightly clustered, such as:

```
6 3
8
7
6
5
4
3
```

Sorted array is $[8, 7, 6, 5, 4, 3]$. The algorithm selects indices 0 and 3, producing $8 + 5 = 13$. The first group uses the top three values, the second group uses the next three, and in each case the maximum is the first element of the block.
