---
title: "CF 106097G - Mortar Mayhem"
description: "I cannot safely write a correct full editorial yet because I still need to resolve a mismatch between the information I initially assumed and the actual statement. From the contest page, the real problem is: Each of the $n$ points (mortars) sits on a 2D grid."
date: "2026-06-25T11:58:43+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106097
codeforces_index: "G"
codeforces_contest_name: "UTPC Contest 10-1-25 Div. 1 (Advanced)"
rating: 0
weight: 106097
solve_time_s: 26
verified: false
draft: false
---

[CF 106097G - Mortar Mayhem](https://codeforces.com/problemset/problem/106097/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 26s  
**Verified:** no  

## Solution
I cannot safely write a correct full editorial yet because I still need to resolve a mismatch between the information I initially assumed and the actual statement.

From the contest page, the real problem is:

Each of the $n$ points (mortars) sits on a 2D grid. For every mortar $i$, we must choose another mortar $j$ that it “targets” according to a distance rule involving Manhattan distance and a threshold $d$, with tie-breaking by minimum distance and then minimum index. The intended difficulty comes from doing this efficiently for $n \le 10^5$, not by checking all pairs.

What is still unclear (and crucial for a correct editorial) is the exact targeting rule, because the statement snippet we have is incomplete/ambiguous in the part that defines which candidates are valid and what “closest enemy which is at least distance $d$” precisely means in combination with the sample behavior. The sample alone is not sufficient to reconstruct the intended condition reliably.

To avoid hallucinating a wrong solution (which would completely break the editorial), I need one of the following:

Either paste the full statement from Codeforces (especially the exact definition of when a mortar considers another as a valid target), or confirm that the rule is:

“each $i$ chooses the closest $j \ne i$ such that Manhattan distance $\ge d$, ties by smallest index.”

Once that is confirmed, I can produce the full senior-level editorial with:

a correct geometric reduction (this problem typically reduces to sorting in rotated coordinates or sweep-line with ordered sets / dominance structure),

a clear explanation of why naive $O(n^2)$ fails,

and a precise construction that passes $10^5$.

Send the missing rule and I’ll write the complete Codeforces-style editorial in the format you requested.
