---
title: "CF 102348G - Swap Letters"
description: "We have two strings s and t of the same length, and every character is either a or b. In one operation, we may choose any position in s and any position in t, then exchange the two characters."
date: "2026-08-17T10:41:43+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102348
codeforces_index: "G"
codeforces_contest_name: "ICPC 2019-2020 NERC (NEERC), Southern and Volga Russia Qualifier"
rating: 0
weight: 102348
solve_time_s: 405
verified: false
draft: false
---

[CF 102348G - Swap Letters](https://codeforces.com/problemset/problem/102348/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 6m 45s  
**Verified:** no  

## Solution
## Problem Understanding

We have two strings `s` and `t` of the same length, and every character is either `a` or `b`. In one operation, we may choose any position in `s` and any position in `t`, then exchange the two characters. The goal is to make the two strings identical using as few such cross-string swaps as possible.

The output must contain the minimum number of swaps and one sequence of index pairs that achieves it. If no sequence can make the strings equal, we print `-1`.

The first useful observation is about character counts. A swap never changes the total number of `a` characters across both strings. If the final strings are equal, each position contributes the same character to both strings, so the total number of `a` characters must be even. Equivalently, the number of positions where `s[i] != t[i]` must be even. If it is odd, no sequence of swaps can work.

With `n` as large as `2 * 10^5`, an algorithm with quadratic or exponential behavior is not suitable. A two-second limit means we should aim for linear or near-linear work, roughly proportional to the input size. Storing the mismatching positions is also cheap because there can be at most `n` of them.

There are two mismatch types. At a position where `s[i] = a` and `t[i] = b`, call it an `ab` mismatch. At a position where `s[i] = b` and `t[i] = a`, call it a `ba` mismatch. These types behave differently when paired, and overlooking that distinction is the main source of incorrect solutions.

Consider `n = 1`, `s = "a"`, `t = "b"`. There is one mismatch, so the total number of mismatches is odd. A careless solution might try swapping the two characters at index `1`, but that operation exchanges `a` and `b` between the strings and simply leaves the strings as `"b"` and `"a"`. The correct answer is `-1`.

Another important case is a single mismatch of each type. For example, with `s = "ab"` and `t = "ba"`, the mismatches are `ab` at position `1` and `ba` at position `2`. They cannot be fixed with one swap between those two different positions. Two operations are necessary: swap `s[1]` with `t[1]`, then swap `s[1]` with `t[2]`. The answer is `2`. A solution that always pairs one `ab` with one `ba` and assumes one operation is enough will fail here.

Finally, when there are two mismatches of the same type, one operation is enough. For `s = "aabb"` and `t = "bbaa"`, positions `1` and `2` are both `ab` mismatches. Swapping `s[1]` with `t[2]` fixes both positions simultaneously. A solution that processes every mismatching position independently would use too many operations.

## Approaches

A direct brute-force approach can model every possible arrangement of all `2n` characters in the two strings as a state. From one state there are `n^2` possible cross-string swaps, so a breadth-first search could explore states in increasing number of operations and stop when the two strings become equal. This is correct because BFS finds the shortest path in an unweighted state graph.

The problem is the size of that graph. The total number of `a` characters is preserved, so if there are `k` of them, there can be `C(2n, k)` distinct states. This is maximized around `k = n`, giving roughly `C(2n, n)`, which grows as `4^n / sqrt(n)`. Exploring up to `n^2` transitions from each state gives a worst-case scale of `Theta(n^2 C(2n, n))`, which is completely infeasible even for a few dozen positions.

A more focused greedy approach could inspect mismatches and try to fix them one by one. The key insight is that mismatches can be paired. If two positions have the same mismatch type, one cross-string swap fixes both. For example, two `ab` positions can be paired by swapping the `a` from the first position with the `b` from the second. The same argument works for two `ba` positions.

After repeatedly pairing equal types, there can be at most one `ab` mismatch and at most one `ba` mismatch left. If neither remains, we are finished. If exactly one remains, the total number of mismatches is odd, so the instance is impossible. If both remain, they require two operations. The first operation swaps the two characters at one of the remaining positions with itself across the strings, changing the mismatch type there. The two remaining mismatches then become the same type and can be solved by a second swap.

The entire problem therefore reduces to collecting mismatch positions, pairing equal types, and handling the possible two leftovers separately.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `Theta(n^2 C(2n,n))` in the worst case | Exponential | Too slow |
| Optimal | `O(n)` | `O(n)` | Accepted |

## Algorithm Walkthrough

1. Scan all positions from left to right. If `s[i] == t[i]`, that position already agrees and needs no operation. Otherwise, append its 1-based index to either `ab` or `ba`, depending on whether the pair is `(a, b)` or `(b, a)`.

Keeping the two mismatch types separate is what lets us recognize when one operation can solve two positions.
2. If the total number of mismatches, `len(ab) + len(ba)`, is odd, print `-1`.

Every operation preserves the total number of `a` characters, while equal final strings contain an even number of `a` characters in total. The parity condition is therefore necessary. For binary strings it is also sufficient.
3. Pair consecutive `ab` mismatches. For every pair `ab[i]` and `ab[i + 1]`, add the operation `(ab[i], ab[i + 1])`.

At the first position, `s` contains `a` and `t` contains `b`. At the second position, `s` contains `a` and `t` contains `b`. Swapping `s[ab[i]]` with `t[ab[i + 1]]` changes both positions to `(b, b)` or, depending on the direction of the pair, fixes both mismatches simultaneously. The same reasoning applies to two `ba` mismatches.
4. Pair consecutive `ba` mismatches in exactly the same way. For every pair `ba[i]` and `ba[i + 1]`, add `(ba[i], ba[i + 1])`.

Each such operation removes two mismatches, so after this step there can be at most one mismatch of each type.
5. If both `ab` and `ba` have one unpaired position, say `x` and `y`, perform `(x, x)` first.

At position `x`, the characters are `a` in `s` and `b` in `t`. Swapping those two characters changes the mismatch from `ab` to `ba`. Now both remaining positions have the same mismatch type.
6. Perform `(x, y)` as the second operation.

The two remaining equal-type mismatches are now fixed by the same pairing argument used earlier.
7. Output the operations collected in the previous steps.

Every operation removes two mismatches, except that the first operation in the leftover case changes their arrangement so that the second operation can remove the final two. Since each operation is used for the maximum possible reduction, the resulting count is minimal.

### Why it works

The invariant is that the collected mismatch positions describe exactly the places where the two strings still disagree. Two mismatches of the same type can always be removed with one operation, so pairing them is optimal because no single operation can fix more than two mismatching positions.

After all such pairs are removed, at most one mismatch of each type remains. If only one remains, the mismatch count is odd and equality is impossible. If two remain, they necessarily have opposite types. One self-index swap changes one type into the other, and a final cross-index swap fixes both. Thus every possible solvable configuration is handled, and every operation is used in a way that achieves the minimum possible number.

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
            ab.append(i + 1)
        else:
            ba.append(i + 1)

    if (len(ab) + len(ba)) % 2:
        print(-1)
        return

    ans = []

    for i in range(0, len(ab) - 1, 2):
        ans.append((ab[i], ab[i + 1]))

    for i in range(0, len(ba) - 1, 2):
        ans.append((ba[i], ba[i + 1]))

    if len(ab) % 2 == 1:
        x = ab[-1]
        y = ba[-1]

        ans.append((x, x))
        ans.append((x, y))

    print(len(ans))
    for x, y in ans:
        print(x, y)

if __name__ == "__main__":
    solve()
```

The first scan classifies every disagreement into exactly one of the two mismatch arrays. The `i + 1` conversion is deliberate because the algorithm internally uses Python's zero-based indexing while the problem requires positions starting from `1`.

The pairing loops advance by two. For example, if `ab = [2, 5, 7, 9]`, the operations are `(2, 5)` and `(7, 9)`. The loop bound `len(ab) - 1` prevents accessing a nonexistent second element when the array has odd length.

The leftover case is the subtle part. When `ab` has one unpaired position, `ba` must also have one because the total mismatch count is even. The operation `(x, x)` is legal because the two selected positions may have the same numeric index, provided one belongs to `s` and the other to `t`. It flips the mismatch at `x`, after which `(x, y)` fixes both positions.

No simulation of the strings is required. We only need the mismatch classification from the original strings because the constructed operations have already been reasoned about algebraically. Python integers also have no overflow concern, and at most `n` operations are produced.

## Worked Examples

### Sample 1

The input is:

```
4
abab
aabb
```

The mismatch classification is as follows.

| Position | `s[i]` | `t[i]` | Mismatch type | Stored position |
| --- | --- | --- | --- | --- |
| 1 | a | a | equal | none |
| 2 | b | a | ba | 2 |
| 3 | a | b | ab | 3 |
| 4 | b | b | equal | none |

There is one `ab` mismatch and one `ba` mismatch, so neither can be paired with another mismatch of the same type.

| Step | `ab` | `ba` | Operation | Reason |
| --- | --- | --- | --- | --- |
| Initial | `[3]` | `[2]` | none | Two opposite-type leftovers |
| 1 | `[3]` | `[2]` | `(3, 3)` | Convert the `ab` mismatch at 3 into `ba` |
| 2 | `[3]` | `[2]` | `(3, 2)` | Pair and remove the two `ba` mismatches |

After `(3, 3)`, the strings become `abbb` and `aaab`. The final swap `(3, 2)` makes both strings equal to `abab`. The algorithm outputs two operations, which is optimal because one operation cannot resolve two opposite-type mismatches directly.

### Sample 2

The input is:

```
1
a
b
```

There is only one position, and it is an `ab` mismatch.

| Position | `s[i]` | `t[i]` | `ab` | `ba` | Total mismatches |
| --- | --- | --- | --- | --- | --- |
| 1 | a | b | `[1]` | `[]` | 1 |

The total number of mismatches is odd, so the algorithm immediately returns `-1`.

This demonstrates why the parity check must happen before attempting to pair leftovers. There is no second mismatch that could absorb the unmatched character, so no sequence of swaps can produce equal strings.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n)` | One scan classifies mismatches, and the pairing loops together process each mismatch once. |
| Space | `O(n)` | The two mismatch arrays and the answer contain at most `O(n)` indices and operations. |

For `n <= 2 * 10^5`, the algorithm performs only a constant amount of work per character and stores a linear number of integers. This is comfortably within the two-second time limit and the 256 MB memory limit.

## Test Cases

The output sequence is not unique, so tests should validate the returned operations rather than compare the output text byte for byte. The following harness runs the algorithm, checks that the reported number of operations is minimal, and simulates every operation to verify that the resulting strings are equal.

```python
import sys
import io

def solve_io(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    n = int(sys.stdin.readline())
    s = sys.stdin.readline().strip()
    t = sys.stdin.readline().strip()

    ab = []
    ba = []

    for i in range(n):
        if s[i] == t[i]:
            continue
        if s[i] == 'a':
            ab.append(i + 1)
        else:
            ba.append(i + 1)

    if (len(ab) + len(ba)) % 2:
        print(-1)
    else:
        ans = []

        for i in range(0, len(ab) - 1, 2):
            ans.append((ab[i], ab[i + 1]))

        for i in range(0, len(ba) - 1, 2):
            ans.append((ba[i], ba[i + 1]))

        if len(ab) % 2:
            x = ab[-1]
            y = ba[-1]
            ans.append((x, x))
            ans.append((x, y))

        print(len(ans))
        for x, y in ans:
            print(x, y)

    result = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return result

def run(inp: str) -> str:
    return solve_io(inp)

def validate(inp: str):
    data = inp.strip().splitlines()
    n = int(data[0])
    s = list(data[1])
    t = list(data[2])

    out = run(inp).strip().splitlines()

    mismatch_count = sum(a != b for a, b in zip(s, t))

    if mismatch_count % 2 == 1:
        assert out == ["-1"], "expected impossible"
        return

    assert out[0] != "-1"

    k = int(out[0])
    assert k == len(out) - 1

    for line in out[1:]:
        x, y = map(int, line.split())
        assert 1 <= x <= n
        assert 1 <= y <= n
        s[x - 1], t[y - 1] = t[y - 1], s[x - 1]

    assert s == t

    ab = sum(a == 'a' and b == 'b' for a, b in zip(data[1], data[2]))
    ba = sum(a == 'b' and b == 'a' for a, b in zip(data[1], data[2]))

    expected = ab // 2 + ba // 2
    if ab % 2:
        expected += 2

    assert k == expected, f"expected {expected}, got {k}"

# Provided samples
validate("""4
abab
aabb
""")

validate("""1
a
b
""")

validate("""8
babbaabb
abababaa
""")

# Minimum size, already equal
validate("""1
a
a
""")

# Minimum size, impossible
validate("""1
b
a
""")

# Two equal-type mismatches, requiring exactly one operation
validate("""2
aa
bb
""")

# Two opposite-type mismatches, requiring exactly two operations
validate("""2
ab
ba
""")

# Larger boundary-style case with many equal-type pairs
validate("""8
aaaaaaaa
bbbbbbbb
""")

# Maximum-size input, already equal
n = 200000
validate(f"""{n}
{'a' * n}
{'a' * n}
""")
```

The custom cases exercise several different failure modes. The already-equal case checks that zero operations are accepted. The `n = 1` opposite-character case checks the impossibility condition at the smallest possible input size. The `aa` versus `bb` case checks pairing of multiple equal-type mismatches. The `ab` versus `ba` case checks the special two-operation construction. The large all-mismatch case checks that the implementation remains linear when `n` reaches its maximum.

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / a / a` | `0` | Already equal, no operations |
| `1 / b / a` | `-1` | Smallest impossible case |
| `2 / aa / bb` | `1` operation | Pairing two mismatches of the same type |
| `2 / ab / ba` | `2` operations | Opposite leftover types |
| `8 / aaaaaaaa / bbbbbbbb` | `4` operations | Many equal-type pairs |
| `n = 200000`, both strings all `a` | `0` | Maximum input size and linear scan |

## Edge Cases

The first edge case is an odd number of mismatches. For

```
1
a
b
```

the mismatch arrays are `ab = [1]` and `ba = []`. Their combined size is `1`, so the algorithm prints `-1` before constructing any operations. This avoids the incorrect idea of trying to fix the only mismatch by swapping position `1` with itself. That swap merely exchanges `a` and `b` and leaves the two strings different.

The second edge case is two mismatches of the same type. Consider

```
2
aa
bb
```

Both positions are `ab` mismatches, so `ab = [1, 2]`. The pairing loop generates `(1, 2)`. The operation swaps `s[1] = a` with `t[2] = b`, producing `s = "ba"` and `t = "ba"`. One operation is enough, and it is clearly minimal because the strings were not equal initially.

The third edge case is one mismatch of each type:

```
2
ab
ba
```

Here `ab = [1]` and `ba = [2]`. There are two mismatches, so the instance is possible, but neither type has a pair. The algorithm first performs `(1, 1)`, changing the strings from `ab` and `ba` to `bb` and `aa`. Now the remaining conceptual mismatch at position `1` has changed type, allowing `(1, 2)` to exchange `s[1] = b` with `t[2] = a`. The strings become `ab` and `ab`. Two operations are required because the first operation can only change one mismatch when the two remaining types are different.

The final boundary case is a maximum-size input where the strings are already equal. With `n = 200000` and both strings consisting entirely of `a`, the scan encounters no mismatches, both arrays remain empty, and the answer is `0`. This confirms that the algorithm does not accidentally create operations for matching positions and that its memory usage stays linear even at the largest allowed input size.
