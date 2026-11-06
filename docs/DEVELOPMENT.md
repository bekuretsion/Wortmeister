# Development

The app runs without a build step or third-party JavaScript dependencies. Browser storage keys and vocabulary entry IDs remain stable when files move.

- `app/`: application logic and collection views, loaded in the order listed in `index.html`.
- `seeds/`: browser datasets, inspectable JSON datasets, and vocabulary glosses.
- `static/css/`: shared interface styles.
- `tests/`: Node test-runner checks for review behavior, vocabulary integrity, and linked entries.
- `docs/audits/`: extraction reports.
- `tools/`: extraction and dataset builders, local server, and deployment preparation.

From the repository root:

```sh
node tools/server.cjs
node --test tests/core.test.cjs tests/book.test.cjs tests/dictionary.test.cjs
node tools/prepare-publish.cjs
```

Python extraction scripts require `pdfplumber` and access to the locally supplied PDFs. Intermediate files are kept under the ignored `tmp/` directory. Run `tools/extract_index.py` and `tools/extract_rows.py` before `tools/build_book.py`; run `tools/extract_dictionary.py` before `tools/build_dictionary.py`. Builders write datasets to `seeds/` and audit reports to `docs/audits/`.

`publish/` is generated output. It is not the source tree. The allowlisted local server exposes only website assets.
