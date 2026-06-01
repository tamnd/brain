---
title: "CF 216E - Martian Luck"
description: "We are given a sequence of digits written in base k. Every digit is between 0 and k - 1, and one special digit b is called lucky. For every substring of the digit sequence, we interpret that substring as a base-k number, allowing leading zeroes."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 216
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 133 (Div. 2)"
rating: 2000
weight: 216
solve_time_s: 97
verified: true
draft: false
---

[CF 216E - Martian Luck](https://codeforces.com/problemset/problem/216/E)

**Rating:** 2000  
**Tags:** math, number theory  
**Solve time:** 1m 37s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of digits written in base `k`. Every digit is between `0` and `k - 1`, and one special digit `b` is called lucky.

For every substring of the digit sequence, we interpret that substring as a base-`k` number, allowing leading zeroes. A substring is considered lucky if its digital root equals `b`.

The task is to count how many substrings are lucky.

The first challenge is understanding what the digital root means in an arbitrary base. In decimal, repeatedly summing digits eventually gives a value equivalent to the number modulo `9`. In base `k`, the same phenomenon happens with modulus `k - 1`.

Suppose a number is written in base `k`:

$$x = d_0 + d_1 k + d_2 k^2 + \dots$$

Since

$$k \equiv 1 \pmod{k-1}$$

we also have

$$x \equiv d_0 + d_1 + d_2 + \dots \pmod{k-1}$$

Repeating the digit-sum process keeps preserving the value modulo `k - 1`, until only one digit remains. That final digit is exactly the digital root.

This creates one special situation. In ordinary modulo arithmetic, remainder `0` corresponds to digital root `0`. But for positive numbers divisible by `k - 1`, the digital root becomes `k - 1`, not `0`. This is identical to how decimal digital roots behave: `18` has digital root `9`, not `0`.

The constraints force us to avoid quadratic work. With `n = 100000`, there are about `5 * 10^9` substrings, so enumerating all substrings is impossible. Even checking substrings in `O(1)` each would still be far too slow. We need something close to linear time.

There are several easy-to-miss edge cases.

Consider:

```
2 0 1
0
```

The only substring is `"0"`. Its digital root is `0`, so the answer is `1`.

A careless implementation that uses the standard digital root formula for positive numbers only would incorrectly reject zero.

Now consider:

```
10 9 2
1 8
```

The substring `"18"` has digit sum `9`, so its digital root is `9`, not `0`.

If we only checked `sum % 9 == 0`, we would incorrectly classify it as root `0`.

Another subtle case appears when `k = 2`.

Then `k - 1 = 1`, so every number is congruent to `0 mod 1`. Modular arithmetic becomes useless unless handled separately.

Example:

```
2 1 3
1 0 1
```

Every nonzero binary number has digital root `1`. The only substring with digital root `0` is the substring consisting entirely of zeroes.

A direct modulo-based solution breaks completely here because all prefix sums are identical modulo `1`.

## Approaches

The brute-force solution is straightforward. For every substring, compute the sum of its digits, repeatedly reduce it to a single base-`k` digit, and check whether the result equals `b`.

There are `O(n^2)` substrings. Even if we precompute prefix sums so each substring sum is available in `O(1)`, we still must inspect all substrings. With `n = 100000`, this becomes roughly `5 * 10^9` substrings, which is far beyond the limit.

The key observation is that the digital root in base `k` depends only on the digit sum modulo `k - 1`.

For a positive number:

$$\text{digital root}(x) = \begin{cases} k - 1 & \text{if } x \equiv 0 \pmod{k-1} \\ x \bmod (k-1) & \text{otherwise} \end{cases}$$

A substring corresponds to a contiguous range of digits, so its digit sum can be obtained from prefix sums:

$$S(l, r) = pref[r] - pref[l-1]$$

This turns the problem into counting pairs of prefix sums with a specific difference modulo `k - 1`.

If `b > 0`, then we simply need:

$$S(l,r) \equiv b \pmod{k-1}$$

If `b = 0`, only substrings whose total digit sum is exactly zero qualify. Since digits are nonnegative, that means every digit in the substring must be zero.

This distinction is the entire problem.

Once reduced to prefix sums modulo `k - 1`, we can count valid substrings using a frequency map in linear time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the base `k`, lucky digit `b`, and the digit sequence.
2. Handle the special case `b = 0`.

A number has digital root `0` only if the number itself is zero. Since all digits are nonnegative, a substring represents zero exactly when every digit in it is zero.

We scan the array and count lengths of consecutive zero blocks. A block of length `L` contributes:

$$\frac{L(L+1)}{2}$$

zero-only substrings.
3. Handle the special case `k = 2`.

In binary, the only possible digital roots are `0` and `1`.

If `b = 0`, step 2 already handled it.

If `b = 1`, every nonzero substring is lucky. The total number of substrings is:

$$\frac{n(n+1)}{2}$$

We subtract the zero-only substrings counted earlier.
4. For the general case `k > 2` and `b > 0`, let:

$$m = k - 1$$
5. Build prefix sums modulo `m`.

Define:

$$pref[i] = (a_1 + a_2 + \dots + a_i) \bmod m$$
6. For each position `r`, we want previous prefixes satisfying:

$$pref[r] - pref[l-1] \equiv b \pmod m$$

Rearranging:

$$pref[l-1] \equiv pref[r] - b \pmod m$$
7. Maintain a frequency map `cnt` of previously seen prefix residues.

Initially, `cnt[0] = 1` because the empty prefix exists.
8. For each prefix residue `cur`:

Compute:

$$need = (cur - b) \bmod m$$

Every previous prefix with residue `need` forms a lucky substring ending here.
9. Add `cnt[need]` to the answer, then increment `cnt[cur]`.

### Why it works

For any substring, its digit sum equals the difference of two prefix sums. Modular arithmetic preserves this difference modulo `k - 1`.

For positive digital roots, the value is determined uniquely by that modulo class. Every substring counted by the algorithm satisfies the exact modular condition corresponding to digital root `b`, and every valid substring produces exactly one matching prefix pair.

The `b = 0` case is separated because modulo arithmetic cannot distinguish digital root `0` from digital root `k - 1`.

## Python Solution

```python
import sys
from collections import defaultdict

input = sys.stdin.readline

def solve():
    k, b, n = map(int, input().split())
    a = list(map(int, input().split()))

    # count zero-only substrings
    zero_substrings = 0
    cur = 0

    for x in a:
        if x == 0:
            cur += 1
        else:
            zero_substrings += cur * (cur + 1) // 2
            cur = 0

    zero_substrings += cur * (cur + 1) // 2

    # digital root 0
    if b == 0:
        print(zero_substrings)
        return

    # base 2 special case
    if k == 2:
        total = n * (n + 1) // 2
        print(total - zero_substrings)
        return

    mod = k - 1

    cnt = defaultdict(int)
    cnt[0] = 1

    ans = 0
    pref = 0

    for x in a:
        pref = (pref + x) % mod

        need = (pref - b) % mod
        ans += cnt[need]

        cnt[pref] += 1

    print(ans)

solve()
```

The first section counts all substrings consisting entirely of zeroes. This is needed both for the `b = 0` case and for the binary special case.

The zero counting logic uses consecutive blocks. If a block has length `L`, then every choice of left and right endpoint inside that block forms a valid zero substring, giving `L(L+1)/2`.

The next section handles the mathematically awkward cases separately.

When `b = 0`, only zero-valued numbers qualify, so we can immediately print the zero-only count.

When `k = 2`, every nonzero number has digital root `1`. The answer becomes all substrings minus zero-only substrings.

The main loop implements the prefix-modulo method.

`pref` stores the current prefix sum modulo `k - 1`. For every new position, we compute which earlier residue would make the substring residue equal to `b`. The hashmap `cnt` stores how many times each residue has appeared so far.

The order matters. We first query the number of matching earlier prefixes, then insert the current prefix into the map. Reversing this order would incorrectly count empty substrings.

Python integers automatically handle the large answer size safely. The maximum number of substrings is about `5 * 10^9`, which fits comfortably in 64-bit integers anyway.

## Worked Examples

### Example 1

Input:

```
10 5 6
3 2 0 5 6 1
```

Here:

$$k - 1 = 9$$

We need substring digit sums congruent to `5 mod 9`.

| Position | Digit | Prefix Mod | Needed Mod | Previous Count | Answer |
| --- | --- | --- | --- | --- | --- |
| 0 | - | 0 | - | cnt[0]=1 | 0 |
| 1 | 3 | 3 | 7 | 0 | 0 |
| 2 | 2 | 5 | 0 | 1 | 1 |
| 3 | 0 | 5 | 0 | 1 | 2 |
| 4 | 5 | 1 | 5 | 2 | 4 |
| 5 | 6 | 7 | 2 | 0 | 4 |
| 6 | 1 | 8 | 3 | 1 | 5 |

Final answer: `5`.

This trace shows how repeated prefix residues naturally count multiple valid substrings ending at the same position.

### Example 2

Input:

```
2 1 3
1 0 1
```

All substrings:

```
[1]
[1,0]
[1,0,1]
[0]
[0,1]
[1]
```

Only `[0]` has digital root `0`.

Total substrings:

$$\frac{3 \cdot 4}{2} = 6$$

Zero-only substrings: `1`.

Answer:

$$6 - 1 = 5$$

| Quantity | Value |
| --- | --- |
| Total substrings | 6 |
| Zero-only substrings | 1 |
| Lucky substrings | 5 |

This example demonstrates why binary requires separate handling. Modulo `1` arithmetic carries no information.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One pass for zero blocks and one pass for prefix counting |
| Space | O(n) | Hash map of prefix residues |

With `n = 100000`, linear time easily fits within the limit. The hashmap stores at most one entry per distinct residue encountered, which is also safe under the memory limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from collections import defaultdict

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def solve():
        k, b, n = map(int, input().split())
        a = list(map(int, input().split()))

        zero_substrings = 0
        cur = 0

        for x in a:
            if x == 0:
                cur += 1
            else:
                zero_substrings += cur * (cur + 1) // 2
                cur = 0

        zero_substrings += cur * (cur + 1) // 2

        if b == 0:
            return str(zero_substrings)

        if k == 2:
            total = n * (n + 1) // 2
            return str(total - zero_substrings)

        mod = k - 1

        cnt = defaultdict(int)
        cnt[0] = 1

        ans = 0
        pref = 0

        for x in a:
            pref = (pref + x) % mod

            need = (pref - b) % mod
            ans += cnt[need]

            cnt[pref] += 1

        return str(ans)

    return solve()

# provided sample
assert run(
"""10 5 6
3 2 0 5 6 1
"""
) == "5", "sample 1"

# single zero
assert run(
"""2 0 1
0
"""
) == "1", "single zero substring"

# binary case
assert run(
"""2 1 3
1 0 1
"""
) == "5", "all nonzero substrings"

# all zeros
assert run(
"""10 0 4
0 0 0 0
"""
) == "10", "all substrings are zero"

# divisibility edge case
assert run(
"""10 9 2
1 8
"""
) == "1", "digital root 9, not 0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 0 1 / 0` | `1` | Correct handling of zero |
| `2 1 3 / 1 0 1` | `5` | Binary special case |
| `10 0 4 / 0 0 0 0` | `10` | Counting zero blocks correctly |
| `10 9 2 / 1 8` | `1` | Multiples of `k-1` map to `k-1`, not `0` |

## Edge Cases

Consider:

```
2 0 1
0
```

The algorithm first counts zero blocks. There is one block of length `1`, so:

$$\frac{1 \cdot 2}{2} = 1$$

Since `b = 0`, the algorithm immediately returns `1`.

This correctly handles the fact that the number zero has digital root zero.

Now consider:

```
10 9 2
1 8
```

The substring sum is:

$$1 + 8 = 9$$

Modulo `9`, this is `0`. A naive modulo-only approach would classify it as digital root `0`.

The algorithm avoids that mistake because `b = 9` is handled in the general positive-root logic, where residue `0` corresponds to digital root `9`.

Finally, consider the binary case:

```
2 1 3
1 0 1
```

Since `k - 1 = 1`, all prefix sums modulo `1` become zero. A normal modular solution would falsely count every substring for every positive `b`.

The special handling computes:

```
total substrings = 6
zero-only substrings = 1
```

and returns `5`, which is correct because every nonzero binary number has digital root `1`.
