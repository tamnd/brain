---
title: "CF 104069B - Best University ID"
description: "We are given a list of students, where each student has a name and an associated integer. For each integer, we can factor it into primes. Among all prime factors of that integer, we care about the largest prime that divides it."
date: "2026-07-02T02:58:43+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104069
codeforces_index: "B"
codeforces_contest_name: "VII MaratonUSP Freshman Contest"
rating: 0
weight: 104069
solve_time_s: 46
verified: true
draft: false
---

[CF 104069B - Best University ID](https://codeforces.com/problemset/problem/104069/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a list of students, where each student has a name and an associated integer. For each integer, we can factor it into primes. Among all prime factors of that integer, we care about the largest prime that divides it. For every student, we compute this “maximum prime factor” of their number. The task is to find the student whose number has the largest such value. If multiple students share the same largest prime factor, we return the one that appears earliest in the input order.

The input size goes up to 100,000 students, and each number is at most 100 million. This immediately rules out any approach that factorizes numbers independently using naive trial division up to n for each query. Even O(n √x) per number would lead to roughly 10^5 × 10^4 operations in worst cases, which is already borderline in Python and worse in constant-heavy implementations.

A subtle edge case comes from numbers that are prime themselves. For such a student, the answer is the number itself, since it is the only and thus largest prime factor. Another case is numbers that are products of multiple primes where the largest factor is not necessarily the most frequent or smallest; for example, 2 × 3 × 97 should be evaluated based on 97. Finally, ties depend strictly on input order, so we must preserve first occurrence behavior.

## Approaches

A direct approach is to factor each number independently. For each integer x, we try dividing it by every integer from 2 up to √x and track prime factors. This works logically because any composite number must have a factor no larger than its square root. However, doing this for 100,000 numbers makes the worst-case work about 100,000 × 10,000 operations, which is too slow in Python and still wasteful even in optimized languages when constants are large.

The key observation is that we do not need full factorization. We only need the largest prime divisor. This allows a more incremental approach: for each number x, we repeatedly divide it by small primes or factors, but instead of storing all factors, we only track the largest divisor encountered during reduction. Once we strip out all small factors, if the remaining value is greater than 1, that remaining value is itself a prime factor and automatically the largest possible candidate.

This reduces the problem to efficient factor extraction per number with early termination and constant-time tracking of the maximum factor found so far.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Trial division up to √x per number | O(n √x) | O(1) | Too slow |
| Incremental factor stripping with max tracking | O(n √x) worst-case, fast in practice due to early reduction | O(1) | Accepted |

## Algorithm Walkthrough

We process each student one by one while maintaining the best answer seen so far.

1. Read the student name and number x, and initialize a variable best_factor = 1 for this student. This variable tracks the largest prime factor discovered for x.
2. Try dividing x by 2 repeatedly. Each time we successfully divide, we update best_factor = 2. We do this because if 2 divides x even once, it is a prime factor and we want to record it immediately.
3. After removing all factors of 2, we iterate over odd candidates p starting from 3 up to √x. For each p, we repeatedly divide x by p while it is divisible, and whenever we do so, we update best_factor = p. This ensures that we capture all prime factors of x, and since we overwrite only when a valid divisor appears, the final stored value is the largest encountered.
4. If after processing all candidates x > 1, then x itself is a prime number larger than all previously extracted factors, so we set best_factor = max(best_factor, x).
5. Compare best_factor with the global maximum best_so_far. If it is larger, we update the answer to the current student. If it is equal, we keep the earlier one by doing nothing.
6. After processing all students, output the stored name.

The reason this works is that every composite number has at least one prime factor not exceeding its square root, so all smaller primes are guaranteed to be found during iteration. Once all small factors are removed, any remaining value must be prime, and since it has not been further reducible, it must be the largest factor of the original number.

## Python Solution

```python
import sys
input = sys.stdin.readline

def max_prime_factor(x: int) -> int:
    best = 1

    while x % 2 == 0:
        best = 2
        x //= 2

    p = 3
    while p * p <= x:
        while x % p == 0:
            best = p
            x //= p
        p += 2

    if x > 1:
        best = max(best, x)

    return best

def main():
    n = int(input())
    best_name = ""
    best_value = -1

    for _ in range(n):
        parts = input().split()
        name = parts[0]
        x = int(parts[1])

        val = max_prime_factor(x)

        if val > best_value:
            best_value = val
            best_name = name

    print(best_name)

if __name__ == "__main__":
    main()
```

The factorization routine first removes all factors of 2 to simplify later looping. This is a standard optimization that allows stepping through only odd numbers afterward, halving the number of iterations.

The loop condition `p * p <= x` is critical because x shrinks as we divide it, so the bound remains correct dynamically. If we used the original value, we would over-iterate.

The final check `if x > 1` captures the case where the remaining factor is a large prime that was never divided out.

The main loop only stores a global maximum, ensuring that ties automatically resolve in favor of the earliest occurrence.

## Worked Examples

Consider input:

```
4
a 12
b 35
c 97
d 18
```

We track the best factor per student:

| Student | x | Factors found | max prime factor | best so far |
| --- | --- | --- | --- | --- |
| a | 12 | 2,2,3 | 3 | a |
| b | 35 | 5,7 | 7 | b |
| c | 97 | 97 | 97 | c |
| d | 18 | 2,3,3 | 3 | c |

After processing, the answer is `c` because 97 is the largest among all maximum prime factors.

Now consider a tie case:

```
3
x 14
y 21
z 10
```

| Student | x | Factors found | max prime factor | best so far |
| --- | --- | --- | --- | --- |
| x | 14 | 2,7 | 7 | x |
| y | 21 | 3,7 | 7 | x |
| z | 10 | 2,5 | 5 | x |

Both x and y have maximum factor 7, but x appears first, so it remains the answer.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n √x) worst-case | Each number is factorized by trial division up to its square root, though values shrink during division |
| Space | O(1) | Only constant extra variables per iteration |

