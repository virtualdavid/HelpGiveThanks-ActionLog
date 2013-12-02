total: action buttons: total
#PURPOSE merge selected record's time data into one total record and then link these records so that time added in the future to any of the
merge records will be automatically added to the one total record.
#
#
#
#NOTE: the three # symbols set apart chunks of script.
#NOTE: the ﬁnish and error script chunks are almost identical (the error message differ in telling where in the script they occur). For this reason,
they are not numbered as part of a particular chuck of the script, and are separated by three # symbols to set them apart.
#
#
#
#basic administration tasks
Set Error Capture [ On ]
Allow User Abort [ Off ]
Set Variable [ $userID; Value:reference::farmerID ]
#
#
#
#A) BEGIN ﬁnd selected merge records and create new total record and link all records together
#
#1 check if there are 1 or more records to merge and if not halt the script. (Can't merge if zero records are selected. 1 record can be merged
which is really making a copy of that record for instances where the user has been tracking 2 things with one brainstate but now wants to
separate the tracking of these with 2 separate brainstate records.)
If [ brainstate::groupAddCheckboxCount < 1 ]
Show Custom Dialog [ Title: "!"; Message: "At least 1 brainstates must be selected for a merge."; Buttons: “OK” ]
Halt Script
End If
#
#2 make a list of only the records to be merged
Enter Find Mode [ ]
Set Field [ brainstate::_keyUser; $userID ]
Set Field [ brainstate::groupAddCheckbox; "t" ]
Perform Find [ ]
#
#
#
#BEGIN ﬁnd error 1
If [ Get ( LastError ) ≠ 0 ]
#tell user the error number.
Show Custom Dialog [ Title: "!"; Message: "Unexpected error " & Get ( LastError ) & " peforming merge script part A2."; Buttons: “OK” ]
#Find all records user had showing when they clicked the merge button
Enter Find Mode [ ]
Set Field [ brainstate::_keyUser; $userID ]
Perform Find [ ]
If [ steward::retiredStatus = "r" ]
Constrain Found Set [ Speciﬁed Find Requests: Omit Records; Criteria: brainstate::sortRetired: “r” ]
[ Restore ]
End If
If [ steward::hideStatus = "" and steward::showORhide = "hide" ]
Constrain Found Set [ Speciﬁed Find Requests: Omit Records; Criteria: brainstate::hide: “t” ]
[ Restore ]
Sort Records [ ]
[ No dialog ]
Halt Script
End If
If [ steward::showStatus ≠ "" and steward::showORhide = "show" ]
Constrain Found Set [ Speciﬁed Find Requests: Omit Records; Criteria: brainstate::Show: “=” ]
[ Restore ]
December 1, 2013 17:28:54 ActionLog.fp7 - total -1-total: action buttons: total
Sort Records [ ]
[ No dialog ]
Halt Script
End If
Sort Records [ ]
[ No dialog ]
Go to Record/Request/Page
[ First ]
Go to Field [ ]
Halt Script
End If
#END ﬁnd error 1
#
#
#
#3 create the new total record
Go to Layout [ “01SortAndSchedule” (brainstate) ]
New Record/Request
Set Field [ brainstate::_keyUser; $userID ]
Set Field [ brainstate::linkinfo; "total of: " ]
Set Field [ brainstate::description; "NEW TOTAL RECORD the ID numbers of the records totaled by this record can be seen by either clicking or
hovering over the i at the far right of this description ﬁeld." ]
Set Field [ brainstate::groupType; "merge" ]
#
#4 link all records
Set Variable [ $brainstateID; Value:brainstate::_lockBrainstateID ]
Set Variable [ $brainstateDisplayID; Value:brainstate::_Number ]
Go to Record/Request/Page
[ First ]
Loop
Set Field [ brainstate::groupID; $brainstateID ]
Set Field [ brainstate::groupDisplayID; $brainstateDisplayID ]
Go to Record/Request/Page
[ Next; Exit after last ]
End Loop
#
#A) END ﬁnd selected merge records and create new total record and link all records together
#
#
#
Loop
#B) BEGIN add a merge record's ID# to the description of the new total record.
#
#1 make sure there is a record to be merged (this step will be important when this loop is repeated after the ﬁrst record to be merged is
omitted).
Go to Record/Request/Page
[ First ]
If [ brainstate::_lockBrainstateID ≠ brainstate::groupID ]
#
#2 capture merged ID number for total's linkinfo ﬁeld: total of: ID, ID, ID, etc.
Set Variable [ $CurrentBrainstateID; Value:brainstate::_lockBrainstateID ]
Set Variable [ $CurrentBrainstateDisplayID; Value:brainstate::_Number ]
Go to Record/Request/Page
[ Last ]
Set Field [ brainstate::linkinfo; If ( WordCount ( brainstate::linkinfo ) = 2 ;
brainstate::linkinfo & $CurrentBrainstateDisplayID ;
brainstate::linkinfo & ", " & $CurrentBrainstateDisplayID ) ]
Go to Record/Request/Page
[ First ]
December 1, 2013 17:28:54 ActionLog.fp7 - total -2-total: action buttons: total Go to Record/Request/Page
[ First ]
#
#
#
#BEGIN ﬁnish
Else If [ brainstate::_lockBrainstateID = brainstate::groupID ]
#If all records are empty then the merge is complete and now the user needs to be shown the new total record and all the records that
will feed into it until they are separated.
Enter Find Mode [ ]
Set Field [ brainstate::groupID; $brainstateID ]
Perform Find [ ]
Sort Records [ Speciﬁed Sort Order: brainstate::_lockBrainstateID; descending ]
[ Restore; No dialog ]
Go to Record/Request/Page
[ First ]
Go to Layout [ “TotalSort” (brainstate) ]
Go to Field [ ]
Halt Script
#END ﬁnish
#
#
#
End If
#
#B) END add a merge record's ID# to the description of the new total record.
#
#
#
#C BEGIN ﬁnd merge record's related day records
#
#1 make a list of the ﬁrst brainstate's day records in a new window
Go to Layout [ “calcTotalSelectedList” (day1) ]
Enter Find Mode [ ]
Set Field [ day1::_keyBrainstate; $CurrentBrainstateID ]
Perform Find [ ]
#
#C END ﬁnd merge record's related day records
#
#
#
#D BEGIN no records found loop (this loop will either complete the merge process or ﬁnd a merge record with related day records)
#
Loop
#
#1 if records are found exit loop
Exit Loop If [ Get ( LastError ) = 0 ]
#
#2 clear the merge ﬁeld (the big X in the box on the ToBeMerged layout) and omit this record
If [ Get ( LastError ) = 401 ]
Go to Layout [ “01SortAndSchedule” (brainstate) ]
Set Field [ brainstate::groupAddCheckbox; "" ]
Omit Record
#
#
#
#BEGIN ﬁnish
If [ brainstate::_lockBrainstateID = brainstate::groupID ]
December 1, 2013 17:28:54 ActionLog.fp7 - total -3-total: action buttons: total
#If all records are empty then the merge is complete and now the user needs to be shown the new total record and all the
records that will feed into it until they are separated.
Enter Find Mode [ ]
Set Field [ brainstate::groupID; $brainstateID ]
Perform Find [ ]
Sort Records [ Speciﬁed Sort Order: brainstate::_lockBrainstateID; descending ]
[ Restore; No dialog ]
Go to Record/Request/Page
[ First ]
Go to Layout [ “TotalSort” (brainstate) ]
Go to Field [ ]
Halt Script
End If
#END ﬁnish
#
#
#
#BEGIN ﬁnd error 2
Else If [ Get ( LastError ) ≠ 0 ]
#tell user the error number
Show Custom Dialog [ Title: "!"; Message: "Unexpected error " & Get ( LastError ) & " peforming merge script part D2.";
Buttons: “OK” ]
#Find all records user had showing when they clicked the merge button
Enter Find Mode [ ]
Set Field [ brainstate::_keyUser; $userID ]
Perform Find [ ]
If [ steward::retiredStatus = "r" ]
Constrain Found Set [ Speciﬁed Find Requests: Omit Records; Criteria: brainstate::sortRetired: “r” ]
[ Restore ]
End If
If [ steward::hideStatus = "" and steward::showORhide = "hide" ]
Constrain Found Set [ Speciﬁed Find Requests: Omit Records; Criteria: brainstate::hide: “t” ]
[ Restore ]
Sort Records [ ]
[ No dialog ]
Halt Script
End If
If [ steward::showStatus ≠ "" and steward::showORhide = "show" ]
Constrain Found Set [ Speciﬁed Find Requests: Omit Records; Criteria: brainstate::Show: “=” ]
[ Restore ]
Sort Records [ ]
[ No dialog ]
Halt Script
End If
Sort Records [ ]
[ No dialog ]
Go to Record/Request/Page
[ First ]
Go to Field [ ]
Halt Script
End If
#END ﬁnd error 2
#
#
#
#3 capture next records ID number for total's linkinfo ﬁeld: total of: ID, ID, ID, etc.
Set Variable [ $CurrentBrainstateID; Value:brainstate::_lockBrainstateID ]
Set Variable [ $CurrentBrainstateDisplayID; Value:brainstate::_Number ]
Go to Record/Request/Page
[ Last ]
December 1, 2013 17:28:54 ActionLog.fp7 - total -4-total: action buttons: total Go to Record/Request/Page
[ Last ]
Set Field [ brainstate::linkinfo; If ( WordCount ( brainstate::linkinfo ) = 2 ;
brainstate::linkinfo & $CurrentBrainstateDisplayID ;
brainstate::linkinfo & ", " & $CurrentBrainstateDisplayID ) ]
Go to Record/Request/Page
[ First ]
#
#4 make a list of this record's day records in a new window.
Go to Layout [ “calcTotalSelectedList” (day1) ]
Enter Find Mode [ ]
Set Field [ day1::_keyBrainstate; $CurrentBrainstateID ]
Perform Find [ ]
End Loop
#
#D END no records found loop
#
#
#
#E BEGIN create new related day records and add selected record's time to them
#
Loop
#1 ﬁnd any day records for the new brainstate that match the kfDay of the ﬁrst merge record. If this new record already has data in it,
then we want to add new data to the old data; not replace the old data with new data.
Set Variable [ $mergeDay; Value:day1::_keyDay ]
Enter Find Mode [ ]
Go to Layout [ “calcTotalNewRecord” (day2) ]
Set Field [ day2::_keyBrainstate; $brainstateID ]
Set Field [ day2::_keyDay; $mergeDay ]
Perform Find [ ]
#
#2 if no matches are found, create a new day record and put in the time of the ﬁrst the current day record
If [ Get ( LastError ) = 401 ]
New Record/Request
Set Field [ day2::_keyBrainstate; $brainstateID ]
Set Field [ day2::_keyDay; $mergeDay ]
Set Field [ day2::swStart; day2::_keyDay & " 0:00:00" ]
Go to Layout [ “calcTotalSelectedList” (day1) ]
Set Variable [ $TotalActivity; Value:day1::swTotalActivity ]
Go to Layout [ “calcTotalNewRecord” (day2) ]
Set Field [ day2::swPause; Case (
$TotalActivity > Time ( 23 ; 59 ; 59 ) ; day2::_keyDay & " 24:00:00" ;
$TotalActivity < Time ( 0 ; 0 ; 0 ) ; day2::_keyDay & " 00:00:00" ;
day2::_keyDay & " " & $TotalActivity )
//insures that no more than 24 hours will be put into a day and that a day with negative time does not cause an error. ]
#
#
#
#BEGIN ﬁnd error 3
Else If [ Get ( LastError ) ≠ 0 ]
#tell user the error number
Show Custom Dialog [ Title: "!"; Message: "Unexpected error" & Get ( LastError ) & "peforming merge script part E2."; Buttons:
“OK” ]
#Find all records user had showing when they clicked the merge button.
Enter Find Mode [ ]
December 1, 2013 17:28:54 ActionLog.fp7 - total -5-total: action buttons: total
Set Field [ brainstate::_keyUser; $userID ]
Perform Find [ ]
If [ steward::retiredStatus = "r" ]
Constrain Found Set [ Speciﬁed Find Requests: Omit Records; Criteria: brainstate::sortRetired: “r” ]
[ Restore ]
End If
If [ steward::hideStatus = "" and steward::showORhide = "hide" ]
Constrain Found Set [ Speciﬁed Find Requests: Omit Records; Criteria: brainstate::hide: “t” ]
[ Restore ]
Sort Records [ ]
[ No dialog ]
Halt Script
End If
If [ steward::showStatus ≠ "" and steward::showORhide = "show" ]
Constrain Found Set [ Speciﬁed Find Requests: Omit Records; Criteria: brainstate::Show: “=” ]
[ Restore ]
Sort Records [ ]
[ No dialog ]
Halt Script
End If
Sort Records [ ]
[ No dialog ]
Go to Record/Request/Page
[ First ]
Go to Field [ ]
Halt Script
#END ﬁnd error 3
#
#
#
#3 if a match is found, then add the current day's time to this day's time.
Else If [ Get ( LastError ) = 0 ]
Go to Layout [ “calcTotalSelectedList” (day1) ]
Set Variable [ $TotalActivity; Value:day1::swTotalActivity ]
Go to Layout [ “calcTotalNewRecord” (day2) ]
Set Field [ day2::swPause; Case (
$TotalActivity + day2::swTotalActivity > Time ( 23 ; 59 ; 59 ) ; day2::_keyDay & " 24:00:00" ;
$TotalActivity + day2::swTotalActivity < Time ( 0 ; 0 ; 0 ) ; day2::_keyDay & " 00:00:00" ;
day2::_keyDay & " " & ($TotalActivity + day2::swTotalActivity) )
//insures that no more than 24 hours will be put into a day and that a day with negative time does not cause an error. ]
End If
#
#4 repeat loop for found record's next related day record.
Go to Layout [ “calcTotalSelectedList” (day1) ]
Go to Record/Request/Page
[ Next; Exit after last ]
End Loop
#
#E END create new related day records and add selected record's time to them
#
#
#
#F BEGIN go to next record with related day records to be added to the new total record.
#
Go to Layout [ “01SortAndSchedule” (brainstate) ]
#Clear the merge ﬁeld (the big X in the box on the ToBeMerged layout).
Set Field [ brainstate::groupAddCheckbox; "" ]
December 1, 2013 17:28:54 ActionLog.fp7 - total -6-total: action buttons: total
Omit Record
#
#F END go to next record with related day records to be added to the new total record.
#
#
#
End Loop
December 1, 2013 17:28:54 ActionLog.fp7 - total -7-