#!/usr/bin/env python3
"""Calculate transparent workload volume from a versioned profile."""

import argparse
from pathlib import Path

import yaml


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", default="production")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    profiles = yaml.safe_load((root / "configs/workload_profiles.yml").read_text())["profiles"]
    profile = profiles[args.profile]
    annual = int(profile["annual_input_bytes"])
    record_size = int(profile["average_compressed_record_bytes"])
    print(f"profile={args.profile}")
    print(f"annual_input_bytes={annual:,}")
    print(f"annual_input_pb_decimal={annual / 1e15:.3f}")
    print(f"estimated_records={annual // record_size:,}")
    print(f"average_bytes_per_second={annual / (365 * 24 * 3600):,.0f}")


if __name__ == "__main__":
    main()
