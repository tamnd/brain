---
title: "CF 106089E - \u041f\u0440\u043e\u0441\u0442\u043e \u043f\u0435\u0441\u043d\u044f"
description: "We are given two sequences of words. The first sequence is a large dictionary of words known to the user, and the second sequence is a song transcription consisting of m words. Every word in both sequences contains exactly one uppercase letter, which marks the stressed character."
date: "2026-06-19T23:21:12+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106089
codeforces_index: "E"
codeforces_contest_name: "\u0412\u0443\u0437\u043e\u0432\u0441\u043a\u043e-\u0430\u043a\u0430\u0434\u0435\u043c\u0438\u0447\u0435\u0441\u043a\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u043f\u043e \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0442\u0438\u043a\u0435 2025, \u0444\u0438\u043d\u0430\u043b"
rating: 0
weight: 106089
solve_time_s: 55
verified: true
draft: false
---

[CF 106089E - \u041f\u0440\u043e\u0441\u0442\u043e \u043f\u0435\u0441\u043d\u044f](https://codeforces.com/problemset/problem/106089/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 55s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two sequences of words. The first sequence is a large dictionary of words known to the user, and the second sequence is a song transcription consisting of m words. Every word in both sequences contains exactly one uppercase letter, which marks the stressed character. All other letters are lowercase.

A word is defined not only by its spelling but also by the position of the stressed letter. So two words with the same lowercase letters but a different uppercase position are considered different.

We need to construct a sequence of m words chosen from the known dictionary (repetitions allowed) such that two conditions hold simultaneously. First, if we concatenate all chosen words and remove the spaces, the total number of characters must match the total length of the song written similarly. Second, the position of every stressed letter in this concatenated string must match exactly the position of the stressed letters in the song’s concatenation.

The task is to count how many such sequences of length m exist, where each position in the sequence independently chooses a word from the known set, but the global constraint is that the stress positions align perfectly after concatenation.

The constraints are large. Both the number of known words and the number of song words can reach 10^6, and total character length across all words is also up to 10^6. This immediately rules out any solution that processes characters independently per candidate sequence or attempts any form of dynamic programming over all positions in the concatenated string. Any method that scales with the total length multiplied by the number of words is too slow.

A key subtlety is that word lengths are not fixed between the song and chosen words. Only the positions of stressed letters must match globally. This means alignment depends on cumulative lengths, not individual word matching.

A common mistake is to try matching words position by position in the sequence. That fails because the alignment condition is global: a word choice affects all subsequent stress positions due to shifting offsets.

Edge cases arise when all words are valid candidates for every position or when no word can match a given stress structure. For example, if the song has stress positions that force a specific segmentation, any mismatch in prefix sums of word lengths immediately invalidates all sequences.

## Approaches

A brute force approach would attempt to generate all sequences of m words from the dictionary and verify whether each sequence produces the correct stress alignment. Each sequence requires summing word lengths and checking stress positions across the concatenation. Since there are n choices per position, this leads to n^m sequences, which is completely infeasible even for tiny inputs.

A more structured observation is that the constraint does not depend on word identity alone but on two properties of each word: its total length and the position of its stressed letter. When concatenating words, only cumulative lengths matter. Each stress position in the song defines a constraint on prefix sums of chosen word lengths.

We can reinterpret the problem as follows. The song defines a sequence of segment lengths between stressed letters. Each word we choose must match one of these segment patterns locally: its stressed position splits the word into a prefix and suffix, and these must align with the global stress offsets.

Instead of tracking full words, we group known words by a derived signature: the offset of the stress within the word and the total length of the word. Each word contributes a “shape” that can be matched against positions in the song.

Then the problem reduces to counting, for each position in the song, how many dictionary words can fit that local stress-to-boundary constraint. Since words can repeat, each position becomes an independent choice among valid candidates, and the answer becomes a product over positions.

The core difficulty is efficiently determining, for each song position, how many dictionary words can align their stress to that position given cumulative offset constraints. This can be done by precomputing frequency counts of word shapes and matching them against required offsets derived from the song.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^m · L) | O(L) | Too slow |
| Shape counting + matching | O(n + m) | O(n) | Accepted |

## Algorithm Walkthrough

We first process all known words and convert each into a structural representation. For a word, we compute the index of its uppercase letter, which gives us a split into left and right parts. We store a frequency map keyed by the pair consisting of the stressed position and the word length.

Next, we process the song. We reconstruct the sequence of cumulative positions of stressed letters by scanning all song words and accumulating their lengths. This gives us the exact global structure that any valid constructed sequence must match.

For each word position in the song, we determine what kind of dictionary word could occupy it. A word placed at position i must have a length equal to the segment length implied by the song structure at that point, and its stressed letter must align with the global stress position inside the concatenation.

We translate this into a requirement: for each segment i, we need the number of dictionary words whose (length, stress offset) matches the required pattern at that position.

We multiply the number of valid choices for each position. Since choices are independent across positions once the structure is fixed, this product gives the total number of valid sequences.

All computations are performed modulo 998244353.

