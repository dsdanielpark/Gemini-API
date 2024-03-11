Development Status :: 3 - Alpha

# FAQ
The most important notice is to close the Gemini website or browser immediately after confirming a successful response from generate_content, and not to visit the Gemini web again.


I've been able to receive valid responses for several days without refreshing the cookie values using this method (as of March 11, 2024). However, this information may change depending on Google's revisions, similar to the Bard API. 

While the latest bot_server param is available, I choose not to use it. This decision is based on past experiences where security measures, such as frequent changes in cookies or enhancements in rate limiting, were enforced in newer services for security purposes.




## Before using the Gemini API
- Google Gemini can return different responses based on various factors such as account, country, region, IP, etc., following Google's policies. It cannot be resolved at the package level. (e.g., [CAPTCHA](https://en.wikipedia.org/wiki/CAPTCHA) or [HTTP 429 error](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429))
- The cookie values for this service is unofficial. Additionally, exposing it can allow others to easily use the Gemini service with your Google ID, so never expose it.
- This service has very limited and variable call limits per unit of time, and exceeding rate limiting temporarily prevents obtaining normal response results.
- Sending the same question multiple times in requests can also temporarily prevent obtaining normal response results.
- Some regions may require additional cookie values besides __Secure-1PSID; refer to the issue page.
- Using this package for real-world applications is highly inappropriate. Due to rate limiting and variable API policies, it will only function temporarily.
- If the time interval between requests is very short, the Google API process may interpret it as performing a large number of requests and may not return normal responses.
- All these policies are subject to change, and the interface is also variable.
- The reason this Gemini API's method names do not follow the typical inference format of general LLMs is to prevent confusion with the official API. This Python package merely serves as an unofficial API to fetch responses from Gemini's website, so please do not be mistaken.

<br>



### #01. Response Error
```python
```

The error you're experiencing isn't originating from the package itself; it's related to your Google account and may be due to various factors like your country or region settings, which can prevent you from receiving accurate results from Gemini. Therefore, it's beyond the scope of the package to resolve, but please consider checking the following:

1. First, thoroughly read the readme and see if it pertains to cases of temporary abnormal responses from the package. Try again after some time or a few hours: [Before using Gemini API](https://github.com/dsdanielpark/Gemini-API/blob/main/README.md)
2. Bypass proxies: [Behind a proxy](https://github.com/dsdanielpark/Gemini-API#behind-a-proxy)
3. Try using an account from a different region or change the language settings of your Google account.
4. Restart your browser to refresh the cookie values and use the new __Secure-1PSID.
5. Try passing three or more cookies using [Multi-cookie Gemini](https://github.com/dsdanielpark/Gemini-API/blob/main/documents/README_DEV.md). If that doesn't work, consider passing almost all cookie values.

Please let me know if you need further assistance.

***

### #02. Response Status is 429

```
Exception: Response status code is not 200. Response Status is 429
```

Both are not package-related issues and are unsolvable problems. It is recommended to work around them as much as possible. This is a problem at the level of Google's API, and while it would take a long time to develop software to work around it, even assuming that it could be developed, it is not worth developing because it is easily blocked. There are no plans to update it further. There is no package-level solution to prevent captcha or HTTP 429 errors other than efforts such as bypassing readme and proxy, and creating a time interval between requests to avoid rate limiting.
- `CAPTCHA`: a program or system intended to distinguish human from machine input, typically as a way of [thwarting](https://www.google.com/search?sca_esv=573532060&sxsrf=AM9HkKmd5Faz1q0x4sLsgIG3VgVR9V18iA:1697335053753&q=thwarting&si=ALGXSlbSiMNWMsv5Y0U_0sBS8EWzwSlNZdPczeDdDqrhgxYO86hMDzIqBVTJp6ZKxKdXeVsCSihVIJAH_MROqwPM7RtQB0OoEA%3D%3D&expnd=1) spam and automated extraction of data from websites.
- `The HTTP 429`: Too Many Requests response status code indicates the user has sent too many requests in a given amount of time ("rate limiting")

***

### #03. Google RotateCookies
- With the change from bard to gemini, cookie values are refreshed and patched with every response. Therefore, it's necessary to automatically set new cookies for each request.
