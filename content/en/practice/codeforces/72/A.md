---
title: "CF 72A - Goshtasp, Vishtasp and Eidi"
description: "The problem asks us to decide whether a positive integer $n$ can be represented as a sum of distinct integers, where each integer is either 1 or a prime number. If such a representation exists, we need to produce one that is lexicographically largest."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 72
codeforces_index: "A"
codeforces_contest_name: "Unknown Language Round 2"
rating: 1800
weight: 72
solve_time_s: 78
verified: true
draft: false
---

[CF 72A - Goshtasp, Vishtasp and Eidi](https://codeforces.com/problemset/problem/72/A)

**Rating:** 1800  
**Tags:** *special, greedy, math  
**Solve time:** 1m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem asks us to decide whether a positive integer $n$ can be represented as a sum of distinct integers, where each integer is either 1 or a prime number. If such a representation exists, we need to produce one that is lexicographically largest. Lexicographically largest means that, when comparing sequences element by element, we prefer sequences where larger numbers appear earlier.

The input is a single integer $n$ with $1 \le n \le 10000$. This upper bound is small enough to allow algorithms that might examine all primes up to $n$ or perform some linear-time processing, but it rules out any brute-force approach that tries all subsets of primes, since the number of subsets grows exponentially.

Edge cases arise from small numbers and numbers that are themselves prime. For example, $n = 1$ should output `1=1`. If $n$ itself is a prime, the lexicographically largest solution is simply the singleton sequence `[n]`. Numbers like 4 need special handling, because `4 = 2 + 2` is not allowed (elements must be distinct), so the algorithm must consider combinations like `1 + 3`.

The main subtlety comes from the requirement that the numbers must be distinct and the answer must be lexicographically largest. A careless solution might just take the smallest primes and fill with ones, but that would not satisfy the lexicographic requirement.

## Approaches

A brute-force approach would enumerate all subsets of `1` and the primes up to `n` and check if their sum equals `n`. This is correct but infeasible for `n` up to 10000 because the number of subsets of primes grows exponentially, easily exceeding $2^{1229}$ subsets (the number of primes ≤ 10000).

The key observation is that if we want a lexicographically largest sequence, we should start from the largest possible numbers. For any $n$, if $n$ is prime, `[n]` is automatically the best sequence. If not, we can repeatedly pick the largest prime ≤ remaining sum, or 1 if no prime is small enough, and add it to the sequence. This greedy approach works because the numbers are distinct, and the largest-first approach guarantees the lexicographic preference. The remaining sum is always reduced, so the process terminates.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^π(n)) | O(n) | Too slow |
| Optimal Greedy | O(n√n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Generate all prime numbers up to $n$ using a sieve. The sieve ensures we can check if a number is prime in O(1) time.
2. If $n$ itself is prime, print `n=n` and terminate. This is trivially lexicographically largest.
3. Otherwise, initialize an empty list `answer` and set `remaining = n`.
4. Iterate over primes in descending order. For each prime $p$, if $p \le$ remaining, append it to `answer` and subtract it from `remaining`.
5. If `remaining > 0` after considering all primes, append `1`s as needed to sum to `n`. This works because `1` can be used multiple times but must be considered distinct in the sequence.
6. Print the sequence in the format `n=a1+a2+...+am`.

Why it works: At each step, we select the largest available prime, which ensures lexicographic maximality. Since we only pick primes ≤ remaining, we never overshoot. Any leftover amount can be filled with `1`s to ensure the sum is exactly `n`. The sequence remains distinct because primes are naturally distinct, and `1` is treated separately. This greedy approach is guaranteed to produce a valid representation if one exists.

## Python Solution

```python
import sys
input = sys.stdin.readline

def sieve(limit):
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, limit + 1, i):
                is_prime[j] = False
    primes = [i for i, val in enumerate(is_prime) if val]
    return primes

def main():
    n = int(input())
    primes = sieve(n)
    
    if n in primes or n == 1:
        print(f"{n}={n}")
        return
    
    answer = []
    remaining = n
    for p in reversed(primes):
        if p <= remaining:
            answer.append(p)
            remaining -= p
    answer.extend([1] * remaining)
    result = '+'.join(map(str, answer))
    print(f"{n}={result}")

if __name__ == "__main__":
    main()
```

The sieve generates all primes ≤ `n` efficiently. We handle the trivial prime or `1` case first. The descending iteration ensures we pick the largest primes for lexicographic maximality. Extending with `1`s ensures we hit the exact sum when leftover is small. Off-by-one errors are avoided by using `<= remaining` and including `remaining` 1s at the end.

## Worked Examples

### Input: 11

| remaining | prime selected | answer list |
| --- | --- | --- |
| 11 | 11 | [11] |
| 0 | done | [11] |

The largest prime ≤ 11 is 11 itself. Remaining becomes 0, so we output `11=11`. Lexicographically largest because the largest number appears first.

### Input: 8

| remaining | prime selected | answer list |
| --- | --- | --- |
| 8 | 7 | [7] |
| 1 | no prime ≤ 1 | [7,1] |

We pick 7, leaving 1. We fill with a `1` to get `[7,1]`. Output `8=7+1`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n√n) | Sieve runs in O(n log log n), descending prime selection in O(n). |
| Space | O(n) | Storing sieve array and answer list. |

Given `n ≤ 10000`, this algorithm runs comfortably within the 5-second limit and 256 MB memory limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    main()
    return sys.stdout.getvalue().strip()

# provided sample
assert run("11\n") == "11=11", "sample 1"
# custom cases
assert run("1\n") == "1=1", "minimum value"
assert run("4\n") == "4=3+1", "needs combination with 1"
assert run("8\n") == "8=7+1", "combination with largest prime first"
assert run("28\n") == "28=23+5", "sum of two primes"
assert run("10\n") == "10=7+3", "largest primes sum to n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 1=1 | minimum input handled |
| 4 | 4=3+1 | non-trivial combination with 1 |
| 8 | 8=7+1 | greedy selection of largest prime |
| 28 | 28=23+5 | multiple primes needed |
| 10 | 10=7+3 | sum of two primes |

## Edge Cases

For `n = 1`, the sieve produces no primes ≤ 1, but we handle `n == 1` separately, giving `1=1`. For `n` itself being prime, like `11`, the algorithm terminates immediately with `[n]`, guaranteeing the largest element appears first. For numbers like `4`, the largest prime ≤ 4 is 3, leaving a remainder 1. Adding `1` gives a valid sequence `[3,1]`. These checks ensure correctness for the smallest, prime, and combination cases.
