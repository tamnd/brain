---
title: "CF 102399H - \u0424\u043e\u043a\u0443\u0441 \u0441 \u0434\u0435\u043b\u0435\u043d\u0438\u0435\u043c \u0438 \u0443\u043c\u043d\u043e\u0436\u0435\u043d\u0438\u0435\u043c"
description: "We have (n) distinct positive integers (a1,ldots,an). A card contains some positive integer (x). Taking that card lets us perform exactly one operation on exactly one array element: multiply it by (x), or divide it by (x) when the division is exact."
date: "2026-08-11T15:56:29+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102399
codeforces_index: "H"
codeforces_contest_name: "2019 \u041c\u043e\u0441\u043a\u043e\u0432\u0441\u043a\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432, \u043b\u0438\u0433\u0430 A"
rating: 0
weight: 102399
solve_time_s: 248
verified: true
draft: false
---

[CF 102399H - \u0424\u043e\u043a\u0443\u0441 \u0441 \u0434\u0435\u043b\u0435\u043d\u0438\u0435\u043c \u0438 \u0443\u043c\u043d\u043e\u0436\u0435\u043d\u0438\u0435\u043c](https://codeforces.com/problemset/problem/102399/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 4m 8s  
**Verified:** yes  

## Solution
## Problem Understanding

We have (n) distinct positive integers (a_1,\ldots,a_n). A card contains some positive integer (x). Taking that card lets us perform exactly one operation on exactly one array element: multiply it by (x), or divide it by (x) when the division is exact. Afterward the card disappears, so the same value (x) cannot be used again.

The goal is to make all array elements equal while taking as few cards as possible. The input gives the number of elements and the distinct array values in increasing order. The output is the minimum number of cards that must be consumed.

The original contest statement has a 1 second time limit and 512 MB memory limit. With (n) up to (200,000), an (O(n^2)) solution would perform around (4\cdot10^{10}) pair checks in the worst case, which is far beyond what fits in a one-second contest limit. We need an essentially linear or near-linear algorithm.

There are several easy-to-miss details. First, cards are globally unique. If two elements both need the card (2), we cannot perform both operations with that card. For example,

```
5
2 3 6 12 18
```

has answer (5), not (4). Choosing the final value (6) looks promising because every element is comparable with (6): the required card values are (3,2,2,3). The repeated (2) and repeated (3) make that plan impossible. A careless solution that only checks divisibility and counts one operation per element would incorrectly return (4).

Second, a final value that is not present in the original array cannot give an (n-1) solution. With (n-1) operations, at least one element receives no operation because every operation affects only one element. That untouched element remains equal to its original value, so the common final value must be one of the original array elements. For example,

```
3
6 10 15
```

cannot be solved in two cards. The value (30) lets every element reach the target with one card, using cards (5,3,2), but (30) was not in the array, so all three elements must be changed. The correct answer is (3).

Third, (n=1) needs zero cards because the single element is already equal to itself. For example,

```
1
42
```

has answer (0). This is also the only meaningful way to test an "all elements equal" case, because the input guarantees that the array elements are distinct.

Finally, arithmetic involving (10^{18}) needs care in languages with fixed-width integers. Even an intermediate LCM can become much larger than (10^{18}), although Python integers themselves do not overflow. The implementation still caps the LCM because once it exceeds (10^{18}), it can never divide an array element.

## Approaches

A direct solution starts by observing that the final answer is surprisingly restricted.

Suppose we want to make every element equal using (k) cards. Every card changes only one element, so if (k<n-1), at least two array elements are never touched. They are distinct initially and remain distinct, so equality is impossible. Thus every solution needs at least (n-1) cards.

An (n)-card solution always exists. Let (g) be the GCD of all array elements. Divide every (a_i) by (a_i/g), sending every element to (g). The required card values are all distinct because the original (a_i) are distinct. Thus (n) cards are always enough.

The answer is consequently either (n-1) or (n).

Now consider when (n-1) cards are possible. Exactly one array element can be untouched. Let its value be (y). Since the final value is (y), every other element (a_i) must reach (y) in exactly one operation.

One operation can change (a_i) to (y) only in one of two situations. If (a_i<y), then (a_i) must divide (y), and the required card is (y/a_i). If (a_i>y), then (y) must divide (a_i), and the required card is (a_i/y).

The required card is completely determined by (a_i) and (y). Since cards cannot be reused, all these ratios must be different.

So an element (y=a_i) is a valid (n-1) target exactly when every other array element is comparable with (y) under divisibility, and all resulting ratios are distinct.

The remaining problem is finding all possible candidates without checking all (n) elements for every array position.

For a candidate (a_i), every smaller element must divide (a_i). Equivalently, the LCM of all elements before (i) must divide (a_i). We can maintain this prefix LCM while scanning the array. The LCM can be capped at (10^{18}+1), because every array element is at most (10^{18}), so a larger LCM can never divide a candidate.

Similarly, every larger element must be divisible by (a_i). Equivalently, (a_i) must divide the GCD of all elements after (i). A suffix GCD array gives this condition in constant time.

There cannot be many candidates. If (a_i) and (a_j), with (i<j), are both candidates, then the condition for (a_i) says that (a_i\mid a_j). Since the values are distinct, (a_j\ge 2a_i). Starting from a positive value and never exceeding (10^{18}), this can happen at most about 60 times. That allows us to inspect every candidate against the whole array.

For each candidate, we scan the array, compute the required card ratio for every other element, and insert the ratio into a set. If an element is not divisible by the candidate in either direction, the candidate fails. If a ratio appears twice, the candidate also fails because it would require the same card twice.

The brute-force method checks all (n) possible targets and scans all (n) elements for each one. Its worst case is (O(n^2)), about (4\cdot10^{10}) target-element checks for (n=200,000). The optimal method first filters candidates using prefix LCM and suffix GCD, and there are only (O(\log 10^{18})) of them.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n^2)) | (O(n)) | Too slow |
| Optimal | (O(n\log 10^{18})) | (O(n)) | Accepted |

