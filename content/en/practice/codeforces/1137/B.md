---
title: "CF 1137B - Camp Schedule"
description: "We are given two binary strings. The first string s is not the schedule we must output directly. Instead, it acts as a multiset of characters."
date: "2026-06-12T03:57:18+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "hashing", "strings"]
categories: ["algorithms"]
codeforces_contest: 1137
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 545 (Div. 1)"
rating: 1600
weight: 1137
solve_time_s: 111
verified: true
draft: false
---

[CF 1137B - Camp Schedule](https://codeforces.com/problemset/problem/1137/B)

**Rating:** 1600  
**Tags:** greedy, hashing, strings  
**Solve time:** 1m 51s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two binary strings.

The first string `s` is not the schedule we must output directly. Instead, it acts as a multiset of characters. We are allowed to rearrange its symbols in any order, but the total number of `'0'` characters and `'1'` characters must remain exactly the same.

The second string `t` is a target pattern. Among all possible rearrangements of `s`, we want one that maximizes the number of times `t` appears as a substring.

The output is any rearrangement of `s` that achieves this maximum.

The key restriction is that only the order may change. If `s` contains 100 zeros and 200 ones, the answer must also contain exactly 100 zeros and 200 ones.

The lengths of both strings can reach 500,000. At this scale, quadratic algorithms are completely impossible. Even an $O(n^2)$ scan would require around $2.5 \times 10^{11}$ operations in the worst case. We need a solution that is essentially linear in the total input size.

The main difficulty is that maximizing substring occurrences is not the same as greedily placing copies of `t` independently. Different occurrences may overlap. In fact, overlap is exactly what allows us to fit more occurrences into a fixed amount of characters.

Consider:

```
t = 10101
```

The next occurrence can begin before the previous one fully ends because the suffix `"101"` is also a prefix. Ignoring overlaps wastes characters and produces fewer occurrences.

Another easy mistake is stopping after building one copy of `t`.

Example:

```
s = 11110000
t = 1100
```

A naive solution might place one copy:

```
1100 + remaining
```

But if resources allow, we should continue adding overlapping copies whenever possible.

A third edge case occurs when we cannot build even a single copy of `t`.

Example:

```
s = 1111
t = 000
```

Since there are no zeros available, every arrangement has zero occurrences. The correct answer is simply any string using all characters of `s`, such as:

```
1111
```

Trying to force a partial copy of `t` would violate the character counts.

## Approaches

A brute-force view is to consider every permutation of the characters of `s`, count how many times `t` appears, and choose the best one.

This is obviously correct because it examines every valid schedule. Unfortunately, if `|s| = 500000`, the number of permutations is astronomical and completely infeasible.

A more realistic brute-force idea is to repeatedly append a full copy of `t` whenever enough zeros and ones remain. This maximizes the number of non-overlapping occurrences.

The flaw is that occurrences are allowed to overlap. Suppose:

```
t = 10101
```

The suffix `"101"` equals the prefix `"101"`.

After writing one occurrence:

```
10101
```

we only need to append `"01"` to create another occurrence:

```
1010101
```

The overlap saves three characters. Since our supply of zeros and ones is limited, saving characters means fitting more occurrences.

This observation points directly to prefix-function or KMP thinking. If we know the longest proper prefix of `t` that is also a suffix, then after writing one occurrence we do not need to restart from scratch. We can append only the non-overlapping tail.

Let

```
k = longest border length of t
```

Then:

```
tail = t[k:]
```

After the first copy of `t`, every additional occurrence can be created by appending `tail`.

Since each appended tail creates exactly one new occurrence while consuming the minimum possible number of characters, repeatedly appending the tail is always optimal.

The algorithm becomes:

1. Count available zeros and ones from `s`.
2. Check whether one copy of `t` can be formed.
3. If not, output all characters arbitrarily.
4. Otherwise place one copy of `t`.
5. Compute the longest border of `t` using KMP.
6. Repeatedly append the non-overlapping tail while character counts permit.
7. Append all remaining unused characters.

Everything is linear because KMP computes the border in $O(|t|)$ time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O( | s | + |

## Algorithm Walkthrough

1. Count the number of zeros and ones available in `s`.
2. Count the number of zeros and ones required by one full copy of `t`.
3. If `s` does not contain enough zeros or ones to build even one copy of `t`, no occurrence can ever exist. Output all remaining characters in any order and stop.
4. Compute the KMP prefix-function of `t`.
5. Let `k = pi[-1]`. This is the length of the longest proper prefix of `t` that is also a suffix.
6. Append one complete copy of `t` to the answer and subtract its character counts from the available supply.
7. Define:

```
tail = t[k:]
```

This is exactly the part that must be appended to create one more occurrence while reusing the overlap.
8. Count the zeros and ones contained in `tail`.
9. While enough characters remain to write another copy of `tail`, append it and subtract its counts.
10. After no more tails can be added, append all remaining zeros and then all remaining ones.

### Why it works

After the first occurrence of `t` has been written, every future occurrence should overlap the previous one as much as possible. The maximum legal overlap between two consecutive copies is exactly the longest border of `t`.

Any smaller overlap consumes more characters while creating the same number of occurrences. Since the supply of zeros and ones is fixed, consuming fewer characters per additional occurrence can never be worse.

The KMP border gives the largest possible overlap. Thus each appended `tail` creates one new occurrence at the minimum possible character cost. Repeating this greedily maximizes the number of occurrences that fit into the available counts. Once another `tail` cannot be afforded, no alternative construction can create an additional occurrence because every occurrence requires at least as many new characters as the tail does.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().strip()
t = input().strip()

cnt0 = s.count('0')
cnt1 = len(s) - cnt0

need0 = t.count('0')
need1 = len(t) - need0

if cnt0 < need0 or cnt1 < need1:
    print('0' * cnt0 + '1' * cnt1)
    sys.exit()

m = len(t)

pi = [0] * m
for i in range(1, m):
    j = pi[i - 1]
    while j > 0 and t[i] != t[j]:
        j = pi[j - 1]
    if t[i] == t[j]:
        j += 1
    pi[i] = j

k = pi[-1]
tail = t[k:]

tail0 = tail.count('0')
tail1 = len(tail) - tail0

ans = [t]

cnt0 -= need0
cnt1 -= need1

while cnt0 >= tail0 and cnt1 >= tail1:
    ans.append(tail)
    cnt0 -= tail0
    cnt1 -= tail1

ans.append('0' * cnt0)
ans.append('1' * cnt1)

print(''.join(ans))
```

The first section counts available resources and checks whether even one copy of `t` is possible. If not, every arrangement yields zero occurrences, so any valid rearrangement is optimal.

The prefix-function computation is standard KMP. The value `pi[-1]` gives the longest border of the entire string.

The subtle idea is the construction of `tail = t[k:]`. If the border length is `k`, then the first `k` characters of the next occurrence are already present as a suffix of the previous occurrence. Only the remaining suffix must be appended.

The loop appends as many tails as possible. Each iteration creates exactly one new occurrence while spending the minimum possible number of characters.

Finally, leftover zeros and ones are appended. At that point no further occurrence can be created because we already failed the affordability test for another tail.

## Worked Examples

### Example 1

Input:

```
s = 101101
t = 110
```

Counts:

```
zeros = 2
ones = 4
```

Prefix function:

```
t = 110
pi = [0,1,0]
```

Longest border:

```
k = 0
tail = 110
```

| Step | Answer | Remaining 0s | Remaining 1s |
| --- | --- | --- | --- |
| Start | "" | 2 | 4 |
| Add first t | 110 | 1 | 2 |
| Add tail | 110110 | 0 | 0 |
| Finish | 110110 | 0 | 0 |

Output:

```
110110
```

There are two occurrences of `"110"`, beginning at positions 1 and 4.

### Example 2

Input:

```
s = 11110000
t = 1010
```

Prefix function:

```
pi = [0,0,1,2]
```

Longest border:

```
k = 2
tail = 10
```

| Step | Answer | Remaining 0s | Remaining 1s |
| --- | --- | --- | --- |
| Start | "" | 4 | 4 |
| Add first t | 1010 | 2 | 2 |
| Add tail | 101010 | 1 | 1 |
| Add tail | 10101010 | 0 | 0 |
| Finish | 10101010 | 0 | 0 |

The overlap saves characters and allows three occurrences instead of only two non-overlapping copies.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O( | s |
| Space | O( | t |

With lengths up to 500,000, a linear algorithm easily fits within the 1-second time limit and 512 MB memory limit. The solution performs only a few passes over the strings.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    s = input().strip()
    t = input().strip()

    cnt0 = s.count('0')
    cnt1 = len(s) - cnt0

    need0 = t.count('0')
    need1 = len(t) - need0

    if cnt0 < need0 or cnt1 < need1:
        print('0' * cnt0 + '1' * cnt1)
        return

    pi = [0] * len(t)
    for i in range(1, len(t)):
        j = pi[i - 1]
        while j and t[i] != t[j]:
            j = pi[j - 1]
        if t[i] == t[j]:
            j += 1
        pi[i] = j

    k = pi[-1]
    tail = t[k:]

    ans = [t]

    cnt0 -= need0
    cnt1 -= need1

    tail0 = tail.count('0')
    tail1 = len(tail) - tail0

    while cnt0 >= tail0 and cnt1 >= tail1:
        ans.append(tail)
        cnt0 -= tail0
        cnt1 -= tail1

    ans.append('0' * cnt0)
    ans.append('1' * cnt1)

    print(''.join(ans))

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    global input
    input = sys.stdin.readline

    out = io.StringIO()
    old = sys.stdout
    sys.stdout = out
    solve()
    sys.stdout = old
    return out.getvalue().strip()

# sample
assert run("101101\n110\n") == "110110"

# cannot build even one copy
assert run("1111\n000\n") == "1111"

# single character target
assert run("00111\n1\n") == "11100"

# perfect overlap chain
assert run("11110000\n1010\n") == "10101010"

# minimum size
assert run("0\n0\n") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1111 / 000` | `1111` | No occurrence can be formed |
| `00111 / 1` | `11100` | Single-character target |
| `11110000 / 1010` | `10101010` | Repeated overlapping construction |
| `0 / 0` | `0` | Smallest possible input |

## Edge Cases

### Cannot form the first occurrence

Input:

```
s = 1111
t = 000
```

Available counts:

```
zeros = 0
ones = 4
```

Required:

```
zeros = 3
ones = 0
```

The first occurrence is impossible. The algorithm immediately outputs all remaining characters:

```
1111
```

Any arrangement has zero occurrences, so this is optimal.

### Target with a large border

Input:

```
s = 11110000
t = 1010
```

The longest border has length 2.

```
1010
  10
```

The algorithm repeatedly appends only `"10"` instead of another full `"1010"`. This creates more occurrences from the same character supply.

### Border length zero

Input:

```
s = 101101
t = 110
```

The longest border is zero, so:

```
tail = t
```

No overlap is possible. The algorithm naturally degenerates into repeatedly placing complete copies of `t`, which is exactly optimal when no overlap exists.

### Single-character target

Input:

```
s = 00111
t = 1
```

The prefix-function value is zero and the tail is `"1"`.

The algorithm places as many `'1'` characters as possible first:

```
111
```

Then appends the remaining zeros:

```
11100
```

Every `'1'` position forms an occurrence, which is the maximum achievable count.
