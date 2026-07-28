---
title: "CF 102766F - Singhal and Broken Keyboard (easy version)"
description: "We have a keyboard with only two possible keys, a and b. When a key is pressed, the keyboard does not print the character once. Instead, it prints either two copies or three copies of that character."
date: "2026-07-28T23:40:36+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102766
codeforces_index: "F"
codeforces_contest_name: "Codedigger Training Contest -String"
rating: 0
weight: 102766
solve_time_s: 75
verified: true
draft: false
---

[CF 102766F - Singhal and Broken Keyboard (easy version)](https://codeforces.com/problemset/problem/102766/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 15s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a keyboard with only two possible keys, `a` and `b`. When a key is pressed, the keyboard does not print the character once. Instead, it prints either two copies or three copies of that character. Given the sequence of keys Singhal presses, we need to count how many different final strings could appear.

The input contains several original strings. Each string contains only `a` and `b`, and the output for each one is the number of distinct strings that can be produced, modulo `10^9 + 7`.

The main difficulty is that different choices of expansions can lead to the same final string. For example, pressing `a` twice can produce `aaaa`, `aaaaa`, or `aaaaaa`. The result `aaaaa` can be created by expanding the first `a` to length two and the second to length three, or the other way around. We only count the resulting string once.

The total length of all input strings is at most `10^5`. This rules out generating all possible outputs because the number of combinations grows exponentially. If a string has length `n`, there are already `2^n` possible choices of whether each key press becomes two or three characters. Even for moderate `n`, this is far beyond what a one second solution can handle. We need to find a counting formula that processes each character a constant number of times.

The tricky cases come from consecutive equal characters. A naive approach might treat every key press independently and multiply by two choices per character. That overcounts because neighboring equal characters form one continuous block in the final string.

For example:

```
Input:
aa

Correct output:
3
```

The possible outputs are `aaaa`, `aaaaa`, and `aaaaaa`. Multiplying two independent choices would give four possibilities, but two different expansion choices produce the same middle string.

Another important case is when all characters are different from their neighbors.

```
Input:
aba

Correct output:
8
```

Each character creates its own separate block, so every choice changes the final string. The possible block lengths are independently chosen as either two or three, giving `2 * 2 * 2 = 8` results.

A final edge case is a single character.

```
Input:
b

Correct output:
2
```

The only possibilities are `bb` and `bbb`. The algorithm must still handle a string with only one run correctly.

## Approaches

The brute-force approach is to simulate every possible keyboard behavior. For every character, choose whether it expands to length two or three, build the resulting string, and store all results in a set. This is correct because the set removes duplicates automatically.

However, for a string of length `n`, there are `2^n` expansion choices. A string of length `50` would already create more than one quadrillion possibilities, so this method cannot work under the constraints.

The useful observation comes from looking at runs of equal characters. Consider a consecutive block of the same character with length `k`. Every character in this block expands to either two or three copies, so the total length of the block can be any value from `2k` to `3k`. Every length in this interval is possible because each character contributes either two or two plus one extra character.

The number of possible final lengths for this block is:

```
3k - 2k + 1 = k + 1
```

Different blocks of characters cannot interfere with each other because neighboring blocks contain different letters. The final string is completely determined by the expanded length of every block. Therefore, the number of possible strings is the product of the number of choices for every run.

The brute-force method works because every expansion choice is considered separately, but it fails because many choices collapse into the same run length. Compressing the string into runs removes this duplication and reduces the problem to a simple multiplication.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n * n) | O(2^n * n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Scan the string from left to right and identify consecutive groups of equal characters. A group represents one block that will remain a single character block after expansion.
2. For every group with length `k`, multiply the answer by `k + 1`. This value represents all possible final lengths of this block, from `2k` through `3k`.
3. Continue until every group has been processed. Keep the multiplication under modulo `10^9 + 7` because the number of possible strings can become very large.

Why it works:

A final string can be described uniquely by the expanded lengths of the original runs. The characters of different runs alternate, so knowing the length of each run tells us exactly where every character changes. A run of length `k` has exactly `k + 1` possible expanded lengths. Since each run can choose its length independently, multiplying these values counts every possible final string exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10 ** 9 + 7

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        s = input().strip()

        result = 1
        current = 1

        for i in range(1, len(s)):
            if s[i] == s[i - 1]:
                current += 1
            else:
                result = (result * (current + 1)) % MOD
                current = 1

        result = (result * (current + 1)) % MOD
        ans.append(str(result))

    print("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The variable `current` stores the size of the current run. Whenever the character changes, that run is finished and contributes its factor of `current + 1`.

The final run needs separate handling after the loop because there is no next character that would trigger the multiplication. Forgetting this step is a common source of wrong answers.

The modulo operation is applied after every multiplication. Python integers do not overflow, but keeping values reduced prevents unnecessary growth and matches the required output.

The algorithm only counts runs, so it does not need to store the expanded strings or even the run structure. It uses constant extra memory apart from the input and output storage.

## Worked Examples

For `S = "aba"`:

| Step | Current character | Current run length | Result |
| --- | --- | --- | --- |
| Start | a | 1 | 1 |
| Finish a | a | 1 | 2 |
| Finish b | b | 1 | 4 |
| Finish a | a | 1 | 8 |

The three runs are independent. Each run can become length two or three, so the answer is `2 * 2 * 2 = 8`.

For `S = "aa"`:

| Step | Current character | Current run length | Result |
| --- | --- | --- | --- |
| Start | a | 1 | 1 |
| End of string | a | 2 | 3 |

The two key presses are part of one run. The run length can become four, five, or six, giving three distinct strings.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Every character is visited once while forming runs. |
| Space | O(1) | Only counters and the current answer are stored. |

The total length of all strings is `10^5`, so a linear scan easily fits within the limits. The solution avoids the exponential number of expansion choices by counting possible run lengths directly.

## Test Cases

```python
import sys
import io

MOD = 10 ** 9 + 7

def solution(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []

    for _ in range(t):
        s = input().strip()

        ans = 1
        run = 1

        for i in range(1, len(s)):
            if s[i] == s[i - 1]:
                run += 1
            else:
                ans = ans * (run + 1) % MOD
                run = 1

        ans = ans * (run + 1) % MOD
        out.append(str(ans))

    return "\n".join(out)

assert solution("""4
a
ab
aba
aa
""") == """2
4
8
3""", "provided samples"

assert solution("""1
b
""") == "2", "single character"

assert solution("""1
aaaa
""") == "5", "single long run"

assert solution("""1
ababab
""") == "64", "all separate runs"

assert solution("""1
aabbaa
""") == "27", "multiple equal blocks"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `b` | `2` | Minimum-size string with one run |
| `aaaa` | `5` | A single large block where choices merge |
| `ababab` | `64` | Every character forms an independent block |
| `aabbaa` | `27` | Several runs with different lengths |

## Edge Cases

For the input:

```
aa
```

The algorithm sees one run of length `2`. It multiplies the answer by `2 + 1`, producing `3`. The three possible final strings are `aaaa`, `aaaaa`, and `aaaaaa`. It does not count different expansion orders separately because only the total run length matters.

For the input:

```
aba
```

The algorithm processes three runs of length `1`. Each contributes a factor of `2 +?`

Correction: each run of length `1` contributes `1 + 1 = 2`, so the answer becomes `2 * 2 * 2 = 8`. Since the runs contain different characters, no two choices can merge into the same final string.

For the input:

```
b
```

There is one run with length `1`. Its possible lengths are `2` and `3`, giving the factor `1 + 1 = 2`. The algorithm handles the case because the last run is multiplied after the scan ends.
