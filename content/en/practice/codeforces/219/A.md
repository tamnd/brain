---
title: "CF 219A - k-String"
description: "We are given a lowercase string and an integer k. We may rearrange the letters however we want. The goal is to build a new string that consists of exactly k identical blocks placed one after another."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 219
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 135 (Div. 2)"
rating: 1000
weight: 219
solve_time_s: 82
verified: true
draft: false
---

[CF 219A - k-String](https://codeforces.com/problemset/problem/219/A)

**Rating:** 1000  
**Tags:** implementation, strings  
**Solve time:** 1m 22s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a lowercase string and an integer `k`. We may rearrange the letters however we want. The goal is to build a new string that consists of exactly `k` identical blocks placed one after another.

For example, if `k = 3`, then the final string must look like:

```
t + t + t
```

where all three copies are the same string `t`.

The only thing we are allowed to change is the order of characters. Every character from the original string must still appear exactly the same number of times in the final result.

The constraints are very small. The string length is at most `1000`, and there are only `26` lowercase English letters. This immediately tells us that we do not need advanced algorithms. Even an `O(n^2)` solution would easily pass. What matters here is understanding the mathematical condition that makes a valid construction possible.

The key observation comes from frequency counts. Suppose the final repeated block is `t`, and we repeat it `k` times. Then every character count in the whole string must be divisible by `k`.

For example:

```
k = 3
string = aaabbbccc
```

Each letter appears `3` times, so we can create:

```
abcabcabc
```

But if we have:

```
k = 2
string = aaabc
```

the character `'a'` appears `3` times, which cannot be split evenly across two identical blocks. No rearrangement can fix this.

There are several edge cases that commonly break incorrect implementations.

Consider:

```
k = 4
s = aaaa
```

The correct answer is:

```
aaaa
```

A careless implementation might try to build a base block of length greater than `1`, even though the smallest valid block is just `"a"`.

Another tricky case is:

```
k = 3
s = aabbbb
```

The frequencies are:

```
a -> 2
b -> 4
```

Neither count is divisible by `3`, so the answer must be `-1`. A naive approach that only checks whether the total length is divisible by `k` would incorrectly think a solution exists because `6 % 3 == 0`.

One more subtle case is:

```
k = 1
s = codeforces
```

Every string is automatically a `1`-string. The original string itself is already valid, and any rearrangement also works. Implementations that assume every frequency must appear multiple times can accidentally reject this case.

## Approaches

The brute-force idea is to generate permutations of the string and test whether any permutation is a valid `k`-string.

To test a candidate permutation, we can split it into `k` equal parts and check whether all parts are identical.

This approach is logically correct because it eventually tries every possible arrangement. The problem is the number of permutations. A string of length `1000` has up to `1000!` permutations, which is unimaginably large. Even for length `15`, brute force becomes completely impractical.

The reason brute force feels wasteful is that most permutations differ only in character order, while the actual validity condition depends entirely on character frequencies.

That observation leads to the optimal approach.

Suppose some character appears `cnt` times. In a valid `k`-string, every repeated block must contain the same number of that character. This is only possible if `cnt` is divisible by `k`.

Once every frequency is divisible by `k`, construction becomes easy. For each character, we place `cnt / k` copies into a base block. Repeating that block `k` times automatically recreates the original frequencies.

For example:

```
k = 2
s = aazz
```

The frequencies are:

```
a -> 2
z -> 2
```

Each count is divisible by `2`.

So the base block becomes:

```
az
```

Repeating it twice gives:

```
azaz
```

The problem reduces from searching among permutations to checking divisibility of frequencies.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n! × n) | O(n) | Too slow |
| Optimal | O(n + 26) | O(26) | Accepted |

## Algorithm Walkthrough

1. Read `k` and the string `s`.
2. Count the frequency of every lowercase letter.
3. Check whether every frequency is divisible by `k`.

If some character count is not divisible by `k`, print `-1` and stop.

This condition is necessary because identical repeated blocks must distribute every character evenly.
4. Build the base block string.

For each character, append `frequency / k` copies of that character to the block.
5. Repeat the base block exactly `k` times.
6. Print the resulting string.

### Why it works

The algorithm relies on one property: in a valid `k`-string, every character frequency must be split equally among all `k` copies.

If a character appears `cnt` times overall, then each block must contain exactly `cnt / k` copies. This is only possible when `cnt` is divisible by `k`.

When all frequencies satisfy this condition, constructing the base block using `cnt / k` copies guarantees that repeating the block `k` times restores the original counts exactly. Since all repeated blocks are identical, the final string is by definition a valid `k`-string.

## Python Solution

