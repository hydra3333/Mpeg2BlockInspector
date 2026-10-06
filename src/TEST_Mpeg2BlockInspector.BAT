@echo on
@setlocal enableextensions

set "mpg_path=E:\SOFTWARE-Win11\MULTIMEDIA\Mpeg2BlockInspector\Mpeg2BlockInspector\VHSC_samples"

set "mpg_filepart=TEST_2A_A001"
REM set "mpg_filepart=TEST_2A_A001_blocky"

set "mpg_path=E:\SOFTWARE-Win11\MULTIMEDIA\Mpeg2BlockInspector\Mpeg2BlockInspector\VHSC_samples"

set "mpg_part=%mpg_path%\%mpg_filepart%"
set "mpg_file=%mpg_part%.mpg"
set "mpg_index=%mpg_part%.idx"
set "mpg_log=%mpg_part%.log"

set mpg_

del "%mpg_index%" >NUL 2>&1
del "%mpg_index%.s1tmp" >NUL 2>&1

"C:\SOFTWARE\ffmpeg\ffmpeg.exe" -v error -i "%mpg_file%" -c:v copy -an -f mpeg2video - | "E:\SOFTWARE-Win11\MULTIMEDIA\Mpeg2BlockInspector\Mpeg2BlockInspector\src\x64\Release\Mpeg2BlockInspector.exe" -b - -m "%mpg_index%" >"%mpg_log%" 2>&1

@echo Inspector exit code: %ERRORLEVEL%

dir /s /b "%mpg_part%.*"

dir "%mpg_part%.*"

@echo python "E:\SOFTWARE-Win11\MULTIMEDIA\Mpeg2BlockInspector\Mpeg2BlockInspector\src\Stage1_Inspector_Analyzer_v0_1.py" summary "%mpg_index%"
python "E:\SOFTWARE-Win11\MULTIMEDIA\Mpeg2BlockInspector\Mpeg2BlockInspector\src\Stage1_Inspector_Analyzer_v0_1.py" summary "%mpg_index%"

pause
exit /b


E:\SOFTWARE-Win11\MULTIMEDIA\Mpeg2BlockInspector\Mpeg2BlockInspector\src>set "mpg_path=E:\SOFTWARE-Win11\MULTIMEDIA\Mpeg2BlockInspector\Mpeg2BlockInspector\VHSC_samples"

E:\SOFTWARE-Win11\MULTIMEDIA\Mpeg2BlockInspector\Mpeg2BlockInspector\src>
E:\SOFTWARE-Win11\MULTIMEDIA\Mpeg2BlockInspector\Mpeg2BlockInspector\src>set "mpg_filepart=TEST_2A_A001"

E:\SOFTWARE-Win11\MULTIMEDIA\Mpeg2BlockInspector\Mpeg2BlockInspector\src>REM set "mpg_filepart=TEST_2A_A001_blocky"

E:\SOFTWARE-Win11\MULTIMEDIA\Mpeg2BlockInspector\Mpeg2BlockInspector\src>
E:\SOFTWARE-Win11\MULTIMEDIA\Mpeg2BlockInspector\Mpeg2BlockInspector\src>set "mpg_path=E:\SOFTWARE-Win11\MULTIMEDIA\Mpeg2BlockInspector\Mpeg2BlockInspector\VHSC_samples"

E:\SOFTWARE-Win11\MULTIMEDIA\Mpeg2BlockInspector\Mpeg2BlockInspector\src>
E:\SOFTWARE-Win11\MULTIMEDIA\Mpeg2BlockInspector\Mpeg2BlockInspector\src>set "mpg_part=%mpg_path%\%mpg_filepart%"

E:\SOFTWARE-Win11\MULTIMEDIA\Mpeg2BlockInspector\Mpeg2BlockInspector\src>set "mpg_file=%mpg_part%.mpg"

E:\SOFTWARE-Win11\MULTIMEDIA\Mpeg2BlockInspector\Mpeg2BlockInspector\src>set "mpg_index=%mpg_part%.idx"

