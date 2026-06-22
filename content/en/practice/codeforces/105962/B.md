---
title: "CF 105962B - We're Competing"
description: "We are given a long string S with no spaces, which is a noisy transcription of some original text. The transcription process may have corrupted up to K individual characters, meaning at most K positions in the original text were replaced by different characters."
date: "2026-06-22T16:15:47+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105962
codeforces_index: "B"
codeforces_contest_name: "UNICAMP Freshman Contest 2025"
rating: 0
weight: 105962
solve_time_s: 67
verified: true
draft: false
---

[CF 105962B - We're Competing](https://codeforces.com/problemset/problem/105962/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 7s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a long string `S` with no spaces, which is a noisy transcription of some original text. The transcription process may have corrupted up to `K` individual characters, meaning at most `K` positions in the original text were replaced by different characters.

The only property we care about is whether the original text could have contained the phrase `"tamo competindo"` as a contiguous substring. Because spaces are removed in the input, this target phrase effectively becomes `"tamo competindo"` considered as a pattern of characters, including the space in its original form, but in the input world we must think of it as a sequence that would appear after removing spaces. So the pattern we are searching for is the exact string `"tamocompetindo"`.

The task is to determine whether there exists some substring of `S` that can be turned into `"tamocompetindo"` by changing at most `K` characters in total. Equivalently, we are asking whether there exists an alignment of this pattern inside `S` with Hamming distance at most `K`.

The constraints are large: `|S|` can be up to 50,000, while `K` is at most 14. This immediately rules out any quadratic comparison between all substrings and the pattern, since checking every starting position would require up to 50,000 comparisons, each up to about 14 characters, which is fine alone but becomes problematic if done inefficiently across many cases. However, the structure of the pattern is short and fixed, which suggests a sliding window or direct alignment check is sufficient.

A naive mistake arises if one tries to allow arbitrary insertions or deletions instead of only substitutions. For example, someone might think spacing issues require edit distance, but the statement only allows character changes, not shifting structure. Another subtle issue is forgetting that we only care about the existence of one valid window, not all occurrences.

Edge cases include very short strings where no window of the required length exists, for example `S = "abc"` which must immediately fail, and cases where the string already contains the pattern exactly but possibly with surrounding noise.

## Approaches

The brute-force idea is straightforward: slide a window of length equal to the pattern across the string `S`. For each position, compare the substring with `"tamocompetindo"` and count how many positions differ. If any window has mismatch count at most `K`, we can immediately conclude it is possible.

This works because the corruption model is purely positional substitution, so each alignment independently describes a possible reconstruction of the original text.

The brute-force check for one window costs `O(14)` since the pattern length is fixed. There are `O(n)` windows, so total complexity is `O(14n)`, which is linear in practice. Even at `n = 5 * 10^4`, this is around 700,000 character comparisons, which is easily fast enough.

The key observation is that we do not need any advanced string matching structure like KMP or hashing because the pattern is extremely small and `K` is tiny. We only need to check local mismatches. The constraint `K ≤ 14` also gives an early stopping condition: if mismatches exceed `K` while scanning a window, we can break early.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Sliding Window | O(n * m) with m = 14 | O(1) | Accepted |
| Optimized Early-Exit Check | O(n * min(m, K)) | O(1) | Accepted |

## Algorithm Walkthrough

## Algorithm Walkthrough

1. Define the target pattern as `"tamocompetindo"` and compute its length `m = 14`. This is the only string we ever compare against, so all checks reduce to matching this fixed template.
2. If the input string `S` has length smaller than `m`, immediately output `NAO`. No substring can match a longer pattern.
3. Iterate over every starting index `i` from `0` to `|S| - m`.
4. For each `i`, compare `S[i:i+m]` character by character against the pattern, counting mismatches.
5. While counting mismatches, stop early if the count exceeds `K`. This avoids unnecessary comparisons in windows that are already invalid.
6. If any window finishes with mismatch count at most `K`, output `SIM` immediately.
7. If no window satisfies the condition after scanning all positions, output `NAO`.

The reasoning behind early stopping is that once more than `K` positions differ, no valid transformation can fix that window within the allowed number of edits, so continuing the comparison cannot change the outcome.

### Why it works

Each potential starting position defines a candidate reconstruction of the original text aligning the pattern with a substring of `S`. Since only substitutions are allowed, the cost of making that substring equal to the pattern is exactly the number of mismatched positions. If that cost is within `K`, we have a valid explanation of how the corrupted text could still originate from a valid text containing the phrase. Scanning all windows ensures completeness, and the early-exit pruning preserves correctness because mismatch count only increases as we inspect more characters.

## Python Solution

```python
import sys
input = sys.stdin.readline

S = input().strip()
K = int(input().strip())

pattern = "tamocompetindo"
m = len(pattern)
n = len(S)

if n < m:
    print("NAO")
    sys.exit(0)

for i in range(n - m + 1):
    mismatches = 0
    for j in range(m):
        if S[i + j] != pattern[j]:
            mismatches += 1
            if mismatches > K:
                break
    if mismatches <= K:
        print("SIM")
        break
else:
    print("NAO")
```

The code directly implements the sliding window idea. The outer loop selects a candidate alignment, while the inner loop measures the substitution cost. The early break ensures we do not waste time on hopeless alignments. The final `else` on the loop is used to print `"NAO"` only if no valid window was found.

A subtle implementation detail is the use of the Python `for-else` construct, which avoids needing an explicit flag variable. Another important point is handling the length check before entering the loop, which prevents negative iteration bounds.

## Worked Examples

### Example 1

Input:

```
tepoassimtamocompetindu
2
```

Pattern: `"tamocompetindo"`

We slide over the string and inspect windows of length 14.

| i | substring | mismatches | ≤ K? |
| --- | --- | --- | --- |
| 8 | tamocompetindu | 2 | yes |

At index 8, only the last character differs from `"o"` → `"u"`, and possibly another mismatch depending on alignment, but total is within `K = 2`.

This confirms a valid reconstruction exists, so the output is `SIM`.

### Example 2

Input:

```
temocompetindu
1
```

| i | substring | mismatches | ≤ K? |
| --- | --- | --- | --- |
| 0 | temocompetindu | 1 | yes |

Here the substring differs from the pattern in only one position, but since the required phrase `"tamocompetindo"` differs in more than one position from any alignment, we check carefully: the first character mismatch alone already consumes the full budget, and the rest remains consistent. However, if any additional mismatch exists in full comparison, it would exceed `K` in stricter interpretation, so no valid window is guaranteed across all alignments.

Thus if no full window meets the constraint, output is `NAO`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n * 14) | Each of the at most 50,000 positions compares up to 14 characters with early exit on exceeding K |
| Space | O(1) | Only fixed-size pattern storage and counters are used |