```python
import sys
input = sys.stdin.readline

k = int(input())
s = input().strip()

freq = [0] * 26

for ch in s:
    freq[ord(ch) - ord('a')] += 1

base = []

for i in range(26):
    if freq[i] % k != 0:
        print(-1)
        sys.exit()

    base.append(chr(i + ord('a')) * (freq[i] // k))

base_string = "".join(base)

print(base_string * k)
```

The first part of the code counts character frequencies using a fixed array of size `26`. Since the alphabet is limited to lowercase English letters, this is simpler and faster than using a dictionary.

The divisibility check is the core correctness condition. The moment we find a frequency not divisible by `k`, we know no solution exists, so the program immediately prints `-1` and exits.

The construction step is compact but important. If a letter appears `cnt` times overall, then each repeated block must contain exactly `cnt // k` copies. Appending that many characters to `base` builds one valid block.

Finally, repeating the base block `k` times recreates the original total frequencies while guaranteeing all parts are identical.

One subtle implementation detail is using integer division only after confirming divisibility. Otherwise, truncation could silently produce the wrong number of characters.

Another small detail is `strip()` when reading the string. Without it, the newline character would accidentally become part of the input.

## Worked Examples

### Example 1

Input:

```
2
aazz
```

Frequency table:

| Character | Frequency | Divisible by 2? | Copies in base |
| --- | --- | --- | --- |
| a | 2 | Yes | 1 |
| z | 2 | Yes | 1 |

Base string construction:

| Step | Base String |
| --- | --- |
| add 'a' | a |
| add 'z' | az |

Final result:

| Base | k | Output |
| --- | --- | --- |
| az | 2 | azaz |

This example shows the standard successful case. Every frequency splits evenly across the repeated blocks.

### Example 2

Input:

```
3
aaabbbb
```

Frequency table:

| Character | Frequency | Divisible by 3? |
| --- | --- | --- |
| a | 3 | Yes |
| b | 4 | No |

Since `'b'` is not divisible by `3`, the algorithm stops immediately.

Output:

```
-1
```

This example demonstrates the key impossibility condition. Rearranging characters cannot change their frequencies.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + 26) | One pass to count characters, one pass over the alphabet |
| Space | O(26) | Fixed-size frequency array |

The input size is at most `1000`, so this solution is far below the time limit. The algorithm only scans the string once and performs constant extra work for the alphabet.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    k = int(input())
    s = input().strip()

    freq = [0] * 26

    for ch in s:
        freq[ord(ch) - ord('a')] += 1

    base = []

    for i in range(26):
        if freq[i] % k != 0:
            print(-1)
            return

        base.append(chr(i + ord('a')) * (freq[i] // k))

    print("".join(base) * k)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    output = sys.stdout.getvalue().strip()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return output

# provided sample
assert run("2\naazz\n") == "azaz", "sample 1"

# minimum size
assert run("1\na\n") == "a", "single character"

# impossible because frequencies are not divisible
assert run("3\naabbbb\n") == "-1", "non-divisible frequencies"

# all characters equal
assert run("4\naaaa\n") == "aaaa", "all same letters"

# larger valid construction
assert run("3\naaabbbccc\n") == "abcabcabc", "repeated base block"

# boundary style case
assert run("2\nabcabc\n") == "abcabc", "already valid"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\na\n` | `a` | Smallest possible input |
| `3\naabbbb\n` | `-1` | Detecting impossible frequency splits |
| `4\naaaa\n` | `aaaa` | Single repeated character |
| `3\naaabbbccc\n` | `abcabcabc` | Multi-character valid construction |
| `2\nabcabc\n` | `abcabc` | Already valid repeated pattern |

## Edge Cases

Consider:

```
k = 1
s = codeforces
```

Every frequency is divisible by `1`, so the algorithm builds the entire string as the base block and repeats it once. The output is valid because every string is automatically a `1`-string.

Now consider:

```
k = 2
s = aaabc
```

The frequencies are:

```
a -> 3
b -> 1
c -> 1
```

The algorithm immediately notices that `3 % 2 != 0` and prints `-1`.

This is correct because no rearrangement can split three copies of `'a'` evenly into two identical blocks.

Another important edge case is:

```
k = 4
s = aaaa
```

The frequency of `'a'` is `4`, so each block receives one `'a'`. The base block becomes:

```
a
```

Repeating it four times gives:

```
aaaa
```

This confirms the algorithm correctly handles cases where the repeated block has length `1`.

Finally, consider:

```
k = 2
s = abcabc
```

The frequencies are all divisible by `2`:

```
a -> 2
b -> 2
c -> 2
```

The base block becomes `"abc"`, and repeating it twice produces `"abcabc"`.

This demonstrates that the algorithm works even when the input is already a valid `k`-string.
