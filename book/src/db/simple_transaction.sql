BEGIN TRANSACTION;
DELETE FROM Equipment WHERE PersonID = "skol" and EquipmentID = "CX-211 oscilloscope";
INSERT INTO Equipment VALUES("ipav", "CX-211 oscilloscope");
END TRANSACTION;
