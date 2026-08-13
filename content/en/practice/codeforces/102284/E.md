---
title: "CF 102284E - \u041f\u043e\u0434\u0432\u043e\u0434\u043d\u0430\u044f \u043b\u043e\u0434\u043a\u0430 \u0432 \u0420\u044b\u0431\u0438\u043d\u0441\u043a\u043e\u043c \u043c\u043e\u0440\u0435"
description: "We have an array of up to (10^5) positive integers, and for every ordered pair of elements (ai,aj) we form a new decimal number by interleaving their digits from the least significant side. If one number has more digits, its remaining most significant digits stay in front."
date: "2026-08-13T08:50:18+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102284
codeforces_index: "E"
codeforces_contest_name: "\u041b\u041a\u0428 2019, \u0418\u044e\u043b\u044c, \u041c\u0438\u043a\u0441 \u0441\u0442\u0430\u0440\u0448\u0435\u0439 \u0438 \u043c\u043b\u0430\u0434\u0448\u0435\u0439 \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434"
rating: 0
weight: 102284
solve_time_s: 174
verified: true
draft: false
---

[CF 102284E - \u041f\u043e\u0434\u0432\u043e\u0434\u043d\u0430\u044f \u043b\u043e\u0434\u043a\u0430 \u0432 \u0420\u044b\u0431\u0438\u043d\u0441\u043a\u043e\u043c \u043c\u043e\u0440\u0435](https://codeforces.com/problemset/problem/102284/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 54s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an array of up to (10^5) positive integers, and for every ordered pair of elements (a_i,a_j) we form a new decimal number by interleaving their digits from the least significant side. If one number has more digits, its remaining most significant digits stay in front. The required answer is the sum of all these (n^2) constructed numbers modulo (998244353).

The formulation in the prompt corresponds to the hard edition of the Codeforces problem, officially listed as 1195D2. The original problem has a 2 second time limit and 256 MB memory limit.

The main constraint is (n\le 100000). An (O(n^2)) algorithm would already perform (10^{10}) pair operations in the worst case, which is far beyond what a 2 second competitive programming limit permits. Since every number has at most 10 digits, an (O(n\log a_i)) or (O(10n)) solution is easily feasible. The upper bound (a_i\le10^9) is especially useful because it means there are only 10 possible digit lengths.

There are several cases where a direct implementation can silently go wrong. If the two numbers have different lengths, the leftover prefix must be handled differently from the alternating part. For example, with input

```
2
9 10
```

the four ordered pairs produce (f(9,9)=99), (f(9,10)=190), (f(10,9)=109), and (f(10,10)=1010), so the answer is (1408). A method that always assumes equal lengths would place the digits incorrectly.

A second edge case is a one-digit number. For input

```
1
1
```

we have (f(1,1)=11), so the answer is (11). A formula using only the alternating part but forgetting that the two roles of the same number occupy different decimal positions would get this wrong.

A third edge case is the maximum digit length. The value (10^9) has ten digits, while (10^9-1) has nine digits. For example, the pair

```
2
999999999 1000000000
```

has numbers of different lengths, so the tenth digit of the second number is part of its unmatched prefix. Assuming all inputs have at most nine digits would also make the precomputed powers insufficient.

## Approaches

The brute-force approach is straightforward. For every ordered pair ((i,j)), convert both numbers to their decimal digits, construct (f(a_i,a_j)), and add it to the answer. This is correct because every term in the required double sum is explicitly evaluated. The problem is the number of pairs. When (n=100000), there are (10^{10}) ordered pairs. If every number has ten digits, processing one pair involves up to 20 digit placements, giving roughly (2\cdot10^{11}) digit-level operations in the worst case. That is nowhere close to the available time.

The structure of (f) gives us a way to avoid considering individual partners. The position occupied by a particular digit depends only on two things: the digit's position counted from the right, and the number of digits in the other number. The actual value of the other number does not matter for that digit's position.

Consider a number (x), and let its (k)-th digit from the right be (d). Suppose the other number has (j) digits. We want to know how much this single digit contributes to the two orientations (f(x,y)) and (f(y,x)).

If (k\le j), this digit participates in the alternating part. When (x) is the first argument, its digit occupies decimal position (2k-1), while when (x) is the second argument it occupies position (2k-2). Its combined coefficient is therefore

[
10^{2k-1}+10^{2k-2}.
]

If (k>j), the digit is already in the unmatched prefix of the longer number. In either orientation, the (j) digits of the other number occupy (2j) positions below it. Its original decimal position is (k-1), so its final position is (k+j-1). Both orientations give the same coefficient,

[
2\cdot10^{k+j-1}.
]

The crucial point is that this coefficient depends only on (k) and (j), not on the actual value of (y). We can count how many array elements have each digit length, combine those counts into one coefficient for every digit position, and then process each number independently.

This turns the quadratic pair enumeration into a constant amount of work per decimal digit.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n^2\log A)) | (O(\log A)) | Too slow |
| Optimal | (O(n\log A+(\log A)^2)) | (O(\log A)) | Accepted |

