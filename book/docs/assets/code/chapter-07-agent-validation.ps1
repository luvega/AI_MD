$ErrorActionPreference = 'Stop'
python tools/validate_online_book.py --map book/book_map.toml --book-root book/docs --require-nature-refs --require-imagegen
python tools/graph_health.py . --json --stale-days 180 | Out-File book/docs/resources/latest-graph-health.json
python -m unittest discover -s tests
