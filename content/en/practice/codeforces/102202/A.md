---
title: "CF 102202A - Rainbow Beads"
description: "We have a string of length (N), where every position contains one of three colors: R, B, or V. We may choose one contiguous substring and give it away. The chosen substring must look diverse to three different observers."
date: "2026-08-18T10:59:34+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102202
codeforces_index: "A"
codeforces_contest_name: "2019 KAIST RUN Spring Contest"
rating: 0
weight: 102202
solve_time_s: 897
verified: false
draft: false
---

[CF 102202A - Rainbow Beads](https://codeforces.com/problemset/problem/102202/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 14m 57s  
**Verified:** no  

## Solution
## Problem Understanding

We have a string of length (N), where every position contains one of three colors: `R`, `B`, or `V`. We may choose one contiguous substring and give it away. The chosen substring must look diverse to three different observers.

For an ordinary observer, neighboring colors must simply be different. A red-colorblind observer treats `R` and `V` as the same color, so `R` cannot be adjacent to `V`. A blue-colorblind observer treats `B` and `V` as the same color, so `B` cannot be adjacent to `V`.

Combining these three requirements gives a much simpler condition. An adjacent pair can only be `RB` or `BR`. Equal colors are forbidden, `RV` and `VR` are forbidden, and `BV` and `VB` are forbidden. Consequently, a valid substring of length at least two contains no `V` at all and must alternate perfectly between `R` and `B`.

A substring consisting of one `V` is also valid because it has no adjacent pair to violate any condition. Thus the answer is the maximum length of an alternating `R` and `B` segment, with the value at least (1).

The constraint (N \le 250,000) rules out algorithms that inspect a quadratic number of substrings with substantial work per substring. Even an (O(N^2)) solution performs around (31) billion pairwise extensions at the maximum input size, which is far beyond a one-second time limit in Python. We need a linear scan.

There are several small cases where an implementation based only on the alternating `R` and `B` idea can go wrong. For example, with input `1` and string `V`, the correct answer is `1`. A careless implementation that searches only for `R/B` runs could return `0`.

With input `4` and string `RRRR`, the correct answer is `1`. No pair of adjacent positions is valid, but every individual jewel is valid. An implementation that initializes the answer to zero and only updates it when it finds a valid adjacent pair would fail here.

With input `3` and string `RVB`, the correct answer is `1`. Although all three original colors are different, `RV` is considered equal by a red-colorblind observer and `VB` is considered equal by a blue-colorblind observer. Checking only ordinary color differences would incorrectly return `3`.

With input `5` and string `RBRBB`, the correct answer is `4`, coming from `RBRB`. A scan that forgets to include the final position when a run ends can incorrectly return `3`.

## Approaches

A direct solution can enumerate every possible starting position and extend the substring one character at a time. While extending, we check whether the newest adjacent pair is allowed. If it is, the current substring remains valid and we update the answer. If it is not, no longer substring with that same starting position can be valid, because every longer substring would still contain the invalid adjacent pair.

This brute-force method is correct because every possible substring is considered, and a substring is accepted exactly while all of its adjacent pairs satisfy the required condition. However, on a string such as `RBRBRB...`, almost every starting position can be extended all the way to the end. The number of adjacent-pair checks is then

[
1+2+\cdots+(N-1)=\frac{N(N-1)}2,
]

which is (\Theta(N^2)). For (N=250,000), that is (31,249,875,000) checks, so it is not suitable.

The key observation is that validity depends only on adjacent pairs. When scanning from left to right, suppose the current suffix is valid. If the next pair is valid, the suffix can simply be extended by one position. If the next pair is invalid, every substring ending at that position and starting at or before the beginning of the current suffix is also invalid. We only need to restart the valid length at the current position.

For this particular problem, a pair is valid exactly when it is `RB` or `BR`. Thus we can maintain the length of the longest valid substring ending at the current position. If `s[i]` differs from `s[i-1]` and neither character is `V`, we extend the current run. Otherwise, the longest valid substring ending at `i` has length exactly one.

The scan never moves backward, so the whole computation takes (O(N)).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(N^2)) | (O(1)) | Too slow |
| Optimal | (O(N)) | (O(1)) | Accepted |

## Algorithm Walkthrough

1. Read the string and initialize `cur = 1` and `ans = 1`. A single jewel is always valid, so these are safe initial values even when the string contains only one character or only `V` characters.
2. Scan the string from the second character to the last character. At position `i`, check whether `s[i-1]` and `s[i]` form either `RB` or `BR`.
3. If the pair is valid, increment `cur`. The substring represented by the current valid run can safely absorb this new character because the only newly introduced adjacency is valid.
4. If the pair is invalid, set `cur = 1`. The previous valid run cannot continue through this position because its final adjacency is invalid. Starting at the current position is still possible because a single character has no adjacent pair.
5. Update `ans = max(ans, cur)` after processing each position. The largest `cur` seen during the scan is exactly the longest valid contiguous substring.

### Why it works

