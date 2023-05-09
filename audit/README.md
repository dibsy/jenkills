# Groovy Script Console Snippets

- We can run these automation scripts remotely and periodically to get report of the Jenkins Security / Implemented Best Practices



### Usage
``` bash
curl --data-urlencode "script=$(< ./list-global-credentials.groovy)" http://USERNAME:TOKEN@SERVER:PORT/scriptText
curl --data-urlencode "script=$(< ./list-global-credentials.groovy)" http://myuser:XXXXXX8XX@34.227.160.66:8080/scriptText


dd0f4c9e-01dc-47c3-a0cd-3fff32e2a6cd has scope GLOBAL
3b258e73-5e16-4338-883e-7a24927aefe1 has scope GLOBAL
8ada641e-429c-4547-9921-a1581dbf86ef has scope GLOBAL
github-token has scope GLOBAL

```

### References
- https://www.jenkins.io/doc/book/managing/script-console/
