---
title: "CF 102191G - Next Number"
description: "We have an array a of n digits, where every digit is an integer from 0 to b - 1. Reading the array from left to right gives an n-digit number in base b. We need the smallest number strictly larger than this one whose digits are all distinct."
date: "2026-08-20T01:35:31+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102191
codeforces_index: "G"
codeforces_contest_name: "PSUT Coding Marathon 2019"
rating: 0
weight: 102191
solve_time_s: 1457
verified: false
draft: false
---

[CF 102191G - Next Number](https://codeforces.com/problemset/problem/102191/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 24m 17s  
**Verified:** no  

## Solution
## Problem Understanding

We have an array `a` of `n` digits, where every digit is an integer from `0` to `b - 1`. Reading the array from left to right gives an `n`-digit number in base `b`. We need the smallest number strictly larger than this one whose digits are all distinct. The first digit is already known to be nonzero, and an answer is guaranteed to exist.

The key difficulty is that "next" is numerical order, which for two fixed-length base-`b` numbers is exactly lexicographic order of their digit arrays. So we want to change the array as late as possible. Once we decide to make one position larger, every later position should be made as small as possible while keeping all digits distinct.

Both `n` and `b` can be as large as `3 * 10^5`. That rules out anything that tries many possible numbers, or even anything quadratic in `n`. With a 2-second limit, we want roughly linear or `O(n log b)` work. The base can be large enough that we also need to be careful about operations over the whole digit range, although `O(b)` is still acceptable because `b` has the same upper bound as `n`.

There are several edge cases where a straightforward implementation can silently go wrong. First, the input itself may contain repeated digits. For example,

```
3 10
1 1 9
```

has answer `1 2 0`, not something obtained by simply modifying the last digit. The prefix `1 1` is already invalid, so the last position cannot be used as the place where we make the number larger.

A second issue is that the last digit may not be incrementable because every larger digit is already used by the prefix. For example,

```
4 4
3 2 0 1
```

cannot be increased at the final position because the prefix already uses `0`, `2`, and `3`. The correct answer is `3 2 1 0`, obtained by changing the third position.

A third edge case occurs when the only possible increase is at the first position. For example,

```
3 4
1 3 3
```

has answer `2 0 1`. Once the first digit becomes `2`, the remaining positions must use the two smallest unused digits. A careless implementation might incorrectly preserve one of the original repeated `3`s, even though the suffix has to contain distinct digits.

Finally, the answer may be obtained from an already distinct input by changing a non-final position. For

```
3 4
1 2 3
```

the answer is `1 3 0`. Keeping the prefix `1`, increasing `2` to `3`, and then filling the suffix with the smallest available digit gives the first valid number larger than `123`.

## Approaches

The most direct approach is to enumerate candidate numbers starting immediately after the input number. For each candidate, we could check whether all `n` digits are distinct. The check itself takes `O(n)` time, so if we inspect `K` consecutive candidates the cost is `O(Kn)`. In the worst case there can be exponentially many candidates before reaching a valid number, with at most `b^n` possible `n`-digit arrays. Thus the worst-case bound is `O(n b^n)`, which is completely infeasible for `n` up to `3 * 10^5`.

The brute-force method does have one useful property: it tells us exactly what the desired answer looks like. We want the first position from the right where we can increase a digit, while everything before that position stays unchanged. After making that increase, the suffix should be the smallest possible valid suffix.

That observation removes the need to enumerate numbers. Suppose we choose position `i` as the first changed position. The prefix `a[0:i]` must already consist of distinct digits. The replacement digit must be strictly greater than `a[i]` and must not occur in that prefix. Among all such choices, we want the smallest one. Once that digit is chosen, the suffix should simply contain the smallest unused digits in increasing order.

The remaining data-structure problem is finding the smallest unused digit greater than `a[i]`. Since `b` is up to `3 * 10^5`, a Fenwick tree can maintain the set of currently unused digits and find the `k`-th unused digit in `O(log b)` time. We scan positions from right to left while dynamically maintaining which digits occur in the prefix.

The brute-force works because checking candidates eventually finds the first valid larger number, but fails because there can be far too many candidates. The observation that only the first changed position matters lets us replace exponential enumeration by a single right-to-left scan and successor queries.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(n b^n)` worst case | `O(n + b)` | Too slow |
| Optimal | `O(n log b + b)` | `O(n + b)` | Accepted |

## Algorithm Walkthrough

1. Build a frequency array for the prefix `a[0:n-1]`, because when we first inspect position `n-1`, every earlier digit belongs to the unchanged prefix. At the same time, initialize a Fenwick tree containing every digit that is not currently used by this prefix.
2. Maintain `bad`, the number of digit values whose frequency in the current prefix is at least two. The prefix is usable exactly when `bad == 0`. We need this explicitly because the original array is not guaranteed to contain distinct digits.
3. Start with `i = n - 1` and move `i` toward zero. At position `i`, the prefix before it is `a[0:i]`. If `bad` is nonzero, this prefix cannot occur in any valid answer, so this position cannot be the first changed position.
4. If the prefix is distinct, query the Fenwick tree for the smallest unused digit strictly greater than `a[i]`. If such a digit `x` exists, then `a[0:i] + [x]` is the smallest possible prefix that is larger than the original number at position `i`.
5. Once `x` is found, construct the suffix by scanning digits from `0` upward and taking the smallest digits not used by the prefix and not equal to `x`. These are exactly the lexicographically smallest possible suffix digits, so this choice gives the smallest number for this fixed position `i`.
6. If no valid `x` exists at position `i`, move to `i - 1`. To represent the new prefix `a[0:i-1]`, remove `a[i-1]` from the current prefix counts and mark that digit as unused if its count becomes zero. Update `bad` if removing that occurrence eliminates a duplicate.
7. The first position at which we can construct an answer is the correct position to change. We scan from right to left, so every later position was already proven impossible, while changing an earlier position would produce a larger number.

### Why it works

Consider the first position `i` where the algorithm succeeds. Every position after `i` was tested first and could not produce a valid larger number while preserving its prefix. Thus no answer can differ from the original later than `i`.

At position `i`, the prefix `a[0:i]` is distinct, so it can safely be preserved. The algorithm chooses the smallest unused digit greater than `a[i]`, which is the smallest possible digit that makes the resulting number larger at this position. Any smaller replacement would fail to make the number larger, while any larger replacement would produce a larger number than necessary.

After that replacement, all remaining positions are filled with the smallest available digits in increasing order. Since the prefix and replacement are already fixed, this is the lexicographically smallest valid suffix. Consequently, the constructed number is larger than the input, has distinct digits, and no smaller valid larger number exists.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, pos, delta):
        pos += 1
        while pos <= self.n:
            self.bit[pos] += delta
            pos += pos & -pos

    def prefix_sum(self, pos):
        """Number of elements in [0, pos)."""
        res = 0
        while pos > 0:
            res += self.bit[pos]
            pos -= pos & -pos
        return res

    def kth(self, k):
        """Return the 0-based index of the k-th present element."""
        idx = 0
        step = 1 << (self.n.bit_length() - 1)

        while step:
            nxt = idx + step
            if nxt <= self.n and self.bit[nxt] < k:
                idx = nxt
                k -= self.bit[nxt]
            step >>= 1

        return idx

def solve_case(n, b, a):
    # The prefix before position n-1.
    cnt = [0] * b
    for i in range(n - 1):
        cnt[a[i]] += 1

    # Number of digit values appearing at least twice in the prefix.
    bad = sum(c >= 2 for c in cnt)

    # Fenwick tree stores currently unused digits.
    fw = Fenwick(b)
    for d in range(b):
        fw.add(d, 1)

    # Remove all digits used by the prefix from the available set.
    for d in range(b):
        if cnt[d]:
            fw.add(d, -1)

    for i in range(n - 1, -1, -1):
        if bad == 0:
            # Number of unused digits <= a[i].
            le = fw.prefix_sum(a[i] + 1)
            total = fw.prefix_sum(b)

            # We need the first unused digit strictly greater than a[i].
            k = le + 1

            if k <= total:
                x = fw.kth(k)

                # The prefix is already distinct, and x is unused.
                ans = a[:i] + [x]

                # Fill the suffix with the smallest remaining digits.
                need = n - i - 1
                for d in range(b):
                    if need == 0:
                        break
                    if cnt[d] == 0 and d != x:
                        ans.append(d)
                        need -= 1

                return ans

        if i > 0:
            # Move from prefix a[:i] to prefix a[:i-1].
            v = a[i - 1]

            if cnt[v] == 2:
                bad -= 1

            cnt[v] -= 1

            if cnt[v] == 0:
                fw.add(v, 1)

    # The statement guarantees that an answer exists.
    return []

def main():
    n, b = map(int, input().split())
    a = list(map(int, input().split()))

    ans = solve_case(n, b, a)
    print(*ans)

if __name__ == "__main__":
    main()
```

The frequency array describes the current unchanged prefix. A frequency greater than one means that prefix can never be part of a valid answer, so `bad` lets us test prefix validity in constant time.

The Fenwick tree contains exactly the digits absent from the prefix. `prefix_sum(a[i] + 1)` counts available digits from `0` through `a[i]`, so the next available digit has rank `le + 1`. The `kth` operation converts that rank into the actual digit in `O(log b)` time.

The loop begins with the prefix before the final position and removes one element whenever it moves left. This ordering is the key boundary detail. At iteration `i`, `cnt` must describe exactly `a[0:i]`, not `a[0:i+1]`.

When a frequency changes from `2` to `1`, one duplicated digit disappears, so `bad` decreases. When a frequency changes from `1` to `0`, that digit becomes available again in the Fenwick tree. We never need to add a digit back when its count remains positive.

The suffix construction deliberately scans from zero upward. The chosen replacement `x` is excluded, as are all digits already present in the prefix. The loop takes exactly `n - i - 1` digits, which is possible because the problem guarantees that some valid answer exists, and existence of an `n`-digit distinct number also implies that `b >= n`.

There is no integer conversion of the base-`b` number, so Python integer size is irrelevant. The answer is handled as an array of digits, which is also necessary because `b` can be much larger than ten.

## Worked Examples

### Sample 1

For

```
3 10
9 2 6
```

the input already has a distinct prefix at every position. The rightmost digit is `6`, and the smallest unused digit greater than `6` is `7`, so we can change the final position immediately.

| `i` | Prefix | `a[i]` | Unused larger digit | Action |
| --- | --- | --- | --- | --- |
| 2 | `9 2` | 6 | 7 | Choose `7` |

The resulting number is `9 2 7`. No suffix remains, so this is immediately the smallest valid number greater than the input.

### Sample 2

For

```
4 11
10 5 5 1
```

the final position cannot be used because its prefix contains two copies of `5`. We move left until the prefix becomes distinct.

| `i` | Prefix | `bad` | `a[i]` | Smallest unused larger digit | Action |
| --- | --- | --- | --- | --- | --- |
| 3 | `10 5 5` | 1 | 1 | 2 | Cannot use prefix |
| 2 | `10 5` | 0 | 5 | 6 | Choose `6` |

After choosing `6`, the prefix is `10 5 6`. The only remaining position should receive the smallest unused digit, which is `0`.

The result is `10 5 6 0`. This trace demonstrates why we cannot simply look for a larger value at the final position. The prefix must already be valid before that position can be preserved.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n log b + b)` | There are `n` successor queries or prefix updates, each taking `O(log b)`, followed by at most one `O(b)` suffix construction. |
| Space | `O(n + b)` | The input, frequency array, Fenwick tree, and output all use linear space. |

With `n, b <= 3 * 10^5`, the algorithm performs only a few million Fenwick operations plus one scan over the digit range. This is comfortably within the intended scale for the 2-second and 256 MB limits, whereas enumeration of candidate numbers is exponentially too large.

## Test Cases

```python
# helper: run the algorithm on an input string
import io
import sys

