"""Workflow executor service."""

from typing import Any, Type

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.logger import logger
from src.workflows.base import BaseWorkflow


class WorkflowExecutor:
    """Workflow execution service."""

    def __init__(self):
        """Initialize workflow executor."""
        self.workflows: dict[str, Type[BaseWorkflow]] = {}

    def register(self, name: str, workflow_class: Type[BaseWorkflow]) -> None:
        """
        Register a workflow type.

        Args:
            name: Workflow name
            workflow_class: Workflow class
        """
        self.workflows[name] = workflow_class
        logger.info(f"Registered workflow: {name}")

    def get_workflow_class(self, name: str) -> Type[BaseWorkflow]:
        """
        Get workflow class by name.

        Args:
            name: Workflow name

        Returns:
            Workflow class

        Raises:
            KeyError: If workflow not found
        """
        if name not in self.workflows:
            raise KeyError(f"Workflow '{name}' not registered")

        return self.workflows[name]

    async def execute(self, db: AsyncSession, workflow_id: int, workflow_name: str) -> dict[str, Any]:
        """
        Execute a workflow.

        Args:
            db: Database session
            workflow_id: Workflow database ID
            workflow_name: Workflow type name

        Returns:
            Workflow execution result
        """
        workflow_class = self.get_workflow_class(workflow_name)
        workflow = workflow_class(db, workflow_id)
        return await workflow.execute()


# Global executor instance
executor = WorkflowExecutor()
