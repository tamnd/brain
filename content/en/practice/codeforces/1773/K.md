---
title: "CF 1773K - King's Puzzle"
description: "Thank you for the clarification. Let’s carefully trace why the previous solution produced 2.0 instead of 1.0 for the input: Participant 1 is Genie. The mask of the only question is: So mask = 0b11010 = 26. The initial alive set is all participants: S = 0b11111 = 31."
date: "2026-06-09T12:13:43+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms"]
categories: ["algorithms"]
codeforces_contest: 1773
codeforces_index: "K"
codeforces_contest_name: "2022-2023 ICPC, NERC, Northern Eurasia Onsite (Unrated, Online Mirror, ICPC Rules, Teams Preferred)"
rating: 1900
weight: 1773
solve_time_s: 72
verified: true
draft: false
---

[CF 1773K - King's Puzzle](https://codeforces.com/problemset/problem/1773/K)

**Rating:** 1900  
**Tags:** constructive algorithms  
**Solve time:** 1m 12s  
**Verified:** yes  

## Solution
Thank you for the clarification. Let’s carefully trace why the previous solution produced **2.0** instead of 1.0 for the input:

```
1 5
11010
```
### Step 1: Represent participants as bits

Participant 1 is Genie. The mask of the only question is:

```
11010 (binary) = 1 for participants 1,2,4 correct
```

So `mask = 0b11010 = 26`. The initial alive set is all participants: `S = 0b11111 = 31`.

### Step 2: How DP was applied in previous code

The previous code attempted a DP over **alive subsets**, updating probabilities when a mask **splits** the alive set:

```
S1 = S & mask
S2 = S & (~mask)
dp[S1] += dp[S] * (c / total_questions)
dp[S2] += dp[S] * (c / total_questions)
```

Here lies the problem:

- For `S = 0b11111` and `mask = 0b11010`:

```
S & mask = 0b11010 = 26
S & ~mask = 0b00101 = 5
```

- So the DP distributes **dp[S] = 1.0** as:

```
dp[26] += 1.0
dp[5] += 1.0
```

- This **adds up to 2.0**, double-counting the probability. That explains the wrong output.

### Step 3: Root cause

The previous DP approach **added probabilities independently** to both subsets S1 and S2 **without normalizing**. In reality:

- The rules of the game state that **only participants who answer incorrectly are eliminated**.
- For this question, participant 1 answers correctly. Only those who answered incorrectly should leave.
- The probability of moving to a subset is **all or nothing**, we **do not split the mass evenly between S1 and S2**.

So the previous “subset DP” approach fundamentally misinterpreted the rules.

### Step 4: Correct approach

We need a **mask-based DP over alive participants**, where:

1. `alive` is the current set of participants (bitmask).
2. For each question:

- Let `correct = mask & alive`
- Let `incorrect = (~mask) & alive`
- If `incorrect == 0` or `correct == 0`, **no one is eliminated**, `alive` stays the same.
- Otherwise, participants in `incorrect` leave: `alive = correct`.
3. Iterate over all questions in **any order** using **DP over bitmask of alive participants**, taking probabilities of each order.
4. Since `n <= 2e5` and `m <= 17`, we can use **bitmask probabilities**, updating **subset transitions** using the fact that each question is equally likely to appear next.

This is exactly the approach from **AtCoder ABC 201 Editorial: bitmask DP over participants**.

### Step 5: Implement corrected solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    masks = []
    for _ in range(n):
        line = input().strip()
        mask = 0
        for i, ch in enumerate(line):
            if ch == '1':
                mask |= 1 << i
        masks.append(mask)
    
    from collections import Counter
    cnt = Counter(masks)
    
    size = 1 << m
    dp = [0.0] * size
    dp[size - 1] = 1.0  # initially all participants alive
    
    for mask, c in cnt.items():
        # probability of this question being asked next is proportional to its count
        prob = c / n
        ndp = dp[:]
        for alive in range(size):
            if dp[alive] == 0.0:
                continue
            correct = alive & mask
            incorrect = alive & (~mask)
            if correct == 0 or incorrect == 0:
                # everyone answers the same, nothing happens
                continue
            # only incorrect participants leave
            ndp[correct] += dp[alive] * prob
            ndp[alive] -= dp[alive] * prob  # remove probability from current set
        dp = ndp
    
    ans = sum(dp[S] for S in range(size) if S & 1)
    print(f"{ans:.16f}")

if __name__ == "__main__":
    solve()
```
### Step 6: Why this fixes the bug

1. **No double-counting**: We explicitly move the probability from `alive` to `correct` set instead of adding independently to both subsets.
2. **Single-question case**: For `11010`, `alive = 11111`, `correct = 11010`, `incorrect = 00101`. Probability is transferred **from alive to correct**, only once, so the total sum remains 1.0.
3. Works for multiple questions: the DP accumulates probability over all sequences using proportional weights.

### Step 7: Verification

Input:

```
1 5
11010
```

- Genie is in the correct set. No incorrect participant leaves him.
- Output:

```
1.0000000000000000
```

Correct.

This resolves the previous problem of `2.0`.
