---
title: "CF 196A - Lexicographically Maximum Subsequence"
description: "We are given a lowercase string and may choose any non-empty subsequence of its characters while preserving their original order. Among all possible subsequences, we need the one that is lexicographically largest."
date: "2026-06-03T09:41:06+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "strings"]
categories: ["algorithms"]
codeforces_contest: 196
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 124 (Div. 1)"
rating: 1100
weight: 196
solve_time_s: 89
verified: true
draft: false
---

[CF 196A - Lexicographically Maximum Subsequence](https://codeforces.com/problemset/problem/196/A)

**Rating:** 1100  
**Tags:** greedy, strings  
**Solve time:** 1m 29s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a lowercase string and may choose any non-empty subsequence of its characters while preserving their original order.

Among all possible subsequences, we need the one that is lexicographically largest. Lexicographic comparison behaves exactly like dictionary order: the first position where two strings differ decides the winner, and if one string is a prefix of the other, the longer string is larger.

The string length can reach $10^5$. A subsequence problem immediately suggests an exponential search space because every character can either be taken or skipped. There are $2^n-1$ non-empty subsequences, which is completely impossible to enumerate when $n=10^5$. Even algorithms that repeatedly scan large suffixes can become too slow if they perform $O(n^2)$ work. With a 2-second limit, we should target linear time or close to it.

Several situations are easy to mishandle.

Consider:

```
abc
```

The answer is:

```
c
```

A careless approach might try to keep many characters because longer strings are sometimes larger. Here, however, the very first character dominates lexicographic order. Any subsequence starting with `a` or `b` loses immediately to one starting with `c`.

Another tricky case is:

```
zzza
```

The answer is:

```
zzza
```

Once we decide that `z` is the best possible first character, we should not take only one occurrence. Keeping all later `z` characters makes the result larger because the prefixes remain equal and the longer string wins.

A third example is:

```
ababba
```

The answer is:

```
bbba
```

Choosing only the first maximum character is not enough. After taking a `b`, we must solve the same problem on the remaining suffix and continue greedily.

## Approaches

The brute-force idea is straightforward: generate every subsequence, compare them lexicographically, and keep the best one.

This works because the definition of the problem is exactly "find the maximum among all subsequences". Unfortunately, a string of length $n$ has $2^n$ subsequences. Even for $n=50$, that is already more than one quadrillion possibilities. For $n=10^5$, it is hopeless.

To find something faster, we should think about what determines lexicographic order.

The first character is the most important position. If a subsequence begins with `y`, it can never beat a subsequence beginning with `z`. That means the first character of the answer must be the maximum character appearing anywhere in the string.

Suppose the largest character appearing in the current suffix is `c`. Any optimal answer must start with a `c`. Which occurrences of `c` should we keep?

Take all of them.

If two candidate answers start with the same prefix and one continues with extra copies of the same maximum character, the longer one is lexicographically larger. There is no penalty for taking a maximum character because it cannot make an earlier position worse.

This observation leads to a very simple view. Process the string from right to left while maintaining the largest character seen so far. A character belongs in the answer exactly when it is equal to the suffix maximum at its position.

For example:

```
ababba
```

Suffix maxima are:

```
b b b b b a
```

Any position whose character equals its suffix maximum is selected:

```
a b a b b a
  ^   ^ ^ ^
```

The resulting subsequence is:

```
bbba
```

This requires only one linear scan.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^n \cdot n)$ | $O(2^n)$ | Too slow |
| Optimal | $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Read the string.
2. Traverse the string from right to left.
3. Maintain `mx`, the largest character encountered so far in the suffix.
4. When the current character is greater than `mx`, update `mx`.
5. If the current character equals `mx`, add it to the answer.

The character is a suffix maximum. Any optimal lexicographically maximum subsequence must contain it.
6. The collected characters were obtained from right to left, so reverse them.
7. Output the resulting string.

### Why it works

At any position, let `M` be the largest character appearing anywhere to its right, including itself.

If the current character is smaller than `M`, choosing it would force the subsequence to start with a worse character than one that begins at an occurrence of `M`. Such a choice can never belong to an optimal answer.

If the current character equals `M`, skipping it is also suboptimal. Keeping this character gives an additional occurrence of the largest available letter while preserving the possibility of choosing all future optimal characters. Since lexicographic order prefers longer strings when prefixes are equal, taking every suffix-maximum character is always beneficial.

