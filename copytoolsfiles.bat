REM -------------------------------------------------
REM copy tools'files to the dest directory structure
REM -------------------------------------------------

set DEST_TOOLS_ROOT_PATH=C:\ATTEST\tools

xcopy /E /I /H /Y .\T251 %DEST_TOOLS_ROOT_PATH%\WP2\T251
xcopy /E /I /H /Y .\T252 %DEST_TOOLS_ROOT_PATH%\WP2\T252
xcopy /E /I /H /Y .\T26 %DEST_TOOLS_ROOT_PATH%\WP2\T26

xcopy /E /I /H /Y .\T31V2 %DEST_TOOLS_ROOT_PATH%\WP3\T31V2
xcopy /E /I /H /Y .\T32V2 %DEST_TOOLS_ROOT_PATH%\WP3\T32V2
xcopy /E /I /H /Y .\T33V3 %DEST_TOOLS_ROOT_PATH%\WP3\T33V3

xcopy /E /I /H /Y .\TSG %DEST_TOOLS_ROOT_PATH%\WP4\TSG
xcopy /E /I /H /Y .\T41V2 %DEST_TOOLS_ROOT_PATH%\WP4\T41V2
xcopy /E /I /H /Y .\T44V3 %DEST_TOOLS_ROOT_PATH%\WP4\T44V3
xcopy /E /I /H /Y .\T45 %DEST_TOOLS_ROOT_PATH%\WP4\T45

xcopy /E /I /H /Y .\T51 %DEST_TOOLS_ROOT_PATH%\WP5\T51
xcopy /E /I /H /Y .\T52 %DEST_TOOLS_ROOT_PATH%\WP5\T52
xcopy /E /I /H /Y .\T53 %DEST_TOOLS_ROOT_PATH%\WP5\T53
