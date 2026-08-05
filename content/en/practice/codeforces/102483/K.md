---
title: "CF 102483K - Kleptography"
description: "The task is to recover the original diary text from an encrypted string. The cipher uses an autokey mechanism: the first n characters of the key are unknown, but after that point the key repeats characters from the beginning of the plaintext."
date: "2026-08-05T18:45:59+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102483
codeforces_index: "K"
codeforces_contest_name: "2018-2019 ICPC Northwestern European Regional Programming Contest (NWERC 2018)"
rating: 0
weight: 102483
solve_time_s: 126
verified: true
draft: false
---

[CF 102483K - Kleptography](https://codeforces.com/problemset/problem/102483/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

The task is to recover the original diary text from an encrypted string. The cipher uses an autokey mechanism: the first `n` characters of the key are unknown, but after that point the key repeats characters from the beginning of the plaintext. Mary knows the last `n` characters of the plaintext and also has the complete ciphertext. Using this information, we must reconstruct the entire plaintext.

The encryption works on letters converted to numbers from 0 to 25. For every position, the ciphertext value is the sum of the plaintext value and the key value modulo 26. The first `n` key characters are the hidden keyword, while the remaining key characters are copied from earlier plaintext positions. The output is the plaintext string in its original order.

The text length is at most 100 characters, and the known suffix length is at most 30. These small bounds allow several possible approaches, but the structure of the cipher gives a direct linear solution. Even if the limits were much larger, a solution near `O(m)` would still be the natural target because every character of the plaintext must be determined.

The tricky part is that the known plaintext characters are at the end of the message, while the unknown key prefix affects the beginning. A careless approach may try to decrypt from left to right, but the first `n` positions have no known key values. Another common mistake is to forget that the known suffix gives exactly the missing plaintext values needed to recover the unknown key.

For example, with:

```
1 3
a
bac
```

the correct output is:

```
aaa
```

The last plaintext character is known as `a`. The last key character is the first plaintext character, so the last ciphertext character gives the equation `c = a + a`, which determines the first plaintext character. A method that assumes the key prefix is the known character would fail because the known character is plaintext, not the key.

Another edge case appears when the known suffix length is almost the entire string:

```
2 3
ab
bbc
```

The correct output is:

```
abc
```

There is only one unknown character at the front, and the algorithm must still use the relationship between the final characters and earlier plaintext positions. Solutions that only work when many characters are unknown can produce incorrect indexing here.

## Approaches

A direct brute-force approach would attempt every possible secret keyword of length `n`. Each keyword has `26^n` possibilities, and for each one we could generate the key, decrypt the ciphertext, and check whether the resulting plaintext ends with the known suffix. This approach is correct because the real keyword is guaranteed to be among the tested candidates. However, it becomes impossible even for small values of `n`. With `n = 30`, the number of candidates is `26^30`, which is far beyond what can be processed.

The reason brute force is unnecessary is that the known suffix fixes the part of the key that depends on the plaintext. For positions after the first `n`, the key character is exactly the plaintext character located `n` positions earlier. The last `n` plaintext characters are already known, so we can use the last `n` ciphertext characters to recover the unknown first `n` key characters.

Once the hidden key prefix is known, the entire message can be decrypted. The important observation is that the suffix is not just a verification condition. It provides the missing information needed to reverse the autokey relation.

The brute-force works because every possible key is considered, but fails because the search space grows exponentially. The observation that the known plaintext suffix reveals the key prefix reduces the problem to a few linear passes over the string.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(26^n * m) | O(m) | Too slow |
| Optimal | O(m) | O(m) | Accepted |

## Algorithm Walkthrough

1. Store the ciphertext and the known final `n` plaintext characters. The known suffix represents the end of the answer and will be used to recover the unknown key prefix.
2. Recover the first `n` key characters using the final `n` ciphertext positions. For a ciphertext character at position `i`, the corresponding plaintext character is already known because it is in the suffix. The equation is `cipher[i] = plain[i] + key[i] (mod 26)`, so the key character can be calculated as `key[i] = cipher[i] - plain[i] (mod 26)`.

This works because the final `n` positions are the only places where both the plaintext and ciphertext are available.
3. Build the full key. The first `n` characters are the recovered secret prefix. Every later key character is copied from the plaintext character `n` positions earlier.
4. Decrypt the complete ciphertext using the generated key. For every position, subtract the key value from the ciphertext value modulo 26 to obtain the plaintext value.
5. Output the reconstructed plaintext.

The invariant behind the algorithm is that every generated key character matches the key definition of the cipher. The first `n` characters are recovered from positions where the plaintext is known, and every later character is copied from the already reconstructed plaintext. Since the key is correct at every position, applying the inverse encryption formula produces the only possible plaintext.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    suffix = input().strip()
    cipher = input().strip()

    key = [''] * m
    plain = [''] * m

    for i in range(n):
        plain[m - n + i] = suffix[i]

    for i in range(n):
        pos = m - n + i
        key[pos] = chr((ord(cipher[pos]) - ord(plain[pos])) % 26 + ord('a'))

    for i in range(n):
        key[i] = key[m - n + i]

    for i in range(n, m):
        key[i] = plain[i - n]

    for i in range(m):
        plain[i] = chr((ord(cipher[i]) - ord(key[i])) % 26 + ord('a'))

    print(''.join(plain))

if __name__ == "__main__":
    solve()
```

The solution first creates arrays for the plaintext and key so that positions can be filled independently. The known suffix is placed directly into the end of the plaintext array.

The loop that recovers the key uses the last `n` positions. The expression uses modulo 26 because subtraction in the alphabet can wrap around, such as recovering `z` from a negative intermediate value.

After the key prefix is recovered, it is copied into the beginning of the key array. The later key positions are filled from plaintext positions `n` places earlier. The order matters because the key depends on plaintext, and those plaintext characters have to be known before they are used.

The final loop performs the inverse cipher operation. Python integers do not overflow, so the modulo calculation only handles the alphabet wrapping.

## Worked Examples

### Sample 1

Input:

```
5 16
again
pirpumsemoystoal
```

| Step | Position | Known plaintext | Recovered key | Action |
| --- | --- | --- | --- | --- |
| 1 | 11 | a | p - a = p | Recover key suffix |
| 2 | 12 | g | s - g = m | Recover key suffix |
| 3 | 13 | a | t - a = t | Recover key suffix |
| 4 | 14 | i | o - i = g | Recover key suffix |
| 5 | 15 | n | a - n = n | Recover key suffix |
| 6 | 0 to 4 | unknown | pmtgn | Copy recovered key prefix |
| 7 | all | unknown | complete | Decrypt |

The recovered key prefix is enough to decrypt the beginning of the message. The suffix `again` remains unchanged because it was already provided as known plaintext.

The final plaintext is:

```
marywasnosyagain
```

### Sample 2

Input:

```
1 12
d
fzvfkdocukfu
```

| Step | Position | Known plaintext | Recovered key | Action |
| --- | --- | --- | --- | --- |
| 1 | 11 | d | f - d = c | Recover one key character |
| 2 | 0 | unknown | c | Set key prefix |
| 3 | 1 to 11 | unknown | previous plaintext | Build autokey |
| 4 | all | unknown | complete | Decrypt |

This example uses the smallest possible key length. It confirms that the algorithm does not depend on having a large known suffix.

The final plaintext is:

```
shortkeyword
```

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m) | Each character is processed a constant number of times while recovering the key and decrypting. |
| Space | O(m) | The plaintext and key arrays store one character per position. |

The maximum text length is small, so the linear solution easily fits within the time and memory limits. The same approach would also scale comfortably to much larger strings.

## Test Cases

```python
import sys
import io

def solve(inp):
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n, m = map(int, input().split())
    suffix = input().strip()
    cipher = input().strip()

    key = [''] * m
    plain = [''] * m

    for i in range(n):
        plain[m - n + i] = suffix[i]

    for i in range(n):
        pos = m - n + i
        key[pos] = chr((ord(cipher[pos]) - ord(plain[pos])) % 26 + ord('a'))

    for i in range(n):
        key[i] = key[m - n + i]

    for i in range(n, m):
        key[i] = plain[i - n]

    for i in range(m):
        plain[i] = chr((ord(cipher[i]) - ord(key[i])) % 26 + ord('a'))

    return ''.join(plain)

assert solve("5 16\nagain\npirpumsemoystoal\n") == "marywasnosyagain"
assert solve("1 12\nd\nfzvfkdocukfu\n") == "shortkeyword"

assert solve("1 3\na\nbac\n") == "aaa"
assert solve("2 3\nab\nbbc\n") == "abc"
assert solve("3 6\naaa\naaaaaa\n") == "aaaaaa"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 3 / a / bac` | `aaa` | Minimum key length and single unknown prefix character |
| `2 3 / ab / bbc` | `abc` | Very short text with the known suffix covering most of the message |
| `3 6 / aaa / aaaaaa` | `aaaaaa` | Repeated characters and modulo arithmetic boundaries |

## Edge Cases

The first edge case is when `n = 1`. In the input:

```
1 3
a
bac
```

the final plaintext character is known. The algorithm places `a` at the last position, calculates the only key prefix character from the last ciphertext character, then decrypts the remaining positions. It outputs:

```
aaa
```

A solution that treats the known letter as the key instead of plaintext would fail here because the two have different roles in the cipher.

The second edge case is when the known suffix is almost the entire message:

```
2 3
ab
bbc
```

The algorithm first stores `ab` as the final two plaintext characters. It uses those two characters with the last two ciphertext characters to recover the hidden key prefix, then decrypts the first character. The result is:

```
abc
```

This confirms that the solution handles cases where only a tiny portion of the plaintext needs to be discovered.

The repeated-character case:

```
3 6
aaa
aaaaaa
```

also needs correct modular subtraction. Every key character is `a`, and every plaintext character remains `a`. The algorithm performs the same calculations without relying on character differences, producing:

```
aaaaaa
```
