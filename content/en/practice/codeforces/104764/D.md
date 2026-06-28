---
title: "CF 104764D - Jelly Swarm"
description: "We are given a set of distinct integer positions on a line, each representing a jellyfish. From these positions we must choose exactly $K$ of them and consider only those chosen points."
date: "2026-06-28T21:41:14+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104764
codeforces_index: "D"
codeforces_contest_name: "UTPC Contest 11-03-23 Div. 1 (Advanced)"
rating: 0
weight: 104764
solve_time_s: 62
verified: false
draft: false
---

[CF 104764D - Jelly Swarm](https://codeforces.com/problemset/problem/104764/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 2s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a set of distinct integer positions on a line, each representing a jellyfish. From these positions we must choose exactly $K$ of them and consider only those chosen points. Among all possible choices of $K$ points, we look at the largest distance between any two chosen points, and we want to make that quantity as small as possible.

Once a subset is chosen, Jerry can stand anywhere, but that does not change the fact that the spread of the group is determined only by the leftmost and rightmost selected jellyfish. The maximum distance inside any chosen set is simply the difference between its maximum and minimum element. So the task reduces to selecting a subset of size $K$ that minimizes the range.

The input size reaches $2 \cdot 10^5$, so any solution that tries all subsets or even all combinations is immediately impossible. A quadratic scan over pairs or subsets would require on the order of $10^{10}$ operations in the worst case, which is far beyond a 1 second limit. We should expect at most a near-linear or $N \log N$ solution.

A naive pitfall is forgetting that only the chosen extremes matter. For example, if positions are $[1, 2, 10, 11]$ and $K = 3$, choosing $\{1, 2, 11\}$ gives range 10, while $\{1, 2, 10\}$ gives range 9, even though both include the same small elements. The structure depends entirely on which three consecutive points in sorted order are chosen.

Another subtle issue is assuming that Jerry’s position matters for the distance. It does not. The problem asks for the maximum distance among jellyfish only, so Jerry is irrelevant to the objective function.

## Approaches

The brute-force idea is to enumerate every subset of size $K$, compute its minimum and maximum element, and take the smallest possible difference. This is correct because the definition of the objective is purely combinational over subsets. However, the number of such subsets is $\binom{N}{K}$, which becomes enormous even for moderate values of $N$. For $N = 200000$, this is completely infeasible, and even for $N = 40$ it is already too large.

The key structural observation is that once the positions are sorted, any optimal subset of size $K$ must consist of $K$ consecutive elements in that sorted order. If a subset skips an element inside its span, replacing a larger chosen element with that skipped smaller one can only reduce the range or keep it unchanged. This monotonicity collapses the search space from combinatorial to linear over windows.

Thus, after sorting, the problem becomes scanning all contiguous windows of length $K$ and computing the difference between endpoints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(\binom{N}{K} \cdot K)$ | $O(K)$ | Too slow |
| Sliding window on sorted array | $O(N \log N)$ | $O(1)$ extra | Accepted |

## Algorithm Walkthrough

1. Sort all jellyfish positions in increasing order. This ensures any group’s spread is determined by contiguous structure in this ordering rather than arbitrary selection.
2. Initialize an answer variable with a very large value. This will track the best (smallest) range encountered.
3. Iterate over every index $i$ such that a window of size $K$ starting at $i$ fits inside the array. For each $i$, consider the group formed by elements from $i$ to $i + K - 1$.
4. Compute the range of this group as $a[i + K - 1] - a[i]$. This is valid because within a sorted array, the maximum and minimum of a contiguous segment are its endpoints.
5. Update the answer with the minimum value over all such windows.

After finishing the scan, the stored answer is the smallest possible range.

### Why it works

After sorting, suppose an optimal subset is not contiguous in index order. Then there exists at least one element inside the interval between its minimum and maximum that is not selected. Replacing one of the chosen extreme elements with this missing interior element cannot increase the range, because it moves an endpoint inward or keeps it unchanged. Repeating this argument transforms any optimal subset into a contiguous block without worsening its objective value. Thus restricting attention to consecutive segments does not lose optimality.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    
    a.sort()
    
    ans = float('inf')
    
    for i in range(n - k + 1):
        ans = min(ans, a[i + k - 1] - a[i])
    
    print(ans)

if __name__ == "__main__":
    main()
```

The solution starts by reading input and sorting the position list. Sorting is essential because it converts the geometric problem on a line into a structured array problem where windows represent candidate groups.

The loop over starting indices enumerates all valid size-$K$ segments. For each segment, we compute its spread directly from endpoints. The minimum over all such spreads is stored. The use of a single pass ensures linear scanning after sorting.

A common mistake is trying to maintain a dynamic window without sorting first. That breaks the endpoint property and leads to incorrect range calculations. Another mistake is miscomputing indices, especially forgetting that the last valid start is $n - k$.

## Worked Examples

### Sample 1

Input:

```
5 3
8 6 1 5 5
```

Sorted array becomes $[1, 5, 5, 6, 8]$.

We evaluate windows:

| i | Window | Range |
| --- | --- | --- |
| 0 | [1, 5, 5] | 4 |
| 1 | [5, 5, 6] | 1 |
| 2 | [5, 6, 8] | 3 |

Minimum range is 1.

This shows that clustering around repeated or close values significantly reduces spread, and the optimal group always emerges from a contiguous segment.

### Sample 2

Input:

```
7 4
1 2 4 5 6 7 9
```

Sorted array is identical.

| i | Window | Range |
| --- | --- | --- |
| 0 | [1, 2, 4, 5] | 4 |
| 1 | [2, 4, 5, 6] | 4 |
| 2 | [4, 5, 6, 7] | 3 |
| 3 | [5, 6, 7, 9] | 4 |

Answer is 3.

This confirms that the optimal window is not necessarily at one end of the array, but anywhere the local density is highest.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N \log N)$ | sorting dominates, scan is linear |
| Space | $O(1)$ extra | only sorting and a few variables used |

The constraints allow up to $2 \cdot 10^5$ elements, and $O(N \log N)$ sorting is well within limits in Python. The linear scan afterward is negligible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    a.sort()

    ans = float('inf')
    for i in range(n - k + 1):
        ans = min(ans, a[i + k - 1] - a[i])
    return str(ans)

# provided samples
assert run("5 3\n8 6 1 5 5\n") == "1"
assert run("7 4\n1 2 4 5 6 7 9\n") == "3"

# custom cases
assert run("1 1\n100\n") == "0", "single element"
assert run("4 2\n1 10 20 30\n") == "9", "smallest pair dominates"
assert run("5 5\n1 2 3 4 5\n") == "4", "take all elements"
assert run("6 3\n1 2 2 100 101 102\n") == "0", "tight cluster"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 0 | minimal edge case |
| spaced numbers | 9 | correct pair window |
| take all | 4 | full range handling |
| clustered values | 0 | best local window detection |

## Edge Cases

A key edge case is when $K = 1$. The range of any single element is zero, and the algorithm handles this because every window of size 1 produces $a[i] - a[i] = 0$.

Another case is when all values are identical, although the statement guarantees distinct positions. If that restriction were removed, the sliding window still correctly returns zero for any $K$, since all endpoints match.

Large gaps between clusters test whether the algorithm correctly avoids picking extreme ends. For example, $[1, 2, 3, 100, 101]$ with $K = 3$ yields optimal window $[1,2,3]$ or $[100,101, \text{(invalid)}]$ depending on position, and the scan correctly selects the dense region rather than endpoints spanning the entire range.

The algorithm naturally handles all of these because every candidate is evaluated uniformly through endpoint differences after sorting.
