---
title: "CF 1015A - Points in Segments"
description: "We are given a one-dimensional number line from 1 to m, and several closed intervals placed on it. Each interval covers every integer point between its endpoints, including both ends."
date: "2026-06-16T22:25:43+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1015
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 501 (Div. 3)"
rating: 800
weight: 1015
solve_time_s: 88
verified: true
draft: false
---

[CF 1015A - Points in Segments](https://codeforces.com/problemset/problem/1015/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 1m 28s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a one-dimensional number line from 1 to m, and several closed intervals placed on it. Each interval covers every integer point between its endpoints, including both ends. Because intervals may overlap, some points can be covered multiple times while others might not be covered at all.

The task is to identify all integer points in the range from 1 to m that are not covered by any interval. In other words, we are painting segments on a line and asking which positions remain unpainted.

The constraints are very small: both the number of segments and the coordinate range are at most 100. This immediately tells us that even quadratic or cubic approaches are safe, and we do not need advanced data structures. A direct simulation over all points is already sufficient.

The main subtlety comes from correctly handling overlap and endpoints. Since segments are inclusive, a point exactly equal to l or r must be considered covered. A common mistake is to treat segments as half-open or to forget marking endpoints.

A second edge case arises when segments fully cover the entire range. For example, if we have [1, m], every point is covered and the answer must be 0 with no second line. A careless implementation that always prints a second line may fail formatting requirements.

Another corner case is overlapping single-point segments. For instance, [2,2], [2,2], [2,3]. The point 2 must still be treated as covered once, and duplicates must not affect correctness.

## Approaches

The most direct way to solve the problem is to check every point from 1 to m and test whether it lies inside at least one segment. For each point x, we scan all segments and check if there exists an i such that li ≤ x ≤ ri. If no such segment exists, we add x to the answer.

This works because the constraints are tiny: at most 100 points and 100 segments, leading to at most 10,000 checks, which is trivial.

However, the brute-force structure has redundancy. Each point independently re-checks all segments, even though coverage can be precomputed more efficiently. Since the coordinate range is small, we can instead maintain a boolean array mark[1..m], initially false, and mark every point covered by any segment in a single pass over segments. After processing all segments, we simply collect indices where mark is still false. This removes repeated scanning and makes the solution cleaner and more direct.

The key observation is that we do not need to answer queries online; we only need final coverage. That allows us to convert range marking into a simple array sweep.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n·m) per point scan → O(n·m²) | O(1) | Accepted but redundant |
| Optimal (marking array) | O(n·m) | O(m) | Accepted |

## Algorithm Walkthrough

We use a boolean array to record whether each position is covered.

1. Initialize an array covered of size m+1 with all values set to false. This represents that initially no points are covered by any segment.
2. Iterate over each segment [l, r]. For every integer x from l to r inclusive, set covered[x] = true. This directly encodes the definition of coverage.
3. After processing all segments, iterate from 1 to m. Collect all indices x such that covered[x] is still false. These are exactly the uncovered points.
4. Let k be the number of uncovered points. Print k, and if k > 0 print the collected points in any order, typically increasing order.

The reason we can safely do this is that each segment independently contributes coverage, and marking is idempotent. If multiple segments cover the same point, repeated assignments do not change the result.

### Why it works

At every step, covered[x] is true if and only if there exists at least one processed segment that contains x. Since we process all segments exactly once and only set values to true when coverage exists, no false positives are introduced. Likewise, any point not inside any segment is never marked, so it remains false. This creates a precise equivalence between the array state and the union of all segments.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m = map(int, input().split())

covered = [False] * (m + 1)

for _ in range(n):
    l, r = map(int, input().split())
    for x in range(l, r + 1):
        covered[x] = True

ans = []
for x in range(1, m + 1):
    if not covered[x]:
        ans.append(x)

print(len(ans))
if ans:
    print(*ans)
```

The solution uses a direct boolean marking array. The inner loop over each segment expands coverage explicitly, which is safe due to the small constraints. The final pass collects all unmarked points in increasing order.

A subtle implementation detail is the use of range(l, r + 1), which correctly includes the right endpoint. Missing the +1 would incorrectly exclude segment endpoints and produce wrong answers.

The output formatting condition is also important: when there are no uncovered points, we must not print an empty second line.

## Worked Examples

### Example 1

Input:

```
n = 3, m = 5
segments = [2,2], [1,2], [5,5]
```

| Segment | Marked range | Covered array (1..5) |
| --- | --- | --- |
| [2,2] | 2 | F T F F F |
| [1,2] | 1,2 | T T F F F |
| [5,5] | 5 | T T F F T |

After processing:

| x | covered[x] | action |
| --- | --- | --- |
| 1 | True | skip |
| 2 | True | skip |
| 3 | False | add |
| 4 | False | add |
| 5 | True | skip |

Output:

```
2
3 4
```

This confirms that overlapping segments are handled correctly and that uncovered gaps are detected precisely.

### Example 2

Input:

```
n = 1, m = 7
segments = [1,7]
```

| Segment | Marked range | Covered array (1..7) |
| --- | --- | --- |
| [1,7] | 1..7 | T T T T T T T |

| x | covered[x] | action |
| --- | --- | --- |
| 1 | True | skip |
| 2 | True | skip |
| 3 | True | skip |
| 4 | True | skip |
| 5 | True | skip |
| 6 | True | skip |
| 7 | True | skip |

Output:

```
0
```

This shows the full-coverage edge case where no output points exist.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n·m) | Each segment marks at most m positions, and n ≤ 100 |
| Space | O(m) | Boolean array storing coverage for each point |

The maximum number of operations is at most 10,000, which is trivial under the constraints. Memory usage is also negligible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque
    import sys
    input = sys.stdin.readline

    n, m = map(int, input().split())
    covered = [False] * (m + 1)

    for _ in range(n):
        l, r = map(int, input().split())
        for x in range(l, r + 1):
            covered[x] = True

    ans = [str(x) for x in range(1, m + 1) if not covered[x]]
    if ans:
        return str(len(ans)) + "\n" + " ".join(ans)
    else:
        return "0"

# provided sample
assert run("3 5\n2 2\n1 2\n5 5\n") == "2\n3 4"

# all covered
assert run("1 5\n1 5\n") == "0"

# no segments
assert run("0 3\n") == "3\n1 2 3"

# single point gaps
assert run("2 5\n1 1\n5 5\n") == "3\n2 3 4"

# overlapping segments
assert run("3 5\n1 3\n2 4\n4 5\n") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| full coverage | 0 | complete overlap edge case |
| no segments | all points | empty input behavior |
| endpoint-only gaps | middle uncovered region | off-by-one correctness |
| overlapping intervals | no gaps | union handling |

## Edge Cases

A key edge case is when all segments merge into a single continuous block. For example:

```
3 5
1 3
2 5
1 5
```

Processing marks every point from 1 to 5. The covered array becomes all true. The final scan finds no false entries, so ans is empty and we correctly output 0. Any implementation that unconditionally prints a second line would violate the required format here.

Another case is when segments only cover endpoints:

```
2 5
1 1
5 5
```

Only positions 2, 3, and 4 remain false. The marking loop ensures that only exact inclusive ranges are filled, so endpoints do not leak coverage into adjacent cells.
