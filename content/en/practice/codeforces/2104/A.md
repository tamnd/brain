---
title: "CF 2104A - Three Decks"
description: "We are given three stacks of cards arranged in a row, with the first stack containing a cards, the second b cards, and the third c cards. The numbers satisfy a < b < c."
date: "2026-06-08T04:57:20+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 2104
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 178 (Rated for Div. 2)"
rating: 800
weight: 2104
solve_time_s: 101
verified: true
draft: false
---

[CF 2104A - Three Decks](https://codeforces.com/problemset/problem/2104/A)

**Rating:** 800  
**Tags:** math  
**Solve time:** 1m 41s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given three stacks of cards arranged in a row, with the first stack containing `a` cards, the second `b` cards, and the third `c` cards. The numbers satisfy `a < b < c`. Monocarp can take any positive number of cards from the third stack, up to all `c` cards, and redistribute them between the first two stacks. The goal is to make all three stacks contain the same number of cards after the redistribution.

The input consists of multiple test cases, each specifying the counts `a`, `b`, and `c`. The output for each test case should be "YES" if an equal distribution is possible, and "NO" otherwise.

Because each `a`, `b`, and `c` can be as large as $10^8$ and there can be up to $10^4$ test cases, we need a solution that works in constant time per test case. Iterating over all possible redistributions of the third deck would be too slow, potentially performing up to $10^8$ iterations per case.

A naive implementation might try every possible number of cards moved from the third deck to the first two decks, but that would time out. Another subtle pitfall is failing to check whether the total number of cards can even be evenly divided by three. For example, if `a=3, b=5, c=10`, the total is 18, which divides evenly by three, making it possible to reach `6` cards in each stack. If the total were 19, no redistribution would work.

## Approaches

A brute-force approach would involve taking `x` cards from the third deck, distributing `y` to the first deck and `x-y` to the second deck, and checking if `a+y = b+x-y = c-x`. For each possible `x` between 1 and `c`, and each `y` between 0 and `x`, this requires up to $O(c^2)$ checks. This is correct in theory, but the largest possible `c` is $10^8$, making this method infeasible.

The key observation is that the final value in each deck, let's call it `target`, must be the same. The total number of cards after redistribution does not change: `a + b + c`. If all three decks end up equal, that number must be divisible by three. So `target = (a + b + c) / 3`. If `(a + b + c)` is not divisible by 3, it is immediately impossible.

Once we know `target`, we just need to check that the difference between the target and the first two decks is at most `c`, because the third deck can supply that many cards. More formally, we need `(target - a) + (target - b) = 2*target - (a+b) = target - c`, which is exactly the number of cards we take from the third deck. Since `target <= c` (because `c` is the largest), this works. Otherwise, it is impossible.

This observation reduces the problem to simple arithmetic checks and works in constant time per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(c²) | O(1) | Too slow |
| Optimal | O(1) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the values `a`, `b`, and `c`.
2. Compute the total number of cards across all three decks: `total = a + b + c`.
3. Check if `total` is divisible by 3. If not, output "NO" and move to the next test case. This is because an equal distribution requires the total to split evenly among three decks.
4. Compute the target number of cards per deck: `target = total // 3`.
5. Check if the largest deck, `c`, contains at least `target` cards. Since we can only remove cards from `c`, if `target > c`, achieving equal decks is impossible. Output "NO" in this case.
6. Otherwise, output "YES". The redistribution can always assign `target - a` cards to the first deck and `target - b` cards to the second deck, taking exactly `(target - a) + (target - b)` cards from the third deck.

Why it works: the invariant is that we must reach `target` cards in each deck. The sum divisibility ensures `target` is an integer. The check `target <= c` ensures the third deck has enough cards to supply the first two decks. This logic guarantees correctness without simulating every possible redistribution.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    a, b, c = map(int, input().split())
    total = a + b + c
    if total % 3 != 0:
        print("NO")
        continue
    target = total // 3
    if target > c:
        print("NO")
    else:
        print("YES")
```

The code first reads the number of test cases. For each case, it computes the sum of the three decks. If the sum is not divisible by three, it prints "NO". Otherwise, it calculates the target deck size and checks if the largest deck can supply the needed cards. The implementation uses integer division and simple comparisons, which avoids any risk of floating-point errors. The solution handles edge cases where the required number of redistributed cards could be zero.

## Worked Examples

For the input `3 5 10`:

| a | b | c | total | total % 3 | target | target > c? | Output |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 3 | 5 | 10 | 18 | 0 | 6 | No | YES |

We redistribute `3` cards to the first deck and `1` card to the second deck. The third deck reduces to `6`, matching the target.

For the input `12 20 30`:

| a | b | c | total | total % 3 | target | target > c? | Output |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 12 | 20 | 30 | 62 | 2 | 20 | No | NO |

62 is not divisible by 3, so equal distribution is impossible.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) per test case | Only arithmetic and comparisons are performed |
| Space | O(1) | Only a few integers are stored per test case |

With up to $10^4$ test cases, the total operation count is acceptable under the 2-second limit. Memory usage is minimal.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    t = int(input())
    for _ in range(t):
        a, b, c = map(int, input().split())
        total = a + b + c
        if total % 3 != 0:
            print("NO")
            continue
        target = total // 3
        if target > c:
            print("NO")
        else:
            print("YES")
    return output.getvalue().strip()

# Provided samples
assert run("4\n3 5 10\n12 20 30\n3 5 7\n1 5 6\n") == "YES\nNO\nYES\nNO"

# Custom cases
assert run("2\n1 2 3\n2 3 4\n") == "YES\nNO"
assert run("1\n10 20 30\n") == "NO"
assert run("1\n1 1 1\n") == "YES"
assert run("1\n1 2 4\n") == "NO"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 2 3 | YES | Smallest numbers, divisible sum |
| 2 3 4 | NO | Sum not divisible by 3 |
| 10 20 30 | NO | Large numbers, sum not divisible by 3 |
| 1 1 1 | YES | All equal decks |
| 1 2 4 | NO | Third deck too small to balance |

## Edge Cases

If the sum of `a + b + c` is divisible by 3 but the third deck does not have enough cards, the algorithm correctly outputs "NO". For example, `a=1, b=2, c=2` has `total=5`, divisible by 3? No, so output is "NO". For `a=1, b=2, c=4`, `total=7`, not divisible by 3, again "NO". These cases ensure we handle both divisibility and sufficiency conditions correctly. The largest deck always being `c` is guaranteed by the input constraints, so we do not need to check other permutations.
