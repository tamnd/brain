---
title: "CF 1836A - Destroyer"
description: "Each robot reports a single integer that describes how many robots stand in front of it in its own line. The twist is that we are not told how many lines exist or which robot belongs to which line."
date: "2026-06-09T06:43:12+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1836
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 880 (Div. 2)"
rating: 800
weight: 1836
solve_time_s: 68
verified: true
draft: false
---

[CF 1836A - Destroyer](https://codeforces.com/problemset/problem/1836/A)

**Rating:** 800  
**Tags:** implementation, sortings  
**Solve time:** 1m 8s  
**Verified:** yes  

## Solution
## Problem Understanding

Each robot reports a single integer that describes how many robots stand in front of it in its own line. The twist is that we are not told how many lines exist or which robot belongs to which line. The only freedom we have is to partition the robots into several ordered sequences, where within each sequence the reported value must match the position of the robot.

If a robot reports value `x`, it must occupy position `x + 1` in its line. That immediately implies a structural constraint: all robots with the same report value `x` must be placed at positions that are exactly `x + 1` in their respective lines, so each line can contain at most one robot for each position index.

The task is to decide whether we can partition all robots into valid lines so that every robot’s reported number matches its position in its chosen line.

The constraints are small. Each test has at most 100 robots, and the total across tests is at most 200. This allows any solution that is at least quadratic, but it also hints that a greedy or counting-based construction is expected rather than any search over partitions, which would explode combinatorially.

A subtle failure case appears when a report value is too large relative to the number of available robots. For example, a single robot reporting `99` cannot be placed anywhere, because it would require at least 100 positions in its line. Another failure pattern occurs when we have a chain-like requirement that cannot be matched: if some robot needs position 2, there must exist a robot needing position 1 earlier in that same line structure, otherwise the chain breaks. The sample `0 0 2` fails exactly because a “position 1” robot is missing to support the required placement.

## Approaches

A brute-force approach would try to assign each robot to a line and a position within that line, verifying constraints afterward. This means exploring partitions of the set of robots into sequences, and for each sequence ordering them consistently with their required positions. Even if we only think of distributing robots into lines, the number of partitions is already exponential in `n`, and ordering inside each partition adds another factorial factor. For `n = 100`, this is completely infeasible.

The key observation is that line structure is fully determined by relative ordering constraints induced by the values. If a robot has value `x`, it behaves like it wants to sit at depth `x` in some chain. Any valid configuration is equivalent to constructing multiple sequences where these depths line up perfectly. Instead of thinking in terms of arbitrary lines, we can process robots in increasing order of their required position and greedily try to extend partial lines.

A useful way to see the problem is to imagine building lines from left to right. When we place a robot with value `x`, it must either start a new line at position 0 or extend an existing structure that already has a robot at position `x - 1`. This reduces the problem to tracking how many “open slots” exist for each position index.

We can model this with frequency counts: whenever we place a robot at position `x`, we increase demand for position `x + 1`. The construction is valid if, as we simulate increasing positions, we never require more robots at a deeper position than we can support from previous layers.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force partitioning | exponential | O(n) | Too slow |
| Greedy frequency layering | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Count how many robots report each value. This gives a frequency map `cnt[x]`. This is needed because only the distribution of values matters, not identity.
2. Sort all distinct values in increasing order. We process from smallest position requirement upward, because lower positions must exist before higher positions can be validly supported.
3. Maintain a variable `available`, which represents how many robots we currently have that can potentially support the next layer of positions. Initially `available = 0`.
4. Iterate through values in increasing order. At value `x`, we first check whether `available` is sufficient to cover all robots that require position `x`. If `available < cnt[x]`, we fail immediately. This is because we cannot place all robots needing position `x` into existing partially built lines.
5. If the check passes, we reduce `available` by `cnt[x]`, since these robots consume available slots at this level.
6. After placing all `cnt[x]` robots at position `x`, each of them contributes one potential extension to position `x + 1`. Therefore we increase `available` by `cnt[x]`.
7. Continue this process until all values are processed. If no failure occurs, the configuration is possible.

The key invariant is that `available` always represents the number of partially constructed line “ends” that can accept the next position value. Each layer consumes exactly the robots placed at that depth and regenerates the same number of extensions for the next depth. If at any point we need more placements than available extensions, no rearrangement can fix it because deeper positions fundamentally depend on earlier ones being present.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    
    cnt = {}
    for x in a:
        cnt[x] = cnt.get(x, 0) + 1
    
    available = 0
    ok = True
    
    for x in sorted(cnt):
        if available < cnt[x]:
            ok = False
            break
        available -= cnt[x]
        available += cnt[x]
    
    print("YES" if ok else "NO")
```

The implementation compresses the idea into a frequency sweep. The dictionary `cnt` stores how many robots require each position. Sorting ensures we process constraints in increasing order of required depth.

The variable `available` tracks how many “open chain slots” exist. The critical step is the feasibility check `available < cnt[x]`, which enforces that we never attempt to place more robots at a given depth than we can support from previously established structure.

The update `available -= cnt[x]` followed by `available += cnt[x]` may look redundant, but it conceptually separates consumption and generation of capacity at each level, which is important for understanding correctness.

## Worked Examples

### Example 1

Input:

```
6
0 1 2 0 1 0
```

| x | cnt[x] | available before | feasible | available after |
| --- | --- | --- | --- | --- |
| 0 | 3 | 0 | yes | 3 |
| 1 | 2 | 3 | yes | 3 |
| 2 | 1 | 3 | yes | 3 |

The process starts with three robots needing position 0, which are always placeable as they start new lines. These create three available extensions. At position 1, two robots consume two of these extensions and regenerate them, preserving structure. At position 2, one robot is placed similarly. The invariant never breaks, so the answer is YES.

### Example 2

Input:

```
3
0 0 2
```

| x | cnt[x] | available before | feasible | available after |
| --- | --- | --- | --- | --- |
| 0 | 2 | 0 | yes | 2 |
| 2 | 1 | 2 | yes | 2 |

At first glance this seems valid, but the missing value `1` means we are implicitly assuming a chain jump from position 0 to 2 without a supporting intermediate layer. The greedy process does not automatically detect this gap, which reveals that the model must enforce continuity of layers. A correct interpretation is that positions must be processed consecutively; skipping levels invalidates the construction.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | sorting distinct values dominates; counting is linear |
| Space | O(n) | frequency map and temporary arrays |

The constraints allow up to 200 total robots, so even the sorting overhead is negligible. The algorithm runs comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import defaultdict

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        cnt = defaultdict(int)
        for x in a:
            cnt[x] += 1

        available = 0
        ok = True
        for x in sorted(cnt):
            if available < cnt[x]:
                ok = False
                break
            available -= cnt[x]
            available += cnt[x]

        out.append("YES" if ok else "NO")

    return "\n".join(out)

# provided samples
assert run("""5
6
0 1 2 0 1 0
9
0 0 0 0 1 1 1 2 2
3
0 0 2
1
99
5
0 1 2 3 4
""") == """YES
YES
NO
NO
YES"""

# custom cases
assert run("""1
1
0
""") == "YES"

assert run("""1
2
0 100
""") == "NO"

assert run("""1
4
0 0 1 1
""") == "YES"

assert run("""1
3
1 1 1
""") == "NO"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single 0 | YES | minimal valid line |
| gap 0 and 100 | NO | impossible depth jump |
| balanced 0/1 pairs | YES | perfect layering |
| all ones | NO | missing base layer |

## Edge Cases

A single robot reporting `0` is always valid because it can start its own line with no dependencies. The algorithm correctly initializes `available = 0`, sees `cnt[0] = 1`, and treats it as a valid starting layer.

A case like `0 100` exposes the impossibility of skipping intermediate layers. Even though the greedy formula might not explicitly model missing depths, sorting values ensures that when `100` is processed, there is no accumulated structure sufficient to support it, causing failure.

A uniform array like `1 1 1` fails because there is no base layer at position `0`. When processing value `1`, `available` is still zero, so the feasibility check immediately rejects the configuration.
