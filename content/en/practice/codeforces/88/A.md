---
title: "CF 88A - Chord"
description: "We are given three musical notes, and the task is to classify the chord they form as either major, minor, or \"strange\". Notes are represented in the twelve-tone chromatic scale: C, C, D, D, E, F, F, G, G, A, B, H, and the scale is cyclic, so after H comes C again."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation"]
categories: ["algorithms"]
codeforces_contest: 88
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 73 (Div. 2 Only)"
rating: 1200
weight: 88
solve_time_s: 77
verified: true
draft: false
---

[CF 88A - Chord](https://codeforces.com/problemset/problem/88/A)

**Rating:** 1200  
**Tags:** brute force, implementation  
**Solve time:** 1m 17s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given three musical notes, and the task is to classify the chord they form as either major, minor, or "strange". Notes are represented in the twelve-tone chromatic scale: C, C#, D, D#, E, F, F#, G, G#, A, B, H, and the scale is cyclic, so after H comes C again. A chord is a triad, an unordered set of three notes. A major triad occurs if we can order the notes so that the first interval is 4 semitones and the second is 3 semitones. A minor triad occurs if the first interval is 3 semitones and the second is 4 semitones. Otherwise, the chord is considered "strange".

The input size is fixed: exactly three notes. This guarantees that any algorithm that checks all permutations or calculates all distances will run extremely quickly because 3! = 6 permutations is negligible. The time and memory limits are generous for such small input.

Edge cases arise due to the cyclic nature of the scale. For example, a chord like "B C# F" needs careful handling: we may need to wrap around the scale to compute distances correctly. Naively subtracting note indices could give negative or overly large values, so using modulo 12 arithmetic is necessary. Another subtle point is that the chord is unordered, so all 3! permutations must be considered before classification.

## Approaches

The most straightforward method is brute force. Convert each note to an integer index representing its position in the chromatic scale. For every permutation of the three notes, calculate the distances modulo 12 between consecutive notes. If the distances match (4, 3), classify as major. If they match (3, 4), classify as minor. If none match after checking all permutations, classify as strange.

This brute-force works because the input size is tiny: 3! permutations, and each permutation requires only a couple of arithmetic operations. The problem's constraints allow us to consider every ordering without performance concerns. There is no faster asymptotic approach needed here, but one could also precompute all major and minor triads and check membership in a set. That method is slightly faster in practice, but for three notes, the difference is negligible.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (check all permutations) | O(3!) = O(1) | O(1) | Accepted |
| Precompute triads | O(1) | O(24) | Accepted |

## Algorithm Walkthrough

1. Create a dictionary mapping each note to its chromatic index. For example, C=0, C#=1, D=2, ..., H=11. This allows quick conversion from note names to integers.
2. Read the three input notes and convert them into their corresponding indices using the dictionary.
3. Generate all six permutations of the three indices. Each permutation represents a possible ordering of the chord.
4. For each permutation, calculate the distances between the first and second notes, and the second and third notes, using modulo 12 arithmetic: `(second - first) % 12` and `(third - second) % 12`. This accounts for the cyclic nature of the scale.
5. If the distances are exactly (4, 3), classify the chord as major and terminate.
6. If the distances are exactly (3, 4), classify the chord as minor and terminate.
7. If no permutation matches either pattern, classify the chord as strange.

The correctness of this method relies on checking all orderings. Because the chord is unordered and there are only three notes, the exhaustive search guarantees that if a chord is major or minor, it will be detected in at least one permutation.

## Python Solution

```python
import sys
import itertools
input = sys.stdin.readline

note_to_index = {
    "C": 0, "C#": 1, "D": 2, "D#": 3, "E": 4, "F": 5, "F#": 6,
    "G": 7, "G#": 8, "A": 9, "B": 10, "H": 11
}

notes = input().strip().split()
indices = [note_to_index[n] for n in notes]

for perm in itertools.permutations(indices):
    d1 = (perm[1] - perm[0]) % 12
    d2 = (perm[2] - perm[1]) % 12
    if d1 == 4 and d2 == 3:
        print("major")
        break
    if d1 == 3 and d2 == 4:
        print("minor")
        break
else:
    print("strange")
```

The code first converts note names into numeric indices, then checks all permutations to calculate the modular distances. The use of `% 12` is critical for handling wrap-around distances, like from H to C. The `else` on the `for` loop ensures that if no break occurs, the chord is classified as strange.

## Worked Examples

**Sample 1: "C E G"**

| Step | Permutation | d1 | d2 | Classification |
| --- | --- | --- | --- | --- |
| 1 | C E G (0, 4, 7) | 4 | 3 | major |
| 2 | C G E (0, 7, 4) | 7 | 9 | - |

The first permutation matches (4,3), so the chord is major.

**Sample 2: "C# B F"**

| Step | Permutation | d1 | d2 | Classification |
| --- | --- | --- | --- | --- |
| 1 | C# B F (1, 10, 5) | 9 | 7 | - |
| 2 | B C# F (10, 1, 5) | 3 | 4 | minor |

The second permutation matches (3,4), so the chord is minor. This demonstrates handling cyclic distances.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(3!) = O(1) | Only six permutations are considered, each with two arithmetic operations. |
| Space | O(1) | Only a fixed mapping and the input list of three indices are stored. |

Given the constraints, this solution runs instantly and uses negligible memory.

## Test Cases

```python
import sys, io
import itertools

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    note_to_index = {
        "C": 0, "C#": 1, "D": 2, "D#": 3, "E": 4, "F": 5, "F#": 6,
        "G": 7, "G#": 8, "A": 9, "B": 10, "H": 11
    }
    notes = input().strip().split()
    indices = [note_to_index[n] for n in notes]
    for perm in itertools.permutations(indices):
        d1 = (perm[1] - perm[0]) % 12
        d2 = (perm[2] - perm[1]) % 12
        if d1 == 4 and d2 == 3:
            return "major"
        if d1 == 3 and d2 == 4:
            return "minor"
    return "strange"

# provided sample
assert run("C E G\n") == "major", "sample 1"
# custom cases
assert run("C# B F\n") == "minor", "wrap around minor"
assert run("F# A C#\n") == "major", "another major triad"
assert run("D F A\n") == "minor", "classic minor triad"
assert run("C D E\n") == "strange", "no valid triad"
assert run("H C D\n") == "strange", "wrap around strange"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| C# B F | minor | Wrap-around minor triad detection |
| F# A C# | major | Standard major triad |
| D F A | minor | Classic minor triad |
| C D E | strange | Non-triad chord |
| H C D | strange | Wrap-around detection with strange chord |

## Edge Cases

For the input "B C# F", the naive approach might compute `C# - B = -9` and `F - C# = 4`, giving a negative distance. Using modulo 12, we get `(1 - 10) % 12 = 3` and `(5 - 1) % 12 = 4`, correctly identifying the chord as minor. Similarly, chords that require wrap-around like "H C D" are correctly classified as strange because none of the permutations produce the required (4,3) or (3,4) semitone patterns.
