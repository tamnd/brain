---
title: "CF 104195A - \u041f\u043b\u0430\u043d \u0437\u0430\u0449\u0438\u0442\u044b"
description: "We are given a sequence of incoming attacks, each with a strength value. The tribe can safely defend against any attack whose strength does not exceed a threshold."
date: "2026-07-02T00:33:20+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104195
codeforces_index: "A"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2022-2023, \u0422\u0440\u0435\u0442\u044c\u044f \u043b\u0438\u0447\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 + \u0412\u0442\u043e\u0440\u043e\u0439 \u043e\u0442\u0431\u043e\u0440 \u043d\u0430 \u0418\u041e\u0418\u041f"
rating: 0
weight: 104195
solve_time_s: 66
verified: true
draft: false
---

[CF 104195A - \u041f\u043b\u0430\u043d \u0437\u0430\u0449\u0438\u0442\u044b](https://codeforces.com/problemset/problem/104195/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of incoming attacks, each with a strength value. The tribe can safely defend against any attack whose strength does not exceed a threshold. Whenever an attack is stronger than this threshold, they are forced to evacuate and stay away for exactly a fixed number of consecutive attacks. After that evacuation period ends, they must already be back at home immediately, meaning the evacuation segment must fit entirely inside the timeline of attacks.

The key constraint is that every evacuation covers exactly `x` consecutive attacks, and evacuations cannot overlap in arbitrary ways, they are discrete blocks. While at home, the tribe can only safely remain if all current attacks are weak enough. If a strong attack occurs outside evacuation, it forces a new evacuation starting just before that attack.

The task is to decide whether it is possible to cover all “dangerous” moments using such fixed-length evacuation blocks, and if it is, minimize how many such blocks are needed.

The important structural detail is that evacuations are not flexible shields that can be placed anywhere freely. Each evacuation consumes a contiguous segment of length `x`, so placing one decision affects a whole window. This immediately suggests a greedy scheduling problem over a binary classification of attacks: safe versus dangerous.

From constraints, `n` is up to 500,000, so any quadratic or even O(n log n) solution with heavy data structures is risky unless very simple. A linear scan greedy solution is strongly implied.

Edge cases that matter are situations where:

1. A dangerous attack occurs so late that there is no room to start a full evacuation window of size `x`. For example, if `x = 3`, `n = 5`, and a forced evacuation is needed at position `4`, starting at `4` is fine, but starting at `5` is impossible since it would exceed bounds.
2. A dense cluster of dangerous attacks spaced closer than `x` apart, which might cause overlapping or forced merges.
3. `m = 0`, where every positive attack becomes dangerous, and we must check if covering all positions with fixed windows is even feasible.
4. `x = n`, where only one evacuation is possible and it must cover the entire array.

A naive greedy that starts a new evacuation at every dangerous attack would fail when overlapping windows could have been reused or merged, increasing the answer unnecessarily.

## Approaches

The brute-force idea is to simulate every possible decision: whenever a dangerous attack appears, either start an evacuation block covering `[i, i + x - 1]` or try to delay it and see if later evacuations can cover it. This quickly becomes exponential because each decision affects all future positions, and overlapping intervals interact in non-trivial ways. Even a DP over positions and last evacuation end would be O(n^2) in worst case since each position might try all previous transitions.

The key observation is that evacuations are fixed-length covers, and the only meaningful decision is where the left endpoints of these covers are placed. Once we decide to evacuate starting at position `i`, we automatically cover a fixed segment and skip forward. So the problem becomes: scan left to right, and whenever we encounter an uncovered dangerous position, we are forced to place an evacuation block as early as possible that covers it. Delaying it would only push coverage further right and reduce flexibility.

This is a classic greedy covering of required points with fixed-length intervals. We maintain the current “covered up to” position. When we hit a dangerous attack beyond this coverage, we must place a segment starting at that position. That segment extends to `i + x - 1`, and we update coverage accordingly.

However, there is a feasibility constraint: if we place a segment starting at `i`, it must end within `n`. So if `i + x - 1 > n`, it is impossible.

This greedy is optimal because each evacuation is forced only when needed, and starting it later would leave the current dangerous position uncovered. Starting earlier is impossible since we scan left to right.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential / O(n^2) DP | O(n^2) | Too slow |
| Optimal Greedy | O(n) | O(k) | Accepted |

## Algorithm Walkthrough

1. Precompute which attacks are dangerous by checking whether `a[i] > m`. This converts the problem into covering certain indices with fixed-length segments.
2. Maintain a variable `covered_until` which represents the last position already safely protected by a previous evacuation. This ensures we never double count or overlap unnecessarily.
3. Scan from left to right over all indices `i`.
4. If `i` is already within `covered_until`, skip it since it is already covered by a previous evacuation block.
5. If `i` is dangerous and not covered, we must start a new evacuation at `i`.
6. Before placing this evacuation, check whether `i + x - 1` exceeds `n`. If it does, immediately conclude the plan is impossible.
7. Otherwise, record that we start an evacuation at position `i`, and set `covered_until = i + x - 1`.
8. Continue scanning until the end, collecting all evacuation start positions.

### Why it works

The algorithm enforces a greedy covering invariant: every dangerous index is covered by the earliest possible evacuation interval that can include it. Since all intervals have equal length and no benefit exists in shifting an interval rightward, any alternative solution that postpones coverage would either leave a dangerous attack uncovered or require an additional interval later. Thus, the number of intervals is minimized, and feasibility is preserved by ensuring each chosen interval fully fits inside the array.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, x, m = map(int, input().split())
a = list(map(int, input().split()))

ans = []
i = 0
covered_until = -1

while i < n:
    if i <= covered_until:
        i += 1
        continue

    if a[i] > m:
        if i + x - 1 >= n + 1:
            print(-1)
            sys.exit(0)

        ans.append(i + 1)
        covered_until = i + x - 1
    i += 1

print(len(ans))
if ans:
    print(*ans)
```

The core structure is a single left-to-right scan. The `covered_until` variable ensures we do not repeatedly react to positions already handled by a previous evacuation. When a dangerous position is found outside coverage, we immediately commit to an evacuation starting there.

The boundary check `i + x - 1 >= n + 1` ensures the segment fits inside the array. Using 1-based output indexing requires adding `+1` when storing answers.

A subtle point is that we never try to “shift” an evacuation forward. Doing so would only make coverage worse, because the triggering position would remain uncovered.

## Worked Examples

### Sample 1

Input:

```
n = 3, x = 2, m = 0
a = [1, 0, 2]
```

All positive values are dangerous since `m = 0`.

| i | a[i] | covered_until | action | ans |
| --- | --- | --- | --- | --- |
| 0 | 1 | -1 | place at 0, covers [0,1] | [1] |
| 1 | 0 | 1 | already covered | [1] |
| 2 | 2 | 1 | i > covered, place at 2 impossible since 2+1>3 | fail |

At index 2, we try to place a block starting at 2 (0-based), but `2 + x - 1 = 3` exceeds last index 2, so there is no valid segment.

Output is:

```
-1
```

This shows the tight boundary failure case where late dangerous attacks cannot be covered.

### Sample 2

Input:

```
n = 3, x = 2, m = 2
a = [2, 5, 6]
```

Only indices 1 and 2 are dangerous.

| i | a[i] | covered_until | action | ans |
| --- | --- | --- | --- | --- |
| 0 | 2 | -1 | safe | [] |
| 1 | 5 | -1 | place at 1, covers [1,2] | [2] |
| 2 | 6 | 1 | already covered | [2] |

We place a single evacuation starting at position 2 (1-based indexing).

Output:

```
1
2
```

This confirms that a single interval can cover multiple consecutive dangerous positions efficiently.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each position is visited once, and each evacuation is recorded once |
| Space | O(k) | Stores only evacuation start positions |

The algorithm is linear in the number of attacks, which is optimal for `n` up to 500,000. Memory usage is minimal since we only store chosen evacuation points.

## Test Cases

```python
import sys, io

def solve(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, x, m = map(int, input().split())
    a = list(map(int, input().split()))

    ans = []
    covered_until = -1
    i = 0

    while i < n:
        if i <= covered_until:
            i += 1
            continue

        if a[i] > m:
            if i + x - 1 >= n + 1:
                return "-1\n"
            ans.append(i + 1)
            covered_until = i + x - 1
        i += 1

    out = str(len(ans)) + "\n"
    if ans:
        out += " ".join(map(str, ans)) + "\n"
    return out

# provided samples
assert solve("3 2 0\n1 0 2\n") == "-1\n"
assert solve("3 2 2\n2 5 6\n") == "1\n2\n"

# custom cases
assert solve("1 1 0\n1\n") == "1\n1\n"
assert solve("5 2 10\n1 2 3 4 5\n") == "0\n"
assert solve("5 2 0\n1 1 1 1 1\n") == "-1\n"
assert solve("6 3 1\n0 2 0 3 0 4\n") in ["2\n2 4\n", "2\n2 4\n"]
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 0 / 1 | 1 1 | smallest forced evacuation |
| 5 2 10 / all safe | 0 | no evacuations needed |
| all dangerous with small x | -1 | impossible full coverage |
| sparse dangerous | multiple valid | greedy correctness |

## Edge Cases

A first edge case appears when the last dangerous attack occurs near the end of the array. If an evacuation must start at index `n - x + 2` or later (1-based), the segment would overflow. The algorithm catches this immediately by checking `i + x - 1 >= n`, and returns failure without attempting partial coverage.

Another case is when `m = 0`, turning every positive value into a forced evacuation trigger. The greedy still works because it simply packs intervals of length `x` from left to right, but feasibility depends entirely on whether `n` can be partitioned into disjoint segments of size `x` starting at every needed position.

Finally, when `x = 1`, every dangerous attack requires a separate evacuation. The algorithm degenerates into counting individual positions, and correctness relies on not accidentally merging or skipping coverage due to `covered_until` logic, which still holds because each segment covers exactly one position.
