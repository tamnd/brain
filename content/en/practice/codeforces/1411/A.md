---
title: "CF 1411A - In-game Chat"
description: "We are given several chat messages. Each message is a string containing lowercase English letters and the character )."
date: "2026-06-11T07:28:47+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1411
codeforces_index: "A"
codeforces_contest_name: "Technocup 2021 - Elimination Round 3"
rating: 800
weight: 1411
solve_time_s: 83
verified: true
draft: false
---

[CF 1411A - In-game Chat](https://codeforces.com/problemset/problem/1411/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 1m 23s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several chat messages. Each message is a string containing lowercase English letters and the character `)`.

A message is considered bad if the number of consecutive `)` characters at the very end of the string is strictly greater than the number of all remaining characters before them.

For example, in the string `ab))))`, there are 4 closing parentheses at the end and 2 other characters before them. Since `4 > 2`, the message is bad.

For each test case, we must determine whether the message is bad and print `"Yes"` or `"No"`.

The constraints are extremely small. Each string has length at most 100, and there are at most 100 test cases. Even an algorithm that scans every character several times would be fast enough. The goal is not optimization but correctly identifying the suffix of closing parentheses and comparing its size with the rest of the string.

One easy mistake is counting all `)` characters in the string instead of only the consecutive ones at the end.

Consider:

```
7
a)b)c))
```

The suffix of consecutive `)` characters has length 2. The remaining part has length 5. Since `2 > 5` is false, the answer is `"No"`.

A solution that counts every `)` would get 4 and incorrectly conclude the message is bad.

Another edge case is when the entire string consists of closing parentheses.

```
3
)))
```

The suffix length is 3 and the remaining length is 0. Since `3 > 0`, the answer is `"Yes"`.

A third subtle case is equality.

```
6
abc)))
```

The suffix length is 3 and the remaining length is also 3. The definition requires a strictly greater count, so the correct answer is `"No"`.

A careless implementation using `>=` would fail here.

## Approaches

A brute-force solution would first identify every possible suffix of the string, check whether it consists entirely of `)` characters, and then compute its length. Since the string length is at most 100, even such an inefficient method would still run comfortably within the limits.

The problem structure gives a much simpler observation. Only the final consecutive block of `)` matters. Everything before that block belongs to the "remaining characters" count.

Instead of examining many suffixes, we can start from the end of the string and count how many consecutive `)` characters appear. The moment we encounter any other character, we stop. That count is exactly the suffix size required by the statement.

If the suffix contains `cnt` parentheses, then the remaining part contains `n - cnt` characters. The message is bad precisely when:

```
cnt > n - cnt
```

The brute-force method works because it eventually finds the ending block, but scanning backward once gives the same information directly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Accepted but unnecessary |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the length `n` and the string `s`.
2. Start from the last character of the string and move left.
3. Count how many consecutive `)` characters appear at the end. Store this count in `cnt`.
4. Stop as soon as a character different from `)` is encountered, because only the final consecutive block matters.
5. Compute the number of remaining characters as `n - cnt`.
6. If `cnt > n - cnt`, print `"Yes"`.
7. Otherwise, print `"No"`.

### Why it works

The definition of a bad message depends only on the consecutive closing parentheses at the end of the string. By scanning backward, we compute exactly that quantity.

Every character not belonging to this ending block is part of the remaining portion of the string. Thus `n - cnt` is precisely the number of remaining characters mentioned in the statement.

The algorithm directly checks the condition from the definition, so its answer is always correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    for _ in range(t):
        n = int(input())
        s = input().strip()

        cnt = 0
        i = n - 1

        while i >= 0 and s[i] == ')':
            cnt += 1
            i -= 1

        if cnt > n - cnt:
            print("Yes")
        else:
            print("No")

solve()
```

The implementation follows the algorithm exactly.

The variable `cnt` stores the length of the suffix consisting of consecutive `)` characters. The loop starts at the last index and keeps moving left while the current character is `)`.

Once a different character appears, the suffix has ended and there is no need to continue scanning. The number of remaining characters is simply `n - cnt`.

The final comparison uses `>` rather than `>=`. This detail is crucial because equal counts do not make the message bad.

Since the string length is very small, integer overflow and memory concerns do not exist here.

## Worked Examples

### Example 1

Input string:

```
gege)))))
```

| Step | Position | Character | cnt |
| --- | --- | --- | --- |
| Start | 8 | ) | 0 |
| 1 | 8 | ) | 1 |
| 2 | 7 | ) | 2 |
| 3 | 6 | ) | 3 |
| 4 | 5 | ) | 4 |
| 5 | 4 | ) | 5 |
| Stop | 3 | e | 5 |

After the scan:

| Value | Result |
| --- | --- |
| n | 9 |
| cnt | 5 |
| n - cnt | 4 |
| Condition | 5 > 4 |

Output:

```
Yes
```

This example shows a suffix longer than the remaining prefix, so the message is bad.

### Example 2

Input string:

```
gl))hf))))))
```

| Step | Position | Character | cnt |
| --- | --- | --- | --- |
| Start | 11 | ) | 0 |
| 1 | 11 | ) | 1 |
| 2 | 10 | ) | 2 |
| 3 | 9 | ) | 3 |
| 4 | 8 | ) | 4 |
| 5 | 7 | ) | 5 |
| 6 | 6 | ) | 6 |
| Stop | 5 | f | 6 |

After the scan:

| Value | Result |
| --- | --- |
| n | 12 |
| cnt | 6 |
| n - cnt | 6 |
| Condition | 6 > 6 |

Output:

```
No
```

This trace demonstrates the strict comparison. Equality is not enough.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is examined at most once while scanning from the end |
| Space | O(1) | Only a few integer variables are used |

With `n ≤ 100` and at most 100 test cases, the solution performs at most a few thousand character inspections. It easily fits within the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    out = []

    t = int(input())

    for _ in range(t):
        n = int(input())
        s = input().strip()

        cnt = 0
        i = n - 1

        while i >= 0 and s[i] == ')':
            cnt += 1
            i -= 1

        out.append("Yes" if cnt > n - cnt else "No")

    return "\n".join(out)

# provided sample
assert run(
"""5
2
))
12
gl))hf))))))
9
gege)))))
14
)aa))b))))))))
1
)
"""
) == "\n".join([
    "Yes",
    "No",
    "Yes",
    "Yes",
    "Yes"
]), "sample 1"

# minimum size
assert run(
"""1
1
)
"""
) == "Yes", "single parenthesis"

# equality boundary
assert run(
"""1
6
abc)))
"""
) == "No", "suffix equals remaining length"

# no ending dominance
assert run(
"""1
7
a)b)c))
"""
) == "No", "only ending block counts"

# all parentheses
assert run(
"""1
10
))))))))))
"""
) == "Yes", "entire string is suffix"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `")"` | `Yes` | Smallest valid input |
| `"abc)))"` | `No` | Equality is not sufficient |
| `"a)b)c))"` | `No` | Only trailing parentheses matter |
| `"()))))))))"` (all parentheses) | `Yes` | Entire string can be the suffix |

## Edge Cases

### Equality Between Both Parts

Input:

```
1
6
abc)))
```

The backward scan counts `cnt = 3`. The remaining characters are `6 - 3 = 3`.

The comparison becomes:

```
3 > 3
```

which is false, so the output is:

```
No
```

This confirms that the condition is strictly greater.

### Entire String Consists of Parentheses

Input:

```
1
3
)))
```

The scan reaches the beginning of the string and counts `cnt = 3`.

The remaining part contains:

```
3 - 3 = 0
```

Since:

```
3 > 0
```

the output is:

```
Yes
```

The algorithm handles this naturally without any special cases.

### Parentheses Appear Earlier in the String

Input:

```
1
7
a)b)c))
```

Scanning from the end counts only the final block:

```
cnt = 2
```

The earlier parentheses are ignored because they are not part of the ending suffix.

The remaining length is:

```
7 - 2 = 5
```

Since:

```
2 > 5
```

is false, the answer is:

```
No
```

This verifies that the algorithm follows the exact definition of the problem rather than counting all parentheses in the string.
