---
title: "CF 106145F - Tung Tung Tung"
description: "The problem gives two strings made only from L and R. The first string describes the actual sequence of drum hits. Each hit creates either one visible character or two identical visible characters in the recorded sound. The second string is the recording we hear."
date: "2026-06-25T11:29:06+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106145
codeforces_index: "F"
codeforces_contest_name: "UTPC Contest 10-29-25"
rating: 0
weight: 106145
solve_time_s: 30
verified: true
draft: false
---

[CF 106145F - Tung Tung Tung](https://codeforces.com/problemset/problem/106145/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 30s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem gives two strings made only from `L` and `R`. The first string describes the actual sequence of drum hits. Each hit creates either one visible character or two identical visible characters in the recorded sound. The second string is the recording we hear. We need to decide whether every hit in the first string can be expanded into one or two copies of the same character to form the second string.

For example, a hit sequence `LR` can become `LR`, `LLR`, `LRR`, or `LLRR`. The expansion of each original character is independent, so the only allowed change is that every character may be duplicated once.

The constraints make a direct simulation of every possible expansion impossible. If a string has length `n`, each character has two choices, so trying all possible recordings would require checking up to `2^n` possibilities. Even for a few dozen characters this becomes infeasible. The intended solution must process each character a constant number of times, giving an `O(n)` algorithm.

The tricky parts are not the large strings but the boundaries between groups of equal characters. A common mistake is to only check whether the two strings have the same compressed form. Compression alone is not enough because the lengths of the groups matter.

For example:

```
Input:
p = "L"
s = "LLL"
```

The correct output is:

```
NO
```

A careless solution may see that both strings consist only of `L` and accept them. However, one original hit can produce at most two `L` characters, so three characters are impossible.

Another edge case is when the order of groups changes:

```
Input:
p = "LR"
s = "LLL"
```

The correct output is:

```
NO
```

The second string has only one group of `L`, while the original sequence has two different hits. The missing `R` cannot be created by expanding an `L`.

A final boundary case is when the recorded string is shorter:

```
Input:
p = "LL"
s = "L"
```

The correct output is:

```
NO
```

Each original character must contribute at least one character, so two hits cannot disappear into one recorded character.

## Approaches

A brute force approach would try every possible way to expand the first string. For each character we choose whether it stays as one character or becomes two copies, then compare the generated result with the recording. This is correct because it examines every possible interpretation of the hits. The problem is that a string of length `n` has `2^n` possible expansions, which quickly becomes too large.

The useful observation is that every character in the original string corresponds to a consecutive block of the same character in the recording. An `L` can only create `L` characters, and it must create either one or two of them. The same applies to `R`.

This means we do not need to construct the possible expanded strings. We only need to walk through both strings and compare matching groups. If the original string has a group of `k` identical characters, the recorded string must have a group of the same character with length between `k` and `2k`. In this problem, because every character of the original string is a separate hit, each original group length is counted directly. This reduces the problem to comparing run lengths.

The brute force works because every valid expansion follows the rules of the hits, but fails because it explores choices that can be checked locally. The observation that every hit only affects its own consecutive block lets us replace exponential exploration with a linear scan.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Set two pointers at the beginning of the original string and the recorded string. The pointers represent the next unprocessed hit and sound.
2. For the current character in the original string, count how many consecutive equal characters it has. Do the same for the corresponding group in the recorded string. The groups must start with the same character because a hit cannot change from `L` to `R` or the other way around.
3. Check the relationship between the two group lengths. The recorded group length must be at least the original group length because every hit creates one sound, and it must be at most twice the original group length because every hit can create at most two sounds.
4. Move both pointers to the next groups and repeat until one of the strings is exhausted.
5. After the scan finishes, accept only if both strings have been completely consumed. Any remaining characters mean one string contains unmatched hits or sounds.

Why it works:

Every maximal block of equal characters in the original string represents a consecutive sequence of hits on the same drum. Those hits cannot mix with other characters in the recording, so they must correspond to exactly one block in the recorded string. The only possible difference is the length of that block, because each hit contributes either one or two characters. The algorithm checks precisely this condition for every block, so it accepts exactly the valid recordings.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        p = input().strip()
        s = input().strip()

        i = 0
        j = 0
        ok = True

        while i < len(p) and j < len(s):
            if p[i] != s[j]:
                ok = False
                break

            pi = i
            while i < len(p) and p[i] == p[pi]:
                i += 1

            sj = j
            while j < len(s) and s[j] == s[sj]:
                j += 1

            p_len = i - pi
            s_len = j - sj

            if s_len < p_len or s_len > 2 * p_len:
                ok = False
                break

        if i != len(p) or j != len(s):
            ok = False

        ans.append("YES" if ok else "NO")

    print("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The main loop keeps two indices, one for each string. It never moves backwards, which is why the total work is linear.

The inner loops find the end of the current block. After they finish, `p_len` is the number of hits producing this block and `s_len` is the number of sounds in the recording. The only valid range is from `p_len` to `2 * p_len`.

The final comparison of `i` and `j` is needed because the main loop can stop after one string ends. Without this check, an implementation could incorrectly accept a prefix match while ignoring extra characters.

Python integers are not a concern here because the algorithm only stores lengths and indices. The largest values are bounded by the input size.

## Worked Examples

Consider:

```
p = "LR"
s = "LLRR"
```

| Step | Original group | Recorded group | Original length | Recorded length | Result |
| --- | --- | --- | --- | --- | --- |
| 1 | L | LL | 1 | 2 | valid |
| 2 | R | RR | 1 | 2 | valid |

Both groups satisfy the one to two copies rule, so the answer is `YES`.

This example shows that every hit may be duplicated and that the groups must still appear in the same order.

Consider:

```
p = "LR"
s = "LLLR"
```

| Step | Original group | Recorded group | Original length | Recorded length | Result |
| --- | --- | --- | --- | --- | --- |
| 1 | L | LLL | 1 | 3 | invalid |

The first hit would need to create three `L` characters, which is impossible. The algorithm rejects immediately.

This example demonstrates why checking only the character order is insufficient.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Every character in both strings is visited once. |
| Space | O(1) | Only pointers, counters, and the answer state are stored. |

The total length of all strings is processed through a single pass. This fits easily within typical competitive programming limits because the algorithm performs only constant work per character.

## Test Cases

```python
import sys
import io

def solution(data):
    sys.stdin = io.StringIO(data)
    input = sys.stdin.readline

    t = int(input())
    ans = []

    for _ in range(t):
        p = input().strip()
        s = input().strip()

        i = 0
        j = 0
        ok = True

        while i < len(p) and j < len(s):
            if p[i] != s[j]:
                ok = False
                break

            a = i
            while i < len(p) and p[i] == p[a]:
                i += 1

            b = j
            while j < len(s) and s[j] == s[b]:
                j += 1

            x = i - a
            y = j - b

            if y < x or y > 2 * x:
                ok = False
                break

        if i != len(p) or j != len(s):
            ok = False

        ans.append("YES" if ok else "NO")

    return "\n".join(ans)

assert solution("""5
R
RR
LRLR
LRLR
LR
LLLR
LLLLLRL
LLLLRRLL
LLRLRLRRL
LLLRLRRLLRRRL
""") == """YES
YES
NO
NO
YES"""

assert solution("""1
L
L
""") == "YES"

assert solution("""1
L
LLL
""") == "NO"

assert solution("""1
LR
LLRR
""") == "YES"

assert solution("""1
LL
L
""") == "NO"

assert solution("""1
LLLL
LLLLLLLL
""") == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `L` and `L` | `YES` | Minimum valid case |
| `L` and `LLL` | `NO` | Prevents accepting groups that are too long |
| `LR` and `LLRR` | `YES` | Checks duplication of multiple groups |
| `LL` and `L` | `NO` | Prevents accepting missing sounds |
| `LLLL` and `LLLLLLLL` | `YES` | Checks a large single group boundary |

## Edge Cases

For the case:

```
p = "L"
s = "LLL"
```

the algorithm compares the only groups. The original group length is `1` and the recorded group length is `3`. Since `3` is larger than `2 * 1`, the condition fails and the answer is `NO`.

For the case:

```
p = "LR"
s = "LLL"
```

the first group comparison sees `L` against `LLL`. The recorded group has length `3`, which already exceeds the maximum possible expansion of one hit. The algorithm stops without trying to match the remaining `R`, correctly returning `NO`.

For the case:

```
p = "LL"
s = "L"
```

the original group requires two sounds because there are two hits. The recorded group contains only one character, so its length is smaller than the minimum required length. The algorithm rejects the input.

For the case:

```
p = "LLLL"
s = "LLLLLLLL"
```

the algorithm treats the entire strings as one group. The original group length is `4` and the recorded group length is `8`, which is exactly the largest allowed value. The input is accepted.
