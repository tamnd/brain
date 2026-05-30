---
title: "CF 452F - Permutation"
description: "The permutation contains every value from 1 to n exactly once. We need to determine whether there exist two distinct values a and b such that their arithmetic mean $$frac{a+b}{2}$$ appears somewhere between them in the permutation order."
date: "2026-05-30T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "divide-and-conquer", "hashing"]
categories: ["algorithms"]
codeforces_contest: 452
codeforces_index: "F"
codeforces_contest_name: "MemSQL Start[c]UP 2.0 - Round 1"
rating: 2700
weight: 452
solve_time_s: 157
verified: false
draft: false
---

[CF 452F - Permutation](https://codeforces.com/problemset/problem/452/F)

**Rating:** 2700  
**Tags:** data structures, divide and conquer, hashing  
**Solve time:** 2m 37s  
**Verified:** no  

## Solution
## Problem Understanding

The permutation contains every value from `1` to `n` exactly once.

We need to determine whether there exist two distinct values `a` and `b` such that their arithmetic mean

$$\frac{a+b}{2}$$

appears somewhere between them in the permutation order.

Since the mean must itself be an integer in the permutation, `a` and `b` must have the same parity. If we define

$$m = \frac{a+b}{2},$$

then the three values form an arithmetic progression

$$m-d,\; m,\; m+d.$$

The condition from the statement says that the position of `m` lies strictly between the positions of `m-d` and `m+d`.

So the problem is really asking whether there exists an arithmetic progression of length three in value space whose middle value is also the middle element in permutation order.

The constraint `n ≤ 300000` is the key difficulty. A quadratic scan over all possible centers and distances would require roughly

$$\sum_{m=1}^{n} O(\min(m,n-m))$$

checks, which is about `O(n²)`. With `n = 300000`, that means tens of billions of operations, completely impossible within a one second limit.

The solution needs something close to `O(n log n)`.

A subtle edge case appears when the middle value is very close to one of the boundaries.

Example:

```
3
2 1 3
```

For center value `1`, there are no symmetric values `1-d` and `1+d`. A careless implementation that does not handle empty ranges correctly may incorrectly report a match. The correct answer is:

```
NO
```

Another easy mistake is checking only one ordering of the endpoints.

Example:

```
3
3 2 1
```

The value `2` is between `1` and `3` in the permutation even though the larger endpoint appears first. The correct answer is:

```
YES
```

A third trap is treating the problem as "find any arithmetic progression in the values".

Example:

```
5
1 2 3 4 5
```

The values `1,2,3` form an arithmetic progression and `2` is between them in the permutation, so the answer is:

```
YES
```

But if we reorder them:

```
5
2 1 3 4 5
```

The same values still form an arithmetic progression, yet `2` is not between `1` and `3` anymore. The permutation positions matter just as much as the values themselves.

## Approaches

The most direct solution is to choose every possible middle value `m`, then try every valid distance `d`.

For each pair `(m-d, m+d)`, we look at their positions in the permutation and check whether the position of `m` lies between them.

This works because every valid answer corresponds to exactly such a triple.

The problem is the running time. A middle value near the center of the range has roughly `n/2` possible distances. Summed over all centers, the total work becomes `O(n²)`.

We need to exploit more structure.

Suppose we process the permutation from left to right.

At some moment we are standing on value `x`.

Every value already processed lies to the left of `x` in the permutation.

Every value not yet processed lies to the right of `x`.

Let us build a binary array over the value axis:

```
0 = already processed
1 = not processed yet
```

Initially every position contains `1`.

When we arrive at value `x`, we have not updated `x` yet, so `x` still belongs to the right side.

Now consider symmetric values around `x`:

```
x-d and x+d
```

If their bits are different, then one of them has already appeared and the other has not.

That means one endpoint lies to the left of `x` in the permutation and the other lies to the right.

Exactly the condition we need.

So for a fixed center `x`, the answer is YES if and only if there exists some distance `d` such that

```
bit[x-d] != bit[x+d]
```

Look at what this means globally.

The segment

```
[x-r, x+r]
```

where

```
r = min(x-1, n-x)
```

must be symmetric around `x`.

If every symmetric pair is equal, the segment is a palindrome.

If some symmetric pair differs, the segment is not a palindrome, and we have found a valid arithmetic progression.

The entire problem becomes:

1. Maintain a binary array.
2. Perform point updates `1 -> 0`.
3. For each value `x`, check whether a centered interval is a palindrome.

This is a classic rolling-hash task. A segment tree can maintain forward and reverse polynomial hashes under point updates. An interval is a palindrome exactly when its forward and reverse hashes are equal.

That gives `O(log n)` per query and update.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Segment Tree + Rolling Hash | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Create a binary array of length `n` where every value initially equals `1`.

This represents that every value is still on the right side of the current scan position.
2. Build a segment tree over this binary array.

Each node stores:

- forward hash of the segment
- reverse hash of the segment
- segment length
3. Process the permutation from left to right.

Let the current value be `x`.
4. Compute

$$r = \min(x-1,\; n-x).$$

Only values within this radius have symmetric partners around `x`.
5. Query the interval

$$[x-r,\; x+r].$$

Obtain its forward and reverse hashes.
6. If the hashes are different, the interval is not a palindrome.

Then some pair `x-d` and `x+d` belongs to opposite sides of the current position in the permutation. The required configuration exists, so print `"YES"`.
7. After the check, update position `x` from `1` to `0`.

From now on, value `x` belongs to the left side for future centers.
8. If the entire permutation is processed without finding a non-palindromic interval, print `"NO"`.

### Why it works

At the moment we process value `x`, every value already seen lies left of `x` in the permutation, and every unseen value lies right of `x`.

For any distance `d`, the pair `(x-d, x+d)` contributes one symmetric pair in the binary array.

If their bits differ, one endpoint is left of `x` and the other is right of `x`. Thus the position of `x` lies between the positions of `x-d` and `x+d`, producing a valid arithmetic progression.

If all symmetric pairs are equal, every endpoint pair lies on the same side of `x`, so no arithmetic progression centered at `x` satisfies the condition.

A palindrome check over the centered interval is exactly checking whether all symmetric pairs are equal. Hence the algorithm reports YES exactly when a valid triple exists.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD1 = 1000000007
MOD2 = 1000000009
BASE = 911382323

def solve():
    n = int(input())
    p = list(map(int, input().split()))

    pw1 = [1] * (n + 1)
    pw2 = [1] * (n + 1)

    for i in range(1, n + 1):
        pw1[i] = (pw1[i - 1] * BASE) % MOD1
        pw2[i] = (pw2[i - 1] * BASE) % MOD2

    size = 4 * n + 5

    fh1 = [0] * size
    fh2 = [0] * size
    rh1 = [0] * size
    rh2 = [0] * size
    seg_len = [0] * size

    def pull(idx):
        left = idx * 2
        right = left + 1

        llen = seg_len[left]
        rlen = seg_len[right]

        seg_len[idx] = llen + rlen

        fh1[idx] = (fh1[left] * pw1[rlen] + fh1[right]) % MOD1
        fh2[idx] = (fh2[left] * pw2[rlen] + fh2[right]) % MOD2

        rh1[idx] = (rh1[right] * pw1[llen] + rh1[left]) % MOD1
        rh2[idx] = (rh2[right] * pw2[llen] + rh2[left]) % MOD2

    def build(idx, l, r):
        seg_len[idx] = r - l + 1

        if l == r:
            fh1[idx] = fh2[idx] = 1
            rh1[idx] = rh2[idx] = 1
            return

        mid = (l + r) // 2
        build(idx * 2, l, mid)
        build(idx * 2 + 1, mid + 1, r)
        pull(idx)

    def update(idx, l, r, pos):
        if l == r:
            fh1[idx] = fh2[idx] = 0
            rh1[idx] = rh2[idx] = 0
            return

        mid = (l + r) // 2

        if pos <= mid:
            update(idx * 2, l, mid, pos)
        else:
            update(idx * 2 + 1, mid + 1, r, pos)

        pull(idx)

    def merge(a, b):
        if a[4] == 0:
            return b
        if b[4] == 0:
            return a

        len_a = a[4]
        len_b = b[4]

        return (
            (a[0] * pw1[len_b] + b[0]) % MOD1,
            (a[1] * pw2[len_b] + b[1]) % MOD2,
            (b[2] * pw1[len_a] + a[2]) % MOD1,
            (b[3] * pw2[len_a] + a[3]) % MOD2,
            len_a + len_b
        )

    def query(idx, l, r, ql, qr):
        if ql <= l and r <= qr:
            return (
                fh1[idx],
                fh2[idx],
                rh1[idx],
                rh2[idx],
                seg_len[idx]
            )

        mid = (l + r) // 2

        if qr <= mid:
            return query(idx * 2, l, mid, ql, qr)

        if ql > mid:
            return query(idx * 2 + 1, mid + 1, r, ql, qr)

        left_part = query(idx * 2, l, mid, ql, qr)
        right_part = query(idx * 2 + 1, mid + 1, r, ql, qr)

        return merge(left_part, right_part)

    build(1, 1, n)

    for x in p:
        radius = min(x - 1, n - x)
        L = x - radius
        R = x + radius

        res = query(1, 1, n, L, R)

        if res[0] != res[2] or res[1] != res[3]:
            print("YES")
            return

        update(1, 1, n, x)

    print("NO")

solve()
```

The segment tree stores forward and reverse hashes simultaneously. When two child segments are merged, the forward hash behaves exactly like ordinary polynomial hashing, while the reverse hash concatenates the children in the opposite order.

The query function returns both hashes for any interval. If the forward and reverse hashes match under both moduli, the interval is a palindrome.

One implementation detail that is easy to get wrong is the timing of the update. The palindrome check must happen before changing the current value from `1` to `0`. At that moment the current value still belongs to the right side, which matches the interpretation used in the proof.

Another subtle point is the radius computation. We only compare symmetric pairs that actually exist. Values near `1` or `n` have fewer valid distances, so the interval must be clipped using

$$\min(x-1,\; n-x).$$

## Worked Examples

### Example 1

Input:

```
4
1 3 4 2
```

Processing state:

| Current value | Binary array before check | Queried interval | Palindrome? |
| --- | --- | --- | --- |
| 1 | 1111 | [1,1] | Yes |
| 3 | 0111 | [2,4] | Yes |
| 4 | 0101 | [4,4] | Yes |
| 2 | 0100 | [1,3] | Yes |

No interval ever becomes non-palindromic, so the answer is:

```
NO
```

This trace shows that every symmetric value pair around each center remains on the same side of the center in permutation order.

### Example 2

Input:

```
5
1 5 2 4 3
```

Processing state:

| Current value | Binary array before check | Queried interval | Palindrome? |
| --- | --- | --- | --- |
| 1 | 11111 | [1,1] | Yes |
| 5 | 01111 | [5,5] | Yes |
| 2 | 01110 | [1,3] | No |

At value `2`, the interval `[1,3]` is:

```
0 1 1
```

Its symmetric positions differ:

```
value 1 -> 0
value 3 -> 1
```

One endpoint is left of `2` and the other is right of `2`.

That corresponds to the arithmetic progression:

```
1, 2, 3
```

so the answer is:

```
YES
```

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | One range query and one point update per value |
| Space | O(n) | Segment tree and power arrays |

With `n = 300000`, `O(n log n)` is roughly a few million segment tree operations, which comfortably fits within the time limit. The memory usage is linear and well below the available 256 MB.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    MOD1 = 1000000007
    MOD2 = 1000000009
    BASE = 911382323

    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    out = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = out

    n = int(input())
    p = list(map(int, input().split()))

    pw1 = [1] * (n + 1)
    pw2 = [1] * (n + 1)

    for i in range(1, n + 1):
        pw1[i] = (pw1[i - 1] * BASE) % MOD1
        pw2[i] = (pw2[i - 1] * BASE) % MOD2

    size = 4 * n + 5

    fh1 = [0] * size
    fh2 = [0] * size
    rh1 = [0] * size
    rh2 = [0] * size
    seg_len = [0] * size

    def pull(idx):
        l = idx * 2
        r = l + 1

        llen = seg_len[l]
        rlen = seg_len[r]

        seg_len[idx] = llen + rlen

        fh1[idx] = (fh1[l] * pw1[rlen] + fh1[r]) % MOD1
        fh2[idx] = (fh2[l] * pw2[rlen] + fh2[r]) % MOD2

        rh1[idx] = (rh1[r] * pw1[llen] + rh1[l]) % MOD1
        rh2[idx] = (rh2[r] * pw2[llen] + rh2[l]) % MOD2

    def build(idx, l, r):
        seg_len[idx] = r - l + 1

        if l == r:
            fh1[idx] = fh2[idx] = 1
            rh1[idx] = rh2[idx] = 1
            return

        m = (l + r) // 2
        build(idx * 2, l, m)
        build(idx * 2 + 1, m + 1, r)
        pull(idx)

    def update(idx, l, r, pos):
        if l == r:
            fh1[idx] = fh2[idx] = 0
            rh1[idx] = rh2[idx] = 0
            return

        m = (l + r) // 2

        if pos <= m:
            update(idx * 2, l, m, pos)
        else:
            update(idx * 2 + 1, m + 1, r, pos)

        pull(idx)

    def merge(a, b):
        if a[4] == 0:
            return b
        if b[4] == 0:
            return a

        la = a[4]
        lb = b[4]

        return (
            (a[0] * pw1[lb] + b[0]) % MOD1,
            (a[1] * pw2[lb] + b[1]) % MOD2,
            (b[2] * pw1[la] + a[2]) % MOD1,
            (b[3] * pw2[la] + a[3]) % MOD2,
            la + lb
        )

    def query(idx, l, r, ql, qr):
        if ql <= l and r <= qr:
            return (fh1[idx], fh2[idx], rh1[idx], rh2[idx], seg_len[idx])

        m = (l + r) // 2

        if qr <= m:
            return query(idx * 2, l, m, ql, qr)

        if ql > m:
            return query(idx * 2 + 1, m + 1, r, ql, qr)

        return merge(
            query(idx * 2, l, m, ql, qr),
            query(idx * 2 + 1, m + 1, r, ql, qr)
        )

    build(1, 1, n)

    ans = "NO"

    for x in p:
        r = min(x - 1, n - x)
        res = query(1, 1, n, x - r, x + r)

        if res[0] != res[2] or res[1] != res[3]:
            ans = "YES"
            break

        update(1, 1, n, x)

    print(ans)

    sys.stdout = old_stdout
    return out.getvalue()

# provided samples
assert run("4\n1 3 4 2\n") == "NO\n", "sample 1"
assert run("5\n1 5 2 4 3\n") == "YES\n", "sample 2"

# custom cases
assert run("1\n1\n") == "NO\n", "minimum size"
assert run("3\n1 2 3\n") == "YES\n", "simple progression"
assert run("3\n2 1 3\n") == "NO\n", "center not between endpoints"
assert run("5\n5 4 3 2 1\n") == "YES\n", "reverse order"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1` | `NO` | Smallest possible permutation |
| `1 2 3` | `YES` | Direct arithmetic progression |
| `2 1 3` | `NO` | Same values but wrong position ordering |
| `5 4 3 2 1` | `YES` | Endpoint order can be reversed |

## Edge Cases

Consider:

```
1
1
```

The only value is `1`. Its radius is zero, so the queried interval is just `[1,1]`. A single character is always a palindrome. The algorithm never finds a mismatch and correctly outputs:

```
NO
```

Now look at:

```
3
2 1 3
```

When processing value `1`, both `2` and `3` are still unprocessed. The interval around `1` has radius zero, so nothing is detected. Later, when processing `2`, values `1` and `3` are both on the same side of `2` in permutation order. The centered interval remains palindromic and the algorithm outputs:

```
NO
```

Finally:

```
3
3 2 1
```

When processing value `2`, value `3` has already been seen while value `1` has not. Their bits differ, so the interval around `2` is not a palindrome. The algorithm immediately reports:

```
YES
```

This confirms that the method correctly handles both endpoint orders. The middle value only needs to lie between them in the permutation, regardless of which endpoint appears first.

Sources:
