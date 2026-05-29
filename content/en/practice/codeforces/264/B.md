---
title: "CF 264B - Good Sequences"
description: "We are given a strictly increasing array of integers. We want to build the longest subsequence such that every pair of neighboring numbers shares at least one common prime factor."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dp", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 264
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 162 (Div. 1)"
rating: 1500
weight: 264
solve_time_s: 116
verified: true
draft: false
---

[CF 264B - Good Sequences](https://codeforces.com/problemset/problem/264/B)

**Rating:** 1500  
**Tags:** dp, number theory  
**Solve time:** 1m 56s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a strictly increasing array of integers. We want to build the longest subsequence such that every pair of neighboring numbers shares at least one common prime factor.

Since the original array is already strictly increasing, any subsequence automatically preserves increasing order. The real condition is about adjacency: for every consecutive pair in the chosen subsequence, the gcd must be greater than 1.

For example, in the array `2 3 4 6 9`, the subsequence `2 4 6 9` works because:

- `gcd(2,4)=2`
- `gcd(4,6)=2`
- `gcd(6,9)=3`

Its length is 4.

The constraints are large enough that quadratic dynamic programming is impossible. With `n` up to `10^5`, checking every previous element for every current element would require roughly `10^10` comparisons in the worst case, far beyond the time limit. We need something close to linear or `n log n`.

The values are also bounded by `10^5`, which is extremely useful. Whenever values are small, prime factorization and sieve-based preprocessing become attractive.

A few edge cases are easy to mishandle.

Consider this input:

```
1
1
```

The correct answer is:

```
1
```

Even though `1` has no prime factors, a sequence of length 1 is always valid because there are no adjacent pairs to violate the gcd condition. A careless implementation that only updates states through prime factors may incorrectly output 0.

Another tricky case is when numbers do not connect transitively.

```
3
6 35 10
```

The correct answer is:

```
2
```

We can take `6 -> 10` or `35 -> 10`, but not all three. Although `6` shares a factor with `10`, and `35` shares a factor with `10`, the pair `6` and `35` is coprime. A naive “component merging” idea would fail here because the relation is not transitive.

Repeated prime factors inside one number can also create bugs.

```
2
12 18
```

The correct answer is:

```
2
```

The prime factors of `12` are `{2,3}`, not `{2,2,3}`. If we process duplicate factors separately, we may accidentally reuse updates from the same number and inflate the answer incorrectly.

## Approaches

The most direct dynamic programming idea is:

Let `dp[i]` be the length of the longest valid subsequence ending at `a[i]`.

To compute `dp[i]`, we check every previous position `j < i`. If `gcd(a[j], a[i]) > 1`, then we may extend the subsequence ending at `j`.

The transition becomes:

```
dp[i] = 1 + max(dp[j])
```

over all valid `j`.

This is correct because every valid subsequence ending at `a[i]` must come from some earlier compatible value. The problem is complexity. We would examine every pair of indices, giving `O(n^2)` gcd checks. With `n = 10^5`, that becomes too slow.

The key observation is that compatibility depends only on shared prime factors.

Two numbers have gcd greater than 1 exactly when they share at least one prime divisor. Instead of remembering answers for every previous index, we can remember answers for every prime.

Suppose we maintain:

```
best[p] = longest valid subsequence whose last number is divisible by p
```

Now process numbers from left to right.

For a value `x`, factorize it into distinct primes. Any previous subsequence that can connect to `x` must end with one of those primes. So:

```
dp[x] = 1 + max(best[p])
```

over all prime divisors `p` of `x`.

After computing this value, we update all those primes:

```
best[p] = max(best[p], dp[x])
```

This reduces the problem from comparing against all earlier numbers to comparing against only the distinct prime divisors of the current number.

Since every number up to `10^5` has only a small number of distinct prime factors, the total work becomes very manageable.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(n^2)` | `O(n)` | Too slow |
| Optimal | `O(MAXA log log MAXA + n log MAXA)` | `O(MAXA)` | Accepted |

Here `MAXA = 10^5`.

## Algorithm Walkthrough

1. Precompute the smallest prime factor for every integer up to `10^5` using a sieve.

This allows us to factorize each number quickly.
2. Create an array `best` where `best[p]` stores the maximum length of a valid subsequence ending with a number divisible by prime `p`.
3. Process the input numbers from left to right.

Since the array is already strictly increasing, any subsequence we build automatically respects the increasing condition.
4. Factorize the current number `x` into its distinct prime divisors.

We only need distinct primes because the condition depends on sharing a prime factor, not on multiplicity.
5. Compute the best subsequence ending at `x`.

Initialize:

```
cur = 1
```

Then for every prime divisor `p` of `x`:

```
cur = max(cur, best[p] + 1)
```

If some previous subsequence ended with a number divisible by `p`, then appending `x` keeps the gcd condition valid.
6. Update all involved primes.

For every prime divisor `p` of `x`:

```
best[p] = max(best[p], cur)
```

Future numbers divisible by `p` may extend this subsequence.
7. Track the global maximum answer during processing.

### Why it works

The invariant is:

```
best[p]
```

always equals the maximum length of a valid subsequence whose last element is divisible by `p`, considering only numbers processed so far.

When processing a new number `x`, any valid predecessor must share at least one prime factor with `x`. So every extendable subsequence is represented in one of the corresponding `best[p]` values.

Taking the maximum over those primes finds the optimal predecessor. Updating the same primes afterward preserves the invariant for future elements.

Because every valid transition corresponds to sharing some prime factor, and every shared prime factor is checked, the algorithm never misses an optimal subsequence.

## Python Solution

```python
import sys
input = sys.stdin.readline

MAXA = 100000

def build_spf():
    spf = list(range(MAXA + 1))

    for i in range(2, int(MAXA ** 0.5) + 1):
        if spf[i] == i:
            for j in range(i * i, MAXA + 1, i):
                if spf[j] == j:
                    spf[j] = i

    return spf

def get_distinct_primes(x, spf):
    primes = []

    while x > 1:
        p = spf[x]
        primes.append(p)

        while x % p == 0:
            x //= p

    return primes

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    spf = build_spf()

    best = [0] * (MAXA + 1)

    ans = 1

    for x in a:
        if x == 1:
            ans = max(ans, 1)
            continue

        primes = get_distinct_primes(x, spf)

        cur = 1

        for p in primes:
            cur = max(cur, best[p] + 1)

        for p in primes:
            best[p] = max(best[p], cur)

        ans = max(ans, cur)

    print(ans)

solve()
```

The sieve computes the smallest prime factor for every value. Instead of trial division up to `sqrt(x)` for every number, we can repeatedly divide by the precomputed smallest prime factor. This makes factorization very fast.

The helper `get_distinct_primes` removes repeated factors. For example, `12` becomes `[2,3]` rather than `[2,2,3]`. That detail matters because repeated updates during the same iteration could accidentally reuse freshly updated values.

The array `best` is indexed directly by prime value. Since all numbers are at most `10^5`, allocating an array of size `100001` is cheap and faster than using dictionaries.

The special handling for `x == 1` is necessary because `1` has no prime divisors. A sequence containing only `1` is still valid, but it cannot connect to anything else.

The order of operations is also important. We first compute `cur` using the old `best` values, then update `best`. If we updated immediately while iterating through primes, one prime factor of the current number could incorrectly influence another factor from the same number.

## Worked Examples

### Example 1

Input:

```
5
2 3 4 6 9
```

| Current x | Prime factors | best before | cur | best after |
| --- | --- | --- | --- | --- |
| 2 | {2} | best[2]=0 | 1 | best[2]=1 |
| 3 | {3} | best[3]=0 | 1 | best[3]=1 |
| 4 | {2} | best[2]=1 | 2 | best[2]=2 |
| 6 | {2,3} | best[2]=2, best[3]=1 | 3 | best[2]=3, best[3]=3 |
| 9 | {3} | best[3]=3 | 4 | best[3]=4 |

Final answer:

```
4
```

This trace shows how prime-based states naturally represent all usable predecessors. The value `6` can extend sequences ending with either prime `2` or prime `3`, so it combines information from both.

### Example 2

Input:

```
4
7 10 15 21
```

| Current x | Prime factors | best before | cur | best after |
| --- | --- | --- | --- | --- |
| 7 | {7} | best[7]=0 | 1 | best[7]=1 |
| 10 | {2,5} | best[2]=0, best[5]=0 | 1 | best[2]=1, best[5]=1 |
| 15 | {3,5} | best[3]=0, best[5]=1 | 2 | best[3]=2, best[5]=2 |
| 21 | {3,7} | best[3]=2, best[7]=1 | 3 | best[3]=3, best[7]=3 |

Final answer:

```
3
```

The optimal subsequence is `10 -> 15 -> 21`. Even though `7` shares a factor with `21`, the algorithm correctly chooses the longer chain through prime `3`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(MAXA log log MAXA + n log MAXA)` | sieve preprocessing plus factorization of all numbers |
| Space | `O(MAXA)` | smallest prime factor array and DP array |

With `MAXA = 10^5`, the sieve is very small. Each number has only a few distinct prime factors, so the total processing easily fits within the 2-second limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

MAXA = 100000

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def build_spf():
        spf = list(range(MAXA + 1))

        for i in range(2, int(MAXA ** 0.5) + 1):
            if spf[i] == i:
                for j in range(i * i, MAXA + 1, i):
                    if spf[j] == j:
                        spf[j] = i

        return spf

    def get_distinct_primes(x, spf):
        primes = []

        while x > 1:
            p = spf[x]
            primes.append(p)

            while x % p == 0:
                x //= p

        return primes

    n = int(input())
    a = list(map(int, input().split()))

    spf = build_spf()

    best = [0] * (MAXA + 1)

    ans = 1

    for x in a:
        if x == 1:
            ans = max(ans, 1)
            continue

        primes = get_distinct_primes(x, spf)

        cur = 1

        for p in primes:
            cur = max(cur, best[p] + 1)

        for p in primes:
            best[p] = max(best[p], cur)

        ans = max(ans, cur)

    return str(ans)

# provided sample
assert run("5\n2 3 4 6 9\n") == "4", "sample 1"

# minimum size
assert run("1\n1\n") == "1", "single element"

# all numbers pairwise coprime
assert run("4\n2 3 5 7\n") == "1", "no valid extensions"

# repeated prime factors
assert run("2\n12 18\n") == "2", "duplicate prime factors handled"

# chain through alternating primes
assert run("5\n6 10 15 21 35\n") == "5", "long connected chain"

# disconnected middle element
assert run("3\n6 35 10\n") == "2", "cannot connect all three"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1` | `1` | Single-element sequence |
| `2 3 5 7` | `1` | No pair shares a factor |
| `12 18` | `2` | Distinct-prime extraction |
| `6 10 15 21 35` | `5` | Long transitive chain |
| `6 35 10` | `2` | Connectivity is not transitive |

## Edge Cases

Consider the smallest possible input:

```
1
1
```

The algorithm sees that `1` has no prime factors, so it cannot participate in any extension. Still, a single-element subsequence is valid. The special case keeps the answer at least 1, producing the correct result.

Now consider pairwise coprime numbers:

```
4
2 3 5 7
```

Processing each value gives no usable predecessor because every `best[p]` is initially zero. Every `cur` remains 1, so the final answer is 1. This confirms the algorithm does not create fake connections.

Next, examine repeated prime factors:

```
2
12 18
```

The distinct prime divisors are:

- `12 -> {2,3}`
- `18 -> {2,3}`

When processing `18`, the algorithm reads old values of `best[2]` and `best[3]`, both equal to 1, and computes `cur = 2`. Because repeated factors are removed, the number does not accidentally update itself multiple times during the same iteration.

Finally, consider a misleading transitive structure:

```
3
6 35 10
```

The transitions are:

- `6 -> 10` is valid
- `35 -> 10` is valid
- `6 -> 35` is invalid

While processing `35`, no shared primes exist with `6`, so its subsequence length stays 1. Later, `10` extends from `6` to produce length 2. The algorithm correctly avoids constructing the invalid chain of length 3.
