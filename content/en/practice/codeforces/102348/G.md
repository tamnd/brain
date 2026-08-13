---
title: "CF 102348G - Swap Letters"
description: "We have two binary strings s and t of the same length. At one operation, we may choose any position in s and any position in t, then exchange those two characters. The two positions do not have to be equal, so an operation can fix two different mismatches at once."
date: "2026-08-14T02:20:45+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102348
codeforces_index: "G"
codeforces_contest_name: "ICPC 2019-2020 NERC (NEERC), Southern and Volga Russia Qualifier"
rating: 0
weight: 102348
solve_time_s: 332
verified: false
draft: false
---

[CF 102348G - Swap Letters](https://codeforces.com/problemset/problem/102348/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 5m 32s  
**Verified:** no  

## Solution
## Problem Understanding

We have two binary strings `s` and `t` of the same length. At one operation, we may choose any position in `s` and any position in `t`, then exchange those two characters. The two positions do not have to be equal, so an operation can fix two different mismatches at once.

The goal is to make the entire strings identical using as few cross-string swaps as possible. We must either print the minimum number of swaps together with one optimal sequence, or print `-1` when no sequence can work.

The useful way to look at a position is by comparing its two characters. There are only four possibilities. Positions containing `aa` or `bb` are already correct. A position containing `ab` means `s[i] = a` and `t[i] = b`, while `ba` means the opposite. A swap between suitable positions can eliminate two mismatches simultaneously.

The length can reach `2 * 10^5`, so an algorithm that scans all pairs of positions is already too slow. A quadratic algorithm can perform roughly `4 * 10^10` pair checks in the worst case, far beyond what a 2-second limit allows. We need a solution whose work grows linearly with the string length, apart from the number of operations we actually print.

There is also a global feasibility condition. Every operation merely exchanges characters between the two strings, so the total number of `a` characters across both strings never changes. For the final strings to be equal, every character must occur an even number of times across the two strings. Consequently, if the total number of `a` characters is odd, the answer is impossible. The same condition can be expressed more directly using mismatches: the number of `ab` positions plus the number of `ba` positions must be even.

A first edge case is a single mismatch. For input

```
1
a
b
```

the only position is `ab`, so the total number of mismatches is odd. The correct output is `-1`. A careless implementation that simply records mismatches and pairs whatever is available could leave one unmatched position and incorrectly print a sequence.

A second edge case occurs when there is one `ab` mismatch and one `ba` mismatch. For example,

```
2
ab
ba
```

two operations are necessary. The first swap can transform the `ab` position into `ba`, but it does not finish the problem. A second swap is required to resolve the resulting pair. Treating every pair of mismatches as solvable in one operation would incorrectly claim that one operation is enough.

A third edge case is that all positions can already match. For example,

```
3
aba
aba
```

requires zero operations. An implementation that assumes at least one mismatch exists can accidentally access an empty mismatch list or print an unnecessary operation.

## Approaches

A straightforward approach is to inspect mismatching positions and repeatedly search for two positions whose characters can be exchanged to make progress. Since there are two kinds of mismatch, one can try every possible pair of indices and test whether swapping the corresponding characters reduces the number of mismatches. This is correct because an exhaustive search considers every legal swap, but it is too expensive. With `n` positions, there are `n²` possible cross-string swaps, and repeatedly searching through them can require on the order of `n²` checks. At `n = 2 * 10^5`, that is about `4 * 10^10` candidate swaps.

The key observation is that the actual characters matter only through the mismatch type. Suppose positions `i` and `j` are both of type `ab`. At both positions we have `s = a` and `t = b`. Swapping `s[i]` with `t[j]` exchanges `a` and `b`, so both positions become `bb` and `aa`. Thus two `ab` mismatches can be fixed by one operation. The same argument works for two `ba` mismatches.

This immediately suggests storing the indices of the two mismatch types separately. Every pair inside the same type costs exactly one operation, and there is no reason to search for a better arrangement because one operation is the theoretical minimum for fixing two mismatches.

The only interesting case is when both mismatch lists have odd size. After pairing as many positions as possible, one `ab` and one `ba` remain. They cannot be fixed in one operation because their character orientations are opposite. However, two operations suffice. If `i` is the remaining `ab` position and `j` is the remaining `ba` position, first swap `s[i]` with `t[i]`. Position `i` changes from `ab` to `ba`. Now positions `i` and `j` are both `ba`, so swapping `s[i]` with `t[j]` fixes both.

The minimum follows from the same structure. Every operation can fix at most two mismatching positions, so pairing two equal mismatch types in one operation is optimal. When one mismatch of each type remains, one operation cannot fix both, while the construction above fixes them in exactly two. The resulting number of operations is therefore minimal.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(n²)` or worse with repeated searches | `O(n)` | Too slow |
| Optimal | `O(n)` | `O(n)` | Accepted |

## Algorithm Walkthrough

1. Scan every position `i` from `0` to `n - 1`. If `s[i] = t[i]`, nothing needs to be done there. If `s[i] = a` and `t[i] = b`, store `i` in the `ab` list. If `s[i] = b` and `t[i] = a`, store `i` in the `ba` list. These two lists contain exactly the positions that still need attention.
2. Check the parity of the two mismatch lists. If `len(ab) + len(ba)` is odd, print `-1`. The number of mismatches cannot change parity in a way that allows every position to become equal, because the total number of each character across both strings is preserved.
3. Pair consecutive positions in `ab`. For every pair `ab[i]` and `ab[i + 1]`, add the operation `(ab[i], ab[i + 1])`. Both positions have the form `ab`, so swapping the `a` from the first position in `s` with the `b` from the second position in `t` changes both positions into equal pairs.
4. Pair consecutive positions in `ba` in the same way. For every pair `ba[i]` and `ba[i + 1]`, add `(ba[i], ba[i + 1])`. Since both positions have the form `ba`, the same reasoning fixes both with one operation.
5. If both lists have an odd length, one position `i` remains in `ab` and one position `j` remains in `ba`. Add the operation `(i, i)`. Since position `i` is `ab`, swapping its own two characters changes it into `ba`.
6. Add a second operation `(i, j)`. Position `i` is now `ba`, and position `j` was already `ba`, so swapping `s[i]` with `t[j]` changes both positions into equal pairs.
7. Convert every stored zero-based index to one-based indexing when printing. Output the number of operations followed by the operation pairs.

### Why it works

The invariant is that every position not stored in `ab` or `ba` is already equal, while every stored position is represented by exactly one mismatch type. A same-type pair is always removable in one operation, so all such pairs can be eliminated independently. If two odd-sized mismatch lists remain, the first operation changes one leftover `ab` into `ba`, after which the two leftovers have the same type and the second operation removes them. If the total mismatch count is odd, the conserved total number of each character makes the target state unreachable. Every operation fixes at most two mismatches, and the algorithm uses one operation whenever two mismatches can be fixed together, with exactly two operations for the unavoidable opposite-type leftovers. Hence the produced sequence is both valid and minimum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    s = input().strip()
    t = input().strip()

    ab = []
    ba = []

    for i in range(n):
        if s[i] == t[i]:
            continue
        if s[i] == 'a':
            ab.append(i)
        else:
            ba.append(i)

    if (len(ab) + len(ba)) % 2:
        print(-1)
        return

    ans = []

    for i in range(0, len(ab) - 1, 2):
        ans.append((ab[i], ab[i + 1]))

    for i in range(0, len(ba) - 1, 2):
        ans.append((ba[i], ba[i + 1]))

    if len(ab) % 2 == 1:
        i = ab[-1]
        j = ba[-1]
        ans.append((i, i))
        ans.append((i, j))

    out = [str(len(ans))]
    for x, y in ans:
        out.append(f"{x + 1} {y + 1}")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The first loop classifies every position exactly once. Equal positions are ignored, while the two possible mismatch orientations are stored separately. Because the alphabet contains only `a` and `b`, there is no third mismatch type to handle.

The two pairing loops advance by two. This is why the upper bound is `len(ab) - 1` rather than `len(ab)`: the final unpaired element must be left untouched until the special two-operation case is handled. The same applies to `ba`.

The special case checks only `len(ab) % 2`. Once the total number of mismatches is known to be even, `ab` and `ba` necessarily have the same parity. Thus if `ab` is odd, `ba` is also odd and both have exactly one leftover element after pairing.

The operation indices are stored internally as zero-based values because Python strings use zero-based indexing. The output requires one-based positions, so `x + 1` and `y + 1` are printed. No simulation of the swaps is needed. The classification of a pair proves what that operation does, and avoiding simulation keeps the implementation simple.

There is no integer overflow concern in Python. The maximum number of operations is at most `n + 1`, which is small enough to store and print directly. The output itself can contain `O(n)` lines, so constructing it as a list of strings and writing it once is more efficient than performing many individual `print` calls.

## Worked Examples

### Sample 1

The input is

```
4
abab
aabb
```

The position classification is:

| Position | `s[i]` | `t[i]` | Type |
| --- | --- | --- | --- |
| 1 | `a` | `a` | equal |
| 2 | `b` | `a` | `ba` |
| 3 | `a` | `b` | `ab` |
| 4 | `b` | `b` | equal |

The resulting variables are:

| `ab` | `ba` | Operations added |
| --- | --- | --- |
| `[3]` | `[2]` | none yet |
| `[3]` | `[2]` | `(3, 3)` |
| `[3]` | `[2]` | `(3, 3)`, `(3, 2)` |

The first operation uses the remaining `ab` position itself. Position 3 changes from `ab` to `ba`. Now positions 3 and 2 are both `ba`, so the second operation fixes them together. The final answer has two operations, matching the sample's minimum.

### Sample 2

The input is

```
1
a
b
```

The scan produces:

| Position | `s[i]` | `t[i]` | `ab` | `ba` |
| --- | --- | --- | --- | --- |
| 1 | `a` | `b` | `[1]` | `[]` |

The total mismatch count is one, which is odd.

| Total mismatches | Feasible? | Output |
| --- | --- | --- |
| 1 | No | `-1` |

There is no second mismatching position with which the lone character imbalance can be resolved. The algorithm rejects the case before trying to access a nonexistent partner.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n)` | Every character is scanned once, every mismatch is processed once, and the output contains `O(n)` operations. |
| Space | `O(n)` | The two mismatch lists and the output operation list together contain `O(n)` elements. |

With `n` up to `2 * 10^5`, a linear scan is easily appropriate for the 2-second limit. The memory usage is also linear and comfortably below 256 MB. The number of printed operations is itself linear, so the algorithm is asymptotically optimal because merely reading the input and producing the answer already requires `O(n)` work in the worst case.

## Test Cases

The test harness should validate the properties of the output rather than compare the exact operation sequence, because the problem allows any optimal sequence. Different correct implementations can produce different, equally minimal pairs of indices.

```python
import sys
import io

def solve_io():
    input = sys.stdin.readline

    n = int(input())
    s = input().strip()
    t = input().strip()

    ab = []
    ba = []

    for i in range(n):
        if s[i] == t[i]:
            continue
        if s[i] == 'a':
            ab.append(i)
        else:
            ba.append(i)

    if (len(ab) + len(ba)) % 2:
        print(-1)
        return

    ans = []

    for i in range(0, len(ab) - 1, 2):
        ans.append((ab[i], ab[i + 1]))

    for i in range(0, len(ba) - 1, 2):
        ans.append((ba[i], ba[i + 1]))

    if len(ab) % 2:
        i = ab[-1]
        j = ba[-1]
        ans.append((i, i))
        ans.append((i, j))

    print(len(ans))
    for x, y in ans:
        print(x + 1, y + 1)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve_io()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

def check(inp: str):
    data = inp.strip().splitlines()
    n = int(data[0])
    s = data[1]
    t = data[2]

    out = run(inp).strip().splitlines()

    possible = (sum(c == 'a' for c in s) +
                sum(c == 'a' for c in t)) % 2 == 0

    if not possible:
        assert out == ["-1"]
        return

    k = int(out[0])
    assert len(out) == k + 1

    # The theoretical minimum.
    ab = []
    ba = []
    for i in range(n):
        if s[i] == t[i]:
            continue
        if s[i] == 'a':
            ab.append(i)
        else:
            ba.append(i)

    expected = len(ab) // 2 + len(ba) // 2
    if len(ab) % 2:
        expected += 2

    assert k == expected

    ss = list(s)
    tt = list(t)

    for line in out[1:]:
        x, y = map(int, line.split())
        assert 1 <= x <= n
        assert 1 <= y <= n

        x -= 1
        y -= 1
        ss[x], tt[y] = tt[y], ss[x]

    assert ss == tt

# Provided samples.
check("""4
abab
aabb
""")

check("""1
a
b
""")

check("""8
babbaabb
abababaa
""")

# Minimum size, already equal.
check("""1
a
a
""")

# Minimum size, impossible with one mismatch.
check("""1
b
a
""")

# All equal values, with a longer input.
check("""6
aaaaaa
aaaaaa
""")

# Two same-type mismatches, requiring exactly one operation.
check("""2
aa
bb
""")

# Opposite mismatch types, requiring the special two-operation construction.
check("""2
ab
ba
""")

# Larger boundary-style case.
n = 200000
s = "a" * n
t = "b" * n
check(f"{n}\n{s}\n{t}\n")

print("all tests passed")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / a / a` | `0` operations | Minimum-size already-equal case |
| `1 / b / a` | `-1` | Minimum-size impossible case and odd mismatch count |
| `6 / aaaaaa / aaaaaa` | `0` operations | All positions already equal |
| `2 / aa / bb` | `1` operation | Two mismatches of the same type |
| `2 / ab / ba` | `2` operations | The special opposite-type construction |
| `n = 200000`, `s = a...a`, `t = b...b` | `100000` operations | Maximum-size input and linear-time behavior |

The harness also checks that every reported index is inside the valid one-based range, applies the operations to the strings, verifies that the final strings are equal, and independently computes the theoretical minimum. This catches both incorrect operation construction and off-by-one errors.

## Edge Cases

The odd-mismatch case is handled before any pairing. For

```
1
a
b
```

the `ab` list has size one and the `ba` list has size zero. Their total is odd, so the algorithm immediately prints `-1`. No invalid partner is accessed.

The opposite-type case is the subtle one. For

```
2
ab
ba
```

we get `ab = [0]` and `ba = [1]`. Both lists are odd. The algorithm first adds `(0, 0)`, changing the first position from `ab` to `ba`. It then adds `(0, 1)`. At that moment both positions have type `ba`, so exchanging `s[0] = b` with `t[1] = a` makes position 1 equal to `aa` and position 2 equal to `bb`. Two operations are used, and one operation cannot suffice.

For an already-equal input such as

```
3
aba
aba
```

both mismatch lists remain empty. The total mismatch count is zero, the pairing loops do nothing, the special case does nothing, and the program prints `0`. This is the correct minimum because no swap is necessary.

For two mismatches of the same type, consider

```
2
aa
bb
```

Both positions are `ab`, so `ab = [0, 1]`. The first pairing loop adds `(0, 1)`. Swapping `s[0] = a` with `t[1] = b` produces `bb` in the first position and `aa` in the second, so the strings become equal after exactly one operation. The algorithm reaches the lower bound of one operation.

Finally, the maximum-size case with

```
200000
aaaaaaaaaa...aaaaaaaaaa
bbbbbbbbbb...bbbbbbbbbb
```

has `200000` `ab` mismatches. They can be grouped into `100000` pairs, and each pair requires one swap. The algorithm performs one linear scan and generates exactly `100000` operations. It never examines the roughly `4 * 10^10` possible cross-string index pairs, which is the key reason it remains fast enough.
