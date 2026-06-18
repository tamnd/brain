---
problem: 926C
contest_id: 926
problem_index: C
name: "Is This a Zebra?"
contest_name: "VK Cup 2018 - Wild-card Round 1"
rating: 1700
tags: ["implementation"]
answer: passed_samples
verified: true
solve_time_s: 73
date: 2026-06-17
model: gpt-5-3-mini
samples_passed: 1
samples_total: 1
share_url: https://chatgpt.com/share/6a3270b2-6b2c-83ec-a440-f77b7015f16a
---

# CF 926C - Is This a Zebra?

**Rating:** 1700  
**Tags:** implementation  
**Model:** gpt-5-3-mini  
**Solve time:** 1m 13s  
**Verified:** yes (1/1 samples)  
**Share:** https://chatgpt.com/share/6a3270b2-6b2c-83ec-a440-f77b7015f16a  

---

## Solution

## Problem Understanding

We are given a one-dimensional image represented as a sequence of length $n$, where each position is either black or white. The interpretation is column-wise: every column is uniformly colored, so the entire picture reduces to a binary array.

The task is to decide whether this array could be decomposed into contiguous blocks where each block consists of identical values, and all blocks have the same length. The colors must alternate between adjacent blocks. In other words, the array should be a repetition of a fixed pattern length $k$, where each segment of length $k$ is constant, and consecutive segments flip color.

The output is a simple feasibility check: whether such a uniform stripe width exists that can generate the entire sequence.

The constraint $n \le 100000$ implies that any solution must be linear or near-linear. An $O(n^2)$ attempt that tries every possible stripe width and validates it directly would require checking up to $n$ candidates, each costing $O(n)$, leading to $10^{10}$ operations in the worst case. That is far beyond acceptable limits. Even an $O(n \log n)$ solution is unnecessary since the structure can be verified in a single pass.

A few edge cases are easy to underestimate.

If all elements are identical, for example $[1,1,1,1]$, the correct answer is “YES” because it can be seen as a single stripe covering the entire array. A naive implementation that insists on at least two alternating segments might incorrectly reject this case.

If the array length is odd and we try to force equal stripe widths greater than one, such as $[0,0,0,1,1]$, some implementations might incorrectly assume valid segmentation exists without checking that the final block is complete. The requirement is global divisibility, not local consistency.

If the array alternates every element, such as $[0,1,0,1,0,1]$, the stripe width must be 1. Any approach that assumes stripes must be longer than one would fail here.

## Approaches

A brute-force approach tries every possible stripe width $k$ from 1 to $n$. For each candidate $k$, we split the array into consecutive segments of length $k$ and verify two conditions: each segment must be uniform, and adjacent segments must differ.

This works because it directly mirrors the definition of a valid zebra pattern. However, the cost becomes prohibitive. For each $k$, we scan the entire array, yielding $O(n)$ work per candidate and $O(n^2)$ total complexity in the worst case. With $n = 100000$, this is too slow.

The key observation is that the array is fully determined by its run-length encoding. Once we compress it into consecutive blocks of identical values, the problem reduces to checking whether all run lengths are equal.

If the array is valid, then every run of consecutive identical values must align perfectly with stripe boundaries. That means no run can be split across stripes, and no stripe can merge multiple runs of different lengths. Therefore, all runs must have exactly the same length, except possibly if there is only one run in total.

This transforms the problem into a simple scan where we compute run lengths and verify uniformity.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(1)$ | Too slow |
| Optimal | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Traverse the array from left to right while tracking consecutive equal values. Each time the value changes, record the length of the segment that just ended. This step compresses the input into run lengths, which capture all structural information relevant to stripe formation.
2. Store the first run length as a reference value $k$. This represents the candidate stripe width.
3. For every subsequent run, compare its length with $k$. If any run differs, the structure cannot be partitioned into equal-width stripes, so the answer becomes invalid immediately.
4. If traversal finishes without contradictions, accept the configuration.

The key idea is that valid zebra patterns enforce strict alignment between run boundaries and stripe boundaries. If two consecutive runs had different lengths, any stripe width would either split a run or merge mismatched runs, both of which violate the definition.

### Why it works

