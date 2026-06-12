---
title: "CF 908A - New Year and Counting Cards"
description: "We see one side of every card. A visible side can be either a lowercase letter or a digit. The statement we want to verify is: \"Whenever a card has a vowel on one side, the other side contains an even digit.\" We may flip some cards."
date: "2026-06-12T10:28:05+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation"]
categories: ["algorithms"]
codeforces_contest: 908
codeforces_index: "A"
codeforces_contest_name: "Good Bye 2017"
rating: 800
weight: 908
solve_time_s: 94
verified: true
draft: false
---

[CF 908A - New Year and Counting Cards](https://codeforces.com/problemset/problem/908/A)

**Rating:** 800  
**Tags:** brute force, implementation  
**Solve time:** 1m 34s  
**Verified:** yes  

## Solution
## Problem Understanding

We see one side of every card. A visible side can be either a lowercase letter or a digit.

The statement we want to verify is:

"Whenever a card has a vowel on one side, the other side contains an even digit."

We may flip some cards. The task is to find the minimum number of cards that must be checked in the worst case to determine whether the statement is true for all cards.

The key observation is that this is a logical implication:

> vowel ⇒ even digit

To verify an implication, we only need to inspect cards that could possibly violate it.

The input length is at most 50, which is tiny. Even quadratic or cubic solutions would fit comfortably. The challenge is not performance but identifying exactly which cards matter.

A common mistake is to flip every vowel and every digit. Some visible cards can never contradict the rule, so checking them provides no information.

Consider the card showing the consonant `b`.

```
b
```

No matter what is on the other side, this card cannot violate the implication. If the hidden side is an odd digit, the visible side is still not a vowel. If the hidden side is a letter, the implication is irrelevant. The correct contribution is 0 flips.

Another easy mistake is to ignore odd digits.

```
1
```

If the hidden side is `a`, the card would become a counterexample: vowel on one side and odd digit on the other. We must flip such cards. The correct answer is 1.

A more subtle case is the digit `0`.

```
0
```

Since `0` is even, a hidden vowel would still satisfy the rule. This card can never disprove the implication, so it does not need to be flipped. Treating all digits equally would incorrectly count it.

## Approaches

A brute-force way to think about the problem is to examine every visible character and ask whether flipping that card could reveal a violation of the statement. Since there are at most 50 cards, we could manually classify each one. This already runs in linear time.

The real challenge is determining the correct classification.

A card must be checked if its visible side is a vowel. The hidden side must then be even, and we cannot know that without looking.

A card must also be checked if its visible side is an odd digit. If the hidden side happens to be a vowel, the statement would be false.

All other cards are irrelevant.

For consonants, the implication places no restriction on the opposite side. A consonant paired with an odd digit is perfectly valid.

For even digits, a hidden vowel would still satisfy the implication because the digit is even.

This observation reduces the entire problem to counting two groups:

1. Visible vowels.
2. Visible odd digits.

The answer is simply the size of their union.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force classification of every card | O(n) | O(1) | Accepted |
| Optimal counting of vowels and odd digits | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the input string.
2. Create a set containing the vowels: `a`, `e`, `i`, `o`, `u`.
3. Create a set containing the odd digits: `1`, `3`, `5`, `7`, `9`.
4. Initialize the answer to 0.
5. Scan each character in the string.
6. If the character is a vowel, increment the answer.

We must inspect such a card because the hidden side is required to be an even digit.
7. Otherwise, if the character is an odd digit, increment the answer.

We must inspect such a card because the hidden side might be a vowel, creating a violation.
8. Ignore all remaining characters.

These are consonants and even digits, neither of which can directly violate the implication.
9. Print the final count.

### Why it works

The implication can only be violated by a card whose two sides are:

```
vowel + odd digit
```

If a visible card already shows a vowel, we must check whether the hidden side is odd. If a visible card already shows an odd digit, we must check whether the hidden side is a vowel.

Every possible counterexample is detected by examining exactly these cards. Conversely, a visible consonant or even digit can never participate in a violation regardless of what is hidden on the other side. Counting visible vowels and visible odd digits is both necessary and sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().strip()

vowels = {'a', 'e', 'i', 'o', 'u'}
odd_digits = {'1', '3', '5', '7', '9'}

ans = 0

for ch in s:
    if ch in vowels or ch in odd_digits:
        ans += 1

print(ans)
```

The implementation follows the reasoning directly.

The vowel set contains exactly the letters that trigger the implication. Whenever one appears, the corresponding card must be flipped.

The odd-digit set contains exactly the digits that could violate the implication if a vowel is hidden on the opposite side.

The condition uses a logical OR because either situation requires inspection. No character can belong to both groups, but the OR expresses the rule naturally and keeps the code simple.

The input size is tiny, so a single linear scan is more than sufficient.

## Worked Examples

### Example 1

Input:

```
ee
```

| Character | Vowel? | Odd Digit? | Answer |
| --- | --- | --- | --- |
| e | Yes | No | 1 |
| e | Yes | No | 2 |

Final answer:

```
2
```

Both visible cards show vowels. Each must be checked because its hidden side is required to be even.

### Example 2

Input:

```
bcdf
```

| Character | Vowel? | Odd Digit? | Answer |
| --- | --- | --- | --- |
| b | No | No | 0 |
| c | No | No | 0 |
| d | No | No | 0 |
| f | No | No | 0 |

Final answer:

```
0
```

Every visible card is a consonant. The implication only constrains cards containing vowels, so no flips are needed.

### Example 3

Input:

```
a0b7
```

| Character | Vowel? | Odd Digit? | Answer |
| --- | --- | --- | --- |
| a | Yes | No | 1 |
| 0 | No | No | 1 |
| b | No | No | 1 |
| 7 | No | Yes | 2 |

Final answer:

```
2
```

The vowel `a` must be checked, and the odd digit `7` must also be checked. The even digit `0` and consonant `b` are irrelevant.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One pass through the string |
| Space | O(1) | Only a few small fixed-size sets are stored |

With at most 50 characters, the algorithm performs only a handful of operations. It easily fits within the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    s = input().strip()

    vowels = {'a', 'e', 'i', 'o', 'u'}
    odd_digits = {'1', '3', '5', '7', '9'}

    ans = 0
    for ch in s:
        if ch in vowels or ch in odd_digits:
            ans += 1

    return str(ans)

# provided sample
assert run("ee\n") == "2", "sample 1"

# custom cases
assert run("b\n") == "0", "single consonant"
assert run("1\n") == "1", "single odd digit"
assert run("0\n") == "0", "single even digit"
assert run("aeiou\n") == "5", "all vowels"
assert run("13579\n") == "5", "all odd digits"
assert run("24680\n") == "0", "all even digits"
assert run("a0b7\n") == "2", "mixed case"
assert run(("a" * 50) + "\n") == "50", "maximum length"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `b` | `0` | Consonants do not need checking |
| `1` | `1` | Odd digits must be checked |
| `0` | `0` | Even digits are safe |
| `aeiou` | `5` | Every vowel contributes |
| `13579` | `5` | Every odd digit contributes |
| `24680` | `0` | No relevant cards |
| `a0b7` | `2` | Mixed classification |
| `a` repeated 50 times | `50` | Maximum input length |

## Edge Cases

Consider a card showing only a consonant:

```
b
```

The algorithm checks whether `b` is a vowel or an odd digit. It is neither, so the answer remains 0. This is correct because no hidden value can make a consonant violate the implication.

Consider a card showing an odd digit:

```
1
```

The algorithm recognizes `1` as an odd digit and increments the answer to 1. We must inspect this card because the hidden side could be a vowel, creating the forbidden combination `(vowel, odd digit)`.

Consider a card showing an even digit:

```
0
```

The algorithm does not count it. If the hidden side is a vowel, the rule is still satisfied because the digit is even. If the hidden side is not a vowel, the rule is also satisfied. No flip is needed.

Consider a string with no vowels at all:

```
bcdf
```

Every character is ignored. The answer is 0, which matches the fact that the implication is automatically true when no vowel appears on any card side currently visible.
