---
title: "CF 100D - World of Mouth"
description: "We start with an initial string and pass it around a circle of n people. Every person is allowed to modify the string in only one of two ways: 1. Remove exactly one character from the end. 2. Add exactly one character to the end. A person may also choose to do nothing."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special", "strings"]
categories: ["algorithms"]
codeforces_contest: 100
codeforces_index: "D"
codeforces_contest_name: "Unknown Language Round 3"
rating: 1500
weight: 100
solve_time_s: 138
verified: true
draft: false
---

[CF 100D - World of Mouth](https://codeforces.com/problemset/problem/100/D)

**Rating:** 1500  
**Tags:** *special, strings  
**Solve time:** 2m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

We start with an initial string and pass it around a circle of `n` people. Every person is allowed to modify the string in only one of two ways:

1. Remove exactly one character from the end.
2. Add exactly one character to the end.

A person may also choose to do nothing.

After exactly `n` transmissions, we obtain the final string. We must decide whether the final string could have been produced legally from the initial string.

The key detail is that every operation affects only the suffix of the string. Characters in the middle are never touched directly. The only mutable part is the current end of the string.

The constraints are unusually large. The number of moves can reach `8 * 10^6`, and each string can have length up to `10^7`. Any algorithm with quadratic behavior is impossible. Even linear algorithms must avoid unnecessary copies or repeated scans. A solution that rebuilds strings repeatedly or simulates operations one by one will time out or run out of memory.

The large input sizes also force us to think carefully about what actually changes during the process. Since operations only happen at the end, the relative order of preserved characters never changes. That observation is the entire problem.

Several edge cases are easy to mishandle.

Consider:

```
n = 2
initial = abc
final = abc
```

The correct answer is `Yes`. Both people may simply do nothing. A careless solution that assumes every move must modify the string would incorrectly reject this.

Now consider:

```
n = 1
initial = abc
final = ab
```

The correct answer is `Yes`. One deletion is enough. But:

```
n = 1
initial = abc
final = a
```

The correct answer is `No`, because a single move can change the length by at most one.

Another subtle case is when one string is a prefix of the other:

```
n = 3
initial = abc
final = abcde
```

The answer is `Yes`. We only need two append operations, and the remaining move can be unused.

But this fails:

```
n = 1
initial = abc
final = abcde
```

The answer is `No`, because growing by two characters requires at least two operations.

The most important structural edge case is when the strings disagree before the shorter string ends:

```
n = 10
initial = abcd
final = abxd
```

The answer is `No`. Since only the end may change, we can never alter the `c` into `x` without first deleting everything after it. The preserved part must always be a common prefix.

## Approaches

A brute-force idea is to simulate all possible sequences of operations. At each step we may append a character, remove the last character, or do nothing. Even if we restrict append choices to letters appearing in the target string, the branching factor is enormous. After `n` steps, the number of possible states becomes exponential.

Another brute-force refinement is to think backward from the final string. We could try every possible number of deletions and additions. This still becomes infeasible because the strings may contain millions of characters.

The reason brute force feels tempting is that each move is simple. But the number of move sequences is gigantic, while the actual structural freedom is tiny.

The critical observation is that operations only affect the suffix. That means every character before the first mismatch must remain untouched forever. So the transformation is possible if and only if the two strings share some common prefix, and everything after that prefix can be deleted and rebuilt within at most `n` operations.

Suppose the longest common prefix length is `L`.

To transform:

```
initial -> final
```

we must:

1. Delete the last `len(initial) - L` characters.
2. Append the last `len(final) - L` characters.

The minimum required operations are:

```
(len(initial) - L) + (len(final) - L)
```

If this value is at most `n`, then we can spend extra moves doing nothing, because each person is allowed to leave the string unchanged.

So the whole problem reduces to computing the longest common prefix and checking whether the required edit count fits inside `n`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(min( | s | , |

## Algorithm Walkthrough

1. Read `n`, the initial string `s`, and the final string `t`.
2. Scan both strings from left to right while characters match.

Maintain an index `L`, the length of the longest common prefix.

Once we encounter the first mismatch, no later character can ever be preserved because operations only modify suffixes.
3. Compute how many deletions are necessary.

We must remove every character in `s` after position `L`.

That count is:

```
len(s) - L
```
4. Compute how many append operations are necessary.

We must build the remaining suffix of `t`.

That count is:

```
len(t) - L
```
5. Add the two values to obtain the minimum required operations.
6. If the minimum required operations are at most `n`, print `Yes`.

Otherwise print `No`.

### Why it works

The preserved part of the string must always remain a prefix because all operations occur at the end. Once two strings differ at some position, every later character in the original string must eventually be deleted before the target suffix can be constructed.

The longest common prefix is therefore the maximum portion we can keep unchanged. Any valid transformation must delete the remainder of the initial string and append the remainder of the target string. That gives the minimum number of required operations, and any extra moves may simply leave the string unchanged. So the condition is both necessary and sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    s = input().strip()
    t = input().strip()

    l = 0
    limit = min(len(s), len(t))

    while l < limit and s[l] == t[l]:
        l += 1

    operations = (len(s) - l) + (len(t) - l)

    if operations <= n:
        print("Yes")
    else:
        print("No")

solve()
```

The implementation mirrors the mathematical argument directly.

The loop computes the longest common prefix without creating substrings. That matters because the strings may contain up to ten million characters. Repeated slicing would allocate huge amounts of memory and slow the program dramatically.

After the loop, every character after index `l` in the original string must be removed, and every character after index `l` in the target string must be appended. The formula for `operations` comes directly from that observation.

The comparison uses `<= n`, not `== n`. This is a common source of mistakes. People are allowed to leave the string unchanged during a move, so having extra unused moves is perfectly valid.

Another subtle detail is using `strip()` when reading strings. The input lines contain trailing newlines that should not become part of the strings.

## Worked Examples

### Example 1

Input:

```
100
Codeforces
MMIODPC
```

| Step | Value |
| --- | --- |
| Initial string | `Codeforces` |
| Final string | `MMIODPC` |
| Longest common prefix length | `0` |
| Deletions needed | `10` |
| Additions needed | `7` |
| Total operations | `17` |
| Compare with `n=100` | `17 <= 100` |

Output:

```
Yes
```

This example shows that extra moves do not matter. We only need 17 modifications, and the remaining 83 people may pass the string unchanged.

### Example 2

Input:

```
2
abcd
abxy
```

| Step | Value |
| --- | --- |
| Initial string | `abcd` |
| Final string | `abxy` |
| Longest common prefix length | `2` |
| Deletions needed | `2` |
| Additions needed | `2` |
| Total operations | `4` |
| Compare with `n=2` | `4 > 2` |

Output:

```
No
```

This demonstrates why only the common prefix can survive. The suffix `cd` must be deleted before `xy` can be appended.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(min( | s |
| Space | O(1) extra | Only a few integer variables are used |

The solution comfortably fits the limits. Even with strings of length ten million, a single linear scan is feasible in Python when implemented carefully without substring creation or repeated concatenation.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    n = int(input())
    s = input().strip()
    t = input().strip()

    l = 0
    limit = min(len(s), len(t))

    while l < limit and s[l] == t[l]:
        l += 1

    operations = (len(s) - l) + (len(t) - l)

    if operations <= n:
        print("Yes")
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

    return out.strip()

# provided sample
assert run(
"""100
Codeforces
MMIODPC
"""
) == "Yes", "sample 1"

# identical strings, zero operations needed
assert run(
"""2
abc
abc
"""
) == "Yes", "same strings"

# not enough operations
assert run(
"""1
abc
a
"""
) == "No", "requires two deletions"

# pure append
assert run(
"""3
abc
abcde
"""
) == "Yes", "two appends fit"

# mismatch inside string
assert run(
"""2
abcd
abxy
"""
) == "No", "needs four operations"

# full replacement
assert run(
"""6
aaaa
bbbb
"""
) == "No", "needs eight operations"

print("All tests passed.")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `abc -> abc` | `Yes` | Extra moves may be unused |
| `abc -> a` with `n=1` | `No` | Length difference alone can exceed limit |
| `abc -> abcde` with `n=3` | `Yes` | Pure append operations |
| `abcd -> abxy` with `n=2` | `No` | Internal mismatch requires rebuilding suffix |
| `aaaa -> bbbb` with `n=6` | `No` | Complete replacement cost |

## Edge Cases

Consider:

```
1
abc
ab
```

The longest common prefix is `ab`, so `L = 2`.

We need:

```
3 - 2 = 1 deletion
2 - 2 = 0 additions
```

Total operations = `1`.

Since `1 <= n`, the algorithm prints `Yes`.

Now consider:

```
1
abc
a
```

The longest common prefix is only `a`, so:

```
3 - 1 = 2 deletions
1 - 1 = 0 additions
```

Total operations = `2`.

Since `2 > 1`, the algorithm correctly prints `No`.

Next, examine a case where the strings differ in the middle:

```
10
abcd
abxd
```

The longest common prefix is `ab`.

The algorithm computes:

```
4 - 2 = 2 deletions
4 - 2 = 2 additions
```

Total operations = `4`.

Even though the strings have equal length, changing `c` into `x` still requires deleting the suffix and rebuilding it. The algorithm captures this automatically through the common-prefix logic.

Finally, consider identical strings:

```
5
hello
hello
```

The longest common prefix length is `5`.

Required operations:

```
0 deletions
0 additions
```

Total operations = `0`.

Since unused moves are allowed, the algorithm correctly prints `Yes`.
