from typing import Iterable, Callable
import argparse
from logging import getLogger, basicConfig
import subprocess
import multiprocessing
import time
import math
import os
import shutil
import csv
from functools import partial
import datetime
from ahc_settings import AHCSettings

logger = getLogger(__name__)
basicConfig(
    format="%(asctime)s [%(levelname)s] : %(message)s",
    datefmt="%H:%M:%S",
    level=os.getenv("LOG_LEVEL", "INFO"),
)


def to_red(arg):
    return f"\u001b[31m{arg}\u001b[0m"


def to_green(arg):
    return f"\u001b[32m{arg}\u001b[0m"


class ParallelTester:
    """テストケース並列回し屋です。

    - 実行例(127並列)ahc_settings.pyを設定して以下のコマンドを実行

    ``$ python3 ./parallel_tester.py -c -v -njobs 127``
    """

    def __init__(
        self,
        compile_command: str,
        execute_command: str,
        input_file_names: list[str],
        cpu_count: int,
        verbose: bool,
        get_score: Callable[[list[float]], float],
    ) -> None:
        """
        Args:
            compile_command (str): コンパイルコマンドです。
            execute_command (str): 実行コマンドです。
                                    実行時引数は ``append_execute_command()`` メソッドで指定することも可能です。
            input_file_names (list[str]): 入力ファイル名のリストです。
            cpu_count (int): CPU数です。
            verbose (bool): ログを表示します。
            get_score (Callable[[list[float]], float]): スコアのリストに対して平均などを取って返してください。
        """
        self.compile_command = compile_command.split()
        self.execute_command = execute_command.split()
        self.input_file_names = input_file_names
        self.cpu_count = cpu_count
        self.verbose = verbose
        self.get_score = get_score

    def show_score(self, scores: list[float]) -> float:
        """スコアのリストを受け取り、 ``get_score`` 関数で計算します。
        ついでに表示もします。
        """
        score = self.get_score(scores)
        logger.info(f"Ave.{score}")
        return score

    def append_execute_command(self, args: Iterable[str]) -> None:
        """コマンドライン引数を追加します。"""
        for arg in args:
            self.execute_command.append(str(arg))

    def compile(self) -> None:
        """``compile_command`` よりコンパイルします。"""
        logger.info("compiling...")
        subprocess.run(
            self.compile_command,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True,
            check=True,
        )

    def _process_file(self, input_file: str) -> tuple[str, float]:
        """入力`input_file`を処理します。

        Returns:
            tuple[str, float]: ファイル名、スコア
        """
        with open(input_file, "r", encoding="utf-8") as f:
            input_text = "".join(f.read())
        try:
            result = subprocess.run(
                self.execute_command,
                input=input_text,
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE,
                text=True,
                check=True,
            )
            score_line = result.stderr.rstrip().split("\n")[-1]
            _, score = score_line.split(" = ")
            score = float(score)
            if self.verbose:
                logger.info(f"{input_file}: {score=}")

            # stderr
            filename = input_file[len("./in/") :]
            with open(
                f"{self.output_dir}/err/{filename}", "w", encoding="utf-8"
            ) as out_f:
                out_f.write(result.stderr)

            # stdout
            filename = input_file[len("./in/") :]
            with open(
                f"{self.output_dir}/out/{filename}", "w", encoding="utf-8"
            ) as out_f:
                out_f.write(result.stdout)

            return input_file, score
        except subprocess.CalledProcessError as e:
            # logger.exception(e)
            logger.error(to_red(f"Error occured in {input_file}"))
            return input_file, math.nan
        except Exception as e:
            logger.exception(e)
            logger.error(to_red(f"!!! Error occured in {input_file}"))
            return input_file, math.nan

    def run(self) -> list[float]:
        """実行します。"""
        pool = multiprocessing.Pool(processes=self.cpu_count)
        result = pool.map(
            partial(self._process_file), self.input_file_names, chunksize=1
        )
        pool.close()
        pool.join()
        scores = [s for _, s in result]
        return scores

    def run_record(self) -> list[tuple[str, float]]:
        """実行します。"""
        dt_now = datetime.datetime.now()

        self.output_dir = "./alltests/"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        self.output_dir += dt_now.strftime("%Y-%m-%d_%H-%M-%S")
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        if not os.path.exists(f"{self.output_dir}/err/"):
            os.makedirs(f"{self.output_dir}/err/")
        if not os.path.exists(f"{self.output_dir}/out/"):
            os.makedirs(f"{self.output_dir}/out/")

        pool = multiprocessing.Pool(processes=self.cpu_count)
        result = pool.map(
            partial(self._process_file), self.input_file_names, chunksize=1
        )
        pool.close()
        pool.join()

        # score
        result.sort()
        with open(
            f"{self.output_dir}/result.csv", "w", encoding="utf-8", newline=""
        ) as f:
            writer = csv.writer(f)
            writer.writerow(["filename", "score"])
            for filename, score in result:
                writer.writerow([filename, score])

        # 出力を`./out/`へも書き出す
        if not os.path.exists("./out/"):
            os.makedirs("./out/")
        for item in os.listdir(f"{self.output_dir}/out/"):
            src_path = os.path.join(f"{self.output_dir}/out/", item)
            dest_path = os.path.join("./out/", item)
            if os.path.isfile(src_path):
                shutil.copy2(src_path, dest_path)
            elif os.path.isdir(src_path):
                shutil.copytree(src_path, dest_path)

        return result

    @staticmethod
    def get_args() -> argparse.Namespace:
        """実行時引数を解析します。"""
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "-c",
            "--compile",
            required=False,
            action="store_true",
            default=False,
            help="if compile the file. default is `False`.",
        )
        parser.add_argument(
            "-v",
            "--verbose",
            required=False,
            action="store_true",
            default=False,
            help="show logs. default is `False`.",
        )
        parser.add_argument(
            "-njobs",
            "--number_of_jobs",
            required=False,
            type=int,
            action="store",
            default=1,
            help="set the number of cpu_count. default is `1`.",
        )
        return parser.parse_args()


