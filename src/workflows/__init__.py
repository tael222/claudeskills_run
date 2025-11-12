"""Workflows module."""

from src.workflows.base import BaseWorkflow
from src.workflows.examples import DataProcessingWorkflow, EchoWorkflow, FileOperationsWorkflow
from src.workflows.executor import WorkflowExecutor, executor

# Register example workflows
executor.register("echo", EchoWorkflow)
executor.register("file_operations", FileOperationsWorkflow)
executor.register("data_processing", DataProcessingWorkflow)

__all__ = [
    "BaseWorkflow",
    "WorkflowExecutor",
    "executor",
    "EchoWorkflow",
    "FileOperationsWorkflow",
    "DataProcessingWorkflow",
]
