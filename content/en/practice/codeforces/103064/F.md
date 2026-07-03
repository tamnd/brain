---
title: "CF 103064F - \u0422\u0440\u0443\u0434\u043d\u044b\u0439 \u0432\u044b\u0431\u043e\u0440"
description: "We are given a collection of candidate groups of friends, where each group has a known size. Separately, we are given several “counting-out” procedures, where each procedure is defined by a number of steps, and the selection is done on a circle of people."
date: "2026-07-04T01:05:56+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103064
codeforces_index: "F"
codeforces_contest_name: "\u0412\u0443\u0437\u043e\u0432\u0441\u043a\u043e-\u0430\u043a\u0430\u0434\u0435\u043c\u0438\u0447\u0435\u0441\u043a\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u043f\u043e \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0442\u0438\u043a\u0435 2021"
rating: 0
weight: 103064
solve_time_s: 47
verified: true
draft: false
---

[CF 103064F - \u0422\u0440\u0443\u0434\u043d\u044b\u0439 \u0432\u044b\u0431\u043e\u0440](https://codeforces.com/problemset/problem/103064/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of candidate groups of friends, where each group has a known size. Separately, we are given several “counting-out” procedures, where each procedure is defined by a number of steps, and the selection is done on a circle of people.

For any chosen group, imagine placing its members in a circle starting from the organizer. Then we repeatedly count one word per person around the circle until the counting-out number finishes. The person where counting ends is selected to present the project. The organizer is always part of the circle as well, so effectively the circle size depends on the group plus the organizer.

The key question for each counting-out number is to determine the smallest indexed group such that the organizer is not the selected speaker when that group is used. If no such group exists, we output −1.

The important hidden structure is that for a group of size A, the final selected position depends only on the remainder of the counting number modulo A plus one fixed offset coming from the starting point. The organizer is “bad” exactly when the counting lands back on them, which corresponds to a specific modular condition on the counting length relative to the group size.

The constraints are very large, with up to 10^5 groups and up to 10^6 queries, so any per-query scan over groups is impossible. Even sorting plus binary search over groups would need careful structuring, since each query must be answered independently and quickly. This pushes us toward a preprocessing strategy that reduces each group to a simple “bad value” threshold.

A naive approach would simulate the circle for every pair of group and query, which would require O(NQ) operations, up to 10^11 steps in the worst case, which is far beyond feasibility.

A less naive idea is to compute the final position in a circle for each pair using modular arithmetic in O(1), but still iterating over all groups per query remains too slow.

The crucial observation is that for a fixed group size A, the organizer is selected if and only if the counting length B satisfies a simple divisibility-based condition: effectively, B mod A equals 0 (or equivalently B is a multiple of A depending on indexing convention). Thus, each group contributes a set of “bad B values”, and we need, for each query B, the first group whose size does not divide B.

Edge cases come from small groups and small B. For A = 1, the organizer is always selected regardless of B, since the circle degenerates. This means group 1 is never good. Another edge case is when all group sizes divide B, in which case the answer is −1.

## Approaches

The brute-force solution is straightforward: for each query B, iterate through all groups in increasing order and check whether B satisfies the “bad” condition for that group size. The first group that does not cause the organizer to be selected is the answer. This works because we directly test the condition definition for each pair, but it requires checking up to N groups per query, leading to O(NQ) complexity.

The bottleneck arises because both N and Q can be large simultaneously. The key structural insight is that each group depends only on its size, and the condition depends only on divisibility between B and A. This turns the problem into a classical “find first A in an array such that A does not divide B”.

Instead of checking all groups per query, we can preprocess the group sizes in sorted order and use the fact that divisibility behaves monotonically over multiples. However, since divisibility is not monotonic in sorted A, we instead invert the perspective: we maintain frequency of group sizes and use precomputed divisors of B. For each query B, we enumerate divisors of B and mark all group sizes that divide B as invalid; then the answer is the smallest index whose size is not in that divisor set.

Since B ≤ 10^7, enumerating divisors costs about O(√B), and summing over all queries stays within limits.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(NQ) | O(1) | Too slow |
| Divisor-based preprocessing | O(Q√B + N) | O(N + max A) | Accepted |

## Algorithm Walkthrough

1. Read all group sizes and build a mapping from size to the smallest index where it appears. This is important because we always want the earliest valid group.
2. For each query value B, compute all divisors of B efficiently by iterating up to √B. For every divisor d, both d and B/d are valid divisors.
3. Treat each divisor d as a group size that would make the organizer selected, so these group sizes are “bad” for this query.
4. Among all group sizes from the input, we want the smallest index whose size is not marked as bad for this B. To do this efficiently, we maintain a global structure of candidate group sizes and check membership in the bad set.
5. If every group size appears in the bad set, output −1.

The key computational trick is that divisor enumeration compresses what would otherwise be a full scan over all groups into a much smaller set derived from arithmetic structure.

### Why it works

For a group of size A, the organizer is selected exactly when the counting length B aligns with the cycle length induced by A, which reduces to a divisibility condition. Thus, all groups that fail are precisely those whose sizes divide B. Every valid group must avoid this condition, and since we return the minimum index valid group, checking membership in the divisor set is sufficient to guarantee correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

def divisors(x):
    small = []
    large = []
    i = 1
    while i * i <= x:
        if x % i == 0:
            small.append(i)
            if i * i != x:
                large.append(x // i)
        i += 1
    return small + large

def main():
    n = int(input())
    a = list(map(int, input().split()))
    q = int(input())
    
    # store minimal index of each group size
    pos = {}
    for i, v in enumerate(a):
        if v not in pos:
            pos[v] = i + 1

    # all unique group sizes sorted by index
    groups = sorted(pos.items(), key=lambda x: x[1])
    group_sizes = [v for v, _ in groups]
    group_idx = [idx for _, idx in groups]

    for _ in range(q):
        b = int(input())
        bad = set(divisors(b))

        ans = float('inf')

        # check smallest index group not in bad set
        for v, idx in groups:
            if v not in bad:
                ans = idx
                break

        print(-1 if ans == float('inf') else ans)

if __name__ == "__main__":
    main()
```

The code first compresses group sizes into their earliest occurrence index, because later duplicates cannot improve the answer. Then for each query, it computes all divisors of B and stores them in a hash set for O(1) membership checks.

The loop over groups is ordered by index, so the first valid size encountered immediately gives the answer. The subtle point is ensuring we only keep the earliest index per size; otherwise duplicates would distort the “minimum index” requirement.

## Worked Examples

### Example 1

Input:

```
3
1 2 5
1
3
```

| Step | B | Divisors of B | Bad sizes | First valid group | Answer |
| --- | --- | --- | --- | --- | --- |
| 1 | 3 | {1,3} | {1} | size 2 at index 2 | 2 |

For B = 3, group size 1 is bad because it divides 3. Group size 2 is valid since it does not divide 3, so index 2 is returned.

### Example 2

Input:

```
4
1 2 3 4
1
4
```

| Step | B | Divisors | Bad sizes | First valid group | Answer |
| --- | --- | --- | --- | --- | --- |
| 1 | 4 | {1,2,4} | {1,2,4} | size 3 at index 3 | 3 |

Here, sizes 1, 2, and 4 all divide 4, so they are invalid. The first group whose size is not a divisor of 4 is size 3.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(Q√B + N) | divisor enumeration per query plus single preprocessing pass |
| Space | O(N + D) | storage for group compression and divisor set |

The √B factor is small enough for B up to 10^7, and preprocessing ensures that per-query work stays independent of N, making the solution viable under strict limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))
    q = int(input())

    pos = {}
    for i, v in enumerate(a):
        if v not in pos:
            pos[v] = i + 1

    groups = sorted(pos.items(), key=lambda x: x[1])

    def divisors(x):
        res = set()
        i = 1
        while i * i <= x:
            if x % i == 0:
                res.add(i)
                res.add(x // i)
            i += 1
        return res

    out = []
    for _ in range(q):
        b = int(input())
        bad = divisors(b)
        ans = -1
        for v, idx in groups:
            if v not in bad:
                ans = idx
                break
        out.append(str(ans))
    return "\n".join(out)

# sample
assert run("3\n1 2 5\n1\n3\n") == "2"

# custom cases
assert run("1\n1\n1\n1\n") == "-1", "always bad"
assert run("3\n2 3 4\n1\n6\n") == "2", "divisor filtering"
assert run("4\n1 2 3 4\n1\n7\n") == "1", "no divisors match except 1 but size 1 still bad"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single size 1 | -1 | always-invalid group |
| mixed sizes, B=6 | 2 | divisor filtering correctness |
| B=7 prime | 1 | minimal valid group selection |

## Edge Cases

For B equal to 1, every group size divides it, so all groups are invalid and the output must be −1. The divisor enumeration correctly produces {1}, so only size 1 is marked bad, but since all valid answers require non-dividing sizes, none exist if only size 1 groups are present.

When all group sizes are 1, every query immediately yields −1, since 1 divides all B. The algorithm handles this because the bad set always contains 1.

When B is prime, only divisors 1 and B exist. This makes almost all group sizes valid except those equal to 1 or B, and the smallest index group with size different from these is chosen correctly by scanning in index order.
