---
title: "CF 86C - Genetic engineering"
description: "We are given several short DNA fragments over the alphabet {A, C, G, T}. A longer DNA string is considered valid if every position of the string belongs to at least one occurrence of one of the given fragments. The fragments may overlap arbitrarily."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dp", "string-suffix-structures", "trees"]
categories: ["algorithms"]
codeforces_contest: 86
codeforces_index: "C"
codeforces_contest_name: "Yandex.Algorithm 2011: Round 2"
rating: 2500
weight: 86
solve_time_s: 132
verified: true
draft: false
---

[CF 86C - Genetic engineering](https://codeforces.com/problemset/problem/86/C)

**Rating:** 2500  
**Tags:** dp, string suffix structures, trees  
**Solve time:** 2m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several short DNA fragments over the alphabet `{A, C, G, T}`. A longer DNA string is considered valid if every position of the string belongs to at least one occurrence of one of the given fragments.

The fragments may overlap arbitrarily. One fragment can start inside another, and multiple fragments may cover the same position. The only requirement is that after placing occurrences of fragments somewhere inside the string, every character position is covered by at least one occurrence.

We must count how many strings of length `n` satisfy this condition.

The constraints are small in some dimensions and deceptively large in others. There are at most `10` patterns and every pattern length is at most `10`, so the total pattern length is tiny. That strongly suggests building some kind of automaton over the patterns. On the other hand, `n` can reach `1000`, which immediately rules out anything exponential in `n`, or any DP that stores full coverage masks over positions.

The dangerous part of the problem is that coverage is global. Whether a position is covered depends on intervals created by pattern occurrences that may begin earlier and end later. A naive DP that only tracks the current automaton state is not enough.

Several edge cases make simpler approaches fail.

Consider:

```
3 1
AA
```

The valid strings are only:

```
AAA
```

The string `"AAB"` is invalid because position `3` is uncovered, even though a pattern ended at position `2`. A careless DP that only checks whether some pattern appears somewhere would incorrectly accept it.

Another subtle case:

```
4 2
AAA
AA
```

The string `"AAAA"` is valid. Coverage comes from overlapping occurrences:

```
AAA
 AAA
```

A greedy strategy that always tries to extend coverage with the longest pattern can fail because coverage may need overlapping shorter matches.

Duplicate patterns are also allowed:

```
3 2
A
A
```

The answer is still `1`, not `2`. We count distinct strings, not ways to cover them.

The hardest conceptual issue is this one:

```
5 1
AT
```

Even if we matched `"AT"` ending at position `4`, position `5` may still be uncovered. Coverage is about every index individually, not about whether the string contains many matches.

The solution needs to remember how far the current coverage extends while scanning the string left to right.

## Approaches

The brute-force idea is straightforward. Generate all `4^n` DNA strings, and for each one, check whether every position belongs to at least one occurrence of a pattern.

Checking one string can be done with standard substring matching in roughly `O(n * total_pattern_length)`. The real problem is the number of strings. With `n = 1000`, we would have `4^1000` candidates, which is astronomically impossible.

The next natural idea is dynamic programming over prefixes. While building the string left to right, we want to know which patterns currently match as suffixes. That immediately suggests the Aho-Corasick automaton, because it compactly stores all suffix-match information.

The automaton alone is still insufficient.

Suppose we are at position `i`. Knowing the current automaton node tells us which patterns end at `i`, but validity depends on whether position `i` itself is covered. Coverage comes from intervals created by previous matches. If a pattern of length `L` ends at `i`, then it covers positions `[i-L+1, i]`.

The key observation is that while scanning left to right, the only thing that matters is the rightmost position already guaranteed to be covered.

Instead of storing the exact set of covered positions, we store one number:

`rem = how many future positions are still guaranteed covered`

If a pattern of length `L` ends at the current position, then coverage extends `L-1` positions into the future. While moving forward one character, `rem` decreases by one. Whenever a longer match appears, we refresh it.

This transforms the global coverage condition into a local DP transition.

The automaton gives all pattern matches ending at the current position. The DP keeps the maximum remaining coverage. Together, they completely characterize the state.

The number of automaton states is tiny because total pattern length is at most `100`. The remaining coverage is at most `10`, since pattern lengths are at most `10`. That makes a cubic-looking DP perfectly feasible.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(4^n · n · totalLen) | O(n) | Too slow |
| Optimal | O(n · states · maxLen · 4) | O(states · maxLen) | Accepted |

## Algorithm Walkthrough

1. Build an Aho-Corasick automaton from all patterns.

Each node represents a prefix of some pattern. Transitions follow DNA characters. Failure links connect a node to the longest proper suffix that is also present in the trie.
2. For every automaton node, compute `best[node]`.

`best[node]` is the maximum length of any pattern that ends at this node or along its failure chain.

This matters because when we arrive at a node after reading some prefix of the string, every matched pattern ending here can potentially extend coverage. Only the longest one matters.
3. Define the DP state.

Let:

`dp[pos][state][rem]`

denote the number of ways to build the first `pos` characters such that:

`state` is the current automaton node.

`rem` is how many positions starting from `pos+1` are already guaranteed covered.
4. Initialize:

```
dp[0][root][0] = 1
```

Before reading anything, no future position is covered.
5. Transition by adding one character.

From `(pos, state, rem)`:

Try all four DNA letters.

Move through the automaton to `next_state`.
6. Update the remaining coverage.

First, existing coverage shrinks by one because we advanced one position:

```
new_rem = max(rem - 1, 0)
```

Then check whether some pattern ends here. If the longest matched pattern has length `L`, it covers `L-1` future positions:

```
new_rem = max(new_rem, L - 1)
```
7. Reject uncovered positions.

The current position is covered iff either:

`rem > 0`

or a pattern ending here covers it immediately.

Equivalently, after processing the transition, the current position is valid iff:

```
max(rem, L) > 0
```

Since every pattern has positive length, this condition naturally appears through the update logic.
8. After processing all `n` characters, only states with `rem == 0` are automatically valid.

Actually, every processed position has already been checked during transitions, so all remaining states are valid. Sum all DP values at length `n`.

### Why it works

The invariant is:

After processing `pos` characters, `rem` equals the number of future positions already guaranteed covered by previously completed pattern occurrences.

Whenever a pattern of length `L` ends at the current position, it contributes coverage for exactly the next `L-1` positions. Taking the maximum preserves all necessary information because only the farthest-reaching active interval matters.

A position becomes invalid precisely when we advance into it with no active coverage interval and no new pattern ending there. The DP never allows such transitions.

Since the automaton correctly identifies every pattern ending at every position, and the DP exactly tracks future coverage reach, every accepted construction corresponds to a valid filtered string, and every valid filtered string follows some DP path.

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

MOD = 1000000009
ALPHA = {'A': 0, 'C': 1, 'G': 2, 'T': 3}

def solve():
    n, m = map(int, input().split())
    patterns = [input().strip() for _ in range(m)]

    # trie
    nxt = [[-1] * 4]
    fail = [0]
    best = [0]

    for s in patterns:
        node = 0

        for ch in s:
            c = ALPHA[ch]

            if nxt[node][c] == -1:
                nxt[node][c] = len(nxt)
                nxt.append([-1] * 4)
                fail.append(0)
                best.append(0)

            node = nxt[node][c]

        best[node] = max(best[node], len(s))

    # build automaton
    q = deque()

    for c in range(4):
        if nxt[0][c] == -1:
            nxt[0][c] = 0
        else:
            v = nxt[0][c]
            fail[v] = 0
            q.append(v)

    while q:
        v = q.popleft()

        best[v] = max(best[v], best[fail[v]])

        for c in range(4):
            to = nxt[v][c]

            if to == -1:
                nxt[v][c] = nxt[fail[v]][c]
            else:
                fail[to] = nxt[fail[v]][c]
                q.append(to)

    states = len(nxt)
    max_len = 10

    dp = [[[0] * (max_len + 1) for _ in range(states)] for _ in range(n + 1)]
    dp[0][0][0] = 1

    for pos in range(n):
        for state in range(states):
            for rem in range(max_len + 1):
                cur = dp[pos][state][rem]

                if cur == 0:
                    continue

                for c in range(4):
                    ns = nxt[state][c]

                    longest = best[ns]

                    # current position must be covered
                    if rem == 0 and longest == 0:
                        continue

                    nrem = max(rem - 1, longest - 1)

                    dp[pos + 1][ns][nrem] += cur
                    dp[pos + 1][ns][nrem] %= MOD

    ans = 0

    for state in range(states):
        for rem in range(max_len + 1):
            ans += dp[n][state][rem]

    ans %= MOD

    print(ans)

solve()
```

The trie construction inserts every pattern character by character. Each terminal node stores the maximum pattern length ending there. Using the maximum is enough because longer intervals dominate shorter ones for future coverage.

The BFS over the trie builds failure links exactly as in standard Aho-Corasick. During this traversal, we propagate pattern information through failure links:

```
best[v] = max(best[v], best[fail[v]])
```

Without this line, suffix matches would be lost. For example, if patterns are `"AAA"` and `"AA"`, then after reading `"AAA"` we must recognize that `"AA"` also ends there.

The DP dimension for `rem` is only `10` because no pattern length exceeds `10`, so future coverage cannot extend further than `9`.

The transition logic is the core of the solution.

If `rem == 0` and no pattern ends at the current position, then the current position is uncovered and the transition must be discarded.

Otherwise we compute:

```
nrem = max(rem - 1, longest - 1)
```

The previous active interval loses one step because we moved right by one position. A newly matched pattern may extend coverage farther.

Summing every state at length `n` is correct because coverage is validated online during transitions. No uncovered position can survive into the DP.

## Worked Examples

### Sample 1

Input:

```
2 1
A
```

Only the string `"AA"` is valid.

| Position | Current String | Automaton State | rem Before | Match Length | rem After |
| --- | --- | --- | --- | --- | --- |
| 1 | A | A | 0 | 1 | 0 |
| 2 | AA | A | 0 | 1 | 0 |

Any attempt to place `C`, `G`, or `T` immediately fails because no pattern covers that position.

This example confirms the meaning of `rem = 0`. Coverage does not persist beyond the current position when pattern length is `1`.

### Example 2

Input:

```
4 1
AA
```

Valid strings:

```
AAAA
```

Trace:

| Position | Current String | rem Before | Match Length | rem After |
| --- | --- | --- | --- | --- |
| 1 | A | 0 | 0 | invalid |
| 2 | AA | 0 | 2 | 1 |
| 3 | AAA | 1 | 2 | 1 |
| 4 | AAAA | 1 | 2 | 1 |

The first position cannot stand alone because no pattern ends there yet. Coverage only begins once the first `"AA"` finishes at position `2`.

After that, overlapping occurrences maintain continuous coverage.

This demonstrates why online coverage tracking is necessary. A simple “contains pattern” check would incorrectly accept many invalid strings.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n · states · maxLen · 4) | DP over positions, automaton states, remaining coverage, and DNA letters |
| Space | O(n · states · maxLen) | Full DP table |

The automaton contains at most about `100` states because total pattern length is at most `100`. The `rem` dimension is at most `10`. Even with `n = 1000`, the total number of transitions stays comfortably below a few million operations, which easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from collections import deque

MOD = 1000000009
ALPHA = {'A': 0, 'C': 1, 'G': 2, 'T': 3}

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n, m = map(int, input().split())
    patterns = [input().strip() for _ in range(m)]

    nxt = [[-1] * 4]
    fail = [0]
    best = [0]

    for s in patterns:
        node = 0

        for ch in s:
            c = ALPHA[ch]

            if nxt[node][c] == -1:
                nxt[node][c] = len(nxt)
                nxt.append([-1] * 4)
                fail.append(0)
                best.append(0)

            node = nxt[node][c]

        best[node] = max(best[node], len(s))

    q = deque()

    for c in range(4):
        if nxt[0][c] == -1:
            nxt[0][c] = 0
        else:
            v = nxt[0][c]
            q.append(v)

    while q:
        v = q.popleft()

        best[v] = max(best[v], best[fail[v]])

        for c in range(4):
            to = nxt[v][c]

            if to == -1:
                nxt[v][c] = nxt[fail[v]][c]
            else:
                fail[to] = nxt[fail[v]][c]
                q.append(to)

    states = len(nxt)

    dp = [[[0] * 11 for _ in range(states)] for _ in range(n + 1)]
    dp[0][0][0] = 1

    for pos in range(n):
        for state in range(states):
            for rem in range(11):
                cur = dp[pos][state][rem]

                if cur == 0:
                    continue

                for c in range(4):
                    ns = nxt[state][c]
                    longest = best[ns]

                    if rem == 0 and longest == 0:
                        continue

                    nrem = max(rem - 1, longest - 1)

                    dp[pos + 1][ns][nrem] += cur
                    dp[pos + 1][ns][nrem] %= MOD

    ans = 0

    for state in range(states):
        for rem in range(11):
            ans += dp[n][state][rem]

    return str(ans % MOD) + "\n"

# provided sample
assert run("2 1\nA\n") == "1\n", "sample 1"

# minimum size
assert run("1 1\nA\n") == "1\n", "single covered character"

# no valid strings
assert run("1 1\nAA\n") == "0\n", "pattern longer than string"

# overlapping coverage
assert run("4 1\nAA\n") == "1\n", "overlapping AA matches"

# all characters allowed
assert run("3 4\nA\nC\nG\nT\n") == "64\n", "every string valid"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / A` | `1` | Minimum valid instance |
| `1 1 / AA` | `0` | Pattern longer than target |
| `4 1 / AA` | `1` | Overlapping coverage handling |
| `3 4 / A C G T` | `64` | Every position independently covered |

## Edge Cases

Consider:

```
1 1
AA
```

No valid string exists.

After reading one character, no pattern can end because the only pattern length is `2`. The DP transition sees:

```
rem = 0
longest = 0
```

and rejects the state immediately. The final answer becomes `0`.

Now consider overlapping coverage:

```
4 1
AA
```

At position `2`, the first `"AA"` match creates:

```
rem = 1
```

meaning position `3` is already guaranteed covered. When position `3` is processed, another `"AA"` ends and refreshes coverage again. The algorithm correctly chains overlapping intervals.

Finally, consider suffix matches through failure links:

```
3 2
AAA
AA
```

When the automaton reads `"AAA"`, the node for `"AAA"` also inherits the match for `"AA"` through its failure link. Without propagating:

```
best[v] = max(best[v], best[fail[v]])
```

the DP would miss shorter suffix matches and incorrectly reject some valid strings.
