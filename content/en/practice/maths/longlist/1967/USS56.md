---
title: "IMO 1967 LL USS56"
description: "In a group of interpreters each one speaks one or several foreign"
date: "2026-05-29T11:51:44+07:00"
tags: ["imo", "longlist", "mathematics", "olympiad"]
categories: ["mathematics"]
year: 1967
type: "longlist"
origin: "USS"
weight: 196700056
draft: false
---

# IMO 1967 LL USS56

**Origin:** USS

## Problem

In a group of interpreters each one speaks one or several foreign
languages; 24 of them speak Japanese, 24 Malay, 24 Farsi. Prove that it
is possible to select a subgroup in which exactly 12 interpreters speak
Japanese, exactly 12 speak Malay, and exactly 12 speak Farsi.

## Solution

We shall prove by induction on n the following statement: If in some group
of interpreters exactly n persons, n \geq2, speak each of the three languages,
then it is possible to select a subgroup in which each language is spoken
by exactly two persons.
The statement of the problem easily follows from this: it suﬃces to select
six such groups.

The case n = 2 is trivial. Let us assume n \geq2, and let Nj, Nm, Nf, Njm,
Njf, Nmf, Njmf be the sets of those interpreters who speak only Japanese,
only Malay, only Farsi, only Japanese and Malay, only Japanese and Farsi,
only Malay and Farsi, and all the three languages, respectively, and nj, nm,
nf, njm, njf, nmf, njmf the cardinalities of these sets, respectively. By the
condition of the problem, nj+njm+njf +njmf = nm+njm+nmf+njmf =
nf + njf + nmf + njmf = 24, and consequently
nj −nmf = nm −njf = nf −njm = c.
Now if c < 0, then njm, njf, nmf > 0, and it is enough to select one inter-
preter from each of the sets Njm, Njf, Nmf. If c > 0, then nj, nm, nf > 0,
and it is enough to select one interpreter from each of the sets Nj, Nm, Nf
and then use the inductive assumption. Also, if c = 0, then w.l.o.g.
nj = nmf > 0, and it is enough to select one interpreter from each of
the sets Nj, Nmf and then use the inductive hypothesis. This completes
the induction.
