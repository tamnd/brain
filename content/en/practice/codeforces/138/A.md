---
title: "CF 138A - Literature Lesson"
description: "Each poem is divided into quatrains, groups of four lines. Two lines rhyme if the suffix starting from the k-th vowel from the end is identical in both lines. For example, with k = 1, we compare suffixes starting at the last vowel."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 138
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 99 (Div. 1)"
rating: 1600
weight: 138
solve_time_s: 120
verified: true
draft: false
---

[CF 138A - Literature Lesson](https://codeforces.com/problemset/problem/138/A)

**Rating:** 1600  
**Tags:** implementation  
**Solve time:** 2m  
**Verified:** yes  

## Solution
## Problem Understanding

Each poem is divided into quatrains, groups of four lines. Two lines rhyme if the suffix starting from the k-th vowel from the end is identical in both lines. For example, with `k = 1`, we compare suffixes starting at the last vowel. With `k = 2`, we compare suffixes starting at the second-last vowel.

For every quatrain we only care about four possible rhyme structures:

- `aabb`, meaning lines `(1,2)` rhyme and `(3,4)` rhyme
- `abab`, meaning `(1,3)` rhyme and `(2,4)` rhyme
- `abba`, meaning `(1,4)` rhyme and `(2,3)` rhyme
- `aaaa`, meaning all four lines rhyme together

The whole poem has a valid scheme if every quatrain is compatible with the same structure. A quatrain with all four lines rhyming is flexible, because it can represent any scheme.

The input gives `n` quatrains and the value `k`. Then come `4n` lines of text. We must output one of the valid schemes or `"NO"` if no common scheme exists.

The constraints are small enough that we do not need sophisticated string algorithms. There are at most `2500` quatrains, so at most `10000` lines. The total length of all strings is only `10^4`, which means even scanning every character several times is cheap. An `O(total_length)` or `O(total_length + n)` solution is easily fast enough.

The tricky part is not performance, it is handling the rhyme rules correctly.

One common mistake is treating lines with fewer than `k` vowels as matching each other. They never rhyme with anything, including another short line.

For example:

```
1 2
sky
try
day
may
```

The first two lines each contain only one vowel, so they cannot rhyme for `k = 2`. The correct output is:

```
NO
```

Another easy bug is forgetting that `aaaa` quatrains are compatible with every scheme.

Example:

```
2 1
day
may
sun
fun
code
mode
road
toad
```

The first quatrain is `aabb`. The second is `aaaa`. The whole poem is still valid as `aabb`.

A third subtle case appears when multiple schemes fit individually, but no single scheme works globally.

Example:

```
2 1
day
may
sun
fun
red
bed
red
bed
```

The first quatrain is only `aabb`. The second is `abab` and `abba`. There is no common scheme across all quatrains, so the answer is:

```
NO
```

## Approaches

A brute-force solution would directly compare lines character by character whenever we need to test whether two lines rhyme. For each comparison, we scan backward to locate the k-th vowel, extract the suffix, and compare it with another suffix.

This works because the total input size is small. Even if we performed several comparisons per quatrain, the total amount of processed text would still be manageable.

The weakness of the brute-force version is repetition. The same line may participate in several rhyme checks, causing us to repeatedly recompute its rhyme suffix.

The key observation is that a line can be reduced to a single canonical representation: the suffix starting from the k-th vowel from the end. Once we compute this suffix once, rhyme checking becomes simple equality testing.

For example:

```
commit -> ommit   (k = 2)
hermit -> ermit
```

Now rhyming reduces to:

```
suffix1 == suffix2
```

If a line has fewer than `k` vowels, we assign it an invalid marker and it automatically fails every rhyme test.

Each quatrain only has four lines, so there are only three meaningful pairing patterns to test. After determining which schemes a quatrain supports, we intersect those possibilities with the global set of valid schemes.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n × average_line_length × repeated_checks) | O(1) | Accepted |
| Optimal | O(total_length + n) | O(total_length) | Accepted |

## Algorithm Walkthrough

1. Read all input lines.
2. For every line, compute its rhyme suffix.

Scan the string from right to left while counting vowels. Once the k-th vowel is reached, store the substring starting there.

If the scan finishes before finding `k` vowels, mark the line as invalid.
3. Process each quatrain independently.

