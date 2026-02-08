*** Settings ***
Library    RequestsLibrary

*** Keywords ***
Create API Session
    Create Session    telecom    ${BASE_URL}

Check Health API
    ${resp}=    GET On Session    telecom    /health
    Should Be Equal As Integers    ${resp.status_code}    200
    Should Be Equal    ${resp.json()['status']}    UP

Register Subscriber
    [Arguments]    ${subscriber_id}
    ${headers}=    Create Dictionary    Content-Type=application/json
    ${payload}=    Create Dictionary    subscriberId=${subscriber_id}
    ${resp}=    POST On Session    telecom    /ims/register
    ...    json=${payload}
    ...    headers=${headers}
    Should Be Equal As Integers    ${resp.status_code}    200
    Should Be Equal    ${resp.json()['registrationStatus']}    REGISTERED

Register Subscriber With Invalid Payload
    ${headers}=    Create Dictionary    Content-Type=application/json
    ${resp}=    POST On Session    telecom    /ims/register
    ...    json={}
    ...    headers=${headers}
    ...    expected_status=400
    Should Be Equal As Integers    ${resp.status_code}    400
    Should Contain    ${resp.text}    error

Register Subscriber Async
    [Arguments]    ${subscriber_id}
    ${headers}=    Create Dictionary    Content-Type=application/json
    ${payload}=    Create Dictionary    subscriberId=${subscriber_id}

    POST On Session    telecom    /ims/register
    ...    json=${payload}
    ...    headers=${headers}
    ...    expected_status=202

    FOR    ${i}    IN RANGE    3
        ${resp}=    GET On Session    telecom    /ims/status/${subscriber_id}
        Run Keyword If    '${resp.json()["status"]}' == 'REGISTERED'    Exit For Loop
        Sleep    1s
    END

    Should Be Equal    ${resp.json()["status"]}    REGISTERED

