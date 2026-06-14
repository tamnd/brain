---
title: "CF 1551C - Interesting Story"
description: "We are given several independent test cases. In each test case, we receive a list of words, and we want to select as many of these words as possible so that the selected subset satisfies a specific imbalance condition."
date: "2026-06-14T20:41:34+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "sortings", "strings"]
categories: ["algorithms"]
codeforces_contest: 1551
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 734 (Div. 3)"
rating: 1500
weight: 1551
solve_time_s: 287
verified: true
draft: false
---

[CF 1551C - Interesting Story](https://codeforces.com/problemset/problem/1551/C)

**Rating:** 1500  
**Tags:** greedy, sortings, strings  
**Solve time:** 4m 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several independent test cases. In each test case, we receive a list of words, and we want to select as many of these words as possible so that the selected subset satisfies a specific imbalance condition.

The condition is evaluated by looking at letter frequencies across all chosen words. Among the letters `a, b, c, d, e`, we want to find a letter such that its total number of occurrences in the chosen words is strictly greater than the total number of occurrences of all the other letters combined.

Another way to see this is to imagine we pick some words, then count how many times each letter appears globally. We are looking for a letter that “dominates” the rest of the alphabet combined.

The task is not to maximize anything inside a word, but to choose a subset of words that makes this dominance possible, while keeping the subset as large as possible.

The constraints are large: the total number of words across all test cases is up to 2 · 10^5, and total character length is up to 4 · 10^5. This rules out any solution that tries all subsets or repeatedly recomputes character counts per candidate subset. Any per-test-case solution must be close to linear or linearithmic in the total input size.

A naive idea would be to try every subset of words, but that is exponential in n and immediately infeasible. Even trying to sort subsets or recompute full frequency tables per prefix would be too slow.

A more subtle failure mode comes from greedily taking all words: this clearly fails when no single letter dominates globally. For example, words that are balanced like `"abcde"` contribute equally to all letters, making dominance impossible no matter how many are taken.

Another subtle issue is assuming we should pick words where a chosen letter is frequent inside the word. That alone is not sufficient because the condition depends on _global comparison against all other letters combined_, not just maximizing a single letter locally.

## Approaches

The key difficulty is that the condition is global over letter counts, but decisions are made at the word level. This suggests reducing each word into how much it “helps” or “hurts” a candidate letter.

Fix a letter, say `x`. For a chosen set of words, we want:

```
count_x > sum of counts of all other letters
```

Rewriting this, we define for each word a score relative to `x`:

```
score(word, x) = (# of x in word) - (# of non-x letters in word)
```

If we sum this over selected words, the condition becomes:

```
total_score(x) > 0
```

So for a fixed letter, each word becomes a single integer contribution. We want to pick as many words as possible such that their total score is positive. The optimal strategy for a fixed letter is greedy: sort words by score in descending order and take prefixes while the running sum stays positive.

The final answer is the best result over all 5 letters.

This works because once we fix the target letter, the problem becomes a maximum-size prefix selection under a monotonic constraint on prefix sums.

### Comparison

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force subsets | O(2^n · n) | O(n) | Too slow |
| Try each letter + greedy sorting | O(5 · n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We process each test case independently.

1. For each of the five letters `a` to `e`, treat it as the candidate dominant letter.

This reduces the problem to checking whether that letter can dominate the rest.
2. For each word, compute its contribution score for the chosen letter: count occurrences of the letter minus occurrences of all other letters.

This converts each word into a single integer value representing its usefulness for this letter.
3. Sort all words by this score in descending order.

This ensures we consider the most beneficial words first, which maximizes how long the prefix remains positive.
4. Traverse the sorted list and maintain a running sum. Keep extending the prefix as long as adding the next word keeps the sum strictly positive.

Once the sum would become non-positive, we stop.
5. Record the maximum number of words achievable for this letter.
6. Repeat for all five letters and take the maximum result across them.

### Why it works

For a fixed letter, the transformation reduces the original constraint into a linear inequality on a sum of independent contributions. Any optimal selection must consist of words with highest marginal benefit first; otherwise swapping a lower-score word with a higher-score word only increases the total sum or keeps it unchanged while not reducing size. This exchange argument guarantees that the best valid subset corresponds to a prefix of the sorted order.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve_case(words):
    best = 0

    for target in "abcde":
        vals = []
        for w in words:
            c = 0
            for ch in w:
                if ch == target:
                    c += 1
                else:
                    c -= 1
            vals.append(c)

        vals.sort(reverse=True)

        s = 0
        cnt = 0
        for v in vals:
            if s + v <= 0:
                break
            s += v
            cnt += 1

        best = max(best, cnt)

    return best

def main():
    t = int(input())
    for _ in range(t):
        n = int(input())
        words = [input().strip() for _ in range(n)]
        print(solve_case(words))

if __name__ == "__main__":
    main()
```

The code follows the reduction described earlier. Each word is converted into a score relative to the current target letter. Sorting ensures we always prioritize words that most strongly support the dominance condition. The prefix accumulation enforces the strict positivity requirement directly.

A subtle detail is the stopping condition `s + v <= 0`. We must stop immediately when adding a word would break strict dominance, since any further words are no better due to sorting order. Another important point is recomputing scores separately for each letter, since the optimal subset depends heavily on which letter is chosen as dominant.

## Worked Examples

### Example 1

Input:

```
3
bac
aaada
e
```

We evaluate letter `a`:

| Step | Word | Score | Running Sum | Taken |
| --- | --- | --- | --- | --- |
| 1 | aaada | +3 | 3 | yes |
| 2 | bac | -1 | 2 | yes |
| 3 | e | -1 | 1 | yes |

We successfully take all 3 words.

This works because `a` dominates the rest after aggregation.

### Example 2

Input:

```
3
aba
abcde
aba
```

For letter `a`:

| Step | Word | Score | Running Sum | Taken |
| --- | --- | --- | --- | --- |
| 1 | aba | +1 | 1 | yes |
| 2 | aba | +1 | 2 | yes |
| 3 | abcde | -3 | - | stop |

We stop before taking all words, since including `abcde` breaks dominance.

This demonstrates why greedy ordering is necessary: a globally “bad” word must be delayed or excluded even if it appears in the input early.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(5 · n log n) | Each test sorts n word scores for each of 5 letters |
| Space | O(n) | Stores per-word transformed scores |

The total input size across test cases is bounded, so the solution runs comfortably within limits. Sorting dominates runtime but remains efficient for 2 · 10^5 total words.

## Test Cases

```python
import sys, io

def solve(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def solve_case(words):
        best = 0
        for target in "abcde":
            vals = []
            for w in words:
                c = 0
                for ch in w:
                    c += 1 if ch == target else -1
                vals.append(c)
            vals.sort(reverse=True)
            s = 0
            cnt = 0
            for v in vals:
                if s + v <= 0:
                    break
                s += v
                cnt += 1
            best = max(best, cnt)
        return best

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        words = [input().strip() for _ in range(n)]
        out.append(str(solve_case(words)))
    return "\n".join(out)

# provided samples
assert solve("""6
3
bac
aaada
e
3
aba
abcde
aba
2
baba
baba
4
ab
ab
c
bc
5
cbdca
d
a
d
e
3
b
c
ca
""") == """3
2
0
2
3
2"""

# edge cases
assert solve("""1
1
abcde
""") == "0"

assert solve("""1
2
a
a
""") == "2"

assert solve("""1
3
abc
abc
abc
""") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single balanced word | 0 | no dominance possible |
| all identical single-letter words | 2 | greedy fully selects |
| symmetric full words | 0 | all letters cancel out |

## Edge Cases

A critical edge case is when every word is perfectly balanced like `"abcde"`. For such input, every letter contributes equally, so every score is zero. The algorithm sorts zeros and immediately stops because the first addition already violates strict positivity.

Another edge case is when all words consist of a single repeated letter, for example `"a", "a", "a"`. For target letter `a`, every score is positive, so all words are taken. For other letters, all scores are negative, producing zero selections. The maximum correctly becomes the full count.

A third case is mixed dominance where a word strongly supports one letter but slightly harms it overall, forcing ordering effects. The sorting step ensures such words are placed correctly, and the prefix rule prevents invalid selections from creeping in later in the sequence.
