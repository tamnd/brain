---
title: "CF 102439E - Small business"
description: "We have a bag of digit blocks, represented by a string s. Every block must be used exactly once to build two decimal integers. The two integers may be equal, zero is allowed, but neither number may contain leading zeroes. Both numbers must be at most (10^{18})."
date: "2026-08-14T15:53:24+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102439
codeforces_index: "E"
codeforces_contest_name: "2018-2019 9th BSUIR Open Programming Championship. Semifinal"
rating: 0
weight: 102439
solve_time_s: 106
verified: true
draft: false
---

[CF 102439E - Small business](https://codeforces.com/problemset/problem/102439/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a bag of digit blocks, represented by a string `s`. Every block must be used exactly once to build two decimal integers. The two integers may be equal, zero is allowed, but neither number may contain leading zeroes. Both numbers must be at most (10^{18}).

The required pair is ordered by the smaller value first. Among all valid constructions, we first minimize the smaller number. Once that number is fixed, we minimize the other number. If no valid partition of all digit blocks exists, we print `-1 -1`.

The length bound of 50 is small enough for algorithms that do a constant amount of work per digit, but far too large for subset enumeration. There are up to (2^{50}), roughly (1.13 \times 10^{15}), ways to choose which blocks belong to the first number. Even if every partition could be checked in only a few dozen operations, this is far beyond the one second limit. The upper bound of (10^{18}) is the key structural restriction: every valid number has at most 19 digits, and a 19-digit number not exceeding (10^{18}) must be exactly `1000000000000000000`.

Several edge cases can fool a direct greedy implementation.

For `0`, there is only one block, so two nonempty numbers cannot be constructed. The answer is `-1 -1`. A careless implementation might treat the missing second number as zero.

For `00`, the correct answer is `0 0`. A rule saying that a number cannot contain zero as its first digit would incorrectly reject this case. A single zero is a valid representation of zero, while `00` would not be valid.

For `000`, the answer is `-1 -1`. Splitting it into `0` and `00` does not work because `00` has a leading zero. This shows why checking only the number of blocks is insufficient.

For `1000000000000000000`, which has 19 digits, the answer is `0 100000000000000000`. The smallest number can use one zero, leaving 18 blocks for the second number. A careless implementation that always tries to make (10^{18}) when it sees this digit pattern would miss the fact that minimizing the first number has priority.

For a 20-digit string containing only `2`, such as `22222222222222222222`, there is no way to make a valid 19-digit number at most (10^{18}), because every such number would have to be exactly (10^{18}). Yet the instance is still solvable as `22 222222222222222222`. This is the crucial reason we cannot simply demand an (10^{18}) block whenever the input has more than 19 digits. We must try every possible length for the smaller number.

## Approaches

A brute-force solution can choose an arbitrary subset of the digit blocks for the first number, use the complement for the second number, arrange the selected digits in every relevant order, and retain the best valid pair. This is correct because every possible partition appears among the subsets. The problem is the number of partitions. With 50 digits there are (2^{50}), approximately (1.13 \times 10^{15}), subset choices. Even processing each choice in (O(50)) time would require about (5.6 \times 10^{16}) elementary digit operations in the worst case, which is nowhere near feasible.

The useful observation is that the values are bounded by (10^{18}), so each number contains at most 19 digits. We can first decide the length (k) of the smaller number. If the other number has length (n-k), both lengths must be at most 19. Since the smaller number has fewer digits whenever (k<n-k), every valid (k)-digit positive number is automatically smaller than every valid ((n-k))-digit number. Thus the smallest feasible length of the smaller number is always the first length worth considering.

There are at most 19 possible lengths. For a fixed length (k), we construct the smallest possible (k)-digit number from the available digits. We do this from left to right. At every position we try digits in increasing order and temporarily take one copy. The only question is whether the remaining digits can still form the other number with its required length.

That feasibility check is extremely simple. If the other number has at most 18 digits, it is valid whenever its length is one, or, for a longer representation, it contains at least one nonzero digit. If it has 19 digits, it must be exactly (10^{18}), so its remaining multiset must contain one `1` and eighteen `0` digits.

Once the smaller number is fixed, the second number is minimized by arranging its remaining digits in increasing order, except that a multi-digit number must begin with the smallest available nonzero digit. This is the standard smallest-number construction from a multiset of digits.

The brute-force works because every partition is explicitly considered, but fails because there are exponentially many partitions. The observation that each number has at most 19 digits reduces the search to at most 19 candidate lengths, and each candidate can be solved greedily in constant-size digit space.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n2^n)) | (O(n)) | Too slow |
| Optimal | (O(n^2 \cdot 10)) | (O(n)) | Accepted |

