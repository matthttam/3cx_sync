# 3cx Sync
## Description
A utility designed to allow user synchronization from a CSV file to the 3CX phone system.

> :warning: Notice
 This package is not affiliated with 3CX. It is an unofficial package that is designed to make it easier to interact with the 3CX API.

## 3CX API Compatibility
The 3CX API can change at any time. They do provide a swagger file. The following table works to show compatibility between this package and the 3CX and swagger reported versions.
| 3cx Sync Version | 3CX Version|
|----------------- |------------|
| 1.0.4            | Version 20.0 Update 6 + |
| < 1.0.3          | < Version 20.0 Update 6 |

## Installation
Simply download the EXE to a folder and run it.

## Setup
This application has a GUI to configure what csv file to use and what fields to sync.

The first step is to configure the app which requires a username and password.
> :warning: Unless you use a keyring application and check the box for storing the credential securely, the credential will be stored in plain text.

Note, that the "Static" field selection is not fully implemented. For static true or false fields, I recommend having a field called True with the value True and a field for False with the value False in your CSV file so you can easily set some fields as always true or false.

For now, this application only works with a CSV source but it is built to allow for other sync sources to be created in the future.

## Running a Sync
Although there is no way to do a dry run at this time, there is a pause button during the sync that allows you to stop temporarily and read the logging on the screen.

### Logging
This application will log to app.log next to the exe. This is the same log information that is shown during the run.

### Silent Run
You can export your config file and reference it with a command line when triggering a sync. This allows you to run this as a scheduled task or cron job.

```
3cx_sync.exe -c="C:\Path\to\Your\Config\Folder" --mode="CSV" -s
```