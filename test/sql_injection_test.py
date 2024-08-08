import requests

url = "http://localhost:8000/users"

test_cases = [
    "'", "''", "`", "``", ",", "\"", "\"\"", "/", "\\", "\\\\", ";", "' or \"",
    "-- or #", "' OR '1", "' OR 1 -- -", "\" OR \"\" = \"", "\" OR 1 = 1 -- -",
    "' OR '' = '", "'='", "'LIKE'", "'=0--+", " OR 1=1", "' OR 'x'='x", "' AND id IS NULL; --",
    "'''''''''''''UNION SELECT '2", "%00", "/*…*/", "+", "||", "%", "@variable", "@@variable",
    "AND 1", "AND 0", "AND true", "AND false", "1-false", "1-true", "1*56", "-2", "1' ORDER BY 1--+",
    "1' ORDER BY 2--+", "1' ORDER BY 3--+", "1' ORDER BY 1,2--+", "1' ORDER BY 1,2,3--+",
    "1' GROUP BY 1,2,--+", "1' GROUP BY 1,2,3--+", "' GROUP BY columnnames having 1=1 --",
    "-1' UNION SELECT 1,2,3--+", "' UNION SELECT sum(columnname ) from tablename --",
    "-1 UNION SELECT 1 INTO @,@", "-1 UNION SELECT 1 INTO @,@,@", "1 AND (SELECT * FROM Users) = 1",
    "' AND MID(VERSION(),1,1) = '5';", "' and 1 in (select min(name) from sysobjects where xtype = 'U' and name > '.') --",
    ",(select * from (select(sleep(10)))a)", "%2c(select%20*%20from%20(select(sleep(10)))a)",
    "';WAITFOR DELAY '0:0:30'--", "#", "/*", "-- -", ";%00",
]

passed = 0
failed = 0

for case in test_cases:
    data = {
        "username": case,
        "password": "",
        "api_key": "a"
    }
    response = requests.post(url, json=data)
    print(f"Test case: {case}")
    print("Status code:", response.status_code)
    print("Response body:", response.json())
    if response.ok:
        response_data = response.json()
        user_id = response_data["user_id"]
        response = requests.get(url)
        response_data = response.json()
        expected = data["username"]
        actual = [user["username"] for user in response_data if user["id"] == user_id][0]
        print(f"test passed: {expected == actual}, expected: {expected}, actual: {actual}")
        if expected == actual:
            passed += 1
        else:
            failed += 1
    print("-" * 50)

print("SQL INJECTION: ")
print(f"PASSED: {passed}")
print(f"FAILED: {failed}")
print("-" * 50)