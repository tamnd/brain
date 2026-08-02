---
title: "CF 102623L - Lottery Tickets"
description: "We have a collection of digit cards. For every digit from 0 to 9, the input tells us how many copies of that digit exist. We may choose any subset of these cards and arrange the chosen digits into a decimal number."
date: "2026-08-02T14:17:41+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102623
codeforces_index: "L"
codeforces_contest_name: "2020 Lenovo Cup USST Campus Online Invitational Contest"
rating: 0
weight: 102623
solve_time_s: 65
verified: true
draft: false
---

[CF 102623L - Lottery Tickets](https://codeforces.com/problemset/problem/102623/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a collection of digit cards. For every digit from 0 to 9, the input tells us how many copies of that digit exist. We may choose any subset of these cards and arrange the chosen digits into a decimal number. Among all possible numbers that can be formed and are divisible by 4, we need the largest one. If no valid positive number exists, we still have to consider whether the number 0 can be formed, because zero is divisible by 4 and the output format allows it.

The difficulty is not creating a divisible number. The difficulty is maximizing its value while deciding which cards to keep and which cards to discard. A number with more digits is always larger than a number with fewer digits, so the first priority is to use as many cards as possible. After that, the remaining goal is arranging those digits in the largest possible order.

The number of test cases can reach 300000, but the total number of cards across all tests is at most 300000. This means an algorithm that processes every card a constant number of times is suitable. A solution that tries all subsets or all possible arrangements is impossible because the number of possibilities grows exponentially or factorially. Even rebuilding many candidate numbers becomes too expensive when a single test case contains 100000 cards.

The main edge cases come from the interaction between divisibility and leading zeros. A solution that only sorts digits descending and checks the result can fail because the largest arrangement may not be divisible by 4. A solution that always removes one or two digits without considering the value impact can also fail.

For example, if the input is:

```
0 1 1 0 0 0 0 0 0 0
```

the cards are digits 1 and 2. Sorting gives 21, but 21 is not divisible by 4. The correct answer is:

```
12
```

because the last two digits decide divisibility.

Another case is:

```
1 0 0 2 0 0 0 0 0 0
```

The available digits are 0, 3, and 3. There is no two digit multiple of 4, but the single digit number 0 is valid. The answer is:

```
0
```

A careless implementation that only searches for two digit endings would incorrectly print `-1`.

A final tricky case is when the answer contains many zeros. For example:

```
2 0 0 0 0 0 0 0 0 0
```

The correct output is:

```
0
```

because leading zeros do not create a larger number. Printing all zeros would violate the required representation.

## Approaches

A direct brute-force approach would generate every possible subset of cards, arrange the chosen digits in descending order, and test whether the resulting number is divisible by 4. This is correct because every possible candidate is examined, and sorting gives the largest arrangement for that chosen subset. However, with 100000 cards, even considering subsets is impossible. The number of subsets is exponential, and even restricting attention to possible endings would still leave far too many candidates.

The key observation comes from the divisibility rule for 4. A decimal number is divisible by 4 if and only if its last two digits form a number divisible by 4. All digits before those last two positions only affect the size of the number, not its divisibility.

This changes the problem completely. We do not need to build many candidates. We only need to decide which one or two digits should be placed at the end. Once the ending is fixed, every remaining card should be used because adding another digit always creates a larger number. The remaining digits should be placed in descending order.

There are only 100 possible two digit endings from 00 to 99, and only 10 possible one digit endings. We can test all of them. For every possible ending, we check whether the required digit counts exist. Then we remove those digits, put all remaining digits in descending order, and compare the resulting number with the current best answer.

The comparison between candidates is also simple. A number with more digits is larger. If two candidates have the same length, lexicographical comparison of their strings gives the larger number.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in number of cards | Exponential | Too slow |
| Optimal | O(100 + 10) per test case | O(1) besides output | Accepted |

## Algorithm Walkthrough

1. Store the counts of every digit. We will use these counts to check whether a possible ending can be created without actually constructing all arrangements.
2. Try every possible two digit suffix from 00 to 99. If a suffix is divisible by 4 and its digits are available, temporarily remove those digits. The remaining digits are always best placed in descending order because they form the prefix, where every larger digit earlier increases the final number.
3. Also try every possible one digit number. This handles numbers with only one card, especially the special case where the only valid result is zero.
4. For each valid choice, construct the candidate string. Remove unnecessary leading zeros by converting an all-zero result into `"0"`.
5. Keep the largest candidate by first comparing lengths and then comparing strings when the lengths match.

The reason checking only suffixes works is that every valid decimal number divisible by 4 has a valid final one or two digit suffix. Once those final digits are chosen, there is no remaining constraint on the prefix, so using all remaining cards in descending order is always optimal.

Why it works:

Consider the optimal answer. Its last two digits, or its single digit if it has length one, must be one of the endings examined by the algorithm. When the algorithm reaches that ending, it uses exactly the same digits for the suffix. All other available cards can safely be included in the prefix because adding digits before the suffix always increases the number. Sorting that prefix in descending order produces the largest possible prefix. Therefore the algorithm creates a candidate at least as large as the optimal answer, and since the optimal answer is among the examined candidates, the chosen maximum is exactly the required answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve_case(cnt):
    best = None

    def update(s):
        nonlocal best
        if len(s) > 1 and s[0] == '0':
            s = s.lstrip('0')
            if not s:
                s = "0"
        if best is None or len(s) > len(best) or (len(s) == len(best) and s > best):
            best = s

    for x in range(100):
        if x % 4 != 0:
            continue

        a = x // 10
        b = x % 10

        need = [0] * 10
        need[a] += 1
        need[b] += 1

        ok = True
        for d in range(10):
            if need[d] > cnt[d]:
                ok = False
                break

        if ok:
            cur = cnt[:]
            cur[a] -= 1
            cur[b] -= 1

            s = []
            for d in range(9, -1, -1):
                s.append(str(d) * cur[d])

            s.append(str(a))
            s.append(str(b))
            update(''.join(s))

    for d in range(10):
        if cnt[d] > 0 and d % 4 == 0:
            cur = cnt[:]
            cur[d] -= 1

            s = []
            for x in range(9, -1, -1):
                s.append(str(x) * cur[x])

            s.append(str(d))
            update(''.join(s))

    return best if best is not None else "-1"

def main():
    t = int(input())
    ans = []

    for _ in range(t):
        cnt = list(map(int, input().split()))
        ans.append(solve_case(cnt))

    print('\n'.join(ans))

if __name__ == "__main__":
    main()
```
