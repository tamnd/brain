---
title: "CF 106125H - Hidden Sequence"
description: "We are given three strings consisting of the characters 1, 2, and 3. The hidden object is the real sequence of game winners. If player 1 wins a game, then players 2 and 3 write down 1, but player 1 forgets to record that game."
date: "2026-06-19T19:59:59+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106125
codeforces_index: "H"
codeforces_contest_name: "Delft Algorithm Programming Contest 2025 (DAPC 2025)"
rating: 0
weight: 106125
solve_time_s: 50
verified: true
draft: false
---

[CF 106125H - Hidden Sequence](https://codeforces.com/problemset/problem/106125/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given three strings consisting of the characters `1`, `2`, and `3`.

The hidden object is the real sequence of game winners. If player `1` wins a game, then players `2` and `3` write down `1`, but player `1` forgets to record that game. The same rule applies symmetrically for the other players.

As a result, each input string is the full winner sequence with one specific character removed:

- `s1` is the winner sequence with all `1`s deleted.
- `s2` is the winner sequence with all `2`s deleted.
- `s3` is the winner sequence with all `3`s deleted.

The task is to reconstruct the original winner sequence. The statement guarantees that the answer exists and is unique.

The strings can have length up to `10^5`, so the hidden sequence itself can also have length on that scale. Any algorithm that repeatedly scans the strings, performs expensive substring operations, or backtracks heavily will be too slow. We need something close to linear time.

A subtle aspect is that each occurrence of a winner appears in exactly two of the three strings. For example, if the next winner is `2`, then that `2` appears in `s1` and `s3`, but not in `s2`. Recovering the sequence means identifying which character must come next based on the current unread positions of the three strings.

Consider a small example:

```
s1 = 2
s2 = 1
s3 = 21
```

The answer is:

```
21
```

The first winner is `2`. That `2` appears at the front of `s1` and `s3`. After consuming it from those two strings, the remaining unread characters are `""`, `"1"`, and `"1"`, so the next winner must be `1`.

A common mistake is to try matching characters greedily between arbitrary pairs of strings without respecting order. For example:

```
s1 = 23
s2 = 13
s3 = 12
```

The answer is:

```
123
```

At the beginning, all three strings start with different characters. Looking only at frequencies gives no clue. The key observation is that exactly two strings must agree on the next winner.

Another easy trap appears when the same winner occurs many times consecutively:

```
s1 = 2222
s2 = ""
s3 = 2222
```

This would correspond to the hidden sequence `2222`. Any reconstruction method must correctly consume matching prefixes multiple times in a row rather than trying to alternate between different winners.

## Approaches

A brute-force reconstruction would try to determine the next winner by testing all possibilities.

Suppose we have current positions in the three strings. We could try appending `1`, `2`, or `3` to the answer and check whether the choice is consistent with the strings. After choosing a winner, the two strings that should contain that winner advance by one position.

This approach is correct because every step of the hidden sequence corresponds to one of three possible winners. Unfortunately, exploring possibilities recursively leads to an exponential search tree. Even with pruning, strings of length up to `10^5` make such a strategy impossible.

The crucial observation is that the next winner is actually forced.

Take the first unconsumed character of each string. If the next winner is `1`, then the next unread character of `s2` and `s3` must both be `1`. Similarly, winner `2` would appear next in `s1` and `s3`, and winner `3` would appear next in `s1` and `s2`.

Because the answer is guaranteed to be unique, at every step exactly one character appears as the current character in exactly two strings. That character must be the next winner. After outputting it, we advance the pointers of those two strings and repeat.

Another way to view it is from the ends. The winner of the first game appears first in exactly two lists. Once we identify that winner, we remove it from those two lists. The same argument then applies to the remaining suffixes. This yields a simple pointer-based linear algorithm. The official solution uses exactly this observation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Search | Exponential | Exponential | Too slow |
| Three-Pointer Reconstruction | O(n) | O(1) besides output | Accepted |

## Algorithm Walkthrough

1. Read the three strings `s1`, `s2`, and `s3`.
2. Maintain three indices `i1`, `i2`, and `i3`, initially zero. Each index points to the first unread character of its string.
3. While at least one string still has unread characters, look at the current character of each string whose pointer has not reached the end.
4. Count which character among `1`, `2`, and `3` appears at the front of exactly two strings.
5. That character is the next winner in the hidden sequence. Append it to the answer.
6. Advance the pointers of exactly those two strings whose current character equals the chosen winner.
7. Repeat until all characters from all strings have been consumed.

### Why it works

Every occurrence of a winner appears in exactly two lists and is absent from the winner's own list.

Suppose the next hidden winner is `x`. Then the next unread character in the two lists belonging to the other players must both be `x`, because those lists preserve the original order of winners. The third list does not contain this occurrence at all.

So at any moment, the next winner is precisely the character that appears at the current position of exactly two strings. Consuming that character from those two strings removes one occurrence of the next game from all representations. The remaining suffixes correspond to the remaining games, so the same argument applies inductively. The algorithm reconstructs every winner in the correct order and cannot choose an incorrect character.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    s = [input().strip() for _ in range(3)]

    p = [0, 0, 0]
    ans = []

    while True:
        cur = []

        for k in range(3):
            if p[k] < len(s[k]):
                cur.append((k, s[k][p[k]]))

        if not cur:
            break

        cnt = {'1': 0, '2': 0, '3': 0}

        for _, ch in cur:
            cnt[ch] += 1

        winner = None
        for ch in "123":
            if cnt[ch] == 2:
                winner = ch
                break

        ans.append(winner)

        for k, ch in cur:
            if ch == winner:
                p[k] += 1

    print("".join(ans))

solve()
```

The implementation mirrors the proof directly.

The array `p` stores the current unread position in each string. At every iteration we inspect only the characters currently pointed to, never scanning backward or searching ahead.

The dictionary `cnt` records how many strings currently begin with each possible winner. Since only three symbols exist, this work is constant time.

After identifying the winner, we advance exactly the pointers whose current character equals that winner. This is the critical step. Advancing any other pointer would destroy the ordering information preserved by the lists.

Each pointer moves forward at most the length of its string. No pointer ever moves backward, so the total amount of work is linear.

## Worked Examples

### Example 1

Input:

```
2
1
21
```

Expected output:

```
21
```

| Step | p1 | p2 | p3 | Front chars | Winner | Answer |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 0 | 0 | 2,1,2 | 2 | 2 |
| 2 | 1 | 0 | 1 | -,1,1 | 1 | 21 |

This example shows the fundamental rule. The next winner is always the character appearing at the front of exactly two strings.

### Example 2

Input:

```
23
13
12
```

Expected output:

```
123
```

| Step | p1 | p2 | p3 | Front chars | Winner | Answer |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 0 | 0 | 2,1,1 | 1 | 1 |
| 2 | 0 | 1 | 1 | 2,3,2 | 2 | 12 |
| 3 | 1 | 1 | 2 | 3,3,- | 3 | 123 |

This trace demonstrates that the three strings can all begin with different symbols. The correct choice is still uniquely determined because exactly one symbol appears twice among the current positions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each pointer advances only forward, and every character is processed once |
| Space | O(n) | The answer string has length n, auxiliary memory is O(1) |

If the hidden sequence has length `n`, then the three input strings together also contain only `2n` characters. Every character causes one pointer increment exactly once, so the algorithm easily handles inputs of size `10^5`.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    s = [input().strip() for _ in range(3)]
    p = [0, 0, 0]
    ans = []

    while True:
        cur = []

        for k in range(3):
            if p[k] < len(s[k]):
                cur.append((k, s[k][p[k]]))

        if not cur:
            break

        cnt = {'1': 0, '2': 0, '3': 0}

        for _, ch in cur:
            cnt[ch] += 1

        winner = None
        for ch in "123":
            if cnt[ch] == 2:
                winner = ch
                break

        ans.append(winner)

        for k, ch in cur:
            if ch == winner:
                p[k] += 1

    return "".join(ans)

# provided samples
assert run("2\n1\n21\n") == "21", "sample 1"
assert run("23\n13\n12\n") == "123", "sample 2"
assert run("23232323\n11331133\n12121212\n") == "121323121323", "sample 3"

# custom cases
assert run("2\n12\n1\n") == "12", "minimum nontrivial case"
assert run("22\n1\n221\n") == "221", "repeated winner"
assert run("33\n133\n1\n") == "133", "winner appears consecutively at end"
assert run("232\n13\n122\n") == "1232", "mixed ordering"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 / 12 / 1` | `12` | Small reconstruction |
| `22 / 1 / 221` | `221` | Consecutive identical winners |
| `33 / 133 / 1` | `133` | Long suffix of same winner |
| `232 / 13 / 122` | `1232` | Multiple transitions between winners |

## Edge Cases

Consider:

```
2
1
21
```

Initially the fronts are `(2,1,2)`. The character `2` appears twice, so the algorithm outputs `2` and advances the first and third pointers. The remaining fronts become `(end,1,1)`, forcing winner `1`. The output is `21`, which is correct.

Now consider repeated winners:

```
22
1
221
```

The fronts are `(2,1,2)`, so winner `2` is chosen. After advancing two pointers, the fronts are again `(2,1,2)`. The algorithm correctly chooses another `2`. Only then does `1` become the character appearing twice. The result is `221`.

A more interesting case is:

```
23
13
12
```

All three strings begin with different symbols. A frequency-based reconstruction of the entire strings would fail. Looking only at the current unread positions gives counts `{1:2, 2:1, 3:0}`, forcing winner `1`. Repeating the same logic reconstructs `123` exactly.

These examples illustrate why the local "appears in exactly two current positions" invariant is sufficient to recover the entire sequence uniquely.
