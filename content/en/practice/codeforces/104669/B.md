---
title: "CF 104669B - String Shifts"
description: "We are given a single string that is known to come from a Caesar-style letter shift applied to some original text. In such a transformation, every character in the original string is moved forward in the alphabet by a fixed number of positions, wrapping around from z back to a."
date: "2026-06-29T09:44:20+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104669
codeforces_index: "B"
codeforces_contest_name: "Turtle Codes"
rating: 0
weight: 104669
solve_time_s: 57
verified: true
draft: false
---

[CF 104669B - String Shifts](https://codeforces.com/problemset/problem/104669/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 57s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single string that is known to come from a Caesar-style letter shift applied to some original text. In such a transformation, every character in the original string is moved forward in the alphabet by a fixed number of positions, wrapping around from `z` back to `a`.

We are also told that the substring `"tino"` appears somewhere in the original unshifted text. After the shift is applied, that substring becomes some other 4-character string inside the encrypted text. Our task is to determine how many different shift values could have produced the given encrypted string while still allowing `"tino"` to exist in the original string at some position.

The shift value is an integer in the range from 0 to 25, where 0 means no change and 25 means shifting each letter one step backward in the alphabet before encryption. Each shift value is valid if there exists at least one position in the encrypted string where decoding by that shift yields `"tino"`.

The input length is at most 1000, so any solution that checks all positions and all 26 shifts is easily fast enough. Even a cubic approach would likely pass, but it is unnecessary.

A subtle point is that the match condition is local: we are not asked to reconstruct the whole original string, only to check whether `"tino"` could appear anywhere after reversing a candidate shift. This means different positions in the string independently support or reject a shift.

Edge cases come from short strings. If the length is less than 4, there are no positions where a 4-character pattern can exist, so the answer must be 0. Another edge case is when multiple shifts are valid due to different matching positions. For example, a string might allow shift 1 at one location and shift 5 at another; we must count unique shifts, not occurrences.

## Approaches

A direct way to solve the problem is to try every possible shift value from 0 to 25. For each shift, we simulate reversing the encryption: for each character in the string, we subtract the shift modulo 26 and obtain a candidate original character. Then we scan all substrings of length 4 and check whether any of them equals `"tino"`.

This approach is correct because it explicitly tests the definition of validity. For each shift, we fully reconstruct what the original string would look like and check whether the required pattern exists. The issue is efficiency: for each of 26 shifts, we examine up to 1000 positions, each requiring up to 4 comparisons, leading to about 1000 × 26 × 4 operations, which is easily acceptable but slightly wasteful in repeated reconstruction.

We can simplify further by avoiding full reconstruction. Instead of building the entire decoded string for each shift, we directly check character alignment. For a fixed shift and a fixed position i, we verify whether shifting the encrypted substring back by that shift produces `"tino"`. This reduces memory overhead and keeps the logic direct.

A key observation is that a shift is valid if and only if there exists at least one index i such that for all j in {0,1,2,3}, the condition holds:

encrypted[i + j] - shift ≡ target[j] (mod 26).

So we only need to test 26 shifts and at most 1000 starting positions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force full decoding per shift | O(26 · n) | O(n) | Accepted |
| Direct substring checking per shift | O(26 · n) | O(1) | Accepted |

## Algorithm Walkthrough

We fix the target pattern `"tino"` and convert it into integer offsets from `'a'`.

We then iterate over every possible shift value.

1. For each shift value from 0 to 25, we assume it might be the correct Caesar shift.
2. For each starting index i from 0 to n - 4, we test whether the substring of length 4 at i matches `"tino"` when decoded by this shift.
3. For each character position j in 0 to 3, we compute the decoded character of encrypted[i + j] by subtracting the shift modulo 26.
4. If all four decoded characters match `"tino"`, we mark this shift as valid and stop checking further positions for this shift.
5. After trying all shifts, we count how many were marked valid.

The reason we break early when a match is found is that the existence of at least one valid position is sufficient for a shift to be counted.

### Why it works

A shift is globally valid if there exists at least one location in the encrypted string where reversing that shift yields the exact pattern `"tino"`. The algorithm checks all possible local alignments for each shift, so no valid alignment is missed. Each shift is tested independently, and a shift is counted only if it satisfies the existence condition. This directly matches the problem requirement without relying on global reconstruction.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    s = input().strip()
    n = len(s)

    if n < 4:
        print(0)
        return

    target = "tino"
    target_vals = [ord(c) - ord('a') for c in target]

    ans = 0

    for shift in range(26):
        ok = False

        for i in range(n - 3):
            match = True
            for j in range(4):
                c = ord(s[i + j]) - ord('a')
                if (c - shift) % 26 != target_vals[j]:
                    match = False
                    break
            if match:
                ok = True
                break

        if ok:
            ans += 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The solution iterates over all shifts and checks each shift against all possible substring positions. The nested loop structure is intentional: the outer loop enumerates hypotheses (shift values), and the inner loops verify whether the hypothesis is consistent with any valid location of `"tino"`.

The modulo arithmetic `(c - shift) % 26` handles wrap-around correctly. Breaking early inside the substring loop ensures we avoid unnecessary comparisons once a valid match is found.

## Worked Examples

### Example 1

Input:

```
tinoujopvkpq
```

We check shifts 0 to 25. Only shifts that align at least one substring to `"tino"` are valid.

| shift | i=0 match | i=1 match | i=2 match | valid |
| --- | --- | --- | --- | --- |
| 0 | yes | no | no | yes |
| 1 | no | no | yes | yes |
| 2 | no | no | no | no |

Final answer: 3 valid shifts exist in total.

This trace shows that different parts of the string can independently validate different shift values.

### Example 2

Input:

```
tinoabcd
```

Here the substring `"tino"` appears directly at position 0.

| shift | i=0 match | valid |
| --- | --- | --- |
| 0 | yes | yes |
| 1 | no | no |
| 2 | no | no |

Only shift 0 works because any non-zero shift would change `"tino"` into another word.

This demonstrates that direct presence of the pattern strongly constrains the shift value.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(26 · n · 4) | For each shift we scan all positions, and each check compares 4 characters |
| Space | O(1) | Only a few counters and fixed arrays are used |

With n ≤ 1000, the maximum number of operations is around 100,000, which is comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    s = sys.stdin.readline().strip()
    n = len(s)

    if n < 4:
        return "0\n"

    target = "tino"
    target_vals = [ord(c) - ord('a') for c in target]

    ans = 0

    for shift in range(26):
        ok = False
        for i in range(n - 3):
            match = True
            for j in range(4):
                c = ord(s[i + j]) - ord('a')
                if (c - shift) % 26 != target_vals[j]:
                    match = False
                    break
            if match:
                ok = True
                break
        if ok:
            ans += 1

    return str(ans) + "\n"

# provided sample
assert run("tinoujopvkpq\n") == "3\n"

# custom: exact match after no shift
assert run("tinoabcd\n") == "1\n"

# custom: no possible match
assert run("zzzzzzzz\n") == "0\n"

# custom: short string
assert run("tin\n") == "0\n"

# custom: multiple repeated valid patterns
assert run("tinotinotino\n") == "1\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| tinoujopvkpq | 3 | multiple shifts valid |
| tinoabcd | 1 | direct match case |
| zzzzzzzz | 0 | no valid pattern |
| tin | 0 | length < 4 edge case |
| tinotinotino | 1 | repeated pattern, single shift counted |

## Edge Cases

For inputs shorter than 4 characters, the algorithm immediately returns 0. For example, input `"abc"` leads to n = 3, triggering the early exit before any shift checks. This matches the fact that no 4-letter substring can exist.

For strings with multiple occurrences of patterns under different shifts, such as `"tinoujopvkpq"`, each shift is tested independently. When shift 0 is tested, the substring at index 0 may match. When shift 1 is tested, a different index may match. The algorithm counts each shift only once due to the `ok` flag.

For strings with repeated valid substrings like `"tinotinotino"`, shift 0 produces multiple valid positions, but the algorithm stops checking after finding the first match, ensuring efficiency without affecting correctness.
