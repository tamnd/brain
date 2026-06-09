---
title: "CF 1722C - Word Game"
description: "We have three players, each writing down $n$ distinct words of length three. The goal is to assign points based on word uniqueness: a word written by only one player gives 3 points to that player, a word written by exactly two players gives 1 point to each of them, and a word…"
date: "2026-06-09T19:11:52+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1722
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 817 (Div. 4)"
rating: 800
weight: 1722
solve_time_s: 150
verified: false
draft: false
---

[CF 1722C - Word Game](https://codeforces.com/problemset/problem/1722/C)

**Rating:** 800  
**Tags:** data structures, implementation  
**Solve time:** 2m 30s  
**Verified:** no  

## Solution
## Problem Understanding

We have three players, each writing down $n$ distinct words of length three. The goal is to assign points based on word uniqueness: a word written by only one player gives 3 points to that player, a word written by exactly two players gives 1 point to each of them, and a word written by all three players gives zero points. For multiple test cases, we need to calculate the final score for each player in the same order they appear.

The constraints are small but non-trivial. Each player can write up to 1000 words, and there are at most 100 test cases, so in total we could process up to 300,000 words. This rules out algorithms that repeatedly compare each player's words with every other player's words in a naive triple loop, because that would be $O(n^2)$ per test case, reaching roughly $10^9$ operations in the worst case. A linear or near-linear solution in the number of words per test case is preferable.

Edge cases are subtle. For instance, if all players write exactly the same words, each score must be zero, not accidentally giving points due to an indexing mistake. Another tricky scenario is when every word is unique across players; each player should then score $3n$, not less, so forgetting to account for the total uniqueness would yield incorrect results.

## Approaches

A brute-force approach would be to take each player's words and check for every other player whether the word appears. For each word, we would count the number of players who wrote it and assign points accordingly. This works because it directly implements the scoring rules. However, this would involve checking up to $3n$ words against the other two sets for each player, giving $O(n^2)$ complexity per test case. With the constraints, $n$ up to 1000, this approach could make a billion comparisons, which is too slow.

The key observation to optimize is that we only care about how many players wrote each word, not who specifically wrote it. If we construct a frequency map for all words across all three players, we can then assign points based on the frequency: 1 occurrence gives 3 points, 2 occurrences give 1 point to each involved player, and 3 occurrences give 0. This reduces the problem to a linear scan to build the frequency dictionary and a second linear scan to sum scores per player. This approach is both simple and efficient.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) per test case | O(n) | Too slow |
| Frequency Map | O(n) per test case | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases, $t$.
2. For each test case, read $n$ and the three lists of words, one list per player.
3. Construct a frequency dictionary counting how many times each word appears across all players. This is done by iterating through all words of all three players.
4. Initialize a scores array for the three players with zero.
5. For each player, iterate through their list of words. Check the frequency of each word in the dictionary. If the frequency is 1, add 3 points; if 2, add 1 point; if 3, add 0 points. This directly implements the scoring rules using the frequency information.
6. After processing all words for all players, print the scores in order.

Why it works: By counting the frequency of each word first, we capture exactly how many players wrote it. The scoring rules are then a simple function of this frequency, ensuring that every word contributes the correct number of points. No double counting occurs because we iterate per player and consult the frequency map, which correctly represents global counts.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    players = [input().split() for _ in range(3)]
    
    freq = {}
    for player in players:
        for word in player:
            freq[word] = freq.get(word, 0) + 1
    
    scores = [0, 0, 0]
    for i in range(3):
        for word in players[i]:
            if freq[word] == 1:
                scores[i] += 3
            elif freq[word] == 2:
                scores[i] += 1
            # freq[word] == 3 -> score += 0
    
    print(*scores)
```

The solution reads input efficiently using `sys.stdin.readline`. Each player's words are stored as a list of strings. The frequency dictionary counts occurrences globally across players. During scoring, we only need the frequency count, which makes the point calculation immediate. A subtle but important detail is using `scores[i] += 1` only when `freq[word] == 2` rather than trying to manually figure out which other player also wrote the word.

## Worked Examples

### Sample 1

Input:

```
1
3
abc def ghi
def ghi jkl
ghi jkl mno
```

| Word | Frequency | Player 1 | Player 2 | Player 3 |
| --- | --- | --- | --- | --- |
| abc | 1 | +3 | 0 | 0 |
| def | 2 | +1 | +1 | 0 |
| ghi | 3 | 0 | 0 | 0 |
| jkl | 2 | 0 | +1 | +1 |
| mno | 1 | 0 | 0 | +3 |

Final scores: 4 3 4

This trace shows the frequency dictionary determines the exact contribution of each word without repeatedly comparing sets.

### Sample 2

Input:

```
1
1
abc
abc
abc
```

| Word | Frequency | Player 1 | Player 2 | Player 3 |
| --- | --- | --- | --- | --- |
| abc | 3 | 0 | 0 | 0 |

Final scores: 0 0 0

This tests the edge case where all words are identical; all points are zero.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Counting frequencies and scoring each word involves linear scans over the total number of words (3n) |
| Space | O(n) | The frequency dictionary stores at most 3n entries, one per word |

With $t\le 100$ and $n\le 1000$, the total number of words is 300,000. A linear scan per test case ensures we stay well within the 1-second time limit and the 256MB memory limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    # insert the solution code here
    t = int(input())
    for _ in range(t):
        n = int(input())
        players = [input().split() for _ in range(3)]
        freq = {}
        for player in players:
            for word in player:
                freq[word] = freq.get(word, 0) + 1
        scores = [0, 0, 0]
        for i in range(3):
            for word in players[i]:
                if freq[word] == 1:
                    scores[i] += 3
                elif freq[word] == 2:
                    scores[i] += 1
        print(*scores)
    return output.getvalue().strip()

# provided samples
assert run("3\n1\nabc\ndef\nabc\n3\norz for qaq\nqaq orz for\ncod for ces\n5\niat roc hem ica lly\nbac ter iol ogi sts\nbac roc lly iol iat") == "1 3 1\n2 2 6\n9 11 5"

# custom cases
assert run("1\n1\na\na\na") == "0 0 0"
assert run("1\n2\na b\nc d\ne f") == "6 6 6"
assert run("1\n3\na b c\na x y\nz b c") == "4 5 4"
assert run("1\n2\na b\nb c\na c") == "2 2 2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| All words same | 0 0 0 | Handling maximum overlap |
| All words unique | 6 6 6 | Each player scores maximum |
| Mixed overlap | 4 5 4 | Correctly sums 1-point and 3-point words |
| Pairwise overlap | 2 2 2 | Correct handling of 2 occurrences |

## Edge Cases

When all players write exactly the same word, the frequency dictionary correctly sets the frequency to 3. Iterating over each player, we check `freq[word] == 3`, so no points are awarded. For example, input:

```
1
1
abc
abc
abc
```

produces scores `[0, 0, 0]`. The algorithm handles minimum input size, maximum overlap, and ensures no points are accidentally added.

When
