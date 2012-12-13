CREATE TABLE Scientists(
    PersonID     TEXT PRIMARY KEY,        -- uniquely identifies entries
    FamilyName   TEXT NOT NULL,           -- must have value
    PersonalName TEXT NOT NULL,           -- ditto
    Email        TEXT UNIQUE              -- no duplicates
);
