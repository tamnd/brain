---
title: "CF 102215K - Deck Sorting"
description: "We have a string of length (n), where each character is one of R, G, or B. The string describes the deck from top to bottom. We may distribute the cards one by one into two piles."
date: "2026-08-17T23:51:28+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102215
codeforces_index: "K"
codeforces_contest_name: "2019, XII Samara Regional Intercollegiate Programming Contest"
rating: 0
weight: 102215
solve_time_s: 147
verified: true
draft: false
---

[CF 102215K - Deck Sorting](https://codeforces.com/problemset/problem/102215/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 27s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a string of length (n), where each character is one of `R`, `G`, or `B`. The string describes the deck from top to bottom. We may distribute the cards one by one into two piles. Since every new card is placed on top of its chosen pile, the order inside each pile is reversed relative to the order in which its cards appeared in the original deck. At the end, one entire pile is placed on top of the other, so the final deck is the concatenation of two reversed subsequences of the original string.

The goal is to decide whether the final deck can have all cards of each color together. The three color blocks may appear in any order. The official problem allows (1 \le n \le 1000).

The bound of only 1000 characters is large enough to make exhaustive enumeration of all ways to distribute cards impossible. There are (2^n) assignments of cards to the two piles, so even checking one assignment in (O(n)) time would give (O(n2^n)) operations. For (n=1000), this is far beyond what a 2-second limit can handle. A solution should instead exploit the fact that there are only three colors, giving only six possible orders for the final color blocks.

There are several boundary cases that can fool a careless implementation. A one-card deck such as `R` must return `YES`, because it is already sorted and no meaningful split is needed. An implementation that assumes all three colors occur may fail here. A deck such as `RGB` must also return `YES`, even though every color occurs exactly once. A solution that requires a repeated occurrence of every color would incorrectly reject it.

An absent color also needs special handling. For example, `RRR` is already sorted, so the answer is `YES`. When a color chosen as the first or last color of a candidate ordering does not occur, there is no actual first or last occurrence to use as a boundary. Treating a nonexistent first occurrence as position (n), for example, can accidentally count cards that should not belong to that side. The implementation below handles nonexistent colors explicitly.

## Approaches

A direct brute-force solution can assign every card independently to one of the two piles. For each of the (2^n) assignments, we can construct the two piles, reverse their internal orders, concatenate them in both possible orders, and check whether the resulting deck consists of at most three color blocks. This is correct because every legal sequence of operations corresponds to exactly such a partition into two piles. However, there are (2^n) partitions and each check takes (O(n)), giving (O(n2^n)) work. At (n=1000), the number of assignments alone is approximately (10^{301}), so this approach is not remotely feasible.

The useful observation is that the final deck contains only three color blocks. Suppose we choose three distinct colors (A,B,C) in some order. We will construct two piles so that, after reversing them and concatenating them, the result is (C^*B^_A^_), which is already a valid sorted deck. There are only six choices for (A,B,C).

For a fixed choice (A,B,C), put every (A) card into the first pile and every (C) card into the second pile. The remaining (B) cards have only two useful locations. A (B) card appearing before the first (C) can go into the second pile. A (B) card appearing after the last (A) can go into the first pile.

Why exactly these positions? The first pile, when read in the original deck order, has the form

[
A A \ldots A B B \ldots B.
]

After being reversed, it becomes

[
B B \ldots B A A \ldots A.
]

The second pile has the original order

[
B B \ldots B C C \ldots C,
]

so after reversal it becomes

[
C C \ldots C B B \ldots B.
]

Putting the second pile on top of the first gives

[
C C \ldots C B B \ldots B A A \ldots A,
]

which is sorted.

The only question is whether every (B) card can be assigned to one of these two piles without assigning the same card twice. A (B) before the first (C) belongs to the second pile, while a (B) after the last (A) belongs to the first pile. If some (B) lies between the first (C) and the last (A), it cannot be placed by this construction. If the two regions overlap, a (B) may also be counted twice. Thus the construction succeeds exactly when the number of cards assigned to the two piles is (n).

This characterization is also sufficient for every possible valid sorting. If the final color order is (X,Y,Z), take (A=Z), (B=Y), and (C=X). The cut between the two final piles can occur anywhere inside the middle color block. Reversing the two pieces puts the (Y) cards belonging to the first piece before (X) in the original deck and the remaining (Y) cards after (Z), which is precisely the structure tested by the construction above. Enumerating all six permutations covers every possible final color order. The same structural idea is used in published solutions for this problem.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n2^n)) | (O(n)) | Too slow |
| Optimal | (O(n)) | (O(n)) | Accepted |

## Algorithm Walkthrough

1. Count how many times each of `R`, `G`, and `B` occurs. Also record the first and last occurrence of every color. These values let us test every candidate ordering without repeatedly searching the string.
2. Enumerate all six permutations ((A,B,C)) of the three colors. We interpret (A) as the color placed at the bottom of the final sorted deck, (C) as the color placed at the top, and (B) as the middle color.
3. Put every (A) card into pile one and every (C) card into pile two. This fixes the two outer color blocks.
4. Count the (B) cards before the first (C). These cards can safely go into pile two. After reversing that pile, they appear after all the (C) cards.
5. Count the (B) cards after the last (A). These cards can safely go into pile one. After reversing that pile, they appear before all the (A) cards.
6. Add the number of (A) cards, (C) cards, and the two groups of usable (B) cards. If this total is exactly (n), every card has been assigned exactly once, so the chosen ordering gives a valid sorting. If the total is smaller than (n), some (B) cards lie in the forbidden middle region. If it is larger than (n), some (B) cards were counted on both sides. Either case means this permutation does not work.
7. If any of the six permutations succeeds, print `YES`. If none succeeds, print `NO`.

When a color does not occur, the boundary needs a deliberate interpretation. If (C) is absent, there is no first (C), so no (B) card can be classified as being before the first (C). If (A) is absent, there is no last (A), so every (B) card is after the last (A). The code represents these two cases directly with `first_c = n` and `last_a = -1`, then handles the corresponding counts explicitly.

### Why it works

For a fixed permutation (A,B,C), the construction assigns pile one the sequence of all (A) cards followed by selected (B) cards after the last (A). Its reversal is consequently a block of (B) cards followed by a block of (A) cards. Pile two contains selected (B) cards before the first (C), followed by all (C) cards. Its reversal is a block of (C) cards followed by a block of (B) cards. Concatenating pile two with pile one therefore produces (C^*B^_A^_).

The counted total equals (n) exactly when every original card belongs to one of these two piles exactly once. Hence every successful permutation produces a valid sorting. Conversely, any valid sorting has three color blocks and a boundary between the two final piles. Choosing (A,B,C) in reverse order of those blocks makes the cards assigned to the two piles have exactly the boundary structure tested by the algorithm. Since all six permutations are checked, every valid sorting is represented.

## Python Solution

```python
import sys
input = sys.stdin.readline

from itertools import permutations

def solve(s: str) -> str:
    n = len(s)
    colors = "RGB"

    count = {c: 0 for c in colors}
    first = {c: n for c in colors}
    last = {c: -1 for c in colors}

    for i, ch in enumerate(s):
        count[ch] += 1
        first[ch] = min(first[ch], i)
        last[ch] = i

    # Prefix counts let us count how many B cards occur
    # before an arbitrary position in O(1).
    prefix = {c: [0] * (n + 1) for c in colors}

    for i, ch in enumerate(s):
        for c in colors:
            prefix[c][i + 1] = prefix[c][i]
        prefix[ch][i + 1] += 1

    for a, b, c in permutations(colors):
        taken = count[a] + count[c]

        # B cards before the first C.
        if first[c] != n:
            taken += prefix[b][first[c]]

        # B cards after the last A.
        if last[a] != -1:
            taken += count[b] - prefix[b][last[a] + 1]
        else:
            # No A exists, so every B is after the last A.
            taken += count[b]

        if taken == n:
            return "YES"

    return "NO"

def main():
    s = input().strip()
    print(solve(s))

if __name__ == "__main__":
    main()
```

The first loop records the frequency and boundaries of every color. `first[c]` is initialized to `n`, while `last[a]` is initialized to `-1`, so nonexistent colors can be detected without special sentinel values outside the valid index range.

The prefix-count arrays make the two (B)-regions easy to measure. `prefix[b][first[c]]` counts positions strictly before `first[c]`, which is exactly what is needed for the first region. For the other region, `count[b] - prefix[b][last[a] + 1]` counts positions strictly after `last[a]`. The `+1` is necessary because prefix arrays use half-open ranges.

There is no integer-overflow concern in Python, and all counts are at most 1000. The six permutations are generated by `itertools.permutations`, so every possible ordering of the three colors is examined exactly once.