## Algorithm Walkthrough

1. Read the sorted array and build a suffix GCD array. For every position (i), this array stores the GCD of all values strictly to the right of (i). For the last position, the suffix GCD is (0), which is convenient because every positive integer divides (0).
2. Scan the array from left to right while maintaining the LCM of all values strictly before the current position. If this LCM exceeds (10^{18}), replace it with a special value larger than (10^{18}). Such an LCM can never divide any candidate array element.
3. Mark (a_i) as a possible target only when the prefix LCM divides (a_i) and (a_i) divides the suffix GCD. The first condition says every smaller element can reach (a_i) with one operation. The second says every larger element can reach (a_i) with one operation.
4. For every possible target (y), scan all array elements other than (y). If (x<y), compute the required card as (y/x). If (x>y), compute it as (x/y). The candidate guarantees that these divisions are exact, so no additional divisibility test is necessary here.
5. Insert every required ratio into a set. If the same ratio appears twice, reject this target because the corresponding card exists only once on the table. If every ratio is distinct, the target gives a valid (n-1)-card construction, so immediately output (n-1).
6. If no candidate works, output (n). The GCD construction described earlier guarantees that (n) cards are always sufficient.

### Why it works

The lower bound (n-1) follows because fewer operations would leave at least two distinct original elements untouched. An (n-1)-operation solution must touch every element except one, so its final value must equal that untouched element. Every changed element must then be transformable to that target in exactly one operation, which is possible precisely when the two values are divisible one way or the other. The required card is their quotient, so all quotients must be distinct.

The prefix LCM condition is exactly equivalent to saying that every smaller array element divides the candidate. The suffix GCD condition is exactly equivalent to saying that the candidate divides every larger element. Once those conditions hold, the ratio scan checks the only remaining restriction, namely that no card value is required twice. Hence the algorithm finds an (n-1) solution exactly when one exists. If it finds none, the lower bound rules out every smaller answer and the GCD construction supplies an (n)-card solution, so (n) is optimal.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

LIMIT = 10**18
INF = LIMIT + 1

