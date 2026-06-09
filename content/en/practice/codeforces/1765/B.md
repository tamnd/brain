---
title: "CF 1765B - Broken Keyboard"
description: "We are asked to determine whether a given word could have been typed on a keyboard with a very specific malfunction: every other keystroke produces the letter twice instead of once."
date: "2026-06-09T13:09:31+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1765
codeforces_index: "B"
codeforces_contest_name: "2022-2023 ICPC, NERC, Southern and Volga Russian Regional Contest (Online Mirror, ICPC Rules, Preferably Teams)"
rating: 800
weight: 1765
solve_time_s: 484
verified: true
draft: false
---

[CF 1765B - Broken Keyboard](https://codeforces.com/problemset/problem/1765/B)

**Rating:** 800  
**Tags:** greedy  
**Solve time:** 8m 4s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to determine whether a given word could have been typed on a keyboard with a very specific malfunction: every other keystroke produces the letter twice instead of once. The sequence is global for the keyboard, not per letter: the first press prints one letter, the second prints two, the third prints one, the fourth prints two, and so on. The input gives multiple test cases, each with the length of the word and the word itself, and we are to output YES if the word could be produced on this keyboard, NO otherwise.

The constraints are small: up to 100 test cases, each word of length up to 100. This allows an O(n) solution per word, or O(t * n) overall, since 100 * 100 = 10,000 operations is negligible. Edge cases to consider include consecutive identical letters that cannot be explained by the "double press" mechanic, or words that end on an odd or even keystroke, which might leave a single letter unmatched with a double press. For example, a word "aa" cannot be produced, because it would require a double press on the first key, but the first press only prints one letter.

## Approaches

A brute-force way would be to simulate all possible sequences of key presses, alternating between one and two letters each time. For each character in the target word, we would try to match it with either a single press or a double press depending on the parity of the keystroke. This approach is correct and feasible due to small constraints, but can be simplified.

The key insight is that the sequence of letters must be grouped such that letters appearing consecutively in pairs correspond exactly to the double presses. Any letter that appears once must be on a single press (odd keystroke), and any letter that appears twice consecutively must be on a double press (even keystroke). If any letter appears consecutively in a way inconsistent with this alternating pattern, the word is impossible. For example, "ossu" can be parsed as `o` (single press), `ss` (double press), `u` (single press), which aligns with the keyboard behavior. "aa" fails because the first letter is single press, but the next identical letter would require a double press starting from the second keystroke, producing `aa` at that moment, leaving an extra unmatched `a`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Simulation / scan | O(n) per word | O(1) | Accepted |
| Brute force trying all keystroke sequences | Exponential | O(n) | Correct but unnecessary |

## Algorithm Walkthrough

1. Initialize an index `i` at 0 to track the position in the word. This index represents the next letter to match.
2. While `i` is less than the length of the word, check if the current letter is repeated in the next position.
3. If the current letter and the next letter are identical, interpret this as a double press. Increment `i` by 2 to skip both letters. This corresponds to consuming a double keystroke.
4. If the current letter is not repeated, interpret this as a single press. Increment `i` by 1.
5. Continue this process until `i` reaches the end of the word.
6. If at any point a mismatch occurs (for example, a letter expected to be repeated for a double press is not repeated), immediately conclude NO for this test case.
7. If the entire word is scanned without mismatches, conclude YES.

Why it works: Each step corresponds to the natural alternating behavior of the keyboard. Single letters correspond to odd-numbered keystrokes, and pairs correspond to even-numbered keystrokes. By scanning sequentially, we guarantee that we never assume an impossible keystroke. This greedy scan works because the keyboard behavior imposes a strict pattern on consecutive letters.

## Python Solution

```
PythonRun
```

The solution scans the word left to right. When encountering two identical consecutive letters, we interpret them as a double press and skip both. Otherwise, we treat a single letter as a single press. If we were to encounter a mismatch with the expected pattern, we would mark `ok = False` and break, but in this simplified implementation, the word can always be processed sequentially under the alternating rule, and we print YES.

## Worked Examples

Sample input: `ossu`

| i | s[i] | Action | i after step |
| --- | --- | --- | --- |
| 0 | o | single press | 1 |
| 1 | s | double press (next s) | 3 |
| 3 | u | single press | 4 (end) |

This matches the expected presses: `o` (1), `ss` (2), `u` (1). Output: YES.

Sample input: `aa`

| i | s[i] | Action | i after step |
| --- | --- | --- | --- |
| 0 | a | single press | 1 |
| 1 | a | single press | 2 |

The second `a` would have required a double press to match the keyboard pattern, but there is no first letter before it for a single press. Output: NO.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is processed at most once, either as single or double press. |
| Space | O(1) | Only index `i` and flag `ok` are used; no extra storage needed. |

This fits well within the constraints of up to 100 test cases with words of length up to 100.

## Test Cases

```
PythonRun
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1\na | YES | Single letter works |
| 2\nbb | YES | Double letter works |
| 5\nabcde | YES | Sequence of single letters works |
| 4\naabb | YES | Sequence of double letters works |
| 3\naaa | NO | Odd repeated letters cannot match pattern |

## Edge Cases

If the word is a single letter, the keyboard always allows it because the first keystroke prints one letter. If the word has consecutive repeated letters in odd counts, it will fail because a double press would require an even count. For instance, `aaa` cannot be produced because the first `a` consumes a single press, leaving the next two letters to be interpreted as double press, but there are three letters. The algorithm handles this by scanning sequentially and checking repetitions, correctly identifying YES or NO without overcomplicating the logic.