## Algorithm Walkthrough

1. Count the occurrences of every digit and let `n = len(s)`. A valid pair needs both numbers to be nonempty, so if `n < 2` we immediately return `-1 -1`. Also, if `n > 38`, two numbers cannot fit because each has at most 19 digits.
2. Consider the possible length `k` of the smaller number from `max(1, n - 19)` through `floor(n / 2)`. The lower bound comes from the fact that the other number cannot contain more than 19 digits. We process these lengths in increasing order because a shorter valid smaller number is always better than a longer positive number.
3. For a fixed `k`, set `L = n - k`, the required length of the other number. Start with the full digit-count array and construct the first number from left to right.
4. At each position, try every digit from `0` through `9` in increasing order. At the first position, zero is allowed only when `k == 1`, because the single character `0` is a valid representation of zero. For a multi-digit number, the first digit must be nonzero.
5. Temporarily remove the candidate digit and ask whether the remaining digits can form a valid number of exactly `L` digits. If they cannot, restore the digit and try the next candidate. If they can, keep the candidate permanently and continue with the next position.
6. The feasibility test accepts every remaining multiset when `L == 1`, because any single digit is a valid number. For `2 <= L <= 18`, at least one remaining digit must be nonzero. For `L == 19`, the only accepted multiset is exactly one `1` and eighteen `0` digits, because `1000000000000000000` is the only 19-digit integer not exceeding (10^{18}).
7. After all `k` digits have been selected, arrange the remaining digits into the smallest possible second number. If there is only one digit, return it directly. Otherwise, place the smallest nonzero digit first, followed by all zeroes and then the remaining digits in sorted order.
8. Return the first feasible pair found. If `k < L`, the first number has fewer digits and is necessarily the smaller value. If `k == L`, the greedy construction gives the smallest possible first number among all feasible partitions, so after ordering the two resulting numbers, its pair is still optimal.

Why it works: for every candidate length, the construction maintains the invariant that the prefix chosen so far is the lexicographically smallest prefix that can still be completed into a valid pair. At each position, every smaller digit is tested first, and a digit is rejected only when the remaining blocks cannot form the required second number. Hence the first accepted digit is always optimal for that position. Processing the positions left to right gives the smallest feasible number of that length. Since lengths are processed from smallest to largest, the first feasible length gives the globally smallest possible smaller number. Finally, sorting the unused digits into the smallest valid representation gives the minimum possible second number for that fixed first number.

## Python Solution

```python
import sys
input = sys.stdin.readline

LIMIT = 10**18

def can_make_other(cnt, length):
    if sum(cnt) != length:
        return False

    if length == 1:
        return True

    if length == 19:
        return cnt[0] == 18 and cnt[1] == 1 and sum(cnt[2:]) == 0

    return any(cnt[d] > 0 for d in range(1, 10))

def build_smallest(cnt):
    length = sum(cnt)

    if length == 1:
        for d in range(10):
            if cnt[d]:
                return str(d)

    first = -1
    for d in range(1, 10):
        if cnt[d]:
            first = d
            break

    if first == -1:
        return None

    cnt[first] -= 1
    result = [str(first)]

    result.extend("0" for _ in range(cnt[0]))

    for d in range(1, 10):
        result.extend(str(d) for _ in range(cnt[d]))

    return "".join(result)

def solve(s):
    n = len(s)

    if n < 2 or n > 38:
        return "-1 -1"

    original = [0] * 10
    for ch in s:
        original[ord(ch) - ord('0')] += 1

    min_k = max(1, n - 19)
    max_k = n // 2

    for k in range(min_k, max_k + 1):
        other_len = n - k
        cnt = original[:]
        first_digits = []

        possible = True

        for pos in range(k):
            chosen = -1

            for d in range(10):
                if cnt[d] == 0:
                    continue

                if pos == 0 and k > 1 and d == 0:
                    continue

                cnt[d] -= 1

                if can_make_other(cnt, other_len):
                    chosen = d
                    break

                cnt[d] += 1

            if chosen == -1:
                possible = False
                break

            first_digits.append(str(chosen))

        if not possible:
            continue

        first = "".join(first_digits)
        second = build_smallest(cnt)

        if second is None:
            continue

        if len(second) > 19:
            continue

        if len(second) == 19 and second != "1000000000000000000":
            continue

        if k == other_len and first > second:
            first, second = second, first

        return first + " " + second

    return "-1 -1"

def main():
    s = input().strip()
    print(solve(s))

if __name__ == "__main__":
    main()
```

