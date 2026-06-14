---
title: "CF 1533B - Nearest Point Function"
description: "We are given several test cases, each consisting of a sorted array of distinct integers. Think of these numbers as fixed points on a number line. A query point $y$ is chosen, and a function returns the closest point in the array to $y$ based on absolute distance."
date: "2026-06-14T18:31:16+07:00"
tags: ["codeforces", "competitive-programming", "*special", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1533
codeforces_index: "B"
codeforces_contest_name: "Kotlin Heroes: Episode 7"
rating: 0
weight: 1533
solve_time_s: 252
verified: true
draft: false
---

[CF 1533B - Nearest Point Function](https://codeforces.com/problemset/problem/1533/B)

**Rating:** -  
**Tags:** *special, implementation  
**Solve time:** 4m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several test cases, each consisting of a sorted array of distinct integers. Think of these numbers as fixed points on a number line. A query point $y$ is chosen, and a function returns the closest point in the array to $y$ based on absolute distance.

The function behaves normally when there is a unique closest point. It fails only when $y$ is exactly equally distant from two different array values, because then there are two valid answers and the tie is undefined.

So the task is not to simulate queries. Instead, we must determine whether there exists any integer $y$ that would land exactly in a “tie position” between two array elements.

The input sizes are large: the total number of elements across all test cases reaches $2 \cdot 10^5$, which rules out anything quadratic per test case. Any solution that tries all candidate query points or checks all integer positions between values would be far too slow because the gaps between numbers can be up to $10^9$, making enumeration impossible.

A common mistake is to assume that ties could involve non-adjacent elements. For example, one might think a point could be equally close to $x_i$ and $x_j$ even if there are values in between. That cannot happen, because any intermediate point would always be closer to one of the inner values. Another subtle mistake is forgetting that $y$ must be an integer. A midpoint that is not an integer does not create a valid crash even if it is geometrically centered.

## Approaches

The brute-force idea would be to iterate over all integer values between the minimum and maximum array elements and, for each $y$, compute the closest array point. If two points tie, we declare success. This is correct logically, but completely infeasible. The range of values can reach $10^9$, so even a single test case could require billions of checks.

The key observation is that a tie can only happen in a very structured situation. For any two adjacent elements $x_i$ and $x_{i+1}$, the set of points closer to $x_i$ lies on the left side of their midpoint, and the set closer to $x_{i+1}$ lies on the right side. A tie happens exactly at the midpoint.

Since we only care about integer $y$, this midpoint must be an integer, which happens only when $x_i + x_{i+1}$ is even. This reduces the entire problem to checking whether any adjacent pair has an even difference.

This transforms what looked like a geometric search into a simple scan over adjacent differences.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over all $y$ | $O(\text{range} \cdot n)$ | $O(1)$ | Too slow |
| Check adjacent parity | $O(n)$ per test case | $O(1)$ | Accepted |

## Algorithm Walkthrough

We reduce the problem to checking adjacent pairs in the sorted array.

1. Read the array of points, which is already sorted and contains no duplicates. This ordering ensures that any candidate tie must occur between neighbors.
2. For each adjacent pair $(x_i, x_{i+1})$, compute the difference $d = x_{i+1} - x_i$.
3. If $d$ is even, we immediately know there exists an integer midpoint $y = \frac{x_i + x_{i+1}}{2}$. At this value, both endpoints are equally distant, which guarantees a crash.
4. If no adjacent pair has an even difference, conclude that no integer midpoint exists anywhere in the array, so no tie is possible.
5. Repeat this process for all test cases independently.

The crucial decision point is step 3, because it connects arithmetic structure directly to geometric symmetry on the number line.

### Why it works

Any point $y$ is closest to a continuous region of the number line bounded by perpendicular bisectors between consecutive elements. These boundaries occur exactly at midpoints of adjacent pairs. Since the array is sorted, every region of ambiguity is defined only by neighbors, and no farther pair can compete without being dominated by intermediate points. Therefore, the existence of a valid crash point is equivalent to the existence of an integer midpoint between some adjacent pair.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    x = list(map(int, input().split()))
    
    ok = False
    for i in range(n - 1):
        if (x[i + 1] - x[i]) % 2 == 0:
            ok = True
            break
    
    print("YES" if ok else "NO")
```

The implementation directly follows the observation that only adjacent differences matter. The loop stops early once a valid pair is found, which is important for efficiency when large arrays contain an early even gap.

A subtle detail is that we compute the difference rather than the sum. Both are equivalent for parity, but subtraction avoids any concern about large intermediate values, even though Python handles large integers safely.

## Worked Examples

Consider the input:

```
6
1 2 5 7 9 11
```

| i | x[i] | x[i+1] | difference | even? | decision |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 2 | 1 | no | continue |
| 1 | 2 | 5 | 3 | no | continue |
| 2 | 5 | 7 | 2 | yes | crash possible |

At index 2, the midpoint is 6, which is exactly equidistant from 5 and 7, so the function fails.

Now consider:

```
6
1 2 5 8 9 12
```

| i | x[i] | x[i+1] | difference | even? | decision |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 2 | 1 | no | continue |
| 1 | 2 | 5 | 3 | no | continue |
| 2 | 5 | 8 | 3 | no | continue |
| 3 | 8 | 9 | 1 | no | continue |
| 4 | 9 | 12 | 3 | no | continue |

No adjacent pair has an even gap, so no integer midpoint exists that creates ambiguity. The function never has two equally close candidates.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ per test case | Each array is scanned once to check adjacent differences |
| Space | $O(1)$ | No additional data structures beyond input storage |

The total input size across all test cases is bounded by $2 \cdot 10^5$, so a linear scan per test case remains comfortably within time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdin
    input = stdin.readline
    
    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        x = list(map(int, input().split()))
        ok = False
        for i in range(n - 1):
            if (x[i + 1] - x[i]) % 2 == 0:
                ok = True
                break
        out.append("YES" if ok else "NO")
    return "\n".join(out)

# provided samples
assert run("""7
2
1 3
2
1 100
3
1 50 101
2
1 1000000000
2
1 999999999
6
1 2 5 7 9 11
6
1 2 5 8 9 12
""") == """YES
NO
NO
NO
YES
YES
NO"""

# custom cases
assert run("""1
2
10 14
""") == "YES", "even gap midpoint exists"

assert run("""1
2
10 13
""") == "NO", "odd gap no integer midpoint"

assert run("""1
3
1 4 7
""") == "NO", "all gaps odd"

assert run("""1
3
1 4 6
""") == "YES", "one even gap"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 10 14 | YES | basic even gap detection |
| 10 13 | NO | odd gap rejects correctly |
| 1 4 7 | NO | multiple odd gaps |
| 1 4 6 | YES | mixed gaps, one valid is enough |

## Edge Cases

For arrays of size two, the entire decision collapses to a single parity check. If the two values differ by an odd number, no integer lies exactly halfway, so no crash is possible. If the difference is even, the midpoint is an integer and always triggers ambiguity.

For large sparse arrays, the same logic still holds because intermediate points do not influence adjacency-based Voronoi boundaries. Even if values are far apart, only the parity of the distance matters, not the magnitude.

For sequences with uniform spacing like arithmetic progressions, the answer depends entirely on the step size. If the step is even, every adjacent pair generates a valid midpoint, producing a crash. If the step is odd, no midpoint is an integer and the function remains safe throughout.
