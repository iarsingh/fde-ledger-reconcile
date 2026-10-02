# Readout

On the sample drop, one payment matches for 1500 cents. The replay of evt-1 is ignored. evt-2 is the same payment on a new event id and is not added again. pay-4 is 8000 against a 7900 settlement and stays an exception. pay-7 has no settlement and stays pending.

We are not claiming a cash number for the month. The shadow week measures two things: replayed files produce the same matched total, and every amount mismatch is still in the exception queue at the end of the day.
