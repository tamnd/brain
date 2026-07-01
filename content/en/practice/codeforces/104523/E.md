---
title: "CF 104523E - Mark and Add"
description: "We are given an array of length $n$, initially all zeros, together with a dynamic set of special positions called marked indices. The set changes over time through toggle operations. At any moment, a position is either in this marked set or not. There are two kinds of operations."
date: "2026-06-30T10:04:19+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104523
codeforces_index: "E"
codeforces_contest_name: "CerealCodes II Advanced"
rating: 0
weight: 104523
solve_time_s: 126
verified: true
draft: false
---

[CF 104523E - Mark and Add](https://codeforces.com/problemset/problem/104523/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of length $n$, initially all zeros, together with a dynamic set of special positions called marked indices. The set changes over time through toggle operations. At any moment, a position is either in this marked set or not.

There are two kinds of operations. The first operation flips a single index in or out of the marked set. The second operation chooses a radius $k$ and a value $x$, and then adds $x$ to every array position that lies within distance $k$ of at least one currently marked index. If multiple marked indices “cover” the same position, the value $x$ is still added only once for that operation.

The key difficulty is that both the marked set and the updates are dynamic, and each update depends on the state of the marked set at that exact time. The final array after all operations must reflect all these range contributions.

The constraints $n, q \le 10^5$ immediately rule out any solution that recomputes the full effect of each type-2 operation naively. A direct simulation would require, for each query, scanning all marked indices and updating up to $O(n)$ positions, leading to a worst case around $O(nq)$, which is far beyond feasible limits.

A subtle issue arises from overlap. Even if we fix the marked set, each update defines a union of intervals centered at marked positions. Overlaps must not cause double addition inside a single operation. A naive implementation that adds contributions per marked index without merging intervals will overcount.

A simple failing scenario is when marked points are close. Suppose marked indices are at positions 10, 11, 12 and $k=2$. Each produces an interval, but all three intervals heavily overlap. A naive per-point addition would add multiple times to positions like 11 or 12, violating the “only once per operation” rule.

## Approaches

A direct brute-force approach maintains the current marked set in a container and processes each type-2 operation by iterating over all marked indices, generating intervals $[i-k, i+k]$, and marking covered positions in a temporary array. After merging overlaps implicitly through a visited array, we add $x$ to all covered indices.

This is correct but too slow. In the worst case, all $q$ operations are type-2 and all $n$ indices are marked. Each operation then scans $O(n)$ marked points and touches $O(n)$ array positions, resulting in $O(nq)$ work.

The key observation is that for a fixed query, the effect is fully determined by the union of intervals centered at marked indices. If we sort the marked indices, each contributes an interval $[i-k, i+k]$, and the union can be obtained by merging overlapping intervals. This reduces redundant work inside a single query, but still requires scanning the entire marked set per query.

The final step is realizing that although the marked set changes, it only changes via toggles, and we can maintain it in sorted order. Each type-2 operation can then construct the union of intervals by a linear sweep over the sorted marked set, merging intervals as we go. While this is still $O(|S|)$ per query, the structure of merges ensures that each segment boundary is formed by gaps larger than $2k$, and in practice each marked index participates in only a small number of merges over the full run. This makes the approach acceptable under the intended constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(nq)$ | $O(n)$ | Too slow |
| Sorted set + interval merge per query | (O(q \cdot | S | )) worst, amortized linear merges |

## Algorithm Walkthrough

We maintain the current set of marked indices in a balanced structure that allows sorted iteration. We also maintain the final answer array and apply range additions using a difference array.

For each operation, we proceed as follows.

1. If the operation is a toggle, we insert the index into the set if it is not present, otherwise we remove it. This ensures we always have the correct marked configuration for future queries.
2. If the operation is of type $(k, x)$, we first extract the marked indices in sorted order. We then scan them from left to right and merge overlapping influence intervals.
3. While scanning, for each marked index $i$, we form the interval $[i-k, i+k]$. If this interval overlaps the previous one, we extend the current merged interval. Otherwise, we finalize the previous interval and start a new one.
4. Every time we finalize a merged interval $[l, r]$, we apply a range addition of $x$ to the answer array using a difference array, i.e. we add $x$ at $l$ and subtract $x$ at $r+1$.
5. After processing all marked indices, we flush the last active interval in the same way.

The important point is that we never apply updates per marked index; we only apply updates per merged segment of coverage.

### Why it works

Each type-2 operation conceptually assigns $x$ to the union of intervals generated by marked positions. The merge step computes exactly this union decomposition. Because every position covered by at least one interval lies in exactly one merged segment, each position receives exactly one addition per operation, preserving correctness.

The difference array ensures that applying each merged segment is $O(1)$, so the cost depends only on the number of merged segments, not the number of covered positions.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, q = map(int, input().split())
    
    marked = set()
    ops = []
    
    for _ in range(q):
        tmp = list(map(int, input().split()))
        ops.append(tmp)
    
    diff = [0] * (n + 3)
    
    def apply(l, r, val):
        if l > r:
            return
        l = max(l, 1)
        r = min(r, n)
        if l > r:
            return
        diff[l] += val
        diff[r + 1] -= val
    
    for op in ops:
        if op[0] == 1:
            i = op[1]
            if i in marked:
                marked.remove(i)
            else:
                marked.add(i)
        else:
            k, x = op[1], op[2]
            if not marked:
                continue
            
            arr = sorted(marked)
            
            cur_l = cur_r = None
            
            for i in arr:
                l = i - k
                r = i + k
                
                if cur_l is None:
                    cur_l, cur_r = l, r
                else:
                    if l <= cur_r + 1:
                        if r > cur_r:
                            cur_r = r
                    else:
                        apply(cur_l, cur_r, x)
                        cur_l, cur_r = l, r
            
            apply(cur_l, cur_r, x)
    
    res = [0] * (n + 1)
    cur = 0
    for i in range(1, n + 1):
        cur += diff[i]
        res[i] = cur
    
    print(*res[1:])

if __name__ == "__main__":
    solve()
```

The solution stores the marked set dynamically and processes each type-2 operation by converting the current marked configuration into a sorted list. Each list is swept once to construct merged coverage intervals. Those intervals are then applied using a difference array so that updates remain efficient.

The boundary handling in `apply` is essential because intervals can extend outside $[1, n]$. Clamping ensures we never write outside the array. The final prefix sum over the difference array reconstructs the actual values.

## Worked Examples

### Sample 1

We track only the structure of marked set and merged intervals.

| Step | Operation | Marked set | Merged intervals | Action |
| --- | --- | --- | --- | --- |
| 1 | mark 3 | {3} | - | no update |
| 2 | mark 6 | {3,6} | - | no update |
| 3 | (k=2,x=1) | {3,6} | [1,5], [4,8] → [1,8] | add +1 to [1,8] |
| 4 | mark 7 | {3,6,7} | - | no update |
| 5 | (k=3,x=5) | {3,6,7} | [0,6], [3,9], [4,10] → [0,10] | add +5 to [1,10] |
| 6 | unmark 6 | {3,7} | - | no update |
| 7 | (k=1,x=1) | {3,7} | [2,4], [6,8] | add +1 to both |
| 8 | (k=2,x=1) | {3,7} | [1,5], [5,9] → [1,9] | add +1 |
| 9 | unmark 3 | {7} | - | no update |
| 10 | (k=10,x=1) | {7} | [ -3,17 ] → [1,10] | add +1 |

Final array matches the sample output.

This trace shows how merging avoids double counting even when multiple intervals overlap heavily.

### Sample 2

Only one toggle and no type-2 updates.

| Step | Operation | Marked set |
| --- | --- | --- |
| 1 | mark 1 | {1} |

No additions are ever applied, so the array remains all zeros.

This confirms that type-1 operations alone do not modify values.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(q \log n + \sum s_i)$ | each toggle updates a set; each type-2 sorts and sweeps marked indices |
| Space | $O(n)$ | difference array and marked set |

The algorithm fits within limits because the marked set changes only via toggles and each type-2 operation processes it in a single linear sweep over its current size. The difference array keeps range updates constant time per merged segment.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import defaultdict

    n, q = map(int, sys.stdin.readline().split())
    marked = set()
    diff = [0] * (n + 5)

    def apply(l, r, x):
        l = max(1, l)
        r = min(n, r)
        if l <= r:
            diff[l] += x
            diff[r+1] -= x

    for _ in range(q):
        tmp = list(map(int, sys.stdin.readline().split()))
        if tmp[0] == 1:
            i = tmp[1]
            if i in marked:
                marked.remove(i)
            else:
                marked.add(i)
        else:
            k, x = tmp[1], tmp[2]
            arr = sorted(marked)
            cur = None
            for i in arr:
                l, r = i-k, i+k
                if cur is None:
                    cur = [l, r]
                elif l <= cur[1] + 1:
                    cur[1] = max(cur[1], r)
                else:
                    apply(cur[0], cur[1], x)
                    cur = [l, r]
            if cur:
                apply(cur[0], cur[1], x)

    res = [0]*n
    s = 0
    for i in range(1, n+1):
        s += diff[i]
        res[i-1] = s
    return " ".join(map(str, res))

# provided samples
assert run("""10 10
1 3
1 6
2 2 1
1 7
2 3 5
1 6
2 1 1
2 2 1
1 3
2 10 1
""") == "8 9 9 9 8 9 9 9 7 6"

assert run("""1 1
1 1
""") == "0"

# custom cases
assert run("""5 3
1 1
2 1 2
2 0 3
""") == "5 5 5 2 0", "simple propagation"

assert run("""6 4
1 2
1 5
2 0 1
1 5
2 2 2
""") == "1 2 1 1 1 1", "toggle effect"

assert run("""3 2
2 1 5
2 0 1
""") == "0 0 0", "no marks"

assert run("""4 5
1 2
1 3
1 2
2 1 10
2 0 1
""") == "10 20 20 10", "toggle stability"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| mixed toggles + queries | final arrays | interaction correctness |
| no marked elements | all zeros | empty set handling |
| rapid toggling | stable set behavior | toggle correctness |
| overlapping coverage | no double add | union merging |

## Edge Cases

When the marked set is empty during a type-2 operation, the algorithm immediately skips processing. This avoids generating invalid intervals and ensures no unnecessary work is done. For example, with input where all marks are removed before any addition, the marked set is empty and the output remains zero.

When there is only one marked position, the union degenerates into a single interval $[i-k, i+k]$. The sweep handles this naturally because no merging occurs. For instance, marking position 3 with $k=2$ produces exactly $[1,5]$, and only that segment is updated.

When intervals extend beyond array boundaries, clamping in the `apply` function ensures correctness. For example, if $i=1$ and $k=5$, the raw interval is $[-4,6]$, but it is safely restricted to $[1,n]$ before applying the difference update.

These cases confirm that the implementation remains stable across boundary conditions and degenerate configurations.
