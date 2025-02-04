from iaEditais.schemas.Guideline import Guideline, CreateGuideline
from uuid import UUID
from datetime import datetime
from iaEditais.schemas.Evaluation import Evaluation, CreateEvaluation
from iaEditais.repositories import TaxonomyRepository


def post_guideline(guideline: CreateGuideline) -> Guideline:
    guideline = Guideline(**guideline.model_dump())
    TaxonomyRepository.post_guideline(guideline)
    return guideline


def get_guidelines() -> list[Guideline]:
    guidelines = TaxonomyRepository.get_guidelines()
    return guidelines


def put_guideline(guideline: Guideline) -> Guideline:
    guideline.updated_at = datetime.now()
    TaxonomyRepository.put_guideline(guideline)
    return guideline


def delete_guideline(guideline_id) -> dict:
    TaxonomyRepository.delete_guideline(guideline_id)
    return {'message': 'Source deleted successfully'}


def post_evaluation(evaluation: CreateEvaluation) -> Evaluation:
    evaluation = Evaluation(**evaluation.model_dump())
    TaxonomyRepository.post_evaluation(evaluation)
    return evaluation


def get_evaluations(guideline_id: UUID = None) -> list[Evaluation]:
    return TaxonomyRepository.get_evaluations(guideline_id)


def put_evaluation(evaluation: Evaluation) -> Evaluation:
    return TaxonomyRepository.put_evaluation(evaluation)


def delete_evaluation(evaluation_id) -> dict:
    TaxonomyRepository.delete_evaluation(evaluation_id)
    return {'message': 'Source deleted successfully'}