def solve_case(a):
    n = len(a)

    # suffix_gcd[i] = gcd(a[i], ..., a[n-1])
    # We need the gcd strictly after i, so suffix_gcd[i + 1].
    suffix_gcd = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        suffix_gcd[i] = math.gcd(a[i], suffix_gcd[i + 1])

    candidates = []

    # pref_lcm is the LCM of elements strictly before i.
    pref_lcm = 1

    for i, x in enumerate(a):
        if pref_lcm <= LIMIT and x % pref_lcm == 0:
            if suffix_gcd[i + 1] % x == 0:
                candidates.append(i)

        if pref_lcm <= LIMIT:
            g = math.gcd(pref_lcm, x)
            multiplier = x // g

            if pref_lcm > LIMIT // multiplier:
                pref_lcm = INF
            else:
                pref_lcm *= multiplier

    # Try every possible untouched element.
    for idx in candidates:
        target = a[idx]
        used = set()

        for x in a:
            if x == target:
                continue

            if x < target:
                card = target // x
            else:
                card = x // target

            if card in used:
                break

            used.add(card)
        else:
            return n - 1

    return n

def main():
    n = int(input())
    a = list(map(int, input().split()))
    print(solve_case(a))

if __name__ == "__main__":
    main()
```

The suffix GCD array is built from right to left. `suffix_gcd[i + 1]` contains exactly the elements after position `i`, so checking `suffix_gcd[i + 1] % x == 0` handles the right side of a candidate.

The prefix LCM is updated only after testing the current element, because the candidate itself must not be part of the prefix. The LCM is computed as (L/\gcd(L,x)\cdot x), which avoids unnecessary multiplication by a common factor.

The cap at (10^{18}+1) is a performance and clarity measure. Once the prefix LCM is larger than (10^{18}), no future array value can be divisible by it, because all array values are at most (10^{18}). We never need to know the exact larger LCM.

During candidate validation, the divisibility conditions have already been established. That lets the code use integer division directly instead of performing another modulo operation for every element.

The set contains card values, not transformed array values. Two elements may need the same quotient even though they start from different values, and that is exactly the situation in which the candidate must be rejected.

Python has arbitrary-precision integers, so there is no overflow when computing the LCM. The explicit cap still prevents the LCM from growing unnecessarily large and keeps the operation bounded.

## Worked Examples

### Sample 1

The input is

```
2
1 2
```

The prefix LCM and suffix GCD conditions leave both positions as possible candidates, but the first candidate already succeeds.

| Candidate | Prefix LCM | Suffix GCD | Required cards | Result |
| --- | --- | --- | --- | --- |
| (1) | (1) | (2) | (2) | Valid |

The target is (1). The element (2) is divided by card (2), producing (1). Only one card is needed, so the answer is (n-1=1).

This also confirms the boundary where the smallest element itself is the target.

### Sample 2

The input is

```
5
2 3 6 12 18
```

The candidate filtering produces the following results.

| Candidate | Prefix LCM | Suffix GCD | Candidate condition | Required cards | Result |
| --- | --- | --- | --- | --- | --- |
| (2) | (1) | (3) | Fails | (3,\ldots) | Reject |
| (3) | (2) | (6) | Fails | (2,\ldots) | Reject |
| (6) | (6) | (6) | Passes | (3,2,2,3) | Reject |
| (12) | (6) | (18) | Fails | (6,4,2,2) | Reject |
| (18) | (12) | (0) | Fails | (9,6,3,2) | Reject |

The interesting candidate is (6). Every array value is comparable with (6), but the card sequence would have to contain both (2) twice and (3) twice. Since each card exists only once, this cannot be done in four operations.

No target can give an (n-1) solution, so the answer is (n=5). A five-card construction exists, for example by targeting (72) and using cards (32,24,12,6,4).

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n\log 10^{18})) | There are at most about 60 candidate targets, and each candidate is checked in (O(n)) time |
| Space | (O(n)) | The suffix GCD array and the candidate list require linear space |

The logarithmic factor is tiny because (\log_2(10^{18})<60). With (n=200,000), the algorithm performs a linear preprocessing pass and at most roughly 60 candidate scans. The candidate bound is much stronger on typical inputs, and the scan stops immediately when a valid target is found. The memory usage is linear and comfortably fits the 512 MB limit.

## Test Cases

```python
import sys
import io
import math

LIMIT = 10**18
INF = LIMIT + 1