E:\SOFTWARE-Win11\MULTIMEDIA\Mpeg2BlockInspector\Mpeg2BlockInspector\src>set "mpg_log=%mpg_part%.log"

E:\SOFTWARE-Win11\MULTIMEDIA\Mpeg2BlockInspector\Mpeg2BlockInspector\src>
E:\SOFTWARE-Win11\MULTIMEDIA\Mpeg2BlockInspector\Mpeg2BlockInspector\src>set mpg_
mpg_file=E:\SOFTWARE-Win11\MULTIMEDIA\Mpeg2BlockInspector\Mpeg2BlockInspector\VHSC_samples\TEST_2A_A001.mpg
mpg_filepart=TEST_2A_A001
mpg_index=E:\SOFTWARE-Win11\MULTIMEDIA\Mpeg2BlockInspector\Mpeg2BlockInspector\VHSC_samples\TEST_2A_A001.idx
mpg_log=E:\SOFTWARE-Win11\MULTIMEDIA\Mpeg2BlockInspector\Mpeg2BlockInspector\VHSC_samples\TEST_2A_A001.log
mpg_part=E:\SOFTWARE-Win11\MULTIMEDIA\Mpeg2BlockInspector\Mpeg2BlockInspector\VHSC_samples\TEST_2A_A001
mpg_path=E:\SOFTWARE-Win11\MULTIMEDIA\Mpeg2BlockInspector\Mpeg2BlockInspector\VHSC_samples

E:\SOFTWARE-Win11\MULTIMEDIA\Mpeg2BlockInspector\Mpeg2BlockInspector\src>
E:\SOFTWARE-Win11\MULTIMEDIA\Mpeg2BlockInspector\Mpeg2BlockInspector\src>del "%mpg_index%" >NUL 2>&1

E:\SOFTWARE-Win11\MULTIMEDIA\Mpeg2BlockInspector\Mpeg2BlockInspector\src>del "%mpg_index%.s1tmp" >NUL 2>&1

E:\SOFTWARE-Win11\MULTIMEDIA\Mpeg2BlockInspector\Mpeg2BlockInspector\src>
E:\SOFTWARE-Win11\MULTIMEDIA\Mpeg2BlockInspector\Mpeg2BlockInspector\src>"C:\SOFTWARE\ffmpeg\ffmpeg.exe" -v error -i "%mpg_file%" -c:v copy -an -f mpeg2video - | "E:\SOFTWARE-Win11\MULTIMEDIA\Mpeg2BlockInspector\Mpeg2BlockInspector\src\x64\Release\Mpeg2BlockInspector.exe" -b - -m "%mpg_index%" >"%mpg_log%" 2>&1

E:\SOFTWARE-Win11\MULTIMEDIA\Mpeg2BlockInspector\Mpeg2BlockInspector\src>@echo Inspector exit code: %ERRORLEVEL%
Inspector exit code: 0

E:\SOFTWARE-Win11\MULTIMEDIA\Mpeg2BlockInspector\Mpeg2BlockInspector\src>
E:\SOFTWARE-Win11\MULTIMEDIA\Mpeg2BlockInspector\Mpeg2BlockInspector\src>dir /s /b "%mpg_part%.*"
E:\SOFTWARE-Win11\MULTIMEDIA\Mpeg2BlockInspector\Mpeg2BlockInspector\VHSC_samples\TEST_2A_A001.idx
E:\SOFTWARE-Win11\MULTIMEDIA\Mpeg2BlockInspector\Mpeg2BlockInspector\VHSC_samples\TEST_2A_A001.log
E:\SOFTWARE-Win11\MULTIMEDIA\Mpeg2BlockInspector\Mpeg2BlockInspector\VHSC_samples\TEST_2A_A001.mpg

E:\SOFTWARE-Win11\MULTIMEDIA\Mpeg2BlockInspector\Mpeg2BlockInspector\src>
E:\SOFTWARE-Win11\MULTIMEDIA\Mpeg2BlockInspector\Mpeg2BlockInspector\src>dir "%mpg_part%.*"
 Volume in drive E is E-DRIVE
 Volume Serial Number is 366A-E763

 Directory of E:\SOFTWARE-Win11\MULTIMEDIA\Mpeg2BlockInspector\Mpeg2BlockInspector\VHSC_samples

