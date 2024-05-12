# AHC-tester

忘れた時のための覚書

## `ahc_settings.py`

`parallel_tester.py`, `optimizer.py` のための設定ファイル。
以下のものを書く。

### 共通

- コンパイルコマンド
  - `compile_command = 'g++ ./main.cpp -O2 -std=c++20'` など
- 実行コマンド
  - `execute_command = './a.out'` など
- 入力ファイル(リスト)
  - `input_file_names = [f'./in/{str(i).zfill(4)}.txt' for i in range(100)]` など
  - `optimizer` 用の時は、テストケースを減らすとよいかも
- 評価関数 `get_score`

### `optimizer` 用
- `study_name`
  - `study_name = 'test'` など
  - `study_name` が既にある場合、そのデータベースが利用される。
- `direction`
  - `direction = 'maximize'` など
  - minimize / maximize
- `multi_run` の `cpu_count`
  - `n_jobs_multi_run = 10` など
  - 多くしたい
- optuna の試行回数
  - `n_trials = 50` など
- optuna の `cpu_count`
  - `n_jobs_optuna = 1` など
  - 増やし過ぎには注意
- 推定するもの
  - `objective(trial: optuna.trial.Trial) -> tuple:`
  - 返り値のタプルはコマンドライン引数として渡す順番にする

## `parallel_tester.py`

テストケースを並列実行します。

例：
```
python3 ./parallel_tester.py -c -v -njobs 10
```

### コマンドライン引数
- `-c`
  - コンパイルします。
- `-v`
  - ログを表示します。
- `-njobs`
  - cpu数を指定します。

## `optimizer.py`

optuna を用いてパラーメタ探索をして、よしなに出力します。

例：
```
python3 ./oprimizer.py
```
