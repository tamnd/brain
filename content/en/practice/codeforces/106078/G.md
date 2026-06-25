---
title: "CF 106078G - Saturn"
description: "We have a target string t and a list of recorded data strings. We may choose any subset of the recorded strings, but their original order cannot change. The chosen strings are concatenated, and the goal is to make the target string appear as a substring as many times as possible."
date: "2026-06-25T12:09:16+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106078
codeforces_index: "G"
codeforces_contest_name: "UTPC Contest 9-17-25 Div. 1 (Advanced)"
rating: 0
weight: 106078
solve_time_s: 42
verified: true
draft: false
---

[CF 106078G - Saturn](https://codeforces.com/problemset/problem/106078/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a target string `t` and a list of recorded data strings. We may choose any subset of the recorded strings, but their original order cannot change. The chosen strings are concatenated, and the goal is to make the target string appear as a substring as many times as possible. Overlapping occurrences count, so a match ending at one position can share characters with another match.

The input consists of a short target pattern and up to 1000 data points. Each data point is a string of length at most 100. The output is the maximum number of times the target can occur after choosing the best subset.

The main constraint that shapes the solution is the small target length. The target has length at most 20, while the total amount of data can reach around 100000 characters. A solution that tries every subset of strings is impossible because there are exponentially many choices. Even checking every possible concatenation boundary would be too expensive. We need to compress the information we carry between chosen strings.

The only part of the already built concatenation that matters for future matches is the suffix that could become the beginning of a future occurrence of `t`. For example, if the target is `abab`, after reading some text, we only need to know whether the current suffix is `a`, `ab`, or `aba`. The entire previous concatenation is irrelevant.

A careless implementation can fail on overlapping matches. For example, if the target is `aaa` and the chosen text is `aaaa`, the correct output is `2`, because the occurrences are positions 1 to 3 and 2 to 4. A solution that jumps past the matched characters after finding an occurrence would only count `1`.

Another tricky case is when an occurrence crosses the boundary between two selected strings. Consider target `abc` and data strings `ab` and `c`. Choosing both strings gives the concatenation `abc`, so the answer is `1`. A method that counts occurrences inside each string separately would incorrectly output `0`.

A final edge case is choosing no string. If every data string is useless, the answer must remain `0`. For example, with target `xyz` and one data string `aaaa`, the correct output is `0`.

## Approaches

A direct approach would be to try every possible subset of the data points. For each subset, we concatenate the chosen strings and count the occurrences of `t`. This is correct because every valid final document corresponds to exactly one subset. The problem is the number of subsets, which can be `2^1000`, so this approach is far beyond what we can handle.

The key observation is that the future does not depend on the full concatenation. When we process strings from left to right, we only need the automaton state describing the longest suffix of the current text that is also a prefix of `t`. This is the same state information used by prefix-function based string matching.

Since the target length is at most 20, there are only a small number of possible states. For every data string, we can precompute what happens if we append it while starting from each possible state. The transition tells us the new state and how many new occurrences of `t` are created.

The problem then becomes a simple dynamic programming process. While scanning the data points, `dp[state]` stores the maximum number of matches achievable after considering the processed strings and ending in that automaton state. For each new string, we either skip it or take it and apply its precomputed transition.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n * total length) | O(total length) | Too slow |
| Optimal | O(n * | t | * ( |

## Algorithm Walkthrough

1. Build a prefix-function based automaton for the target string. For every possible state, store the next state after reading a character and whether that character completes an occurrence. The state represents how many characters of the target currently match a suffix of what we have read.
2. For every data string, simulate adding it to the current text starting from every possible state. Store the resulting state and the number of occurrences created. This works because the target is short, so precomputing all transitions is cheap.
3. Initialize the dynamic programming array with state `0` having value `0`. This represents an empty chosen concatenation.
4. Process the data strings in order. For each string, first copy the current DP values as the option where we skip this string.
5. For every current automaton state, try taking the current string. Move to the precomputed next state and add the number of matches produced by this string. Keep the best value for that state.
6. After all strings are processed, the answer is the maximum value among all automaton states because the final suffix state does not matter.

Why it works: the DP invariant is that after processing the first `i` data strings, `dp[s]` is the best possible number of occurrences among all choices of those strings that leave the matcher in state `s`. Skipping a string keeps the same state and score, while taking a string uses the exact effect of appending it. Since every possible choice is either taking or skipping the next string, all valid concatenations are considered. The automaton state contains exactly the information needed for future extensions, so no necessary information is lost.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    target = input().strip()
    n = int(input())
    strings = [input().strip() for _ in range(n)]

    m = len(target)

    pi = [0] * m
    for i in range(1, m):
        j = pi[i - 1]
        while j > 0 and target[i] != target[j]:
            j = pi[j - 1]
        if target[i] == target[j]:
            j += 1
        pi[i] = j

    nxt = [[0] * 26 for _ in range(m)]
    add = [[0] * 26 for _ in range(m)]

    for state in range(m):
        for c in range(26):
            ch = chr(ord('a') + c)
            j = state
            while j > 0 and target[j] != ch:
                j = pi[j - 1]
            if target[j] == ch:
                j += 1
            if j == m:
                add[state][c] = 1
                j = pi[m - 1]
            nxt[state][c] = j

    transitions = []
    for s in strings:
        cur = []
        for start in range(m):
            state = start
            score = 0
            for ch in s:
                idx = ord(ch) - ord('a')
                score += add[state][idx]
                state = nxt[state][idx]
            cur.append((state, score))
        transitions.append(cur)

    dp = [-10**9] * m
    dp[0] = 0

    for trans in transitions:
        ndp = dp[:]
        for state in range(m):
            if dp[state] < 0:
                continue
            to, gain = trans[state]
            if dp[state] + gain > ndp[to]:
                ndp[to] = dp[state] + gain
        dp = ndp

    print(max(dp))

if __name__ == "__main__":
    solve()
```

The prefix function builds the failure links needed to continue matching after a mismatch. This avoids rescanning the whole target whenever a character does not fit.

The `nxt` and `add` tables describe the automaton. `nxt[state][character]` is the suffix state after reading the character, while `add[state][character]` tells whether that character completes an occurrence. When an occurrence is found, the state falls back to the longest proper suffix that is also a prefix, which is what allows overlaps.

The transition table for each data string is computed once. The simulation uses the automaton instead of repeatedly searching the target, so even long data strings are processed quickly.

The DP update copies the current array first because skipping the string must remain possible. Then every state tries taking the string and updates the resulting state. There is no issue with integer overflow in Python, but the negative initial value represents impossible states.

## Worked Examples

For the first sample:

```
target = lol
strings:
olo
lol
olo
```

The DP evolution is:

| Data processed | Best states after processing | Maximum score |
| --- | --- | --- |
| none | state 0: 0 | 0 |
| olo | no full match yet | 0 |
| lol | taking it creates one match | 1 |
| olo | crossing the previous boundary creates more matches | 3 |

The trace demonstrates why keeping the suffix state matters. The last string does not contain `lol` alone, but it completes matches because of the previous chosen text.

For the second sample:

```
target = ababac
strings:
abab
aba
abac
```

| Data processed | Best choice | Score |
| --- | --- | --- |
| none | empty | 0 |
| abab | take first string | 0 |
| aba | skip or take, no completed target | 0 |
| abac | combine first and last | 1 |

This shows the DP handles choices between taking and skipping strings while preserving the original order.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n * m * (m + L)) | Each of the `n` strings is simulated from every target state, where `m` is the target length and `L` is the string length. |
| Space | O(m) | The DP only stores one value per automaton state. |

Here `m` is at most 20, so the state space is tiny. The total processed text length is at most around 100000 characters, making this approach easily fast enough.

## Test Cases

```python
import sys
import io

def solve(inp):
    old = sys.stdin
    sys.stdin = io.StringIO(inp)

    target = sys.stdin.readline().strip()
    n = int(sys.stdin.readline())
    strings = [sys.stdin.readline().strip() for _ in range(n)]

    m = len(target)

    pi = [0] * m
    for i in range(1, m):
        j = pi[i - 1]
        while j > 0 and target[i] != target[j]:
            j = pi[j - 1]
        if target[i] == target[j]:
            j += 1
        pi[i] = j

    nxt = [[0] * 26 for _ in range(m)]
    add = [[0] * 26 for _ in range(m)]

    for s in range(m):
        for c in range(26):
            ch = chr(97 + c)
            j = s
            while j > 0 and target[j] != ch:
                j = pi[j - 1]
            if target[j] == ch:
                j += 1
            if j == m:
                add[s][c] = 1
                j = pi[m - 1]
            nxt[s][c] = j

    dp = [0] + [-10**9] * (m - 1)

    for text in strings:
        trans = []
        for start in range(m):
            state = start
            score = 0
            for ch in text:
                x = ord(ch) - 97
                score += add[state][x]
                state = nxt[state][x]
            trans.append((state, score))

        ndp = dp[:]
        for i in range(m):
            if dp[i] >= 0:
                j, gain = trans[i]
                ndp[j] = max(ndp[j], dp[i] + gain)
        dp = ndp

    sys.stdin = old
    return str(max(dp)) + "\n"

assert solve("""lol
3
olo
lol
olo
""") == "3\n"

assert solve("""ababac
3
abab
aba
abac
""") == "1\n"

assert solve("""aaa
1
aaaa
""") == "2\n"

assert solve("""abc
2
ab
c
""") == "1\n"

assert solve("""xyz
1
aaaa
""") == "0\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `lol` with three strings | `3` | Overlapping and boundary matches |
| `ababac` sample | `1` | Choosing a subset in order |
| `aaa` and `aaaa` | `2` | Overlapping occurrences |
| `abc` with `ab`, `c` | `1` | Matches across string boundaries |
| `xyz` with `aaaa` | `0` | No useful data points |

## Edge Cases

For target `aaa` and the string `aaaa`, the automaton starts in state `0`. After reading the first three characters, it finds one occurrence and falls back to state `2`, representing the suffix `aa`. Reading the fourth character creates another occurrence. The algorithm outputs `2` because it never discards the suffix after a match.

For target `abc` and strings `ab` and `c`, the first chosen string leaves the automaton in state `2`, meaning the current suffix is `ab`. When the second string begins with `c`, the automaton immediately completes the pattern and adds one to the score. This handles matches that span multiple selected strings.

For target `xyz` and string `aaaa`, every transition stays away from a completed match. The DP keeps the best reachable score as `0`, which represents choosing nothing useful. The algorithm never forces the selection of a string, so impossible contributions do not affect the result.
