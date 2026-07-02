---
title: "CF 103480K - \u6b22\u8fce\u6765\u5230\u676d\u5e08\u5927"
description: "We are given a single integer n, and we are asked to print a fixed message exactly n times, each occurrence on its own line. The message itself is always identical and does not depend on any input besides n."
date: "2026-07-03T06:33:03+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103480
codeforces_index: "K"
codeforces_contest_name: "The 4th Hangzhou Normal University Freshman Programming Contest"
rating: 0
weight: 103480
solve_time_s: 46
verified: true
draft: false
---

[CF 103480K - \u6b22\u8fce\u6765\u5230\u676d\u5e08\u5927](https://codeforces.com/problemset/problem/103480/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single integer n, and we are asked to print a fixed message exactly n times, each occurrence on its own line. The message itself is always identical and does not depend on any input besides n.

From a computational perspective, the input only determines how many times we repeat a constant string. There is no transformation, no conditional logic, and no accumulation of state beyond counting repetitions. This places the problem firmly in the category of linear output generation, where the output size is Θ(n) and the algorithm must spend at least Θ(n) time simply to write the result.

The constraint 1 ≤ n ≤ 100 is extremely small. Even the most naive repeated printing approach is easily sufficient, and any concern about performance or memory is irrelevant here.

There are no meaningful edge cases in terms of structure, but there are still a couple of minor correctness pitfalls that appear in similar tasks. If one forgets to include newline characters between outputs, all messages may be concatenated into a single line. Another mistake is printing an extra trailing blank line or an extra space at the end of each line, which would cause strict output comparison to fail even though the visible output looks similar. For example, if n = 3, the correct output is three separate lines, while a buggy solution might produce a single line like "Welcome to HZNUWelcome to HZNUWelcome to HZNU".

## Approaches

The most direct way to solve this problem is to simulate the requirement literally. We read n and then print the required string inside a loop that runs n times. Each iteration outputs the same constant line.

A brute-force interpretation and the optimal implementation are effectively identical here. The brute-force view is simply "for each count from 1 to n, print the string". This works because each output line is independent and does not require memory of previous iterations or computation of derived values.

The only reason this pattern becomes interesting in other problems is when n is large, for example 10^7 or 10^9, where raw printing dominates runtime and requires careful I/O optimization. Here, since n is at most 100, even Python’s standard printing is fast enough.

There is no alternative algorithmic structure to exploit. No mathematical formula reduces the number of printed lines, because the output itself explicitly requires n lines.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force iteration over n prints | O(n) | O(1) | Accepted |
| Optimal (same as above) | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We now describe the exact steps used to construct the output.

1. Read the integer n from standard input. This value determines how many times the output line must be produced.
2. Repeat a loop exactly n times. Each iteration corresponds to one required output line.
3. In each iteration, print the string "Welcome to HZNU" followed by a newline. The newline is essential because each repetition must appear on a separate line.

The algorithm does not maintain any additional state. The loop counter itself is sufficient to control repetition.

### Why it works

The correctness comes from a direct one-to-one correspondence between loop iterations and required output lines. Each iteration produces exactly one copy of the fixed string, and there is no interaction between iterations. Since the output specification requires exactly n identical lines, any sequence that prints the string once per iteration for n iterations must match the specification exactly.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    n = int(input().strip())
    out = "Welcome to HZNU"
    for _ in range(n):
        print(out)

if __name__ == "__main__":
    main()
```

The solution reads the integer using fast input and stores the output string in a variable to avoid reconstructing it repeatedly inside the loop. This is not strictly necessary for such a small constraint but reflects standard competitive programming hygiene.

The loop uses a simple range iteration, ensuring exactly n outputs. Each call to print automatically appends a newline, which matches the required formatting.

A common subtle mistake in similar problems is manually concatenating strings and printing once, which risks missing newline separators or exceeding memory when n is large. Here we avoid that by streaming output line by line.

## Worked Examples

Consider the input n = 3.

| Iteration | Printed string |
| --- | --- |
| 1 | Welcome to HZNU |
| 2 | Welcome to HZNU |
| 3 | Welcome to HZNU |

Each iteration independently produces the same output line. After the third iteration, the program terminates.

This confirms that the algorithm does not depend on prior state and consistently emits the required constant string per iteration.

Now consider n = 1.

| Iteration | Printed string |
| --- | --- |
| 1 | Welcome to HZNU |

With a single iteration, the output consists of exactly one line, matching the requirement without any extra spacing or missing newline issues.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | The loop executes once per required output line |
| Space | O(1) | Only a constant string and loop variable are stored |

The time complexity directly matches the output size, since printing itself dominates execution. With n ≤ 100, this is trivially fast in Python and well within typical time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    import io as sysio

    buf = sysio.StringIO()
    with redirect_stdout(buf):
        main()
    return buf.getvalue()

def main():
    n = int(input().strip())
    for _ in range(n):
        print("Welcome to HZNU")

# provided samples
assert run("1\n") == "Welcome to HZNU\n", "sample 1"
assert run("3\n") == "Welcome to HZNU\nWelcome to HZNU\nWelcome to HZNU\n"

# custom cases
assert run("2\n") == "Welcome to HZNU\nWelcome to HZNU\n", "small repeat case"
assert run("5\n") == "Welcome to HZNU\n" * 5, "repetition consistency"
assert run("100\n").count("Welcome to HZNU\n") == 100, "upper bound repetition"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | single line output | minimum case correctness |
| 3 | three identical lines | basic repetition structure |
| 100 | 100 identical lines | upper bound stability |

## Edge Cases

The main edge case is the lower bound n = 1. In this situation, the loop executes exactly once, and the output must still include a newline. The implementation handles this naturally because the loop does not special-case small values.

For example, with input:

```
1
```

the execution performs one iteration and prints:

```
Welcome to HZNU
```

There is no extra line and no missing newline. Since the loop boundary is inclusive and controlled directly by n, there is no off-by-one risk.

Another subtle case in similar problems is accidental concatenation of output without separators. Here, each print call independently emits a newline, so even for n = 100, the structure remains correct as a sequence of distinct lines.