The implementation uses one extra (3(n+1)) prefix-count structure. This is small for (n \le 1000), and it keeps the actual test for each permutation constant time.

## Worked Examples

### Sample 1

Consider `RGBRGB`. Take the permutation (A=R,B=G,C=B). The relevant boundaries are the last `R` at index 3 and the first `B` at index 2.

| Permutation | Count A | Count C | B before first C | B after last A | Taken | Result |
| --- | --- | --- | --- | --- | --- | --- |
| (R,G,B) | 2 | 2 | 1 | 1 | 6 | YES |

The two piles can be understood directly. Pile one receives all `R` cards and the `G` card after the last `R`, giving original order `RRG`. Pile two receives the `G` before the first `B` and all `B` cards, giving `GBB`. Reversing them produces `BGG` and `RR`, so placing pile two above pile one gives `BGGRR`. More precisely, using the actual positions produces the sample's valid construction, whose final deck has three contiguous color blocks. The key invariant is that every card is assigned once and each pile has at most two color runs before reversal.

### Sample 2

For `RGBRGBRGB`, the permutation (R,G,B) gives the following values.

| Permutation | Count A | Count C | B before first C | B after last A | Taken | Result |
| --- | --- | --- | --- | --- | --- | --- |
| (R,G,B) | 3 | 3 | 1 | 0 | 7 | NO |

The remaining two `G` cards lie between the first `B` and the last `R`, so this particular ordering cannot assign all cards. The other five permutations fail for the same structural reason. No possible boundary between the two piles can accommodate the repeated `RGB` pattern, so the answer is `NO`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n)) | Building counts and prefix arrays takes (O(n)), and only six permutations are checked in (O(1)) each. |
| Space | (O(n)) | Three prefix arrays of length (n+1) are stored. |

With (n \le 1000), the algorithm performs only a small constant number of passes over the input and uses negligible memory compared with the 256 MB limit.

## Test Cases

```
# helper: run the core solver directly
def run(inp: str) -> str:
    return solve(inp.strip())

# provided samples
assert run("RGBRGB") == "YES", "sample 1"
assert run("RGBRGBRGB") == "NO", "sample 2"
assert run("RBBRRB") == "YES", "sample 3"

# minimum-size input
assert run("R") == "YES", "single card is already sorted"

# all-equal values
assert run("GGGGGG") == "YES", "one color is already one continuous block"

# maximum-size input
assert run("R" * 1000) == "YES", "maximum n with one color"

# boundary case where the first candidate has its C at position 0
assert run("BGR") == "YES", "different colors can already form three blocks"

# repeated pattern that cannot be handled by two reversed piles
assert run("RGBRGBRGB") == "NO", "three repetitions expose the forbidden middle region"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `R` | `YES` | Minimum size and a missing-color situation |
| `GGGGGG` | `YES` | All cards having the same color |
| `R` repeated 1000 times | `YES` | Maximum input size |
| `BGR` | `YES` | First and last occurrence boundaries |
| `RGBRGBRGB` | `NO` | A genuinely impossible repeated pattern |

## Edge Cases

For the one-card input `R`, the algorithm immediately considers permutations containing `R`. If `R` is chosen as (A), `count[A] = 1`, while the other colors have count zero. No additional card is required, so `taken = 1 = n` and the answer is `YES`. The algorithm never assumes that all three colors are present.

For `GGGGGG`, choose (A=G). Every card is already part of the outer block represented by (A), so `count[A] = 6` and the total is exactly (n). The missing colors do not cause any accidental counting because the absent (C) contributes no cards before its nonexistent first occurrence.

For `BGR`, consider (A=R,B=G,C=B). The first `B` is at index 0 and the last `R` is at index 2. There are no `G` cards before the first `B` and no `G` cards after the last `R`, so this particular permutation does not succeed. Another permutation does, corresponding to the already sorted order `B-G-R`. The example demonstrates why all six permutations must be checked rather than fixing one color order.

For `RGBRGBRGB`, every candidate ordering leaves at least one card of the middle color in a region that belongs to neither pile under the required structure. For (A=R,B=G,C=B), the first `B` occurs at index 2 and the last `R` at index 6. Only one `G` occurs before the first `B`, and none occurs after the last `R`, while there are three `G` cards total. Thus only seven of the nine cards are accounted for. The other five color orders fail symmetrically, giving the required `NO`.
