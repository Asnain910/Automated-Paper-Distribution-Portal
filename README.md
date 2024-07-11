Automated Paper Distribution Portal Documentation

Project Overview

The "Automated Paper Distribution Portal" is designed to automate the process of assigning faculty members to set examination papers. The portal streamlines the distribution process, reduces manual errors, and ensures a fair selection of faculty for paper setting duties.

Features

User Interface: A form with dropdown menus for selecting parameters and a file type input for uploading a CSV file containing faculty details. The choices selected in the form by the user will be included in the email.
CSV File Processing: Reads the uploaded CSV file, processes the data, and randomly selects three faculty members to set the examination papers.
Automated Email Notifications: Automatically sends an email to the selected faculty members with necessary attachments and instructions regarding paper setting.

Technologies Used

Frontend: HTML, CSS, JavaScript
Backend: Flask (Python)
Database: None (CSV file processing)
Email: smtplib (Python)
Other: pandas for CSV file processing, email.mime for email construction
