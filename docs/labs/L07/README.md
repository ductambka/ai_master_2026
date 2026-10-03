# L07 — Evaluation harness độc lập model provider

Harness này đánh giá output JSONL của RAG/QA pipeline mà không import SDK, gọi
API, hoặc phụ thuộc provider cụ thể. Provider chỉ cần xuất hai file theo schema:

```json
{"id":"q1","relevant_ids":["d1"],"claims":[{"text":"Paris is the capital of France.","citation_ids":["d1"]}]}
{"id":"q1","retrieved_ids":["d1"],"claims":[{"text":"Paris is the capital of France.","citation_ids":["d1"]}]}
```

Gold records có `relevant_ids` và các claim chuẩn; prediction records có cùng
`id`, danh sách xếp hạng `retrieved_ids`, và claim/citation do provider sinh.
Claim citation được coi là được hỗ trợ khi citation dự đoán giao với citation
gold của claim khớp.
Mỗi claim gold chỉ được ghép một lần trong từng metric; output lặp cùng một
claim không thể làm tăng số claim gold được bao phủ.

## Chạy

```bash
python -m ai_master.cli evaluate \
  --gold docs/labs/L07/fixtures/gold.jsonl \
  --predictions docs/labs/L07/fixtures/predictions.jsonl \
  --output /tmp/l07-evaluation.json --k 2 --seed 7
```

Kết quả JSON có `version`, `seed`, SHA-256 `input_checksum`, recall@k, exact
citation coverage, semantic-lite citation coverage (Jaccard token overlap), và
unsupported-claim rate. Input rỗng hợp lệ và cho metric 0; JSON hỏng, schema
hỏng, ID trùng hoặc prediction không có trong gold bị từ chối.

## Giới hạn validity

Đây là metric lexical deterministic để regression testing, không phải phán
quyết chất lượng sự thật. Semantic-lite không hiểu phủ định, số liệu, đồng
nghĩa hay quan hệ entailment; cần human evaluation hoặc evaluator độc lập cho
kết luận chất lượng cuối cùng. Harness không gọi mạng/API.