def solution(inp: str) -> str:
    data = list(map(int, inp.split()))
    n = data[0]
    a = data[1:1 + n]

    suffix_gcd = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        suffix_gcd[i] = math.gcd(a[i], suffix_gcd[i + 1])

    candidates = []
    pref_lcm = 1

    for i, x in enumerate(a):
        if pref_lcm <= LIMIT and x % pref_lcm == 0:
            if suffix_gcd[i + 1] % x == 0:
                candidates.append(i)

        if pref_lcm <= LIMIT:
            g = math.gcd(pref_lcm, x)
            multiplier = x // g
            if pref_lcm > LIMIT // multiplier:
                pref_lcm = INF
            else:
                pref_lcm *= multiplier

    for idx in candidates:
        target = a[idx]
        used = set()

        for x in a:
            if x == target:
                continue

            if x < target:
                card = target // x
            else:
                card = x // target

            if card in used:
                break
            used.add(card)
        else:
            return str(n - 1)

    return str(n)

def run(inp: str) -> str:
    return solution(inp).strip()

# Provided samples
assert run("""2
1 2
""") == "1", "sample 1"

assert run("""5
2 3 6 12 18
""") == "5", "sample 2"

assert run("""3
239 717 1434
""") == "2", "sample 3"

# n = 1, already equal to itself
assert run("""1
42
""") == "0", "single element"

# A clean n-1 construction.
# Target 1 needs cards 2, 3, 4, 5, 6.
assert run("""6
1 2 3 4 5 6
""") == "5", "distinct card ratios"

# Target 6 works with cards 3 and 2.
assert run("""3
2 3 6
""") == "2", "interior target"

# No array element can be an n-1 target.
# Target 30 would use cards 5, 3, 2, so n cards are enough.
assert run("""3
6 10 15
""") == "3", "non-array target"

# Values close to the 1e18 boundary.
# Neither divides the other, so two cards are necessary.
assert run("""2
999999999999999999 1000000000000000000
""") == "2", "1e18 boundary"

# Maximum-size test.
# The target 1 works, requiring every card 2..200000 exactly once.
max_n = 200000
max_input = str(max_n) + "\n" + " ".join(map(str, range(1, max_n + 1))) + "\n"
assert run(max_input) == str(max_n - 1), "maximum n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 42` | `0` | Minimum size and vacuously equal elements |
| `1 2 3 4 5 6` | `5` | A valid target at the smallest value with all distinct cards |
| `2 3 6` | `2` | An interior target and distinct card ratios |
| `6 10 15` | `3` | A non-array target can use one card per element but cannot reach (n-1) |
| `999999999999999999 1000000000000000000` | `2` | Values at the (10^{18}) boundary |
| `1..200000` | `199999` | Maximum (n), linear preprocessing, and a valid (n-1) construction |

## Edge Cases

For a single element,

```
1
42
```

the candidate is (42), the prefix LCM is (1), and the suffix GCD is (0). The candidate is valid, the ratio set is empty, and the algorithm returns (1-1=0). No operation is needed.

For repeated card requirements,

```
5
2 3 6 12 18
```

the candidate (6) passes the divisibility conditions. Its required ratios are (3,2,2,3). The set detects the second occurrence of (2) immediately, so (6) cannot provide an (n-1) solution. The other possible candidates fail the divisibility conditions, giving the correct answer (5).

For a target outside the array, consider

```
3
6 10 15
```

The value (30) is divisible by all three elements, and the ratios (5,3,2) are distinct. That gives a valid three-card construction, but it cannot give a two-card construction because none of the original elements is (30). With two operations, one element would have to remain untouched and would force the final value to be one of (6,10,15). The algorithm correctly returns (3).

For values near the upper bound,

```
2
999999999999999999 1000000000000000000
```

neither number divides the other. No original value can be a one-card target, so the answer cannot be (1). Two cards are sufficient by dividing each number by itself and reaching (1), so the answer is (2). The implementation also never relies on multiplication producing a value above (10^{18}).

For a large prefix LCM, the cap matters. Suppose the prefix contains values whose LCM already exceeds (10^{18}). No future array value can be divisible by that prefix LCM, because every future value is at most (10^{18}). The implementation replaces the LCM by (10^{18}+1), so all later candidates are rejected without constructing enormous integers.

For the maximum input size, the array

```
1 2 3 ... 200000
```

has (200,000) distinct values. Target (1) requires the cards (2,3,\ldots,200000), all distinct, so the answer is (199999). The candidate is found by the prefix LCM condition immediately, and the ratio scan confirms that every required card is unique.
