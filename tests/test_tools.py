from agentswarm.tools import CalculatorTool, WebFetcherTool, ToolRegistry

def test_calculator_tool_valid():
    calc = CalculatorTool()
    res = calc.run(expression="((6.8 / 1.4) ** (1 / 4) - 1) * 100")
    assert res["status"] == "success"
    assert round(res["result"], 2) == 48.46

def test_calculator_tool_invalid():
    calc = CalculatorTool()
    res = calc.run(expression="__import__('os').system('ls')")
    assert res["status"] == "error"

def test_tool_registry():
    registry = ToolRegistry()
    assert "calculator" in registry._tools
    assert "web_fetcher" in registry._tools
    output = registry.execute("calculator", expression="15 * 8")
    assert output["result"] == 120.0
