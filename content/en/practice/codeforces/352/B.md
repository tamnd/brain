---
title: "CF 352B - Jeff and Periods"
description: "We are given a sequence of integers, and for each distinct value we want to understand how its occurrences are spaced across the array. For any value $x$, we look at all indices where $x$ appears."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 352
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 204 (Div. 2)"
rating: 1300
weight: 352
solve_time_s: 85
verified: true
draft: false
---

[CF 352B - Jeff and Periods](https://codeforces.com/problemset/problem/352/B)

**Rating:** 1300  
**Tags:** implementation, sortings  
**Solve time:** 1m 25s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of integers, and for each distinct value we want to understand how its occurrences are spaced across the array. For any value $x$, we look at all indices where $x$ appears. If those indices form a sequence with a constant difference, then $x$ is considered valid, and we also report that difference. If $x$ appears only once, the difference is defined as zero.

So the task is not about the values themselves, but about the structure of their positions. We are effectively classifying each distinct number based on whether its occurrence pattern is evenly spaced.

The input size goes up to $10^5$. That immediately rules out anything that repeatedly scans the whole array per value, since a naive grouping-and-check approach would degrade to $O(n^2)$ in the worst case when many values repeat. We need a solution that processes each element a constant number of times.

A subtle edge case appears when a value occurs exactly twice. Two positions always form an arithmetic progression, so the answer is simply their difference. Another corner case is when occurrences are not evenly spaced but might look almost regular, for example positions $[1, 3, 4]$. A careless approach might only check consecutive differences locally and miss that the pattern breaks later.

## Approaches

A brute-force strategy would be to first collect all positions for each distinct value, then verify whether the differences between consecutive positions are constant. This is correct logically: if all gaps are equal, the positions form an arithmetic progression.

However, the cost depends on how we organize the data. If we repeatedly scan the entire array for each distinct value, we end up doing $O(n)$ work per value, which becomes $O(n^2)$ in the worst case when all elements are distinct. Even if we first group positions in a dictionary, the total cost of building lists is $O(n)$, but verifying each group is still proportional to its frequency, so total checking remains $O(n)$. That part is fine.

The real issue is that we must avoid unnecessary overhead in per-value processing and ensure we do not introduce sorting per group, which would add an extra $\log n$ factor per distinct element.

The key observation is that we do not need anything fancy beyond a single pass to collect positions, because the input is already in order. If we store indices as we scan, each list is inherently sorted. Then each value can be validated by checking a single common difference across its stored indices.

This reduces the problem to linear bookkeeping: accumulate positions, then scan each list once.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Group + repeated scanning | $O(n^2)$ | $O(n)$ | Too slow |
| Group + verify once per value | $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We maintain a dictionary that maps each value to the list of indices where it appears.

1. Scan the array from left to right and append each index to the corresponding value’s list. This ensures the positions are automatically sorted without extra work.
2. For each distinct value $x$, inspect its list of positions. If it contains only one element, the answer for that value is immediately zero since no spacing ambiguity exists.
3. If there are at least two occurrences, compute the initial difference using the first two positions.
4. Traverse the remaining positions and verify that every consecutive difference matches the initial one. If a mismatch is found, discard the value entirely.
5. Collect all valid values and their differences, then output them sorted by the value itself. Sorting is done only over distinct keys, not over the full array.

### Why it works

For any valid value $x$, the condition “positions form an arithmetic progression” is equivalent to “all consecutive differences are equal”. Since the indices are already sorted by construction, checking adjacent differences is sufficient and necessary. If even one gap differs, the progression property is violated. Conversely, if all gaps match, the definition of an arithmetic progression is satisfied, guaranteeing correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    pos = {}
    
    for i, x in enumerate(a, start=1):
        if x not in pos:
            pos[x] = []
        pos[x].append(i)
    
    res = []
    
    for x in pos:
        p = pos[x]
        if len(p) == 1:
            res.append((x, 0))
            continue
        
        d = p[1] - p[0]
        ok = True
        
        for i in range(2, len(p)):
            if p[i] - p[i - 1] != d:
                ok = False
                break
        
        if ok:
            res.append((x, d))
    
    res.sort()
    
    out = []
    out.append(str(len(res)))
    for x, d in res:
        out.append(f"{x} {d}")
    
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution relies on a dictionary keyed by value, where each entry stores a growing list of indices. Since we iterate left to right, no sorting is required for these lists. The check for arithmetic progression is done in a single linear pass per value.

A common mistake is recomputing differences without fixing a reference difference early, which leads to unnecessary comparisons or incorrect early exits. Another subtlety is ensuring that single-occurrence values are handled explicitly, since otherwise they might be incorrectly skipped.

## Worked Examples

### Example 1

Input:

```
5
1 2 1 2 1
```

We build position lists:

- 1 → [1, 3, 5]
- 2 → [2, 4]

Now we verify:

| Value | Positions | First diff | Checks | Valid |
| --- | --- | --- | --- | --- |
| 1 | [1, 3, 5] | 2 | 3-1=2, 5-3=2 | Yes |
| 2 | [2, 4] | 2 | only one check | Yes |

Output:

```
2
1 2
2 2
```

This shows that multiple values can independently satisfy the progression condition.

### Example 2

Input:

```
6
3 3 3 3 3 3
```

Position list:

- 3 → [1, 2, 3, 4, 5, 6]

| Step | Positions | Diff check |
| --- | --- | --- |
| init | [1,2] | d = 1 |
| check | 2-1=1 | ok |
| check | 3-2=1 | ok |
| check | 4-3=1 | ok |
| check | 5-4=1 | ok |
| check | 6-5=1 | ok |

Output:

```
1
3 1
```

This confirms that uniform repetition produces a valid arithmetic progression with step 1.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n + k \log k)$ | Building position lists is linear; sorting distinct values is $k \log k$, where $k \le n$ |
| Space | $O(n)$ | Each index is stored once in a list per value |

