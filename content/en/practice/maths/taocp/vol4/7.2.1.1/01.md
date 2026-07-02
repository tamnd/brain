---
title: "TAOCP 7.2.1.1 Exercise 1"
description: "Introduce shifted variables $b_j = a_j - l_j$."
date: "2026-07-02T07:41:44+07:00"
tags: ["taocp", "mathematics", "algorithms", "volume-4", "simple"]
categories: ["mathematics"]
section: "7.2.1.1"
section_title: "Generating All n-Tuples"
chapter: 7
chapter_title: "Combinatorial Searching"
volume: 4
book_pages: "281–321"
exercise: 1
rating: "10"
category: "simple"
recommended: false
verified: true
solve_time_s: 54
weight: 7020101001
draft: false
---

[Section 7.2.1.1: Generating All n-Tuples](../)

**Exercise 1.** [*10*] [10] Explain how to generate all n-tuples (a1, . . . , an) in which lj ≤aj ≤uj, given
lower bounds lj and upper bounds uj for each component. (Assume that lj ≤uj.)

**Verified:** yes  
**Solve time:** 54s  

---

Introduce shifted variables $b_j = a_j - l_j$. The bounds $l_j \le a_j \le u_j$ become $0 \le b_j \le u_j - l_j$. Define $m_j = u_j - l_j + 1$, so each $b_j$ satisfies $0 \le b_j < m_j$. The problem reduces to generating all $n$-tuples $(b_1,\dots,b_n)$ in a mixed-radix system with radices $m_1,\dots,m_n$.

Apply Algorithm M of Section 7.2.1.1 to generate all $(b_1,\dots,b_n)$ by repeated increment in mixed radix, treating $(b_1,\dots,b_n)$ as digits of a number with radix sequence $m_j$. For each generated tuple, output $a_j = b_j + l_j$ for $1 \le j \le n$, which produces exactly the required set of $n$-tuples satisfying $l_j \le a_j \le u_j$. This completes the construction. ∎
