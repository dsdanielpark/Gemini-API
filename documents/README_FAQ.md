Development Status :: 3 - Alpha

# FAQ
Cookie values may only be valid for a limited time (approximately 15-20 minutes and may be subject to rate limiting even sooner). Again, it's challenging to implement this in official services. Also, this is not an official Google package, and its availability for future use is uncertain.

## Before using the Gemini API
- Google Gemini can return different responses based on various factors such as account, country, region, IP, etc., following Google's policies. It cannot be resolved at the package level. (e.g., [CAPTCHA](https://en.wikipedia.org/wiki/CAPTCHA) or [HTTP 429 error](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429))
- The cookie values for this service is unofficial. Additionally, exposing it can allow others to easily use the Gemini service with your Google ID, so never expose it.
- This service has very limited and variable call limits per unit of time, and exceeding rate limiting temporarily prevents obtaining normal response results.
- Sending the same question multiple times in requests can also temporarily prevent obtaining normal response results.
- Some regions may require additional cookie values besides __Secure-1PSID; refer to the issue page.
- The __Secure-1PSID cookie value may change frequently. Logout, restart your web browser, and enter the new __Secure-1PSID cookie value.
- Using this package for real-world applications is highly inappropriate. Due to rate limiting and variable API policies, it will only function temporarily.
- If the time interval between requests is very short, the Google API process may interpret it as performing a large number of requests and may not return normal responses.
- All these policies are subject to change, and the interface is also variable.
- The reason this Gemini API's method names do not follow the typical inference format of general LLMs is to prevent confusion with the official API. This Python package merely serves as an unofficial API to fetch responses from Gemini's website, so please do not be mistaken.
- The official API format for Gemini will likely be as follows.

<br>

***

### Q: Why is the package structure so messy and unorganized like this?

### A: While rapidly adapting to Google's interface changes, various unexpected features were added, causing the structure to become messy. This package is not intended for providing stable services, and it may become unusable at any time based on Google's decisions, so it hasn't been heavily optimized. It would be advisable to use it temporarily for testing purposes only.

[#263](https://github.com/dsdanielpark/Gemini-API/discussions/267)

Originally, Gemini had very simple functionality as it was meant for experimental purposes. It used to fetch only a single response through a single cookie even in the 'get_answer' function. However, various additional features were added to Gemini over time, such as uploading images, fetching image links, or executing code, among others. The Gemini API package was developed quickly in Python to implement these features and perform lightweight testing.

In other words, the package initially lacked these diverse functionalities, and as unexpected features were added, the focus was solely on getting the functionality to work. This resulted in a messy package structure and less-than-clean code.

Additionally, implementing asynchronous functionality did not provide significant benefits, but it was added upon the requests of some developers to quickly implement the features. It was discovered that some users needed more than one cookie, so the goal was to implement these functionalities within the existing structure in the shortest possible time.

Overall, it was difficult to predict the interface or structure, and this package was created primarily for temporary and lightweight prototyping, as it was not meant for providing a stable service.

Therefore, it is very messy and not optimized, and this continues to be a major concern. The package's functionality may stop working at any time due to changes in Google's interface decisions.

Furthermore, adapting to new features or removing them is not straightforward. I feel a great responsibility for providing developers with unoptimized code that has caused inefficiencies, but developing a new package to address this issue has been challenging given the uncertainty of when the functionality might come to an end.

Nevertheless, I am making efforts to revise the package structure whenever possible. Your understanding is appreciated.

***

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
