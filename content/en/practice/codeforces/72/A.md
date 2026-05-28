---
title: "CF 72A - Goshtasp, Vishtasp and Eidi"
description: "We need to represent a positive integer as a sum of distinct values, where every chosen value is either the number 1 or a prime number. If no such representation exists, we print 0. The output format is slightly unusual. We do not print only the numbers."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 72
codeforces_index: "A"
codeforces_contest_name: "Unknown Language Round 2"
rating: 1800
weight: 72
solve_time_s: 100
verified: true
draft: false
---

[CF 72A - Goshtasp, Vishtasp and Eidi](https://codeforces.com/problemset/problem/72/A)

**Rating:** 1800  
**Tags:** *special, greedy, math  
**Solve time:** 1m 40s  
**Verified:** yes  

## Solution
## Problem Understanding

We need to represent a positive integer as a sum of distinct values, where every chosen value is either the number 1 or a prime number. If no such representation exists, we print `0`.

The output format is slightly unusual. We do not print only the numbers. We print an equality like:

```
24=19+5
```

Among all valid representations, we must output the lexicographically largest sequence.

Lexicographic comparison works exactly like dictionary order. We compare the first elements, then the second, and so on. If one sequence ends earlier, we temporarily append zeroes to the shorter sequence during comparison. Because of this rule, larger earlier numbers are always preferable, and shorter sequences are not automatically better.

The constraint is tiny, only `n ≤ 10000`. That means even algorithms with quadratic or exponential behavior over small subsets may survive. We can comfortably generate all primes up to `10000`, try combinations, or run dynamic programming over sums.

The real difficulty is not performance. The challenge is understanding what the lexicographically largest sequence actually looks like.

Several edge cases are easy to mishandle.

For `n = 1`, the answer is simply:

```
1=1
```

A careless implementation might reject it because 1 is not prime. The statement explicitly allows the number 1.

For `n = 2`, the answer is:

```
2=2
```

Using `1+1` is illegal because numbers must be distinct.

For `n = 4`, the answer is:

```
4=3+1
```

An implementation that greedily takes the largest prime and then recursively solves the rest without checking distinctness may accidentally produce `2+2`.

Another subtle case is lexicographic order. For `n = 10`, these are both valid:

```
10=7+3
10=5+3+2
```

The correct answer is the first one because `7 > 5` at the first differing position. Minimizing the number of terms is not the objective, but the lexicographic rule naturally pushes us toward the largest possible first number.

The sequence order also matters. We are free to print numbers in any order, so the lexicographically largest representation should always be sorted in descending order.

## Approaches

A brute-force solution would generate every subset of valid numbers `{1} ∪ {primes ≤ n}` and check whether the subset sum equals `n`. Since there are roughly 1229 primes below `10000`, this is completely impossible. Even restricting ourselves to smaller candidates still leaves exponential complexity.

A more realistic brute-force method uses dynamic programming over subsets or recursive backtracking. For each prime, we either take it or skip it. Since `n` is only `10000`, memoization on `(position, remaining_sum)` works. The state count is manageable, around `1229 × 10000`.

The brute-force DP is correct because every valid representation corresponds to some path through the recursion tree. The problem is that reconstructing the lexicographically largest answer becomes messy. We would need careful tie-breaking between many equivalent states.

The key observation is that the structure of valid answers is much simpler than it first appears.

We want the lexicographically largest sequence. That means the first number should be as large as possible.

Suppose `p` is the largest prime not exceeding `n`.

If `p = n`, then the answer is immediately `[n]`, which is clearly optimal because no first element can exceed `n`.

Otherwise, we want to know whether the remaining value `n - p` can be represented using distinct allowed numbers that do not reuse `p`.

Now comes the crucial simplification.

Every integer except `2` can be represented as a sum of distinct primes and possibly `1`. In fact, for this problem, after taking the largest possible prime first, the remaining value is always small enough to finish greedily.

Trying the largest prime first is always optimal lexicographically. If it works, no alternative with a smaller first number can beat it.

So the problem reduces to repeatedly taking the largest unused prime that keeps the remaining sum representable.

Because `n ≤ 10000`, we can simply use recursive search with memoization and always iterate candidates in descending order. The first valid construction we find is automatically lexicographically largest.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^π(n)) | O(π(n)) | Too slow |
| Optimal | O(n × π(n)) | O(n × π(n)) | Accepted |

Here `π(n)` denotes the number of primes up to `n`.

## Algorithm Walkthrough

1. Generate all primes up to `10000` using the sieve of Eratosthenes.

We need fast access to every usable prime candidate.
2. Build a list containing all allowed numbers.

This list is:

```
[largest primes ..., 2, 1]
```

Descending order is critical because we want the lexicographically largest answer.
3. Use DFS with memoization.

The recursive state is:

```
dfs(index, remaining)
```

where `index` tells us which candidates are still available and `remaining` is the sum we still need to build.
4. At each state, try taking the current number first.

If the recursive call succeeds, prepend the current number to the returned sequence and stop immediately.

Since we process candidates from largest to smallest, the first successful solution is lexicographically optimal.
5. If taking the current number fails, skip it and continue.
6. When `remaining == 0`, return an empty sequence.

This means we successfully built the target sum.
7. When we exhaust candidates or `remaining < 0`, return failure.
8. Print the answer in the required format.

If no solution exists, print `0`.

### Why it works

The recursion explores all subsets of distinct allowed numbers, so any valid representation is reachable.

Candidates are processed in descending order. Whenever the algorithm chooses a number, it only does so after verifying that a complete solution exists below it. The first successful branch has the largest possible first element. The same logic recursively applies to the suffix of the sequence.

