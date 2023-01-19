# ATTEST-ICT Platform: tools integration

The requirements and the instructions to install the tools integration component, with the tools from the open-source toolbox code, is detailed in the ATTEST D6.2 "Integration of the open-source toolbox" (Appendix: Installation guide).

The script copytoolsfiles.bat can be used to copy the all the tools' code to the directory structure as expected by the ICT platform.

An install.bat, that can be found in all the tools directories, creates the specific tool's Conda environment.
A launch.bat, also provided for all the tools, activates the tool's environment and executes it. 

Please note that there may be the need to change the install.bat and launch.bat scripts, to reflect a specific installation (e.g., with the correct path for a third party solver executable).
