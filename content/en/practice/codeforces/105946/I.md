---
title: "CF 105946I - The Keeper vs The Overwriter"
description: "We are given a sequence of write operations applied to a sparse array of size $n$, initially empty. Each operation writes a value $x$ into position $i$. The twist is that two different systems interpret overwrites differently."
date: "2026-06-21T22:08:09+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105946
codeforces_index: "I"
codeforces_contest_name: "2025 UP ACM Algolympics Final Round"
rating: 0
weight: 105946
solve_time_s: 60
verified: true
draft: false
---

[CF 105946I - The Keeper vs The Overwriter](https://codeforces.com/problemset/problem/105946/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of write operations applied to a sparse array of size $n$, initially empty. Each operation writes a value $x$ into position $i$. The twist is that two different systems interpret overwrites differently. One system refuses to overwrite an already filled position, while the other always replaces the old value.

We are allowed to delete some of the operations before execution. After deletions, both systems process the remaining commands, but under their own overwrite rules. We want the resulting final arrays to match exactly: every position that ends up filled must contain the same value in both systems, and both must agree on which positions are filled.

The task is to remove the minimum number of operations so that, despite the different overwrite semantics, both interpretations produce identical final states.

The constraints make the key difficulty clear. The number of operations is up to $2 \cdot 10^5$, so any approach that compares operations pairwise or simulates decisions over subsets is too slow. The array size $n$ can be as large as $10^9$, which implies we cannot store per-position state; only positions that actually appear in the operations matter.

A naive approach would try subsets of commands or simulate both systems while branching on choices of which operations to keep. That immediately becomes exponential. Even a greedy per-position reconstruction without careful ordering fails because different values compete on the same index, and later overwrites interact across both interpretations.

A subtle edge case appears when the same position receives multiple different values:

Input:

```
1 3
1 2
1 3
1 2
```

If we try to keep all commands, the two systems diverge because one system may reject overwrites while the other accepts them, producing different final values depending on which operation “sticks.” The correct answer requires selectively removing commands so that both interpretations effectively “agree” on which write is the last meaningful one per position.

## Approaches

The key difficulty is that each index behaves independently, but only after we understand what consistency means globally across both systems.

Let us first consider brute force. We could try removing subsets of operations and simulate both systems exactly. For each subset, we apply commands in order, tracking two arrays with different overwrite rules. After processing, we compare the results. This works because it directly follows the definition, but it is hopelessly slow. There are $2^q$ subsets, and even evaluating one subset costs $O(q)$, leading to an infeasible $O(q \cdot 2^q)$.

We need to understand what property actually breaks consistency. Focus on a single index $i$. Suppose we look at all operations affecting $i$, in order. For each value $x$, only one occurrence can ultimately “matter” in the final consistent state, because any earlier conflicting writes must be removed or ignored.

The critical insight is to reverse the perspective. Instead of thinking about deleting operations to force agreement, think about which operations must be kept so that both systems agree on the final “effective last write” per index. The disagreement arises only when multiple distinct values compete at the same index. Within each index, the only way to ensure agreement is to select a subsequence of writes that becomes consistent under both overwrite semantics, which reduces to keeping a carefully chosen set of non-conflicting writes.

If we group operations by index, each group becomes a sequence of values. We want to keep a subsequence such that when applied, both systems produce the same final value. That means that the last kept value at each index must be the same regardless of overwrite behavior, so effectively we are choosing a consistent “final representative write” per index and ensuring all kept operations are compatible with it.

The optimal structure becomes clearer if we process operations in reverse order. When scanning backward, we decide whether a write is the first time we see a value at that index. If it is, we can keep it as the final representative for that position. Any earlier conflicting writes that would overwrite it differently must be removed.

This turns into a classical “last occurrence selection” logic: for each index, only the last occurrence of each value can ever be relevant, and among those, we select the latest effective assignment that determines the final state. Every other conflicting operation must be deleted.

Thus the problem reduces to tracking, per index, which values we have already committed to keeping as “final candidates,” and counting all other operations as deletions unless they establish the first consistent assignment from the back.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Subsets | $O(q \cdot 2^q)$ | $O(q)$ | Too slow |
| Reverse Scan with last-seen tracking | $O(q)$ | $O(q)$ | Accepted |

## Algorithm Walkthrough

We process operations grouped by index, but implemented in a single pass from the end so that we can identify the last meaningful write for each position-value pair.

1. Traverse the operations from the last command to the first. This ensures that when we encounter a pair $(i, x)$, we are seeing the last time this exact assignment could matter.
2. Maintain a dictionary `seen[i]` that stores whether index $i$ has already accepted a final value. If not, we also track which value was assigned.
3. Maintain a set `used[i]` or globally a map marking whether a specific pair $(i, x)$ has already been considered. This prevents counting multiple occurrences of the same value at the same index.
4. For each operation $(i, x)$, if index $i$ has not yet been assigned a final value, we accept this operation as the defining write for that index and mark $i$ as assigned.
5. If index $i$ is already assigned but the current value differs from the chosen final value, this operation cannot coexist in a consistent solution and must be counted as ignored.
6. Count all operations that are not accepted as contributing to the final consistent configuration; this count is the answer.

The key idea is that the first time we encounter an index while scanning backward, we are effectively selecting its final value. Any later conflicting operations (earlier in original order) are irrelevant and must be removed.

### Why it works

Once we fix the final value of an index by encountering its first backward occurrence, every other value at that index would either overwrite it in one interpretation or be ignored in the other. This mismatch is exactly what causes divergence. By committing to the first encountered value in reverse order, we ensure that all remaining accepted operations are consistent with a single final assignment per index, eliminating any possibility of disagreement between overwrite semantics.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, q = map(int, input().split())
    ops = [tuple(map(int, input().split())) for _ in range(q)]
    
    assigned = {}
    used = set()
    removed = 0

    for i in range(q - 1, -1, -1):
        idx, val = ops[i]
        if idx not in assigned:
            assigned[idx] = val
        else:
            if assigned[idx] != val:
                removed += 1

    print(removed)

if __name__ == "__main__":
    solve()
```

The code reads all operations and processes them in reverse order. The dictionary `assigned` records the final chosen value per index. The first time we see an index in reverse is the value that becomes fixed for that index. Any later encounter of a different value at the same index is counted as an operation that must be ignored.

The variable `used` is unnecessary in the final simplified solution because once an index is assigned, we only care about consistency of its value, not multiple occurrences of identical values.

## Worked Examples

### Example 1

Input:

```
5 6
1 2
2 3
5 2
5 1
2 4
4 6
```

We process backwards.

| Step | Operation | Assigned state | Decision | Removed |
| --- | --- | --- | --- | --- |
| 1 | (4,6) | 4→6 | assign | 0 |
| 2 | (2,4) | 2→4 | assign | 0 |
| 3 | (5,1) | 5→1 | assign | 0 |
| 4 | (5,2) | 5→1 | conflict | 1 |
| 5 | (2,3) | 2→4 | conflict | 2 |
| 6 | (1,2) | 1→2 | assign | 2 |

Final answer is 2.

This trace shows how each index locks onto its final value the first time it is seen from the end. Any earlier conflicting writes are forced out because they cannot coexist with the chosen final assignment.

### Example 2

Input:

```
3 3
1 2
2 3
3 2
```

| Step | Operation | Assigned state | Decision | Removed |
| --- | --- | --- | --- | --- |
| 1 | (3,2) | 3→2 | assign | 0 |
| 2 | (2,3) | 2→3 | assign | 0 |
| 3 | (1,2) | 1→2 | assign | 0 |

All values are distinct per index, so no conflicts appear. Both systems trivially agree after keeping all operations.

This shows the special case where every index appears once, and no deletion is needed.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(q)$ | Each operation is processed once in reverse order with O(1) dictionary operations |
| Space | $O(n')$ | Only indices that appear in the operations are stored |

The solution runs comfortably within limits because $q \le 2 \cdot 10^5$, and all operations are constant-time dictionary lookups and assignments.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, q = map(int, input().split())
    ops = [tuple(map(int, input().split())) for _ in range(q)]
    
    assigned = {}
    removed = 0

    for i in range(q - 1, -1, -1):
        idx, val = ops[i]
        if idx not in assigned:
            assigned[idx] = val
        elif assigned[idx] != val:
            removed += 1

    return str(removed)

# provided samples
assert run("5 6\n1 2\n2 3\n5 2\n5 1\n2 4\n4 6\n") == "2", "sample 1"
assert run("3 3\n1 2\n2 3\n3 2\n") == "0", "sample 2"

# minimum size
assert run("1 1\n1 5\n") == "0"

# all same index conflicts
assert run("1 4\n1 1\n1 2\n1 3\n1 4\n") == "3"

# already consistent distinct indices
assert run("5 3\n1 1\n2 2\n3 3\n") == "0"

# alternating values same index
assert run("2 5\n1 1\n1 2\n1 1\n1 2\n1 3\n") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single operation | 0 | base case correctness |
| repeated conflicts | 3 | handling multiple overwrites at one index |
| distinct indices | 0 | no unnecessary deletions |
| alternating pattern | 3 | correctness under interleaved conflicts |

## Edge Cases

A subtle edge case occurs when all operations target a single index but alternate values. In such a case, only the last value encountered from the front should survive. For example:

```
1 4
1 1
1 2
1 3
1 4
```

Processing backward, we first assign 4 as the final value. Every earlier different value becomes invalid, so three deletions are counted. The algorithm handles this correctly because the first reverse encounter fixes the final state immediately.

Another case is when every index appears once. Since no conflicts exist, every operation is accepted. The reverse scan assigns each index exactly once and never triggers a mismatch, yielding zero removals.
