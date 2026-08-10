---
title: "CF 102394F - Fixing Banners"
description: "We have exactly six old banners. From each banner, we must choose exactly one character, giving us exactly six characters in total. We may reorder those six characters freely, and the final word must be harbin."
date: "2026-08-10T19:07:27+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102394
codeforces_index: "F"
codeforces_contest_name: "The 2019 China Collegiate Programming Contest Harbin Site"
rating: 0
weight: 102394
solve_time_s: 81
verified: true
draft: false
---

[CF 102394F - Fixing Banners](https://codeforces.com/problemset/problem/102394/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 21s  
**Verified:** yes  

## Solution
## Problem Understanding

We have exactly six old banners. From each banner, we must choose exactly one character, giving us exactly six characters in total. We may reorder those six characters freely, and the final word must be `harbin`.

The key restriction is that two characters cannot come from the same banner, because every banner contributes exactly one character. Since the letters of `harbin` are all different, the task is equivalent to asking whether the six banners can be matched one-to-one with the six required letters so that every banner contains its assigned letter.

For each test case, the input consists of six non-empty lowercase strings. We need to print `Yes` if such a one-to-one assignment exists and `No` otherwise. The input contains up to 50,000 test cases, but the total number of characters across every banner is at most (2\cdot10^6). That total-length bound strongly suggests that scanning every input character a constant number of times is safe. An algorithm that depends polynomially on the banner lengths, such as trying many combinations of positions, would be far too expensive.

There are two subtle cases that can fool a frequency-based solution. First, having enough copies of every required letter in the combined banners is not sufficient because one banner cannot provide two letters. For example,

```
1
harbin
x
x
x
x
x
```

has every required letter somewhere, but the answer is `No`. The first banner contains all six useful letters, while the other five banners contain none of them, so six different banners cannot supply the six letters.

A second issue is that a required letter may appear many times in one banner, but those copies still represent only one usable character because we must cut exactly one character from that banner. For example,

```
1
hhhhhh
aaaaaa
rrrrrr
bbbbbb
iiiiii
nnnnnn
```

has many copies of every required letter, but the answer is `Yes` because each required letter is available from its own banner. In contrast,

```
1
hhhhhh
hhhhhh
aaaaaa
rrrrrr
bbbbbb
iiiiii
```

has no banner containing `n`, so the answer is `No`.

The problem comes from the fact that availability and assignment are different questions. We first need to know which required letters each banner can provide, and then we need to check whether those possibilities can be combined without using a banner twice.

## Approaches

A direct brute-force solution can choose one position from each of the six banners. If their lengths are (L_1,L_2,\ldots,L_6), there are

[
L_1L_2L_3L_4L_5L_6
]

different choices. For every choice, we can check whether the selected six characters can be rearranged into `harbin`. This is correct because every possible way of taking one character from every banner is considered.

The problem is the number of choices. Under the total-length limit of (2\cdot10^6), the product is maximized when the six lengths are as balanced as possible, namely two lengths of 333,334 and four lengths of 333,333. That already gives

[
333334^2\cdot333333^4
]

candidate selections, roughly (1.37\cdot10^{33}). Even checking one candidate in constant time would be impossible.

The brute force works because it explicitly respects the one-character-per-banner restriction, but it explores the actual character positions even though their positions inside a banner do not matter. For the target word, a banner is relevant only through which of the six letters `h`, `a`, `r`, `b`, `i`, and `n` it contains.

This observation reduces each banner to a six-bit mask. Bit zero can represent `h`, bit one `a`, and so on. If a banner contains `h` and `r`, its mask records exactly those two possibilities. We then need to choose one distinct target letter from each of the six masks.

Because there are only six target letters, we can represent the set of already chosen letters by another six-bit mask. A small dynamic programming procedure processes the banners one at a time. For each banner, we either do not use a particular target letter from it, or choose one currently unused letter that the banner contains. After all six banners have been processed, the full mask means every required letter has been assigned to a different banner.

The state space contains only (2^6=64) masks, so the assignment part is tiny. The only work depending on the actual input size is scanning the characters to construct the six masks.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(L_1L_2L_3L_4L_5L_6)) | (O(1)) | Too slow |
| Optimal | (O(S+6^2 2^6)) | (O(2^6)) | Accepted |

