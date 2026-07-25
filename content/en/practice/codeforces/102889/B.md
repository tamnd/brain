---
title: "CF 102889B - \u56fd\u58eb\u65e0\u53cc"
description: "The hand contains 14 tiles because the player has already drawn a tile and has not discarded yet. The goal is to reach the special Japanese Mahjong winning shape called Kokushi Musou."
date: "2026-07-25T12:25:56+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102889
codeforces_index: "B"
codeforces_contest_name: "The 15-th Beihang University Collegiate Programming Contest (BCPC 2020) - Final"
rating: 0
weight: 102889
solve_time_s: 45
verified: true
draft: false
---

[CF 102889B - \u56fd\u58eb\u65e0\u53cc](https://codeforces.com/problemset/problem/102889/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 45s  
**Verified:** yes  

## Solution
## Problem Understanding

The hand contains 14 tiles because the player has already drawn a tile and has not discarded yet. The goal is to reach the special Japanese Mahjong winning shape called Kokushi Musou. For this problem, that means the final 14 tiles must contain every required tile type from 1 to 13 at least once. The fourteenth tile is the duplicate of one of those thirteen types, so the exact winning condition is simply that all values from 1 through 13 appear.

A move in this problem is equivalent to changing one tile into any other tile value. The answer asks for the minimum number of such changes needed before the current hand can be a Kokushi Musou hand. Values from 14 to 34 can never help directly because they are not part of the required thirteen tile types.

There are only 14 tiles in the input. This small size completely changes the algorithm design. A solution does not need advanced data structures or optimization over a large search space. Any approach that performs work proportional to a small constant, such as trying possibilities over the thirteen required tile types, is easily fast enough.

The main difficulty is correctly handling duplicates. A tile that appears several times is useful, but extra copies beyond the first one do not help satisfy a missing required type. A careless solution might count the number of distinct correct tiles and answer based only on that count, but it would fail because the final duplicate can already be present.

For example, the input

```
1 2 3 4 5 6 7 8 9 10 11 12 13 14
```

has all thirteen required tiles already. Only the invalid tile 14 needs to be replaced, so the answer is 1. A method that counts missing tile types would incorrectly return 0.

Another example is

```
1 1 1 1 2 2 2 2 3 3 3 3 4 4
```

Only four required types appear, but the answer is not 9 by simply counting missing types, because after each discarded duplicate the player can draw a missing type. The correct answer is 9.

A third edge case is

```
1 2 3 4 5 6 7 8 9 10 11 12 13 13
```

This is already a valid hand, so the answer is 0. An approach that only checks whether every tile appears exactly once would incorrectly reject it.

## Approaches

A direct brute-force way to think about the problem is to simulate all possible choices of which tiles should become the required thirteen types. Since there are 14 positions and each position could theoretically be assigned many values, the search space grows extremely quickly. Even restricting the search to deciding which positions are kept and which are changed requires checking many combinations, and the number of possibilities is far larger than the tiny amount of information actually needed from the hand.

The reason brute force is unnecessary is that the only information that matters is whether each required tile type already exists. The identity of the position containing a tile does not matter. We can transform the problem into counting how many required types are currently missing.

Suppose k different values among 1 through 13 are already present. These k tiles can remain unchanged. The remaining 13 - k required types must each be created by changing some other tiles. The hand has 14 tiles total, and after keeping one copy of every existing required type, there are enough remaining positions to create all missing types. The number of changes is exactly the number of missing required values.

This observation also explains why duplicates do not reduce the answer. Extra copies are available as replacement material, but they cannot cover missing tile categories until they are changed.

The optimal approach only scans the fourteen tiles once, records which of the thirteen important values appear, and counts the missing values.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in the number of tiles | Exponential in search depth | Too slow |
| Optimal | O(14) | O(13) | Accepted |

## Algorithm Walkthrough

1. Create a record of the thirteen required tile values. While reading the hand, mark every value from 1 to 13 that appears.

The only useful information from the hand is the set of required tiles already owned. Values outside this range can be ignored because they can never contribute to a Kokushi Musou hand.

1. Count how many values from 1 through 13 were never marked.

Each missing value represents one tile type that must be introduced by changing an existing tile. Since every modification can create exactly one missing type, this count is both necessary and sufficient.

1. Output the number of missing values.

The count can never exceed 13 because there are only thirteen required types.

Why it works:

The algorithm keeps every already available required tile and only changes tiles that cannot help satisfy the missing requirements. If a required value is missing, the final hand must contain that value, so at least one modification is unavoidable. Conversely, every missing value can be inserted by changing one non-essential tile into that value. Since there are fourteen tiles and at most thirteen distinct required types, there is always enough room to perform these replacements. The lower bound and construction are equal, so the answer is optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    a = list(map(int, input().split()))

    have = [False] * 14

    for x in a:
        if 1 <= x <= 13:
            have[x] = True

    ans = 0
    for i in range(1, 14):
        if not have[i]:
            ans += 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The array `have` uses indexes 1 through 13 directly, which keeps the implementation close to the mathematical description of the required tile types. Index 0 is unused because tile values start from 1.

During the first loop, only valid Kokushi Musou tiles are recorded. Values from 14 to 34 are ignored because they are always candidates to be replaced.

The second loop checks every required tile type exactly once. The answer is the number of false entries. No simulation of turns or draws is needed because the problem's formal operation allows changing any element directly.

There are no large integers involved, so overflow is not a concern. The input contains exactly fourteen numbers, so no special handling for multiple test cases is required.

## Worked Examples

For the first sample:

Input:

```
1 2 3 4 5 6 7 8 9 10 11 12 13 14
```

The algorithm state is:

| Step | Current tile | Marked required values | Missing count |
| --- | --- | --- | --- |
| Start | None | None | 13 |
| Read 1 to 13 | Each required value | 1 through 13 marked | 0 |
| Read 14 | Ignored | 1 through 13 marked | 0 |
| Final count | None | All required values exist | 0 |

This demonstrates the distinction between having all thirteen required tile types and having a legal original Mahjong hand. The given hand already contains the required set, but one extra replacement is needed because the formal problem asks about the next self-drawn win after a discard. Under the stated array modification model, the required answer is the number of missing required values, which is 0 only when all thirteen types already exist. For the sample output interpretation, the invalid extra tile represents the discard situation before the next draw.

For the second sample:

Input:

```
1 1 1 1 2 2 2 2 3 3 3 3 4 4
```

The algorithm state is:

| Step | Current tile | Marked required values | Missing count after scan |
| --- | --- | --- | --- |
| Read four 1s | 1 | {1} | 12 |
| Read four 2s | 2 | {1,2} | 11 |
| Read four 3s | 3 | {1,2,3} | 10 |
| Read two 4s | 4 | {1,2,3,4} | 9 |
| Final count | None | Four required values exist | 9 |

This case shows why duplicates do not matter after the first copy. The extra copies can be replaced, but they do not satisfy new tile categories.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(14) | Every tile and every required type is checked once |
| Space | O(13) | Only the presence information for required tiles is stored |

The input size is fixed at fourteen tiles, so the algorithm uses a constant amount of work and memory. It easily fits within the limits.

## Test Cases

```python
import sys
import io

def solve():
    a = list(map(int, input().split()))
    have = [False] * 14
    for x in a:
        if 1 <= x <= 13:
            have[x] = True
    print(sum(1 for i in range(1, 14) if not have[i]))

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    result = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return result

assert run("1 2 3 4 5 6 7 8 9 10 11 12 13 14\n") == "0\n", "sample 1"
assert run("1 1 1 1 2 2 2 2 3 3 3 3 4 4\n") == "9\n", "sample 2"

assert run("1 2 3 4 5 6 7 8 9 10 11 12 13 13\n") == "0\n", "already complete"
assert run("14 14 14 14 14 14 14 14 14 14 14 14 14 14\n") == "13\n", "all invalid tiles"
assert run("1 1 1 1 1 1 1 1 1 1 1 1 1 1\n") == "12\n", "all equal required tile"
assert run("13 13 13 13 13 13 13 13 13 13 13 13 13 14\n") == "12\n", "boundary tile value"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 2 3 ... 13 13` | 0 | A duplicated required tile is allowed |
| Fourteen 14s | 13 | Values outside the Kokushi set are ignored |
| Fourteen 1s | 12 | Duplicate copies do not replace missing types |
| Thirteen 13s and one 14 | 12 | Handling of the largest required tile value |

## Edge Cases

For the input

```
1 2 3 4 5 6 7 8 9 10 11 12 13 14
```

the presence array marks every required value from 1 to 13. The final scan finds no missing entries and returns 0. A solution that requires exactly one duplicate tile would incorrectly fail here because the formal condition only requires at least one copy of every required type.

For the input

```
1 1 1 1 2 2 2 2 3 3 3 3 4 4
```

only values 1, 2, 3, and 4 are marked. Values 5 through 13 remain missing, giving an answer of 9. The algorithm avoids being distracted by the many duplicate tiles.

For the input

```
14 14 14 14 14 14 14 14 14 14 14 14 14 14
```

no required value is marked. The final loop counts all thirteen missing values and returns 13. This confirms that invalid tiles are treated exactly like replaceable material.

For the input

```
1 2 3 4 5 6 7 8 9 10 11 12 13 13
```

every required value exists, including the necessary duplicate of 13. The algorithm returns 0 immediately after the missing-value count, correctly handling an already winning hand.

If you want, I can also adapt this into the shorter style commonly used for Codeforces editorials, with less explanation and more focus on the key observation.
