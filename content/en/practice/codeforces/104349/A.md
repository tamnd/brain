---
title: "CF 104349A - Human Readable"
description: "We are given a raw file size measured in bytes, and we must display it in a compact “human-readable” format using only three possible units: bytes (B), kibibytes (KiB), and mebibytes (MiB)."
date: "2026-07-01T18:14:40+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104349
codeforces_index: "A"
codeforces_contest_name: "TheForces Round #13 (Boombastic-Forces)"
rating: 0
weight: 104349
solve_time_s: 85
verified: false
draft: false
---

[CF 104349A - Human Readable](https://codeforces.com/problemset/problem/104349/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 25s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a raw file size measured in bytes, and we must display it in a compact “human-readable” format using only three possible units: bytes (B), kibibytes (KiB), and mebibytes (MiB). The output is always a single number followed immediately by one of these unit strings, with no spaces.

Each unit corresponds to a power-of-two scaling. One KiB equals 1024 bytes, and one MiB equals 1024 KiB, which is 1024 squared bytes. The number we print must always be an integer between 1 and 1023 inclusive, and we are required to round down when converting between units.

So the task is to choose the largest possible unit such that after conversion the value is still at least 1 and at most 1023, and then output the floored integer in that unit.

The constraint on m goes up to 10^9, which is small enough that we only ever deal with at most MiB scale because 1024^2 is about 10^6, and 1024^3 already exceeds 10^9. That means the decision space is very shallow: only B, KiB, and MiB matter.

A naive mistake arises when trying to always convert upward or always normalize greedily without checking bounds. For example, treating 1401 bytes as 1401 B is invalid because 1401 exceeds 1023, but converting it to KiB gives 1 KiB after flooring, which is valid. Another pitfall is losing the rule that the number must stay within [1, 1023], which forbids outputs like 0 MiB or 0 KiB even if mathematically correct.

Another subtle issue is ordering: if we try KiB first and then MiB, we may incorrectly choose a smaller unit even when MiB is valid. For instance, 14510629 bytes should be 13 MiB, but a careless approach might stop at KiB because it “fits earlier” after rounding.

## Approaches

The brute-force idea is to try all three units independently. For each unit, we compute the converted value using integer division and check whether it lies in the valid range [1, 1023]. If multiple units are valid, we choose the largest unit among them (MiB over KiB over B). This works because there are only three candidates, and each conversion is constant time.

The inefficiency only appears if we imagine a generalized version with many units or repeated recomputation, but even then the structure is trivial enough that brute force is already optimal in practice.

The key observation is that the unit system is strictly hierarchical and each step is a factor of 1024. This means we never need to search or optimize dynamically; we only need to test divisibility by fixed constants and apply flooring division. The constraint on the numeric range forces exactly one valid representation, so the answer is determined by the highest unit that keeps the quotient in range.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(1) per test | O(1) | Accepted |
| Optimal | O(1) per test | O(1) | Accepted |

## Algorithm Walkthrough

We evaluate each test case independently.

1. Start with the given size in bytes, m. This is the base representation, and all other units are derived from repeated division by 1024.
2. Check whether representing the value in MiB is possible. Compute m // (1024 * 1024). If the result is at least 1 and at most 1023, we immediately choose MiB as the unit. This is because MiB is the largest allowed unit, and we want the most compressed representation.
3. If MiB is not valid, check KiB. Compute m // 1024. If this value lies in [1, 1023], we output KiB with that number.
4. If neither MiB nor KiB works, we fall back to bytes and output m B directly. At this point m must already be in [1, 1023], because otherwise KiB would have been valid.
5. Print the chosen number concatenated with the unit string.

Why it works follows from the structure of base-1024 scaling. Each unit is exactly 1024 times the previous one, so the converted values are uniquely determined by integer division. The constraint that the output number must remain in [1, 1023] ensures that at most one unit level can satisfy the condition after flooring. Since MiB dominates KiB which dominates B, selecting the highest valid unit cannot skip a valid smaller representation or miss a valid larger one.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        m = int(input())

        mib = m // (1024 * 1024)
        if 1 <= mib <= 1023:
            print(str(mib) + "MiB")
            continue

        kib = m // 1024
        if 1 <= kib <= 1023:
            print(str(kib) + "KiB")
            continue

        print(str(m) + "B")

if __name__ == "__main__":
    solve()
```

The solution directly follows the unit hierarchy. The MiB check is done first because it yields the most compact representation if valid. The KiB check is only reached if MiB fails, and bytes are used only when both scaled representations exceed the allowed numeric bounds or are too small. Integer division naturally enforces the required rounding down behavior, so no additional rounding logic is needed.

A common implementation mistake is to check KiB before MiB, which can produce suboptimal units. Another is forgetting the lower bound of 1, which can lead to outputs like 0 KiB for small values under 1024, which are invalid.

## Worked Examples

First, consider the input m = 1401.

| Step | m | MiB | KiB | Chosen |
| --- | --- | --- | --- | --- |
| Check MiB | 1401 | 0 | - | no |
| Check KiB | 1401 | - | 1 | KiB |

Here 1401 // 1024 = 1, which is valid. The MiB conversion gives 0, which is invalid because it falls below the minimum required number. The algorithm correctly selects KiB.

Now consider m = 14510629.

| Step | m | MiB | KiB | Chosen |
| --- | --- | --- | --- | --- |
| Check MiB | 14510629 | 13 | - | MiB |
| Stop | - | 13 | - | MiB |

Here 14510629 // 1048576 equals 13. This lies within [1, 1023], so MiB is selected immediately. KiB is never evaluated because MiB already satisfies the requirement.

These examples show how the hierarchy enforces a unique selection and how flooring interacts with unit conversion.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case performs a constant number of arithmetic operations and comparisons |
| Space | O(1) | Only a few integer variables are used regardless of input size |

The constraints allow up to 100 test cases, and each case is handled in constant time. The solution therefore runs well within limits with negligible memory usage.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        m = int(input())

        mib = m // (1024 * 1024)
        if 1 <= mib <= 1023:
            out.append(str(mib) + "MiB")
            continue

        kib = m // 1024
        if 1 <= kib <= 1023:
            out.append(str(kib) + "KiB")
            continue

        out.append(str(m) + "B")

    return "\n".join(out)

# provided samples
assert run("3\n29\n1401\n14510629\n") == "29B\n1KiB\n13MiB"

# custom cases
assert run("1\n1\n") == "1B"
assert run("1\n1023\n") == "1023B"
assert run("1\n1024\n") == "1KiB"
assert run("1\n1048576\n") == "1MiB"
assert run("1\n1048575\n") == "1023KiB"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 1B | smallest possible value |
| 1023 | 1023B | upper bound for bytes |
| 1024 | 1KiB | exact KiB boundary |
| 1048576 | 1MiB | exact MiB boundary |
| 1048575 | 1023KiB | boundary just below MiB |

## Edge Cases

For m = 1, the MiB check gives 0 and KiB check also gives 0, so the algorithm falls back to bytes and outputs 1B. This is correct because only bytes can represent values below 1024.

For m = 1024, MiB is 0, KiB is 1, so the algorithm selects 1KiB. This matches the requirement that we must switch to the next unit as soon as the current one exceeds the valid numeric range.

For m = 1048576, MiB becomes 1, which is valid, so the algorithm selects 1MiB directly. This demonstrates that the highest valid unit is always preferred, and that exact powers of 1024 map cleanly to higher units without ambiguity.
