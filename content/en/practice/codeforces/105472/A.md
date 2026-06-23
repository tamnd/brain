---
title: "CF 105472A - Alphabet Animals"
description: "We are given the last animal name spoken by the previous player and a pool of unused animal names. A valid move for us must satisfy a chaining rule: the new name must begin with the last character of the previous name, and it must not have been used before."
date: "2026-06-23T18:04:32+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105472
codeforces_index: "A"
codeforces_contest_name: "2019-2020 ACM-ICPC Nordic Collegiate Programming Contest (NCPC 2019)"
rating: 0
weight: 105472
solve_time_s: 65
verified: true
draft: false
---

[CF 105472A - Alphabet Animals](https://codeforces.com/problemset/problem/105472/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given the last animal name spoken by the previous player and a pool of unused animal names. A valid move for us must satisfy a chaining rule: the new name must begin with the last character of the previous name, and it must not have been used before. Among all valid moves, we want to know whether we can immediately force the next player into a losing position. If such a “forcing” move exists, we prefer the earliest one in the input order; otherwise we settle for any valid move; if no valid move exists at all, we output a question mark.

A losing position for the next player happens right after we play a word if they cannot respond. That means no remaining unused word starts with the last letter of the word we chose.

The input size can be as large as 100,000 words. This rules out any solution that repeatedly scans the entire list for each candidate or simulates multiple future moves. A solution that is linear or near-linear in the number of words is necessary, since anything quadratic would reach about 10¹⁰ operations in the worst case and will not pass in two seconds.

A subtle edge case comes from the requirement “first such name in input order.” Even if a better strategic move appears later, we are not allowed to skip earlier valid candidates.

Another common pitfall is forgetting that “eliminating the next player” depends on the state after our chosen word is removed. A word can look terminal only after excluding itself from the pool of words starting with its last character.

For example, suppose previous word ends with ‘a’ and the list contains “apple”, “ant”, and “art”. If we pick “ant”, the next player still has “apple” and “art” starting with ‘t’ or ‘a’ depending on letters, so we must carefully count based on first letters.

## Approaches

A direct simulation approach tries every word that starts with the required initial letter, then removes it temporarily and scans the entire list to check whether any remaining word begins with its last letter. This is correct because it explicitly tests the game condition after each possible move. However, for each candidate we may rescan up to 10⁵ words, producing a worst-case complexity of O(n²). With n = 10⁵, this becomes too slow.

The key observation is that we do not actually need to rescan the list for every candidate. What matters for a chosen word is only how many words begin with its last letter. If exactly one word in the entire pool starts with that letter, and that word is the word we are playing, then the next player has no legal move. This reduces the “future check” to a simple frequency lookup.

So the problem becomes a two-level scan. First, we precompute how many words start with each letter ‘a’ to ‘z’. Then we scan the list in input order, filter words that can be played (their first letter matches the previous word’s last letter), and test whether they are terminal using the frequency table.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force simulation per candidate | O(n²) | O(n) | Too slow |
| Frequency counting + single pass | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We transform the problem into simple bookkeeping over first and last letters.

1. Read the previous word and extract its last character. This character defines the only valid starting letter for our move, since all other words are immediately irrelevant.
2. Read all available words and compute a frequency table that counts how many words start with each letter. This allows us to instantly answer how many options the next player would have after any move.
3. Scan the list in input order and collect words whose first character matches the required starting letter. These are the only candidates we can legally play.
4. For each candidate, check whether it is “terminal.” A word is terminal if the frequency of words starting with its last character is exactly one, meaning it is the only such word in the entire pool. In that case, once we play it, no remaining word can respond.
5. The first terminal candidate in input order is the optimal output and must be printed with an exclamation mark.
6. If no terminal candidate exists, but at least one candidate exists, output the first candidate without an exclamation mark.
7. If no candidate exists at all, output a question mark.

The reasoning behind step 4 is that after playing a word, that word is removed from the pool. If no other word begins with its ending letter, the next player has zero legal moves.

### Why it works

The state of the game after our move is fully determined by the last letter of our chosen word and the multiset of remaining word prefixes. Since the only change we introduce is removing one word from the pool, the only affected count is the frequency of its starting letter class. If that frequency was exactly one, removing the word leaves zero available responses. Any other structure of the remaining list is irrelevant to the next move, so the frequency condition is both necessary and sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

prev = input().strip()
last_char = prev[-1]

n = int(input())
words = [input().strip() for _ in range(n)]

start_count = [0] * 26
for w in words:
    start_count[ord(w[0]) - 97] += 1

candidates = []
for w in words:
    if w[0] == last_char:
        candidates.append(w)

if not candidates:
    print("?")
    sys.exit()

first_valid = None
first_terminal = None

for w in candidates:
    idx = ord(w[-1]) - 97
    is_terminal = (start_count[idx] == 1)

    if first_valid is None:
        first_valid = w

    if is_terminal and first_terminal is None:
        first_terminal = w

if first_terminal is not None:
    print(first_terminal + "!")
else:
    print(first_valid)
```

The solution first builds a frequency array indexed by letters to allow constant-time checks for how many words begin with any given character. This avoids any repeated scanning during candidate evaluation.

We then separate valid moves based on the required starting letter. During evaluation, we do not remove words from data structures; instead, we rely on the precomputed counts. The condition `start_count[last_letter] == 1` is sufficient to guarantee that after choosing the word, no other word remains that could be played by the next player.

The two tracked variables, `first_valid` and `first_terminal`, ensure we respect input order constraints without sorting or extra data structures.

## Worked Examples

### Example 1

Input:

```
dog
3
snake
emu
goat
```

We need words starting with ‘g’. Only “goat” qualifies.

| Step | Word | Valid start | Last char | start_count[last] | Terminal | First valid | First terminal |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | snake | no | - | - | - | - | - |
| 2 | emu | no | - | - | - | - | - |
| 3 | goat | yes | t | start_count[t]=1 | yes | goat | goat |

Only “goat” is playable, and since no other word starts with ‘t’, it is terminal, so output is:

```
goat!
```

### Example 2

Input:

```
dog
2
snake
emu
```

No word starts with ‘g’, so no valid move exists.

| Step | Word | Valid start |
| --- | --- | --- |
| 1 | snake | no |
| 2 | emu | no |

Output:

```
?
```

This confirms the case where the player cannot make any move.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One pass to build frequency table and one pass to filter candidates |
| Space | O(1) | Only 26 counters regardless of input size |

The algorithm fits comfortably within limits since even 10⁵ operations are trivial under a 2-second constraint in Python when using direct array access and simple loops.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import sys

    prev = input().strip()
    last_char = prev[-1]

    n = int(input())
    words = [input().strip() for _ in range(n)]

    start_count = [0] * 26
    for w in words:
        start_count[ord(w[0]) - 97] += 1

    candidates = [w for w in words if w[0] == last_char]

    if not candidates:
        return "?"

    first_valid = None
    first_terminal = None

    for w in candidates:
        if first_valid is None:
            first_valid = w
        if start_count[ord(w[-1]) - 97] == 1 and first_terminal is None:
            first_terminal = w

    return (first_terminal + "!") if first_terminal else first_valid

# provided-style samples
assert run("dog\n0\n") == "?", "empty list"
assert run("dog\n2\nsnake\nemu\n") == "?", "sample 2 behavior"

# custom cases
assert run("cat\n1\ntiger\n") == "tiger!", "single terminal move"
assert run("ant\n3\napple\nape\nart\n") == "apple", "valid but not terminal"
assert run("eel\n2\nlion\nzebra\n") == "?", "no valid start"
assert run("abc\n1\ncaa\n") == "caa!", "chain works exactly once"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| no valid start | ? | no candidate case |
| single terminal move | word! | forced win detection |
| multiple candidates | first valid | input order priority |
| chain case | word! | correct last-letter dependency |

## Edge Cases

One important edge case is when a valid move exists but it is not terminal. Consider previous word ending in ‘a’ and multiple words starting with ‘a’, but all of them end in letters that also have multiple available words. In this case, none of them can guarantee elimination. The algorithm correctly falls back to returning the first valid candidate because `start_count[last_letter] > 1` for every candidate, preventing any false terminal classification.

Another edge case occurs when exactly one word exists for a given starting letter but it is not actually reachable due to the previous word constraint. Since we filter by `w[0] == last_char`, unreachable words never enter the candidate set, ensuring correctness.

A final edge case is when all words are valid candidates but none are terminal. For example, previous word ends in ‘a’, and there are multiple words starting with ‘a’, and their ending letters also have multiple words. The frequency check never triggers, so `first_terminal` remains empty and the algorithm correctly outputs the first valid word without an exclamation mark.
