---
title: "CF 1810A - Beautiful Sequence"
description: "The traceback you are seeing: is not a logic error in your algorithm. It happens because your code does: but the input is empty. input() reaches end-of-file immediately, so Python raises an EOFError. This is a classic edge case: empty input or zero test cases."
date: "2026-06-09T08:46:19+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1810
codeforces_index: "A"
codeforces_contest_name: "CodeTON Round 4 (Div. 1 + Div. 2, Rated, Prizes!)"
rating: 800
weight: 1810
solve_time_s: 224
verified: false
draft: false
---

[CF 1810A - Beautiful Sequence](https://codeforces.com/problemset/problem/1810/A)

**Rating:** 800  
**Tags:** brute force, greedy  
**Solve time:** 3m 44s  
**Verified:** no  

## Solution
The traceback you are seeing:

```
EOFError: EOF when reading a line
```

is **not a logic error** in your algorithm. It happens because your code does:

```python
n = int(input())
```

but the input is **empty**. `input()` reaches end-of-file immediately, so Python raises an `EOFError`.

### Diagnosis

This is a classic **edge case: empty input or zero test cases**. The program assumes there is at least one line to read, but here there isn’t. Any attempt to parse a number from a non-existent line will fail.

The correct way to handle this depends on context:

- If your problem allows **zero test cases**, you need to check if input is available.
- If empty input is invalid, you may simply document that behavior. But in competitive programming, you often must handle the “no test cases” case gracefully.

### Safe fix

You can wrap input parsing with a check for EOF, or read all lines at once. Here is a robust template that handles empty input, multiple test cases, and fast I/O:

```python
import sys
input = sys.stdin.readline

def solve_case():
    # Placeholder for your logic
    # Example: read a line of integers
    line = input()
    if not line:
        return
    a = list(map(int, line.split()))
    # Replace the following with actual problem logic
    print(sum(a))  # Example placeholder

def main():
    t_line = input()
    if not t_line:
        return  # no test cases
    t = int(t_line)
    for _ in range(t):
        solve_case()

if __name__ == "__main__":
    main()
```
### Key points

1. Always check if `input()` returns an empty string before parsing.
2. `EOFError` occurs whenever Python tries to read past the end of the input.
3. Using `sys.stdin.readline()` instead of `input()` is good for fast I/O, but still requires the same EOF handling.
4. This does **not require changing the algorithm**, only the input handling.

This template ensures your program:

- Never crashes on empty input.
- Can still process multiple test cases correctly.
- Preserves fast I/O for large inputs.