Let the four processed suffixes be `a, b, c, d`.
4. Determine which rhyme schemes this quatrain supports.

A rhyme between two lines exists only if both suffixes are valid and equal.
5. Check the four-line rhyme first.

If all four suffixes are equal and valid, this quatrain supports `aaaa`.
6. Check the remaining patterns.

`aabb` requires:

```
a == b and c == d
```

`abab` requires:

```
a == c and b == d
```

`abba` requires:

```
a == d and b == c
```
7. Maintain a global set of still-possible poem schemes.

Initially:

```
{aabb, abab, abba}
```

A quatrain supporting `aaaa` does not restrict anything.

Otherwise intersect the global set with the schemes supported by this quatrain.
8. If the global set becomes empty, print `"NO"`.
9. Otherwise print:

- `"aaaa"` if every quatrain was fully rhyming
- any remaining scheme otherwise

### Why it works

Each line is converted into the exact substring that defines rhyming under the problem rules. Two lines rhyme if and only if these processed suffixes are equal and valid.

For every quatrain we explicitly test all legal rhyme structures. A scheme survives globally only if every quatrain is compatible with it. Since the algorithm never removes a genuinely valid scheme and never accepts an invalid one, the remaining set after all intersections is exactly the set of valid poem schemes.

## Python Solution

```python
import sys
input = sys.stdin.readline

VOWELS = set("aeiou")

def get_suffix(s, k):
    cnt = 0

    for i in range(len(s) - 1, -1, -1):
        if s[i] in VOWELS:
            cnt += 1

        if cnt == k:
            return s[i:]

    return None

def solve():
    n, k = map(int, input().split())

    schemes = {"aabb", "abab", "abba"}
    all_aaaa = True

    for _ in range(n):
        lines = [input().strip() for _ in range(4)]
        suf = [get_suffix(x, k) for x in lines]

        possible = set()

        if (
            suf[0] is not None and
            suf[0] == suf[1] == suf[2] == suf[3]
        ):
            possible.add("aaaa")

        if (
            suf[0] is not None and
            suf[0] == suf[1] and
            suf[2] is not None and
            suf[2] == suf[3]
        ):
            possible.add("aabb")

        if (
            suf[0] is not None and
            suf[0] == suf[2] and
            suf[1] is not None and
            suf[1] == suf[3]
        ):
            possible.add("abab")

        if (
            suf[0] is not None and
            suf[0] == suf[3] and
            suf[1] is not None and
            suf[1] == suf[2]
        ):
            possible.add("abba")

        if "aaaa" not in possible:
            all_aaaa = False
            schemes &= possible

    if all_aaaa:
        print("aaaa")
    elif schemes:
        print(sorted(schemes)[0])
    else:
        print("NO")

solve()
```

The helper function `get_suffix` implements the rhyme definition directly. It scans backward until reaching the k-th vowel. Returning `None` for invalid lines is safer than returning an empty string because empty strings might accidentally compare equal.

The quatrain logic mirrors the mathematical definition of each rhyme scheme. Every comparison explicitly checks that the participating suffixes are valid.

The `all_aaaa` flag handles the special rule that if every quatrain fully rhymes, the answer must be `"aaaa"` rather than an arbitrary compatible scheme.

The global intersection step is the core idea. Each quatrain restricts the set of allowed poem schemes. Once a scheme fails for one quatrain, it can never recover later.

## Worked Examples

### Example 1

Input:

```
1 1
day
may
sun
fun
```

Processed suffixes:

| Line | Suffix |
| --- | --- |
| day | ay |
| may | ay |
| sun | un |
| fun | un |

Scheme checks:

| Scheme | Valid |
| --- | --- |
| aaaa | No |
| aabb | Yes |
| abab | No |
| abba | No |

Final answer:

```
aabb
```

This trace shows the simplest non-trivial case. Only one pairing pattern works, so the poem scheme is uniquely determined.

### Example 2

Input:

```
2 1
code
mode
road
toad
red
bed
red
bed
```

First quatrain:

| Line | Suffix |
| --- | --- |
| code | ode |
| mode | ode |
| road | oad |
| toad | oad |

Valid schemes:

