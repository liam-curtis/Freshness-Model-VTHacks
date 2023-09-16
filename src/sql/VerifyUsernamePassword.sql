CREATE DEFINER=`davidjdeg2`@`%` PROCEDURE `VerifyUsernamePassword`(
    IN p_Username VARCHAR(50),
    IN p_Password VARCHAR(100),
    OUT result INT
)
BEGIN
    DECLARE storedPassword VARCHAR(100);

    -- Retrieve the stored password for the given username
    SELECT PasswordHash INTO storedPassword
    FROM Users
    WHERE Username = p_Username;

    -- Check if the username exists and the passwords match
    IF storedPassword IS NOT NULL AND storedPassword = SHA2(CONCAT(p_Password, Salt), 256) THEN
        SET result = 1; -- Username and password match
    ELSE
        SET result = 0; -- Username and password do not match
    END IF;
END