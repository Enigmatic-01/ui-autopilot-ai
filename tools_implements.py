import  os
from pydantic import BaseModel,Field
from langchain_core.tools import BaseTool
from typing import Type
from workspace import *
# -----------------------------
# READ DIRECTORY
# -----------------------------

class ReadDirInput(BaseModel):
    path: str = Field(description="Directory path inside workspace")


class ReadDirectoryTool(BaseTool):
    name: str = "read_directory"
    description: str = "List files and folders inside a directory"
    args_schema: Type[BaseModel] = ReadDirInput

    def _run(self, path: str):
        try:
            p = safe_path(path)

            if not p.exists():
                return "Directory does not exist"

            if not p.is_dir():
                return "Path is not a directory"

            return "\n".join(os.listdir(p)) or "Directory is empty"

        except Exception as e:
            return f"Error: {str(e)}"


# -----------------------------
# CREATE DIRECTORY
# -----------------------------

class CreateDirInput(BaseModel):
    path: str = Field(description="Directory path to create")


class CreateDirectoryTool(BaseTool):
    name: str = "create_directory"
    description: str = "Create a directory inside workspace"
    args_schema: Type[BaseModel] = CreateDirInput

    def _run(self, path: str):
        try:
            p = safe_path(path)

            if p.exists():
                return "Directory already exists"

            p.mkdir(parents=True, exist_ok=True)

            return f"Directory created: {path}"

        except Exception as e:
            return f"Error: {str(e)}"


# -----------------------------
# WRITE FILE
# -----------------------------

class WriteFileInput(BaseModel):
    path: str = Field(description="File path to write")
    content: str = Field(description="File content")


import shutil
from filelock import FileLock

class WriteFileTool(BaseTool):
    name: str = "write_file"
    description: str = "Write content to a file"
    args_schema: Type[BaseModel] = WriteFileInput

    def _run(self, **kwargs):

        if "content" not in kwargs:
            if "content:" in kwargs:
                kwargs["content"] = kwargs.pop("content:")
            elif "content " in kwargs:
                kwargs["content"] = kwargs.pop("content ")

       
        
        path = kwargs["path"].lstrip("/")  
        content = kwargs["content"]

        p = safe_path(path)

        # ensure parent directory exists
        p.parent.mkdir(parents=True, exist_ok=True)

        # file lock (prevents parallel write conflicts)
        lock = FileLock(str(p) + ".lock")

        with lock:

            if p.exists():
                if p.is_file():
                    p.unlink()
                elif p.is_dir():
                    shutil.rmtree(p)

            p.write_text(content, encoding="utf-8")

        return f"File written: {path}"
# -----------------------------
# READ FILE
# -----------------------------

class ReadFileInput(BaseModel):
    path: str = Field(description="File path to read")


class ReadFileTool(BaseTool):
    name: str = "read_file"
    description: str = "Read file content"
    args_schema: Type[BaseModel] = ReadFileInput

    def _run(self, path: str):
        try:
            p = safe_path(path)

            if not p.exists():
                return "File does not exist"

            if not p.is_file():
                return "Path is not a file"

            return p.read_text()

        except Exception as e:
            return f"Error: {str(e)}"


# -----------------------------
# LIST DIRECTORIES
# -----------------------------

class ListDirInput(BaseModel):
    path: str = Field(description="Directory path")


class ListDirectoriesTool(BaseTool):
    name: str = "list_directories"
    description: str = "List directories inside a path"
    args_schema: Type[BaseModel] = ListDirInput

    def _run(self, path: str):
        try:
            p = safe_path(path)

            if not p.exists():
                return "Directory does not exist"

            if not p.is_dir():
                return "Path is not a directory"

            dirs = [d.name for d in p.iterdir() if d.is_dir()]

            return "\n".join(dirs) or "No directories found"

        except Exception as e:
            return f"Error: {str(e)}"