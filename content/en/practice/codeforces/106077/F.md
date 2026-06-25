---
title: "CF 106077F - Saturn"
description: "We are given a target string t that represents the claim Shani wants to prove. She has a sequence of recorded data strings. She may choose any subset of these strings, but the chosen strings must keep their original order when concatenated."
date: "2026-06-25T12:11:20+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106077
codeforces_index: "F"
codeforces_contest_name: "UTPC Contest 9-17-25 Div. 2 (Beginner)"
rating: 0
weight: 106077
solve_time_s: 46
verified: true
draft: false
---

[CF 106077F - Saturn](https://codeforces.com/problemset/problem/106077/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a target string `t` that represents the claim Shani wants to prove. She has a sequence of recorded data strings. She may choose any subset of these strings, but the chosen strings must keep their original order when concatenated. The committee then searches for every occurrence of `t` inside the final concatenated text, including occurrences that overlap, and Shani wants to maximize that count.

The input contains the target pattern, followed by the number of available strings and the strings themselves. The output is the largest possible number of times the target pattern can appear after choosing the best subsequence of strings.

The key constraints shape the solution. There are at most 1000 data strings, each of length at most 100, while the target length is at most 20. A solution around `O(n^2)` might pass for the number of strings, but the actual challenge is handling the effect of concatenating strings. We need to avoid storing the whole previous concatenation, because it can reach length 100000. The small target length suggests that only information related to the target pattern can matter.

The edge cases come from matches crossing the boundaries of chosen strings. A solution that counts matches inside each string independently will fail. For example:

```
Input
abc
2
a
bc
```

The correct output is:

```
1
```

Choosing both strings creates `abc`, where the match uses the end of the first string and the beginning of the second. A method that only scans each string separately would see no occurrence.

Another tricky case is overlapping matches. Consider:

```
Input
aa
1
aaa
```

The correct output is:

```
2
```

The matches are positions 1 to 2 and 2 to 3. A careless implementation that moves past the matched text instead of allowing overlaps would only count one.

## Approaches

The straightforward approach is to try every possible subset of strings, concatenate the chosen ones, and count occurrences of the pattern. This is correct because every valid final text corresponds to exactly one subset. However, there are up to 1000 strings, so there are `2^1000` possible subsets. Even generating the candidates is impossible.

The next observation is that the future does not depend on the entire concatenation. When we append another string, the only previous characters that can affect a new occurrence of `t` are the suffix of the current text that could become a prefix of `t`. This is exactly the information maintained by a string matching automaton.

We can build a KMP automaton for `t`. A state represents the length of the longest suffix of the processed text that is also a prefix of `t`. Whenever we append a character, the automaton moves to a new state and tells us whether a full match was created. Because the pattern length is at most 20, the number of states is tiny.

For every data string, we can precompute its effect on every automaton state. If we include the string, we gain some number of matches and move to another state. If we skip it, the state and score stay the same. This turns the problem into a dynamic program over the strings and automaton states.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n * total length) | O(total length) | Too slow |
| Optimal | O(n * | t | * total string length) |

## Algorithm Walkthrough

1. Build the KMP prefix function for the target string. The prefix function allows us to quickly find the next automaton state after reading a character.

The state only stores how much of the target has already been matched as a suffix. This is enough because any future occurrence can only depend on this suffix information.
2. Create a transition table for every data string. For every possible starting KMP state, simulate reading the whole string and record the ending state and how many times the target appears during the simulation.

Doing this once prevents us from repeatedly scanning the same string during the dynamic programming.
3. Initialize a dynamic programming array. `dp[state]` stores the maximum number of matches achievable after processing some prefix of the data list and ending in that automaton state.

Before choosing any strings, the automaton is in state zero with score zero.
4. Process the data strings one by one. For each string, copy the current DP values because skipping the string is always allowed. Then try taking the string from every previous state, applying the precomputed transition and adding the gained matches.

This step considers exactly the two choices for each string: ignore it or append it.
5. The answer is the maximum value among all final states. The ending automaton state does not matter because no more characters are added.

The invariant is that after processing the first `i` strings, every `dp[state]` represents the best possible score among all choices from those strings that leave the automaton in that state. Skipping preserves the existing valid possibilities, while taking a string considers every possible previous state and applies the exact effect of appending it. Since these are the only two possible actions, the invariant holds for every processed string.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = input().strip()
    n = int(input())
    s = [input().strip() for _ in range(n)]

    m = len(t)

    pi = [0] * m
    for i in range(1, m):
        j = pi[i - 1]
        while j > 0 and t[i] != t[j]:
            j = pi[j - 1]
        if t[i] == t[j]:
            j += 1
        pi[i] = j

    def advance(state, ch):
        while state > 0 and t[state] != ch:
            state = pi[state - 1]
        if t[state] == ch:
            state += 1
        if state == m:
            return pi[m - 1], 1
        return state, 0

    trans = []
    for word in s:
        cur = []
        for start in range(m):
            state = start
            gain = 0
            for ch in word:
                state, add = advance(state, ch)
                gain += add
            cur.append((state, gain))
        trans.append(cur)

    dp = [-10**9] * m
    dp[0] = 0

    for word_id in range(n):
        ndp = dp[:]
        for state in range(m):
            if dp[state] < 0:
                continue
            nxt, gain = trans[word_id][state]
            if dp[state] + gain > ndp[nxt]:
                ndp[nxt] = dp[state] + gain
        dp = ndp

    print(max(dp))

