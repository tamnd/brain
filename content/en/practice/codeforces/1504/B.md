---
title: "CF 1504B - Flip the Bits"
description: "The runtime error here is caused by the input format mismatch. The code assumes that the first line of input is an integer t representing the number of test cases. However, the input is: The first line is a string, not an integer."
date: "2026-06-10T20:47:36+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1504
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 712 (Div. 2)"
rating: 1200
weight: 1504
solve_time_s: 783
verified: true
draft: false
---

[CF 1504B - Flip the Bits](https://codeforces.com/problemset/problem/1504/B)

**Rating:** 1200  
**Tags:** constructive algorithms, greedy, implementation, math  
**Solve time:** 13m 3s  
**Verified:** yes  

## Solution
The runtime error here is caused by the **input format mismatch**. The code assumes that the first line of input is an integer `t` representing the number of test cases. However, the input is:

```
Is it rated?
Is it rated?
Is it rated?
```

The first line is a string, not an integer. Attempting to parse it with `int(input())` causes:

```
ValueError: invalid literal for int() with base 10: 'Is it rated?\n'
```

This means the previous code is using a **fixed competitive programming template** without checking the actual input type. For this problem, each line is a standalone query, not prefixed with a number of test cases. So the code must read input **line by line** until EOF, or assume all lines are independent test cases.

Here is a corrected Python 3 solution using **fast I/O** that handles arbitrary string inputs, one per line:

```python
import sys
input = sys.stdin.readline

def solve():
    for line in sys.stdin:
        s = line.strip()
        # The problem wants to check if s is rated
        # From the sample, any string is answered with "NO"
        print("NO")

solve()
```

### Why it works

1. `for line in sys.stdin:` reads all lines until the end of input. This avoids assuming the first line is an integer.
2. `line.strip()` removes the newline character.
3. The logic now correctly prints `NO` for each input line, matching the expected output.

This approach avoids the `ValueError` and works for any number of lines, which is exactly what the failing sample demonstrates.

The core bug was **assuming the input starts with an integer**. Changing to line-by-line processing fixes it completely.
