FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install --no-cache-dir .

COPY . .

ENTRYPOINT ["python", "-m", "agentswarm.cli"]
CMD ["Autonomous AI Voice Agents in 2026"]
