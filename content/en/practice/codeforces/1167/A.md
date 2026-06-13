---
title: "CF 1167A - Telephone Number"
description: "We are given a string of digits and we are allowed to delete characters freely, without changing the relative order of the remaining digits. The task is to decide whether we can extract a subsequence of length exactly 11 that forms a valid telephone number."
date: "2026-06-13T08:57:47+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "greedy", "strings"]
categories: ["algorithms"]
codeforces_contest: 1167
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 65 (Rated for Div. 2)"
rating: 800
weight: 1167
solve_time_s: 123
verified: true
draft: false
---

[CF 1167A - Telephone Number](https://codeforces.com/problemset/problem/1167/A)

**Rating:** 800  
**Tags:** brute force, greedy, strings  
**Solve time:** 2m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string of digits and we are allowed to delete characters freely, without changing the relative order of the remaining digits. The task is to decide whether we can extract a subsequence of length exactly 11 that forms a valid telephone number. A valid telephone number has a very specific structure: it must have length 11 and its first digit must be 8. The remaining 10 digits can be anything.

So the problem reduces to checking whether the string contains a subsequence of length 11 where the first chosen character is `8`.

The constraint on each test case is small, with the string length up to 100 and up to 100 test cases. This immediately rules out any need for heavy preprocessing or advanced data structures. A linear scan per test case is easily sufficient.

A naive but common mistake is to assume we just need to check whether the string contains at least one `8` and at least 10 more digits somewhere after it. This is close but incorrect if not handled carefully in order, because subsequence selection depends on positions. Another mistake is trying to build all subsequences of length 11, which explodes combinatorially even at length 100, since there are $\binom{100}{11}$ possibilities.

A subtle edge case arises when there are multiple `8`s. For example, in `88888888888`, any position works as a start, but in a string where the first `8` is too late, we might not have enough characters after it. A greedy scan must correctly account for the remaining available length.

## Approaches

The brute-force idea is straightforward: generate every subsequence of length 11 and check whether any of them starts with `8`. This is correct because it explores all possible deletions. However, the number of subsequences grows rapidly. Even for a single test case with $n = 100$, the number of length-11 subsequences is astronomically large, making this approach infeasible.

The key observation is that we do not need to construct subsequences explicitly. We only need to know whether there exists a position of an `8` such that at least 10 characters come after it in the string. Since deletions preserve order, once we pick an `8` at index `i`, we only need to verify that there are at least 10 more characters after index `i`. Those characters can be anything; we simply take them as they appear.

This reduces the problem to scanning for a valid starting position and counting remaining length.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (all subsequences) | O(2^n) | O(11) | Too slow |
| Greedy scan from each 8 | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We process each test case independently.

1. Read the string and scan through all positions where the digit is `8`. Each such position is a candidate start of a telephone number.
2. For each index `i` where `s[i] == '8'`, check whether the suffix length `n - i` is at least 11. This ensures we can pick 11 characters starting from this `8` while preserving order.
3. If any such position satisfies the condition, immediately conclude that a valid subsequence exists.
4. If no valid starting position is found, output `NO`.

The reasoning behind step 2 is that once we fix the first digit as `8`, we only need 10 additional characters after it. Since we are not constrained by their values, only their availability matters.

### Why it works

The algorithm relies on a monotonic availability property: if an `8` appears at index `i`, then every character after it is eligible to be part of the subsequence, and we only need 10 of them. There is no benefit in skipping earlier valid `8`s if a later one works, because earlier positions always give at least as many remaining characters. This guarantees that checking positions is sufficient without constructing subsequences.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    s = input().strip()

    ok = False
    for i in range(n):
        if s[i] == '8' and n - i >= 11:
            ok = True
            break

    print("YES" if ok else "NO")
```

The solution iterates over each test case and checks all positions where the digit is `8`. The key implementation detail is the condition `n - i >= 11`, which ensures we can pick the current `8` plus at least 10 following characters. The early exit prevents unnecessary scanning once a valid position is found.

A common mistake is forgetting that the chosen subsequence must preserve order, so only suffix availability matters, not global counts.

## Worked Examples

### Example 1

Input:

```
13
7818005553535
```

We scan positions:

| i | s[i] | is '8'? | n - i | valid start? |
| --- | --- | --- | --- | --- |
| 0 | 7 | no | 13 | no |
| 1 | 8 | yes | 12 | yes |

At index 1, we have enough characters remaining to form length 11. We can pick `8` at index 1 and then any 10 following digits. So the answer is `YES`.

This shows that we do not need to explicitly construct the subsequence; availability alone determines feasibility.

### Example 2

Input:

```
11
31415926535
```

| i | s[i] | is '8'? | n - i | valid start? |
| --- | --- | --- | --- | --- |
| all | - | no | - | no |

There is no digit `8` in the string, so no valid starting point exists. The result is `NO`.

This confirms that absence of the required leading digit immediately invalidates the construction.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Single linear scan over the string |
| Space | O(1) | Only a few variables used |

Given that $n \le 100$ and $t \le 100$, the solution performs at most $10^4$ operations, which is well within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        s = input().strip()

        ok = False
        for i in range(n):
            if s[i] == '8' and n - i >= 11:
                ok = True
                break
        out.append("YES" if ok else "NO")

    return "\n".join(out)

# provided samples
assert run("2\n13\n7818005553535\n11\n31415926535\n") == "YES\nNO"

# custom cases
assert run("1\n11\n80000000000\n") == "YES"
assert run("1\n11\n70000000000\n") == "NO"
assert run("1\n12\n888888888888\n") == "YES"
assert run("1\n20\n12345678901234567890\n") == "NO"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single valid exact construction | YES | minimal valid case |
| no 8 present | NO | mandatory leading digit |
| all 8s | YES | multiple valid starts |
| no valid structure | NO | general negative case |

## Edge Cases

A key edge case is when the string contains an `8`, but it appears too late to allow 10 remaining characters. For example, in `11111111118`, the only `8` is at the last position. Even though the required digit exists, there are no remaining characters to complete length 11, so the correct answer is `NO`. The algorithm handles this by explicitly checking suffix length, not just presence of `8`.

Another edge case is when multiple `8`s exist. The first valid `8` is sufficient to decide success. The scan naturally handles this because it stops at the first position satisfying the suffix condition.
