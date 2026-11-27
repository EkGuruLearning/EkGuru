# India Language Inventory — Deep Audit (Phase 6)

Batch: southern-asia (pass 1) · Status: PRELIMINARY · Date: 2026-09-14

India is the inventory's anchor country (EkGuru's home market and all 10
production courses). This file is the Phase 6 deep audit: every Eighth Schedule
language verified against the Constitution, plus the structural facts that make
India the hardest country in the dataset (no census since 2011, the Hindi
umbrella, cross-border splits, classical-language politics).

## 1. Coverage

- Entries: **25** (22/22 Eighth Schedule + English + Bhojpuri + Indian Sign Language).
- Living languages (Ethnologue 27, medium confidence): **≈450**.
- 2011 Census mother tongues: **≈19,500 raw returns**, rationalised to 121
  languages + grouped "others". The rationalisation itself is a political act —
  see §5 (Hindi umbrella).

## 2. The 22 scheduled languages — entry table

| # | Language | 639-3 | Roles | Speakers (2011-based) | EkGuru |
|---|----------|-------|-------|----------------------|--------|
| 1 | Hindi | hin | official, widely-spoken, lingua-franca | 528M L1 (umbrella — §5) | course |
| 2 | Bengali | ben | national, official-regional, widely-spoken | 97M | course |
| 3 | Marathi | mar | national, official-regional, widely-spoken | 83M | course |
| 4 | Telugu | tel | national, official-regional, widely-spoken | 81M | course |
| 5 | Tamil | tam | national, official-regional, widely-spoken | 69M | course |
| 6 | Gujarati | guj | national, official-regional, widely-spoken | 55M | course |
| 7 | Urdu | urd | national, official-regional, widely-spoken | 51M | course |
| 8 | Kannada | kan | national, official-regional, widely-spoken | 44M | course |
| 9 | Odia | ory | national, official-regional, widely-spoken | 38M | **none** |
| 10 | Malayalam | mal | national, official-regional, widely-spoken | 35M | course |
| 11 | Punjabi (Eastern) | pan | national, official-regional, widely-spoken | 33M | course |
| 12 | Assamese | asm | national, official-regional, widely-spoken | 15M | **none** |
| 13 | Maithili | mai | national, widely-spoken | 14M (IN) + NP | none |
| 14 | Santali | sat | national | 7M | none |
| 15 | Kashmiri | kas | national, official-regional | 7M | none |
| 16 | Nepali | nep | national, official-regional | 3M (IN) | none |
| 17 | Sindhi | snd | national (no state) | 2.8M | none |
| 18 | Dogri | doi | national, official-regional | 2.6M | none |
| 19 | Konkani | kok | national, official-regional | 2.3M | none |
| 20 | Bodo | brx | national, official-regional | 1.5M | none |
| 21 | Manipuri (Meitei) | mni | national, official-regional | 1.8M | none |
| 22 | Sanskrit | san | national, liturgical, official-regional | 25k L1 (liturgical) | none |

Non-scheduled entries: English (eng — official via 1963 Act, pack),
Bhojpuri (bho — widely-spoken, ~51M, no course), Indian Sign Language
(ins — sign, medium confidence).

## 3. Gap analysis (EkGuru coverage)

Covered: 10/22 scheduled (all P0 "in production — maintain").
Uncovered, ranked by learner value:

1. **Odia (ory)** — 38M speakers, classical language (2014), state-official
   (Odisha). Largest uncovered scheduled language. Top course candidate.
2. **Assamese (asm)** — 15M, classical language (2024 batch), state-official
   (Assam). Top-2 course candidate.
3. **Bhojpuri (bho)** — ~51M, NOT scheduled, no state machinery, huge
   migrant-learner base (Delhi/Mumbai/Gulf). Non-obvious P1: demand without
   institutional support is exactly the gap a private course fills.
4. **Maithili (mai)** — 14M IN + NP second-language base; scheduled 2003,
   still no state official status anywhere (Bihar never adopted it).
   Cross-border (NP entry exists) — one pack serves both.
5. **Kashmiri (kas)** — official (J&K, 2020 Act), Perso-Arabic + Devanagari
   script split is the pedagogical crux. Cross-border (PK/AJK entry exists).
6. **Santali (sat)** — only Austroasiatic scheduled language; Ol Chiki script
   story; cross-border (BD entry exists).
7. **Nepali (nep)** — scheduled-macro treatment (§6); Sikkim/WB official.
   Shared planning with NP (npi) entry.
8. **Sindhi (snd)** — scheduled but stateless (no state official status
   post-Partition); Perso-Arabic vs Devanagari split. Shared with PK entry.
9. **Dogri / Konkani / Bodo / Manipuri** — small-base scheduled; pack-level.
   Konkani's five-script tradition is the teaching problem, not the size.
10. **Sanskrit (san)** — liturgical + classical + Uttarakhand second-official;
    learner demand is real (school/heritage) but pedagogy differs (classical
    language). Pack, not a conversational course.