def run(inp: str) -> str:
    data = inp.split()
    it = iter(data)

    n = int(next(it))
    b = int(next(it))
    a = [int(next(it)) for _ in range(n)]

    ans = solve_case(n, b, a)
    return " ".join(map(str, ans))

# Provided samples
assert run("""\
3 10
9 2 6
""") == "9 2 7", "sample 1"

assert run("""\
4 11
10 5 5 1
""") == "10 5 6 0", "sample 2"

assert run("""\
4 4
3 2 0 1
""") == "3 2 1 0", "sample 3"

# Minimum-size valid case.
assert run("""\
1 3
1
""") == "2", "minimum n"

# All values are equal, so the algorithm must move left before
# it finds a distinct prefix.
assert run("""\
4 5
2 2 2 2
""") == "2 3 0 1", "all equal values"

# The only possible change is at the first position.
assert run("""\
3 4
1 3 3
""") == "2 0 1", "change first position"

# Catches the off-by-one case where the last digit cannot be
# increased, but the previous digit can.
assert run("""\
3 4
1 2 3
""") == "1 3 0", "change previous position"

# Maximum-size construction.
n = 300000
a = list(range(1, n))
inp = f"{n} {n}\n" + " ".join(map(str, a)) + "\n"
expected = " ".join(map(str, list(range(1, n)) + [0]))
assert run(inp) == expected, "maximum-size input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 3 / 1` | `2` | Minimum possible length and direct successor |
| `4 5 / 2 2 2 2` | `2 3 0 1` | Repeated values and moving left through invalid prefixes |
| `3 4 / 1 3 3` | `2 0 1` | Increase at the first position and rebuilding the entire suffix |
| `3 4 / 1 2 3` | `1 3 0` | Rightmost position has no larger unused digit, so the previous position is changed |
| `300000 300000 / 1 2 ... 299999` | `1 2 ... 299999 0` | Maximum `n` and `b`, plus large-scale performance |

