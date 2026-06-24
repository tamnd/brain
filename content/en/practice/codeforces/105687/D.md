---
title: "CF 105687D - Matchmaker"
description: "We are given a lowercase string and many substring queries. For each query interval $[l, r]$, we look only at that substring. Two equal letters can form a match, and every character can belong to at most one match."
date: "2026-06-25T06:12:17+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105687
codeforces_index: "D"
codeforces_contest_name: "AlgoChief Sprint Round 2"
rating: 0
weight: 105687
solve_time_s: 50
verified: true
draft: false
---

[CF 105687D - Matchmaker](https://codeforces.com/problemset/problem/105687/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a lowercase string and many substring queries. For each query interval $[l, r]$, we look only at that substring.

Two equal letters can form a match, and every character can belong to at most one match. The goal is to achieve the largest possible number of matches inside the chosen substring. Before creating matches, we may change characters, replacing any position with any lowercase letter we want.

For each query, we must find the minimum number of character changes required so that the substring can achieve the maximum possible number of matches.

If a substring has length $m$, the largest possible number of disjoint pairs is $\lfloor m/2 \rfloor$. Any valid final arrangement must leave at most one unpaired character.

The input size is large. Across all test cases, the total value of $n + q$ is at most $2 \cdot 10^5$. A solution that scans every character of every queried substring would require $O(nq)$ work in the worst case, which is far too slow. We need something close to $O(1)$ or $O(\text{alphabet size})$ per query.

A few situations are easy to mishandle.

Consider:

```
substring = "abcdef"
```

Every frequency is 1. The length is 6, so we need 3 pairs. We must perform exactly 3 changes, for example:

```
abcdef -> aabbcc
```

A greedy idea such as "change characters until all letters become equal" would use many more operations than necessary.

Consider:

```
substring = "aaabbb"
```

The frequencies are $3$ and $3$. We already have two pairs:

```
aaa -> one pair + one leftover
bbb -> one pair + one leftover
```

Only one extra pair is missing, so the answer is 1.

Consider:

```
substring = "abcde"
```

The length is odd. One character is allowed to remain unmatched. The answer is 2, not 3:

```
abcde -> aabcd
```

This is where many implementations make a mistake by trying to pair every character.

## Approaches

A brute-force view is to inspect a queried substring, count frequencies, and somehow search for the minimum number of edits needed to reach a fully pairable configuration. That quickly becomes impractical because there can be up to $10^5$ queries per test case. Even recomputing frequencies from scratch for every query would cost $O(nq)$ operations in the worst case.

The key observation comes from looking at parity.

Suppose a letter appears $c$ times. It contributes $\lfloor c/2 \rfloor$ existing pairs. Summing over all letters gives the number of pairs already present.

Let the substring length be $m$, and let `odd` be the number of letters whose frequency is odd.

Using

$$\sum \left\lfloor \frac{c_i}{2} \right\rfloor
=
\frac{m - \text{odd}}{2},$$

the current number of pairs is completely determined by the number of odd frequencies.

The maximum possible number of pairs is $\lfloor m/2 \rfloor$. The missing number of pairs is

$$\left\lfloor \frac{m}{2} \right\rfloor
-
\frac{m-\text{odd}}{2}.$$

Evaluating this expression gives:

For even $m$:

$$\frac{\text{odd}}{2}$$

For odd $m$:

$$\frac{\text{odd}-1}{2}$$

Both cases are exactly

$$\left\lfloor \frac{\text{odd}}{2} \right\rfloor.$$

Now consider one character change. We can take a leftover character from one odd-frequency letter and turn it into another odd-frequency letter, eliminating two odd counts and creating one additional pair. So each required extra pair costs exactly one change.

The problem reduces to finding the number of odd frequencies in every queried substring.

Since the alphabet contains only 26 lowercase letters, we can build prefix frequency arrays. Then each query reconstructs the 26 frequencies in $O(26)$ time and counts how many are odd.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n)$ per query | $O(1)$ | Too slow |
| Optimal | $O(26)$ per query | $O(26n)$ | Accepted |

## Algorithm Walkthrough

1. Build prefix frequency counts for all 26 lowercase letters.
2. For each query $[l, r]$, compute the frequency of every letter inside the substring using prefix differences.
3. Count how many of those 26 frequencies are odd. Call this value `odd`.
4. Output `odd // 2`.

The reason step 4 works is that every change can merge two odd-frequency groups into one additional pair. If there are `odd` odd counts, we must eliminate all but at most one of them. The number of required eliminations is exactly `odd // 2`.

### Why it works

The invariant is that a frequency with even parity contributes no unmatched character, while a frequency with odd parity contributes exactly one unmatched character.

