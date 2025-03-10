import optuna

"""example
python3 ./parallel_tester.py -c -v -njobs 127

python3 ./oprimizer.py
g++ ./main.cpp -O2 -std=c++20 -o a.out -I./../../../Library_cpp
"""


class AHCSettings:
    """
    AHCテスターの設定ファイル

    https://github.com/titan-23/Library_py/tree/main/titan_pylib/ahc/readme.md
    """

    # parallel_tester -------------------- #
    compile_command = "g++ ./main.cpp -O2 -std=c++20 -o a.out -I./../../../Library_cpp"
    execute_command = "./a.out"
    input_file_names = [f"./in/{str(i).zfill(4)}.txt" for i in range(100)]
    timeout = None

    def get_score(scores: list[float]) -> float:
        return sum(scores) / len(scores) * 100

    # ------------------------------------ #

    # optimizer -------------------------- #
    # study_name
    study_name = "test"

    # direction: minimize / maximize
    direction = "minimize"

    # parallel_tester の cpu_count
    n_jobs_parallel_tester = 127

    # optuna の試行回数
    n_trials = 50

    # optuna の cpu_count
    n_jobs_optuna = 1

    def objective(trial: optuna.trial.Trial) -> tuple:
        # 返り値のタプルはコマンドライン引数として渡す順番にする
        start_temp = trial.suggest_float("start_temp", 1, 100, log=True)
        k = trial.suggest_float("k", 0.0001, 1, log=True)
        end_temp = start_temp * k
        return (start_temp, end_temp)

    # ------------------------------------ #