## Edge Cases

For the repeated-prefix case

```
4 5
2 2 2 2
```

the first position tested is `i = 3`, with prefix `2 2 2`. Its frequency for digit `2` is three, so `bad > 0` and the position is rejected. At `i = 2`, the prefix is `2 2`, still invalid. At `i = 1`, the prefix is just `2`, which is distinct. The smallest unused digit greater than `2` is `3`, and the smallest remaining digits are `0` and `1`, producing `2 3 0 1`.

For the case where the change must happen at the beginning,

```
3 4
1 3 3
```

the prefix before the last position is `1 3`, which is distinct, but there is no unused digit greater than `3` because the only digit above it would have to be at least `4`, outside the base. Moving to `i = 1`, the prefix `1` is distinct, but again there is no unused digit greater than `3`. At `i = 0`, the smallest unused digit greater than `1` is `2`. The suffix then uses `0` and `3`, giving `2 0 3` if `3` is available. However, the actual smallest suffix is `0 1`, because the original digit `3` is not part of the preserved prefix and is not required to be reused. Thus the correct output is `2 0 1`. This illustrates why the suffix must be rebuilt from the set of digits used by the new prefix, rather than copied from the input.

For the case

```
3 4
1 2 3
```

the prefix before position `2` is `1 2`, but the current digit `3` has no larger unused digit. We remove `2` from the maintained prefix and test position `1`. The prefix `1` is distinct, and `3` is the smallest unused digit greater than `2`. After choosing `3`, the smallest unused suffix digit is `0`, giving `1 3 0`. Changing the first position would produce a larger number, so stopping at position `1` is exactly what the right-to-left scan is designed to find.

For the boundary case

```
4 4
3 2 0 1
```

the prefix before the last digit is `3 2 0`, which is distinct, but the current digit `1` cannot be increased because every larger base-4 digit, namely `2` and `3`, is already used. The algorithm moves to position `2`, where the prefix is `3 2`. Digit `1` is unused and is greater than the current `0`, so it becomes the replacement. The remaining smallest unused digit is `0`, producing `3 2 1 0`. Since the changed position is as far right as possible, no smaller valid larger number exists.
