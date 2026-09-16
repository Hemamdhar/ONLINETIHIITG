"""Export sequence proxies and check split leakage from a prepared manifest."""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("sequence_metadata_v1.csv"))
    args = parser.parse_args()
    if not args.manifest.exists():
        report = {"status": "blocked", "reason": f"manifest_not_found:{args.manifest}"}
        args.output.with_suffix(".json").write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(json.dumps(report, indent=2))
        return 2
    records = json.loads(args.manifest.read_text(encoding="utf-8"))
    groups = defaultdict(set)
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["source_path", "dataset", "split", "group", "source_sha256"])
        writer.writeheader()
        for record in records:
            groups[record["group"]].add(record["split"])
            writer.writerow({key: record.get(key, "") for key in writer.fieldnames})
    overlap = {group: sorted(splits) for group, splits in groups.items() if len(splits) > 1}
    report = {"status": "ready", "records": len(records), "groups": len(groups), "cross_split_group_overlap": overlap}
    args.output.with_suffix(".json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if not overlap else 1


if __name__ == "__main__":
    raise SystemExit(main())
