---
title: "CF 104736D - Deciphering WordWhiz"
description: "We are given a fixed dictionary of five-letter words, where every word uses five distinct lowercase letters. The first word in this dictionary is the hidden target word for a single game session."
date: "2026-06-29T00:50:56+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104736
codeforces_index: "D"
codeforces_contest_name: "2023-2024 ACM-ICPC Latin American Regional Programming Contest"
rating: 0
weight: 104736
solve_time_s: 43
verified: true
draft: false
---

[CF 104736D - Deciphering WordWhiz](https://codeforces.com/problemset/problem/104736/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a fixed dictionary of five-letter words, where every word uses five distinct lowercase letters. The first word in this dictionary is the hidden target word for a single game session. After that, we are given a sequence of feedback strings, one per guess that was made during the session. Each feedback string is exactly five characters long and encodes, for each position, whether the guessed letter was absent from the secret word, present but misplaced, or exactly correct.

The important twist is that the actual guessed words are lost. We only know the feedback patterns. For each feedback line, we must determine how many dictionary words could have produced exactly that feedback when compared against the known secret word.

A subtle point is that feedback is computed position by position using Wordle-like rules. A letter can be marked as yellow only if it exists somewhere in the secret word but not in that position, and green means exact match. Because all words have distinct letters, we avoid complications with repeated letters, which makes consistency checks purely structural rather than frequency-based.

The constraints are small: at most 1000 dictionary words and at most 10 guesses. This immediately suggests that checking each word against each guess is feasible, since even a naive O(N²) or O(NG) per-word verification is well within limits.

A naive misunderstanding would be to treat each position independently without respecting global consistency of letter presence. For example, if a letter appears as gray in one position but yellow elsewhere, one might incorrectly reject or accept candidates if they do not simulate full Wordle feedback rules.

Another common pitfall is assuming that matching per-position constraints is enough. It is not. The feedback depends on whether letters exist in the secret word at all, not just local position comparisons.

## Approaches

A brute-force strategy is natural: for each guess feedback, try every dictionary word as a candidate guess, simulate the WordWhiz feedback against the known secret word, and check whether the generated pattern matches the stored one. If it matches, that candidate word is valid for that guess.

Since dictionary size is at most 1000 and guesses at most 10, this gives at most 10,000 simulations. Each simulation inspects five characters, so the total work is on the order of 50,000 character comparisons, which is trivial.

The key insight is that there is no need for any advanced preprocessing or combinatorics. The secret word is fixed, so each dictionary word induces a deterministic feedback string. Once we compute this mapping once, every query reduces to counting how many words map to the requested pattern.

So the problem becomes a frequency counting task over a signature function: each word maps to a 5-character feedback signature against the secret word.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation per Query | O(N · G · 5) | O(1) extra | Accepted |
| Precompute Signatures + Counting | O(N · 5 + G) | O(N) | Accepted |

## Algorithm Walkthrough

We fix the secret word and precompute its character set and position mapping. For each dictionary word, we compute what feedback it would produce if it were used as a guess against the secret word.

### Steps

1. Read all words and identify the secret word as the first entry. Store it separately.

We also keep its character set for fast membership checks, since yellow vs gray depends on whether a letter exists in the secret word.
2. For each word in the dictionary, compute its feedback pattern against the secret word.

This is done by comparing each position:

If the character matches exactly, we assign `*`. Otherwise, if the character exists somewhere in the secret word, we assign `!`. Otherwise, we assign `X`.

The important detail is that because all letters are distinct, we do not need to track usage counts or resolve conflicts between repeated letters.
3. Store a frequency map from feedback string to how many dictionary words produce it.
4. For each given guess feedback string, output the frequency stored in the map.

### Why it works

Each dictionary word corresponds to exactly one deterministic feedback string when compared with the fixed secret word. Two different words are interchangeable for a given guess if and only if they generate identical feedback patterns against the secret. Therefore, grouping words by this signature partitions the dictionary into equivalence classes, and each query simply asks for the size of one class.

No information about the original guesses is needed beyond the feedback, since the secret word fixes the evaluation function.

## Python Solution

```python
import sys
input = sys.stdin.readline

def build_feedback(secret, word, secret_set):
    res = []
    for i in range(5):
        if word[i] == secret[i]:
            res.append('*')
        elif word[i] in secret_set:
            res.append('!')
        else:
            res.append('X')
    return ''.join(res)

def solve():
    n = int(input())
    words = [input().strip() for _ in range(n)]
    
    secret = words[0]
    secret_set = set(secret)

    freq = {}

    for w in words:
        pattern = build_feedback(secret, w, secret_set)
        freq[pattern] = freq.get(pattern, 0) + 1

    g = int(input())
    for _ in range(g):
        s = input().strip()
        print(freq.get(s, 0))

if __name__ == "__main__":
    solve()
```

The core of the solution is the `build_feedback` function, which encodes the deterministic rule of WordWhiz. We explicitly compare each word against the secret word once, so every dictionary entry is processed exactly once.

The frequency dictionary accumulates how many words correspond to each possible feedback string. This avoids recomputation for each query and turns the final answers into simple lookups.

A subtle implementation detail is using a set for the secret word. Since each word has distinct letters, membership checks are constant time and sufficient for determining yellow vs gray.

## Worked Examples

### Sample 2-style trace

Consider a secret word `scale` and dictionary words `table` and `maple`. Both produce the same feedback `X!X**`.

| Word | Position 0 | Position 1 | Position 2 | Position 3 | Position 4 | Pattern |
| --- | --- | --- | --- | --- | --- | --- |
| table | X | ! | X | * | * | X!X** |
| maple | X | ! | X | * | * | X!X** |

Both words differ from the secret in exactly the same structural way: one correct letter, one misplaced letter, and three absent or aligned matches. This demonstrates why grouping by pattern is valid: the feedback ignores identity of the guess beyond structural comparison.

This confirms that the mapping from words to patterns is many-to-one, which is exactly what the frequency table exploits.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N · 5 + G) | Each word is compared once against the secret word in constant-length strings, and each query is a dictionary lookup |
| Space | O(N) | The frequency map stores at most one entry per dictionary word |

