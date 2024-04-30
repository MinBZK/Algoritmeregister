from fastapi import APIRouter, Depends, Path, HTTPException, status
from app import schemas, middleware
from app.controllers import get_template_summary, get_template_by_id

router = APIRouter()

output_schemas = schemas.get_all_output_schemas_union()


@router.get("/{standard_version}", response_model=list[schemas.StandardSupplier])
async def get_template_list(
    _: schemas.User = Depends(middleware.get_current_user),
    standard_version: str = Path(alias="standard_version"),
):
    if standard_version != "0.4.0":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="ONLY 0_4_0 AVAILABLE"
        )
    return get_template_summary(standard_version)


@router.get(
    "/{standard_version}/{id}",
    response_model=schemas.AlgoritmeVersionTemplate | None,
)
async def get_one_template(
    _: schemas.User = Depends(middleware.get_current_user),
    standard_version: str = Path(alias="standard_version"),
    id: str = Path(alias="id"),
):
    if standard_version != "0.4.0":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="ONLY 0_4_0 AVAILABLE"
        )
    return get_template_by_id(standard_version, id)
