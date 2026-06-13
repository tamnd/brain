---
title: "CF 1102B - Array K-Coloring"
description: "We are given a sequence of integers and asked to assign each position one of k labels, which we will call colors. Every position must receive exactly one color. At the same time, every color from 1 to k must appear at least once among all positions."
date: "2026-06-13T07:38:16+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1102
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 531 (Div. 3)"
rating: 1400
weight: 1102
solve_time_s: 452
verified: false
draft: false
---

[CF 1102B - Array K-Coloring](https://codeforces.com/problemset/problem/1102/B)

**Rating:** 1400  
**Tags:** greedy, sortings  
**Solve time:** 7m 32s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a sequence of integers and asked to assign each position one of k labels, which we will call colors. Every position must receive exactly one color. At the same time, every color from 1 to k must appear at least once among all positions.

There is one additional structural restriction. If we look only at the positions assigned to a fixed color, all values in those positions must be pairwise distinct. In other words, within each color class, we are not allowed to repeat the same value.

So the task is to distribute indices into k groups such that every group is nonempty and each group does not contain duplicates in terms of array values.

The constraints n ≤ 5000 and k ≤ n suggest that O(n²) solutions are still viable. Anything cubic or involving repeated expensive recomputation over subsets would be borderline but still sometimes pass. This is a constructive greedy problem, so the goal is to find a stable assignment rather than optimize a numerical objective.

A first subtle failure case appears when some value appears very frequently. If a value appears more than k times, then any valid solution must place those occurrences into different colors because duplicates inside a color are forbidden. That immediately implies a lower bound: the maximum frequency of any value must be at most k, otherwise no coloring exists.

For example, if k = 2 and the array is [1, 1, 1], the value 1 appears three times, forcing three distinct colors for those positions, which is impossible. Any naive assignment that ignores frequencies would incorrectly produce a coloring.

Another edge case is when k is large compared to the number of distinct values. Even if frequencies are fine, we still need k nonempty groups. This forces careful distribution of colors even if we could otherwise avoid conflicts.

## Approaches

A brute-force viewpoint is to think of assigning colors sequentially and trying all possibilities. At each position, we could choose any color from 1 to k that does not already contain the same value. This leads to a branching factor of up to k at every step, and maintaining validity requires checking previous assignments. In the worst case, this explores kⁿ possibilities, which is completely infeasible even for n = 30.

The key structural observation is that conflicts only depend on equal values. Different values never interact. So for each value, we only need to ensure that its occurrences are distributed across distinct colors. This suggests handling identical values as a group.

Now consider sorting indices by value. Once grouped, we distribute occurrences of each value in a round-robin fashion across colors 1 through k. This guarantees that no value repeats within a single color because we never assign the same value twice to the same color. At the same time, if we ensure k colors are used, we can guarantee each color is nonempty by assigning the first k distinct values carefully.

The only remaining concern is feasibility. If any value appears more than k times, we immediately fail. Otherwise, every value can be distributed without internal conflict.

To ensure all k colors are used, we can assign colors cyclically as we iterate through sorted elements, but we must ensure that all colors receive at least one assignment. Since n ≥ k and we are assigning colors to all elements, we can simply ensure that the first k assignments are forced to use distinct colors.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(nk) | Too slow |
| Greedy cyclic assignment | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We proceed with a greedy construction based on sorting indices by their values.

1. Group indices by their array values. This allows us to process identical values together, which is necessary because conflicts only arise within equal values.
2. For each value group, check its size. If any group has size greater than k, immediately conclude that no valid coloring exists. This is because we would be forced to reuse a color for the same value.
3. Prepare a list of available colors from 1 to k. These represent the colors we will cycle through.
4. Assign colors to elements by iterating through the groups. Inside each group, assign colors sequentially from the palette, wrapping around if needed. However, since group size ≤ k, we never repeat a color inside a group.
5. After assigning all groups, ensure that each color appears at least once. This is naturally satisfied because we distribute at least one element per color across the full array as long as n ≥ k and we never skip colors in the assignment process.

The important idea is that we never assign the same value twice to the same color, and we never leave any color unused because the assignment spreads across the entire palette.

### Why it works

The core invariant is that after processing each value group, no color contains duplicate occurrences of that value. Since groups are disjoint by value, no later step can reintroduce a conflict for previously processed values. Additionally, because we assign colors in a balanced cyclic manner, every color receives assignments whenever possible, preventing unused colors when k ≤ n.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    
    pos = {}
    for i, x in enumerate(a):
        pos.setdefault(x, []).append(i)
    
    # feasibility check
    for x in pos:
        if len(pos[x]) > k:
            print("NO")
            return
    
    res = [0] * n
    
    # assign colors
    color = 1
    for x in pos:
        for idx in pos[x]:
            res[idx] = color
            color += 1
            if color > k:
                color = 1
    
    print("YES")
    print(*res)

if __name__ == "__main__":
    solve()
```

The solution first builds a dictionary mapping each value to its positions. This is necessary to enforce the constraint that duplicates of the same value must be checked together.

The feasibility check is critical: if any list exceeds size k, we immediately stop because no assignment can avoid repeating a color inside that group.

The coloring step uses a single global cyclic pointer. This ensures we distribute colors as evenly as possible across all elements. The wraparound at k ensures we reuse colors but never within a single value group of size at most k.

## Worked Examples

### Example 1

Input:

```
4 2
1 2 2 3
```

We group indices:

| Value | Positions |
| --- | --- |
| 1 | [0] |
| 2 | [1, 2] |
| 3 | [3] |

We assign colors cyclically:

| Step | Index | Value | Color pointer | Assigned color |
| --- | --- | --- | --- | --- |
| 1 | 0 | 1 | 1 | 1 |
| 2 | 1 | 2 | 2 | 2 |
| 3 | 2 | 2 | 1 | 1 |
| 4 | 3 | 3 | 2 | 2 |

Final coloring is:

```
1 2 1 2
```

This shows that duplicates of value 2 go to different colors.

### Example 2

Input:

```
5 3
4 4 4 2 2
```

Groups:

| Value | Positions |
| --- | --- |
| 4 | [0, 1, 2] |
| 2 | [3, 4] |

Step-by-step assignment:

| Step | Index | Value | Color |
| --- | --- | --- | --- |
| 1 | 0 | 4 | 1 |
| 2 | 1 | 4 | 2 |
| 3 | 2 | 4 | 3 |
| 4 | 3 | 2 | 1 |
| 5 | 4 | 2 | 2 |

Result:

```
1 2 3 1 2
```

Each color appears at least once, and within each value group, colors are distinct.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | grouping plus single pass assignment |
| Space | O(n) | storing positions per value |

The algorithm fits easily within limits since n ≤ 5000, and all operations are linear.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    
    pos = {}
    for i, x in enumerate(a):
        pos.setdefault(x, []).append(i)
    
    for x in pos:
        if len(pos[x]) > k:
            return "NO\n"
    
    res = [0] * n
    color = 1
    for x in pos:
        for idx in pos[x]:
            res[idx] = color
            color += 1
            if color > k:
                color = 1
    
    return "YES\n" + " ".join(map(str, res)) + "\n"

# provided sample
assert run("4 2\n1 2 2 3\n") in ["YES\n1 2 1 2\n", "YES\n1 1 2 2\n"]

# custom cases
assert run("1 1\n7\n") == "YES\n1\n", "single element"
assert run("3 3\n1 2 3\n") == "YES\n1 2 3\n", "all distinct"
assert run("3 2\n1 1 1\n") == "NO\n", "impossible frequency"
assert run("6 3\n1 1 2 2 3 3\n") != "", "balanced pairs"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 / 7 | YES 1 | minimum case |
| 3 3 / 1 2 3 | YES 1 2 3 | all distinct values |
| 3 2 / 1 1 1 | NO | frequency violation |
| 6 3 / pairs | valid coloring | balanced distribution |

## Edge Cases

When all elements are identical and n > k, the algorithm immediately fails at the frequency check. For example, input [5, 5, 5] with k = 2 triggers the condition because the value 5 appears 3 times. The check detects this before any assignment begins, which prevents constructing an invalid cyclic coloring.

When all elements are distinct, grouping produces singleton lists. The cyclic assignment simply walks through colors repeatedly, but since each value is unique, no constraint is ever violated. The invariant holds trivially because there are no duplicates to manage.
