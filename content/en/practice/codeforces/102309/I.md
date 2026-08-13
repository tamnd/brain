---
title: "CF 102309I - IPv6 Address of Orz Pandas"
description: "Each test case gives one non-negative integer representing a complete 128-bit IPv6 address. An IPv6 address has exactly eight 16-bit sections, so the first job is to write the integer as exactly 32 hexadecimal digits and split those digits into eight groups of four."
date: "2026-08-13T23:49:19+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102309
codeforces_index: "I"
codeforces_contest_name: "The 2019 \u201cOrz Panda\u201d Cup Programming Contest"
rating: 0
weight: 102309
solve_time_s: 99
verified: true
draft: false
---

[CF 102309I - IPv6 Address of Orz Pandas](https://codeforces.com/problemset/problem/102309/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 39s  
**Verified:** yes  

## Solution
## Problem Understanding

Each test case gives one non-negative integer representing a complete 128-bit IPv6 address. An IPv6 address has exactly eight 16-bit sections, so the first job is to write the integer as exactly 32 hexadecimal digits and split those digits into eight groups of four. Each group is then written without leading zeroes.

After that normalization, a consecutive run of zero-valued groups may be replaced by `::`, but only if the run contains at least two groups. The compression can be used at most once. Among all legal representations, we first want the one that leaves the fewest explicit sections, and then the lexicographically smallest representation. The official problem specifies up to 128-bit inputs, multiple test cases until EOF, and a 1 second, 256 MB limit.

The 128-bit bound is especially friendly here because an IPv6 address always becomes exactly eight groups. There is no input-dependent array of size (n), and no need for a complicated data structure. Even a method that examines every possible zero interval only has (8 \cdot 9 / 2 = 36) intervals to consider. Python's arbitrary-precision integers also remove the overflow concerns that would arise in languages whose standard integer type is smaller than 128 bits.

The first subtle case is a single zero group. For example, the integer `340282366920938463463374607431768145920` represents `ffff:ffff:ffff:ffff:ffff:ffff:ffff:0`. The correct output is `ffff:ffff:ffff:ffff:ffff:ffff:ffff:0`. A careless implementation might compress the final zero into `::`, producing `ffff:ffff:ffff:ffff:ffff:ffff:ffff::`, but a single omitted section is explicitly forbidden.

The second subtle case is an address containing no nonzero groups at all. For input `0`, the eight normalized groups are all `0`, and the correct output is `::`. Treating the all-zero address like an ordinary prefix and suffix can accidentally produce an empty string or an invalid single colon.

The third subtle case is when several zero runs have the same maximum length. Consider the eight groups `1:0:0:2:0:0:3:4`. Both `1::2:0:0:3:4` and `1:0:0:2::3:4` compress two zero groups and are equally good with respect to the number of remaining sections. The correct answer is `1:0:0:2::3:4`, because it is lexicographically smaller. A solution that simply chooses the first longest run will fail this case.

Finally, a zero run at the beginning or end needs special string construction. For `1`, the normalized groups are `0:0:0:0:0:0:0:1`, so the answer is `::1`. For `0`, both sides of the compressed run are empty, so the answer is exactly `::`, not `:`.

## Approaches

A direct brute-force solution is possible because there are only eight groups. After normalizing them, we can consider every interval `[l, r]` whose groups are all zero. There are at most 36 intervals, and intervals of length one are discarded. For every remaining interval, we construct the address obtained by replacing that interval with `::`, then compare candidates according to the required ordering. If there is no valid interval, the uncompressed normalized address is the answer.

This brute force is already fast enough for the actual problem. In the worst case there are 36 possible intervals, and constructing one candidate touches at most eight groups, so there are at most (36 \times 8 = 288) group-level operations per test case, apart from short string operations. There is no meaningful input size at which this approach becomes too slow under the given fixed eight-group representation. The address format itself prevents the usual (O(n^2)) explosion seen in variable-length problems.

We can simplify the search further by observing what the first optimization criterion means. Compressing a zero run of length (k) removes exactly (k) explicit groups and replaces them with one `::`. Thus the number of remaining sections is minimized precisely by choosing a longest zero run. A run of length one is never eligible, so only runs of length at least two matter.

Once the maximum run length is known, every candidate uses the same number of remaining groups and also removes the same number of characters. The only remaining criterion is lexicographic order. For equal-length zero runs, choosing the later run is always lexicographically smaller. At the first position where two candidates differ, the candidate that compresses the earlier run contains `:`, while the candidate that leaves that zero group explicit contains `0`. Since `0` is lexicographically smaller than `:`, the later run wins. We can either use this fact directly or, more robustly, construct candidates for all maximum-length runs and take Python's `min`.

The optimal implementation scans the eight groups once to find the longest zero runs, constructs candidates only for runs of that maximum length, and takes the lexicographically smallest one. The asymptotic complexity is still (O(8)), which is simply (O(1)), but the reasoning directly reflects the optimization criteria instead of enumerating irrelevant intervals.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(8²) | O(8) | Accepted |
| Optimal | O(8) | O(8) | Accepted |

## Algorithm Walkthrough

1. Convert the input integer to hexadecimal with exactly 32 digits. Padding is necessary because leading zero bits are still part of the 128-bit address. Split the result into eight groups of four hexadecimal digits and remove leading zeroes from each group, leaving `"0"` when a group is entirely zero.
2. Scan the eight normalized groups from left to right. Whenever a zero group is found, continue until the zero run ends and record its starting position and length. Keep the maximum length found, ignoring runs shorter than two groups because RFC-style compression cannot represent a single omitted section.
3. If no run of length at least two exists, join the eight normalized groups with colons and return that address. There is no legal use of `::` in this situation.
4. For every zero run whose length equals the maximum length, construct a candidate address by replacing that complete run with `::`. The groups before and after the run are kept unchanged. Considering only maximum-length runs is sufficient because every shorter run leaves more explicit sections.
5. Compare the candidates lexicographically and return the smallest one. This handles runs at the beginning, middle, and end without needing separate tie-breaking logic.
6. If the selected run covers all eight groups, the construction produces `::`. If it starts at the first group, the result has the form `::suffix`; if it ends at the last group, it has the form `prefix::`. These cases are handled explicitly when joining the two sides.

Why it works: after normalization, every legal abbreviation differs only in which consecutive zero run is replaced by `::`. A run of length (k) leaves (8-k) explicit sections, so every optimal abbreviation must use a longest legal zero run. Among runs of equal maximum length, constructing all candidates and selecting the lexicographically smallest one exactly implements the final tie-break rule. Every constructed candidate represents the same original eight groups, because `::` stands for precisely the omitted zero groups. Thus the selected candidate satisfies all three requirements: legal compression, the minimum possible number of remaining sections, and the smallest lexicographic representation among those choices.

## Python Solution

```python
import sys
input = sys.stdin.readline

def make_candidate(groups, l, r):
    left = groups[:l]
    right = groups[r + 1:]

    # Two empty fields joined by ':' produce '::'.
    return ":".join(left + ["", ""] + right)

def abbreviate(x):
    # Exactly 32 hexadecimal digits correspond to eight 16-bit groups.
    h = f"{x:032x}"
    groups = []

    for i in range(0, 32, 4):
        part = h[i:i + 4]
        value = part.lstrip("0")
        groups.append(value if value else "0")

    best_len = 0
    runs = []

    i = 0
    while i < 8:
        if groups[i] != "0":
            i += 1
            continue

        j = i
        while j < 8 and groups[j] == "0":
            j += 1

        length = j - i

        if length >= 2:
            if length > best_len:
                best_len = length
                runs = [(i, j - 1)]
            elif length == best_len:
                runs.append((i, j - 1))

        i = j

    if best_len == 0:
        return ":".join(groups)

    answer = None

    for l, r in runs:
        candidate = make_candidate(groups, l, r)
        if answer is None or candidate < answer:
            answer = candidate

    return answer

def solve():
    out = []

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        x = int(line)
        out.append(abbreviate(x))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The conversion `f"{x:032x}"` is the key representation step. The width of 32 is not cosmetic: an integer such as `1` must become `00000000000000000000000000000001`, otherwise the eight 16-bit boundaries would be lost.

Each four-character chunk is converted to its normalized hexadecimal form with `lstrip("0")`. The fallback to `"0"` is necessary because stripping all zeroes from `"0000"` produces an empty string.

The zero-run scan uses `i` as the first unprocessed group and advances `j` until the current run ends. Setting `i = j` skips the entire run, so each of the eight groups is inspected only a constant number of times. Runs of length one are deliberately ignored.

The candidate builder uses two empty strings rather than trying to concatenate prefixes and suffixes with special cases. For example, `["1", "", "", "2"]` joined with `:` becomes `1::2`, while `["", "", "1"]` becomes `::1` and `["1", "", ""]` becomes `1::`. If all groups are compressed, `["", ""]` becomes `::`.

Python integers have arbitrary precision, so reading the decimal input with `int` handles the entire range from zero through (2^{128}-1) directly. No manual decimal-to-binary conversion or overflow handling is needed.

The candidate comparison is intentionally delegated to Python's normal string ordering. Since all candidates considered at this point have the same optimal zero-run length, no candidate can win because it is shorter in the first optimization criterion. The string comparison is only resolving the final lexicographic tie.

## Worked Examples

### Sample 1

The first sample integer is `42540578239448488099419523072699400193`. Its normalized hexadecimal groups are `2001:470:f003:0:0:0:0:1`.

| i | Group | Current zero run | Best length | Best runs |
| --- | --- | --- | --- | --- |
| 0 | `2001` | none | 0 | none |
| 1 | `470` | none | 0 | none |
| 2 | `f003` | none | 0 | none |
| 3 | `0` | 3..6, length 4 | 4 | 3..6 |
| 7 | `1` | none | 4 | 3..6 |

There is one maximum run, from group 3 through group 6. Replacing those four zero groups with `::` gives `2001:470:f003::1`.

This example demonstrates the main optimization directly. A run of four zero groups leaves only four explicit groups, while compressing any shorter run would leave more sections.

### Sample 2

For input `1`, the fixed-width hexadecimal representation is `00000000000000000000000000000001`.

| i | Group | Current zero run | Best length | Best runs |
| --- | --- | --- | --- | --- |
| 0 | `0` | 0..6, length 7 | 7 | 0..6 |
| 7 | `1` | none | 7 | 0..6 |

The zero run reaches the beginning of the address and ends immediately before the final `1`. The candidate builder sees an empty left side and produces `::1`.

This trace confirms that leading zero groups must remain part of the address while searching for a compression interval. They are not discarded as numerical leading zeroes of the whole integer.

### Sample 3

For input `0`, all eight normalized groups are zero.

| i | Group | Current zero run | Best length | Best runs |
| --- | --- | --- | --- | --- |
| 0 | `0` | 0..7, length 8 | 8 | 0..7 |

The maximum run covers the entire address, so the candidate consists only of `::`.

This case verifies the boundary where both the prefix and suffix are empty. It is the one case where the complete IPv6 address is represented by a compression marker with nothing on either side.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(8) = O(1) per test case | The address always contains exactly eight 16-bit groups, and the scan and candidate construction examine only those groups. |
| Space | O(8) = O(1) per test case | We store eight normalized groups and at most eight candidate run positions. |

The input integer has at most 128 bits, so even the conversion to hexadecimal is constant-size work. The one-second limit is easily sufficient because every test case performs only a handful of operations on an eight-element representation. Memory usage is also negligible compared with the 256 MB limit specified by the problem.

## Test Cases

```python
import sys
import io

def make_candidate(groups, l, r):
    return ":".join(groups[:l] + ["", ""] + groups[r + 1:])

def abbreviate(x):
    h = f"{x:032x}"
    groups = []

    for i in range(0, 32, 4):
        part = h[i:i + 4]
        part = part.lstrip("0")
        groups.append(part if part else "0")

    best_len = 0
    runs = []

    i = 0
    while i < 8:
        if groups[i] != "0":
            i += 1
            continue

        j = i
        while j < 8 and groups[j] == "0":
            j += 1

        length = j - i

        if length >= 2:
            if length > best_len:
                best_len = length
                runs = [(i, j - 1)]
            elif length == best_len:
                runs.append((i, j - 1))

        i = j

    if best_len == 0:
        return ":".join(groups)

    return min(make_candidate(groups, l, r) for l, r in runs)

def solve():
    out = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            out.append(abbreviate(int(line)))
    return "\n".join(out)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    try:
        return solve() + "\n"
    finally:
        sys.stdin = old_stdin

# Provided samples
assert run("42540578239448488099419523072699400193\n") == \
       "2001:470:f003::1\n", "sample 1"

assert run("1\n") == "::1\n", "sample 2"

assert run("0\n") == "::\n", "sample 3"

# Maximum 128-bit value, containing no zero groups.
assert run("340282366920938463463374607431768211455\n") == \
       "ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff\n", \
       "maximum value"

# A single zero group must not be compressed.
assert run("340282366920938463463374607431768145920\n") == \
       "ffff:ffff:ffff:ffff:ffff:ffff:ffff:0\n", \
       "single zero group"

# Two equally long zero runs. The later one is lexicographically smaller.
tie_value = (
    (1 << 112) +
    (2 << 64) +
    (3 << 16) +
    4
)
assert run(str(tie_value) + "\n") == \
       "1:0:0:2::3:4\n", \
       "lexicographic tie"

# No compressible zero run.
no_run_value = (
    (1 << 112) +
    (2 << 96) +
    (3 << 80) +
    (4 << 64) +
    (5 << 48) +
    (6 << 32) +
    (7 << 16) +
    8
)
assert run(str(no_run_value) + "\n") == \
       "1:2:3:4:5:6:7:8\n", \
       "no zero run"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0` | `::` | The entire address is one zero run. |
| `340282366920938463463374607431768211455` | `ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff` | Maximum 128-bit value and absence of zero groups. |
| `340282366920938463463374607431768145920` | `ffff:ffff:ffff:ffff:ffff:ffff:ffff:0` | A single zero section must not be compressed. |
| `1:0:0:2:0:0:3:4` encoded by `tie_value` | `1:0:0:2::3:4` | Equal maximum runs and the lexicographic tie-break. |
| `1:2:3:4:5:6:7:8` encoded by `no_run_value` | `1:2:3:4:5:6:7:8` | No legal compression interval. |

## Edge Cases

For the all-zero address, the input is `0`. Fixed-width conversion produces eight `0000` groups, which normalize to eight `"0"` strings. The scanner finds one run from positions 0 through 7 with length 8, so it is strictly better than every other possible compression. The candidate has no groups on either side and becomes `::`. The algorithm never produces `:` because the candidate builder inserts two empty fields before joining.

For a single zero section at the end, the input `340282366920938463463374607431768145920` corresponds to `ffff:ffff:ffff:ffff:ffff:ffff:ffff:0`. The scanner sees seven nonzero groups followed by a zero run of length one. Since the run length is below two, it is rejected entirely. The fallback is the normalized address itself, giving `ffff:ffff:ffff:ffff:ffff:ffff:ffff:0`. This is the boundary that catches implementations which compress every zero run without checking its length.

For equal maximum runs, the value used in the tests represents `1:0:0:2:0:0:3:4`. The scanner records a run of length two at positions 1 through 2 and another run of length two at positions 4 through 5. Both satisfy the primary optimization criterion. The generated candidates are `1::2:0:0:3:4` and `1:0:0:2::3:4`. Comparing them reaches the first compressed position after the common prefix `1:`. The first candidate has `:`, while the second has `0`, and `0` is lexicographically smaller, so the second candidate is selected.

For an address with no compressible run, the test value represents `1:2:3:4:5:6:7:8`. Every group is nonzero, so the scanner never records a valid run and `best_len` remains zero. The algorithm skips candidate construction and simply joins the normalized groups, producing `1:2:3:4:5:6:7:8`. This also prevents an accidental `::` from being inserted when there are no zero sections at all.

For the input `1`, the normalized address contains seven zero groups followed by `1`. The scanner records positions 0 through 6 as a run of length seven, which is the unique optimum. The left side of the compression is empty and the right side is `1`, so the constructed string is `::1`. This verifies the leading-run boundary and also confirms why the original integer must first be padded to all 32 hexadecimal digits.