## 4. Constitutional backbone (what the entries cite)

- **Arts. 343–344**: Hindi (Devanagari) = Union official language; English
  continues via the Official Languages Act 1963 (indefinite — the 1965
  switch-over never happened).
- **Art. 351**: duty to develop Hindi — the legal root of the Hindi umbrella (§5).
- **Eighth Schedule**: 22 languages (14 in 1950; +Sindhi 1967; +Konkani/Manipuri/
  Nepali 1992; +Bodo/Dogri/Maithili/Santali 2003). No additions since 2003
  despite demands (Bhojpuri, Rajasthani, Bhoti, …).
- **State official languages**: entries cite official-regional per state Acts
  (Bengali-WB, Marathi-MH, …). J&K: Official Languages Act 2020
  (Kashmiri/Dogri/Hindi/Urdu/English).
- **Classical languages** (cultural status, entries note it, no inventory role):
  Tamil 2004, Sanskrit 2005, Kannada/Telugu 2008, Malayalam 2013, Odia 2014,
  Marathi/Pali/Prakrit/Assamese/Bengali October 2024.

## 5. The Hindi umbrella (census artefact — do not take L1 at face value)

The 2011 figure "Hindi 528M" folds in Bhojpuri, Rajasthani varieties, Magahi,
Chhattisgarhi, Haryanvi, Braj, Awadhi, Bundeli, Bagheli, Garhwali, Kumaoni and
more — many with their own ISO codes and tens of millions of speakers.
Consequences for the inventory:

- `hin` speaker band uses the umbrella figure with a confidence penalty and an
  explicit note; learner Hindi = Khari Boli standard (variation note, Phase 10).
- Bhojpuri (bho) gets its own entry DESPITE being inside the umbrella, because
  demand + distinct code + 50M speakers clear the bar. It is the test case for
  the rule "census folding does not delete a language".
- Rajasthani (macro dispute), Magahi, Chhattisgarhi, Haryanvi sit in
  notesLongTail pending pass 2 — each is a Bhojpuri-class candidate.

## 6. Code treatments specific to India

- **Dogri macro**: `doi` is scope=M per SIL bulk (2026-09-14) — members dgo (individual) + xnr (Kangri).
  The census/Ethnologue Kangri-overlap debate is now grounded: overlap is with a macro MEMBER.
- **Nepali dual-code**: IN entry uses macro `nep` (India schedules the
  diaspora umbrella incl. Sikkim/WB varieties); NP/BT entries use individual
  `npi`. Same language, never merged silently (METHOD §Phase-4 note).
- **Punjabi split**: IN `pan` (Eastern, Gurmukhi) vs PK `pnb` (Western,
  Shahmukhi) — distinct codes AND scripts, cross-noted, never merged.
- **Konkani macro**: `kok` (macro; members incl. `gom` Goan Konkani).
  Five-script tradition; Goa mandates Devanagari.
- **Manipuri individual**: `mni` is scope=I per SIL bulk (2026-09-14) — the macro question is CLOSED,
  no member split exists. Course planning unblocked on codes.
- **Sanskrit**: `san` (SIL macro: cls + vsn; type=H Historical — relations carry HISTORICAL status);
  liturgical + national + official-regional (Uttarakhand).
- **Bodo**: `brx` (Boro); BTC official.
- **Sindhi**: `snd` (individual; Pakistan side same code, Perso-Arabic both).

## 7. Cross-border entries (shared planning)

| Language | IN code | Other side | Note |
|----------|---------|------------|------|
| Punjabi | pan | PK pnb | distinct code+script — separate courses, cross-notes |
| Kashmiri | kas | PK kas (AJK) | same code — one pack, script notes |
| Nepali | nep | NP/BT npi | same language — one course serves all |
| Sindhi | snd | PK snd | same code — one pack |
| Santali | sat | BD sat | same code — one pack |
| Bengali | ben | BD ben | same code — course exists, BD notes fold in |
| Urdu | urd | PK urd | same code — course exists |
| Tamil | tam | LK tam | variation note (Jaffna vs TN standard) |

## 8. Pass-2 verification list (India)

1. Rajasthani macro question (mwr vs umbrella) — census + Linguistic Survey of India.
2. Magahi/Chhattisgarhi/Haryanvi entries vs long-tail (threshold ruling).
3. `mni` macro question — CLOSED by SIL bulk (scope=I individual).
4. ISL (ins): ISLRTC + Deaf community sources; dialect spread (Delhi/Mumbai/
   Kolkata varieties vs one-code treatment).
5. Sanskrit L1 figure (25k, census "mother tongue" gaming is well documented).
6. Mizo (lus), Khasi (kha) state-official entries (currently long-tail).
7. Tulu (tcy) classical-demand watch.
8. Urdu script-note accuracy (course exists — check against course content).
9. 2021 Census never happened (COVID, then delays) — ALL 2011-based figures
   are 15 years stale; flag any course-planning use accordingly.
10. Pali/Prakrit classical-2024: confirm no-L1 liturgical treatment holds.
