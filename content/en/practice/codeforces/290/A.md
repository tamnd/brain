---
title: "CF 290A - Mysterious strings"
description: "The entire task is a joke problem from the April Fools contest. The input is a single integer a between 1 and 40. Instead of computing anything, we must output a specific string associated with that position."
date: "2026-06-05T16:49:16+07:00"
tags: ["codeforces", "competitive-programming", "*special", "implementation"]
categories: ["algorithms"]
codeforces_contest: 290
codeforces_index: "A"
codeforces_contest_name: "April Fools Day Contest 2013"
rating: 1400
weight: 290
solve_time_s: 83
verified: true
draft: false
---

[CF 290A - Mysterious strings](https://codeforces.com/problemset/problem/290/A)

**Rating:** 1400  
**Tags:** *special, implementation  
**Solve time:** 1m 23s  
**Verified:** yes  

## Solution
## Problem Understanding

The entire task is a joke problem from the April Fools contest.

The input is a single integer `a` between 1 and 40. Instead of computing anything, we must output a specific string associated with that position. The sample values reveal that `2` maps to `"Adams"`, `8` maps to `"Van Buren"`, and `29` maps to `"Harding"`. The hidden observation is that the numbers correspond to the first forty presidents of the United States, in chronological order. The required output is simply the surname of the `a`-th president.

The constraint is tiny. Since `a` never exceeds 40, any solution that stores forty strings and performs a single lookup is effectively instantaneous.

The only real source of mistakes is indexing.

For example, with input

```
1
```

the correct output is

```
Washington
```

because the list is numbered starting from 1. A careless implementation that uses the input directly as a zero-based array index would return the second entry instead.

Another common mistake appears with input

```
40
```

The correct output is

```
Reagan
```

The array contains exactly forty elements, so the last valid zero-based index is `39`. Accessing index `40` would be out of bounds.

## Approaches

A brute-force viewpoint would be to manually check all possible values of `a` and print the corresponding answer using a long chain of `if` statements. Since there are only forty possibilities, this is perfectly fast enough.

A cleaner approach stores all forty surnames in an array. Then the problem becomes a direct table lookup. The input value is 1-based, while arrays are normally 0-based, so the answer is stored at position `a - 1`.

The brute-force version already runs in constant time because the input range is fixed. The array solution is preferred because it is shorter, easier to verify, and less error-prone.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (`if` chain) | O(1) | O(1) | Accepted |
| Optimal (array lookup) | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Create an array containing the surnames of the first forty U.S. presidents in chronological order.
2. Read the integer `a`.
3. Convert the 1-based position into a 0-based array index by computing `a - 1`.
4. Output the string stored at that index.

Why it works:

The array is constructed so that position `i` contains the surname corresponding to president number `i + 1`. The input value `a` asks for the `a`-th entry in that sequence. Accessing index `a - 1` retrieves exactly that surname, so the produced output matches the required mapping for every valid input.

## Python Solution

```python
import sys
input = sys.stdin.readline

presidents = [
    "Washington", "Adams", "Jefferson", "Madison", "Monroe",
    "Adams", "Jackson", "Van Buren", "Harrison", "Tyler",
    "Polk", "Taylor", "Fillmore", "Pierce", "Buchanan",
    "Lincoln", "Johnson", "Grant", "Hayes", "Garfield",
    "Arthur", "Cleveland", "Harrison", "Cleveland",
    "McKinley", "Roosevelt", "Taft", "Wilson", "Harding",
    "Coolidge", "Hoover", "Roosevelt", "Truman",
    "Eisenhower", "Kennedy", "Johnson", "Nixon",
    "Ford", "Carter", "Reagan"
]

a = int(input())
print(presidents[a - 1])
```

The array contains the entire mapping required by the problem. Reading the input gives a value between 1 and 40. Since Python lists are indexed from 0, the correct element is `presidents[a - 1]`.

The only subtle point is the index conversion. Forgetting the `- 1` shifts every answer by one position and causes either wrong answers or an out-of-range access when `a = 40`.

## Worked Examples

### Example 1

Input:

```
2
```

| Step | a | Index Used | Output |
| --- | --- | --- | --- |
| Read input | 2 | - | - |
| Compute index | 2 | 1 | - |
| Lookup | 2 | 1 | Adams |

Output:

```
Adams
```

This trace shows the 1-based to 0-based conversion. The second president is stored at array index 1.

### Example 2

Input:

```
29
```

| Step | a | Index Used | Output |
| --- | --- | --- | --- |
| Read input | 29 | - | - |
| Compute index | 29 | 28 | - |
| Lookup | 29 | 28 | Harding |

Output:

```
Harding
```

This example confirms that the solution works equally well for positions deep inside the list. No iteration or searching is required.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | One array access |
| Space | O(1) | Fixed-size array of 40 strings |

The running time does not depend on the input value. A single lookup and print operation easily fit within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

PRESIDENTS = [
    "Washington", "Adams", "Jefferson", "Madison", "Monroe",
    "Adams", "Jackson", "Van Buren", "Harrison", "Tyler",
    "Polk", "Taylor", "Fillmore", "Pierce", "Buchanan",
    "Lincoln", "Johnson", "Grant", "Hayes", "Garfield",
    "Arthur", "Cleveland", "Harrison", "Cleveland",
    "McKinley", "Roosevelt", "Taft", "Wilson", "Harding",
    "Coolidge", "Hoover", "Roosevelt", "Truman",
    "Eisenhower", "Kennedy", "Johnson", "Nixon",
    "Ford", "Carter", "Reagan"
]

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    a = int(sys.stdin.readline())
    return PRESIDENTS[a - 1] + "\n"

# provided sample
assert run("2\n") == "Adams\n", "sample 1"

# custom cases
assert run("1\n") == "Washington\n", "first element"
assert run("40\n") == "Reagan\n", "last element"
assert run("8\n") == "Van Buren\n", "middle value"
assert run("29\n") == "Harding\n", "another known mapping"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `Washington` | Minimum valid index |
| `40` | `Reagan` | Maximum valid index |
| `8` | `Van Buren` | Correct middle lookup |
| `29` | `Harding` | Another non-trivial position |

## Edge Cases

Consider the smallest input:

```
1
```

The algorithm computes `1 - 1 = 0` and accesses the first array element. The output is:

```
Washington
```

This confirms that the first position is handled correctly and that no negative indexing occurs.

Consider the largest input:

```
40
```

The algorithm computes `40 - 1 = 39` and accesses the last valid array position. The output is:

```
Reagan
```

This verifies that the implementation stays within array bounds.

Consider a value near the beginning:

```
2
```

The computed index is `1`, producing:

```
Adams
```

This case catches the classic off-by-one error. If the subtraction were omitted, the program would incorrectly return `"Jefferson"` instead.
