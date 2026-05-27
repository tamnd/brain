---
title: "CF 1941C - Rudolf and the Ugly String"
description: "We are given a string and want to remove the minimum number of characters so that the resulting string no longer contain"
date: "2026-05-27T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dp", "greedy", "strings"]
categories: ["algorithms"]
codeforces_contest: 1941
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 933 (Div. 3)"
rating: 900
weight: 1941
solve_time_s: 161
verified: true
draft: false
---

[CF 1941C - Rudolf and the Ugly String](https://codeforces.com/problemset/problem/1941/C)

**Rating:** 900  
**Tags:** dp, greedy, strings  
**Solve time:** 2m 41s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string and want to remove the minimum number of characters so that the resulting string no longer contains `"pie"` or `"map"` as a substring.

The key detail is that deletions can happen at arbitrary positions. We are not rearranging characters, only deleting some of them. Every occurrence of `"pie"` or `"map"` must be broken somehow.

The string length across all test cases can reach `10^6`, which immediately rules out anything quadratic. An `O(n^2)` solution would perform around `10^12` operations in the worst case, far beyond the limit. We need something close to linear time.

A first instinct might be to repeatedly search for `"pie"` and `"map"` and delete one character from each occurrence. That mostly works, but overlapping patterns create tricky situations where one deletion can destroy two bad substrings at once.

The classic example is:

```
mapie
```

This string contains both `"map"` and `"pie"`:

```
mapie
^^^
  ^^^
```

A careless greedy solution might count both separately and answer `2`. But deleting the middle character `'p'` destroys both substrings at once, so the correct answer is `1`.

Another edge case appears when multiple bad substrings overlap only partially. Consider:

```
mapmap
```

The two `"map"` occurrences are independent:

```
mapmap
^^^
   ^^^
```

One deletion cannot break both occurrences, so the answer is `2`.

Very short strings also matter. For input:

```
p
```

there cannot possibly be a substring of length `3`, so the answer is `0`. Implementations that blindly check `s[i:i+3]` without bounds handling can make mistakes here.

A final subtle case is repeated overlaps:

```
pppiepieeee
```

The occurrences are:

```
pppiepieeee
  ^^^
     ^^^
```

These do not overlap in a useful way, so we really need two deletions.

## Approaches

A brute-force strategy is to try every possible set of deletions and check whether the resulting string becomes beautiful. This is obviously correct because it explores all possibilities, but it is completely infeasible. Even deciding for each character whether to keep or remove it creates `2^n` possibilities.

A more reasonable brute-force improvement is to repeatedly scan the string for `"pie"` and `"map"`, deleting one character whenever one is found. Since each bad substring has length `3`, deleting any one of its characters destroys that occurrence.

The problem is overlap handling. If we greedily process `"map"` first inside `"mapie"`, we may delete `'m'` or `'a'`, then still have `"pie"` remaining. We end up using two deletions instead of one.

The key insight is that the only useful overlap between `"map"` and `"pie"` is the special pattern:

```
mapie
```

Inside this pattern, one deletion is enough to destroy both bad substrings. Specifically, removing the central `'p'` works.

Outside this case, every occurrence of `"map"` or `"pie"` must contribute at least one deletion independently.

So the optimal strategy becomes:

1. Scan the string left to right.
2. First check whether `"mapie"` starts at the current position.
3. If it does, count one deletion and skip the whole pattern.
4. Otherwise, check whether `"map"` or `"pie"` starts there.
5. If yes, count one deletion and skip that substring.

This works because `"mapie"` is the only overlap where one deletion saves work compared to handling the two patterns separately.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Greedy Linear Scan | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize the answer counter to `0`.

This variable stores the minimum number of deletions needed.
2. Scan the string from left to right using an index `i`.

We examine substrings beginning at each position.
3. First check whether the substring starting at `i` is `"mapie"`.

This is the critical overlap case. If we process `"map"` or `"pie"` first, we may accidentally use two deletions instead of one.
4. If `"mapie"` is found, increment the answer by `1` and move `i` forward by `5`.

One deletion destroys both bad substrings, and none of the characters inside this block need to be reconsidered.
5. Otherwise, check whether the substring starting at `i` is `"map"` or `"pie"`.

Each such occurrence requires one deletion.
6. If either substring is found, increment the answer by `1` and move `i` forward by `3`.

After deleting one character from this substring, the entire occurrence becomes harmless.
7. If no bad substring starts at `i`, move to the next character.
8. After the scan finishes, output the answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())

