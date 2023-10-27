# ATTEST-ICT Tools: open-source toolbox integration

This project provides the integration infrastructure for the open-source toolbox, and it is used by the ICT Platform. It includes the tools integrated in the Platform, and the set of wrappers used by the Platform to run the tools.

# Installation

In all the tools directories (but T51, T52 T53) there is an install.bat script that creates the specific tool's Conda environment: please open a terminal in each tool directory and run the tool's installation script
For T51, T52 and T5.3 execute Setup_ATTEST_env.ps1).

Once all the tools environments have been created, the copytoolsfiles.bat script can be used to copy all the tools code into the directory structure, as expected by the ICT platform.

A launch.bat, one for each tool, activates the tool's environment and executes it. 

Please note that there may be the need to change the install.bat and launch.bat scripts, to reflect a specific installation (e.g., with the correct path for a third party solver executable).

More information about the integration of the ATTEST open-source toolbox inside the ATTEST ICT Platform, can be found in the ATTEST D6.2 "Integration of the open-source toolbox".

Note: this project contains code from the ATTEST open-source toolkit, licensed under the EUPL v1.2
