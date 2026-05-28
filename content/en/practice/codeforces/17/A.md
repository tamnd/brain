---
title: "CF 17A - Noldbach problem"
description: "We are given two integers, n and k. We look at all prime numbers from 2 up to n. Among those primes, we want to count how many can be written in the form:"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 17
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 17"
rating: 1000
weight: 17
solve_time_s: 106
verified: true
draft: false
---
[CF 17A - Noldbach problem](https://codeforces.com/problemset/problem/17/A)

**Rating:** 1000  
**Tags:** brute force, math, number theory  
**Solve time:** 1m 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two integers, `n` and `k`. We look at all prime numbers from `2` up to `n`. Among those primes, we want to count how many can be written in the form:

$$p_i + p_{i+1} + 1$$

where `p_i` and `p_{i+1}` are neighboring primes, meaning consecutive primes in increasing order.

For example, the consecutive primes `5` and `7` produce:

$$5 + 7 + 1 = 13$$

Since `13` is also prime, it counts.

The task is to determine whether at least `k` primes up to `n` satisfy this property. If yes, print `YES`, otherwise print `NO`.

The constraints are very small. `n` is at most `1000`, so even fairly inefficient prime generation methods are acceptable. A quadratic algorithm over all numbers up to `1000` still runs instantly. This changes the focus of the problem from optimization to correctness and clean implementation.

The tricky part is interpreting the condition correctly. We are not checking whether a number can be written as the sum of any two primes plus one. The two primes must be consecutive in the ordered list of primes.

Consider this input:

```
27 2
```

The valid constructions are:

$$5 + 7 + 1 = 13$$

and

$$7 + 11 + 1 = 19$$

Both `13` and `19` are prime and at most `27`, so the answer is `YES`.

A common mistake is to allow non-neighboring primes. For example:

```
20 1
```

A careless implementation might use:

$$3 + 13 + 1 = 17$$

and conclude that `17` counts. That is wrong because `3` and `13` are not neighboring primes. The correct neighboring pairs are `(2,3)`, `(3,5)`, `(5,7)`, `(7,11)`, and so on.

Another easy mistake is forgetting that the generated number itself must also be prime and must not exceed `n`.

For example:

```
10 1
```

Using neighboring primes:

$$2 + 3 + 1 = 6$$

`6` is not prime, so it does not count.

$$3 + 5 + 1 = 9$$

`9` is also not prime.

No valid numbers exist, so the correct answer is `NO`.

One more edge case is `k = 0`. In that situation the answer is always `YES`, because having at least zero valid primes is automatically true.

Example:

```
2 0
```

The correct output is:

```
YES
```

A solution that only checks whether it found some valid numbers could incorrectly print `NO`.

## Approaches

The most direct brute-force approach is to test every number from `2` to `n` and try all pairs of primes to see whether the number can be represented as:

$$p_i + p_j + 1$$

while also checking whether the primes are neighboring.

Since there are roughly `168` primes up to `1000`, this approach is still small enough to pass. The worst-case work is around:

$$1000 \times 168^2$$

which is only a few million operations.

The brute-force method works because the constraints are tiny, but it does unnecessary work. The expression we care about is completely determined by consecutive primes. Once the list of primes is known, every valid candidate is simply:

$$p_i + p_{i+1} + 1$$

There is no reason to test arbitrary combinations.

This observation simplifies the problem dramatically. We first generate all primes up to `n`. Then we iterate through consecutive pairs of primes, compute the candidate value, and check whether that candidate itself is prime and at most `n`.

To make primality checks fast, we store all primes in a set. Then membership testing becomes constant time.

The structure of the problem naturally leads to this solution because the condition already specifies consecutive primes. Instead of searching for representations of numbers, we directly generate all possible representations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(P²) | O(P) | Accepted |
| Optimal | O(n log log n) | O(n) | Accepted |

Here `P` is the number of primes up to `n`.

## Algorithm Walkthrough

1. Generate all prime numbers from `2` to `n` using the Sieve of Eratosthenes.

The sieve is simple and reliable for small constraints. It also gives fast primality lookup later.
2. Store all generated primes in both a list and a set.

The list preserves the order of primes, which is necessary for accessing neighboring primes. The set allows constant-time checks for whether a number is prime.
3. Iterate through consecutive prime pairs.

For every index `i`, take:

$$primes[i] \text{ and } primes[i+1]$$
4. Compute:

$$candidate = primes[i] + primes[i+1] + 1$$

This is exactly the form required by the problem.
5. Check whether the candidate is in the prime set and does not exceed `n`.

If both conditions hold, increase the count.
6. After processing all neighboring pairs, compare the count with `k`.

If the count is at least `k`, print `YES`. Otherwise print `NO`.

### Why it works

The algorithm examines every possible expression allowed by the problem definition, because every valid number must come from exactly one pair of neighboring primes. No valid candidate is skipped.

For each consecutive pair, we compute the only number that pair can produce. Checking membership in the prime set guarantees that we count only primes. Since every counted value satisfies the required construction and every possible construction is tested, the final count is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())

    is_prime = [True] * (n + 1)

    if n >= 0:
        is_prime[0] = False
    if n >= 1:
        is_prime[1] = False

    for i in range(2, int(n ** 0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = False

    primes = []
    for i in range(2, n + 1):
        if is_prime[i]:
            primes.append(i)

    prime_set = set(primes)

    count = 0

    for i in range(len(primes) - 1):
        candidate = primes[i] + primes[i + 1] + 1

        if candidate <= n and candidate in prime_set:
            count += 1

    print("YES" if count >= k else "NO")

solve()
```

The first section builds the sieve. `is_prime[x]` tells us whether `x` is prime. Starting from `i * i` avoids redundant work because smaller multiples were already handled by smaller primes.

After the sieve, we collect all primes into a list. Their order matters because the problem specifically requires neighboring primes.

The set version of the primes is used for fast lookup. Without it, checking whether a candidate is prime would require repeated linear searches or repeated primality tests.

The loop over consecutive pairs is the core of the solution. Using `range(len(primes) - 1)` prevents accessing beyond the end of the list when reading `primes[i + 1]`.

The condition:

```
candidate <= n and candidate in prime_set
```

is important. Even if the generated number is prime, it only counts if it lies within the allowed range.

Finally, we compare the count with `k` and print the required answer.

## Worked Examples

### Example 1

Input:

```
27 2
```

Generated primes:

$$[2, 3, 5, 7, 11, 13, 17, 19, 23]$$

| Neighboring Primes | Candidate | Prime? | Count |
| --- | --- | --- | --- |
| 2, 3 | 6 | No | 0 |
| 3, 5 | 9 | No | 0 |
| 5, 7 | 13 | Yes | 1 |
| 7, 11 | 19 | Yes | 2 |
| 11, 13 | 25 | No | 2 |
| 13, 17 | 31 | Too large | 2 |
| 17, 19 | 37 | Too large | 2 |
| 19, 23 | 43 | Too large | 2 |

Final count is `2`, which is at least `k = 2`, so the output is:

```
YES
```

This trace shows how only neighboring primes are considered and how candidates larger than `n` are ignored.

### Example 2

Input:

```
45 7
```

Primes up to `45`:

$$[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43]$$

| Neighboring Primes | Candidate | Prime? | Count |
| --- | --- | --- | --- |
| 2, 3 | 6 | No | 0 |
| 3, 5 | 9 | No | 0 |
| 5, 7 | 13 | Yes | 1 |
| 7, 11 | 19 | Yes | 2 |
| 11, 13 | 25 | No | 2 |
| 13, 17 | 31 | Yes | 3 |
| 17, 19 | 37 | Yes | 4 |
| 19, 23 | 43 | Yes | 5 |
| 23, 29 | 53 | Too large | 5 |

Only `5` valid primes exist, but `k = 7`, so the answer is:

```
NO
```

This example demonstrates that the count can stop growing long before all primes are processed.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log log n) | Sieve of Eratosthenes dominates the runtime |
| Space | O(n) | Arrays and sets storing primality information |

With `n ≤ 1000`, the runtime is tiny. The sieve and all loops finish almost instantly within the time limit, and the memory usage is negligible compared to the available `64 MB`.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n, k = map(int, input().split())

    is_prime = [True] * (n + 1)

    if n >= 0:
        is_prime[0] = False
    if n >= 1:
        is_prime[1] = False

    for i in range(2, int(n ** 0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = False

    primes = []

    for i in range(2, n + 1):
        if is_prime[i]:
            primes.append(i)

    prime_set = set(primes)

    count = 0

    for i in range(len(primes) - 1):
        candidate = primes[i] + primes[i + 1] + 1

        if candidate <= n and candidate in prime_set:
            count += 1

    print("YES" if count >= k else "NO")

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    return sys.stdout.getvalue().strip()

# provided samples
assert run("27 2\n") == "YES", "sample 1"
assert run("45 7\n") == "NO", "sample 2"

# minimum input
assert run("2 0\n") == "YES", "k=0 should always work"

# no valid constructions
assert run("10 1\n") == "NO", "no prime fits the condition"

# exactly one valid prime
assert run("13 1\n") == "YES", "13 = 5 + 7 + 1"

# boundary around valid count
assert run("19 2\n") == "YES", "13 and 19 both count"

# impossible large k
assert run("1000 1000\n") == "NO", "count can never reach 1000"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 0` | `YES` | Handles `k = 0` correctly |
| `10 1` | `NO` | Rejects non-prime candidates |
| `13 1` | `YES` | Detects a single valid construction |
| `19 2` | `YES` | Counts multiple valid neighboring pairs |
| `1000 1000` | `NO` | Handles impossible large targets |

## Edge Cases

Consider the input:

```
20 1
```

The algorithm generates neighboring prime pairs:

$$(2,3), (3,5), (5,7), (7,11), \dots$$

Their candidates are:

$$6, 9, 13, 19, \dots$$

`13` and `19` are valid because they are prime and at most `20`.

The algorithm never considers expressions like:

$$3 + 13 + 1 = 17$$

because `3` and `13` are not neighboring primes. This prevents overcounting.

Now consider:

```
10 1
```

The candidates are:

$$2 + 3 + 1 = 6$$

and

$$3 + 5 + 1 = 9$$

Neither is prime. The prime-set lookup correctly rejects both values, so the count remains `0` and the output becomes `NO`.

Finally, consider:

```
2 0
```

The prime list contains only `[2]`, so there are no neighboring pairs at all. The count stays `0`.

The final comparison checks:

$$0 \ge 0$$

which is true, so the algorithm prints `YES`. This handles the empty-case logic correctly without any special branching.
