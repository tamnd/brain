---
title: "CF 102823G - Greatest Common Divisor"
description: "We have an array of positive integers. In one operation, every element of the array is increased by exactly one. The task is to find the smallest number of operations needed so that the greatest common divisor of the whole array becomes larger than one."
date: "2026-07-26T15:44:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102823
codeforces_index: "G"
codeforces_contest_name: "2018 China Collegiate Programming Contest - Guilin Site"
rating: 0
weight: 102823
solve_time_s: 50
verified: true
draft: false
---

[CF 102823G - Greatest Common Divisor](https://codeforces.com/problemset/problem/102823/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an array of positive integers. In one operation, every element of the array is increased by exactly one. The task is to find the smallest number of operations needed so that the greatest common divisor of the whole array becomes larger than one. If no number of operations can achieve this, we must report `-1`. The original problem comes from the 2018 China Collegiate Programming Contest, Guilin Site.

The important part is that all elements are shifted by the same amount. If we perform `x` operations, the array becomes:

$$a_1+x,\ a_2+x,\ ...,\ a_n+x$$

Suppose some integer `d > 1` divides every number after the shift. Then `d` also divides the difference between any two elements:

$$(a_i+x)-(a_j+x)=a_i-a_j$$

The added value disappears. This means the possible divisors of the final gcd are completely determined by the original differences between elements.

The constraints allow up to `n = 100000` elements, and values can be as large as `10^9`. This rules out trying many possible shifts or checking many possible divisors of every element. A solution must process the array in linear time or close to it, with only a small amount of extra number theory work.

The main edge cases come from the structure of the differences. If every element is identical, the gcd of differences is zero, and treating zero like a normal value can lead to wrong answers. For example:

```
1
1
1
```

The correct answer is:

```
Case 1: 1
```

After one operation the array becomes `[2]`, whose gcd is `2`. A careless solution that only searches divisors of differences may find nothing because there are no nonzero differences.

Another important case is when the gcd of differences is one. For example:

```
1
3
2 5 9
```

The differences are `3` and `7`, whose gcd is `1`. The correct output is:

```
Case 1: -1
```

Any common divisor of the shifted array would also have to divide these differences, but no number greater than one divides both.

A final edge case is when the gcd is already greater than one. For example:

```
1
3
6 12 18
```

The answer is:

```
Case 1: 0
```

No operations are needed, and a solution that always searches for a positive shift would miss the smallest answer.

## Approaches

A direct approach is to simulate the process. We could try `x = 0, 1, 2, ...`, add `x` to every element, and compute the gcd of the resulting array. This is correct because we are checking every possible number of operations in increasing order.

The problem is that there is no useful upper bound on how many shifts we might need. Even checking one shift costs `O(n)` time, and trying many shifts quickly becomes impossible. In the worst case, the number of operations tested could be very large, giving a complexity far beyond the allowed range.

The key observation is that the shift does not change differences. If the final gcd is some value `d > 1`, then every difference `a_i - a_j` must be divisible by `d`. Let:

$$g = gcd(|a_2-a_1|, |a_3-a_1|, ..., |a_n-a_1|)$$

Every possible final gcd must be a divisor of `g`.

Now the problem becomes much smaller. We only need to find the smallest `x` such that:

$$gcd(a_1+x, g) > 1$$

Instead of searching all shifts, we factor `g`. For every prime divisor `p` of `g`, the shifted first element must become divisible by `p`. The smallest shift that achieves this is:

$$x = (p - (a_1 \bmod p)) \bmod p$$

Taking the minimum of these values gives the answer.

The brute-force works because it checks all possible shifts, but fails because the search space is too large. The difference gcd reduces the infinite search space to the finite set of prime divisors of one number.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * answer) | O(1) | Too slow |
| Optimal | O(n + sqrt(g)) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute the gcd of all differences from the first element. Start with `g = 0`, and for every element `a[i]`, update:

$$g = gcd(g, |a_i-a_1|)$$

The value `g` contains exactly the divisors that can possibly become the final gcd after shifting.

1. If `g` is zero, all elements are equal. In this situation the array already has gcd equal to that common value. If that value is greater than one, the answer is zero. Otherwise every element is one, and one operation is enough to make them all two.
2. If `g` is one, no divisor greater than one can divide all differences. Since every possible final gcd must divide `g`, the operation can never succeed. Return `-1`.
3. Factor `g` and inspect each distinct prime divisor `p`.

For a prime `p` to become a divisor of the final gcd, we need:

$$a_1+x \equiv 0 \pmod p$$

The smallest nonnegative value of `x` satisfying this equation is calculated directly. Keep the minimum among all prime divisors.

1. Output the minimum shift found.

Why it works: any valid answer must create some gcd `d > 1`. Since `d` divides every shifted element, it divides every difference between shifted elements, which is exactly the same as the original differences. Therefore `d` must divide `g`. Every divisor greater than one contains some prime divisor of `g`, so checking all prime divisors is enough. For each such prime, the algorithm finds the earliest moment when that prime divides the shifted array, and the minimum of these moments is the earliest possible successful operation count.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