Here (S) is the total length of the six strings in one test case. Since six and (2^6) are constants, the optimal solution is effectively linear in the input size.

## Algorithm Walkthrough

1. Define the target as `harbin` and assign one bit to each of its six letters. For example, `h` uses bit 0, `a` uses bit 1, and `n` uses bit 5. Since all six target letters are distinct, every valid construction corresponds to selecting every bit exactly once.
2. Read the six banner strings and build one mask for each banner. While scanning a string, if its current character is one of the six target letters, set the corresponding bit in that banner's mask. Repeated occurrences of the same character do not matter because a banner can contribute only one character.
3. Create a dynamic programming array `dp` with 64 states. `dp[mask]` means that, after processing some prefix of the banners, it is possible to have selected exactly the target letters represented by `mask`, using at most one character from every processed banner.
4. Initially set `dp[0]` to true because before processing any banner, no target letter has been selected.
5. Process the banners one by one. For every reachable state `mask`, inspect every target letter represented in the current banner's mask. If that letter's bit is not already present in `mask`, create the new state `mask | bit`. This represents taking that letter from the current banner.
6. Keep the possibility of not using a particular banner's useful letter when forming intermediate states. This is represented by carrying the existing state forward. Although the final solution must use exactly one character from every banner, a banner may contribute a character that is not part of `harbin`, and such a choice has no effect on the target-letter assignment. Since there are exactly six banners and exactly six required letters, any state containing all six target letters after processing all banners necessarily uses one distinct useful letter from every banner.
7. After all six banners have been processed, check whether the state `(1 << 6) - 1` is reachable. If it is, print `Yes`; otherwise print `No`.

### Why it works

The invariant is that `dp[mask]` is true exactly when the processed banners can provide the distinct target letters represented by `mask`, with no banner contributing more than one of them. When a transition adds a bit, that bit was not previously selected, so no required letter is used twice, and the transition takes the new letter from the current banner, so no banner contributes twice. Conversely, any valid assignment can be followed banner by banner: whenever its assigned letter belongs to `harbin`, the corresponding transition is available. Thus the full six-bit mask is reachable exactly when the six banners can supply all six required letters one-to-one.

## Python Solution

```python
import sys
input = sys.stdin.readline

TARGET = "harbin"
BIT = {ch: 1 << i for i, ch in enumerate(TARGET)}
FULL = (1 << 6) - 1

def solve_case():
    masks = []

    for _ in range(6):
        s = input().strip()
        mask = 0

        for ch in s:
            bit = BIT.get(ch)
            if bit is not None:
                mask |= bit

        masks.append(mask)

    dp = [False] * (1 << 6)
    dp[0] = True

    for available in masks:
        ndp = dp[:]

        for mask in range(1 << 6):
            if not dp[mask]:
                continue

            choices = available & ~mask

            while choices:
                bit = choices & -choices
                choices -= bit
                ndp[mask | bit] = True

        dp = ndp

    return "Yes" if dp[FULL] else "No"

def main():
    t = int(input())
    answer = []

    for _ in range(t):
        answer.append(solve_case())

    sys.stdout.write("\n".join(answer))

if __name__ == "__main__":
    main()
```

The `TARGET` string fixes the correspondence between each required character and one bit. The dictionary lookup turns a target character into its bit in constant time, while characters outside `harbin` can simply be ignored.

For each banner, `mask` records only whether a required character occurs at least once. This is enough because taking the first `h` or the last `h` from the same banner makes no difference. The `get` call avoids a separate membership test and also gives us a convenient way to ignore irrelevant lowercase letters.

The dynamic programming array has 64 entries because there are six independent yes-or-no choices about whether each target letter has already been supplied. `ndp = dp[:]` preserves the existing states, corresponding to processing the current banner without assigning one of its target letters to the tracked construction.

