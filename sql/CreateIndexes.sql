CREATE UNIQUE INDEX account_idx_apikey ON account (apikey);
CREATE UNIQUE INDEX account_idx_mbuser ON account (mbuser);
CREATE INDEX account_google_idx_account_id ON account_google (account_id);
CREATE INDEX account_openid_idx_account_id ON account_openid (account_id);
CREATE UNIQUE INDEX application_idx_apikey ON application (apikey);
CREATE INDEX fingerprint_idx_length ON fingerprint (length);
CREATE INDEX fingerprint_idx_track_id ON fingerprint (track_id);
CREATE INDEX fingerprint_source_idx_submission_id ON fingerprint_source (submission_id);
CREATE INDEX foreignid_idx_vendor ON foreignid (vendor_id);
CREATE UNIQUE INDEX foreignid_idx_vendor_name ON foreignid (vendor_id, name);
CREATE UNIQUE INDEX foreignid_vendor_idx_name ON foreignid_vendor (name);
CREATE UNIQUE INDEX format_idx_name ON format (name);
CREATE INDEX recording_acoustid_idx_acoustid ON recording_acoustid (acoustid);
CREATE UNIQUE INDEX recording_acoustid_idx_uniq ON recording_acoustid (recording, acoustid);
CREATE UNIQUE INDEX source_idx_uniq ON source (application_id, account_id, version);
CREATE INDEX stats_idx_date ON stats (date);
CREATE INDEX stats_idx_name_date ON stats (name, date);
CREATE INDEX stats_lookups_idx_date ON stats_lookups (date);
CREATE INDEX stats_user_agents_idx_date ON stats_user_agents (date);
CREATE INDEX submission_idx_handled ON submission (id) WHERE handled = false;
CREATE UNIQUE INDEX track_idx_gid ON track (gid);
CREATE INDEX track_foreignid_idx_foreignid_id ON track_foreignid (foreignid_id);
CREATE UNIQUE INDEX track_foreignid_idx_uniq ON track_foreignid (track_id, foreignid_id);
CREATE INDEX track_mbid_idx_mbid ON track_mbid (mbid);
CREATE UNIQUE INDEX track_mbid_idx_uniq ON track_mbid (track_id, mbid);
CREATE INDEX track_mbid_change_idx_track_mbid_id ON track_mbid_change (track_mbid_id);
CREATE INDEX track_mbid_source_idx_source_id ON track_mbid_source (source_id);
CREATE INDEX track_mbid_source_idx_track_mbid_id ON track_mbid_source (track_mbid_id);
CREATE INDEX track_meta_idx_meta_id ON track_meta (meta_id);
CREATE UNIQUE INDEX track_meta_idx_uniq ON track_meta (track_id, meta_id);
CREATE INDEX track_puid_idx_puid ON track_puid (puid);
CREATE UNIQUE INDEX track_puid_idx_uniq ON track_puid (track_id, puid);
