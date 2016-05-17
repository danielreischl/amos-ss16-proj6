#!/usr/bin/env python
# encoding: utf-8

# File to maintain all constants which will be used in all DataProcessing Scripts


# Length of one Drive
DRIVE_LENGTH = 4
# Length of all drives
LINE_LENGTH = 12
# Amount of Drives
AMOUNT_OF_DRIVES = 3
# Amount of Carriers
AMOUNT_OF_CARRIERS = 3
# Wait time of the Simulator in Seconds used in dataProcessing.py
WAIT_TIME_IN_SECONDS_DPPY = 0.001
#Session of the demonstrator setting
SESSION = 1
# WaitTime of manipulateData.py
WAIT_TIME_IN_SECONDS_MPY = 5
# Separator of the CSV-Files
CSV_SEPARATOR = ";"
# Path of SQLITEDB
PATH_OF_SQLLITE_DB = './django/db.sqlite3'
NAME_TABLE_SESSION = 'tbl_Session'
NAME_TABLE_CARRIER = 'tbl_Carrier'
NAME_TABLE_ITERATION = 'tbl_Iteration'
# Name of Table for processed data
NAME_TABLE_PROCESSED_DATA = 'helloWorld_tbl_TimeStampData'
# Name of Table for commulated data
NAME_TABLE_COM_DATA = 'helloWorld_tbl_IterationData'

