---
title: "CF 188E - HQ9+"
description: "We are given a single string representing a program written in the joke language HQ9+. Most characters do nothing, but four specific uppercase characters are meaningful. The instruction H prints \"Hello, World!"
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special", "implementation"]
categories: ["algorithms"]
codeforces_contest: 188
codeforces_index: "E"
codeforces_contest_name: "Surprise Language Round 6"
rating: 1400
weight: 188
solve_time_s: 77
verified: true
draft: false
---

[CF 188E - HQ9+](https://codeforces.com/problemset/problem/188/E)

**Rating:** 1400  
**Tags:** *special, implementation  
**Solve time:** 1m 17s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single string representing a program written in the joke language HQ9+. Most characters do nothing, but four specific uppercase characters are meaningful.

The instruction `H` prints `"Hello, World!"`, the instruction `Q` prints the program itself, and the instruction `9` prints the lyrics of `"99 Bottles of Beer"`. The instruction `+` only changes an internal accumulator and does not print anything.

The task is much simpler than simulating the language completely. We only need to decide whether the program produces any output at all. That means we only care whether the string contains at least one of the output-producing instructions: `H`, `Q`, or `9`.

The input length is at most 100 characters, which is tiny. Even an inefficient solution would run instantly. A single linear scan over the string is more than enough.

The main trap is misunderstanding which characters actually produce output. The character `+` is a valid HQ9+ instruction, but it does not print anything.

Consider this input:

```
+++++
```

The correct answer is:

```
NO
```

A careless implementation that checks for any HQ9+ instruction instead of specifically output-producing instructions would incorrectly print `YES`.

Case sensitivity is another detail that can quietly break solutions.

For example:

```
hq9
```

The correct answer is:

```
YES
```

because `9` is valid and prints output, but lowercase `h` and `q` are ignored. If the string were:

```
hq
```

the answer would be:

```
NO
```

because lowercase letters are not instructions.

## Approaches

The most direct approach is to simulate the program instruction by instruction. For each character, we could check whether it is `H`, `Q`, `9`, or `+`, and then imitate the corresponding behavior. If we encounter `H`, `Q`, or `9`, we know output occurs and can stop immediately.

This brute-force simulation is already fast enough because the string length is at most 100. Even printing the hypothetical outputs would still be manageable at this scale.

The problem becomes even simpler once we observe what the question is actually asking. We are not asked to execute the program or generate its output. We only need to know whether any output exists.

Only three characters can ever print something: `H`, `Q`, and `9`. The `+` instruction changes internal state but never produces visible output. Every other character is ignored completely.

That observation reduces the task to a membership check. We scan the string once and ask whether any character belongs to the set `{H, Q, 9}`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n) | O(1) | Accepted |
| Optimal Character Check | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the input string representing the HQ9+ program.
2. Scan the string character by character.
3. For each character, check whether it is one of `H`, `Q`, or `9`.
4. If such a character exists, print `YES` immediately because at least one instruction produces output.
5. If the scan finishes without finding any of these characters, print `NO`.

### Why it works

The language has exactly three output-producing instructions: `H`, `Q`, and `9`. Any program containing at least one of them must print something during execution. Every other character either does nothing or only changes internal state without producing output.

The algorithm checks exactly this condition and nothing else, so it cannot misclassify any program.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().strip()

if any(c in "HQ9" for c in s):
    print("YES")
else:
    print("NO")
```

The program reads the input string and performs a single linear scan.

The expression:

```
any(c in "HQ9" for c in s)
```

checks whether at least one character belongs to the set of output-producing instructions.

Using `"HQ9"` instead of `"HQ9+"` is the key detail. The `+` instruction modifies the accumulator but never prints anything, so it must not trigger a `YES`.

The `.strip()` call removes the trailing newline from input. Without it, the newline character would also be scanned, although it would not affect correctness here.

## Worked Examples

### Example 1

Input:

```
Hello!
```

| Position | Character | Output-producing? | Result |
| --- | --- | --- | --- |
| 0 | H | Yes | Stop, answer is YES |

Output:

```
YES
```

The first character is `H`, which prints `"Hello, World!"`. The algorithm immediately knows the program produces output.

### Example 2

Input:

```
++++
```

| Position | Character | Output-producing? | Result |
| --- | --- | --- | --- |
| 0 | + | No | Continue |
| 1 | + | No | Continue |
| 2 | + | No | Continue |
| 3 | + | No | Continue |

Output:

```
NO
```

This trace demonstrates the most common trap. The program contains valid HQ9+ instructions, but none of them print anything.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | The string is scanned once |
| Space | O(1) | Only a few variables are used |

With at most 100 characters, the solution runs essentially instantly. The memory usage is constant and far below the limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    import sys
    input = sys.stdin.readline

    s = input().strip()

    if any(c in "HQ9" for c in s):
        print("YES")
    else:
        print("NO")

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()

    backup_stdout = sys.stdout
    sys.stdout = out

    solve()

    sys.stdout = backup_stdout
    return out.getvalue()

# provided sample
assert run("Hello!\n") == "YES\n", "sample 1"

# custom cases
assert run("+++++\n") == "NO\n", "plus does not print"
assert run("qwerty\n") == "NO\n", "lowercase letters ignored"
assert run("9\n") == "YES\n", "single output instruction"
assert run(("A" * 99) + "Q\n") == "YES\n", "output instruction at end"
assert run("H\n") == "YES\n", "minimum positive case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `+++++` | `NO` | `+` is not output-producing |
| `qwerty` | `NO` | Lowercase letters are ignored |
| `9` | `YES` | Single valid instruction works |
| `AAAA...AAQ` | `YES` | Finds instruction at the end |
| `H` | `YES` | Minimum positive input |

## Edge Cases

Consider the input:

```
+++++
```

The algorithm scans every character and checks membership in `"HQ9"`. Since `+` is not included, no match is found and the final answer is `NO`.

This correctly handles the distinction between valid instructions and output-producing instructions.

Now consider:

```
hq
```

The scan sees lowercase `h` and lowercase `q`. Neither matches uppercase `H` or `Q`, so the algorithm prints:

```
NO
```

This confirms the implementation respects the language's case sensitivity.

Finally, consider:

```
abc9xyz
```

The algorithm skips irrelevant characters until it reaches `9`. Since `9` prints output, the algorithm immediately concludes the answer is:

```
YES
```

This demonstrates that non-instruction characters do not interfere with detection.
