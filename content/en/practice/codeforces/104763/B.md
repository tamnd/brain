---
title: "CF 104763B - Jellyfish Lights"
description: "We are given a short sequence of lights in a tunnel, each light being either off (0) or on (1). The goal is to transform this sequence into a perfectly alternating pattern, where adjacent lights always differ."
date: "2026-06-28T21:48:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104763
codeforces_index: "B"
codeforces_contest_name: "UTPC Contest 11-03-23 Div. 2 (Beginner)"
rating: 0
weight: 104763
solve_time_s: 64
verified: true
draft: false
---

[CF 104763B - Jellyfish Lights](https://codeforces.com/problemset/problem/104763/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 4s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a short sequence of lights in a tunnel, each light being either off (0) or on (1). The goal is to transform this sequence into a perfectly alternating pattern, where adjacent lights always differ. There are exactly two valid target patterns: one that starts with 0 and alternates as 0101..., and one that starts with 1 and alternates as 1010....

A single operation consists of flipping a light, changing it from 0 to 1 or from 1 to 0. We need to determine the minimum number of flips required to turn the given configuration into either of the two alternating patterns.

The input size is small, with n up to 100. This immediately suggests that even solutions that inspect every position and compare against multiple patterns are easily fast enough. A linear scan per candidate pattern already gives at most a few hundred operations, so anything O(n) or even O(n²) is safe.

The main edge cases come from very small inputs and from inputs that are already alternating or almost alternating. For example, if the input is "0", both target patterns reduce to either "0" or "1", so the answer is either 0 or 1 depending on comparison. If the string is already alternating like "010101", the answer must be 0, and any solution that incorrectly assumes only one starting pattern could still work but risks missing the optimal alignment in other cases.

A subtle mistake appears when considering only one target pattern. For instance, if the input is "1010", it already matches the pattern starting with 1, but differs completely from the pattern starting with 0. Only checking one of them would give a wrong answer in general.

## Approaches

A direct brute-force approach would explicitly construct both target strings of length n, then compare them against the input by counting mismatches. For each possible starting bit, we generate the full alternating string and compute Hamming distance. This is correct because every valid solution must match one of these two fixed patterns exactly.

The brute-force cost is trivial: generating two strings of length n and comparing them costs O(n) per pattern, so O(2n). With n ≤ 100, this is negligible. Even if we were more naive and toggled each position repeatedly to simulate transformations, we would still remain within limits, but that would be unnecessary.

The key observation is that the structure of the target is completely fixed. There are only two candidates, and each position independently contributes either 0 or 1 to the mismatch count. This removes any need for simulation or greedy decisions. We can compute the cost directly by scanning once and accumulating mismatches against both patterns.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force construction + compare | O(n) | O(n) | Accepted |
| Single scan mismatch counting | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the input string and treat it as an array of characters. We will compare it against two conceptual alternating patterns without explicitly storing them.
2. Initialize two counters: one for the cost of matching a pattern starting with 0, and one for the pattern starting with 1. These represent how many flips are needed for each target.
3. Iterate through each index i from 0 to n - 1. At each position, determine what the correct character should be in both patterns. For the pattern starting with 0, the expected value is i % 2. For the pattern starting with 1, the expected value is 1 - (i % 2).
4. Compare the current character with both expected values. If it differs, increment the corresponding counter. This step directly measures how many flips are required if we choose that pattern.
5. After processing all positions, take the minimum of the two counters and output it. This represents the best possible alternating pattern.

### Why it works

Each position in the string is independent with respect to the final cost because flipping one light does not affect any other position. The total number of flips required for a fixed target pattern is exactly the number of mismatched indices between the input and that pattern. Since there are only two valid patterns, and every valid alternating configuration must match one of them exactly, the minimum over these two mismatch counts is necessarily the optimal answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input().strip())
s = input().strip()

cost0 = 0  # pattern 0101...
cost1 = 0  # pattern 1010...

for i, ch in enumerate(s):
    bit = ord(ch) - 48  # convert '0'/'1' to int

    expected0 = i % 2
    expected1 = 1 - (i % 2)

    if bit != expected0:
        cost0 += 1
    if bit != expected1:
        cost1 += 1

print(min(cost0, cost1))
```

The implementation keeps two running mismatch counts instead of constructing the target strings. The conversion `ord(ch) - 48` avoids repeated string comparisons. Each index contributes independently to both counters, which is why both checks are done in the same loop without interference.

A common mistake is to update only one counter depending on the first mismatch found. Both must be evaluated because each pattern is a separate hypothesis about the final configuration.

## Worked Examples

### Example 1

Input:

```
5
01011
```

We compare against both patterns.

| i | s[i] | expected0 | cost0 | expected1 | cost1 |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 0 | 1 | 1 |
| 1 | 1 | 1 | 0 | 0 | 2 |
| 2 | 0 | 0 | 0 | 1 | 3 |
| 3 | 1 | 1 | 0 | 0 | 4 |
| 4 | 1 | 0 | 1 | 1 | 4 |

Final costs are cost0 = 1 and cost1 = 4, so the answer is 1.

This trace shows that the optimal pattern is determined purely by global mismatch accumulation, not by local decisions. The last character alone determines the only mismatch.

### Example 2

Input:

```
4
1010
```

| i | s[i] | expected0 | cost0 | expected1 | cost1 |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 1 | 1 | 0 |
| 1 | 0 | 1 | 2 | 0 | 0 |
| 2 | 1 | 0 | 3 | 1 | 0 |
| 3 | 0 | 1 | 4 | 0 | 0 |

Final answer is 0 because the string already matches the pattern starting with 1.

This confirms that evaluating both patterns is essential, since the correct answer depends entirely on alignment with the best starting bit.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each position is processed once with constant work |
| Space | O(1) | Only two counters are maintained |

With n ≤ 100, the solution is far below any practical limit. Even with much larger constraints, this linear scan would remain efficient.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input().strip())
    s = input().strip()

    cost0 = 0
    cost1 = 0

    for i, ch in enumerate(s):
        bit = ord(ch) - 48

        if bit != (i % 2):
            cost0 += 1
        if bit != (1 - i % 2):
            cost1 += 1

    return str(min(cost0, cost1))

assert run("5\n01011\n") == "1", "sample 1"

assert run("1\n0\n") == "0", "already valid single element"

assert run("1\n1\n") == "0", "already valid single element"

assert run("4\n0000\n") == "2", "all equal needs half flips"

assert run("4\n0101\n") == "0", "already alternating start 0"

assert run("4\n1010\n") == "0", "already alternating start 1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1-length cases | 0 | minimal boundary correctness |
| 0000 | 2 | worst uniform mismatch behavior |
| 0101 | 0 | correct recognition of first pattern |
| 1010 | 0 | correct recognition of second pattern |

## Edge Cases

One important edge case is the smallest input size n = 1. For input "0", both alternating patterns are valid candidates of length 1, so the mismatch counts are 0 and 1 respectively, giving answer 0. The algorithm handles this correctly because both counters are computed independently and the minimum is taken.

Another case is a fully uniform string like "0000". The algorithm compares it against both patterns. Against 0101 it mismatches at indices 1 and 3, giving cost 2. Against 1010 it mismatches at indices 0 and 2, also giving cost 2. The output is therefore 2, matching the fact that half the positions must be flipped.

A final case is when the string already matches one pattern exactly, such as "1010". The mismatch counter for that pattern remains zero throughout the scan, while the other accumulates errors. Since we take the minimum, the output is correctly 0.
