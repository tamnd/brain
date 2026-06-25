---
title: "CF 106157I - Itsy Bits"
description: "The task is to choose the size of a storage unit for a single unsigned integer. The system knows the largest value that will ever be stored, and it wants to reserve a number of bits that follows the hardware rule: the number of bits itself must be a power of two."
date: "2026-06-25T11:19:30+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106157
codeforces_index: "I"
codeforces_contest_name: "2025 United Kingdom and Ireland Programming Contest (UKIEPC 2025)"
rating: 0
weight: 106157
solve_time_s: 25
verified: true
draft: false
---

[CF 106157I - Itsy Bits](https://codeforces.com/problemset/problem/106157/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 25s  
**Verified:** yes  

## Solution
## Problem Understanding

The task is to choose the size of a storage unit for a single unsigned integer. The system knows the largest value that will ever be stored, and it wants to reserve a number of bits that follows the hardware rule: the number of bits itself must be a power of two. Valid storage sizes are therefore 1, 2, 4, 8, 16, 32, 64, and so on.

The input is one integer representing the maximum value that must fit in memory. The output is the smallest valid bit size that can store that value, followed by the correct singular or plural wording.

A storage unit with `b` bits can represent values from `0` to `2^b - 1`. Because the input can be as large as `10^18`, the answer must be found without iterating through all possible values up to the input. Any approach with work proportional to `n` would require around one quintillion operations in the worst case, which is far beyond what a normal contest time limit allows. We only need to inspect the small set of possible bit sizes.

The edge cases come from the boundary between two storage sizes. For example, input `1` must produce `1 bit`, because one bit can store values `0` and `1`. A solution that starts checking from two bits would incorrectly output `2 bits`.

Another boundary case is a value exactly equal to a storage capacity minus one. For input `255`, the correct output is `8 bits`, because eight bits store values from `0` through `255`. A careless solution that checks whether `n < 255` instead of `n <= 255` would incorrectly move to `16 bits`.

The other important case is when the value exceeds a power-of-two boundary by only one. For input `256`, eight bits are no longer enough because their maximum value is `255`. The answer becomes `16 bits`.

## Approaches

A direct approach would try every possible number of bits, starting from one, and test whether that many bits can store the given value. The check for a candidate size `b` is simply whether `2^b - 1` is at least the required maximum value. This method is correct because it examines sizes in increasing order and stops at the first valid one.

The problem with this approach depends on how the candidates are generated. If we imagine checking every possible bit count from `1` up to the input value, the worst case input near `10^18` would require about `10^18` checks, which is impossible. The useful observation is that only powers of two are allowed as answers. There are only a handful of such values before exceeding the largest possible input. We can repeatedly double the current answer until the capacity is large enough.

The brute-force idea works because the answer is the first valid size. The observation that valid sizes form a tiny geometric sequence lets us skip all invalid sizes between them.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(1) | Too slow |
| Optimal | O(log n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Start with a storage size of `1` bit. This is the smallest possible allocation and must be considered because very small numbers can fit there.
2. Check whether this number of bits can store the required maximum value. A size of `bits` works when `2^bits - 1` is at least the input value.
3. If the current size is too small, double it. This moves to the next valid storage size because all allowed sizes are powers of two.
4. Continue until the capacity is large enough. The first size that works is the required answer.
5. Print the size with the correct suffix. The only singular case is `1`, where the output should contain `bit`; every other size uses `bits`.

Why it works: the algorithm only considers valid storage sizes, and it checks them in increasing order. Since the answer is defined as the smallest valid size, the first size whose capacity reaches the required value must be the optimal choice. No skipped value could be a better answer because all skipped values are not allowed storage sizes.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())

    bits = 1
    while (1 << bits) - 1 < n:
        bits *= 2

    if bits == 1:
        print("1 bit")
    else:
        print(f"{bits} bits")

if __name__ == "__main__":
    solve()
```

The variable `bits` stores the current number of bits allocated. It starts at `1` because one-bit storage is a valid possibility.

The loop condition checks the largest value representable by the current storage size. The expression `(1 << bits) - 1` is exactly `2^bits - 1`, which avoids floating-point calculations and keeps all operations as integer arithmetic.

Multiplying `bits` by two is the key step. The answer is not allowed to be an arbitrary number like `5` or `12`, so increasing by one would waste time checking invalid candidates. Doubling jumps directly between valid storage sizes.

The final condition handles the only grammatical exception. The storage size `1` uses the singular word, while all larger sizes use the plural form.

## Worked Examples

For the input:

```
1
```

| Step | bits | Capacity |
| --- | --- | --- |
| Start | 1 | 1 |

The capacity of one bit is enough because it can represent values from `0` to `1`. The algorithm stops immediately and prints `1 bit`. This demonstrates the smallest possible case.

For the input:

```
1100586419201
```

| Step | bits | Capacity |
| --- | --- | --- |
| Start | 1 | 1 |
| Double | 2 | 3 |
| Double | 4 | 15 |
| Double | 8 | 255 |
| Double | 16 | 65535 |
| Double | 32 | 4294967295 |
| Double | 64 | 18446744073709551615 |

The first several storage sizes are too small. A 64-bit storage unit is the first allowed size whose capacity reaches the input, so the output is `64 bits`. This trace shows why the answer cannot simply be the next integer number of bits.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log n) | The number of doublings is proportional to the number of bits needed to represent the input. |
| Space | O(1) | Only the current candidate size is stored. |

The input limit of `10^18` only requires checking a small number of powers of two. The algorithm performs far fewer operations than a linear scan and easily fits within the contest limits.

## Test Cases

```python
import sys
import io

def solve_case(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n = int(input())
    bits = 1
    while (1 << bits) - 1 < n:
        bits *= 2

    return f"{bits} {'bit' if bits == 1 else 'bits'}"

# provided samples
assert solve_case("1\n") == "1 bit", "sample 1"
assert solve_case("37\n") == "8 bits", "sample 2"
assert solve_case("1100586419201\n") == "64 bits", "sample 3"

# custom cases
assert solve_case("0\n") == "1 bit", "zero still fits in one bit"
assert solve_case("255\n") == "8 bits", "maximum value of 8 bits"
assert solve_case("256\n") == "16 bits", "just above 8 bit capacity"
assert solve_case("18446744073709551615\n") == "64 bits", "largest 64 bit value"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0` | `1 bit` | Minimum storage size and lower boundary |
| `255` | `8 bits` | Exact maximum capacity of a valid size |
| `256` | `16 bits` | Transition to the next power-of-two size |
| `18446744073709551615` | `64 bits` | Large-value handling |

## Edge Cases

For input:

```
1
```

The algorithm starts with `bits = 1`. The capacity calculation gives `2^1 - 1 = 1`, which is enough, so the loop is skipped. The output is `1 bit`, handling the singular form correctly.

For input:

```
255
```

The algorithm tests `8` bits and finds that `2^8 - 1 = 255`. Since the comparison is inclusive, the value fits exactly and the answer remains `8 bits`.

For input:

```
256
```

The algorithm finds that `8` bits provide capacity `255`, which is insufficient. It doubles the size to `16`, where the capacity is `65535`, and outputs `16 bits`.

For input:

```
1100586419201
```

The algorithm keeps doubling through the allowed storage sizes. Values from `1` through `32` bits cannot represent the input, while `64` bits can. Since every smaller valid size was rejected first, the result is guaranteed to be minimal.
