---
title: "CF 106414N - Primemas"
description: "We need build an integer array with a given length. The only requirement is that every pair of different positions has a prime number as its sum. The values themselves only need to stay inside the allowed range, and any valid construction is accepted."
date: "2026-06-25T09:49:32+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106414
codeforces_index: "N"
codeforces_contest_name: "Rutgers University Programming Contest Spring 2026 - Open Division"
rating: 0
weight: 106414
solve_time_s: 28
verified: true
draft: false
---

[CF 106414N - Primemas](https://codeforces.com/problemset/problem/106414/N)

**Rating:** -  
**Tags:** -  
**Solve time:** 28s  
**Verified:** yes  

## Solution
## Problem Understanding

We need build an integer array with a given length. The only requirement is that every pair of different positions has a prime number as its sum. The values themselves only need to stay inside the allowed range, and any valid construction is accepted.

The key difficulty is that the condition applies to every pair, not just neighboring elements. With a large array, checking all pairs would involve too many operations, so the solution must create the array in a way where the property is obvious without testing each pair.

The length can reach $2 \cdot 10^5$, and the total length across test cases has the same bound. This rules out any approach that compares pairs, because that would take $O(n^2)$ work. Even a single test case with 200000 elements would create around 20 billion pairs, which cannot fit into the time limit. We need a construction that takes only linear time in the output size.

The tricky cases come from parity. A careless construction might accidentally create a pair with an even sum larger than 2, which can never be prime. For example, an array with input `3` could not be built as `2 4 6`, because the pair `2 + 4 = 6` is not prime. The correct output can be:

```
3
```

producing:

```
1 1 2
```

The sums are `1 + 1 = 2`, `1 + 2 = 3`, and `1 + 2 = 3`, all prime.

Another edge case is the smallest allowed length. For input:

```
2
```

the array only has one pair to satisfy. A construction like:

```
1 2
```

works because the only sum is `3`. A solution that assumes there must be several equal values still needs to handle this case.

## Approaches

A direct approach would try to generate some numbers and verify all pair sums. The verification is easy: for every pair of indices, compute the sum and test whether it is prime. The problem is the number of pairs. For $n$ elements there are $\frac{n(n-1)}{2}$ pairs, which becomes about $2 \cdot 10^{10}$ when $n=200000$. Even before considering prime checks, this is too slow.

The useful observation comes from looking at parity. Any prime number except 2 is odd. If two numbers have the same parity, their sum is even. That means two even numbers cannot appear together, because their sum would be an even number greater than 2. Two odd numbers can only work when their sum is exactly 2, which means both numbers must be 1.

This leaves a very simple structure. We can put as many `1`s as we want, because every pair of `1`s gives the prime number 2. We can add exactly one even number, because it only needs to form prime sums with the ones. Choosing `2` works because `1 + 2 = 3`, which is prime.

The final array is always a sequence of `n - 1` ones followed by a single `2`. The construction does not need any search, primality testing, or special handling.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n) | O(1) besides output | Accepted |

## Algorithm Walkthrough

1. Read the required array length `n`.
2. Create `n - 1` copies of the value `1`. Any two of these elements sum to `2`, which is prime.
3. Append one final value `2`. Every sum involving this value and a `1` becomes `3`, which is also prime.
4. Output the constructed array.

The reason this construction works is that it avoids all dangerous pairs. The only repeated value is `1`, and the only even value is `2`, so no pair can create an even composite number.

Why it works: the invariant is that every pair in the generated array is either two `1`s or one `1` and one `2`. The first case always gives sum `2`, and the second case always gives sum `3`. Since both values are prime, every possible pair satisfies the condition.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        n = int(input())
        ans.append(" ".join(["1"] * (n - 1) + ["2"]))

    print("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The code directly follows the construction from the algorithm. For each test case, it creates exactly `n - 1` ones and adds one final `2`.

The multiplication or primality logic that a brute force solution would need is completely avoided. The array is valid by construction, so the program only spends time creating the required output.

The list size is controlled by `n`, and Python integers are easily large enough because the largest printed value is only `2`. There are no indexing decisions or boundary calculations that can introduce off by one errors beyond making sure the number of ones is exactly `n - 1`.

## Worked Examples

Consider the input:

```
2
2
3
```

For the first test case:

| Step | n | Created ones | Current array |
| --- | --- | --- | --- |
| Start | 2 | 0 | [] |
| Add ones | 2 | 1 | [1] |
| Add final value | 2 | 1 | [1, 2] |

The only pair has sum `1 + 2 = 3`, so the construction is valid.

For the second test case:

| Step | n | Created ones | Current array |
| --- | --- | --- | --- |
| Start | 3 | 0 | [] |
| Add ones | 3 | 2 | [1, 1] |
| Add final value | 3 | 2 | [1, 1, 2] |

The pair sums are:

| Pair | Sum |
| --- | --- |
| First 1 and second 1 | 2 |
| First 1 and 2 | 3 |
| Second 1 and 2 | 3 |

All possible pairs produce primes. This trace shows why duplicates are safe when the duplicated value is `1`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each element printed is created once |
| Space | O(n) | The output array for each test case contains n values |

The total size of all test cases is at most $2 \cdot 10^5$, so the linear construction easily fits the limits. The solution performs no pair checks and no prime calculations.

## Test Cases

```python
import sys
import io

def solve(inp: str) -> str:
    data = inp.strip().split()
    t = int(data[0])
    idx = 1
    out = []

    for _ in range(t):
        n = int(data[idx])
        idx += 1
        out.append(" ".join(["1"] * (n - 1) + ["2"]))

    return "\n".join(out)

# provided style samples
assert solve("2\n2\n3\n") == "1 2\n1 1 2"

# minimum size
assert solve("1\n2\n") == "1 2"

# all generated values must handle larger output sizes
assert len(solve("1\n10\n").split()) == 10

# repeated ones case
assert solve("1\n5\n") == "1 1 1 1 2"

# boundary style case
assert solve("1\n3\n") == "1 1 2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2` | `1 2` | Minimum valid length |
| `3` | `1 1 2` | The first case with repeated values |
| `5` | `1 1 1 1 2` | Correct placement of the single even number |
| `10` | Ten numbers | Linear construction for larger sizes |

## Edge Cases

For `n = 2`, the algorithm creates one `1` and one `2`:

```
Input:
1
2
```

The output is:

```
1 2
```

There is only one pair, and its sum is `3`. The construction does not rely on having multiple copies of `1`, so the smallest input is handled naturally.

For a large number of elements, such as:

```
1
6
```

the output is:

```
1 1 1 1 1 2
```

Every pair among the first five elements gives `2`, and every pair containing the last element gives `3`. The algorithm never creates two even values, which avoids the common parity mistake.

For arrays with many equal values, such as:

```
1
5
```

the result is:

```
1 1 1 1 2
```

A naive implementation might think duplicates are dangerous, but the duplicate value `1` is exactly what makes the construction work because two copies add up to the smallest prime number.
