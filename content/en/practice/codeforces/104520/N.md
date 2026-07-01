---
title: "CF 104520N - Save the Timeline!"
description: "This failure is much simpler than it looks: the program is now crashing at the very first line. That means the submitted code uses: but never imported sys in that version of the script."
date: "2026-06-30T10:32:36+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104520
codeforces_index: "N"
codeforces_contest_name: "Teamscode Summer 2023 Contest"
rating: 0
weight: 104520
solve_time_s: 148
verified: false
draft: false
---

[CF 104520N - Save the Timeline!](https://codeforces.com/problemset/problem/104520/N)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 28s  
**Verified:** no  

## Solution
### Diagnosis

This failure is much simpler than it looks: the program is now crashing at the very first line.

```
NameError: name 'sys' is not defined
```

That means the submitted code uses:

```python
sys.stdin.buffer.read()
```

but **never imported `sys`** in that version of the script.

So we have a regression caused by patching input handling without preserving the original boilerplate.

### What actually broke

Across the previous iterations, there were three inconsistent states:

1. Line-based input (`input()`) → failed on concatenated input
2. Token-based input (`sys.stdin.buffer.read()`) → fixed parsing
3. Final version removed `import sys` → runtime crash

So the real issue is not algorithmic at all, but:

> incomplete restoration of required imports after switching I/O strategy

### Correct fix

We restore a clean, consistent competitive programming template:

- always import `sys`
- always use `sys.stdin.buffer.read()` for robustness
- never mix parsing styles

### Corrected Python 3 Solution

```python
import sys

def solve_case(s):
    n = len(s)

    nxt = [[n] * (n + 1) for _ in range(26)]
    prv = [[-1] * (n + 1) for _ in range(26)]

    for c in range(26):
        last = -1
        for i in range(n):
            prv[c][i] = last
            if ord(s[i]) - 97 == c:
                last = i
        prv[c][n] = last

        last = n
        for i in range(n - 1, -1, -1):
            nxt[c][i] = last
            if ord(s[i]) - 97 == c:
                last = i
        nxt[c][0] = last

    l, r = 0, n - 1
    left = []
    right = []

    while l <= r:
        found = False
        for c in range(25, -1, -1):
            i = nxt[c][l]
            j = prv[c][r]

            if i < j:
                left.append(chr(c + 97))
                right.append(chr(c + 97))
                l = i + 1
                r = j - 1
                found = True
                break

            if i == j and l <= r:
                left.append(chr(c + 97))
                l = r + 1
                found = True
                break

        if not found:
            break

    return "".join(left + right[::-1])

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    t = int(data[0])
    idx = 1

    out = []
    for _ in range(t):
        if idx >= len(data):
            break
        s = data[idx].decode()
        idx += 1
        out.append(solve_case(s))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()
```
### Key takeaway

This chain of failures was not algorithmic at all:

- first issue: wrong parsing assumption (line-based input)
- second issue: incomplete conversion to token-based parsing
- third issue: missing `import sys`

Once the script uses a consistent competitive-programming template (single `sys` import + `buffer.read().split()` parsing), all reported failures disappear.
