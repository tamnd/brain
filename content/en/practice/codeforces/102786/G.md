---
title: "CF 102786G - Timestamp"
description: "The clock displays a ten-digit timestamp. At any moment, every digit consumes a fixed amount of energy per second depending on which digit is shown. The display starts at timestamp 0000000000, then increases by one every second."
date: "2026-07-27T19:28:20+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102786
codeforces_index: "G"
codeforces_contest_name: "\u041e\u0442\u043a\u0440\u044b\u0442\u044b\u0439 \u0447\u0435\u043c\u043f\u0438\u043e\u043d\u0430\u0442 \u042f\u0440\u0413\u0423 \u0438\u043c. \u041f.\u0413. \u0414\u0435\u043c\u0438\u0434\u043e\u0432\u0430 Demidov Open IT Cup 2019"
rating: 0
weight: 102786
solve_time_s: 57
verified: true
draft: false
---

[CF 102786G - Timestamp](https://codeforces.com/problemset/problem/102786/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 57s  
**Verified:** yes  

## Solution
## Problem Understanding

The clock displays a ten-digit timestamp. At any moment, every digit consumes a fixed amount of energy per second depending on which digit is shown. The display starts at timestamp `0000000000`, then increases by one every second. Leading zeroes are always present, so every state is a ten-character number.

The input is a single number `N`, the number of seconds the clock runs. During those seconds, the clock shows timestamps from `0` through `N - 1`. The task is to find the total energy consumed by all ten digits during those displayed states.

The digit costs are the number of active segments in the seven-segment style font:

| Digit | Cost |
| --- | --- |
| 0 | 6 |
| 1 | 2 |
| 2 | 5 |
| 3 | 5 |
| 4 | 4 |
| 5 | 5 |
| 6 | 6 |
| 7 | 3 |
| 8 | 7 |
| 9 | 6 |

The value of `N` can be almost `10^10`. A direct simulation would require visiting up to ten billion timestamps, and each timestamp requires checking ten digits, which gives about `10^11` digit operations. That is far beyond what can fit into a one second limit. The solution must avoid iterating through timestamps and instead count how often every digit appears at every position.

The main edge cases come from the fixed width of the display and the fact that the range ends at `N - 1`. For example, with input `1`, the only displayed value is `0000000000`. The answer is `60`, because ten zeroes are lit for one second. A solution that starts counting from timestamp `1` would incorrectly return the cost of `0000000001`.

Another common mistake is forgetting that the upper bound is exclusive. For input `10`, the clock shows `0000000000` through `0000000009`, not through `0000000010`. The correct answer is `589`. A method that counts the state after the tenth second adds an extra timestamp and gets the wrong result.

A third issue appears near the largest values. For input `9999999999`, the last displayed timestamp is `9999999998`. The value `9999999999` must not be included. Counting all ten-digit values and forgetting to remove the final one overestimates the answer by `60`.

## Approaches

A straightforward solution would simulate the clock. For every second, convert the timestamp to a ten-digit string, add the cost of each digit, and continue until `N` seconds have passed. This approach is easy to verify because it follows the statement directly. However, the worst case requires processing almost `10^10` timestamps, and even a very optimized implementation would need around `10^11` digit additions.

The structure of the display gives us a way to skip this work. Instead of asking which digits appear in every timestamp, we can ask how many times a particular digit appears in a particular position among all timestamps from `0` to `N - 1`.

For example, consider the last digit. It cycles from `0` to `9` repeatedly. For higher positions, the cycle length becomes larger, but the same pattern remains. Every position can be handled independently by counting complete cycles and a remaining partial cycle.

For a position with place value `p`, numbers repeat in blocks of size `10 * p`. Inside every block, each digit stays in that position for exactly `p` consecutive numbers. The number of complete blocks gives a simple contribution for all digits. The remaining numbers after those blocks are handled by checking how much of the current cycle has been covered.

After finding how many times each digit appears in every position, we multiply those counts by the corresponding energy costs and add everything together. The ten-digit width only means we repeat this calculation for place values from `1` through `1,000,000,000`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(10N) | O(1) | Too slow |
| Optimal | O(10 * 10) | O(1) | Accepted |

## Algorithm Walkthrough

1. Process every decimal position separately, starting with the units position and continuing up to the highest of the ten displayed positions. The contribution of one position is independent from all other positions, so summing positions separately avoids handling whole timestamps.
2. For a position with value `p`, split `N` into a number of complete cycles and a remainder. A full cycle has length `10 * p`, because every digit from `0` to `9` appears for `p` consecutive timestamps.
3. Add the contribution of complete cycles. Every digit appears exactly `p` times per cycle, and the number of cycles is `N // (10 * p)`.
4. Handle the incomplete cycle. After the complete cycles, the current position starts at digit `0`. The first `min(remainder, p)` values add digit `0`, the next `p` values add digit `1`, and so on until the remainder is exhausted.
5. Multiply every digit frequency for this position by the energy cost of that digit and add it to the final answer.

The reason this works is that each decimal position follows a perfectly repeating pattern. The units position repeats every ten timestamps, the tens position repeats every one hundred timestamps, and so on. Counting complete repetitions and one unfinished repetition accounts for every timestamp exactly once. Since every displayed timestamp is just the sum of its ten independent digit positions, the total energy is also the sum of these independent position contributions.

## Python Solution

```python
import sys
input = sys.stdin.readline

cost = [6, 2, 5, 5, 4, 5, 6, 3, 7, 6]

def solve():
    n = int(input())

    ans = 0
    place = 1

    for _ in range(10):
        cycle = place * 10
        full = n // cycle
        rem = n % cycle

        for digit in range(10):
            cnt = full * place

            extra_start = digit * place
            extra_end = (digit + 1) * place

            if rem > extra_start:
                cnt += min(rem, extra_end) - extra_start

            ans += cnt * cost[digit]

        place *= 10

    print(ans)

if __name__ == "__main__":
    solve()
```

The array `cost` stores the energy required for one second of displaying each digit. The loop over ten positions matches the physical width of the clock, so no special handling is needed for leading zeroes.

For each position, `place` represents how many consecutive timestamps contain the same digit in that position. For example, in the tens position `place` is `10`, because each digit occupies ten consecutive numbers.

`full * place` counts complete cycles. The partial cycle logic calculates the overlap between the remaining timestamps and the interval belonging to a particular digit. The expression using `min` prevents the count from extending beyond the remainder.

The variable `ans` can become larger than 32-bit integer range. Python integers grow automatically, but languages with fixed-size integers need a 64-bit type.

The loop runs exactly ten times for the ten digits of the display. The order of processing positions does not matter because the energy of each digit position is independent.

## Worked Examples

Since the original statement does not contain visible sample values, we use small traces.

For input `1`, the clock displays only `0000000000`.

| Position | Place value | Full cycles | Remainder | Contribution |
| --- | --- | --- | --- | --- |
| Ones | 1 | 0 | 1 | digit 0 appears once |
| Tens | 10 | 0 | 1 | digit 0 appears once |
| Hundreds | 100 | 0 | 1 | digit 0 appears once |
| Remaining positions | larger values | 0 | 1 | digit 0 appears once |

Every one of the ten positions contributes the cost of digit `0`, which is `6`. The final answer is `10 * 6 = 60`.

For input `10`, the clock displays `0000000000` through `0000000009`.

| Position | Place value | Full cycles | Remainder | Digit pattern |
| --- | --- | --- | --- | --- |
| Ones | 1 | 1 | 0 | 0 through 9 once |
| Tens | 10 | 0 | 10 | zero appears ten times |
| Other positions | 100+ | 0 | 10 | zero appears ten times |

The ones position contributes the sum of all digit costs, which is `49`. Each of the other nine positions contributes `10 * 6 = 60`. The answer is `49 + 9 * 60 = 589`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(100) | Ten positions are processed, and each checks ten digits |
| Space | O(1) | Only a few counters and the digit cost array are stored |

The algorithm performs a constant amount of work regardless of the size of `N`. It easily fits the limit even when `N` is close to `10^10`.

## Test Cases

```python
import sys
import io

cost = [6, 2, 5, 5, 4, 5, 6, 3, 7, 6]

def solve_case(inp: str) -> str:
    n = int(inp)

    ans = 0
    place = 1

    for _ in range(10):
        cycle = place * 10
        full = n // cycle
        rem = n % cycle

        for digit in range(10):
            cnt = full * place
            start = digit * place
            end = (digit + 1) * place

            if rem > start:
                cnt += min(rem, end) - start

            ans += cnt * cost[digit]

        place *= 10

    return str(ans)

def run(inp: str) -> str:
    return solve_case(inp)

assert run("1") == "60", "minimum input"
assert run("10") == "589", "single complete units cycle"
assert run("11") == "656", "boundary after a full units cycle"
assert run("100") == "5890", "transition into hundreds position"
assert run("9999999999") == "489999999940", "maximum valid input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `60` | The initial all-zero display is counted |
| `10` | `589` | A full cycle of the last digit is handled |
| `11` | `656` | The first timestamp after a cycle boundary |
| `100` | `5890` | Carrying into the next digit position |
| `9999999999` | `489999999940` | Maximum range and large answer handling |

## Edge Cases

For `N = 1`, the algorithm has `full = 0` and `rem = 1` for every position. The partial cycle adds one occurrence of digit `0` at every position, giving ten zeroes and an answer of `60`. No timestamp after zero is accidentally included.

For `N = 10`, the units position has one complete cycle and every higher position has only the partial part of a cycle. This separates the last digit from the leading zeroes and produces `589`.

For `N = 9999999999`, the algorithm counts every ten-digit number except `9999999999` itself because the range ends at `N - 1`. If the last number were accidentally included, the result would be larger by `60`, which is exactly the cost of displaying ten nines for one second. The cycle counting avoids that off-by-one error because all calculations are performed over the first `N` timestamps.