That exactly matches lexicographic maximization.

Memoization guarantees that each state is solved once, so repeated subproblems do not explode exponentially.

## Python Solution

```python
import sys
from functools import lru_cache

input = sys.stdin.readline

def sieve(limit):
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False

    for i in range(2, int(limit ** 0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, limit + 1, i):
                is_prime[j] = False

    return [i for i in range(2, limit + 1) if is_prime[i]]

def solve():
    n = int(input())

    primes = sieve(n)
    nums = primes[::-1] + [1]

    @lru_cache(None)
    def dfs(idx, rem):
        if rem == 0:
            return ()

        if idx == len(nums) or rem < 0:
            return None

        cur = nums[idx]

        if cur <= rem:
            take = dfs(idx + 1, rem - cur)
            if take is not None:
                return (cur,) + take

        return dfs(idx + 1, rem)

    ans = dfs(0, n)

    if ans is None:
        print(0)
        return

    expr = "+".join(map(str, ans))
    print(f"{n}={expr}")

solve()
```

The sieve computes all primes up to `n`. Since the limit is tiny, the standard `O(n log log n)` sieve is more than enough.

The candidate list is stored in descending order because lexicographic maximization depends entirely on trying larger numbers first.

The recursive function returns either a tuple representing a valid suffix or `None` if the state is impossible. Returning the actual sequence directly makes reconstruction simple.

The line:

```
if take is not None:
    return (cur,) + take
```

is the key greedy choice. The moment we find a valid continuation using a larger number, we stop searching smaller alternatives.

Memoization is essential. Without it, many states such as `(idx, rem)` would be recomputed repeatedly.

The recursion always advances `idx + 1`, which guarantees distinctness. No number can be reused.

## Worked Examples

### Example 1

Input:

```
11
```

Execution trace:

| Step | Current Candidate | Remaining Before | Action | Remaining After |
| --- | --- | --- | --- | --- |
| 1 | 11 | 11 | Take | 0 |

Constructed sequence:

```
[11]
```

Output:

```
11=11
```

This demonstrates the strongest possible lexicographic case. A single prime equal to `n` immediately dominates every other representation.

### Example 2

Input:

```
10
```

Execution trace:

| Step | Current Candidate | Remaining Before | Action | Remaining After |
| --- | --- | --- | --- | --- |
| 1 | 7 | 10 | Take | 3 |
| 2 | 5 | 3 | Skip | 3 |
| 3 | 3 | 3 | Take | 0 |

Constructed sequence:

```
[7, 3]
```

Output:

```
10=7+3
```

This trace shows why descending order matters. Although `5+3+2` is also valid, the algorithm prefers `7` immediately because it gives a lexicographically larger sequence.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n × π(n)) | Each DP state `(index, remaining)` is solved once |
| Space | O(n × π(n)) | Memoization table stores all reachable states |

The number of primes below `10000` is small, roughly 1229. The total state count stays well within acceptable limits for a 5-second limit and 256 MB memory limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from functools import lru_cache

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def sieve(limit):
        is_prime = [True] * (limit + 1)
        is_prime[0] = is_prime[1] = False

        for i in range(2, int(limit ** 0.5) + 1):
            if is_prime[i]:
                for j in range(i * i, limit + 1, i):
                    is_prime[j] = False

        return [i for i in range(2, limit + 1) if is_prime[i]]

    n = int(input())

    primes = sieve(n)
    nums = primes[::-1] + [1]

    @lru_cache(None)
    def dfs(idx, rem):
        if rem == 0:
            return ()

        if idx == len(nums) or rem < 0:
            return None

        cur = nums[idx]

        if cur <= rem:
            take = dfs(idx + 1, rem - cur)
            if take is not None:
                return (cur,) + take

        return dfs(idx + 1, rem)

    ans = dfs(0, n)

    if ans is None:
        return "0\n"

    expr = "+".join(map(str, ans))
    return f"{n}={expr}\n"

# provided sample
assert run("11\n") == "11=11\n", "sample 1"

# minimum input
assert run("1\n") == "1=1\n", "single allowed non-prime"

# distinctness check
assert run("4\n") == "4=3+1\n", "cannot use 2 twice"

# lexicographic ordering
assert run("10\n") == "10=7+3\n", "7+3 beats 5+3+2"

# larger prime
assert run("9973\n") == "9973=9973\n", "large prime input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `1=1` | Handles the special allowed value `1` |
| `4` | `4=3+1` | Prevents reuse of identical numbers |
| `10` | `10=7+3` | Correct lexicographic maximization |
| `9973` | `9973=9973` | Large prime boundary case |

## Edge Cases

For input:

```
1
```

The algorithm builds the candidate list:

```
[1]
```

The DFS immediately takes `1`, reducing the remaining sum to `0`.

Output:

```
1=1
```

This confirms that the implementation correctly treats `1` as a valid allowed number even though it is not prime.

For input:

```
4
```

The candidate list is:

```
[3, 2, 1]
```

The algorithm first takes `3`, leaving `1`. Then it takes `1`.

Sequence:

```
[3, 1]
```

It never produces `2+2` because recursion always moves to the next index after taking a number, preventing reuse.

For input:

```
10
```

The DFS first attempts `7`. Since the remaining value `3` is solvable, the algorithm commits immediately.

It never explores representations beginning with `5`, because any such representation is lexicographically worse.

Output:

```
10=7+3
```

This confirms that descending exploration combined with early stopping correctly implements lexicographic maximization.
