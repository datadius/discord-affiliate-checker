# discord-affiliate-checker

Client has requested a discord bot that checks three exchanges for affiliate data.

Phemex, Bingx, Fairdesk

![image](https://github.com/datadius/discord-affiliate-checker/assets/16731794/ecaedb44-c0fc-42b3-8e8d-477bde78bacc)

Get direct trader user under current partner user

request


GET https://api.fairdesk.com/api/v1/private/account/partner-direct-user-deposit?traderUid=100480
X-fairdesk-access-key:xxxxxxxx
x-fairdesk-request-expiry: 1650038027000
x-fairdesk-request-signature: ff4e7f99e97096fb2cbbf048768a350c11b9a9f999f8b02aa2d6f51a754111111


response
{
  "status": 0,
  "error": "OK",
  "errorParams": null,
  "data": 1022630000.00000000
}

Note: If the traderUid is not valid or not direct trader of current API user, then returned data will be -9999



Endpoint Security Type

    Each private API call must be signed and pass to server in HTTP header x-fairdesk-request-signature.
    Endpoints use HMAC SHA256 signatures. The HMAC SHA256 signature is a keyed HMAC SHA256 operation. Use your apiSecret as the key and the string (URL Path + QueryString + Expiry + body) as the value for the HMAC operation.
    apiSecret = Base64::urlDecode(API Secret)
    The signature is case sensitive.

Signature Example 1: HTTP GET Request

    API REST Request URL: https://api.fairdesk.com/api/v1/private/account/symbol-config
    Request Path: /api/v1/private/account/symbol-config
    Request Query:
    Request Body:
    Request Expiry: 1649999999999
    Signature: HMacSha256(/api/v1/private/account/symbol-config + 1649999999999)

Signature Example 2: HTTP POST Request

    API REST Request URL: https://api.fairdesk.com/api/v1/private/account/config/adjust-leverage
    Request Path: /api/v1/private/account/config/adjust-leverage
    Request Query:
    Request Body: { "symbol": "btcusdt", "isolated": true, "leverage": "120"}
    Request Expire: 1649999999999
    Signature: HMacSha256(/api/v1/private/account/config/adjust-leverage + 1649999999999 + { "symbol": "btcusdt", " isolated": true, "leverage": "120"})


