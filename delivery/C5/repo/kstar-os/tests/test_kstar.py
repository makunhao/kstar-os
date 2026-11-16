#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""KSTAR OS 的回归测试：只测可观察行为，不测内部实现。

每个用例把仓库复制到临时目录再跑，避免污染真实记忆。
运行：python3 -m unittest discover -s tests -v
"""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


class KstarTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / "repo"
        shutil.copytree(REPO, self.root,
                        ignore=shutil.ignore_patterns(".git", "logs", "__pycache__", "tests", "*.pyc"))
        self.script = self.root / "scripts" / "kstar.py"

    def tearDown(self):
        self.tmp.cleanup()

    def kstar(self, *args, code=0):
        p = subprocess.run([sys.executable, str(self.script), *args],
                           capture_output=True, text=True, cwd=self.root)
        self.assertEqual(p.returncode, code, msg=f"stdout={p.stdout}\nstderr={p.stderr}")
        return p.stdout

    # ---------------------------------------------------------------- status
    def test_status_reports_five_layers(self):
        out = self.kstar("status")
        for word in ("L1", "L2", "L3", "L4", "L5"):
            self.assertIn(word, out)

    # ---------------------------------------------------------------- L1
    def test_capture_writes_daily_file(self):
        self.kstar("capture", "今天发现了一个渲染 bug", "--tag", "test")
        files = list((self.root / "memory" / "L1_raw").glob("*.md"))
        self.assertTrue(files)
        self.assertIn("渲染 bug", files[0].read_text(encoding="utf-8"))

    # ---------------------------------------------------------------- L2
    def test_episode_computes_delta(self):
        self.kstar("episode", "--title", "测试经验", "--situation", "s", "--task", "t",
                   "--action", "a", "--result", "r", "--lesson", "l",
                   "--expected", "0.8", "--actual", "0.5")
        idx = json.loads((self.root / "memory" / "L2_episodes" / "episodes.json").read_text(encoding="utf-8"))
        last = idx[-1]
        self.assertEqual(last["title"], "测试经验")
        self.assertAlmostEqual(last["delta"], -0.3, places=3)
        body = (self.root / "memory" / "L2_episodes" / last["file"]).read_text(encoding="utf-8")
        self.assertIn("-0.300", body)

    # ---------------------------------------------------------------- L3
    def test_skill_use_increments_counter(self):
        self.kstar("skill-new", "demo-skill", "--desc", "演示用技能")
        self.kstar("skill-use", "demo-skill", "--context", "单测", "--outcome", "成功", "--delta", "-0.1")
        usage = json.loads((self.root / "memory" / "L3_skills" / "demo-skill" / "usage.json").read_text(encoding="utf-8"))
        self.assertEqual(len(usage["uses"]), 1)
        self.assertEqual(usage["uses"][0]["outcome"], "成功")

    def test_skill_use_rejects_unknown_skill(self):
        out = self.kstar("skill-use", "no-such-skill", "--context", "x", "--outcome", "y", code=2)
        self.assertIn("没有这个技能", out)

    def test_skill_iteration_is_recorded(self):
        self.kstar("skill-new", "iter-skill", "--desc", "迭代测试")
        self.kstar("skill-iter", "iter-skill", "--frm", "0.1", "--to", "0.2",
                   "--why", "第一次用就发现步骤缺前提", "--effect", "补了输入检查")
        usage = json.loads((self.root / "memory" / "L3_skills" / "iter-skill" / "usage.json").read_text(encoding="utf-8"))
        self.assertEqual(len(usage["iterations"]), 1)
        self.assertTrue((self.root / "memory" / "L3_skills" / "iter-skill" / "iterations.md").exists())

    # ---------------------------------------------------------------- recall
    def test_recall_finds_skill_by_keyword(self):
        self.kstar("skill-new", "render-fix", "--desc", "修复渲染输出问题")
        out = self.kstar("recall", "渲染")
        self.assertIn("render-fix", out)

    # ---------------------------------------------------------------- reflect / export
    def test_reflect_outputs_mean_delta(self):
        out = self.kstar("reflect", "--since", "1970-01-01")
        self.assertIn("平均 ΔR", out)

    def test_export_html_is_self_contained(self):
        target = self.root / "logs" / "dash.html"
        out = self.kstar("export-html", "--out", str(target))
        html = target.read_text(encoding="utf-8")
        self.assertIn("<html", html)
        self.assertNotIn("http://", html)
        self.assertNotIn("https://", html)
        self.assertIn("KSTAR OS", out + html)


if __name__ == "__main__":
    unittest.main(verbosity=2)
