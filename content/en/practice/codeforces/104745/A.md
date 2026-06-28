---
title: "CF 104745A - Saving the cinema"
description: "The task is to build a tiny classifier that reads a single name and returns a fixed sentence depending on which fictional universe that name belongs to. The input is always exactly one of three possible character names."
date: "2026-06-28T23:01:51+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104745
codeforces_index: "A"
codeforces_contest_name: "CAMA 2023"
rating: 0
weight: 104745
solve_time_s: 45
verified: true
draft: false
---

[CF 104745A - Saving the cinema](https://codeforces.com/problemset/problem/104745/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 45s  
**Verified:** yes  

## Solution
## Problem Understanding

The task is to build a tiny classifier that reads a single name and returns a fixed sentence depending on which fictional universe that name belongs to. The input is always exactly one of three possible character names. Each name maps to a specific universe: one corresponds to Star Wars, another corresponds to Star Trek, and the last one does not belong to either.

From an algorithmic perspective, the input space is constant sized. There is no parsing ambiguity, no hidden structure, and no computation beyond equality checks against known strings. This places the problem firmly in the category where any asymptotically optimal solution is trivial, and performance constraints do not influence design decisions.

Even though the logic is simple, there are still a couple of implementation pitfalls. A naive attempt might involve partial matching instead of exact string comparison. For example, checking whether the input contains the substring “o” would incorrectly match all three inputs, leading to ambiguous or incorrect classification.

Another subtle failure mode appears when handling whitespace or newline characters. If the input is not stripped properly, a direct equality comparison against “Yoda”, “Spock”, or “Frodo” will fail even though the logical value matches. For instance, reading input as `"Yoda\n"` and comparing directly to `"Yoda"` would produce a mismatch unless input is normalized.

A third edge case is incorrect capitalization handling. The problem specifies exact strings, so treating input in a case insensitive manner would incorrectly accept variants like “yoda” or “YODA”, which should not be considered valid.

## Approaches

A brute-force strategy in this context would still be direct comparison against each possible valid string using a sequence of conditional checks. Even if implemented inefficiently, such as scanning through a list of candidates and comparing character by character, the total work remains constant because the number of valid strings is fixed at three and their lengths are bounded.

A more structured approach is to explicitly map each input string to its corresponding output sentence using a dictionary or chained conditionals. This removes any ambiguity and makes the transformation direct: each key corresponds to exactly one output string.

The key observation is that the domain is finite and known ahead of time. This reduces the problem from a general string classification task to a lookup table problem with constant time resolution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (manual comparisons) | O(1) | O(1) | Accepted |
| Direct mapping (dictionary / if-else) | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the input string from standard input and remove trailing whitespace so that formatting artifacts do not affect comparisons. This ensures the string is in a normalized form suitable for exact matching.
2. Compare the normalized string against the three known valid cases. Each comparison is a full string equality check, which is sufficient because the set of valid inputs is fixed and small.
3. If the string matches “Yoda”, output the sentence indicating membership in Star Wars.
4. If the string matches “Spock”, output the sentence indicating membership in Star Trek.
5. If the string matches “Frodo”, output the sentence stating that it belongs to neither universe.

Each branch is mutually exclusive, so exactly one output is produced.

### Why it works

The correctness rests on the fact that the input domain contains exactly three possible values, and each value is associated with exactly one output. Because equality comparison partitions the input space into disjoint cases that cover all possibilities, every valid input is handled uniquely. There is no possibility of overlap or missing cases since the mapping is exhaustive over the allowed set.

## Python Solution

```python
import sys

def solve():
    s = sys.stdin.readline().strip()

    if s == "Yoda":
        print("Pertenece a Star Wars.")
    elif s == "Spock":
        print("Pertenece a Star Trek.")
    else:
        print("No pertenece ni a Star Wars ni a Star Trek.")

if __name__ == "__main__":
    solve()
```

The solution reads a single line, normalizes it using `strip`, and then performs a direct comparison chain. The `strip` call is essential because input from standard input typically includes a trailing newline, which would otherwise break exact equality checks.

The conditional structure is intentionally ordered so that the two known universe memberships are checked first. The final `else` branch safely handles the only remaining valid input, “Frodo”, since the problem guarantees that input is always one of the three allowed strings.

## Worked Examples

### Example 1

Input is “Spock”.

| Step | Current string | Condition checked | Result |
| --- | --- | --- | --- |
| 1 | Spock | strip applied | Spock |
| 2 | Spock | equals "Yoda" | false |
| 3 | Spock | equals "Spock" | true |
| 4 | Spock | output printed | Star Trek sentence |

This trace shows that the second comparison succeeds immediately, and no further branching is needed.

### Example 2

Input is “Frodo”.

| Step | Current string | Condition checked | Result |
| --- | --- | --- | --- |
| 1 | Frodo | strip applied | Frodo |
| 2 | Frodo | equals "Yoda" | false |
| 3 | Frodo | equals "Spock" | false |
| 4 | Frodo | falls to else | true |
| 5 | Frodo | output printed | neither universe sentence |

This confirms that the fallback branch correctly captures the only remaining valid case.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a constant number of string comparisons are performed |
| Space | O(1) | No additional data structures are used beyond a single input string |

The constant time behavior is sufficient for any reasonable input size, and the memory footprint does not grow with input because the problem processes exactly one string.

## Test Cases

```python
import sys, io
from contextlib import redirect_stdout

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided samples
assert run("Spock") == "Pertenece a Star Trek."
assert run("Yoda") == "Pertenece a Star Wars."
assert run("Frodo") == "No pertenece ni a Star Wars ni a Star Trek."

# custom cases
assert run("Yoda\n") == "Pertenece a Star Wars.", "newline handling"
assert run("Spock ") == "Pertenece a Star Trek.", "trailing space handling"
assert run("Frodo") == "No pertenece ni a Star Wars ni a Star Trek.", "neutral case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `"Yoda\n"` | Star Wars sentence | newline normalization |
| `"Spock "` | Star Trek sentence | trailing whitespace handling |
| `"Frodo"` | neither sentence | fallback correctness |

## Edge Cases

The most relevant edge case is the presence of hidden whitespace characters in the input. If the input arrives as “Yoda\n”, a direct comparison without normalization would fail. In the implementation, the `strip()` call ensures that the internal value becomes exactly “Yoda”, after which the first condition evaluates to true and the correct Star Wars sentence is produced.

Another case is trailing spaces, such as “Spock ”. After stripping, the string becomes “Spock”, so the second condition matches and the Star Trek sentence is printed. This demonstrates that normalization happens before classification, ensuring robustness against formatting noise.

The final case is the guaranteed fallback input “Frodo”. Since it does not match either of the first two conditions, execution naturally falls into the final branch and produces the correct “neither” response without requiring an explicit equality check.
