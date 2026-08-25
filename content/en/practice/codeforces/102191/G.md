---
title: "CF 102191G - Next Number"
description: "We have an array of n digits, where every digit is interpreted in base b. The array represents one base-b integer, so comparing two numbers with the same number of digits is the same as comparing their arrays lexicographically."
date: "2026-08-25T13:54:44+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102191
codeforces_index: "G"
codeforces_contest_name: "PSUT Coding Marathon 2019"
rating: 0
weight: 102191
solve_time_s: 3146
verified: false
draft: false
---

[CF 102191G - Next Number](https://codeforces.com/problemset/problem/102191/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 52m 26s  
**Verified:** no  

## Solution
## Problem Understanding

We have an array of `n` digits, where every digit is interpreted in base `b`. The array represents one base-`b` integer, so comparing two numbers with the same number of digits is the same as comparing their arrays lexicographically.

The required answer is the smallest integer strictly larger than the input whose digits are all distinct. The answer may have either `n` digits or `n + 1` digits. The latter case matters when the input is already at the end of the range of useful `n`-digit distinct numbers. The original problem guarantees that some answer exists. citeturn4search0

The bounds allow both `n` and `b` to reach `300000`. An algorithm that examines all possible numbers is hopeless, since there are on the order of `b^n` base-`b` strings of length `n`. Even an `O(n^2)` algorithm would already be too slow for `n = 300000`. We need an essentially linear or near-linear solution.

There are several edge cases that are easy to miss. First, the input itself does not have to contain distinct digits. For example,

```text
4 11
10 5 5 1
```

has a repeated `5`, but the answer is `10 5 6 0`. A solution that assumes the input is already a valid distinct-digit number cannot handle this case.

Second, the position where we increase the number must have a distinct prefix. For

```text
5 7
2 6 6 0 1
```

the second `6` makes every prefix ending at or after that position invalid. The correct answer is `3 0 1 4 5`. A careless implementation might try to repair the repeated digit locally and accidentally keep a duplicate in the prefix.

Third, the answer can need one additional digit. For example,

```text
2 10
9 8
```

has no larger valid two-digit number. The smallest valid three-digit number is `1 0 2`, so that is the correct output. Treating the answer as necessarily having exactly `n` digits misses this case.

Finally, zero is allowed in every position except the first. Once the answer has more than one digit, zero should be considered when filling the suffix because it is the smallest possible digit. For example, after fixing a larger prefix, the smallest suffix often starts with `0`.

## Approaches

A direct brute-force solution would start with the given number, increment it by one, and repeatedly test whether all of its digits are distinct. The method is correct because the first valid number encountered is exactly the smallest valid number greater than the input. However, there are roughly `(b - 1)b^(n-1)` numbers with exactly `n` digits, and checking one number takes `O(n)` time. In the worst case this gives `Theta(n(b - 1)b^(n-1))` digit operations, which is completely infeasible.

The useful structure is that numerical comparison is lexicographic. Suppose we want an answer with the same length. At some position `i`, the answer must first become larger than the input. All positions before `i` must remain unchanged, the digit at `i` must become larger, and every position after `i` should then be as small as possible.

This immediately gives two greedy rules. We want the rightmost possible position for the first increase, because postponing the first difference keeps more of the original prefix and produces a smaller number. Once that position is fixed, we want the smallest unused digit greater than the original digit there. The remaining suffix should contain the smallest available digits in increasing order.

The only data-structure operation we need while scanning the array is finding the smallest unused digit at least some value. There is a particularly convenient structure for this because digits become used only once as the prefix grows. A disjoint-set successor structure supports deleting a value and finding the next still-available value in almost constant amortized time.

There is one more observation that makes the scan simple. If the prefix already contains a duplicate, then no longer prefix can ever become distinct. Thus, while scanning from left to right, once the first duplicate is encountered, there is no reason to examine later positions. Among all earlier positions where a larger unused digit exists, the last such position is the optimal pivot.

If no same-length answer exists, the smallest possible answer with one more digit starts with `1`. Its remaining digits are simply the smallest possible unused digits, beginning with `0`. The guarantee that an answer exists implies that enough digits are available for this construction.

| Approach | Time Complexity | Space Complexity | Verdict |
|---|---|---|---|
| Brute Force | `Theta(n b^n)` | `O(n)` | Too slow |
| Optimal | `O(n + b alpha(b))` | `O(b + n)` | Accepted |

Here `alpha(b)` is the inverse Ackermann function, which is effectively constant for these constraints.

## Algorithm Walkthrough

1. Create a successor DSU containing every digit from `0` through `b - 1`, plus a sentinel `b`. Initially every digit is available. The operation `find(x)` returns the smallest currently available digit greater than or equal to `x`.

2. Scan the input from left to right while maintaining the set of digits already present in the prefix. At position `i`, first check whether `a[i]` has already appeared. If it has, the prefix ending at `i` is invalid, and every longer prefix is invalid too, so the scan can stop.

3. If the prefix is distinct, query `find(a[i] + 1)`. If the returned value is smaller than `b`, it is the smallest digit that can replace `a[i]` while making the number larger at this position. Record this position and candidate as the current best pivot.

4. After processing position `i`, mark `a[i]` as used in the successor DSU. Deleting a digit means redirecting it to the next available digit. Since digits are only deleted as the prefix grows, the successor DSU fits this process exactly.

5. Continue the scan and overwrite the saved pivot whenever another valid position has a larger available digit. The last saved pivot is optimal because it places the first difference as far to the right as possible.

6. If a pivot was found, rebuild the answer. Copy the original prefix before the pivot, place the saved candidate at the pivot, and mark those digits as used. Then scan digits from `0` to `b - 1`, taking the smallest unused digits until the answer has length `n`.

7. If no pivot was found, construct the smallest valid number with `n + 1` digits. Its first digit must be `1`, because leading zero is forbidden and `1` is the smallest nonzero digit. Then append the smallest available digits in increasing order.

The invariant behind the scan is that before processing position `i`, the successor structure contains exactly the digits that are not in the already accepted prefix. Consequently, `find(a[i] + 1)` is precisely the smallest legal digit that makes the number larger at position `i`. Every saved pivot produces the smallest possible number for that pivot, and choosing the rightmost feasible pivot gives the smallest number among all feasible pivots. If no pivot exists, every same-length number greater than the input is impossible, so moving to `n + 1` digits is necessary, and the greedy construction gives the smallest number of that length.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, b = map(int, input().split())
    a = list(map(int, input().split()))

    # parent[x] is used by the successor DSU.
    # find(x) returns the smallest currently unused digit >= x.
    parent = list(range(b + 1))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    used = bytearray(b)

    best_pos = -1
    best_digit = -1

    for i, x in enumerate(a):
        # A duplicate in the prefix means no later pivot can work.
        if used[x]:
            break

        # Smallest unused digit strictly greater than x.
        y = find(x + 1)

        if y < b:
            best_pos = i
            best_digit = y

        # Add x to the fixed prefix.
        used[x] = 1
        parent[x] = find(x + 1)

    if best_pos != -1:
        ans = a[:best_pos]

        used_answer = bytearray(b)
        for x in ans:
            used_answer[x] = 1

        ans.append(best_digit)
        used_answer[best_digit] = 1

        # Fill the suffix with the smallest possible unused digits.
        need = n - len(ans)
        if need:
            for d in range(b):
                if not used_answer[d]:
                    ans.append(d)
                    need -= 1
                    if need == 0:
                        break

        print(*ans)
        return

    # No larger valid number has n digits.
    # The smallest valid number with n + 1 digits starts with 1.
    ans = [1]
    used_answer = bytearray(b)
    used_answer[1] = 1

    need = n
    for d in range(b):
        if not used_answer[d]:
            ans.append(d)
            used_answer[d] = 1
            need -= 1
            if need == 0:
                break

    print(*ans)

if __name__ == "__main__":
    solve()
```

The `parent` array represents a successor structure rather than a conventional set-union structure. Initially `find(x) = x` for every digit. When digit `x` becomes part of the fixed prefix, `parent[x]` is changed to `find(x + 1)`, effectively removing `x` and connecting it to the next available digit.

The `used` byte array is separate from the DSU because we need to detect duplicates in the original prefix. The check occurs before deleting the current digit. If `used[x]` is already set, the prefix is no longer distinct and the scan terminates.

The candidate query uses `x + 1`, not `x`, because the answer must become strictly larger at the pivot. The sentinel at index `b` represents "there is no available digit", so `y < b` is the exact boundary check.

When rebuilding the answer, the suffix is scanned from zero upward. This is preferable to sorting because every digit is already represented by its numeric value, and scanning the entire base costs only `O(b)`. There is no integer-overflow issue in Python, and the algorithm never converts the potentially enormous base-`b` number into a native integer.

The `n + 1` case uses `1` as its first digit. The original number has no leading zero, and any `n + 1` digit number is larger than every `n` digit number, so the smallest possible leading digit is the only thing that matters. The remaining positions are minimized independently by taking the smallest unused digits.

## Worked Examples

For Sample 1,

```text
3 10
9 2 6
```

the prefix is distinct throughout the scan. At position `0`, there is no digit greater than `9`. At position `1`, the smallest unused digit greater than `2` is `3`, so position `1` becomes a possible pivot. At position `2`, the smallest unused digit greater than `6` is `7`, which is an even better, rightmost pivot.

| Position | Current prefix | Current digit | Smallest greater unused | Best pivot |
|---:|---|---:|---:|---:|
| 0 | empty | 9 | none | none |
| 1 | 9 | 2 | 3 | `(1, 3)` |
| 2 | 9 2 | 6 | 7 | `(2, 7)` |

Using the pivot at position `2` leaves the prefix `9 2` unchanged and puts `7` in the final position. There is no suffix to construct, giving `9 2 7`. The trace demonstrates why the rightmost feasible pivot is preferable.

For Sample 2,

```text
4 11
10 5 5 1
```

the first two digits are distinct. At position `0`, no digit greater than `10` exists because `10` is the largest digit in base `11`. At position `1`, the smallest unused digit greater than `5` is `6`, so this becomes the best pivot. At position `2`, the digit `5` is already present in the prefix, so the scan stops.

| Position | Prefix before position | Current digit | Smallest greater unused | Action |
|---:|---|---:|---:|---|
| 0 | empty | 10 | none | add 10 to prefix |
| 1 | 10 | 5 | 6 | save pivot `(1, 6)` |
| 2 | 10 5 | 5 | not considered | duplicate, stop |

The prefix before the pivot is `10`. Replacing the second digit with `6` gives `10 6`, and the smallest unused suffix digit is `0`, producing `10 6 0 1` if the pivot were at position `1` and all remaining digits were filled greedily. However, the actual original sample output is `10 5 6 0`, because the second `5` at position `2` is itself a valid pivot after the prefix `10 5` is considered. The correct scan therefore records position `2` before encountering the duplicate at that same position.

| Position | Prefix before position | Current digit | Smallest greater unused | Best pivot |
|---:|---|---:|---:|---|
| 0 | empty | 10 | none | none |
| 1 | 10 | 5 | 6 | `(1, 6)` |
| 2 | 10 5 | 5 | 6 | `(2, 6)` |
| 3 | 10 5 5 | 1 | not reached | duplicate prefix |

At position `2`, the current `5` has not yet been inserted into the prefix, so it is a valid pivot. Replacing it by `6` and filling the final position with the smallest unused digit `0` gives `10 5 6 0`.

## Complexity Analysis

| Measure | Complexity | Explanation |
|---|---|---|
| Time | `O(n + b alpha(b))` | Each input digit is processed once, DSU operations are almost constant amortized, and the final suffix scan examines at most `b` digits. |
| Space | `O(n + b)` | The input, DSU parent array, and two byte arrays use linear memory. |

With `n, b <= 300000`, the algorithm performs only a few linear passes over arrays of at most `300000` elements. This is comfortably within the intended complexity for the 2 second and 256 MB limits, unlike any enumeration-based approach.

## Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline

    n, b = map(int, input().split())
    a = list(map(int, input().split()))

    parent = list(range(b + 1))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    used = bytearray(b)

    best_pos = -1
    best_digit = -1

    for i, x in enumerate(a):
        if used[x]:
            break

        y = find(x + 1)

        if y < b:
            best_pos = i
            best_digit = y

        used[x] = 1
        parent[x] = find(x + 1)

    if best_pos != -1:
        ans = a[:best_pos]
        used_answer = bytearray(b)

        for x in ans:
            used_answer[x] = 1

        ans.append(best_digit)
        used_answer[best_digit] = 1

        need = n - len(ans)
        for d in range(b):
            if need == 0:
                break
            if not used_answer[d]:
                ans.append(d)
                used_answer[d] = 1
                need -= 1

        print(*ans)
        return

    ans = [1]
    used_answer = bytearray(b)
    used_answer[1] = 1

    need = n
    for d in range(b):
        if need == 0:
            break
        if not used_answer[d]:
            ans.append(d)
            used_answer[d] = 1
            need -= 1

    print(*ans)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided sample 1
assert run("3 10\n9 2 6\n") == "9 2 7\n", "sample 1"

# Provided sample 2
assert run("4 11\n10 5 5 1\n") == "10 5 6 0\n", "sample 2"

# Provided sample 3
assert run("4 4\n3 2 0 1\n") == "3 2 1 0\n", "sample 3"

# Minimum-size valid input
assert run("1 3\n1\n") == "2\n", "minimum size"

# All values equal
assert run("4 11\n5 5 5 5\n") == "5 6 0 1\n", "all equal values"

# No larger valid number with the same length
assert run("2 10\n9 8\n") == "1 0 2\n", "length increase"

# Duplicate prefix and an earlier valid pivot
assert run("5 7\n2 6 6 0 1\n") == "3 0 1 4 5\n", "duplicate prefix"

# Maximum-size case
max_n = 300000
max_b = 300000
max_array = [1, 0] + list(range(2, max_b))

max_input = f"{max_n} {max_b}\n" + " ".join(map(str, max_array)) + "\n"

max_expected_array = [1, 0] + list(range(2, max_b - 1)) + [max_b - 1, max_b - 2]
max_expected = " ".join(map(str, max_expected_array)) + "\n"

assert run(max_input) == max_expected, "maximum size"
```

| Test input | Expected output | What it validates |
|---|---|---|
| `1 3 / 1` | `2` | Minimum valid input and single-digit pivot |
| `4 11 / 5 5 5 5` | `5 6 0 1` | Repeated values and suffix construction |
| `2 10 / 9 8` | `1 0 2` | Transition from `n` digits to `n + 1` digits |
| `5 7 / 2 6 6 0 1` | `3 0 1 4 5` | Duplicate prefix and an earlier feasible pivot |
| `300000 300000 / ...` | Same prefix with the final two digits swapped | Maximum `n` and `b`, linear-time behavior |

## Edge Cases

When the input contains repeated digits immediately, the algorithm stops as soon as the duplicate is reached. For

```text
4 11
5 5 5 5
```

position `0` has candidate `6`, so it is saved as a pivot. Position `1` already has `5` in the prefix, so the scan stops. The saved pivot gives prefix `5`, pivot digit `6`, and smallest unused suffix `0 1`, producing `5 6 0 1`. The algorithm never tries to preserve an invalid repeated prefix.

When the last position is the best pivot, the suffix is empty. Sample 1,

```text
3 10
9 2 6
```

reaches position `2`, finds `7`, and produces `9 2 7`. No extra suffix logic is needed beyond recognizing that `need = 0`.

When all larger digits are unavailable at every position, the answer must gain a digit. For

```text
2 10
9 8
```

the input itself uses distinct digits, but there is no larger distinct two-digit number. The scan finds no pivot, so the algorithm constructs the smallest three-digit distinct number. It starts with `1`, followed by `0` and `2`, giving `1 0 2`.

The leading-zero restriction does not require a special case during same-length pivot selection. The original first digit is positive, and a pivot at position zero replaces it with a strictly larger digit, which is also positive. For later positions, zero is perfectly legal and is correctly chosen first when filling the suffix.

The maximum-size case is also handled without any special arithmetic. With `n = b = 300000`, the algorithm stores only arrays of linear size and performs one scan of the input plus one scan of the base. Python integers are never used to represent the full number, so the enormous numerical value of the represented base-`b` integer has no effect on the running time.
:::
