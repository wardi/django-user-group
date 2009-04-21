-- This migration will allow multiple speakers (and no speakers) for each talk

START TRANSACTION;

CREATE TABLE "meetings_talk_speakers" (
    "id" serial NOT NULL PRIMARY KEY,
    "talk_id" integer NOT NULL REFERENCES "meetings_talk" ("id") DEFERRABLE INITIALLY DEFERRED,
    "speaker_id" integer NOT NULL REFERENCES "meetings_speaker" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("talk_id", "speaker_id")
);
insert into "meetings_talk_speakers" select id, id as talk_id, speaker_id from "meetings_talk";
alter table "meetings_talk" drop "speaker_id";
select setval('meetings_talk_speakers_id_seq', (select max(id) from "meetings_talk_speakers"));

COMMIT;
