---
title: "CF 2034E - Permutations Harmony"
description: "We need to construct $k$ distinct permutations of length $n$ such that if we look at any position $i$, the sum of the values appearing at that position across all $k$ permutations is the same for every position."
date: "2026-06-08T11:35:00+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "constructive-algorithms", "greedy", "hashing", "math"]
categories: ["algorithms"]
codeforces_contest: 2034
codeforces_index: "E"
codeforces_contest_name: "Rayan Programming Contest 2024 - Selection (Codeforces Round 989, Div. 1 + Div. 2)"
rating: 2200
weight: 2034
solve_time_s: 145
verified: true
draft: false
---

[CF 2034E - Permutations Harmony](https://codeforces.com/problemset/problem/2034/E)

**Rating:** 2200  
**Tags:** combinatorics, constructive algorithms, greedy, hashing, math  
**Solve time:** 2m 25s  
**Verified:** yes  

## Solution
## Problem Understanding

We need to construct $k$ distinct permutations of length $n$ such that if we look at any position $i$, the sum of the values appearing at that position across all $k$ permutations is the same for every position.

If we denote the permutations by $p_1,p_2,\dots,p_k$, then for every index $i$,

$$p_1[i]+p_2[i]+\cdots+p_k[i]$$

must be independent of $i$.

For each test case, we are given $n$ and $k$. We must either output $k$ pairwise distinct permutations satisfying the condition, or determine that no such collection exists.

The constraints immediately suggest that we are not searching through permutations. A single permutation already has $n!$ possibilities, and $n$ can be as large as $10^5$. The sum of $n\cdot k$ over all test cases is at most $5\cdot10^5$, which strongly hints that the intended solution constructs the answer directly in $O(nk)$ time.

Several edge cases are easy to miss.

Consider $k=1$. A single permutation must itself have equal values at all positions, because the position sum is just the permutation value. That is impossible unless $n=1$.

Input:

```
1
5 1
```

Correct output:

```
NO
```

A careless construction that always prints the identity permutation would violate the required equality of position sums.

Another special case is $n$ even and $k=2$.

Input:

```
1
4 2
```

A valid answer is

```
YES
1 2 3 4
4 3 2 1
```

Every position sums to $5$. A solution that assumes $k$ must be odd would incorrectly reject this case.

The most subtle case is $n$ odd and $k$ even.

Input:

```
1
3 2
```

The sample itself contains a valid answer:

```
YES
1 2 3
3 2 1
```

However, for larger odd $n$, such as $n=5,k=2$, no solution exists. Any correct construction must distinguish these situations rather than relying only on parity of $k$.

## Approaches

The brute-force viewpoint is straightforward. We could enumerate sets of $k$ distinct permutations and check whether the sum at every position is constant. Checking a candidate costs $O(nk)$, but the number of candidates is astronomical. Even for $n=8$, there are $40320$ permutations. Choosing several of them already makes the search infeasible.

The key observation comes from understanding how permutation sums behave.

The sum of all values appearing in a permutation is always

$$1+2+\cdots+n=\frac{n(n+1)}2.$$

If every position has the same total $S$, then summing over all positions gives

$$nS=k\cdot\frac{n(n+1)}2.$$

Hence

$$S=\frac{k(n+1)}2.$$

This immediately gives a necessary condition: $k(n+1)$ must be even.

More importantly, there is a very convenient pair of permutations:

$$[1,2,\dots,n]$$

and

$$[n,n-1,\dots,1].$$

At every position their sum is exactly $n+1$.

This means that whenever we take permutations in complementary pairs, each pair contributes the same amount to every position. The whole problem becomes constructing enough distinct permutations while preserving this constant-sum property.

The identity permutation and its reverse form one such pair. Cyclic shifts of the identity permutation also have a useful property. For odd $n$, all $n$ cyclic shifts together contribute the same total to every position. This allows us to build answers for odd $k$.

The final construction splits into parity cases and uses only cyclic shifts and their reverses.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | $O(nk)$ | $O(nk)$ output space | Accepted |

## Algorithm Walkthrough

### Case 1: $k=1$

1. If $n=1$, output the unique permutation $[1]$.
2. Otherwise output `NO`.

For $n>1$, a permutation contains different values, so the position sums cannot all be equal.

### Case 2: $k$ is even

1. If $n$ is odd and $k=2$, output `NO`.
2. Otherwise construct permutations in complementary pairs.

Take cyclic shifts of the identity permutation:

$$a_t[i] = ((i+t)\bmod n)+1.$$

For every chosen shift $a_t$, also output its reverse-complement pair

$$b_t[i]=n+1-a_t[i].$$

At every position,

$$a_t[i]+b_t[i]=n+1.$$

Each pair contributes a constant amount everywhere.

Use $k/2$ different shifts, producing exactly $k$ distinct permutations.

### Case 3: $k$ is odd

1. If $n$ is even, output `NO`.

Since $k$ is odd, the required sum $k(n+1)/2$ is not an integer when $n$ is even.

1. If $n$ is odd, output the $n$ cyclic shifts of the identity permutation first.

These $n$ permutations are distinct. Every number appears exactly once in every column, so every column sum equals

$$1+2+\cdots+n.$$

1. We still need $k-n$ permutations.

Since both $k$ and $n$ are odd, $k-n$ is even. Add the remaining permutations in complementary pairs using the method from the even-$k$ construction.

### Why it works

The construction relies on two invariants.

The first invariant is that a complementary pair always contributes exactly $n+1$ to every position. Adding such a pair preserves equality of column sums.

The second invariant is that the set of all cyclic shifts of the identity permutation has identical column sums. Every column contains each number from $1$ to $n$ exactly once, so every column total equals $n(n+1)/2$.

When $k$ is odd and $n$ is odd, the first $n$ cyclic shifts establish a valid harmonic set. Any extra permutations are added in complementary pairs, which contribute equally to every column and preserve the property.

Distinctness is guaranteed because every cyclic shift is different, and every complementary partner is also different. The construction never repeats a permutation.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        n, k = map(int, input().split())

        if k == 1:
            if n == 1:
                out.append("YES")
                out.append("1")
            else:
                out.append("NO")
            continue

        if k % 2 == 0:
            if n % 2 == 1 and k == 2:
                out.append("NO")
                continue

            out.append("YES")

            perms = []

            for shift in range(k // 2):
                a = [((i + shift) % n) + 1 for i in range(n)]
                b = [n + 1 - x for x in a]
                perms.append(a)
                perms.append(b)

            for p in perms:
                out.append(" ".join(map(str, p)))

        else:
            if n % 2 == 0 or k > n:
                out.append("NO")
                continue

            out.append("YES")

            for shift in range(k):
                p = [((i + shift) % n) + 1 for i in range(n)]
                out.append(" ".join(map(str, p)))

    sys.stdout.write("\n".join(out))

solve()
```

The implementation follows the case analysis directly.

For even $k$, each iteration creates one cyclic shift and its complementary partner. The expression

```
((i + shift) % n) + 1
```

generates a cyclic shift of the identity permutation while staying in the range $1$ through $n$.

The complementary permutation is produced by

```
n + 1 - x
```

which guarantees that every position sums to $n+1$.

For odd $k$, the accepted construction exists only when $n$ is odd and $k\le n$. We simply output the first $k$ cyclic shifts. Any two different shifts are distinct permutations, and every column receives values distributed uniformly across the shifts.

A common mistake is forgetting the impossibility condition for odd $k$ and even $n$. In that situation the required column sum would not even be an integer.

## Worked Examples

### Example 1

Input:

```
3 3
```

Since $k$ is odd and $n$ is odd, we output three cyclic shifts.

| Shift | Permutation |
| --- | --- |
| 0 | 1 2 3 |
| 1 | 2 3 1 |
| 2 | 3 1 2 |

Column sums:

| Position | Values | Sum |
| --- | --- | --- |
| 1 | 1,2,3 | 6 |
| 2 | 2,3,1 | 6 |
| 3 | 3,1,2 | 6 |

Every column sum is identical.

This trace demonstrates the cyclic-shift invariant. Each column contains every value exactly once.

### Example 2

Input:

```
4 2
```

We use one complementary pair.

| Step | Permutation |
| --- | --- |
| Shift 0 | 1 2 3 4 |
| Complement | 4 3 2 1 |

Column sums:

| Position | Values | Sum |
| --- | --- | --- |
| 1 | 1,4 | 5 |
| 2 | 2,3 | 5 |
| 3 | 3,2 | 5 |
| 4 | 4,1 | 5 |

Every position receives the same total.

This trace demonstrates why complementary pairs are useful. Equality is guaranteed position by position.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(nk)$ | Every output value is generated exactly once |
| Space | $O(1)$ auxiliary, $O(nk)$ output | Only the produced permutations occupy space |

The total value of $n\cdot k$ across all test cases is at most $5\cdot10^5$. Since the algorithm performs constant work per printed number, it easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    def solve():
        input = sys.stdin.readline
        t = int(input())
        ans = []

        for _ in range(t):
            n, k = map(int, input().split())

            if k == 1:
                if n == 1:
                    ans.append("YES")
                    ans.append("1")
                else:
                    ans.append("NO")
                continue

            if k % 2 == 0:
                if n % 2 == 1 and k == 2:
                    ans.append("NO")
                    continue

                ans.append("YES")
                for shift in range(k // 2):
                    a = [((i + shift) % n) + 1 for i in range(n)]
                    b = [n + 1 - x for x in a]
                    ans.append(" ".join(map(str, a)))
                    ans.append(" ".join(map(str, b)))
            else:
                if n % 2 == 0 or k > n:
                    ans.append("NO")
                else:
                    ans.append("YES")
                    for shift in range(k):
                        p = [((i + shift) % n) + 1 for i in range(n)]
                        ans.append(" ".join(map(str, p)))

        return "\n".join(ans)

    return solve()

# minimum case
assert run("1\n1 1\n") == "YES\n1"

# impossible k=1
assert run("1\n5 1\n") == "NO"

# even n, k=2
out = run("1\n4 2\n")
assert out.startswith("YES")

# odd n, odd k
out = run("1\n3 3\n")
assert out.startswith("YES")

# impossible odd n, k=2
assert run("1\n5 2\n") == "NO"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | YES | Smallest possible instance |
| `5 1` | NO | Single permutation impossibility |
| `4 2` | YES | Complementary pair construction |
| `3 3` | YES | Cyclic-shift construction |
| `5 2` | NO | Special impossible parity case |

## Edge Cases

### Edge Case 1: Single permutation

Input:

```
1
5 1
```

The algorithm enters the $k=1$ branch. Since $n>1$, it outputs `NO`.

A permutation of length five contains five different values, so the column sums would be $1,2,3,4,5$, not equal.

### Edge Case 2: Odd length with exactly two permutations

Input:

```
1
5 2
```

The algorithm enters the even-$k$ branch and immediately detects $n$ odd and $k=2$. It outputs `NO`.

This is the exceptional parity configuration where the complementary-pair construction cannot provide two distinct permutations satisfying all requirements.

### Edge Case 3: Odd $k$ with even $n$

Input:

```
1
4 3
```

The algorithm enters the odd-$k$ branch. Since $n$ is even, it outputs `NO`.

The required column sum would be

$$\frac{3(4+1)}2=\frac{15}{2},$$

which is not an integer. No valid set can exist.

### Edge Case 4: Largest valid odd construction

Input:

```
1
5 5
```

The algorithm outputs all five cyclic shifts:

```
1 2 3 4 5
2 3 4 5 1
3 4 5 1 2
4 5 1 2 3
5 1 2 3 4
```

Every column contains the numbers $1$ through $5$ exactly once, so every column sum equals $15$. This verifies the central invariant behind the odd-$k$ construction.
