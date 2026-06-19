---
title: "CF 106189H - IP v6"
description: "The task is about normalizing an IPv6 address representation. The input is a single string consisting of hexadecimal groups separated by colons."
date: "2026-06-20T04:20:44+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106189
codeforces_index: "H"
codeforces_contest_name: "ICPC Central Russia Regional Contest, 2025"
rating: 0
weight: 106189
solve_time_s: 51
verified: true
draft: false
---

[CF 106189H - IP v6](https://codeforces.com/problemset/problem/106189/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 51s  
**Verified:** yes  

## Solution
## Problem Understanding

The task is about normalizing an IPv6 address representation. The input is a single string consisting of hexadecimal groups separated by colons. In a valid expanded IPv6 form there should always be exactly eight groups, each representing a 16-bit value written as up to four hexadecimal digits. However, the input may use a compressed form where one or more consecutive groups are omitted, represented by a double colon or by missing segments caused by adjacent separators.

The goal is to reconstruct the full canonical form. That means we must interpret the separators, restore the missing groups with zeros, and ensure that the final representation has exactly eight components. Each component must be written as a four-character hexadecimal string, padded with leading zeros if necessary.

The input size constraint is not explicitly large in the statement, but this type of problem is always designed for linear parsing. Any solution that repeatedly splits, inserts, or shifts arrays inefficiently would still pass, but unnecessary quadratic behavior is avoidable.

A subtle edge case appears when the address begins or ends with a compression, for example `"::1"` or `"2001::"`. Another corner case is multiple consecutive missing sections, where more than one group is implied to be zero. A naive split-based approach that assumes every empty substring corresponds to exactly one group fails when the compression represents multiple missing segments.

For instance, `"1::1"` should become seven zero groups between the two ones, not just a single zero group.

## Approaches

A direct interpretation approach is to split the string by the colon character and treat each resulting segment as a group. The problem is that IPv6 compression breaks this assumption. When two colons appear consecutively, the split produces an empty string, but that empty string does not represent one zero group, it represents an entire block of missing groups whose size depends on how many segments are already present elsewhere in the address.

The correct reasoning is to treat the address as having a fixed total of eight segments. After splitting, we count how many non-empty groups are present. The difference between eight and this count is the number of zero groups that must be inserted at the position where the empty segment appears.

Once the structure is restored, each segment is normalized independently. Every group must be converted into an integer from hexadecimal and printed with exactly four digits, preserving leading zeros.

The key observation is that compression happens at most once in a valid IPv6 address, so there is at most one region where expansion is needed. That guarantees a single insertion point for zero blocks.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Direct split without handling compression | O(n) | O(n) | Wrong |
| Split + rebuild with zero expansion | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Split the input string by the colon character into raw segments. This preserves empty strings that correspond to compression points. The structure of the split array encodes where missing blocks occur.
2. Count how many segments are non-empty. This tells us how many explicit groups are already provided in the address.
3. Determine how many groups are missing by subtracting the number of explicit groups from eight. This value is the number of zero groups that must be inserted.
4. Construct the final list by scanning the split segments. Whenever an empty segment is encountered, it represents the compression point. Replace that position with the required number of `"0000"` groups.
5. For every non-empty segment, normalize it by left-padding with zeros until it becomes four characters long. This ensures uniform representation of each 16-bit block.
6. After reconstruction, ensure the result contains exactly eight groups. Join them using colons to form the final IPv6 address.

The important structural idea is that the compressed form only removes a single contiguous block of zero groups, so all missing information is localized and can be restored deterministically.

### Why it works

The IPv6 compression rule guarantees that at most one sequence of consecutive zero groups is replaced by a double colon. This means the split representation contains exactly one location where expansion is needed. Since the total number of groups is fixed at eight, the missing length is uniquely determined. Every valid reconstruction must preserve explicit groups in order, and only the compressed region is flexible, so filling it with the computed number of zeros yields a unique canonical form.

## Python Solution

```python
import sys
input = sys.stdin.readline

def normalize(group: str) -> str:
    return group.zfill(4)

s = input().strip()
parts = s.split(':')

# count explicit groups
explicit = sum(1 for x in parts if x != '')

missing = 8 - explicit

res = []
i = 0
n = len(parts)

while i < n:
    if parts[i] == '':
        if missing > 0:
            res.extend(['0000'] * missing)
            missing = 0
        i += 1
    else:
        res.append(normalize(parts[i]))
        i += 1

print(':'.join(res))
```

The solution works by first parsing the structure of separators, then injecting the missing zero blocks exactly once at the compression point. The normalization step ensures each group is four hexadecimal digits. A subtle point is that we must consume the empty segment only once; multiple empty entries can appear depending on how the compression is placed, but only one of them represents the expansion site.

## Worked Examples

Consider the input `"2001:db8::1"`.

We split into `["2001", "db8", "", "1"]`. There are three explicit groups, so five are missing. The empty entry triggers insertion of five `"0000"` groups. The final sequence becomes:

| Step | Action | Result |
| --- | --- | --- |
| 1 | read 2001 | [2001] |
| 2 | read db8 | [2001, 0db8] |
| 3 | empty block expands | [2001, 0db8, 0000, 0000, 0000, 0000, 0000] |
| 4 | read 1 | [2001, 0db8, 0000, 0000, 0000, 0000, 0001] |

The final output is `"2001:0db8:0000:0000:0000:0000:0000:0001"`.

Now consider `"::1"`.

Splitting gives `["", "", "1"]`. There is one explicit group, so seven are missing. The empty region expands into seven zero blocks, and then the final `"1"` is normalized.

| Step | Action | Result |
| --- | --- | --- |
| 1 | empty expands | seven 0000 blocks |
| 2 | read 1 | append 0001 |

The result becomes `"0000:0000:0000:0000:0000:0000:0000:0001"`.

These traces confirm that the empty segment consistently acts as a placeholder for the entire compressed region.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | IPv6 has fixed maximum of 8 segments, so processing is constant bounded |
| Space | O(1) | only a fixed number of groups are stored |

The algorithm easily fits within any reasonable limits since the structure size never grows beyond a constant bound.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    input = _sys.stdin.readline

    s = input().strip()
    parts = s.split(':')

    explicit = sum(1 for x in parts if x != '')
    missing = 8 - explicit

    res = []
    i = 0
    while i < len(parts):
        if parts[i] == '':
            if missing > 0:
                res.extend(['0000'] * missing)
                missing = 0
            i += 1
        else:
            res.append(parts[i].zfill(4))
            i += 1

    return ':'.join(res)

# basic
assert run("1::1\n") == "0001:0000:0000:0000:0000:0000:0000:0001"
# already full
assert run("abcd:0:0:0:0:0:0:1\n") == "abcd:0000:0000:0000:0000:0000:0000:0001"
# leading compression
assert run("::\n") == "0000:0000:0000:0000:0000:0000:0000:0000"
# trailing compression
assert run("2001:db8::\n") == "2001:0db8:0000:0000:0000:0000:0000:0000"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1::1` | expanded middle block | central compression handling |
| full address | padded groups | normalization correctness |
| `::` | all zeros | full compression case |
| trailing `::` | suffix expansion | edge placement handling |

## Edge Cases

One important edge case is when the compression appears at the beginning of the string, producing an initial empty segment after splitting. In this case the algorithm must ensure that the expansion happens before any real group is processed. The construction logic handles this because the first empty segment triggers immediate insertion of the missing zero blocks.

Another case is when the input already contains eight explicit groups without any compression. Here no empty segment exists, so the missing count becomes zero and no expansion occurs. The algorithm simply normalizes each group independently, preserving correctness without modification.
