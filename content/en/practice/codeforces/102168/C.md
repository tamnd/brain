---
title: "CF 102168C - \u0421\u043a\u043e\u0431\u043e\u0447\u043a\u0438"
description: "We have a string of parentheses with even length. The number of opening and closing parentheses is the same, so changing positions by swaps never changes the total number of either type. One operation chooses two different positions and exchanges their characters."
date: "2026-08-19T15:12:24+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102168
codeforces_index: "C"
codeforces_contest_name: "\u041b\u0438\u0447\u043d\u044b\u0439 \u0447\u0435\u043c\u043f\u0438\u043e\u043d\u0430\u0442 \u0421\u0430\u043c\u0430\u0440\u0441\u043a\u043e\u0433\u043e \u0443\u043d\u0438\u0432\u0435\u0440\u0441\u0438\u0442\u0435\u0442\u0430 \u0441\u0440\u0435\u0434\u0438 \u043d\u043e\u0432\u0438\u0447\u043a\u043e\u0432 2018-2019"
rating: 0
weight: 102168
solve_time_s: 232
verified: true
draft: false
---

[CF 102168C - \u0421\u043a\u043e\u0431\u043e\u0447\u043a\u0438](https://codeforces.com/problemset/problem/102168/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 52s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a string of parentheses with even length. The number of opening and closing parentheses is the same, so changing positions by swaps never changes the total number of either type. One operation chooses two different positions and exchanges their characters. The task is to find the minimum number of such swaps needed to make the string a regular bracket sequence.

A parenthesis sequence is regular exactly when every prefix contains at least as many `(` as `)`, and the whole sequence contains the same number of both. The second condition is already guaranteed by the input, so the only thing that can be wrong is that some prefix has too many closing parentheses.

The length can reach (10^6). A quadratic algorithm would already perform around (10^{12}) elementary operations in the worst case, far beyond what a two-second limit can support. We need a linear or close-to-linear solution, and the input is large enough that even repeatedly scanning long suffixes is dangerous.

A useful edge case is `)(`. Its total balance is zero, but the first prefix has balance (-1), so the answer is `1`. A solution that checks only the final balance would incorrectly return zero.

Another edge case is `))((`. Its minimum prefix balance is (-2), but only one swap is necessary: exchanging the first `)` with the third character gives `()()`. A solution that counts every unit of deficit separately could incorrectly return two.

The rounding direction also matters. For `)))(((`, the minimum prefix balance is (-3), while the answer is `2`, not `1`. One swap changes a prefix balance by exactly two, so a deficit of three requires two swaps.

The provided samples are `))((`, whose answer is `1`, and `(())`, whose answer is `0`.

## Approaches

A direct greedy implementation could scan from left to right and, whenever the current prefix becomes invalid, search to the right for an unused `(` and swap it with the offending `)`. The idea is correct because a negative prefix must receive an opening parenthesis from somewhere later, and such a swap increases the balance of every affected prefix by two.

The problem is the search for that future `(`. In a string such as `))))...((((...`, there can be a linear-distance search for each correction. With (n) characters, this can require (\Theta(n^2)) character inspections. For (n=10^6), that is on the order of (10^{12}) operations, which is far too slow.

The observation that removes the expensive part is that we never actually need to know which future opening parenthesis will be swapped. We only need to know how much a bad prefix is below zero. Represent `(` as (+1) and `)` as (-1). Suppose some prefix has balance (-d). Swapping a `)` from this prefix with a `(` after the prefix increases that prefix balance by exactly (2). Thus one swap can repair two units of deficit.

Let (m) be the minimum prefix balance. If (m \ge 0), the sequence is already regular and no swap is needed. If (m<0), at least (\lceil -m/2\rceil) swaps are necessary. The same number of swaps is always sufficient: whenever the running balance would become negative, we can conceptually exchange that closing parenthesis with a later opening one. The correction raises the affected balances by two, and because the total balance is zero, a suitable opening parenthesis necessarily exists later.

There is an even simpler way to implement the same reasoning. While scanning, keep the current balance and the smallest balance seen. At the end, the answer is

\frac{-m+1}{2}
]

for negative (m). Equivalently, we can count how many times the balance would become negative and immediately reset it from (-1) to (1). The minimum-balance formula is cleaner because it makes the proof explicit.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n^2)) for repeated searching and swapping | (O(n)) | Too slow |
| Optimal | (O(n)) | (O(1)) besides the input string | Accepted |

## Algorithm Walkthrough

1. Read the entire parenthesis string and initialize `balance = 0` and `minimum = 0`. The variable `balance` represents the difference between the number of opening and closing parentheses in the current prefix.
2. Scan the string from left to right. Add `1` when the current character is `(` and subtract `1` when it is `)`.
3. After processing each character, update `minimum` with the smallest balance reached so far. A negative value means that the corresponding prefix contains more closing than opening parentheses.
4. After the scan, if `minimum` is nonnegative, output `0`. Every prefix already has a nonnegative balance, and the total balance is zero, so the sequence is regular.
5. If `minimum` is negative, output `(-minimum + 1) // 2`. Each swap can increase the balance of a bad prefix by at most two, while the greedy repair can achieve exactly that improvement, so this is the minimum number of swaps.

### Why it works

Consider a prefix whose balance is the global minimum (m<0). Every valid sequence must raise this prefix from (m) to at least zero. A swap can move one `(` from after the prefix to inside it while moving one `)` out, changing the prefix balance by exactly (2). Consequently, at least (\lceil -m/2\rceil) swaps are required.

