---
title: "CF 106403B - Clock Creation"
description: "We are designing a clock made from several independent gears. A gear with x teeth completes a full cycle every x seconds because it moves one tooth per second."
date: "2026-06-25T10:07:05+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106403
codeforces_index: "B"
codeforces_contest_name: "Bay Area Programming Contest 2026 Novice Division"
rating: 0
weight: 106403
solve_time_s: 39
verified: true
draft: false
---

[CF 106403B - Clock Creation](https://codeforces.com/problemset/problem/106403/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 39s  
**Verified:** yes  

## Solution
## Problem Understanding

We are designing a clock made from several independent gears. A gear with `x` teeth completes a full cycle every `x` seconds because it moves one tooth per second. All gears start aligned at time zero and move together, so the first moment when every gear returns to its initial position is the least common multiple of all gear sizes.

The task is to choose the gear sizes so that this first simultaneous return happens exactly after `k` seconds. Among all possible choices, we need the construction with the smallest total number of teeth.

The input contains several values of `k`. For each one, the output must describe one optimal set of gear sizes. The number of gears and the teeth count of every gear must be printed.

The value of `k` is at most `100000`, and there can be up to `10000` test cases. This means we cannot afford algorithms that try many combinations of gears. A search over possible subsets or partitions of factors would grow far too quickly. We need to use the mathematical structure of least common multiples and factorization.

The main edge cases come from the fact that the least common multiple only cares about the largest power of each prime that appears.

For example, if the input is:

```
1
16
```

the correct output is:

```
1
16
```

A careless solution might output `2 8`, because `lcm(2, 8) = 8`, which is not enough. The full prime power `2^4` must appear somewhere.

Another case is:

```
1
12
```

The correct construction is:

```
2
4 3
```

Using `2 2 3` would also make the least common multiple equal to `12`, but the total number of teeth is larger: `7` instead of `7` in this specific case it ties, while for other values repeated factors can be worse. The optimal construction must avoid unnecessary duplication and keep exactly the needed prime powers.

A final boundary case is a prime number:

```
1
97
```

The only useful construction is:

```
1
97
```

Splitting a prime into smaller gears is impossible because no smaller factors can create the prime in an LCM.

## Approaches

A direct brute-force idea would be to try different collections of gears and check whether their least common multiple is `k`. This is correct because a valid construction is exactly a collection whose LCM matches the required return time. The issue is the number of possible collections. Even restricting ourselves to divisors of `k`, the number of combinations grows exponentially with the number of factors, so this approach becomes unusable.

The key observation is that every integer can be written as a product of prime powers. Suppose:

`k = p1^a1 * p2^a2 * ... * pm^am`

For the LCM of the gears to contain `pi^ai`, at least one gear must contain that exact highest power of `pi`. If every gear contains a smaller power of `pi`, the LCM will miss that factor. On the other hand, adding a gear that contains multiple prime powers can only increase the total sum compared with keeping those prime powers separate.

For example, instead of using a single gear `12`, using gears `4` and `3` gives the same LCM with a smaller or equal sum. The cheapest construction is therefore to create one gear for every prime power in the factorization of `k`.

The brute-force approach fails because it ignores the independent contribution of prime powers. Once we recognize that each prime power can be handled separately, the problem becomes simple factorization.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in number of factors | Depends on search depth | Too slow |
| Optimal | O(sqrt(k)) per test case | O(number of prime factors) | Accepted |

## Algorithm Walkthrough

1. Factor `k` into prime powers. Start with the smallest possible divisor and repeatedly remove factors. Whenever a prime factor is found, keep multiplying it until the whole power of that prime has been extracted.

The reason we keep the complete power is that the LCM needs the maximum exponent of every prime, not just the prime itself.

1. Store each extracted prime power as one gear size.

For example, `72 = 2^3 * 3^2`, so the extracted values are `8` and `9`.

1. If the remaining value after trial division is greater than one, it is a prime factor larger than the square root of the original number. Add it as its own gear.
2. Output the number of extracted prime powers and the list of gear sizes.

Why it works:

Every prime power in the factorization of `k` appears in at least one chosen gear, so the LCM of all chosen gears contains every factor required by `k`. Since every chosen gear divides `k`, the LCM cannot contain anything extra, so it is exactly `k`.

For optimality, consider any valid construction. For every prime `p` in `k`, some gear must contain the full required power of `p`, otherwise the LCM would be missing that power. The cheapest way to satisfy each requirement is to use exactly those prime powers as separate gears. Combining two required prime powers into one gear replaces their sum with their product, and for integers greater than one the product is never smaller than the sum in this setting. Thus the separate prime-power construction minimizes the total number of teeth.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve_case(k):
    ans = []
    x = k
    d = 2
    while d * d <= x:
        if x % d == 0:
            power = 1
            while x % d == 0:
                x //= d
                power *= d
            ans.append(power)
        d += 1 if d == 2 else 2

    if x > 1:
        ans.append(x)

    return ans

def main():
    t = int(input())
    out = []
    for _ in range(t):
        k = int(input())
        ans = solve_case(k)
        out.append(str(len(ans)))
        out.append(" ".join(map(str, ans)))
    print("\n".join(out))

if __name__ == "__main__":
    main()
```

The factorization loop tries divisors until the square of the divisor exceeds the remaining value. Once that happens, any remaining value must be prime, because a composite number would have a factor not larger than its square root.

When a divisor is found, the inner loop removes all copies of that prime. The variable `power` accumulates the full prime power, such as turning repeated factors of `2` into `8` for `72`.

The increment skips even candidates after checking `2`, which avoids unnecessary work. Since `k` is only `100000`, simple trial division is already fast enough.

The output always contains at least one gear because `k` is at least `2`. A prime input leaves the prime in `x`, and that final value is handled by the remaining-factor check.

## Worked Examples

For the input:

```
1
72
```

the execution is:

| Step | Remaining value | Divisor | Extracted gear | Gears |
| --- | --- | --- | --- | --- |
| Start | 72 | 2 | 8 | 8 |
| After removing 2 | 9 | 3 | 9 | 8, 9 |
| After removing 3 | 1 | none | none | 8, 9 |

The output is:

```
2
8 9
```

The trace shows that the algorithm preserves the highest power of every prime, giving `lcm(8,9)=72`.

For the input:

```
1
210
```

the execution is:

| Step | Remaining value | Divisor | Extracted gear | Gears |
| --- | --- | --- | --- | --- |
| Start | 210 | 2 | 2 | 2 |
| After removing 2 | 105 | 3 | 3 | 2, 3 |
| After removing 3 | 35 | 5 | 5 | 2, 3, 5 |
| After removing 5 | 7 | 7 | 7 | 2, 3, 5, 7 |

The output is:

```
4
2 3 5 7
```

This demonstrates the case where every factor is distinct and no prime powers larger than one are needed.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(sqrt(k)) per test case | Trial division only checks possible factors up to the square root of the remaining value |
| Space | O(number of prime factors) | Only the resulting gear sizes are stored |

With `k <= 100000`, the square root is at most about `317`, so even thousands of test cases fit comfortably within the limits.

## Test Cases

```python
import sys
import io

def solve_case(k):
    ans = []
    x = k
    d = 2
    while d * d <= x:
        if x % d == 0:
            power = 1
            while x % d == 0:
                x //= d
                power *= d
            ans.append(power)
        d += 1 if d == 2 else 2
    if x > 1:
        ans.append(x)
    return ans

def run(inp: str) -> str:
    data = list(map(int, inp.split()))
    t = data[0]
    res = []
    idx = 1
    for _ in range(t):
        ans = solve_case(data[idx])
        idx += 1
        res.append(str(len(ans)))
        res.append(" ".join(map(str, ans)))
    return "\n".join(res)

assert run("""4
2
12
72
210
""") == """1
2
2
4 3
2
8 9
4
2 3 5 7""", "samples"

assert run("""1
97
""") == """1
97""", "prime input"

assert run("""1
16
""") == """1
16""", "single prime power"

assert run("""1
100000
""") == """2
32 3125""", "large composite with powers"

assert run("""1
36
""") == """2
4 9""", "multiple repeated factors"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2` | One gear of size `2` | Minimum value boundary |
| `97` | One gear of size `97` | Prime handling |
| `16` | One gear of size `16` | Full prime power extraction |
| `100000` | `32 3125` | Large factorization with repeated powers |
| `36` | `4 9` | Correct separation of different prime powers |

## Edge Cases

For `k = 16`, the algorithm extracts the factor `2` four times and combines it into one gear value:

```
16 = 2^4
```

The produced construction is:

```
1
16
```

The LCM is exactly `16`, while using smaller gears would fail unless their combined LCM contains the full fourth power of two.

For `k = 12`, the factorization is:

```
12 = 2^2 * 3
```

The algorithm outputs:

```
2
4 3
```

The LCM is `12`. A construction containing only `2` and `3` would produce `6`, so keeping the full power `4` is necessary.

For `k = 97`, the remaining value after trial division is still `97`, so it is added directly:

```
1
97
```

A prime cannot be assembled from smaller divisors, so the single gear is the only possible optimal construction.
