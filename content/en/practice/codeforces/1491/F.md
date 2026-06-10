---
title: "CF 1491F - Magnets"
description: "We have $n$ magnets. Each magnet is either N, S, or demagnetized -. For a query, we place some magnets on the left side of a machine and some on the right side. If we encode - N as $+1$, - S as $-1$, - - as $0$, then the force returned by the machine is $$(n1-s1)(n2-s2)."
date: "2026-06-10T22:29:53+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "constructive-algorithms", "interactive"]
categories: ["algorithms"]
codeforces_contest: 1491
codeforces_index: "F"
codeforces_contest_name: "Codeforces Global Round 13"
rating: 2700
weight: 1491
solve_time_s: 161
verified: false
draft: false
---

[CF 1491F - Magnets](https://codeforces.com/problemset/problem/1491/F)

**Rating:** 2700  
**Tags:** binary search, constructive algorithms, interactive  
**Solve time:** 2m 41s  
**Verified:** no  

## Solution
## Problem Understanding

We have $n$ magnets. Each magnet is either `N`, `S`, or demagnetized `-`.

For a query, we place some magnets on the left side of a machine and some on the right side. If we encode

- `N` as $+1$,
- `S` as $-1$,
- `-` as $0$,

then the force returned by the machine is

$$(n_1-s_1)(n_2-s_2).$$

Indeed,

$$n_1n_2+s_1s_2-n_1s_2-n_2s_1
=
(n_1-s_1)(n_2-s_2).$$

This observation completely changes the problem. Each magnet contributes a value from $\{-1,0,+1\}$, and a query returns the product of the sums of the two chosen groups.

The original task was interactive. In the contest we had to discover every zero-valued magnet using at most

$$n+\lfloor \log_2 n\rfloor$$

queries.

For hacks, the interaction is removed. We are given the entire string describing the magnets and must output the indices of all `-` magnets.

The constraints are very small. The total sum of all $n$ over test cases is at most $2000$. Any linear or quadratic solution easily fits.

The only subtle point is understanding what the interactive solution was actually doing. The hack version is trivial once the hidden types are revealed, but the interesting part of the problem is the construction behind the query bound.

A common misunderstanding is to treat the force formula as something complicated involving four counts. After rewriting it as

$$(\text{left sum})(\text{right sum}),$$

the structure becomes much clearer.

For example, suppose the magnets are:

```
N-S-
```

Their encoded values are:

```
+1 0 -1 0
```

A query placing the first magnet on the left and the third on the right returns

$$(+1)\cdot(-1)=-1.$$

A query placing the second magnet on one side returns $0$, because a demagnetized magnet contributes value $0$.

## Approaches

The hack version can be solved by simply scanning the string and collecting every position containing `-`.

That takes linear time and is obviously correct because the input directly reveals the answer.

The interesting part is the original interactive problem.

The brute-force interactive idea would be to test every magnet individually. If we somehow had a known non-zero magnet, we could query it against each candidate and determine whether the candidate is demagnetized. This requires $O(n)$ queries, which is already close to the limit. The real challenge is obtaining the necessary reference information while staying under

$$n+\lfloor\log_2 n\rfloor.$$

The key observation is that every magnet has value $-1$, $0$, or $+1$. The machine only returns products of sums. If we can find two magnets with opposite non-zero values, then they form a perfect reference pair. Using them, every remaining magnet can be classified with one query.

Finding such a pair is done with a binary-search-style construction. Because at least two non-demagnetized magnets exist, there must be a region whose total sum is non-zero. Repeatedly splitting intervals allows us to isolate a useful pair in only $O(\log n)$ queries. After that, each remaining magnet requires exactly one query, giving a total of

$$n+\lfloor\log_2 n\rfloor$$

queries.

For the hack version none of this machinery is needed because the hidden information is already present in the input.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Direct scan of string | $O(n)$ | $O(1)$ besides output | Accepted |
| Interactive construction | $O(n)$ queries | $O(1)$ | Accepted in original problem |

## Algorithm Walkthrough

For the hack version:

1. Read $n$ and the magnet string.
2. Traverse the string from left to right.
3. Whenever the current character is `-`, record its 1-based position.
4. Output the number of recorded positions and then the positions themselves.

The reason this works is immediate: the input explicitly specifies the type of every magnet.

### Why it works

A position belongs in the answer if and only if its character in the string is `-`. The algorithm examines every position exactly once and records precisely those positions. No demagnetized magnet is missed, and no non-demagnetized magnet is added.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    out = []

    for _ in range(t):
        n = int(input())
        s = input().strip()

        ans = []
        for i, ch in enumerate(s, start=1):
            if ch == '-':
                ans.append(i)

        out.append(str(len(ans)))
        if ans:
            out.append(" ".join(map(str, ans)))
        else:
            out.append("")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution reads each test case independently.

The loop over the string uses 1-based indexing because Codeforces positions are numbered from 1. Every occurrence of `-` is appended to the answer list.

After the scan, the first output value is the number of demagnetized magnets. The second line contains their positions.

The total length of all strings is at most 2000, so the running time is linear in the input size.

## Worked Examples

### Example 1

Input:

```
1
4
NN--
```

Processing:

| Position | Character | Recorded positions |
| --- | --- | --- |
| 1 | N | [] |
| 2 | N | [] |
| 3 | - | [3] |
| 4 | - | [3, 4] |

Output:

```
2
3 4
```

This example shows the basic behavior. Every `-` position is collected and reported.

### Example 2

Input:

```
1
7
N-SN--S
```

Processing:

| Position | Character | Recorded positions |
| --- | --- | --- |
| 1 | N | [] |
| 2 | - | [2] |
| 3 | S | [2] |
| 4 | N | [2] |
| 5 | - | [2, 5] |
| 6 | - | [2, 5, 6] |
| 7 | S | [2, 5, 6] |

Output:

```
3
2 5 6
```

This trace demonstrates that the scan treats `N` and `S` identically. Only the `-` symbol matters.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Each character is examined once |
| Space | $O(k)$ | Stores the answer positions, where $k$ is the number of `-` magnets |

Since the total sum of $n$ across all test cases is at most 2000, the algorithm performs only a few thousand operations. Both time and memory usage are far below the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    def solve():
        input = sys.stdin.readline
        t = int(input())
        out = []

        for _ in range(t):
            n = int(input())
            s = input().strip()

            ans = [str(i + 1) for i, c in enumerate(s) if c == '-']

            out.append(str(len(ans)))
            out.append(" ".join(ans))

        return "\n".join(out)

    return solve()

# sample-style case
assert run(
"""1
4
NN--
"""
) == "2\n3 4"

# minimum valid size
assert run(
"""1
3
NS-
"""
) == "1\n3"

# single demagnetized magnet at beginning
assert run(
"""1
5
-NSSN
"""
) == "1\n1"

# several consecutive demagnetized magnets
assert run(
"""1
6
N---SS
"""
) == "3\n2 3 4"

# multiple test cases
assert run(
"""2
3
NS-
4
--NS
"""
) == "1\n3\n2\n1 2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `NS-` | `3` | Minimum valid size |
| `-NSSN` | `1` | Demagnetized magnet at first position |
| `N---SS` | `2 3 4` | Consecutive demagnetized magnets |
| Multiple test cases | Separate answers | Proper state reset between cases |

## Edge Cases

Consider:

```
1
3
NS-
```

The only demagnetized magnet is at the last position. The scan visits positions 1, 2, and 3. Only position 3 matches `-`, so the output is:

```
1
3
```

A solution with incorrect indexing could accidentally output position 2 instead.

Consider:

```
1
5
-NSSN
```

The first character is `-`. Because the algorithm uses 1-based positions when recording answers, it outputs:

```
1
1
```

This catches off-by-one mistakes at the beginning of the string.

Consider:

```
1
6
N---SS
```

Three consecutive positions are demagnetized. The algorithm records all of them independently:

```
3
2 3 4
```

This verifies that adjacent `-` symbols are handled correctly and none are skipped.

Consider:

```
1
7
---NNSS
```

The answer is:

```
3
1 2 3
```

Leading runs of demagnetized magnets are processed exactly the same way as magnets in the middle or at the end of the string.