for _ in range(t):
    n = int(input())
    s = input().strip()

    ans = 0
    i = 0

    while i < n:
        if i + 4 < n and s[i:i + 5] == "mapie":
            ans += 1
            i += 5
        elif i + 2 < n and (s[i:i + 3] == "map" or s[i:i + 3] == "pie"):
            ans += 1
            i += 3
        else:
            i += 1

    print(ans)
```

The implementation directly follows the greedy scan described earlier.

The first condition checks for `"mapie"` before anything else. That ordering matters. If we checked `"map"` first, then `"mapie"` would be counted incorrectly as two deletions.

The bounds checks are also important:

```
i + 4 < n
```

guarantees that `s[i:i+5]` is valid for checking `"mapie"`.

Similarly:

```
i + 2 < n
```

protects the length-3 substring checks.

Skipping ahead by `5` or `3` avoids reprocessing characters that already belong to a handled bad substring.

## Worked Examples

### Example 1

Input:

```
mmapnapie
```

| i | Current Slice | Action | Answer |
| --- | --- | --- | --- |
| 0 | mma | nothing | 0 |
| 1 | map | found `"map"` | 1 |
| 4 | nap | nothing | 1 |
| 5 | api | nothing | 1 |
| 6 | pie | found `"pie"` | 2 |

Final answer:

```
2
```

This example shows two completely separate bad substrings. Each requires its own deletion.

### Example 2

Input:

```
mapie
```

| i | Current Slice | Action | Answer |
| --- | --- | --- | --- |
| 0 | mapie | found `"mapie"` | 1 |

Final answer:

```
1
```

This trace demonstrates the special overlap case. Treating `"map"` and `"pie"` independently would incorrectly produce `2`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is processed at most once |
| Space | O(1) | Only a few variables are used |

The total input size is at most `10^6`, so a linear scan is easily fast enough within a 2 second limit. Memory usage stays constant regardless of string length.

## Test Cases

### Test Case 1

Input:

```
1
1
a
```

Expected output:

```
0
```

This verifies the minimum string length case.

### Test Case 2

Input:

```
1
5
mapie
```

Expected output:

```
1
```

This checks the important overlap optimization.

### Test Case 3

Input:

```
1
6
mapmap
```

Expected output:

```
2
```

This confirms that independent occurrences are counted separately.

### Test Case 4

Input:

```
1
9
piepiepie
```

Expected output:

```
3
```

This stresses repeated non-overlapping bad substrings.

## Edge Cases

The first tricky case is the overlap pattern:

```
mapie
```

The algorithm checks `"mapie"` before `"map"` or `"pie"`. At index `0`, it detects the full overlap and adds only one deletion. Then it skips all five characters. The final answer becomes `1`, which is optimal.

Now consider independent occurrences:

```
mapmap
```

At index `0`, the algorithm finds `"map"` and increments the answer to `1`. It skips three positions and lands on the second `"map"`, which requires another deletion. The result is `2`.

For a very short string:

```
p
```

the conditions:

```
i + 4 < n
i + 2 < n
```

both fail immediately, so no substring checks happen. The answer remains `0`.

Finally, examine repeated patterns:

```
pppiepieeee
```

The scan reaches the first `"pie"` and counts one deletion. After skipping ahead, it reaches the second `"pie"` and counts another. Since these occurrences do not overlap, the correct answer is `2`.
