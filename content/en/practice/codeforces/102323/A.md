---
title: "CF 102323A - Vowel Count"
description: "The task is to examine several names and decide whether each name contains more vowels than consonants. The only vowels are the five lowercase letters a, e, i, o, and u. Every other lowercase letter is a consonant."
date: "2026-08-13T04:07:35+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102323
codeforces_index: "A"
codeforces_contest_name: "UCF Locals 2014"
rating: 0
weight: 102323
solve_time_s: 47
verified: true
draft: false
---

[CF 102323A - Vowel Count](https://codeforces.com/problemset/problem/102323/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

The task is to examine several names and decide whether each name contains more vowels than consonants. The only vowels are the five lowercase letters `a`, `e`, `i`, `o`, and `u`. Every other lowercase letter is a consonant.

For each name, the program must reproduce the name exactly as it was read, then print `1` if its vowel count is strictly larger than its consonant count, and `0` otherwise. The original UCF Local Programming Contest statement specifies that there are `n` names, each name has between 1 and 20 lowercase letters, and the output consists of the original name followed by the corresponding decision.

The maximum name length is only 20, so even a straightforward scan is easily fast enough. A linear scan performs at most 20 character checks per name. With the natural implementation of checking a character against all five possible vowels, that is at most 100 simple comparisons per name. Even if the number of names is large, there is no reason to consider quadratic or exponential algorithms here.

The comparison must be strict. For example, the input

```
1
ab
```

contains one vowel and one consonant, so the correct output is

```
ab
0
```

A careless implementation using `vowels >= consonants` would incorrectly print `1`.

Another edge case is a name containing no vowels. For

```
1
bcdf
```

the vowel count is zero and the consonant count is four, so the output is

```
bcdf
0
```

An implementation that initializes the answer to `1` and only changes it after finding a vowel could get this case wrong.

The opposite extreme also matters. For

```
1
aeiou
```

all five characters are vowels, so the correct output is

```
aeiou
1
```

The program should count every occurrence, not merely determine whether the name contains at least one vowel.

## Approaches

The most direct approach is to inspect every character in every name and determine whether it is one of `a`, `e`, `i`, `o`, or `u`. We maintain a vowel counter and increment it whenever the current character is a vowel. Since the name length is at most 20, the worst case for explicitly comparing every character with all five vowels is `5 * 20 = 100` character comparisons for one name. The total work is therefore `O(5n)`, which simplifies to `O(n)` for a name of length `n`. This approach is already comfortably within the one-second limit and the 256 MB memory limit specified by the contest.

A slightly cleaner version observes that membership in the fixed set of five vowels can be expressed directly with a string such as `"aeiou"`. Then `ch in "aeiou"` answers whether the current character is a vowel, while the scan itself remains linear. The important structure is that every character contributes independently to the answer. There is no interaction between neighboring characters, so there is no reason to build substrings, sort the name, or perform repeated searches.

The brute-force version and the optimal version have the same asymptotic complexity because the alphabet of possible vowels has constant size. The optimization is mainly a reduction in unnecessary constant work and a clearer expression of the underlying operation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(5n) = O(n) | O(1) | Accepted |
| Optimal | O(n) | O(1) | Accepted |

There is no genuinely too-slow brute-force algorithm under the given constraints. Even the five-comparison version performs only 100 vowel comparisons for the longest possible name. Calling it too slow would overstate the constraints. The one-pass membership check is preferable because it directly models the problem and avoids the unnecessary factor of five.

## Algorithm Walkthrough

1. Read the number of names, `t`, because the input contains several independent cases.
2. For each name, initialize `vowels` to zero. The counter represents exactly how many characters processed so far belong to the vowel set.
3. Scan the name from left to right. For every character, test whether it belongs to `"aeiou"`. If it does, increment `vowels`; otherwise leave the counter unchanged because that character is a consonant.
4. After the complete name has been scanned, its consonant count is `len(name) - vowels`. Comparing these two counts determines the required result.
5. Print the original name first, followed by `1` when `vowels > len(name) - vowels`, and `0` otherwise. The strict `>` comparison handles the equal-count case correctly.

### Why it works

After processing any prefix of the name, `vowels` is exactly the number of vowel characters in that prefix. Every character is classified once, so when the scan ends, `vowels` equals the total number of vowels in the entire name. Since every character is either a vowel or a consonant, the remaining `len(name) - vowels` characters are exactly the consonants. The final comparison therefore prints `1` precisely when the number of vowels is greater than the number of consonants.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    for _ in range(t):
        name = input().strip()

        vowels = 0
        for ch in name:
            if ch in "aeiou":
                vowels += 1

        consonants = len(name) - vowels

        print(name)
        print(1 if vowels > consonants else 0)

if __name__ == "__main__":
    solve()
```

The first line gives the number of independent names, so the outer loop processes exactly `t` cases. The call to `strip()` removes the newline produced by `input()` while preserving the actual lowercase letters of the name.

The inner loop implements the scan from Algorithm Walkthrough step 3. The expression `ch in "aeiou"` is sufficient because the statement restricts names to lowercase letters. There is no need to handle uppercase vowels or punctuation.

After counting vowels, subtracting from the name length gives the consonant count without requiring a second scan. The final comparison uses `>` rather than `>=`, which is the boundary condition that distinguishes strictly more vowels from an equal number.

There are no integer overflow concerns in Python, and the algorithm stores only the current name and one integer counter.

## Worked Examples

The first sample contains four names:

```
4
ali
arup
travis
orooji
```

For `ali`, the scan encounters `a` as a vowel, `l` as a consonant, and `i` as a vowel. The resulting counts are two vowels and one consonant.

| Character | Vowels | Consonants |
| --- | --- | --- |
| `a` | 1 | 0 |
| `l` | 1 | 1 |
| `i` | 2 | 1 |

The result is `1`. For `arup`, the vowels are `a` and `u`, while `r` and `p` are consonants, giving an equal split and therefore `0`. For `travis`, there are two vowels and four consonants, giving `0`. For `orooji`, there are four vowels and two consonants, giving `1`.

The complete output is:

```
ali
1
arup
0
travis
0
orooji
1
```

The second sample can be constructed to exercise the equal-count boundary:

```
3
a
bc
aeiou
```

The traces are:

| Name | Vowels | Consonants | Result |
| --- | --- | --- | --- |
| `a` | 1 | 0 | 1 |
| `bc` | 0 | 2 | 0 |
| `aeiou` | 5 | 0 | 1 |

The first case demonstrates the smallest legal name. The second demonstrates a name containing no vowels. The third demonstrates that every occurrence of a vowel is counted.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(L) per name | Every character of a name of length `L` is inspected once, and the vowel set has constant size. |
| Space | O(1) auxiliary | Only the vowel counter and a few scalar variables are needed apart from the input string itself. |

With `L <= 20`, each name requires at most 20 iterations. Even the explicit five-way vowel comparison would require only 100 character comparisons for the largest possible name, so the solution is far below the available one-second time limit. The memory usage is also negligible compared with the 256 MB limit.

## Test Cases

```python
import sys
import io

def solve_text(inp: str) -> str:
    data = io.StringIO(inp)
    t = int(data.readline())
    out = []

    for _ in range(t):
        name = data.readline().strip()

        vowels = 0
        for ch in name:
            if ch in "aeiou":
                vowels += 1

        consonants = len(name) - vowels

        out.append(name)
        out.append("1" if vowels > consonants else "0")

    return "\n".join(out) + "\n"

# Provided sample
assert solve_text(
    """4
ali
arup
travis
orooji
"""
) == """ali
1
arup
0
travis
0
orooji
1
""", "provided sample"

# Minimum-size input
assert solve_text(
    """1
a
"""
) == """a
1
""", "single vowel"

# No vowels
assert solve_text(
    """1
bcdf
"""
) == """bcdf
0
""", "no vowels"

# Equal number of vowels and consonants
assert solve_text(
    """1
ab
"""
) == """ab
0
""", "equal counts"

# Maximum-size name, all vowels
assert solve_text(
    """1
aaaaaaaaaaaaaaaaaaaa
"""
) == """aaaaaaaaaaaaaaaaaaaa
1
""", "maximum length"

# Several cases, including all consonants and mixed vowels
assert solve_text(
    """4
z
ae
baba
aeiouaeiou
"""
) == """z
0
ae
1
baba
1
aeiouaeiou
1
""", "mixed edge cases"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a` | `a` followed by `1` | Minimum-size input and a name with only vowels |
| `bcdf` | `bcdf` followed by `0` | Zero-vowel case |
| `ab` | `ab` followed by `0` | Equal vowel and consonant counts |
| `aaaaaaaaaaaaaaaaaaaa` | The name followed by `1` | Maximum allowed length and all-equal values |
| Multiple mixed names | Corresponding `1` or `0` values | Independent processing of multiple test cases and counting repeated vowels |

## Edge Cases

For the strict comparison boundary, consider the exact input

```
1
ab
```

The algorithm starts with `vowels = 0`. It reads `a`, increments the counter to `1`, then reads `b` and leaves it at `1`. The name has length two, so `consonants = 2 - 1 = 1`. Since `1 > 1` is false, the output is

```
ab
0
```

This catches the common mistake of treating equality as a successful case.

For a name with no vowels, consider

```
1
bcdf
```

Every character fails the membership test, so `vowels` remains zero. The consonant count becomes `4 - 0 = 4`, and the comparison `0 > 4` is false. The output is

```
bcdf
0
```

The counter never needs a special correction for this case.

For a name containing only vowels, consider

```
1
aeiou
```

Each of the five characters belongs to the vowel set, so the counter reaches five. The consonant count is `5 - 5 = 0`, and `5 > 0` is true. The output is

```
aeiou
1
```

The algorithm counts repeated occurrences as separate vowels, which is required. For example, the maximum-length name

```
1
aaaaaaaaaaaaaaaaaaaa
```

contains twenty vowel occurrences. The counter reaches twenty, the consonant count is zero, and the program prints `1`.

Finally, the input may contain several names with completely different characteristics. Each iteration creates a fresh `vowels` counter, so information from one name cannot leak into the next. This is why an input such as

```
3
a
bc
ae
```

produces

```
a
1
bc
0
ae
1
```

The per-name reset is part of the correctness invariant: the counter always describes only the current name.
