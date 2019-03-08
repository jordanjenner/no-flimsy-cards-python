# no-flimsy-cards-python

This was coded as part of a group project for university where we made a barrier system which used NFC. The way this was implemented was in no way secure as user id's were sent as plaintext responses as opposed to using the right series of APDU commands to send the user id as encrypted text and actually check whether the APDU command was coming from a verified source.
