---
title: "CF 102800A - Chord"
description: "Each test case describes three musical notes that are already ordered from the lowest pitch to the highest pitch."
date: "2026-07-27T17:35:47+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102800
codeforces_index: "A"
codeforces_contest_name: "The 14th Jilin Provincial Collegiate Programming Contest"
rating: 0
weight: 102800
solve_time_s: 60
verified: true
draft: false
---

[CF 102800A - Chord](https://codeforces.com/problemset/problem/102800/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m  
**Verified:** yes  

## Solution
## Problem Understanding

Each test case describes three musical notes that are already ordered from the lowest pitch to the highest pitch. The notes may belong to different octaves, but the input guarantees that the distance from the first note to the second and from the second note to the third is at most 11 semitones. Our task is to determine whether these three notes form a major triad, a minor triad, or neither.

The only information that matters is the number of semitones between consecutive notes. A major triad has intervals of 4 semitones followed by 3 semitones. A minor triad has intervals of 3 semitones followed by 4 semitones. Any other pair of intervals must be reported as `Dissonance`.

The number of test cases is at most 2000, which is very small. Every test case contains only three notes, so even constant time processing per case is more than sufficient. The solution only needs a mapping from note names to their positions within an octave and a few arithmetic operations.

The first subtle case is when the notes cross an octave boundary. For example,

```
A C E
```

The correct output is

```
Minor triad
```

The note `C` has a smaller index than `A` inside a single octave, but it is actually in the next octave. Simply subtracting octave indices would produce a negative value. The interval computation must add 12 whenever the next note's index is smaller.

Another easy mistake is assuming that every increasing sequence of notes can be classified as a chord. For example,

```
C F A
```

The intervals are 5 and 4 semitones, which matches neither chord definition. The correct output is

```
Dissonance
```

A final edge case is when the input is musically descending in terms of note names but still ascending in pitch because of octaves.

```
E D C
```

The correct output is

```
Dissonance
```

Although `D` and `C` appear earlier in the chromatic scale, they belong to higher octaves. A solution that ignores octave wrapping would compute incorrect negative distances.

## Approaches

A straightforward approach is to simulate the musical definition directly. Convert every note into its position inside an octave, compute the semitone distance between consecutive notes, adjust for octave wrapping whenever necessary, then compare the two distances against the two valid patterns.

One could also imagine generating every possible major and minor triad and checking whether the input matches one of them. Since there are only 12 possible roots and two chord types, this still requires only 24 patterns and is easily fast enough. Although correct, it introduces unnecessary preprocessing and comparisons.

The direct interval computation is simpler because the problem definition is already expressed in terms of consecutive semitone distances. Once each note is mapped to an integer from 0 to 11, every test case reduces to two interval calculations and two comparisons.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(24) per test case | O(24) | Accepted, but unnecessary |
| Optimal | O(1) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Create a mapping from each note name to its position in the chromatic scale.
2. Read the three notes and convert them into their numeric positions.
3. Compute the interval from the first note to the second. If the second position is smaller, add 12 before subtracting so the interval represents moving upward into the next octave.
4. Compute the second interval in exactly the same way.
5. If the two intervals are `(4, 3)`, print `Major triad`.
6. Otherwise, if the intervals are `(3, 4)`, print `Minor triad`.
7. Otherwise, print `Dissonance`.

### Why it works

The input guarantees that the notes are already ordered from lower pitch to higher pitch. The only complication is that moving upward may cross an octave boundary. Adding 12 whenever the numeric note value decreases reconstructs the actual upward semitone distance. After those two distances are computed, the chord type is determined entirely by the problem definition. Since every possible input produces exactly one pair of consecutive intervals, the algorithm always classifies the chord correctly.

## Python Solution

```python
import sys
input = sys.stdin.readline

pos = {
    "C": 0,
    "C#": 1,
    "D": 2,
    "D#": 3,
    "E": 4,
    "F": 5,
    "F#": 6,
    "G": 7,
    "G#": 8,
    "A": 9,
    "A#": 10,
    "B": 11,
}

def interval(a, b):
    if b < a:
        b += 12
    return b - a

t = int(input())

for _ in range(t):
    n1, n2, n3 = input().split()

    x = pos[n1]
    y = pos[n2]
    z = pos[n3]

    d1 = interval(x, y)
    d2 = interval(y, z)

    if d1 == 4 and d2 == 3:
        print("Major triad")
    elif d1 == 3 and d2 == 4:
        print("Minor triad")
    else:
        print("Dissonance")
```

The dictionary stores the chromatic scale as integers from 0 through 11. This makes interval calculations simple integer subtraction instead of string processing.

The helper function handles the only tricky part of the implementation. When the second note has a smaller numeric value, it belongs to the next octave, so adding 12 reconstructs the correct upward distance. Because the statement guarantees each interval is at most 11 semitones, this adjustment is always sufficient.

Each test case computes two intervals and compares them against the only two valid patterns. There are no off by one issues because the chromatic scale is represented with consecutive integers and every interval is measured directly as the difference between positions after octave adjustment.

## Worked Examples

### Example 1

Input:

```
C E G
```

| Note | Numeric Value |
| --- | --- |
| C | 0 |
| E | 4 |
| G | 7 |

| d1 | d2 | Result |
| --- | --- | --- |
| 4 | 3 | Major triad |

The intervals match the major triad definition exactly, so the algorithm prints `Major triad`.

### Example 2

Input:

```
A C E
```

| Note | Numeric Value |
| --- | --- |
| A | 9 |
| C | 0 |
| E | 4 |

| d1 | d2 | Result |
| --- | --- | --- |
| (12 + 0) - 9 = 3 | 4 | Minor triad |

This example demonstrates why octave adjustment is necessary. Without adding 12, the first interval would incorrectly become `-9`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(T) | Each test case performs constant work. |
| Space | O(1) | Only the fixed note mapping and a few variables are stored. |

Even with the maximum of 2000 test cases, the total work is tiny. The solution easily satisfies the given limits.

## Test Cases

```python
import sys
import io

def solve():
    import sys
    input = sys.stdin.readline

    pos = {
        "C": 0,
        "C#": 1,
        "D": 2,
        "D#": 3,
        "E": 4,
        "F": 5,
        "F#": 6,
        "G": 7,
        "G#": 8,
        "A": 9,
        "A#": 10,
        "B": 11,
    }

    def interval(a, b):
        if b < a:
            b += 12
        return b - a

    t = int(input())
    out = []

    for _ in range(t):
        a, b, c = input().split()
        d1 = interval(pos[a], pos[b])
        d2 = interval(pos[b], pos[c])

        if d1 == 4 and d2 == 3:
            out.append("Major triad")
        elif d1 == 3 and d2 == 4:
            out.append("Minor triad")
        else:
            out.append("Dissonance")

    print("\n".join(out))

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    ans = sys.stdout.getvalue()
    sys.stdin = backup_stdin
    sys.stdout = backup_stdout
    return ans

assert run(
"""5
C E G
A C E
B D F#
C F A
E D C
"""
) == (
"""Major triad
Minor triad
Minor triad
Dissonance
Dissonance
"""
)

assert run(
"""1
C E G
"""
) == (
"""Major triad
"""
)

assert run(
"""1
A C E
"""
) == (
"""Minor triad
"""
)

assert run(
"""1
C F A
"""
) == (
"""Dissonance
"""
)

assert run(
"""1
B D# F#
"""
) == (
"""Major triad
"""
)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `C E G` | `Major triad` | Standard major chord. |
| `A C E` | `Minor triad` | Correct handling of octave wrapping. |
| `C F A` | `Dissonance` | Invalid interval pattern. |
| `B D# F#` | `Major triad` | Major chord crossing an octave boundary. |

## Edge Cases

Consider the input

```
1
A C E
```

The mapped values are `9`, `0`, and `4`. The algorithm detects that `0 < 9`, adds 12, and computes the first interval as `3`. The second interval is `4`. Since the interval pair is `(3, 4)`, the output is

```
Minor triad
```

This correctly handles octave wrapping.

Now consider

```
1
C F A
```

The mapped values are `0`, `5`, and `9`. The intervals become `(5, 4)`. Neither valid chord pattern matches, so the algorithm prints

```
Dissonance
```

This confirms that only the two exact interval sequences are accepted.

Finally, consider

```
1
E D C
```

The mapped values are `4`, `2`, and `0`. The algorithm computes the intervals as `(10, 10)` after octave adjustment. Neither pair matches `(4, 3)` or `(3, 4)`, so the output is

```
Dissonance
```

This demonstrates that descending note names do not confuse the interval calculation because octave wrapping is handled explicitly.
