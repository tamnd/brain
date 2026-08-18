---
title: "CF 102202A - Rainbow Beads"
description: "We have a string of length (N), where every jewel is colored R, B, or V. We may choose one contiguous substring and give it away. The chosen substring must look colorful to three different observers."
date: "2026-08-18T20:54:06+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102202
codeforces_index: "A"
codeforces_contest_name: "2019 KAIST RUN Spring Contest"
rating: 0
weight: 102202
solve_time_s: 577
verified: false
draft: false
---

[CF 102202A - Rainbow Beads](https://codeforces.com/problemset/problem/102202/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 9m 37s  
**Verified:** no  

## Solution
## Problem Understanding

We have a string of length (N), where every jewel is colored `R`, `B`, or `V`. We may choose one contiguous substring and give it away. The chosen substring must look colorful to three different observers.

A normal observer distinguishes all three colors, so adjacent jewels must have different original characters. A red-colorblind observer sees `R` and `V` as the same color, while a blue-colorblind observer sees `B` and `V` as the same color. The chosen substring must have no equal adjacent colors for any of these observers.

The key consequence is stronger than the original condition first suggests. Consider any adjacent pair containing `V`. If the other jewel is `R`, a red-colorblind observer sees two consecutive red jewels. If the other jewel is `B`, a blue-colorblind observer sees two consecutive blue jewels. If the pair is `VV`, everybody sees equal colors. Thus `V` cannot be adjacent to anything inside a valid substring.

The only adjacent pair that survives all three observers is `RB` or `BR`. Consequently, every valid substring of length at least two must contain only `R` and `B`, and those characters must alternate.

For example, `RBRB` is valid, while `RVB` is not. A single jewel such as `V` is always valid because it has no adjacent pair at all.

The input can contain up to (250,000) jewels. An (O(N^2)) algorithm would examine roughly (N(N+1)/2) substrings, which is about (31.25) billion when (N=250,000). That is far beyond a one-second time limit. We need to inspect the string only a constant number of times, giving an (O(N)) solution.

There are several edge cases that can easily cause an incorrect implementation.

Consider

```
1
V
```

The answer is `1`. A solution that only searches for alternating `R` and `B` segments might incorrectly return zero, forgetting that a single jewel is always valid.

Consider

```
4
RVBR
```

The answer is `1`. Although `V` is not equal to either neighboring character, it cannot be adjacent to `R` for the red-colorblind observer or to `B` for the blue-colorblind observer. A solution that checks only adjacent characters in the original string would incorrectly accept parts containing `V`.

Consider

```
5
RBRBB
```

The answer is `4`, from `RBRB`. The final `BB` breaks the alternating pattern, so a careless implementation that keeps the current length after seeing an invalid pair could overcount.

Finally,

```
5
RRRRR
```

has answer `1`. Equal adjacent `R` jewels are immediately invalid, but each individual jewel remains a valid substring.

## Approaches

A direct approach is to enumerate every contiguous substring and check whether it is colorful for all three observers. There are (N(N+1)/2) substrings. If each substring is checked by scanning all of its adjacent pairs, the worst-case work is (O(N^3)), which is clearly impossible.

We can make that naive idea slightly better by fixing a starting position and extending the substring one jewel at a time. Once an invalid adjacent pair appears, every longer substring beginning at the same position is also invalid, so we do not need to rescan the whole substring. This reduces the work to (O(N^2)), because in the worst case we still inspect every possible ending position for every starting position. For (N=250,000), that is about (31.25) billion extensions, still far too many.

The brute-force approach works because validity is determined entirely by adjacent pairs. The useful observation is that after combining the requirements of all three observers, almost every pair becomes forbidden. `R` next to `B` is the only valid pair. A `V` can never participate in a valid substring of length greater than one.

That means we do not need to consider arbitrary substrings at all. We only need to find the longest contiguous section where every character is `R` or `B` and every adjacent pair is different. Such a section is simply an alternating sequence like `RBRBR` or `BRBRB`.

We can scan the string once. While the current character continues an alternating `R`/`B` sequence, increase its length. Otherwise, start a new sequence of length one if the current character is `R` or `B`. For `V`, no longer sequence can pass through it, so the current length becomes one.

Since a single jewel is always valid, the answer is at least one.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(N^3)) | (O(1)) | Too slow |
| Incremental Brute Force | (O(N^2)) | (O(1)) | Too slow |
| Optimal Scan | (O(N)) | (O(1)) | Accepted |

## Algorithm Walkthrough

1. Read the string and initialize the best valid length to `1`. A one-jewel substring has no adjacent pair, so it is always colorful.
2. Maintain `cur`, the length of the longest valid substring ending at the current position. Initially `cur = 1`.
3. For every position after the first, inspect the previous and current characters. If both are `R` or `B` and they are different, the pair is valid for all three observers, so extend the current substring by setting `cur += 1`.
4. Otherwise, the previous substring cannot be extended through this position. Set `cur = 1`, because the current jewel by itself is always a valid substring.
5. Update the global answer with `max(ans, cur)` after processing each character.

The reason we can discard the previous substring immediately after an invalid pair is that every longer substring ending at the current position and beginning before the invalid pair would still contain that same forbidden adjacent pair. There is no benefit in keeping any of it.

### Why it works

For a substring of length at least two to be colorful for all three observers, every adjacent pair must be valid for all three color interpretations. `R-B` and `B-R` are the only such pairs. Every pair containing `V` is invalid for at least one observer, and equal `R` or equal `B` pairs are invalid for the normal observer.

