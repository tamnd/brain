---
title: "CF 106169B - Nostalgia"
description: "The program being analyzed is written in Scratch and consists of simple commands that read values, store them in variables, calculate new values, and print results. During their early testing, the programmers used an extra debugging output before every input operation."
date: "2026-06-25T11:07:47+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106169
codeforces_index: "B"
codeforces_contest_name: "2025-2026 ICPC NERC, Kyrgyzstan Regional Contest"
rating: 0
weight: 106169
solve_time_s: 37
verified: true
draft: false
---

[CF 106169B - Nostalgia](https://codeforces.com/problemset/problem/106169/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 37s  
**Verified:** yes  

## Solution
## Problem Understanding

The program being analyzed is written in Scratch and consists of simple commands that read values, store them in variables, calculate new values, and print results. During their early testing, the programmers used an extra debugging output before every input operation. That extra output was simply the name of the variable that was about to receive the input, which helped them understand what value the program was waiting for.

The task is to calculate how many characters were printed by these additional debugging outputs. The final submitted version of the program would not contain those outputs, so only the variable names connected to input operations contribute to the answer.

The input contains the number of program lines followed by the commands themselves. Among all possible commands, only the lines that store the special temporary value `answer` into a variable represent an input operation. For every such line, the length of the destination variable name must be added to the result.

The number of lines can reach 100000, so the solution must inspect each line a constant number of times. An approach that simulates the Scratch program or tries to evaluate every variable value would do unnecessary work. A linear scan is enough because the answer depends only on the names of variables receiving input.

A common mistake is to count every variable name that appears in the program. For example:

```
6
Ask read_token and wait
Set first to answer
Set result to first + second
Say result
Ask read_token and wait
Set second to answer
```

The correct output is:

```
11
```

Only `first` and `second` were used for input, contributing `5 + 6 = 11`. Counting `result` would incorrectly add characters from a variable that was only calculated.

Another edge case is repeated input into the same variable:

```
8
Ask read_token and wait
Set a to answer
Ask read_token and wait
Set a to answer
Set b to a + a
Say b
Ask read_token and wait
Set c to answer
```

The correct output is:

```
3
```

The variable `a` contributes twice and `c` contributes once, so the total is `1 + 1 + 1 = 3`. A careless implementation that counts unique variable names would return `2`, which is incorrect.

## Approaches

The straightforward approach is to understand every command in the Scratch program, track variables, and simulate execution. This would be correct because it follows the exact behavior of the original program. However, it solves a much harder problem than necessary. The values stored in variables, arithmetic operations, and printed results never affect the answer. If every operation were simulated, the implementation would spend time maintaining information that is irrelevant.

The key observation is that the additional output happened only immediately before an input. The statement guarantees that every input request is paired with exactly one assignment from `answer`, and every such assignment follows an input request. This means every line of the form `Set name to answer` directly reveals one variable name that was printed during testing.

The problem is reduced to string processing. We only need to recognize those assignment lines and add the length of the variable name appearing after `Set`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) with unnecessary simulation work | O(number of variables) | Correct but overcomplicated |
| Optimal | O(n) | O(1) extra space | Accepted |

## Algorithm Walkthrough

1. Read the number of lines in the Scratch program and process the commands one by one. Since every line can be inspected independently, there is no need to store the entire program.
2. For every line that represents `Set name to answer`, extract `name` and add its length to the answer. This is the only command type that corresponds to an additional local testing output.
3. Ignore all other commands because they either manipulate values internally or display the final program output. They do not create extra debugging characters.
4. Print the accumulated total.

Why it works:

The invariant maintained during the scan is that after processing any prefix of the program, the stored answer equals the number of extra characters produced by all input operations inside that prefix. A line contributes only when it stores `answer` into a variable, and in that case the local testing output would have been exactly that variable name. Every such line is counted once, and no other line can contribute. After the complete scan, the invariant gives the required total.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    ans = 0

    for _ in range(n):
        line = input().strip()
        if line.startswith("Set ") and line.endswith(" to answer"):
            name = line[4:line.index(" to answer")]
            ans += len(name)

    print(ans)

if __name__ == "__main__":
    solve()