A substring with `odd` odd-frequency letters has exactly `odd` unmatched characters. To achieve the maximum possible matching, at most one unmatched character may remain. Each edit can reduce the number of unmatched characters by two, because it moves one character from one odd group into another odd group. Hence the minimum number of edits needed is precisely `odd // 2`.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    for _ in range(t):
        n, q = map(int, input().split())
        s = input().strip()

        pref = [[0] * (n + 1) for _ in range(26)]

        for i, ch in enumerate(s, 1):
            idx = ord(ch) - ord('a')

            for c in range(26):
                pref[c][i] = pref[c][i - 1]

            pref[idx][i] += 1

        ans = []

        for _ in range(q):
            l, r = map(int, input().split())

            odd = 0

            for c in range(26):
                freq = pref[c][r] - pref[c][l - 1]
                odd += freq & 1

            ans.append(str(odd // 2))

        sys.stdout.write("\n".join(ans) + "\n")

solve()
```

The prefix array stores cumulative counts for every letter. The frequency of a letter inside a query interval is obtained by subtracting two prefix values.

For each query we never examine the substring itself. We only inspect the 26 letter counts. The answer depends solely on how many of those counts are odd.

The most common implementation mistake is forgetting that queries are 1-indexed. Using `pref[c][r] - pref[c][l - 1]` avoids that off-by-one error.

Another subtle point is that the answer is not based on the substring length. Once the frequencies are known, only the parity pattern matters. Two substrings with completely different lengths can produce the same answer if they have the same number of odd-frequency letters.

## Worked Examples

### Example 1

Input:

```
6 1
abcdef
1 6
```

Frequencies inside the query:

| Letter | Frequency | Odd? |
| --- | --- | --- |
| a | 1 | Yes |
| b | 1 | Yes |
| c | 1 | Yes |
| d | 1 | Yes |
| e | 1 | Yes |
| f | 1 | Yes |

`odd = 6`

| odd | answer |
| --- | --- |
| 6 | 3 |

Output:

```
3
```

This demonstrates the extreme case where every character is unmatched. Three edits create three pairs.

### Example 2

Input:

```
6 1
aaabbb
1 6
```

Frequencies:

| Letter | Frequency | Odd? |
| --- | --- | --- |
| a | 3 | Yes |
| b | 3 | Yes |

`odd = 2`

| odd | answer |
| --- | --- |
| 2 | 1 |

Output:

```
1
```

This example shows that only parity matters. Even though there are already many repeated letters, two odd groups remain, requiring one edit.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(26q + 26n)$ | Build prefixes and inspect 26 letters per query |
| Space | $O(26n)$ | Prefix counts for each letter |

Since the alphabet size is fixed at 26, the running time is effectively linear in the total input size. With $\sum(n+q) \le 2 \cdot 10^5$, this comfortably fits within the limits.

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
        n, q = map(int, input().split())
        s = input().strip()

        pref = [[0] * (n + 1) for _ in range(26)]

        for i, ch in enumerate(s, 1):
            idx = ord(ch) - ord('a')

            for c in range(26):
                pref[c][i] = pref[c][i - 1]

            pref[idx][i] += 1

        for _ in range(q):
            l, r = map(int, input().split())

            odd = 0
            for c in range(26):
                freq = pref[c][r] - pref[c][l - 1]
                odd += freq & 1

            out.append(str(odd // 2))

    return "\n".join(out)

# provided sample
assert run(
"""2
6 4
abcdef
1 6
2 2
3 6
1 4
6 3
aaabbb
1 3
4 6
1 6
"""
) == "\n".join(["3", "0", "2", "2", "0", "0", "1"])

# minimum size
assert run(
"""1
1 1
a
1 1
"""
) == "0"

# all equal
assert run(
"""1
5 1
aaaaa
1 5
"""
) == "0"

# all distinct odd length
assert run(
"""1
5 1
abcde
1 5
"""
) == "2"

# off-by-one boundary query
assert run(
"""1
4 2
abca
1 1
1 4
"""
) == "\n".join(["0", "1"])
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a` | `0` | Minimum size |
| `aaaaa` | `0` | Already optimal |
| `abcde` | `2` | Odd-length substring |
| `abca` with queries on boundaries | `0`, `1` | Prefix indexing correctness |

## Edge Cases

Consider:

```
1
1 1
a
1 1
```

The frequency array contains one odd count. The algorithm computes:

```
odd = 1
answer = 1 // 2 = 0
```

A single character cannot form a pair, but it is already optimal because one unmatched character is allowed.

Consider:

```
1
1
abcdef
1 6
```

All six frequencies are odd.

```
odd = 6
answer = 6 // 2 = 3
```

The algorithm correctly determines that three edits are necessary to create three pairs.

Consider:

```
1
1
abcde
1 5
```

There are five odd frequencies.

```
odd = 5
answer = 5 // 2 = 2
```

One odd frequency may remain because the length is odd. The formula automatically handles this without any special case.

Consider:

```
1
1
aaabbb
1 6
```

The frequencies are $3$ and $3$.

```
odd = 2
answer = 1
```

Changing one leftover character from one group into the other creates the final missing pair, matching the optimal result.