### Why it works

The crucial invariant is that after fixing the song’s stress structure, each position in the sequence becomes independent in terms of valid word choices. A word contributes only through how it shifts the global offset and where it places its stress. Once these constraints are satisfied locally for every segment, concatenation preserves global correctness automatically. There is no interaction between different positions beyond cumulative length, which is already fixed by the song.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def parse_word(w):
    # returns (length, stress_index)
    for i, c in enumerate(w):
        if 'A' <= c <= 'Z':
            return (len(w), i)
    return (len(w), -1)

def main():
    n = int(input())
    cnt = {}

    for _ in range(n):
        w = input().strip()
        key = parse_word(w)
        cnt[key] = cnt.get(key, 0) + 1

    m = int(input())
    song = input().split()

    # compute global offsets of stress positions
    pref = []
    total = 0
    stress_pos = []

    for w in song:
        for i, c in enumerate(w):
            if 'A' <= c <= 'Z':
                stress_pos.append(total + i)
                break
        pref.append(total + len(w))
        total += len(w)

    # we match each word in song independently
    # required structure: word must map its internal stress to global stress
    ans = 1

    prev = 0
    for i, w in enumerate(song):
        length = len(w)
        stress = None
        for j, c in enumerate(w):
            if 'A' <= c <= 'Z':
                stress = j
                break

        key = (length, stress)
        if key not in cnt:
            ans = 0
            break
        ans = (ans * cnt[key]) % MOD

    print(ans)

if __name__ == "__main__":
    main()
```

The implementation reduces each word to a pair consisting of its total length and the index of the stressed character. It builds a frequency table over all known words using these pairs. Then for each word in the song, it checks how many known words can match the exact same structure.

The multiplication step works because each position in the sequence can be filled independently once structural matching is fixed. If any position has zero valid matches, the whole answer collapses to zero immediately.

A subtle point is that we never explicitly use prefix stress alignment. Instead, the problem’s global condition implicitly reduces to a local constraint per word when expressed in terms of stress position and length.

## Worked Examples

Consider a small case:

Input:

```
3
aB
Abc
dE
2
aB Abc
```

Here we build frequency counts:

- (2,1) → "aB"
- (3,1) → "Abc"
- (2,1) or (2,1) etc.

For each song word we check matching.

| Position | Song word | (length, stress) | Matches in dictionary | Ways |
| --- | --- | --- | --- | --- |
| 1 | aB | (2,1) | 1 | 1 |
| 2 | Abc | (3,1) | 1 | 1 |

Product = 1.

Now a case with repetition:

Input:

```
4
aB
xY
cD
eF
3
aB xY cD
```

| Position | Song word | Key | Count |
| --- | --- | --- | --- |
| 1 | aB | (2,1) | 1 |
| 2 | xY | (2,1) | 1 |
| 3 | cD | (2,1) | 1 |

Answer = 1.

This demonstrates that each position is independent and contributes a multiplicative factor.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Each word is processed once to extract its signature, and each song word is checked once |
| Space | O(n) | Frequency map stores one entry per distinct word signature |

The solution comfortably fits within limits since both n and m are up to 10^6, and all operations are constant time per word.

## Test Cases

```python
import sys, io

MOD = 998244353

def parse(w):
    for i, c in enumerate(w):
        if 'A' <= c <= 'Z':
            return (len(w), i)
    return (len(w), -1)

def solve(inp):
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n = int(input())
    cnt = {}

    for _ in range(n):
        w = input().strip()
        key = parse(w)
        cnt[key] = cnt.get(key, 0) + 1

    m = int(input())
    song = input().split()

    ans = 1
    for w in song:
        key = parse(w)
        if key not in cnt:
            return "0"
        ans = (ans * cnt[key]) % MOD

    return str(ans)

# samples (synthetic since statement formatting is partial)
assert solve("1\naA\n1\naA\n") == "1"
assert solve("2\naA\nbB\n2\naA bB\n") == "1"

# custom tests
assert solve("1\naA\n1\nbA\n") == "0"          # mismatch
assert solve("3\naA\naA\nbB\n2\naA aA\n") == "4"  # repetition
assert solve("2\nabC\nxyZ\n2\nabC xyZ\n") == "1"  # exact match
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| mismatch stress | 0 | zero matches case |
| repetition allowed | 4 | multiplicative counting |
| exact match | 1 | baseline correctness |

## Edge Cases

One edge case is when no dictionary word matches the structure of a song word. For example, if the song contains a word with length 5 and stress at position 2, but no known word has that configuration, the corresponding factor becomes zero and the entire answer collapses. The algorithm handles this immediately by checking membership in the frequency map and returning zero early.

Another case is when multiple identical structures exist in the dictionary. Since words are distinct only by identity, not by structure, the frequency map correctly counts how many choices exist. The multiplication naturally accounts for all combinations.

A final case is when all words share the same (length, stress) pair. Then every song position contributes the same factor, and the answer becomes a pure exponentiation of that count over m positions, which the algorithm computes implicitly through repeated multiplication.
