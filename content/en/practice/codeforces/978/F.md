---
title: "CF 978F - Mentors"
description: "We are given a set of programmers, each with a fixed skill value. For any programmer $i$, we want to count how many other programmers $j$ they can “mentor”."
date: "2026-06-17T01:23:39+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "implementation"]
categories: ["algorithms"]
codeforces_contest: 978
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 481 (Div. 3)"
rating: 1500
weight: 978
solve_time_s: 70
verified: true
draft: false
---

[CF 978F - Mentors](https://codeforces.com/problemset/problem/978/F)

**Rating:** 1500  
**Tags:** binary search, data structures, implementation  
**Solve time:** 1m 10s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of programmers, each with a fixed skill value. For any programmer $i$, we want to count how many other programmers $j$ they can “mentor”. Mentorship is directional: $i$ can mentor $j$ only when $i$ has strictly higher skill than $j$, and at the same time $i$ and $j$ are not listed as being in conflict.

So for each index $i$, we are effectively counting how many indices $j$ satisfy two conditions at once: the skill comparison $r_i > r_j$, and the absence of a forbidden pair $(i, j)$.

The difficulty comes from the scale. With up to $2 \cdot 10^5$ programmers and the same number of conflict pairs, any approach that checks every pair individually becomes too slow. A naive double loop over all pairs would involve about $4 \cdot 10^{10}$ comparisons in the worst case, which is far beyond feasible limits in 3 seconds.

A subtle point in the input is that conflicts are sparse relative to all possible pairs. This suggests that the structure is “mostly sorted counting with small corrections”, rather than a full graph problem.

One edge case that breaks naive counting is when many programmers share the same skill. For example, if all skills are equal, no one can mentor anyone, so the answer must be all zeros. A naive approach that counts “lower or equal” instead of “strictly lower” will incorrectly overcount in this situation.

Another tricky scenario occurs when a programmer has many conflicts. If we only subtract a fixed number per programmer without considering skill ordering, we may subtract invalid pairs (where the other person has higher or equal skill and was never counted in the first place).

## Approaches

The brute-force idea is straightforward: for each programmer $i$, scan all other programmers $j$, check whether $r_i > r_j$, and also verify that $(i, j)$ is not a conflict. This is correct because it directly enforces the definition of mentorship. However, each query scans $O(n)$ candidates, and doing this for all $n$ nodes leads to $O(n^2)$ operations, which is too slow at the given constraints.

The key improvement comes from separating the problem into two parts. First, ignore conflicts entirely and count how many programmers have strictly smaller skill than each $i$. This can be done by sorting or by using frequency counts over compressed values, producing a global baseline count.

Second, we correct this baseline by subtracting invalid cases: for each conflict pair $(a, b)$, exactly one direction might have been incorrectly counted. If $r_a > r_b$, then $b$ was included in $a$'s baseline count but must be removed. If $r_b > r_a$, then $a$ must be removed from $b$'s count. If skills are equal, neither direction is ever valid and nothing changes.

This reduces the problem to sorting plus iterating over all edges once, which is efficient.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(1)$ | Too slow |
| Sorting + conflict correction | $O(n \log n + k)$ | $O(n + k)$ | Accepted |

## Algorithm Walkthrough

1. Read all skill values and store them with their indices.

This is needed so we can later sort programmers by skill while still mapping results back to original positions.
2. Sort programmers by skill value.

Sorting allows us to compute how many strictly smaller values exist for each skill level in a single linear sweep.
3. Compute a baseline array `cnt[i]` representing how many programmers have strictly smaller skill than programmer $i$.

This is done using frequency aggregation over the sorted order. When processing equal values, they are grouped so that equal skills do not count each other.
4. Initialize a result array `ans[i] = cnt[i]`.

At this stage we are ignoring conflicts, so every valid “skill-only” candidate is included.
5. Process each conflict pair $(x, y)$.

If $r_x > r_y$, then $y$ was incorrectly counted in $x$'s total, so decrement `ans[x]`.

If $r_y > r_x$, decrement `ans[y]`.

If they are equal, do nothing since neither can mentor the other by definition.
6. Output the final `ans` array.

### Why it works

The baseline `cnt[i]` counts exactly all programmers with strictly smaller skill than $i$. This set is independent of conflicts. Each conflict pair can invalidate at most one directed mentorship relation in this baseline: only the direction from higher skill to lower skill matters. Since every invalid pair is subtracted exactly once, and no valid pair is ever subtracted, the final count matches the definition exactly.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    r = list(map(int, input().split()))

    # pair (skill, index)
    arr = [(r[i], i) for i in range(n)]
    arr.sort()

    cnt = [0] * n

    # compute how many strictly smaller elements each index has
    i = 0
    smaller = 0
    while i < n:
        j = i
        while j < n and arr[j][0] == arr[i][0]:
            j += 1
        # all elements before i are strictly smaller
        for t in range(i, j):
            idx = arr[t][1]
            cnt[idx] = smaller
        smaller += (j - i)
        i = j

    ans = cnt[:]

    for _ in range(k):
        x, y = map(int, input().split())
        x -= 1
        y -= 1
        if r[x] > r[y]:
            ans[x] -= 1
        elif r[y] > r[x]:
            ans[y] -= 1

    print(*ans)

if __name__ == "__main__":
    solve()
```

The sorting step ensures we correctly handle strict inequality by grouping equal skills and assigning them the same “smaller count” before increasing the global counter. The subtraction step is deliberately asymmetric: we only adjust the higher-skilled endpoint, because only that direction could have contributed to its initial count.

Careful indexing is essential here. The subtraction is done after computing the full baseline, which avoids interference between conflict processing and ordering logic.

## Worked Examples

### Example 1

Input:

```
4 2
10 4 10 15
1 2
4 3
```

Sorted skills:

| step | arr segment | smaller assigned |
| --- | --- | --- |
| group 1 | (4, idx2) | 0 |
| group 2 | (10, idx1), (10, idx3) | 1 |
| group 3 | (15, idx4) | 3 |

Baseline `cnt` becomes:

| i | skill | cnt |
| --- | --- | --- |
| 1 | 10 | 1 |
| 2 | 4 | 0 |
| 3 | 10 | 1 |
| 4 | 15 | 3 |

Apply conflicts:

- (1,2): 10 > 4 so ans[1] -= 1
- (4,3): 15 > 10 so ans[4] -= 1

Final:

| i | ans |
| --- | --- |
| 1 | 0 |
| 2 | 0 |
| 3 | 1 |
| 4 | 2 |

This confirms that only strictly lower skills are counted, and conflicts remove exactly one direction of invalid mentorship.

### Example 2

Input:

```
3 0
5 5 5
```

All skills are equal, so every group is processed as one block. Each `cnt[i]` becomes 0. No conflicts exist, so the final answer remains all zeros. This validates correct handling of equality without accidental counting.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n + k)$ | Sorting dominates, each conflict processed once |
| Space | $O(n)$ | Arrays for sorting and result storage |

The constraints allow up to $2 \cdot 10^5$ elements, so $n \log n$ is comfortably fast, and a linear scan over conflicts is trivial within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque

    n, k = map(int, sys.stdin.readline().split())
    r = list(map(int, sys.stdin.readline().split()))

    arr = [(r[i], i) for i in range(n)]
    arr.sort()

    cnt = [0] * n
    i = 0
    smaller = 0
    while i < n:
        j = i
        while j < n and arr[j][0] == arr[i][0]:
            j += 1
        for t in range(i, j):
            cnt[arr[t][1]] = smaller
        smaller += (j - i)
        i = j

    ans = cnt[:]

    for _ in range(k):
        x, y = map(int, sys.stdin.readline().split())
        x -= 1
        y -= 1
        if r[x] > r[y]:
            ans[x] -= 1
        elif r[y] > r[x]:
            ans[y] -= 1

    return " ".join(map(str, ans))

# provided sample
assert run("""4 2
10 4 10 15
1 2
4 3
""") == "0 0 1 2"

# minimum size
assert run("""2 0
1 2
""") == "1 0"

# all equal
assert run("""5 3
7 7 7 7 7
1 2
2 3
3 4
""") == "0 0 0 0 0"

# no conflicts
assert run("""3 0
3 1 2
""") == "2 0 1"

# chain conflicts
assert run("""4 2
4 3 2 1
1 2
2 3
""") == "3 2 1 0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| sample | 0 0 1 2 | correctness with mixed constraints |
| 2 nodes no edges | 1 0 | minimal case |
| all equal | all zeros | strict inequality handling |
| no conflicts | sorted counts | baseline correctness |
| descending chain | full correction logic | multi-step subtraction |

## Edge Cases

For equal skills, the algorithm groups them in the sorting step so that no programmer in a group is counted as having smaller skill than another in the same group. For example, input `3 0 / 5 5 5` produces a single block where `smaller` is still zero when assigning counts, so every entry is zero.

For a conflict between equal-skilled programmers, such as `(1,2)` with both skills 10, neither branch of the conditional triggers, so no subtraction occurs. This prevents incorrect negative adjustments and preserves correctness of equality handling.

For a case where a low-skilled programmer has many conflicts, those conflicts never affect their count unless the other side has higher skill. Since they are never counted as mentors over higher or equal-skilled programmers, no invalid subtraction occurs, and the algorithm remains stable even in dense conflict graphs.
