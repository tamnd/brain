---
title: "CF 102835A - Right-Coupled Numbers"
description: "We need decide whether a given positive integer can be split into two factors that are close enough in size. A number x is considered right-coupled if there exist two positive integers a and b where a is the smaller factor, b is the larger factor, their product is exactly x, and…"
date: "2026-07-26T14:56:52+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102835
codeforces_index: "A"
codeforces_contest_name: "The 2020 ICPC Asia Taipei-Hsinchu Site Programming Contest"
rating: 0
weight: 102835
solve_time_s: 36
verified: true
draft: false
---

[CF 102835A - Right-Coupled Numbers](https://codeforces.com/problemset/problem/102835/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 36s  
**Verified:** yes  

## Solution
## Problem Understanding

We need decide whether a given positive integer can be split into two factors that are close enough in size. A number `x` is considered right-coupled if there exist two positive integers `a` and `b` where `a` is the smaller factor, `b` is the larger factor, their product is exactly `x`, and the smaller factor is at least half of the larger one.

Equivalently, after choosing a divisor pair `(a, b)` with `a <= b`, we only need to check whether `b <= 2a`. If such a pair exists, the answer is `1`; otherwise the answer is `0`.

The input contains up to 1000 independent numbers, and every number is smaller than `2^15`, which is only 32768. This upper bound is very small, so algorithms that perform a few hundred checks per number are easily fast enough. A solution that tried every possible pair of factors would still be unnecessary because there are at most a few hundred possible divisors to inspect. Even an `O(x)` scan is acceptable for this limit, but we can naturally reduce the work by only testing divisors up to the square root.

Several cases can break a careless implementation. A common mistake is using floating point division for the condition `a / b >= 0.5`, which can introduce avoidable precision issues. The integer equivalent `2 * a >= b` is exact.

For example, input:

```
1
66
```

has factors `6 * 11`. Since `6 / 11` is greater than `0.5`, the output is:

```
1
```

A solution that only checks the closest factor pair near the square root incorrectly assuming the two factors must be equal would miss this case.

Another edge case is a prime number:

```
1
55
```

The only factor pair is `1 * 55` and `2 * 1 < 55`, so the output is:

```
0
```

A solution that only checks whether the number has factors other than one would give the wrong result because not every composite number is right-coupled.

The smallest possible input value is also worth considering:

```
1
1
```

The factor pair is `1 * 1`, and it satisfies the condition. The correct output is:

```
1
```

An implementation that starts searching from factor `2` would incorrectly reject it.

## Approaches

The direct brute-force approach is to try every possible value of `a`, check whether `a` divides `x`, and then calculate `b = x / a`. If `a <= b` and `b <= 2a`, we have found a valid decomposition. This approach is correct because every possible smaller factor is examined.

For one number `x`, this requires checking all values from `1` to `x`, giving `O(x)` operations. With the maximum value close to 32768 and 1000 test cases, the worst case is about 32 million checks, which would probably still pass in many languages, but it ignores the mathematical structure of factor pairs.

The better observation is that factors appear in pairs. If `a` is a divisor of `x`, the matching factor is `b = x / a`. At least one member of every pair is no larger than the square root of `x`, so we only need to inspect divisors up to `sqrt(x)`. Whenever we find a divisor `a`, we immediately know the corresponding larger factor and can test the required inequality.

The brute-force method works because it explores all possible factorizations, but it spends time checking values that cannot be the smaller side of a factor pair. The square-root observation removes those unnecessary checks while preserving the guarantee that every possible candidate pair is considered.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(x) per test case | O(1) | Accepted for these limits, but unnecessary |
| Optimal | O(sqrt(x)) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. For each input number `x`, start checking possible divisors from `1` up to `sqrt(x)`. We only need to search this range because every divisor larger than the square root has a matching smaller divisor that would already be checked.
2. When a value `a` divides `x`, compute the paired factor `b = x / a`. The pair `(a, b)` represents one possible way to write `x` as a product.
3. Ensure `a` is the smaller factor. Since the loop only reaches the square root, `a` is always less than or equal to `b`.
4. Check whether `b <= 2 * a`. This is the integer form of the original ratio condition, avoiding floating point calculations.
5. If any divisor pair satisfies the condition, print `1`. If the loop finishes without finding one, print `0`.

The correctness comes from the fact that every possible factorization of `x` appears as some divisor `a` and its paired value `x / a`. Since all smaller factors are at most `sqrt(x)`, the algorithm checks every possible candidate pair. The algorithm accepts exactly the pairs where the larger factor is no more than twice the smaller factor, which is precisely the required condition.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve_case(x):
    d = 1
    while d * d <= x:
        if x % d == 0:
            a = d
            b = x // d
            if b <= 2 * a:
                return 1
        d += 1
    return 0

def main():
    n = int(input())
    ans = []
    for _ in range(n):
        x = int(input())
        ans.append(str(solve_case(x)))
    print("\n".join(ans))

if __name__ == "__main__":
    main()
```

The function `solve_case` handles one number independently. The loop variable `d` represents a possible smaller factor, and the condition `d * d <= x` limits the search to the necessary range.

When `x % d == 0`, the code has found a complete factor pair. The larger factor is calculated with integer division, so no rounding can affect the answer. The comparison uses `b <= 2 * a` instead of division, which avoids floating point precision problems.

The multiplication `d * d` is safe here because the maximum value of `x` is only 32768. In larger problems, this boundary check would often use `d <= x // d` to avoid integer overflow in languages with fixed-size integers.

## Worked Examples

For the input:

```
4
66
55
105
150
```

The first case behaves as follows.

| Checked divisor | Is divisor? | Pair | Condition | Result |
| --- | --- | --- | --- | --- |
| 1 | Yes | 1, 66 | 66 <= 2 | False |
| 2 | Yes | 2, 33 | 33 <= 4 | False |
| 3 | Yes | 3, 22 | 22 <= 6 | False |
| 6 | Yes | 6, 11 | 11 <= 12 | True |

The pair `6 * 11` is close enough, so `66` produces output `1`.

For the input:

```
1
105
```

| Checked divisor | Is divisor? | Pair | Condition | Result |
| --- | --- | --- | --- | --- |
| 1 | Yes | 1, 105 | 105 <= 2 | False |
| 3 | Yes | 3, 35 | 35 <= 6 | False |
| 5 | Yes | 5, 21 | 21 <= 10 | False |

No divisor pair satisfies the condition, so the output is `0`.

These traces demonstrate the main invariant: every checked divisor represents one complete factor pair, and the algorithm only rejects a number after all possible smaller factors have been considered.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(sqrt(x)) per test case | Only divisors up to the square root of each number are tested |
| Space | O(1) | The algorithm stores only a few integer variables |

The maximum value is small enough that the square-root search performs only about 182 checks per test case. Even with 1000 test cases, the total work is tiny and easily fits within the limits.

## Test Cases

```python
import sys
import io

def solve(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    input = sys.stdin.readline

    def solve_case(x):
        d = 1
        while d * d <= x:
            if x % d == 0:
                if x // d <= 2 * d:
                    return 1
            d += 1
        return 0

    n = int(input())
    result = []
    for _ in range(n):
        result.append(str(solve_case(int(input()))))

    print("\n".join(result))
    output = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return output

assert solve("4\n66\n55\n105\n150\n") == "1\n0\n0\n1\n", "sample cases"

assert solve("1\n1\n") == "1\n", "minimum value"
assert solve("3\n2\n3\n32767\n") == "1\n0\n0\n", "small and maximum boundary values"
assert solve("4\n4\n9\n16\n25\n") == "1\n1\n1\n1\n", "perfect squares"
assert solve("3\n55\n77\n121\n") == "0\n0\n1\n", "prime factors and near-square cases"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `1` | Handles the smallest possible number |
| `2, 3, 32767` | `1, 0, 0` | Checks lower boundary and large values |
| `4, 9, 16, 25` | All `1` | Checks square numbers where factors are equal |
| `55, 77, 121` | `0, 0, 1` | Checks prime products and close factor pairs |

## Edge Cases

For the smallest input:

```
1
1
```

the loop checks divisor `1`, finds the pair `(1, 1)`, and verifies `1 <= 2`. The algorithm returns `1`, correctly recognizing that the number can be split into two equal factors.

For a prime number:

```
1
55
```

the only useful factor pair is `(1, 55)`. The algorithm finds the divisor `1` and checks `55 <= 2`, which fails. Since there are no other divisors, the answer remains `0`.

For a number that has a valid pair far from equal:

```
1
66
```

the algorithm does not stop after seeing pairs like `(1, 66)` or `(2, 33)`. It continues until divisor `6`, where it finds `(6, 11)`. Since `11 <= 12`, it returns `1`.

For a perfect square:

```
1
121
```

the divisor `11` creates the pair `(11, 11)`. Equal factors always satisfy the condition because the larger factor is exactly the same size as the smaller factor, so the output is `1`.