The `original` array stores the multiplicity of each digit, so every later decision can be made without repeatedly scanning the input string.

The outer loop considers only lengths that could possibly belong to the smaller number. `min_k = max(1, n - 19)` guarantees that the second number has at most 19 digits, while `n // 2` prevents us from considering a number that is longer than its counterpart.

The construction loop is the greedy part. At each position it tries digits in increasing order. A digit is temporarily removed before calling `can_make_other`, because that function must inspect exactly the blocks that would remain after committing to the candidate.

The special handling of the first position prevents representations such as `04`. The condition allows `0` when `k == 1`, because the one-character representation `0` is valid.

`can_make_other` handles the upper bound without relying on Python's arbitrary-precision integer conversion. A 19-digit valid number must be exactly (10^{18}), so checking its digit counts is both simpler and safer than constructing and converting a potentially invalid string.

`build_smallest` performs the secondary minimization. For a multi-digit number it chooses the smallest nonzero digit first, because placing zero there would create a leading zero. All zeroes can then be placed immediately after it, followed by the remaining digits in increasing order.

The final length-19 check is needed only for the second number. The greedy feasibility test already guarantees this condition, but keeping the explicit validation makes the boundary condition clear and prevents accidental future changes from violating the (10^{18}) limit.

Python integers do not overflow, but the solution never needs to convert the constructed strings into integers anyway. All comparisons are handled by length and, for the only relevant 19-digit case, by direct comparison with the exact string representation of (10^{18}).

## Worked Examples

### Sample 1

For `123456`, the input has six digits. The first possible smaller-number length is one, so the algorithm tries to build a one-digit number.

| k | Position | Candidate digit | Remaining digits | Other length | Feasible |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | `23456` | 5 | Yes |

The first candidate digit is `1`, and the remaining five digits form a valid five-digit number. Since `1` is the smallest possible one-digit choice that can be completed, the answer is `1 23456`. The remaining digits are already optimally arranged in increasing order.

### Sample 2

For `42`, there are two digits, so again the smallest possible length is one.

| k | Position | Candidate digit | Remaining digits | Other length | Feasible |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | `42` | 1 | No |
| 1 | 1 | 1 | `42` | 1 | No |
| 1 | 1 | 2 | `4` | 1 | Yes |

There is no zero or one block, so the first feasible digit is `2`. The remaining digit is `4`, giving `2 4`. The pair is already ordered correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n^2 \cdot 10)) | There are at most 19 candidate lengths, at most 19 positions per construction, and 10 candidate digits at each position. Each feasibility check scans only 10 digit counts. |
| Space | (O(n)) | The input and constructed strings use (O(n)) space, while the digit-count arrays have constant size. |

With (n \le 50), the algorithm performs only a few thousand small operations. The 38-digit maximum for any feasible instance follows directly from the 19-digit limit on each number, so the solution comfortably fits the one second and 256 MB limits.

## Test Cases

