import json
import subprocess
import sys

from ru_tax import calc


def run(args):
    return subprocess.run(
        [sys.executable, "ru_tax.py", *args], capture_output=True, text=True
    )


def test_npd_cheaper_below_limit_default_share():
    r = calc(1_200_000, 80)
    assert r["npd"]["available"] is True
    assert r["npd"]["net"] > r["ip_usn"]["net"]


def test_npd_unavailable_above_limit():
    r = calc(3_000_000, 80)
    assert r["npd"]["available"] is False
    assert r["npd"]["tax"] is None
    assert r["npd"]["net"] is None


def test_npd_available_at_exact_limit():
    r = calc(2_400_000, 100)
    assert r["npd"]["available"] is True


def test_ip_fixed_contribution_floor_at_zero_income():
    r = calc(0, 80)
    assert r["ip_usn"]["tax"] == 57_390
    assert r["ip_usn"]["net"] == -57_390


def test_ip_percent_threshold():
    r = calc(300_000, 0)
    assert r["ip_usn"]["tax"] == 300_000 * 0.06 + 57_390


def test_b2b_share_changes_npd_rate():
    all_b2b = calc(1_000_000, 100)
    all_b2c = calc(1_000_000, 0)
    assert all_b2b["npd"]["tax"] == 60_000
    assert all_b2c["npd"]["tax"] == 40_000


def test_cli_json_output_is_valid_json():
    result = run(["--income", "1200000", "--json"])
    assert result.returncode == 0
    data = json.loads(result.stdout)
    assert data["income"] == 1_200_000.0


def test_cli_table_output_mentions_both_regimes():
    result = run(["--income", "1200000"])
    assert result.returncode == 0
    assert "НПД" in result.stdout
    assert "ИП" in result.stdout


def test_cli_crypto_flag_adds_warning():
    with_crypto = run(["--income", "900000", "--crypto"])
    without_crypto = run(["--income", "900000"])
    assert "418-ФЗ" in with_crypto.stdout
    assert "418-ФЗ" not in without_crypto.stdout


def test_cli_rejects_negative_income():
    result = run(["--income", "-5"])
    assert result.returncode == 1
    assert "отрицательным" in result.stderr


def test_cli_rejects_out_of_range_b2b_share():
    result = run(["--income", "100", "--b2b-share", "150"])
    assert result.returncode == 1
    assert "0-100" in result.stderr


def test_cli_missing_required_income_exits_nonzero():
    result = run([])
    assert result.returncode != 0


def main():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"PASS: {t.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"FAIL: {t.__name__}: {e}")
    print(f"\n{len(tests) - failed}/{len(tests)} passed")
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
