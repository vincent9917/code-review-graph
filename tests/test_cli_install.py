"""Tests for install CLI platform-specific behavior."""

from __future__ import annotations

import argparse
from pathlib import Path

from code_review_graph.cli import _handle_init


def _args(tmp_path: Path, platform: str) -> argparse.Namespace:
    return argparse.Namespace(
        repo=str(tmp_path),
        dry_run=False,
        platform=platform,
        no_skills=False,
        no_hooks=False,
    )


def test_handle_init_codex_installs_codex_only(monkeypatch, tmp_path, capsys):
    monkeypatch.setattr(
        "code_review_graph.incremental.find_repo_root",
        lambda: tmp_path,
    )
    monkeypatch.setattr(
        "code_review_graph.skills.install_platform_configs",
        lambda repo_root, target, dry_run=False: ["Codex"],
    )

    called = {
        "claude_skills": False,
        "codex_skills": False,
        "claude_hooks": False,
        "codex_hooks": False,
    }

    def _install_claude_skills():
        called["claude_skills"] = True
        return Path.home() / ".claude" / "skills"

    def _install_codex_skills():
        called["codex_skills"] = True
        return Path.home() / ".codex" / "skills"

    def _install_claude_hooks(repo_root):
        called["claude_hooks"] = True
        return Path.home() / ".claude" / "settings.json"

    def _install_codex_hooks(repo_root):
        called["codex_hooks"] = True
        return Path.home() / ".codex" / "hooks.json"

    monkeypatch.setattr("code_review_graph.skills.install_claude_skills", _install_claude_skills)
    monkeypatch.setattr("code_review_graph.skills.install_codex_skills", _install_codex_skills)
    monkeypatch.setattr("code_review_graph.skills.install_claude_hooks", _install_claude_hooks)
    monkeypatch.setattr("code_review_graph.skills.install_codex_hooks", _install_codex_hooks)

    # Mock detect so codex is detected but claude is not
    monkeypatch.setitem(
        __import__("code_review_graph.skills", fromlist=["PLATFORMS"]).PLATFORMS,
        "codex",
        {
            **__import__("code_review_graph.skills", fromlist=["PLATFORMS"]).PLATFORMS["codex"],
            "detect": lambda: True,
        },
    )
    monkeypatch.setitem(
        __import__("code_review_graph.skills", fromlist=["PLATFORMS"]).PLATFORMS,
        "claude",
        {
            **__import__("code_review_graph.skills", fromlist=["PLATFORMS"]).PLATFORMS["claude"],
            "detect": lambda: False,
        },
    )

    _handle_init(_args(tmp_path, "codex"))
    out = capsys.readouterr().out

    assert called["claude_skills"] is False
    assert called["codex_skills"] is True
    assert called["claude_hooks"] is False
    assert called["codex_hooks"] is True
    assert "Installed Codex hooks" in out
    assert "Installed Codex skills" in out


def test_handle_init_claude_installs_claude_only(monkeypatch, tmp_path, capsys):
    monkeypatch.setattr(
        "code_review_graph.incremental.find_repo_root",
        lambda: tmp_path,
    )
    monkeypatch.setattr(
        "code_review_graph.skills.install_platform_configs",
        lambda repo_root, target, dry_run=False: ["Claude Code"],
    )

    called = {
        "claude_skills": False,
        "codex_skills": False,
        "claude_hooks": False,
        "codex_hooks": False,
    }

    def _install_claude_skills():
        called["claude_skills"] = True
        return Path.home() / ".claude" / "skills"

    def _install_codex_skills():
        called["codex_skills"] = True
        return Path.home() / ".codex" / "skills"

    def _install_claude_hooks(repo_root):
        called["claude_hooks"] = True
        return Path.home() / ".claude" / "settings.json"

    def _install_codex_hooks(repo_root):
        called["codex_hooks"] = True
        return Path.home() / ".codex" / "hooks.json"

    monkeypatch.setattr("code_review_graph.skills.install_claude_skills", _install_claude_skills)
    monkeypatch.setattr("code_review_graph.skills.install_codex_skills", _install_codex_skills)
    monkeypatch.setattr("code_review_graph.skills.install_claude_hooks", _install_claude_hooks)
    monkeypatch.setattr("code_review_graph.skills.install_codex_hooks", _install_codex_hooks)

    monkeypatch.setitem(
        __import__("code_review_graph.skills", fromlist=["PLATFORMS"]).PLATFORMS,
        "claude",
        {
            **__import__("code_review_graph.skills", fromlist=["PLATFORMS"]).PLATFORMS["claude"],
            "detect": lambda: True,
        },
    )
    monkeypatch.setitem(
        __import__("code_review_graph.skills", fromlist=["PLATFORMS"]).PLATFORMS,
        "codex",
        {
            **__import__("code_review_graph.skills", fromlist=["PLATFORMS"]).PLATFORMS["codex"],
            "detect": lambda: False,
        },
    )

    _handle_init(_args(tmp_path, "claude"))
    out = capsys.readouterr().out

    assert called["claude_skills"] is True
    assert called["codex_skills"] is False
    assert called["claude_hooks"] is True
    assert called["codex_hooks"] is False
    assert "Installed Claude Code hooks" in out
    assert "Installed Claude Code skills" in out


