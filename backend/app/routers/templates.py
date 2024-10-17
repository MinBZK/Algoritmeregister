from fastapi import APIRouter, Depends, Path, HTTPException, status
from app import schemas
from app.controllers import get_template_summary, get_template_by_id
from app.middleware.authorisation.authoriser import AuthType, Authoriser

router = APIRouter()

output_schemas = schemas.get_all_output_schemas_union()


@router.get(
    "/{standard_version}",
    response_model=list[schemas.StandardSupplier],
    dependencies=[Depends(Authoriser(AuthType.BaseOnly))],
)
async def get_template_list(
    standard_version: str = Path(alias="standard_version"),
):
    standard_version_int = int(standard_version.replace(".", ""))
    if standard_version_int < 10:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ONLY_VERSION_1.0_AND_HIGHER_IS_AVAILABLE",
        )
    return get_template_summary(standard_version)


@router.get(
    "/{standard_version}/{id}",
    response_model=schemas.AlgoritmeVersionTemplate | None,
    dependencies=[Depends(Authoriser(AuthType.BaseOnly))],
)
async def get_one_template(
    standard_version: str = Path(alias="standard_version"),
    id: str = Path(alias="id"),
):
    standard_version_int = int(standard_version.replace(".", ""))
    if standard_version_int < 10:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ONLY_VERSION_1.0_AND_HIGHER_IS_AVAILABLE",
        )
    return get_template_by_id(standard_version, id)
