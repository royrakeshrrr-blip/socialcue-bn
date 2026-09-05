# Dataset provenance

The experiment input is `SOCIALCUE-BN-GOLD-V1.0`, finalized on 2026-09-02.

- Instances: 450
- Message families: 150
- Variants per family: A/B/C
- DEVELOPMENT: 90 instances from 30 families
- TEST: 360 instances from 120 families
- Gold labels: 19 TUI, 210 TUMI, 221 APNI
- Gold answerability: all 450 `ANSWERABLE`
- Gold confidence: all 450 `HIGH`

The underlying messages began as AI-assisted authoring candidates and were subjected to two native-Bangla human reviews plus completed adjudication. The final labels in this package come from the completed reviewer/agreement/adjudication workflow. This provenance must not be rewritten as wholly human-originated authoring.

The source workbook is included as `SocialCue-BN_Gold_Benchmark_v1.0.xlsx`.

SHA-256 of the included workbook:

`033145da288aa6b38296d3a46f0f2f2e659003223e2a509f9625992673fafbaa`

The CSV exports preserve the workbook's 28 benchmark columns. The experiment runner sends only the message and the context fields permitted by the selected prompt condition; it never sends gold labels.
