Chapel door report, 1.1.0
========================

The author reported that the opening Chapel door would not open after the maiden
reward change. Screenshots `eldenring 2026-09-23 19-43-44.png` and
`eldenring 2026-09-23 19-43-35.png` show the finger restriction at the door and
the vanilla ground message beside the maiden. The exact save creation date and
whether the shard had been collected were not confirmed.

The live regulation matched the accepted 1.1.0 regulation during investigation:
83f5fbe3a640f5b36d7a0436734ab9a44db0aaa0726f606bee4c7c1862ede37c.
This supports the regulation version, not a complete contemporaneous inventory
of every file loaded by the running game.

ER-079 records the door portion as a partial failure. The active ObjAct item
requirement was missed by the earlier static review. The
[1.1.1 correction](../CHAPEL-POLISH-UPDATE.md) removes that requirement locally
and leaves the shard optional. The author subsequently confirmed the reported
1.1.1 door/message failure was a stale-load issue and is now resolved. This
confirms the observed door/message behavior after reloading, not the remaining
ER-080 reload/return/NG+ cases or ER-081/ER-082.