```

The code reads each Scratch command exactly once. The condition checks both parts that identify an input assignment: the command must begin with `Set`, and the value assigned must be the reserved word `answer`.

The variable name is located between the fixed prefix `Set ` and the suffix ` to answer`. Using the position of the suffix avoids depending on variable length and handles all valid names correctly.

The implementation does not store commands or variables because no information from previous lines is needed. The integer answer can reach up to `10^9`, which Python handles without overflow concerns.

## Worked Examples

### Example 1

Input:

```
6
Ask read_token and wait
Set first to answer
Ask read_token and wait
Set second to answer
Set result to first + second
Say result
```

| Step | Command | Recognized input variable | Current answer |
| --- | --- | --- | --- |
| 1 | Ask read_token and wait | none | 0 |
| 2 | Set first to answer | first | 5 |
| 3 | Ask read_token and wait | none | 5 |
| 4 | Set second to answer | second | 11 |
| 5 | Set result to first + second | none | 11 |
| 6 | Say result | none | 11 |

The trace shows that only variables receiving user input matter. Calculated variables such as `result` are ignored.

### Example 2

Input:

```
15
Ask read_token and wait
Set a to answer
Ask read_token and wait
Set bb to answer
Set ccc to a * bb
Set dddd to a / bb
Set dddd to ccc + dddd
Say dddd
Ask read_token and wait
Set bb to answer
Ask read_token and wait
Set ccc to answer
Set x to bb * dddd
Set x to ccc - x
Say x
```

| Step | Command | Recognized input variable | Current answer |
| --- | --- | --- | --- |
| 1 | Ask read_token and wait | none | 0 |
| 2 | Set a to answer | a | 1 |
| 3 | Ask read_token and wait | none | 1 |
| 4 | Set bb to answer | bb | 3 |
| 5 | Set ccc to a * bb | none | 3 |
| 6 | Set dddd to a / bb | none | 3 |
| 7 | Set dddd to ccc + dddd | none | 3 |
| 8 | Say dddd | none | 3 |
| 9 | Ask read_token and wait | none | 3 |
| 10 | Set bb to answer | bb | 5 |
| 11 | Ask read_token and wait | none | 5 |
| 12 | Set ccc to answer | ccc | 8 |
| 13 | Set x to bb * dddd | none | 8 |
| 14 | Set x to ccc - x | none | 8 |
| 15 | Say x | none | 8 |

This example demonstrates that repeated variables are counted each time they receive input. The variable name itself is not the unit being counted, the input events are.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Every program line is checked once. |
| Space | O(1) | Only the current line and accumulated answer are stored. |

The constraints allow up to 100000 lines, so a linear scan easily fits within the required limits. The solution performs only string checks and length additions, with no expensive data structures.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    result = sys.stdout.getvalue()
    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return result

# provided sample 1
assert run("""6
Ask read_token and wait
Set first to answer
Ask read_token and wait
Set second to answer
Set result to first + second
Say result
""") == "11\n", "sample 1"

# provided sample 2
assert run("""15
Ask read_token and wait
Set a to answer
Ask read_token and wait
Set bb to answer
Set ccc to a * bb
Set dddd to a / bb
Set dddd to ccc + dddd
Say dddd
Ask read_token and wait
Set bb to answer
Ask read_token and wait
Set ccc to answer
Set x to bb * dddd
Set x to ccc - x
Say x
""") == "8\n", "sample 2"

# minimum number of lines
assert run("""2
Ask read_token and wait
Set x to answer
""") == "1\n", "single character variable"

# repeated input to the same variable
assert run("""6
Ask read_token and wait
Set abc to answer
Ask read_token and wait
Set abc to answer
Say abc
Say abc
""") == "6\n", "repeated inputs"

# many non-input commands
assert run("""5
Set a to answer
Set b to a + a
Set c to b * b
Say c
Say a
""") == "1\n", "only answer assignments count"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single input into `x` | 1 | Minimum variable length handling |
| Two inputs into `abc` | 6 | Repeated occurrences are counted separately |
| Program with arithmetic only after one input | 1 | Non-input assignments are ignored |
| Provided samples | 11 and 8 | Matches official examples |

## Edge Cases

A program may contain many variable names, but only input variables contribute. For the input:

```
6
Ask read_token and wait
Set first to answer
Set result to first + first
Say result
Ask read_token and wait
Set second to answer
```

the algorithm recognizes only `first` and `second`, producing `5 + 6 = 11`. The arithmetic line involving `result` is skipped because it does not contain `answer`.

Repeated inputs require counting every occurrence. For:

```
8
Ask read_token and wait
Set a to answer
Ask read_token and wait
Set a to answer
Set b to a + a
Say b
Ask read_token and wait
Set c to answer
```

the scan adds `1` for each occurrence of `a` and `1` for `c`, giving `3`. The algorithm handles this naturally because it processes commands rather than maintaining a set of variable names.

Commands that happen to mention variables but are not input assignments are ignored. A line such as `Set value to other + value` changes program state, but no extra debugging output was produced before it, so it must not affect the answer.
