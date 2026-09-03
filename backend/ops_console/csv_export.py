import csv
import io


def build_classification_csv(results) -> str:
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["customer_id", "timestamp", "amount", "reason_code", "bucket", "confidence", "source", "reasoning"])
    for r in results:
        w.writerow([r.customer_id, r.timestamp, r.amount, r.reason_code_raw, r.bucket, f"{r.confidence:.2f}", r.source, r.reasoning])
    return buf.getvalue()