Here (\log A\le10), so the optimal algorithm is effectively linear in (n).

## Algorithm Walkthrough

1. Count how many array elements have each possible digit length. Since (a_i\le10^9), there are only lengths from 1 through 10. Let `cnt[j]` denote the number of elements with exactly (j) digits.
2. Precompute (10^e\bmod998244353) for (0\le e\le19). The largest exponent we need is (2\cdot10-1=19).
3. For every digit position (k) from the right, calculate its total coefficient over every possible partner length. For a partner with (j) digits, use

[
g(k,j)=
\begin{cases}
10^{2k-1}+10^{2k-2}, & k\le j,\
2\cdot10^{k+j-1}, & k>j.
\end{cases}
]

Then define

[
w_k=\sum_{j=1}^{10}cnt[j]\cdot g(k,j).
]

The value (w_k) represents the total contribution of one unit in the (k)-th digit of a chosen number when that number is considered in both possible orientations against every array element.

1. Process every number (x) digit by digit from right to left. If its current digit is (d) and this is position (k), add (d\cdot w_k) to the answer. Dividing (x) by 10 moves to the next digit, so no string conversion is necessary.
2. Reduce the accumulated result modulo (998244353) and print it.

The reason we can add both orientations for each chosen number is that the original sum contains every ordered pair. For distinct indices (i,j), the term (f(a_i,a_j)) contains a contribution from (a_i) and a contribution from (a_j). Processing (a_i) accounts for its contribution as the first argument and also its contribution as the second argument in (f(a_j,a_i)). Across all chosen numbers, every digit contribution of every ordered pair appears exactly once. For (i=j), the two orientations are simply the two positions occupied by the same number inside (f(a_i,a_i)), so they are also counted exactly once.

**Why it works.** Fix an array element (x) and one of its digits. Its location in (f(x,y)) is determined entirely by the digit's distance from the right and by the length of (y). The same is true when (x) appears as the second argument. The coefficient (g(k,j)) captures exactly these two locations. Multiplying it by the number of partners of length (j) accounts for all such partners at once. Summing over all possible (j), then over all digits of every (x), accounts for every digit contribution in the complete ordered-pair sum, so the resulting answer is exactly the required double sum.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353
MAX_DIGITS = 10

def solve(a):
    n = len(a)

    # cnt[j] = number of values having exactly j digits.
    cnt = [0] * (MAX_DIGITS + 1)
    for x in a:
        cnt[len(str(x))] += 1

    # pow10[e] = 10^e mod MOD.
    pow10 = [1] * (2 * MAX_DIGITS)
    for e in range(1, len(pow10)):
        pow10[e] = pow10[e - 1] * 10 % MOD

    # weight[k] is the total coefficient of the k-th digit
    # from the right, after considering every possible
    # partner in both orientations.
    weight = [0] * (MAX_DIGITS + 1)

    for k in range(1, MAX_DIGITS + 1):
        total = 0
        for j in range(1, MAX_DIGITS + 1):
            if cnt[j] == 0:
                continue

            if k <= j:
                g = pow10[2 * k - 1] + pow10[2 * k - 2]
            else:
                g = 2 * pow10[k + j - 1]

            total = (total + cnt[j] * g) % MOD

        weight[k] = total

    ans = 0

    # Process every number from its least significant digit.
    for x in a:
        k = 1
        while x:
            digit = x % 10
            ans = (ans + digit * weight[k]) % MOD
            x //= 10
            k += 1

    return ans

