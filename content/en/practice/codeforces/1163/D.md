---
title: "CF 1163D - Mysterious Code"
description: "We are given a string c which represents a partially unreadable code. Some positions in c are readable lowercase letters, and others are asterisks representing unknown characters."
date: "2026-06-12T02:22:06+07:00"
tags: ["codeforces", "competitive-programming", "dp", "strings"]
categories: ["algorithms"]
codeforces_contest: 1163
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 558 (Div. 2)"
rating: 2100
weight: 1163
solve_time_s: 66
verified: true
draft: false
---

[CF 1163D - Mysterious Code](https://codeforces.com/problemset/problem/1163/D)

**Rating:** 2100  
**Tags:** dp, strings  
**Solve time:** 1m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string `c` which represents a partially unreadable code. Some positions in `c` are readable lowercase letters, and others are asterisks representing unknown characters. We are also given two strings: `s`, which we want to appear as many times as possible in the final recovered code, and `t`, which we want to minimize in the same string. The task is to replace the asterisks in `c` with lowercase letters to maximize the difference between the number of occurrences of `s` and `t`.

The string `c` can be up to 1000 characters long, while `s` and `t` are up to 50 characters long. Because `c` is relatively small, it is feasible to perform dynamic programming across the positions of `c`. The main challenge is that each replacement in an asterisk affects multiple possible substring matches of `s` and `t`, and overlapping occurrences must be handled carefully. A naive approach that tries all possible replacements would require checking `26^1000` possibilities in the worst case, which is astronomically large and completely infeasible.

Non-obvious edge cases include situations where `s` and `t` partially overlap, or where every character in `c` is an asterisk. For example, if `c = "***"`, `s = "aa"`, and `t = "aaa"`, a careless greedy approach that maximizes `s` locally might inadvertently create an extra occurrence of `t`, reducing the overall score. Another edge case is when `s` and `t` share common prefixes; maximizing `s` may simultaneously create occurrences of `t` if overlapping is ignored.

## Approaches

A brute-force solution would generate all possible replacements of asterisks and count occurrences of `s` and `t` for each candidate string. This works for extremely small strings, but with `|c|` up to 1000, there could be up to `26^1000` candidate strings, which is completely infeasible.

The key observation is that the problem can be reduced to dynamic programming with string matching automata. We can maintain a DP table `dp[pos][state_s][state_t]` where `pos` is the current position in `c`, `state_s` is the length of the prefix of `s` matched so far, and `state_t` is the length of the prefix of `t` matched so far. For each character in `c` (or each replacement if it is an asterisk), we update the states according to the transition of a finite automaton that tracks how much of `s` and `t` has been matched. When a full `s` is matched, we increase the score by 1, and when a full `t` is matched, we decrease the score by 1.

Constructing the automaton efficiently relies on the Knuth-Morris-Pratt failure function. This allows us to compute in constant time, for a given state and next character, the next state in the automaton. With this approach, we reduce an exponential problem to a DP over `n * |s| * |t|` states with `O(26)` transitions per state, which is feasible for the given constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(26^n * n) | O(n) | Too slow |
| Automaton DP | O(n * | s | * |

## Algorithm Walkthrough

1. Precompute the failure function for `s` and `t` to allow fast transitions between partial matches. For a string `p`, `fail[i]` is the length of the longest prefix of `p` that is a suffix of `p[0:i]`. This lets us know, given a partial match and a next character, what the new match length is.
2. Construct transition tables `next_s[state][char]` and `next_t[state][char]` for `s` and `t` respectively. `next_s[state][char]` tells us the length of the new prefix of `s` matched after seeing `char` given that we have matched `state` characters so far. The same applies for `t`.
3. Initialize a DP table `dp[pos][state_s][state_t]` filled with negative infinity except `dp[0][0][0] = 0`. Here `pos` is the index in `c`, `state_s` is how many characters of `s` we have matched ending at `pos-1`, and `state_t` is how many characters of `t` we have matched ending at `pos-1`.
4. Iterate over positions `pos` from 0 to `len(c)-1`. For each `(state_s, state_t)`, try all possible next characters. If `c[pos]` is a known letter, only that letter is considered; otherwise, all 26 letters are considered.
5. For each character `ch`, compute the next states `new_s = next_s[state_s][ch]` and `new_t = next_t[state_t][ch]`. Update the DP: `dp[pos+1][new_s][new_t] = max(dp[pos+1][new_s][new_t], dp[pos][state_s][state_t] + score)`, where `score` is 1 if `new_s` reached full `|s|` (subtract `|s|` from `new_s` after counting) and -1 if `new_t` reached full `|t|` (subtract `|t|` from `new_t` after counting).
6. After filling the DP table, the answer is the maximum value over all `dp[len(c)][*][*]`.

Why it works: The DP maintains the invariant that `dp[pos][state_s][state_t]` is the maximum achievable `f(c', s) - f(c', t)` using the first `pos` characters of `c` and ending with partial matches `state_s` and `state_t`. The automaton transitions ensure that overlapping occurrences are correctly handled.

## Python Solution

```python
import sys
input = sys.stdin.readline

def compute_kmp_transition(pattern):
    m = len(pattern)
    fail = [0] * m
    for i in range(1, m):
        j = fail[i-1]
        while j > 0 and pattern[i] != pattern[j]:
            j = fail[j-1]
        if pattern[i] == pattern[j]:
            j += 1
        fail[i] = j
    nxt = [[0]*26 for _ in range(m+1)]
    for state in range(m+1):
        for c in range(26):
            if state < m and ord(pattern[state]) - ord('a') == c:
                nxt[state][c] = state + 1
            else:
                j = state
                while j > 0 and (j == m or ord(pattern[j]) - ord('a') != c):
                    j = fail[j-1]
                if j < m and ord(pattern[j]) - ord('a') == c:
                    nxt[state][c] = j + 1
                else:
                    nxt[state][c] = 0
    return nxt

def main():
    c = input().strip()
    s = input().strip()
    t = input().strip()
    n = len(c)
    ns = len(s)
    nt = len(t)
    nxt_s = compute_kmp_transition(s)
    nxt_t = compute_kmp_transition(t)
    INF = float('-inf')
    dp = [[ [INF]*(nt+1) for _ in range(ns+1)] for _ in range(n+1)]
    dp[0][0][0] = 0
    for i in range(n):
        for ps in range(ns+1):
            for pt in range(nt+1):
                if dp[i][ps][pt] == INF:
                    continue
                chars = [ord(c[i])-ord('a')] if c[i] != '*' else list(range(26))
                for ch in chars:
                    ns_state = nxt_s[ps][ch]
                    nt_state = nxt_t[pt][ch]
                    score = 0
                    if ns_state == ns:
                        score += 1
                        ns_state = nxt_s[ns_state-1][ch]
                    if nt_state == nt:
                        score -= 1
                        nt_state = nxt_t[nt_state-1][ch]
                    dp[i+1][ns_state][nt_state] = max(dp[i+1][ns_state][nt_state], dp[i][ps][pt] + score)
    result = max(dp[n][ps][pt] for ps in range(ns+1) for pt in range(nt+1))
    print(result)

if __name__ == "__main__":
    main()
```

The `compute_kmp_transition` function precomputes the next state transitions for each prefix of the pattern for each possible character. The DP table `dp[i][ps][pt]` tracks the best achievable score for each combination of partial matches. When processing an asterisk, all 26 letters are tried, whereas a known character forces a single transition. Updating the DP with `max` ensures we always keep the optimal choice.

## Worked Examples

For the input:

```
*****
katie
shiro
```

| i | ps | pt | dp[i][ps][pt] | ch tried | ns_state | nt_state | new dp |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 |  |  |  |  |  |  |  |
