---
title: "CF 106073J - Jo\u00e3o Jo\u00e3o"
description: "We are given a fixed collection of 10 tasks, each labeled with a difficulty value from the set {1, 2, 3, 4}. The organizer wants to eventually be able to select a set of four tasks, one from each difficulty level."
date: "2026-06-21T09:26:36+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106073
codeforces_index: "J"
codeforces_contest_name: "The 2025 ICPC South America - Brazil First Phase"
rating: 0
weight: 106073
solve_time_s: 41
verified: true
draft: false
---

[CF 106073J - Jo\u00e3o Jo\u00e3o](https://codeforces.com/problemset/problem/106073/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 41s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a fixed collection of 10 tasks, each labeled with a difficulty value from the set {1, 2, 3, 4}. The organizer wants to eventually be able to select a set of four tasks, one from each difficulty level. Right now, some difficulties may already be present among the 10 tasks, and some may be missing entirely.

The task is to determine the minimum number of additional tasks that must be created so that all four difficulty levels appear at least once in the pool of tasks.

The input is simply 10 integers, each describing the difficulty of an existing task. The output is a single integer: how many of the four difficulty levels are currently absent.

Since the input size is constant (exactly 10 numbers), there are no meaningful asymptotic constraints. Any solution, even linear or constant extra work, is sufficient. The key is correctness rather than efficiency.

The main failure mode in a naive approach is confusing frequency with presence. We do not care how many tasks of a difficulty exist beyond zero versus nonzero. For example, having ten tasks of difficulty 1 does not help if difficulties 2, 3, and 4 are missing. A correct solution must track only whether each difficulty appears at least once.

A second edge case arises when all four difficulties are already present. In that case, no new tasks are required, and the answer is zero. Any approach that computes “4 minus count” must ensure it never produces negative values.

## Approaches

A brute-force interpretation would try to simulate building the missing set of difficulties by repeatedly adding tasks until all four difficulty types appear. Since each addition can only introduce one missing category, one might repeatedly check which difficulties are missing and conceptually add them one by one.

This works but is unnecessarily indirect. In the worst case, one would scan the current set after each hypothetical addition, leading to repeated work even though the state space is extremely small and static.

The key observation is that the final requirement depends only on which of the four values appear at least once. Each difficulty class is independent, so we can compress the entire input into a boolean presence array of size 4. Once this is known, the answer is simply the number of missing categories.

This reduces the problem from a dynamic “construction” process to a static counting problem.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(10 * 4) conceptual | O(4) | Accepted but unnecessary |
| Presence Counting | O(10) | O(4) | Accepted |

## Algorithm Walkthrough

1. Initialize a boolean structure `seen[1..4]` with all values set to false. This represents whether we have encountered each difficulty level so far.
2. Read the 10 input values one by one. For each value `d`, mark `seen[d] = true`. This step compresses the entire dataset into a simple existence map rather than storing frequencies.
3. After processing all values, iterate over the four difficulty levels and count how many entries in `seen` are still false. Each false entry corresponds to a missing difficulty class.
4. Output this count directly, since each missing difficulty requires exactly one new task to be introduced.

The algorithm avoids any simulation of task creation because each missing category is independent and requires exactly one addition regardless of how many tasks already exist in other categories.

### Why it works

The correctness relies on the fact that the requirement is purely existential: we only need at least one task of each difficulty level. The input contributes to satisfaction of a level in a binary way, either it exists or it does not. Therefore, compressing all occurrences into a boolean presence state preserves all information relevant to the final answer. The final count of missing categories directly equals the number of new tasks needed, since each addition can introduce exactly one previously missing difficulty.

## Python Solution

```python
import sys
input = sys.stdin.readline

vals = list(map(int, input().split()))

seen = [False] * 5

for v in vals:
    seen[v] = True

ans = 0
for d in range(1, 5):
    if not seen[d]:
        ans += 1

print(ans)
```

The solution reads the 10 integers and immediately marks which difficulty levels appear. The array `seen` is sized 5 so indices align naturally with difficulty labels 1 through 4, avoiding off-by-one mistakes.

The final loop simply counts how many of the four positions remain false. This avoids any arithmetic tricks like subtraction from 4, which can be error-prone if not carefully bounded.

## Worked Examples

### Example 1

Input:

```
1 3 4 1 3 4 1 3 4 1
```

We track the presence as follows:

| Step | Value | seen[1] | seen[2] | seen[3] | seen[4] |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | true | false | false | false |
| 2 | 3 | true | false | true | false |
| 3 | 4 | true | false | true | true |
| 4-10 | repeats | true | false | true | true |

After processing, only difficulty 2 is missing. The algorithm counts one missing entry and outputs 1. This confirms that duplicate occurrences do not affect correctness, since presence is all that matters.

### Example 2

Input:

```
4 1 1 4 3 1 2 1 2 2
```

| Step | Value | seen[1] | seen[2] | seen[3] | seen[4] |
| --- | --- | --- | --- | --- | --- |
| After processing all | mixed | true | true | true | true |

All four difficulty levels are present, so no new tasks are required. The algorithm outputs 0, confirming that the logic correctly handles the fully satisfied case without producing negative or invalid values.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(10) | We scan a fixed-size input once and do constant-time updates per element |
| Space | O(1) | Only a fixed boolean array of size 4 (plus input storage) |

The constraints are constant-sized, so this solution runs instantly and uses negligible memory. Even under generalized constraints, the same approach scales linearly with input size.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    vals = list(map(int, input().split()))
    seen = [False] * 5
    for v in vals:
        seen[v] = True
    ans = sum(1 for d in range(1, 5) if not seen[d])
    return str(ans)

# provided samples
assert run("1 3 4 1 3 4 1 3 4 1") == "1"
assert run("4 1 1 4 3 1 2 1 2 2") == "0"

# all same value
assert run("1 1 1 1 1 1 1 1 1 1") == "3"

# already complete set
assert run("1 2 3 4 1 2 3 4 1 2") == "0"

# missing two categories
assert run("1 1 1 1 1 1 1 1 1 3") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all 1s | 3 | worst missing diversity |
| full set | 0 | no additions needed |
| only 1s and 3s | 2 | partial coverage |

## Edge Cases

A key edge case is when all tasks belong to a single difficulty. For example:

Input:

```
1 1 1 1 1 1 1 1 1 1
```

The algorithm marks only `seen[1] = true`. The remaining three values are false, so the count is 3. This matches the requirement that we must introduce one task each for difficulties 2, 3, and 4.

Another edge case is when the input already contains all difficulties but in scattered order:

```
2 3 1 4 2 3 1 4 2 3
```

After processing, all `seen` entries become true. The loop counts zero missing categories, producing output 0. The correctness comes from treating repeated occurrences as irrelevant, since presence is already saturated after the first occurrence of each value.
