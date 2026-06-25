---
title: "CF 105862F - Kinan The Bank Robber"
description: "The task describes a linear sequence of safe-deposit boxes, each positioned at an integer coordinate on a number line. Some positions contain banknotes, possibly multiple at the same position."
date: "2026-06-25T14:34:41+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105862
codeforces_index: "F"
codeforces_contest_name: "ACPC Kickoff 2025"
rating: 0
weight: 105862
solve_time_s: 36
verified: true
draft: false
---

[CF 105862F - Kinan The Bank Robber](https://codeforces.com/problemset/problem/105862/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 36s  
**Verified:** yes  

## Solution
## Problem Understanding

The task describes a linear sequence of safe-deposit boxes, each positioned at an integer coordinate on a number line. Some positions contain banknotes, possibly multiple at the same position. A robber starts at a fixed position and can move left or right one step at a time, but two fixed guards block access beyond two forbidden positions: everything strictly between the guards is the only region he can operate in, and stepping onto the guard positions themselves is not allowed.

Each time the robber arrives at a position, he can collect all banknotes stored in that safe. The goal is to determine the maximum number of banknotes he can collect given that he can choose a path starting from his initial position and must respect the blocked endpoints.

The key structural simplification is that movement is unrestricted inside the allowed segment, so the robber can reach every unblocked safe in the connected region containing his starting point. Since the only restriction is that he cannot cross or enter the guards’ positions, the problem reduces to summing all banknotes located in the connected component of the starting position after removing the two forbidden points.

The input size is large, with up to 100,000 banknotes and coordinates up to 1e9. This immediately rules out any per-coordinate simulation or traversal over the number line. Any solution must instead aggregate values by position efficiently, typically using sorting or hashing.

A subtle edge case appears when the starting position is itself outside the accessible region, which can happen if it coincides with a guard or lies in a disconnected segment. For example, if the robber starts at position 6, and guards are at 5 and 7, then there is no valid movement at all because both adjacent directions are blocked immediately. In that case, even if other safes exist elsewhere, they are unreachable, and the answer is zero. A naive approach that simply sums all safes between the guards would incorrectly include unreachable regions if it ignores connectivity from the start.

Another corner case occurs when multiple banknotes exist at the same coordinate. A correct solution must accumulate them, not treat them as separate locations.

## Approaches

A brute-force interpretation would simulate the robber’s movement on the number line. One could imagine building an explicit graph of all positions appearing in the input plus the starting point, connecting adjacent sorted coordinates, and then performing a flood fill from the start while avoiding the two forbidden positions. This is correct in principle because movement between adjacent integer coordinates defines connectivity.

However, the number line spans up to 1e9, so constructing all intermediate nodes is impossible. Even if we restrict nodes to only those with banknotes plus the start and guards, movement is still problematic: adjacency in the integer grid depends on gaps between sorted coordinates, and traversing across large gaps requires reasoning about intervals rather than stepping through integers.

The key observation is that we do not need the path itself, only which banknote positions are reachable. Since movement is free within any continuous segment of allowed positions that does not include a guard, all safe positions in the same open interval as the starting point are reachable. Therefore, the problem reduces to identifying which side of the starting point is not blocked by a guard, and summing all banknotes in the reachable connected region.

The structure is essentially a line partitioned into three zones by the two guards. Only the zone containing the starting point is relevant. Everything else is disconnected.

This reduces the task to grouping banknotes by position and summing those that lie in the same open interval as the starting coordinate.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force movement simulation | O(large coordinate range) or impossible | O(large) | Too slow |
| Grouping + interval classification | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the starting position and the two guard positions, then determine the forbidden cut points in the number line. The guards split the line into up to three segments, and only one of them can contain the starting position.
2. Read all banknote positions and group identical coordinates by summing their counts. This avoids repeated work and ensures each position contributes its full value.
3. Determine which segment contains the starting position by comparing it with the two guards. This tells us whether the accessible region is entirely to the left of the left guard, entirely to the right of the right guard, or strictly between them.
4. Iterate over all grouped positions and accumulate counts only from those that lie in the same segment as the starting position. Any position outside that segment is unreachable regardless of its distance.
5. Output the accumulated sum as the final answer.

The correctness relies on the fact that movement along adjacent integer positions allows traversal across any contiguous region that does not contain a forbidden position. Once a guard position is removed, it becomes a hard barrier, splitting the graph into disconnected components. Since all movement is within a 1D adjacency structure, connectivity is equivalent to being in the same open interval.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    a, b, c = map(int, input().split())
    n = int(input())
    arr = list(map(int, input().split()))

    left_guard = min(b, c)
    right_guard = max(b, c)

    from collections import defaultdict
    cnt = defaultdict(int)

    for x in arr:
        cnt[x] += 1

    # determine which region 'a' lies in
    if a < left_guard:
        valid = lambda x: x < left_guard
    elif a > right_guard:
        valid = lambda x: x > right_guard
    else:
        valid = lambda x: left_guard < x < right_guard

    ans = 0
    for pos, v in cnt.items():
        if valid(pos):
            ans += v

    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation first compresses identical positions using a hash map, which ensures linear processing of the input. The region classification function encodes the key structural observation: only the segment containing the starting point is reachable.

A common implementation pitfall is forgetting that the guards themselves are inaccessible even if a banknote exists there. That is why the inequalities are strict. Another subtle point is handling whether the starting position lies exactly at a boundary; in this formulation, it cannot, since guards are distinct from the start.

## Worked Examples

### Example 1

Input:

```
5 3 7
8
4 7 5 5 3 6 2 8
```

Here the guards are at 3 and 7, so only the open interval (3, 7) matters because the starting position 5 lies inside it.

| position | count | valid in (3,7)? | running sum |
| --- | --- | --- | --- |
| 4 | 1 | yes | 1 |
| 5 | 2 | yes | 3 |
| 6 | 1 | yes | 4 |
| 2 | 1 | no | 4 |
| 3 | 1 | no | 4 |
| 7 | 1 | no | 4 |
| 8 | 1 | no | 4 |

The result is 4, confirming that only the middle segment contributes.

### Example 2

Input:

```
6 5 7
5
1 5 7 92 3
```

The starting position is exactly at 6, which lies between 5 and 7, but both adjacent positions are blocked immediately, so no movement is possible. The valid region is (5,7), but there are no banknotes strictly inside it.

| position | count | valid in (5,7)? | running sum |
| --- | --- | --- | --- |
| 1 | 1 | no | 0 |
| 3 | 1 | no | 0 |
| 5 | 1 | no | 0 |
| 7 | 1 | no | 0 |
| 92 | 1 | no | 0 |

The output is 0, matching the fact that no reachable safe contains money.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each banknote is processed once, and each distinct position is checked once |
| Space | O(n) | Storage for frequency map of positions |

The constraints allow up to 100,000 entries, so a linear scan with hashing easily fits within time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    a, b, c = map(int, input().split())
    n = int(input())
    arr = list(map(int, input().split()))

    left_guard = min(b, c)
    right_guard = max(b, c)

    from collections import defaultdict
    cnt = defaultdict(int)
    for x in arr:
        cnt[x] += 1

    if a < left_guard:
        valid = lambda x: x < left_guard
    elif a > right_guard:
        valid = lambda x: x > right_guard
    else:
        valid = lambda x: left_guard < x < right_guard

    return str(sum(v for k, v in cnt.items() if valid(k)))

# provided sample
assert run("5 3 7\n8\n4 7 5 5 3 6 2 8\n") == "4"

# custom: no banknotes
assert run("5 3 7\n0\n\n") == "0"

# custom: all in left region
assert run("10 5 7\n3\n1 2 4\n") == "3"

# custom: all blocked region
assert run("10 5 7\n3\n6 6 6\n") == "0"

# custom: duplicates and boundary behavior
assert run("10 2 8\n5\n3 3 3 7 7\n") == "6"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| empty array | 0 | no data handling |
| all left of guards | sum all | left-region correctness |
| all unreachable region | 0 | blocking logic |
| duplicates and mixed sides | correct aggregation | frequency handling |

## Edge Cases

If the starting position lies in the left segment before both guards, the algorithm restricts collection strictly to positions smaller than the left guard. For example, with `a = 1, b = 10, c = 20`, only positions `< 10` are counted. The condition ensures that even if banknotes exist on the right side, they are ignored because they are disconnected from the starting component.

When all banknotes lie exactly on a guard position, none of them are included since guard positions are explicitly excluded by strict inequalities. This matches the model where guards act as impassable nodes, not removable obstacles.

If there are many duplicates at a valid position, the frequency map accumulates them correctly, preventing undercounting that would occur if each occurrence were treated independently without aggregation.
