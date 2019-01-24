# SystemMonitor-GUI
This is a [Liberouter GUI](https://github.com/cesnet/liberouter-gui/) module for displaying [Munin](https://github.com/munin-monitoring/munin) graphs. This module is currently in beta. Please report all bugs using github issues.

## Installation
Place Monitor folder inside of your Liberouter GUI's modules folder and run bootstrap.py to register Monitor as a new module. After restarting your development server, you should see Monitor in Liberouter GUI.
Open `patterns.json` located in `Monitor/backend/patterns.json` and edit `"munin-path":` to your munin installation folder. You should set the path to folder containing generated graphs.

## Configuration
You can configure graph patterns as well as Munin's home folder by editing file found in `Monitor/backend/patterns.json`
Patterns should be valid expressions for python's `re` module. ([docs](https://docs.python.org/3/library/re.html))

### Example of valid pattern:
```js 
{
   "title": "Nemea",
   "pattern": "nemea_.*",
   "enabled": "true"
}
```
- title: Name shown in Monitor's menu and category dropdown list
- pattern: Python re valid expression that matches all the files you want in your category. Note that backend adds file extension and interval string to your pattern, so **do not add file extensions to patterns**. For example, pattern `"nemea_.*\.png"` would be invalid.
- enabled: you can set this to "false", if you do not want certain category to appear in Monitor.

## Dashboard customization
You can customize graphs, that appear on Dashboard page. After you configure your munin path and your patterns, open dashboard and you should see a form titled "Add graph". Choose a category from dropdown (category = pattern) and a list of all graphs in selected category should appear in a new dropdown. You can filter the list of graphs by writing text to the search field above the dropdown or you can filter graphs by interval by changing the value of "Filter interval" dropdown.

After you add some graphs, you can delete them by clicking the red 'x' icon in the top right corner of them. You can select graphs by clicking on them. After you click on a graph, border should appear, showing that the graph is selected. After you select some graphs, you can change their interval by changing the interval dropdown located in the top left of the page, or you can delete them by clicking the red "Remove selected" button

## File format customization
By default, only .png images are supported. If you want to add support for more file formats, you can change variable `extension_filter` in the file `Monitor/backend/images.py`. Default value is `'*.png'`. Value should be a valid expression for fnmatch ([docs](https://docs.python.org/3.4/library/fnmatch.html))

## Generating new graph names
All graphs displayed in Monitor GUI should be in format `.*-interval.png`, where valid intervals are `day`, `week`, `month,` or `year`. Graphs can be in subfolders, you can use folder in a pattern, so for example `nemea/.*_cpu` is a valid pattern.
