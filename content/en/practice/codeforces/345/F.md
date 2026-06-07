---
title: "CF 345F - Superstitions Inspection"
description: "The input is not given in the usual structured format with counts. Instead, it is a small text file that alternates between country names and lists of superstitions. A line that does not start with is a country name."
date: "2026-06-07T15:47:38+07:00"
tags: ["codeforces", "competitive-programming", "*special"]
categories: ["algorithms"]
codeforces_contest: 345
codeforces_index: "F"
codeforces_contest_name: "Friday the 13th, Programmers Day"
rating: 2700
weight: 345
solve_time_s: 114
verified: false
draft: false
---

[CF 345F - Superstitions Inspection](https://codeforces.com/problemset/problem/345/F)

**Rating:** 2700  
**Tags:** *special  
**Solve time:** 1m 54s  
**Verified:** no  

## Solution
## Problem Understanding

The input is not given in the usual structured format with counts. Instead, it is a small text file that alternates between country names and lists of superstitions.

A line that does **not** start with `* ` is a country name. A line that starts with `* ` is a superstition belonging to the most recently seen country.

Country names are guaranteed to be unique. A country may have zero superstitions. The task is to find which superstitions appear in the largest number of countries.

The tricky part is that names are compared in a normalized form. Letter case must be ignored, and multiple spaces between words do not matter. Two names represent the same sequence if, after splitting into words, the word sequences are identical ignoring case.

For example:

```
Friday the   13th
friday   THE 13TH
```

represent the same superstition and must be treated as one object.

The output must contain every superstition whose country count is maximal. The names must be printed in lowercase and sorted lexicographically as sequences of words.

The input contains at most 50 lines, and each line contains at most 50 characters. Even an inefficient solution would process only a few thousand characters. The challenge is not performance but correctly parsing and normalizing the data.

Several edge cases can silently break a careless implementation.

Consider inconsistent spacing:

```
A
* black   cat
B
* black cat
```

Correct output:

```
black cat
```

A solution that compares raw strings would incorrectly treat these as different superstitions.

Consider varying capitalization:

```
A
* Friday The 13th
B
* friday the 13th
```

Correct output:

```
friday the 13th
```

A case-sensitive comparison would count two separate superstitions.

Consider countries with no superstitions:

```
A
B
* lucky coin
```

Correct output:

```
lucky coin
```

The parser must recognize that `B` starts a new country even though `A` had no superstition entries.

Consider lexicographic ordering of word sequences:

```
A
* zebra
B
* apple
```

Both occur once, so both must be output:

```
apple
zebra
```

The ordering is applied after normalization.

## Approaches

A brute-force approach would first parse all countries and store, for each country, the set of its superstitions. Then for every distinct superstition, scan every country and test whether the superstition appears there. If there are `S` distinct superstitions and `C` countries, this requires `O(SC)` membership checks after parsing.

With the actual constraints this would already fit easily, because the entire input contains at most 50 lines. Still, it performs work that is not necessary.

The key observation is that the quantity we need is simply the number of countries containing each superstition. Once a superstition line is read and normalized, we already know which country it belongs to. We can increment a global counter for that superstition immediately.

The problem statement guarantees that entries inside a country are unique, so each superstition contributes at most one count per country. After processing the whole file, every superstition has its exact country frequency.

The remaining work is straightforward. Find the maximum frequency, collect every superstition having that frequency, sort them lexicographically, and print them.

Although both approaches are easily fast enough here, the counting approach is simpler and directly matches the quantity we are asked to compute.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(SC) | O(S + total entries) | Accepted |
| Optimal | O(total lines · line length) | O(S) | Accepted |

## Algorithm Walkthrough

1. Read all input lines.
2. Maintain a dictionary `cnt` mapping a normalized superstition name to the number of countries containing it.
3. Process each line in order.
4. If the line starts with `* `, it represents a superstition.

Normalize it by removing the leading `* `, splitting into words, converting every word to lowercase, and joining the words with a single space.
5. Increment `cnt[normalized_name]`.

This is correct because every superstition entry belongs to exactly one country, and entries inside a country are guaranteed to be unique.
6. If the line does not start with `* `, it is a country name. No counting action is needed.
7. After all lines are processed, compute the maximum value stored in `cnt`.
8. Collect every superstition whose count equals this maximum.
9. Sort the collected names lexicographically.
10. Print them one per line.

### Why it works

After normalization, every textual representation of the same superstition becomes exactly the same string. Each superstition entry contributes one occurrence to exactly one country, and duplicate entries inside a country are forbidden by the statement. Consequently, the value stored in `cnt[x]` after processing the entire file is precisely the number of countries containing superstition `x`.

The algorithm outputs exactly those superstitions whose counts equal the global maximum, which is the definition of the required answer. Sorting the normalized strings produces the required lexicographic order.

## Python Solution

```python
import sys
input = sys.stdin.readline

def normalize(s: str) -> str:
    return " ".join(s.lower().split())

def solve():
    lines = [line.rstrip("\n") for line in sys.stdin]

    cnt = {}

    for line in lines:
        if line.startswith("* "):
            superstition = normalize(line[2:])
            cnt[superstition] = cnt.get(superstition, 0) + 1

    best = max(cnt.values())

    ans = sorted(
        name for name, value in cnt.items()
        if value == best
    )

    sys.stdout.write("\n".join(ans))

solve()
```

The `normalize` function is the heart of the solution. Calling `split()` without arguments collapses any number of consecutive spaces into a single separator. Converting to lowercase handles case-insensitive comparison. Joining with a single space creates a canonical representation.

Country names are ignored after parsing because only superstition frequencies matter. The statement guarantees that country names are distinct and that superstition entries inside a country are unique, so no extra bookkeeping is necessary.

A common mistake is to call `lower()` but leave the original spacing unchanged. Then `"black cat"` and `"black   cat"` would still be treated as different strings. Using `split()` followed by `" ".join(...)` avoids this problem.

Another easy mistake is to sort before normalization. The output must contain lowercase canonical forms, so normalization must happen first and the normalized strings must be stored in the dictionary.

## Worked Examples

### Sample 1

Input:

```
Ukraine
* Friday the   13th
* black   cat
* knock the   wood
USA
* wishing well
* friday   the   13th
Holland
France
* Wishing Well
```

Processing trace:

| Line | Normalized superstition | Count after update |
| --- | --- | --- |
| * Friday the   13th | friday the 13th | 1 |
| * black   cat | black cat | 1 |
| * knock the   wood | knock the wood | 1 |
| * wishing well | wishing well | 1 |
| * friday   the   13th | friday the 13th | 2 |
| * Wishing Well | wishing well | 2 |

Final counts:

| Superstition | Count |
| --- | --- |
| friday the 13th | 2 |
| wishing well | 2 |
| black cat | 1 |
| knock the wood | 1 |

Maximum frequency is 2.

Output:

```
friday the 13th
wishing well
```

This example demonstrates both normalization rules. Different capitalization and different spacing collapse into the same canonical name.

### Example 2

Input:

```
A
* Lucky Coin
B
* lucky   coin
C
* rabbit foot
```

Processing trace:

| Line | Normalized superstition | Count after update |
| --- | --- | --- |
| * Lucky Coin | lucky coin | 1 |
| * lucky   coin | lucky coin | 2 |
| * rabbit foot | rabbit foot | 1 |

Final counts:

| Superstition | Count |
| --- | --- |
| lucky coin | 2 |
| rabbit foot | 1 |

Output:

```
lucky coin
```

This trace confirms that multiple textual spellings of the same superstition contribute to a single frequency counter.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(T) | Each character of the input is processed a constant number of times |
| Space | O(S) | One dictionary entry per distinct superstition |

Here `T` is the total number of characters in the input and `S` is the number of distinct normalized superstitions. With at most 50 short lines, the running time is negligible compared to the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    lines = inp.splitlines()

    cnt = {}

    for line in lines:
        if line.startswith("* "):
            s = " ".join(line[2:].lower().split())
            cnt[s] = cnt.get(s, 0) + 1

    best = max(cnt.values())
    ans = sorted(k for k, v in cnt.items() if v == best)

    return "\n".join(ans)

# provided sample
assert run(
"""Ukraine
* Friday the   13th
* black   cat
* knock the   wood
USA
* wishing well
* friday   the   13th
Holland
France
* Wishing Well
"""
) == "friday the 13th\nwishing well"

# minimum valid input
assert run(
"""A
* X
"""
) == "x"

# spacing normalization
assert run(
"""A
* black   cat
B
* black cat
"""
) == "black cat"

# case normalization
assert run(
"""A
* Lucky Coin
B
* lucky coin
"""
) == "lucky coin"

# multiple winners requiring sorting
assert run(
"""A
* zebra
B
* apple
"""
) == "apple\nzebra"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| One country, one superstition | `x` | Minimum valid input |
| Different spacing | `black cat` | Space normalization |
| Different capitalization | `lucky coin` | Case-insensitive matching |
| Two distinct winners | `apple`, `zebra` | Lexicographic output order |

## Edge Cases

Consider inconsistent spacing:

```
A
* black   cat
B
* black cat
```

The first entry normalizes to `black cat`. The second entry normalizes to exactly the same string. The dictionary count becomes 2. The algorithm outputs:

```
black cat
```

Consider inconsistent capitalization:

```
A
* Friday The 13th
B
* friday the 13th
```

Both entries normalize to `friday the 13th`. The count becomes 2 and the output is:

```
friday the 13th
```

Consider countries without superstition lists:

```
A
B
* lucky coin
```

The parser treats both `A` and `B` as country names because neither line begins with `* `. Only one superstition entry is processed, producing:

```
lucky coin
```

Consider several superstitions tied for first place:

```
A
* zebra
B
* apple
```

Both frequencies are 1. The algorithm collects both names and sorts them lexicographically, producing:

```
apple
zebra
```

This confirms that ties are handled correctly and that sorting occurs after normalization.
