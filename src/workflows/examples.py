"""Example workflows."""

import asyncio
from pathlib import Path
from typing import Any

from src.workflows.base import BaseWorkflow


class EchoWorkflow(BaseWorkflow):
    """Simple echo workflow for testing."""

    async def run(self) -> dict[str, Any]:
        """
        Echo the input message.

        Expected parameters:
            message (str): Message to echo

        Returns:
            Dictionary with echoed message
        """
        parameters = self.workflow.parameters or {}
        message = parameters.get("message", "Hello, World!")

        # Simulate some work
        await asyncio.sleep(1)

        return {
            "message": message,
            "echoed_at": self.workflow.started_at.isoformat() if self.workflow.started_at else None,
            "workflow_id": self.workflow_id,
        }


class FileOperationsWorkflow(BaseWorkflow):
    """Workflow for file operations."""

    async def run(self) -> dict[str, Any]:
        """
        Perform file operations.

        Expected parameters:
            operation (str): Operation type (create, read, delete)
            path (str): File path
            content (str, optional): Content for create operation

        Returns:
            Operation result
        """
        parameters = self.workflow.parameters or {}
        operation = parameters.get("operation")
        file_path = parameters.get("path")

        if not operation or not file_path:
            raise ValueError("Both 'operation' and 'path' parameters are required")

        path = Path(file_path)
        result = {"operation": operation, "path": str(path)}

        if operation == "create":
            content = parameters.get("content", "")
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
            result["status"] = "created"
            result["size"] = len(content)

        elif operation == "read":
            if not path.exists():
                raise FileNotFoundError(f"File {path} not found")
            content = path.read_text()
            result["status"] = "read"
            result["content"] = content
            result["size"] = len(content)

        elif operation == "delete":
            if path.exists():
                path.unlink()
                result["status"] = "deleted"
            else:
                result["status"] = "not_found"

        else:
            raise ValueError(f"Unknown operation: {operation}")

        return result


class DataProcessingWorkflow(BaseWorkflow):
    """Workflow for simple data processing."""

    async def run(self) -> dict[str, Any]:
        """
        Process data array.

        Expected parameters:
            data (list): Array of numbers
            operation (str): Operation (sum, average, max, min)

        Returns:
            Processing result
        """
        parameters = self.workflow.parameters or {}
        data = parameters.get("data", [])
        operation = parameters.get("operation", "sum")

        if not isinstance(data, list):
            raise ValueError("'data' must be a list")

        # Convert to numbers
        try:
            numbers = [float(x) for x in data]
        except (ValueError, TypeError) as e:
            raise ValueError(f"All data items must be numeric: {e}")

        if not numbers:
            return {"operation": operation, "result": None, "count": 0}

        # Perform operation
        if operation == "sum":
            result_value = sum(numbers)
        elif operation == "average":
            result_value = sum(numbers) / len(numbers)
        elif operation == "max":
            result_value = max(numbers)
        elif operation == "min":
            result_value = min(numbers)
        else:
            raise ValueError(f"Unknown operation: {operation}")

        return {
            "operation": operation,
            "result": result_value,
            "count": len(numbers),
            "data_preview": numbers[:5],  # First 5 items
        }
