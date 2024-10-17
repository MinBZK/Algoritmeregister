import sys

sys.path.append("..")
from etl.logger import get_logger
from etl.jobs import broken_link_reporter, generate_html_figures
from scripts.archive import translate_algorithms, translate_organizations

logger = get_logger()


def run_jobs(log, task):
    logger.info(f"Starting {log}")
    task()
    logger.info(f"Finished {log}")


def main():
    run_jobs("generating broken link report", broken_link_reporter.main)
    run_jobs("generate_html_figures", generate_html_figures.main)
    run_jobs("check for untranslated algo descriptions", translate_algorithms.main)


if __name__ == "__main__":
    main()
