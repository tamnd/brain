---
title: "CF 1538A - Stone Game"
description: "We are given a row of stones, each stone having a distinct strength value. In one move, we are allowed to remove only one of the two boundary stones, either the leftmost or the rightmost remaining stone."
date: "2026-06-14T18:57:09+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "dp", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1538
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 725 (Div. 3)"
rating: 800
weight: 1538
solve_time_s: 219
verified: true
draft: false
---

[CF 1538A - Stone Game](https://codeforces.com/problemset/problem/1538/A)

**Rating:** 800  
**Tags:** brute force, dp, greedy  
**Solve time:** 3m 39s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a row of stones, each stone having a distinct strength value. In one move, we are allowed to remove only one of the two boundary stones, either the leftmost or the rightmost remaining stone. Eventually, we want to remove both the weakest stone and the strongest stone in the array.

The task is to determine the minimum number of such boundary removals needed until both extreme values have been deleted.

The key observation from the constraints is that each test case is small, with at most 100 stones. This immediately rules out any need for advanced data structures or simulation over many states. Even an O(n) or O(n^2) solution per test case is easily fast enough.

A naive interpretation might suggest simulating all possible sequences of left and right deletions until both target elements are removed, but that leads to an exponential number of possibilities. Even for n = 100, that is completely infeasible.

There are a few subtle cases that break careless reasoning. First, it is not always optimal to remove from one side until both targets are gone, because depending on positions of the minimum and maximum values, the best strategy might involve removing from the left first or the right first or a mix of both.

For example, if the minimum is near the left end and the maximum is near the right end, we might want to remove the closer side for each. But if both are on the same side, removing from that side alone might be optimal.

A second edge case is when one extreme is already close to an end but the other is deep inside the array. Greedy removal from one side without comparing both directions can easily overcount moves.

## Approaches

A brute-force approach would try every sequence of removing left or right until both the minimum and maximum elements are removed. Each state is defined by the current subarray, and from each state we branch into two possibilities. This forms a binary tree of depth up to n, which leads to O(2^n) states. Even with pruning, the structure is still exponential because each decision affects future availability of both targets.

The key insight is to stop thinking about sequences and instead think about positions. The only thing that matters is where the minimum and maximum elements are located in the original array. Once we know their indices, the problem becomes equivalent to shrinking the array from both ends until both indices are removed.

If we denote the positions of the minimum and maximum elements as i and j, then we only care about how many removals are needed to eliminate both indices. There are only three meaningful strategies. We can remove from the left until both are gone, remove from the right until both are gone, or remove from both ends: some from the left and some from the right.

This reduces the problem to evaluating a constant number of cases based on i and j.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Optimal | O(n) per test | O(1) | Accepted |

## Algorithm Walkthrough

1. Scan the array to locate the index of the minimum element and the index of the maximum element. These positions fully determine the rest of the computation because all other values are irrelevant to the removal process.
2. Let i be the minimum index and j be the maximum index. Without loss of generality, assume i <= j. If not, swap them. This normalization avoids case splitting later.
3. Compute three candidate strategies. First, remove everything from the left up to the farther of i and j. This takes max(i, j) + 1 moves because we index from zero.
4. Second, remove everything from the right up to the closer of i and j. This takes n - min(i, j) moves, since we delete from the right until both positions disappear.
5. Third, remove the left part up to i and the right part up to j independently. This takes (i + 1) + (n - j) moves. This corresponds to first deleting all elements before i, then deleting all elements after j.
6. The answer is the minimum of these three values, since each corresponds to a valid deletion strategy that guarantees both target elements are removed.

### Why it works

The state of the game is always a contiguous subarray, so any sequence of moves corresponds to shrinking boundaries inward. The minimum and maximum elements must both lie outside the final remaining segment. Therefore, any valid strategy is equivalent to choosing a final segment that excludes both indices. The cost of reaching that segment is determined only by how many elements are removed from the left and right, which reduces the problem to minimizing over boundary positions.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    
    mn = min(range(n), key=lambda i: a[i])
    mx = max(range(n), key=lambda i: a[i])
    
    i, j = mn, mx
    if i > j:
        i, j = j, i
    
    # three strategies
    left_only = j + 1
    right_only = n - i
    both = (i + 1) + (n - j)
    
    print(min(left_only, right_only, both))
```

The solution first identifies the indices of the minimum and maximum values using a linear scan. It then normalizes their order so that the minimum index comes first. This allows a clean formulation of the three removal strategies without case splitting.

The first strategy removes from the left until the rightmost of the two targets disappears. The second removes from the right until the leftmost disappears. The third splits removal between both ends, which corresponds to isolating a middle segment that still contains neither extreme.

All arithmetic directly counts how many deletions are required, and no simulation of the process is needed.

## Worked Examples

### Example 1

Input: `[1, 5, 4, 3, 2]`

Minimum is at index 0, maximum is at index 1.

| Step | i (min) | j (max) | left_only | right_only | both | answer |
| --- | --- | --- | --- | --- | --- | --- |
| init | 0 | 1 | 2 | 5 | 4 | 2 |

The best strategy is to remove the leftmost twice, eliminating both 1 and 5 quickly. This shows that focusing only on one side can outperform mixed removals.

### Example 2

Input: `[2, 1, 3, 4, 5, 6, 8, 7]`

Minimum is at index 1, maximum is at index 6.

| Step | i | j | left_only | right_only | both | answer |
| --- | --- | --- | --- | --- | --- | --- |
| init | 1 | 6 | 7 | 7 | 3 + 2 = 5 | 5 |

Here the optimal solution is to remove a prefix up to the minimum and a suffix after the maximum. This avoids wasting moves on the middle region.

These two examples show the contrast between extreme clustering and separated extremes, which is exactly what the three-case formula captures.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | One scan to find min and max indices |
| Space | O(1) | Only a few variables are used |

The constraints allow up to 100 test cases with n up to 100, so a linear scan per case is trivial. The solution runs well within limits.

## Test Cases

```python
import sys, io

def solve(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline
    
    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        mn = min(range(n), key=lambda i: a[i])
        mx = max(range(n), key=lambda i: a[i])
        
        i, j = mn, mx
        if i > j:
            i, j = j, i
        
        left_only = j + 1
        right_only = n - i
        both = (i + 1) + (n - j)
        
        out.append(str(min(left_only, right_only, both)))
    
    return "\n".join(out)

# provided samples
assert solve("""5
5
1 5 4 3 2
8
2 1 3 4 5 6 8 7
8
4 2 3 1 8 6 7 5
4
3 4 2 1
4
2 3 1 4
""") == """2
4
5
3
2"""

# custom cases
assert solve("""3
2
1 2
2
2 1
5
3 1 5 2 4
""") == """1
1
3"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 2` | `1` | trivial ordering |
| `2 1` | `1` | reversed ordering |
| `3 1 5 2 4` | `3` | mixed internal positions |

## Edge Cases

When the minimum and maximum are adjacent, the answer is always 2 unless they are already at the ends. For input `[2, 1, 3, 4]`, min and max are at indices 1 and 0, so the best move is to remove one side and then the other, giving 2 moves.

When both extremes are already at opposite ends, such as `[1, 2, 3, 4, 5]`, the answer becomes 2 because removing either side twice isolates both targets immediately. The algorithm captures this through the `both` or single-side formulas without special casing.

When both extremes are in the middle, such as `[3, 1, 5, 2, 4]`, the optimal strategy is splitting removals from both ends. The computed `both` value correctly reflects that only elements outside the interval between the two positions need to be removed.
