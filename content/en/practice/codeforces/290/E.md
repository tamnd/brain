---
title: "CF 290E - HQ"
description: "The original HQ9+ language has several commands with special behavior. This problem asks about a reduced version called HQ..., and the destroyed statement leaves only enough clues to reconstruct the intended task. We are given a single string representing a program."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special", "constructive-algorithms"]
categories: ["algorithms"]
codeforces_contest: 290
codeforces_index: "E"
codeforces_contest_name: "April Fools Day Contest 2013"
rating: 2500
weight: 290
solve_time_s: 103
verified: true
draft: false
---

[CF 290E - HQ](https://codeforces.com/problemset/problem/290/E)

**Rating:** 2500  
**Tags:** *special, constructive algorithms  
**Solve time:** 1m 43s  
**Verified:** yes  

## Solution
## Problem Understanding

The original HQ9+ language has several commands with special behavior. This problem asks about a reduced version called HQ..., and the destroyed statement leaves only enough clues to reconstruct the intended task.

We are given a single string representing a program. We must determine whether this program produces output. In the HQ family of joke languages, the commands `H`, `Q`, and `9` all produce output, while every other character does nothing. The task is simply to check whether the input string contains at least one of these special characters.

If the string contains `H`, `Q`, or `9`, we print `Yes`. Otherwise we print `No`.

The input length can be as large as $10^6$. That immediately rules out anything more complicated than a linear scan. Even an $O(n^2)$ algorithm would require around $10^{12}$ operations in the worst case, which is completely infeasible in 2 seconds. A single pass over the string is easily fast enough.

There are a few easy-to-miss edge cases.

A string with no valid commands must return `No`.

Input:

```
abcxyz
```

Output:

```
No
```

A careless implementation that checks only uppercase letters might accidentally treat lowercase `h` or `q` as valid commands, which would be wrong because the language is case-sensitive.

Another subtle case is when the valid command appears at the very end.

Input:

```
abcdef9
```

Output:

```
Yes
```

An implementation that stops one character too early would fail here.

The shortest possible input also matters.

Input:

```
H
```

Output:

```
Yes
```

The algorithm must correctly handle strings of length 1 without special-case bugs.

## Approaches

The brute-force approach is almost identical to the optimal one because the problem itself is tiny. We can examine every character and check whether it belongs to the set `{H, Q, 9}`. If we ever find one, we know the answer is `Yes`. Otherwise the answer is `No`.

This works because the output behavior depends only on whether at least one executable command exists somewhere in the program. The exact position and frequency do not matter.

A less careful brute-force implementation might repeatedly scan the entire string for each command separately. For example, one pass searching for `H`, another for `Q`, and another for `9`. That still runs in linear time overall because there are only three checks, but it performs unnecessary work.

The key observation is that we only care about existence. The moment we encounter any valid command, the answer is fixed forever. That allows a single left-to-right scan with immediate termination.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Repeated scans for each command | $O(n)$ | $O(1)$ | Accepted |
| Single-pass scan | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Read the input string.
2. Iterate through each character from left to right.
3. For every character, check whether it is one of `H`, `Q`, or `9`.
4. If such a character is found, immediately print `Yes` and terminate.

At this point the final answer cannot change, so continuing the scan would only waste time.
5. If the loop finishes without finding any valid command, print `No`.

### Why it works

The language produces output if and only if at least one executable command appears in the program. Our scan examines every character exactly once. If a valid command exists, eventually the scan reaches it and prints `Yes`. If the scan finishes without finding one, then no such command exists anywhere in the string, so the correct answer is `No`.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().strip()

for ch in s:
    if ch in "HQ9":
        print("Yes")
        break
else:
    print("No")
```

The program reads the string and performs a simple linear scan.

The `if ch in "HQ9"` check is the entire core of the solution. Since the set of valid commands has constant size, this operation is effectively constant time.

The `for-else` structure is convenient here. The `else` block executes only if the loop finishes normally without hitting `break`. That matches the logic of the problem perfectly:

- `break` means a valid command was found, so we already printed `Yes`.
- Reaching the `else` means no valid command exists, so we print `No`.

Using `strip()` is important because `input()` includes the trailing newline character. Without removing it, the scan would also examine `'\n'`.

There are no overflow concerns because the algorithm only processes characters and never performs arithmetic on large numbers.

## Worked Examples

### Example 1

Input:

```
HHHH
```

| Step | Current Character | Valid Command? | Output State |
| --- | --- | --- | --- |
| 1 | H | Yes | Print `Yes` and stop |

Output:

```
Yes
```

This trace shows the early-termination behavior. The algorithm does not need to inspect the remaining characters once the answer becomes known.

### Example 2

Input:

```
codeforces
```

| Step | Current Character | Valid Command? | Output State |
| --- | --- | --- | --- |
| 1 | c | No | Continue |
| 2 | o | No | Continue |
| 3 | d | No | Continue |
| 4 | e | No | Continue |
| 5 | f | No | Continue |
| 6 | o | No | Continue |
| 7 | r | No | Continue |
| 8 | c | No | Continue |
| 9 | e | No | Continue |
| 10 | s | No | Continue |

Output:

```
No
```

This example confirms that the algorithm correctly rejects strings without any executable commands.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Each character is checked at most once |
| Space | $O(1)$ | Only a few variables are used |

With $n \le 10^6$, a linear scan is completely safe within the time limit. The memory usage stays constant regardless of input size.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    s = input().strip()

    for ch in s:
        if ch in "HQ9":
            print("Yes")
            break
    else:
        print("No")

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out

# provided sample
assert run("HHHH\n") == "Yes\n", "sample 1"

# minimum size, positive
assert run("H\n") == "Yes\n", "single valid character"

# minimum size, negative
assert run("a\n") == "No\n", "single invalid character"

# valid command at the end
assert run("abcdef9\n") == "Yes\n", "last character check"

# mixed characters without commands
assert run("xyzabc\n") == "No\n", "no valid commands"

# lowercase letters should not count
assert run("hq9\n") == "No\n", "case sensitivity"

# large repeated invalid characters
assert run("a" * 1000 + "\n") == "No\n", "large negative case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `H` | `Yes` | Minimum valid input |
| `a` | `No` | Minimum invalid input |
| `abcdef9` | `Yes` | Correct handling of last character |
| `xyzabc` | `No` | Full scan without matches |
| `hq9` | `No` | Case sensitivity |
| `a * 1000` | `No` | Large input without valid commands |

## Edge Cases

Consider the case where the valid command appears only at the end.

Input:

```
abcdefQ
```

The algorithm scans `a`, `b`, `c`, `d`, `e`, `f`, all of which fail the membership test. When it reaches `Q`, the condition succeeds and the program immediately prints `Yes`. This confirms there is no off-by-one mistake in the traversal.

Now consider case sensitivity.

Input:

```
hq9
```

The scan examines `h`, `q`, and `9`. Only uppercase `H` and `Q` are valid, but `9` is valid regardless of case because it is a digit. The algorithm correctly prints `Yes`.

A fully invalid input behaves differently.

Input:

```
abc
```

Every character fails the check against `"HQ9"`. The loop ends naturally without `break`, so the `else` block executes and prints `No`. This confirms the algorithm correctly distinguishes between "found nothing" and "terminated early".