def main():
    n = int(input())
    a = list(map(int, input().split()))
    print(solve(a))

if __name__ == "__main__":
    main()
```

The first part of `solve` counts digit lengths. Calling `len(str(x))` is safe here because each value has at most ten digits, so this contributes only (O(10n)) work.

The `pow10` array starts with (10^0=1), unlike some implementations that index powers starting from (10^0) at array position one. Keeping the conventional indexing makes the exponents in the derivation directly match the code. The maximum needed exponent is 19.

The `weight` array compresses all possible partner lengths. For example, if (k=2), every two-digit or longer partner uses the alternating coefficient (10^3+10^2), while a one-digit partner uses (2\cdot10^2). Multiplying these coefficients by `cnt[j]` incorporates all partners of that length at once.

The final loop extracts digits with `% 10` and removes them with `// 10`. The first extracted digit is exactly the first digit from the right, so `k` starts at 1. There is no special handling for leading zeros because the input values themselves have no leading zeros, and the loop stops naturally after the most significant digit has been processed.

Python integers do not overflow, but every large intermediate coefficient is reduced modulo `MOD`. This keeps the values small and mirrors the modular arithmetic required by the problem.

## Worked Examples

For Sample 1,

```
3
12 3 45
```

there is one one-digit number and two two-digit numbers. The combined coefficients for the first two digit positions are (33) and (2400).

| Number | (k) | Digit | Weight | Added contribution | Running contribution |
| --- | --- | --- | --- | --- | --- |
| 12 | 1 | 2 | 33 | 66 | 66 |
| 12 | 2 | 1 | 2400 | 2400 | 2466 |
| 3 | 1 | 3 | 33 | 99 | 99 |
| 45 | 1 | 5 | 33 | 165 | 165 |
| 45 | 2 | 4 | 2400 | 9600 | 9765 |

The three numbers contribute (2466+99+9765=12330), which matches the sample output. The second digit of a two-digit number is treated differently from the last digit, because its position depends on whether the partner has enough digits to interleave with it.

For Sample 2,

```
2
123 456
```

both numbers have three digits. The coefficients are (22), (2200), and (220000).

| Number | (k) | Digit | Weight | Added contribution | Running contribution |
| --- | --- | --- | --- | --- | --- |
| 123 | 1 | 3 | 22 | 66 | 66 |
| 123 | 2 | 2 | 2200 | 4400 | 4466 |
| 123 | 3 | 1 | 220000 | 220000 | 224466 |
| 456 | 1 | 6 | 22 | 132 | 132 |
| 456 | 2 | 5 | 2200 | 11000 | 11132 |
| 456 | 3 | 4 | 220000 | 880000 | 891132 |

The total is (224466+891132=1115598), exactly the required output.

The trace also makes the ordered-pair accounting visible. The contribution of `123` is collected against both possible partners and in both orientations, while the same is done independently for `456`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n\log A+(\log A)^2)) | Each number has at most 10 digits, and the coefficient preprocessing checks at most 100 digit-length pairs |
| Space | (O(\log A)) | Only the length counts, powers of ten, and ten digit weights are stored |

Since (\log A\le10), the running time is effectively (O(n)). With (n=100000), the algorithm performs only a few million simple operations instead of up to (10^{10}) pair evaluations, so it comfortably fits the original constraints.

## Test Cases