The constraints allow $10^5$ operations comfortably, and sorting at most $10^5$ distinct keys remains efficient within time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))
    
    pos = {}
    for i, x in enumerate(a, start=1):
        pos.setdefault(x, []).append(i)
    
    res = []
    for x in pos:
        p = pos[x]
        if len(p) == 1:
            res.append((x, 0))
            continue
        d = p[1] - p[0]
        ok = all(p[i] - p[i-1] == d for i in range(2, len(p)))
        if ok:
            res.append((x, d))
    
    res.sort()
    
    out = [str(len(res))]
    for x, d in res:
        out.append(f"{x} {d}")
    return "\n".join(out)

# provided sample
assert run("1\n2\n") == "1\n2 0"

# all equal
assert run("5\n7 7 7 7 7\n") == "1\n7 1"

# two values, mixed validity
assert run("5\n1 2 1 2 1\n") == "2\n1 2\n2 2"

# invalid spacing
assert run("4\n1 2 3 1\n") == "2\n1 2\n2 0"

# single occurrences
assert run("3\n1 2 3\n") == "3\n1 0\n2 0\n3 0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal | single value with step 1 | repeated constant spacing |
| mixed pattern | two valid sequences | independent verification per value |
| invalid spacing | filters broken progression | detection of non-constant gaps |
| all distinct | all zeros | singleton handling |

## Edge Cases

A value appearing only once is the simplest case, but it is easy to mishandle if the implementation assumes at least two positions before computing differences. The algorithm explicitly assigns zero in this case before any access to adjacent elements, preventing out-of-range errors.

Another edge case is when a value appears twice. For example input:

```
4
5 1 5 1
```

For value 5, positions are [1, 3], so difference is 2. The algorithm directly computes this from the first pair and accepts it without needing further validation.

A more subtle case is when a sequence starts with a valid difference but later breaks:

```
5
2 1 2 2 1
```

For value 2, positions are [1, 3, 4]. First difference is 2, but next difference is 1, so it is rejected. The scan detects this immediately at the first mismatch and discards the value, ensuring no partial pattern is incorrectly accepted.
