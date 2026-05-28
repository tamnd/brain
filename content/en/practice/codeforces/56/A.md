---
title: "CF 56A - Bar"
description: "Vasya walks into a bar and sees several customers. For each customer, he only knows one piece of information: either the person’s age or the drink they ordered. He wants to determine how many people must still be checked to guarantee that nobody under 18 is drinking alcohol."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 56
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 52 (Div. 2)"
rating: 1000
weight: 56
solve_time_s: 88
verified: true
draft: false
---

[CF 56A - Bar](https://codeforces.com/problemset/problem/56/A)

**Rating:** 1000  
**Tags:** implementation  
**Solve time:** 1m 28s  
**Verified:** yes  

## Solution
## Problem Understanding

Vasya walks into a bar and sees several customers. For each customer, he only knows one piece of information: either the person’s age or the drink they ordered. He wants to determine how many people must still be checked to guarantee that nobody under 18 is drinking alcohol.

A customer definitely needs checking in two situations. The first is when we already know the customer is under 18, because we must verify the drink. The second is when we already know the customer ordered alcohol, because we must verify the age.

The input is a sequence of strings. Some strings are numbers representing ages, and some are drink names written in uppercase letters. The task is simply to count how many entries are suspicious and require verification.

The constraints are tiny. There are at most 100 customers, and each string has length at most 100. Even inefficient solutions would run instantly. A linear scan through the input is more than enough.

The main difficulty is not performance, but correctly distinguishing between ages and drink names.

One easy mistake is forgetting that exactly age 18 is legal. Only ages strictly less than 18 require checking.

For example:

```
3
17
18
19
```

The correct output is:

```
1
```

Only the 17-year-old must be checked.

Another common mistake is treating every word as alcohol. Only the drinks from the given list count.

For example:

```
4
WATER
JUICE
BEER
COKE
```

The correct output is:

```
1
```

Only `BEER` is alcoholic.

A more subtle bug appears when parsing numbers. The input `"0"` or `"5"` is still an age and must be handled numerically, not as a string drink name.

For example:

```
2
5
VODKA
```

The correct output is:

```
2
```

The first customer is underage, and the second customer ordered alcohol.

## Approaches

The brute-force interpretation is very direct. For every customer, we try to determine whether the known information already proves the person might be violating the law.

If the input token is a number, we compare it against 18. If the age is smaller, this person must be checked.

If the token is a word, we compare it against the list of alcoholic drinks. If the word belongs to that set, this person must also be checked.

Even though this already sounds like the final solution, we can still think about the naive version first. Suppose we stored the alcohol names in a list and, for every drink, scanned the entire list linearly. Since there are only 11 alcohol names and at most 100 customers, the total work would still be tiny, around 1100 comparisons.

The cleaner optimization is to store all alcoholic drinks in a set. Then membership checks become constant time on average. This reduces the logic to one pass through the input with immediate lookups.

The key observation is that each customer can be evaluated independently. No interaction exists between different customers, so there is no need for sorting, dynamic programming, or graph processing. We simply count suspicious entries.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n × 11) | O(1) | Accepted |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Store all alcoholic drink names in a set.

A set allows fast membership checks when we encounter drink names.
2. Read the number of customers `n`.
3. Initialize a counter `ans = 0`.
4. For each of the `n` input strings:

Check whether the string represents a number or a word.
5. If the string is numeric:

Convert it to an integer age.

If the age is less than 18, increment `ans`.

These customers are potentially drinking alcohol illegally, so they must be checked.
6. Otherwise, the string is a drink name.

If the drink exists in the alcohol set, increment `ans`.

These customers may be underage, so they must be checked.
7. Print `ans`.

### Why it works

Every customer falls into exactly one of two categories: known age or known drink.

If we know the age and it is below 18, we must inspect the drink to verify legality. If we know the drink and it is alcoholic, we must inspect the age.

Customers who are at least 18 are already safe regardless of drink. Customers drinking non-alcoholic beverages are also already safe regardless of age.

The algorithm counts exactly the customers whose missing information could reveal a violation. Since each customer is processed independently and every suspicious case is counted once, the final answer is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

alcohol = {
    "ABSINTH",
    "BEER",
    "BRANDY",
    "CHAMPAGNE",
    "GIN",
    "RUM",
    "SAKE",
    "TEQUILA",
    "VODKA",
    "WHISKEY",
    "WINE"
}

n = int(input())
ans = 0

for _ in range(n):
    s = input().strip()

    if s.isdigit():
        if int(s) < 18:
            ans += 1
    else:
        if s in alcohol:
            ans += 1

