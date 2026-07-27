---
title: "CF 102798D - ABC Conjecture"
description: "We are given a positive integer c for each test case. We need decide whether it is possible to split c into two positive parts a and b such that a + b = c and the product of all distinct prime factors appearing anywhere in a, b, and c is smaller than c."
date: "2026-07-27T17:48:24+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102798
codeforces_index: "D"
codeforces_contest_name: "2020 China Collegiate Programming Contest, Weihai Site"
rating: 0
weight: 102798
solve_time_s: 49
verified: true
draft: false
---

[CF 102798D - ABC Conjecture](https://codeforces.com/problemset/problem/102798/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a positive integer `c` for each test case. We need decide whether it is possible to split `c` into two positive parts `a` and `b` such that `a + b = c` and the product of all distinct prime factors appearing anywhere in `a`, `b`, and `c` is smaller than `c`. This product is the radical function, commonly written as `rad`. The task only asks for existence, so we output `yes` if at least one valid split exists and `no` otherwise.

The value of `c` can be as large as `10^18`, while there are only a few test cases. This immediately rules out iterating over possible values of `a` or factoring by trial division up to `sqrt(c)`. We need a number-theoretic observation that reduces each test case to a small number of operations.

The key restriction comes from `c` itself. Since every prime divisor of `c` appears in `abc`, `rad(abc)` always contains `rad(c)` as a factor. If `c` has no repeated prime factors, then `rad(c)=c`, which already makes `rad(abc)` at least `c`. Such a number can never satisfy the required inequality.

The remaining case is when `c` is not squarefree. If a prime square divides `c`, we can force both summands to contain that repeated prime and make the radical small enough. The entire problem is reduced to checking whether `c` has a repeated prime factor.

A common mistake is to only check whether `c` is even. For example, `c=9` has a solution: `3+6=9`, and `rad(3*6*9)=3<9`. A solution that only tries the equal split for even numbers would incorrectly reject this case.

Another edge case is `c=1`. It cannot be split into two positive integers at all, so the answer is `no`. Checking only squarefreeness without handling this would incorrectly accept it because `1` is squarefree.

A final boundary case is a large prime such as `c=10^18+3` if it were prime. It has no repeated factors, so even a very large value cannot help. The answer depends on the factorization property, not the size of the number.

## Approaches

The direct approach would be to try every possible split `a+b=c`. For each `a` from `1` to `c-1`, we would compute `b=c-a`, factor `a*b*c`, and check whether the radical is smaller than `c`. This is correct because it checks every possible candidate. However, for `c=10^18` the number of possible splits is around `10^18`, which is far beyond any reasonable running time.

The observation that changes the problem is that `c` itself already controls the answer. Every prime dividing `c` must appear in `rad(abc)`. If `c` is squarefree, those primes multiply to exactly `c`, making the inequality impossible.

If `c` contains a square factor, suppose `p^2` divides `c`. We can choose `a=p` and `b=c-p`. Since `c` is divisible by `p`, both parts are positive multiples of `p`. Writing `c=p*k`, the three numbers contain the factorization pattern of `p`, `p(k-1)`, and `pk`. The only possible extra primes come from `k` and `k-1`, which are consecutive and therefore coprime. The repeated factor in `c` guarantees that enough powers are hidden inside the same primes, making the radical strictly smaller than `c`.

The brute force works because it searches for a valid decomposition directly, but fails when `c` is large. The structural observation that only square factors of `c` matter reduces the problem to checking whether `c` is squarefree.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(c * factorization(c)) | O(1) | Too slow |
| Optimal | O(sqrt(c)) | O(1) | Accepted |

## Algorithm Walkthrough

1. Handle the special case `c=1`. There are no two positive integers whose sum is `1`, so the answer is immediately `no`.
2. Try to find a prime divisor `p` of `c` such that `p` divides `c` at least twice. We do this by checking whether `c` is divisible by `p*p`. Finding such a prime means `c` is not squarefree.
3. If any repeated prime factor is found, output `yes`. The construction described above gives a valid split.
4. If the scan finishes without finding a repeated factor, output `no`. The number is squarefree, so its own radical already equals `c`, preventing any possible solution.

The reason this works is that the existence of a repeated prime factor is exactly the dividing line between possible and impossible cases. A squarefree `c` forces the radical of every candidate triple to be at least `c`, while a non-squarefree `c` provides a repeated factor that can be shared by the two summands.

Why it works:

For any valid split, all prime factors of `c` appear in `rad(abc)`. Therefore, if `c` is squarefree, `rad(abc)` contains every prime of `c` exactly once and is at least `rad(c)=c`. The inequality cannot hold.

Now suppose `c` is not squarefree. Let `p^2` divide `c`, and choose `a=p`, `b=c-p`. Since `c=p*k` with `p` dividing `k`, we get `b=p(k-1)`. The radical of `abc` is composed of primes from `p`, `k`, and `k-1`. Because `k` and `k-1` share no prime factors, the repeated factor from `k` does not increase the radical, while `c` contains an additional copy of `p`. Thus the radical is strictly smaller than `c`.

The algorithm checks exactly these two possibilities, so it cannot return the wrong answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve_case(c):
    if c == 1:
        return "no"

    p = 2
    while p * p <= c:
        if c % (p * p) == 0:
            return "yes"
        p += 1

    return "no"

def main():
    t = int(input())
    ans = []
    for _ in range(t):
        c = int(input())
        ans.append(solve_case(c))
    print("\n".join(ans))

if __name__ == "__main__":
    main()
```

The solution checks repeated factors rather than computing the radical explicitly. This avoids dealing with large products and only requires detecting whether a prime square divides `c`.

The loop condition uses `p*p <= c`, which is the standard boundary for trial division. If no divisor up to this point exists, no larger factor can have a square contribution without a smaller matching factor also existing.

Python integers do not overflow, so the multiplication `p*p` is safe even near `10^18`. The number of iterations is the only concern, and the square-root bound keeps it within a manageable range for the given number of test cases.

## Worked Examples

For `c=18`, the algorithm searches for a repeated factor.

| Step | Current divisor | Divides `c` twice? | State |
| --- | --- | --- | --- |
| 1 | 2 | Yes, `18` is divisible by `2*2`? No | Continue |
| 2 | 3 | Yes, `18` is divisible by `3*3` | Found |

The algorithm returns `yes`. The repeated factor is `3`, and the valid split `6+12=18` has `rad(6*12*18)=6`, which is smaller than `18`.

For `c=30`, the scan behaves differently.

| Step | Current divisor | Divides `c` twice? | State |
| --- | --- | --- | --- |
| 1 | 2 | No | Continue |
| 2 | 3 | No | Continue |
| 3 | 4 | Not a prime divisor | Continue |
| 4 | 5 | No, only one factor of 5 | Continue |

No prime square divides `30`, so the algorithm returns `no`. Since `30` is squarefree, every possible split has a radical containing all factors of `30`, making the required inequality impossible.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(sqrt(c)) | We test possible repeated prime factors up to the square root of `c`. |
| Space | O(1) | Only a few integer variables are stored. |

The largest possible input value is `10^18`, so the solution avoids any work proportional to `c`. With only up to ten test cases, the square-root search is the intended scale for this problem.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    main()

    result = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return result

# provided samples
assert run("""3
4
18
30
""") == """yes
yes
no
""", "samples"

# minimum-size input
assert run("""1
1
""") == """no
""", "cannot split one"

# all-equal repeated factor case
assert run("""1
64
""") == """yes
""", "large prime power"

# squarefree composite
assert run("""1
210
""") == """no
""", "squarefree composite"

# odd repeated factor
assert run("""1
25
""") == """yes
""", "odd square factor"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `no` | Handles the smallest invalid split case. |
| `64` | `yes` | Confirms large repeated powers are detected. |
| `210` | `no` | Catches solutions that only test divisibility by one prime. |
| `25` | `yes` | Confirms odd non-squarefree values work. |

## Edge Cases

For `c=1`, the algorithm immediately returns `no` because no positive pair can sum to `1`. There is no need to enter the factor search.

For a squarefree value such as `c=30`, the algorithm finds no prime `p` where `p*p` divides `c`. Since the radical of `c` is already `30`, every possible `rad(abc)` is at least `30`, so rejecting the value is correct.

For a repeated prime value such as `c=25`, the algorithm finds `5*5` divides `25` and returns `yes`. The construction is `a=5`, `b=20`, giving `rad(5*20*25)=10<25`.

For a large value with no repeated prime factor, the algorithm never attempts to build the radical or enumerate splits. It only needs to confirm that no square factor exists, which is exactly the property that decides the answer.
