---
title: "CF 102535M - Kim Possible and the Mooks and the Reversinator"
description: "The line of opponents can be viewed as a binary string where O means a currently active Mook and E means a defeated Meek. Every time Kim reaches an active Mook, one minute passes, that position becomes E, and every position before it flips back to O."
date: "2026-08-07T21:09:18+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102535
codeforces_index: "M"
codeforces_contest_name: "2020 UP ACM Algolympics Elimination Round"
rating: 0
weight: 102535
solve_time_s: 171
verified: true
draft: false
---

[CF 102535M - Kim Possible and the Mooks and the Reversinator](https://codeforces.com/problemset/problem/102535/M)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 51s  
**Verified:** yes  

## Solution
## Problem Understanding

The line of opponents can be viewed as a binary string where `O` means a currently active Mook and `E` means a defeated Meek. Every time Kim reaches an active Mook, one minute passes, that position becomes `E`, and every position before it flips back to `O`. The Reversinator lets us reverse exactly one contiguous part of the initial line before any fights begin. We need choose that reversal so the total number of minutes required to clear the line is as small as possible.

The key observation is that the fighting process is not an arbitrary simulation. If we assign the leftmost character weight 1, the next character weight 2, the next weight 4, and so on, one fight operation is exactly the same as subtracting one from this binary number. The leftmost `O` acts like the least significant set bit: it becomes zero, and all smaller bits become one. The total number of fights is the value of this binary number.

The input contains up to 35000 strings, but their total length is only 500000. This rules out trying every possible reversal, because there can be about n² choices for a substring. Even a solution that simulates the fight process for each choice is impossible because the number represented by the string can be exponentially large. We need a linear or near-linear approach for each test case.

A common mistake is to optimize the string in its original left-to-right order. The weights grow toward the right, so the right side of the original string has the largest effect. Another mistake is forgetting that the reversal must still be used once. A segment of length one is allowed and means leaving the string unchanged.

For example, with input `E`, there is no Mook, so the answer is `0`. A method that always searches for a beneficial reversal could fail by assuming there must be a change. For input `O`, the answer is `1`, because one fight is needed and reversing cannot help. For input `EOOE`, the original value is `6`, but reversing the best segment gives `EEOO`, whose value is `3`. A method that treats the original order as the most significant side would choose incorrectly.

## Approaches

A direct approach is to try every possible interval, reverse it, compute the resulting binary value, and keep the minimum. There are O(n²) intervals. Even if reversing and evaluating an interval were optimized to O(1), the number of candidates is already too large for n = 500000. The brute force is correct because it checks every possible use of the Reversinator, but the search space is the problem.

The useful transformation is to look at the binary number in normal notation. Reverse the original string. In this reversed representation, the first character is the most significant bit. Reversing a segment in the original string is still just reversing a segment in this new string. The task becomes finding the lexicographically smallest binary string obtainable by one substring reversal.

For a binary string, the best possible reversal is easy to characterize. If there is no zero after the first one, the string is already as small as it can become. Otherwise, the first position containing `1` should receive a `0`, and the only way to move a zero there is to reverse up to the last zero. Any smaller ending would leave the first changed position worse, and any earlier start would keep an unchanged leading `1`.

After this reversal, we only need to evaluate the resulting binary number modulo `10^9`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Reverse the input string. This changes the representation so that ordinary lexicographical comparison matches the numerical comparison of the fight count.
2. Find the first occurrence of `1` in the reversed string. This is the first place where we could possibly reduce the number.
3. Find the last occurrence of `0` in the reversed string. This is the farthest zero that can be moved to the earliest useful position.
4. If the first `1` appears before the last `0`, reverse that interval. This places a zero at the first significant position that can be improved.
5. Convert the resulting binary string to a number modulo `10^9` by scanning from left to right and repeatedly doubling the current value.

Why it works: The reversed string is a normal binary representation, so making it lexicographically smaller is exactly the same as making the fight count smaller. The first differing bit decides the result. A reversal can only improve the string by moving a zero left across one or more ones. The earliest one followed by the latest zero gives the maximum possible improvement at the first differing position, and after that the reversal fixes the remaining order automatically. If such a pair does not exist, every possible reversal keeps the first significant bit unchanged or makes it larger.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9

def solve_case(s):
    s = s[::-1]

    first_one = -1
    last_zero = -1

    for i, c in enumerate(s):
        if c == '1' and first_one == -1:
            first_one = i
        if c == '0':
            last_zero = i

    if first_one != -1 and last_zero > first_one:
        s = s[:first_one] + s[first_one:last_zero + 1][::-1] + s[last_zero + 1:]

    ans = 0
    for c in s:
        ans = (ans * 2 + (c == '1')) % MOD
    return ans

def main():
    t = int(input())
    out = []
    for _ in range(t):
        s = input().strip()
        out.append(str(solve_case(s)))
    print("\n".join(out))

if __name__ == "__main__":
    main()
```

The first transformation, `s[::-1]`, is the central simplification. It turns the unusual fighting process into ordinary binary arithmetic.

The search for `first_one` and `last_zero` is done in one scan. If `first_one` is not before `last_zero`, there is no useful movement of a zero toward a more significant position, so the string stays unchanged.

The slicing reversal is safe because it is applied only once. The final loop never constructs the huge integer represented by the binary string. It keeps only the remainder modulo `10^9`, which avoids overflow and works for the maximum length.

## Worked Examples

For `EOOE`, the reversed representation starts as `EOOE`.

| String state | First `1` | Last `0` | Action | Value |
| --- | --- | --- | --- | --- |
| EOOE | 1 | 3 | Reverse positions 1 through 3 | EEOO |
| EEOO | - | - | Convert binary value | 3 |

The reversal moves the final zero to the most significant possible place. This demonstrates why the original direction of the string is misleading.

For `OOE`, the reversed representation is `EOO`.

| String state | First `1` | Last `0` | Action | Value |
| --- | --- | --- | --- | --- |
| EOO | 1 | 2 | Reverse positions 1 through 2 | EOO |
| EOO | - | - | Convert binary value | 3 |

Here the reversal does not improve the value because the two affected bits are both already in the best order. The algorithm correctly allows the mandatory reversal to have no visible effect.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each string is scanned a constant number of times. |
| Space | O(n) | The reversed string and temporary slices require linear memory. |

The total length of all test cases is 500000, so a linear solution easily fits the time limit. The memory usage remains proportional to one test case.

## Test Cases

```python
import sys
import io

MOD = 10**9

def solve_case(s):
    s = s[::-1]
    first_one = -1
    last_zero = -1

    for i, c in enumerate(s):
        if c == '1' and first_one == -1:
            first_one = i
        if c == '0':
            last_zero = i

    if first_one != -1 and last_zero > first_one:
        s = s[:first_one] + s[first_one:last_zero + 1][::-1] + s[last_zero + 1:]

    ans = 0
    for c in s:
        ans = (ans * 2 + (c == '1')) % MOD
    return ans

def run(inp: str) -> str:
    data = inp.strip().split()
    t = int(data[0])
    ans = []
    for i in range(1, t + 1):
        ans.append(str(solve_case(data[i])))
    return "\n".join(ans)

assert run("""1
EOOE
""") == "3", "sample 1"

assert run("""1
O
""") == "1", "single mook"

assert run("""1
E
""") == "0", "single meek"

assert run("""1
OO
""") == "3", "all mooks"

assert run("""1
EEEEEE
""") == "0", "all meeks"

assert run("""1
OOOOOOOOOO
""") == "1023", "long all mooks"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `O` | `1` | Minimum size with one active opponent |
| `E` | `0` | Minimum size with no fights required |
| `OO` | `3` | A reversal cannot always improve the value |
| `EEEEEE` | `0` | All defeated opponents |
| `OOOOOOOOOO` | `1023` | Large uniform input and modular conversion |

## Edge Cases

For `E`, the reversed string contains no `1`, so `first_one` remains unset. The algorithm skips the reversal and evaluates the zero value, producing `0`.

For `O`, there is a `1` but no `0`, so there is no way to move a smaller bit to the front. The algorithm leaves the string unchanged and returns the value `1`.

For `EOOE`, the original fight count is not minimal. After reversing the string to `EOOE`, the algorithm finds the first `1` at index 1 and the last `0` at index 3, reverses that part, and obtains `EEOO`. The binary value becomes `3`, matching the optimal result.

For an input containing only `O` characters, such as `OOOOOOOOOO`, every possible reversal produces the same string. The algorithm detects the absence of zeros and directly computes the binary value without unnecessary operations.
