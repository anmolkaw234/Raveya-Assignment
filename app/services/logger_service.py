from sqlalchemy.orm import Session

from app.models.entities import PromptLog


class LoggerService:
    @staticmethod
    def log_prompt_response(
        db: Session,
        *,
        module: str,
        request_payload: dict,
        prompt_text: str,
        response_payload: dict,
    ) -> None:
        row = PromptLog(
            module=module,
            request_payload=request_payload,
            prompt_text=prompt_text,
            response_payload=response_payload,
        )
        db.add(row)
        db.commit()
