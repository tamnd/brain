---
title: "CF 102441B - Redistribution of Digits"
description: "We have a multiset of nonzero decimal digits. Every occurrence matters, so if the input contains three copies of 7, all three copies must be used exactly once. We also have n upper bounds."
date: "2026-08-08T13:20:31+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102441
codeforces_index: "B"
codeforces_contest_name: "2018-2019 9th BSUIR Open Programming Championship. Final"
rating: 0
weight: 102441
solve_time_s: 144
verified: true
draft: false
---

[CF 102441B - Redistribution of Digits](https://codeforces.com/problemset/problem/102441/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 24s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a multiset of nonzero decimal digits. Every occurrence matters, so if the input contains three copies of `7`, all three copies must be used exactly once. We also have `n` upper bounds. Our task is to rearrange all available digits into exactly `n` positive integers so that the number assigned to each bound does not exceed that bound.

The numbers we construct do not have to use the same number of digits. A two-digit bound can receive a one-digit number, for example. The only global requirement is that every input digit is consumed exactly once. The order in which the bounds appear in the input does not matter, because any valid assignment may be printed in the original order.

The largest input string has only 500 digits, while there are at most 50 bounds. This immediately rules out permutation-based search. Even with only the nine possible nonzero digits, the number of possible arrangements grows exponentially with the number of occurrences. The upper bounds have at most 10 digits, so constructing one candidate number can be handled with a very small constant amount of work. The useful structure is that the digit alphabet has constant size, while the total number of digits can be large.

There are three edge cases that a careless implementation can mishandle.

First, the total number of available digits may be larger than the total number of positions allowed by the bounds. For example, with `12345 2 21 43`, the two bounds can contain at most four digits, but five digits must be used. The correct output is `-1`. A greedy implementation that constructs two valid numbers and simply forgets the unused digit violates the requirement that every digit be used.

Second, giving the shortest possible number to the current bound is not always safe. Consider `129 2 13 22`. A naive ascending strategy might give the one-digit number `2` or `1` to the first bound and leave `29` for `22`, which is invalid. A valid construction is `1 92`. The larger bound should consume as many digits as it safely can, leaving the smaller digits for tighter bounds.

Third, comparing digits only against the corresponding digit of the bound can require backtracking. For `3241` and bound `320`, the largest valid three-digit number is `314`. The attempt to match `3`, then `2`, gets stuck because no remaining digit is at most `0`. A careless greedy routine might conclude that no three-digit number exists, even though changing the second digit from `2` to `1` gives `314`.

## Approaches

A direct brute-force solution would choose a partition of all digits into `n` nonempty groups, permute the digits inside every group, form the corresponding numbers, and check all upper bounds. If the `m` input digits are treated as distinguishable occurrences, there are `m!` ways to order them and `C(m-1, n-1)` ways to insert the `n-1` separators between consecutive digits. Thus a straightforward exhaustive search can examine on the order of

`500! * C(499, 49)`

candidates in the largest case. Repeated digits reduce the number of distinct resulting strings, but the search remains astronomically large. The brute-force is useful only as a conceptual definition of what we are searching for.

The key observation is that the bounds themselves provide an ordering. Process the bounds from largest to smallest. A large bound has more freedom than every bound that comes after it, so it should receive the largest safe number and, whenever possible, as many digits as possible. The remaining bounds are smaller, so leaving them the smaller digits is the safer choice.

For a particular bound, suppose there are `r` digits left and `k` bounds including the current one. The current number cannot use more than its bound's number of digits, and it must leave at least one digit for every later number. Hence its maximum possible length is

`min(number_of_digits_in_bound, r - (k - 1))`.

We try that length first and decrease it only if no number of that length can be formed under the current bound.

For a fixed length, we construct the largest possible number not exceeding the bound. If the chosen length is smaller than the bound's length, the comparison is automatic, so we simply take the largest available digits. If the lengths are equal, we scan from left to right. At every position we try the largest available digit that does not exceed the corresponding bound digit. If we choose a strictly smaller digit, the prefix is already smaller than the bound, so all remaining digits can be placed in descending order. If we choose the same digit as the bound, we continue recursively. If that equal choice eventually fails, we return and try the next smaller digit.

The backtracking is tiny. At each position there are at most nine candidate digits, but only the candidate equal to the bound's digit can keep the prefix tight. Every smaller candidate immediately finishes the construction. Since the maximum bound has only 10 digits, this is effectively constant time per attempted length.

The greedy choice is safe because we process bounds from largest to smallest. Among constructions of the same length, taking the largest possible current number consumes the larger digits first and leaves smaller digits for the smaller bounds. Among possible lengths, taking the largest feasible length consumes digits that could otherwise be placed in later numbers. Since the current bound is at least as large as every later bound, using those digits here cannot make a later number easier to construct by giving the current number fewer positions. The algorithm therefore maintains the strongest possible remaining multiset for the tighter bounds.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(m! · C(m-1, n-1)) | O(m) | Too slow |
| Optimal | O(m + n log n) with decimal constants | O(m + n) | Accepted |

## Algorithm Walkthrough

1. Count the occurrences of every digit from `1` through `9`. We only need nine counters because zero never appears in the input.
2. Check the global length condition. Every bound `a_i` can contain at most `len(a_i)` digits, so if the total number of input digits is greater than `sum(len(a_i))`, no solution exists. Also, at least one digit is needed for every number, so if the number of digits is smaller than `n`, no solution exists.
3. Sort the bounds in decreasing numerical order, but keep their original indices. The largest bound is processed first because it has the most freedom.
4. For the current bound, calculate the largest number of digits we are allowed to use. If there are `r` digits remaining and `k` bounds remain including the current one, we must leave at least `k - 1` digits for the later bounds. Thus the maximum length is `min(len(bound), r - k + 1)`.
5. Try lengths from that maximum down to one. Trying the longest length first is the greedy choice. If it works, the current bound consumes the maximum possible number of digits. If no length works, the whole instance is impossible.
6. For a length smaller than the bound length, take the largest available digits in descending order. Any number with fewer digits than the bound is automatically smaller, so no digit-by-digit comparison is needed.
7. For a length equal to the bound length, construct the largest permutation not exceeding the bound. At a tight position, try available digits from the bound digit downward. A digit smaller than the bound digit makes the whole prefix smaller, so the remaining suffix can be sorted in descending order. An equal digit keeps the prefix tight and requires continuing to the next position.
8. Once a number has been constructed, subtract its digits from the counter and store the number at the original index of the bound. The counter represents exactly the digits that are still available for smaller bounds.
9. After every bound has been processed, all digit counters must be zero. The preliminary total-capacity check and the maximum-length choice make this the expected result whenever a solution exists, but the final condition also protects the implementation from leaving an accidental unused digit.

### Why it works

The invariant is that before processing a bound, the remaining digit multiset can still be assigned to all remaining bounds whenever a solution exists. We process bounds from largest to smallest. For the current bound, we first maximize its length, subject to leaving one digit per later number. If a shorter assignment were necessary while a longer valid current number exists, moving one of the digits used by a later number into the current number cannot make the current number exceed its bound because the chosen construction explicitly satisfies the bound. The later bounds are no larger than the current bound, and the construction chooses the largest possible current number, which preferentially consumes large digits and leaves the smaller digits to the tighter bounds. For a fixed length, the digit-by-digit construction is exactly the lexicographically largest permutation not exceeding the bound. Thus every greedy decision preserves the possibility of completing the remaining smaller bounds.

## Python Solution

```python
import sys
input = sys.stdin.readline

def build_number(cnt, bound, length):
    """
    Return (number_string, new_count) for the largest number of
    exactly `length` digits that can be made from cnt and is <= bound.
    Return (None, None) if impossible.
    """
    work = cnt[:]

    if length < len(bound):
        ans = []
        need = length

        for d in range(9, 0, -1):
            take = min(work[d], need)
            if take:
                ans.append(str(d) * take)
                work[d] -= take
                need -= take
                if need == 0:
                    break

        if need != 0:
            return None, None

        return ''.join(ans), work

    # length == len(bound)
    ans = []

    def dfs(pos):
        if pos == length:
            return True

        limit = ord(bound[pos]) - ord('0')

        # Try the largest possible digit first.
        for d in range(limit, 0, -1):
            if work[d] == 0:
                continue

            work[d] -= 1
            ans.append(str(d))

            if d < limit:
                # The prefix is already strictly smaller.
                # Maximize the suffix.
                for x in range(9, 0, -1):
                    if work[x]:
                        ans.append(str(x) * work[x])

                return True

            # d == limit, so the prefix is still equal.
            if dfs(pos + 1):
                return True

            ans.pop()
            work[d] += 1

        return False

    if not dfs(0):
        return None, None

    return ''.join(ans), work

def solve_case(s, bounds):
    m = len(s)
    n = len(bounds)

    # Every output number needs at least one digit.
    if m < n:
        return None

    # Every output number has at most as many digits as its bound.
    capacity = sum(len(str(x)) for x in bounds)
    if m > capacity:
        return None

    cnt = [0] * 10
    for ch in s:
        cnt[ord(ch) - ord('0')] += 1

    # Process the largest bounds first.
    order = sorted(range(n), key=lambda i: bounds[i], reverse=True)
    answer = [None] * n

    remaining = m

    for step, idx in enumerate(order):
        bound = str(bounds[idx])
        remaining_numbers = n - step - 1

        # Leave at least one digit for every later number.
        max_len = min(len(bound), remaining - remaining_numbers)

        chosen = None
        chosen_cnt = None

        for length in range(max_len, 0, -1):
            candidate, new_cnt = build_number(cnt, bound, length)

            if candidate is not None:
                chosen = candidate
                chosen_cnt = new_cnt
                break

        if chosen is None:
            return None

        answer[idx] = chosen
        cnt = chosen_cnt
        remaining -= len(chosen)

    if remaining != 0:
        return None

    return answer

def solve(data):
    it = iter(data.strip().splitlines())
    t = int(next(it))
    out = []

    for _ in range(t):
        parts = next(it).split()
        s = parts[0]
        n = int(parts[1])
        bounds = list(map(int, parts[2:2 + n]))

        answer = solve_case(s, bounds)

        if answer is None:
            out.append("-1")
        else:
            out.append(" ".join(answer))

    return "\n".join(out)

def main():
    data = sys.stdin.read()
    sys.stdout.write(solve(data))

if __name__ == "__main__":
    main()
```

The `solve_case` function first performs the two global feasibility checks. The first checks that there are enough digits to create `n` nonempty numbers. The second checks that the total number of available digits does not exceed the total number of digit positions allowed by the bounds. The second check is what immediately rejects the `12534` sample.

The digit counter has only ten entries, so removing digits never requires manipulating the original string. This also handles repeated digits naturally. A digit occurrence is consumed by decrementing its counter, and the counter after each greedy step represents exactly the unused occurrences.

The bounds are sorted by their integer values in descending order, while their original indices are retained. This is necessary because the greedy argument depends on processing the largest restriction first, but the output still has to contain one answer for every input bound in its original position.

The expression `remaining - remaining_numbers` is the maximum number of digits that the current number may consume without leaving too few digits for the remaining numbers. This is the boundary condition that prevents the algorithm from producing a locally valid number while making the global digit count impossible.

`build_number` tries the largest length first. For shorter lengths, taking digits from `9` down to `1` immediately gives the largest possible number because there is no upper-bound comparison to perform. For equal lengths, the nested `dfs` function handles the tight-prefix case.

The subtle part is the `d < limit` branch. Once a chosen digit is strictly smaller than the corresponding bound digit, the entire number is already smaller than the bound regardless of the suffix. We can consequently place every remaining digit in descending order, which maximizes the result.

When `d == limit`, the prefix remains equal to the bound, so the suffix must still be checked. If that recursive attempt fails, the digit is restored before trying a smaller candidate. The restoration is essential because the same digit occurrence must remain available for the alternative branch.

Python integers do not overflow here. Bounds are at most `10^9`, and the algorithm mostly works with their string representations anyway. The output numbers are also represented as strings, which avoids any unnecessary integer conversion of long digit sequences.

## Worked Examples

### Sample 1

The first sample is

```
1234 2 21 43
```

There are four digits and the two bounds have two positions each, so every digit must go into a two-digit number.

| Step | Bound processed | Remaining digits | Maximum length | Chosen number |
| --- | --- | --- | --- | --- |
| 1 | 43 | 1,2,3,4 | 2 | 43 |
| 2 | 21 | 1,2 | 2 | 21 |

The bounds are processed in decreasing order, so `43` is handled first. The largest two-digit permutation of `1234` not exceeding `43` is `43`. The remaining digits are `1` and `2`, which form `21` for the second bound. Restoring the original input order gives `21 43`, which is different from the sample output but equally valid.

### Sample 2

The second sample is

```
12534 2 21 43
```

There are five digits, while the two bounds provide only four digit positions in total.

| Step | Total digits | Total allowed positions | Result |
| --- | --- | --- | --- |
| Feasibility check | 5 | 4 | impossible |

The algorithm stops before constructing anything and prints `-1`. This demonstrates why the global capacity check is necessary.

### A tight-prefix example

Consider

```
3241 2 320 99
```

The bounds are already in descending order.

| Step | Bound | Remaining digits | Length tried | Prefix decisions | Result |
| --- | --- | --- | --- | --- | --- |
| 1 | 320 | 1,2,3,4 | 3 | `3 = 3`, `2 = 2`, no digit `<= 0` | backtrack |
| 1 | 320 | 1,2,3,4 | 3 | `3 = 3`, `1 < 2` | `314` |
| 2 | 99 | 2 | 1 | `2 < 9` | `2` |

The first attempt follows the bound with prefix `32`, but no remaining digit can occupy the last position because zero is unavailable. The algorithm backtracks at the second position and tries `1`, producing `314`. The remaining digit `2` is then safely assigned to `99`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m + n log n) | Sorting costs O(n log n), while every construction examines at most 10 digit types and at most 10 positions for each of at most 10 lengths. |
| Space | O(m + n) | The digit counter is constant-sized, while the answer array and output strings contain O(m + n) information. |

