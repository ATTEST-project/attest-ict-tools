# ATTEST-ICT Platform: tools integration

The requirements and the instructions to install the tools integration component, with the tools from the open-source toolbox code, is detailed in the ATTEST D6.2 "Integration of the open-source toolbox" (Appendix: Installation guide).

An install.bat, that can be found in all the tools directories, creates the specific tool's Conda environment for the tool.

Once all the tools environments have been created, the copytoolsfiles.bat script can be used to copy all the tools code into the directory structure as expected by the ICT platform.

A launch.bat, one for each tool, activates the tool's environment and executes it. 

Please note that there may be the need to change the install.bat and launch.bat scripts, to reflect a specific installation (e.g., with the correct path for a third party solver executable).
