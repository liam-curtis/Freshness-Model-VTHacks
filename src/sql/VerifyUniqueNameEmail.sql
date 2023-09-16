CREATE DEFINER=`davidjdeg2`@`%` PROCEDURE `VerifyUniqueNameEmail`(
IN p_Name VARCHAR(50),
IN p_Email VARCHAR(50),
OUT result INT
)
BEGIN    
	DECLARE condition_met BOOLEAN;

	SET condition_met = EXISTS (
			SELECT 1 FROM USER 
			WHERE UserName = p_Name OR Email = p_EMail
    );
    IF condition_met THEN
        SET result = 1; -- Condition is true
    ELSE
        SET result = 0; -- Condition is false
    END IF;	
END