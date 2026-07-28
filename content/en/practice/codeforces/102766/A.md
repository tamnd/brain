---
title: "CF 102766A - Singhal and Swap"
description: "The problem gives two lowercase strings, S and T. An operation chooses one position from S and one position from T and exchanges the characters at those positions. The operation can be repeated any number of times."
date: "2026-07-28T23:46:31+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102766
codeforces_index: "A"
codeforces_contest_name: "Codedigger Training Contest -String"
rating: 0
weight: 102766
solve_time_s: 64
verified: true
draft: false
---

[CF 102766A - Singhal and Swap](https://codeforces.com/problemset/problem/102766/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 4s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem gives two lowercase strings, `S` and `T`. An operation chooses one position from `S` and one position from `T` and exchanges the characters at those positions. The operation can be repeated any number of times. The goal is to make the final version of `S` as small as possible in lexicographical order. The original statement and examples are from Codeforces Gym 102766A.

The key part of the operation is that characters never disappear or appear. They only move between the two strings. Since the final string `S` has the same length as the original `S`, the only question is which characters from the combined pool of `S` and `T` should remain inside `S`.

The constraints are small, with each string having length at most 100 and at most 100 test cases. This means even a solution that sorts the combined characters is easily fast enough. A quadratic or even slightly worse approach would still likely pass, but understanding the structure lets us solve it directly in linear time after counting characters.

The common mistakes come from treating the strings separately. For example, if we only sort `S`, we miss useful characters available in `T`.

Consider this input:

```
1
ba
c
```

The correct output is:

```
ab
```

A careless solution that only rearranges characters already inside `S` would keep `ba`, but swapping `c` with `b` gives `ca`, and then swapping is not useful. The actual minimum is obtained by taking the smallest two characters from the combined pool `{a,b,c}`, which are `a` and `b`.

Another edge case is when the two strings contain many equal characters.

```
1
aaa
aaa
```

The correct output is:

```
aaa
```

A solution that assumes every swap changes the string may perform unnecessary work or incorrectly try to replace equal characters.

A final edge case is when the smallest characters are all located in `T`.

```
1
zzz
abc
```

The correct output is:

```
abc
```

A solution that only considers improving positions using direct swaps one by one can stop too early. The operation can be repeated, so every position in `S` can eventually receive the globally best available characters.

## Approaches

A brute force approach would try to simulate swaps and explore the different strings that can be reached. For every possible swap, it could generate another state and continue until no new states appear. This is correct because every legal sequence of operations is represented somewhere in the search. The problem is that the number of possible states grows extremely quickly. If the combined length is `m`, the number of ways to choose which `|S|` characters belong to `S` is already `C(m, |S|)`, before considering different orders. Even for moderate lengths this becomes impossible.

The brute force works because it explores exactly the reachable states, but fails because there are far too many reachable states. The observation that unlocks the problem is that the exact sequence of swaps does not matter. The only thing that matters is the multiset of characters that ends up in `S`.

Every swap transfers one character in and one character out. Since we can choose any position in `S` and any position in `T`, we can repeatedly replace unwanted characters in `S` with smaller characters from `T`. This means the final `S` can contain any `|S|` characters from the combined multiset.

To minimize a string lexicographically, we should choose the smallest available characters. After choosing them, placing them in sorted order gives the smallest possible arrangement.

The whole problem reduces to counting all characters in `S + T`, taking the first `|S|` characters in sorted order, and returning them.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(number of reachable states) | O(number of reachable states) | Too slow |
| Optimal | O( | S | + |

## Algorithm Walkthrough

1. Count the frequency of every character in both strings together. The swaps preserve this combined frequency, so this represents the complete pool of characters available.
2. Determine that the final string `S` must contain exactly `|S|` characters. We need to choose this many characters from the combined pool.
3. Iterate through the alphabet from `'a'` to `'z'` and repeatedly take characters while there are still positions to fill in `S`. Taking smaller letters first is the greedy choice because lexicographical order is decided by the earliest differing position.
4. Append the chosen characters in alphabetic order and print the result. Sorting is naturally achieved by iterating through the alphabet instead of collecting and sorting a list.

Why it works: The invariant is that after choosing characters from the alphabet in increasing order, the partially built answer always contains the smallest possible prefix among all valid final strings. If a larger character was chosen while a smaller unused character existed, replacing the larger character would make the string smaller at the first position where they differ. Since every character in the final `S` comes from the same conserved pool, selecting the smallest `|S|` characters and ordering them increasingly gives the global optimum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        s = input().strip()
        t_str = input().strip()

        cnt = [0] * 26

        for c in s:
            cnt[ord(c) - ord('a')] += 1

        for c in t_str:
            cnt[ord(c) - ord('a')] += 1

        need = len(s)
        cur = []

        for i in range(26):
            take = min(cnt[i], need)
            if take:
                cur.append(chr(ord('a') + i) * take)
                need -= take
            if need == 0:
                break

        ans.append(''.join(cur))

    sys.stdout.write('\n'.join(ans))

if __name__ == "__main__":
    solve()
```

The input loop reads each pair of strings because each test case consists of one source string and one auxiliary string. The frequency array has size 26 because only lowercase English letters exist.

The two counting loops combine the characters from both strings. This is the central transformation of the problem: once the strings are merged conceptually, the original locations no longer matter.

The construction loop scans characters from smallest to largest. The value stored in `need` tracks how many characters still have to be placed into the final `S`. Using `min(cnt[i], need)` prevents taking more copies than exist or more characters than the answer length requires.

There are no index boundary issues because the alphabet loop is fixed from 0 to 25. Python integers also avoid overflow concerns. The final answer is built directly in sorted order, so no extra sorting step is needed.

## Worked Examples

### Example 1

Input:

```
1
ab
a
```

The combined characters are `a`, `a`, and `b`. The final `S` needs two characters.

| Step | Character considered | Frequency available | Characters taken | Remaining |
| --- | --- | --- | --- | --- |
| 1 | a | 2 | aa | 0 |
| 2 | b | 1 | none | 0 |

The answer is:

```
aa
```

This demonstrates that characters from `T` can become part of `S`, and the original positions do not restrict the final choice.

### Example 2

Input:

```
1
abd
codedigger
```

The combined pool begins with:

```
a b c d d e e g g i o r
```

The final `S` needs three characters.

| Step | Character considered | Frequency available | Characters taken | Remaining |
| --- | --- | --- | --- | --- |
| 1 | a | 1 | a | 2 |
| 2 | b | 1 | b | 1 |
| 3 | c | 1 | c | 0 |

The answer is:

```
abc
```

This confirms the greedy choice of taking the smallest available letters globally.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O( | S |
| Space | O(26) | Only the lowercase letter frequencies are stored |

The maximum input size is small, but the solution also scales well for much larger strings because it only performs a constant amount of extra work after counting characters.

## Test Cases

```python
import sys
import io

def solve_io(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    def solve():
        input = sys.stdin.readline
        t = int(input())
        out = []

        for _ in range(t):
            s = input().strip()
            t_str = input().strip()

            cnt = [0] * 26

            for c in s + t_str:
                cnt[ord(c) - ord('a')] += 1

            need = len(s)
            res = []

            for i in range(26):
                take = min(cnt[i], need)
                res.append(chr(i + ord('a')) * take)
                need -= take
                if need == 0:
                    break

            out.append(''.join(res))

        return '\n'.join(out)

    result = solve()
    sys.stdin = old_stdin
    return result

assert solve_io("""5
ab
a
abc
abc
abd
codedigger
dbc
a
adb
codealittle
""") == """aa
aab
abc
abc
aab""", "samples"

assert solve_io("""1
a
a
""") == "a", "single character"

assert solve_io("""1
zzz
abc
""") == "abc", "all useful characters in T"

assert solve_io("""1
aaa
aaa
""") == "aaa", "all equal values"

assert solve_io("""1
zyx
abcdefghijklmnopqrstuvw
""") == "abc", "boundary with many smaller characters"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `ab / a` | `aa` | Characters can move from `T` into `S` |
| `a / a` | `a` | Minimum size case |
| `zzz / abc` | `abc` | Best characters may all come from `T` |
| `aaa / aaa` | `aaa` | Equal character handling |
| `zyx / abc...w` | `abc` | Correct greedy selection across the alphabet |

## Edge Cases

For `S = "ba"` and `T = "c"`, the frequency array contains one `a`, one `b`, and one `c`. The algorithm needs two characters and scans the alphabet. It takes `a` first, then `b`, producing `ab`. This avoids the mistake of only rearranging the original `S`.

For `S = "aaa"` and `T = "aaa"`, the frequency of `a` is six. The algorithm takes exactly three copies because `need` starts at three. It stops immediately after filling the answer, producing `aaa` without trying unnecessary swaps.

For `S = "zzz"` and `T = "abc"`, the algorithm sees that the smallest three characters in the total pool are `a`, `b`, and `c`. It places them into the answer directly, showing why repeated swaps allow complete replacement of the original contents of `S`.
