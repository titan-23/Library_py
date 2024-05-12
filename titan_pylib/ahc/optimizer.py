import optuna
import time
from logging import getLogger, basicConfig
import os
import multiprocessing
from parallel_tester import ParallelTester, build_tester
from ahc_settings import AHCSettings

logger = getLogger(__name__)
basicConfig(
    format="%(asctime)s [%(levelname)s] : %(message)s",
    datefmt="%H:%M:%S",
    level=os.getenv("LOG_LEVEL", "INFO"),
)


class Optimizer:

    def __init__(self, settings: AHCSettings) -> None:
        self.settings: AHCSettings = settings
        self.path = f"./optimizer_results/{self.settings.study_name}"

    def optimize(self) -> None:
        if not os.path.exists(self.path):
            os.makedirs(self.path)

        tester: ParallelTester = build_tester(
            self.settings, njobs=self.settings.n_jobs_parallel_tester
        )
        tester.compile()

        start = time.time()

        study: optuna.Study = optuna.create_study(
            direction=self.settings.direction,
            study_name=self.settings.study_name,
            storage=f"sqlite:///{self.path}/{self.settings.study_name}.db",
            load_if_exists=True,
        )

        def _objective(trial: optuna.trial.Trial) -> float:
            tester: ParallelTester = build_tester(
                self.settings, njobs=self.settings.n_jobs_parallel_tester
            )
            args = self.settings.objective(trial)
            tester.append_execute_command(args)
            scores = tester.run()
            score = tester.get_score(scores)
            return score

        study.optimize(
            _objective,
            n_trials=self.settings.n_trials,
            n_jobs=min(self.settings.n_jobs_optuna, multiprocessing.cpu_count() - 1),
        )

        logger.info(study.best_trial)
        logger.info("writing results ...")
        self.output(study)
        logger.info(f"Finish parameter seraching. Time: {time.time() - start}sec.")

    def output(self, study: optuna.Study) -> None:
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        with open(f"{self.path}/result.txt", "w", encoding="utf-8") as f:
            logger.info(study.best_trial, file=f)

        img_path = self.path + "/images"
        if not os.path.exists(img_path):
            os.makedirs(img_path)

        fig = optuna.visualization.plot_contour(study)
        fig.write_html(f"{img_path}/contour.html")
        fig.write_image(f"{img_path}/contour.png")
        fig = optuna.visualization.plot_edf(study)
        fig.write_html(f"{img_path}/edf.html")
        fig.write_image(f"{img_path}/edf.png")
        fig = optuna.visualization.plot_optimization_history(study)
        fig.write_html(f"{img_path}/optimization_history.html")
        fig.write_image(f"{img_path}/optimization_history.png")
        fig = optuna.visualization.plot_parallel_coordinate(study)
        fig.write_html(f"{img_path}/parallel_coordinate.html")
        fig.write_image(f"{img_path}/parallel_coordinate.png")
        fig = optuna.visualization.plot_slice(study)
        fig.write_html(f"{img_path}/slice.html")
        fig.write_image(f"{img_path}/slice.png")


if __name__ == "__main__":
    optimizer: Optimizer = Optimizer(AHCSettings)
    optimizer.optimize()