The expression `available & ~mask` extracts target letters available in the current banner that have not yet been selected. The low-bit operation `choices & -choices` picks one such letter at a time. This is a standard bitmask technique that avoids looping over all 64 masks for every possible character.

There is no indexing over banner positions after the masks have been built, so there are no character-position boundary issues. Python integers have arbitrary precision, although the largest value used here is only 63. The input is processed line by line, and the output is accumulated and written once, which is appropriate for as many as 50,000 test cases.

## Worked Examples

For the first sample case, the six banners are `welcome`, `toparticipate`, `inthe`, `ccpccontest`, `inharbin`, and `inoctober`. Their relevant target-letter masks are shown below.

| Banner | Available target letters | Mask state |
| --- | --- | --- |
| `welcome` | `e` | 0 |
| `toparticipate` | `a`, `i` | 10 |
| `inthe` | `i`, `n` | 40 |
| `ccpccontest` | `n` | 32 |
| `inharbin` | `h`, `a`, `r`, `b`, `i`, `n` | 63 |
| `inoctober` | `i`, `n`, `b`, `r` | 44 |

The first banner cannot supply any character from `harbin`, so no useful state is created there. The second and third banners can provide some of the required letters, and later banners provide additional choices. However, `h` occurs only in `inharbin`, so that banner must supply `h`. Once that is chosen, the remaining five banners still cannot provide all of `a`, `r`, `b`, `i`, and `n` without reusing a banner or missing a required letter. The full mask is unreachable.

The final state is consequently false, giving `No`.

For the second sample case, the six banners are `harvest`, `belong`, `ninja`, `reset`, `amazing`, and `intriguing`.

| Banner | Useful letters | Mask |
| --- | --- | --- |
| `harvest` | `h`, `a`, `r` | 7 |
| `belong` | `b`, `n` | 33 |
| `ninja` | `i`, `n`, `a` | 42 |
| `reset` | `r` | 4 |
| `amazing` | `a`, `i`, `n` | 50 |
| `intriguing` | `i`, `n`, `r` | 44 |

One valid assignment is to take `h` from `harvest`, `b` from `belong`, `i` from `ninja`, `r` from `reset`, `a` from `amazing`, and `n` from `intriguing`. Each letter comes from a different banner, so the full six-bit mask becomes reachable.

The algorithm eventually reaches mask 63, so this case produces `Yes`. The trace also demonstrates why a banner containing several useful letters does not cause a problem. The DP chooses at most one of them for that banner.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(S+6^2 2^6)) | (S) characters are scanned to build masks, followed by a constant-size DP |
| Space | (O(2^6)) | The DP stores only 64 boolean states and six banner masks |

Across all test cases, the total input length is at most (2\cdot10^6), so the character-scanning portion performs only linear work in that bound. The remaining DP has a fixed cost of at most a few thousand operations per case, which is easily manageable even for 50,000 cases. The solution therefore fits comfortably within the stated 1 second time limit and 512 MB memory limit.

## Test Cases