Thus a valid substring of length at least two is exactly an alternating sequence of `R` and `B`. During the scan, `cur` is precisely the longest such sequence ending at the current position. A valid `R/B` pair extends it, while any other pair makes extension impossible and forces the best valid suffix to be the current single jewel. Taking the maximum value of `cur` over all positions consequently gives the longest valid contiguous substring.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    s = input().strip()

    ans = 1
    cur = 1

    for i in range(1, n):
        if s[i] in "RB" and s[i - 1] in "RB" and s[i] != s[i - 1]:
            cur += 1
        else:
            cur = 1

        if cur > ans:
            ans = cur

    print(ans)

if __name__ == "__main__":
    solve()
```

The input is read with `readline`, which is more than sufficient for a string of length (250,000). The string itself is stored once.

`cur` represents the valid suffix ending at the current position. The condition

```
s[i] in "RB" and s[i - 1] in "RB" and s[i] != s[i - 1]
```

checks exactly whether the new adjacent pair is either `RB` or `BR`. Checking membership in `RB` is necessary because `V` cannot appear in a valid substring of length greater than one.

When the condition fails, `cur` becomes `1` rather than `0`. This handles both ordinary breaks such as `BB` and the special case of `V`. The current jewel can always start a new valid substring by itself.

There is no integer overflow issue in Python, and `cur` never exceeds (N). The scan starts at index `1`, so the previous character access is always inside the string.

## Worked Examples

### Sample 1

The input is:

```
4
RBBB
```

The important state is the length of the current alternating `R/B` suffix.

| Position | Character | Previous | Pair valid? | `cur` | `ans` |
| --- | --- | --- | --- | --- | --- |
| 0 | R | - | - | 1 | 1 |
| 1 | B | R | Yes | 2 | 2 |
| 2 | B | B | No | 1 | 2 |
| 3 | B | B | No | 1 | 2 |

The first two jewels form `RB`, which is valid for every observer. The next `B` creates `BB`, so the alternating sequence must restart there. The answer is `2`.

### Sample 2

The input is:

```
5
RBRBB
```

| Position | Character | Previous | Pair valid? | `cur` | `ans` |
| --- | --- | --- | --- | --- | --- |
| 0 | R | - | - | 1 | 1 |
| 1 | B | R | Yes | 2 | 2 |
| 2 | R | B | Yes | 3 | 3 |
| 3 | B | R | Yes | 4 | 4 |
| 4 | B | B | No | 1 | 4 |

The prefix `RBRB` is completely alternating, giving length `4`. The final `B` cannot extend it because it creates `BB`. The answer is consequently `4`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(N)) | Every jewel is processed exactly once after the first one. |
| Space | (O(N)) | The input string requires (O(N)) storage; the algorithm itself uses (O(1)) additional space. |

With (N \le 250,000), the algorithm performs only a few constant-time operations per character. This is comfortably within the one-second constraint, while the quadratic approaches would require billions of iterations in the worst case.

## Test Cases

```python
import sys
import io

def solution(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    n = int(input())
    s = input().strip()

    ans = 1
    cur = 1

    for i in range(1, n):
        if s[i] in "RB" and s[i - 1] in "RB" and s[i] != s[i - 1]:
            cur += 1
        else:
            cur = 1

        ans = max(ans, cur)

    sys.stdin = old_stdin
    return str(ans)

# Provided samples
assert solution("4\nRBBB\n") == "2", "sample 1"
assert solution("5\nRBRBB\n") == "4", "sample 2"

# Minimum-size input
assert solution("1\nV\n") == "1", "single V is always valid"

# All equal values
assert solution("5\nRRRRR\n") == "1", "equal adjacent colors are invalid"

# V cannot be part of a multi-character valid substring
assert solution("5\nRVBRB\n") == "4", "longest valid part is BRBR"

# Maximum-size input
assert solution("250000\n" + "RB" * 125000 + "\n") == "250000", \
    "entire maximum-length alternating string is valid"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\nV\n` | `1` | Minimum size and the fact that a single `V` is valid |
| `5\nRRRRR\n` | `1` | Repeated equal colors must break the sequence |
| `5\nRVBRB\n` | `4` | `V` cannot belong to a valid substring of length greater than one |
| `250000\n` followed by `RB` repeated 125000 times | `250000` | Maximum input size and the full-length boundary case |

## Edge Cases

For the single-jewel case

```
1
V
```

the loop does not execute because there is no adjacent pair. `ans` starts at `1`, so the algorithm prints `1`. This is why initializing the answer to zero would also work only if the implementation separately handled the empty scan, while the chosen initialization naturally matches the problem's guarantee that (N \ge 1).

For a substring containing `V`, consider

```
4
RVBR
```

At position `1`, the pair `RV` is invalid, so `cur` becomes `1`. At position `2`, the pair `VB` is also invalid, so `cur` remains `1`. At position `3`, `BR` is valid, so `cur` becomes `2`. The answer is `2`, corresponding to the final substring `BR`. This demonstrates that `V` is not merely a separator between two sequences, but that it cannot participate in a multi-jewel valid substring at all.

For repeated colors,

```
5
RRRRR
```

every adjacent pair is `RR`. Each pair fails the alternating `R/B` condition, so `cur` repeatedly resets to `1`. The maximum remains `1`, which is correct because any substring of length at least two contains equal adjacent red jewels.

For a boundary where the longest sequence reaches the end,

```
5
BRBRB
```

every pair is valid. `cur` progresses through `1, 2, 3, 4, 5`, and `ans` reaches `5`. There is no special end-of-string handling because the answer is updated while processing the final character.

For the maximum-size alternating input, consisting of `250000` characters in the pattern `RBRB...`, every adjacent pair is either `RB` or `BR`. The current length consequently reaches `250000`, and the algorithm returns the entire bead. This confirms that the linear scan handles the largest allowed input without any special-case logic.
