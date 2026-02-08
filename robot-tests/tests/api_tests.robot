*** Settings ***
Library     String
Resource    ../resources/api_keywords.robot
Resource    ../variables/config.robot
Suite Setup    Create API Session

*** Test Cases ***
Health API Should Be UP
    Check Health API

IMS Registration Should Fail With Invalid Request
    Register Subscriber With Invalid Payload

IMS Registration Should Succeed Async
    ${id}=    Generate Random String    6    [NUMBERS]
    Register Subscriber Async    ${id}

