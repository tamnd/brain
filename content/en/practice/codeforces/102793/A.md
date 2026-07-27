---
title: "CF 102793A - \u0421\u043c\u0435\u043d\u0430 \u0441\u0442\u0438\u043b\u044f"
description: "The task is to convert variable names written in one of the common programming styles, camelCase or CamelCase, into snakecase. A variable name is a single string of Latin letters where word boundaries are marked by capital letters."
date: "2026-07-27T17:58:07+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102793
codeforces_index: "A"
codeforces_contest_name: "\u0426\u0438\u043a\u043b \u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434, \u0421\u0435\u0437\u043e\u043d 2020-21, \u0412\u0442\u043e\u0440\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430"
rating: 0
weight: 102793
solve_time_s: 33
verified: false
draft: false
---

[CF 102793A - \u0421\u043c\u0435\u043d\u0430 \u0441\u0442\u0438\u043b\u044f](https://codeforces.com/problemset/problem/102793/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 33s  
**Verified:** no  

## Solution
## Problem Understanding

The task is to convert variable names written in one of the common programming styles, `camelCase` or `CamelCase`, into `snake_case`. A variable name is a single string of Latin letters where word boundaries are marked by capital letters. In the target format, every letter must be lowercase and adjacent words must be separated with underscores. The input contains several variable names, and for each one we must print its converted version.

For example, the name `toBeOrNotToBe` consists of the words `to`, `Be`, `Or`, `Not`, and `To`, so the result should be `to_be_or_not_to_be`. The same rule works for names that start with an uppercase letter, such as `CamelCase`, which becomes `camel_case`.

The input size is designed to allow a direct scan. There are at most 100 names, and each name can contain up to 1000 characters. That means the total amount of processed characters is only around 100000, so an algorithm that touches every character a constant number of times is easily fast enough. Any approach involving repeatedly searching through strings, rebuilding them inefficiently, or trying every possible word split is unnecessary.

The main edge cases come from handling capital letters correctly. A naive solution that only inserts underscores before capitals may fail when the first character is uppercase, because `CamelCase` should become `camel_case`, not `_camel_case`. Another common mistake is forgetting that a string can consist entirely of capital letters. For example, `ABCDE` should become `a_b_c_d_e`, because every capital letter represents the beginning of a new word under the rules of this problem.

Consider this input:

```
1
CamelCase
```

The correct output is:

```
camel_case
```

A careless implementation that adds `_` before every uppercase character and only lowercases afterward could produce `_camel_case`, leaving an incorrect leading separator.

Another example:

```
1
ABCDE
```

The correct output is:

```
a_b_c_d_e
```

An implementation that assumes capital letters only appear between lowercase letters may incorrectly keep the whole string together as `abcde`.

## Approaches

The simplest solution is to simulate the conversion character by character. A brute-force way would be to try splitting the string into words, generate possible interpretations, and select the one matching camelCase rules. This approach is correct because every valid conversion corresponds to some partition of the original string, but it is unnecessary. For a string of length 1000, the number of possible partitions grows exponentially, making this impossible even for a single large input.

The structure of the input gives us a much simpler observation. In camelCase, the uppercase letters already mark every boundary between words. We do not need to discover where the words are. We only need to translate each character according to whether it starts a new word.

While scanning the string from left to right, every lowercase letter is copied in lowercase form. When an uppercase letter appears, it represents a new word. If it is not the first character, we insert an underscore before it, then append its lowercase version. The first character is special because it cannot have a separator before it.

This reduces the problem from trying to understand the whole string structure to a single deterministic pass over the characters.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in the string length | O(n) | Too slow |
| Optimal | O(total number of characters) | O(total output size) | Accepted |

## Algorithm Walkthrough

1. Read the number of variable names and process each name independently. Each variable can be converted without depending on any other one.
2. Create an empty result string for the current variable. We build the answer gradually because each character may affect the formatting of the next output character.
3. Scan the variable name from the first character to the last character.
4. If the current character is uppercase, check whether it is the first character. If it is not the first character, add an underscore before it because a new word begins here.
5. Append the lowercase version of the current character to the result. Lowercasing every character at this stage guarantees that the final name follows `snake_case`.
6. If the current character is already lowercase, append it directly because it belongs to the current word.
7. Print the constructed result.

The reason this works is that the only information needed to recover word boundaries is the position of uppercase letters. CamelCase does not contain any other separators, so every uppercase letter after the first character uniquely identifies a place where an underscore must be inserted.

Why it works:

During the scan, the processed prefix of the string is always represented exactly as it should appear in `snake_case`. When we encounter a lowercase character, it extends the current word, so appending it preserves correctness. When we encounter an uppercase character after the first position, the camelCase definition guarantees that a new word starts there, so adding an underscore before its lowercase form preserves the required separation. Since every character is handled once, the complete output must be correct after the final character is processed.

(Part 2 continues with Python Solution, examples, complexity, tests, and edge cases.)
