---
title: "CF 103361N - \u041f\u043e\u0434\u0433\u043e\u0442\u043e\u0432\u043a\u0430 \u043a \u041d\u043e\u0432\u043e\u043c\u0443 \u0433\u043e\u0434\u0443"
description: "We are given a small collection of Christmas trees, each with a positive integer height. The task is to pick three different trees such that all three have exactly the same height. The output is the indices of those three trees."
date: "2026-07-03T13:09:56+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103361
codeforces_index: "N"
codeforces_contest_name: "\u041e\u0442\u043a\u0440\u044b\u0442\u0430\u044f \u041a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u041e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u042e\u041c\u0428 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e"
rating: 0
weight: 103361
solve_time_s: 53
verified: true
draft: false
---

[CF 103361N - \u041f\u043e\u0434\u0433\u043e\u0442\u043e\u0432\u043a\u0430 \u043a \u041d\u043e\u0432\u043e\u043c\u0443 \u0433\u043e\u0434\u0443](https://codeforces.com/problemset/problem/103361/N)

**Rating:** -  
**Tags:** -  
**Solve time:** 53s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a small collection of Christmas trees, each with a positive integer height. The task is to pick three different trees such that all three have exactly the same height. The output is the indices of those three trees. If no such triple exists, we report that it is impossible.

The input size is very small, at most 100 trees, and each height is also bounded by 100. This immediately tells us that even relatively slow quadratic or cubic approaches would be acceptable, since the total number of operations in the worst case is on the order of 10^6 or 10^7, which is trivial for a 2 second limit in Python.

A subtle failure mode appears when one is tempted to pick “any repeated height”. Having at least two equal heights is not enough. For example, if the heights are `[5, 5, 7]`, there is repetition but not enough copies to form a triple, so the answer must still be `-1`. The condition is strictly that some value appears at least three times.

Another edge situation is when multiple valid answers exist. Any valid triple of distinct indices is acceptable, so the algorithm should not overthink selection or try to optimize for lexicographic order.

## Approaches

A direct brute force idea is to examine every triple of indices `(i, j, k)` and check whether `h[i] == h[j] == h[k]`. This is straightforward and correct because it explicitly verifies all possible triples. However, its cost is proportional to the number of triples, which is roughly `n^3 / 6`. With `n = 100`, this is about 160,000 iterations, which is still actually fine in Python, but it is unnecessarily heavy given the simplicity of the structure.

The key observation is that we do not care which triple we pick beyond equality of values. We only need to know whether some value appears at least three times, and if so, we need any three indices where it occurs. This transforms the problem from searching combinations of indices into a frequency and bookkeeping task.

Instead of generating triples, we track where each height occurs. As soon as we find a height with three recorded positions, we can immediately output them. This reduces the problem to a single pass over the array.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Triples | O(n^3) | O(1) | Accepted but unnecessary |
| Frequency with indices | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We maintain a mapping from each height to the list of indices where it appears.

1. Iterate through the list of trees from left to right while recording indices for each height. This ensures we preserve the natural order of occurrence, which gives valid indices immediately.
2. Whenever we append a new index to the list of a particular height, check whether the list size has reached 3. The moment it reaches 3, we can stop processing further because we already have a valid answer.
3. Output those three stored indices in any order and terminate the program.
4. If we finish scanning all trees without any height reaching frequency 3, output `-1`.

The key design choice is the early exit at step 2. There is no need to fully build the frequency table once a valid triple is found.

### Why it works

For each height value, we maintain exactly the set of indices where it appears. If any height appears at least three times, then those three occurrences form a valid solution by definition of the problem. Since we only store actual indices from the input, we never fabricate or duplicate positions. The algorithm therefore cannot output invalid indices or mismatched heights.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    h = list(map(int, input().split()))
    
    pos = {}
    
    for i, val in enumerate(h, start=1):
        if val not in pos:
            pos[val] = []
        pos[val].append(i)
        if len(pos[val]) == 3:
            print(pos[val][0], pos[val][1], pos[val][2])
            return
    
    print(-1)

if __name__ == "__main__":
    solve()
```

The solution uses a dictionary keyed by height to store indices. Each index is 1-based to match typical competitive programming conventions. The early return ensures we stop immediately after finding a valid triple. The only subtle point is ensuring we append before checking the length condition so that the current index is included in the candidate triple.

## Worked Examples

### Example 1

Input:

```
6
1 2 3 2 1 2
```

We track occurrences:

| i | height | stored positions after step | action |
| --- | --- | --- | --- |
| 1 | 1 | [1] | continue |
| 2 | 2 | [2] | continue |
| 3 | 3 | [3] | continue |
| 4 | 2 | [2, 4] | continue |
| 5 | 1 | [1, 5] | continue |
| 6 | 2 | [2, 4, 6] | output |

At index 6, height 2 reaches three occurrences, so we output `2 4 6`.

This confirms the invariant that we always maintain exact occurrence positions, so the first time a list reaches size 3, it is a valid answer.

### Example 2

Input:

```
5
1 2 3 4 5
```

| i | height | stored positions |
| --- | --- | --- |
| 1 | 1 | [1] |
| 2 | 2 | [2] |
| 3 | 3 | [3] |
| 4 | 4 | [4] |
| 5 | 5 | [5] |

No list ever reaches size 3, so the algorithm finishes scanning and outputs `-1`.

This shows the fallback behavior when no valid triple exists.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each tree is processed once, with O(1) average dictionary operations per step |
| Space | O(n) | In the worst case all indices are stored in the map |

The constraints n ≤ 100 make this solution extremely fast in practice, but even if n were much larger, the same linear structure would remain valid.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    
    solve()
    
    out = sys.stdout.getvalue().strip()
    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return out

def solve():
    input = sys.stdin.readline
    n = int(input())
    h = list(map(int, input().split()))
    
    pos = {}
    for i, val in enumerate(h, start=1):
        pos.setdefault(val, []).append(i)
        if len(pos[val]) == 3:
            print(pos[val][0], pos[val][1], pos[val][2])
            return
    print(-1)

# provided samples
assert run("6\n1 2 3 2 1 2\n") in ["2 4 6", "6 4 2"]
assert run("5\n1 2 3 4 5\n") == "-1"

# custom cases
assert run("3\n7 7 7\n") in ["1 2 3", "2 1 3", "3 2 1"], "all equal minimum triple"
assert run("4\n1 1 1 1\n") in ["1 2 3", "1 3 2"], "more than three occurrences"
assert run("6\n5 4 5 4 5 4\n") in ["1 3 5", "2 4 6"], "multiple valid groups"
assert run("1\n10\n") == "-1", "minimum n no triple"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal 3 | any permutation of 1 2 3 | basic success case |
| all equal 4 | any triple among first 3 | extra duplicates |
| alternating | 1 3 5 or 2 4 6 | multiple valid choices |
| single element | -1 | minimum boundary |

## Edge Cases

When all trees have the same height, the first three indices immediately form a valid answer. The algorithm handles this without scanning the rest of the array once the third occurrence is reached.

When there are exactly two occurrences of every height, no list ever reaches size three, so the scan completes fully and correctly outputs `-1`.

When the valid triple appears late in the array, the algorithm still detects it because it continuously accumulates indices and does not depend on any ordering assumptions beyond sequential processing.