That many swaps are also sufficient. Whenever a prefix becomes negative, there must be an opening parenthesis later because the entire string has equal numbers of opening and closing parentheses. Swapping such a future `(` with the offending `)` raises all balances between the two positions by two. Repeating this operation removes the deficit, and the required number of corrections is exactly (\lceil -m/2\rceil). The algorithm computes precisely that lower bound, so its answer is optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    s = input().strip()

    balance = 0
    minimum = 0

    for ch in s:
        if ch == '(':
            balance += 1
        else:
            balance -= 1

        if balance < minimum:
            minimum = balance

    print((-minimum + 1) // 2)

if __name__ == "__main__":
    solve()
```

The input is read as one string because there is exactly one test case. The string can contain up to (10^6) characters, so `sys.stdin.readline` avoids unnecessary input overhead.

The scan maintains the prefix balance using only one integer. There is no need to modify the string, because the proof shows that the exact positions used by the swaps do not affect the number of operations, only the worst prefix deficit matters.

`minimum` starts at zero rather than at a large positive value because the empty prefix has balance zero. This also makes already-valid strings such as `(())` and `()()` naturally produce an answer of zero.

The expression `(-minimum + 1) // 2` performs integer ceiling division for a positive value. For example, a deficit of one gives `1`, a deficit of two gives `1`, and a deficit of three gives `2`. Python integers do not overflow, so there is no special handling needed even at length (10^6).

The final balance itself does not need to be checked. The statement guarantees equal numbers of opening and closing parentheses, so after the entire string has been processed the balance is necessarily zero.

## Worked Examples

### Sample 1: `))((`

The sequence starts with two closing parentheses, so the first prefixes become invalid. The minimum balance is (-2), meaning one swap can repair the entire deficit.

| Position | Character | Balance | Minimum |
| --- | --- | --- | --- |
| 0 | `)` | -1 | -1 |
| 1 | `)` | -2 | -2 |
| 2 | `(` | -1 | -2 |
| 3 | `(` | 0 | -2 |

The answer is

[
\frac{-(-2)+1}{2} = \frac{3}{2} = 1
]

using integer division. One possible swap is between positions 0 and 2, producing `()()`.

The trace shows why the final balance alone is insufficient. The final value is zero, but the minimum prefix balance is negative, so the original sequence is not regular.

### Sample 2: `(())`

Every prefix has a nonnegative balance, so the minimum is zero.

| Position | Character | Balance | Minimum |
| --- | --- | --- | --- |
| 0 | `(` | 1 | 0 |
| 1 | `(` | 2 | 0 |
| 2 | `)` | 1 | 0 |
| 3 | `)` | 0 | 0 |

The answer is `0`. The sequence already satisfies the required prefix condition and has total balance zero.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n)) | Every character is processed exactly once. |
| Space | (O(1)) auxiliary | Only `balance` and `minimum` are maintained after reading the string. |

With (n\le 10^6), a linear scan performs only about one million iterations. That is comfortably within the intended scale of the two-second limit, while the quadratic approach could require roughly (10^{12}) operations.

## Test Cases

```python
import sys
import io

def solve_string(s: str) -> str:
    balance = 0
    minimum = 0

    for ch in s:
        if ch == '(':
            balance += 1
        else:
            balance -= 1

        minimum = min(minimum, balance)

    return str((-minimum + 1) // 2)

def run(inp: str) -> str:
    return solve_string(inp.strip()) + "\n"

# Provided samples
assert run("))((") == "1\n", "sample 1"
assert run("(())") == "0\n", "sample 2"

# Minimum-size valid input
assert run("()") == "0\n", "minimum size"

# A single unit of negative prefix balance
assert run(")(") == "1\n", "one swap needed"

# Odd-sized deficit, catches incorrect floor division
assert run(")))(((") == "2\n", "ceil division is required"

# Maximum-size input, already regular
assert run("()" * 500000) == "0\n", "maximum size"

# All possible symbols cannot be equal under the input guarantee,
# so the closest meaningful all-equal-style stress case is a
# repeated identical valid block.
assert run("()" * 10) == "0\n", "repeated blocks"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `()` | `0` | Minimum nonempty input and an already-valid sequence |
| `)(` | `1` | Negative prefix despite total balance being zero |
| `)))(((` | `2` | Correct ceiling division when the deficit is odd |
| `()` repeated 500000 times | `0` | Maximum input size and linear-time behavior |
| `()` repeated 10 times | `0` | Repeated balanced blocks and stable prefix tracking |

The input restriction makes a literal all-equal string impossible, because the number of `(` and `)` must be equal. A string containing only `(` or only `)` would violate the guarantee, so the test suite uses the largest meaningful repeated-character-pattern cases instead.

## Edge Cases

For `)(`, the balances are (-1) and (0). The minimum is (-1), so the formula gives `(-(-1) + 1) // 2 = 1`. Swapping the two positions produces `()`. A final-balance-only solution would miss the invalid first prefix.

For `))((`, the balances are (-1,-2,-1,0), so the minimum is (-2). The formula gives `1`. The key point is that one swap changes a prefix balance by two, so a deficit of two does not require two separate corrections.

For `)))(((`, the balances are (-1,-2,-3,-2,-1,0). The minimum is (-3), giving `(-(-3) + 1) // 2 = 2`. This catches the common mistake of using `-minimum // 2`, which would round downward and incorrectly return `1`.

For `()` repeated 500000 times, the balance alternates between `1` and `0`, so `minimum` remains zero throughout the entire million-character input. The algorithm performs one constant amount of work per character and returns `0`. This exercises the upper input bound without requiring any swaps.

For `(())`, the balance progresses through `1,2,1,0`, never becoming negative. The algorithm consequently returns zero without attempting to find a swap, which confirms that already-valid sequences are handled without special-case manipulation.
