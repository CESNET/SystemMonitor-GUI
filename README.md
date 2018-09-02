# SystemMonitor-GUI
This is a [Liberouter GUI](https://github.com/cesnet/liberouter-gui/) module for displaying [Munin](https://github.com/munin-monitoring/munin) graphs.
*This module is stil in development and might not work yet.*

## Installation
Place Monitor folder inside of your Liberouter GUI's modules folder and run bootstrap.py to register Monitor as a new module. After restarting your development server, you should see Monitor in Liberouter GUI.

## Configuration
You can configure graph patterns as well as Munin's home folder by editing file found in backend/patterns.json