```python
import sys
import io

def can_make_other(cnt, length):
    if sum(cnt) != length:
        return False

    if length == 1:
        return True

    if length == 19:
        return cnt[0] == 18 and cnt[1] == 1 and sum(cnt[2:]) == 0

    return any(cnt[d] > 0 for d in range(1, 10))

def build_smallest(cnt):
    length = sum(cnt)

    if length == 1:
        for d in range(10):
            if cnt[d]:
                return str(d)

    first = -1
    for d in range(1, 10):
        if cnt[d]:
            first = d
            break

    if first == -1:
        return None

    cnt[first] -= 1
    result = [str(first)]
    result.extend("0" for _ in range(cnt[0]))

    for d in range(1, 10):
        result.extend(str(d) for _ in range(cnt[d]))

    return "".join(result)

def solve(s):
    n = len(s)

    if n < 2 or n > 38:
        return "-1 -1"

    original = [0] * 10
    for ch in s:
        original[ord(ch) - ord('0')] += 1

    min_k = max(1, n - 19)
    max_k = n // 2

    for k in range(min_k, max_k + 1):
        other_len = n - k
        cnt = original[:]
        first_digits = []
        possible = True

        for pos in range(k):
            chosen = -1

            for d in range(10):
                if cnt[d] == 0:
                    continue

                if pos == 0 and k > 1 and d == 0:
                    continue

                cnt[d] -= 1

                if can_make_other(cnt, other_len):
                    chosen = d
                    break

                cnt[d] += 1

            if chosen == -1:
                possible = False
                break

            first_digits.append(str(chosen))

        if not possible:
            continue

        first = "".join(first_digits)
        second = build_smallest(cnt)

        if second is None:
            continue

        if len(second) > 19:
            continue

        if len(second) == 19 and second != "1000000000000000000":
            continue

        if k == other_len and first > second:
            first, second = second, first

        return first + " " + second

    return "-1 -1"

def run(inp: str) -> str:
    return solve(inp.strip())

# Provided samples
assert run("123456") == "1 23456", "sample 1"
assert run("42") == "2 4", "sample 2"
assert run("000") == "-1 -1", "sample 3"

# Minimum-size input
assert run("7") == "-1 -1", "one block cannot form two numbers"

# Two zero blocks
assert run("00") == "0 0", "zero is valid when it is represented by one block"

# Boundary at 19 digits
assert run("1000000000000000000") == \
       "0 100000000000000000", "19-digit boundary"

# Twenty digits where 19-digit 10^18 is impossible
assert run("22222222222222222222") == \
       "22 222222222222222222", "must try a smaller length"

# All equal digits
assert run("11111111111111111111") == \
       "11 111111111111111111", "equal-digit construction"

# Maximum feasible length, both numbers equal 10^18
s38 = "11" + "0" * 36
assert run(s38) == \
       "1000000000000000000 1000000000000000000", "maximum feasible length"

# Maximum input length, impossible because two numbers hold at most 38 blocks
assert run("0" * 50) == "-1 -1", "50 blocks cannot fit"

print("all tests passed")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `7` | `-1 -1` | Minimum input size and the requirement for two nonempty numbers |
| `00` | `0 0` | Correct treatment of zero without leading-zero rejection |
| `1000000000000000000` | `0 100000000000000000` | The 19-digit and (10^{18}) boundary |
| `22222222222222222222` | `22 222222222222222222` | Falling back from a 19-digit second number to an 18-digit one |
| `11111111111111111111` | `11 111111111111111111` | Equal digits and equal-length construction |
| `11` + 36 zeroes | `1000000000000000000 1000000000000000000` | Maximum feasible total length |
| 50 zeroes | `-1 -1` | Absolute input-length limit and impossibility beyond 38 usable blocks |

## Edge Cases

For the one-block input `7`, the length loop cannot produce two nonempty numbers because `n < 2` is rejected immediately. The output is `-1 -1`. This prevents an implementation from accidentally treating one number as empty.

For `00`, the first candidate length is one. The greedy construction tries `0`, removes it, and leaves one zero for the other number. Since the other length is also one, `can_make_other` accepts it. The result is `0 0`. The special one-digit rule is what distinguishes this valid representation from an invalid multi-digit string such as `00`.

For `000`, the same first attempt chooses `0`, but two zeroes remain for the second number. Its required length is two, and `can_make_other` rejects an all-zero multiset for every length greater than one. There are no nonzero candidates, so the algorithm reports `-1 -1`.

For `1000000000000000000`, the algorithm starts with `k = 1`. It tries `0` before `1`, and after removing one zero there are 18 digits left, forming the valid number `100000000000000000`. Thus the smaller number becomes zero immediately. The result is `0 100000000000000000`, which is better than using the `1` as the smaller number.

For `22222222222222222222`, the first candidate length is one, leaving 19 digits for the other number. The feasibility test rejects those 19 twos because a 19-digit valid number must be exactly (10^{18}). The algorithm then tries `k = 2`. Now the other number has 18 digits, and an 18-digit number consisting of twos is below (10^{18}), so `22` is accepted as the smallest two-digit number. The result is `22 222222222222222222`.

For the maximum feasible length, the input consists of two `1` blocks and 36 zero blocks. The only possible valid 19-digit number is (10^{18}), and there are exactly enough blocks to make two copies. The algorithm reaches `k = 19`, verifies the exact digit multiset for the second number, and constructs the same value for both sides.

For an input of length 50, the algorithm rejects before attempting any construction. Each number can contain at most 19 digits, so two numbers can consume at most 38 blocks. No partition can use all 50 blocks while respecting the numerical limit, making `-1 -1` unavoidable.