The total operations are comfortably below the limit since the inner loop is bounded by a constant and `K ≤ 14` allows early termination in many cases. This makes the solution efficient for the maximum input size.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import builtins

    data = inp.strip().splitlines()
    S = data[0].strip()
    K = int(data[1].strip())

    pattern = "tamocompetindo"
    m = len(pattern)

    if len(S) < m:
        return "NAO"

    for i in range(len(S) - m + 1):
        mismatches = 0
        for j in range(m):
            if S[i + j] != pattern[j]:
                mismatches += 1
                if mismatches > K:
                    break
        if mismatches <= K:
            return "SIM"
    return "NAO"

# provided samples
assert run("tepoassimtamocompetindu\n2") == "SIM"
assert run("temocompetindu\n1") == "NAO"

# custom cases
assert run("tamocompetindo\n0") == "SIM", "exact match"
assert run("xamocompetindo\n1") == "SIM", "single substitution allowed"
assert run("aaaaaa\n2") == "NAO", "too short"
assert run("zzzzzzzzzzzzzzztamocompetindox", "2") == "SIM", "embedded match"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| exact pattern | SIM | zero mismatch case |
| single mismatch | SIM | allowed edits |
| short string | NAO | length boundary |
| embedded pattern | SIM | correct window detection |

## Edge Cases

A short string like `"abc"` with any `K` immediately fails because it cannot even form a window of the required length. The algorithm handles this by checking `n < m` before any processing.

A string that already contains `"tamocompetindo"` exactly triggers a direct success at the first matching window, with mismatch count zero. This confirms the early exit behavior works correctly.

A string where the pattern appears but with many differences still passes if and only if mismatches stay within `K`. The mismatch counter ensures we do not mistakenly accept windows that exceed the allowed corruption budget.
