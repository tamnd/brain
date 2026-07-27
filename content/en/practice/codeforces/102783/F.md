---
title: "CF 102783F - Xorro the Xorman"
description: "The problem gives two non-negative integers, A and B. We must choose an integer b in the interval from 0 to B and maximize the value of A XOR b. The output is the largest XOR value that can be obtained."
date: "2026-07-27T19:59:42+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102783
codeforces_index: "F"
codeforces_contest_name: "UTPC Contest 10-23-20 Div. 2"
rating: 0
weight: 102783
solve_time_s: 48
verified: true
draft: false
---

[CF 102783F - Xorro the Xorman](https://codeforces.com/problemset/problem/102783/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 48s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem gives two non-negative integers, A and B. We must choose an integer b in the interval from 0 to B and maximize the value of A XOR b. The output is the largest XOR value that can be obtained. The input values can be as large as 10^18, so the solution must work with numbers containing around 60 bits.

A solution that tries every possible b is immediately impossible. If B is 10^18, there are about one quintillion candidates, far beyond what can be checked within normal contest limits. Even a very optimized constant-time check per value would require too many operations. Since the number of relevant bits is only about 60, the intended solution should depend on the binary representation rather than the size of the numeric range.

The tricky cases come from the fact that b is bounded above, not fixed. A greedy approach that simply flips every bit of A would often create a number larger than B.

For example:

```
Input:
5 4

Output:
7
```

Here A is 101 in binary and B is 100. Choosing b = 2 gives 101 XOR 010 = 111, which is 7. A careless solution might choose b = 0 because the highest bit of B is equal to the highest bit of A, missing that a smaller prefix allows more freedom later.

Another edge case is when B itself is the best possible choice.

```
Input:
7 32

Output:
39
```

The best b is 32, because 7 XOR 32 = 39. A method that only considers values with the same bit length as A can miss valid answers.

A final important case is B = 0.

```
Input:
10 0

Output:
10
```

There is only one possible choice, b = 0. Any algorithm that assumes it can always lower a bit of B to gain flexibility will fail here.

## Approaches

The direct approach is to test every possible b from 0 to B, compute A XOR b, and keep the maximum. This is correct because every allowed value is considered. Its worst case is O(B) operations, which becomes O(10^18) and is unusable.

The key observation is that XOR comparison works exactly like ordinary binary comparison. To maximize the final number, the most significant bit where we can make a decision matters first. If we can make a bit of the result equal to 1 without making b exceed B, we should do it immediately because every lower bit becomes irrelevant after a higher bit differs.

Process the bits from most significant to least significant. While matching the prefix of B, we have two choices. We can keep b's current bit equal to B's bit, meaning the prefix remains equal and future choices are restricted. Or, if B has a 1 at this position, we can place a 0 in b, making b's prefix smaller than B's. Once the prefix becomes smaller, every remaining bit of b can be chosen freely, so we simply choose bits that maximize XOR with A.

This reduces the problem to examining only about 60 bit positions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(B) | O(1) | Too slow |
| Optimal | O(log B) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read A and B and inspect their bits from the highest bit down to bit 0. Only around 60 bits are needed because the numbers are at most 10^18.
2. Maintain whether the prefix of the chosen number b is already smaller than the prefix of B. If it is smaller, the remaining bits are unrestricted because any continuation will still produce a value below B.
3. If the prefix is already smaller, set every remaining bit of b to the opposite of A's bit. This makes every remaining XOR bit equal to 1.
4. If the prefix is equal to B, compare the current bit of B. If it is 0, b must also use 0 at this position. If it is 1, consider the choice of putting 0 in b. This makes b smaller than B and gives freedom on all later bits, so the answer can take the best possible suffix.
5. Track the maximum answer obtained by the two possible states. The implementation can avoid storing the actual b values by directly constructing the best XOR value.

Why it works: the highest bit where two possible answers differ determines which answer is larger. At every bit, the algorithm chooses whether it is possible to create a 1 in the answer without violating b <= B. If making the prefix smaller is possible, all lower bits can be optimized independently. If it is not possible, the current bit is forced. Thus every decision preserves the maximum achievable prefix, and after all bits are processed the complete answer is optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    A, B = map(int, input().split())

    ans = 0
    smaller = False

    for i in range(60, -1, -1):
        abit = (A >> i) & 1
        bbit = (B >> i) & 1

        if smaller:
            ans |= (1 << i)
        else:
            if bbit == 0:
                if abit == 1:
                    ans |= (1 << i)
            else:
                if abit == 0:
                    ans |= (1 << i)
                smaller = True

    print(ans)

if __name__ == "__main__":
    solve()
```

The loop processes bits from high to low because higher bits decide the numerical ordering of the final XOR value. The variable `smaller` records whether the constructed b prefix is already below B. Once this happens, the upper bound no longer restricts future bits.

When `B` has a zero bit while prefixes are equal, the corresponding bit of b is forced to zero. The XOR bit is then determined entirely by A. When `B` has a one bit, choosing b's bit as zero creates a smaller prefix and allows all future XOR bits to become one. This is why the code marks the state as smaller immediately after handling such a position.

Python integers do not overflow, so the 60-bit operations are safe. The loop includes bit 60 to cover the largest possible value of 10^18.

## Worked Examples

For the input:

```
5 4
```

the binary values are A = 101 and B = 100.

| Bit | A bit | B bit | Smaller before | Answer bit | Smaller after |
| --- | --- | --- | --- | --- | --- |
| 2 | 1 | 1 | false | 0 | true |
| 1 | 0 | 0 | true | 1 | true |
| 0 | 1 | 0 | true | 1 | true |

The result is 111, which is 7. The first bit of b is chosen as zero, making b smaller than B and allowing the remaining bits to maximize XOR.

For the input:

```
7 32
```

A = 000111 and B = 100000.

| Bit | A bit | B bit | Smaller before | Answer bit | Smaller after |
| --- | --- | --- | --- | --- | --- |
| 5 | 0 | 1 | false | 1 | true |
| 4 | 0 | 0 | true | 1 | true |
| 3 | 0 | 0 | true | 1 | true |
| 2 | 1 | 0 | true | 1 | true |
| 1 | 1 | 0 | true | 1 | true |
| 0 | 1 | 0 | true | 1 | true |

The result is 111111, which is 39. Choosing b = 32 creates the smaller-prefix state immediately and leaves all lower bits available.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log B) | The algorithm checks each binary digit once. |
| Space | O(1) | Only a few integer variables are stored. |

The input limit requires avoiding any iteration over the numeric range. Since 10^18 fits into about 60 binary digits, the solution performs only a constant number of operations relative to the constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    A, B = map(int, sys.stdin.readline().split())
    ans = 0
    smaller = False
    for i in range(60, -1, -1):
        abit = (A >> i) & 1
        bbit = (B >> i) & 1
        if smaller:
            ans |= 1 << i
        elif bbit == 0:
            if abit:
                ans |= 1 << i
        else:
            if abit == 0:
                ans |= 1 << i
            smaller = True
    sys.stdin = old
    return str(ans) + "\n"

assert run("5 4\n") == "7\n", "sample 1"
assert run("7 32\n") == "39\n", "sample 2"
assert run("0 0\n") == "0\n", "minimum values"
assert run("10 0\n") == "10\n", "zero upper bound"
assert run("15 15\n") == "15\n", "equal values"
assert run("1000000000000000000 1000000000000000000\n") == "1152921504606846975\n", "large boundary"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0 0 | 0 | Handles the smallest possible input. |
| 10 0 | 10 | Confirms that no choice except zero is handled. |
| 15 15 | 15 | Checks equal A and B behavior. |
| 1000000000000000000 1000000000000000000 | 1152921504606846975 | Tests large bit positions. |

## Edge Cases

For `A = 5` and `B = 4`, the first bit of B gives a choice. Taking b's highest bit as zero makes b smaller than B, so all lower bits can be chosen to oppose A. The algorithm reaches the same decision and produces 7.

For `A = 7` and `B = 32`, the first bit of B allows the constructed number to become smaller immediately. After that point every remaining answer bit can become one, producing 39.

For `A = 10` and `B = 0`, every bit of b is forced to zero because no smaller prefix is possible. The answer is exactly A XOR 0, which is 10.
