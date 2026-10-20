#!/usr/bin/env python3
import argparse
import json
import sys

NPD_LIMIT = 2_400_000
IP_FIXED_CONTRIBUTION_2026 = 57_390
IP_PCT_THRESHOLD = 300_000


def calc(income: float, b2b_share: float):
    b2b_part = income * (b2b_share / 100)
    b2c_part = income - b2b_part
    npd_tax = b2b_part * 0.06 + b2c_part * 0.04
    npd_available = income <= NPD_LIMIT

    ip_tax = income * 0.06 + IP_FIXED_CONTRIBUTION_2026 + max(0, income - IP_PCT_THRESHOLD) * 0.01

    return {
        "income": income,
        "b2b_share_pct": b2b_share,
        "npd": {
            "available": npd_available,
            "tax": round(npd_tax, 2) if npd_available else None,
            "net": round(income - npd_tax, 2) if npd_available else None,
        },
        "ip_usn": {
            "tax": round(ip_tax, 2),
            "net": round(income - ip_tax, 2),
        },
        "npd_limit": NPD_LIMIT,
    }


def fmt(n):
    return f"{n:,.0f}".replace(",", " ")


def format_table(result, crypto):
    lines = []
    income = result["income"]
    npd, ip = result["npd"], result["ip_usn"]
    lines.append(f"Годовой доход: {fmt(income)} ₽")
    lines.append("")
    if npd["available"]:
        lines.append(f"НПД (самозанятый): налог {fmt(npd['tax'])} ₽, на руки {fmt(npd['net'])} ₽")
    else:
        lines.append("НПД (самозанятый): недоступен — доход выше лимита 2 400 000 ₽/год")
    lines.append(f"ИП на УСН 6%:      налог+взносы {fmt(ip['tax'])} ₽, на руки {fmt(ip['net'])} ₽")
    lines.append("")

    if not npd["available"]:
        lines.append(f"При этом доходе доступен только ИП: на руки {fmt(ip['net'])} ₽")
    elif npd["net"] >= ip["net"]:
        diff = npd["net"] - ip["net"]
        lines.append(f"Выгоднее: самозанятость (на {fmt(diff)} ₽ больше на руки)")
    else:
        diff = ip["net"] - npd["net"]
        lines.append(f"Выгоднее: ИП (на {fmt(diff)} ₽ больше на руки)")

    if crypto:
        lines.append("")
        lines.append(
            "Внимание: доход в USDT/крипте от иностранного клиента на НПД — серая правовая\n"
            "зона с 418-ФЗ (с 2025 года формально НПД не распространяется на доходы от\n"
            "операций с криптовалютой). Для регулярного крипто-дохода предсказуемость ИП\n"
            "может быть важнее разницы в налоге, показанной выше."
        )

    lines.append("")
    lines.append(
        "Упрощённый расчёт для одиночного фрилансера без сотрудников и без региональных\n"
        "льгот по УСН. Не налоговая консультация — проверьте текущие ставки у бухгалтера\n"
        "или на сайте ФНС перед решением."
    )
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Сравнить налог НПД (самозанятый) и налог+взносы ИП на УСН 6% при заданном годовом доходе (цифры 2026 года)."
    )
    parser.add_argument("--income", type=float, required=True, help="Годовой доход в рублях")
    parser.add_argument(
        "--b2b-share",
        type=float,
        default=80.0,
        help="Доля дохода от компаний/ИП (не физлиц), %% — влияет на ставку НПД 6%% vs 4%% (по умолчанию 80)",
    )
    parser.add_argument(
        "--crypto",
        action="store_true",
        help="Доход (целиком или частично) приходит в USDT/крипте от иностранного клиента — добавляет предупреждение про 418-ФЗ",
    )
    parser.add_argument("--json", action="store_true", help="Вывод в формате JSON вместо таблицы")
    args = parser.parse_args()

    if args.income < 0:
        print("--income не может быть отрицательным", file=sys.stderr)
        sys.exit(1)
    if not (0 <= args.b2b_share <= 100):
        print("--b2b-share должен быть в диапазоне 0-100", file=sys.stderr)
        sys.exit(1)

    result = calc(args.income, args.b2b_share)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_table(result, args.crypto))


if __name__ == "__main__":
    main()
