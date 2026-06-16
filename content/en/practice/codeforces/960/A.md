---
title: "CF 960A - Check the string"
description: "We are given a string made only of the characters a, b, and c. This string is claimed to have been constructed in a very specific way: it starts with one or more a characters, then some b characters are appended, and finally some c characters are appended at the end."
date: "2026-06-17T01:50:04+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 960
codeforces_index: "A"
codeforces_contest_name: "Divide by Zero 2018 and Codeforces Round 474 (Div. 1 + Div. 2, combined)"
rating: 1200
weight: 960
solve_time_s: 64
verified: true
draft: false
---

[CF 960A - Check the string](https://codeforces.com/problemset/problem/960/A)

**Rating:** 1200  
**Tags:** implementation  
**Solve time:** 1m 4s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string made only of the characters `a`, `b`, and `c`. This string is claimed to have been constructed in a very specific way: it starts with one or more `a` characters, then some `b` characters are appended, and finally some `c` characters are appended at the end. After these three phases, the string must contain at least one `a` and at least one `b`, while `c` may or may not exist depending on the construction rule.

The key constraint is not only about counts but also about structure. The string must be in non-decreasing phase order: all `a` come first, then all `b`, then all `c`. On top of that, the number of `c` characters must equal either the number of `a` characters or the number of `b` characters (or both if they are equal).

The task is to decide whether a given string could have been produced by such a process.

The input size is at most 5000 characters. This is small enough that any solution up to roughly quadratic behavior would pass comfortably, but the structure of the problem suggests a linear scan is sufficient. Since we are only verifying a pattern and not constructing anything, we should expect an O(n) check.

A naive misunderstanding would be to focus only on counts. For example, a string like `acbbc` has equal counts of `a`, `b`, and `c` but is not valid because the order is broken. Another subtle failure is assuming that the string can be rearranged, but rearrangement is not allowed.

Edge cases that often break incorrect solutions include:

- Mixed ordering such as `aba...` where `b` appears before all `a` are finished.
- Missing required segments, such as no `b` at all.
- Correct ordering but wrong `c` count, such as `aabccc` where `a=2`, `b=1`, `c=3`, invalid since `c` matches neither 2 nor 1.
- Strings like `aaabbbccc` where everything is clean and counts match `a` or `b`.

## Approaches

A brute-force interpretation would try splitting the string into three segments and checking all possible split points. For each split `(i, j)`, we interpret `S[0:i]` as all `a`, `S[i:j]` as all `b`, and `S[j:]` as all `c`, then verify both ordering and the count condition. This requires trying O(n²) splits, and each verification costs O(n), leading to O(n³) in the worst case, which is unnecessary and wasteful even for n = 5000.

The structure of the problem removes the need for guessing split points. The string, if valid, has a rigid monotonic pattern: once a character type changes, it never returns. This means we can scan left to right and ensure transitions follow `a → b → c` only. At the same time, we count occurrences of each character.

Once the scan finishes, we only need to check two conditions: the ordering constraint is satisfied and the final counts satisfy `c == a or c == b`, with the additional implicit requirement that both `a > 0` and `b > 0` because the construction guarantees at least one of each.

This reduces the entire problem to a single pass with constant bookkeeping.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force splits | O(n³) | O(1) | Too slow |
| Single scan counting | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize counters `ca`, `cb`, `cc` to zero. Also track a stage variable that represents which block we are currently in: `0` for `a`, `1` for `b`, `2` for `c`.
2. Scan the string from left to right.
3. For each character:

- If it is `a`, it is only valid if we are still in stage `0`. Increment `ca`.
- If it is `b`, we must be in stage `0` or `1`. If we are in stage `0`, switch to stage `1`. Increment `cb`.
- If it is `c`, we must be in stage `1` or `2`. If we are in stage `1`, switch to stage `2`. Increment `cc`.

Any violation of allowed transitions immediately invalidates the string.
4. After scanning, ensure that both `ca > 0` and `cb > 0`.
5. Finally check whether `cc == ca` or `cc == cb`.

The reason transitions are enforced during scanning is to ensure we never allow a `b` before finishing all `a`, or a `c` before finishing all `b`.

### Why it works

The construction process guarantees a three-phase monotone structure. Any valid string must have a unique partition into contiguous blocks of `a`, then `b`, then `c`. The stage variable enforces exactly this partitioning. Since every character is processed once and only once under strict transition rules, any deviation from the required order is detected immediately. After structure is verified, the only remaining degree of freedom is the count of `c`, which must match one of the earlier block sizes by definition of the construction.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().strip()

ca = cb = cc = 0
stage = 0  # 0 = a, 1 = b, 2 = c

valid = True

for ch in s:
    if ch == 'a':
        if stage != 0:
            valid = False
            break
        ca += 1
    elif ch == 'b':
        if stage == 2:
            valid = False
            break
        if stage == 0:
            stage = 1
        cb += 1
    else:  # 'c'
        if stage < 1:
            valid = False
            break
        if stage == 1:
            stage = 2
        cc += 1

if not valid or ca == 0 or cb == 0:
    print("NO")
else:
    print("YES" if (cc == ca or cc == cb) else "NO")
```

The code maintains a strict phase variable `stage` that encodes which segment we are currently allowed to extend. This prevents illegal back-transitions such as encountering an `a` after a `b`. The counters track exact frequencies needed for the final condition.

One subtle point is that transitions only move forward: once we enter stage `1`, we never go back. This matches the irreversibility of the construction process.

## Worked Examples

### Example 1: `aaabccc`

| index | char | stage before | stage after | ca | cb | cc | valid |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | a | 0 | 0 | 1 | 0 | 0 | yes |
| 2 | a | 0 | 0 | 2 | 0 | 0 | yes |
| 3 | a | 0 | 0 | 3 | 0 | 0 | yes |
| 4 | b | 0 | 1 | 3 | 1 | 0 | yes |
| 5 | c | 1 | 2 | 3 | 1 | 1 | yes |
| 6 | c | 2 | 2 | 3 | 1 | 2 | yes |
| 7 | c | 2 | 2 | 3 | 1 | 3 | yes |

Final check: `ca = 3`, `cb = 1`, `cc = 3`. Since `cc == ca`, output is `YES`.

This trace confirms that once the transition to `b` and then `c` happens, the stage locking correctly preserves order.

### Example 2: `aabcb`

| index | char | stage before | stage after | ca | cb | cc | valid |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | a | 0 | 0 | 1 | 0 | 0 | yes |
| 2 | a | 0 | 0 | 2 | 0 | 0 | yes |
| 3 | b | 0 | 1 | 2 | 1 | 0 | yes |
| 4 | c | 1 | 2 | 2 | 1 | 1 | yes |
| 5 | b | 2 | invalid | 2 | 1 | 1 | no |

The moment we see `b` after entering the `c` stage, the construction rule is violated. This demonstrates why ordering enforcement is essential, since count checks alone would incorrectly accept it.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is processed once in a single pass |
| Space | O(1) | Only a fixed number of counters and a stage variable are used |

The input limit of 5000 characters is easily handled by a linear scan, which performs at most 5000 iterations and constant work per iteration.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from sys import stdout
    input = _sys.stdin.readline

    s = input().strip()

    ca = cb = cc = 0
    stage = 0
    valid = True

    for ch in s:
        if ch == 'a':
            if stage != 0:
                valid = False
                break
            ca += 1
        elif ch == 'b':
            if stage == 2:
                valid = False
                break
            if stage == 0:
                stage = 1
            cb += 1
        else:
            if stage < 1:
                valid = False
                break
            if stage == 1:
                stage = 2
            cc += 1

    if not valid or ca == 0 or cb == 0:
        return "NO"
    return "YES" if (cc == ca or cc == cb) else "NO"

# provided sample
assert run("aaabccc\n") == "YES"

# custom cases
assert run("aaaabbbcccc\n") == "YES"
assert run("aaaa\n") == "NO"
assert run("ab\n") == "NO"
assert run("aabbccc\n") == "NO"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `aaaa` | NO | missing `b` and `c` phase requirement |
| `ab` | NO | missing `c` and no valid `c` equality |
| `aabbccc` | NO | `c` count mismatch condition |

## Edge Cases

A critical edge case is when the string has correct ordering but fails the count constraint. For input `aaabbbcccc`, the scan produces `ca=3`, `cb=3`, `cc=4`. The stage logic accepts it structurally, but final check rejects it since `cc` matches neither `ca` nor `cb`.

Another edge case is when transitions occur too early. For `baaa`, the first character `b` forces stage `1`, but encountering `a` afterwards violates the rule immediately, causing early rejection before any counting matters.

A final case is a minimal valid structure like `abc`. The scan sets `ca=1`, `cb=1`, `cc=1`, and since `cc == ca == cb`, it is accepted, confirming that equality of all three segments is handled naturally by the final condition.
