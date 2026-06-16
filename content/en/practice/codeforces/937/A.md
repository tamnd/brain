---
title: "CF 937A - Olympiad"
description: "We are given a list of participant scores, and we need to count how many different ways we can choose a group of participants to receive diplomas under a very specific rule. A valid group is determined by picking a score threshold."
date: "2026-06-17T02:45:18+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 937
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 467 (Div. 2)"
rating: 800
weight: 937
solve_time_s: 62
verified: true
draft: false
---

[CF 937A - Olympiad](https://codeforces.com/problemset/problem/937/A)

**Rating:** 800  
**Tags:** implementation, sortings  
**Solve time:** 1m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a list of participant scores, and we need to count how many different ways we can choose a group of participants to receive diplomas under a very specific rule.

A valid group is determined by picking a score threshold. Once a participant with some score is included, every participant whose score is greater than or equal to that score must also be included. This means the chosen set is completely determined by a cutoff value: everything above or equal to it is selected, everything below it is excluded. There is one additional restriction that participants with score zero can never be included in any valid group. Also, the chosen group cannot be empty.

The input is simply the list of scores. The output is the number of distinct valid groups that can be formed.

The constraints are small, with at most 100 participants, so even quadratic or sorting-based solutions are easily fast enough. This is a signal that we should focus on reasoning about structure rather than optimization tricks.

A subtle edge case appears when zeros are present. A naive approach that counts all distinct score thresholds without separating zeros will incorrectly include configurations where zero-score participants become part of the selected suffix. Another edge case is when all non-zero scores are equal. In that case, only one valid selection exists, even though there are many ways to pick thresholds if we think mechanically about splitting sorted values.

For example, consider input:

```
5
0 1 2 2 3
```

A careless interpretation might count thresholds at 0, 1, 2, 3 and think all produce valid groups. But the threshold at 0 would include zero-score participants, which is forbidden, so that choice must be excluded.

Another example:

```
3
0 5 5
```

Only one valid group exists: selecting score 5 includes both 5s, and selecting anything else either violates rules or produces the same set.

## Approaches

The brute-force idea is to try every possible subset of participants and check whether it satisfies the rule. For each subset, we would verify two conditions: no zero-score participant is included, and if a participant is included then all participants with higher or equal score are also included. With n participants, there are 2^n subsets, and checking each subset takes O(n), giving O(n·2^n), which becomes infeasible even for moderate n.

The key observation is that the structure of valid subsets is extremely rigid. Once we pick a participant with some score x, we are forced to include everyone with score at least x. So instead of thinking in terms of subsets of indices, we should think in terms of score thresholds.

After sorting the scores, every valid group corresponds to choosing a distinct score value as the cutoff, but only among positive scores. Each distinct positive score value defines exactly one valid set: all participants with scores at least that value. If we move the threshold from a higher score to a lower one, we only add more participants, never remove earlier ones in a way that creates a new configuration beyond the distinct score levels.

Thus, the answer reduces to counting how many distinct positive score values exist.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n·2^n) | O(n) | Too slow |
| Optimal | O(n log n) | O(1) or O(n) | Accepted |

## Algorithm Walkthrough

1. Read all scores into an array. This is necessary because we need to analyze the distribution of values rather than individual identities.
2. Remove or ignore all zero values. These participants cannot appear in any valid group, so they cannot influence which groups exist.
3. Sort the remaining positive scores. Sorting groups equal values together, which makes it easy to identify distinct score levels.
4. Scan through the sorted list and count how many times the value changes. Each distinct value represents a new possible threshold.
5. Output this count as the number of valid diploma assignment sets.

The key idea is that each distinct positive score defines exactly one “cut point” where the selected set changes meaningfully.

### Why it works

After sorting, all participants are arranged by score. Any valid selection must correspond to choosing a minimum included score x. Once x is fixed, the set is uniquely determined as all elements with score ≥ x. Therefore, the number of valid sets is exactly the number of distinct values x that can serve as such a minimum, which is exactly the number of distinct positive scores.