06/10/2026  10:09 PM         3,820,832 TEST_2A_A001.idx
06/10/2026  10:09 PM                 0 TEST_2A_A001.log
16/08/2026  07:15 PM         9,179,136 TEST_2A_A001.mpg
               3 File(s)     12,999,968 bytes
               0 Dir(s)  931,274,706,944 bytes free

E:\SOFTWARE-Win11\MULTIMEDIA\Mpeg2BlockInspector\Mpeg2BlockInspector\src>
E:\SOFTWARE-Win11\MULTIMEDIA\Mpeg2BlockInspector\Mpeg2BlockInspector\src>@echo python "E:\SOFTWARE-Win11\MULTIMEDIA\Mpeg2BlockInspector\Mpeg2BlockInspector\src\Stage1_Inspector_Analyzer_v0_1.py" summary "%mpg_index%"
python "E:\SOFTWARE-Win11\MULTIMEDIA\Mpeg2BlockInspector\Mpeg2BlockInspector\src\Stage1_Inspector_Analyzer_v0_1.py" summary "E:\SOFTWARE-Win11\MULTIMEDIA\Mpeg2BlockInspector\Mpeg2BlockInspector\VHSC_samples\TEST_2A_A001.idx"

E:\SOFTWARE-Win11\MULTIMEDIA\Mpeg2BlockInspector\Mpeg2BlockInspector\src>python "E:\SOFTWARE-Win11\MULTIMEDIA\Mpeg2BlockInspector\Mpeg2BlockInspector\src\Stage1_Inspector_Analyzer_v0_1.py" summary "%mpg_index%"
VALID: E:\SOFTWARE-Win11\MULTIMEDIA\Mpeg2BlockInspector\Mpeg2BlockInspector\VHSC_samples\TEST_2A_A001.idx
records=300 sequences=1
dimensions: 704x576 MB=44x36 frames=300
picture types: B=133 (44.33%), I=34 (11.33%), P=133 (44.33%)
picture structures: FRAME=300 (100.00%)
transform states: FIELD=29330 (6.17%), FRAME=281112 (59.16%), NONE=164758 (34.67%)
coding states: INTER=371425 (78.16%), INTRA=91514 (19.26%), SKIPPED=12261 (2.58%)
mixed FRAME/FIELD frames=263 (87.67%)
QP effective: min=1 max=80 mean=16.534 median=12.0
macroblock Q updates=106447 (22.40%)
dct_type bits read=310442 (65.33%)
INTER CBP=0 with dct_type bit actually read=0
custom matrix frames: intra=0 non_intra=0 chroma_intra_diff=0 chroma_non_intra_diff=0
I transforms: FIELD=13077 (24.28%), FRAME=40779 (75.72%)
P transforms: FIELD=15684 (7.44%), FRAME=172598 (81.93%), NONE=22390 (10.63%)
B transforms: FIELD=569 (0.27%), FRAME=67735 (32.15%), NONE=142368 (67.58%)
horizontal state neighbours: FIELD-FIELD=15175, FIELD-FRAME=25437, FIELD-NONE=1511, FRAME-FRAME=226401, FRAME-NONE=69177, NONE-NONE=126699
vertical state neighbours: FIELD-FIELD=16903, FIELD-FRAME=23620, FIELD-NONE=1233, FRAME-FRAME=228283, FRAME-NONE=66355, NONE-NONE=125606
QP histogram: 1=19, 10=63927, 12=45530, 14=29046, 16=17867, 18=16570, 2=124, 20=17208, 22=19915, 24=38012, 28=33295, 3=1169, 32=22186, 36=11479, 4=6504, 40=6276, 44=4622, 48=3148, 5=14586, 52=2155, 56=1679, 6=26354, 64=1061, 7=27959, 72=750, 8=63336, 80=423

E:\SOFTWARE-Win11\MULTIMEDIA\Mpeg2BlockInspector\Mpeg2BlockInspector\src>
