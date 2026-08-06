---
name: docker-mounted-workspace
description: Find the Docker container that bind-mounts the current workspace, map its path, and run build, test, or inspection commands inside it.
---

# Docker Mounted Workspace

Use this skill when the user is working through Docker but the current Codex thread is attached to the host workspace. The goal is to discover the matching running container from the current working directory, convert the host path to the container path, and run the requested command there.

## Quick Start

1. Resolve the current host workspace path with `pwd`.
2. Use `scripts/docker_workspace_exec.py` to find the running container whose bind mount best matches that path.
3. Run the requested command inside that container instead of on the host.

Preferred command form:

```bash
python3 scripts/docker_workspace_exec.py --workdir "$PWD" -- make
```

Pass explicit shell commands when needed:

```bash
python3 scripts/docker_workspace_exec.py --workdir "$PWD" --shell "make clean && make && ./mdriver -V"
```

## Workflow

### 1. Confirm the workspace path

Run `pwd` from the project directory. Do not guess the host path.

### 2. Discover the container

Run the helper script with `--workdir "$PWD"` first. The script:

- lists running containers with `docker ps`
- inspects each container's mounts
- keeps bind mounts whose source is an ancestor of the workspace path
- prefers the longest matching source path
- computes the in-container working directory by replacing the host prefix with the container destination

When the user has multiple plausible containers, prefer the best match from the script output instead of inventing a name.

### 3. Execute inside the container

Use the script to run the command in the resolved in-container working directory.

Common patterns:

```bash
python3 scripts/docker_workspace_exec.py --workdir "$PWD" -- make
python3 scripts/docker_workspace_exec.py --workdir "$PWD" -- ctest --output-on-failure
python3 scripts/docker_workspace_exec.py --workdir "$PWD" --shell "./configure && make test"
```

### 4. Report the resolved container path

When you run a command, mention:

- the chosen container name
- the resolved in-container working directory
- the command you ran or summarized outcome

This makes follow-up debugging easier when the container name changes later.

## Operational Rules

- Prefer running build, test, and runtime commands through the helper script once the user indicates Docker is the source of truth.
- Treat missing Docker permission as an execution blocker and request escalation rather than falling back silently to host builds.
- Prefer `--` for simple argv-safe commands like `make`, `cargo test`, `npm test`, or `pytest`.
- Prefer `--shell` only when shell operators such as `&&`, pipes, globs, or environment variable assignments are required.
- If no running container matches the current workspace path, say that clearly and include the host path you tried to match.
- If the container exists but the target directory is missing inside the container, stop and report the mismatch instead of guessing another path.

## Resources

### `scripts/docker_workspace_exec.py`

Use this helper for both discovery and execution. It supports:

- `--workdir PATH` to target a host workspace
- `--print-match` to only print the resolved container and container path
- `--shell CMD` to run a shell command inside the container
- `-- COMMAND ...` to run a command without shell quoting issues

Run `--print-match` first when you want to explain the mapping before execution.
