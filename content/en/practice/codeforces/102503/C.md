---
title: "CF 102503C - Partial Reduplication"
description: "A dish name is built by concatenating three possible pieces: TJ, si, and log. Each occurrence of one piece represents one serving of its corresponding ingredient."
date: "2026-08-06T19:01:17+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102503
codeforces_index: "C"
codeforces_contest_name: "National Olympiad in Informatics - Philippines (NOI.PH) Online Eliminations 2020"
rating: 0
weight: 102503
solve_time_s: 274
verified: true
draft: false
---

[CF 102503C - Partial Reduplication](https://codeforces.com/problemset/problem/102503/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 4m 34s  
**Verified:** yes  

## Solution
## Problem Understanding

A dish name is built by concatenating three possible pieces: `TJ`, `si`, and `log`. Each occurrence of one piece represents one serving of its corresponding ingredient. The pieces are mixed together without separators, and the task is to recover how many times each of the three pieces appears.

The input gives several dish names. Each name comes with its length, but the length is only there as input metadata, because the string itself contains all the information needed. For every name, the output must contain three counts in the order `TJ`, `si`, and `log`.

The total length of all dish names is at most 100000. That means an algorithm should process each character only a constant number of times. A quadratic approach would perform around 100000² operations in the worst case, which is far beyond what is needed and would not fit comfortably in the time limit. A linear scan is enough because every character belongs to exactly one of the three valid pieces.

The main edge cases come from the fact that the pieces have different lengths. A careless solution might count characters instead of tokens, or assume every lowercase segment has the same size.

For example:

```
1
TJTJ
```

The correct output is:

```
2 0 0
```

Counting the number of `T` characters or treating every two characters as a token works here by accident, but it fails as soon as `si` and `log` appear.

Another case is:

```
1
silog
```

The correct output is:

```
0 1 1
```

A solution that searches for `log` first and skips three characters may incorrectly miss the `si` part if it does not maintain the correct scanning position.

A final boundary case is a name containing only one token:

```
1
log
```

The correct output is:

```
0 0 1
```

The implementation must handle short strings without trying to read characters beyond the end.

## Approaches

The straightforward approach is to repeatedly look for known pieces in the string and remove them. Since the string is guaranteed to be valid, we can always find a decomposition into `TJ`, `si`, and `log`. This method is correct because every removed piece corresponds to one serving.

The problem with this approach is the repeated searching and rebuilding of the remaining string. If a string has length 100000, repeatedly scanning large portions of it can lead to around 100000 × 100000 operations in the worst case, which is about 10 billion character checks. That is unnecessary.

The key observation is that the string is already arranged as a sequence of valid pieces. We do not need to find where the pieces are globally. We only need to decide the current piece while moving from left to right. The first character completely determines the token type. A `T` must start a `TJ`, while a lowercase character starts either `si` or `log`. Among lowercase tokens, the second character distinguishes them because `si` begins with `s` and `log` begins with `l`.

The brute-force works because every valid decomposition gives the same counts, but it fails because it keeps rediscovering positions that a single scan can identify immediately. The observation that every token has a unique starting pattern lets us reduce the entire task to a linear parser.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Start at the first character of the dish name and move from left to right. Maintain three counters for `TJ`, `si`, and `log`.
2. If the current character is `T`, count one `TJ` and move the index forward by two positions. The validity guarantee means the next character must be `J`.
3. If the current character is `s`, count one `si` and move the index forward by two positions. The next character must be `i`, so the token is fully consumed.
4. If the current character is `l`, count one `log` and move the index forward by three positions. The next two characters are guaranteed to complete the token.
5. After the scan reaches the end of the string, print the three counters.

The reason this parsing works is that no two valid tokens share the same starting character. When the scan is at the beginning of a remaining token, there is exactly one possible interpretation, so there is no need for backtracking or dynamic programming.

Why it works:

The invariant during the scan is that every character before the current index has already been split into complete tokens and counted correctly. At each step, the next token is uniquely identified by its first character, so the algorithm consumes exactly one valid token and increases exactly its corresponding counter. Since the input is guaranteed to be a valid dish name, the scan consumes the whole string, leaving the counters equal to the number of occurrences of each ingredient token.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        n, s = input().split()

        tj = 0
        si = 0
        log = 0

        i = 0
        while i < len(s):
            if s[i] == 'T':
                tj += 1
                i += 2
            elif s[i] == 's':
                si += 1
                i += 2
            else:
                log += 1
                i += 3

        ans.append(f"{tj} {si} {log}")

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The input is read using `sys.stdin.readline` because there can be many test cases. The function processes each string independently and stores the answers before printing them together.

The three counters directly represent the required output values. The index variable is advanced by the length of the token that was recognized. This is the important implementation detail because increasing it by one would repeatedly inspect characters that are already part of a counted token.

No bounds checking is needed before reading the next characters of a token because the input guarantees that every dish name is valid. Integer overflow is not a concern in Python, and the maximum possible counter value is only the string length.

## Worked Examples

### Sample 1

Input:

```
1
TJTJTJTJTJ
```

The scan repeatedly finds the two-character token `TJ`.

| Index | Current token | TJ count | si count | log count |
| --- | --- | --- | --- | --- |
| 0 | TJ | 1 | 0 | 0 |
| 2 | TJ | 2 | 0 | 0 |
| 4 | TJ | 3 | 0 | 0 |
| 6 | TJ | 4 | 0 | 0 |
| 8 | TJ | 5 | 0 | 0 |

The invariant is visible here: after every jump, the processed prefix consists only of complete tokens. The final answer is `5 0 0`.

### Sample 2, first case

Input:

```
TJsilogsilogloglog
```

| Index | Current token | TJ count | si count | log count |
| --- | --- | --- | --- | --- |
| 0 | TJ | 1 | 0 | 0 |
| 2 | si | 1 | 1 | 0 |
| 4 | log | 1 | 1 | 1 |
| 7 | si | 1 | 2 | 1 |
| 9 | log | 1 | 2 | 2 |
| 12 | log | 1 | 2 | 3 |
| 15 | log | 1 | 2 | 4 |

The trace shows why looking only at the first character is enough. Every transition has one possible token, so the parser never needs to reconsider previous choices. The final answer is `1 2 4`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Every character is visited once as part of exactly one token. |
| Space | O(1) | Only three counters and the current index are stored. |

The total input size is at most 100000 characters, so a linear scan easily fits within the time limit. The memory usage stays constant apart from storing the input strings required by Python.

## Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline
    t = int(input())
    out = []

    for _ in range(t):
        n, s = input().split()
        tj = si = log = 0
        i = 0

        while i < len(s):
            if s[i] == 'T':
                tj += 1
                i += 2
            elif s[i] == 's':
                si += 1
                i += 2
            else:
                log += 1
                i += 3

        out.append(f"{tj} {si} {log}")

    return "\n".join(out)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    result = solve()
    sys.stdin = old_stdin
    return result

assert run("""1
10 TJTJTJTJTJ
""") == "5 0 0", "sample 1"

assert run("""2
18 TJsilogsilogloglog
10 silogsilog
""") == "1 2 4\n0 2 2", "sample 2"

assert run("""1
2 TJ
""") == "1 0 0", "single TJ token"

assert run("""1
3 log
""") == "0 0 1", "single log token"

assert run("""1
14 silogloglog
""") == "0 1 3", "multiple adjacent log tokens"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `TJ` | `1 0 0` | Handles the shortest possible hotdog token. |
| `log` | `0 0 1` | Handles the shortest possible egg token. |
| `silogloglog` | `0 1 3` | Checks that the parser separates adjacent tokens correctly. |

## Edge Cases

For the input:

```
1
TJTJ
```

the algorithm starts at index `0`, sees `T`, adds one to the `TJ` counter, and jumps to index `2`. It repeats the same action and produces:

```
2 0 0
```

This handles strings made only from one token type.

For the input:

```
1
silog
```

the algorithm first sees `s`, counts `si`, and moves to the `l` character. It then counts `log`. The result is:

```
0 1 1
```

This confirms that shorter tokens can appear immediately before longer tokens without ambiguity.

For the input:

```
1
log
```

the algorithm enters the `else` branch once, increases the `log` counter, and moves past all three characters. The output is:

```
0 0 1
```

The scan never attempts to access characters outside the string because the index moves exactly by the size of the recognized token.
