# EPA Geolocated Photograph Log Desktop GUI
## Overview
This desktop tool generates a report that shows locations and geographical references of field images.

## Installation
<ol>
  <li>Download and install <a href="https://www.python.org/downloads/">Python 3</a> onto your computer (this application was developed and tested using Python 3.9 but may be compatible with similar versions).</li>
  <li>Download the repository and store it within a proper location on your computer.</i>
  <li>Execute setup.py with your Python installation.</li>
</ol>

Alternatively, you can download a standalone exacuteable file of the application without having to go through the installation process. Click on this <a href="https://github.com/tylerrichman-erg/EPA-Geolocated-Photograph-Log-DesktopGUI/blob/main/EPA-Geolocated-Photograph-Log-DesktopGUI_1_0_1.zip">link</a> and select the "Download raw file" button to download a zip file containing a pregenerated executable file of the application.

## Usage
<ol>
  <li>Double-click on the executable file to launch the application.</li>
  <li>Input the photographer and facility name into the text entries.</li>
  <li>Input the inspection date into the date entry (today's date is selected by default).</li>
  <li>Click on the “Select File(s)” button. This will open a file dialog to select images for the report. The GPS data for the selected images will appear within the table. The table only displays 10 rows at a time, but the user can scroll to view additional rows not currently within the display.</li>
  <li>If necessary, update the coordinates and bearing of the photos within the table. Click the Enter button on your keyboard after making an update to ensure that the change has been made.</li>
  <li>Click on the button containing the folder icon to select an output file location for the report.</li>
  <li>Click the “Generate Report” button. A pop-up will notify the user once the report has been generated or if any errors have occured.</li>
  <li>Open the report in Microsoft Word and manually fill in the descriptions for each of the photographs. </li>
</ol>

## Version History
<ins>1.0.1 (2025/05/01)</ins>: Increased spatial extent of output document maps.<br>
<ins>1.0.0 (2025/04/23)</ins>: Operational version release.

## Contact
Please email tyler.richman@erg.com with any questions or comments regarding the tool.