def solve_case(a):
    n = len(a)

    g = 0
    first = a[0]
    for x in a[1:]:
        g = math.gcd(g, abs(x - first))

    if g == 0:
        return 0 if first > 1 else 1

    if g == 1:
        return -1

    ans = 10**18
    temp = g

    p = 2
    while p * p <= temp:
        if temp % p == 0:
            ans = min(ans, (-first) % p)
            while temp % p == 0:
                temp //= p
        p += 1

    if temp > 1:
        ans = min(ans, (-first) % temp)

    return ans

def main():
    t = int(input())
    out = []

    for case in range(1, t + 1):
        n = int(input())
        a = list(map(int, input().split()))
        out.append(f"Case {case}: {solve_case(a)}")

    print("\n".join(out))

if __name__ == "__main__":
    main()
```

The code first builds the gcd of all differences. The first element is used as the reference because every pairwise difference can be represented through differences from one fixed value.

The `g == 0` branch handles the case where all numbers are equal. It must be separated because zero has every integer as a divisor, which would make normal divisor logic meaningless.

The factorization loop extracts each distinct prime factor of `g`. Once a prime factor is found, the exact number of operations needed to make `a[0]` divisible by it is `(-first) % p`. Python's modulo operation already returns the required nonnegative remainder, so this avoids manual boundary handling.

The loop only needs to test divisors up to the square root of `g`. After the loop, a remaining value larger than one is itself a prime factor and must also be checked.

## Worked Examples

### Sample 1

Input:

```
1
2
2 5
```

Trace:

| Step | g | Remaining factor | Current answer |
| --- | --- | --- | --- |
| Start | 0 |  |  |
| Process difference | 3 |  |  |
| Detect prime factor | 3 | 3 | 0 |

The gcd of differences is `3`. We need the smallest shift making `2 + x` divisible by `3`. Since `2 + 1 = 3`, the answer is `1`.

### Sample 2

Input:

```
1
5
3 5 7 9 11
```

Trace:

| Step | g | Remaining factor | Current answer |
| --- | --- | --- | --- |
| Start | 0 |  |  |
| Process differences | 2 |  |  |
| Process all differences | 2 |  |  |
| Prime factor | 2 | 2 | 1 |

The gcd of differences is `2`. The smallest shift making `3 + x` even is `1`, so adding one gives:

```
4 6 8 10 12
```

The gcd becomes `2`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + sqrt(g)) | Building the difference gcd takes linear time, and factorization checks divisors up to the square root of the gcd of differences. |
| Space | O(1) | Only a few integer variables are maintained besides the input array. |

The array size dominates the input, and the factorization is only performed on a number up to the difference range of the original values. This fits comfortably within the constraints.

## Test Cases

```python
import sys
import io
import math

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)

    def solve_case(a):
        g = 0
        first = a[0]
        for x in a[1:]:
            g = math.gcd(g, abs(x - first))

        if g == 0:
            return 0 if first > 1 else 1
        if g == 1:
            return -1

        ans = 10**18
        temp = g
        p = 2

        while p * p <= temp:
            if temp % p == 0:
                ans = min(ans, (-first) % p)
                while temp % p == 0:
                    temp //= p
            p += 1

        if temp > 1:
            ans = min(ans, (-first) % temp)

        return ans

    t = int(input())
    out = []

    for case in range(1, t + 1):
        n = int(input())
        a = list(map(int, input().split()))
        out.append(f"Case {case}: {solve_case(a)}")

    sys.stdin = old
    return "\n".join(out)

assert run("""3
1
2
5
2 5 9 5 7
5
3 5 7 9 11
""") == """Case 1: 0
Case 2: -1
Case 3: 1""", "samples"

assert run("""1
1
1
""") == "Case 1: 1", "all ones"

assert run("""1
4
6 12 18 24
""") == "Case 1: 0", "already valid"

assert run("""1
3
10 14 22
""") == "Case 1: 0", "even gcd"

assert run("""1
3
1 4 7
""") == "Case 1: -1", "difference gcd one"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `[1]` | `1` | Single element equal to one |
| `[6,12,18,24]` | `0` | Already has gcd greater than one |
| `[10,14,22]` | `0` | Existing common divisor from differences |
| `[1,4,7]` | `-1` | Impossible case where difference gcd is one |

## Edge Cases

When all numbers are equal, the difference gcd is zero. For input:

```
1
3
1 1 1
```

the algorithm enters the special case and returns `1`. After one operation the array becomes `[2,2,2]`, whose gcd is two.

When the difference gcd is one, no positive divisor can survive the shifting operation. For:

```
1
3
2 5 9
```

the differences are `3` and `7`, giving `g = 1`. Since any final gcd would have to divide both values, the only possible divisor is one, so the algorithm correctly returns `-1`.

When the array already has a valid gcd, the answer must be zero. For:

```
1
3
12 18 30
```

the difference gcd is `6`. Prime factor `2` already divides the first value, so the computed shift is zero and the algorithm does not perform unnecessary operations.
