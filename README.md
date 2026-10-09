# Оценка архитектурной документации, сгенерированной LLM

В OpenCode с помощью скилла `generate-docs` сгенерировали архитектурную документацию для OpenTelemetry Collector и Apache Commons CLI. Для каждого проекта использовали две модели: MiMo-V2.6-Flash Free и Space Bunny Free.

Затем скиллом `evaluate-docs` проверили документацию по исходному коду и общему эталону для каждого проекта. Документы Collector проверял MiMo, документы Commons CLI — Space Bunny. Всего выполнено четыре проверки.

## Результаты

Precision — доля подтверждённых утверждений; recall — покрытие эталонных фактов; F1 объединяет обе метрики.

| Проект | Генератор | Проверяющий | Precision | Recall | F1 |
|---|---|---|---:|---:|---:|
| Collector | MiMo | MiMo | 95,90% | 94,12% | 95,00% |
| Collector | Space Bunny | MiMo | 90,91% | 79,41% | 84,77% |
| Commons CLI | MiMo | Space Bunny | 92,63%* | 62,50% | 74,64%* |
| Commons CLI | Space Bunny | Space Bunny | 89,80% | 63,64% | 74,49% |

На Collector по этим проверкам лучший результат у MiMo; на Commons CLI результаты близки.

*В отчёте Commons CLI -> MiMo итоговые счётчики расходятся с таблицей. Здесь метрики пересчитаны по её вердиктам: 88 подтверждённых утверждений из 95, покрыто 55 фактов из 88. Оригинальный отчёт сохранён без изменений.*

## Исходные репозитории

- [OpenTelemetry Collector](https://github.com/open-telemetry/opentelemetry-collector/tree/7b425533dfa04ff0a0d3b384381979e945a69b2a) — коммит, использованный в проверках.
- [Apache Commons CLI](https://github.com/apache/commons-cli/tree/d95484f57dfa4b99ac9069bb3f44df680306e8e9) — коммит, использованный в проверках.

## Что где лежит

- [experiments/opentelemetry-collector/](experiments/opentelemetry-collector/) — материалы Collector.
- [experiments/commons-cli/](experiments/commons-cli/) — материалы Commons CLI.
- В папках каждого проекта: `documents/` — две сгенерированные документации; `evaluations/` — два отчёта; `reference-facts.md` — общий эталон.
- [skills/generate-docs/](skills/generate-docs/) — скилл генерации.
- [skills/evaluate-docs/](skills/evaluate-docs/) — скилл проверки и `metrics.py` для расчёта метрик.