def test_handle_init_all_detects_both(monkeypatch, tmp_path, capsys):
    monkeypatch.setattr(
        "code_review_graph.incremental.find_repo_root",
        lambda: tmp_path,
    )
    monkeypatch.setattr(
        "code_review_graph.skills.install_platform_configs",
        lambda repo_root, target, dry_run=False: ["Claude Code", "Codex"],
    )

    called = {
        "claude_skills": False,
        "codex_skills": False,
        "claude_hooks": False,
        "codex_hooks": False,
    }

    def _install_claude_skills():
        called["claude_skills"] = True
        return Path.home() / ".claude" / "skills"

    def _install_codex_skills():
        called["codex_skills"] = True
        return Path.home() / ".codex" / "skills"

    def _install_claude_hooks(repo_root):
        called["claude_hooks"] = True
        return Path.home() / ".claude" / "settings.json"

    def _install_codex_hooks(repo_root):
        called["codex_hooks"] = True
        return Path.home() / ".codex" / "hooks.json"

    monkeypatch.setattr("code_review_graph.skills.install_claude_skills", _install_claude_skills)
    monkeypatch.setattr("code_review_graph.skills.install_codex_skills", _install_codex_skills)
    monkeypatch.setattr("code_review_graph.skills.install_claude_hooks", _install_claude_hooks)
    monkeypatch.setattr("code_review_graph.skills.install_codex_hooks", _install_codex_hooks)

    monkeypatch.setitem(
        __import__("code_review_graph.skills", fromlist=["PLATFORMS"]).PLATFORMS,
        "claude",
        {
            **__import__("code_review_graph.skills", fromlist=["PLATFORMS"]).PLATFORMS["claude"],
            "detect": lambda: True,
        },
    )
    monkeypatch.setitem(
        __import__("code_review_graph.skills", fromlist=["PLATFORMS"]).PLATFORMS,
        "codex",
        {
            **__import__("code_review_graph.skills", fromlist=["PLATFORMS"]).PLATFORMS["codex"],
            "detect": lambda: True,
        },
    )

    _handle_init(_args(tmp_path, "all"))
    out = capsys.readouterr().out

    assert called["claude_skills"] is True
    assert called["codex_skills"] is True
    assert called["claude_hooks"] is True
    assert called["codex_hooks"] is True
    assert "Installed Claude Code hooks" in out
    assert "Installed Codex hooks" in out


def test_handle_init_dry_run_skips_skills_and_hooks(monkeypatch, tmp_path, capsys):
    monkeypatch.setattr(
        "code_review_graph.incremental.find_repo_root",
        lambda: tmp_path,
    )
    monkeypatch.setattr(
        "code_review_graph.skills.install_platform_configs",
        lambda repo_root, target, dry_run=False: ["Claude Code", "Codex"],
    )

    called = {
        "claude_skills": False,
        "codex_skills": False,
        "claude_hooks": False,
        "codex_hooks": False,
    }

    def _install_claude_skills():
        called["claude_skills"] = True
        return Path.home() / ".claude" / "skills"

    def _install_codex_skills():
        called["codex_skills"] = True
        return Path.home() / ".codex" / "skills"

    def _install_claude_hooks(repo_root):
        called["claude_hooks"] = True
        return Path.home() / ".claude" / "settings.json"

    def _install_codex_hooks(repo_root):
        called["codex_hooks"] = True
        return Path.home() / ".codex" / "hooks.json"

    monkeypatch.setattr("code_review_graph.skills.install_claude_skills", _install_claude_skills)
    monkeypatch.setattr("code_review_graph.skills.install_codex_skills", _install_codex_skills)
    monkeypatch.setattr("code_review_graph.skills.install_claude_hooks", _install_claude_hooks)
    monkeypatch.setattr("code_review_graph.skills.install_codex_hooks", _install_codex_hooks)

    args = argparse.Namespace(
        repo=str(tmp_path),
        dry_run=True,
        platform="all",
        no_skills=False,
        no_hooks=False,
    )

    _handle_init(args)
    out = capsys.readouterr().out

    assert called["claude_skills"] is False
    assert called["codex_skills"] is False
    assert called["claude_hooks"] is False
    assert called["codex_hooks"] is False
    assert "[dry-run]" in out