def build_tester(
    settings: AHCSettings, njobs: int = 1, verbose: bool = False
) -> ParallelTester:
    """`ParallelTester` を返します

    Args:
        njobs (int, optional): cpu_count です。
        verbose (bool, optional): ログを表示します。

    Returns:
        ParallelTester: テスターです。
    """
    tester = ParallelTester(
        compile_command=settings.compile_command,
        execute_command=settings.execute_command,
        input_file_names=settings.input_file_names,
        cpu_count=min(njobs, multiprocessing.cpu_count() - 1),
        verbose=verbose,
        get_score=settings.get_score,
    )
    return tester


def main():
    """実行時引数をもとに、 ``tester`` を立ち上げ実行します。"""
    args = ParallelTester.get_args()
    njobs = min(args.number_of_jobs, multiprocessing.cpu_count() - 1)
    logger.info(f"{njobs=}")

    tester = build_tester(AHCSettings, njobs, args.verbose)

    if args.compile:
        tester.compile()

    logger.info("Start.")

    start = time.time()
    scores = tester.run_record()

    nan_case = []
    for filename, s in scores:
        if math.isnan(s):
            nan_case.append(filename)
    if nan_case:
        logger.info("=====================")
        logger.error(to_red(f"ErrorCount: {len(nan_case)}."))
        for f in nan_case:
            logger.error(to_red(f"  ErrorCase: {f}"))
        logger.info("=====================")
    else:
        logger.info(to_green("Finished correctly."))

    score = tester.show_score([s for _, s in scores])
    logger.info(f"Finished in {time.time() - start:.4f} sec.")
    return score


if __name__ == "__main__":
    main()