print(ans)
```

The solution begins by storing all alcoholic drinks in a set. A set is the natural structure here because membership checks are fast and concise.

The loop processes one customer at a time. The method `isdigit()` cleanly separates ages from drink names. Since drink names contain only uppercase letters, there is no ambiguity.

When the token is numeric, the code converts it to an integer and checks whether it is strictly less than 18. Using `< 18` instead of `<= 18` is important because age 18 is legal.

When the token is not numeric, the code checks whether the drink belongs to the alcohol set. Only the listed drinks count as alcoholic.

The algorithm never stores all customers simultaneously, so memory usage stays constant.

## Worked Examples

### Example 1

Input:

```
5
18
VODKA
COKE
19
17
```

| Step | Input | Type | Suspicious? | ans |
| --- | --- | --- | --- | --- |
| 1 | 18 | age | No | 0 |
| 2 | VODKA | alcohol | Yes | 1 |
| 3 | COKE | non-alcohol | No | 1 |
| 4 | 19 | age | No | 1 |
| 5 | 17 | age | Yes | 2 |

Final output:

```
2
```

This trace shows both kinds of suspicious customers. `VODKA` requires checking the age, while `17` requires checking the drink.

### Example 2

Input:

```
6
WINE
16
JUICE
18
BEER
7
```

| Step | Input | Type | Suspicious? | ans |
| --- | --- | --- | --- | --- |
| 1 | WINE | alcohol | Yes | 1 |
| 2 | 16 | age | Yes | 2 |
| 3 | JUICE | non-alcohol | No | 2 |
| 4 | 18 | age | No | 2 |
| 5 | BEER | alcohol | Yes | 3 |
| 6 | 7 | age | Yes | 4 |

Final output:

```
4
```

This example exercises all boundary conditions. Age `18` is correctly treated as legal, while non-alcoholic drinks such as `JUICE` are ignored.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each customer is processed once |
| Space | O(1) | The alcohol set has constant size |

With at most 100 customers, the program runs essentially instantly. The memory usage is also negligible because the alcohol list always contains exactly 11 strings.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    alcohol = {
        "ABSINTH",
        "BEER",
        "BRANDY",
        "CHAMPAGNE",
        "GIN",
        "RUM",
        "SAKE",
        "TEQUILA",
        "VODKA",
        "WHISKEY",
        "WINE"
    }

    n = int(input())
    ans = 0

    for _ in range(n):
        s = input().strip()

        if s.isdigit():
            if int(s) < 18:
                ans += 1
        else:
            if s in alcohol:
                ans += 1

    print(ans)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdout = sys.__stdout__
    return out.getvalue().strip()

# provided sample
assert run(
"""5
18
VODKA
COKE
19
17
""") == "2", "sample 1"

# minimum-size input
assert run(
"""1
18
""") == "0", "minimum case"

# all alcoholic drinks
assert run(
"""3
BEER
WINE
VODKA
""") == "3", "all alcoholic"

# boundary ages
assert run(
"""4
17
18
19
0
""") == "2", "boundary ages"

# mixed safe and unsafe
assert run(
"""6
WATER
JUICE
5
TEQUILA
100
MILK
""") == "2", "mixed case"

# maximum-style repeated inputs
assert run(
"""5
1
2
3
4
5
""") == "5", "all underage"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single customer age 18 | 0 | Legal boundary age |
| Only alcoholic drinks | 3 | Drink lookup correctness |
| Ages 17, 18, 19, 0 | 2 | Strict comparison with 18 |
| Mixed drinks and ages | 2 | Combined logic |
| All underage ages | 5 | Every underage customer counted |

## Edge Cases

Consider the legal boundary age.

Input:

```
3
17
18
19
```

The algorithm processes each value numerically.

`17 < 18`, so the answer becomes 1.

`18 < 18` is false, so the answer stays 1.

`19 < 18` is also false.

The final output is:

```
1
```

This confirms the algorithm correctly treats exactly 18 as legal.

Now consider unknown drinks that are not alcoholic.

Input:

```
4
WATER
COKE
BEER
JUICE
```

The algorithm checks each word against the alcohol set.

`WATER` is not present.

`COKE` is not present.

`BEER` is present, so the answer increases to 1.

`JUICE` is not present.

The final output is:

```
1
```

This prevents the common mistake of treating every drink name as alcohol.

Finally, consider very small ages.

Input:

```
2
0
VODKA
```

The token `0` is numeric, so it is converted to integer 0. Since `0 < 18`, the answer becomes 1.

`VODKA` belongs to the alcohol set, so the answer becomes 2.

The final output is:

```
2
```

This confirms the algorithm correctly handles single-digit numeric strings as ages instead of drink names.