```python
import sys
import io

TARGET = "harbin"
BIT = {ch: 1 << i for i, ch in enumerate(TARGET)}
FULL = (1 << 6) - 1

def solve_data(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    try:
        input = sys.stdin.readline
        t = int(input())
        ans = []

        for _ in range(t):
            masks = []

            for _ in range(6):
                s = input().strip()
                mask = 0

                for ch in s:
                    bit = BIT.get(ch)
                    if bit is not None:
                        mask |= bit

                masks.append(mask)

            dp = [False] * 64
            dp[0] = True

            for available in masks:
                ndp = dp[:]

                for mask in range(64):
                    if not dp[mask]:
                        continue

                    choices = available & ~mask

                    while choices:
                        bit = choices & -choices
                        choices -= bit
                        ndp[mask | bit] = True

                dp = ndp

            ans.append("Yes" if dp[FULL] else "No")

        return "\n".join(ans) + "\n"

    finally:
        sys.stdin = old_stdin

# Provided sample
sample = """\
2
welcome
toparticipate
inthe
ccpccontest
inharbin
inoctober
harvest
belong
ninja
reset
amazing
intriguing
"""
assert solve_data(sample) == "No\nYes\n", "provided sample"

# Minimum-size case: every banner contains exactly one required letter.
minimum = """\
1
h
a
r
b
i
n
"""
assert solve_data(minimum) == "Yes\n", "minimum-size valid case"

# All-equal values: no banner can provide six distinct target letters.
all_equal = """\
1
aaaa
aaaa
aaaa
aaaa
aaaa
aaaa
"""
assert solve_data(all_equal) == "No\n", "all-equal case"

# Several required letters are concentrated in one banner.
# Aggregate frequency is sufficient to fool a careless solution,
# but one banner can contribute only one character.
concentrated = """\
1
harbin
x
x
x
x
x
"""
assert solve_data(concentrated) == "No\n", "one-banner concentration"

# Every required letter exists, but two required letters are forced
# into the same banner, while another banner has no useful letter.
forced_conflict = """\
1
har
b
i
n
x
x
"""
assert solve_data(forced_conflict) == "No\n", "forced assignment conflict"

# Maximum total input length: exactly 2,000,000 characters.
# Each of the six banners contains its required letter once,
# so the answer is Yes.
lengths = [333334, 333334, 333333, 333333, 333333, 333333]
letters = "harbin"
large_lines = [
    letters[i] + "x" * (lengths[i] - 1)
    for i in range(6)
]
maximum = "1\n" + "\n".join(large_lines) + "\n"
assert sum(map(len, large_lines)) == 2_000_000
assert solve_data(maximum) == "Yes\n", "maximum-size case"

print("All tests passed.")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `h`, `a`, `r`, `b`, `i`, `n` | `Yes` | Minimum-size valid input and exact one-to-one assignment |
| Six copies of `aaaa` | `No` | All-equal values and missing required letters |
| `harbin` followed by five `x` strings | `No` | Prevents treating combined character frequencies as sufficient |
| `har`, `b`, `i`, `n`, `x`, `x` | `No` | Detects a forced assignment conflict between banners |
| Six strings totaling exactly 2,000,000 characters | `Yes` | Maximum total input size and linear scanning |

## Edge Cases

The first edge case is concentration of all useful letters in one banner. For

```
1
harbin
x
x
x
x
x
```

the first banner has mask 63 and every other banner has mask 0. The DP can move from mask 0 to any one-bit state while processing the first banner, but no later banner can add another bit. Mask 63 is unreachable, so the result is `No`. This is exactly the situation where simply counting occurrences across all six strings gives the wrong answer.

The second edge case is repeated copies of a character inside one banner. Consider

```
1
hhhh
aaaa
rrrr
bbbb
iiii
nnnn
```

Each banner's mask contains only one bit, regardless of the number of copies. The DP selects one different bit from each banner and reaches the full mask. The result is `Yes`. The repeated characters cannot be counted as multiple available resources because only one character may be cut from each banner.

The third edge case is a missing required character. For

```
1
har
b
i
n
x
x
```

the masks are `har`, `b`, `i`, `n`, empty, and empty. The DP can reach at most the four-bit combination `h`, `a`, `r`, `b`, `i`, `n` only if those letters can all be supplied by distinct banners, but `har` contains three required letters while it can contribute only one. The two empty banners cannot contribute anything. The full mask is unreachable, so the answer is `No`.

The maximum-size case tests a different boundary. Six strings can contain exactly 2,000,000 characters in total, for example with lengths 333,334, 333,334, 333,333, 333,333, 333,333, and 333,333. If each string contains its corresponding required letter once and the rest consists of irrelevant characters, the six masks are all different one-bit masks and the answer is `Yes`. The algorithm scans all 2,000,000 characters once and then performs only the fixed-size DP, so the large input size does not change the asymptotic behavior.
