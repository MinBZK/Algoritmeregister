from app.database.database import SessionLocal
from sqlalchemy import and_, exists, func, select
from app.util.logger import get_logger
from app.models import AlgoritmeVersion, ActionHistory
from collections import defaultdict

# python -m etl.jobs.remove_intermediate_concepts

# This script removes intermediate concepts from the algoritme_version table that are in the EXPIRED state,
# have never been published, and have no action history of being published.
# It also deletes their associated action history records.

# Initialize new independent logger
logger = get_logger(__name__)


def remove_concepts(db):
    # Get all algoritme ids
    algoritme_ids = db.scalars(select(AlgoritmeVersion.algoritme_id).distinct()).all()
    algos_to_be_removed = []
    removed_algos_by_id = defaultdict(list)

    for alg_id in algoritme_ids:
        # Get all alg_versions_records and their corresponding action history
        alg_versions_records = (
            db.query(AlgoritmeVersion)
            .join(
                ActionHistory, ActionHistory.algoritme_version_id == AlgoritmeVersion.id
            )
            .filter(AlgoritmeVersion.algoritme_id == alg_id)
            .order_by(ActionHistory.create_dt.asc())
            .all()
        )

        # Check if any alg_versions_records is published in current batch
        has_publications = any(
            alg_vers_record.state == "PUBLISHED"
            for alg_vers_record in alg_versions_records
        )

        # If no version is published, skip to next algoritme(id). Meaning there are no publications for this algoritme.
        if not has_publications:
            continue

        # Find timestamp of last published action
        last_published_action = (
            db.query(func.max(ActionHistory.create_dt))
            .filter(
                ActionHistory.operation == "published",
                ActionHistory.algoritme_version_id.in_(
                    [v.id for v in alg_versions_records]
                ),
            )
            .scalar()
        )
        # For each expired version, check if it was created before the last publication and was never published itself
        for alg_vers_record in alg_versions_records:
            if alg_vers_record.state != "EXPIRED":
                continue

            # Skip if created after last published
            version_created_at = (
                db.query(func.min(ActionHistory.create_dt))
                .filter(ActionHistory.algoritme_version_id == alg_vers_record.id)
                .scalar()
            )

            if last_published_action and version_created_at > last_published_action:
                continue  # It's a new concept created after the last published — keep it

            # Check if there was ever published (operation='published')
            was_published = db.query(
                exists().where(
                    and_(
                        ActionHistory.algoritme_version_id == alg_vers_record.id,
                        ActionHistory.operation == "published",
                    )
                )
            ).scalar()

            if was_published:
                continue

            logger.info(
                f"The following expired concepts from alg_version table with algo_vers_id {alg_vers_record.id} "
                f"(algoritme with algo_id {alg_id}) will be removed, because they are not published and have no "
                f"action history of being published: {alg_vers_record.name} with state {alg_vers_record.state}"
            )

            algos_to_be_removed.append(alg_vers_record.id)
            removed_algos_by_id[alg_id].append(alg_vers_record.id)

    if algos_to_be_removed:
        logger.info(
            f"Deleting {len(algos_to_be_removed)} expired concept alg_versions_records and their action histories"
        )

        # Delete all related action history records first
        db.query(ActionHistory).filter(
            ActionHistory.algoritme_version_id.in_(algos_to_be_removed)
        ).delete(synchronize_session=False)

        # Then delete the algoritme alg_versions_records
        db.query(AlgoritmeVersion).filter(
            AlgoritmeVersion.id.in_(algos_to_be_removed)
        ).delete(synchronize_session=False)

        db.commit()
    else:
        logger.info("No expired concept alg_versions_records found to delete.")

    if removed_algos_by_id:
        logger.info(
            "Summary of versions to be removed per algoritme_id: [algoritme_version_id]"
        )
        for alg_id, version_ids in removed_algos_by_id.items():
            logger.info(f"  algoritme_id {alg_id}: {version_ids}")


def main():
    logger.info(
        "Starting script for removing intermediate concepts without publication."
    )
    db = SessionLocal()
    remove_concepts(db)
    logger.info(
        "Finished script for removing intermediate concepts without publication."
    )
    db.close()

if __name__ == "__main__":
    main()
