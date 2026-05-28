---
title: "CF 25B - Phone numbers"
description: "We are given a string of digits representing a phone number. The task is to split this string into pieces where every pi"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 25
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 25 (Div. 2 Only)"
rating: 1100
weight: 25
solve_time_s: 84
verified: true
draft: false
---

[CF 25B - Phone numbers](https://codeforces.com/problemset/problem/25/B)

**Rating:** 1100  
**Tags:** implementation  
**Solve time:** 1m 24s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string of digits representing a phone number. The task is to split this string into pieces where every piece has length either 2 or 3. The groups must appear in the original order, and they are joined with `-` characters in the output.

The problem does not ask for every possible partition. Any valid grouping is accepted.

The constraints are tiny. The phone number length is at most 100, so even fairly inefficient solutions would run comfortably within the limit. This changes the nature of the problem. The challenge is not optimization, but constructing a grouping that always works and handling the small corner cases correctly.

The tricky part is that greedy choices can accidentally leave a single digit at the end. A group of length 1 is illegal, so the algorithm must avoid creating that situation.

Consider the input:

```
5
12345
```

If we greedily take groups of 3 first, we get:

```
123-45
```

This is valid.

But if we process differently and take groups of 2 first:

```
12-34
```

we are left with `5`, which cannot form a valid group.

Another subtle case is when the remaining length becomes 4. For example:

```
7
1234567
```

If we take a group of 3 immediately:

```
123-456
```

we are left with `7`, which is invalid.

The correct strategy is:

```
12-34-567
```

or

```
123-45-67
```

Both work because the final remaining lengths are always decomposable into 2s and 3s.

The smallest valid input also needs care:

```
2
98
```

The entire string itself is already one valid group. A careless implementation that always tries to extract 3 digits first would fail immediately.

## Approaches

A brute-force solution would try every possible way to split the string. At each position, we can either take 2 digits or 3 digits, then recurse on the remainder. Since each position branches into two choices, the total number of possibilities grows exponentially.

For a length around 100, the number of recursive states becomes enormous. Even though many branches die early, a naive exhaustive search is unnecessary work for such a structured problem.

The reason brute force works conceptually is simple. Every valid partition is just a sequence of choices between lengths 2 and 3. If we explore all sequences, we eventually find a valid one.

The key observation is that we do not need to search. Every number of length at least 2 can always be represented using only 2s and 3s, except length 1. So the real goal is only to avoid leaving exactly one digit ungrouped.

That leads to a direct constructive strategy. While more than 4 digits remain, we safely take groups of 2. Why 2? Because subtracting 2 repeatedly preserves the ability to finish the remaining suffix with groups of 2 or 3.

Once the remaining length becomes 2, 3, or 4, we stop and handle it directly:

If 2 digits remain, take one group of 2.

If 3 digits remain, take one group of 3.

If 4 digits remain, split it into two groups of 2.

This guarantees that no group has invalid size.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow conceptually |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the phone number string.
2. Create an empty list called `groups` to store the resulting chunks.
3. Maintain an index pointing to the current unread position.
4. While the number of remaining digits is greater than 4, take the next 2 digits and append them to `groups`.

Taking 2 digits repeatedly is safe because it prevents the remainder from ever becoming 1.
5. After the loop finishes, the remaining length must be 2, 3, or 4.
6. If 2 digits remain, append them as one final group.
7. If 3 digits remain, append them as one final group.
8. If 4 digits remain, split them into two groups of 2 and append both.

Splitting 4 into `2 + 2` avoids producing a forbidden group of size 1.
9. Print all groups joined by `-`.

### Why it works

The algorithm maintains a simple invariant: after every step, the remaining number of digits is still representable using only groups of size 2 and 3.

Subtracting 2 from any valid remaining length greater than 4 keeps the remainder valid. The process eventually reaches one of the base lengths 2, 3, or 4, all of which have direct valid decompositions.

The only impossible remainder is 1, and the algorithm is designed specifically to avoid creating it.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
s = input().strip()

groups = []
i = 0

while n - i > 4:
    groups.append(s[i:i + 2])
    i += 2

remaining = n - i

if remaining == 2:
    groups.append(s[i:i + 2])
elif remaining == 3:
    groups.append(s[i:i + 3])
else:
    groups.append(s[i:i + 2])
    groups.append(s[i + 2:i + 4])

print("-".join(groups))
```

The solution follows the constructive strategy directly.

The variable `i` tracks how many digits have already been processed. The loop continues while more than 4 digits remain because lengths 2, 3, and 4 can already be finished safely without further decisions.

The handling of length 4 is the most important boundary condition. A common mistake is to take a group of 3 first, leaving one digit behind. Splitting into `2 + 2` avoids that issue completely.

The implementation uses slicing on the original string, which is clean and efficient for these small constraints.

## Worked Examples

### Example 1

Input:

```
6
549871
```

| Step | i | Remaining | Action | Groups |
| --- | --- | --- | --- | --- |
| Start | 0 | 6 | Take 2 digits | `["54"]` |
| Loop | 2 | 4 | Stop loop | `["54"]` |
| Finish | 2 | 4 | Split into 2 + 2 | `["54", "98", "71"]` |

Output:

```
54-98-71
```

This example shows why the algorithm stops when 4 digits remain. The suffix `9871` is handled as `98-71`, avoiding an invalid leftover digit.

### Example 2

Input:

```
7
1234567
```

| Step | i | Remaining | Action | Groups |
| --- | --- | --- | --- | --- |
| Start | 0 | 7 | Take 2 digits | `["12"]` |
| Loop | 2 | 5 | Take 2 digits | `["12", "34"]` |
| Loop End | 4 | 3 | Stop loop | `["12", "34"]` |
| Finish | 4 | 3 | Take final 3 digits | `["12", "34", "567"]` |

Output:

```
12-34-567
```

This trace demonstrates the invariant clearly. Every step preserves a remainder that can still be decomposed into valid groups.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each digit is processed once |
| Space | O(n) | The output groups store all digits |

The input size is at most 100, so linear processing is easily fast enough. Memory usage is also tiny because the stored groups together contain exactly the original digits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    n = int(input())
    s = input().strip()

    groups = []
    i = 0

    while n - i > 4:
        groups.append(s[i:i + 2])
        i += 2

    remaining = n - i

    if remaining == 2:
        groups.append(s[i:i + 2])
    elif remaining == 3:
        groups.append(s[i:i + 3])
    else:
        groups.append(s[i:i + 2])
        groups.append(s[i + 2:i + 4])

    print("-".join(groups))

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()

    backup_stdout = sys.stdout
    sys.stdout = out

    solve()

    sys.stdout = backup_stdout
    return out.getvalue().strip()

# provided sample
assert run("6\n549871\n") == "54-98-71", "sample 1"

# minimum size
assert run("2\n98\n") == "98", "minimum length"

# exactly 3 digits
assert run("3\n123\n") == "123", "single group of 3"

# exactly 4 digits
assert run("4\n1111\n") == "11-11", "split 4 into 2+2"

# odd length
assert run("7\n1234567\n") == "12-34-567", "avoid leftover 1"

# maximum-style repetitive case
assert run("10\n9999999999\n") == "99-99-99-99-99", "many groups of 2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 / 98` | `98` | Minimum valid input |
| `3 / 123` | `123` | Single group of 3 |
| `4 / 1111` | `11-11` | Correct handling of remainder 4 |
| `7 / 1234567` | `12-34-567` | Preventing leftover size 1 |
| `10 / 9999999999` | `99-99-99-99-99` | Repeated loop execution |

## Edge Cases

Consider the input:

```
4
1111
```

The algorithm immediately skips the loop because only 4 digits remain. It enters the final case and splits the string into:

```
11-11
```

A careless greedy approach that takes 3 digits first would produce:

```
111-1
```

which is invalid because a group of size 1 is forbidden.

Now consider:

```
7
1234567
```

The algorithm processes:

```
12
```

leaving 5 digits. It then processes:

```
34
```

leaving 3 digits, which can safely become one final group:

```
567
```

The final answer is:

```
12-34-567
```

This shows how repeatedly removing 2 digits prevents the remainder from becoming 1.

Finally, examine the smallest boundary:

```
2
98
```

The loop never runs because the remaining length is already valid. The algorithm directly outputs:

```
98
```

No special hacks are required because the base cases naturally handle the shortest allowed inputs.
