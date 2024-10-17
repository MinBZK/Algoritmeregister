import argparse

from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.models import AlgoritmeVersion


def migrate_versions(session: Session):
    """Remove trailing zeros from publication standards."""
    old_versions = ['0.1.0', '0.4.0', '1.0.0']
    for old_version in old_versions:
        new_version = old_version.rstrip('0').rstrip('.')
        print(f'Updating version: {old_version} -> {new_version}')
        (
            session.query(AlgoritmeVersion)
            .filter(AlgoritmeVersion.standard_version == old_version)
            .update({AlgoritmeVersion.standard_version: new_version})
        )
    session.commit()
    print('Migration complete')


def revert(session: Session):
    """Revert the migration."""
    new_versions = ['0.1', '0.4', '1.0']
    for new_version in new_versions:
        original_version = new_version + '.0'
        print(f'Reverting version: {new_version} -> {original_version}')
        (
            session.query(AlgoritmeVersion)
            .filter(AlgoritmeVersion.standard_version == new_version)
            .update({AlgoritmeVersion.standard_version: original_version})
        )
    session.commit()
    print('Revert complete')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=(
            "This script removes trailing zeros from publication standards in the AlgoritmeVersion database. "
            "By default, it performs the migration. "
            "Use the --revert option to revert the migration."
        )
    )
    parser.add_argument(
        '--revert',
        action='store_true',
        help='Use this option to revert back the stripped zeros.'
    )
    args = parser.parse_args()

    session = SessionLocal()
    if args.revert:
        revert(session)
    else:
        migrate_versions(session)
    session.commit()
    session.close()
