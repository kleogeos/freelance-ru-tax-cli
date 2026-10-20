# freelance-ru-tax-cli

![Test CLI](https://github.com/kleogeos/freelance-ru-tax-cli/actions/workflows/test.yml/badge.svg)

Compare Russian НПД (self-employed/"самозанятый") tax vs ИП on УСН 6% ("ИП на упрощёнке") for a given annual income, using 2026 rates and fixed contributions. No dependencies, no sign-up — just Python 3.

```bash
python3 ru_tax.py --income 1200000
```

```
Годовой доход: 1 200 000 ₽

НПД (самозанятый): налог 67 200 ₽, на руки 1 132 800 ₽
ИП на УСН 6%:      налог+взносы 138 390 ₽, на руки 1 061 610 ₽

Выгоднее: самозанятость (на 71 190 ₽ больше на руки)

Упрощённый расчёт для одиночного фрилансера без сотрудников и без региональных
льгот по УСН. Не налоговая консультация — проверьте текущие ставки у бухгалтера
или на сайте ФНС перед решением.
```

### Options

| Flag | Default | Meaning |
|---|---|---|
| `--income` | required | Годовой доход в рублях |
| `--b2b-share` | `80` | Доля дохода от компаний/ИП (не физлиц), % — влияет на ставку НПД: 6% с юрлиц/ИП, 4% с физлиц |
| `--crypto` | off | Доход приходит в USDT/крипте от иностранного клиента — добавляет предупреждение про 418-ФЗ |
| `--json` | off | Вывод в формате JSON вместо таблицы |

### What this does and doesn't cover

Covers the headline comparison for a solo freelancer with no employees: НПД tax rate (4%/6% depending on client type) against ИП on УСН "Доходы" 6% plus the 2026 fixed insurance contribution (57,390 ₽/year, due regardless of income) and the 1% surcharge on income above 300,000 ₽/year. Flags when income exceeds the 2.4M ₽/year НПД ceiling, where self-employment stops being legally available.

Does **not** cover regional УСН rate discounts, employees, УСН "Доходы минус расходы", or a definitive legal answer on crypto income under НПД — that's a genuinely unsettled grey area under 418-ФЗ (see the linked article below). This is a planning estimate, not tax or legal advice — rates and thresholds change yearly, verify current figures before deciding.

There's also a free [browser version](https://kleogeos.github.io/freelancer-tools/kalkulyator-samozanyatyy-ili-ip.html) with the same math, a [Node.js/npx port](https://github.com/kleogeos/freelance-ru-tax-js) if you'd rather not touch Python, a full [written breakdown](https://kleogeos.github.io/freelancer-tools/samozanyatyy-ili-ip-dlya-frilansera-2026.html) of НПД vs ИП for freelancers, a deeper dive on [getting paid in USDT as a самозанятый](https://kleogeos.github.io/freelancer-tools/mozhno-li-samozanyatomu-poluchat-oplatu-v-usdt.html), and more free tools (invoicing, rate calculator, contract checklist) at [Freelancer Toolbox](https://kleogeos.github.io/freelancer-tools/).

### Tests

```bash
python3 test_ru_tax.py
```

### License

MIT