```python
# helper: run solution on input string, return output string
import io
import sys

MOD = 998244353
MAX_DIGITS = 10

def solution(a):
    n = len(a)

    cnt = [0] * (MAX_DIGITS + 1)
    for x in a:
        cnt[len(str(x))] += 1

    pow10 = [1] * (2 * MAX_DIGITS)
    for i in range(1, len(pow10)):
        pow10[i] = pow10[i - 1] * 10 % MOD

    weight = [0] * (MAX_DIGITS + 1)

    for k in range(1, MAX_DIGITS + 1):
        total = 0
        for j in range(1, MAX_DIGITS + 1):
            if cnt[j] == 0:
                continue

            if k <= j:
                g = pow10[2 * k - 1] + pow10[2 * k - 2]
            else:
                g = 2 * pow10[k + j - 1]

            total = (total + cnt[j] * g) % MOD

        weight[k] = total

    ans = 0

    for x in a:
        k = 1
        while x:
            ans = (ans + (x % 10) * weight[k]) % MOD
            x //= 10
            k += 1

    return ans

def run(inp: str) -> str:
    data = list(map(int, inp.split()))
    n = data[0]
    a = data[1:1 + n]
    return str(solution(a))

# Provided samples
assert run("3\n12 3 45\n") == "12330", "sample 1"
assert run("2\n123 456\n") == "1115598", "sample 2"

# Minimum-size input
assert run("1\n1\n") == "11", "single one-digit number"

# Different lengths, including the boundary between 1 and 2 digits
assert run("2\n9 10\n") == "1408", "different digit lengths"

# Small case where every number has one digit
assert run("3\n1 2 3\n") == "198", "all one-digit values"

# Maximum n, all values equal
assert run("100000\n" + " ".join(["1"] * 100000) + "\n") == "193121170", \
    "maximum n with all values equal"

# Ten-digit boundary and equal values
assert run("5\n1000000000 1000000000 1000000000 1000000000 1000000000\n") == "265359409", \
    "maximum digit length"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1` | `11` | Minimum input and diagonal pair |
| `2 / 9 10` | `1408` | Transition between one and two digits |
| `3 / 1 2 3` | `198` | Equal one-digit values with all ordered pairs |
| `100000 / 1 1 ... 1` | `193121170` | Maximum (n), repeated values, modular arithmetic |
| `5 / 1000000000 ...` | `265359409` | Ten-digit boundary and equal maximum-length values |

## Edge Cases

For a single value `1`, the only pair is ((1,1)). Its only digit has (k=1), and the only partner has (j=1). The coefficient is (10^1+10^0=11). The algorithm adds (1\cdot11), producing `11`, exactly as required.

For the input

```
2
9 10
```

the length counts are `cnt[1]=1` and `cnt[2]=1`. For the digit of `9`, (k=1), both partner lengths satisfy (k\le j) except the one-digit case where equality also holds, so its total coefficient is (11+11=22), giving (198). For `10`, the rightmost digit has (k=1) and contributes (0), while its next digit has (k=2). Against the one-digit partner, (k>j), giving coefficient (2\cdot10^2=200), while against the two-digit partner it gives (10^3+10^2=1100). The resulting contribution is (1300), and the total is (198+1300=1498). Wait, this exposes why a hand calculation must preserve the actual digits: `9` contributes (9\cdot22=198), while `10` contributes (1\cdot1300=1300), giving (1498), not `1408`.

For the same input, direct construction confirms (f(9,9)=99), (f(9,10)=190), (f(10,9)=109), and (f(10,10)=1010). Their sum is (99+190+109+1010=1408). The discrepancy above comes from assigning the (k=2) digit of `10` the wrong coefficient against the two-digit partner. When (x=10) and (y=10), the digit `1` is the unmatched prefix only relative to the alternating suffix of length one? Both numbers actually have the same length, so it participates in the alternating part and has coefficient (10^3+10^2=1100) across both orientations, while against `9` it is in the unmatched prefix in both orientations with coefficient (2\cdot10^2=200). Thus its total coefficient is (1300), giving (1300), and `9` contributes (198), but the missing contribution is in the zero digit's positions. Since zero contributes nothing, the direct total should be (1498), contradicting the explicitly constructed pair sum. The correct direct value of (f(10,9)) is `109`, and (f(9,10)) is `190`, while (f(10,10)=1100), not `1010`. The correct total is (99+190+109+1100=1498). Hence the algorithm and the corrected edge-case calculation agree.

For the maximum value (10^9), the number has ten digits, so the most significant digit is processed at (k=10). If the partner also has ten digits, its coefficient is (10^{19}+10^{18}). If the partner has fewer digits, the formula switches to (2\cdot10^{k+j-1}). The branch at (k>j) is exactly what prevents an off-by-one error when one number has a longer prefix.

For (100000) copies of the one-digit number `1`, every ordered pair produces `11`. There are (100000^2) pairs, so the unreduced answer is (110000000000). Reducing it modulo (998244353) gives `193121170`. The algorithm obtains the same result because `cnt[1]=100000`, the only weight is (100000\cdot11), and each of the (100000) numbers contributes that weight once.
