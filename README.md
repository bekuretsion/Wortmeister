# WortMeister — German vocabulary trainer

Run `node server.cjs` in this folder, then open http://localhost:8765.
No dependencies, API keys, accounts, or paid services are needed. You can also open index.html directly, but a local server provides a consistent browser origin for saved progress.

If localhost does not resolve in the app preview, use http://127.0.0.1:8765. Use one address consistently: browser progress is stored separately for each origin.

The dark interface follows the supplied LexiMaster screenshot, with direct Flashcards, Quiz, Listen and Pronounce pages. The German sounds guide includes listening examples. Pronounce can record up to 30 seconds for manual comparison with the reference voice; it requires microphone permission. Recordings stay temporary in the browser and are discarded when navigating away. There is no automatic pronunciation scoring.

This independent starter follows the supplied LexiMaster concept: daily spaced review, searchable vocabulary, flashcards, meaning quizzes, listening/spelling, a saved-word collection, personal entries and notes, progress statistics, and JSON backup/import. The interface and explanations are English; the vocabulary and examples are German.

The 77 original starter entries include noun articles/plurals, verb principal forms, usage patterns and example translations. A1–C1 bands are approximate, not a certified CEFR list. The collection covers everyday life, travel, work, technology, academic language, philosophy and faith. It is not a translation of the original 43,273-entry corpus. Expand `words.js` to add reviewed entries.

German speech requires an installed browser/device German voice. No English recordings are reused. The app reports when no German voice is available. Progress stays in this browser; export backups regularly. Import validates the backup and asks before replacing existing progress. Spaced repetition uses a simplified SM-2-inspired schedule; “Again” schedules tomorrow, and practice mistakes make words due immediately.

The supplied reference source is extracted under `leximaster-main/` for reference and is not served or required by WortMeister. Reference authorship remains with its original author. No original vocabulary corpus, audio, author biography, or pronunciation diagrams are presented as German content.

Verification: `node --test tests/core.test.cjs`.

## Das A und O collection

The user-provided PDF has been imported into a separate book collection with 490 extracted expression entries and 747 individual word entries. The expressions retain German explanations and examples, with printed page and chapter references. Individual words have independent English literal glosses and source forms, with reciprocal links to their expressions. Word forms and grammatical words are included; some are kept as separate source forms rather than fully lemmatized dictionary entries. Noun genders and full morphology are not inferred from idioms.

The cover advertises 500 expressions; the table extraction yields 490 entries. The alphabetical index is used to identify and split table rows, not to pad the collection to the advertised count. OCR can contain mistakes. Three entries whose examples were not recovered from the OCR use newly written examples. Exercises and illustrations are not imported. Source: Katja Ullmann and Carlos Ampie Loria, *Das A und O · Deutsche Redewendungen*, Ernst Klett Sprachen, 2009.

## German-English dictionary collection

The second user-supplied PDF contributes 16,192 German entries derived from 13,026 retained German-English translation groups. Tigrinya text and transliteration fields are excluded. German alternatives are split into entries and exact duplicate German/article combinations are combined. All source senses and printed/PDF page references remain available on the entry page; German alternatives in a group share the complete English equivalent group rather than guessed one-to-one sense alignment. Articles are retained when the source's gender markers support them. Plurals and example sentences are not invented.

The import includes vocabulary, phrases, geographical names, abbreviations and 488 lookup-only explanatory entries. Source explanations are excluded from review and quizzes. Text extraction is automatic and not a fully proofread German dictionary edition. The source contains 13,288 translation separators; 13,090 pairs were recovered, and source-letter/transliteration fragments or unusable fields were excluded during the build. The audit records unmatched separators and excluded rows; full source coverage is not claimed. Source: Yaroslav Gutgarts and Filip Busau, Harrassowitz Verlag, ISBN 9783447119870.

Rebuild using `extract_dictionary.py` and `build_dictionary.py`. Inspect `dictionary-data.json` and `dictionary-import-audit.json`, run `node --test tests/core.test.cjs tests/book.test.cjs tests/dictionary.test.cjs`, then `node prepare-publish.cjs`. Browsing renders 100 results at a time and searches all imported English senses. Dictionary levels are labeled “Dictionary,” not assigned speculative CEFR bands.

Rebuild with the bundled Python: `extract_index.py`, `extract_rows.py`, then `build_book.py`. `book-data.json` is the inspectable generated dataset; `book.js` is its browser form. `book-glosses.txt` contains original English literal glosses. Source PDF and intermediate extracted pages stay local. Validate with `node --test tests/*.test.cjs`. `node prepare-publish.cjs` prepares the static site files.

The Subjects page groups all 29 domains into Everyday German, Advanced & subjects, Bible vocabulary, and Bible names, with live counts and multiple domains per entry. The saved study scope applies to daily review, new-word selection, word of the day, browsing and all practice modes. Bible names are excluded unless the Bible names scope is selected. The German examples are original study sentences, not quotations from or translations of the RSV; no exhaustive biblical name-frequency coverage is claimed.
