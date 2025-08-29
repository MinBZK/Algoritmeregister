import sys

sys.path.append("..")
from etl.logger import get_logger
from etl.jobs import broken_link_reporter, generate_html_figures, calculate_embeddings, remove_intermediate_concepts
from scripts.archive import translate_algorithms, translate_organizations, add_precomputed_values

logger = get_logger(__name__)


def run_jobs(log, task):
    logger.info(f"Starting {log}")
    task()
    logger.info(f"Finished {log}")


def main():
    run_jobs("Remove intermediate concepts", remove_intermediate_concepts.main)
    run_jobs("Update highlighted algorithms", add_precomputed_values.main)
    run_jobs("Calculate embeddings", calculate_embeddings.main)
    run_jobs("Generating broken link report", broken_link_reporter.main)
    run_jobs("Generate html figures", generate_html_figures.main)
    run_jobs("Check for untranslated algo descriptions", translate_algorithms.main)
    # run_jobs("Check for untranslated organisations", translate_organizations.main)
    


if __name__ == "__main__":
    main()
