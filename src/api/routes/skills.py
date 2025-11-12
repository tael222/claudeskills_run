"""Skills API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.models import Skill, SkillCreate, SkillListResponse, SkillResponse
from src.core.database import get_async_db
from src.core.logger import logger

router = APIRouter()


@router.get("", response_model=SkillListResponse)
async def list_skills(
    skip: int = 0,
    limit: int = 100,
    enabled_only: bool = False,
    db: AsyncSession = Depends(get_async_db),
) -> SkillListResponse:
    """List all skills."""
    try:
        query = select(Skill)

        if enabled_only:
            query = query.where(Skill.enabled == True)

        query = query.offset(skip).limit(limit).order_by(Skill.name)

        result = await db.execute(query)
        skills = result.scalars().all()

        count_query = select(Skill)
        if enabled_only:
            count_query = count_query.where(Skill.enabled == True)

        count_result = await db.execute(count_query)
        total = len(count_result.scalars().all())

        return SkillListResponse(
            skills=[SkillResponse.model_validate(s) for s in skills], total=total
        )
    except Exception as e:
        logger.error(f"Failed to list skills: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list skills: {str(e)}",
        )


@router.post("", response_model=SkillResponse, status_code=status.HTTP_201_CREATED)
async def create_skill(
    skill_data: SkillCreate,
    db: AsyncSession = Depends(get_async_db),
) -> SkillResponse:
    """Create a new skill."""
    try:
        # Check if skill already exists
        result = await db.execute(select(Skill).where(Skill.name == skill_data.name))
        existing = result.scalar_one_or_none()

        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Skill '{skill_data.name}' already exists",
            )

        skill = Skill(
            name=skill_data.name,
            display_name=skill_data.display_name,
            description=skill_data.description,
            version=skill_data.version,
            config=skill_data.config,
            source_path=skill_data.source_path,
            source_url=skill_data.source_url,
            prompts=skill_data.prompts,
            examples=skill_data.examples,
        )

        db.add(skill)
        await db.commit()
        await db.refresh(skill)

        logger.info(f"Created skill: {skill.name} (ID: {skill.id})")
        return SkillResponse.model_validate(skill)
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"Failed to create skill: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create skill: {str(e)}",
        )


@router.get("/{skill_id}", response_model=SkillResponse)
async def get_skill(
    skill_id: int,
    db: AsyncSession = Depends(get_async_db),
) -> SkillResponse:
    """Get skill by ID."""
    try:
        result = await db.execute(select(Skill).where(Skill.id == skill_id))
        skill = result.scalar_one_or_none()

        if not skill:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Skill {skill_id} not found",
            )

        return SkillResponse.model_validate(skill)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get skill {skill_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get skill: {str(e)}",
        )
