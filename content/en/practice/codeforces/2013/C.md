---
title: "CF 2013C - Password Cracking"
description: "We are given a hidden binary string of length n. The only operation available is to ask whether some binary string t appears as a contiguous substring of the hidden string."
date: "2026-06-09T02:51:37+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "interactive", "strings"]
categories: ["algorithms"]
codeforces_contest: 2013
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 973 (Div. 2)"
rating: 1400
weight: 2013
solve_time_s: 133
verified: false
draft: false
---

[CF 2013C - Password Cracking](https://codeforces.com/problemset/problem/2013/C)

**Rating:** 1400  
**Tags:** constructive algorithms, interactive, strings  
**Solve time:** 2m 13s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a hidden binary string of length `n`. The only operation available is to ask whether some binary string `t` appears as a contiguous substring of the hidden string.

The original problem is interactive, but in the hacked version the hidden string is given directly in the input. Our task is to reconstruct exactly the strategy that would discover the hidden string using at most `2n` substring queries.

The central challenge is that a query does not tell us where a string appears, only whether it appears somewhere inside the password. We must exploit this very limited information efficiently.

The constraint `n ≤ 100` is tiny from a computational perspective. The real restriction is the interactive limit of at most `2n` queries. Any strategy that tries many candidates for every position would immediately exceed the allowed number of questions.

The tricky cases come from strings where extending in one direction suddenly becomes impossible.

Consider the hidden string:

```
1111
```

If we start from `"1"` and keep extending to the right, every extension with `'1'` succeeds. Eventually we obtain the entire string.

Now consider:

```
0010
```

Suppose we currently know `"001"`. Trying to append `'0'` succeeds and we finish. But if at some point neither right extension works, we must realize that we have already reached the right boundary of the hidden string and need to start growing in the opposite direction.

Another subtle case is when the password contains only one type of character.

```
00000
```

A careless solution might assume that if `"01"` is not a substring then both digits must exist somewhere else. In reality the whole string may consist entirely of zeros. The construction must remain valid even when only one character appears.

The smallest case is:

```
n = 1
```

The password is either `"0"` or `"1"`. The algorithm must correctly initialize itself without assuming the existence of longer substrings.

## Approaches

A brute force strategy would try every binary string of length `n` and ask whether it is the password. There are `2^n` possibilities, which becomes completely infeasible even for moderate values of `n`.

A more reasonable brute force idea is to determine the password one character at a time. Suppose we already know a prefix. We could ask whether appending `0` works, then whether appending `1` works, and continue. The problem is that substring queries do not tell us whether we are building the actual prefix of the password. They only tell us whether the candidate appears somewhere inside the string. A substring may occur in the middle, causing the reconstruction to drift away from the true answer.

The key observation is that we do not need to know where our current string appears. We only need to maintain a string that is guaranteed to be some substring of the password.

Start with a substring of length one. Then repeatedly try to extend it to the right. If appending `0` still produces a substring, keep it. Otherwise try appending `1`.

As long as one of these succeeds, our substring becomes longer.

Eventually neither extension succeeds. At that moment the current substring already touches the right end of the password. If there were a character to its right, one of the two possible extensions would necessarily exist.

Once we reach the right boundary, we switch directions. Now we prepend characters. If adding `0` to the front still yields a substring, we do so. Otherwise we prepend `1`.

Every successful query increases the known length by one. The process stops when the substring length becomes exactly `n`, which means we have reconstructed the whole password.

The elegant part is the query count. Every successful extension increases the length by one, so there are exactly `n-1` successful growth operations. Every growth may require at most two queries. The moment we switch directions happens only once. This keeps the total number of queries within `2n`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Enumeration | O(2^n · n) | O(n) | Too slow |
| Constructive Growth | O(n) queries | O(n) | Accepted |

## Algorithm Walkthrough

1. Query whether `"0"` is a substring.
2. If the answer is yes, initialize `cur = "0"`. Otherwise initialize `cur = "1"`.
3. Repeatedly try to extend `cur` to the right.
4. Ask whether `cur + "0"` is a substring. If yes, replace `cur` with that longer string.
5. Otherwise ask whether `cur + "1"` is a substring. If yes, replace `cur` with that longer string.
6. If neither right extension exists, stop extending right. At this point `cur` must already reach the right end of the password.
7. While `len(cur) < n`, extend to the left.
8. Ask whether `"0" + cur` is a substring. If yes, prepend `0`.
9. Otherwise prepend `1`.
10. Continue until the length becomes exactly `n`.
11. Output `cur`.

### Why it works

The invariant is that `cur` is always a substring of the hidden password.

Initially this is true because either `"0"` or `"1"` must occur.

Whenever we append or prepend a character, we only do so after receiving confirmation that the new string is also a substring. The invariant remains true.

Suppose right extension becomes impossible. Neither `cur + "0"` nor `cur + "1"` appears in the password. If `cur` were not already touching the right boundary, there would be some next character after one occurrence of `cur`, and one of those two extensions would exist. This contradiction proves that `cur` reaches the right end.

Once the right boundary is reached, every remaining unknown character lies to the left. Prepending the correct character always yields a valid substring, so the string can be grown until its length reaches `n`.

Since the final string has length `n` and is a substring of a password whose length is also `n`, the two strings must be identical.

## Python Solution

The original submission is interactive. The hacked version supplies the hidden password directly, so we simulate the substring queries locally.

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    for _ in range(t):
        n = int(input())
        s = input().strip()

        def ask(x):
            return x in s

        if ask("0"):
            cur = "0"
        else:
            cur = "1"

        while len(cur) < n:
            if ask(cur + "0"):
                cur += "0"
            elif ask(cur + "1"):
                cur += "1"
            else:
                break

        while len(cur) < n:
            if ask("0" + cur):
                cur = "0" + cur
            else:
                cur = "1" + cur

        print(cur)

solve()
```

The helper function `ask()` simulates an interactive query by checking whether a candidate string occurs inside the hidden password.

The first phase keeps extending to the right. The moment both possible right extensions fail, the algorithm has reached the right boundary and exits that loop.

The second phase grows only to the left. One of the two prepended characters must work because the current substring already ends at the password's right boundary and still has not reached length `n`.

A common mistake is continuing to test right extensions after both fail. That would waste queries in the interactive version and obscure the key observation that we have already found the right end.

Another easy error is assuming that after a failed `"0" + cur"` query the correct answer must be `"1" + cur"` without first proving that `cur` touches the right boundary. The correctness argument relies on the fact that the direction switch happens exactly when right growth becomes impossible.

## Worked Examples

### Example 1

Hidden string:

```
010
```

| Step | Current `cur` | Query | Result |
| --- | --- | --- | --- |
| Start | - | `"0"` | Yes |
| 1 | `0` | `00` | No |
| 2 | `0` | `01` | Yes |
| 3 | `01` | `010` | Yes |

Length becomes `3`, which equals `n`.

Final answer:

```
010
```

This example shows the simplest case where the password can be reconstructed entirely by right extensions.

### Example 2

Hidden string:

```
1100
```

| Step | Current `cur` | Query | Result |
| --- | --- | --- | --- |
| Start | - | `"0"` | Yes |
| 1 | `0` | `00` | Yes |
| 2 | `00` | `000` | No |
| 3 | `00` | `001` | No |
| Switch | `00` | right growth impossible | - |
| 4 | `00` | `000` | No |
| 5 | `00` | `100` | Yes |
| 6 | `100` | `0100` | No |
| 7 | `100` | `1100` | Yes |

Final answer:

```
1100
```

This trace demonstrates the crucial direction switch. After reaching the password's right boundary, all remaining characters are discovered by prepending.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) queries | Each successful extension increases length by one |
| Space | O(n) | Stores the reconstructed string |

The password length never exceeds 100, so even a straightforward string-based implementation is easily fast enough. The constructive strategy stays within the required `2n` query limit and uses only linear memory.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline
    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        s = input().strip()

        def ask(x):
            return x in s

        if ask("0"):
            cur = "0"
        else:
            cur = "1"

        while len(cur) < n:
            if ask(cur + "0"):
                cur += "0"
            elif ask(cur + "1"):
                cur += "1"
            else:
                break

        while len(cur) < n:
            if ask("0" + cur):
                cur = "0" + cur
            else:
                cur = "1" + cur

        out.append(cur)

    return "\n".join(out)

# minimum size
assert run("2\n1\n0\n1\n1\n") == "0\n1"

# all zeros
assert run("1\n5\n00000\n") == "00000"

# all ones
assert run("1\n6\n111111\n") == "111111"

# direction switch required
assert run("1\n4\n1100\n") == "1100"

# alternating pattern
assert run("1\n6\n010101\n") == "010101"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `n=1, s=0` | `0` | Smallest possible instance |
| `00000` | `00000` | All characters identical |
| `111111` | `111111` | Initialization from `"1"` |
| `1100` | `1100` | Right-boundary detection and left growth |
| `010101` | `010101` | Repeated overlapping substrings |

## Edge Cases

### Password consists entirely of zeros

Input:

```
1
5
00000
```

The algorithm starts from `"0"` and repeatedly extends with another zero:

```
0 -> 00 -> 000 -> 0000 -> 00000
```

No direction switch is needed. Every intermediate string remains a valid substring, and the final length reaches `n`.

### Password consists entirely of ones

Input:

```
1
4
1111
```

The query `"0"` fails, so initialization uses `"1"`.

Growth proceeds as:

```
1 -> 11 -> 111 -> 1111
```

This confirms that the algorithm does not depend on the presence of both binary digits.

### Immediate direction switch

Input:

```
1
4
1100
```

Starting from `"0"`:

```
0 -> 00
```

Neither `"000"` nor `"001"` is a substring, so the algorithm immediately concludes that `"00"` already reaches the right boundary.

It then prepends:

```
00 -> 100 -> 1100
```

The final result is correct because every prepend operation is verified by a substring query.

### Length one

Input:

```
1
1
1
```

Initialization produces `"1"`.

The current length already equals `n`, so neither extension loop executes. The algorithm immediately outputs `"1"`.

This avoids off-by-one mistakes when no growth operations are required.
