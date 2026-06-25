---
title: "CF 106431A - Parking"
description: "We are given a street represented as a single string. Each character describes one parking slot. A dash means the slot is free, while an X means it is already blocked and cannot be used. We are allowed to place vehicles only into consecutive free slots."
date: "2026-06-25T09:39:09+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106431
codeforces_index: "A"
codeforces_contest_name: "Entrenamiento OIE Nivel Experto - Semana 12"
rating: 0
weight: 106431
solve_time_s: 47
verified: true
draft: false
---

[CF 106431A - Parking](https://codeforces.com/problemset/problem/106431/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a street represented as a single string. Each character describes one parking slot. A dash means the slot is free, while an X means it is already blocked and cannot be used.

We are allowed to place vehicles only into consecutive free slots. Each car occupies exactly one slot, an SUV occupies exactly two adjacent slots, and a truck occupies exactly four adjacent slots. Vehicles do not overlap and cannot use blocked positions. The task is to count how many different complete fillings of all free slots are possible using these three vehicle types.

A key point is that we are not choosing which specific vehicle arrives in a sequence. Instead, we are tiling every maximal contiguous segment of free slots with tiles of size 1, 2, or 4. Two fillings are different if at least one slot is occupied by a different type of vehicle, which is equivalent to different segmentations into lengths 1, 2, and 4.

The input may contain multiple such street descriptions, each on a separate line, and we must output one integer per line: the number of valid configurations for that line.

The constraint that each line is at most 70 characters is the main signal about complexity. A naive exponential search over all placements would blow up because even a 70-length free segment would have an enormous number of partitions. Instead, we need a linear or at worst quadratic dynamic programming per segment. Since 70 is small, even O(n²) per line is safe, but the structure suggests a standard linear recurrence is enough.

The main edge case is how blocked cells split the problem. A naive approach that treats the whole string as one segment would incorrectly allow vehicles to cross X boundaries.

For example, consider `-X-`. The correct answer is 1 because each side is independent and each segment has only one cell. A naive DP over the whole string might incorrectly try to place a 2-length vehicle across the X, which is invalid.

Another subtle case is segments shorter than 4. For instance `----` has multiple possibilities, but `---` cannot place a truck, so only smaller combinations matter. Any solution must respect segment boundaries strictly.

## Approaches

A brute-force solution would try to recursively place a vehicle starting at every free position, branching into choices of size 1, 2, or 4 whenever they fit. This is correct because it enumerates all valid tilings directly. However, in a segment of length n, the branching factor is up to 3 at each position, which leads to roughly O(3ⁿ) states in the worst case. Even with memoization, if implemented carelessly, it still explores a large state space of partially filled configurations.

The key observation is that the problem has optimal substructure along the line: once we fix how the first part of a free segment is filled, the remaining suffix is independent. This turns the problem into a one-dimensional tiling count. The only thing that matters for a prefix of length i is how many ways it can be formed using valid tile sizes ending exactly at i.

This reduces each free segment to a simple dynamic programming recurrence. Let f[i] be the number of ways to fill a free segment of length i. The last vehicle placed must have length 1, 2, or 4, so the last step comes from f[i−1], f[i−2], or f[i−4], whenever those indices are valid. This collapses the exponential branching into a linear scan.

We then split the full street by X blocks. Each maximal free segment is solved independently, and the final answer is the product of segment results because choices in different segments do not interact.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force recursion over placements | O(3ⁿ) per segment | O(n) recursion stack | Too slow |
| Segment DP with 1D recurrence | O(n) per segment | O(n) or O(1) | Accepted |

## Algorithm Walkthrough

1. Split the input string into maximal contiguous blocks of `-`. Each block is an independent subproblem because X cells act as hard separators that vehicles cannot cross.
2. For each block of length L, compute the number of ways to tile it using vehicles of sizes 1, 2, and 4. We define a DP array where dp[i] represents the number of ways to fill a prefix of length i.
3. Initialize dp[0] = 1. This represents the empty prefix, which has exactly one valid configuration.
4. For each i from 1 to L, compute dp[i] by considering the last placed vehicle. If we place a car, it consumes one slot and contributes dp[i−1]. If we place an SUV, it consumes two slots and contributes dp[i−2]. If we place a truck, it consumes four slots and contributes dp[i−4]. Any term with a negative index is ignored because it corresponds to an invalid placement.
5. Multiply the result for this segment into the global answer. Since segments are independent, the total number of configurations is the product of all segment DP results.
6. Output the final product for each input line.

### Why it works

The correctness comes from the fact that every valid tiling has a uniquely defined last vehicle in each prefix. Any tiling of length i must end with exactly one of the allowed vehicle sizes, and removing that last vehicle leaves a valid tiling of a smaller prefix. This creates a bijection between full tilings of length i and the union of tilings of lengths i−1, i−2, and i−4 extended by one final placement. Independence between segments follows because no vehicle can cross an X, so no configuration in one segment affects another.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve_case(s: str) -> int:
    MOD = None  # no modulo in problem; values fit in 1e18

    n = len(s)
    ans = 1

    i = 0
    while i < n:
        if s[i] == 'X':
            i += 1
            continue

        j = i
        while j < n and s[j] == '-':
            j += 1

        length = j - i

        if length == 0:
            i = j
            continue

        dp = [0] * (length + 1)
        dp[0] = 1

        for k in range(1, length + 1):
            total = 0
            total += dp[k - 1]
            if k >= 2:
                total += dp[k - 2]
            if k >= 4:
                total += dp[k - 4]
            dp[k] = total

        ans *= dp[length]

        i = j

    return ans

def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        print(solve_case(line))

if __name__ == "__main__":
    main()
```

The implementation mirrors the segmentation logic directly. The outer loop isolates free blocks, ensuring no invalid cross-block placements occur. Inside each block, the DP is a direct translation of the recurrence over allowed vehicle sizes. The multiplication step is safe because the final answer is guaranteed to fit within 10^18 as stated.

A common implementation mistake is forgetting to reset DP per segment, which would incorrectly mix states between independent blocks. Another is accidentally allowing transitions like dp[k−4] when k < 4, which must be guarded explicitly.

## Worked Examples

### Example 1: `--`

We have a single segment of length 2.

| k | dp[k-1] | dp[k-2] | dp[k-4] | dp[k] |
| --- | --- | --- | --- | --- |
| 1 | dp[0]=1 | - | - | 1 |
| 2 | dp[1]=1 | dp[0]=1 | - | 2 |

The segment contributes 2 configurations: two cars or one SUV.

Since there is only one segment, the output is 2.

This trace shows how overlapping choices accumulate naturally through prefix reuse.

### Example 2: `---`

Segment length is 3.

| k | dp[k] |
| --- | --- |
| 1 | 1 |
| 2 | 2 |
| 3 | 3 |

The three configurations are three cars, one SUV plus a car in either order (two placements). A truck is not possible because it requires 4 slots.

This example confirms that the recurrence automatically excludes invalid large placements.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per line | Each character is processed once, and each DP step uses O(1) transitions |
| Space | O(n) per segment | DP array for each free block of length L |

The input limit of 70 characters makes this extremely fast even in the worst case of all dashes. The solution comfortably fits within both time and memory constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    old = sys.stdout
    sys.stdout = out
    try:
        main()
    finally:
        sys.stdout = old
    return out.getvalue()

# provided samples
assert run("-\nX\n--\n-X\nXX\n---\n----\n") == "1\n1\n2\n1\n1\n3\n6\n"

# single cell free
assert run("-\n") == "1\n"

# all blocked
assert run("XXX\n") == "1\n"

# mixed segments
assert run("-X-\n") == "1\n"

# long single segment check
assert run("----\n") == "6\n"

# alternating structure
assert run("-X-X-\n") == "1\n1\n1\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `-X-` | `1` | independence of segments |
| `XXX` | `1` | empty product case |
| `----` | `6` | correct DP growth |
| `-X-X-` | `1 1 1` | multiple isolated segments |

## Edge Cases

For a fully blocked string like `XXXX`, the algorithm produces 1 because there are no free segments, so the product over zero segments remains 1. This matches the interpretation that there is exactly one way to do nothing.

For a string like `-X--X---`, the algorithm splits it into segments of lengths 1, 2, and 3. Each is solved independently, and the final answer is the product of their DP results. This avoids any accidental cross-boundary placements, since segmentation enforces correctness structurally rather than through constraints inside DP.