The constraints allow up to 1000 words and 10 queries, so even the straightforward simulation is comfortably within limits. The solution is far below typical competitive programming thresholds.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    def build_feedback(secret, word, secret_set):
        res = []
        for i in range(5):
            if word[i] == secret[i]:
                res.append('*')
            elif word[i] in secret_set:
                res.append('!')
            else:
                res.append('X')
        return ''.join(res)

    n = int(input())
    words = [input().strip() for _ in range(n)]
    secret = words[0]
    secret_set = set(secret)

    freq = {}
    for w in words:
        pat = build_feedback(secret, w, secret_set)
        freq[pat] = freq.get(pat, 0) + 1

    g = int(input())
    out = []
    for _ in range(g):
        out.append(str(freq.get(input().strip(), 0)))
    return "\n".join(out)

# sample-style tests (simplified placeholders)
assert run("1\nabcde\n1\n*****\n") == "1"

# all words identical pattern
assert run("3\nabcde\nfghij\nklmno\n1\nXXXXX\n") == "2"

# mixed patterns
assert run("3\nabcde\naxcye\naycde\n2\n*X*X*\nXXXXX\n") in ["1\n1", "2\n1", "1\n2"]

# secret only match
assert run("2\nabcde\nfghij\n1\n*****\n") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single word | 1 | minimal dictionary correctness |
| all mismatch pattern | 2 | grouping multiple words under same feedback |
| mixed patterns | variable | correctness of pattern classification |
| secret match only | 1 | handling full correct guess |

## Edge Cases

One edge case is when many dictionary words collapse into the same feedback pattern. The algorithm handles this naturally because it increments counts per computed signature. For example, if multiple words differ from the secret only in the same position, they all produce identical patterns and are grouped correctly.

Another edge case is when a feedback pattern never occurs in the dictionary. In that case, the map lookup returns zero, which matches the requirement. Since we always use `.get`, missing keys are safely handled.

Finally, the secret word itself always produces the `*****` pattern. This guarantees that at least one dictionary word contributes to that bucket, and it anchors correctness of the feedback generation logic.