| Scheme | Valid |
| --- | --- |
| aaaa | No |
| aabb | Yes |
| abab | No |
| abba | No |

Global set becomes:

```
{aabb}
```

Second quatrain:

| Line | Suffix |
| --- | --- |
| red | ed |
| bed | ed |
| red | ed |
| bed | ed |

Valid schemes:

| Scheme | Valid |
| --- | --- |
| aaaa | Yes |
| aabb | Yes |
| abab | Yes |
| abba | Yes |

The second quatrain imposes no restriction because `aaaa` is valid.

Final answer:

```
aabb
```

This demonstrates why `aaaa` quatrains must be treated specially.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(total_length + n) | Each character is scanned once while extracting suffixes |
| Space | O(total_length) | Stored suffix strings dominate memory usage |

The total input size is only `10^4` characters, so this solution easily fits within the limits. Even Python string slicing is completely safe at this scale.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

VOWELS = set("aeiou")

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def get_suffix(s, k):
        cnt = 0

        for i in range(len(s) - 1, -1, -1):
            if s[i] in VOWELS:
                cnt += 1

            if cnt == k:
                return s[i:]

        return None

    n, k = map(int, input().split())

    schemes = {"aabb", "abab", "abba"}
    all_aaaa = True

    for _ in range(n):
        lines = [input().strip() for _ in range(4)]
        suf = [get_suffix(x, k) for x in lines]

        possible = set()

        if (
            suf[0] is not None and
            suf[0] == suf[1] == suf[2] == suf[3]
        ):
            possible.add("aaaa")

        if (
            suf[0] is not None and
            suf[0] == suf[1] and
            suf[2] is not None and
            suf[2] == suf[3]
        ):
            possible.add("aabb")

        if (
            suf[0] is not None and
            suf[0] == suf[2] and
            suf[1] is not None and
            suf[1] == suf[3]
        ):
            possible.add("abab")

        if (
            suf[0] is not None and
            suf[0] == suf[3] and
            suf[1] is not None and
            suf[1] == suf[2]
        ):
            possible.add("abba")

        if "aaaa" not in possible:
            all_aaaa = False
            schemes &= possible

    if all_aaaa:
        return "aaaa"
    elif schemes:
        return sorted(schemes)[0]
    else:
        return "NO"

# provided sample
assert run(
"""1 1
day
may
sun
fun
"""
) == "aabb"

# minimum-size input with full rhyme
assert run(
"""1 1
cat
hat
mat
bat
"""
) == "aaaa"

# insufficient vowels
assert run(
"""1 2
sky
try
day
may
"""
) == "NO"

# conflicting schemes
assert run(
"""2 1
day
may
sun
fun
red
bed
red
bed
"""
) == "aabb"

# only abab works
assert run(
"""1 1
light
stone
bright
phone
"""
) == "abab"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single quatrain with all rhymes | aaaa | Special handling of universal rhyme |
| Lines with too few vowels | NO | Invalid lines never rhyme |
| Mixed compatible quatrains | aabb | Global intersection logic |
| Cross pairing only | abab | Correct scheme detection |
| Smallest valid input | aaaa | Boundary size handling |

## Edge Cases

Consider the case where lines do not contain enough vowels.

Input:

```
1 2
sky
try
day
may
```

The algorithm computes:

| Line | Suffix |
| --- | --- |
| sky | None |
| try | None |
| day | ay |
| may | ay |

Every scheme requires at least one comparison involving invalid suffixes, so no scheme is added to `possible`. The final answer becomes `"NO"`.

Now consider a fully rhyming quatrain.

Input:

```
1 1
red
bed
fed
led
```

All suffixes become `"ed"`.

The algorithm marks all four schemes as valid, including `aaaa`. Since every quatrain satisfies `aaaa`, the final output is exactly:

```
aaaa
```

This matters because printing `"aabb"` would technically describe the rhyme pattern, but the problem explicitly requires `"aaaa"` when every quatrain fully rhymes.

Finally, consider incompatible quatrains.

Input:

```
2 1
day
may
sun
fun
cat
dog
cat
dog
```

The first quatrain supports only `aabb`.

The second supports only `abab`.

After intersection:

```
{aabb} ∩ {abab} = empty
```

The algorithm immediately detects that no global scheme exists and prints:

```
NO
```
