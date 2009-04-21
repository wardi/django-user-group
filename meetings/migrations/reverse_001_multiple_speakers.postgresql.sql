-- This migration will reverse allowing multiple speakers 
-- (and no speakers) for each talk, discarding all but one speaker from
-- talks with multiple speakers.  
-- WARNING: Talks with no speakers will cause this migration to fail.

START TRANSACTION;

alter table "meetings_talk" add column "speaker_id" integer NULL REFERENCES "meetings_speaker" ("id") DEFERRABLE INITIALLY DEFERRED;

update "meetings_talk" 
set "speaker_id" = "meetings_talk_speakers"."speaker_id" 
from "meetings_talk_speakers" 
where "meetings_talk_speakers"."talk_id" = "meetings_talk"."id";

alter table "meetings_talk" alter column "speaker_id" set NOT NULL;
DROP TABLE "meetings_talk_speakers" CASCADE;

COMMIT;
