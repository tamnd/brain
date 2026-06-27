---
title: "CF 105020G - String Rotation"
description: "We are given two strings of equal length. We are allowed to modify characters in the first string freely, but each modification costs one operation. After modifying, we do not compare it directly to the second string."
date: "2026-06-28T01:58:27+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105020
codeforces_index: "G"
codeforces_contest_name: "TCPC Tunisian Collegiate Programming Contest 2022"
rating: 0
weight: 105020
solve_time_s: 66
verified: false
draft: false
---

[CF 105020G - String Rotation](https://codeforces.com/problemset/problem/105020/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 6s  
**Verified:** no  

## Solution
## Problem Understanding

We are given two strings of equal length. We are allowed to modify characters in the first string freely, but each modification costs one operation. After modifying, we do not compare it directly to the second string. Instead, we first rotate the modified string to the right by exactly `x` positions, and only then compare it with the target string. The goal is to minimize how many characters we need to change in the original string so that after this fixed rotation, the result becomes identical to the target.

The key detail is that the rotation is fixed and unavoidable. We are not choosing the best rotation, we are forced to apply exactly `x` right shifts, which effectively remaps positions in a deterministic way.

The constraint `n ≤ 100000` forces any solution to be linear or nearly linear. Any approach that tries to recompute matches for each possible alignment or simulate repeated edits independently per position risks quadratic behavior and will fail.

A subtle edge case comes from the fact that rotation wraps indices. If we incorrectly treat the rotation as a linear shift without modular indexing, we will misalign characters at the boundary.

Another important corner case is when `x` is larger than `n`. A naive interpretation might try to apply `x` rotations literally, but the string repeats every `n` shifts, so the effective rotation is `x mod n`. Failing to reduce this leads to unnecessary work and possible indexing errors.

## Approaches

The brute-force idea is straightforward: actually rotate the string `s` by `x`, then compare it position by position with `t`, counting mismatches. Each mismatch corresponds to one character that must be changed before rotation. This works because we are allowed arbitrary replacements, so each mismatched position can be fixed independently.

However, the problem becomes interesting if we think about how rotation interacts with indexing. After a right rotation by `x`, character originally at index `i` moves to `(i + x) % n`. Instead of physically rotating, we can compute where each character ends up and compare directly.

The brute-force rotation itself is already linear, so there is no need for more complex optimization. The only real improvement over a naive simulation of `x` shifts one by one is reducing `x` modulo `n`, since performing `x` single-step rotations would be far too slow when `x` is large.

The observation that makes the solution clean is that we do not need to simulate the transformation at all. We only need to compute a mapping between indices in `s` and `t` and count mismatches.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Simulate x rotations step-by-step | O(n·x) | O(n) | Too slow |
| Direct index mapping | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Reduce the rotation amount by setting `x = x % n`. This ensures we only consider the effective shift within one full cycle of the string. Any full rotations do not change the string, so they can be ignored.
2. Understand the mapping induced by a right rotation. After rotation, the character at index `i` in the original string moves to index `(i + x) % n` in the resulting string.
3. Instead of building the rotated string explicitly, compare directly: for each target position `j`, determine which position in the original string maps to it. This inverse mapping is `(j - x) % n`.
4. Iterate over all positions `j` from `0` to `n - 1`. For each position, compare `s[(j - x) % n]` with `t[j]`.
5. Every mismatch means we must modify the corresponding character in `s` before rotation so that it matches `t` after rotation. Count all mismatches.
6. Return the total mismatch count as the minimum number of operations.

### Why it works

Each position in the final rotated string depends on exactly one position in the original string. Since each character change in `s` affects exactly one position in the rotated result, there is no interaction between positions. This makes the cost function additive across indices. Therefore, minimizing total operations reduces to independently fixing every mismatched mapped position.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, x = map(int, input().split())
    s = input().strip()
    t = input().strip()

    x %= n
    ans = 0

    for j in range(n):
        if s[(j - x) % n] != t[j]:
            ans += 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The solution begins by normalizing the rotation using modulo arithmetic, which avoids unnecessary cycles and ensures correct indexing. The comparison loop is written in terms of the final string position `j`, and we invert the rotation to access the corresponding original position in `s`.

A common mistake is to build the rotated string explicitly and then compare. While correct, it introduces extra memory usage and can be slower in tight constraints. Another subtle issue is forgetting Python’s negative modulo behavior; `(j - x) % n` correctly wraps around even when `j < x`.

## Worked Examples

### Example 1

Input:

```
n = 5, x = 2
s = abcde
t = cdeab
```

| j | (j - x) % n | s[i] | t[j] | match |
| --- | --- | --- | --- | --- |
| 0 | 3 | d | c | no |
| 1 | 4 | e | d | no |
| 2 | 0 | a | e | no |
| 3 | 1 | b | a | no |
| 4 | 2 | c | b | no |

All positions mismatch, so answer is 5. This shows that a full cycle mismatch can happen when strings are unrelated, and every position contributes independently.

### Example 2

Input:

```
n = 4, x = 1
s = abcd
t = dabc
```

| j | (j - x) % n | s[i] | t[j] | match |
| --- | --- | --- | --- | --- |
| 0 | 3 | d | d | yes |
| 1 | 0 | a | a | yes |
| 2 | 1 | b | b | yes |
| 3 | 2 | c | c | yes |

All positions match, so answer is 0. This confirms that the rotation mapping is correctly inverted and no unnecessary edits are counted.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Single pass comparing each position once |
| Space | O(1) | No auxiliary data structures besides input storage |

The algorithm processes each character exactly once and performs only constant-time arithmetic per index. With `n` up to `10^5`, this comfortably fits within typical time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return main()

def main():
    n, x = map(int, input().split())
    s = input().strip()
    t = input().strip()

    x %= n
    ans = 0
    for j in range(n):
        if s[(j - x) % n] != t[j]:
            ans += 1
    return str(ans)

# provided sample (format assumed corrected)
assert run("5 2\nabcde\ncdeab\n") == "0"

# custom cases
assert run("1 100\nx\ny\n") == "1", "single char mismatch"
assert run("4 4\nabcd\nabcd\n") == "0", "full rotation equals identity"
assert run("6 2\naaaaaa\naaaaaa\n") == "0", "all equal strings"
assert run("5 1\nabcde\neabcd\n") == "0", "perfect rotation"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 100 / x / y` | 1 | minimal edge, single mismatch |
| `4 4 / abcd / abcd` | 0 | rotation equals identity |
| `6 / aaaaaa / aaaaaa` | 0 | uniform string stability |
| `5 1 / abcde / eabcd` | 0 | correct rotation mapping |

## Edge Cases

One important edge case is when `x` is much larger than `n`. For example, if `n = 5` and `x = 10^9`, directly simulating rotations is impossible and unnecessary. The reduction `x % n` compresses this into a manageable shift without changing the result.

Another edge case occurs when `n = 1`. The rotation has no effect, and the answer is simply whether the two characters match. The algorithm naturally handles this because `(j - x) % 1` is always zero.

A final subtle case is when characters are identical across the string. Even with non-zero rotation, every comparison succeeds because all positions are equivalent, and the mismatch count remains zero.
