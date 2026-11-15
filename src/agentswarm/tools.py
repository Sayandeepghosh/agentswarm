import ast
import operator
import re
from abc import ABC, abstractmethod
from typing import Dict, Any, Callable, Type
from bs4 import BeautifulSoup
import httpx

class BaseTool(ABC):
    name: str
    description: str

    @abstractmethod
    def run(self, **kwargs) -> Dict[str, Any]:
        pass

class WebFetcherTool(BaseTool):
    name = "web_fetcher"
    description = "Fetches a URL, strips boilerplate, and extracts title, headers, and body text."

    def run(self, url: str, timeout_seconds: int = 6) -> Dict[str, Any]:
        if not url.startswith(("http://", "https://")):
            return {"status": "error", "message": "Invalid URL protocol. Must start with http:// or https://"}

        try:
            with httpx.Client(timeout=timeout_seconds, follow_redirects=True) as client:
                resp = client.get(url, headers={"User-Agent": "AgentSwarm/0.1 (Research Bot)"})
                resp.raise_for_status()
                soup = BeautifulSoup(resp.text, "html.parser")

                for tag in soup(["script", "style", "nav", "footer", "header", "noscript"]):
                    tag.decompose()

                title = soup.title.string.strip() if soup.title and soup.title.string else "Untitled"
                text = " ".join(soup.get_text().split())

                return {
                    "status": "success",
                    "url": url,
                    "title": title,
                    "content_sample": text[:1500],
                    "total_chars": len(text)
                }
        except Exception as e:
            return {"status": "error", "message": f"Network fetch failed: {str(e)}"}

class CalculatorTool(BaseTool):
    name = "calculator"
    description = "Performs safe arithmetic calculations using AST parsing."

    _operators: Dict[Type[ast.AST], Callable] = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
    }

    def _eval(self, node: ast.AST) -> float:
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return float(node.value)
        elif isinstance(node, ast.BinOp):
            left = self._eval(node.left)
            right = self._eval(node.right)
            op_type = type(node.op)
            if op_type in self._operators:
                return float(self._operators[op_type](left, right))
        elif isinstance(node, ast.UnaryOp):
            operand = self._eval(node.operand)
            op_type = type(node.op)
            if op_type in self._operators:
                return float(self._operators[op_type](operand))
        raise ValueError(f"Unsupported mathematical expression node: {type(node)}")

    def run(self, expression: str) -> Dict[str, Any]:
        # Sanitize
        clean_expr = re.sub(r"[^0-9+\-*/().\s]", "", expression)
        if not clean_expr.strip():
            return {"status": "error", "message": "Empty or invalid mathematical expression."}

        try:
            parsed = ast.parse(clean_expr, mode="eval")
            result = self._eval(parsed.body)
            return {"status": "success", "expression": clean_expr, "result": round(result, 4)}
        except Exception as e:
            return {"status": "error", "message": f"Calculation error: {str(e)}"}

class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}
        self.register(WebFetcherTool())
        self.register(CalculatorTool())

    def register(self, tool: BaseTool) -> None:
        self._tools[tool.name] = tool

    def get(self, name: str) -> BaseTool:
        if name not in self._tools:
            raise KeyError(f"Tool '{name}' is not registered. Available: {list(self._tools.keys())}")
        return self._tools[name]

    def execute(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        tool = self.get(tool_name)
        return tool.run(**kwargs)
