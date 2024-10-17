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
        Checks if the algorithm_id in the request is owned by organisation_name.
        """
        organisation_name = request.path_params.get("organisation_name", None)
        algorithm_id = request.path_params.get("algorithm_id", None)

        algo_repo = AlgoritmeRepository(db)
        algo = algo_repo.get_by_lars(algorithm_id)
        if not algo:
            raise HTTPException(404)

        if algo.owner != organisation_name:
            raise HTTPException(403)
