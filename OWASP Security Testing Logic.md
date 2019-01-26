# OWASP Security Tests Logic.

Check for the script tag in source code for xss

	1. rXSS
		Check for the user defined variable.
		Replace with XSS Payloads
	2. pXSS
		Check for the user input, which will store backend and displyed to client.
		Replace with XSS Payloads

		Shopping Cart
		User Profiles

Check for database driven parameter by checking the functionality and intelliegence

	3. SQLi
		Check for the data, which is driven from SQL server.
		Find Login based.
		Error based.
		Blind SQLi
			Boolean based SQLi
			Time-based SQLi