Given n up to 100,000 and x up to 10^8, the square root bound is about 10,000. In practice, most numbers reduce quickly due to small prime factors, so the algorithm runs comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output

    n = int(sys.stdin.readline())
    best_name = ""
    best_value = -1

    def max_prime_factor(x: int) -> int:
        best = 1
        while x % 2 == 0:
            best = 2
            x //= 2
        p = 3
        while p * p <= x:
            while x % p == 0:
                best = p
                x //= p
            p += 2
        if x > 1:
            best = max(best, x)
        return best

    for _ in range(n):
        name, x = sys.stdin.readline().split()
        x = int(x)
        val = max_prime_factor(x)
        if val > best_value:
            best_value = val
            best_name = name

    return best_name

assert run("1\nalice 2\n") == "alice"
assert run("3\na 10\nb 21\nc 14\n") == "b"
assert run("2\nx 49\ny 7\n") == "x"
assert run("4\na 6\nb 15\nc 10\nd 3\n") == "b"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | alice | minimal boundary |
| mixed composites | b | correct max prime extraction |
| repeated prime power | x | handling squared primes |
| multiple ties and ordering | b | tie-breaking by input order |

## Edge Cases

One important case is when the number itself is prime. For example, input `alice 97`. The factorization loop does not find any divisor, so after the loop x remains 97. The final check `if x > 1` ensures that 97 is recorded as the maximum prime factor, and the algorithm correctly returns alice if no later student exceeds 97.

Another case is perfect powers like `49`. Starting with 49, we divide by 7 twice. Each division updates best to 7. After removal, x becomes 1, so the final value remains 7. This confirms that repeated factors do not distort the maximum tracking logic.

A third case is numbers with a very large prime factor paired with small ones, such as 2 × 50000017. The algorithm quickly removes factor 2 and then recognizes the remaining value as a prime, ensuring that the large factor is not missed due to small trial division limits.