Thus the optimal subsequence consists exactly of the positions whose character equals the maximum character in their suffix.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    s = input().strip()

    mx = ''
    ans = []

    for ch in reversed(s):
        if ch > mx:
            mx = ch
        if ch == mx:
            ans.append(ch)

    print(''.join(reversed(ans)))

if __name__ == "__main__":
    solve()
```

The variable `mx` stores the largest character seen in the suffix processed so far. Because we scan from right to left, this is exactly the suffix maximum for the current position.

Whenever the current character equals `mx`, we keep it. Characters smaller than the suffix maximum are discarded because a larger character exists later and dominates lexicographic order.

The answer is collected in reverse order because the scan proceeds from the end of the string toward the beginning. Reversing once at the end restores the original left-to-right order of the subsequence.

There are no integer overflow concerns because the algorithm manipulates only characters and lists. The only subtle point is using `if ch == mx` after potentially updating `mx`. This guarantees that newly discovered maximum characters are included.

## Worked Examples

### Example 1

Input:

```
ababba
```

| Position (right to left) | Character | Current mx | Taken? | Collected |
| --- | --- | --- | --- | --- |
| 5 | a | a | Yes | a |
| 4 | b | b | Yes | ab |
| 3 | b | b | Yes | abb |
| 2 | a | b | No | abb |
| 1 | b | b | Yes | abbb |
| 0 | a | b | No | abbb |

After reversing:

```
bbba
```

This trace shows that every retained character is equal to the maximum character in its suffix.

### Example 2

Input:

```
zzza
```

| Position (right to left) | Character | Current mx | Taken? | Collected |
| --- | --- | --- | --- | --- |
| 3 | a | a | Yes | a |
| 2 | z | z | Yes | az |
| 1 | z | z | Yes | azz |
| 0 | z | z | Yes | azzz |

After reversing:

```
zzza
```

This example demonstrates why all occurrences of the maximum character should be preserved. Keeping every `z` produces a lexicographically larger result than keeping only one.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | One pass over the string |
| Space | $O(n)$ | The answer subsequence may contain all characters |

With $n \le 10^5$, a linear scan is easily fast enough. The memory usage is also safe because storing the answer requires at most $10^5$ characters.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    s = input().strip()

    mx = ''
    ans = []

    for ch in reversed(s):
        if ch > mx:
            mx = ch
        if ch == mx:
            ans.append(ch)

    return ''.join(reversed(ans))

# provided sample
assert run("ababba\n") == "bbba", "sample 1"

# minimum size
assert run("a\n") == "a", "single character"

# all equal characters
assert run("aaaaaa\n") == "aaaaaa", "all equal"

# strictly increasing
assert run("abcde\n") == "e", "only largest suffix maximum survives"

# strictly decreasing
assert run("edcba\n") == "edcba", "every position is a suffix maximum"

# repeated maximum letters
assert run("zzza\n") == "zzza", "keep all maximum letters"

# maximum-character block in middle
assert run("abzczzb\n") == "zzz", "multiple suffix maxima"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a` | `a` | Minimum length |
| `aaaaaa` | `aaaaaa` | All characters retained |
| `abcde` | `e` | Only final maximum survives |
| `edcba` | `edcba` | Every position is a suffix maximum |
| `zzza` | `zzza` | Repeated largest character |
| `abzczzb` | `zzz` | Multiple maximum occurrences across the string |

## Edge Cases

Consider:

```
abc
```

Scanning from right to left gives suffix maxima:

```
c c c
```

Only the final `c` equals its suffix maximum at its own position. The algorithm outputs:

```
c
```

Any subsequence beginning with `a` or `b` loses immediately because its first character is smaller.

Now consider:

```
zzza
```

The suffix maxima are:

```
z z z a
```

Every character equals its suffix maximum, so all characters are selected. The output becomes:

```
zzza
```

A common mistake is to keep only the first occurrence of the maximum character and output `z`, which is lexicographically smaller because `zzza` has the same prefix and is longer.

Finally, consider:

```
ababba
```

The suffix maxima are:

```
b b b b b a
```

Selected positions are the three `b` characters and the final `a`, producing:

```
bbba
```

The algorithm correctly skips both `a` characters that have a larger character later in the string. Those positions can never belong to a lexicographically maximum subsequence.