The invariant is that after processing position `i`, `cur` is the length of the longest valid substring that ends exactly at `i`. If the pair between `i-1` and `i` is `RB` or `BR`, appending `s[i]` to the previous longest valid suffix preserves validity, so the new length is `cur + 1`. If that pair is anything else, every substring of length at least two ending at `i` would contain this invalid pair, so the only valid suffix ending at `i` has length one. Taking the maximum over all positions consequently gives the longest valid substring anywhere in the original bead.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    s = input().strip()

    cur = 1
    ans = 1

    for i in range(1, n):
        if (s[i - 1] == 'R' and s[i] == 'B') or \
           (s[i - 1] == 'B' and s[i] == 'R'):
            cur += 1
        else:
            cur = 1

        ans = max(ans, cur)

    print(ans)

if __name__ == "__main__":
    solve()
```

The initialization uses `1` because every individual jewel is a valid bead. This also handles (N=1) without requiring a special case inside the loop.

The condition explicitly checks for `RB` or `BR`. Checking only `s[i] != s[i-1]` would be wrong because `RV`, `VR`, `BV`, and `VB` are all forbidden. Checking for `V` separately is possible, but the two allowed pairs give the cleanest condition.

When an invalid pair is found, `cur` becomes `1`, not `0`. The current character itself can always start a new valid substring. Updating `ans` after both the extension and reset handles runs that finish at the final character as well.

Python integers do not have an overflow issue here, and the algorithm stores only the input string plus a constant number of integers.

## Worked Examples

### Sample 1

For `RBBB`, the only valid adjacent pair is `RB`. Once the first `B` is followed by another `B`, the current valid run has to restart.

| Position | Character | Pair | `cur` | `ans` |
| --- | --- | --- | --- | --- |
| 0 | R | none | 1 | 1 |
| 1 | B | RB | 2 | 2 |
| 2 | B | BB | 1 | 2 |
| 3 | B | BB | 1 | 2 |

The longest valid substring is `RB`, so the answer is `2`. The trace also shows why equal adjacent colors immediately terminate the current run.

### Sample 2

For `RBRBB`, the first four characters form an alternating sequence, and the final `BB` breaks it.

| Position | Character | Pair | `cur` | `ans` |
| --- | --- | --- | --- | --- |
| 0 | R | none | 1 | 1 |
| 1 | B | RB | 2 | 2 |
| 2 | R | BR | 3 | 3 |
| 3 | B | RB | 4 | 4 |
| 4 | B | BB | 1 | 4 |

The substring `RBRB` has length `4`, and the final `B` cannot extend it because the resulting `BB` pair is invalid. The algorithm keeps the previously achieved maximum, giving `4`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(N)) | Every character is processed exactly once. |
| Space | (O(N)) | The input string requires (O(N)) memory; the algorithm itself uses (O(1)) extra space. |

With (N) as large as (250,000), a single linear scan is easily within the intended scale for a one-second limit. The memory usage is also small compared with the 1024 MB limit.

## Test Cases

```python
import sys
import io

def solution(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    try:
        sys.stdin = io.StringIO(inp)
        sys.stdout = io.StringIO()

        input = sys.stdin.readline

        n = int(input())
        s = input().strip()

        cur = 1
        ans = 1

        for i in range(1, n):
            if (s[i - 1] == 'R' and s[i] == 'B') or \
               (s[i - 1] == 'B' and s[i] == 'R'):
                cur += 1
            else:
                cur = 1

            ans = max(ans, cur)

        print(ans)
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

assert solution("4\nRBBB\n") == "2\n", "sample 1"
assert solution("5\nRBRBB\n") == "4\n", "sample 2"

assert solution("1\nV\n") == "1\n", "single V"
assert solution("5\nRRRRR\n") == "1\n", "all equal"
assert solution("6\nRBRBRB\n") == "6\n", "entire string is alternating"
assert solution("7\nRRBRBRR\n") == "5\n", "long run in the middle"

max_n = 250000
assert solution(f"{max_n}\n" + "R" * max_n + "\n") == "1\n", \
    "maximum-size all-equal input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / V` | `1` | Minimum size and the fact that a single `V` is valid |
| `RRRRR` | `1` | All-equal colors and repeated resets |
| `RBRBRB` | `6` | The whole string can be the answer |
| `RRBRBRR` | `5` | A longest valid run can occur strictly inside the string |
| `R...R` with 250000 `R`s | `1` | Maximum input size and linear performance |

## Edge Cases

For a one-character input such as

```
1
V
```

the loop does not execute because there is no adjacent pair. The initial value `ans = 1` is already correct. This is why initializing the answer to zero would be unnecessarily fragile.

For an all-equal string such as

```
5
RRRRR
```

the first position starts with `cur = 1`. Every following pair is `RR`, so the algorithm resets `cur` to `1` at every position. The answer remains `1`, which matches the fact that no two adjacent jewels can coexist in a colorful substring.

For a string containing violet between the two other colors,

```
3
RVB
```

the pair `RV` fails the explicit allowed-pair check, so `cur` becomes `1`. The next pair `VB` fails as well, leaving the answer at `1`. This directly handles both colorblind interpretations without needing to simulate either observer separately.

For a longest valid segment at the end,

```
5
RRBRB
```

the scan resets at the first `RR`, then grows through `BR` and `RB`. The final position leaves `cur = 3`, corresponding to `BRB`, so the answer is `3`. This confirms that the algorithm updates the answer after processing the final character and does not require a separator after the longest run.

For the maximum-size all-equal input, the algorithm performs exactly one pass through all (250,000) characters. Every adjacent pair causes a constant-time reset, so the running time remains (O(N)), unlike the quadratic brute-force approach.