if __name__ == "__main__":
    solve()
```

The prefix function construction is the usual KMP preprocessing. It lets the automaton recover from mismatches without rescanning the already processed text.

The `advance` function processes one character. If a full match is completed, the automaton returns to the longest border of the pattern instead of state zero. This is what allows overlapping matches to be counted correctly.

The transition table stores the effect of every string from every possible state. The number of states is at most 20, so precomputing it is cheap compared with repeatedly scanning strings inside the DP.

The DP update uses a copied array because every string can be skipped. Taking a string reads from the old array and writes into the new one, avoiding accidental reuse of the same string multiple times. The final maximum is used because any suffix state is acceptable.

## Worked Examples

For the first sample:

```
t = lol

strings:
olo
lol
olo
```

The trace is:

| Processed strings | Current best states | Maximum score |
| --- | --- | --- |
| none | state 0: 0 | 0 |
| olo | state 3: 1 | 1 |
| olo, lol | state 3: 2 | 2 |
| all three | state 3: 3 | 3 |

The automaton keeps enough suffix information to recognize the `lol` formed when strings touch each other.

For the second sample:

```
t = ababac

strings:
abab
aba
abac
```

The trace is:

| Processed strings | Action | Score |
| --- | --- | --- |
| none | empty text | 0 |
| abab | take first string | 0 |
| abab + aba | take second string | 0 |
| abab + aba + abac | take third string | 1 |

The best choice is to join the first and third strings. The table shows that the DP does not greedily take strings, it keeps all possible automaton states.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n * m * L) | Each string is simulated from every KMP state, where `m` is the pattern length and `L` is the maximum string length. |
| Space | O(m^2 + m) | The transition table has `n * m` entries in the implementation, and the DP itself only needs `m` states. |

With `m <= 20`, the automaton is very small. Even though the number of strings is 1000, each transition simulation touches only about 2000 characters, which is easily within the limit.

## Test Cases

```python
import sys, io

def solve_case(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = input().strip()
    n = int(input())
    s = [input().strip() for _ in range(n)]

    m = len(t)

    pi = [0] * m
    for i in range(1, m):
        j = pi[i - 1]
        while j > 0 and t[i] != t[j]:
            j = pi[j - 1]
        if t[i] == t[j]:
            j += 1
        pi[i] = j

    def advance(state, ch):
        while state > 0 and t[state] != ch:
            state = pi[state - 1]
        if t[state] == ch:
            state += 1
        if state == m:
            return pi[m - 1], 1
        return state, 0

    trans = []
    for word in s:
        cur = []
        for start in range(m):
            state = start
            gain = 0
            for ch in word:
                state, add = advance(state, ch)
                gain += add
            cur.append((state, gain))
        trans.append(cur)

    dp = [-10**9] * m
    dp[0] = 0

    for i in range(n):
        ndp = dp[:]
        for st in range(m):
            nxt, gain = trans[i][st]
            ndp[nxt] = max(ndp[nxt], dp[st] + gain)
        dp = ndp

    return str(max(dp)) + "\n"

assert solve_case("""lol
3
olo
lol
olo
""") == "3\n"

assert solve_case("""ababac
3
abab
aba
abac
""") == "1\n"

assert solve_case("""abc
2
a
bc
""") == "1\n"

assert solve_case("""aa
1
aaa
""") == "2\n"

assert solve_case("""x
4
x
x
a
x
""") == "3\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `abc` with `a`, `bc` | `1` | Matches crossing string boundaries |
| `aa` with `aaa` | `2` | Overlapping matches |
| `x` with several strings | `3` | Repeated one character matches |
| Sample cases | Sample outputs | General DP correctness |

## Edge Cases

For the boundary crossing case:

```
abc
2
a
bc
```

The DP first processes `a`, leaving the automaton in the state that represents matching the prefix `a`. When `bc` is taken, the automaton continues from that state and completes `abc`, adding one match.

For overlapping matches:

```
aa
1
aaa
```

After the first `a`, the automaton remembers one matched character. The second `a` completes a match, but instead of resetting completely it falls back to the border of `aa`, which is another `a`. The third `a` creates the second match.

For repeated identical strings:

```
x
4
x
x
a
x
```

The DP can choose the first, second, and fourth strings. Each chosen string adds one occurrence. The skipped string does not affect the automaton state, so the final answer is three.
