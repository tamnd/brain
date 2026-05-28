---
title: "CF 137A - Postcards and photos"
description: "We are given a string made of two characters, C and P. Each character represents one object hanging on the wall. C means postcard, P means photo. Polycarpus removes objects from left to right. He cannot skip positions, and at any moment he may carry only one type of object."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 137
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 98 (Div. 2)"
rating: 900
weight: 137
solve_time_s: 88
verified: true
draft: false
---

[CF 137A - Postcards and photos](https://codeforces.com/problemset/problem/137/A)

**Rating:** 900  
**Tags:** implementation  
**Solve time:** 1m 28s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string made of two characters, `C` and `P`. Each character represents one object hanging on the wall. `C` means postcard, `P` means photo.

Polycarpus removes objects from left to right. He cannot skip positions, and at any moment he may carry only one type of object. He also cannot carry more than 5 objects at once.

The task is to compute the minimum number of trips to the closet needed to remove every object.

The important detail is that once the object type changes, he must empty his hands before continuing. For example, in the sequence `CCCPP`, he can carry the three postcards together, but when the first photo appears he must first visit the closet.

The string length is at most 100, which is tiny. Even quadratic solutions would easily pass. Still, the structure of the problem allows a direct linear scan.

A common mistake is to think globally instead of locally. Since Polycarpus walks strictly from left to right and cannot skip items, each maximal contiguous block of equal characters is independent from the others.

Consider this example:

```
CCCCCC
```

The correct answer is `2`, not `6`. He can carry at most 5 items, so the block of 6 postcards requires two trips.

Another easy mistake is forgetting to split by type changes.

```
CPPPP
```

The correct answer is `2`. One trip for the single postcard, one trip for the four photos. Treating the whole string length as one batch would incorrectly give `1`.

There is also an off-by-one pitfall when a block size is exactly divisible by 5.

```
CCCCCCCCCC
```

The correct answer is `2`, not `3`. Ten items fit perfectly into two trips of size 5. Using a formula like `len // 5 + 1` without checking divisibility would fail here.

## Approaches

The brute-force idea is to simulate the process literally. We walk through the string while tracking the current carried type and how many objects are currently in hand. Whenever the type changes or the hand reaches 5 items, we make a trip to the closet and continue.

This simulation is already fast enough because the string is extremely short. The total work is proportional to the string length.

There is an even cleaner way to think about the same process.

The wall naturally splits into maximal contiguous groups of equal characters. For example:

```
CCCPPCCCC
```

becomes:

```
CCC | PP | CCCC
```

Each group is completely independent because Polycarpus cannot mix types in his hands. Inside one group of size `k`, the minimum number of trips is simply:

```
ceil(k / 5)
```

since each trip can carry at most 5 objects.

The whole problem reduces to scanning the string, finding the lengths of consecutive equal-character blocks, and summing their required trips.

The brute-force simulation works because it models the real process directly, but the grouping observation turns the problem into a simple counting task.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n) | O(1) | Accepted |
| Optimal Group Counting | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the input string.
2. Initialize an answer variable `ans = 0`.
3. Scan the string from left to right while grouping consecutive equal characters together.
4. For each group, count its length `cnt`.
5. Compute how many trips this group needs using:

```
(cnt + 4) // 5
```

This is integer arithmetic for `ceil(cnt / 5)`.

1. Add this value to the final answer.
2. Continue until the entire string is processed.
3. Print the answer.

Why it works:

Each trip may contain only one object type, so objects from different groups can never be combined into one trip. Inside a single group, taking as many objects as possible per trip is always optimal because every trip has the same cost. Carrying fewer than 5 items voluntarily would only increase the number of trips. Since every group is handled optimally and independently, the total sum is globally optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().strip()

n = len(s)
ans = 0
i = 0

while i < n:
    j = i

    while j < n and s[j] == s[i]:
        j += 1

    cnt = j - i
    ans += (cnt + 4) // 5

    i = j

print(ans)
```

The solution uses two pointers, `i` and `j`, to identify contiguous blocks of equal characters.

`i` marks the start of the current group. `j` moves forward until the character changes. The group length is `j - i`.

The expression `(cnt + 4) // 5` is a standard integer-only way to compute ceiling division by 5. It handles all cases correctly, including when the group size is exactly divisible by 5.

Updating `i = j` moves directly to the next unprocessed group.

The implementation avoids unnecessary arrays or extra memory because the groups are processed on the fly.

## Worked Examples

### Example 1

Input:

```
CPCPCPC
```

| Step | Group | Length | Trips for Group | Total Answer |
| --- | --- | --- | --- | --- |
| 1 | C | 1 | 1 | 1 |
| 2 | P | 1 | 1 | 2 |
| 3 | C | 1 | 1 | 3 |
| 4 | P | 1 | 1 | 4 |
| 5 | C | 1 | 1 | 5 |
| 6 | P | 1 | 1 | 6 |
| 7 | C | 1 | 1 | 7 |

Final output:

```
7
```

This example shows the worst possible fragmentation. Since the type changes after every object, nothing can be grouped together.

### Example 2

Input:

```
CCCCCCPPPPPP
```

| Step | Group | Length | Trips for Group | Total Answer |
| --- | --- | --- | --- | --- |
| 1 | CCCCCC | 6 | 2 | 2 |
| 2 | PPPPPP | 6 | 2 | 4 |

Final output:

```
4
```

This demonstrates how large groups are split into batches of at most 5 items. Each block of 6 needs exactly two trips.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is processed once |
| Space | O(1) | Only a few variables are used |

The input size is tiny, so the solution easily fits within the limits. Even for the maximum length of 100, the algorithm performs only a single linear scan.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    s = input().strip()

    n = len(s)
    ans = 0
    i = 0

    while i < n:
        j = i

        while j < n and s[j] == s[i]:
            j += 1

        cnt = j - i
        ans += (cnt + 4) // 5

        i = j

    print(ans)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out

# provided sample
assert run("CPCPCPC\n") == "7\n", "sample 1"

# custom cases
assert run("C\n") == "1\n", "single item"
assert run("CCCCCCCCCC\n") == "2\n", "exact multiple of 5"
assert run("PPPPPP\n") == "2\n", "single group larger than 5"
assert run("CCCPPCCCC\n") == "3\n", "multiple groups"
assert run(("C" * 100) + "\n") == "20\n", "maximum length all same"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `C` | `1` | Minimum-size input |
| `CCCCCCCCCC` | `2` | Exact divisibility by 5 |
| `PPPPPP` | `2` | One extra trip after capacity overflow |
| `CCCPPCCCC` | `3` | Correct separation between groups |
| `C` repeated 100 times | `20` | Maximum-size input |

## Edge Cases

Consider the input:

```
CCCCCCCCCC
```

The algorithm finds one group of length 10.

```
(10 + 4) // 5 = 14 // 5 = 2
```

So the answer is `2`. This correctly handles the exact-divisibility case.

Now consider:

```
CPPPP
```

The groups are:

```
C
PPPP
```

The first contributes `1` trip, the second contributes `1` trip, for a total of `2`.

The algorithm never tries to combine objects across a type change, which matches the rules exactly.

Finally, consider the highly alternating case:

```
PCPCPC
```

Every group has size `1`, so every object requires its own trip.

The algorithm processes six separate groups:

```
1 + 1 + 1 + 1 + 1 + 1 = 6
```

This confirms the grouping logic also handles the maximum possible fragmentation correctly.
