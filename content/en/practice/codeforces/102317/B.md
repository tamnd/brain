---
title: "CF 102317B - Phoneme Palindromes"
description: "A normal palindrome reads identically from both directions. Here, two different letters can also represent the same sound."
date: "2026-08-16T18:44:31+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102317
codeforces_index: "B"
codeforces_contest_name: "UCF Locals 2016"
rating: 0
weight: 102317
solve_time_s: 179
verified: true
draft: false
---

[CF 102317B - Phoneme Palindromes](https://codeforces.com/problemset/problem/102317/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 59s  
**Verified:** yes  

## Solution
## Problem Understanding

A normal palindrome reads identically from both directions. Here, two different letters can also represent the same sound. For example, if `c` and `k` are declared equivalent, then `cak` is a phoneme palindrome because its outer letters, `c` and `k`, sound the same, while the middle `a` matches itself.

The input contains several independent test cases. For each test case, we first receive a collection of disjoint pairs of lowercase letters. Each pair says that its two letters have the same sound. A letter belongs to at most one such pair, so the equivalence relation is especially simple. After the pairs, we receive several strings. For every string, we must decide whether every character has the same sound as the character at the symmetric position from the other end. The output must reproduce the original string followed by `YES` or `NO`, with a header and a blank line separating test cases.

The number of equivalent pairs is at most 13, which covers at most 26 letters. Each test string has length at most 50, and there are at most 100 strings in one test case. These limits are small enough that even checking all 13 pairs for every symmetric character pair is easily fast enough. The optimal implementation can do better by assigning each letter a representative of its sound class, reducing every comparison to constant time.

A string of length one is always a phoneme palindrome. For example, with any set of sound pairs, the input

```
1
1
c k
1
a
```

produces

```
Test case #1:
a YES
```

There is no opposite character to disagree with, so a careless implementation that requires at least one pair of positions could incorrectly reject it.

A second edge case occurs when the characters are different but equivalent. With `c` and `k` declared equivalent, the string `ck` is valid:

```
1
1
c k
1
ck
```

The correct result is

```
Test case #1:
ck YES
```

Comparing the raw characters instead of their sounds would incorrectly produce `NO`.

The opposite situation also matters. With `c` and `k` equivalent, `cab` is not a phoneme palindrome because the outer characters are `c` and `b`, which have different sounds:

```
1
1
c k
1
cab
```

The correct result is

```
Test case #1:
cab NO
```

A careless implementation that only checks whether the string contains known equivalent letters, rather than checking the corresponding positions, could incorrectly accept it.

## Approaches

The direct brute-force approach stores the sound-equivalent pairs and, for every string, examines positions from the two ends toward the center. When the two characters are equal, the pair is immediately valid. When they differ, we scan all declared sound pairs to see whether those two characters form one of the pairs. If no pair matches, the string is not a phoneme palindrome. This is correct because a string is a phoneme palindrome exactly when every symmetric pair of positions has the same sound.

In the worst case, a test case contains 100 strings of length 50. There are at most 25 symmetric position comparisons per string, and each unsuccessful comparison may inspect all 13 sound pairs. That gives at most

`100 * 25 * 13 = 32,500`

pair checks for one test case. This is tiny under the given bounds, so the brute-force method is actually fast enough.

The cleaner solution comes from noticing that the sound relation is fixed for an entire test case. Instead of repeatedly searching the list of pairs, assign every letter a canonical representative. If `c` and `k` sound the same, both can map to `c`. Letters without a partner map to themselves. Then two letters have the same sound exactly when their representatives are equal.

This turns each symmetric comparison into a constant-time array lookup. The algorithm still scans each string once, but the inner search through up to 13 pairs disappears. The key observation is that the sound information is static, so we should preprocess it once rather than rediscovering it for every character comparison.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(q · L · p) | O(p) | Accepted under the given limits |
| Optimal | O(q · L + p) | O(26) | Accepted |

Here `q` is the number of strings, `L` is the maximum string length, and `p` is the number of sound-equivalent pairs.

## Algorithm Walkthrough

1. Read the number of test cases and process each one independently. The sound relationships from one test case must not affect any later test case.
2. Create a mapping for all 26 lowercase letters, initially mapping every letter to itself. This represents the default rule that a letter always sounds like itself.
3. For every declared pair `(a, b)`, assign the same representative to both letters. Since no letter occurs in more than one pair, we can simply choose `a` as the representative and set both `a` and `b` to `a`.
4. Read each string and compare its characters symmetrically, using indices `left` and `right`. Start with the first and last characters and move both indices toward the center.
5. For each symmetric pair, compare `representative[s[left]]` with `representative[s[right]]`. If they differ, the two characters have different sounds, so the entire string immediately fails.
6. If all symmetric pairs have equal representatives, print the original string followed by `YES`. If a mismatch was found, print the original string followed by `NO`.

### Why it works

The invariant is that two letters have the same representative exactly when they have the same sound. Initially every letter represents itself, and for every declared equivalent pair both letters are assigned the same representative. Because each letter belongs to at most one pair, no conflicting assignments can occur.

For every symmetric position pair in a string, the algorithm checks equality of these representatives. Equality means the two characters sound the same, while inequality means they do not. A phoneme palindrome is defined precisely by having equal sounds at every symmetric pair, so accepting exactly when all such comparisons succeed is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    output = []

    for case_no in range(1, t + 1):
        p = int(input())

        representative = list(range(26))

        for _ in range(p):
            a, b = input().split()
            x = ord(a) - ord('a')
            y = ord(b) - ord('a')

            representative[y] = x
            representative[x] = x

        q = int(input())

        output.append(f"Test case #{case_no}:")

        for _ in range(q):
            s = input().strip()

            left = 0
            right = len(s) - 1
            ok = True

            while left < right:
                x = representative[ord(s[left]) - ord('a')]
                y = representative[ord(s[right]) - ord('a')]

                if x != y:
                    ok = False
                    break

                left += 1
                right -= 1

            output.append(f"{s} {'YES' if ok else 'NO'}")

        output.append("")

    sys.stdout.write("\n".join(output))

if __name__ == "__main__":
    solve()
```

The `representative` array has 26 entries, one for each lowercase letter. Keeping integer indices instead of strings makes the sound comparison a simple array lookup.

When a pair such as `c k` is read, `c` becomes the representative of both letters. A comparison between `c` and `k` consequently becomes a comparison between the same integer, so it succeeds even though the characters themselves differ.

The two-pointer loop only needs to examine the first half of the string. Once `left >= right`, every symmetric pair has already been checked. For odd-length strings, the middle character is never compared with anything, which is correct because a single character always matches itself.

The code stops at the first mismatch because later positions cannot repair a failed symmetric pair. The original string is stored unchanged, so the required output can reproduce it exactly.

The output is accumulated in a list and written once at the end. This avoids repeated writes and also makes it straightforward to place the required blank line after every test case.

## Worked Examples

The official sample input contains two test cases.

### Sample 1

```
1
1
c k
6
a
cac
ck
cab
kaak
ckckkcck
```

The mapping is `c -> c`, `k -> c`, and every other letter maps to itself.

For `cac`, the outer characters are both represented by `c`, and the middle character is irrelevant.

| String | Left | Right | Left sound | Right sound | Result |
| --- | --- | --- | --- | --- | --- |
| `a` | 0 | 0 |  |  | YES |
| `cac` | 0 | 2 | c | c | continue |
| `cac` | 1 | 1 |  |  | YES |
| `ck` | 0 | 1 | c | c | YES |
| `cab` | 0 | 2 | c | b | NO |
| `kaak` | 0 | 3 | c | c | continue |
| `kaak` | 1 | 2 | a | a | YES |
| `ckckkcck` | 0 | 7 | c | c | continue |
| `ckckkcck` | 1 | 6 | c | c | continue |
| `ckckkcck` | 2 | 5 | c | c | continue |
| `ckckkcck` | 3 | 4 | c | c | continue |
| `ckckkcck` | 4 | 3 |  |  | YES |

The resulting output is:

```
Test case #1:
a YES
cac YES
ck YES
cab NO
kaak YES
ckckkcck YES
```

The trace demonstrates why raw character equality is insufficient. In `ck`, the characters differ, but their representatives are equal.

### Sample 2

```
1
2
a z
x s
5
abbbz
asxz
cx
sxxabzxss
ks
```

Here `a` and `z` share a representative, as do `x` and `s`.

| String | Symmetric pair | Left sound | Right sound | Result |
| --- | --- | --- | --- | --- |
| `abbbz` | `a`, `z` | a | a | continue |
| `abbbz` | `b`, `b` | b | b | YES |
| `asxz` | `a`, `z` | a | a | continue |
| `asxz` | `s`, `x` | x | x | YES |
| `cx` | `c`, `x` | c | x | NO |
| `sxxabzxss` | `s`, `s` | x | x | continue |
| `sxxabzxss` | `x`, `s` | x | x | continue |
| `sxxabzxss` | `x`, `x` | x | x | continue |
| `sxxabzxss` | `a`, `z` | a | a | continue |
| `sxxabzxss` | `b`, `b` | b | b | YES |
| `ks` | `k`, `s` | k | x | NO |

The resulting output is:

```
Test case #1:
abbbz YES
asxz YES
cx NO
sxxabzxss YES
ks NO
```

This example exercises both directions of the equivalence pairs. The representative mapping makes `x` and `s` interchangeable without needing to search the original pair list.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(p + q · L) | Building the mapping takes O(p), and every string is scanned from both ends in O(L) time |
| Space | O(26) | The sound mapping contains one entry for each lowercase letter, apart from the output buffer |

With `p <= 13`, `q <= 100`, and `L <= 50`, the actual amount of work is very small. Even the brute-force solution performs only 32,500 sound-pair checks in the largest single test case, while the representative mapping reduces this further to at most 2,500 symmetric character comparisons. The solution comfortably fits the 1 second and 256 MB limits reported for the contest problem.

## Test Cases

The official samples are given in the contest materials.

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline
    t = int(input())
    output = []

    for case_no in range(1, t + 1):
        p = int(input())
        representative = list(range(26))

        for _ in range(p):
            a, b = input().split()
            x = ord(a) - ord('a')
            y = ord(b) - ord('a')
            representative[y] = x
            representative[x] = x

        q = int(input())
        output.append(f"Test case #{case_no}:")

        for _ in range(q):
            s = input().strip()
            left, right = 0, len(s) - 1
            ok = True

            while left < right:
                if representative[ord(s[left]) - 97] != representative[ord(s[right]) - 97]:
                    ok = False
                    break
                left += 1
                right -= 1

            output.append(f"{s} {'YES' if ok else 'NO'}")

        output.append("")

    return "\n".join(output)

def run(inp: str) -> str:
    global input
    old_stdin = sys.stdin
    old_input = input

    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    try:
        return solve()
    finally:
        sys.stdin = old_stdin
        input = old_input

# provided sample 1
sample1 = """1
1
c k
6
a
cac
ck
cab
kaak
ckckkcck
"""

expected1 = """Test case #1:
a YES
cac YES
ck YES
cab NO
kaak YES
ckckkcck YES
"""

assert run(sample1) == expected1, "sample 1"

# provided sample 2
sample2 = """1
2
a z
x s
5
abbbz
asxz
cx
sxxabzxss
ks
"""

expected2 = """Test case #1:
abbbz YES
asxz YES
cx NO
sxxabzxss YES
ks NO
"""

assert run(sample2) == expected2, "sample 2"

# Minimum-size input, a single character.
assert run("""1
1
a b
1
z
""") == """Test case #1:
z YES
""", "single-character string"

# All characters are equivalent in the only declared pair.
assert run("""1
1
a z
4
az
za
aaaa
azaa
""") == """Test case #1:
az YES
za YES
aaaa YES
azaa YES
""", "equivalent outer characters"

# Boundary case where the first comparison fails immediately.
assert run("""1
1
c k
3
cab
babc
kc
""") == """Test case #1:
cab NO
babc NO
kc YES
""", "early mismatch and equivalent pair"

# Maximum-size string and all-equal values.
large = "a" * 50
assert run(f"""1
1
b c
1
{large}
""") == f"""Test case #1:
{large} YES
""", "length 50 all-equal string"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single-character `z` | `z YES` | Minimum string length and the `left < right` boundary |
| `az`, `za`, `aaaa`, `azaa` with `a z` equivalent | All `YES` | Different letters with the same sound and all-equal characters |
| `cab`, `babc`, `kc` with `c k` equivalent | `NO`, `NO`, `YES` | Immediate mismatches and equivalent boundary characters |
| 50 copies of `a` | `YES` | Maximum string length and repeated identical characters |

## Edge Cases

For a one-character string, the loop does not execute because `left == right`. The algorithm accepts the string immediately. For example,

```
1
1
c k
1
a
```

produces `a YES`. This is exactly the palindrome definition at the phoneme level because there is only one sound to compare.

For different but equivalent characters, the representative mapping handles the case without special logic. With

```
1
1
c k
1
ck
```

the mapping contains `representative[c] = c` and `representative[k] = c`. The only comparison is consequently `c == c`, so the output is `ck YES`.

For a genuine mismatch, the algorithm stops as soon as it finds one. With

```
1
1
c k
1
cab
```

the first comparison is between `c` and `b`. Their representatives are `c` and `b`, so the algorithm sets `ok` to false and prints `cab NO`. It does not need to inspect the middle character.

For an even-length string, every character belongs to a symmetric pair. With

```
1
1
c k
1
kaak
```

the first comparison is `k` against `k`, represented by `c` against `c`, and the second is `a` against `a`. Both succeed, giving `kaak YES`.

For an odd-length string, the center character has no counterpart that could invalidate the palindrome. In `cac`, the outer `c` characters match, and the middle `a` is never compared. The algorithm correctly returns `cac YES`.

Finally, the sound pairs are independent. With `a z` and `x s`, a comparison between `a` and `z` succeeds while a comparison between `a` and `x` fails. The mapping encodes exactly these independent relationships, so a character cannot accidentally inherit the sound of an unrelated pair.