Any valid solution partitions the array into equal-length blocks where values alternate. Each block is uniform, so every run of identical values must be fully contained within a single block. Since all blocks have equal size, every run must also have identical length. This forces a one-to-one correspondence between runs and stripes, making equality of run lengths both necessary and sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input().strip())
a = list(map(int, input().split()))

runs = []

cur = a[0]
length = 1

for i in range(1, n):
    if a[i] == cur:
        length += 1
    else:
        runs.append(length)
        cur = a[i]
        length = 1

runs.append(length)

ok = True
for i in range(1, len(runs)):
    if runs[i] != runs[0]:
        ok = False
        break

print("YES" if ok else "NO")
```

The implementation directly constructs run lengths in a single pass. The loop maintains a current segment and counts how long it continues until a change occurs. Each completed run is appended to the list.

The validation step is intentionally minimal: once we have run lengths, only equality matters. The first run defines the stripe width, and every other run must match it.

A subtle point is that we do not need to explicitly check alternation of values, because run construction already guarantees alternation by definition of a change point.

## Worked Examples

### Example 1

Input:

```
9
0 0 0 1 1 1 0 0 0
```

Run construction:

| i | value | current run | action | runs |
| --- | --- | --- | --- | --- |
| 0 | 0 | 1 | start | [] |
| 1 | 0 | 2 | extend | [] |
| 2 | 0 | 3 | extend | [] |
| 3 | 1 | 1 | close run, start new | [3] |
| 4 | 1 | 2 | extend | [3] |
| 5 | 1 | 3 | extend | [3] |
| 6 | 0 | 1 | close run | [3, 3] |
| 7 | 0 | 2 | extend | [3, 3] |
| 8 | 0 | 3 | extend | [3, 3] |

Final runs: $[3,3,3]$

All run lengths match, so the answer is YES.

This confirms the invariant that a consistent stripe width induces identical run lengths.

### Example 2

Input:

```
7
0 0 0 1 1 1 1
```

Run construction:

| i | value | current run | action | runs |
| --- | --- | --- | --- | --- |
| 0-2 | 0 | 3 | running | [] |
| 3-5 | 1 | 3 | close + start | [3] |
| 6 | 1 | 4 | extend | [3] |

Final runs: $[3,4]$

Run lengths differ, so no uniform stripe width exists.

This shows how a single inconsistent segment breaks global feasibility even though local alternation is valid.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Each element is visited once to build run lengths |
| Space | $O(n)$ | In worst case alternating values create $n$ runs |

The linear scan fits comfortably within the constraints for $n \le 100000$. Even the worst-case alternating input only produces 100000 runs, which is still manageable in both time and memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input().strip())
    a = list(map(int, input().split()))

    runs = []
    cur = a[0]
    length = 1

    for i in range(1, n):
        if a[i] == cur:
            length += 1
        else:
            runs.append(length)
            cur = a[i]
            length = 1

    runs.append(length)

    ok = all(x == runs[0] for x in runs)
    return "YES" if ok else "NO"

# provided sample
assert run("9\n0 0 0 1 1 1 0 0 0\n") == "YES"

# all equal
assert run("4\n1 1 1 1\n") == "YES"

# alternating
assert run("6\n0 1 0 1 0 1\n") == "YES"

# invalid unequal runs
assert run("7\n0 0 0 1 1 1 1\n") == "NO"

# single element
assert run("1\n0\n") == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal | YES | single-run case |
| alternating | YES | stripe width = 1 |
| unequal runs | NO | detects mismatch |
| n = 1 | YES | minimal boundary case |

## Edge Cases

A single constant array such as $[1,1,1,1]$ produces exactly one run. The algorithm records runs = $[4]$, and since there are no contradictions, it returns YES. This matches the interpretation that a single stripe is valid.

An alternating array such as $[0,1,0,1]$ produces runs $[1,1,1,1]$. Equality holds across all runs, so stripe width 1 is inferred correctly, confirming that the method does not assume minimum stripe size.

A case like $[0,0,0,1,1]$ produces runs $[3,2]$. The mismatch is detected immediately at the second run, demonstrating that global alignment fails even though local alternation exists.