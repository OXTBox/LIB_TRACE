# LIB_TRACE: notes for Claude Code

Read `README.md`. Keep handlers pure. Compile-check with
`~/projects/LIB_MCP/tools/lcmcp compile livecode/lib_trace.livecodescript` and run
`python3 tests/run_tests.py` (real LiveCode) after every change.

A loop in a traced handler hangs the LIB_MCP standalone: keep the step limit in any
outline-following loop. If a test hangs, kill it with `taskkill.exe /IM xt3d_MCP.exe /F`
and delete `C:\LIB_MCP\devtoken_8767.txt`; the next call starts a fresh one.
