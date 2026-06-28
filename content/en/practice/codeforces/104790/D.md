---
title: "CF 104790D - Democratic Naming"
description: "Every city in the new county has a name of the same length. The county's final name is chosen one character at a time. For each position, every city votes for the letter that appears at that position in its own name."
date: "2026-06-28T16:41:29+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104790
codeforces_index: "D"
codeforces_contest_name: "2023 Benelux Algorithm Programming Contest (BAPC 23)"
rating: 0
weight: 104790
solve_time_s: 75
verified: true
draft: false
---

[CF 104790D - Democratic Naming](https://codeforces.com/problemset/problem/104790/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 15s  
**Verified:** yes  

## Solution
## Problem Understanding

Every city in the new county has a name of the same length. The county's final name is chosen one character at a time. For each position, every city votes for the letter that appears at that position in its own name. The letter with the highest number of votes becomes the corresponding letter of the county name. If several letters receive the same highest number of votes, the alphabetically smallest one is selected.

The input consists of the number of cities, the common length of every city name, and then the names themselves. The required output is the single name produced by applying the voting rule independently at every character position.

The constraints are fairly small. There are at most 1000 city names, each containing at most 1000 characters. This means there are at most one million input characters in total. Any algorithm that processes each character once or a constant number of times easily fits within typical contest limits. Algorithms that repeatedly rescan all strings for every possible answer would still be acceptable here, but there is no reason to do extra work when a direct counting solution exists.

The first non-obvious edge case is a tie between multiple letters. Consider the input

```
2 1
b
a
```

Both letters receive one vote, so the correct output is

```
a
```

A careless implementation that simply keeps the first maximum encountered would incorrectly output `b`.

Another case is when every city has the same name. For example,

```
3 4
code
code
code
```

The answer must be

```
code
```

Since every position has unanimous agreement, no tie-breaking logic should interfere.

A final case is when every position has a different winner. For example,

```
3 3
abc
bbc
cac
```

The output is

```
abc
```

Each column must be processed independently. Combining information from different positions would produce the wrong result.

## Approaches

The most direct solution is to process each position separately. For one column, count how many times each letter appears among all city names, then choose the letter with the highest frequency. If several letters have the same frequency, choose the alphabetically smallest one. Repeating this for all positions produces the required answer.

This approach already performs only one pass over every input character. Since there are at most one million characters, the total work is about one million counting operations plus checking the 26 lowercase letters for every position. That is easily fast enough.

The key observation is that every character position is completely independent from every other position. The decision for the first letter never affects the decision for the second letter. Because the alphabet contains only 26 lowercase letters, maintaining a frequency array of size 26 for each column is both simple and efficient.

| Approach | Time Complexity | Space Complexity | Verdict |
|---|---:|---:|---|
| Brute Force | O(n × m × 26) | O(26) | Accepted |
| Optimal | O(n × m + 26 × m) | O(26) | Accepted |

Although both rows have essentially the same asymptotic complexity because the alphabet size is constant, the frequency-counting formulation is the natural and intended solution.

## Algorithm Walkthrough

1. Read the values of `n` and `m`, then store all city names.

2. Create an empty list that will hold the characters of the final county name.

3. For every character position from `0` to `m - 1`, create a frequency array of length 26 initialized to zero.

4. Visit every city name and increment the counter corresponding to the letter appearing at the current position.

   Each city contributes exactly one vote to the current column, so after this pass the frequency array contains the complete election result for that position.

5. Scan the 26 counters in alphabetical order and keep track of the letter with the largest frequency.

   Because the scan is performed from `'a'` to `'z'`, updating the answer only when a strictly larger frequency is found automatically keeps the alphabetically smallest letter whenever frequencies are tied.

6. Append the selected letter to the answer.

7. After all positions have been processed, join the collected letters into a string and print it.

### Why it works

For every position, the algorithm counts exactly how many votes every possible letter receives. These counts exactly match the definition of the election. Choosing the letter with the largest count satisfies the majority rule, and scanning letters in alphabetical order guarantees that ties are resolved in favor of the smallest letter. Since every position is processed independently, every character of the constructed name is correct, making the entire output correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m = map(int, input().split())
names = [input().strip() for _ in range(n)]

answer = []

for col in range(m):
    freq = [0] * 26

    for name in names:
        freq[ord(name[col]) - ord('a')] += 1

    best = 0
    for i in range(1, 26):
        if freq[i] > freq[best]:
            best = i

    answer.append(chr(best + ord('a')))

print("".join(answer))
```

The program begins by reading all city names so every column can be accessed efficiently.

For each column, it creates a fresh frequency array with one entry for every lowercase letter. Every city contributes one vote by incrementing the appropriate counter.

The variable `best` stores the index of the current winning letter. The scan begins with `'a'` as the initial candidate. The comparison uses `>` instead of `>=`. This detail is what implements the tie-breaking rule. When two letters have equal frequency, the earlier one in the alphabet remains selected because it was encountered first.

Finally, the chosen letters are converted back into characters, collected in a list, and joined into the final county name.

## Worked Examples

### Sample 1

Input

```
3 5
apple
maple
alpha
```

| Position | Letters | Winning letter | Answer so far |
|---:|---|---|---|
| 0 | a, m, a | a | a |
| 1 | p, a, l | a | aa |
| 2 | p, p, p | p | aap |
| 3 | l, l, h | l | aapl |
| 4 | e, e, a | e | aaple |

The final answer is `aaple`. The second column demonstrates the tie-breaking rule. The letters `a`, `l`, and `p` each appear once, so the smallest letter, `a`, is chosen.

### Sample 2

Input

```
3 4
icpc
back
laps
```

| Position | Letters | Winning letter | Answer so far |
|---:|---|---|---|
| 0 | i, b, l | b | b |
| 1 | c, a, a | a | ba |
| 2 | p, c, p | p | bap |
| 3 | c, k, s | c | bapc |

The final answer is `bapc`. Every column is processed independently, confirming that earlier decisions never affect later ones.

## Complexity Analysis

| Measure | Complexity | Explanation |
|---|---:|---|
| Time | O(n × m + 26 × m) | Every input character is counted once, then 26 counters are checked for each column. |
| Space | O(26) | Only one frequency array of fixed size is needed besides the input. |

The total number of processed characters is at most one million, and each character is handled exactly once. The extra scan over 26 letters per column is negligible. The algorithm comfortably fits within the problem constraints.

## Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline

    n, m = map(int, input().split())
    names = [input().strip() for _ in range(n)]

    ans = []

    for col in range(m):
        freq = [0] * 26
        for name in names:
            freq[ord(name[col]) - ord('a')] += 1

        best = 0
        for i in range(1, 26):
            if freq[i] > freq[best]:
                best = i

        ans.append(chr(best + ord('a')))

    print("".join(ans))

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out

# provided samples
assert run("3 5\napple\nmaple\nalpha\n") == "aaple\n", "sample 1"
assert run("3 4\nicpc\nback\nlaps\n") == "bapc\n", "sample 2"

# minimum size
assert run("1 1\nz\n") == "z\n", "single city"

# tie breaking
assert run("2 1\nb\na\n") == "a\n", "alphabetical tie"

# all equal
assert run("3 3\ncat\ncat\ncat\n") == "cat\n", "identical names"

# different winners per column
assert run("3 3\nabc\nbbc\ncac\n") == "abc\n", "independent columns"
```

| Test input | Expected output | What it validates |
|---|---|---|
| One city with one letter | `z` | Minimum input size |
| Two names `b` and `a` | `a` | Alphabetical tie-breaking |
| Three identical names | Same name | Unanimous voting |
| `abc`, `bbc`, `cac` | `abc` | Each column handled independently |

## Edge Cases

Consider the tie-breaking example.

```
2 1
b
a
```

The frequency array for the only column becomes `[1, 1, 0, ..., 0]`. The scan starts with `'a'` as the current winner. When `'b'` is examined, its frequency is equal rather than larger, so the winner is not changed. The output is correctly `a`.

Now consider unanimous voting.

```
3 4
code
code
code
```

Every column contains only one distinct letter. The frequency arrays each have a single maximum, so the selected letters are `c`, `o`, `d`, and `e`. The algorithm outputs `code` exactly as expected.

Finally, consider different winners in different columns.

```
3 3
abc
bbc
cac
```

The first column has frequencies `{a:1, b:1, c:1}`, so `a` wins by alphabetical order. The second column has `b` appearing twice, making it the winner. The third column has `c` in every name, making it unanimous. The algorithm never mixes information between columns, producing the correct answer `abc`.
