import sys


def calculate_metrics(
    supported_claims: int,
    total_claims: int,
    covered_facts: int,
    total_reference_facts: int,
) -> tuple[float, float, float]:
    precision = supported_claims / total_claims if total_claims else 0.0
    recall = covered_facts / total_reference_facts if total_reference_facts else 0.0

    if precision + recall == 0:
        f1 = 0.0
    else:
        f1 = 2 * precision * recall / (precision + recall)

    return precision, recall, f1


if __name__ == "__main__":
    if len(sys.argv) != 5:
        raise SystemExit(
            "Usage: python3 metrics.py "
            "<supported_claims> <total_claims> "
            "<covered_facts> <total_reference_facts>"
        )

    precision, recall, f1 = calculate_metrics(
        int(sys.argv[1]),
        int(sys.argv[2]),
        int(sys.argv[3]),
        int(sys.argv[4]),
    )

    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1:        {f1:.4f}")
