CREATE DEFINER=`davidjdeg2`@`%` PROCEDURE `InsertUserWithHashedPassword`(
    IN p_Username VARCHAR(50),
    IN p_Password VARCHAR(100),
    IN p_Email VARCHAR(50),
    IN p_FirstName VARCHAR(50),
    IN p_LastName VARCHAR(50)
)
BEGIN
    DECLARE v_Salt CHAR(36);
    DECLARE v_Hash CHAR(64);

    -- Generate a random salt
    SET v_Salt = UUID();

    -- Hash the password with the salt using SHA-256
    SET v_Hash = SHA2(CONCAT(p_Password, v_Salt), 256);

    -- Insert the user into the Users table with hashed password and salt
    INSERT INTO User (Username, PasswordHash, Email,  FirstName, LastName, Salt)
    VALUES (p_Username, v_Hash, p_Email, p_FirstName, p_LastName, v_Salt);
END