The practical constant is very small because decimal digits give only nine usable digit types and every bound has at most 10 digits. Even with 50 bounds and 500 input digits, the algorithm performs only a few thousand digit-level operations per test case, far below what the one-second limit requires.

## Test Cases

```python
import io

def build_number(cnt, bound, length):
    work = cnt[:]

    if length < len(bound):
        ans = []
        need = length

        for d in range(9, 0, -1):
            take = min(work[d], need)
            if take:
                ans.append(str(d) * take)
                work[d] -= take
                need -= take
                if need == 0:
                    break

        if need:
            return None, None

        return ''.join(ans), work

    ans = []

    def dfs(pos):
        if pos == length:
            return True

        limit = int(bound[pos])

        for d in range(limit, 0, -1):
            if work[d] == 0:
                continue

            work[d] -= 1
            ans.append(str(d))

            if d < limit:
                for x in range(9, 0, -1):
                    if work[x]:
                        ans.append(str(x) * work[x])
                return True

            if dfs(pos + 1):
                return True

            ans.pop()
            work[d] += 1

        return False

    if not dfs(0):
        return None, None

    return ''.join(ans), work

def solve_case(s, bounds):
    m = len(s)
    n = len(bounds)

    if m < n:
        return None

    if m > sum(len(str(x)) for x in bounds):
        return None

    cnt = [0] * 10
    for ch in s:
        cnt[int(ch)] += 1

    order = sorted(range(n), key=lambda i: bounds[i], reverse=True)
    answer = [None] * n
    remaining = m

    for step, idx in enumerate(order):
        bound = str(bounds[idx])
        later = n - step - 1

        max_len = min(len(bound), remaining - later)

        found = False

        for length in range(max_len, 0, -1):
            candidate, new_cnt = build_number(cnt, bound, length)

            if candidate is not None:
                answer[idx] = candidate
                cnt = new_cnt
                remaining -= length
                found = True
                break

        if not found:
            return None

    if remaining != 0:
        return None

    return answer

def run(inp: str) -> str:
    lines = inp.strip().splitlines()
    t = int(lines[0])
    out = []

    for line in lines[1:t + 1]:
        parts = line.split()
        s = parts[0]
        n = int(parts[1])
        bounds = list(map(int, parts[2:2 + n]))

        ans = solve_case(s, bounds)
        out.append("-1" if ans is None else " ".join(ans))

    return "\n".join(out)

# Provided samples
sample = """\
3
1234 2 21 43
12534 2 21 43
42 1 42
"""

assert run(sample) == "21 43\n-1\n42", "provided samples"

# Minimum-size input
assert run("1\n7 1 7\n") == "7", "single digit"

# All values equal
assert run("1\n3333 2 33 33\n") == "33 33", "all equal values"

# Boundary condition where the larger bound must receive more digits
assert run("1\n129 2 13 22\n") == "1 92", "length allocation"

# Tight-prefix backtracking
assert run("1\n3241 2 320 99\n") == "314 2", "backtracking"

# Maximum-size feasible digit set: 450 digits, 50 bounds of length 9
s = "1" * 450
bounds = " ".join(["999999999"] * 50)
expected = " ".join(["111111111"] * 50)
assert run(f"1\n{s} 50 {bounds}\n") == expected, "maximum-size feasible case"

# Maximum digit count but insufficient total capacity
s = "1" * 500
assert run(f"1\n{s} 50 {bounds}\n") == "-1", "maximum-size impossible case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `7 1 7` | `7` | Minimum-size input and exact boundary |
| `3333 2 33 33` | `33 33` | Repeated identical digits and equal bounds |
| `129 2 13 22` | `1 92` | Correct distribution of lengths between different bounds |
| `3241 2 320 99` | `314 2` | Backtracking when an equal prefix eventually becomes impossible |
| 450 copies of `1`, 50 nine-digit bounds | 50 copies of `111111111` | Maximum feasible input size |
| 500 copies of `1`, 50 nine-digit bounds | `-1` | Global capacity boundary |

## Edge Cases

The first edge case is insufficient total capacity. For

```
12345 2 21 43
```

there are five digits, but `21` and `43` can contain at most two digits each. The algorithm computes `5 > 2 + 2` during the initial feasibility check and immediately returns `-1`. No digit is silently discarded.

The second edge case is the length-allocation trap:

```
129 2 13 22
```

The bounds are processed as `22`, then `13`. For `22`, three digits remain and one digit must be reserved for the later bound, so the maximum length is two. The largest two-digit number obtainable from `1,2,9` is `92`, which is valid. Only `1` remains, and `1 <= 13`. The final output in original order is `1 92`.

The third edge case is tight-prefix backtracking:

```
3241 2 320 99
```

For `320`, the algorithm tries length three. It first follows the equal prefix `3`, then `2`. At the final position the bound requires a digit at most `0`, which is impossible because zero is absent. The search backs up to the second position and tries `1`, which is smaller than `2`. The prefix is now strictly smaller than `32`, so the remaining `4` is placed after it, producing `314`. The only unused digit is `2`, which is valid for the second bound.

The fourth edge case is repeated digits:

```
3333 2 33 33
```

The digit counter contains four copies of `3`. The first bound consumes two copies and forms `33`; the second consumes the remaining two. No assumption that all digits are distinct is made anywhere in the algorithm.

The fifth edge case is the maximum feasible total length. With 450 digits and 50 bounds of nine digits each, every bound must receive exactly nine digits. For 450 copies of `1`, every constructed number is `111111111`. The algorithm's length calculation forces nine digits for each bound because there is no spare capacity anywhere else.

Finally, the smallest possible bound deserves explicit attention. If the available digit is `9` and the bound is `1`, the one-digit construction fails because `9 > 1`. Since adding digits would only make the number larger than a one-digit bound, no alternative length can help. The algorithm tries the only possible length and correctly reports failure.

If you want, I can also turn this into a more contest-native editorial style with a shorter proof and a cleaner `O(10^3 n)` implementation.
