@echo on
@setlocal enableextensions

REM Perform preparation
set "path_ffmpeg=C:\SOFTWARE\ffmpeg\ffmpeg.exe"
set "path_Mpeg2BlockInspector=E:\SOFTWARE-Win11\MULTIMEDIA\Mpeg2BlockInspector\Mpeg2BlockInspector\src\x64\Release\Mpeg2BlockInspector.exe"
set "path_Stage1_Inspector_Analyzer=E:\SOFTWARE-Win11\MULTIMEDIA\Mpeg2BlockInspector\Mpeg2BlockInspector\src\Stage1_Inspector_Analyzer_v0_2.py"
REM
set "path_vspipe=D:\TEST\Vapoursynth_x64_R81\lib\site-packages\vapoursynth\vspipe.exe"
REM
REM set "blocky="
set "blocky=_blocky"
REM
set "path_vpy=E:\SOFTWARE-Win11\MULTIMEDIA\Mpeg2BlockInspector\Mpeg2BlockInspector\TESTING\show_source_clip_info%blocky%_2.vpy"
REM
set "mpg_path=E:\SOFTWARE-Win11\MULTIMEDIA\Mpeg2BlockInspector\Mpeg2BlockInspector\VHSC_samples"
set "mpg_filepart=TEST_2A_A001%blocky%"
REM
set "mpg_part=%mpg_path%\%mpg_filepart%"
set "mpg_file=%mpg_part%.mpg"
set "mpg_index=%mpg_part%.idx"
set "mpg_temp_index=%mpg_index%.s1tmp"
set "mpg_log=%mpg_part%.log"
REM
@echo.>>"%mpg_log%" 2>&1
@echo del "%mpg_log%" >>"%mpg_log%" 2>&1
@echo del "%mpg_log%"
del "%mpg_log%" >NUL 2>&1
REM
@echo.>>"%mpg_log%" 2>&1
@echo set path_ >>"%mpg_log%" 2>&1
set path_ >>"%mpg_log%" 2>&1
set path_
REM
@echo.>>"%mpg_log%" 2>&1
@echo set mpg_ >>"%mpg_log%" 2>&1
set mpg_ >>"%mpg_log%" 2>&1
set mpg_
REM
@echo.>>"%mpg_log%" 2>&1
@echo *** "%mpg_temp_index%" is a scratch file created by Inspector and renamed to be the actual index file at completion. >>"%mpg_log%" 2>&1
@echo del "%mpg_temp_index%" >>"%mpg_log%" 2>&1
@echo del "%mpg_temp_index%"
del "%mpg_temp_index%" >NUL 2>&1
REM
@echo.>>"%mpg_log%" 2>&1
@echo *** "%mpg_index%" is the actual index file at completion. >>"%mpg_log%" 2>&1
@echo del "%mpg_index%" >>"%mpg_log%" 2>&1
@echo del "%mpg_index%"
del "%mpg_index%" >NUL 2>&1
REM

REM Run the Mpeg2BlockInspector
@echo.>>"%mpg_log%" 2>&1
@echo "%path_ffmpeg%" -v error -i "%mpg_file%" -c:v copy -an -f mpeg2video - *pipe* "%path_Mpeg2BlockInspector%" -b - -m "%mpg_index%" >>"%mpg_log%" 2>&1
@echo "%path_ffmpeg%" -v error -i "%mpg_file%" -c:v copy -an -f mpeg2video - *pipe* "%path_Mpeg2BlockInspector%" -b - -m "%mpg_index%"
"%path_ffmpeg%" -v error -i "%mpg_file%" -c:v copy -an -f mpeg2video - | "%path_Mpeg2BlockInspector%" -b - -m "%mpg_index%" >>"%mpg_log%" 2>&1
set "inspector_rc=%ERRORLEVEL%"
@echo.>>"%mpg_log%" 2>&1
@echo *** Inspector returned exit code: %inspector_rc% >>"%mpg_log%" 2>&1
@echo *** Inspector returned exit code: %inspector_rc%
@echo.>>"%mpg_log%" 2>&1
@echo dir /s /b "%mpg_part%.*" >>"%mpg_log%" 2>&1
dir /s /b "%mpg_part%.*" >>"%mpg_log%" 2>&1
@echo.>>"%mpg_log%" 2>&1
@echo dir "%mpg_part%.*" >>"%mpg_log%" 2>&1
dir "%mpg_part%.*" >>"%mpg_log%" 2>&1

REM Run the Stage1_Inspector_Analyzer
@echo.>>"%mpg_log%" 2>&1
@echo python "%path_Stage1_Inspector_Analyzer%" summary "%mpg_index%" >>"%mpg_log%" 2>&1
@echo python "%path_Stage1_Inspector_Analyzer%" summary "%mpg_index%"
python "%path_Stage1_Inspector_Analyzer%" summary "%mpg_index%" >>"%mpg_log%" 2>&1

REM Display source mpg clip information
@echo.>>"%mpg_log%" 2>&1
@echo TYPE "%path_vpy%" >>"%mpg_log%" 2>&1
TYPE "%path_vpy%" >>"%mpg_log%" 2>&1
@echo.>>"%mpg_log%" 2>&1
echo "%path_vspipe%" --arg "src=%mpg_file%" --arg "idx=%mpg_index%" --info "%path_vpy%" 2>>"%mpg_log%" 1>&2
echo "%path_vspipe%" --arg "src=%mpg_file%" --arg "idx=%mpg_index%" --info "%path_vpy%"
"%path_vspipe%" --arg "src=%mpg_file%" --arg "idx=%mpg_index%" --info "%path_vpy%" 2>>"%mpg_log%" 1>&2
@echo.>>"%mpg_log%" 2>&1
echo "%path_vspipe%" --container y4m "%path_vpy%" NUL 2>>"%mpg_log%" 1>&2
echo "%path_vspipe%" --container y4m "%path_vpy%" NUL
"%path_vspipe%" --container y4m "%path_vpy%" NUL 2>>"%mpg_log%" 1>&2
@echo.>>"%mpg_log%" 2>&1

@echo.>>"%mpg_log%" 2>&1
@echo *** Created log file "%mpg_log%"

pause
exit /b
