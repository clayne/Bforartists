@echo off
echo Starting bforartists with GPU debugging and glitch workaround options, log files 
echo will be created in your temp folder, windows explorer will open after you 
echo close bforartists to help you find them.
echo.
echo If you report a bug on https://projects.blender.org you can attach these files
echo by dragging them into the text area of your bug report, please include both
echo blender_debug_output.txt and blender_system_info.txt in your report. 
echo.
pause
echo.
echo Starting bforartists and waiting for it to exit....
setlocal

set PYTHONPATH=
set DEBUGLOGS="%temp%\bforartists\debug_logs"
set VK_LOADER_DEBUG=all
mkdir "%DEBUGLOGS%" > NUL 2>&1

"%~dp0\bforartists" --debug --debug-gpu --debug-gpu-force-workarounds --python-expr "import bpy; bpy.context.preferences.filepaths.temporary_directory=r'%DEBUGLOGS%'; bpy.ops.wm.sysinfo(filepath=r'%DEBUGLOGS%\blender_system_info.txt')" > "%DEBUGLOGS%\blender_debug_output.txt" 2>&1 < %0
explorer "%DEBUGLOGS%"