No two different thresholds within the same value produce different sets, and zero cannot serve as a threshold because it violates the restriction. This makes the mapping between valid sets and distinct positive scores one-to-one.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    a = [x for x in a if x > 0]
    a.sort()

    if not a:
        print(0)
        return

    cnt = 1
    for i in range(1, len(a)):
        if a[i] != a[i - 1]:
            cnt += 1

    print(cnt)

if __name__ == "__main__":
    solve()
```

The implementation begins by filtering out zeros because they are explicitly disallowed in any valid selection. Sorting is used to group equal scores together so that distinct values can be counted in a single pass.

The counter starts at one because a non-empty list of positive scores always contributes at least one distinct value. We then increment the counter only when we observe a transition between different values.

A common mistake is forgetting to remove zeros before counting distinct values, which inflates the answer incorrectly by treating zero as a valid threshold.

## Worked Examples

### Example 1

Input:

```
4
1 3 3 2
```

Sorted positive scores:

```
[1, 2, 3, 3]
```

| Step | Index | Value | New distinct? | Count |
| --- | --- | --- | --- | --- |
| init | - | - | - | 1 |
| 1 | 1 | 2 | yes | 2 |
| 2 | 2 | 3 | yes | 3 |
| 3 | 3 | 3 | no | 3 |

Output is 3.

This confirms that each distinct score level corresponds to a valid threshold: 3, 2, and 1.

### Example 2

Input:

```
5
0 0 5 5 5
```

Filtered and sorted:

```
[5, 5, 5]
```

| Step | Index | Value | New distinct? | Count |
| --- | --- | --- | --- | --- |
| init | - | - | - | 1 |
| 1 | 1 | 5 | no | 1 |
| 2 | 2 | 5 | no | 1 |

Output is 1.

This demonstrates that zeros do not contribute any valid group, and all identical positive scores collapse into a single valid selection.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates; linear scan afterward |
| Space | O(n) | Storing filtered scores |

The constraints allow up to 100 elements, so even a simple sorting solution is far below the limit. The memory usage is negligible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return main(inp)

def main(inp=None):
    import sys
    input = sys.stdin.readline
    n = int(input())
    a = list(map(int, input().split()))
    a = [x for x in a if x > 0]
    a.sort()
    if not a:
        return "0"
    cnt = 1
    for i in range(1, len(a)):
        if a[i] != a[i - 1]:
            cnt += 1
    return str(cnt)

# provided sample
assert run("4\n1 3 3 2\n") == "3"

# custom cases
assert run("1\n0\n") == "0"
assert run("3\n5 5 5\n") == "1"
assert run("5\n0 1 2 3 4\n") == "4"
assert run("6\n0 0 0 1 1 2\n") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 0 | 0 | only zeros produce no valid group |
| 5 5 5 | 1 | duplicates collapse correctly |
| 0 1 2 3 4 | 4 | zeros ignored, multiple thresholds |
| 0 0 0 1 1 2 | 2 | mixed zeros and duplicates |

## Edge Cases

A key edge case is when all elements are zero except the constraint guarantees at least one non-zero, but we still must handle cases where filtering removes everything. For input like:

```
3
0 0 5
```

After filtering we get `[5]`. Sorting does nothing. The algorithm initializes count as 1 and returns 1, which corresponds to the only valid selection: taking score 5 and everything above it (just those participants).

Another edge case is when all positive values are identical:

```
4
0 7 7 7
```

Filtered list is `[7, 7, 7]`. The loop never finds a change in value, so count remains 1. This correctly reflects that only one threshold exists.

Finally, strictly increasing scores:

```
4
1 2 3 4
```

Filtered and sorted list is unchanged. Every transition increases the count, producing 4 distinct valid sets, matching the idea that each score level defines a different cutoff.
