from typing import Annotated
from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.middleware.middleware import get_db
from app.repositories.algoritme import AlgoritmeRepository


class RequireOwnership:
    def __init__(
        self,
        request: Request,
        db: Annotated[Session, Depends(get_db)],
    ):
        """
        Checks if the algorithm_id in the request is owned by organisation_id.
        """
        organisation_id = request.path_params.get("organisation_id", None)
        algorithm_id = request.path_params.get("algorithm_id", None)

        if algorithm_id is None:
            raise HTTPException(status_code=400, detail="Algorithm ID is required")

        algo_repo = AlgoritmeRepository(db)
        algo = algo_repo.get_by_lars(algorithm_id)
        if not algo:
            raise HTTPException(404)

        if algo.owner != organisation_id:
            raise HTTPException(403)
