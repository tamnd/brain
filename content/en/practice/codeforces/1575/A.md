---
title: "CF 1575A - Another Sorting Problem"
description: "We have a collection of distinct book titles, all with the same length. The books are not sorted using ordinary lexicographic order. When comparing two titles, we scan from left to right until we find the first position where they differ."
date: "2026-06-10T11:01:24+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "sortings", "strings"]
categories: ["algorithms"]
codeforces_contest: 1575
codeforces_index: "A"
codeforces_contest_name: "COMPFEST 13 - Finals Online Mirror (Unrated, ICPC Rules, Teams Preferred)"
rating: 1100
weight: 1575
solve_time_s: 767
verified: false
draft: false
---

[CF 1575A - Another Sorting Problem](https://codeforces.com/problemset/problem/1575/A)

**Rating:** 1100  
**Tags:** data structures, sortings, strings  
**Solve time:** 12m 47s  
**Verified:** no  

## Solution
## Problem Understanding

We have a collection of distinct book titles, all with the same length. The books are not sorted using ordinary lexicographic order.

When comparing two titles, we scan from left to right until we find the first position where they differ. If that position is odd-numbered, the smaller letter should come first. If that position is even-numbered, the larger letter should come first.

The task is to output the original indices of the books after sorting them according to this custom order.

The constraint $n \cdot m \le 10^6$ is the key observation. The total amount of string data is at most one million characters. Any solution that repeatedly compares strings character-by-character during a custom comparator could become expensive. A solution that transforms each string once and then uses the language's built-in sorting will comfortably fit within the limit. Complexities around $O(nm)$ preprocessing plus $O(n \log n)$ sorting are completely acceptable.

A common mistake is to compare even positions incorrectly. The statement uses 1-based positions. Position 2, 4, 6, ... are descending. In Python strings are 0-based, so indices 1, 3, 5, ... correspond to even positions.

Consider:

```
2 2
AA
AB
```

At position 2, we compare descendingly. Since $B > A$, the string `AB` should come before `AA`. Treating position 2 as ascending produces the wrong order.

Another subtle case occurs when the first difference appears at an even position:

```
2 3
ABC
AAC
```

The first difference is at position 2. Since position 2 is descending, `ABC` comes before `AAC`, even though ordinary lexicographic order would place `AAC` first.

## Approaches

The brute-force approach is to implement the comparison rule directly and sort using that comparator. Each comparison may scan up to $m$ characters. Sorting requires $O(n \log n)$ comparisons, giving $O(nm \log n)$ time. With one million total characters this can still be heavier than necessary, especially in languages where custom comparators are expensive.

The structure of the ordering suggests a cleaner idea. At odd positions we want the usual alphabet order. At even positions we want the reverse alphabet order.

Suppose we transform every even-position character. Replace

$$A \leftrightarrow Z,\quad
B \leftrightarrow Y,\quad
C \leftrightarrow X,\ldots$$

After this transformation, a larger original character at an even position becomes a smaller transformed character. The descending comparison at even positions is converted into an ordinary ascending comparison.

Once every string is transformed this way, the custom order becomes exactly standard lexicographic order on the transformed strings. Then we can sort normally.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force comparator | $O(nm \log n)$ | $O(1)$ extra | Accepted but unnecessary |
| Transform + normal sort | $O(nm + n\log n)$ | $O(nm)$ | Accepted |

## Algorithm Walkthrough

1. Read all strings and remember their original indices.
2. For each string, build a transformed version.
3. Keep characters at odd positions unchanged.
4. For characters at even positions, replace them with their alphabet mirror:

$$c \mapsto \text{'Z'} - (c-\text{'A'})$$

This converts descending comparisons into ascending ones.
5. Store the pair `(transformed_string, original_index)`.
6. Sort all pairs by the transformed string.
7. Output the original indices in the sorted order.

### Why it works

Take two strings $a$ and $b$. Let $k$ be the first position where they differ.

If $k$ is odd, the transformation leaves both characters unchanged. Their order in ordinary lexicographic comparison is exactly the order required by the problem.

If $k$ is even, the transformation replaces each character by its mirror in the alphabet. A larger original character becomes a smaller transformed character. Thus the descending comparison required by the problem becomes an ascending comparison after transformation.

The first differing position remains the same, so the transformed strings compare in ordinary lexicographic order exactly when the original strings compare in asc-desc-ending order. Therefore sorting transformed strings produces precisely the required ordering.

## Python Solution

```python
import sys
input = sys.stdin.readline

def transform(s):
    chars = list(s)
    for i in range(1, len(chars), 2):  # 0-based indices => even positions in statement
        chars[i] = chr(ord('Z') - (ord(chars[i]) - ord('A')))
    return ''.join(chars)

def solve():
    n, m = map(int, input().split())

    arr = []
    for idx in range(1, n + 1):
        s = input().strip()
        arr.append((transform(s), idx))

    arr.sort()

    print(*[idx for _, idx in arr])

if __name__ == "__main__":
    solve()
```

The preprocessing phase creates the transformed representation of every title. The loop starts at index `1` because Python uses 0-based indexing and the problem's even positions correspond to indices `1, 3, 5, ...`.

The transformation uses the alphabet mirror. For example, `A` becomes `Z`, `B` becomes `Y`, and `Z` becomes `A`.

After transformation, no custom comparator is needed. Python's native string ordering already matches the desired order. The final output uses the stored original indices.

## Worked Examples

### Example 1

Input:

```
5 2
AA
AB
BB
BA
AZ
```

Transformation:

| Original | Transformed | Index |
| --- | --- | --- |
| AA | AZ | 1 |
| AB | AY | 2 |
| BB | BY | 3 |
| BA | BZ | 4 |
| AZ | AA | 5 |

Sorting by transformed string:

| Rank | Transformed | Index |
| --- | --- | --- |
| 1 | AA | 5 |
| 2 | AY | 2 |
| 3 | AZ | 1 |
| 4 | BY | 3 |
| 5 | BZ | 4 |

Output:

```
5 2 1 3 4
```

This demonstrates how descending comparison at position 2 is converted into ordinary ascending sorting.

### Example 2

Input:

```
3 3
ABC
AAC
BAC
```

Transformation:

| Original | Transformed |
| --- | --- |
| ABC | AYC |
| AAC | AZC |
| BAC | BZC |

Sorted transformed strings:

| Transformed | Original Index |
| --- | --- |
| AYC | 1 |
| AZC | 2 |
| BZC | 3 |

Output:

```
1 2 3
```

The first two strings differ at position 2. Since position 2 is descending, `B` should come before `A`, which is exactly what the transformed order achieves.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(nm + n\log n)$ | Transform all characters once, then sort $n$ keys |
| Space | $O(nm)$ | Store transformed strings |

The total input size is at most $10^6$ characters. Processing every character once is inexpensive. Sorting $n$ transformed keys easily fits within the time limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve_io(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    n, m = map(int, input().split())

    arr = []
    for idx in range(1, n + 1):
        s = input().strip()

        chars = list(s)
        for i in range(1, len(chars), 2):
            chars[i] = chr(ord('Z') - (ord(chars[i]) - ord('A')))

        arr.append(("".join(chars), idx))

    arr.sort()
    return " ".join(str(idx) for _, idx in arr)

# provided sample
assert solve_io(
"""5 2
AA
AB
BB
BA
AZ
"""
) == "5 2 1 3 4"

# minimum size
assert solve_io(
"""1 1
A
"""
) == "1"

# first difference at even position
assert solve_io(
"""2 2
AA
AB
"""
) == "2 1"

# odd-position comparison dominates
assert solve_io(
"""3 2
BA
AZ
BZ
"""
) == "2 1 3"

# longer strings
assert solve_io(
"""3 3
ABC
AAC
BAC
"""
) == "1 2 3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single string | `1` | Minimum input size |
| `AA`, `AB` | `2 1` | Correct handling of descending even positions |
| `BA`, `AZ`, `BZ` | `2 1 3` | Odd positions still use normal ascending order |
| Three length-3 strings | `1 2 3` | Mixed odd/even position behavior |

## Edge Cases

Consider the input

```
2 2
AA
AB
```

The first difference occurs at position 2. The rule there is descending order, so `AB` must come before `AA`. The transformation maps `AA -> AZ` and `AB -> AY`. Since `AY < AZ`, ordinary sorting returns the correct order.

Consider

```
2 3
ABC
AAC
```

The first difference occurs at position 2. The original comparison is `B` versus `A`, and position 2 is descending. After transformation the strings become `AYC` and `AZC`. The transformed comparison now happens in ordinary ascending order and still places the correct string first.

Consider

```
2 4
AZAZ
AZAY
```

The first difference appears at position 4, another descending position. The transformation changes only positions 2 and 4, preserving the location of the first differing character. The ordering remains correct because every even-position comparison is consistently reversed.
